"""First-publication years for the Gutenberg sci-fi books, from ISFDB. Deterministic: no model calls.

    python -I pipeline/dating.py <library> <isfdb.sqlite> <out.tsv>

For each book: find ISFDB titles with the same normalized title (or the title without its
subtitle, or an alternate title) credited to the same author (pseudonyms and alternate names
count), and take the earliest year among the work and its variants. When a story and, say, its
later novel expansion both match, the one whose length fits the book's word count wins; if that
doesn't settle it, the earliest year is taken and the row is marked ambiguous.

Each year is checked against the transcriber's note ("produced from Galaxy June 1956") and the
library's year. The year used is ISFDB's, unless the note gives an earlier one: an etext can't
be older than the magazine it was made from, so a later ISFDB year means a wrong match.
"""
import html
import json
import os
import re
import sqlite3
import sys
import unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import as_year, front_matter, gutenberg_sf, write_atomic  # noqa: E402

WORKS = ('NOVEL', 'SHORTFICTION', 'SERIAL', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'OMNIBUS', 'POEM', 'ESSAY')
NOTE = re.compile(r'produced from\W+(?:[^.\n]{0,80}?)\b(1[6-9]\d\d|20[0-2]\d)\b', re.I)
SUFFIX = {'jr', 'sr', 'ii', 'iii', 'iv', 'phd', 'md', 'mrs', 'mr', 'miss', 'dr', 'sir', 'prof', 'professor', 'rev'}
PART = re.compile(r'[,.\s—-]*\b(?:part|volume|vol|book|no)\.?\s*(?:\d+|[ivxlc]+)\.?\s*$', re.I)
ISSUE = re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December|'
                   r'Spring|Summer|Fall|Autumn|Winter),?\s+(1[89]\d\d)\b')


def fold(s):
    s = unicodedata.normalize('NFKD', html.unescape(s or ''))
    return ''.join(c for c in s if not unicodedata.combining(c)).lower().replace('&', ' and ')


def norm_title(s):
    words = re.sub(r'[^a-z0-9]+', ' ', fold(s)).split()
    if words and words[0] in ('the', 'a', 'an'):
        words = words[1:]
    return ' '.join(words)


def title_keys(t):
    """The title, then shorter forms: without a parenthesis, before a subtitle, before "or"."""
    t = PART.sub('', t) if PART.search(t) else t   # Gutenberg splits long books into parts
    keys = [norm_title(t)]
    for short in (re.sub(r'\s*[(\[].*?[)\]]', '', t), re.split(r'\s*[:;—]\s*|\s+-\s+|\.\s', t)[0],
                  re.split(r',?\s+or,?\s+', t, flags=re.I)[0]):
        k = norm_title(short)
        if k and k not in keys:
            keys.append(k)
    return keys


def name_tokens(name):
    """'Hyatt Verrill, A.' or 'A. Hyatt Verrill' -> ['a', 'hyatt', 'verrill']."""
    s = fold(name)
    if ',' in s and len(s.split(',')) == 2 and not re.search(r',\s*(jr|sr)\b', s):
        last, first = s.split(',')
        s = first + ' ' + last
    return [w for w in re.sub(r'[^a-z]+', ' ', s).split() if w not in SUFFIX]


def same_person(a, b):
    a, b = name_tokens(a), name_tokens(b)
    if not a or not b or a[-1] != b[-1]:
        return False
    return a == b or len(a) == 1 or len(b) == 1 or a[0][0] == b[0][0]   # "Mrs. Loudon": surname only


def book_authors(author):
    return [p for p in re.split(r'\s+and\s+|\s*&\s*|;\s*', author or '') if p.strip()]


LENGTHS = ['short story', 'novelette', 'novella', 'novel']   # ISFDB's names; SFWA word limits below


def length_class(words):
    return 0 if words < 7500 else 1 if words < 17500 else 2 if words < 40000 else 3


def fits(row, words):
    """Could this ISFDB title be a text of this many words? The count includes front matter, so a
    story may sit one length class off."""
    want, t = length_class(words), row['ttype']
    if t in ('NOVEL', 'SERIAL'):
        return want >= 2
    if t == 'SHORTFICTION':
        have = LENGTHS.index(row['storylen']) if row['storylen'] in LENGTHS else None
        return (want <= 2 and (have is None or abs(have - want) <= 1)) or (have == 2 and words < 60000)
    if t == 'NONFICTION':
        return True
    if t in ('COLLECTION', 'ANTHOLOGY', 'OMNIBUS'):   # never a story that shares the book's title
        return words >= 25000
    return want <= 1   # ESSAY, POEM


def year_of(date):
    y = as_year(str(date or '')[:4])
    return y if y and 1000 < y < 2100 else None


