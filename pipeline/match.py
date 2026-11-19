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
    python -I pipeline/match.py research-plan <run> [n] [prefix]  §5 tiers 1 and 2: claim up to n research batches, print their prompts
    python -I pipeline/match.py verify <run>                  check every source again -> runs/match/milestones.jsonl
    python -I pipeline/match.py deciding-report <run>         tier 2's checkpoint-3 table -> runs/match/deciding_milestones.md
    python -I pipeline/match.py judge-plan <run> [n] [prefix] §6-7: claim up to n judging batches (A, B, then C), print their prompts;
                                                              a changed milestone adds a round (judge_batches)
    python -I pipeline/match.py judge-collect <run>           -> work/match/<run>/judgments.jsonl + runs/match/judging.md
    python -I pipeline/match.py score <run>                   §8: resolutions, points, rankings -> runs/match/scoring.md + deciding.jsonl
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
import csv
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


TRANCHE = 'A'  # use_run: the run `full` is tranche A, with its outputs in runs/match/; any other run is tranche B


def use_run(run):
    """Tranche B runs (PLAN §9) keep their outputs in runs/match/<run>/ and read prompts/b/<name> where one exists.
    Their registry starts as tranche A's final one, so a book counts an idea once across both tranches."""
    global OUT, TRANCHE, REVIEW, RECHECK
    if run != 'full':
        OUT, TRANCHE = os.path.join(ROOT, 'runs', 'match', run), 'B'
        REVIEW, RECHECK = os.path.join(OUT, 'milestone_review.jsonl'), os.path.join(OUT, 'tier2_recheck.jsonl')


def template(name):
    b = os.path.join(PROMPTS, 'b', name)
    return b if TRANCHE == 'B' and os.path.exists(b) else os.path.join(PROMPTS, name)


def book_review():
    """runs/match/book_review.jsonl: corrected years and credits by library path (report §6.7; DESIGN §1a's
    composition dates for ancient texts). Applied on load, so the pinned claims export stays as written."""
    path = os.path.join(ROOT, 'runs', 'match', 'book_review.jsonl')  # one file for both tranches
    return {r['path']: r for r in read_jsonl(path)[0]} if os.path.exists(path) else {}


def claims(run):
    year = {sha(p)[:12]: r['year'] for p, r in book_review().items() if 'year' in r}
    rows = [json.loads(l) for l in open(rd(run, 'claims.jsonl'), encoding='utf-8')]
    return [dict(c, year=year[c['book']], year_source='review') if c['book'] in year else c for c in rows]


def seed_registry():
    return [{'concept_id': c['concept_id'], 'name': c['name'], 'definition': c['definition']}
            for c in map(json.loads, open(SEED_CONCEPTS, encoding='utf-8'))]


def config(run, stage, settings):
    """Record a stage's settings; refuse to continue if one of them changed (a new one is added)."""
    path = rd(run, stage, 'config.json')
    old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    changed = {k: (old[k], v) for k, v in settings.items() if k in old and old[k] != v}
    if changed:
        sys.exit(f'{rel(path)} has other settings (was, now): {changed}')
    if settings.keys() - old.keys():
        write_atomic(path, json.dumps({**old, **settings}, indent=1) + '\n')


def prompt(run, stage, name, tpl_name, **fields):
    text = open(template(tpl_name), encoding='utf-8').read()
    for k, v in fields.items():
        text = text.replace('{' + k + '}', str(v))
    path = rd(run, stage, 'prompts', name + '.md')
    write_atomic(path, text)
    return path


# ---- concepts: propose ----

def concepts_plan(run):
    stage = 'concepts'
    tpl = open(template('concepts_propose.md'), encoding='utf-8').read()
    config(run, stage, {'tranche': TRANCHE, 'sample': SAMPLE, 'shard': SHARD, 'seed': SEED,
                        'claims_sha256': sha(open(rd(run, 'claims.jsonl'), 'rb').read()),
                        'prompt_sha256': sha(tpl), 'seed_concepts_sha256': sha(open(SEED_CONCEPTS, 'rb').read())})
    write_atomic(rd(run, stage, 'registry_seed.jsonl'), jsonl(seed_registry()))
    by = collections.defaultdict(list)
    for c in claims(run):
        if c['tranche'] == TRANCHE:
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
    tpl = open(template('concepts_consolidate.md'), encoding='utf-8').read()
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
    tpl = open(template('concepts_global.md'), encoding='utf-8').read()
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
    tpl = open(template('concepts_audit.md'), encoding='utf-8').read()
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


def b_init(run, n=None):
    """Start a tranche-B run (PLAN §9): work/match/<run>/claims.jsonl, tranche A's export (the tranche filter
    picks B), or for a pilot a fixed-seed sample of `n` society-politics claims; and runs/match/<run>/concepts.jsonl,
    tranche A's final registry, which B's matching uses and its gap pass extends."""
    if TRANCHE != 'B' or os.path.exists(os.path.join(OUT, 'concepts.jsonl')):
        sys.exit(f'{rel(OUT)} is tranche A or already started')
    a_out = os.path.join(ROOT, 'runs', 'match')
    hit = {k for l in open(rd('full', 'matches.jsonl'), encoding='utf-8') for k in json.loads(l)['concepts']}
    reg = read_jsonl(os.path.join(a_out, 'concepts.jsonl'))[0] + \
        [c for c in read_jsonl(os.path.join(a_out, 'concepts_gap.jsonl'))[0] if c['concept_id'] in hit]
    rows = open(rd('full', 'claims.jsonl'), encoding='utf-8').read().splitlines(True)
    if n:
        pool = sorted(l for l in rows if json.loads(l)['tranche'] == 'B' and json.loads(l)['domain'] == 'society-politics')
        rows = sorted(random.Random(f'{SEED}:{run}').sample(pool, int(n)))
    write_atomic(rd(run, 'claims.jsonl'), ''.join(rows))
    write_atomic(os.path.join(OUT, 'concepts.jsonl'), jsonl(dict(c, tranche='A') for c in reg))
    print(f"{sum(json.loads(l)['tranche'] == 'B' for l in rows):,} tranche-B claims -> {rel(rd(run, 'claims.jsonl'))}; "
          f"{len(reg):,} tranche-A concepts -> {rel(os.path.join(OUT, 'concepts.jsonl'))}")


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
        if c['tranche'] == TRANCHE:
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
    tpl = open(template('match.md'), encoding='utf-8').read()
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
    left = sorted(i for i, r in first_pass(run).items() if r['code'] in RETRY)  # tranche B has no second pass (gap_ids)
    random.Random(f'{SEED}:rematch').shuffle(left)
    n = math.ceil(len(left) / BATCH)
    batches = {f'rematch-{i + 1:03d}': {'ids': left[i::n]} for i in range(n)}
    write_atomic(path, json.dumps(batches))
    return batches


def rematch_plan(run, limit=None):
    """Like match-plan, for the claims the first pass coded no_concept or too_vague."""
    stage = 'rematch'
    tpl = open(template('rematch.md'), encoding='utf-8').read()
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
    second = {} if TRANCHE == 'B' else pass_rows(run, 'rematch', rematch_batches(run))
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
    # tranche B's first pass met a registry of mostly technology, so every claim it left unmatched gets the gap pass
    ids = sorted(r['id'] for r in rows if r['code'] in (CODES if TRANCHE == 'B' else {'no_concept'}))
    write_atomic(path, json.dumps(ids))
    return ids


def gap_plan(run):
    """Propose: the no_concept claims by domain group, in shards of about GAP_SHARD."""
    stage = 'gap'
    tpl = open(template('concepts_gap_propose.md'), encoding='utf-8').read()
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
    tpl = open(template('concepts_gap_consolidate.md'), encoding='utf-8').read()
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
    tpl = open(template('concepts_gap_global.md'), encoding='utf-8').read()
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
    tpl = open(template('gapmatch.md'), encoding='utf-8').read()
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
    tpl = open(template('agree.md'), encoding='utf-8').read()
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

RESEARCH_BATCH, CHECK_BATCH, RECHECK_BATCH, TIER2_BATCH = 15, 40, 5, 5
TIER2_KINDS = ('first_demonstration', 'first_practical_use')  # tier 2 checks the kinds that score
VERDICTS = ('confirmed', 'replaced', 'removed', 'added')
KINDS = ('first_demonstration', 'first_practical_use', 'mass_adoption')
PILOT_MILESTONES = os.path.join(ROOT, 'pilot', 'computing', 'milestones3.jsonl')
REVIEW = os.path.join(OUT, 'milestone_review.jsonl')
RECHECK = os.path.join(OUT, 'tier2_recheck.jsonl')  # concepts tier 2 checks again, with the review assist's objection  # checkpoint 3's decisions on tier 2's answers (PLAN §5)
PILOT_REVIEW = os.path.join(ROOT, 'pilot', 'computing', 'raw', 'review3.jsonl')
DATE = re.compile(r'^(-\d{4,}|\d{4})(-\d{2}(-\d{2})?)?$')  # a leading '-' for a year BC (-0602, -62000)


def date_key(d):
    """Sort key for a milestone date: the year as a number (BC years are negative), then month and day."""
    y, rest = re.match(r'(-?\d+)(.*)', d).groups()
    return int(y), rest


def research_concepts(run):
    """Every concept with a matched claim in matches.jsonl, except the computing pilot's concepts
    that have reviewed milestones and the same definition."""
    path, review = rd(run, 'matches.jsonl'), os.path.join(OUT, 'concept_review.jsonl')
    if os.path.exists(review) and os.path.getmtime(review) > os.path.getmtime(path):
        sys.exit('concept_review.jsonl changed after matches.jsonl: run matches-collect first')
    if TRANCHE == 'B':  # tranche A's concepts come with their verified milestones (verify)
        a = {c['concept_id'] for c in main_registry()}
        return [c for c in final_registry(run) if c['concept_id'] not in a]
    seed = {c['concept_id']: c['definition'] for c in seed_registry()}
    done = {json.loads(l)['concept_id'] for l in open(PILOT_MILESTONES, encoding='utf-8')}
    return [c for c in final_registry(run) if not (c['concept_id'] in done and seed.get(c['concept_id']) == c['definition'])]


