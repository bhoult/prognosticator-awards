# Review assist (advisory): a second reader for tier 2's milestones, and for concepts left without one,
# before the user's review. Knowledge only (no web); nothing here changes a milestone.
#   python -I pipeline/review_assist.py plan <run> <base-commit> <round> [batch]            changed milestones -> RA<round>-NNN
#   python -I pipeline/review_assist.py plan-confirmed <run> <base-commit> <round> [batch]  confirmed ones -> RC<round>-NNN
#   python -I pipeline/review_assist.py plan-missing <run> <min-claims> [batch]             no milestone -> RM-NNN
#   python -I pipeline/review_assist.py collect|collect-confirmed <run> <round>; collect-missing <run>
# `plan` takes the tier-2 answers of one round that replaced, added or removed a demonstration or practical
# use, `plan-confirmed` those it confirmed, each beside the milestone before tier 2 (read from <base-commit>'s
# runs/match/milestones.jsonl). `plan-missing` takes the concepts with no milestone that carry at least
# <min-claims> open claims, most first. Inputs and outputs live in work/match/<run>/review; the collected
# suggestions go to runs/match/ (milestone_review_suggestions.md, milestone_review_confirmed.md,
# no_milestone_candidates.md). Reviewers see concept definitions and milestones only, never claims, books or
# points. Decisions on milestones go in runs/match/milestone_review.jsonl, which the user decides.
import collections, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match

KINDS = ('first_demonstration', 'first_practical_use')
MODES = {  # mode: (prompt, batch prefix, recommendations, output in runs/match)
    'changed': ('milestones_review_assist.md', 'RA', ('accept', 'keep_previous', 'unsure'), 'milestone_review_suggestions.md'),
    'confirmed': ('milestones_review_confirmed.md', 'RC', ('accept', 'earlier_exists', 'does_not_fit', 'unsure'),
                  'milestone_review_confirmed.md'),
    'missing': ('milestones_missing_check.md', 'RM', ('happened', 'unsure', 'never_happened'), 'no_milestone_candidates.md'),
}


def milestone_rows(base, rnd, confirmed):
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
            t2 = m and m.get('tier') == 2
            if confirmed != bool(t2 and m.get('checked') == 'confirmed') or \
                    (not confirmed and not (t2 and m.get('checked') in ('replaced', 'added')) and k not in removed):
                continue
            new_m = pick(m) if k not in removed else None
            if new_m:
                new_m['sources'] = [f"{s['kind']}: {s.get('publisher', '')} {s.get('date', '')}".strip() for s in m['sources']]
            out.append({'concept_id': c, 'name': reg[c]['name'], 'definition': reg[c]['definition'],
                        'aliases': reg[c].get('aliases', []), 'kind': kind, 'old': pick(o.get(k)), 'new': new_m})
    return out


def missing_rows(run, min_claims):
    res = {r['id']: r for r in match.read_jsonl(match.rd(run, 'resolutions.jsonl'))[0]}
    have = {m['concept_id'] for m in match.read_jsonl(os.path.join(match.OUT, 'milestones.jsonl'))[0]}
    n = collections.Counter()
    for m in match.read_jsonl(match.rd(run, 'matches.jsonl'))[0]:
        if res.get(m['id'], {}).get('why') == 'no_milestone':
            n.update(c for c in m['concepts'] if c not in have)
    notes = collections.defaultdict(list)
    for r in match.read_jsonl(os.path.join(match.OUT, 'milestone_notes.jsonl'))[0]:
        if r.get('concept_note'):
            notes[r['concept_id']].append(r['concept_note'])
    reg = {c['concept_id']: c for c in match.registry_rows()}
    return [{'concept_id': c, 'name': reg[c]['name'], 'definition': reg[c]['definition'], 'aliases': reg[c].get('aliases', []),
             'type': reg[c].get('type'), 'came_true_guess': reg[c].get('came_true_guess'), 'notes': notes[c]}
            for c, k in sorted(n.items(), key=lambda t: (-t[1], t[0])) if k >= min_claims]


