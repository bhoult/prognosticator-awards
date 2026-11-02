"""Step 2a of RUN2: candidate Wikidata items for each concept.

For each concept, search Wikidata (through WDQS's mwapi EntitySearch service, which is
not rate-limited like wbsearchentities) for the concept name, its "X and Y" parts and its
aliases. Keep up to 6 hits per term with label, description and the number of
time-valued statements. Writes raw/wikidata_candidates.jsonl.
The choice of the one item that truly matches each definition is made by hand from this
file and recorded, with a reason, in raw/wikidata_picks.jsonl.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
Q = """
SELECT ?item ?itemLabel ?itemDescription ?ord (COUNT(DISTINCT ?t) AS ?ndates) WHERE {
  SERVICE wikibase:mwapi {
    bd:serviceParam wikibase:api "EntitySearch"; wikibase:endpoint "www.wikidata.org";
                    mwapi:search "%s"; mwapi:language "en"; mwapi:limit "6".
    ?item wikibase:apiOutputItem mwapi:item. ?ord wikibase:apiOrdinal true.
  }
  OPTIONAL { ?item ?p ?t . FILTER(DATATYPE(?t) = xsd:dateTime) }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} GROUP BY ?item ?itemLabel ?itemDescription ?ord ORDER BY ?ord
"""


def terms(c):
    name = re.sub(r"\(.*?\)", "", c["name"]).strip()
    ts = [name]
    for part in re.split(r"\band\b|,", name):
        part = part.strip()
        if part and part not in ts:
            ts.append(part)
    for a in c.get("aliases", [])[:4]:
        if a not in ts:
            ts.append(a)
    return ts[:7]


def one(c):
    seen = {}
    for t in terms(c):
        try:
            r = net.sparql(Q % t.replace('"', ""))
        except Exception as e:
            print("ERR", c["concept_id"], t, e, file=sys.stderr)
            continue
        for b in r["results"]["bindings"]:
            q = b["item"]["value"].rsplit("/", 1)[1]
            if q not in seen:
                seen[q] = {"qid": q, "label": b.get("itemLabel", {}).get("value", ""),
                           "description": b.get("itemDescription", {}).get("value", ""),
                           "ndates": int(b["ndates"]["value"]), "term": t}
    print(c["concept_id"], len(seen), flush=True)
    return {"concept_id": c["concept_id"], "name": c["name"],
            "definition": c["definition"], "candidates": list(seen.values())}


if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    concepts = [json.loads(line) for line in open(HERE / "concepts.jsonl")]
    with ThreadPoolExecutor(3) as ex:  # WDQS allows a few parallel queries per client
        out = list(ex.map(one, concepts))
    (HERE / "raw/wikidata_candidates.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
