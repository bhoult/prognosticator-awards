"""Write the release database (DESIGN §10; PLAN §11): one SQLite file and one CSV per table, built from
the scored runs of both tranches and the awards.

    python -I pipeline/export_db.py [run ...]      # default: full b

Out: work/release/prognosticator-awards.sqlite, work/release/csv/<table>.csv and a zip of the CSVs, for
a GitHub release (never git: the claims and judgments are tens of megabytes). Books are cited by title,
authors and year under the export's opaque book id, never by their library path. The last run named
holds every tranche's registry and milestones (a tranche-B run starts from tranche A's).
"""
import csv
import json
import os
import sqlite3
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match

OUT = os.path.join(match.ROOT, 'work', 'release')
DB = os.path.join(OUT, 'prognosticator-awards.sqlite')

SCHEMA = """
CREATE TABLE books (            -- one published work; `book` is the claims export's opaque id
    book TEXT PRIMARY KEY, title TEXT, authors TEXT, year INTEGER, corpus_group TEXT,
    claims INTEGER, strict INTEGER);
CREATE TABLE claims (           -- every prediction the extraction kept, as the matchers and judges saw it
    id TEXT PRIMARY KEY, book TEXT REFERENCES books(book), year INTEGER, year_source TEXT, tranche TEXT,
    quote TEXT, description TEXT, category TEXT, specificity INTEGER, stated_time TEXT, polarity TEXT,
    confidence TEXT, valence TEXT, voice TEXT, domain TEXT, second_order INTEGER);
CREATE TABLE concepts (         -- the registry: the ideas claims are matched to
    concept_id TEXT PRIMARY KEY, name TEXT, definition TEXT, type TEXT, domains TEXT, aliases TEXT,
    came_true_guess TEXT, tranche TEXT);
CREATE TABLE milestones (       -- when an idea came true, by kind; sources in milestone_sources
    concept_id TEXT REFERENCES concepts(concept_id), kind TEXT, date TEXT, what TEXT, fit TEXT,
    confidence TEXT, tier INTEGER, note TEXT, PRIMARY KEY (concept_id, kind));
CREATE TABLE milestone_sources (
    concept_id TEXT, kind TEXT, n INTEGER, url TEXT, publisher TEXT, title TEXT, quote TEXT, date TEXT,
    source_kind TEXT, PRIMARY KEY (concept_id, kind, n));
CREATE TABLE matches (          -- the matcher's answer per claim: up to two concepts, or a code
    claim TEXT PRIMARY KEY REFERENCES claims(id), code TEXT, reason TEXT, quote_carries INTEGER);
CREATE TABLE claim_concepts (
    claim TEXT REFERENCES claims(id), concept_id TEXT REFERENCES concepts(concept_id), n INTEGER,
    PRIMARY KEY (claim, concept_id));
CREATE TABLE judgments (        -- two judges' closeness (a, b), a third (c) where they were two steps apart
    pair TEXT PRIMARY KEY, claim TEXT REFERENCES claims(id), concept_id TEXT, polarity TEXT,
    milestone_kind TEXT, milestone_date TEXT, lead INTEGER, a REAL, b REAL, c REAL, score REAL,
    rationale_a TEXT, rationale_b TEXT, rationale_c TEXT, tranche TEXT);
CREATE TABLE resolutions (      -- what became of each claim
    claim TEXT PRIMARY KEY REFERENCES claims(id), resolution TEXT, why TEXT, deadline TEXT);
CREATE TABLE entries (          -- the scoring rows: a book's best claim per realized idea
    claim TEXT REFERENCES claims(id), book TEXT REFERENCES books(book), concept_id TEXT, kind TEXT, date TEXT,
    lead INTEGER, score REAL, points REAL, tranche TEXT, PRIMARY KEY (book, concept_id, tranche));
CREATE TABLE awards (           -- runs/match/awards.json: winners (place 1) and runners-up
    award TEXT, title TEXT, rule TEXT, place INTEGER, name TEXT, points REAL, stat TEXT, why TEXT,
    PRIMARY KEY (award, place));
CREATE VIEW realized AS
    SELECT e.points, e.score, e.lead, b.authors, b.title, b.year, c.name AS idea, e.date AS came_true, cl.quote
    FROM entries e JOIN books b USING (book) JOIN concepts c USING (concept_id) JOIN claims cl ON cl.id = e.claim
    ORDER BY e.points DESC;
"""


def rows(path):
    return match.read_jsonl(path)[0] if os.path.exists(path) else []


def text(v):
    return '; '.join(v) if isinstance(v, list) else v


