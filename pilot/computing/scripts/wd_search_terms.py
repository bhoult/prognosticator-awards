"""Step 2a (second round): search Wikidata for hand-chosen terms where the name search
missed the obvious item. Usage: python3 -I scripts/wd_search_terms.py concept_id=term ...
Appends to raw/wikidata_candidates2.jsonl."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402
from wd_candidates import Q  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
from concurrent.futures import ThreadPoolExecutor


def one(arg):
    cid, term = arg.split("=", 1)
    r = net.sparql(Q % term)
    c = [{"qid": b["item"]["value"].rsplit("/", 1)[1], "label": b.get("itemLabel", {}).get("value", ""),
          "description": b.get("itemDescription", {}).get("value", ""), "ndates": int(b["ndates"]["value"]),
          "term": term} for b in r["results"]["bindings"]]
    return {"concept_id": cid, "term": term, "candidates": c}


with ThreadPoolExecutor(3) as ex:
    res = list(ex.map(one, sys.argv[1:]))
with open(HERE / "raw/wikidata_candidates2.jsonl", "a") as f:
    for r in res:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("##", r["concept_id"], "=", r["term"])
        for c in r["candidates"]:
            print("   ", c["qid"], c["label"][:40], "|", c["description"][:70], "|", c["ndates"])
