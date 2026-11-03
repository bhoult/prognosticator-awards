"""RUN3 step 7: pairs for the second (blind) judge.

round 1: the best pair of each top-100 book-concept entry (rank3.ranking over judgments3.jsonl
         as step 6 left it), every pair scored 1.0, and 50 other judged pairs (judged_by sonnet)
         with score > 0 drawn with a fixed seed (agreement only). Shuffled together.
round 2: (after apply_judge3b.py round 1) entries that entered the recomputed top 100 without a
         second judge.
Writes raw/judge3b_in/judge3b_round<N>.jsonl (the first judge's fields only: no score, no
rationale) and raw/judge3b_key_round<N>.jsonl (pair -> group), and prints counts.
Usage: python3 -I scripts/make_judge3b.py <round>
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rank3  # noqa: E402

HERE = rank3.HERE
rnd = int(sys.argv[1])
L = lambda f: [json.loads(l) for l in open(HERE / f) if l.strip()]  # noqa: E731
J = L("judgments3.jsonl")
claims = rank3.claims()
concepts = {c["concept_id"]: c for c in L("concepts2.jsonl")}
ms3 = {(m["concept_id"], m["kind"]): m for m in L("milestones3.jsonl")}
top = rank3.ranking(J)[:100]
groups = {}
if rnd == 1:
    for _, j in top:
        groups[j["pair"]] = "top100"
    for j in J:
        if j["score"] == 1 and j["pair"] not in groups:
            groups[j["pair"]] = "score1"
    pool = sorted(j["pair"] for j in J if j["judged_by"] == "sonnet" and j["score"] > 0 and j["pair"] not in groups)
    for p in random.Random(31).sample(pool, 50):
        groups[p] = "random50"
else:
    for _, j in top:
        if "judges" not in j:
            groups[j["pair"]] = "top100_new"
order = list(groups)
random.Random(37 + rnd).shuffle(order)
byp = {j["pair"]: j for j in J}
d = HERE / "raw/judge3b_in"
d.mkdir(parents=True, exist_ok=True)
with open(d / f"judge3b_round{rnd}.jsonl", "w") as f:
    for p in order:
        j = byp[p]
        cl, k, m = claims[j["id"]], concepts[j["concept_id"]], ms3[(j["concept_id"], j["milestone_kind"])]
        f.write(json.dumps({"pair": p, "pub_year": cl["year"], "quote": cl["quote"],
                            "claim_description": cl["description"], "concept_name": k["name"],
                            "concept_description": k["definition"], "milestone_kind": j["milestone_kind"],
                            "milestone_date": j["milestone_date"], "milestone_summary": m["what"]},
                           ensure_ascii=False) + "\n")
(HERE / f"raw/judge3b_key_round{rnd}.jsonl").write_text(
    "".join(json.dumps({"pair": p, "group": groups[p]}) + "\n" for p in order))
from collections import Counter
print(len(order), "pairs", dict(Counter(groups.values())))
