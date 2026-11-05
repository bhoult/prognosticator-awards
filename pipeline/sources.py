"""Fetch a source's plain text (and, for records that carry one, its date); check quotes; search
archive.org's full text. The milestone researchers and the verifier (`match.py verify`) use
the same functions, so a quote the researcher's check found is checked the same way again.

From the computing pilot's net.py, page_text.py, page_text3.py and ia_search3.py (runs/match/PLAN.md §5).
Source types:
  Wikipedia             https://<lang>.wikipedia.org/wiki/<title> -> the API's plain-text extract
  Chronicling America   https://www.loc.gov/resource/sn.../?sp=N -> the page's OCR (ALTO XML)
  archive.org items     https://archive.org/details/<id>[/...] -> the item's OCR full text
                        (*_djvu.txt); date = the item's metadata `date`
  archive.org search    https://archive.org/services/search/beta/page_production/?user_query=
                        "<phrase>" AND identifier:<id>&service_backend=fts -> that item's highlighted
                        snippets (for lending-library books, whose OCR text answers 401); date = the
                        item's metadata `date`
  PDF                   any URL ending .pdf -> pdftotext
  NASA NTRS record      https://ntrs.nasa.gov/citations/<id> -> title + abstract; date = publication date
  Crossref              https://api.crossref.org/works/<doi> -> title + abstract; date = issued
  Semantic Scholar      https://api.semanticscholar.org/graph/v1/paper/<id> -> title + abstract;
                        date = publicationDate (else year)
  Google Books API      https://www.googleapis.com/books/v1/volumes?q=... with --volume ID -> that
                        volume's title, textSnippet and description; date = its publishedDate
  PubMed Central        https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/ -> the article through NCBI
                        E-utilities (the article pages may answer with a captcha); date = publication date
  anything else         the page's HTML, tags stripped

Usage:
  python3 -I pipeline/sources.py text URL                       # whole text
  python3 -I pipeline/sources.py text URL "term" [chars] [max]  # each place the term occurs, with
                                                                # [chars] (default 300) of context, in
                                                                # whitespace-flattened text
  python3 -I pipeline/sources.py check URL "quote" [--volume ID]  # FOUND / NOT FOUND (+ record date)
  python3 -I pipeline/sources.py date URL [--volume ID]         # the record's date, if it has one
  python3 -I pipeline/sources.py search '"phrase"' FROM_YEAR TO_YEAR [N] [collection]
                                                                # archive.org full-text search
Nothing is saved: text goes to stdout only (PDFs are converted in a temporary directory that is
deleted at once). Every request carries a descriptive User-Agent; a site that refuses is not
worked around.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

UA = ('prognosticator-awards/1.0 '
      '(https://github.com/bhoult/prognosticator-awards; research on predictions in fiction)')


# ---- HTTP (curl: retry with backoff on 429/5xx, honoring Retry-After) ----

def get(url, params=None, accept='application/json', tries=8, timeout=60):
    """(status, body, final_url); status -1 on network failure."""
    if params:
        url = url + ('&' if '?' in url else '?') + urllib.parse.urlencode(params)
    delay, last = 2.0, (-1, '', url)
    for _ in range(tries):
        p = subprocess.run(['curl', '-sSL', '-m', str(timeout), '-A', UA, '-H', f'Accept: {accept}',
                            '-D', '/dev/stderr', '-w', '\n%{http_code} %{url_effective}', url],
                           capture_output=True, text=True)
        body, tail = p.stdout.rsplit('\n', 1) if '\n' in p.stdout else ('', p.stdout)
        parts = tail.split(' ', 1)
        try:
            code = int(parts[0])
        except ValueError:
            code = -1
        last = (code or -1, body, parts[1] if len(parts) > 1 else url)
        if code == 200:
            return last
        if code in (0, 429, 500, 502, 503, 504) or p.returncode != 0:
            ra = next((l.split(':', 1)[1].strip() for l in p.stderr.splitlines()
                       if l.lower().startswith('retry-after:')), None)
            time.sleep(max(delay, float(ra) if ra and ra.isdigit() else 0))
            delay = min(delay * 2, 60)
            continue
        return last
    return last


def get_json(url, params=None, **kw):
    code, body, _ = get(url, params, **kw)
    if code != 200:
        raise RuntimeError(f'HTTP {code} for {url}: {body[:200]}')
    return json.loads(body)


# ---- quotes ----

def norm(s):
    """Case, whitespace, curly quotes and dashes ignored; OCR soft hyphens joined ("sen¬ sors")."""
    s = html.unescape(s)
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('\xa0', ' ')
    return re.sub(r'\s*¬\s*', '', re.sub(r'\s+', ' ', s).strip().lower())


def has_quote(page, quote):
    return norm(quote) in norm(page)


# ---- source types ----

def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))


def wiki_text(url):
    m = re.match(r'https?://(\w+)\.(?:m\.)?wikipedia\.org/wiki/([^#?]+)', url)
    lang, title = m.group(1), urllib.parse.unquote(m.group(2))
    d = get_json(f'https://{lang}.wikipedia.org/w/api.php',
                 {'action': 'query', 'prop': 'extracts', 'explaintext': 1, 'redirects': 1,
                  'titles': title.replace('_', ' '), 'format': 'json'})
    return '\n'.join(p.get('extract', '') for p in d['query']['pages'].values())


def loc_page_text(url):
    """OCR text of one Chronicling America page via its ALTO XML."""
    code, body, _ = get(url.split('?')[0] + '?' + '&'.join(
        [p for p in urllib.parse.urlparse(url).query.split('&') if p.startswith('sp=')] + ['fo=json']), timeout=120)
    m = re.search(r'segment=(/service/ndnp/[^"&]+?\.xml)', urllib.parse.unquote(body))
    if not m:
        raise RuntimeError('no OCR found for ' + url)
    code, xml, _ = get('https://tile.loc.gov/storage-services' + m.group(1), accept='application/xml', timeout=120)
    return '\n'.join(' '.join(html.unescape(w) for w in re.findall(r'CONTENT="([^"]*)"', tl))
                     for tl in re.findall(r'<TextLine\b.*?</TextLine>', xml, flags=re.S))


def pdf_text(url):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / 'x.pdf'
        p = subprocess.run(['curl', '-sSL', '-m', '180', '-A', UA, '-o', str(f), '-w', '%{http_code}', url],
                           capture_output=True, text=True)
        if p.stdout.strip() != '200':
            raise RuntimeError(f'HTTP {p.stdout.strip()}')
        if f.read_bytes()[:5] != b'%PDF-':
            raise RuntimeError('not a PDF')
        return subprocess.run(['pdftotext', '-q', str(f), '-'], capture_output=True, text=True).stdout


def archive_item(url):
    ident = re.match(r'https?://(?:www\.)?archive\.org/(?:details|stream|download)/([^/?#]+)', url).group(1)
    md = get_json(f'https://archive.org/metadata/{ident}')
    files = [f['name'] for f in md.get('files', []) if f['name'].endswith('_djvu.txt')]
    sub = urllib.parse.unquote(url.split(ident, 1)[1]).strip('/')
    # a subfile named in the URL (details/<id>/<file stem>) wins; else the first text file
    pick = next((f for f in files if sub and f.startswith(sub.split('/page/')[0].split('?')[0])), None) or \
        (files[0] if files else None)
    if not pick:
        raise RuntimeError('no OCR text in item ' + ident)
    code, body, _ = get(f'https://archive.org/download/{ident}/{urllib.parse.quote(pick)}', accept='text/plain', timeout=180)
    if code != 200:
        raise RuntimeError(f'HTTP {code}')
    return body, str(md.get('metadata', {}).get('date', ''))


def fts(url):
    """archive.org full-text search restricted to one item (user_query names `identifier:`): the
    text is the search's highlighted snippets from that item."""
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    ident = re.search(r'identifier:(\S+)', q['user_query'][0]).group(1)
    d = get_json(url, timeout=90)
    snips = [s.replace('{{{', '').replace('}}}', '') for x in d['response']['body']['hits']['hits']
             if x['fields']['identifier'] == ident for s in x.get('highlight', {}).get('text', [])]
    if not snips:
        raise RuntimeError('no snippet from item ' + ident)
    return '\n'.join(snips), str(get_json(f'https://archive.org/metadata/{ident}/metadata')['result'].get('date', ''))