def research_batches(run):
    """research/batches.json, fixed once: `tier1-NNN` batches of RESEARCH_BATCH concepts, `check-NNN`
    batches of CHECK_BATCH concepts guessed never to have come true, both in domain order so that a
    researcher's concepts are related. When every check is done, the concepts a check found a real
    event for are added as more tier1 batches; when every tier1 batch is done, the concepts guessed
    "yes" that it gave no demonstration or practical use go to `recheck-NNN` batches of RECHECK_BATCH,
    a second look with the first researcher's note. Once the first scoring has written
    runs/match/deciding.jsonl, its concepts go to `tier2-NNN` batches of TIER2_BATCH, most points
    first (PLAN §5 tier 2); when every tier2 batch is done, the concepts a later scoring added to
    deciding.jsonl go to a new round of them, numbered on."""
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
    tier1 = [n for n in batches if n.startswith('tier1-')]
    if not any(n.startswith('recheck-') for n in batches) and all(research_problems(run, n) is None for n in tier1):
        miss = [i for n in sorted(tier1) for i in batches[n]['ids']
                if i not in first_pass_dated(run, n) and research_inputs(run, n)[i]['came_true_guess'] == 'yes']
        batches.update({f'recheck-{i // RECHECK_BATCH + 1:03d}': {'ids': miss[i:i + RECHECK_BATCH]}
                        for i in range(0, len(miss), RECHECK_BATCH)})
        write_atomic(path, json.dumps(batches, indent=0))
    deciding, t2 = os.path.join(OUT, 'deciding.jsonl'), [n for n in batches if n.startswith('tier2-')]
    if os.path.exists(deciding) and all(research_problems(run, n) is None for n in t2):
        queued = {i for n in t2 for i in batches[n]['ids']}
        if TRANCHE == 'B':  # tranche A's concepts keep tranche A's milestones (its own tier 2 checks them)
            queued |= {c['concept_id'] for c in main_registry()}
        ids = [r['concept_id'] for r in read_jsonl(deciding)[0] if r['concept_id'] not in queued]
        rnd = 1 + max((batches[n].get('round', 1) for n in t2), default=0)
        batches.update({f'tier2-{len(t2) + i // TIER2_BATCH + 1:03d}': {'ids': ids[i:i + TIER2_BATCH], **({'round': rnd} if rnd > 1 else {})}
                        for i in range(0, len(ids), TIER2_BATCH)})
        if ids:
            write_atomic(path, json.dumps(batches, indent=0))
    # a later round checks again the concepts in runs/match/tier2_recheck.jsonl (the review assist's objections to
    # confirmed answers, and its candidates for concepts with no milestone), once each, with the objection in hand
    t2 = [n for n in batches if n.startswith('tier2-')]
    if os.path.exists(RECHECK) and all(research_problems(run, n) is None for n in t2):
        done = {i for n in t2 if batches[n].get('recheck') for i in batches[n]['ids']}
        ids = list(dict.fromkeys(r['concept_id'] for r in read_jsonl(RECHECK)[0] if r['concept_id'] not in done))
        rnd = 1 + max((batches[n].get('round', 1) for n in t2), default=0)
        batches.update({f'tier2-{len(t2) + i // TIER2_BATCH + 1:03d}': {'ids': ids[i:i + TIER2_BATCH], 'round': rnd, 'recheck': True}
                        for i in range(0, len(ids), TIER2_BATCH)})
        if ids:
            write_atomic(path, json.dumps(batches, indent=0))
    return batches


def first_pass_dated(run, name):
    """The concepts a tier1 batch gave a scoring milestone (a demonstration or a practical use)."""
    return {r['concept_id'] for r in read_jsonl(rd(run, 'research', 'out', name + '.jsonl'))[0]
            if r.get('kind') in ('first_demonstration', 'first_practical_use')}


def research_inputs(run, name):
    return {r['concept_id']: r for r in read_jsonl(rd(run, 'research', 'in', name + '.jsonl'))[0]}


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
    if not name.startswith('tier2-'):
        for r in rows:
            if 'kind' in r:
                bad += milestone_problems(r, ids)
        return bad or None
    # tier 2: one verdict for each milestone it was given, `added` only for a kind it wasn't
    given = {(c, m['kind']): m for c, r in research_inputs(run, name).items() for m in r['milestones']}
    got = collections.Counter((r.get('concept_id'), r.get('kind')) for r in rows if 'checked' in r)
    bad += [f'{c} {k}: no verdict' for c, k in given if not got[(c, k)]]
    bad += [f'{c} {k}: {n} rows' for (c, k), n in got.items() if n > 1]
    for r in rows:
        if 'checked' not in r:
            continue
        k, where = (r.get('concept_id'), r.get('kind')), f"{r.get('concept_id')} {r.get('kind')}"
        if r.get('kind') not in TIER2_KINDS or r['checked'] not in VERDICTS or (r['checked'] == 'added') == (k in given):
            bad.append(f'{where}: checked {r["checked"]!r}')
        elif r['checked'] == 'removed':
            if not str(r.get('note', '')).strip():
                bad.append(f'{where}: removed without a note')
        else:
            bad += milestone_problems(r, ids)
            if r['checked'] == 'confirmed' and DATE.match(str(r.get('date', ''))) and \
                    date_key(r['date'])[0] != date_key(given[k]['date'])[0]:
                bad.append(f"{where}: confirmed with another year ({given[k]['date']} -> {r['date']})")
    top = collections.Counter(r.get('note') for r in rows if 'checked' in r).most_common(1)
    if top and top[0][1] > 2:
        bad.append(f'{top[0][1]} identical notes: {top[0][0]!r}')
    return bad or None


def milestone_problems(r, ids):
    """What is wrong with one researched milestone: its id, kind, date, fit and sources."""
    where = f"{r.get('concept_id')} {r.get('kind')}"
    bad = []
    if r.get('concept_id') not in ids or r.get('kind') not in KINDS or not DATE.match(str(r.get('date', ''))):
        bad.append(f'{where}: id, kind or date {r.get("date")!r}')
    srcs = r.get('sources')
    if not isinstance(srcs, list) or not 1 <= len(srcs) <= 3 or not str(r.get('fit', '')).strip():
        return bad + [f'{where}: sources or fit']
    for s in srcs:
        if not isinstance(s, dict) or not s.get('url') or not s.get('quote') or len(str(s['quote']).split()) > 25 \
                or s.get('kind') not in ('contemporary', 'reference'):
            bad.append(f'{where}: source {str(s)[:80]}')
    return bad


