# Review assist (advisory): a second reader for tier 2's changed milestones before the user's review.
#   python -I pipeline/review_assist.py plan <run> <base-commit> <round> [batch]   writes work/match/<run>/review/{in,prompts}
#   python -I pipeline/review_assist.py collect <run> <round>                      checks the outputs -> runs/match/milestone_review_suggestions.md
# The rows are the tier-2 answers of one round that replaced, added or removed a demonstration or practical use,
# with the milestone before tier 2 read from <base-commit>'s runs/match/milestones.jsonl. Reviewers see concept
# definitions and milestones only, never claims, books or points. Nothing here changes a milestone: the
# suggestions are for runs/match/milestone_review.jsonl, which the user decides.
import collections, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match

KINDS = ('first_demonstration', 'first_practical_use')
RECS = ('accept', 'keep_previous', 'unsure')


def rows(run, base, rnd):
    old = [json.loads(l) for l in subprocess.run(['git', 'show', f'{base}:runs/match/milestones.jsonl'], cwd=match.ROOT,
                                                  capture_output=True, text=True, check=True).stdout.splitlines()]
    new = match.read_jsonl(os.path.join(match.OUT, 'milestones.jsonl'))[0]
    notes = match.read_jsonl(os.path.join(match.OUT, 'milestone_notes.jsonl'))[0]
    ids = [d['concept_id'] for d in match.read_jsonl(os.path.join(match.OUT, 'deciding.jsonl'))[0] if d.get('round', 1) == rnd]
    reg = {c['concept_id']: c for c in match.registry_rows()}
    o, n = {(r['concept_id'], r['kind']): r for r in old}, {(r['concept_id'], r['kind']): r for r in new}
    removed = {(r['concept_id'], r['kind']) for r in notes if r.get('checked') == 'removed'}
    pick = lambda r: r and {k: r[k] for k in ('date', 'what', 'fit', 'note', 'confidence') if r.get(k)}
    out = []
    for c in ids:
        for kind in KINDS:
            k, m = (c, kind), n.get((c, kind))
            if not (m and m.get('tier') == 2 and m.get('checked') in ('replaced', 'added')) and k not in removed:
                continue
            new_m = pick(m) if k not in removed else None
            if new_m:
                new_m['sources'] = [f"{s['kind']}: {s.get('publisher', '')} {s.get('date', '')}".strip() for s in m['sources']]
            out.append({'concept_id': c, 'name': reg[c]['name'], 'definition': reg[c]['definition'],
                        'aliases': reg[c].get('aliases', []), 'kind': kind, 'old': pick(o.get(k)), 'new': new_m})
    return out


def plan(run, base, rnd, batch=30):
    rnd, batch = int(rnd), int(batch)
    tpl = open(os.path.join(match.PROMPTS, 'milestones_review_assist.md'), encoding='utf-8').read()
    rs = rows(run, base, rnd)
    d = match.rd(run, 'review')
    for sub in ('in', 'out', 'prompts'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    names = []
    for i in range(0, len(rs), batch):
        name = f'RA{rnd}-{i // batch + 1:03d}'
        inp, outp = os.path.join(d, 'in', name + '.jsonl'), os.path.join(d, 'out', name + '.jsonl')
        match.write_atomic(inp, match.jsonl(rs[i:i + batch]))
        match.write_atomic(os.path.join(d, 'prompts', name + '.md'),
                           tpl.format(input=inp, output=outp, n=len(rs[i:i + batch])))
        names.append(name)
    print(f'{len(rs)} rows in {len(names)} batches:', ' '.join(names))


def collect(run, rnd):
    d = match.rd(run, 'review')
    out, bad = [], []
    for f in sorted(os.listdir(os.path.join(d, 'in'))):
        if not f.startswith(f'RA{rnd}-'):
            continue
        inp = match.read_jsonl(os.path.join(d, 'in', f))[0]
        p = os.path.join(d, 'out', f)
        res = match.read_jsonl(p)[0] if os.path.exists(p) else []
        if [(r['concept_id'], r['kind']) for r in res] != [(r['concept_id'], r['kind']) for r in inp] or \
                any(r.get('recommendation') not in RECS or not r.get('reason') for r in res):
            bad.append(f)
            continue
        out += [dict(i, **{k: r[k] for k in ('recommendation', 'reason')}) for i, r in zip(inp, res)]
    if bad:
        sys.exit(f'not done or invalid: {bad}')
    tally = collections.Counter(r['recommendation'] for r in out)
    cell = lambda s: ' '.join(str(s).split()).replace('|', '\\|')
    show = lambda m: f"{m['date']}: {cell(m.get('what', ''))}" if m else '(none)'
    lines = [f'# Review assist: tier 2 round {rnd} (advisory)', '',
             f'A second reader (`prompts/milestones_review_assist.md`, knowledge only, no web) looked at every '
             f'demonstration or practical use that tier 2 round {rnd} replaced, added or removed, against the '
             f"concept's definition. {len(out)} rows: " + ', '.join(f'{k} {tally[k]}' for k in RECS) + '. '
             'Nothing here is applied: a decision goes in `milestone_review.jsonl` (keep_previous or accept).', '']
    for rec in ('keep_previous', 'unsure', 'accept'):
        rs = [r for r in out if r['recommendation'] == rec]
        lines += [f'## {rec} ({len(rs)})', '', '| Concept | Kind | Before tier 2 | Tier 2 | Reason |', '|---|---|---|---|---|']
        lines += [f"| {cell(r['name'])} (`{r['concept_id']}`) | {r['kind'].split('_')[1]} | {show(r['old'])} | "
                  f"{show(r['new'])} | {cell(r['reason'])} |" for r in rs]
        lines.append('')
    match.write_atomic(os.path.join(match.OUT, 'milestone_review_suggestions.md'), '\n'.join(lines))
    print(f'{len(out)} rows:', dict(tally), '-> runs/match/milestone_review_suggestions.md')


if __name__ == '__main__':
    {'plan': plan, 'collect': collect}[sys.argv[1]](*sys.argv[2:])
