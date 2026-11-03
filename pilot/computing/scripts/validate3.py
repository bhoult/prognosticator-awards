"""Check the RUN3 outputs: every .jsonl parses; the run-3 files have the expected fields.
Checks each file only if it exists yet (the run is pushed step by step).
Usage: python3 -I scripts/validate3.py   (from pilot/computing/)"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
KINDS = {"first_demonstration", "first_practical_use", "mass_adoption"}
SCORES = (0, 0.25, 0.5, 0.75, 1)
err = []


def load(p):
    rows = []
    for i, l in enumerate(open(HERE / p), 1):
        try:
            rows.append(json.loads(l))
        except json.JSONDecodeError as e:
            err.append(f"{p}:{i}: {e}")
    return rows


for p in sorted(HERE.glob("**/*.jsonl")):
    load(p.relative_to(HERE))
# first- and second-pass outputs must be unchanged since the run-3 sheet commit
frozen = ["concepts.jsonl", "milestones.jsonl", "matches.jsonl", "judgments.jsonl", "report.md",
          "concepts2.jsonl", "milestones2.jsonl", "judgments2.jsonl", "report2.md", "claims.jsonl"]
d = subprocess.run(["git", "diff", "--name-only", "ef37267", "--", *frozen], cwd=HERE, capture_output=True, text=True)
if d.stdout.strip():
    err.append("first/second-pass outputs changed: " + d.stdout.strip().replace("\n", ", "))
cids = {c["concept_id"] for c in load("concepts2.jsonl")}
ex = lambda p: (HERE / p).exists()  # noqa: E731
if ex("raw/targets3.jsonl"):
    t = load("raw/targets3.jsonl")
    if len(t) != 33 or len({r["concept_id"] for r in t}) != 33 or not {r["concept_id"] for r in t} <= cids:
        err.append("targets3: expected 33 distinct known concepts")


def check_ms(p, rows):
    seen = set()
    for i, m in enumerate(rows, 1):
        for k in ["concept_id", "kind", "date", "what", "sources", "confidence"]:
            if k not in m:
                err.append(f"{p}:{i}: missing {k}")
        if m.get("concept_id") not in cids or m.get("kind") not in KINDS:
            err.append(f"{p}:{i}: bad concept/kind")
        key = (m.get("concept_id"), m.get("kind"))
        if key in seen:
            err.append(f"{p}:{i}: duplicate")
        seen.add(key)
        if m.get("confidence") not in ("high", "medium", "low"):
            err.append(f"{p}:{i}: bad confidence")
        if m.get("checked") not in (None, "confirmed", "replaced"):
            err.append(f"{p}:{i}: bad checked")
        if not m.get("sources"):
            err.append(f"{p}:{i}: no sources")
        for s in m.get("sources", []):
            if s.get("kind") not in ("contemporary", "reference", "wikidata") or not s.get("quote") \
                    or len(s["quote"].split()) > 25:
                err.append(f"{p}:{i}: bad source {s.get('url')}")


if ex("milestones3.jsonl"):
    m3 = load("milestones3.jsonl")
    check_ms("milestones3.jsonl", m3)
    for i, m in enumerate(m3, 1):
        if "previous_date" not in m:
            err.append(f"milestones3:{i}: missing previous_date")
        if m.get("target3") and not m.get("fit"):
            err.append(f"milestones3:{i}: target milestone without fit")
if ex("judgments3.jsonl"):
    claims = {c["id"] for c in load("claims.jsonl")}
    pairs = set()
    for i, j in enumerate(load("judgments3.jsonl"), 1):
        if j["id"] not in claims or j["concept_id"] not in cids:
            err.append(f"judgments3:{i}: unknown claim/concept")
        if j["score"] not in SCORES:
            err.append(f"judgments3:{i}: bad score")
        if j["pair"] in pairs:
            err.append(f"judgments3:{i}: duplicate pair")
        pairs.add(j["pair"])
        for k in ("action", "second_pass_score", "second_pass_milestone_date"):
            if k not in j:
                err.append(f"judgments3:{i}: missing {k}")
        if "judges" in j:
            if any(s not in SCORES for s in j["judges"]) or j.get("action2") not in ("agreed", "lower", "median", "lower_no_third"):
                err.append(f"judgments3:{i}: bad judges/action2")
    second = {j["pair"] for j in load("judgments2.jsonl")}
    if not second <= pairs:
        err.append(f"judgments3: {len(second - pairs)} second-pass pairs missing")
print("\n".join(err) if err else "all RUN3 outputs valid")
sys.exit(1 if err else 0)
