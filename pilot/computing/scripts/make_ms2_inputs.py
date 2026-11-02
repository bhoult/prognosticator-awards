"""Step 3 of RUN2: build the research agents' input batches.

Each line: the concept (from concepts2.jsonl), its Wikidata item and dated statements
(raw/wikidata_dates.jsonl), the first-pass milestones and why they were doubted
(milestones.jsonl, raw/doubts1.jsonl). Contiguous chunks so related concepts share a batch.
Usage: python3 -I scripts/make_ms2_inputs.py <outdir> <n_batches>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
outdir, nb = Path(sys.argv[1]), int(sys.argv[2])
concepts = [json.loads(l) for l in open(HERE / "concepts2.jsonl")]
wd = {}
for l in open(HERE / "raw/wikidata_dates.jsonl"):
    r = json.loads(l)
    wd.setdefault(r["concept_id"], {"qid": r["qid"], "label": r["label"], "url": r["url"], "dates": []})
    wd[r["concept_id"]]["dates"].append(f'{r["property_label"]} ({r["property"]}): {r["date"]}')
fp = {}
for l in open(HERE / "milestones.jsonl"):
    m = json.loads(l)
    fp.setdefault(m["concept_id"], []).append({"kind": m["kind"], "date": m["date"], "what": m["what"]})
doubts = {json.loads(l)["concept_id"]: json.loads(l) for l in open(HERE / "raw/doubts1.jsonl")}
rows = []
for c in concepts:
    k = c["concept_id"]
    w = wd.get(k) or ({"qid": c["wikidata"], "label": "", "url": f"https://www.wikidata.org/wiki/{c['wikidata']}",
                       "dates": []} if c["wikidata"] else None)
    rows.append({"concept_id": k, "name": c["name"], "definition": c["definition"],
                 "aliases": c["aliases"], "realizable": c["realizable"], "wikidata": w,
                 "first_pass": fp.get(k, []), "first_pass_note": doubts[k]["first_pass_note"],
                 "doubt": doubts[k]["doubt"]})
outdir.mkdir(parents=True, exist_ok=True)
size = -(-len(rows) // nb)
for b in range(nb):
    chunk = rows[b * size:(b + 1) * size]
    (outdir / f"ms2_in_b{b + 1:02d}.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in chunk))
    print(b + 1, len(chunk))
