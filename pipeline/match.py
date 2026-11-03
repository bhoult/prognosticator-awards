"""Matching-run driver (runs/match/PLAN.md). All state is on disk under work/match/<run>/.

    python -I pipeline/match.py concepts-plan <run>           sample tranche A, write the propose prompts
    python -I pipeline/match.py concepts-ingest <run>         check the proposals
    python -I pipeline/match.py consolidate-plan <run>        group proposals by domain, write prompts
    python -I pipeline/match.py consolidate-ingest <run>      check the consolidated lists
    python -I pipeline/match.py global-plan <run>             all domains' concepts, for the cross-domain pass
    python -I pipeline/match.py audit-plan <run>              cross-domain merges and large concepts, for the audit
    python -I pipeline/match.py concepts-build <run>          registry + mapping + checkpoint 1 -> runs/match/
    python -I pipeline/match.py match-plan <run> [n]          claim up to n pending matching batches, print their prompts
    python -I pipeline/match.py match-ingest <run>            check the matching outputs, summary
    python -I pipeline/match.py log <run> <agent> <stage> <tokens> <tool_uses> <seconds> [note]
    python -I pipeline/match.py status <run>

Subagents can't be started from Python. The orchestrating Claude Code session starts one
subagent per prompt file a *-plan command prints ("Read <file> and follow its instructions"),
and records its usage with `log`. A subagent writes its output file as it goes; the *-ingest
commands check what is there, and a stage's plan command lists only the prompts whose output
is missing or invalid, so a stopped run restarts where it was.

Inputs: work/match/<run>/claims.jsonl from pipeline/export_claims.py, and the computing
pilot's concepts (pilot/computing/concepts2.jsonl) as the seed of the registry.
"""
import collections
import hashlib
import json
import math
import os
import random
import re
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROMPTS = os.path.join(ROOT, 'prompts')
SEED_CONCEPTS = os.path.join(ROOT, 'pilot', 'computing', 'concepts2.jsonl')
OUT = os.path.join(ROOT, 'runs', 'match')
SEED, SAMPLE, SHARD = 2026, 0.25, 2500
# domains consolidated together because their samples are small
GROUPS = {'environment': 'environment+energy', 'energy': 'environment+energy',
          'computing': 'computing+economy+society-politics', 'economy': 'computing+economy+society-politics',
          'society-politics': 'computing+economy+society-politics'}
TYPES, GUESSES = {'technology', 'event', 'social'}, {'yes', 'no', 'unsure'}
KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def sha(data):
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def write_atomic(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + '.part', 'w', encoding='utf-8') as f:
        f.write(text)
    os.replace(path + '.part', path)


def jsonl(rows):
    return ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows)


