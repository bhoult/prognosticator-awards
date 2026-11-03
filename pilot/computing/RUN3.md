# Pilot, third pass: the milestones that decide the ranking, and a second judge

The second pass ([`report2.md`](report2.md)) replaced search summaries with verified quotes, but nearly every source was one Wikipedia article, the judge gave seven 1.0 scores (six of them the new top 6), and several milestones that decide the ranking are late or stretched (§6.4). This pass does not redo everything. It re-researches only the 33 concepts whose milestones carry the top 100 or that lost their milestone, with more sites allowed (contemporary magazines, museum and agency archives, paper metadata), re-scores what changes, and puts a second, blind judge on the top 100.

Read `report2.md`, `RUN2.md`, `DESIGN.md` §6–§8 and the second-pass scripts first; reuse them (`net.py`, `page_text.py`, `merge_milestones2.py`, `make_pairs2.py`, `make_judgments2.py`, `report_tables2.py`, `judge_prompt2.md`).

**Work on this branch and push after every step.** Outputs go in `pilot/computing/` with a `3` in the name; leave the first- and second-pass outputs unchanged (new scripts get a `3` too; don't change what a second-pass script does). Use the Agent tool with `model: "sonnet"`. Spend at most **12 subagents** in total, and log each (purpose, tokens, seconds) in `usage3.tsv`. Do the deterministic steps in code in the main session.

## Targets

The 28 concepts whose milestone (the one the ranking uses) carries an entry in the second pass's top 100 (computed as in `report2.md` §6.2):

mind-reading-machine, thought-to-text, robot-supervisor-hierarchy, brain-computer-interface, speech-to-text-dictation, virtual-reality, iris-retina-recognition, speech-recognition, face-recognition, information-retrieval, automated-factory, speech-synthesis, robot-police-guard, machine-readable-id-card, companion-robot, question-answering-computer, machine-generated-writing, holographic-3d-display, touch-gesture-interface, computer-video-display, machine-learning, robot-vacuum-mower, electronic-book-reader, three-d-printing, real-time-tactical-display, neural-implant-augmentation, spacecraft-guidance-computer, space-station-automation

and the 5 that lost their milestone in the second pass because no source could be fetched: service-robot, computer-personnel-selection, sleep-learning, consumer-analytics, speaker-recognition.

Recompute the 28 from `judgments2.jsonl` and stop if your list differs; write the final list to `raw/targets3.jsonl` with, for each concept, its `milestones2.jsonl` rows and the doubt from `report2.md` §6.4 if there is one.

## Steps

1. **Check the network.** The environment now also allows the hosts below. Fetch one ordinary page or API call from each (descriptive User-Agent, as in `net.py`) and record status and time in `raw/netcheck3.jsonl`; put the table in `report3.md`. Hosts: `books.google.com` and `www.googleapis.com/books/v1` (Google Books: scanned magazines such as *Computerworld*, *InfoWorld*, *Popular Science*, *Popular Mechanics*, *Life*, many in full view), `www.worldradiohistory.com` (scanned electronics and radio magazines), `bitsavers.org` (scanned computer manuals and brochures), `archive.computerhistory.org` and `www.computerhistory.org`, `ethw.org`, `spectrum.ieee.org` and `ieeexplore.ieee.org` (abstract pages), `*.si.edu`, `*.nasa.gov` (including `ntrs.nasa.gov`), `pmc.ncbi.nlm.nih.gov` and `pubmed.ncbi.nlm.nih.gov`, `www.nature.com`, `api.crossref.org` (publication dates of papers), `api.semanticscholar.org`, `babel.hathitrust.org`, `archive.org` (including its full-text search), `www.smithsonianmag.com`, `www.aip.org`, `www.hagley.org`, `www.thehenryford.org`, `www.nobelprize.org`, `*.mit.edu`. Britannica refuses scripted access (403) whatever the allowlist says; don't use it.
2. **Fetch helpers.** Extend the helpers as needed in new files (`scripts/page_text3.py` may import `page_text.py`), so that `--check` works for the source types the agents will use: plain HTML pages, PDF text (`pdftotext` if available, else skip PDFs), Google Books (a source is the API search URL `https://www.googleapis.com/books/v1/volumes?q=...`, and its quote must occur in a returned `textSnippet` or description of the volume cited; `date` is the volume's `publishedDate`), and Crossref/Semantic Scholar metadata (the quote may be the title; the date comes from the record). Test each on one real example before step 3.
3. **Research** → `raw/ms3_b01–b03.jsonl`, three Sonnet agents, 11 concepts each. Write `scripts/milestone_prompt3.md` from `milestone_prompt2.md` with these changes:
   - The input for each concept is its `targets3.jsonl` row: the second-pass milestones and why they are doubted. The second pass is not the answer; check it.
   - **Prefer contemporary sources**: a magazine, newspaper, paper or official document from the year of the event (Google Books magazines, worldradiohistory, bitsavers, the CHM archive, NASA NTRS, papers via Crossref or PubMed). `kind: "contemporary"` only for a source published within two years of the event. A milestone with a contemporary source and a reference source that agree may be `high`.
   - **Earliest, strictly fitting event.** For each kind, name the earlier candidates considered and why each was rejected, as before. For the doubtful ones say explicitly what was searched (e.g. centrally dispatched AGV fleets in 1970s–80s factories for robot-supervisor-hierarchy; Fanuc's 1981–82 unattended plant for automated-factory; 1980s security and hospital delivery robots for robot-police-guard and service-robot).
   - **Fit.** Each milestone gets `fit`: one sentence on how the event matches the definition's function and mechanism. If only a loose analogue exists, give no milestone for that kind and say so (thought-to-text and mind-reading are the test cases: decoding attempted speech is not displaying thoughts; reconstructing what a person sees is not reading memories). A concept with no milestone is fine.
   - If a site refuses (403, captcha, login wall), move on. Never change the User-Agent to look like a browser or work around a block.
4. **Merge** → `milestones3.jsonl`: `milestones2.jsonl` with every row of the 33 target concepts replaced by the new research, and every other row copied unchanged. Verify every source again in code, independently of the agents, as `merge_milestones2.py` did (`raw/quote_check3.jsonl`); a milestone with no verified source is dropped. Add `previous_date` (the second-pass date for that concept and kind, or null).
5. **Earliest-event check** (one Sonnet agent, `scripts/earliest_prompt.md`): only for target milestones in `milestones3.jsonl` that give any matched claim more than 40 years of lead and whose date or event differs from the second pass. Apply as in RUN2 step 4 (`checked`, `replaced_date`), with sources verified in code. If there are none, skip it.
6. **Re-score** → `judgments3.jsonl`: every pair in `judgments2.jsonl`, plus new pairs for concepts that gained a milestone. Same rules as RUN2 step 5: the ranking's milestone is the concept's `first_practical_use`, else `first_demonstration`. Same kind and date as in the second pass: copy the second-pass judgment. Milestone in or before the claim's year: 0 by rule. No milestone: 0. Otherwise judge with `judge_prompt2.md`, batches of up to 200 pairs mixed across concepts with a fixed seed, at most 4 judges. Keep `action`, `first_pass_score`, and add `second_pass_score` and `second_pass_milestone_date`.
7. **Second judge** → `raw/judge3b_*.jsonl`, then applied in `judgments3.jsonl`.
   - Pairs: the best pair of each of the top 100 book–concept entries (ranked as in `report2.md` §6.2, from step 6's scores), every pair scored 1.0, and 50 other judged pairs with score > 0 chosen at random with a fixed seed (for measuring agreement only; their score is not changed). Shuffle them together.
   - A different Sonnet agent judges them blind with `judge_prompt2.md`: it sees the same fields as the first judge, not the first score or rationale.
   - Combine, for the top-100 and 1.0 pairs only: the same score, keep it; one step apart (0.25), take the lower; two or more steps apart, a third blind judge (one agent for all such pairs) and take the median of the three. Record every score in `judges: [first, second, third?]`, the final in `score`, and `action2: "agreed" | "lower" | "median"`.
   - Recompute the top 100. Entries that entered it without a second judge get one in one more round (one agent; if no subagent is left, take the lower of two and say so). Then stop.
8. **Report** → `report3.md`:
   - The network table, and which hosts the agents actually used.
   - **The 33 target milestones for review**, one table: concept, kind, second-pass date, new date, event, source kinds, confidence, `fit`. Then the concepts that now have no milestone, and why.
   - How many sources are contemporary now.
   - Judge agreement: on the top-100 pairs and on the 50 random pairs, how often the two judges agree exactly, within one step, and further; how many went to a third judge; how the scores moved.
   - The new top 20 (each book once per concept), with the second-pass rank of each entry, and `raw/top100_3.tsv` with the whole top 100 (rank, year, quote of at most 25 words, concept, milestone, lead, judges, score, points).
   - What is still doubtful, and what the full run should do differently.
   - Cost and time (`usage3.tsv`).

## Rules

- Don't change anything outside `pilot/computing/`, and don't edit the first- or second-pass outputs.
- Every output is JSON lines, valid and parseable: write `scripts/validate3.py` (like `validate2.py`) and run it before each push.
- Never store article or book text; quotes of at most 25 words only.
- At most 12 subagents. If a step can't be done as written, do the simplest thing that works and say so in the report.
