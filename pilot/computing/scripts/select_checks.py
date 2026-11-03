"""Step 4 of RUN2: pick milestones that give any matched claim more than 40 years of lead.

lead = milestone year - claim year, over all claims matched to the concept (matches.jsonl,
years from claims.jsonl). Writes raw/check_in_bNN.jsonl batches for the checker agents.
Usage: python3 -I scripts/select_checks.py <n_batches>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
nb = int(sys.argv[1]) if len(sys.argv) > 1 else 0
years = {json.loads(l)["id"]: json.loads(l)["year"] for l in open(HERE / "claims.jsonl")}
first = {}
for l in open(HERE / "matches.jsonl"):
    r = json.loads(l)
    for c in r["concepts"]:
        first[c] = min(first.get(c, 9999), years[r["id"]])
concepts = {json.loads(l)["concept_id"]: json.loads(l) for l in open(HERE / "concepts2.jsonl")}
todo = []
for l in open(HERE / "milestones2.jsonl"):
    m = json.loads(l)
    lead = int(m["date"][:4]) - first.get(m["concept_id"], 9999)
    if lead > 40:
        c = concepts[m["concept_id"]]
        todo.append({"concept_id": c["concept_id"], "name": c["name"], "definition": c["definition"],
                     "kind": m["kind"], "date": m["date"], "what": m["what"], "sources": m["sources"],
                     "confidence": m["confidence"], "note": m.get("note", ""), "max_lead_years": lead})
print(len(todo), "milestones with lead > 40 years")
if nb:
    size = -(-len(todo) // nb)
    for b in range(nb):
        chunk = todo[b * size:(b + 1) * size]
        (HERE / f"raw/check_in_b{b + 1:02d}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in chunk))
        print(b + 1, len(chunk))