def read_jsonl(path):
    """Rows of a JSON-lines file, or (None, error) if a line doesn't parse."""
    rows = []
    with open(path, encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    return None, f'line {n}: {e}'
    return rows, None


def rd(run, *p):
    return os.path.join(ROOT, 'work', 'match', run, *p)


def rel(path):
    return os.path.relpath(path, ROOT)


def claims(run):
    return [json.loads(l) for l in open(rd(run, 'claims.jsonl'), encoding='utf-8')]


def seed_registry():
    return [{'concept_id': c['concept_id'], 'name': c['name'], 'definition': c['definition']}
            for c in map(json.loads, open(SEED_CONCEPTS, encoding='utf-8'))]


def config(run, stage, settings):
    """Record a stage's settings; refuse to continue under different ones."""
    path = rd(run, stage, 'config.json')
    if os.path.exists(path):
        old = json.load(open(path, encoding='utf-8'))
        if old != settings:
            sys.exit(f'{rel(path)} has other settings: {old} (now {settings})')
    else:
        write_atomic(path, json.dumps(settings, indent=1) + '\n')


def prompt(run, stage, name, template, **fields):
    text = open(os.path.join(PROMPTS, template), encoding='utf-8').read()
    for k, v in fields.items():
        text = text.replace('{' + k + '}', str(v))
    path = rd(run, stage, 'prompts', name + '.md')
    write_atomic(path, text)
    return path


# ---- concepts: propose ----

def concepts_plan(run):
    stage = 'concepts'
    tpl = open(os.path.join(PROMPTS, 'concepts_propose.md'), encoding='utf-8').read()
    config(run, stage, {'tranche': 'A', 'sample': SAMPLE, 'shard': SHARD, 'seed': SEED,
                        'claims_sha256': sha(open(rd(run, 'claims.jsonl'), 'rb').read()),
                        'prompt_sha256': sha(tpl), 'seed_concepts_sha256': sha(open(SEED_CONCEPTS, 'rb').read())})
    write_atomic(rd(run, stage, 'registry_seed.jsonl'), jsonl(seed_registry()))
    by = collections.defaultdict(list)
    for c in claims(run):
        if c['tranche'] == 'A':
            by[c['domain']].append(c)
    todo = []
    for dom in sorted(by):
        rows = sorted(by[dom], key=lambda c: c['id'])
        pick = random.Random(f'{SEED}:{dom}').sample(rows, round(len(rows) * SAMPLE))
        n = max(1, math.ceil(len(pick) / SHARD))
        for i in range(n):
            name = f'{dom}-{i + 1}'
            part = pick[i::n]
            write_atomic(rd(run, stage, 'in', name + '.jsonl'),
                         jsonl({'id': c['id'], 'description': c['description']} for c in part))
            out = rd(run, stage, 'out', name + '.jsonl')
            if propose_problems(run, name) is None:
                continue
            todo.append(prompt(run, stage, 'propose-' + name, 'concepts_propose.md', workdir=ROOT, domain=dom,
                               n=len(part), shard_in=rel(rd(run, stage, 'in', name + '.jsonl')),
                               registry=rel(rd(run, stage, 'registry_seed.jsonl')), shard_out=rel(out)))
    print(len(todo), 'propose prompts to run:')
    for p in todo:
        print(' ', rel(p))


def propose_problems(run, name):
    """None if the shard's output is complete and valid, else a list of problems."""
    out = rd(run, 'concepts', 'out', name + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    ids = {json.loads(l)['id'] for l in open(rd(run, 'concepts', 'in', name + '.jsonl'), encoding='utf-8')}
    bad, seen = [], set()
    for r in rows:
        cid = r.get('concept_id', '')
        if not KEBAB.match(str(cid)) or cid in seen:
            bad.append(f'bad or repeated id {cid!r}')
        seen.add(cid)
        if not str(r.get('definition', '')).strip() or not str(r.get('name', '')).strip():
            bad.append(f'{cid}: no name or definition')
        if r.get('type') not in TYPES or r.get('came_true_guess') not in GUESSES:
            bad.append(f'{cid}: type or came_true_guess')
    if not rows:
        bad.append('empty')
    return bad or None


def concepts_ingest(run):
    total = 0
    for f in sorted(os.listdir(rd(run, 'concepts', 'in'))):
        name = f[:-6]
        n_in = sum(1 for _ in open(rd(run, 'concepts', 'in', f), encoding='utf-8'))
        p = propose_problems(run, name)
        if p:
            print(f'{name}: {n_in} claims; NOT DONE: {p[:5]}')
            continue
        rows = read_jsonl(rd(run, 'concepts', 'out', f))[0]
        ids = {json.loads(l)['id'] for l in open(rd(run, 'concepts', 'in', f), encoding='utf-8')}
        stray = sum(1 for r in rows for e in r.get('examples') or [] if e not in ids)
        est = sum(int(r.get('est_claims') or 0) for r in rows)
        total += len(rows)
        print(f'{name}: {n_in} claims, {len(rows)} concepts, est. coverage {est / n_in:.0%}, '
              f'types {dict(collections.Counter(r["type"] for r in rows))}' + (f'; {stray} example ids not in the shard (dropped)' if stray else ''))
    print(total, 'concepts proposed')


# ---- concepts: consolidate per domain group ----

def consolidate_plan(run):
    stage = 'consolidate'
    tpl = open(os.path.join(PROMPTS, 'concepts_consolidate.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'groups': GROUPS})
    groups = collections.defaultdict(list)
    for f in sorted(os.listdir(rd(run, 'concepts', 'in'))):
        name = f[:-6]
        if propose_problems(run, name):
            sys.exit(f'proposals for {name} are not done; run concepts-ingest')
        dom = name.rsplit('-', 1)[0]
        ids = {json.loads(l)['id'] for l in open(rd(run, 'concepts', 'in', f), encoding='utf-8')}
        for r in read_jsonl(rd(run, 'concepts', 'out', f))[0]:
            r['examples'] = [e for e in r.get('examples') or [] if e in ids]  # examples are only hints
            groups[GROUPS.get(dom, dom)].append({'shard': name, **r})
    todo = []
    for g, rows in sorted(groups.items()):
        write_atomic(rd(run, stage, 'in', g + '.jsonl'), jsonl(rows))
        if consolidate_problems(run, g) is None:
            continue
        todo.append(prompt(run, stage, 'consolidate-' + g, 'concepts_consolidate.md', workdir=ROOT, domain=g,
                           proposals=rel(rd(run, stage, 'in', g + '.jsonl')),
                           registry=rel(rd(run, 'concepts', 'registry_seed.jsonl')),
                           out=rel(rd(run, stage, 'out', g + '.jsonl')), tmpdir=rel(rd(run, 'tmp', 'consolidate-' + g))))
    print(len(todo), 'consolidate prompts to run:')
    for p in todo:
        print(' ', rel(p))


def consolidate_problems(run, g):
    out = rd(run, 'consolidate', 'out', g + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    props = {f"{r['shard']}:{r['concept_id']}" for r in map(json.loads, open(rd(run, 'consolidate', 'in', g + '.jsonl'), encoding='utf-8'))}
    seed = {c['concept_id'] for c in seed_registry()}
    bad, seen, covered = [], set(), set()
    for r in rows:
        if 'dropped' in r:
            covered.add(r['dropped'])
            continue
        cid = r.get('concept_id', '')
        covered |= set(r.get('merged_from') or []) | set(r.get('split_from') or [])
        if r.get('existing'):
            if cid not in seed:
                bad.append(f'{cid}: marked existing but not in the registry')
            continue
        if not KEBAB.match(str(cid)) or cid in seen or cid in seed:
            bad.append(f'bad, repeated or existing id {cid!r}')
        seen.add(cid)
        if r.get('type') not in TYPES or r.get('came_true_guess') not in GUESSES or not str(r.get('definition', '')).strip():
            bad.append(f'{cid}: type, guess or definition')
    missing = props - covered
    if missing:
        bad.append(f'{len(missing)} proposals not accounted for, e.g. {sorted(missing)[:3]}')
    return bad or None


def consolidate_ingest(run):
    for f in sorted(os.listdir(rd(run, 'consolidate', 'in'))):
        g = f[:-6]
        n_in = sum(1 for _ in open(rd(run, 'consolidate', 'in', f), encoding='utf-8'))
        p = consolidate_problems(run, g)
        if p:
            print(f'{g}: {n_in} proposals; NOT DONE: {p[:5]}')
            continue
        rows = read_jsonl(rd(run, 'consolidate', 'out', f))[0]
        kept = [r for r in rows if 'dropped' not in r and not r.get('existing')]
        print(f'{g}: {n_in} proposals -> {len(kept)} concepts, {sum(1 for r in rows if r.get("existing"))} to existing, '
              f'{sum(1 for r in rows if "dropped" in r)} dropped, {sum(1 for r in kept if r.get("split_from"))} from splits, '
              f'{sum(1 for r in kept if r.get("bundle_check", "ok") != "ok")} bundle notes')


# ---- concepts: across domains, then the registry ----

def consolidated(run):
    rows = []
    for f in sorted(os.listdir(rd(run, 'consolidate', 'in'))):
        g = f[:-6]
        if consolidate_problems(run, g):
            sys.exit(f'consolidation of {g} is not done; run consolidate-ingest')
        rows += [{'group': g, **r} for r in read_jsonl(rd(run, 'consolidate', 'out', f))[0]]
    return rows


def global_plan(run):
    stage = 'global'
    tpl = open(os.path.join(PROMPTS, 'concepts_global.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl)})
    seed = [{**c, 'domains': ['computing'], 'est_claims': None} for c in seed_registry()]
    new = [{k: r.get(k) for k in ('concept_id', 'name', 'definition', 'domains', 'est_claims')}
           for r in consolidated(run) if 'dropped' not in r and not r.get('existing')]
    write_atomic(rd(run, stage, 'in', 'concepts.jsonl'), jsonl(seed + new))
    out = rd(run, stage, 'out', 'merges.jsonl')
    if os.path.exists(out) and read_jsonl(out)[0] is not None:
        print('done:', rel(out))
        return
    print(rel(prompt(run, stage, 'global', 'concepts_global.md', workdir=ROOT,
                     concepts=rel(rd(run, stage, 'in', 'concepts.jsonl')), out=rel(out), tmpdir=rel(rd(run, 'tmp', 'global')))))


def audit_rows(run):
    path = rd(run, 'audit', 'out', 'review.jsonl')
    if not os.path.exists(path):
        return []
    rows, err = read_jsonl(path)
    if rows is None:
        sys.exit(f'audit: {err}')
    return rows


def registry(run, audit=True):
    """(concepts, mapping, merges, audit decisions): the consolidated lists, merged across
    domains, with the audit's decisions (raw/audit/out/review.jsonl) applied if `audit`."""
    review = audit_rows(run) if audit else []
    keep_apart = {(r['keep'], d) for r in review if r['op'] == 'reject_merge' for d in r['drop']}
    reg = {}
    for c in map(json.loads, open(SEED_CONCEPTS, encoding='utf-8')):
        reg[c['concept_id']] = {'concept_id': c['concept_id'], 'name': c['name'], 'definition': c['definition'],
                                'type': 'technology', 'domains': ['computing'], 'aliases': c.get('aliases', []),
                                'wikidata': c.get('wikidata'), 'came_true_guess': 'yes' if c.get('realizable') else 'unsure',
                                'est_claims': None, 'examples': [], 'source': 'computing pilot', 'bundle_check': 'ok'}
    mapping = []
    for r in consolidated(run):
        if 'dropped' in r:
            mapping.append({'proposal': r['dropped'], 'concept_id': None, 'how': 'dropped', 'reason': r.get('reason', '')})
            continue
        for p in r.get('merged_from') or []:
            mapping.append({'proposal': p, 'concept_id': r['concept_id'], 'how': 'existing' if r.get('existing') else 'merged'})
        for p in r.get('split_from') or []:
            mapping.append({'proposal': p, 'concept_id': r['concept_id'], 'how': 'split'})
        if r.get('existing'):
            continue
        new = {k: r.get(k) for k in ('concept_id', 'name', 'definition', 'type', 'domains', 'aliases',
                                     'came_true_guess', 'est_claims', 'examples', 'bundle_check')}
        new.update(wikidata=None, source=r['group'],
                   domains=sorted({d for g in (r.get('domains') or [r['group']]) for d in g.split('+')}))
        old = reg.get(r['concept_id'])
        if old:  # the same id from two domain groups: one concept; keep the definition with more claims
            if (new['est_claims'] or 0) > (old['est_claims'] or 0):
                old, new = new, old
            old['domains'] = sorted(set(old['domains']) | set(new['domains']))
            old['aliases'] = sorted(set(old['aliases'] or []) | set(new['aliases'] or []))
            old['est_claims'] = (old['est_claims'] or 0) + (new['est_claims'] or 0)
            old['examples'] = (old['examples'] or []) + (new['examples'] or [])
            old['source'] = '+'.join(sorted(set(old['source'].split('+')) | {new['source']}))
            new = old
        reg[r['concept_id']] = new
    merges, err = read_jsonl(rd(run, 'global', 'out', 'merges.jsonl'))
    if merges is None:
        sys.exit(f'global merges: {err}')
    merges = [{**m, 'drop': [d for d in m['drop'] if (m['keep'], d) not in keep_apart]} for m in merges]
    merges = [m for m in merges if m['drop']]
    gone = {}
    for m in merges:
        k = m['keep']
        while k in gone:  # kept here, but dropped by an earlier group
            k = gone[k]
        if k not in reg:
            sys.exit(f'global merge keeps unknown {k}')
        for d in m['drop']:
            if d == k or d in gone:
                continue
            if d not in reg:
                sys.exit(f'global merge drops unknown {d}')
            c = reg.pop(d)
            reg[k]['domains'] = sorted(set(reg[k]['domains']) | set(c['domains'] or []))
            reg[k]['aliases'] = sorted(set(reg[k]['aliases'] or []) | set(c['aliases'] or []) | {c['name']})
            reg[k]['est_claims'] = (reg[k]['est_claims'] or 0) + (c['est_claims'] or 0) or None
            reg[k]['examples'] = (reg[k]['examples'] or []) + (c['examples'] or [])
            gone[d] = k
    for m in mapping:
        while m['concept_id'] in gone:
            m['concept_id'], m['how'] = gone[m['concept_id']], m['how'] + '+global'
    for r in review:
        if r['op'] != 'split':
            continue
        cid = r['concept_id']
        while cid in gone:
            cid = gone[cid]
        old = reg.pop(cid, None)
        if old is None:
            sys.exit(f'audit splits unknown {r["concept_id"]}')
        for n in r['into']:
            if n['concept_id'] in reg or not KEBAB.match(n['concept_id']) or n.get('type') not in TYPES \
                    or n.get('came_true_guess') not in GUESSES:
                sys.exit(f'audit split of {cid}: bad or existing id {n["concept_id"]}')
            reg[n['concept_id']] = {**old, **{k: n[k] for k in ('concept_id', 'name', 'definition', 'type', 'came_true_guess')},
                                    'est_claims': None, 'examples': [], 'bundle_check': 'ok', 'split_by_audit': cid}
            gone.setdefault(cid, n['concept_id'])
        for m in mapping:
            if m['concept_id'] == cid:
                m['concept_id'], m['how'] = None, m['how'] + '+audit-split'
    # reviewer decisions (runs/match/concept_review.jsonl): merges after the audit's splits
    for r in reviewer_rows() if audit else []:
        if r['op'] != 'merge':
            continue
        k = r['keep']
        for d in r['drop']:
            if k not in reg or d not in reg:
                sys.exit(f'review merge: unknown {k} or {d}')
            c = reg.pop(d)
            reg[k]['domains'] = sorted(set(reg[k]['domains']) | set(c['domains'] or []))
            reg[k]['aliases'] = sorted(set(reg[k]['aliases'] or []) | set(c['aliases'] or []) | {c['name']})
        review = review + [r]
    return sorted(reg.values(), key=lambda c: c['concept_id']), mapping, merges, review


def reviewer_rows():
    path = os.path.join(OUT, 'concept_review.jsonl')
    return [json.loads(l) for l in open(path, encoding='utf-8') if l.strip()] if os.path.exists(path) else []


def audit_plan(run):
    stage = 'audit'
    tpl = open(os.path.join(PROMPTS, 'concepts_audit.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'largest': 200})
    rows, _, merges, _ = registry(run, audit=False)
    defs = {}
    for c in map(json.loads, open(rd(run, 'global', 'in', 'concepts.jsonl'), encoding='utf-8')):
        defs.setdefault(c['concept_id'], {k: c[k] for k in ('concept_id', 'name', 'definition')})
    write_atomic(rd(run, stage, 'in', 'merges.jsonl'),
                 jsonl({'keep': defs[m['keep']], 'drop': [defs[d] for d in m['drop'] if d in defs]} for m in merges))
    big = sorted((c for c in rows if c.get('est_claims')), key=lambda c: -c['est_claims'])[:200]
    pick = {c['concept_id'] for c in big} | {c['concept_id'] for c in rows if (c.get('bundle_check') or 'ok') != 'ok'}
    write_atomic(rd(run, stage, 'in', 'concepts.jsonl'),
                 jsonl({k: c.get(k) for k in ('concept_id', 'name', 'definition', 'est_claims', 'bundle_check')}
                       for c in rows if c['concept_id'] in pick))
    out = rd(run, stage, 'out', 'review.jsonl')
    print(len(merges), 'merges and', len(pick), 'concepts to audit;',
          rel(prompt(run, stage, 'audit', 'concepts_audit.md', workdir=ROOT, merges=rel(rd(run, stage, 'in', 'merges.jsonl')),
                     concepts=rel(rd(run, stage, 'in', 'concepts.jsonl')), out=rel(out), tmpdir=rel(rd(run, 'tmp', 'audit')))))


def concepts_build(run):
    """runs/match/concepts.jsonl (the registry), concept_mapping.jsonl (proposal -> concept) and
    checkpoint1.md (what the user reviews before matching)."""
    rows, mapping, merges, review = registry(run)
    write_atomic(os.path.join(OUT, 'concepts.jsonl'), jsonl(rows))
    write_atomic(os.path.join(OUT, 'concept_mapping.jsonl'), jsonl(mapping))
    write_atomic(os.path.join(OUT, 'checkpoint1.md'), checkpoint1(rows, mapping, merges, review))
    print(len(rows), 'concepts ->', rel(os.path.join(OUT, 'concepts.jsonl')), '; checkpoint1.md written')


def checkpoint1(rows, mapping, merges, review):
    cell = lambda s: str(s or '').replace('|', '/').replace('\n', ' ')  # noqa: E731
    dom = collections.Counter(d for c in rows for d in (c['domains'] or []))
    out = ['# Checkpoint 1: the concept registry (tranche A)', '',
           f'{len(rows)} concepts. Matching does not start until this is approved (runs/match/PLAN.md §3).', '',
           '| Domain | Concepts |', '|---|---|'] + [f'| {d} | {n} |' for d, n in dom.most_common()]
    out += ['', '| Type | Concepts |', '|---|---|'] + [f'| {t} | {n} |' for t, n in collections.Counter(c['type'] for c in rows).most_common()]
    out += ['', '| Came true (guess) | Concepts |', '|---|---|'] + [f'| {t} | {n} |' for t, n in collections.Counter(c['came_true_guess'] for c in rows).most_common()]
    big = sorted((c for c in rows if c['est_claims']), key=lambda c: -c['est_claims'])[:50]
    out += ['', '## The 50 largest (estimated claims in the 25% sample)', '', '| Concept | Est. | Came true? | Definition |', '|---|---|---|---|']
    out += [f"| {c['concept_id']} | {c['est_claims']} | {c['came_true_guess']} | {cell(c['definition'])} |" for c in big]
    split = [m for m in mapping if m['how'].startswith('split')]
    out += ['', f'## Splits ({len(split)} proposals split)', '', '| Proposal | Became |', '|---|---|']
    by = collections.defaultdict(list)
    for m in split:
        by[m['proposal']].append(m['concept_id'])
    out += [f"| {p} | {', '.join(x or '(split again by the audit)' for x in v)} |" for p, v in sorted(by.items())]
    notes = [c for c in rows if (c.get('bundle_check') or 'ok') != 'ok']
    out += ['', f'## Possible bundles kept ({len(notes)})', '', '| Concept | Note | Definition |', '|---|---|---|']
    out += [f"| {c['concept_id']} | {cell(c['bundle_check'])} | {cell(c['definition'])} |" for c in notes]
    out += ['', f'## Merged across domains ({len(merges)} groups)', '', '| Kept | Dropped | Why |', '|---|---|---|']
    out += [f"| {m['keep']} | {', '.join(m['drop'])} | {cell(m.get('reason'))} |" for m in merges]
    rej = [r for r in review if r['op'] == 'reject_merge']
    out += ['', f'## Cross-domain merges the audit rejected ({len(rej)})', '', '| Kept | Kept apart | Why |', '|---|---|---|']
    out += [f"| {r['keep']} | {', '.join(r['drop'])} | {cell(r.get('reason'))} |" for r in rej]
    spl = [r for r in review if r['op'] == 'split']
    out += ['', f'## Concepts the audit split ({len(spl)})', '', '| Concept | Into | Why |', '|---|---|---|']
    out += [f"| {r['concept_id']} | {', '.join(n['concept_id'] for n in r['into'])} | {cell(r.get('reason'))} |" for r in spl]
    mer = [r for r in review if r['op'] == 'merge']
    out += ['', f'## Reviewer merges ({len(mer)})', '', '| Kept | Merged into it | Why |', '|---|---|---|']
    out += [f"| {r['keep']} | {', '.join(r['drop'])} | {cell(r.get('reason'))} |" for r in mer]
    drop = [m for m in mapping if m['how'] == 'dropped']
    out += ['', f'## Proposals dropped ({len(drop)})', '', '| Proposal | Why |', '|---|---|']
    out += [f"| {m['proposal']} | {cell(m['reason'])} |" for m in drop]
    return '\n'.join(out) + '\n'


# ---- matching ----

BATCH, CLAIM_MINUTES = 350, 60
CODES = {'no_concept', 'untestable', 'too_vague'}


def registry_rows():
    return [json.loads(l) for l in open(os.path.join(OUT, 'concepts.jsonl'), encoding='utf-8')]


def match_batches(run):
    """Fixed once: tranche A claims by domain, shuffled with a fixed seed, about BATCH per batch."""
    path = rd(run, 'match', 'batches.json')
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    by = collections.defaultdict(list)
    for c in claims(run):
        if c['tranche'] == 'A':
            by[c['domain']].append(c['id'])
    batches = {}
    for dom in sorted(by):
        ids = sorted(by[dom])
        random.Random(f'{SEED}:match:{dom}').shuffle(ids)
        n = math.ceil(len(ids) / BATCH)
        for i in range(n):
            batches[f'{dom}-{i + 1:03d}'] = {'domain': dom, 'ids': ids[i::n]}
    write_atomic(path, json.dumps(batches))
    return batches


def match_plan(run, limit=None):
    """Write the inputs and prompts of the batches with no valid output, and claim up to `limit`
    of them (printing their prompts) so that a later call doesn't hand them out again."""
    stage = 'match'
    tpl = open(os.path.join(PROMPTS, 'match.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'batch': BATCH, 'seed': SEED,
                        'claims_sha256': sha(open(rd(run, 'claims.jsonl'), 'rb').read()),
                        'registry_sha256': sha(open(os.path.join(OUT, 'concepts.jsonl'), 'rb').read())})
    batches = match_batches(run)
    reg = registry_rows()
    for dom in sorted({b['domain'] for b in batches.values()}):
        write_atomic(rd(run, stage, 'registry', dom + '.jsonl'),
                     jsonl({k: c[k] for k in ('concept_id', 'name', 'definition')} for c in reg if dom in (c['domains'] or [])))
    by_id = None
    todo, now = [], time.time()
    for name, b in batches.items():
        inp = rd(run, stage, 'in', name + '.jsonl')
        if not os.path.exists(inp):
            if by_id is None:
                by_id = {c['id']: c for c in claims(run)}
            write_atomic(inp, jsonl({k: by_id[i][k] for k in ('id', 'quote', 'description')} for i in b['ids']))
        if match_problems(run, name) is None:
            continue
        mark = rd(run, stage, 'prompts', name + '.claimed')
        if os.path.exists(mark) and now - os.path.getmtime(mark) < CLAIM_MINUTES * 60:
            continue
        todo.append(name)
    todo.sort(key=lambda n: (int(n.rsplit('-', 1)[1]), n))  # in turn across domains
    pick = todo[:int(limit)] if limit else todo
    for name in pick:
        b = batches[name]
        path = prompt(run, stage, name, 'match.md', workdir=ROOT, domain=b['domain'], n=len(b['ids']),
                      half=(len(b['ids']) + 1) // 2, registry=rel(rd(run, stage, 'registry', b['domain'] + '.jsonl')),
                      batch_in=rel(rd(run, stage, 'in', name + '.jsonl')), batch_out=rel(rd(run, stage, 'out', name + '.jsonl')),
                      tmpdir=rel(rd(run, 'tmp', 'match-' + name)))
        write_atomic(rd(run, stage, 'prompts', name + '.claimed'), time.strftime('%Y-%m-%dT%H:%M:%S\n'))
        print(rel(path))
    print(f'{len(pick)} claimed; {len(todo) - len(pick)} more pending; {len(batches)} batches in all', file=sys.stderr)


def match_problems(run, name):
    out = rd(run, 'match', 'out', name + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    ids = [json.loads(l)['id'] for l in open(rd(run, 'match', 'in', name + '.jsonl'), encoding='utf-8')]
    if [r.get('id') for r in rows] != ids:
        return [f'{len(rows)} rows for {len(ids)} claims, or not in input order']
    known = {c['concept_id'] for c in registry_rows()}
    bad = []
    for r in rows:
        cs = r.get('concepts')
        if not isinstance(cs, list) or len(cs) > 2 or any(c not in known for c in cs):
            bad.append(f"{r['id']}: concepts {cs}")
        elif bool(cs) == (r.get('code') in CODES) or (not cs and r.get('code') not in CODES):
            bad.append(f"{r['id']}: code {r.get('code')!r} with concepts {cs}")
        if not isinstance(r.get('quote_carries'), bool) or not str(r.get('reason', '')).strip():
            bad.append(f"{r['id']}: quote_carries or reason")
    top = collections.Counter(r.get('reason') for r in rows).most_common(1)
    if top and top[0][1] > len(rows) * 0.2:
        bad.append(f'{top[0][1]} identical reasons: {top[0][0]!r}')
    return bad or None


def match_ingest(run):
    batches = match_batches(run)
    done, rows, notdone = 0, [], []
    for name in batches:
        p = match_problems(run, name)
        if p is None:
            done += 1
            rows += read_jsonl(rd(run, 'match', 'out', name + '.jsonl'))[0]
        elif p != ['missing']:
            notdone.append((name, p[:3]))
    for name, p in notdone:
        print(f'{name}: INVALID {p}')
    if rows:
        n = len(rows)
        m = sum(1 for r in rows if r['concepts'])
        print(f"{done} of {len(batches)} batches done: {n} claims, {m / n:.0%} matched, "
              f"{sum(1 for r in rows if len(r['concepts']) == 2) / n:.0%} to two concepts, "
              f"codes {dict(collections.Counter(r['code'] for r in rows if r['code']))}, "
              f"quote alone doesn't carry it: {sum(1 for r in rows if not r['quote_carries']) / n:.0%}, "
              f"{len({c for r in rows for c in r['concepts']})} concepts used")


# ---- usage and status ----

def log(run, agent, stage, tokens, tools, seconds, *note):
    path = os.path.join(OUT, 'usage.tsv')
    if not os.path.exists(path):
        write_atomic(path, 'agent\tstage\tmodel\ttotal_tokens\ttool_uses\tseconds\tnote\n')
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\t'.join([agent, stage, 'sonnet', tokens, tools, seconds, ' '.join(note)]) + '\n')


def status(run):
    for stage in ('concepts', 'consolidate', 'global'):
        d = rd(run, stage, 'in')
        if os.path.isdir(d):
            names = [f[:-6] for f in sorted(os.listdir(d))]
            check = {'concepts': propose_problems, 'consolidate': consolidate_problems}.get(stage)
            done = sum(1 for n in names if check and check(run, n) is None) if check else \
                int(os.path.exists(rd(run, 'global', 'out', 'merges.jsonl')))
            print(f'{stage}: {done} of {len(names)} done')
    path = os.path.join(OUT, 'usage.tsv')
    if os.path.exists(path):
        rows = [l.split('\t') for l in open(path, encoding='utf-8').read().splitlines()[1:]]
        print(f'usage: {len(rows)} agents, {sum(int(r[3]) for r in rows):,} tokens')


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    {'concepts-plan': concepts_plan, 'concepts-ingest': concepts_ingest, 'consolidate-plan': consolidate_plan,
     'consolidate-ingest': consolidate_ingest, 'global-plan': global_plan, 'audit-plan': audit_plan,
     'concepts-build': concepts_build, 'match-plan': match_plan, 'match-ingest': match_ingest,
     'log': log, 'status': status}[cmd](*args)
