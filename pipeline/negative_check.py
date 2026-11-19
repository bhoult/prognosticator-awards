"""The negative check's input (prompts/negative_check.md): every contradicted_negative claim of a run, with the
`will_not` pair that decided it, in shards for one agent each.

    python -I pipeline/negative_check.py <run> <shards>

Writes work/match/<run>/awards/negatives-NN.jsonl and negative_check-NN.md. The agents' verdicts, joined in input
order, go to negative_review.jsonl in the run's output folder (runs/match/ for `full`), which `match.py score` applies.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match

ROOT = match.ROOT

run, shards = sys.argv[1], int(sys.argv[2])
match.use_run(run)
rd = lambda f: match.read_jsonl(match.rd(run, f))[0]
res = [r for r in rd('resolutions.jsonl') if r['why'] == 'contradicted_negative']
claims = {c['id']: c for c in match.claims(run)}
reg = {c['concept_id']: c for c in match.registry_rows()}
ms = {(m['concept_id'], m['kind']): m for m in match.read_jsonl(os.path.join(match.OUT, 'milestones.jsonl'))[0]}
best = {}
for j in rd('judgments.jsonl'):
    if j['polarity'] == 'will_not' and (j['lead'] or 0) > 0 and j['score'] is not None:
        if j['claim'] not in best or j['score'] > best[j['claim']]['score']:
            best[j['claim']] = j
rows = []
for r in res:
    c, j = claims[r['id']], best[r['id']]
    m = ms.get((j['concept_id'], j['milestone_kind']), {})
    rows.append({'id': r['id'], 'pub_year': c['year'], 'quote': c['quote'], 'claim_description': c['description'],
                 'concept_name': reg[j['concept_id']]['name'], 'concept_definition': reg[j['concept_id']]['definition'],
                 'milestone_date': j['milestone_date'], 'milestone': m.get('what', '')})
out = match.rd(run, 'awards')
os.makedirs(out, exist_ok=True)
tpl = open(os.path.join(ROOT, 'prompts', 'negative_check.md'), encoding='utf-8').read()
k = -(-len(rows) // shards)
for i in range(shards):
    part = rows[i * k:(i + 1) * k]
    if not part:
        continue
    inp, outp = os.path.join(out, f'negatives-{i + 1:02d}.jsonl'), os.path.join(out, f'negatives_out-{i + 1:02d}.jsonl')
    match.write_atomic(inp, match.jsonl(part))
    text = tpl.replace('{input}', inp).replace('{output}', outp).replace('{n}', str(len(part))).replace('{{', '{').replace('}}', '}')
    match.write_atomic(os.path.join(out, f'negative_check-{i + 1:02d}.md'), text)
    print(os.path.join(out, f'negative_check-{i + 1:02d}.md'), len(part))
print(len(rows), 'contradicted_negative claims')
