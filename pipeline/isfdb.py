"""Copy the ISFDB tables the dating pass needs from an ISFDB MySQL backup into SQLite.

    python -I pipeline/isfdb.py <backup.zip> <out.sqlite>

The backup is the zipped mysqldump from the ISFDB Downloads page (wiki login required; files
on Google Drive, fetched with gdown as ISFDB's own download script does). ISFDB data is CC BY 4.0.
Only the tables below are read: titles, their authors, pseudonyms and alternate names. Nothing
else in the dump is touched. Text is stored as ISFDB has it: latin-1, with HTML entities for
other characters.
"""
import os
import re
import sqlite3
import sys
import zipfile

TABLES = ('titles', 'authors', 'canonical_author', 'pseudonyms', 'trans_titles', 'trans_authors')
TOKEN = re.compile(r"""\(|\)|,|;|NULL|'(?:[^'\\]|\\.)*'|-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?""", re.S)
ESCAPES = {'0': '\0', 'b': '\b', 'n': '\n', 'r': '\r', 't': '\t', 'Z': '\x1a'}


def unescape(s):
    return re.sub(r'\\(.)', lambda m: ESCAPES.get(m.group(1), m.group(1)), s[1:-1], flags=re.S)


def rows(values):
    """Tuples from the part of an INSERT statement after VALUES."""
    row, depth = [], 0
    for m in TOKEN.finditer(values):
        t = m.group(0)
        if t == '(':
            row, depth = [], 1
        elif t == ')':
            depth = 0
            yield row
        elif t in (',', ';'):
            continue
        elif t == 'NULL':
            row.append(None)
        elif t[0] == "'":
            row.append(unescape(t))
        else:
            row.append(float(t) if '.' in t or 'e' in t.lower() else int(t))


def main(zip_path, out):
    z = zipfile.ZipFile(zip_path)
    dump = z.open(z.namelist()[0])
    if os.path.exists(out):
        os.remove(out)
    db = sqlite3.connect(out + '.part')
    cols, cur, counts = {}, None, {}
    for raw in dump:
        line = raw.decode('latin-1')
        m = re.match(r'CREATE TABLE `(\w+)`', line)
        if m:
            cur = m.group(1) if m.group(1) in TABLES else None
            if cur:
                cols[cur] = []
            continue
        if cur:
            m = re.match(r'\s+`(\w+)`', line)
            if m:
                cols[cur].append(m.group(1))
            elif line.startswith(')'):
                db.execute(f'DROP TABLE IF EXISTS {cur}')
                db.execute(f'CREATE TABLE {cur} ({", ".join(cols[cur])})')
                cur = None
            continue
        m = re.match(r'INSERT INTO `(\w+)` VALUES ', line)
        if m and m.group(1) in TABLES:
            t = m.group(1)
            batch = list(rows(line[m.end():]))
            bad = [r for r in batch if len(r) != len(cols[t])]
            if bad:
                raise SystemExit(f'{t}: a row has {len(bad[0])} values, expected {len(cols[t])}')
            db.executemany(f'INSERT INTO {t} VALUES ({",".join("?" * len(cols[t]))})', batch)
            counts[t] = counts.get(t, 0) + len(batch)
    for sql in ('CREATE UNIQUE INDEX titles_id ON titles (title_id)',
                'CREATE UNIQUE INDEX authors_id ON authors (author_id)',
                'CREATE INDEX titles_parent ON titles (title_parent)',
                'CREATE INDEX ca_title ON canonical_author (title_id)',
                'CREATE INDEX ca_author ON canonical_author (author_id)',
                'CREATE INDEX pseudo_author ON pseudonyms (author_id)',
                'CREATE INDEX pseudo_pseudonym ON pseudonyms (pseudonym)',
                'CREATE INDEX trans_titles_title ON trans_titles (title_id)',
                'CREATE INDEX trans_authors_author ON trans_authors (author_id)'):
        db.execute(sql)
    db.execute('CREATE TABLE source (backup, imported_at)')
    db.execute("INSERT INTO source VALUES (?, datetime('now'))", (os.path.basename(zip_path),))
    db.commit()
    db.close()
    os.replace(out + '.part', out)
    print(', '.join(f'{t} {n:,}' for t, n in counts.items()))


if __name__ == '__main__':
    main(*sys.argv[1:])
