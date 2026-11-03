"""RUN3 step 6: merge into judgments3.jsonl (before the second judge of step 7).

One row per pair in raw/pairs3.jsonl, with the fields of judgments2.jsonl plus:
  action      copied (second-pass judgment copied: same kind and date) | rule | no_milestone |
              rejudged (second-pass pair, new milestone) | new (pair judged for the first time)
  first_pass_score / first_pass_milestone_date   kept from judgments2.jsonl where present
  second_pass_score / second_pass_milestone_date  from judgments2.jsonl (null for new pairs)
Judge output: raw/judge3_bNN.jsonl. Flags batches with < 80% distinct rationales.
Usage: python3 -I scripts/make_judgments3.py
"""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
L = lambda f: [json.loads(l) for l in open(HERE / f) if l.strip()]  # noqa: E731
pairs = L("raw/pairs3.jsonl")
j2 = {r["pair"]: r for r in L("judgments2.jsonl")}
scores = {}
for f in sorted(HERE.glob("raw/judge3_b[0-9][0-9].jsonl")):
    rows = L(f.relative_to(HERE))
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
    a, o = p["action"], j2.get(p["pair"])
    if a == "copy":
        row.update(score=o["score"], rationale=o["rationale"], judged_by=o["judged_by"], action="copied")
    elif a == "rule":
        row.update(score=0, rationale="Milestone not after first publication: not a prediction (scored by rule).",
                   judged_by="rule", action="rule")
    elif a == "gone":
        row.update(score=0, rationale="Concept has no milestone in the third pass (scored by rule).",
                   judged_by="rule", action="no_milestone")
    elif p["pair"] in scores:
        s = scores[p["pair"]]
        row.update(score=s["score"], rationale=s.get("rationale") or "(judge gave no rationale)",
                   judged_by="sonnet", action="rejudged" if o else "new")
    else:
        missing.append(p["pair"])
        continue
    if o:
        for k in ("first_pass_milestone_date", "first_pass_score"):
            if k in o:
                row[k] = o[k]
    row["second_pass_score"] = o["score"] if o else None
    row["second_pass_milestone_date"] = o["milestone_date"] if o else None
    row["pair"] = p["pair"]
    out.append(row)
(HERE / "judgments3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
print(len(out), "judgments", dict(Counter(r["action"] for r in out)), "missing", len(missing), missing[:10])
