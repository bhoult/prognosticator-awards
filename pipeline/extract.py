"""Extraction driver: books -> passages -> subagent batches -> verified claims. All state is on disk.

    python -I pipeline/extract.py pick <library> <n> <seed>                 random Gutenberg sci-fi books
    python -I pipeline/extract.py stage1 <library> [<exclude.txt> ...]       Stage 1 book list
    python -I pipeline/extract.py plan <run> <model> <library> <books.txt>  split books, write prompts (path[TAB]year)
    python -I pipeline/extract.py next <run> [in_flight]                    verify, then claim prompts up to in_flight
    python -I pipeline/extract.py release <run> [<batch> ...]               drop claims (all if none given)
    python -I pipeline/extract.py verify <run>                              check new results
    python -I pipeline/extract.py log <run> <batch> <tokens> <seconds> [...] record subagents' usage
    python -I pipeline/extract.py status <run> [stage_words.json]           progress, usage, projection
    python -I pipeline/extract.py stage-words <library> <out.json>          words in every Gutenberg sci-fi book

(Use .venv/bin/python: verify needs rapidfuzz.)

Subagents can't be started from Python. The orchestrating Claude Code session runs `next`,
starts one subagent per prompt file it prints ("Read <file> and follow its instructions"),
and records each subagent's token count with `log`.

Stopping and restarting: nothing is held in memory between commands. A subagent writes
out/<id>.json as soon as it finishes each passage; `verify` checks the quotes and writes
verified/<id>.json (temporary file, then rename). `next` lists only passages that have no
verified file, so a run stopped at any point, mid-batch included, loses at most the passages
being read at that moment. `plan` on an existing run only checks that the settings match.
`next` also claims each batch it prints (prompts/batch_<n>.claimed), so later calls skip batches
that are still being read. Claims expire after CLAIM_MINUTES, so after a stop the unfinished
batches come back by themselves; `release` brings them back at once.

Run layout (under work/, never committed: passages are book text):
    config.json  model, prompt sha256, sizes, seed, books sha256 (written last by plan)
    books.txt    one library-relative path per line
    chunks.jsonl passage id, book, character range of the canonical body, words, year
    passages/    <id>.txt: what a subagent reads (id, year, blanked passage)
    batches.json passage ids per subagent
    prompts/     batch_<n>.md, rewritten by `next` to list only pending passages; batch_<n>.claimed
    out/         raw subagent results
    verified/    checked results: each quote's status and offset in the passage and the book
    usage.jsonl  tokens and seconds per subagent
"""
import hashlib
import json
import os
import random
import re
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus import read_book, windows  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE = os.path.join(ROOT, 'prompts', 'extract_subagent.md')
CHUNK_WORDS, BATCH_WORDS, SEED = 6000, 40000, 2026   # as in the gold set
CLAIM_MINUTES = 30                                   # a subagent takes 2-4 minutes per batch
GOLD = os.path.join(ROOT, 'gold')


def sha(data):
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def write_atomic(path, text):
    tmp = path + '.part'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text)
    os.replace(tmp, path)


def front_matter(path):
    """Header fields only, without reading the whole book."""
    fm = {}
    with open(path, encoding='utf-8', errors='replace') as f:
        if f.readline().strip() != '---':
            return fm
        for line in f:
            if line.strip() == '---':
                break
            key, _, value = line.rstrip('\n').partition(': ')
            try:
                fm[key] = json.loads(value)
            except json.JSONDecodeError:
                fm[key] = value
    return fm


def gutenberg_sf(library):
    out = []
    for root, _, files in os.walk(os.path.join(library, 'Science-Fiction')):
        for f in files:
            if f.endswith('.md'):
                p = os.path.join(root, f)
                if str(front_matter(p).get('source', '')).startswith('Project Gutenberg'):
                    out.append(os.path.relpath(p, library))
    return sorted(out)


