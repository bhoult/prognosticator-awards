"""Rule-based pre-filter: keep only the passages of a book that look like they hold predictions.

    python -I pipeline/prefilter.py tune <gold_dir> <runs_dir> <library> <out_dir>
    python -I pipeline/prefilter.py apply <filter.json> <library> <out_dir> [<book.md> ...]

A paragraph's score is the number of distinct cue words in it, summed (or maxed) over a
window of neighboring paragraphs; paragraphs scoring at least the threshold are kept.
Cue words are learned, not hand-picked: words over-represented in gold-set paragraphs where
a model recorded a speculative claim, ranked by log-odds z-score, and seen in claim
paragraphs of at least MIN_TEXTS different texts, so a character's name can't qualify.

tune: leave-one-text-out over the gold texts (each text is scored by a word list learned
from the others), then the cheapest setting that keeps RECALL_TARGET of the models' claims
is checked on a frozen half/half split and on a random library sample. Writes report.md,
curve.json and filter.json (word list learned from every gold text) to out_dir.

apply: one <out_dir>/<path under library>.json per book, holding kept character spans of
the canonical body (corpus.read_book), never the text. Each file is written atomically and
books already done with the same filter are skipped, so a run can be stopped and restarted
at any point without losing work. With no books listed, applies to every .md in the library.
"""
import collections
import hashlib
import json
import math
import os
import random
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus import read_book  # noqa: E402

MIN_POS, MIN_TEXTS = 3, 3      # a cue word must occur in >= 3 claim paragraphs of >= 3 texts
PRIOR = 1000                   # Dirichlet prior mass for the log-odds
MAX_PARA_WORDS = 300           # longer paragraphs (OCR, run-on text) are split at sentence ends
RECALL_TARGET = 0.95
EXIT_KEPT = 0.70               # not worth using if it still keeps more than this of the sci-fi sample
SAMPLE_SF, SAMPLE_OTHER, SEED = 200, 60, 2026
KS = (25, 50, 100, 200, 400, 800)
COMMON = (0.02, 0.05, 0.1, 0.2)  # most a cue word may appear in, as a share of non-claim paragraphs
SETTINGS = [(c, k, mode, w, t) for c in COMMON for k in KS
            for mode, w in (('sum', 0), ('sum', 1), ('sum', 2), ('max', 1)) for t in (1, 2, 3, 4, 5, 6, 8, 10, 12)]
WORD = re.compile(r'[a-z]+')
YEAR = re.compile(r'(?<!\d)(1\d\d\d|2\d\d\d)(?!\d)')
SENT = re.compile(r'(?<=[.!?…])["”’)]?\s+')


def stem(w):
    if w.endswith('ies') and len(w) > 5:
        return w[:-3] + 'y'
    for suf in ('ing', 'ed', 's'):
        if w.endswith(suf) and len(w) - len(suf) >= 4 and not w.endswith('ss'):
            return w[:-len(suf)]
    return w


def paragraphs(text):
    """Character spans of paragraphs (blank-line separated); very long ones split at sentence ends."""
    spans, at = [], 0
    for m in list(re.finditer(r'\n[ \t]*\n', text)) + [None]:
        end = m.start() if m else len(text)
        if text[at:end].strip():
            spans.extend(split_long(text, at, end))
        if m:
            at = m.end()
    return spans


def split_long(text, a, b):
    if len(text[a:b].split()) <= MAX_PARA_WORDS:
        return [(a, b)]
    out, start = [], a
    for m in SENT.finditer(text, a, b):
        if len(text[start:m.end()].split()) >= MAX_PARA_WORDS // 2:
            out.append((start, m.end()))
            start = m.end()
    if start < b:
        out.append((start, b))
    return out


def tokens_of(par, year):
    toks = [stem(w) for w in WORD.findall(par.lower()) if len(w) > 2]
    if year and any(int(y) > year + 5 for y in YEAR.findall(par)):
        toks.append('<future-year>')
    return toks


def as_year(v):
    try:
        return int(str(v)[:4])
    except ValueError:
        return None


