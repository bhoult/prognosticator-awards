"""Merge raw/matches_NN.jsonl (+ raw/matches_fixes.jsonl) into matches.jsonl, in claim order.

Drops unknown concept ids (reported), keeps at most two concepts, and fails if any claim
is missing.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
claims = [json.loads(l)["id"] for l in open(HERE / "claims.jsonl")]
cids = {json.loads(l)["concept_id"] for l in open(HERE / "concepts.jsonl")}
rows, bad = {}, []
drop = set()
fixes = [json.loads(l) for l in open(HERE / "raw" / "matches_fixes.jsonl")]
for f in fixes:
    drop.add(f.get("replaces"))
for f in sorted((HERE / "raw").glob("matches_[0-9][0-9].jsonl")):
    for line in open(f):
        r = json.loads(line)
        if r["id"] in drop and not any(x["id"] == r["id"] for x in fixes):
            continue
        rows[r["id"]] = r
for r in fixes:
    rows[r["id"]] = r
out = []
for cid in claims:
    if cid not in rows:
        continue
    r = rows[cid]
    cs = [c for c in r["concepts"] if c in cids]
    bad += [(cid, c) for c in r["concepts"] if c not in cids]
    out.append({"id": cid, "concepts": cs[:2], "reason": r["reason"]})
missing = [c for c in claims if c not in rows]
extra = [c for c in rows if c not in set(claims)]
print(len(out), "rows; missing", len(missing), "extra", extra, "unknown concepts", bad)
(HERE / "matches.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
sys.exit(1 if missing else 0)
