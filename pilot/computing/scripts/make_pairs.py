"""Build judge inputs from matches.jsonl and milestones.jsonl.

For every (claim, concept) match whose concept has a first_practical_use milestone (else
first_demonstration), make one pair. Pairs whose milestone year is not after the claim's
year score 0 by rule (DESIGN §8: L <= 0 is not a prediction) and are not sent to a judge.
The rest are written, sorted by concept, into judge batches holding only what the judge
may see: pair id, year, quote, description, concept name/definition, milestone kind, date
and summary. Writes raw/pairs.jsonl (full mapping) and <outdir>/judge_batchNN.jsonl.

Usage: python3 -I scripts/make_pairs.py <outdir> <batch_size>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
outdir, size = Path(sys.argv[1]), int(sys.argv[2])
claims = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / "claims.jsonl")}
concepts = {json.loads(l)["concept_id"]: json.loads(l) for l in open(HERE / "concepts.jsonl")}
ms = {}
for l in open(HERE / "milestones.jsonl"):
    m = json.loads(l)
    ms.setdefault(m["concept_id"], {})[m["kind"]] = m
pairs = []
for l in open(HERE / "matches.jsonl"):
    r = json.loads(l)
    for c in r["concepts"]:
        m = ms.get(c, {}).get("first_practical_use") or ms.get(c, {}).get("first_demonstration")
        if not m:
            continue
        cl = claims[r["id"]]
        pairs.append({"id": r["id"], "concept_id": c, "milestone_kind": m["kind"],
                      "milestone_date": m["date"], "year": cl["year"],
                      "rule_zero": int(m["date"][:4]) <= cl["year"]})
pairs.sort(key=lambda p: (p["concept_id"], p["year"], p["id"]))
for i, p in enumerate(pairs, 1):
    p["pair"] = f"q{i:04d}"
(HERE / "raw" / "pairs.jsonl").write_text("".join(json.dumps(p) + "\n" for p in pairs))
todo = [p for p in pairs if not p["rule_zero"]]
outdir.mkdir(parents=True, exist_ok=True)
for b in range(0, len(todo), size):
    with open(outdir / f"judge_batch{b // size + 1:02d}.jsonl", "w") as f:
        for p in todo[b:b + size]:
            cl, k, m = claims[p["id"]], concepts[p["concept_id"]], ms[p["concept_id"]][p["milestone_kind"]]
            f.write(json.dumps({"pair": p["pair"], "pub_year": cl["year"], "quote": cl["quote"],
                                "claim_description": cl["description"], "concept_name": k["name"],
                                "concept_description": k["definition"], "milestone_kind": p["milestone_kind"],
                                "milestone_date": p["milestone_date"], "milestone_summary": m["what"]},
                               ensure_ascii=False) + "\n")
print(len(pairs), "pairs;", len(pairs) - len(todo), "zero by rule;", len(todo), "to judge in",
      (len(todo) + size - 1) // size, "batches")
