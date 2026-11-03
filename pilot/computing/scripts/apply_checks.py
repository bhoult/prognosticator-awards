"""Step 4 of RUN2: apply the earliest-event checks (raw/check_bNN.jsonl) to milestones2.jsonl.

For each checked milestone the checker's sources are verified exactly as in
merge_milestones2.py (page fetched again, quote <= 25 words and on the page; Wikidata
quotes against raw/wikidata_dates.jsonl). Then:
  confirmed            -> checked: "confirmed" (verified extra sources are added)
  replaced, date given -> date/what/sources/confidence replaced, checked: "replaced",
                          previous date kept in `replaced_date`
  replaced, date null  -> milestone removed (logged)
A replacement with no verified source is not applied: the milestone keeps its date,
gets checked: "confirmed" and a `check_note` saying the proposed replacement failed
verification. Log: raw/check_applied.jsonl. Re-running is safe (it starts from
raw/milestones2_step3.jsonl, the step-3 output saved on the first run).
"""
import json
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_text  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
base = HERE / "raw/milestones2_step3.jsonl"
if not base.exists():
    shutil.copy(HERE / "milestones2.jsonl", base)
ms = [json.loads(l) for l in open(base)]
wd = {}
for l in open(HERE / "raw/wikidata_dates.jsonl"):
    r = json.loads(l)
    wd.setdefault(r["qid"], set()).add(r["date"])
checks = [json.loads(l) for f in sorted(HERE.glob("raw/check_b[0-9][0-9].jsonl")) for l in open(f) if l.strip()]
urls = sorted({s["url"] for c in checks for s in c.get("sources") or [] if s.get("kind") != "wikidata"})


def fetch(u):
    try:
        return u, page_text.text(u)
    except Exception:  # noqa: BLE001
        return u, None


with ThreadPoolExecutor(4) as ex:
    pages = dict(ex.map(fetch, urls))


def verify(s):
    q, url, kind = (s.get("quote") or "").strip(), s.get("url", ""), s.get("kind")
    if not q or len(q.split()) > 25:
        return False
    if kind == "wikidata":
        m = re.search(r"Q\d+", url)
        return bool(m) and any(d in q for d in wd.get(m.group(0), set()))
    if kind not in ("contemporary", "reference"):
        return False
    return pages.get(url) is not None and page_text.has_quote(pages[url], q)


idx = {(m["concept_id"], m["kind"]): m for m in ms}
log, removed = [], set()
for c in checks:
    key = (c["concept_id"], c["kind"])
    m = idx.get(key)
    if not m:
        log.append({"key": key, "result": "unknown milestone"})
        continue
    good = [{k: s.get(k, "") for k in ["url", "publisher", "date", "title", "quote", "kind"]}
            for s in c.get("sources") or [] if verify(s)]
    bad = len(c.get("sources") or []) - len(good)
    if c.get("checked") == "replaced" and c.get("date") is None:
        removed.add(key)
        log.append({"key": key, "result": "removed", "old_date": m["date"], "note": c.get("note", "")})
        continue
    if c.get("checked") == "replaced" and str(c["date"]) != m["date"]:
        if good:
            log.append({"key": key, "result": "replaced", "old_date": m["date"], "new_date": str(c["date"]),
                        "bad_sources": bad})
            m.update(replaced_date=m["date"], date=str(c["date"]), what=c["what"], sources=good,
                     confidence=c.get("confidence", "low"), checked="replaced",
                     note=c.get("note", m.get("note", "")))
        else:
            log.append({"key": key, "result": "replacement rejected (no verified source)",
                        "old_date": m["date"], "proposed": str(c["date"])})
            m.update(checked="confirmed",
                     check_note=f"checker proposed {c['date']} ({c.get('what', '')[:120]}) but no source verified")
        continue
    # confirmed (or "replaced" with the same date: treat as confirmed with new wording)
    seen = {s["url"] + s["quote"] for s in m["sources"]}
    m["sources"] += [s for s in good if s["url"] + s["quote"] not in seen]
    m["checked"] = "confirmed"
    if c.get("confidence"):
        m["confidence"] = c["confidence"]
    m["check_note"] = c.get("note", "")
    log.append({"key": key, "result": "confirmed", "date": m["date"], "bad_sources": bad})
rows = [m for m in ms if (m["concept_id"], m["kind"]) not in removed]
(HERE / "milestones2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
(HERE / "raw/check_applied.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in log))
from collections import Counter
print(len(checks), "checks;", Counter(r["result"] for r in log), ";", len(rows), "milestones")
