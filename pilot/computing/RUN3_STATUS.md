# Run 3: paused (status for resuming)

Paused 2026-11-03 at step 3 because the session's budget ran out. Nothing below step 3 has run.

Done and pushed:
- Targets: `raw/targets3.jsonl` (the 28 recomputed from `judgments2.jsonl` match RUN3.md, plus the 5 that lost their milestone).
- Step 1: `raw/netcheck3.jsonl`. Works: archive.org (full-text search and OCR text of scanned magazines, e.g. *Computerworld*), bitsavers, worldradiohistory PDFs, computerhistory.org, ethw.org, spectrum.ieee.org, nasa.gov and NTRS, PubMed/PMC, Crossref, airandspace.si.edu, aip, hagley, thehenryford, nobelprize, mit.edu. Refused or unusable: Google Books (the API's shared daily quota was exhausted, 429; books.google.com 404), HathiTrust and smithsonianmag.com (403 challenge pages), www.si.edu (403), nature.com (redirects to a blocked login host), IEEE Xplore (202 bot check), Semantic Scholar (intermittent 429), Britannica (403).
- Step 2: `scripts/page_text3.py`, `scripts/ia_search3.py`; each source type was tested on a real example (`raw/helper_tests3.jsonl`); the Google Books test fails on the quota.
- Scripts for steps 4–7, written but not yet run on final data: `merge_milestones3.py`, `select_checks3.py`, `apply_checks3.py`, `earliest_prompt3.md`, `make_pairs3.py`, `make_judgments3.py`, `rank3.py`, `make_judge3b.py`, `apply_judge3b.py`, `validate3.py`.

Step 3 (research), partial:
- The container restarted twice and killed the research agents. `raw/ms3_b02.jsonl` (10 of 11 concepts) and `raw/ms3_b03.jsonl` (9 of 11) were saved. Batch 1 saved nothing.
- Its 11 concepts, plus computer-personnel-selection, consumer-analytics and speaker-recognition, were split into `raw/ms3_in_b04.jsonl` and `raw/ms3_in_b05.jsonl`. Those agents were stopped for budget; whatever they had written is in `raw/ms3_b04.jsonl` and `raw/ms3_b05.jsonl`.
- A trial merge on batches 2–3 kept 43 of 46 milestones. Eight sources were dropped for quotes over 25 words. `milestones3.jsonl` in the repo is that trial and must be regenerated.
- 8 of the 12 subagents are spent (`usage3.tsv`).

To resume:
1. Finish the concepts missing from `raw/ms3_b04.jsonl` and `raw/ms3_b05.jsonl` (at most 2 agents). Verified leads from the lost agents (URL + quote, trimmed to 25 words) are in `raw/leads3.jsonl`: re-check before use.
2. Run `merge_milestones3.py`, then steps 5–8 as RUN3.md says. With 4 agents left, use 1 judge for step 6 and the second and third judges for step 7. Settle round 2 by "lower of two".

Update: batch 6 (`raw/ms3_in_b06.jsonl`, the 8 concepts still unresearched) finished: `raw/ms3_b06.jsonl`, 13 milestones and a note for each of the 8 concepts. **Every one of the 33 targets now has research output** in `raw/ms3_b02/b03/b04/b05/b06.jsonl`. Batches 4 and 5 hold only the concepts they finished; where a concept appears in more than one batch, `merge_milestones3.py` keeps the earliest milestone of each kind. 9 of 12 subagents are spent, 3 left: earliest-event check (if needed), the step-6 judges and the second judge. Settle the third judge and round 2 by "lower of two" and say so.
Next: `python3 -I scripts/merge_milestones3.py`, then steps 5–8.
Open leads: the robot waiter Tanbo R-1 (Pasadena, 1983) for service-robot, and computerized MMPI interpretation for personnel selection; neither could be fetched.