def crossref(url):
    d = get_json(url)['message']
    parts = (d.get('issued') or d.get('published-print') or d.get('published-online') or {}).get('date-parts', [[]])[0]
    date = '-'.join(f'{x:02d}' if i else str(x) for i, x in enumerate(parts) if x)
    return '\n'.join([' '.join(d.get('title', [])), strip_tags(d.get('abstract', ''))]), date


def s2(url):
    u = url if 'fields=' in url else url + ('&' if '?' in url else '?') + 'fields=title,abstract,year,publicationDate'
    d = get_json(u)
    return '\n'.join([d.get('title') or '', d.get('abstract') or '']), d.get('publicationDate') or str(d.get('year') or '')


def ntrs(url):
    d = get_json(f"https://ntrs.nasa.gov/api/citations/{re.search(r'/citations/(\d+)', url).group(1)}")
    pubs = d.get('publications') or []
    return '\n'.join([d.get('title', ''), d.get('abstract', '')]), (pubs[0].get('publicationDate', '') if pubs else '')[:10]


def gbooks(url, volume):
    for it in get_json(url, tries=2).get('items', []):  # the shared daily quota is often exhausted (429)
        if it.get('id') == volume:
            vi = it.get('volumeInfo', {})
            return '\n'.join([vi.get('title', ''), strip_tags(it.get('searchInfo', {}).get('textSnippet', '')),
                              strip_tags(vi.get('description', ''))]), vi.get('publishedDate', '')
    raise RuntimeError(f'volume {volume} not in the API result')


