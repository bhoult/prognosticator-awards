"""RUN3 step 6: decide how every claim-concept pair is scored in run 3.

Pairs: every pair in judgments2.jsonl, plus every (claim, concept) match whose concept has a
run-3 milestone and had no pair before (concepts that gained a milestone). The ranking's
milestone is the concept's first_practical_use, else first_demonstration (milestones3.jsonl).
  gone    no run-3 milestone -> 0
  rule    run-3 milestone year <= claim year -> 0
  copy    second-pass pair with the same milestone kind and date -> copy the second-pass judgment
  judge   otherwise -> judged with judge_prompt2.md (re-judged, or judged for the first time)
Writes raw/pairs3.jsonl and mixed-concept batches raw/judge3_in/judge3_bNN.jsonl (fixed seed).
Usage: python3 -I scripts/make_pairs3.py <batch_size>
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
size = int(sys.argv[1]) if len(sys.argv) > 1 else 200
L = lambda f: [json.loads(l) for l in open(HERE / f)]  # noqa: E731
claims = {c["id"]: c for c in L("claims.jsonl")}
concepts = {c["concept_id"]: c for c in L("concepts2.jsonl")}
ms3 = {}
for m in L("milestones3.jsonl"):
    ms3.setdefault(m["concept_id"], {})[m["kind"]] = m
j2 = {(j["id"], j["concept_id"]): j for j in L("judgments2.jsonl")}


def pick(d):
    return d.get("first_practical_use") or d.get("first_demonstration")


keys = list(j2)
for r in L("matches.jsonl"):
    for c in r["concepts"]:
        if (r["id"], c) not in j2 and pick(ms3.get(c, {})) and (r["id"], c) not in keys:
            keys.append((r["id"], c))
pairs, n = [], 0
for cl, c in keys:
    o = j2.get((cl, c))
    m = pick(ms3.get(c, {}))
    year = claims[cl]["year"]
    p = {"id": cl, "concept_id": c, "year": year, "pair": o["pair"] if o else None,
         "old_kind": o["milestone_kind"] if o else None, "old_date": o["milestone_date"] if o else None}
    if not o:
        n += 1
        p["pair"] = f"t{n:04d}"
    if not m:
        p.update(action="gone", milestone_kind=None, milestone_date=None)
    else:
        p.update(milestone_kind=m["kind"], milestone_date=m["date"])
        if int(m["date"][:4]) <= year:
            p["action"] = "rule"
        elif o and o["milestone_kind"] == m["kind"] and o["milestone_date"] == m["date"]:
            p["action"] = "copy"
        else:
            p["action"] = "judge"
    pairs.append(p)
(HERE / "raw/pairs3.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in pairs))
todo = [p for p in pairs if p["action"] == "judge"]
random.Random(3).shuffle(todo)
outdir = HERE / "raw/judge3_in"
outdir.mkdir(parents=True, exist_ok=True)
for f in outdir.glob("judge3_b*.jsonl"):
    f.unlink()
nb = (len(todo) + size - 1) // size
for b in range(nb):
    chunk = todo[b::nb]  # spread evenly: every batch gets about len/nb pairs
    with open(outdir / f"judge3_b{b + 1:02d}.jsonl", "w") as f:
        for p in chunk:
            cl, k = claims[p["id"]], concepts[p["concept_id"]]
            m = ms3[p["concept_id"]][p["milestone_kind"]]
            f.write(json.dumps({"pair": p["pair"], "pub_year": cl["year"], "quote": cl["quote"],
                                "claim_description": cl["description"], "concept_name": k["name"],
                                "concept_description": k["definition"], "milestone_kind": p["milestone_kind"],
                                "milestone_date": p["milestone_date"], "milestone_summary": m["what"]},
                               ensure_ascii=False) + "\n")
    print(f"batch {b + 1}: {len(chunk)} pairs, {len({p['concept_id'] for p in chunk})} concepts")
print(len(pairs), "pairs", dict(Counter(p["action"] for p in pairs)), "new pairs", n, "->", nb, "batches")