def research_plan(run, limit=None, only=''):
    """Claim up to `limit` research batches (whose names start with `only`) that aren't done or claimed
    in the last CLAIM_MINUTES and print their prompts (tier-1 research, the quick check for concepts
    guessed never to have come true, the second look, or tier 2's check of the deciding milestones)."""
    stage = 'research'
    files = {'tier1': 'milestones_tier1.md', 'check': 'milestones_check.md', 'recheck': 'milestones_recheck.md',
             'tier2': 'milestones_tier2.md'}
    tpl = {k: open(template(f), encoding='utf-8').read() for k, f in files.items()}
    config(run, stage, {'tier1_prompt_sha256': sha(tpl['tier1']), 'check_prompt_sha256': sha(tpl['check']),
                        'recheck_prompt_sha256': sha(tpl['recheck']), 'tier2_prompt_sha256': sha(tpl['tier2']),
                        'batch': RESEARCH_BATCH, 'check_batch': CHECK_BATCH, 'recheck_batch': RECHECK_BATCH,
                        'tier2_batch': TIER2_BATCH})
    batches = research_batches(run)
    reg = {c['concept_id']: c for c in registry_rows()}
    # tier 2: each concept's verified milestones and the earlier notes, as tier 1 left them
    current, earlier = collections.defaultdict(list), collections.defaultdict(list)
    if any(n.startswith('tier2-') for n in batches):
        again = {i for n, b in batches.items() if b.get('recheck') for i in b['ids']}  # these see tier 2's answer
        for m in read_jsonl(os.path.join(OUT, 'milestones.jsonl'))[0]:
            if m['kind'] in TIER2_KINDS and (m['tier'] != 2 or m['concept_id'] in again):
                current[m['concept_id']].append({k: m[k] for k in ('kind', 'date', 'what', 'fit', 'sources', 'confidence',
                                                                   'note', 'searched') if m.get(k)})
        for r in read_jsonl(os.path.join(OUT, 'milestone_notes.jsonl'))[0]:
            if r.get('concept_note') and not r['batch'].startswith('tier2-'):
                earlier[r['concept_id']].append(r['concept_note'])
        # the reviews' decisions too: the first round went without the pilot's, and reopened them
        for f in (PILOT_REVIEW, REVIEW):
            for r in read_jsonl(f)[0] if os.path.exists(f) else []:
                earlier[r['concept_id']].append(f"Review decision on {r['kind']}: {r['reason']}")
        for r in read_jsonl(RECHECK)[0] if os.path.exists(RECHECK) else []:
            earlier[r['concept_id']].append(f"A second reader objected to {r['kind'] or 'the milestones'} ({r['objection']}): "
                                            f"{r['reason']} Check this claim with sources before you confirm or replace.")
    first = {}  # recheck: the first researcher's concept note
    for n in batches:
        if n.startswith('tier1-') and research_problems(run, n) is None:
            first.update({r['concept_id']: r['concept_note'] for r in read_jsonl(rd(run, stage, 'out', n + '.jsonl'))[0]
                          if 'concept_note' in r})
    todo, now = [], time.time()
    for name, b in batches.items():
        inp = rd(run, stage, 'in', name + '.jsonl')
        if not os.path.exists(inp) and name.startswith('tier2-'):  # no claims, leads or points either
            write_atomic(inp, jsonl({**{k: reg[i].get(k) for k in ('concept_id', 'name', 'definition', 'type', 'aliases')},
                                     'milestones': current[i], 'earlier_notes': earlier[i]} for i in b['ids']))
        elif not os.path.exists(inp):  # definitions only: the researchers never see claims (PLAN §5)
            write_atomic(inp, jsonl({**{k: reg[i].get(k) for k in ('concept_id', 'name', 'definition', 'type', 'aliases', 'came_true_guess')},
                                     **({'first_pass_note': first.get(i, '')} if name.startswith('recheck-') else {})}
                                    for i in b['ids']))
        mark = rd(run, stage, 'prompts', name + '.claimed')
        if not name.startswith(only) or research_problems(run, name) is None or \
                (os.path.exists(mark) and now - os.path.getmtime(mark) < CLAIM_MINUTES * 60):
            continue
        todo.append(name)
    todo.sort(key=lambda n: (not n.startswith('check-'), n))  # the checks first: they may add tier-1 batches
    pick = todo[:int(limit)] if limit else todo
    for name in pick:
        path = prompt(run, stage, name, files[name.split('-')[0]],
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
      - for each concept and kind, the earliest verified milestone is kept;
      - then tier 2's verdicts on the deciding milestones override them: a confirmed, replaced or
        added milestone with a verified source takes the place of the earlier one (`tier` 2, with
        `previous_date` and `checked`), a removed one is dropped, and an answer whose sources all
        fail leaves the earlier milestone in place, marked `tier2_rejected`. The checkpoint-3
        table goes to runs/match/deciding_milestones.md;
      - checkpoint 3's decisions in runs/match/milestone_review.jsonl (one row per concept and kind:
        `decision` keep_previous or accept, the `tier2_date` it was made on, and a `reason`) come
        last: keep_previous leaves the earlier milestone in place, marked `tier2_overruled`, and the
        overruled answer goes to the notes. A row whose tier-2 answer has another date stops the run.
    The verdicts are cached in work/match/<run>/research/quote_check.jsonl (url, quote, verdict, record
    date: never page text), so a re-run only fetches new sources and those that failed to fetch. Concept notes, the checks'
    verdicts, and tier 2's removals and fallbacks go to runs/match/milestone_notes.jsonl."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sources
    from concurrent.futures import ThreadPoolExecutor
    batches = research_batches(run)
    ms, ms2, notes = [], [], []
    for name in batches:
        if research_problems(run, name) is not None:
            continue
        for r in read_jsonl(rd(run, 'research', 'out', name + '.jsonl'))[0]:
            if 'checked' in r:
                ms2.append(dict(r, batch=name))
            elif 'kind' in r:
                ms.append(dict(r, batch=name))
            elif 'concept_note' in r or 'verdict' in r:
                notes.append(dict(r, batch=name))
    cache_path = rd(run, 'research', 'quote_check.jsonl')
    cache = {(c['url'], c.get('volume_id'), c['quote']): c for c in (read_jsonl(cache_path)[0] or [])} \
        if os.path.exists(cache_path) else {}
    # a fetch that failed (a 429, a timeout) is tried again on the next run
    need = {(s['url'], s.get('volume_id'), s['quote'].strip()) for m in ms + ms2 for s in m.get('sources') or []} - \
        {k for k, c in cache.items() if not c['verdict'].startswith('fetch failed')}
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
    log = collections.Counter()

    def checked(m, tier):
        """The milestone with only its verified sources, or None if none is left."""
        ey = date_key(m['date'])[0]
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
            return None
        conf = m.get('confidence') if m.get('confidence') in ('high', 'medium', 'low') else 'low'
        if conf == 'high' and not {'contemporary', 'reference'} <= {s['kind'] for s in keep}:
            conf = 'medium'
        return {'concept_id': m['concept_id'], 'kind': m['kind'], 'date': m['date'], 'what': m.get('what', ''),
                'fit': m['fit'], 'sources': keep, 'confidence': conf,
                **{k: m[k] for k in ('note', 'searched') if m.get(k)}, 'tier': tier, 'batch': m['batch']}
    best = {}
    for m in ms:
        r = checked(m, 1)
        if r is None:
            log['milestone dropped'] += 1
            continue
        k = (r['concept_id'], r['kind'])
        if k not in best or date_key(r['date']) < date_key(best[k]['date']):
            best[k] = r
    researched = {i for n, b in batches.items() if not n.startswith('tier2-') for i in b['ids']}
    pilot = [dict(r, tier='pilot') for r in map(json.loads, open(PILOT_MILESTONES, encoding='utf-8'))
             if r['concept_id'] not in researched]
    if TRANCHE == 'B':  # tranche A's verified milestones (they include the pilot's) for its concepts
        pilot = [r for r in read_jsonl(os.path.join(ROOT, 'runs', 'match', 'milestones.jsonl'))[0] if r['concept_id'] not in researched]
    keyed = {(r['concept_id'], r['kind']): r for r in pilot + list(best.values())}
    # tier 2 overrides (PLAN §5): its verdict replaces the milestone, `removed` drops it, and an answer
    # with no verified source leaves the earlier milestone in place, marked; checkpoint 3's review can
    # keep the earlier milestone instead (`keep_previous`)
    review = {(r['concept_id'], r['kind']): r for r in read_jsonl(REVIEW)[0]} if os.path.exists(REVIEW) else {}
    answers = {(m['concept_id'], m['kind']): m.get('date') for m in ms2}  # a `removed` verdict has no date
    for k, rv in review.items():
        if rv.get('decision') not in ('keep_previous', 'accept') or answers.get(k, '') != rv.get('tier2_date'):
            sys.exit(f'milestone_review.jsonl: {k} has no tier-2 answer dated {rv.get("tier2_date")!r}, '
                     f'or the decision {rv.get("decision")!r} is not keep_previous or accept')
    for m in ms2:
        k, prev = (m['concept_id'], m['kind']), keyed.get((m['concept_id'], m['kind']))
        before = {'previous_date': prev['date'] if prev else None, 'checked': m['checked']}
        log['tier 2 ' + m['checked']] += 1
        if review.get(k, {}).get('decision') == 'keep_previous':
            log['tier 2 overruled on review'] += 1
            if prev:
                prev['tier2_overruled'] = f"{m['checked']} {m['date']}: {review[k]['reason']}"
            notes.append({'concept_id': m['concept_id'], 'kind': m['kind'], **before, 'date': m['date'],
                          'overruled': review[k]['reason'],
                          **{f: m[f] for f in ('what', 'fit', 'sources', 'note', 'batch') if m.get(f)}})
            continue
        if m['checked'] == 'removed':
            keyed.pop(k, None)
            notes.append({'concept_id': m['concept_id'], 'kind': m['kind'], **before,
                          **{f: m[f] for f in ('note', 'searched', 'batch') if m.get(f)}})
            continue
        r = checked(m, 2)
        if r is None:
            log['tier 2 fell back'] += 1
            if prev:
                prev['tier2_rejected'] = f"{m['checked']} {m['date']}: no source verified"
            notes.append({'concept_id': m['concept_id'], 'kind': m['kind'], **before, 'date': m['date'],
                          'fell_back': True, **{f: m[f] for f in ('what', 'note', 'batch') if m.get(f)}})
            continue
        keyed[k] = {**r, **before}
    rows = sorted(keyed.values(), key=lambda r: (r['concept_id'], KINDS.index(r['kind'])))
    for c, d in itertools.groupby(rows, key=lambda r: r['concept_id']):
        d = {r['kind']: r['date'] for r in d}
        if {'first_practical_use', 'first_demonstration'} <= d.keys() and \
                date_key(d['first_practical_use'])[0] < date_key(d['first_demonstration'])[0]:
            print(f'WARNING {c}: practical use {d["first_practical_use"]} before demonstration {d["first_demonstration"]}')
    write_atomic(os.path.join(OUT, 'milestones.jsonl'), jsonl(rows))
    write_atomic(os.path.join(OUT, 'milestone_notes.jsonl'), jsonl(sorted(notes, key=lambda r: r['concept_id'])))
    print(f"{len(ms)} researched milestones -> {len(best)} kept for {len({k[0] for k in best})} concepts, "
          f"plus {len(pilot)} pilot rows, {len(ms2)} tier-2 verdicts; {dict(log)}")
    if ms2:
        deciding_report(run)


