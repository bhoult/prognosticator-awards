"""Export verified claims, blind to book and author, for matching and judging.

    python -I pipeline/export_claims.py <out.jsonl> [domain=<domain>] [tranche=A|B] [years=record] [run ...]

Default runs: the extraction pilot, Stage 1, 1b and 1c. Rejected quotes and claims not
speculative at the time are left out. Each line: a claim id (<run>/<passage>#<n>, n counting
the passage's claims from 0), an opaque book id (the first 12 hex digits of the sha256 of the
book's library path), the year, the tranche, and the claim's fields. Book paths, authors and
titles are not exported; the ids lead back to them through the local run directories.

Version 2 (2026-11-03, runs/match/PLAN.md §2); the computing pilot used version 1:
- The extraction pilot's 20 books are included.
- `year` is the book's year in lists/gutenberg-sf-dates.tsv (the ISFDB dating pass) when the
  book is listed with one, else the year the extraction used; anything not a whole number is
  null. `year_source` says which. `years=record` keeps version 1's years.
- `category` and `domain` values outside the extraction prompt's lists are mapped to allowed
  ones (MAP_CATEGORY, MAP_DOMAIN); the original is kept in `category_raw` / `domain_raw`.
- `tranche`: A (technology and science) or B (events and social change), from the category,
  or for `other` from the domain.
"""
import csv
import glob
import hashlib
import json
import os
import sys

FIELDS = ('quote', 'description', 'category', 'specificity', 'stated_time', 'polarity', 'confidence', 'valence',
          'voice', 'domain', 'second_order')
RUNS = ('pilot-sonnet', 'stage1-sonnet', 'stage1b-sonnet', 'stage1c-sonnet')
DATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lists', 'gutenberg-sf-dates.tsv')

CATEGORIES = {'technology', 'science', 'social', 'political', 'event', 'other'}
DOMAINS = {'computing', 'communication', 'transport', 'energy', 'medicine-biology', 'weapons-war', 'space',
           'society-politics', 'economy', 'environment', 'other'}
TECH_DOMAINS = {'computing', 'communication', 'transport', 'energy', 'medicine-biology', 'weapons-war', 'space',
                'environment'}
# category fields that hold a domain-like value (Stage 1 report, "Field problems")
MAP_CATEGORY = {**{d: 'technology' for d in TECH_DOMAINS | {'biology', 'medicine', 'weapons', 'military'}},
                'economy': 'social', 'economic': 'social', 'society-politics': 'social', 'society': 'social'}
MAP_DOMAIN = {'military': 'weapons-war', 'defense': 'weapons-war', 'political': 'society-politics',
              'space-society-politics': 'space'}


def as_year(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def tranche(category, domain):
    if category in ('technology', 'science'):
        return 'A'
    if category in ('social', 'political', 'event'):
        return 'B'
    return 'A' if domain in TECH_DOMAINS else 'B'


def main(out, *args):
    opts = dict(a.split('=', 1) for a in args if '=' in a)
    runs = [a for a in args if '=' not in a] or RUNS
    dated = {}
    if opts.get('years') != 'record':
        dated = {r['path']: as_year(r['year']) for r in csv.DictReader(open(DATES, encoding='utf-8'), delimiter='\t')}
    n = 0
    with open(out + '.part', 'w', encoding='utf-8') as f:
        for run in runs:
            for path in sorted(glob.glob(os.path.join('work', 'extract', run, 'verified', '*.json'))):
                rec = json.load(open(path, encoding='utf-8'))
                year, source = dated.get(rec['book']), 'dating'
                if year is None:
                    year, source = as_year(rec['year']), 'record'
                for i, cl in enumerate(rec['claims']):
                    if cl['verify'] == 'rejected' or cl.get('speculative_at_time') is not True:
                        continue
                    row = {k: cl.get(k) for k in FIELDS}
                    if row['category'] not in CATEGORIES:
                        row['category_raw'], row['category'] = row['category'], MAP_CATEGORY.get(row['category'], 'other')
                    if row['domain'] not in DOMAINS:
                        row['domain_raw'], row['domain'] = row['domain'], MAP_DOMAIN.get(row['domain'], 'other')
                    t = tranche(row['category'], row['domain'])
                    if 'domain' in opts and row['domain'] != opts['domain'] or 'tranche' in opts and t != opts['tranche']:
                        continue
                    book = hashlib.sha256(rec['book'].encode('utf-8')).hexdigest()[:12]
                    f.write(json.dumps({'id': f"{run}/{rec['chunk']}#{i}", 'book': book, 'year': year,
                                        'year_source': source if year is not None else None, 'tranche': t, **row},
                                       ensure_ascii=False) + '\n')
                    n += 1
    os.replace(out + '.part', out)
    print(f'{n} claims -> {out}')


if __name__ == '__main__':
    main(*sys.argv[1:])
