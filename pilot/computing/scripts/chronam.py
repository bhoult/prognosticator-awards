"""Search Chronicling America (now inside loc.gov) for newspaper pages.

Usage: python3 -I scripts/chronam.py "search words" FROM_YEAR TO_YEAR [n]
Prints date, newspaper, page URL and the start of the OCR text for up to n (default 10)
hits. Queries are slow (30-70 s). Read a hit's text with
  python3 -I scripts/page_text.py "<page URL>" "term" 2
(collection runs to 1963).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402

q, y0, y1 = sys.argv[1], sys.argv[2], sys.argv[3]
n = sys.argv[4] if len(sys.argv) > 4 else "10"
code, body, _ = net.get("https://www.loc.gov/collections/chronicling-america/",
                        {"q": q, "dates": f"{y0}/{y1}", "fo": "json", "c": n, "at": "results",
                         "sb": "date"}, timeout=150, tries=3)
if code != 200:
    sys.exit(f"HTTP {code}")
for r in json.loads(body).get("results", []):
    url = r.get("url", "").split("&q=")[0]
    paper = (r.get("partof_title") or [""])[0] if isinstance(r.get("partof_title"), list) else r.get("partof_title")
    desc = r.get("description")
    desc = desc[0] if isinstance(desc, list) and desc else (desc or "")
    print(r.get("date"), "|", paper, "|", url)
    print("   ", str(desc)[:160])