def deciding_report(run):
    """runs/match/deciding_milestones.md, checkpoint 3 (PLAN §5): each checked deciding concept's
    scoring milestone at the first scoring and after tier 2, with its event, sources, confidence and
    fit, and how many pairs change and must be judged again (their pair id hashes the milestone)."""
    batches = research_batches(run)
    t2 = sorted(n for n in batches if n.startswith('tier2-'))
    done = [n for n in t2 if research_problems(run, n) is None]
    ids = {i for n in done for i in batches[n]['ids']}
    deciding = [d for d in read_jsonl(os.path.join(OUT, 'deciding.jsonl'))[0] if d['concept_id'] in ids]
    new, ms = scoring_milestones(), read_jsonl(os.path.join(OUT, 'milestones.jsonl'))[0]
    verdicts = collections.defaultdict(dict)
    for m in ms:
        if m['tier'] == 2:
            verdicts[m['concept_id']][m['kind']] = m['checked']
    side = [r for r in read_jsonl(os.path.join(OUT, 'milestone_notes.jsonl'))[0]
            if r.get('batch', '').startswith('tier2-') and 'kind' in r]
    for r in side:
        verdicts[r['concept_id']][r['kind']] = 'fell back' if r.get('fell_back') else \
            r['checked'] + ', overruled' if r.get('overruled') else 'removed'
    rounds = judge_rounds(run)
    old, pairs = {p['pair'] for r in rounds for p in r}, judge_pairs(run)
    now, fresh = {p['pair'] for p in pairs}, [p for p in new_pairs(rounds, pairs) if 'reuse' not in p]
    again = collections.Counter(p['concept_id'] for p in fresh)
    again_b = sum(1 for p in fresh if p['polarity'] == 'will')
    rv = read_jsonl(REVIEW)[0] if os.path.exists(REVIEW) else []
    short = {'first_demonstration': 'demo.', 'first_practical_use': 'use'}

    def esc(s):
        return str(s).replace('|', '\\|').replace('\n', ' ')

    def srcs(m):
        n = collections.Counter(s['kind'] for s in m['sources'])
        return ', '.join(f'{n[k]} {k}' for k in ('contemporary', 'reference') if n[k])

    changed, same, moves = [], [], collections.Counter()
    for i, d in enumerate(deciding, 1):
        c, m = d['concept_id'], new.get(d['concept_id'])
        name = esc(d['name']) + (f" (round {d['round']})" if d.get('round', 1) > 1 else '')
        before = f"{d['milestone_date']} ({short[d['milestone_kind']]})"
        tier2 = '; '.join(f'{short[k]} {v}' for k, v in sorted(verdicts[c].items()))
        if m is None:
            moves['no scoring milestone left'] += 1
            changed.append(f"| {name} | {d['points']:.0f} | {before} | **none** | {tier2} | | | | | "
                           f"{again[c]} |")
            continue
        after = f"{m['date']} ({short[m['kind']]})"
        unchanged = (m['kind'], m['date']) == (d['milestone_kind'], d['milestone_date'])
        (same if unchanged else changed).append(
            f"| {name} | {d['points']:.0f} | {before} | {after if unchanged else '**' + after + '**'} | {tier2} | "
            f"{esc(m.get('what', ''))} | {srcs(m)} | {m['confidence']} | {esc(m.get('fit', ''))} | {again[c]} |")
        if not unchanged:
            dy = date_key(m['date'])[0] - date_key(d['milestone_date'])[0]
            moves['earlier' if dy < 0 else 'later' if dy > 0 else 'same year, other month or kind'] += 1
    head = ['| Concept | Points | Before tier 2 | After tier 2 | Tier 2 | Event | Sources | Confidence | Fit | Pairs to judge |',
            '|---|---|---|---|---|---|---|---|---|---|']
    tally = collections.Counter(v.split(',')[0] for c in ids for v in verdicts[c].values())
    overruled = sum(v.endswith('overruled') for c in ids for v in verdicts[c].values())
    contemporary = sum(1 for d in deciding if new.get(d['concept_id']) and
                       any(s['kind'] == 'contemporary' for s in new[d['concept_id']]['sources']))
    nround = max((d.get('round', 1) for d in deciding), default=1)
    out = ['# The deciding milestones: checkpoint 3 (runs/match/PLAN.md §5)', '',
           f'Tier 2 checked {len(deciding)} of the deciding concepts ({len(done)} of {len(t2)} batches'
           + (f', in {nround} rounds' if nround > 1 else '') + '): '
           f'`prompts/milestones_tier2.md`, an adversarial earliest-event check of each concept\'s demonstration '
           f'and practical use with a search for contemporary sources, every quote fetched again by `match.py verify`. '
           f"The concepts are in the order the scorings selected them (`runs/match/deciding.jsonl`: the first "
           f"scoring's, then each later round's newcomers, marked with their round); points and the milestone before "
           f"tier 2 are from the scoring that selected the concept.", '',
           f"- **Verdicts:** {', '.join(f'{v} {tally[v]}' for v in (*VERDICTS, 'fell back') if tally[v])}"
           + (' (fell back: no source of the answer verified, so the earlier milestone stays).' if tally['fell back'] else '.')
           + (f' {overruled} overruled on review, which keeps the earlier milestone.' if overruled else ''),
           f"- **Scoring milestone changed** for {len(changed)} of {len(deciding)} concepts: "
           f"{', '.join(f'{k} {v}' for k, v in moves.most_common())}.",
           f'- **Contemporary sources:** {contemporary} of {len(deciding)} scoring milestones have one now, '
           f"{sum(d['contemporary'] for d in deciding)} had one before tier 2.",
           f'- **Judging again:** {len(now - old):,} pairs are in no judging round yet, and {len(old - now):,} judged '
           f'pairs are no longer current. {len(now - old) - len(fresh):,} of the new pairs copy the judgments of an '
           f'earlier pair, since tier 2 '
           f'confirmed the same event in the same kind and year and only the date got more precise; the other '
           f'{len(fresh):,} go to both judges (judge A all, judge B the {again_b:,} `will` pairs).', '',
           (f"Checkpoint 3's decisions are in `runs/match/milestone_review.jsonl`: {len(rv)} rows, "
            f"{sum(r['decision'] == 'keep_previous' for r in rv)} of them keeping the earlier milestone. " if rv else
            'Decisions on any row go in `runs/match/milestone_review.jsonl` before the re-judging. ') +
           'Each concept\'s notes, the candidates the researcher rejected and what it searched are in '
           '`runs/match/milestones.jsonl` and `milestone_notes.jsonl`.', '',
           f'## Scoring milestone changed ({len(changed)})', '', *head, *changed, '',
           f'## Scoring milestone unchanged ({len(same)})', '', *head, *same, '']
    if side:
        out += ['## Removed, fell back, or overruled on review', '', '| Concept | Kind | Before | Verdict | Note |',
                '|---|---|---|---|---|']
        out += [f"| {r['concept_id']} | {short[r['kind']]} | {r.get('previous_date') or ''} | "
                f"{'fell back (' + r['date'] + ')' if r.get('fell_back') else 'overruled on review (' + r['date'] + ')' if r.get('overruled') else 'removed'} | "
                f"{esc(r.get('overruled') or r.get('note', ''))} |"
                for r in sorted(side, key=lambda r: (r['concept_id'], r['kind']))]
    write_atomic(os.path.join(OUT, 'deciding_milestones.md'), '\n'.join(out) + '\n')
    print(f'{len(deciding)} deciding concepts checked, {len(changed)} scoring milestones changed, '
          f'{len(fresh):,} pairs to judge -> runs/match/deciding_milestones.md')


# ---- usage and status ----

# ---- §6–7: pairs and judging ----

JUDGE_BATCH, SCORES = 200, (0, 0.25, 0.5, 0.75, 1)
JUDGE_FIELDS = ('pair', 'pub_year', 'quote', 'claim_description', 'polarity', 'concept_name', 'concept_description',
                'milestone_kind', 'milestone_date', 'milestone_summary')


def scoring_milestones():
    """concept -> its scoring milestone (PLAN §6): first_practical_use, else first_demonstration."""
    best = {}
    for m in read_jsonl(os.path.join(OUT, 'milestones.jsonl'))[0]:
        if m['kind'] == 'first_practical_use' or (m['kind'] == 'first_demonstration' and m['concept_id'] not in best):
            best[m['concept_id']] = m
    return best


def pair_id(claim, concept, m):
    return 'p' + sha('|'.join((claim, concept, m['kind'], m['date'])))[:10]


def judge_pairs(run):
    """Every claim–concept pair whose concept's scoring milestone is dated after the claim's year (a
    lead of zero or less scores 0 by rule, PLAN §6). The pair id hashes the claim, the concept and
    the milestone's kind and date, so a later round can copy every judgment whose pair is unchanged."""
    best, cl = scoring_milestones(), {c['id']: c for c in claims(run)}
    reg = {c['concept_id']: c for c in final_registry(run)}
    pairs = []
    for r in read_jsonl(rd(run, 'matches.jsonl'))[0]:
        c = cl[r['id']]
        for k in r['concepts']:
            m = best.get(k)
            if m is None or c.get('year') is None or date_key(m['date'])[0] <= c['year']:
                continue
            pairs.append({'pair': pair_id(r['id'], k, m), 'claim': r['id'],
                          'concept_id': k, 'lead': date_key(m['date'])[0] - c['year'], 'type': reg[k].get('type'),
                          'pub_year': c['year'], 'quote': c['quote'], 'claim_description': c['description'],
                          'polarity': c['polarity'], 'concept_name': reg[k]['name'],
                          'concept_description': reg[k]['definition'], 'milestone_kind': m['kind'],
                          'milestone_date': m['date'], 'milestone_summary': m.get('what', '')})
    return pairs


def round_path(run, n):
    return rd(run, 'judge', 'pairs.jsonl' if n == 1 else f'pairs-{n}.jsonl')


def judge_rounds(run):
    """The pairs of each judging round, in order: judge/pairs.jsonl, then pairs-2.jsonl, ..."""
    rounds = []
    while os.path.exists(round_path(run, len(rounds) + 1)):
        rounds.append(read_jsonl(round_path(run, len(rounds) + 1))[0])
    return rounds


def new_pairs(rounds, pairs):
    """The pairs no earlier round has. One whose milestone tier 2 confirmed in the same kind and year
    (the same event; only the date got more precise, and lead counts whole years) gets `reuse`: the
    earlier pair whose judgments it copies instead of being judged again."""
    root = {p['pair']: p.get('reuse', p['pair']) for r in rounds for p in r}
    best, out = scoring_milestones(), []
    for p in pairs:
        if p['pair'] in root:
            continue
        m = best[p['concept_id']]
        prev = m.get('previous_date')
        if m.get('checked') == 'confirmed' and prev and date_key(prev)[0] == date_key(m['date'])[0]:
            old = pair_id(p['claim'], p['concept_id'], {'kind': m['kind'], 'date': prev})
            if old in root:
                p = dict(p, reuse=root[old])
        out.append(p)
    return out


