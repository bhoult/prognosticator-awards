"""RUN3 step 5: target milestones in milestones3.jsonl that give any matched claim more than
40 years of lead and whose date differs from the second pass (or that are new), and that are
the ranking's milestone (first_practical_use, else first_demonstration): the others score nothing.
lead = milestone year - claim year over all claims matched to the concept.
Writes raw/check3_in.jsonl, and raw/check3_in_bN.jsonl split round-robin for N checkers.
Usage: python3 -I scripts/select_checks3.py [N]"""
import sys
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
rows = [json.loads(l) for l in open(HERE / "milestones3.jsonl")]
kinds = {}
for m in rows:
    kinds.setdefault(m["concept_id"], set()).add(m["kind"])
todo = []
for m in rows:
    if not m.get("target3"):
        continue
    if m["kind"] != ("first_practical_use" if "first_practical_use" in kinds[m["concept_id"]] else "first_demonstration"):
        continue
    lead = int(m["date"][:4]) - first.get(m["concept_id"], 9999)
    if lead > 40 and m["date"] != m.get("previous_date"):
        c = concepts[m["concept_id"]]
        todo.append({"concept_id": c["concept_id"], "name": c["name"], "definition": c["definition"],
                     "kind": m["kind"], "date": m["date"], "previous_date": m.get("previous_date"),
                     "what": m["what"], "fit": m.get("fit", ""), "sources": m["sources"],
                     "confidence": m["confidence"], "note": m.get("note", ""), "max_lead_years": lead})
(HERE / "raw/check3_in.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in todo))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
for b in range(n):
    (HERE / f"raw/check3_in_b{b + 1}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in todo[b::n]))
print(len(todo), "milestones to check, in", n, "batches")
for r in todo:
    print(" ", r["concept_id"], r["kind"], r["previous_date"], "->", r["date"], "lead", r["max_lead_years"])
