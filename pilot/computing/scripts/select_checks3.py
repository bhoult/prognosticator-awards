"""RUN3 step 5: target milestones in milestones3.jsonl that give any matched claim more than
40 years of lead and whose date differs from the second pass (or that are new).
lead = milestone year - claim year over all claims matched to the concept.
Writes raw/check3_in.jsonl. Usage: python3 -I scripts/select_checks3.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
years = {json.loads(l)["id"]: json.loads(l)["year"] for l in open(HERE / "claims.jsonl")}
first = {}
for l in open(HERE / "matches.jsonl"):
    r = json.loads(l)
    for c in r["concepts"]:
        first[c] = min(first.get(c, 9999), years[r["id"]])
concepts = {json.loads(l)["concept_id"]: json.loads(l) for l in open(HERE / "concepts2.jsonl")}
todo = []
for m in map(json.loads, open(HERE / "milestones3.jsonl")):
    if not m.get("target3"):
        continue
    lead = int(m["date"][:4]) - first.get(m["concept_id"], 9999)
    if lead > 40 and m["date"] != m.get("previous_date"):
        c = concepts[m["concept_id"]]
        todo.append({"concept_id": c["concept_id"], "name": c["name"], "definition": c["definition"],
                     "kind": m["kind"], "date": m["date"], "previous_date": m.get("previous_date"),
                     "what": m["what"], "fit": m.get("fit", ""), "sources": m["sources"],
                     "confidence": m["confidence"], "note": m.get("note", ""), "max_lead_years": lead})
(HERE / "raw/check3_in.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in todo))
print(len(todo), "milestones to check")
for r in todo:
    print(" ", r["concept_id"], r["kind"], r["previous_date"], "->", r["date"], "lead", r["max_lead_years"])
