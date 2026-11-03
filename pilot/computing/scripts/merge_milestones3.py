"""RUN3 step 4: milestones3.jsonl = milestones2.jsonl with the 33 target concepts' rows
replaced by the step-3 research (raw/ms3_bNN.jsonl); every other row copied unchanged.

Every source of the new research is verified again in code, independently of the agents:
  - the page/record is fetched anew (scripts/page_text3.py) and the quote must be <= 25
    words and occur in its text (case, whitespace, curly quotes, OCR soft hyphens normalised);
  - for records that carry a date (archive.org items, NTRS, Crossref, Semantic Scholar,
    Google Books) the source's `date` is set from the record;
  - `contemporary` needs a source date within two years of the event's year; otherwise
    the source is kept as `reference` (logged);
  - wikidata sources: the date must be one of the item's statements (raw/wikidata_dates.jsonl).
A milestone with no verified source is dropped. `high` confidence needs a verified
contemporary and a verified reference source; otherwise it is lowered to `medium` (logged).
Log: raw/quote_check3.jsonl (url, verdict; never page text). Notes: raw/ms3_concept_notes.jsonl.
Each row gets `previous_date` (the second-pass date for that concept and kind, or null);
the new rows also get `target3: true`.
Usage: python3 -I scripts/merge_milestones3.py
"""
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_text3  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
KINDS = ["first_demonstration", "first_practical_use", "mass_adoption"]
L = lambda f: [json.loads(l) for l in open(HERE / f) if l.strip()]  # noqa: E731
cids = [c["concept_id"] for c in L("concepts2.jsonl")]
targets = {r["concept_id"] for r in L("raw/targets3.jsonl")}
m2 = L("milestones2.jsonl")
prev = {(m["concept_id"], m["kind"]): m["date"] for m in m2}
wd = {}
for r in L("raw/wikidata_dates.jsonl"):
    wd.setdefault(r["qid"], set()).add(r["date"])

ms, notes, tools = [], [], []
for f in sorted(HERE.glob("raw/ms3_b[0-9][0-9].jsonl")):
    for r in L(f.relative_to(HERE)):
        r["_file"] = f.name
        if "_tools" in r:
            tools.append((f.name, r["_tools"]))
        elif "kind" in r and "date" in r:
            ms.append(r)
        elif "concept_note" in r:
            notes.append({"concept_id": r["concept_id"], "concept_note": r["concept_note"], "batch": f.name})


def key(s):
    return (s.get("url", ""), s.get("volume_id") or None)


def fetch(k):
    try:
        t, d = page_text3.fetch(k[0], k[1])
        return k, (t, d, "")
    except Exception as e:  # noqa: BLE001
        return k, (None, "", repr(e)[:200])


keys = sorted({key(s) for m in ms for s in m.get("sources", []) if s.get("kind") != "wikidata"}, key=str)
with ThreadPoolExecutor(4) as ex:
    pages = dict(ex.map(fetch, keys))

log, out = [], []
for m in ms:
    keep = []
    ey = int(str(m["date"])[:4]) if m.get("date") else None
    for s in m.get("sources", []):
        q, url, kind = (s.get("quote") or "").strip(), s.get("url", ""), s.get("kind")
        sdate, verdict, note = str(s.get("date") or ""), "", ""
        if not q:
            verdict = "no quote"
        elif len(q.split()) > 25:
            verdict = "quote over 25 words"
        elif kind == "wikidata":
            qid = re.search(r"Q\d+", url)
            verdict = "ok" if qid and any(d in q for d in wd.get(qid.group(0), set())) else "date not in Wikidata statements"
        elif kind not in ("contemporary", "reference"):
            verdict = f"bad kind {kind!r}"
        else:
            txt, rdate, err = pages.get(key(s), (None, "", "not fetched"))
            if txt is None:
                verdict = "fetch failed: " + err
            elif not page_text3.has_quote(txt, q):
                verdict = "quote not on page"
            else:
                verdict = "ok"
                if rdate:
                    if sdate and re.search(r"\d{4}", sdate) and re.search(r"\d{4}", sdate).group(0) not in rdate:
                        note = f"date {sdate} -> record date {rdate}"
                    sdate = rdate
                if kind == "contemporary":
                    ym = re.search(r"\b(\d{4})\b", sdate)
                    sy = int(ym.group(1)) if ym else None
                    if sy is None or ey is None or not (ey - 2 <= sy <= ey + 2):
                        kind = "reference"
                        note = (note + "; " if note else "") + f"contemporary -> reference (source date {sdate or '?'}, event {ey})"
        log.append({"concept_id": m["concept_id"], "kind": m["kind"], "url": url, "source_kind": kind,
                    "verdict": verdict, **({"note": note} if note else {}), "batch": m["_file"]})
        if verdict == "ok":
            row = {k: s.get(k, "") for k in ["url", "publisher", "date", "title", "quote", "kind"]}
            row.update(date=sdate, kind=kind)
            if s.get("volume_id"):
                row["volume_id"] = s["volume_id"]
            keep.append(row)
    if m.get("concept_id") not in targets or m.get("kind") not in KINDS:
        log.append({"concept_id": m.get("concept_id"), "kind": m.get("kind"), "verdict": "not a target concept or bad kind"})
        continue
    if not keep:
        log.append({"concept_id": m["concept_id"], "kind": m["kind"], "date": m["date"],
                    "verdict": "milestone dropped: no verified source"})
        continue
    conf = m.get("confidence", "low")
    kinds = {s["kind"] for s in keep}
    if conf == "high" and not {"contemporary", "reference"} <= kinds:
        log.append({"concept_id": m["concept_id"], "kind": m["kind"], "verdict": "confidence high -> medium (needs a verified contemporary and reference source)"})
        conf = "medium"
    row = {"concept_id": m["concept_id"], "kind": m["kind"], "date": str(m["date"]), "what": m["what"],
           "fit": m.get("fit", ""), "sources": keep, "confidence": conf}
    for k in ("note", "searched"):
        if m.get(k):
            row[k] = m[k]
    row["previous_date"] = prev.get((m["concept_id"], m["kind"]))
    row["target3"] = True
    out.append(row)

best = {}
for r in out:
    k = (r["concept_id"], r["kind"])
    if k not in best or r["date"] < best[k]["date"]:
        best[k] = r
rows = list(best.values())
for m in m2:
    if m["concept_id"] not in targets:
        rows.append({**m, "previous_date": m["date"]})
order = {c: i for i, c in enumerate(cids)}
rows.sort(key=lambda r: (order[r["concept_id"]], KINDS.index(r["kind"])))
# practical use before demonstration?
byc = {}
for r in rows:
    byc.setdefault(r["concept_id"], {})[r["kind"]] = r["date"]
for c, d in byc.items():
    if c in targets and "first_demonstration" in d and "first_practical_use" in d and d["first_practical_use"][:4] < d["first_demonstration"][:4]:
        log.append({"concept_id": c, "verdict": f"WARNING practical use {d['first_practical_use']} before demonstration {d['first_demonstration']}"})
(HERE / "milestones3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
(HERE / "raw/quote_check3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in log))
(HERE / "raw/ms3_concept_notes.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in notes))
print("agent milestones", len(ms), "-> kept", len(best), "for", len({r[0] for r in best}), "target concepts;",
      len(rows), "rows in milestones3.jsonl")
print("source verdicts", Counter(x["verdict"].split(":")[0] for x in log if "url" in x))
for x in log:
    if "url" not in x or x.get("note"):
        print(" ", x)
for t in tools:
    print("tools", t)
