"""Step 4 hand fixes to milestones2.jsonl (run after apply_checks.py).

computer-security-hacking: the check moved first_practical_use to the 1967 Evanston
break-in, which is earlier than the first_demonstration (Creeper, 1971). A practical
use is also a demonstration, so first_demonstration takes the same event.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in open(HERE / "milestones2.jsonl")]
idx = {(r["concept_id"], r["kind"]): r for r in rows}
pu = idx[("computer-security-hacking", "first_practical_use")]
de = idx[("computer-security-hacking", "first_demonstration")]
if de["date"] != pu["date"]:
    de.update(replaced_date=de["date"], date=pu["date"], what=pu["what"], sources=pu["sources"],
              confidence=pu["confidence"], checked="replaced",
              note="Set to the same event as first_practical_use (1967), which the earliest-event "
                   "check found; it predates Creeper (1971).")
(HERE / "milestones2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
print("ok")
