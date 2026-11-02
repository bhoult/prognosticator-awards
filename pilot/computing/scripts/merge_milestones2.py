"""Step 3 of RUN2: merge the research agents' output into milestones2.jsonl.

Reads raw/ms2_bNN.jsonl. Every source is checked independently of the agent:
  - contemporary/reference: the page is fetched again (scripts/page_text.py) and the quote
    must occur in its text (case, whitespace and curly quotes normalised) and be <= 25 words;
  - wikidata: the quote must name a date that raw/wikidata_dates.jsonl has for that item.
Sources that fail are dropped, and a milestone with no source left is dropped. Each check
is logged in raw/quote_check.jsonl (url, verdict; never page text). Pages are fetched once
per run and kept only in memory.
Also writes raw/ms2_concept_notes.jsonl (the agents' per-concept notes) and prints a summary.
Usage: python3 -I scripts/merge_milestones2.py [glob]   (default raw/ms2_b[0-9][0-9].jsonl)
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_text  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
KINDS = ["first_demonstration", "first_practical_use", "mass_adoption"]
pat = sys.argv[1] if len(sys.argv) > 1 else "raw/ms2_b[0-9][0-9].jsonl"
cids = [json.loads(l)["concept_id"] for l in open(HERE / "concepts2.jsonl")]
wd = {}
for l in open(HERE / "raw/wikidata_dates.jsonl"):
    r = json.loads(l)
    wd.setdefault(r["qid"], set()).add(r["date"])

ms, notes, tools = [], [], []
for f in sorted(HERE.glob(pat)):
    for i, l in enumerate(open(f), 1):
        if not l.strip():
            continue
        r = json.loads(l)
        r["_file"] = f.name
        if "_tools" in r:
            tools.append((f.name, r["_tools"]))
        elif "kind" in r and "date" in r:
            ms.append(r)
        elif "concept_note" in r:
            notes.append({"concept_id": r["concept_id"], "concept_note": r["concept_note"], "batch": f.name})

pages = {}


def fetch(url):
    try:
        return url, page_text.text(url), ""
    except Exception as e:  # noqa: BLE001
        return url, None, repr(e)[:200]


urls = sorted({s["url"] for m in ms for s in m.get("sources", []) if s.get("kind") != "wikidata"})
with ThreadPoolExecutor(4) as ex:
    for url, txt, err in ex.map(fetch, urls):
        pages[url] = (txt, err)

log, out = [], []
for m in ms:
    keep = []
    for s in m.get("sources", []):
        q, url, kind = (s.get("quote") or "").strip(), s.get("url", ""), s.get("kind")
        verdict = ""
        if not q:
            verdict = "no quote"
        elif len(q.split()) > 25:
            verdict = "quote over 25 words"
        elif kind == "wikidata":
            qid = re.search(r"Q\d+", url)
            dates = wd.get(qid.group(0), set()) if qid else set()
            verdict = "ok" if any(d in q for d in dates) else "date not in Wikidata statements"
        elif kind not in ("contemporary", "reference"):
            verdict = f"bad kind {kind!r}"
        else:
            txt, err = pages.get(url, (None, "not fetched"))
            if txt is None:
                verdict = "fetch failed: " + err
            else:
                verdict = "ok" if page_text.has_quote(txt, q) else "quote not on page"
        log.append({"concept_id": m["concept_id"], "kind": m["kind"], "url": url,
                    "source_kind": kind, "verdict": verdict, "batch": m["_file"]})
        if verdict == "ok":
            keep.append({k: s.get(k, "") for k in ["url", "publisher", "date", "title", "quote", "kind"]})
    if m.get("concept_id") not in cids or m.get("kind") not in KINDS:
        log.append({"concept_id": m.get("concept_id"), "kind": m.get("kind"), "verdict": "bad concept or kind"})
        continue
    if not keep:
        log.append({"concept_id": m["concept_id"], "kind": m["kind"], "date": m["date"],
                    "verdict": "milestone dropped: no verified source"})
        continue
    row = {"concept_id": m["concept_id"], "kind": m["kind"], "date": str(m["date"]), "what": m["what"],
           "sources": keep, "confidence": m.get("confidence", "low")}
    if m.get("note"):
        row["note"] = m["note"]
    out.append(row)

# one milestone per (concept, kind): keep the earliest if an agent gave two
best = {}
for r in out:
    k = (r["concept_id"], r["kind"])
    if k not in best or r["date"] < best[k]["date"]:
        best[k] = r
order = {c: i for i, c in enumerate(cids)}
rows = sorted(best.values(), key=lambda r: (order[r["concept_id"]], KINDS.index(r["kind"])))
(HERE / "milestones2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
(HERE / "raw/quote_check.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in log))
(HERE / "raw/ms2_concept_notes.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in notes))
from collections import Counter
print("agent milestones", len(ms), "-> kept", len(rows), "for", len({r['concept_id'] for r in rows}), "concepts")
print("source verdicts", Counter(x["verdict"].split(":")[0] for x in log))
for t in tools:
    print("tools", t)
