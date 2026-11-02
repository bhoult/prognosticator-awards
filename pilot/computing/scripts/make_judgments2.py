"""Step 5 of RUN2: merge into judgments2.jsonl.

One row per pair in raw/pairs2.jsonl, with the fields of judgments.jsonl plus `action`:
  copied        first-pass judgment copied (same milestone kind and date)
  rule          milestone in or before the claim's year: score 0 by rule
  no_milestone  concept has no run-2 milestone: score 0, milestone fields null
  rejudged      first-pass pair re-judged against the new milestone (raw/judge2_bNN.jsonl)
  new           pair judged for the first time (concept gained a milestone)
Also checks each judge batch for template rationales (distinct share < 80% is flagged).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
pairs = [json.loads(l) for l in open(HERE / "raw/pairs2.jsonl")]
j1 = {r["pair"]: r for r in map(json.loads, open(HERE / "judgments.jsonl"))}
scores = {}
for f in sorted(HERE.glob("raw/judge2_b[0-9][0-9].jsonl")):
    rows = [json.loads(l) for l in open(f) if l.strip()]
    rats = [r.get("rationale", "") for r in rows]
    share = len(set(rats)) / max(1, len(rats))
    print(f.name, len(rows), "rows, distinct rationales %.0f%%" % (100 * share), "" if share >= 0.8 else "FLAG")
    for r in rows:
        if r.get("score") in (0, 0.25, 0.5, 0.75, 1):
            scores[r["pair"]] = r
out, missing = [], []
for p in pairs:
    row = {"id": p["id"], "concept_id": p["concept_id"], "milestone_kind": p["milestone_kind"],
           "milestone_date": p["milestone_date"],
           "lead_years": int(p["milestone_date"][:4]) - p["year"] if p["milestone_date"] else None}
    a = p["action"]
    if a == "copy":
        o = j1[p["pair"]]
        row.update(score=o["score"], rationale=o["rationale"], judged_by=o["judged_by"], action="copied")
    elif a == "rule":
        row.update(score=0, rationale="Milestone not after first publication: not a prediction (scored by rule).",
                   judged_by="rule", action="rule")
    elif a == "gone":
        row.update(score=0, rationale="Concept has no milestone in the second pass (scored by rule).",
                   judged_by="rule", action="no_milestone")
    elif p["pair"] in scores:
        s = scores[p["pair"]]
        row.update(score=s["score"], rationale=s.get("rationale") or "(judge gave no rationale)",
                   judged_by="sonnet", action="new" if p["pair"].startswith("n") else "rejudged")
    else:
        missing.append(p["pair"])
        continue
    if p["old_date"]:
        row["first_pass_milestone_date"] = p["old_date"]
        if p["pair"] in j1:
            row["first_pass_score"] = j1[p["pair"]]["score"]
    row["pair"] = p["pair"]
    out.append(row)
(HERE / "judgments2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
from collections import Counter
print(len(out), "judgments", dict(Counter(r["action"] for r in out)), "missing", len(missing), missing[:10])
