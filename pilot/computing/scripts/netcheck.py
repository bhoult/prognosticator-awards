"""Step 1 of RUN2: check which evidence sources the network allows.

Writes raw/netcheck.jsonl. Usage: python3 -I scripts/netcheck.py (from pilot/computing/)
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
CHECKS = [
    ("wikidata_sparql", "https://query.wikidata.org/sparql",
     {"query": "SELECT ?d WHERE { wd:Q11035 wdt:P575 ?d }", "format": "json"}),
    ("wikidata_api", "https://www.wikidata.org/w/api.php",
     {"action": "wbsearchentities", "search": "ENIAC", "language": "en", "format": "json"}),
    ("wikipedia_api", "https://en.wikipedia.org/w/api.php",
     {"action": "query", "titles": "ENIAC", "prop": "info", "format": "json"}),
    ("chronicling_america_old", "https://chroniclingamerica.loc.gov/search/pages/results/",
     {"andtext": "electronic brain", "format": "json"}),
    ("chronicling_america_loc", "https://www.loc.gov/collections/chronicling-america/",
     {"q": "electronic brain", "fo": "json", "c": "1"}),
]
out = []
for name, url, params in CHECKS:
    # first attempt without retries, then with retries, to record both
    t = time.time()
    first = net.get(url, params, tries=1, timeout=120)
    code, body, final = net.get(url, params, tries=6, timeout=120)
    ok = code == 200
    if ok:
        try:
            json.loads(body)
        except Exception:
            ok = False
    out.append({"check": name, "url": url, "first_try_status": first[0], "status": code,
                "final_url": final, "json_ok": ok, "seconds": round(time.time() - t, 1),
                "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    print(out[-1])
(HERE / "raw/netcheck.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
