"""Step 2b of RUN2: dated statements for the Wikidata item picked for each concept.

Reads raw/wikidata_picks.jsonl ({concept_id, qid|null, reason}) and fetches every
time-valued statement of the item (P575 discovery or invention, P571 inception, P1619
official opening, P606 first flight, P580 start time, P585 point in time, P577
publication date, ...) with its precision, plus time-valued qualifiers.
Writes raw/wikidata_dates.jsonl (one line per dated statement) and concepts2.jsonl
(concepts.jsonl unchanged except `wikidata`).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
PREC = {9: "year", 10: "month", 11: "day", 8: "decade", 7: "century"}
Q = """
SELECT ?prop ?propLabel ?t ?prec ?qprop ?qpropLabel WHERE {
  wd:%s ?p ?st . ?prop wikibase:claim ?p ; wikibase:statementValue ?psv .
  ?st ?psv ?tv . ?tv wikibase:timeValue ?t ; wikibase:timePrecision ?prec .
  ?st wikibase:rank ?rank . FILTER(?rank != wikibase:DeprecatedRank)
  BIND("" AS ?qprop)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""
QL = 'SELECT ?l WHERE { wd:%s rdfs:label ?l FILTER(LANG(?l)="en") }'


def fmt(t, prec):
    t = t.lstrip("+")
    if prec >= 11:
        return t[:10]
    if prec == 10:
        return t[:7]
    if prec == 8:
        return t[:3] + "0s"
    if prec == 7:
        return t[:2] + "00s"
    return t[:4] if not t.startswith("-") else t[:5]


picks = {json.loads(l)["concept_id"]: json.loads(l) for l in open(HERE / "raw/wikidata_picks.jsonl")}
rows = []
for cid, p in picks.items():
    q = p.get("qid")
    if not q:
        continue
    lab = net.sparql(QL % q)["results"]["bindings"]
    label = lab[0]["l"]["value"] if lab else ""
    for b in net.sparql(Q % q)["results"]["bindings"]:
        prec = int(b["prec"]["value"])
        rows.append({"concept_id": cid, "qid": q, "label": label,
                     "property": b["prop"]["value"].rsplit("/", 1)[1],
                     "property_label": b["propLabel"]["value"],
                     "date": fmt(b["t"]["value"], prec), "precision": PREC.get(prec, str(prec)),
                     "url": f"https://www.wikidata.org/wiki/{q}"})
    print(cid, q, label, sum(r["concept_id"] == cid for r in rows), flush=True)
(HERE / "raw/wikidata_dates.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(HERE / "concepts2.jsonl", "w") as f:
    for l in open(HERE / "concepts.jsonl"):
        c = json.loads(l)
        c["wikidata"] = (picks.get(c["concept_id"]) or {}).get("qid")
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print(len(rows), "dated statements")
