"""Merge raw/judge_NN.jsonl with the rule-zero pairs into judgments.jsonl.

lead_years = milestone year - first publication year (the claim's year is a whole year).
Pairs whose milestone is not after publication get score 0 with judged_by "rule".
raw/judge_rejudge.jsonl, when present, overrides earlier scores for its pairs.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
pairs = [json.loads(l) for l in open(HERE / "raw" / "pairs.jsonl")]
scores = {}
files = sorted((HERE / "raw").glob("judge_[0-9][0-9].jsonl"))
rejudge = HERE / "raw" / "judge_rejudge.jsonl"   # batch 05 again + robot-mower pairs; overrides
if rejudge.exists():
    files.append(rejudge)
for f in files:
    for l in open(f):
        r = json.loads(l)
        if "pair" in r and "score" in r:
            scores[r["pair"]] = r
out, missing = [], []
for p in pairs:
    lead = int(p["milestone_date"][:4]) - p["year"]
    row = {"id": p["id"], "concept_id": p["concept_id"], "milestone_kind": p["milestone_kind"],
           "milestone_date": p["milestone_date"], "lead_years": lead}
    if p["rule_zero"]:
        row.update(score=0, rationale="Milestone not after first publication: not a prediction (scored by rule).",
                   judged_by="rule")
    elif p["pair"] in scores:
        s = scores[p["pair"]]
        row.update(score=s["score"], rationale=s.get("rationale") or "(judge gave no rationale)", judged_by="sonnet")
    else:
        missing.append(p["pair"])
        continue
    row["pair"] = p["pair"]
    out.append(row)
(HERE / "judgments.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
print(len(out), "judgments;", len(missing), "missing", missing[:10])
