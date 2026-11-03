"""RUN3 step 3: research batches raw/ms3_in_b01-03.jsonl from raw/targets3.jsonl.
Adds earliest_claim_year (matches.jsonl + claims.jsonl) and the search hints RUN3.md names.
Usage: python3 -I scripts/make_ms3_inputs.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
BATCHES = [
    "mind-reading-machine robot-supervisor-hierarchy speech-to-text-dictation iris-retina-recognition information-retrieval robot-police-guard question-answering-computer touch-gesture-interface robot-vacuum-mower neural-implant-augmentation service-robot",
    "thought-to-text brain-computer-interface virtual-reality speech-recognition automated-factory machine-readable-id-card machine-generated-writing computer-video-display electronic-book-reader spacecraft-guidance-computer computer-personnel-selection",
    "face-recognition speech-synthesis companion-robot holographic-3d-display machine-learning three-d-printing real-time-tactical-display space-station-automation sleep-learning consumer-analytics speaker-recognition",
]
HINTS = {
    "robot-supervisor-hierarchy": "Centrally dispatched AGV (automated guided vehicle) fleets in 1970s-80s factories and warehouses, directed by a central computer (e.g. FMS lines, Volvo Kalmar 1974, computer-controlled AGV systems in Computerworld / sim_ industrial-engineering periodicals); anything earlier than Kiva (2006-07).",
    "automated-factory": "Fanuc's 1981-82 unattended (lights-out) plant at Mount Fuji / Oshino; other 1960s-80s unmanned factories or automatic plants (contemporary magazines: Computerworld, Popular Science, InfoWorld, sim_ periodicals).",
    "robot-police-guard": "1980s security robots (Denning Mobile Robotics sentry 1985-87, RoboGuard, Prowler, others) and when one was first actually used on patrol by a customer.",
    "service-robot": "1980s hospital delivery robots (Transitions Research Corp. HelpMate, first hospital use), other robots serving the public (restaurants, hotels, museums) before 2014.",
    "thought-to-text": "Test case for fit: decoding attempted or imagined speech is not displaying thoughts. Search for anything that displays or writes out what a person thinks (not what they try to say).",
    "mind-reading-machine": "Test case for fit: reconstructing what a person sees is not reading memories or thoughts. Search for decoding of imagined content, memories or specific thoughts.",
    "speech-to-text-dictation": "RCA's 1956 phonetic typewriter (Olson and Belar) and other 1950s-60s typing-from-speech machines; first dictation product in use.",
    "brain-computer-interface": "Vidal's 1973-77 UCLA work, earlier EEG-controlled devices; decide whether Lucier's 1965 concert piece fits the definition.",
    "holographic-3d-display": "Decide whether static holograms fit; search for the first display of changing (moving) 3D images viewable without glasses.",
    "computer-personnel-selection": "Lost its milestone only for lack of a fetchable source: computerized personnel or job matching in the 1950s-60s.",
    "consumer-analytics": "Lost its milestone only for lack of a fetchable source: the first pass had 1958 credit scoring (Fair Isaac); also computerized market or customer data analysis.",
    "speaker-recognition": "Lost its milestone only for lack of a fetchable source: voiceprint or automatic speaker verification in the 1960s-70s.",
    "sleep-learning": "Lost its milestone only for lack of a fetchable source: decide whether any machine-delivered sleep learning ever worked (it may have no milestone).",
}
years = {json.loads(l)["id"]: json.loads(l)["year"] for l in open(HERE / "claims.jsonl")}
first = {}
for l in open(HERE / "matches.jsonl"):
    r = json.loads(l)
    for c in r["concepts"]:
        first[c] = min(first.get(c, 9999), years[r["id"]])
t = {r["concept_id"]: r for r in map(json.loads, open(HERE / "raw/targets3.jsonl"))}
assert sorted(c for b in BATCHES for c in b.split()) == sorted(t), "batches must cover the 33 targets"
for i, b in enumerate(BATCHES, 1):
    rows = []
    for c in b.split():
        r = dict(t[c])
        r["earliest_claim_year"] = first.get(c)
        r["search_hints"] = HINTS.get(c, "")
        rows.append(r)
    (HERE / f"raw/ms3_in_b{i:02d}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(i, len(rows))
# After two container restarts (see report3.md), batch 1 (no output saved) and the concepts
# batches 2-3 had not finished were re-split by hand into raw/ms3_in_b04.jsonl and
# raw/ms3_in_b05.jsonl (same rows as above).