def main(library, isfdb_path, out):
    books = []
    for p in gutenberg_sf(library):
        raw = open(os.path.join(library, p), encoding='utf-8', errors='replace').read()
        fm = front_matter(os.path.join(library, p))
        m = NOTE.search(raw)
        books.append({'path': p, 'title': str(fm.get('title', '')), 'author': str(fm.get('author', '')),
                      'library_year': as_year(fm.get('year')), 'words': len(raw.split()),
                      'note_year': int(m.group(1)) if m else None,
                      'gutenberg': (re.search(r'#(\d+)', str(fm.get('source', ''))) or [None, None])[1]})
    wanted = {k for b in books for k in title_keys(b['title'])}

    db = sqlite3.connect(isfdb_path)
    by_key = defaultdict(set)
    def index(tid, title):
        # ISFDB titles count with and without their subtitle, as the book titles do.
        for k in {norm_title(title), norm_title(re.split(r'\s*[:;]\s*', title)[0])}:
            if k in wanted:
                by_key[k].add(tid)
    for tid, title in db.execute(f'SELECT title_id, title_title FROM titles WHERE title_ttype IN {WORKS}'):
        index(tid, title)
    for tid, title in db.execute(f'SELECT tt.title_id, tt.trans_title_title FROM trans_titles tt '
                                 f'JOIN titles t ON t.title_id = tt.title_id WHERE t.title_ttype IN {WORKS}'):
        index(tid, title)

    def family(tid):
        root = db.execute('SELECT title_parent FROM titles WHERE title_id = ?', (tid,)).fetchone()
        root = root[0] if root and root[0] else tid
        ids = [root] + [r[0] for r in db.execute('SELECT title_id FROM titles WHERE title_parent = ?', (root,))]
        rows = db.execute(f'SELECT title_id, title_title, title_copyright, title_ttype, title_storylen FROM titles '
                          f'WHERE title_id IN ({",".join("?" * len(ids))})', ids).fetchall()
        return root, [dict(zip(('id', 'title', 'date', 'ttype', 'storylen'), r)) for r in rows]

    def names(tids):
        """Every name of every author credited on these titles, pseudonyms both ways."""
        q = ','.join('?' * len(tids))
        aids = {r[0] for r in db.execute(f'SELECT author_id FROM canonical_author WHERE ca_status = 1 AND title_id IN ({q})', tids)}
        for a in list(aids):
            aids |= {r[0] for r in db.execute('SELECT pseudonym FROM pseudonyms WHERE author_id = ?', (a,))}
            aids |= {r[0] for r in db.execute('SELECT author_id FROM pseudonyms WHERE pseudonym = ?', (a,))}
        if not aids:
            return []
        q = ','.join('?' * len(aids))
        out = [n for r in db.execute(f'SELECT author_canonical, author_legalname FROM authors WHERE author_id IN ({q})', list(aids)) for n in r if n]
        return out + [r[0] for r in db.execute(f'SELECT trans_author_name FROM trans_authors WHERE author_id IN ({q})', list(aids))]

    rows = []
    for b in books:
        found, how = {}, None
        for i, k in enumerate(title_keys(b['title'])):
            for tid in by_key.get(k, ()):
                root, fam = family(tid)
                if root in found:
                    continue
                if any(same_person(a, n) for a in book_authors(b['author']) for n in names([r['id'] for r in fam])):
                    found[root] = fam
            if found:
                how = 'title' if i == 0 else 'short title'
                break
        cands = []
        for root, fam in found.items():
            years = [y for y in (year_of(r['date']) for r in fam) if y]
            main_row = next(r for r in fam if r['id'] == root)
            if years:
                cands.append({'root': root, 'year': min(years), 'row': main_row})
        pick, status = None, 'no match' if not found else 'no date'
        if cands:
            fitting = [c for c in cands if fits(c['row'], b['words'])]
            pick = min(fitting or cands, key=lambda c: (c['year'], c['root']))
            status = ('length mismatch' if not fitting else 'match' if len(cands) == 1
                      else 'by length' if len(fitting) == 1 else 'ambiguous')
        iy = pick['year'] if pick and status != 'length mismatch' else None   # a misfit is shown, not used
        year, source = iy, 'isfdb'
        if b['note_year'] and (iy is None or b['note_year'] < iy):
            year, source = b['note_year'], 'note'
        if year is None and b['library_year']:
            year, source = b['library_year'], 'library'
        if year is None and ISSUE.search(b['title']):   # a magazine issue: "Astounding Stories, March, 1931"
            year, source = int(ISSUE.search(b['title']).group(1)), 'title'
        if year is None:
            source = 'none'
        rows.append({**{k: b[k] for k in ('path', 'gutenberg', 'title', 'author', 'words', 'library_year', 'note_year')},
                     'isfdb_title_id': pick['root'] if pick else None, 'isfdb_title': html.unescape(pick['row']['title']) if pick else None,
                     'isfdb_type': (pick['row']['ttype'] + (f"/{pick['row']['storylen']}" if pick['row']['storylen'] else '')) if pick else None,
                     'isfdb_year': pick['year'] if pick else None, 'match': f'{status} ({how})' if how else status, 'candidates': len(cands),
                     'year': year, 'year_source': source})
    cols = list(rows[0])
    write_atomic(out, '\t'.join(cols) + '\n' + ''.join(
        '\t'.join('' if r[c] is None else str(r[c]).replace('\t', ' ') for c in cols) + '\n' for r in rows))
    summary = defaultdict(int)
    for r in rows:
        summary[r['match'].split(' (')[0]] += 1
        summary['year from ' + r['year_source']] += 1
        if r['year_source'] in ('isfdb', 'note') and r['isfdb_year'] and r['note_year'] and not r['match'].startswith('length'):
            summary['note agrees' if r['note_year'] == r['isfdb_year'] else 'note later' if r['note_year'] > r['isfdb_year'] else 'note earlier'] += 1
        if r['library_year'] is None:
            summary['undated: ' + r['year_source']] += 1
        elif r['year'] != r['library_year']:
            summary['library year changed'] += 1
    print(json.dumps(dict(sorted(summary.items())), indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:])
