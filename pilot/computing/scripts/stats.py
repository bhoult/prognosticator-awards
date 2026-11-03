"""Print the numbers and tables used in report.md.

Usage: python3 -I scripts/stats.py [top|sample|counts]
"""
import collections
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
L = lambda f: [json.loads(x) for x in open(HERE / f)]
claims = {c["id"]: c for c in L("claims.jsonl")}
concepts = {c["concept_id"]: c for c in L("concepts.jsonl")}
ms = {(m["concept_id"], m["kind"]): m for m in L("milestones.jsonl")}
matches = L("matches.jsonl")
js = L("judgments.jsonl")
what = sys.argv[1] if len(sys.argv) > 1 else "counts"


def pts(j):
    return j["score"] * math.log2(1 + min(j["lead_years"], 500)) if j["lead_years"] > 0 else 0


if what == "counts":
    print("claims", len(claims), "concepts", len(concepts),
          "realizable(est)", sum(c["realizable"] for c in concepts.values()))
    mc = {m["concept_id"] for m in ms.values()}
    print("milestones", len(ms), "concepts with milestones", len(mc),
          collections.Counter(k for _, k in ms))
    src = collections.Counter(s["kind"] for m in ms.values() for s in m["sources"])
    print("source kinds", src, "with quote", sum(1 for m in ms.values() for s in m["sources"] if s["quote"]))
    un = sum(1 for m in matches if not m["concepts"])
    two = sum(1 for m in matches if len(m["concepts"]) == 2)
    print("matched", len(matches) - un, "unmatched", un, "two concepts", two,
          "concept links", sum(len(m["concepts"]) for m in matches))
    nom = sum(1 for m in matches for c in m["concepts"] if c not in mc)
    print("links to concepts without milestone", nom)
    used = collections.Counter(c for m in matches for c in m["concepts"])
    print("concepts never matched", [c for c in concepts if c not in used])
    print("judgments", len(js), collections.Counter(j["judged_by"] for j in js))
    print("score dist (all)", sorted(collections.Counter(j["score"] for j in js).items()))
    print("score dist (judge)", sorted(collections.Counter(j["score"] for j in js if j["judged_by"] == "sonnet").items()))
    best = {}
    for j in js:
        best[j["id"]] = max(best.get(j["id"], 0), j["score"])
    print("claims with best score >=0.5", sum(1 for v in best.values() if v >= 0.5),
          ">=0.75", sum(1 for v in best.values() if v >= 0.75))
    by_spec = collections.defaultdict(list)
    for cid, v in best.items():
        by_spec[claims[cid]["specificity"]].append(v)
    print("mean best score by specificity", {k: round(sum(v) / len(v), 3) for k, v in sorted(by_spec.items())},
          {k: len(v) for k, v in sorted(by_spec.items())})
    by_c = collections.defaultdict(list)
    for j in js:
        if j["judged_by"] == "sonnet":
            by_c[j["concept_id"]].append(j["score"])
    top = sorted(by_c.items(), key=lambda kv: -sum(kv[1]))[:15]
    print("concepts by total judged score", [(k, len(v), round(sum(v) / len(v), 2)) for k, v in top])
    print("total points", round(sum(pts(j) for j in js), 1))
elif what == "top":
    seen, rows = set(), []
    for j in sorted(js, key=lambda j: -pts(j)):
        if j["id"] in seen or pts(j) == 0:
            continue
        seen.add(j["id"])
        rows.append(j)
        if len(rows) == 20:
            break
    for i, j in enumerate(rows, 1):
        c, m = claims[j["id"]], ms[(j["concept_id"], j["milestone_kind"])]
        print(json.dumps({"rank": i, "year": c["year"], "quote": c["quote"], "concept": concepts[j["concept_id"]]["name"],
                          "milestone": f'{m["date"]} {m["what"]}', "kind": j["milestone_kind"], "lead": j["lead_years"],
                          "score": j["score"], "points": round(pts(j), 2), "id": j["id"], "rationale": j["rationale"]},
                         ensure_ascii=False))
elif what == "sample":
    pool = [j for j in js if j["judged_by"] == "sonnet"]
    random.seed(20261102)
    for j in random.sample(pool, 30):
        c, m = claims[j["id"]], ms[(j["concept_id"], j["milestone_kind"])]
        print(json.dumps({"pair": j["pair"], "year": c["year"], "quote": c["quote"], "desc": c["description"],
                          "concept": j["concept_id"], "milestone": f'{m["date"]} {m["what"]}',
                          "score": j["score"], "rationale": j["rationale"]}, ensure_ascii=False))
