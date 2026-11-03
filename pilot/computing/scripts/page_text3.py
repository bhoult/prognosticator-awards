"""Fetch a source's plain text (and, for records that carry one, its date); check quotes.

Extends page_text.py (Wikipedia, Chronicling America, plain HTML) with the source types of RUN3:
  archive.org items     https://archive.org/details/<id>[/...]  -> the item's OCR full text
                        (*_djvu.txt); date = the item's metadata `date`
  PDF                   any URL ending .pdf, or served as application/pdf (bitsavers,
                        worldradiohistory, NTRS downloads) -> pdftotext
  NASA NTRS record      https://ntrs.nasa.gov/citations/<id> -> title + abstract; date = publication date
  Crossref              https://api.crossref.org/works/<doi> -> title + abstract; date = issued
  Semantic Scholar      https://api.semanticscholar.org/graph/v1/paper/<id> -> title + abstract;
                        date = publicationDate (else year)
  Google Books API      https://www.googleapis.com/books/v1/volumes?q=... -> for the cited volume
                        (--volume ID, or `volume_id` in a source) its title, textSnippet and
                        description; date = the volume's publishedDate
Usage (from pilot/computing/):
  python3 -I scripts/page_text3.py URL                       # whole text
  python3 -I scripts/page_text3.py URL "term" [chars] [max]  # each place the term occurs, with
                                                             # [chars] (default 300) of context, in
                                                             # whitespace-flattened text (OCR breaks lines)
  python3 -I scripts/page_text3.py --check URL "quote" [--volume ID]   # FOUND / NOT FOUND (+ record date)
  python3 -I scripts/page_text3.py --date URL [--volume ID]  # the record's date, if it has one
Nothing is saved in the repository: text goes to stdout only (PDFs are converted in a
temporary directory that is deleted at once).
"""
import html
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402
import page_text  # noqa: E402

def norm(s):
    """page_text.norm, plus OCR soft hyphens joined ("sen¬ sors" -> "sensors")."""
    return re.sub(r"\s*¬\s*", "", page_text.norm(s))


def has_quote(page, quote):
    return norm(quote) in norm(page)
UA = net.UA.replace("pilot/0.2", "pilot/0.3")
net.UA = UA


def _strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s or ""))