def doc_of(text, year, label, counts=False):
    spans = paragraphs(text)
    toks = [tokens_of(text[a:b], year) for a, b in spans]
    d = {'label': label, 'spans': spans, 'starts': [a for a, _ in spans],
         'words': np.array([len(text[a:b].split()) for a, b in spans]),
         'cues': [set(t) for t in toks]}
    if counts:
        d['counts'] = [collections.Counter(t) for t in toks]
    return d


def overlapping(doc, a, b):
    """Indices of the paragraphs overlapping characters [a, b)."""
    i = max(0, np.searchsorted(doc['starts'], a, side='right') - 1)
    out = []
    while i < len(doc['spans']) and doc['spans'][i][0] < b:
        if doc['spans'][i][1] > a:
            out.append(i)
        i += 1
    return out


def learn(docs, common):
    """Cue words ranked by log-odds z-score of their rate in claim paragraphs vs. the rest."""
    pos, neg = collections.Counter(), collections.Counter()          # token counts
    pos_pars, neg_pars = collections.Counter(), collections.Counter()  # paragraphs containing
    texts = collections.defaultdict(set)
    n_neg = 0
    for d in docs:
        for counts, cues, is_pos in zip(d['counts'], d['cues'], d['pos']):
            if is_pos:
                pos.update(counts)
                pos_pars.update(cues)
                for c in cues:
                    texts[c].add(d['label'])
            else:
                neg.update(counts)
                neg_pars.update(cues)
                n_neg += 1
    n_pos_tok, n_neg_tok = sum(pos.values()), sum(neg.values())
    total = n_pos_tok + n_neg_tok
    ranked = []
    for c in pos:
        if pos_pars[c] < MIN_POS or len(texts[c]) < MIN_TEXTS or neg_pars[c] > common * n_neg:
            continue
        a = PRIOR * (pos[c] + neg[c]) / total
        lo = (math.log((pos[c] + a) / (n_pos_tok + PRIOR - pos[c] - a))
              - math.log((neg[c] + a) / (n_neg_tok + PRIOR - neg[c] - a)))
        if lo > 0:
            ranked.append((-lo / math.sqrt(1 / (pos[c] + a) + 1 / (neg[c] + a)), c))
    return [c for _, c in sorted(ranked)]


def scores(doc, cue_set):
    return np.array([len(c & cue_set) for c in doc['cues']])


def mask(s, mode, w, t):
    if w == 0:
        return s >= t
    pad = np.pad(s, w)
    win = np.stack([pad[i:i + len(s)] for i in range(2 * w + 1)])
    return (win.sum(0) if mode == 'sum' else win.max(0)) >= t


# ---------------------------------------------------------------- tune

def gold_docs(gold, runs):
    chunks = {c['id']: c for c in map(json.loads, open(os.path.join(gold, 'chunks.jsonl'), encoding='utf-8'))}
    docs = {}
    for cid, c in chunks.items():
        raw = open(os.path.join(gold, 'chunks', cid + '.txt'), encoding='utf-8').read()
        docs[cid] = doc_of(raw.split('Passage:\n\n', 1)[1], c['year'], c['text'], counts=True)
        docs[cid]['targets'] = collections.defaultdict(list)
    # Targets: speculative claims each model verified, and the union of all models' claims
    # with near-duplicates (quotes starting within 50 characters) merged.
    union = collections.defaultdict(list)
    for model in ('haiku', 'sonnet', 'opus'):
        for v in map(json.loads, open(os.path.join(runs, model, 'verified.jsonl'), encoding='utf-8')):
            if v.get('speculative_at_time') is False:
                continue
            span = (v['offset'], v['offset'] + len(str(v['quote'])))
            if model != 'haiku':
                docs[v['chunk']]['targets'][model].append(span)
            union[v['chunk']].append(span)
    for cid, spans in union.items():
        merged = []
        for a, b in sorted(spans):
            if merged and a - merged[-1][0] <= 50:
                merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
            else:
                merged.append((a, b))
        docs[cid]['targets']['claims'] = merged
    for a in map(json.loads, open(os.path.join(gold, 'anchors.jsonl'), encoding='utf-8')):
        if a['expect'] in ('realized', 'failed'):
            off = a['offset'] - chunks[a['chunk']]['start']
            docs[a['chunk']]['targets']['anchors'].append((off, off + len(a['anchor'])))
    for d in docs.values():
        d['pos'] = np.zeros(len(d['spans']), bool)
        for a, b in d['targets']['claims']:
            d['pos'][overlapping(d, a, b)] = True
        d['hits'] = {k: [overlapping(d, a, b) for a, b in v] for k, v in d['targets'].items()}
    return docs