def pmc(url):
    ident = re.search(r'/articles/PMC(\d+)', url).group(1)
    code, body, _ = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={ident}',
                        accept='application/xml', timeout=90)
    if code != 200 or '<article' not in body:
        raise RuntimeError(f'HTTP {code}')
    d = re.search(r'<pub-date[^>]*pub-type="(?:epub|ppub)"[^>]*>(.*?)</pub-date>', body, re.S) or \
        re.search(r'<pub-date[^>]*>(.*?)</pub-date>', body, re.S)
    part = lambda t: re.search(rf'<{t}>(\d+)</{t}>', d.group(1)) if d else None  # noqa: E731
    return strip_tags(body), '-'.join(f'{int(m.group(1)):02d}' for m in (part('year'), part('month'), part('day')) if m)


def html_text(url):
    """Any 2xx with a body counts (PubMed answers 203)."""
    code, body, _ = get(url, accept='text/html,application/xhtml+xml,*/*', timeout=90)
    if not (200 <= code < 300) or not body.strip():
        raise RuntimeError(f'HTTP {code}')
    if body.lstrip().startswith('%PDF-'):
        raise RuntimeError('PDF served without .pdf in the URL')
    body = re.sub(r'(?is)<(script|style|noscript)\b.*?</\1>', ' ', body)
    body = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>', '\n', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    return '\n'.join(re.sub(r'[ \t]+', ' ', html.unescape(l)).strip() for l in body.splitlines() if l.strip())