def milestones_settled(run):
    rb = research_batches(run)
    if any(research_problems(run, n) is not None for n in rb):
        sys.exit('research is not done')
    last = max([os.path.getmtime(rd(run, 'research', 'out', n + '.jsonl')) for n in rb] +
               ([os.path.getmtime(REVIEW)] if os.path.exists(REVIEW) else []))
    if last > os.path.getmtime(os.path.join(OUT, 'milestones.jsonl')):
        sys.exit('a research output or milestone_review.jsonl is newer than milestones.jsonl: run verify first')


def judge_batches(run):
    """judge/batches.json and the rounds' pairs, each round fixed once from the verified milestones:
    judge A scores every pair and judge B every `will` pair (a `will_not` claim scores no points, so
    one judge is enough, PLAN §6), each in its own fixed-seed shuffle, in mixed batches of
    JUDGE_BATCH. When A and B are done, the pairs they score two or more steps apart go to judge C.
    When every batch is done and the milestones have changed since the last round (tier 2 and its
    review, PLAN §5), the pairs no round has go to a new round, judge/pairs-<n>.jsonl, whose batches
    continue the numbering; a pair whose event tier 2 only dated more precisely copies its earlier
    judgments instead (new_pairs)."""
    path = rd(run, 'judge', 'batches.json')
    if os.path.exists(path):
        batches = json.load(open(path, encoding='utf-8'))
    else:
        milestones_settled(run)
        pairs = judge_pairs(run)
        write_atomic(round_path(run, 1), jsonl(pairs))
        batches = {}
        for j in 'AB':
            ids = sorted(p['pair'] for p in pairs if j == 'A' or p['polarity'] == 'will')
            random.Random(f'{SEED}:judge{j}').shuffle(ids)
            batches.update({f'{j}-{i // JUDGE_BATCH + 1:03d}': {'pairs': ids[i:i + JUDGE_BATCH]}
                            for i in range(0, len(ids), JUDGE_BATCH)})
        write_atomic(path, json.dumps(batches, indent=0))
    if not all(judge_problems(run, n) is None for n in batches):
        return batches
    a, b = judge_scores(run, batches, 'A'), judge_scores(run, batches, 'B')
    in_c = {p for n in batches if n.startswith('C-') for p in batches[n]['pairs']}
    far = sorted(p for p in b if abs(a[p]['score'] - b[p]['score']) >= 0.5 and p not in in_c)
    if far:
        k = sum(n.startswith('C-') for n in batches)
        random.Random(f'{SEED}:judgeC' + (f':{k}' if k else '')).shuffle(far)
        batches.update({f'C-{k + i // JUDGE_BATCH + 1:03d}': {'pairs': far[i:i + JUDGE_BATCH]}
                        for i in range(0, len(far), JUDGE_BATCH)})
        write_atomic(path, json.dumps(batches, indent=0))
        return batches
    rounds = judge_rounds(run)
    if os.path.getmtime(os.path.join(OUT, 'milestones.jsonl')) > os.path.getmtime(round_path(run, len(rounds))):
        milestones_settled(run)
        new, n = new_pairs(rounds, judge_pairs(run)), len(rounds) + 1
        if new:
            write_atomic(round_path(run, n), jsonl(new))
            for j in 'AB':
                ids = sorted(p['pair'] for p in new if 'reuse' not in p and (j == 'A' or p['polarity'] == 'will'))
                random.Random(f'{SEED}:judge{j}:{n}').shuffle(ids)
                k = sum(x.startswith(j + '-') for x in batches)
                batches.update({f'{j}-{k + i // JUDGE_BATCH + 1:03d}': {'pairs': ids[i:i + JUDGE_BATCH], 'round': n}
                                for i in range(0, len(ids), JUDGE_BATCH)})
            write_atomic(path, json.dumps(batches, indent=0))
    return batches


def judge_problems(run, name):
    """None if the batch's output is complete and well formed (PLAN §7), else what is wrong."""
    out, inp = rd(run, 'judge', 'out', name + '.jsonl'), rd(run, 'judge', 'in', name + '.jsonl')
    if not os.path.exists(inp):
        return ['not planned']
    if not os.path.exists(out):
        return ['missing']
    rows, err = read_jsonl(out)
    if rows is None:
        return [err]
    ids = [json.loads(l)['pair'] for l in open(inp, encoding='utf-8')]
    got = [r.get('pair') for r in rows]
    bad = [] if sorted(got) == sorted(ids) else [f'{len(got)} lines for {len(ids)} pairs, or other ids']
    bad += [f"{r.get('pair')}: score {r.get('score')!r}" for r in rows if r.get('score') not in SCORES]
    bad += [f"{r.get('pair')}: no rationale" for r in rows if not str(r.get('rationale', '')).strip()]
    distinct = len({str(r.get('rationale', '')).strip().lower() for r in rows})
    if rows and distinct < 0.8 * len(rows):
        bad.append(f'{distinct} distinct rationales for {len(rows)} pairs')
    return bad or None


def judge_scores(run, batches, judge):
    return {r['pair']: r for n in batches if n.startswith(judge + '-')
            for r in read_jsonl(rd(run, 'judge', 'out', n + '.jsonl'))[0]}


def judge_plan(run, limit=None, only=''):
    """Claim up to `limit` judging batches (whose names start with `only`) that aren't done or
    claimed in the last CLAIM_MINUTES and print their prompts."""
    stage = 'judge'
    tpl = open(template('judge.md'), encoding='utf-8').read()
    config(run, stage, {'prompt_sha256': sha(tpl), 'batch': JUDGE_BATCH, 'seed': SEED})
    batches = judge_batches(run)
    pairs = {p['pair']: p for r in judge_rounds(run) for p in r}
    todo, now = [], time.time()
    for name, b in batches.items():
        inp = rd(run, stage, 'in', name + '.jsonl')
        if not os.path.exists(inp):  # no claim ids, books or authors reach the judge
            write_atomic(inp, jsonl({k: pairs[p][k] for k in JUDGE_FIELDS} for p in b['pairs']))
        mark = rd(run, stage, 'prompts', name + '.claimed')
        if not name.startswith(only) or judge_problems(run, name) is None or \
                (os.path.exists(mark) and now - os.path.getmtime(mark) < CLAIM_MINUTES * 60):
            continue
        todo.append(name)
    pick = sorted(todo)[:int(limit)] if limit else sorted(todo)
    for name in pick:
        path = prompt(run, stage, name, 'judge.md', workdir=ROOT, n=len(batches[name]['pairs']),
                      batch_in=rel(rd(run, stage, 'in', name + '.jsonl')), batch_out=rel(rd(run, stage, 'out', name + '.jsonl')),
                      tmpdir=rel(rd(run, 'tmp', stage + '-' + name)))
        write_atomic(rd(run, stage, 'prompts', name + '.claimed'), time.strftime('%Y-%m-%dT%H:%M:%S\n'))
        print(rel(path))
    done = sum(1 for n in batches if judge_problems(run, n) is None)
    print(f'{len(pick)} claimed; {len(todo) - len(pick)} more pending; {done} of {len(batches)} batches done', file=sys.stderr)


def judge_collect(run):
    """work/match/<run>/judgments.jsonl and runs/match/judging.md (PLAN §7) for the current pairs: a `will`
    pair scores the mean of judges A and B, or the median of A, B and C where A and B are two or more
    steps apart; a `will_not` pair scores judge A's. A pair a later round reuses copies its earlier
    pair's judgments. The report gives how far A and B agree: overall, by concept type, and on a
    random 300."""
    batches = judge_batches(run)  # adds the C batches once A and B are done, and a round when the milestones change
    left = [n for n in batches if judge_problems(run, n) is not None]
    if left:
        sys.exit(f'{len(left)} judging batches not done, e.g. {left[0]}')
    a, b, c = (judge_scores(run, batches, j) for j in 'ABC')
    rounds, pairs = judge_rounds(run), judge_pairs(run)
    known = {p['pair']: p for r in rounds for p in r}
    if any(p['pair'] not in known for p in pairs):
        sys.exit(f"{sum(p['pair'] not in known for p in pairs)} pairs are in no judging round: run judge-plan")
    rows = []
    for p in pairs:
        k = known[p['pair']].get('reuse', p['pair'])
        sa, sb = a[k]['score'], b[k]['score'] if k in b else None
        if sb is None:
            score = sa
        elif abs(sa - sb) >= 0.5:
            score = sorted((sa, sb, c[k]['score']))[1]
        else:
            score = (sa + sb) / 2
        rows.append({**{f: p[f] for f in ('pair', 'claim', 'concept_id', 'polarity', 'milestone_kind', 'milestone_date', 'lead')},
                     'a': sa, 'b': sb, 'c': c[k]['score'] if k in c else None, 'score': score,
                     'rationale_a': a[k]['rationale'], 'rationale_b': b[k]['rationale'] if k in b else None,
                     **({'reused_from': k} if k != p['pair'] else {})})
    write_atomic(rd(run, 'judgments.jsonl'), jsonl(rows))  # large: kept out of git, published as a release asset (PLAN §11)
    types = {p['pair']: p.get('type') or '?' for p in pairs}
    first = {p['pair'] for p in rounds[0]}

    def agree(rs):
        d = collections.Counter(min(int(abs(r['a'] - r['b']) / 0.25 + 0.5), 2) for r in rs)
        n = len(rs) or 1
        return f"{len(rs)} | {d[0] / n:.0%} | {d[1] / n:.0%} | {d[2] / n:.0%}"
    pairs2 = [r for r in rows if r['b'] is not None]
    rnd = random.Random(f'{SEED}:judge-agree').sample(pairs2, min(300, len(pairs2)))
    out = ['# Judging: how far the two judges agree (PLAN §7)', '',
           f'{len(rows)} pairs judged; {len(pairs2)} by two judges, {sum(r["c"] is not None for r in rows)} decided by a third.'
           + (f' {len(rounds)} rounds: {sum(r["pair"] in first for r in rows):,} of the pairs are from the first, '
              f'{sum("reused_from" in r for r in rows):,} copy the judgments of a first-round pair whose event tier 2 '
              f'dated more precisely, and {sum(r["pair"] not in first and "reused_from" not in r for r in rows):,} were '
              f'judged in a later round.' if len(rounds) > 1 else ''),
           f'Scores: {dict(sorted(collections.Counter(r["score"] for r in rows).items()))}', '',
           '| pairs | n | same | one step | further |', '|---|---|---|---|---|',
           f'| all | {agree(pairs2)} |', f'| random 300 | {agree(rnd)} |']
    for t in sorted({types[r["pair"]] for r in pairs2}):
        out.append(f'| type {t} | {agree([r for r in pairs2 if types[r["pair"]] == t])} |')
    write_atomic(os.path.join(OUT, 'judging.md'), '\n'.join(out) + '\n')
    print(f'{len(rows)} judgments -> work/match/{run}/judgments.jsonl; agreement in runs/match/judging.md')