TARGETS = ('claims', 'sonnet', 'opus', 'anchors')


def tally(acc, doc, keep):
    acc['kept'] += int(doc['words'][keep].sum())
    acc['words'] += int(doc['words'].sum())
    for k in TARGETS:
        for idx in doc['hits'].get(k, []):
            acc[k + '_n'] += 1
            acc[k + '_kept'] += bool(idx) and bool(keep[idx].any())


def evaluate_split(train, test, settings):
    """Learn from train docs, score test docs; one tally per setting."""
    out = {st: collections.Counter() for st in settings}
    for common in sorted({st[0] for st in settings}):
        ranked = learn(train, common)
        for k in sorted({st[1] for st in settings if st[0] == common}):
            cue_set = set(ranked[:k])
            for d in test:
                s = scores(d, cue_set)
                for st in settings:
                    if st[:2] == (common, k):
                        tally(out[st], d, mask(s, *st[2:]))
    return out


def rate(acc, k):
    return acc[k + '_kept'] / max(1, acc[k + '_n'])


def library_sample(library):
    sf, other = [], []
    for root, _, files in os.walk(library):
        for f in files:
            if f.endswith('.md'):
                p = os.path.join(root, f)
                (sf if os.path.relpath(p, library).startswith('Science-Fiction' + os.sep) else other).append(p)
    rng = random.Random(SEED)
    picks = [('sf', p) for p in rng.sample(sorted(sf), SAMPLE_SF)] + [('other', p) for p in rng.sample(sorted(other), SAMPLE_OTHER)]
    out = []
    for group, p in picks:
        fm, body = read_book(p)
        d = doc_of(body, as_year(fm.get('year')), group)
        d['year'] = as_year(fm.get('year'))
        out.append(d)
    return out


