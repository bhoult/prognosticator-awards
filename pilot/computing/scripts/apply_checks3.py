"""RUN3 step 5: apply the earliest-event check (raw/check3_out.jsonl) to milestones3.jsonl,
as apply_checks.py did in RUN2: sources verified in code with page_text3.py (quote <= 25
words and on the page, record dates applied, `contemporary` only within two years of the
event); confirmed -> checked "confirmed" (+ verified sources); replaced with a verified
source -> new date/what/fit/sources, checked "replaced", old date in replaced_date;
replaced with date null -> milestone removed; replacement without a verified source ->
not applied (checked "confirmed", check_note says so). Starts from raw/milestones3_step4.jsonl
(saved on the first run). Log: raw/check3_applied.jsonl.
Usage: python3 -I scripts/apply_checks3.py"""
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_text3  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
base = HERE / "raw/milestones3_step4.jsonl"
if not base.exists():
    shutil.copy(HERE / "milestones3.jsonl", base)
ms = [json.loads(l) for l in open(base)]
checks = [json.loads(l) for l in open(HERE / "raw/check3_out.jsonl") if l.strip()]
cache = {}


def verify(s, event_date):
    q, url, kind = (s.get("quote") or "").strip(), s.get("url", ""), s.get("kind")
    if not q or len(q.split()) > 25 or kind not in ("contemporary", "reference"):
        return None
    k = (url, s.get("volume_id"))
    if k not in cache:
        try:
            cache[k] = page_text3.fetch(*k)
        except Exception:  # noqa: BLE001
            cache[k] = (None, "")
    txt, rdate = cache[k]
    if txt is None or not page_text3.has_quote(txt, q):
        return None
    row = {f: s.get(f, "") for f in ["url", "publisher", "date", "title", "quote", "kind"]}
    if rdate:
        row["date"] = rdate
    if kind == "contemporary":
        sy = int(row["date"][:4]) if re.match(r"\d{4}", str(row["date"])) else None
        ey = int(str(event_date)[:4]) if event_date else None
        if sy is None or ey is None or abs(sy - ey) > 2:
            row["kind"] = "reference"
    return row


idx = {(m["concept_id"], m["kind"]): m for m in ms}
log, removed = [], set()
for c in checks:
    key = (c["concept_id"], c["kind"])
    m = idx.get(key)
    if not m:
        log.append({"key": key, "result": "unknown milestone"})
        continue
    date = c.get("date")
    good = [r for r in (verify(s, date or m["date"]) for s in c.get("sources") or []) if r]
    if c.get("checked") == "replaced" and date is None:
        removed.add(key)
        log.append({"key": key, "result": "removed", "old_date": m["date"], "note": c.get("note", "")})
    elif c.get("checked") == "replaced" and str(date) != m["date"]:
        if good:
            log.append({"key": key, "result": "replaced", "old_date": m["date"], "new_date": str(date)})
            m.update(replaced_date=m["date"], date=str(date), what=c["what"], fit=c.get("fit", m.get("fit", "")),
                     sources=good, confidence=c.get("confidence", "low"), checked="replaced",
                     check_note=c.get("note", ""))
        else:
            log.append({"key": key, "result": "replacement rejected (no verified source)", "proposed": str(date)})
            m.update(checked="confirmed", check_note=f"checker proposed {date} ({c.get('what', '')[:120]}) but no source verified")
    else:
        seen = {s["url"] + s["quote"] for s in m["sources"]}
        m["sources"] += [s for s in good if s["url"] + s["quote"] not in seen]
        m.update(checked="confirmed", check_note=c.get("note", ""))
        log.append({"key": key, "result": "confirmed", "date": m["date"],
                    "bad_sources": len(c.get("sources") or []) - len(good)})
rows = [m for m in ms if (m["concept_id"], m["kind"]) not in removed]
(HERE / "milestones3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
(HERE / "raw/check3_applied.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in log))
print(len(checks), "checks;", Counter(r["result"] for r in log), ";", len(rows), "milestones")
