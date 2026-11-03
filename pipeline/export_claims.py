"""Export verified claims, blind to book and author, for matching and judging.

    python -I pipeline/export_claims.py <out.jsonl> [domain=<domain>] [run ...]

Default runs: Stage 1, 1b and 1c. Rejected quotes and claims not speculative at the time are
left out. Each line: a claim id (<run>/<passage>#<n>, n counting the passage's verified claims
from 0), an opaque book id (the first 12 hex digits of the sha256 of the book's library path),
the passage's year, and the claim's fields. Book paths, authors and titles are not exported;
the ids lead back to them through the local run directories.
"""
import glob
import hashlib
import json
import os
import sys

FIELDS = ('quote', 'description', 'category', 'specificity', 'stated_time', 'polarity', 'confidence', 'valence',
          'voice', 'domain', 'second_order')
RUNS = ('stage1-sonnet', 'stage1b-sonnet', 'stage1c-sonnet')


def main(out, *args):
    opts = dict(a.split('=', 1) for a in args if '=' in a)
    runs = [a for a in args if '=' not in a] or RUNS
    n = 0
    with open(out + '.part', 'w', encoding='utf-8') as f:
        for run in runs:
            for path in sorted(glob.glob(os.path.join('work', 'extract', run, 'verified', '*.json'))):
                rec = json.load(open(path, encoding='utf-8'))
                for i, cl in enumerate(rec['claims']):
                    if cl['verify'] == 'rejected' or cl.get('speculative_at_time') is not True:
                        continue
                    if 'domain' in opts and cl.get('domain') != opts['domain']:
                        continue
                    book = hashlib.sha256(rec['book'].encode('utf-8')).hexdigest()[:12]
                    f.write(json.dumps({'id': f"{run}/{rec['chunk']}#{i}", 'book': book, 'year': rec['year'],
                                        **{k: cl.get(k) for k in FIELDS}}, ensure_ascii=False) + '\n')
                    n += 1
    os.replace(out + '.part', out)
    print(f'{n} claims -> {out}')


if __name__ == '__main__':
    main(*sys.argv[1:])