def tune(gold, runs, library, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    docs = gold_docs(gold, runs)
    by_text = collections.defaultdict(list)
    for d in docs.values():
        by_text[d['label']].append(d)

    # Leave one text out: each text is scored by a word list learned from the other texts.
    loto = {s: collections.Counter() for s in SETTINGS}
    per_text = {}
    for held in sorted(by_text):
        train = [d for t, ds in by_text.items() if t != held for d in ds]
        res = evaluate_split(train, by_text[held], SETTINGS)
        per_text[held] = res
        for s in SETTINGS:
            loto[s].update(res[s])

    # Word lists learned from every gold text, applied to a random library sample (cost estimate).
    ranked_all = {c: learn(list(docs.values()), c) for c in COMMON}
    sample = library_sample(library)
    lib = {s: collections.Counter() for s in SETTINGS}
    for common, k in sorted({st[:2] for st in SETTINGS}):
        cue_set = set(ranked_all[common][:k])
        for d in sample:
            s = scores(d, cue_set)
            for st in SETTINGS:
                if st[:2] == (common, k):
                    keep = mask(s, *st[2:])
                    lib[st][d['label'] + '_kept'] += int(d['words'][keep].sum())
                    lib[st][d['label'] + '_words'] += int(d['words'].sum())

    curve = []
    for s in SETTINGS:
        a, l = loto[s], lib[s]
        curve.append({'common': s[0], 'k': s[1], 'mode': s[2], 'window': s[3], 'threshold': s[4],
                      **{k: rate(a, k) for k in TARGETS},
                      'gold_kept': a['kept'] / a['words'],
                      'sf_kept': l['sf_kept'] / l['sf_words'], 'other_kept': l['other_kept'] / l['other_words']})
    json.dump(curve, open(os.path.join(out_dir, 'curve.json'), 'w'), indent=1)

    ok = [c for c in curve if c['claims'] >= RECALL_TARGET and c['sonnet'] >= RECALL_TARGET]
    best = min(ok, key=lambda c: (c['sf_kept'], c['gold_kept'])) if ok else None
    # Pareto frontier (sci-fi sample kept vs. held-out claim recall) for the report.
    frontier, top = [], -1
    for c in sorted(curve, key=lambda c: (c['sf_kept'], -c['claims'])):
        if c['claims'] > top:
            frontier.append(c)
            top = c['claims']

    lines = ['# Pre-filter tuning report', '',
             f'Decided before the run: use the filter only if some setting keeps at least {RECALL_TARGET:.0%} of the '
             f"models' speculative claims (all models combined, and Sonnet's alone) on held-out texts, while keeping at "
             f'most {EXIT_KEPT:.0%} of a random sample of the sci-fi library. Otherwise drop it.', '',
             f'Gold set: {len(docs)} chunks from {len(by_text)} texts. Held-out numbers are leave-one-text-out: each '
             'text is filtered with a word list learned from the other texts. Library sample: '
             f'{SAMPLE_SF} random sci-fi books and {SAMPLE_OTHER} other books (seed {SEED}), filtered with the list '
             'learned from all gold texts.', '',
             '"Claims" = speculative claims verified for any of Haiku, Sonnet and Opus, near-duplicates merged '
             f"({sum(len(d['targets']['claims']) for d in docs.values())}). \"Known\" = the answer key's realized and "
             'failed predictions.', '',
             '## Frontier (each row keeps more claims than every cheaper one)', '',
             '| Max share | Cue words | Window | Threshold | Claims kept | Sonnet | Opus | Known | Gold text kept | Sci-fi sample kept | Other books kept |',
             '|---|---|---|---|---|---|---|---|---|---|---|']
    for c in frontier:
        lines.append(f"| {c['common']:.0%} | {c['k']} | {c['mode']} ±{c['window']} | {c['threshold']} | {c['claims']:.1%} | {c['sonnet']:.1%} | "
                     f"{c['opus']:.1%} | {c['anchors']:.0%} | {c['gold_kept']:.0%} | {c['sf_kept']:.0%} | {c['other_kept']:.0%} |")
    lines.append('')

    if best is None:
        lines += [f'No setting reached {RECALL_TARGET:.0%} held-out recall. Recommendation: drop the filter.']
    else:
        st = (best['common'], best['k'], best['mode'], best['window'], best['threshold'])
        verdict = ('Recommendation: use it.' if best['sf_kept'] <= EXIT_KEPT
                   else f"Recommendation: drop it (keeps {best['sf_kept']:.0%} of the sci-fi sample, over the {EXIT_KEPT:.0%} limit).")
        lines += ['## Chosen setting', '',
                  f"Cheapest on the sci-fi sample among settings at ≥ {RECALL_TARGET:.0%}: {best['k']} cue words "
                  f"(each in at most {best['common']:.0%} of non-claim paragraphs), "
                  f"{best['mode']} over ±{best['window']} paragraphs, threshold {best['threshold']}. "
                  f"Held-out claims kept {best['claims']:.1%} (Sonnet {best['sonnet']:.1%}, Opus {best['opus']:.1%}), "
                  f"known predictions {best['anchors']:.0%}; keeps {best['sf_kept']:.0%} of the sci-fi sample and "
                  f"{best['other_kept']:.0%} of other books. {verdict}", '']

        # Frozen half/half split, stratified by claim count, as a second check.
        split_path = os.path.join(gold, 'prefilter_split.json')
        if not os.path.exists(split_path):
            order = sorted(by_text, key=lambda t: (-sum(len(d['targets']['claims']) for d in by_text[t]), t))
            halves = {'A': [], 'B': []}
            for i, t in enumerate(order):
                halves['AB'[(i % 4) in (1, 2)]].append(t)   # A B B A A B B A ...
            json.dump(halves, open(split_path, 'w'), indent=1)
        halves = json.load(open(split_path))
        lines += ['## Half/half check (frozen split in `gold/prefilter_split.json`)', '',
                  '| Learned on | Tested on | Claims kept | Sonnet | Opus | Known | Text kept |', '|---|---|---|---|---|---|---|']
        for tr, te in (('A', 'B'), ('B', 'A')):
            res = evaluate_split([d for t in halves[tr] for d in by_text[t]],
                                 [d for t in halves[te] for d in by_text[t]], [st])[st]
            lines.append(f"| {tr} | {te} | {rate(res, 'claims'):.1%} | {rate(res, 'sonnet'):.1%} | {rate(res, 'opus'):.1%} | "
                         f"{rate(res, 'anchors'):.0%} | {res['kept'] / res['words']:.0%} |")
        lines.append('')

        lines += ['## Chosen setting, by held-out text', '',
                  '| Text | Claims | Claims kept | Text kept |', '|---|---|---|---|']
        for t, res in sorted(per_text.items()):
            r = res[st]
            lines.append(f"| {t} | {r['claims_n']} | {rate(r, 'claims'):.0%} | {r['kept'] / r['words']:.0%} |")
        lines.append('')

        cues = ranked_all[best['common']][:best['k']]
        cue_set = set(cues)
        decades = collections.defaultdict(collections.Counter)
        for d in sample:
            if d['label'] != 'sf':
                continue
            dec = f"{d['year'] // 10 * 10}s" if d['year'] else 'unknown'
            keep = mask(scores(d, cue_set), *st[2:])
            decades[dec]['books'] += 1
            decades[dec]['kept'] += int(d['words'][keep].sum())
            decades[dec]['words'] += int(d['words'].sum())
        lines += ['## Sci-fi sample by decade (year in the file name: first publication when known)', '',
                  '| Decade | Books | Words | Kept |', '|---|---|---|---|']
        for dec, c in sorted(decades.items()):
            lines.append(f"| {dec} | {c['books']} | {c['words']:,} | {c['kept'] / c['words']:.0%} |")
        lines.append('')

        json.dump({'common': best['common'], 'k': best['k'], 'mode': best['mode'], 'window': best['window'], 'threshold': best['threshold'],
                   'max_para_words': MAX_PARA_WORDS, 'cues': cues,
                   'held_out': {k: best[k] for k in TARGETS}, 'sf_kept': best['sf_kept']},
                  open(os.path.join(out_dir, 'filter.json'), 'w'), indent=1)
        lines += ['## Cue words (learned from all gold texts, in rank order)', '', ', '.join(cues), '']

    open(os.path.join(out_dir, 'report.md'), 'w').write('\n'.join(lines))
    print('\n'.join(lines))


# ---------------------------------------------------------------- apply

def apply(filter_path, library, out_dir, books):
    flt = json.load(open(filter_path))
    fid = hashlib.sha256(open(filter_path, 'rb').read()).hexdigest()[:16]
    cue_set = set(flt['cues'])
    if not books:
        books = sorted(os.path.join(r, f) for r, _, fs in os.walk(library) for f in fs if f.endswith('.md'))
    done = skipped = 0
    for p in books:
        dest = os.path.join(out_dir, os.path.relpath(p, library) + '.json')
        if os.path.exists(dest):
            try:
                if json.load(open(dest)).get('filter') == fid:
                    skipped += 1
                    continue
            except ValueError:
                pass
        fm, body = read_book(p)
        d = doc_of(body, as_year(fm.get('year')), '')
        keep = mask(scores(d, cue_set), flt['mode'], flt['window'], flt['threshold'])
        spans = []
        for (a, b), k in zip(d['spans'], keep):
            if k:
                if spans and body[spans[-1][1]:a].strip() == '':
                    spans[-1][1] = b
                else:
                    spans.append([a, b])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = dest + '.part'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump({'filter': fid, 'book': os.path.relpath(p, library),
                       'sha256': hashlib.sha256(body.encode('utf-8')).hexdigest(),
                       'words': int(d['words'].sum()), 'kept_words': int(d['words'][keep].sum()), 'spans': spans}, f)
        os.replace(tmp, dest)
        done += 1
    print(f'{done} filtered, {skipped} already done')


if __name__ == '__main__':
    if sys.argv[1] == 'tune':
        tune(*sys.argv[2:6])
    elif sys.argv[1] == 'apply':
        apply(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
