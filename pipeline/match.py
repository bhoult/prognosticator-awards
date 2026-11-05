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
    python -I pipeline/match.py rematch-plan <run> [n]        second pass: no_concept/too_vague claims vs the whole registry
    python -I pipeline/match.py matches-collect <run>         all passes -> work/match/<run>/matches.jsonl
    python -I pipeline/match.py gap-plan <run>                3c: propose concepts for the no_concept claims
    python -I pipeline/match.py gap-ingest <run>              check the gap proposals
    python -I pipeline/match.py gapcons-plan <run>            consolidate them per domain group against the approved registry
    python -I pipeline/match.py gapglobal-plan <run>          the new concepts of all groups, for the cross-group merges
    python -I pipeline/match.py gap-build <run>               -> runs/match/concepts_gap.jsonl + concept_gap_mapping.jsonl
    python -I pipeline/match.py gapmatch-plan <run> [n]       the no_concept claims vs the gap concepts
    python -I pipeline/match.py gap-review <run>              -> runs/match/gap_review.md (a stop before research)
    python -I pipeline/match.py agree-plan <run>              §4: a second agent re-matches 300 random claims
    python -I pipeline/match.py agree-report <run>            -> runs/match/agreement.md
    python -I pipeline/match.py research-plan <run> [n] [prefix]  §5 tier 1: claim up to n research batches, print their prompts
    python -I pipeline/match.py verify <run>                  check every source again -> runs/match/milestones.jsonl
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
import itertools
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