def write_batches(run, mode, tag, rs, batch):
    tpl = open(os.path.join(match.PROMPTS, MODES[mode][0]), encoding='utf-8').read()
    d = match.rd(run, 'review')
    for sub in ('in', 'out', 'prompts'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    names = []
    for i in range(0, len(rs), batch):
        name = f'{MODES[mode][1]}{tag}-{i // batch + 1:03d}'
        inp, outp = os.path.join(d, 'in', name + '.jsonl'), os.path.join(d, 'out', name + '.jsonl')
        match.write_atomic(inp, match.jsonl(rs[i:i + batch]))
        match.write_atomic(os.path.join(d, 'prompts', name + '.md'),
                           tpl.format(input=inp, output=outp, n=len(rs[i:i + batch])))
        names.append(name)
    print(f'{len(rs)} rows in {len(names)} batches:', ' '.join(names))


def plan(run, base, rnd, batch=30, mode='changed'):
    write_batches(run, mode, rnd, milestone_rows(base, int(rnd), mode == 'confirmed'), int(batch))


def plan_missing(run, min_claims, batch=25):
    write_batches(run, 'missing', '', missing_rows(run, int(min_claims)), int(batch))


def collect(run, rnd='', mode='changed'):
    prompt, prefix, recs, target = MODES[mode]
    d = match.rd(run, 'review')
    out, bad = [], []
    rounds = str(rnd).split(',')  # several rounds collect into one file: 2,3,4
    for f in sorted(os.listdir(os.path.join(d, 'in'))):
        if not any(f.startswith(f'{prefix}{r}-') for r in rounds):
            continue
        inp = match.read_jsonl(os.path.join(d, 'in', f))[0]
        p = os.path.join(d, 'out', f)
        res = match.read_jsonl(p)[0] if os.path.exists(p) else []
        key = (lambda r: r['concept_id']) if mode == 'missing' else (lambda r: (r['concept_id'], r['kind']))
        if [key(r) for r in res] != [key(r) for r in inp] or \
                any(r.get('recommendation') not in recs or not r.get('reason') for r in res):
            bad.append(f)
            continue
        out += [dict(i, **{k: r[k] for k in ('recommendation', 'reason', 'kind', 'year', 'event') if k in r})
                for i, r in zip(inp, res)]
    if bad:
        sys.exit(f'not done or invalid: {bad}')
    tally = collections.Counter(r['recommendation'] for r in out)
    cell = lambda s: ' '.join(str(s).split()).replace('|', '\\|')
    show = lambda m: f"{m['date']}: {cell(m.get('what', ''))}" if m else '(none)'
    rr = 'rounds ' + ', '.join(rounds) if len(rounds) > 1 else f'round {rnd}'
    what = {'changed': f'every demonstration or practical use that tier 2 {rr} replaced, added or removed',
            'confirmed': f'every demonstration or practical use that tier 2 {rr} confirmed',
            'missing': 'the concepts with no milestone that carry the most open claims'}[mode]
    lines = [f"# Review assist: {what.split(' that ')[0] if mode != 'missing' else 'concepts with no milestone'} (advisory)", '',
             f'A second reader (`prompts/{prompt}`, knowledge only, no web) looked at {what}, against the '
             f"concept's definition. {len(out)} rows: " + ', '.join(f'{k} {tally[k]}' for k in recs) + '. '
             + ('Nothing here is applied: these are candidates for sourced research.' if mode == 'missing' else
                'Nothing here is applied: a decision goes in `milestone_review.jsonl`.'), '']
    for rec in recs:
        rs = [r for r in out if r['recommendation'] == rec]
        if mode == 'missing':
            lines += [f'## {rec} ({len(rs)})', '', '| Concept | Definition | Earliest event | Reason |', '|---|---|---|---|']
            lines += [f"| {cell(r['name'])} (`{r['concept_id']}`) | {cell(r['definition'])} | "
                      + (f"{r.get('kind', '').replace('first_', '')} {r.get('year', '')}: {cell(r.get('event', ''))}" if rec == 'happened' else '')
                      + f" | {cell(r['reason'])} |" for r in rs]
        else:
            lines += [f'## {rec} ({len(rs)})', '', '| Concept | Kind | Before tier 2 | Tier 2 | Reason |', '|---|---|---|---|---|']
            lines += [f"| {cell(r['name'])} (`{r['concept_id']}`) | {r['kind'].split('_')[1]} | {show(r['old'])} | "
                      f"{show(r['new'])} | {cell(r['reason'])} |" for r in rs]
        lines.append('')
    match.write_atomic(os.path.join(match.OUT, target), '\n'.join(lines))
    print(f'{len(out)} rows:', dict(tally), f'-> runs/match/{target}')


if __name__ == '__main__':
    cmd, a = sys.argv[1], sys.argv[2:]
    {'plan': lambda *x: plan(*x), 'plan-confirmed': lambda run, base, rnd, batch=30: plan(run, base, rnd, batch, 'confirmed'),
     'plan-missing': plan_missing, 'collect': lambda run, rnd: collect(run, rnd),
     'collect-confirmed': lambda run, rnd: collect(run, rnd, 'confirmed'),
     'collect-missing': lambda run: collect(run, '', 'missing')}[cmd](*a)
