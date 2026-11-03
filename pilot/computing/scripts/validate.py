"""Check that every pilot output is valid JSON lines with the expected fields.

Usage: python3 -I scripts/validate.py   (run from pilot/computing/)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
KINDS = {"first_demonstration", "first_practical_use", "mass_adoption"}
SCORES = {0, 0.25, 0.5, 0.75, 1}
errors = []


def load(name):
    p = HERE / name
    if not p.exists():
        return None
    rows = []
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if not line.strip():
            errors.append(f"{name}:{i}: blank line")
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            errors.append(f"{name}:{i}: {e}")
    return rows


def need(name, i, row, keys):
    for k in keys:
        if k not in row:
            errors.append(f"{name}:{i}: missing {k}")


claims = {c["id"]: c for c in load("claims.jsonl")}
concepts = load("concepts.jsonl")
cids = set()
if concepts is not None:
    for i, c in enumerate(concepts, 1):
        need("concepts.jsonl", i, c, ["concept_id", "name", "definition", "wikidata", "aliases"])
        cid = c.get("concept_id", "")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", cid):
            errors.append(f"concepts.jsonl:{i}: bad id {cid!r}")
        if cid in cids:
            errors.append(f"concepts.jsonl:{i}: duplicate {cid}")
        cids.add(cid)
        q = c.get("wikidata")
        if q is not None and not re.fullmatch(r"Q\d+", str(q)):
            errors.append(f"concepts.jsonl:{i}: bad QID {q!r}")

ms = load("milestones.jsonl")
mkeys = set()
if ms is not None:
    for i, m in enumerate(ms, 1):
        need("milestones.jsonl", i, m, ["concept_id", "kind", "date", "what", "sources"])
        if m.get("concept_id") not in cids:
            errors.append(f"milestones.jsonl:{i}: unknown concept {m.get('concept_id')}")
        if m.get("kind") not in KINDS:
            errors.append(f"milestones.jsonl:{i}: bad kind {m.get('kind')}")
        if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", str(m.get("date", ""))):
            errors.append(f"milestones.jsonl:{i}: bad date {m.get('date')}")
        key = (m.get("concept_id"), m.get("kind"))
        if key in mkeys:
            errors.append(f"milestones.jsonl:{i}: duplicate {key}")
        mkeys.add(key)
        if not m.get("sources"):
            errors.append(f"milestones.jsonl:{i}: no sources")
        for s in m.get("sources", []):
            for k in ["url", "publisher", "date", "title", "quote", "kind"]:
                if k not in s:
                    errors.append(f"milestones.jsonl:{i}: source missing {k}")
            if len(str(s.get("quote", "")).split()) > 25:
                errors.append(f"milestones.jsonl:{i}: source quote over 25 words")

matches = load("matches.jsonl")
if matches is not None:
    seen = set()
    for i, m in enumerate(matches, 1):
        need("matches.jsonl", i, m, ["id", "concepts", "reason"])
        if m.get("id") not in claims:
            errors.append(f"matches.jsonl:{i}: unknown claim {m.get('id')}")
        if m.get("id") in seen:
            errors.append(f"matches.jsonl:{i}: duplicate claim {m.get('id')}")
        seen.add(m.get("id"))
        cs = m.get("concepts", [])
        if len(cs) > 2:
            errors.append(f"matches.jsonl:{i}: more than two concepts")
        for c in cs:
            if c not in cids:
                errors.append(f"matches.jsonl:{i}: unknown concept {c}")
    missing = set(claims) - seen
    if missing:
        errors.append(f"matches.jsonl: {len(missing)} claims have no row")

js = load("judgments.jsonl")
if js is not None:
    for i, j in enumerate(js, 1):
        need("judgments.jsonl", i, j, ["id", "concept_id", "milestone_kind", "milestone_date",
                                       "lead_years", "score", "rationale"])
        if j.get("score") not in SCORES:
            errors.append(f"judgments.jsonl:{i}: bad score {j.get('score')}")
        if j.get("id") not in claims:
            errors.append(f"judgments.jsonl:{i}: unknown claim")

if errors:
    print("\n".join(errors[:50]))
    print(f"{len(errors)} errors")
    sys.exit(1)
print("ok:", {n: (len(r) if r is not None else None) for n, r in
              [("concepts", concepts), ("milestones", ms), ("matches", matches), ("judgments", js)]})