# ---- scoring (PLAN §8, DESIGN §8) ----

SCORE_YEAR, GRACE = 2026, 10  # deadlines are checked against a fixed year, so a re-run gives the same result
WEIGHT, CAP = 'log', 500  # DESIGN §8: w = log2(1 + min(L, 500)); 'linear' is the comparison switch
REALIZED_MIN = 0.125  # a `will` pair with a positive lead is realized and earns points from here: every s > 0 (DESIGN §8)
STRICT_MIN = 0.5  # precision counts the claims realized at this score or more (DESIGN §8); the report also ranks at it
NEGATIVE_MIN = 0.5  # a `will_not` pair from this score resolves as contradicted_negative (PLAN §6)
AUTHOR_MIN = 5  # tier 2 also checks every concept that adds this many points to the author totals (PLAN §5, 2026-11-18)
PRECISION_CLAIMS, PPB_BOOKS = 50, 3  # the precision ranking needs this many claims, points per book this many books
ERAS = (('pre-1900', -10 ** 6, 1899), ('1900–1945', 1900, 1945), ('1946–1979', 1946, 1979), ('1980+', 1980, 10 ** 6))
NO_AUTHOR = {'Anonymous', 'Various', 'Milton S. Terry'}  # ranked by text only (DESIGN §1a); Terry translated the Sibylline Oracles
TEXT_ONLY = {'Religion'}  # corpus groups whose library author is the translator
UNITS = ('first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth '
         'fifteenth sixteenth seventeenth eighteenth nineteenth').split()
TENS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()
ORDINAL = {**{w: i + 1 for i, w in enumerate(UNITS)}, **{t[:-1] + 'ieth': 20 + 10 * i for i, t in enumerate(TENS)}}
CENTURY = re.compile(rf"\b(?:(\d{{1,2}})(?:st|nd|rd|th)|(?:({'|'.join(TENS)})[\s-])?({'|'.join(ORDINAL)}))\s+century\b", re.I)
YEAR = re.compile(r"(?<![\d,.])(\d{4})('?s\b)?(?![\d,]|\s*-?\s*(?:years?|yrs?|hours?|miles?)\b|\s*B\.?\s*C)", re.I)


def deadline(stated, pub):
    """The latest calendar year a stated time names, if it is after `pub` (PLAN §8): a year ("by 1975",
    "A.D. 2000"), or a decade's or century's last year ("the 1970s" end in 1979, "the twentieth century" in
    2000). Relative and story times ("two years", "the next century") name none."""
    if not stated or pub is None:
        return None
    ys = [int(y) + (9 if s else 0) for y, s in YEAR.findall(stated)]
    for d, t, o in CENTURY.findall(stated):
        ys.append(100 * (int(d) if d else ORDINAL[o.lower()] + (20 + 10 * TENS.index(t.lower()) if t else 0)))
    ys = [y for y in ys if y > pub]
    return max(ys) if ys else None


def weight(lead):
    return 0 if lead <= 0 else math.log2(1 + min(lead, CAP)) if WEIGHT == 'log' else min(lead, CAP)


