"""Build the gold set: identical chunks for every model under test.

    python -I pipeline/gold.py [gold_dir]

Reads gold/texts.json and gold/answer_key.json and writes:
  gold/chunks/c###.txt   what a model reads: the year and the blanked passage, nothing else
  gold/chunks.jsonl      private map: chunk id -> text, character range, words, year
  gold/anchors.jsonl     each answer-key entry with the chunk and offset of its anchor
  gold/batches.json      chunk ids grouped into one batch per subagent (same for every model)
Deterministic: the seed in texts.json fixes the random picks and the order.
"""
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus import read_book, windows  # noqa: E402

GOLD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'gold')
cfg = json.load(open(os.path.join(GOLD, 'texts.json')))
key = json.load(open(os.path.join(GOLD, 'answer_key.json')))['entries']
LIB, N, rng = cfg['library'], cfg['chunk_words'], random.Random(cfg['seed'])
BATCH_WORDS = 40000


texts = list(cfg['texts'])
gold_paths = {t['path'] for t in texts}
pool = []
for genre in cfg['random_books']['genres']:
    for dp, dn, fn in os.walk(os.path.join(LIB, genre)):
        pool += [os.path.relpath(os.path.join(dp, f), LIB) for f in fn if f.endswith('.md')]
pool = sorted(p for p in pool if p not in gold_paths)
rng.shuffle(pool)
picked = 0
for p in pool:
    if picked == cfg['random_books']['count']:
        break
    fm, body = read_book(os.path.join(LIB, p))
    if len(body.split()) < 40000 or str(fm.get('year')) == 'unknown':
        continue
    texts.append({'id': f'random{picked + 1}', 'path': p, 'year': int(fm['year']), 'take': 'random',
                  'extra': cfg['random_books']['chunks_each'], 'note': 'year is the edition year'})
    picked += 1

chunks, anchors = [], []
for t in texts:
    _, body = read_book(os.path.join(LIB, t['path']))
    for title in t.get('blank_headings', []):  # story titles inside a collection; same length keeps offsets
        body = re.sub(r'(?im)^(#+[^\n]*?)(' + re.escape(title) + r')', lambda m: m.group(1) + '[…]'.ljust(len(m.group(2))), body)
    start, end = t.get('range', [0, len(body)])
    wins = windows(body, start, end, N)
    mine = [e for e in key if e['text'] == t['id']]
    found = {}
    for e in mine:
        at = body.lower().find(e['anchor'].lower(), start, end)
        if at < 0:
            raise SystemExit(f"anchor not found for {e['id']}: {e['anchor']!r}")
        found[e['id']] = at
    with_anchor = sorted({i for i, (a, b) in enumerate(wins) for at in found.values() if a <= at < b})
    if t['take'] == 'all':
        take = list(range(len(wins)))
    else:
        rest = [i for i in range(len(wins)) if i not in with_anchor]
        take = sorted(with_anchor + rng.sample(rest, min(t.get('extra', 0), len(rest))))
    for i in take:
        a, b = wins[i]
        chunks.append({'text': t['id'], 'path': t['path'], 'start': a, 'end': b, 'year': t['year'],
                       'words': len(body[a:b].split()), 'body': body[a:b]})
    for e in mine:
        at = found[e['id']]
        anchors.append({**e, 'offset': at})

rng.shuffle(chunks)  # ids don't reveal which chunks share a book
os.makedirs(os.path.join(GOLD, 'chunks'), exist_ok=True)
for n, c in enumerate(chunks, 1):
    c['id'] = f'c{n:03d}'
    with open(os.path.join(GOLD, 'chunks', c['id'] + '.txt'), 'w', encoding='utf-8') as f:
        f.write(f"First published: {c['year']}\n\nPassage:\n\n{c['body']}")
for a in anchors:
    a['chunk'] = next((c['id'] for c in chunks if c['text'] == a['text'] and c['start'] <= a['offset'] < c['end']), None)

with open(os.path.join(GOLD, 'chunks.jsonl'), 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps({k: v for k, v in c.items() if k != 'body'}, ensure_ascii=False) + '\n')
with open(os.path.join(GOLD, 'anchors.jsonl'), 'w', encoding='utf-8') as f:
    for a in anchors:
        f.write(json.dumps(a, ensure_ascii=False) + '\n')

batches, cur, words = [], [], 0
for c in chunks:
    if cur and words + c['words'] > BATCH_WORDS:
        batches.append(cur)
        cur, words = [], 0
    cur.append(c['id'])
    words += c['words']
batches.append(cur)
json.dump(batches, open(os.path.join(GOLD, 'batches.json'), 'w'), indent=1)

total = sum(c['words'] for c in chunks)
print(f"{len(texts)} texts, {len(chunks)} chunks, {total:,} words, {len(anchors)} anchors "
      f"({sum(a['chunk'] is None for a in anchors)} outside chosen chunks), {len(batches)} batches")
for t in texts:
    cs = [c for c in chunks if c['text'] == t['id']]
    print(f"  {t['id']:16s} {len(cs)} chunk(s) {sum(c['words'] for c in cs):7,} words  {t['path'][:70]}")
