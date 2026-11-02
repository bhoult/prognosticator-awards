"""Fetch a page and print its plain text, or only the lines that contain a term.

Usage (from pilot/computing/):
  python3 -I scripts/page_text.py URL                 # whole text
  python3 -I scripts/page_text.py URL "term" [ctx]    # matching sentences/lines only
  python3 -I scripts/page_text.py --check URL "quote" # exit 0 if quote is on the page

Wikipedia article URLs are read through the API's plain-text extract; Chronicling America
page URLs (www.loc.gov/resource/sn.../ed-N/?sp=N) through the page's OCR (ALTO XML).
Nothing is saved: text goes to stdout only (article text is never stored in the repo).
"""
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402


def norm(s):
    s = html.unescape(s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def wiki_text(url):
    m = re.match(r"https?://(\w+)\.(?:m\.)?wikipedia\.org/wiki/([^#?]+)", url)
    lang, title = m.group(1), urllib.parse.unquote(m.group(2))
    d = net.get_json(f"https://{lang}.wikipedia.org/w/api.php",
                     {"action": "query", "prop": "extracts", "explaintext": 1, "redirects": 1,
                      "titles": title.replace("_", " "), "format": "json"})
    return "\n".join(p.get("extract", "") for p in d["query"]["pages"].values())


def loc_page_text(url):
    """OCR text of one Chronicling America page via its ALTO XML."""
    code, body, _ = net.get(url.split("?")[0] + "?" + "&".join(
        [p for p in urllib.parse.urlparse(url).query.split("&") if p.startswith("sp=")] + ["fo=json"]),
        timeout=120)
    m = re.search(r'segment=(/service/ndnp/[^"&]+?\.xml)', urllib.parse.unquote(body))
    if not m:
        raise RuntimeError("no OCR found for " + url)
    alto = "https://tile.loc.gov/storage-services" + m.group(1)
    code, xml, _ = net.get(alto, accept="application/xml", timeout=120)
    lines = []
    for tl in re.findall(r"<TextLine\b.*?</TextLine>", xml, flags=re.S):
        lines.append(" ".join(html.unescape(w) for w in re.findall(r'CONTENT="([^"]*)"', tl)))
    return "\n".join(lines)


def html_text(url):
    code, body, _ = net.get(url, accept="text/html,application/xhtml+xml,*/*", timeout=90)
    if code != 200:
        raise RuntimeError(f"HTTP {code}")
    body = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", body)
    body = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>", "\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return "\n".join(re.sub(r"[ \t]+", " ", html.unescape(l)).strip()
                     for l in body.splitlines() if l.strip())


def text(url):
    if re.match(r"https?://\w+\.(m\.)?wikipedia\.org/wiki/", url):
        return wiki_text(url)
    if re.match(r"https?://www\.loc\.gov/resource/sn", url):
        return loc_page_text(url)
    return html_text(url)


def has_quote(page, quote):
    return norm(quote) in norm(page)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--check":
        ok = has_quote(text(a[1]), a[2])
        print("FOUND" if ok else "NOT FOUND")
        sys.exit(0 if ok else 1)
    t = text(a[0])
    if len(a) == 1:
        print(t)
    else:
        term, ctx = a[1].lower(), int(a[2]) if len(a) > 2 else 0
        ls = t.splitlines()
        for i, l in enumerate(ls):
            if term in l.lower():
                print("\n".join(ls[max(0, i - ctx): i + ctx + 1]))
                print("--")
