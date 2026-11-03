"""RUN3 targets -> raw/targets3.jsonl.

Recomputes the top 100 book-concept entries of the second pass (score x log2(1 + min(lead, 500)),
each book once per concept, ties by claim id, as report_tables2.py), takes the concepts whose
ranking milestone carries an entry, checks them against the 28 listed in RUN3.md (exit 1 if
they differ), adds the 5 that lost their milestone, and writes for each concept its
milestones2.jsonl rows and the report2.md 6.4 doubt.
Usage: python3 -I scripts/make_targets3.py
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
L = lambda f: [json.loads(l) for l in open(HERE / f)]  # noqa: E731
claims = {c["id"]: c for c in L("claims.jsonl")}
concepts = {c["concept_id"]: c for c in L("concepts2.jsonl")}

EXPECTED = """mind-reading-machine thought-to-text robot-supervisor-hierarchy brain-computer-interface
speech-to-text-dictation virtual-reality iris-retina-recognition speech-recognition face-recognition
information-retrieval automated-factory speech-synthesis robot-police-guard machine-readable-id-card
companion-robot question-answering-computer machine-generated-writing holographic-3d-display
touch-gesture-interface computer-video-display machine-learning robot-vacuum-mower electronic-book-reader
three-d-printing real-time-tactical-display neural-implant-augmentation spacecraft-guidance-computer
space-station-automation""".split()
LOST = ["service-robot", "computer-personnel-selection", "sleep-learning", "consumer-analytics", "speaker-recognition"]

# report2.md section 6.4, per concept
DOUBTS = {
    "robot-supervisor-hierarchy": "2007 Walgreens/Kiva is one year later than the first pass's 2006 Staples/Kiva and carries four of the top 20. Centrally dispatched AGV fleets in factories and warehouses date from the 1970s-80s, but the checker found no fetchable source.",
    "automated-factory": "The first pass had 1981 for Fanuc's unattended plant; only a later (2001) Wikipedia description could be quoted. Probably about 20 years late; carries #19 and #20.",
    "thought-to-text": "The concept list expected this never to come true. 2020 UCSF decoding of attempted speech is not displaying thoughts: both a stretch and #1.",
    "mind-reading-machine": "2008 ATR reconstruction of 10x10-pixel images a person sees is a stretch: it reconstructs what was seen, not specific thoughts or memories. Carries #8, #12, #15.",
    "robot-police-guard": "2015 Knightscope: the checker named likely earlier security robots (1980s) but could not source them.",
    "service-robot": "No milestone survived verification. Hospital delivery robots (late 1980s) and others exist, but no page could be fetched; 63 pairs score 0. A gap in sourcing, not in history.",
    "computer-personnel-selection": "Lost its milestone: no page could be fetched. A gap in sourcing, not in history.",
    "consumer-analytics": "Lost its milestone (the first pass had 1958 credit scoring): no page could be fetched. A gap in sourcing, not in history.",
    "speaker-recognition": "Lost its milestone: no page could be fetched. A gap in sourcing, not in history.",
    "sleep-learning": "Lost its milestone: no page could be fetched. A gap in sourcing, not in history.",
    "brain-computer-interface": "Stretch introduced by the earliest-event check: Lucier's EEG concert piece (1965) as a brain-computer interface.",
    "holographic-3d-display": "Stretch: static holograms (1962) as a 3D display.",
    "speech-to-text-dictation": "Date the agents called approximate: 1961 (RCA's 1956 phonetic typewriter is probably earlier, but unsourced).",
}

ms2 = {}
for m in L("milestones2.jsonl"):
    ms2.setdefault(m["concept_id"], []).append(m)
pick = lambda c: next((m for k in ("first_practical_use", "first_demonstration") for m in ms2.get(c, []) if m["kind"] == k), None)  # noqa: E731

best = {}
for j in L("judgments2.jsonl"):
    if j["score"] and j["lead_years"] and j["lead_years"] > 0:
        p = j["score"] * math.log2(1 + min(j["lead_years"], 500))
        key = (claims[j["id"]]["book"], j["concept_id"])
        if key not in best or p > best[key][0]:
            best[key] = (round(p, 4), j)
rank = sorted(best.values(), key=lambda t: (-t[0], t[1]["id"]))
top = rank[:100]
print("100th entry points", top[-1][0], "101st", rank[100][0])
found = []
for _, j in top:
    if j["concept_id"] not in found:
        found.append(j["concept_id"])
if set(found) != set(EXPECTED):
    print("DIFFERS: extra", sorted(set(found) - set(EXPECTED)), "missing", sorted(set(EXPECTED) - set(found)))
    sys.exit(1)
print(len(found), "concepts match RUN3.md")
out = []
for c in EXPECTED + LOST:
    k = concepts[c]
    out.append({"concept_id": c, "name": k["name"], "definition": k["definition"], "aliases": k["aliases"],
                "realizable": k["realizable"], "group": "top100" if c in EXPECTED else "lost_milestone",
                "top100_entries": sum(1 for _, j in top if j["concept_id"] == c),
                "milestones2": ms2.get(c, []), "doubt": DOUBTS.get(c, "")})
(HERE / "raw/targets3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
print(len(out), "targets written")