def as_year(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def pick(library, n, seed):
    gold = {t['path'] for t in json.load(open(os.path.join(GOLD, 'texts.json')))['texts']}
    gold |= {json.loads(l)['path'] for l in open(os.path.join(GOLD, 'chunks.jsonl'), encoding='utf-8')}
    pool = [p for p in gutenberg_sf(library)
            if p not in gold and as_year(front_matter(os.path.join(library, p)).get('year'))]
    for p in sorted(random.Random(int(seed)).sample(pool, int(n))):
        print(p)


def stage1(library, *exclude):
    """Gutenberg sci-fi with a known year, plus lists/predictive-texts.txt, minus books in the exclude lists.

    Books with an unknown year wait for the dating pass: the model judges what was speculative
    relative to the year it is given."""
    skip = {l.strip() for f in exclude for l in open(f, encoding='utf-8') if l.strip()}
    books = [p for p in gutenberg_sf(library) if as_year(front_matter(os.path.join(library, p)).get('year'))]
    books += [l.strip() for l in open(os.path.join(ROOT, 'lists', 'predictive-texts.txt'), encoding='utf-8') if l.strip()]
    for p in sorted(set(books) - skip):
        print(p)


def load(run, name):
    return json.load(open(os.path.join(run, name), encoding='utf-8'))


def chunks_of(run):
    return [json.loads(l) for l in open(os.path.join(run, 'chunks.jsonl'), encoding='utf-8')]


def plan(run, model, library, books_file):
    """books_file: one library path per line, optionally followed by a tab and the year to use
    instead of the one in the book's header (from pipeline/dating.py)."""
    books, years = [], {}
    for line in open(books_file, encoding='utf-8'):
        path, _, year = line.rstrip('\n').partition('\t')
        if path.strip():
            path = os.path.relpath(path, library) if os.path.isabs(path) else path.strip()
            books.append(path)
            if year.strip():
                years[path] = int(year)
    want = {'model': model, 'prompt_sha256': sha(open(TEMPLATE, 'rb').read()), 'library': library,
            'chunk_words': CHUNK_WORDS, 'batch_words': BATCH_WORDS, 'seed': SEED,
            'books_sha256': sha('\n'.join(f'{b}\t{years[b]}' if b in years else b for b in books))}
    cfg_path = os.path.join(run, 'config.json')
    if os.path.exists(cfg_path):
        have = load(run, 'config.json')
        diff = {k: (have.get(k), v) for k, v in want.items() if have.get(k) != v}
        if diff:
            raise SystemExit(f'{run} exists with different settings {diff}; use a new run directory')
        print(f'{run}: already planned, settings match')
        return
    for d in ('passages', 'prompts', 'out', 'verified'):
        os.makedirs(os.path.join(run, d), exist_ok=True)
    pieces = []
    for b in books:
        fm, body = read_book(os.path.join(library, b))
        year = years.get(b) or as_year(fm.get('year'))
        for a, z in windows(body, 0, len(body), CHUNK_WORDS):
            if body[a:z].strip():
                pieces.append({'book': b, 'start': a, 'end': z, 'words': len(body[a:z].split()),
                               'year': year if year else 'unknown', 'body': body[a:z]})
    random.Random(SEED).shuffle(pieces)  # a batch mixes books, and ids don't reveal which passages share one
    with open(os.path.join(run, 'chunks.jsonl.part'), 'w', encoding='utf-8') as f:
        for n, c in enumerate(pieces, 1):
            c['id'] = f'p{n:05d}'
            c['sha256'] = sha(c['body'])
            write_atomic(os.path.join(run, 'passages', c['id'] + '.txt'),
                         f"Passage id: {c['id']}\nFirst published: {c['year']}\n\nPassage:\n\n{c['body']}")
            f.write(json.dumps({k: v for k, v in c.items() if k != 'body'}, ensure_ascii=False) + '\n')
    os.replace(os.path.join(run, 'chunks.jsonl.part'), os.path.join(run, 'chunks.jsonl'))
    batches, cur, words = [], [], 0
    for c in pieces:
        if cur and words + c['words'] > BATCH_WORDS:
            batches.append(cur)
            cur, words = [], 0
        cur.append(c['id'])
        words += c['words']
    if cur:
        batches.append(cur)
    write_atomic(os.path.join(run, 'batches.json'), json.dumps(batches, indent=1))
    write_atomic(os.path.join(run, 'books.txt'), ''.join(f'{b}\t{years[b]}\n' if b in years else b + '\n' for b in books))
    write_atomic(cfg_path, json.dumps({**want, 'planned_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                                       'books': len(books), 'passages': len(pieces),
                                       'words': sum(c['words'] for c in pieces), 'batches': len(batches)}, indent=1))
    print(f'{run}: {len(books)} books, {len(pieces)} passages, {sum(c["words"] for c in pieces):,} words, '
          f'{len(batches)} batches')


FIELDS = {  # allowed values, from prompts/extract_subagent.md
    'category': {'technology', 'science', 'social', 'political', 'event', 'other'},
    'polarity': {'will', 'will_not'},
    'confidence': {'asserted', 'hedged'},
    'valence': {'positive', 'negative', 'neutral', 'mixed'},
    'voice': {'narrator', 'sympathetic', 'antagonist', 'document'},
    'domain': {'computing', 'communication', 'transport', 'energy', 'medicine-biology', 'weapons-war', 'space',
               'society-politics', 'economy', 'environment', 'other'},
    'specificity': {1, 2, 3, 4, 5},
    'speculative_at_time': {True, False},
    'second_order': {True, False},
}


def field_issues(cl):
    bad = [f for f, ok in FIELDS.items() if cl.get(f) not in ok]
    if not str(cl.get('description', '')).strip():
        bad.append('description')
    return bad


KEYS = ('quote|description|category|specificity|speculative_at_time|stated_time|polarity|confidence|valence|'
        'voice|domain|second_order|chunk|claims')
TEXT_FIELD = re.compile(r'("(?:quote|description|stated_time|category|domain|polarity|confidence|valence|voice)"'
                        r'\s*:\s*")(.*?)("\s*(?:,\s*"(?:' + KEYS + r')"\s*:|\}))', re.S)


def repair_json(raw):
    """Escape stray double quotes inside string fields ("quote": "So," he said, "…").

    A value runs from its key to the next known key (or the end of the claim), so this works
    whether a subagent wrote one field per line or a whole claim per line. Returns parsed
    JSON, or raises ValueError."""
    return json.loads(TEXT_FIELD.sub(lambda m: m.group(1) + re.sub(r'(?<!\\)"', '\\"', m.group(2)) + m.group(3), raw))


def passage_text(run, cid):
    raw = open(os.path.join(run, 'passages', cid + '.txt'), encoding='utf-8').read()
    return raw.split('Passage:\n\n', 1)[1]


def verify(run):
    from quotes import normalize, verify as check  # needs rapidfuzz
    cfg = load(run, 'config.json')
    chunks = {c['id']: c for c in chunks_of(run)}
    batch_of = {cid: n for n, ids in enumerate(load(run, 'batches.json'), 1) for cid in ids}
    siblings = {}
    for cid, n in batch_of.items():
        siblings.setdefault(n, []).append(cid)
    normed = {}

    def norm(cid):
        if cid not in normed:
            normed[cid] = normalize(passage_text(run, cid))
        return normed[cid]

    done = bad = 0
    for name in sorted(os.listdir(os.path.join(run, 'out'))):
        cid = name[:-5]
        if not name.endswith('.json') or cid not in chunks:
            continue
        src, dest = os.path.join(run, 'out', name), os.path.join(run, 'verified', name)
        if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(src):
            continue
        raw = open(src, encoding='utf-8').read()
        repaired = False
        try:
            try:
                result = json.loads(raw)
            except ValueError:
                result, repaired = repair_json(raw), True
            claims = result['claims']
            assert isinstance(claims, list)
        except (ValueError, KeyError, TypeError, AssertionError) as e:
            print(f'{cid}: unreadable result ({type(e).__name__}), left pending')
            bad += 1
            continue
        c = chunks[cid]
        # Passages extracted through the Batch API (pipeline/batch_api.py) carry their own settings.
        # A reply it could not use leaves no out/ file, so a later result there came from a subagent.
        meta_path = os.path.join(run, 'api', 'meta', name)
        meta = json.load(open(meta_path, encoding='utf-8')) if os.path.exists(meta_path) else {}
        if meta.get('problem'):
            meta = {}
        counts = {'claims': 0, 'exact': 0, 'fuzzy': 0, 'rejected': 0, 'found_in_other': 0, 'field_issues': 0}
        checked = []
        for cl in claims:
            if not isinstance(cl, dict):
                continue
            status, at, sim = check(str(cl.get('quote', '')), None, *norm(cid))
            found_in = None
            if at is None:  # written into the wrong passage's file?
                for other in siblings[batch_of[cid]]:
                    if other != cid and check(str(cl.get('quote', '')), None, *norm(other))[1] is not None:
                        found_in = other
                        counts['found_in_other'] += 1
                        break
            issues = field_issues(cl)
            counts['claims'] += 1
            counts[status] += 1
            counts['field_issues'] += bool(issues)
            checked.append({**cl, 'verify': status, 'similarity': sim, 'offset': at,
                            'book_offset': None if at is None else c['start'] + at, 'found_in': found_in,
                            'field_issues': issues})
        record = {'chunk': cid, 'book': c['book'], 'year': c['year'], 'words': c['words'],
                  'method': meta.get('method', 'subagent'), 'model': meta.get('model', cfg['model']),
                  'prompt_sha256': meta.get('prompt_sha256', cfg['prompt_sha256']), 'passage_sha256': c['sha256'],
                  'chunk_field_ok': result.get('chunk') == cid, 'json_repaired': repaired or meta.get('json_repaired', False),
                  'verified_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                  'counts': counts, 'claims': checked}
        write_atomic(dest, json.dumps(record, ensure_ascii=False, indent=1))
        done += 1
    print(f'verified {done} new result(s)' + (f', {bad} unreadable' if bad else ''))


def pending(run):
    have = {n[:-5] for n in os.listdir(os.path.join(run, 'verified')) if n.endswith('.json')}
    return [[cid for cid in ids if cid not in have] for ids in load(run, 'batches.json')]


def next_batches(run, limit=None):
    verify(run)
    template = open(TEMPLATE, encoding='utf-8').read()
    cfg = load(run, 'config.json')
    if sha(template.encode('utf-8')) != cfg['prompt_sha256']:
        raise SystemExit('prompts/extract_subagent.md changed since this run was planned; use a new run')
    words = {c['id']: c['words'] for c in chunks_of(run)}
    todo = [(n, ids) for n, ids in enumerate(pending(run), 1) if ids]

    def claimed(n):
        claim = os.path.join(run, 'prompts', f'batch_{n}.claimed')
        return os.path.exists(claim) and time.time() - os.path.getmtime(claim) < CLAIM_MINUTES * 60

    # A claim lasts until `log` records the subagent as finished, so this counts live subagents,
    # including ones that have written every result but not yet reported back.
    running = sum(claimed(int(f[6:-8])) for f in os.listdir(os.path.join(run, 'prompts')) if f.endswith('.claimed'))
    room = len(todo) if limit is None else max(0, int(limit) - running)  # limit = most subagents in flight
    shown = 0
    for n, ids in todo:
        if shown >= room or claimed(n):
            continue
        claim = os.path.join(run, 'prompts', f'batch_{n}.claimed')
        files = '\n'.join(os.path.abspath(os.path.join(run, 'passages', i + '.txt')) for i in ids)
        path = os.path.abspath(os.path.join(run, 'prompts', f'batch_{n}.md'))
        write_atomic(path, template.replace('{files}', files)
                     .replace('{outdir}', os.path.abspath(os.path.join(run, 'out'))))
        write_atomic(claim, time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        print(f'{path}\t{len(ids)} passages\t{sum(words[i] for i in ids):,} words')
        shown += 1
    print(f'{shown} claimed, {running} already running, {len(todo) - shown - sum(claimed(n) for n, _ in todo)} waiting')


def release(run, *batches):
    names = [f'batch_{b}.claimed' for b in batches] or \
        [n for n in os.listdir(os.path.join(run, 'prompts')) if n.endswith('.claimed')]
    for n in names:
        if os.path.exists(os.path.join(run, 'prompts', n)):
            os.remove(os.path.join(run, 'prompts', n))
    print(f'released {len(names)} claim(s)')


def log(run, *triples):
    """<batch> <tokens> <seconds>, repeated; a finished batch's claim is dropped."""
    with open(os.path.join(run, 'usage.jsonl'), 'a', encoding='utf-8') as f:
        for batch, tokens, seconds in zip(triples[::3], triples[1::3], triples[2::3]):
            f.write(json.dumps({'batch': int(batch), 'tokens': int(tokens), 'seconds': float(seconds),
                                'at': time.strftime('%Y-%m-%d %H:%M:%S')}) + '\n')
            claim = os.path.join(run, 'prompts', f'batch_{int(batch)}.claimed')
            if os.path.exists(claim):
                os.remove(claim)
    print(f'logged {len(triples) // 3}')


def status(run, stage_words=None):
    cfg = load(run, 'config.json')
    chunks = {c['id']: c for c in chunks_of(run)}
    batches = load(run, 'batches.json')
    recs = [json.load(open(os.path.join(run, 'verified', n), encoding='utf-8'))
            for n in sorted(os.listdir(os.path.join(run, 'verified'))) if n.endswith('.json')]
    tot = {k: sum(r['counts'].get(k, 0) for r in recs)
           for k in ('claims', 'exact', 'fuzzy', 'rejected', 'found_in_other', 'field_issues')}
    words_done = sum(r['words'] for r in recs)
    print(f"{run}  model {cfg['model']}  prompt {cfg['prompt_sha256'][:12]}")
    print(f"books {cfg['books']}, passages {len(recs)}/{len(chunks)} verified, "
          f"words {words_done:,}/{cfg['words']:,}, batches {sum(not p for p in pending(run))}/{len(batches)} done")
    methods = {}
    for r in recs:
        methods[r.get('method', 'subagent')] = methods.get(r.get('method', 'subagent'), 0) + 1
    if len(methods) > 1 or 'subagent' not in methods:
        print('passages by method: ' + ', '.join(f'{m} {n}' for m, n in sorted(methods.items())))
    if recs:
        print(f"claims {tot['claims']} ({10000 * tot['claims'] / max(1, words_done):.1f} per 10K words); quotes "
              f"{tot['exact']} exact, {tot['fuzzy']} fuzzy, {tot['rejected']} rejected "
              f"({tot['found_in_other']} of them found in another passage of the batch); "
              f"chunk field wrong in {sum(not r['chunk_field_ok'] for r in recs)} file(s); "
              f"{tot['field_issues']} claim(s) with a field outside its allowed values")
    path = os.path.join(run, 'usage.jsonl')
    usage = [json.loads(l) for l in open(path)] if os.path.exists(path) else []
    if not usage:
        return
    bw = {n: sum(chunks[i]['words'] for i in ids) for n, ids in enumerate(batches, 1)}
    per_word = [u['tokens'] / bw[u['batch']] for u in usage]
    sec_word = [u['seconds'] / bw[u['batch']] for u in usage]
    tokens, words_logged = sum(u['tokens'] for u in usage), sum(bw[u['batch']] for u in usage)
    print(f"usage: {len(usage)} subagents, {tokens:,} tokens, {sum(u['seconds'] for u in usage) / 60:.0f} agent-minutes; "
          f"{10000 * tokens / words_logged:,.0f} tokens per 10K words "
          f"(per batch: {10000 * min(per_word):,.0f} to {10000 * max(per_word):,.0f}, median {10000 * statistics.median(per_word):,.0f})")
    if stage_words:
        sw = json.load(open(stage_words))
        W = sw['words']
        rate = tokens / words_logged
        print(f"projection for {sw['books']:,} books, {W:,} words: {rate * W / 1e6:,.0f}M tokens "
              f"(batch range {min(per_word) * W / 1e6:,.0f}M to {max(per_word) * W / 1e6:,.0f}M); "
              f"{statistics.median(sec_word) * W / 3600:,.0f} agent-hours")


def stage_words(library, out):
    books = gutenberg_sf(library)
    words = 0
    for b in books:
        words += len(read_book(os.path.join(library, b))[1].split())
    write_atomic(out, json.dumps({'stage': 'gutenberg-sf', 'books': len(books), 'words': words,
                                  'counted_at': time.strftime('%Y-%m-%d %H:%M:%S')}, indent=1))
    print(f'{len(books)} books, {words:,} words')


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    {'pick': pick, 'stage1': stage1, 'plan': plan, 'next': next_batches, 'release': release, 'verify': verify,
     'log': log, 'status': status, 'stage-words': stage_words}[cmd](*args)
