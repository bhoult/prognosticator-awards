"""Load library texts the way every model sees them: header removed, author and title blanked.

The blanked body is the canonical text. Chunk offsets, quote verification and
answer-key anchors all refer to it, so the three always line up.

    python -I pipeline/corpus.py find <book.md> <phrase> [<phrase> ...]   show where phrases occur
"""
import json
import re
import sys

BLANK = '[…]'


def read_book(path):
    """Return (front_matter dict, canonical body)."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    head, _, body = text.partition('\n---\n')
    fm = {}
    for line in head.splitlines()[1:]:
        key, _, value = line.partition(': ')
        try:
            fm[key] = json.loads(value)
        except json.JSONDecodeError:
            fm[key] = value
    return fm, blank_identity(body.lstrip('\n'), fm)


def blank_identity(body, fm):
    """Replace the author's name and the work's title, so a model can't recall the book from memory."""
    names = []
    for author in str(fm.get('author', '')).split(';'):
        author = author.strip()
        if author and author.lower() not in ('unknown', 'anonymous', 'various'):
            names.append(author)
            parts = author.replace('.', ' ').split()
            if len(parts) > 1 and len(parts[-1]) > 3:
                names.append(parts[-1])           # surname alone ("Wells")
    title = re.split(r'\s*[(:]', str(fm.get('title', '')))[0].strip()
    if len(title) > 6:
        names.append(title)
    for n in sorted(set(names), key=len, reverse=True):
        body = re.sub(r'(?<!\w)' + re.escape(n) + r'(?!\w)', BLANK, body, flags=re.I)
    return body


def windows(body, start, end, n):
    """Paragraph-aligned windows of about n words over body[start:end]; a short tail joins the last."""
    out, cur, cur_start, words = [], None, start, 0
    for m in re.finditer(r'(?s).+?(?:\n\s*\n|$)', body[start:end]):
        if cur is None:
            cur_start = start + m.start()
        cur = start + m.end()
        words += len(m.group(0).split())
        if words >= n:
            out.append((cur_start, cur))
            cur, words = None, 0
    if cur is not None:
        if out and words < n // 3:  # fold a short tail into the last window
            out[-1] = (out[-1][0], cur)
        else:
            out.append((cur_start, cur))
    return out


def find(path, phrases, width=110):
    _, body = read_book(path)
    for p in phrases:
        hits = [m.start() for m in re.finditer(re.escape(p), body, re.I)]
        print(f'[{p}] {len(hits)} hit(s)')
        for at in hits[:3]:
            snippet = body[max(0, at - 60):at + width].replace('\n', ' ')
            print(f'   @{at}: …{snippet}…')


if __name__ == '__main__':
    if sys.argv[1] == 'find':
        find(sys.argv[2], sys.argv[3:])
