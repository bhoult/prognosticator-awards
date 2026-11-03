"""Search the full text of archive.org's scanned books and magazines (its FTS service).

Usage: python3 -I scripts/ia_search3.py "phrase or words" FROM_YEAR TO_YEAR [N] [collection]
  e.g. python3 -I scripts/ia_search3.py '"security robot"' 1980 1989 10 computerworld
Prints, per hit: the item URL (cite it as https://archive.org/details/<identifier>), year,
title and up to two short highlighted snippets. Snippets are search output, not a fetched
page: read the item with page_text3.py and copy the quote from there.
Useful collections: computerworld, infoworld, byte-magazine, popular-science-magazine
(or none for everything)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402
import page_text3  # noqa: E402,F401  (sets the User-Agent)

q, y0, y1 = sys.argv[1], sys.argv[2], sys.argv[3]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 10
coll = sys.argv[5] if len(sys.argv) > 5 else ""
uq = f"{q} AND year:[{y0} TO {y1}]" + (f" AND collection:{coll}" if coll else "")
d = net.get_json("https://archive.org/services/search/beta/page_production/",
                 {"user_query": uq, "service_backend": "fts", "hits_per_page": n}, timeout=90)
h = d["response"]["body"]["hits"]
print(f"{h['total']} hits for {uq}")
for x in h["hits"]:
    f = x["fields"]
    print(f"https://archive.org/details/{f['identifier']} | {f.get('year')} | {f.get('title')} | page {f.get('page_num')}")
    for s in x.get("highlight", {}).get("text", [])[:2]:
        print("    …" + " ".join(s.replace("{{{", "[").replace("}}}", "]").split())[:220] + "…")