def propose_problems(run, name, stage='concepts'):
    """None if the shard's output is complete and valid, else a list of problems."""
    out = rd(run, stage, 'out', name + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
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


def concepts_ingest(run, stage='concepts'):
    total = 0
    for f in sorted(os.listdir(rd(run, stage, 'in'))):
        name = f[:-6]
        n_in = sum(1 for _ in open(rd(run, stage, 'in', f), encoding='utf-8'))
        p = propose_problems(run, name, stage)
        if p:
            print(f'{name}: {n_in} claims; NOT DONE: {p[:5]}')
            continue
        rows = read_jsonl(rd(run, stage, 'out', f))[0]
        ids = {json.loads(l)['id'] for l in open(rd(run, stage, 'in', f), encoding='utf-8')}
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


def as_list(v):
    """A provenance field: a list, or one id that an agent wrote as a bare string."""
    return [v] if isinstance(v, str) else list(v or [])


def consolidate_problems(run, g, stage='consolidate', known=None):
    """`known`: the concept ids a proposal may be mapped to as existing (default: the seed)."""
    out = rd(run, stage, 'out', g + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    props = {f"{r['shard']}:{r['concept_id']}" for r in map(json.loads, open(rd(run, stage, 'in', g + '.jsonl'), encoding='utf-8'))}
    seed = known if known is not None else {c['concept_id'] for c in seed_registry()}
    bad, seen, covered = [], set(), set()
    for r in rows:
        if 'dropped' in r:
            covered.add(r['dropped'])
            continue
        cid = r.get('concept_id', '')
        covered |= set(as_list(r.get('merged_from'))) | set(as_list(r.get('split_from')))
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


def main_registry():
    """The registry approved at checkpoint 1 (runs/match/concepts.jsonl)."""
    return [json.loads(l) for l in open(os.path.join(OUT, 'concepts.jsonl'), encoding='utf-8')]


def registry_rows():
    """Every concept: the approved registry and the gap pass's (runs/match/concepts_gap.jsonl)."""
    gap = os.path.join(OUT, 'concepts_gap.jsonl')
    return main_registry() + ([json.loads(l) for l in open(gap, encoding='utf-8')] if os.path.exists(gap) else [])


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


def match_problems(run, name, stage='match'):
    out = rd(run, stage, 'out', name + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    ids = [json.loads(l)['id'] for l in open(rd(run, stage, 'in', name + '.jsonl'), encoding='utf-8')]
    if [r.get('id') for r in rows] != ids:
        return [f'{len(rows)} rows for {len(ids)} claims, or not in input order']
    known = {c['concept_id'] for c in registry_rows()}
    bad = []
    for r in rows:
        cs = r.get('concepts')
        # more than two concepts is repaired at collection (the first two are kept, logged)
        if not isinstance(cs, list) or len(cs) > 3 or any(c not in known for c in cs):
            bad.append(f"{r['id']}: concepts {cs}")
        elif bool(cs) == (r.get('code') in CODES) or (not cs and r.get('code') not in CODES):
            bad.append(f"{r['id']}: code {r.get('code')!r} with concepts {cs}")
        if not isinstance(r.get('quote_carries'), bool) or not str(r.get('reason', '')).strip():
            bad.append(f"{r['id']}: quote_carries or reason")
    # first pass: template reasons matter for matches only, since unmatched claims are all retried in
    # the second pass; the second pass is final, so there every row counts
    top = collections.Counter(r.get('reason') for r in rows if r.get('concepts') or stage != 'match').most_common(1)
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


# ---- second pass: the leftovers against the whole registry ----

RETRY = {'no_concept', 'too_vague'}


def first_pass(run):
    """claim id -> first-pass row; exits if a first-pass batch is not done."""
    rows = {}
    for name in match_batches(run):
        if match_problems(run, name) is not None:
            sys.exit(f'first-pass batch {name} is not done')
        for r in read_jsonl(rd(run, 'match', 'out', name + '.jsonl'))[0]:
            rows[r['id']] = r
    return rows


def rematch_batches(run):
    path = rd(run, 'rematch', 'batches.json')
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    left = sorted(i for i, r in first_pass(run).items() if r['code'] in RETRY)
    random.Random(f'{SEED}:rematch').shuffle(left)
    n = math.ceil(len(left) / BATCH)
    batches = {f'rematch-{i + 1:03d}': {'ids': left[i::n]} for i in range(n)}
    write_atomic(path, json.dumps(batches))
    return batches


def rematch_plan(run, limit=None):
    """Like match-plan, for the claims the first pass coded no_concept or too_vague."""
    stage = 'rematch'
    tpl = open(os.path.join(PROMPTS, 'rematch.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'batch': BATCH, 'seed': SEED, 'retry': sorted(RETRY),
                        'registry_sha256': sha(open(os.path.join(OUT, 'concepts.jsonl'), 'rb').read())})
    reg = registry_rows()
    claim_batches(run, stage, rematch_batches(run), 'rematch.md', reg, limit)


def claim_batches(run, stage, batches, template, reg, limit=None):
    """Write the stage's registry and inputs, claim up to `limit` batches that aren't done or
    claimed in the last CLAIM_MINUTES, and print their prompts."""
    write_atomic(rd(run, stage, 'registry.jsonl'), jsonl({k: c[k] for k in ('concept_id', 'name', 'definition')} for c in reg))
    by_id, todo, now = None, [], time.time()
    for name, b in batches.items():
        inp = rd(run, stage, 'in', name + '.jsonl')
        if not os.path.exists(inp):
            if by_id is None:
                by_id = {c['id']: c for c in claims(run)}
            write_atomic(inp, jsonl({k: by_id[i][k] for k in ('id', 'quote', 'description')} for i in b['ids']))
        if match_problems(run, name, stage) is None:
            continue
        mark = rd(run, stage, 'prompts', name + '.claimed')
        if os.path.exists(mark) and now - os.path.getmtime(mark) < CLAIM_MINUTES * 60:
            continue
        todo.append(name)
    pick = todo[:int(limit)] if limit else todo
    for name in pick:
        n = len(batches[name]['ids'])
        path = prompt(run, stage, name, template, workdir=ROOT, domain='all', n=n, half=(n + 1) // 2,
                      n_concepts=len(reg), registry=rel(rd(run, stage, 'registry.jsonl')),
                      batch_in=rel(rd(run, stage, 'in', name + '.jsonl')), batch_out=rel(rd(run, stage, 'out', name + '.jsonl')),
                      tmpdir=rel(rd(run, 'tmp', stage + '-' + name)))
        write_atomic(rd(run, stage, 'prompts', name + '.claimed'), time.strftime('%Y-%m-%dT%H:%M:%S\n'))
        print(rel(path))
    print(f'{len(pick)} claimed; {len(todo) - len(pick)} more pending; {len(batches)} batches in all', file=sys.stderr)


def pass_rows(run, stage, batches):
    rows = {}
    for name in batches:
        if match_problems(run, name, stage) is not None:
            sys.exit(f'{stage} batch {name} is not done')
        for r in read_jsonl(rd(run, stage, 'out', name + '.jsonl'))[0]:
            rows[r['id']] = r
    return rows


def matches_collect(run):
    """work/match/<run>/matches.jsonl: one row per tranche-A claim, the first pass's answer, or the
    second pass's for claims it retried, or the gap pass's (3c) once it has run; more than two
    concepts are cut to the first two (logged)."""
    first = first_pass(run)
    second = pass_rows(run, 'rematch', rematch_batches(run))
    third = pass_rows(run, 'gapmatch', gapmatch_batches(run)) if os.path.exists(rd(run, 'gapmatch', 'batches.json')) else {}
    rows, cut = [], 0
    for i, r in first.items():
        s2, s3 = second.get(i), third.get(i)
        rows.append(dict(s3 or s2 or r, first_code=r['code'], **({'second_pass': True} if s2 else {}),
                         **({'third_pass': True} if s3 else {})))
    _, merged, gap_cut = gap_apply(rows) if third else (None, {}, set())
    for row in rows:
        if len(row['concepts']) > 2:
            row['concepts_dropped'], row['concepts'] = row['concepts'][2:], row['concepts'][:2]
            cut += 1
    write_atomic(rd(run, 'matches.jsonl'), jsonl(rows))
    n = len(rows)
    print(f"{n} claims: {sum(1 for r in rows if r['concepts']) / n:.1%} matched "
          f"({sum(1 for r in rows if r.get('second_pass') and not r.get('third_pass') and r['concepts'])} by the second pass, "
          f"{sum(1 for r in rows if r.get('third_pass') and r['concepts'])} by the gap pass), "
          f"codes {dict(collections.Counter(r['code'] for r in rows if r['code']))}, {cut} cut to two concepts")
    if third:
        print(f"review: {len(merged)} gap concepts merged, {len(gap_cut)} cut "
              f"({sum(1 for r in rows if r.get('gap_cut') and not r['concepts'])} claims back to no_concept)")


# ---- 3c: concepts for the claims that nothing matched ----

GAP_SHARD = 1500


def gap_ids(run):
    """Fixed once: the claims coded no_concept after both passes."""
    path = rd(run, 'gap', 'ids.json')
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    src = rd(run, 'matches.jsonl')
    if not os.path.exists(src):
        sys.exit('run matches-collect first')
    rows = [json.loads(l) for l in open(src, encoding='utf-8')]
    if any(r.get('third_pass') for r in rows):
        sys.exit('matches.jsonl already holds the gap pass; gap/ids.json is missing')
    ids = sorted(r['id'] for r in rows if r['code'] == 'no_concept')
    write_atomic(path, json.dumps(ids))
    return ids


def gap_plan(run):
    """Propose: the no_concept claims by domain group, in shards of about GAP_SHARD."""
    stage = 'gap'
    tpl = open(os.path.join(PROMPTS, 'concepts_gap_propose.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'shard': GAP_SHARD, 'seed': SEED, 'groups': GROUPS,
                        'registry_sha256': sha(open(os.path.join(OUT, 'concepts.jsonl'), 'rb').read())})
    ids, main = set(gap_ids(run)), main_registry()
    write_atomic(rd(run, stage, 'registry_names.jsonl'), jsonl({k: c[k] for k in ('concept_id', 'name')} for c in main))
    by = collections.defaultdict(list)
    for c in claims(run):
        if c['id'] in ids:
            by[GROUPS.get(c['domain'], c['domain'])].append(c)
    todo = []
    for g in sorted(by):
        rows = sorted(by[g], key=lambda c: c['id'])
        random.Random(f'{SEED}:gap:{g}').shuffle(rows)
        n = math.ceil(len(rows) / GAP_SHARD)
        for i in range(n):
            name, part = f'{g}-{i + 1}', rows[i::n]
            write_atomic(rd(run, stage, 'in', name + '.jsonl'),
                         jsonl({'id': c['id'], 'description': c['description']} for c in part))
            if propose_problems(run, name, stage) is None:
                continue
            todo.append(prompt(run, stage, 'propose-' + name, 'concepts_gap_propose.md', workdir=ROOT, domain=g,
                               n=len(part), n_concepts=len(main), shard_in=rel(rd(run, stage, 'in', name + '.jsonl')),
                               registry=rel(rd(run, stage, 'registry_names.jsonl')),
                               shard_out=rel(rd(run, stage, 'out', name + '.jsonl')), tmpdir=rel(rd(run, 'tmp', 'gap-' + name))))
    print(len(todo), 'gap propose prompts to run:')
    for p in todo:
        print(' ', rel(p))


def gapcons_plan(run):
    """Consolidate: one agent per domain group, against the whole approved registry."""
    stage = 'gapcons'
    tpl = open(os.path.join(PROMPTS, 'concepts_gap_consolidate.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'registry_sha256': sha(open(os.path.join(OUT, 'concepts.jsonl'), 'rb').read())})
    groups = collections.defaultdict(list)
    for f in sorted(os.listdir(rd(run, 'gap', 'in'))):
        name = f[:-6]
        if propose_problems(run, name, 'gap'):
            sys.exit(f'gap proposals for {name} are not done; run gap-ingest')
        ids = {json.loads(l)['id'] for l in open(rd(run, 'gap', 'in', f), encoding='utf-8')}
        for r in read_jsonl(rd(run, 'gap', 'out', f))[0]:
            r['examples'] = [e for e in r.get('examples') or [] if e in ids]  # examples are only hints
            groups[name.rsplit('-', 1)[0]].append({'shard': name, **r})
    main = main_registry()
    write_atomic(rd(run, stage, 'registry.jsonl'), jsonl({k: c[k] for k in ('concept_id', 'name', 'definition')} for c in main))
    todo = []
    for g, rows in sorted(groups.items()):
        write_atomic(rd(run, stage, 'in', g + '.jsonl'), jsonl(rows))
        if consolidate_problems(run, g, stage, {c['concept_id'] for c in main}) is None:
            continue
        todo.append(prompt(run, stage, 'consolidate-' + g, 'concepts_gap_consolidate.md', workdir=ROOT, domain=g,
                           proposals=rel(rd(run, stage, 'in', g + '.jsonl')), n_concepts=len(main),
                           registry=rel(rd(run, stage, 'registry.jsonl')), out=rel(rd(run, stage, 'out', g + '.jsonl')),
                           tmpdir=rel(rd(run, 'tmp', 'gapcons-' + g))))
    print(len(todo), 'gap consolidate prompts to run:')
    for p in todo:
        print(' ', rel(p))


def gap_consolidated(run):
    """(new concepts, mapping) from the per-group consolidations, before the cross-group merges;
    the same id from two groups is one concept, and domains come from the proposals' shards."""
    main = {c['concept_id'] for c in main_registry()}
    shard_domains = lambda props: sorted({d for p in props for d in p.split(':')[0].rsplit('-', 1)[0].split('+')})  # noqa: E731
    new, mapping = {}, []
    for f in sorted(os.listdir(rd(run, 'gapcons', 'in'))):
        g = f[:-6]
        if consolidate_problems(run, g, 'gapcons', main):
            sys.exit(f'gap consolidation of {g} is not done')
        for r in read_jsonl(rd(run, 'gapcons', 'out', f))[0]:
            row = gap_row(r, mapping, shard_domains)
            if row is None:
                continue
            old = new.get(row['concept_id'])
            if old:
                old['domains'] = sorted(set(old['domains']) | set(row['domains']))
                old['aliases'] = sorted(set(old['aliases'] or []) | set(row['aliases'] or []))
                old['est_claims'] = (old['est_claims'] or 0) + (row['est_claims'] or 0)
                old['examples'] = (old['examples'] or []) + (row['examples'] or [])
            else:
                new[row['concept_id']] = row
    return new, mapping


def gap_row(r, mapping, shard_domains):
    """One consolidated row: its proposals go to `mapping`; returns the new concept, or None."""
    if 'dropped' in r:
        mapping.append({'proposal': r['dropped'], 'concept_id': None, 'how': 'dropped', 'reason': r.get('reason', '')})
        return None
    for p in as_list(r.get('merged_from')):
        mapping.append({'proposal': p, 'concept_id': r['concept_id'], 'how': 'existing' if r.get('existing') else 'merged'})
    for p in as_list(r.get('split_from')):
        mapping.append({'proposal': p, 'concept_id': r['concept_id'], 'how': 'split'})
    if r.get('existing'):
        return None
    return {**{k: r.get(k) for k in ('concept_id', 'name', 'definition', 'type', 'aliases', 'came_true_guess',
                                     'est_claims', 'examples', 'bundle_check')},
            'domains': shard_domains(as_list(r.get('merged_from')) + as_list(r.get('split_from'))),
            'wikidata': None, 'source': 'gap'}


def gapglobal_plan(run):
    """The new concepts of every group, for one cross-group merge pass."""
    stage = 'gapglobal'
    tpl = open(os.path.join(PROMPTS, 'concepts_gap_global.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl)})
    new, _ = gap_consolidated(run)
    write_atomic(rd(run, stage, 'in', 'concepts.jsonl'),
                 jsonl({k: c[k] for k in ('concept_id', 'name', 'definition', 'domains', 'est_claims')} for c in new.values()))
    out = rd(run, stage, 'out', 'merges.jsonl')
    if os.path.exists(out) and read_jsonl(out)[0] is not None:
        print('done:', rel(out))
        return
    print(len(new), 'new concepts;', rel(prompt(run, stage, 'global', 'concepts_gap_global.md', workdir=ROOT,
                                               concepts=rel(rd(run, stage, 'in', 'concepts.jsonl')), out=rel(out),
                                               tmpdir=rel(rd(run, 'tmp', 'gapglobal')))))


def gap_concepts(run):
    """(new concepts, mapping): the per-group consolidations with the cross-group merges applied."""
    new, mapping = gap_consolidated(run)
    merges, err = read_jsonl(rd(run, 'gapglobal', 'out', 'merges.jsonl'))
    if merges is None:
        sys.exit(f'gap cross-group merges: {err}; run gapglobal-plan')
    gone = {}
    for m in merges:
        k = m['keep']
        while k in gone:
            k = gone[k]
        for d in m['drop']:
            if d == k or d in gone:
                continue
            if k not in new or d not in new:
                sys.exit(f'gap merge: unknown {k} or {d}')
            c = new.pop(d)
            new[k]['domains'] = sorted(set(new[k]['domains']) | set(c['domains']))
            new[k]['aliases'] = sorted(set(new[k]['aliases'] or []) | set(c['aliases'] or []) | {c['name']})
            new[k]['est_claims'] = (new[k]['est_claims'] or 0) + (c['est_claims'] or 0)
            new[k]['examples'] = (new[k]['examples'] or []) + (c['examples'] or [])
            gone[d] = k
    for m in mapping:
        while m['concept_id'] in gone:
            m['concept_id'], m['how'] = gone[m['concept_id']], m['how'] + '+global'
    return sorted(new.values(), key=lambda c: c['concept_id']), mapping


def gap_build(run):
    """runs/match/concepts_gap.jsonl (the new concepts) and concept_gap_mapping.jsonl."""
    new, mapping = gap_concepts(run)
    write_atomic(os.path.join(OUT, 'concepts_gap.jsonl'), jsonl(new))
    write_atomic(os.path.join(OUT, 'concept_gap_mapping.jsonl'), jsonl(mapping))
    how = collections.Counter(m['how'] for m in mapping)
    print(f"{len(new)} new concepts; proposals: {dict(how)}; "
          f"{len({m['concept_id'] for m in mapping if m['how'] == 'existing'})} existing concepts proposed again")


def gap_apply(rows):
    """The reviewer's decisions on the gap concepts (runs/match/concept_review.jsonl), applied to the
    collected rows in place: `gap_merge` rows first, then `gap_min_claims` cuts the new concepts with
    fewer matched claims. A claim left with no concept is no_concept again; what was removed is kept
    in `gap_cut`, and merged ids in `gap_merged`. concepts_gap.jsonl stays as built (the gap pass's
    outputs are checked against it). Returns (kept new ids, merged id -> kept id, cut ids)."""
    new = {json.loads(l)['concept_id'] for l in open(os.path.join(OUT, 'concepts_gap.jsonl'), encoding='utf-8')}
    known = new | {c['concept_id'] for c in main_registry()}
    to, least = {}, 0
    for r in reviewer_rows():
        if r['op'] == 'gap_merge':
            for d in r['drop']:
                if d not in new or r['keep'] not in known or d == r['keep']:
                    sys.exit(f'review gap_merge: {d} is not a new concept, or {r["keep"]} is unknown')
                to[d] = r['keep']
        elif r['op'] == 'gap_min_claims':
            least = r['min']
    final = lambda c: final(to[c]) if c in to else c  # noqa: E731
    for row in rows:
        cs = list(dict.fromkeys(final(c) for c in row['concepts']))
        if cs != row['concepts']:
            row['gap_merged'], row['concepts'] = [c for c in row['concepts'] if c in to], cs
    hits = collections.Counter(c for row in rows for c in row['concepts'] if c in new)
    cut = {c for c in new - set(to) if hits[c] < least}
    for row in rows:
        gone = [c for c in row['concepts'] if c in cut]
        if gone:
            row['gap_cut'], row['concepts'] = gone, [c for c in row['concepts'] if c not in cut]
            if not row['concepts']:
                row['code'] = 'no_concept'
    return new - set(to) - cut, to, cut


def gapmatch_registry():
    """The new concepts, and the approved ones the gap proposals turned out to duplicate."""
    new = [json.loads(l) for l in open(os.path.join(OUT, 'concepts_gap.jsonl'), encoding='utf-8')]
    again = {json.loads(l)['concept_id'] for l in open(os.path.join(OUT, 'concept_gap_mapping.jsonl'), encoding='utf-8')}
    return new + [c for c in main_registry() if c['concept_id'] in again]  # proposals mapped or split onto approved ones


def gapmatch_batches(run):
    path = rd(run, 'gapmatch', 'batches.json')
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    left = list(gap_ids(run))
    random.Random(f'{SEED}:gapmatch').shuffle(left)
    n = math.ceil(len(left) / BATCH)
    batches = {f'gapmatch-{i + 1:03d}': {'ids': left[i::n]} for i in range(n)}
    write_atomic(path, json.dumps(batches))
    return batches


def gapmatch_plan(run, limit=None):
    """Like rematch-plan: the no_concept claims against the gap concepts."""
    stage = 'gapmatch'
    tpl = open(os.path.join(PROMPTS, 'gapmatch.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'batch': BATCH, 'seed': SEED,
                        'gap_registry_sha256': sha(open(os.path.join(OUT, 'concepts_gap.jsonl'), 'rb').read())})
    claim_batches(run, stage, gapmatch_batches(run), 'gapmatch.md', gapmatch_registry(), limit)


SIMILAR = 0.2
STOP = set('that this with from into their them they which when where what will would could than then also only '
           'other such have been being make makes made using uses used kind form like more most some very each '
           'without within through about over under between device machine system people person world'.split())


def similar_pairs(new, main):
    """(score, new id, approved id) for each new concept whose closest approved concept shares at
    least SIMILAR of their content words (Jaccard), highest first."""
    words = lambda c: {w for w in re.findall(r'[a-z]{4,}', ' '.join([c['concept_id'].replace('-', ' '), c['name'],  # noqa: E731
                                                                      c['definition']]).lower()) if w not in STOP}
    mw = [(c['concept_id'], words(c)) for c in main]
    pairs = []
    for c in new:
        w = words(c)
        score, best = max(((len(w & v) / len(w | v) if w | v else 0, cid) for cid, v in mw), default=(0, None))
        if score >= SIMILAR:
            pairs.append((score, c['concept_id'], best))
    return sorted(pairs, reverse=True)


def gap_review(run):
    """runs/match/gap_review.md: the new concepts with the claims the gap pass matched to them,
    for the user's review before milestone research."""
    third = pass_rows(run, 'gapmatch', gapmatch_batches(run))
    hits = collections.Counter(c for r in third.values() for c in r['concepts'][:2])
    new, mapping = gap_concepts(run)
    main = {c['concept_id']: c for c in main_registry()}
    again = collections.Counter(m['concept_id'] for m in mapping if m['concept_id'] in main)
    cell = lambda s: str(s or '').replace('|', '/').replace('\n', ' ')  # noqa: E731
    n, matched = len(third), sum(1 for r in third.values() if r['concepts'])
    out = ['# Gap concepts (3c): review before milestone research', '',
           f'{n:,} claims were coded no_concept after both passes. Agents proposed concepts for what they kept '
           f'returning to; one agent per domain group consolidated them against the approved registry, and one more '
           f'merged duplicates across groups. The gap pass then matched {matched:,} of the {n:,} ({matched / n:.0%}).', '',
           f'- **New concepts:** {len(new)} ({sum(1 for c in new if hits[c["concept_id"]] < 3)} with fewer than 3 matched claims).',
           '- **Where a cut would fall:** ' + '; '.join(
               f'keeping those with at least {k} matched claims keeps {sum(1 for c in new if hits[c["concept_id"]] >= k)} '
               f'concepts and {sum(hits[c["concept_id"]] for c in new if hits[c["concept_id"]] >= k):,} claims' for k in (3, 5, 10)) + '.',
           f'- **Proposals that duplicated an approved concept:** {sum(again.values())}, for {len(again)} concepts '
           f'(claims the earlier passes missed).',
           f'- **Codes after the gap pass:** {dict(collections.Counter(r["code"] for r in third.values() if r["code"]))}.', '',
           'Each new concept will get milestone research. To drop or merge one, add a row to '
           '`runs/match/concept_review.jsonl` before research starts.', '']
    decided = [r for r in reviewer_rows() if r['op'] in ('gap_merge', 'gap_min_claims')]
    if decided:
        out += ['**Decisions** (`concept_review.jsonl`, applied by matches-collect; the tables below are before them):', '']
        what = lambda r: (f"merge {', '.join(r['drop'])} into {r['keep']}" if r['op'] == 'gap_merge'  # noqa: E731
                          else f"cut the new concepts with fewer than {r['min']} matched claims")
        out += [f"- {what(r)}: {r['reason']}" for r in decided] + ['']
    out += ['## New concepts, by matched claims', '',
            '| concept | definition | came true? | domains | proposed | matched |', '|---|---|---|---|---|---|']
    for c in sorted(new, key=lambda c: (-hits[c['concept_id']], c['concept_id'])):
        out.append(f"| `{c['concept_id']}` {cell(c['name'])} | {cell(c['definition'])} | {c['came_true_guess']} | "
                   f"{', '.join(c['domains'])} | {c['est_claims'] or ''} | {hits[c['concept_id']]} |")
    out += ['', '## New concepts that may duplicate an approved one', '',
            'The closest approved concept to each new one by shared words in id, name and definition '
            f'(Jaccard of {SIMILAR:.2f} or more): a check on the consolidators, which judged them distinct.', '',
            '| new concept | approved concept | overlap |', '|---|---|---|']
    for score, a, b in similar_pairs(new, list(main.values())):
        out.append(f'| `{a}` | `{b}` | {score:.2f} |')
    out += ['', '## Approved concepts the gap proposals duplicated', '',
            '| concept | definition | proposals | matched in the gap pass |', '|---|---|---|---|']
    for cid, k in again.most_common():
        out.append(f"| `{cid}` {cell(main[cid]['name'])} | {cell(main[cid]['definition'])} | {k} | {hits[cid]} |")
    write_atomic(os.path.join(OUT, 'gap_review.md'), '\n'.join(out) + '\n')
    print(f'{len(new)} new concepts, {matched:,} of {n:,} claims matched ->', rel(os.path.join(OUT, 'gap_review.md')))


# ---- §4: agreement, a second agent re-matches 300 random claims ----

AGREE_N = 300


def final_registry(run):
    """The approved concepts and the new ones that kept a matched claim after the gap review."""
    hit = {c for l in open(rd(run, 'matches.jsonl'), encoding='utf-8') for c in json.loads(l)['concepts']}
    gap = [json.loads(l) for l in open(os.path.join(OUT, 'concepts_gap.jsonl'), encoding='utf-8')]
    return main_registry() + [c for c in gap if c['concept_id'] in hit]


def agree_plan(run):
    stage = 'agree'
    tpl = open(os.path.join(PROMPTS, 'agree.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'n': AGREE_N, 'seed': SEED})
    path = rd(run, stage, 'batches.json')
    if not os.path.exists(path):
        ids = sorted(json.loads(l)['id'] for l in open(rd(run, 'matches.jsonl'), encoding='utf-8'))
        write_atomic(path, json.dumps({'agree-001': {'ids': random.Random(f'{SEED}:agree').sample(ids, AGREE_N)}}))
    reg = final_registry(run)
    claim_batches(run, stage, json.load(open(path, encoding='utf-8')), 'agree.md', reg)


def agree_report(run):
    """runs/match/agreement.md: the second agent's answers against matches.jsonl."""
    second = pass_rows(run, 'agree', json.load(open(rd(run, 'agree', 'batches.json'), encoding='utf-8')))
    first = {r['id']: r for r in map(json.loads, open(rd(run, 'matches.jsonl'), encoding='utf-8')) if r['id'] in second}
    t = collections.Counter()
    for i, b in second.items():
        a, bc = set(first[i]['concepts']), set(b['concepts'][:2])
        t['both matched' if a and bc else 'both unmatched' if not a and not bc else 'one matched'] += 1
        if a and bc:
            t['same concepts' if a == bc else 'overlap' if a & bc else 'different concepts'] += 1
        elif not a and not bc:
            t['same code' if first[i]['code'] == b['code'] else 'other code'] += 1
        else:
            t['run matched, second agent not' if a else 'second agent matched, run not'] += 1
    n = len(second)
    pct = lambda k: f'{t[k]} ({t[k] / n:.0%})'  # noqa: E731
    out = ['# Matching agreement (runs/match/PLAN.md §4)', '',
           f'A second agent matched {n} claims drawn at random (seed {SEED}) against the whole final registry '
           f'({len(final_registry(run))} concepts), without seeing the run\'s answers. Shares are of all {n}.', '',
           '| | claims |', '|---|---|'] + [f'| {k} | {pct(k)} |' for k in (
               'both matched', 'same concepts', 'overlap', 'different concepts', 'both unmatched', 'same code', 'other code',
               'one matched', 'run matched, second agent not', 'second agent matched, run not')]
    agree = t['same concepts'] + t['overlap'] + t['same code']
    out += ['', f'Agreement (the same or overlapping concepts, or the same code): {agree} of {n} ({agree / n:.0%}).']
    write_atomic(os.path.join(OUT, 'agreement.md'), '\n'.join(out) + '\n')
    print(f'{agree} of {n} agree ->', rel(os.path.join(OUT, 'agreement.md')))


# ---- §5: milestones, tier 1 ----

RESEARCH_BATCH, CHECK_BATCH = 15, 40
KINDS = ('first_demonstration', 'first_practical_use', 'mass_adoption')
PILOT_MILESTONES = os.path.join(ROOT, 'pilot', 'computing', 'milestones3.jsonl')
DATE = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')


def research_concepts(run):
    """Every concept with a matched claim in matches.jsonl, except the computing pilot's concepts
    that have reviewed milestones and the same definition."""
    path, review = rd(run, 'matches.jsonl'), os.path.join(OUT, 'concept_review.jsonl')
    if os.path.exists(review) and os.path.getmtime(review) > os.path.getmtime(path):
        sys.exit('concept_review.jsonl changed after matches.jsonl: run matches-collect first')
    seed = {c['concept_id']: c['definition'] for c in seed_registry()}
    done = {json.loads(l)['concept_id'] for l in open(PILOT_MILESTONES, encoding='utf-8')}
    return [c for c in final_registry(run) if not (c['concept_id'] in done and seed.get(c['concept_id']) == c['definition'])]


def research_batches(run):
    """research/batches.json, fixed once: `tier1-NNN` batches of RESEARCH_BATCH concepts, `check-NNN`
    batches of CHECK_BATCH concepts guessed never to have come true, both in domain order so that a
    researcher's concepts are related. When every check is done, the concepts a check found a real
    event for are added as more tier1 batches."""
    path = rd(run, 'research', 'batches.json')
    if os.path.exists(path):
        batches = json.load(open(path, encoding='utf-8'))
    else:
        cs = sorted(research_concepts(run), key=lambda c: ((c.get('domains') or ['other'])[0], c['concept_id']))
        full = [c['concept_id'] for c in cs if c['came_true_guess'] != 'no']
        quick = [c['concept_id'] for c in cs if c['came_true_guess'] == 'no']
        batches = {f'tier1-{i // RESEARCH_BATCH + 1:03d}': {'ids': full[i:i + RESEARCH_BATCH]} for i in range(0, len(full), RESEARCH_BATCH)}
        batches.update({f'check-{i // CHECK_BATCH + 1:03d}': {'ids': quick[i:i + CHECK_BATCH]} for i in range(0, len(quick), CHECK_BATCH)})
        write_atomic(path, json.dumps(batches, indent=0))
    checks = [n for n in batches if n.startswith('check-')]
    if all(research_problems(run, n) is None for n in checks):
        queued = {i for n, b in batches.items() if n.startswith('tier1-') for i in b['ids']}
        fits = [r['concept_id'] for n in checks for r in read_jsonl(rd(run, 'research', 'out', n + '.jsonl'))[0]
                if r.get('verdict') == 'fits' and r['concept_id'] not in queued]
        if fits:
            k = max(int(n[6:]) for n in batches if n.startswith('tier1-'))
            batches.update({f'tier1-{k + i // RESEARCH_BATCH + 1:03d}': {'ids': fits[i:i + RESEARCH_BATCH], 'from_checks': True}
                            for i in range(0, len(fits), RESEARCH_BATCH)})
            write_atomic(path, json.dumps(batches, indent=0))
    return batches


def research_problems(run, name):
    """None if the batch's output is complete and well formed, else what is wrong."""
    out = rd(run, 'research', 'out', name + '.jsonl')
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    ids = [json.loads(l)['concept_id'] for l in open(rd(run, 'research', 'in', name + '.jsonl'), encoding='utf-8')]
    bad = []
    if name.startswith('check-'):
        got = [r.get('concept_id') for r in rows]
        if sorted(got) != sorted(ids):
            bad.append(f'{len(got)} rows for {len(ids)} concepts, or other ids')
        bad += [f"{r.get('concept_id')}: verdict {r.get('verdict')!r}" for r in rows if r.get('verdict') not in ('fits', 'none')]
        top = collections.Counter(r.get('note') for r in rows).most_common(1)
        if top and top[0][1] > 2:
            bad.append(f'{top[0][1]} identical notes: {top[0][0]!r}')
        return bad or None
    notes = [r['concept_id'] for r in rows if 'concept_note' in r]
    if sorted(notes) != sorted(ids):
        bad.append(f'concept notes for {len(notes)} of {len(ids)} concepts, or other ids')
    for r in rows:
        if 'kind' not in r:
            continue
        where = f"{r.get('concept_id')} {r.get('kind')}"
        if r.get('concept_id') not in ids or r['kind'] not in KINDS or not DATE.match(str(r.get('date', ''))):
            bad.append(f'{where}: id, kind or date {r.get("date")!r}')
        srcs = r.get('sources')
        if not isinstance(srcs, list) or not 1 <= len(srcs) <= 3 or not str(r.get('fit', '')).strip():
            bad.append(f'{where}: sources or fit')
            continue
        for s in srcs:
            if not isinstance(s, dict) or not s.get('url') or not s.get('quote') or len(str(s['quote']).split()) > 25 \
                    or s.get('kind') not in ('contemporary', 'reference'):
                bad.append(f'{where}: source {str(s)[:80]}')
    return bad or None


def research_plan(run, limit=None, only=''):
    """Claim up to `limit` research batches (whose names start with `only`) that aren't done or claimed
    in the last CLAIM_MINUTES and print their prompts (tier-1 research, or the quick check for concepts
    guessed never to have come true)."""
    stage = 'research'
    tpl = {k: open(os.path.join(PROMPTS, f), encoding='utf-8').read()
           for k, f in (('tier1', 'milestones_tier1.md'), ('check', 'milestones_check.md'))}
    config(run, stage, {'tier1_prompt_sha256': sha(tpl['tier1']), 'check_prompt_sha256': sha(tpl['check']),
                        'batch': RESEARCH_BATCH, 'check_batch': CHECK_BATCH})
    batches = research_batches(run)
    reg = {c['concept_id']: c for c in registry_rows()}
    todo, now = [], time.time()
    for name, b in batches.items():
        inp = rd(run, stage, 'in', name + '.jsonl')
        if not os.path.exists(inp):  # definitions only: the researchers never see claims (PLAN §5)
            write_atomic(inp, jsonl({k: reg[i].get(k) for k in ('concept_id', 'name', 'definition', 'type', 'aliases', 'came_true_guess')}
                                    for i in b['ids']))
        mark = rd(run, stage, 'prompts', name + '.claimed')
        if not name.startswith(only) or research_problems(run, name) is None or \
                (os.path.exists(mark) and now - os.path.getmtime(mark) < CLAIM_MINUTES * 60):
            continue
        todo.append(name)
    todo.sort(key=lambda n: (not n.startswith('check-'), n))  # the checks first: they may add tier-1 batches
    pick = todo[:int(limit)] if limit else todo
    for name in pick:
        kind = name.split('-')[0]
        path = prompt(run, stage, name, {'tier1': 'milestones_tier1.md', 'check': 'milestones_check.md'}[kind],
                      workdir=ROOT, n=len(batches[name]['ids']), batch_in=rel(rd(run, stage, 'in', name + '.jsonl')),
                      batch_out=rel(rd(run, stage, 'out', name + '.jsonl')), tmpdir=rel(rd(run, 'tmp', stage + '-' + name)))
        write_atomic(rd(run, stage, 'prompts', name + '.claimed'), time.strftime('%Y-%m-%dT%H:%M:%S\n'))
        print(rel(path))
    done = sum(1 for n in batches if research_problems(run, n) is None)
    print(f'{len(pick)} claimed; {len(todo) - len(pick)} more pending; {done} of {len(batches)} batches done', file=sys.stderr)


def verify(run):
    """runs/match/milestones.jsonl: the pilot's reviewed milestones for its unchanged concepts, and
    the tier-1 research with every source checked again in code, independently of the agents, as
    the pilot's merge did:
      - the page or record is fetched anew (pipeline/sources.py) and the quote must be at most 25
        words and occur in its text;
      - for records that carry a date, the source's `date` is the record's;
      - `contemporary` needs a source dated within two years of the event, else it is `reference`;
      - a milestone with no verified source is dropped; `high` needs a verified contemporary and
        a verified reference source, else it is `medium`;
      - for each concept and kind, the earliest verified milestone is kept.
    The verdicts are cached in work/match/<run>/research/quote_check.jsonl (url, quote, verdict, record
    date: never page text), so a re-run only fetches new sources. Concept notes and the checks'
    verdicts go to runs/match/milestone_notes.jsonl."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sources
    from concurrent.futures import ThreadPoolExecutor
    batches = research_batches(run)
    ms, notes = [], []
    for name in batches:
        if research_problems(run, name) is not None:
            continue
        for r in read_jsonl(rd(run, 'research', 'out', name + '.jsonl'))[0]:
            if 'kind' in r:
                ms.append(dict(r, batch=name))
            elif 'concept_note' in r or 'verdict' in r:
                notes.append(dict(r, batch=name))
    cache_path = rd(run, 'research', 'quote_check.jsonl')
    cache = {(c['url'], c.get('volume_id'), c['quote']): c for c in (read_jsonl(cache_path)[0] or [])} \
        if os.path.exists(cache_path) else {}
    need = {(s['url'], s.get('volume_id'), s['quote'].strip()) for m in ms for s in m['sources']} - set(cache)
    pages = {}

    def get(k):
        try:
            t, d = sources.fetch(k[0], k[1])
            return k, (t, d, '')
        except Exception as e:  # noqa: BLE001
            return k, (None, '', repr(e)[:200])
    with ThreadPoolExecutor(4) as ex:
        for (url, vol), res in ex.map(get, sorted({(u, v) for u, v, _ in need}, key=str)):
            pages[(url, vol)] = res
    for url, vol, q in need:
        t, d, err = pages[(url, vol)]
        verdict = 'fetch failed: ' + err if t is None else 'ok' if sources.has_quote(t, q) else 'quote not on page'
        cache[(url, vol, q)] = {'url': url, 'volume_id': vol, 'quote': q, 'verdict': verdict, 'record_date': d}
    write_atomic(cache_path, jsonl(cache.values()))
    out, log = [], collections.Counter()
    for m in ms:
        ey = int(m['date'][:4])
        keep = []
        for s in m['sources']:
            c = cache[(s['url'], s.get('volume_id'), s['quote'].strip())]
            log[c['verdict'].split(':')[0]] += 1
            if c['verdict'] != 'ok':
                continue
            sdate, kind = c['record_date'] or str(s.get('date') or ''), s['kind']
            sy = re.search(r'(?<!\d)(\d{4})', sdate)
            if kind == 'contemporary' and not (sy and ey - 2 <= int(sy.group(1)) <= ey + 2):
                kind = 'reference'
                log['contemporary -> reference'] += 1
            keep.append({**{k: s.get(k, '') for k in ('url', 'publisher', 'title', 'quote')}, 'date': sdate, 'kind': kind,
                         **({'volume_id': s['volume_id']} if s.get('volume_id') else {})})
        if not keep:
            log['milestone dropped'] += 1
            continue
        conf = m.get('confidence') if m.get('confidence') in ('high', 'medium', 'low') else 'low'
        if conf == 'high' and not {'contemporary', 'reference'} <= {s['kind'] for s in keep}:
            conf = 'medium'
        out.append({'concept_id': m['concept_id'], 'kind': m['kind'], 'date': m['date'], 'what': m.get('what', ''),
                    'fit': m['fit'], 'sources': keep, 'confidence': conf,
                    **{k: m[k] for k in ('note', 'searched') if m.get(k)}, 'tier': 1, 'batch': m['batch']})
    best = {}
    for r in out:
        k = (r['concept_id'], r['kind'])
        if k not in best or r['date'] < best[k]['date']:
            best[k] = r
    researched = {i for b in batches.values() for i in b['ids']}
    pilot = [dict(r, tier='pilot') for r in map(json.loads, open(PILOT_MILESTONES, encoding='utf-8'))
             if r['concept_id'] not in researched]
    rows = sorted(pilot + list(best.values()), key=lambda r: (r['concept_id'], KINDS.index(r['kind'])))
    for c, d in itertools.groupby(rows, key=lambda r: r['concept_id']):
        d = {r['kind']: r['date'] for r in d}
        if d.get('first_practical_use', '9999')[:4] < d.get('first_demonstration', '0000')[:4]:
            print(f'WARNING {c}: practical use {d["first_practical_use"]} before demonstration {d["first_demonstration"]}')
    write_atomic(os.path.join(OUT, 'milestones.jsonl'), jsonl(rows))
    write_atomic(os.path.join(OUT, 'milestone_notes.jsonl'), jsonl(sorted(notes, key=lambda r: r['concept_id'])))
    print(f"{len(ms)} researched milestones -> {len(best)} kept for {len({k[0] for k in best})} concepts, "
          f"plus {len(pilot)} pilot rows; sources {dict(log)}")


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
     'rematch-plan': rematch_plan, 'matches-collect': matches_collect, 'gap-plan': gap_plan,
     'gap-ingest': lambda run: concepts_ingest(run, 'gap'), 'gapcons-plan': gapcons_plan, 'gapglobal-plan': gapglobal_plan,
     'gap-build': gap_build,
     'gapmatch-plan': gapmatch_plan, 'gap-review': gap_review, 'agree-plan': agree_plan, 'agree-report': agree_report,
     'research-plan': research_plan, 'verify': verify,
     'log': log, 'status': status}[cmd](*args)
