"""RUN3 step 7: combine the second (and third) blind judges into judgments3.jsonl.

  python3 -I scripts/apply_judge3b.py third <round>   -> raw/judge3b_in/judge3c_round<N>.jsonl:
        the round's top-100 / 1.0 pairs where the first two judges are two or more steps apart
  python3 -I scripts/apply_judge3b.py apply           -> judgments3.jsonl, from the step-6
        version (saved once as raw/judgments3_step6.jsonl), applying every round present
Combination, for the top-100 and 1.0 pairs only (random-50 pairs are for agreement and keep
their score): same score -> keep ("agreed"); one step (0.25) apart -> the lower ("lower");
two or more steps -> the median of three judges ("median"); if a needed third judge is
missing, the lower of two ("lower_no_third"). Each such row gets judges [first, second,
third?], the final score, action2, and the other judges' rationales (rationale2, rationale3).
Inputs: raw/judge3b_round<N>.jsonl (second judge), raw/judge3c_round<N>.jsonl (third judge),
raw/judge3b_key_round<N>.jsonl (groups).
"""
import json
import shutil
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
L = lambda f: [json.loads(l) for l in open(HERE / f) if l.strip()] if (HERE / f).exists() else []  # noqa: E731
SC = (0, 0.25, 0.5, 0.75, 1)
base = HERE / "raw/judgments3_step6.jsonl"
if not base.exists():
    shutil.copy(HERE / "judgments3.jsonl", base)
J = L("raw/judgments3_step6.jsonl")
byp = {j["pair"]: j for j in J}


def scores(f):
    return {r["pair"]: r for r in L(f) if r.get("score") in SC}


rounds = sorted(int(p.stem.split("round")[1]) for p in HERE.glob("raw/judge3b_key_round*.jsonl"))
if sys.argv[1] == "third":
    rnd = int(sys.argv[2])
    key = {r["pair"]: r["group"] for r in L(f"raw/judge3b_key_round{rnd}.jsonl")}
    s2 = scores(f"raw/judge3b_round{rnd}.jsonl")
    src = {json.loads(l)["pair"]: l for l in open(HERE / f"raw/judge3b_in/judge3b_round{rnd}.jsonl")}
    todo = [p for p, g in key.items() if g != "random50" and p in s2 and abs(byp[p]["score"] - s2[p]["score"]) >= 0.5]
    (HERE / f"raw/judge3b_in/judge3c_round{rnd}.jsonl").write_text("".join(src[p] for p in todo))
    print(len(todo), "pairs for the third judge; missing second scores:",
          [p for p in key if p not in s2])
    sys.exit(0)

for rnd in rounds:
    key = {r["pair"]: r["group"] for r in L(f"raw/judge3b_key_round{rnd}.jsonl")}
    s2, s3 = scores(f"raw/judge3b_round{rnd}.jsonl"), scores(f"raw/judge3c_round{rnd}.jsonl")
    for p, g in key.items():
        if g == "random50" or p not in s2:
            continue
        j = byp[p]
        a, b = j["score"], s2[p]["score"]
        js = [a, b]
        if a == b:
            final, act = a, "agreed"
        elif abs(a - b) == 0.25:
            final, act = min(a, b), "lower"
        elif p in s3:
            js.append(s3[p]["score"])
            final, act = statistics.median(js), "median"
            j["rationale3"] = s3[p].get("rationale", "")
        else:
            final, act = min(a, b), "lower_no_third"
        j.update(judges=js, score=final, action2=act, rationale2=s2[p].get("rationale", ""),
                 judge_round=rnd, judge_group=g)
(HERE / "judgments3.jsonl").write_text("".join(json.dumps(j, ensure_ascii=False) + "\n" for j in J))
from collections import Counter
print("rounds", rounds, dict(Counter(j.get("action2") for j in J if "action2" in j)))