def book_index(run, cl):
    """Opaque book id -> library path, corpus group, authors, title and year. The ids are the first 12 hex
    digits of the sha256 of the library path (export_claims.py), joined back from the extraction run
    directories; authors and titles come from the dating list, else the path. They join only here, at
    scoring, and never reach a model (PLAN §8)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from export_claims import DATES, RUNS
    listed = {r['path']: r for r in csv.DictReader(open(DATES, encoding='utf-8'), delimiter='\t')}
    review = book_review()
    years = {c['book']: c['year'] for c in cl}
    books = {}
    for r in RUNS:
        d = os.path.join(ROOT, 'work', 'extract', r, 'verified')
        for f in sorted(os.listdir(d)):
            path = json.load(open(os.path.join(d, f), encoding='utf-8'))['book']
            b = sha(path)[:12]
            if b in books:
                continue
            group, folder, base = path.split('/')
            names = listed[path]['author'].split(';') if path in listed else [folder]
            if 'authors' in review.get(path, {}):
                names = review[path]['authors'] or ['Various']
            prefix = f'{group}-{folder}-'
            title = base[:-3].split('-', 1)[1]
            title = listed[path]['title'] if path in listed else title[len(prefix):] if title.startswith(prefix) else title
            books[b] = {'book': b, 'path': path, 'group': group, 'title': title, 'year': years.get(b),
                        'authors': [] if group in TEXT_ONLY else [a.strip() for a in names if a.strip() and a.strip() not in NO_AUTHOR]}
    return books


def rankings(pairs, books, floor):
    """Book-concept entries (a book's best claim on each concept), book totals and author totals (DESIGN §8),
    from the realized pairs scoring `floor` or more. Ties go to the lower claim id, as in the pilot."""
    entry = {}
    for p in pairs:
        if p['score'] >= floor:
            e, key = {**p, 'points': round(p['score'] * weight(p['lead']), 4)}, (p['book'], p['concept_id'])
            if key not in entry or (-e['points'], e['claim']) < (-entry[key]['points'], entry[key]['claim']):
                entry[key] = e
    entries = sorted(entry.values(), key=lambda e: (-e['points'], e['claim']))
    book, author, best = collections.Counter(), collections.Counter(), {}
    for e in entries:
        book[e['book']] += e['points']
        for a in books[e['book']]['authors']:
            if (a, e['concept_id']) not in best:  # entries come best first, so the first is the author's best book
                best[a, e['concept_id']] = e
                author[a] += e['points']
    top = lambda c: sorted(c.items(), key=lambda t: (-t[1], t[0]))
    return entries, top(book), top(author), best


def score(run):
    """Resolutions, points and rankings of every tranche-A claim (PLAN §8; DESIGN §8, §8a), from the
    judgments and the scoring milestones. Writes work/match/<run>/books.jsonl and resolutions.jsonl (large,
    out of git), runs/match/scoring.md, and runs/match/deciding.jsonl (PLAN §5's tier-2 concepts; once
    tier 2 has run, a scoring only appends the concepts that carry a top entry and were never selected, as
    a new round, and the report lists the deciding concepts tier 2 has not checked).

    A claim takes the first of these that fits:
    - realized: a `will` pair with a positive lead scoring REALIZED_MIN or more; it earns points;
    - failed, contradicted_negative: a `will_not` pair with a positive lead scoring NEGATIVE_MIN or more, unless
      negative_review.jsonl found the denial vindicated (resolution `vindicated`) or about something else (open);
    - not_a_prediction: a pair whose milestone is in or before the publication year (0 by rule, PLAN §6;
      DESIGN §8a has no status for it);
    - failed, missed_deadline: a `will` claim with a concept whose stated time names a year or century that
      ended more than GRACE years before SCORE_YEAR;
    - untestable: the matcher's code;
    - open: the rest, with why (the matcher's no_concept or too_vague, no_milestone, no_year, not_matched)."""
    jpath = rd(run, 'judgments.jsonl')
    out = rd(run, 'judge', 'out')
    if max(os.path.getmtime(os.path.join(out, f)) for f in os.listdir(out)) > os.path.getmtime(jpath):
        sys.exit('a judging output is newer than judgments.jsonl: run judge-collect first')
    judged = {r['pair']: r for r in read_jsonl(jpath)[0]}
    # prompts/negative_check.md read every contradicted_negative claim again: only `contradicted` ones are a
    # skeptic proved wrong; `vindicated` denials came true, and `unrelated` ones deny something else
    npath = os.path.join(OUT, 'negative_review.jsonl')
    negative = {r['id']: r['verdict'] for r in read_jsonl(npath)[0]} if os.path.exists(npath) else {}
    cl = claims(run)
    books, best = book_index(run, cl), scoring_milestones()
    reg = {c['concept_id']: c for c in final_registry(run)}
    matches = {r['id']: r for r in read_jsonl(rd(run, 'matches.jsonl'))[0]}
    pairs, rows, stale, strict = [], [], [], collections.Counter()
    claims_of = collections.Counter()
    dl_stats = collections.Counter()
    for c in cl:
        if c['tranche'] != TRANCHE:
            continue
        mt, will, ps = matches[c['id']], c['polarity'] == 'will', []
        claims_of[c['book']] += 1
        for k in mt['concepts']:
            m = best.get(k)
            if m is None or c['year'] is None:
                ps.append({'concept_id': k, 'why': 'no_milestone' if m is None else 'no_year'})
                continue
            p = {'claim': c['id'], 'book': c['book'], 'concept_id': k, 'kind': m['kind'], 'date': m['date'],
                 'lead': date_key(m['date'])[0] - c['year']}
            if p['lead'] > 0:
                j = judged.get(pair_id(c['id'], k, m))
                if j is None:
                    stale.append(c['id'])
                    continue
                p['score'] = j['score']
                if will:
                    pairs.append(p)
            ps.append(p)
        hit = [p for p in ps if p.get('lead', 0) > 0 and p['score'] >= (REALIZED_MIN if will else NEGATIVE_MIN)]
        dl = deadline(c['stated_time'], c['year']) if will and mt['concepts'] else None
        pick = None
        if hit:
            pick = min(hit, key=lambda p: (-p['score'] * weight(p['lead']), p['concept_id']))
            res, why = ('realized', None) if will else {'vindicated': ('vindicated', None), 'unrelated': ('open', 'not_contradicted')}.get(
                negative.get(c['id']), ('failed', 'contradicted_negative'))
            strict[c['book']] += will and max(p['score'] for p in hit) >= STRICT_MIN
        elif any(p.get('lead', 1) <= 0 for p in ps):
            pick = min((p for p in ps if p.get('lead', 1) <= 0), key=lambda p: p['concept_id'])
            res, why = 'not_a_prediction', None
        elif dl is not None and dl + GRACE < SCORE_YEAR:
            res, why = 'failed', 'missed_deadline'
        elif mt['code'] == 'untestable':
            res, why = 'untestable', None
        else:
            res = 'open'
            why = mt['code'] or ('no_year' if c['year'] is None and ps else
                                 'not_matched' if any('score' in p for p in ps) else 'no_milestone')
        if dl is not None:
            dl_stats['named'] += 1
            if dl + GRACE < SCORE_YEAR:
                dl_stats['passed'] += 1
                dl_stats[res if res != 'failed' else why] += 1
        row = {'id': c['id'], 'book': c['book'], 'year': c['year'], 'polarity': c['polarity'], 'resolution': res,
               'why': why, 'deadline': dl}
        if pick:
            row.update({'concept_id': pick['concept_id'], 'milestone_kind': pick['kind'], 'milestone_date': pick['date'],
                        'lead': pick['lead'], 'score': pick.get('score'),
                        'points': round(pick['score'] * weight(pick['lead']), 4) if res == 'realized' else 0,
                        'demonstration_only': pick['kind'] == 'first_demonstration',
                        'timing_error': date_key(pick['date'])[0] - dl if dl is not None and res == 'realized' else None})
        rows.append(row)
    if stale:
        sys.exit(f'{len(stale)} pairs are not judged (milestones or matches changed since judging), e.g. {stale[0]}')
    write_atomic(rd(run, 'books.jsonl'), jsonl(dict(books[b], claims=claims_of[b], strict=strict[b]) for b in sorted(books)))
    write_atomic(rd(run, 'resolutions.jsonl'), jsonl(rows))  # large: kept out of git, as the judgments (PLAN §11)

    entries, book_rank, author_rank, author_best = rankings(pairs, books, REALIZED_MIN)
    write_atomic(rd(run, 'entries.jsonl'), jsonl(entries))  # each book's best claim per concept, for pipeline/awards.py
    quote = {c['id']: c['quote'] for c in cl if c['tranche'] == TRANCHE}
    nbooks, nclaims, nstrict = collections.Counter(), collections.Counter(), collections.Counter()
    for b, info in books.items():
        for a in info['authors']:
            nbooks[a] += 1
            nclaims[a] += claims_of[b]
            nstrict[a] += strict[b]
    era = lambda y: next((n for n, lo, hi in ERAS if y is not None and lo <= y <= hi), None)

    # PLAN §5: the deciding concepts, whose milestone carries a top entry or a share of the author totals, for tier 2
    why_k = collections.defaultdict(set)
    for e in entries[:300]:
        why_k[e['concept_id']].add('top-300 prediction')
    best_of_book = {}
    for e in entries:
        best_of_book.setdefault(e['book'], e)
    for b, _ in book_rank[:100]:
        why_k[best_of_book[b]['concept_id']].add('best entry of a top-100 book')
    for a, _ in author_rank[:100]:
        k = min((e for (aa, _), e in author_best.items() if aa == a), key=lambda e: (-e['points'], e['claim']))['concept_id']
        why_k[k].add('best entry of a top-100 author')
    for name, _, _ in ERAS:
        for e in [e for e in entries if era(books[e['book']]['year']) == name][:50]:
            why_k[e['concept_id']].add(f'top-50 entry, {name}')
    long_lead = collections.Counter(k for k, _ in {(p['concept_id'], p['claim']) for p in pairs
                                                   if p['score'] >= REALIZED_MIN and p['lead'] > 40})
    for k, n in long_lead.items():
        if n >= 20:
            why_k[k].add('lead over 40 years for 20+ claims')
    adds = collections.Counter()
    for (_, k), e in author_best.items():  # a concept's share of the author totals: each author's best entry on it
        adds[k] += e['points']
    for k, n in adds.items():
        if n >= AUTHOR_MIN:
            why_k[k].add(f'adds {AUTHOR_MIN}+ points to the author totals')
    per_k = collections.defaultdict(list)
    for e in entries:
        per_k[e['concept_id']].append(e)
    deciding = []
    for k in why_k:
        m, es = best[k], per_k[k]
        top_e = es[0]
        deciding.append({'concept_id': k, 'name': reg[k]['name'], 'reasons': sorted(why_k[k]),
                         'points': round(sum(e['points'] for e in es), 2), 'entries': len(es),
                         'claims_lead_over_40': long_lead[k], 'milestone_kind': m['kind'], 'milestone_date': m['date'],
                         'milestone': m.get('what', ''), 'confidence': m['confidence'], 'tier': m.get('tier'),
                         'contemporary': any(s['kind'] == 'contemporary' for s in m['sources']),
                         'wikipedia_only': all('wikipedia.org' in s['url'] for s in m['sources']),
                         'best_entry': {'book': top_e['book'], 'title': books[top_e['book']]['title'],
                                        'authors': books[top_e['book']]['authors'], 'year': books[top_e['book']]['year'],
                                        'points': top_e['points'], 'score': top_e['score'], 'lead': top_e['lead']}})
    deciding.sort(key=lambda d: (-d['points'], d['concept_id']))
    # deciding.jsonl is tier 2's input. Before tier 2 runs it is the first scoring's selection; after,
    # a scoring only appends the concepts that carry a top entry and were never selected, as a new
    # round, with their milestone as it was (the "before tier 2" column of the checkpoint-3 table)
    dpath, npath = os.path.join(OUT, 'deciding.jsonl'), os.path.join(OUT, 'milestone_notes.jsonl')
    checked = {r['concept_id'] for r in read_jsonl(npath)[0] if r.get('batch', '').startswith('tier2-')
               and 'concept_note' in r} if os.path.exists(npath) else set()
    after = bool(checked)
    picked = read_jsonl(dpath)[0] if after else []
    added = [dict(d, round=1 + max(p.get('round', 1) for p in picked)) for d in deciding
             if d['concept_id'] not in {p['concept_id'] for p in picked}] if after else deciding
    if added:
        write_atomic(dpath, jsonl(picked + added))

    # the report
    def cell(s, n=None):
        s = ' '.join(str(s).split()).replace('|', '\\|')
        return s if n is None or len(s) <= n else s[:n - 1].rstrip() + '…'

    def who(b):
        return '; '.join(books[b]['authors']) or '(text)'

    def bk(b):
        return f"*{cell(books[b]['title'], 60)}* ({books[b]['year']})"

    def entry_row(i, e):
        flag = ' †' if e['kind'] == 'first_demonstration' else ''
        return (f"| {i} | {e['points']:.2f} | {e['score']:g} | {e['lead']} | {cell(who(e['book']), 30)} | {bk(e['book'])} | "
                f"{cell(reg[e['concept_id']]['name'], 40)}{flag} | {e['date']} | {cell(quote[e['claim']], 110)} |")
    entry_head = ['| # | points | score | lead | author | book | concept | milestone | quote |', '|---|---|---|---|---|---|---|---|---|']
    res_n = collections.Counter((r['resolution'], r['why']) for r in rows)
    out = [f"# {'Scoring after tier 2' if after else 'First scoring'}, tranche A (PLAN §8)", '',
           f'Written by `match.py score {run}`. Settings: weight {WEIGHT} (w = log2(1 + min(L, {CAP}))), the '
           f'scoring milestone `first_practical_use` else `first_demonstration`, points from score {REALIZED_MIN:g} '
           f'(every judged score above 0), precision from {STRICT_MIN:g}, `contradicted_negative` from {NEGATIVE_MIN:g}, '
           f'deadlines checked against {SCORE_YEAR} with {GRACE} years of grace. '
           + (f"This scoring follows tier 2 (PLAN §5), which checked {len(checked)} deciding concepts, and "
              f"checkpoint 3's review (`runs/match/milestone_review.jsonl`). " if after else
              'This is the first scoring: tier 2 (PLAN §5) can still move the deciding milestones. ')
           + 'Tranche B is not scored. † = scored on a demonstration only (PLAN §14.5).', '',
           '## Resolutions', '', f'{len(rows):,} tranche-A claims from {len(claims_of):,} books.', '',
           '| resolution | claims | share |', '|---|---|---|']
    for (res, why), n in sorted(res_n.items(), key=lambda t: (-t[1], t[0][0], t[0][1] or '')):
        out.append(f"| {res}{': ' + why if why else ''} | {n:,} | {n / len(rows):.1%} |")
    timing = [r['timing_error'] for r in rows if r.get('timing_error') is not None]
    late = sorted(t for t in timing if t > 0)
    out += ['', f"Deadlines: {dl_stats['named']:,} `will` claims with a concept have a stated time naming a year, "
                f"decade or century after publication; {dl_stats['passed']:,} of those ended before {SCORE_YEAR - GRACE}. Of "
                f"these, {dl_stats['realized']:,} are realized anyway, {dl_stats['missed_deadline']:,} missed the deadline, and "
                f"{dl_stats['not_a_prediction']:,} are not a prediction. Of the {len(timing):,} realized claims with a "
                f"deadline, {len(timing) - len(late):,} came true by it and {len(late):,} after it"
                + (f" (median {late[len(late) // 2]} years late)." if late else '.'),
            '', '## The top 50 predictions', '',
            f'{len(entries):,} book–concept entries earn points (each book counts its best claim once per concept).', '']
    out += entry_head + [entry_row(i, e) for i, e in enumerate(entries[:50], 1)]
    out += ['', '## Authors: total points', '',
            f'Each author counts a concept once, from their best book. {len(author_rank):,} authors score.', '',
            '| # | author | points | concepts | books | points per book | precision |', '|---|---|---|---|---|---|---|']
    ncon = collections.Counter(a for a, _ in author_best)
    for i, (a, pts) in enumerate(author_rank[:30], 1):
        out.append(f'| {i} | {cell(a)} | {pts:.1f} | {ncon[a]} | {nbooks[a]} | {pts / nbooks[a]:.1f} | '
                   f'{nstrict[a] / nclaims[a]:.0%} of {nclaims[a]} |')
    out += ['', '## Books: total points', '', '| # | book | author | group | points | concepts |', '|---|---|---|---|---|---|']
    nent = collections.Counter(e['book'] for e in entries)
    for i, (b, pts) in enumerate(book_rank[:30], 1):
        out.append(f"| {i} | {bk(b)} | {cell(who(b), 40)} | {books[b]['group']} | {pts:.1f} | {nent[b]} |")
    prec = sorted(((nstrict[a] / nclaims[a], a) for a in nclaims if nclaims[a] >= PRECISION_CLAIMS), key=lambda t: (-t[0], t[1]))
    out += ['', '## Precision', '',
            f'Claims realized at a score of {STRICT_MIN:g} or more, of all tranche-A claims by the author; authors with '
            f'{PRECISION_CLAIMS} or more ({len(prec)}).', '', '| # | author | precision | claims | points |', '|---|---|---|---|---|']
    pts_a = dict(author_rank)
    for i, (v, a) in enumerate(prec[:20], 1):
        out.append(f'| {i} | {cell(a)} | {v:.0%} | {nclaims[a]} | {pts_a.get(a, 0):.1f} |')
    ppb = sorted(((pts / nbooks[a], a) for a, pts in author_rank if nbooks[a] >= PPB_BOOKS), key=lambda t: (-t[0], t[1]))
    out += ['', '## Points per book', '', f'Authors with {PPB_BOOKS} or more books in the corpus ({len(ppb)}); every '
            f'book counts, including those with no tranche-A points.', '', '| # | author | points per book | books | points |',
            '|---|---|---|---|---|']
    for i, (v, a) in enumerate(ppb[:20], 1):
        out.append(f'| {i} | {cell(a)} | {v:.1f} | {nbooks[a]} | {pts_a[a]:.1f} |')
    out += ['', '## By era', '', 'The best books of each era, by publication year.', '']
    for name, _, _ in ERAS:
        rk = [(b, p) for b, p in book_rank if era(books[b]['year']) == name]
        out += [f'**{name}** ({len(rk)} books score)', '', '| # | book | author | points |', '|---|---|---|---|']
        out += [f'| {i} | {bk(b)} | {cell(who(b), 40)} | {p:.1f} |' for i, (b, p) in enumerate(rk[:10], 1)] + ['']
    out += ['## Other corpus groups', '', 'The non-fiction, classics, prophecy and religious texts. Ancient and '
            'translated texts are dated by composition, the end of the scholarly range in each text\'s English Wikipedia '
            'article, pinned to a revision (DESIGN §1a; `runs/match/book_review.jsonl`); the second-translation '
            're-judging of §1a is not built. Religious texts rank by text, not by translator.', '', '| group | book | author | points | rank |', '|---|---|---|---|---|']
    pos = {b: i for i, (b, _) in enumerate(book_rank, 1)}
    for g in sorted({v['group'] for v in books.values()} - {'Science-Fiction'}):
        for b, p in [(b, p) for b, p in book_rank if books[b]['group'] == g][:3]:
            out.append(f'| {g} | {bk(b)} | {cell(who(b), 40)} | {p:.1f} | {pos[b]} |')

    s_entries, s_books, s_authors, _ = rankings(pairs, books, STRICT_MIN)
    gone = [p for p in pairs if REALIZED_MIN <= p['score'] < STRICT_MIN]
    lost = sum(e['points'] for e in entries) - sum(e['points'] for e in s_entries)
    out += ['', f'## Sensitivity: points only from a score of {STRICT_MIN:g}', '',
            f'{len(gone):,} of {len(pairs):,} judged `will` pairs score below {STRICT_MIN:g}; without them '
            f'{len(entries) - len(s_entries):,} entries and {lost:,.0f} of {sum(e["points"] for e in entries):,.0f} '
            f'points go. Of the top 30 authors, {len({a for a, _ in author_rank[:30]} & {a for a, _ in s_authors[:30]})} '
            f'stay in the top 30; of the top 30 books, {len({b for b, _ in book_rank[:30]} & {b for b, _ in s_books[:30]})}.',
            '', '| # | author (default) | points | author (from 0.5) | points |', '|---|---|---|---|---|']
    for i, ((a1, p1), (a2, p2)) in enumerate(zip(author_rank[:20], s_authors[:20]), 1):
        out.append(f'| {i} | {cell(a1)} | {p1:.1f} | {cell(a2)} | {p2:.1f} |')

    crit = collections.Counter(r for d in deciding for r in d['reasons'])
    out += ['', f"## {'The deciding concepts after tier 2' if after else 'Tier 2: the deciding concepts'} (PLAN §5)", '',
            (f'{len(deciding)} concepts carry a top entry or add {AUTHOR_MIN}+ points to the author totals now; tier 2 checked '
             f'{sum(d["concept_id"] in checked for d in deciding)} of them (`runs/match/deciding.jsonl` lists every '
             f'concept selected for it, by round). By criterion (a concept can meet several):' if after else
             f'{len(deciding)} concepts carry a top entry; `runs/match/deciding.jsonl` lists them all with their '
             f'scoring milestone. By criterion (a concept can meet several):'), '']
    out += [f'- {r}: {n}' for r, n in sorted(crit.items())]
    conf = collections.Counter(d['confidence'] for d in deciding)
    out += ['', f"Their milestones: confidence {', '.join(f'{k} {v}' for k, v in sorted(conf.items()))}; "
                f"{sum(d['contemporary'] for d in deciding)} have a contemporary source, "
                f"{sum(d['wikipedia_only'] for d in deciding)} rest on Wikipedia alone, "
                f"{sum(d['milestone_kind'] == 'first_demonstration' for d in deciding)} are demonstrations only.", '',
            'The 40 that carry the most points' + (', and every one tier 2 did not check:' if after else ':'), '',
            '| concept | points | entries | lead > 40 | milestone | confidence | sources | best entry |'
            + (' tier 2 |' if after else ''), '|---|---|---|---|---|---|---|---|' + ('---|' if after else '')]
    for i, d in enumerate(deciding):
        if i >= 40 and (not after or d['concept_id'] in checked):
            continue
        src = 'Wikipedia only' if d['wikipedia_only'] else 'contemporary' if d['contemporary'] else 'reference'
        be = d['best_entry']
        out.append(f"| {cell(d['name'], 40)} | {d['points']:.1f} | {d['entries']} | {d['claims_lead_over_40']} | "
                   f"{d['milestone_date']}{' †' if d['milestone_kind'] == 'first_demonstration' else ''}: "
                   f"{cell(d['milestone'], 70)} | {d['confidence']} | {src} | {cell('; '.join(be['authors']) or '(text)', 25)}, "
                   f"*{cell(be['title'], 35)}* ({be['year']}) |"
                   + ((' checked |' if d['concept_id'] in checked else ' **not checked** |') if after else ''))
    write_atomic(os.path.join(OUT, 'scoring.md'), '\n'.join(out) + '\n')
    print(f'{len(rows):,} claims: ' + ', '.join(f"{res}{'/' + why if why else ''} {n:,}" for (res, why), n in res_n.most_common()))
    print(f'{len(entries):,} entries, {len(book_rank):,} books and {len(author_rank):,} authors score; '
          f'{len(deciding)} deciding concepts ({sum(d["concept_id"] not in checked for d in deciding)} not checked by tier 2) '
          f'-> runs/match/scoring.md' + (f', {len(added)} added to deciding.jsonl' if added else ''))


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
    if args:
        use_run(args[0])
    {'concepts-plan': concepts_plan, 'concepts-ingest': concepts_ingest, 'consolidate-plan': consolidate_plan,
     'consolidate-ingest': consolidate_ingest, 'global-plan': global_plan, 'audit-plan': audit_plan,
     'concepts-build': concepts_build, 'match-plan': match_plan, 'match-ingest': match_ingest,
     'rematch-plan': rematch_plan, 'matches-collect': matches_collect, 'gap-plan': gap_plan,
     'gap-ingest': lambda run: concepts_ingest(run, 'gap'), 'gapcons-plan': gapcons_plan, 'gapglobal-plan': gapglobal_plan,
     'gap-build': gap_build,
     'gapmatch-plan': gapmatch_plan, 'gap-review': gap_review, 'agree-plan': agree_plan, 'agree-report': agree_report,
     'research-plan': research_plan, 'verify': verify, 'deciding-report': deciding_report, 'judge-plan': judge_plan,
     'judge-collect': judge_collect, 'score': score,
     'b-init': b_init, 'log': log, 'status': status}[cmd](*args)
