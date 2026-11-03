"""Merge raw/milestones_b*.jsonl and raw/milestones_manual.jsonl into milestones.jsonl.

Keeps one milestone per (concept, kind): the earliest date when an agent gave two.
Also writes raw/qids.jsonl (all null in this pilot; no QID was seen in search results)
and raw/milestone_notes.jsonl (the agents' per-concept notes).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
concepts = [json.loads(l) for l in open(HERE / "concepts.jsonl")]
order = {c["concept_id"]: i for i, c in enumerate(concepts)}
KORDER = {"first_demonstration": 0, "first_practical_use": 1, "mass_adoption": 2}
best, notes, dropped = {}, [], []
files = sorted((HERE / "raw").glob("milestones_b*.jsonl")) + [HERE / "raw" / "milestones_manual.jsonl"]
for f in files:
    for line in open(f):
        r = json.loads(line)
        if "kind" in r and "date" in r:
            if r["concept_id"] not in order:
                dropped.append(r)
                continue
            r = {k: r[k] for k in ["concept_id", "kind", "date", "what", "sources"]}
            k = (r["concept_id"], r["kind"])
            if k in best and best[k]["date"] <= r["date"]:
                dropped.append(r)
                continue
            if k in best:
                dropped.append(best[k])
            best[k] = r
        elif "note" in r:
            notes.append({"concept_id": r["concept_id"], "note": r["note"], "wikidata": r.get("wikidata")})
rows = sorted(best.values(), key=lambda r: (order[r["concept_id"]], KORDER[r["kind"]]))
(HERE / "milestones.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
(HERE / "raw" / "milestone_notes.jsonl").write_text("".join(json.dumps(n, ensure_ascii=False) + "\n" for n in notes))
(HERE / "raw" / "qids.jsonl").write_text("".join(
    json.dumps({"concept_id": n["concept_id"], "wikidata": n["wikidata"]}) + "\n" for n in notes if n["wikidata"]))
with_m = {r["concept_id"] for r in rows}
print(len(rows), "milestones for", len(with_m), "concepts; dropped", len(dropped), [ (d["concept_id"], d["kind"], d["date"]) for d in dropped])
print("no milestone:", [c["concept_id"] for c in concepts if c["concept_id"] not in with_m])