def fetch(url, volume=None):
    """(text, record date or '')."""
    if re.match(r'https?://(pmc\.ncbi\.nlm\.nih\.gov|www\.ncbi\.nlm\.nih\.gov/pmc)/articles/PMC\d+', url):
        return pmc(url)
    if re.match(r'https?://archive\.org/services/search/beta/page_production/\?', url):
        return fts(url)
    if re.match(r'https?://(www\.)?googleapis\.com/books/v1/volumes', url):
        if not volume:
            raise RuntimeError('a Google Books source needs a volume id')
        return gbooks(url, volume)
    if re.match(r'https?://api\.crossref\.org/works/', url):
        return crossref(url)
    if re.match(r'https?://api\.semanticscholar\.org/graph/v1/paper/', url):
        return s2(url)
    if re.match(r'https?://ntrs\.nasa\.gov/citations/\d+', url):
        return ntrs(url)
    if re.match(r'https?://(www\.)?archive\.org/(details|stream)/', url) or \
            re.match(r'https?://(www\.)?archive\.org/download/[^/]+/?$', url):
        return archive_item(url)
    if re.search(r'\.pdf($|[?#])', url, re.I):
        return pdf_text(url), ''
    if re.match(r'https?://\w+\.(m\.)?wikipedia\.org/wiki/', url):
        return wiki_text(url), ''
    if re.match(r'https?://www\.loc\.gov/resource/sn', url):
        return loc_page_text(url), ''
    return html_text(url), ''


def search(q, y0, y1, n=10, coll=''):
    """archive.org full-text search: (total, [(item url, year, title, page, [snippets])])."""
    uq = f'{q} AND year:[{y0} TO {y1}]' + (f' AND collection:{coll}' if coll else '')
    h = get_json('https://archive.org/services/search/beta/page_production/',
                 {'user_query': uq, 'service_backend': 'fts', 'hits_per_page': n}, timeout=90)['response']['body']['hits']
    return h['total'], [(f"https://archive.org/details/{x['fields']['identifier']}", x['fields'].get('year'),
                         x['fields'].get('title'), x['fields'].get('page_num'),
                         [' '.join(s.replace('{{{', '[').replace('}}}', ']').split())[:220]
                          for s in x.get('highlight', {}).get('text', [])[:2]]) for x in h['hits']]


def main(a):
    vol = None
    if '--volume' in a:
        i = a.index('--volume')
        vol = a[i + 1]
        del a[i:i + 2]
    cmd = a[0] if a else ''
    if cmd == 'check' and len(a) == 3:
        t, d = fetch(a[1], vol)
        ok = has_quote(t, a[2])
        print(('FOUND' if ok else 'NOT FOUND') + (f' (record date {d})' if d else ''))
        return 0 if ok else 1
    if cmd == 'date' and len(a) == 2:
        print(fetch(a[1], vol)[1])
        return 0
    if cmd == 'search' and len(a) >= 4:
        total, hits = search(a[1], a[2], a[3], int(a[4]) if len(a) > 4 else 10, a[5] if len(a) > 5 else '')
        print(f'{total} hits (search output, not a fetched page: read the item and copy the quote from there)')
        for url, year, title, page, snips in hits:
            print(f'{url} | {year} | {title} | page {page}')
            for s in snips:
                print('    …' + s + '…')
        return 0
    if cmd == 'text' and len(a) >= 2:
        t, d = fetch(a[1], vol)
        if d:
            print(f'[record date: {d}]')
        if len(a) == 2:
            print(t)
            return 0
        term, ctx, mx = ' '.join(a[2].lower().split()), int(a[3]) if len(a) > 3 else 300, int(a[4]) if len(a) > 4 else 20
        flat = ' '.join(t.split())
        low, start, n = flat.lower(), 0, 0
        while n < mx:
            i = low.find(term, start)
            if i < 0:
                break
            print('…' + flat[max(0, i - ctx): i + len(term) + ctx] + '…\n--')
            start, n = i + len(term), n + 1
        if n == 0:
            print('(term not found)')
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