def build(runs):
    tranche = {r: 'A' if r == 'full' else 'B' for r in runs}
    os.makedirs(os.path.join(OUT, 'csv'), exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    db = sqlite3.connect(DB)
    db.executescript(SCHEMA)
    put = lambda t, rs: db.executemany(f'INSERT INTO {t} VALUES ({",".join("?" * len(rs[0]))})', rs) if rs else None

    books, claims = {}, {}
    for r in runs:
        for b in rows(match.rd(r, 'books.jsonl')):
            w = books.setdefault(b['book'], dict(b, claims=0, strict=0))
            w['claims'], w['strict'] = w['claims'] + b.get('claims', 0), w['strict'] + b.get('strict', 0)
        claims.update({c['id']: c for c in match.claims(r)})
    put('books', [(k, b['title'], text(b['authors']), b['year'], b['group'], b['claims'], b['strict'])
                  for k, b in sorted(books.items())])
    put('claims', [(i, c['book'], c['year'], c.get('year_source'), c['tranche'], c['quote'], c['description'],
                    c['category'], c['specificity'], c['stated_time'], c['polarity'], c['confidence'], c['valence'],
                    c['voice'], c['domain'], int(bool(c.get('second_order')))) for i, c in sorted(claims.items())])

    last = runs[-1]
    match.use_run(last)
    reg = match.final_registry(last)
    put('concepts', [(c['concept_id'], c['name'], c['definition'], c.get('type'), text(c.get('domains')),
                      text(c.get('aliases')), c.get('came_true_guess'), c.get('tranche', 'A')) for c in reg])
    ms = rows(os.path.join(match.OUT, 'milestones.jsonl'))
    put('milestones', [(m['concept_id'], m['kind'], m['date'], m.get('what'), m.get('fit'), m.get('confidence'),
                        m.get('tier'), m.get('note')) for m in ms])
    put('milestone_sources', [(m['concept_id'], m['kind'], n, s.get('url'), s.get('publisher'), s.get('title'),
                               s.get('quote'), s.get('date'), s.get('kind'))
                              for m in ms for n, s in enumerate(m.get('sources') or [])])

    for r in runs:
        ms_ = rows(match.rd(r, 'matches.jsonl'))
        put('matches', [(m['id'], m['code'], m.get('reason'), int(bool(m.get('quote_carries')))) for m in ms_])
        put('claim_concepts', [(m['id'], k, n) for m in ms_ for n, k in enumerate(m['concepts'])])
        put('judgments', [(j['pair'], j['claim'], j['concept_id'], j['polarity'], j['milestone_kind'], j['milestone_date'],
                           j['lead'], j['a'], j['b'], j.get('c'), j['score'], j.get('rationale_a'), j.get('rationale_b'),
                           j.get('rationale_c'), tranche[r]) for j in rows(match.rd(r, 'judgments.jsonl'))])
        put('resolutions', [(x['id'], x['resolution'], x['why'], x.get('deadline')) for x in rows(match.rd(r, 'resolutions.jsonl'))])
        put('entries', [(e['claim'], e['book'], e['concept_id'], e['kind'], e['date'], e['lead'], e['score'], e['points'],
                         tranche[r]) for e in rows(match.rd(r, 'entries.jsonl'))])

    aw = json.load(open(os.path.join(match.ROOT, 'runs', 'match', 'awards.json'), encoding='utf-8'))
    notes = {(n['id'], n['winner']): n['why'] for n in rows(os.path.join(match.ROOT, 'runs', 'match', 'awards_notes.jsonl'))}
    put('awards', [(a['id'], a['title'], a.get('rule'), p, w['name'], w.get('points'), w.get('stat'),
                    notes.get((a['id'], w['name'])) if p == 1 else None)
                   for a in aw['awards'] for p, w in enumerate(([a['winner']] if a.get('winner') else []) + a.get('runners', []), 1)])
    db.commit()

    tables = [t for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    zpath = os.path.join(OUT, 'prognosticator-awards-csv.zip')
    with zipfile.ZipFile(zpath + '.tmp', 'w', zipfile.ZIP_DEFLATED) as z:
        for t in tables:
            cur = db.execute(f'SELECT * FROM {t}')
            path = os.path.join(OUT, 'csv', t + '.csv')
            with open(path, 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                w.writerow([d[0] for d in cur.description])
                w.writerows(cur)
            z.write(path, t + '.csv')
            print(f"{t:18} {db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>8,}")
    os.replace(zpath + '.tmp', zpath)
    db.execute('VACUUM')
    db.close()
    print(f'-> {match.rel(DB)} ({os.path.getsize(DB) / 1e6:.1f} MB), {match.rel(zpath)} ({os.path.getsize(zpath) / 1e6:.1f} MB)')


if __name__ == '__main__':
    build(sys.argv[1:] or ['full', 'b'])
