"""Step 5 of RUN2: decide, for every claim-concept pair, how it is scored in run 2.

Pairs: every (claim, concept) match whose concept has a second-pass milestone (the
first_practical_use one, else first_demonstration, the first pass's rule), plus every
first-pass pair. For each:
  copy    first-pass pair, same milestone kind and same date in run 2 -> copy the judgment
          (the agents re-word every description, so the event is compared by kind+date;
          pairs whose event changed under the same date are listed for review)
  rule    run-2 milestone year <= claim year -> score 0 by rule
  gone    first-pass pair whose concept has no run-2 milestone -> score 0, no milestone
  judge   otherwise -> re-judged (first-pass pair) or judged for the first time (new pair)
Writes raw/pairs2.jsonl and, for `judge`, mixed-concept batches <outdir>/judge2_bNN.jsonl.
Usage: python3 -I scripts/make_pairs2.py <outdir> <batch_size>
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
outdir, size = Path(sys.argv[1]), int(sys.argv[2])
claims = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / "claims.jsonl")}
concepts = {json.loads(l)["concept_id"]: json.loads(l) for l in open(HERE / "concepts2.jsonl")}
ms2 = {}
for l in open(HERE / "milestones2.jsonl"):
    m = json.loads(l)
    ms2.setdefault(m["concept_id"], {})[m["kind"]] = m
ms1 = {}
for l in open(HERE / "milestones.jsonl"):
    m = json.loads(l)
    ms1.setdefault(m["concept_id"], {})[m["kind"]] = m
old = {(p["id"], p["concept_id"]): p for p in map(json.loads, open(HERE / "raw/pairs.jsonl"))}
j1 = {r["pair"]: r for r in map(json.loads, open(HERE / "judgments.jsonl"))}


def pick(d):
    return d.get("first_practical_use") or d.get("first_demonstration")


keys = []
for l in open(HERE / "matches.jsonl"):
    r = json.loads(l)
    for c in r["concepts"]:
        if pick(ms2.get(c, {})) or (r["id"], c) in old:
            keys.append((r["id"], c))
pairs, n = [], 0
for cid_claim, c in keys:
    o = old.get((cid_claim, c))
    m = pick(ms2.get(c, {}))
    year = claims[cid_claim]["year"]
    p = {"id": cid_claim, "concept_id": c, "year": year, "pair": o["pair"] if o else None,
         "old_kind": o["milestone_kind"] if o else None, "old_date": o["milestone_date"] if o else None}
    if not o:
        n += 1
        p["pair"] = f"n{n:04d}"
    if not m:
        p.update(action="gone", milestone_kind=None, milestone_date=None)
    else:
        p.update(milestone_kind=m["kind"], milestone_date=m["date"])
        if int(m["date"][:4]) <= year:
            p["action"] = "rule"
        elif o and o["milestone_kind"] == m["kind"] and o["milestone_date"] == m["date"] and o["pair"] in j1:
            p["action"] = "copy"
            p["old_what"] = ms1[c][o["milestone_kind"]]["what"]
            p["new_what"] = m["what"]
        else:
            p["action"] = "judge"
    pairs.append(p)
(HERE / "raw/pairs2.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in pairs))
todo = [p for p in pairs if p["action"] == "judge"]
random.Random(2).shuffle(todo)          # mixed concepts in every batch
outdir.mkdir(parents=True, exist_ok=True)
for f in outdir.glob("judge2_b*.jsonl"):
    f.unlink()
for b in range(0, len(todo), size):
    with open(outdir / f"judge2_b{b // size + 1:02d}.jsonl", "w") as f:
        for p in todo[b:b + size]:
            cl, k = claims[p["id"]], concepts[p["concept_id"]]
            m = ms2[p["concept_id"]][p["milestone_kind"]]
            f.write(json.dumps({"pair": p["pair"], "pub_year": cl["year"], "quote": cl["quote"],
                                "claim_description": cl["description"], "concept_name": k["name"],
                                "concept_description": k["definition"], "milestone_kind": p["milestone_kind"],
                                "milestone_date": p["milestone_date"], "milestone_summary": m["what"]},
                               ensure_ascii=False) + "\n")
from collections import Counter
print(len(pairs), "pairs", dict(Counter(p["action"] for p in pairs)),
      "new pairs", sum(1 for p in pairs if p["pair"].startswith("n")),
      "->", (len(todo) + size - 1) // size, "batches")
