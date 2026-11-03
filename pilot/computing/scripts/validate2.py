"""Check the RUN2 outputs: valid JSON lines with the expected fields and values.
Usage: python3 -I scripts/validate2.py   (from pilot/computing/)"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
KINDS = {"first_demonstration", "first_practical_use", "mass_adoption"}
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
cons = load("concepts2.jsonl")
old = load("concepts.jsonl")
cids = {c["concept_id"] for c in cons}
for a, b in zip(old, cons):
    if {k: v for k, v in a.items() if k != "wikidata"} != {k: v for k, v in b.items() if k != "wikidata"}:
        err.append(f"concepts2: {b['concept_id']} differs from concepts.jsonl beyond wikidata")
    if b["wikidata"] is not None and not re.fullmatch(r"Q\d+", b["wikidata"]):
        err.append(f"concepts2: bad QID {b['wikidata']}")
seen = set()
for i, m in enumerate(load("milestones2.jsonl"), 1):
    for k in ["concept_id", "kind", "date", "what", "sources", "confidence"]:
        if k not in m:
            err.append(f"milestones2:{i}: missing {k}")
    if m["concept_id"] not in cids or m["kind"] not in KINDS:
        err.append(f"milestones2:{i}: bad concept/kind")
    if (m["concept_id"], m["kind"]) in seen:
        err.append(f"milestones2:{i}: duplicate")
    seen.add((m["concept_id"], m["kind"]))
    if m["confidence"] not in ("high", "medium", "low"):
        err.append(f"milestones2:{i}: bad confidence")
    if m.get("checked") not in (None, "confirmed", "replaced"):
        err.append(f"milestones2:{i}: bad checked")
    if not m["sources"]:
        err.append(f"milestones2:{i}: no sources")
    for s in m["sources"]:
        if s["kind"] not in ("contemporary", "reference", "wikidata") or not s["quote"] or len(s["quote"].split()) > 25:
            err.append(f"milestones2:{i}: bad source {s.get('url')}")
claims = {c["id"] for c in load("claims.jsonl")}
pairs = set()
for i, j in enumerate(load("judgments2.jsonl"), 1):
    if j["id"] not in claims or j["concept_id"] not in cids:
        err.append(f"judgments2:{i}: unknown claim/concept")
    if j["score"] not in (0, 0.25, 0.5, 0.75, 1):
        err.append(f"judgments2:{i}: bad score")
    if j["pair"] in pairs:
        err.append(f"judgments2:{i}: duplicate pair")
    pairs.add(j["pair"])
first = {j["pair"] for j in load("judgments.jsonl")}
if not first <= pairs:
    err.append(f"judgments2: {len(first - pairs)} first-pass pairs missing")
print("\n".join(err) if err else "all RUN2 outputs valid")
sys.exit(1 if err else 0)
