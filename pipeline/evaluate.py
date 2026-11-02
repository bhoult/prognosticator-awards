"""Score extraction runs against the gold set. Deterministic: no model calls.

    python -I pipeline/evaluate.py <gold_dir> <runs_dir> [model ...]

runs_dir/<model>/<chunk>.json holds {"chunk": id, "claims": [...]} per chunk.
Writes <runs_dir>/report.md and report.json, and verified claims per model
(<runs_dir>/<model>/verified.jsonl) for the precision review and the judge test.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quotes import normalize, verify  # noqa: E402

GOLD, RUNS = sys.argv[1:3]
models = sys.argv[3:] or sorted(d for d in os.listdir(RUNS) if os.path.isdir(os.path.join(RUNS, d)))
chunks = {c['id']: c for c in map(json.loads, open(os.path.join(GOLD, 'chunks.jsonl'), encoding='utf-8'))}
anchors = [json.loads(l) for l in open(os.path.join(GOLD, 'anchors.jsonl'), encoding='utf-8')]


def chunk_text(cid):
    raw = open(os.path.join(GOLD, 'chunks', cid + '.txt'), encoding='utf-8').read()
    return raw.split('Passage:\n\n', 1)[1]


batch_of = {cid: n for n, ids in enumerate(json.load(open(os.path.join(GOLD, 'batches.json')))) for cid in ids}
normed = {}


def chunk_norm(cid):
    if cid not in normed:
        normed[cid] = normalize(chunk_text(cid))
    return normed[cid]


report = {}
for model in models:
    d = os.path.join(RUNS, model)
    stats = {'chunks': 0, 'missing': 0, 'bad_json': 0, 'claims': 0, 'exact': 0, 'fuzzy': 0, 'rejected': 0,
             'misfiled': 0, 'words': 0}
    verified = []
    for cid, c in chunks.items():
        path = os.path.join(d, cid + '.json')
        stats['words'] += c['words']
        if not os.path.exists(path):
            stats['missing'] += 1
            continue
        try:
            claims = json.load(open(path, encoding='utf-8'))['claims']
        except (ValueError, KeyError, TypeError):
            stats['bad_json'] += 1
            continue
        stats['chunks'] += 1
        ntext, npos = chunk_norm(cid)
        for cl in claims:
            stats['claims'] += 1
            quote = str(cl.get('quote', ''))
            home = cid
            status, at, sim = verify(quote, None, ntext, npos)
            if at is None:
                # Subagents juggling several files sometimes write a passage's claims into a
                # neighbour's file. Look in the other chunks of the same batch before rejecting.
                for other in (o for o, n in batch_of.items() if n == batch_of[cid] and o != cid):
                    status, at, sim = verify(quote, None, *chunk_norm(other))
                    if at is not None:
                        home = other
                        stats['misfiled'] += 1
                        break
            stats[status] += 1
            if at is not None:
                verified.append({**cl, 'chunk': home, 'text': chunks[home]['text'], 'offset': at,
                                 'verify': status, 'similarity': sim, 'misfiled': home != cid})
    with open(os.path.join(d, 'verified.jsonl'), 'w', encoding='utf-8') as f:
        for v in verified:
            f.write(json.dumps(v, ensure_ascii=False) + '\n')

    rows = []
    for a in anchors:
        # A hit is a verified quote overlapping the anchor phrase, give or take 150 characters.
        a0 = a['offset'] - chunks[a['chunk']]['start'] - 150
        a1 = a0 + 150 + len(a['anchor']) + 150
        hits = [v for v in verified if v['chunk'] == a['chunk']
                and v['offset'] < a1 and v['offset'] + len(str(v.get('quote', ''))) > a0]
        if a['expect'] in ('realized', 'failed'):
            ok = bool(hits)
        else:  # traps: skipped, or flagged as not speculative
            ok = all(not v.get('speculative_at_time', True) for v in hits)
        fields = {}
        if hits and 'polarity' in a:
            fields['polarity'] = any(v.get('polarity') == a['polarity'] for v in hits)
        if hits and 'confidence' in a:
            fields['confidence'] = any(v.get('confidence') == a['confidence'] for v in hits)
        if hits and 'stated_time' in a:
            fields['stated_time'] = any(v.get('stated_time') for v in hits)
        rows.append({'id': a['id'], 'expect': a['expect'], 'ok': ok, 'hits': len(hits), 'fields': fields})
    wanted = [r for r in rows if r['expect'] in ('realized', 'failed')]
    traps = [r for r in rows if r['expect'] not in ('realized', 'failed')]
    field_checks = [ok for r in rows for ok in r['fields'].values()]
    report[model] = {
        **stats,
        'recall': sum(r['ok'] for r in wanted) / len(wanted),
        'traps_ok': f"{sum(r['ok'] for r in traps)}/{len(traps)}",
        'fields_ok': f"{sum(field_checks)}/{len(field_checks)}",
        'verified_rate': (stats['exact'] + stats['fuzzy']) / max(1, stats['claims']),
        'claims_per_10k_words': 10000 * stats['claims'] / max(1, stats['words']),
        'missed': [r['id'] for r in wanted if not r['ok']],
        'traps_failed': [r['id'] for r in traps if not r['ok']],
        'rows': rows,
    }

json.dump(report, open(os.path.join(RUNS, 'report.json'), 'w'), indent=1)
lines = ['# Gold-set extraction report', '',
         '| Model | Chunks done | Claims | Per 10K words | Verified quotes | Misfiled | Recall (known predictions) | Traps handled | Field checks | Missed |',
         '|---|---|---|---|---|---|---|---|---|---|']
for m, r in report.items():
    lines.append(f"| {m} | {r['chunks']}/{len(chunks)} | {r['claims']} | {r['claims_per_10k_words']:.1f} | "
                 f"{r['verified_rate']:.0%} ({r['exact']} exact, {r['fuzzy']} fuzzy, {r['rejected']} rejected) | {r['misfiled']} | "
                 f"{r['recall']:.0%} | {r['traps_ok']} | {r['fields_ok']} | {', '.join(r['missed']) or '-'} |")
open(os.path.join(RUNS, 'report.md'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