def pdf_text(url):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "x.pdf"
        p = subprocess.run(["curl", "-sSL", "-m", "180", "-A", UA, "-o", str(f), "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        if p.stdout.strip() != "200":
            raise RuntimeError(f"HTTP {p.stdout.strip()}")
        if f.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError("not a PDF")
        q = subprocess.run(["pdftotext", "-q", str(f), "-"], capture_output=True, text=True)
        return q.stdout


def archive_item(url):
    m = re.match(r"https?://(?:www\.)?archive\.org/(?:details|stream|download)/([^/?#]+)", url)
    ident = m.group(1)
    md = net.get_json(f"https://archive.org/metadata/{ident}")
    files = [f["name"] for f in md.get("files", []) if f["name"].endswith("_djvu.txt")]
    sub = urllib.parse.unquote(url.split(ident, 1)[1]).strip("/")
    # a subfile named in the URL (details/<id>/<file stem>) wins; else the first text file
    pick = next((f for f in files if sub and f.startswith(sub.split("/page/")[0].split("?")[0])), None)
    if not pick and files:
        pick = files[0]
    if not pick:
        raise RuntimeError("no OCR text in item " + ident)
    code, body, _ = net.get(f"https://archive.org/download/{ident}/{urllib.parse.quote(pick)}",
                            accept="text/plain", timeout=180)
    if code != 200:
        raise RuntimeError(f"HTTP {code}")
    return body, str(md.get("metadata", {}).get("date", ""))


def crossref(url):
    d = net.get_json(url)["message"]
    parts = (d.get("issued") or d.get("published-print") or d.get("published-online") or {}).get("date-parts", [[]])[0]
    date = "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(parts))
    return "\n".join([" ".join(d.get("title", [])), _strip_tags(d.get("abstract", ""))]), date


def s2(url):
    u = url if "fields=" in url else url + ("&" if "?" in url else "?") + "fields=title,abstract,year,publicationDate"
    d = net.get_json(u)
    return "\n".join([d.get("title") or "", d.get("abstract") or ""]), d.get("publicationDate") or str(d.get("year") or "")


def ntrs(url):
    ident = re.search(r"/citations/(\d+)", url).group(1)
    d = net.get_json(f"https://ntrs.nasa.gov/api/citations/{ident}")
    pubs = d.get("publications") or []
    date = (pubs[0].get("publicationDate", "") if pubs else "")[:10]
    return "\n".join([d.get("title", ""), d.get("abstract", "")]), date


def gbooks(url, volume):
    d = net.get_json(url, tries=2)  # the shared daily quota is often exhausted (429)
    for it in d.get("items", []):
        if it.get("id") == volume:
            vi = it.get("volumeInfo", {})
            return "\n".join([vi.get("title", ""), _strip_tags(it.get("searchInfo", {}).get("textSnippet", "")),
                              _strip_tags(vi.get("description", ""))]), vi.get("publishedDate", "")
    raise RuntimeError(f"volume {volume} not in the API result")


def fetch(url, volume=None):
    """Return (text, record_date or '')."""
    if re.match(r"https?://(www\.)?googleapis\.com/books/v1/volumes", url):
        if not volume:
            raise RuntimeError("Google Books source needs a volume id")
        return gbooks(url, volume)
    if re.match(r"https?://api\.crossref\.org/works/", url):
        return crossref(url)
    if re.match(r"https?://api\.semanticscholar\.org/graph/v1/paper/", url):
        return s2(url)
    if re.match(r"https?://ntrs\.nasa\.gov/citations/\d+", url):
        return ntrs(url)
    if re.match(r"https?://(www\.)?archive\.org/(details|stream)/", url) or \
            re.match(r"https?://(www\.)?archive\.org/download/[^/]+/?$", url):
        return archive_item(url)
    if re.search(r"\.pdf($|[?#])", url, re.I):
        return pdf_text(url), ""
    if re.match(r"https?://\w+\.(m\.)?wikipedia\.org/wiki/", url) or re.match(r"https?://www\.loc\.gov/resource/sn", url):
        return page_text.text(url), ""
    return html_text(url), ""


def html_text(url):
    """page_text.html_text, but any 2xx with a body counts (PubMed answers 203)."""
    code, body, _ = net.get(url, accept="text/html,application/xhtml+xml,*/*", timeout=90)
    if not (200 <= code < 300) or not body.strip():
        raise RuntimeError(f"HTTP {code}")
    if body.lstrip().startswith("%PDF-"):
        raise RuntimeError("PDF served without .pdf in the URL")
    body = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", body)
    body = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>", "\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return "\n".join(re.sub(r"[ \t]+", " ", html.unescape(l)).strip() for l in body.splitlines() if l.strip())


def text(url, volume=None):
    return fetch(url, volume)[0]


if __name__ == "__main__":
    a = sys.argv[1:]
    vol = None
    if "--volume" in a:
        i = a.index("--volume")
        vol = a[i + 1]
        del a[i:i + 2]
    if a and a[0] == "--check":
        t, d = fetch(a[1], vol)
        ok = has_quote(t, a[2])
        print(("FOUND" if ok else "NOT FOUND") + (f" (record date {d})" if d else ""))
        sys.exit(0 if ok else 1)
    if a and a[0] == "--date":
        print(fetch(a[1], vol)[1])
        sys.exit(0)
    t, d = fetch(a[0], vol)
    if d:
        print(f"[record date: {d}]")
    if len(a) == 1:
        print(t)
    else:
        term = " ".join(a[1].lower().split())
        ctx = int(a[2]) if len(a) > 2 else 300
        mx = int(a[3]) if len(a) > 3 else 20
        flat = " ".join(t.split())
        low, start, n = flat.lower(), 0, 0
        while n < mx:
            i = low.find(term, start)
            if i < 0:
                break
            print("…" + flat[max(0, i - ctx): i + len(term) + ctx] + "…")
            print("--")
            start, n = i + len(term), n + 1
        if n == 0:
            print("(term not found)")
