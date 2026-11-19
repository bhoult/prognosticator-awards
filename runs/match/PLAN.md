# The full matching and judging run: plan

Status: approved 2026-11-03, with every recommendation in §14. Tranche A is starting.

This run takes every verified claim through DESIGN §5–8: concepts, matching, milestones,
judging, resolutions and scores. The method is the one the computing pilot settled on
(`pilot/computing/report.md`, `report2.md`, `report3.md`; the findings are in DESIGN §5–7).
This plan covers what changes at full scale and what the pilot never tested.

## 1. Scope

- **Claims:** 123,647 from 3,256 books. These are the claims that passed quote verification
  and were speculative when written, from four extraction runs: Stage 1, 1b, 1c, and the
  20-book extraction pilot (`pilot-sonnet`). The computing pilot's export left the 20 pilot
  books out.
- **Two tranches.** The pilot validated its method on technology only, so the run is split:

  | Tranche | Categories | Claims | Books |
  |---|---|---|---|
  | **A**: technology and science | technology, science, and the technical domains | 77,436 | 3,224 |
  | **B**: events and social change | event, social, political, economy | 46,211 | 3,182 |

  A claim goes by its `category`. A category the extractor got wrong is replaced by a mapping
  of its `domain` (§2); the `other` category also goes by domain. Tranche A runs first. B
  needs its own milestone semantics (§9) and is designed after A reports.
- **Not in this run:** `wrong_outcome` judgments (DESIGN §8a), prior art, documented
  influence, author facts, and publishing. This run's outputs feed `schema.sql` and the
  publishing step.

## 2. Export (deterministic)

A new version of `pipeline/export_claims.py` writes `work/match/<run>/claims.jsonl` and
records its sha256.

- **Years from the dating pass.** The extraction headers carried the library's year, and the
  ISFDB dating pass corrected that year for 165 books. The export takes `year` from
  `lists/gutenberg-sf-dates.tsv` when the book is listed there, else from the record.
  - 15,873 claims change year.
  - The computing pilot's lead times for those 165 books used the old years.
  - `unknown` becomes null: those claims are matched, but not scored.
  - Negative years (BCE) work in the lead arithmetic, though none are in these runs yet.
- **No re-extraction for the changed years** (DESIGN §12, question 23). For 145 of the 165
  books the year moved earlier. A claim that was speculative in 1956 was speculative in
  1931 too. For the 20 that moved later, the scoring rule already gives 0 to any claim whose
  milestone falls in or before the publication year.
- **Normalized fields.** Stray labels are mapped, as the Stage 1 report says to do on load:
  - a `category` that holds a domain value (5,319 claims) or another off-list value (about
    330, such as `economic` → `economy`);
  - about 60 off-list `domain` values (`military` → `weapons-war`, `technology` → `other`,
    …).

  Each claim also gets its tranche.
- **Blind:** the export carries the claim id, an opaque book id, the year and the claim's
  fields. The author is joined back only at scoring (§8), from the local run directories.

## 3. Concepts: one registry, built before any matching

**Why one registry:** a book counts once per concept, so the same idea registered twice
under two domains would count twice. The registry is global.

- **Seed:** the computing pilot's 131 concepts (`concepts2.jsonl`), with their reviewed
  milestones (`milestones3.jsonl`).
- **Fields:** `concept_id`, `name`, `definition` (one sentence: what it does and how),
  `type` (`technology`; B adds `event` and `social`), `domains`, `aliases`, `wikidata`,
  and `came_true_guess` (yes / no / unsure, which only decides how much research it gets,
  §5).
- **3a. Propose.** For each domain, agents read a fixed-seed sample of 25% of the claims
  (quote and description) in shards of about 2,500, as in the pilot. Each gets the registry
  so far and proposes only the concepts it lacks.
- **3b. Consolidate,** one agent per domain, then one pass over all names:
  - merge duplicates;
  - **split bundles by rule:** a definition names one function and one mechanism. When it
    joins alternatives that could have different first real-world dates ("a factory, mine or
    power plant"), it is split; alternatives of one thing ("holes in cards or tape") are not
    (DESIGN §12, question 18). The word "or" alone is no test: 95 of the pilot's 131
    definitions contain it.

  Merges and splits go to a mapping file.
- **3c. Close the gaps.** After matching (§4), agents propose concepts for the claims coded
  `no_concept` only, and those claims are matched again (as built, 2026-11-04):
  - **Propose:** the 11,923 no_concept claims after both passes, by domain group in shards of
    at most 1,500, with the approved registry's names; only concepts that at least 3 claims of
    a shard return to.
  - **Consolidate:** one agent per domain group against the whole approved registry (merges,
    splits, proposals that duplicate an approved concept, which are claims the earlier passes
    missed, and nothing under 3 claims), then one cross-group merge pass.
  - **The new concepts** go to `concepts_gap.jsonl`; `concepts.jsonl`, approved at checkpoint
    1, stays as it was.
  - **Match:** the no_concept claims against the new concepts and the approved ones they
    duplicated; the answers go on top of both passes in `matches.jsonl`.
  - **A stop:** `gap_review.md` lists the new concepts with their matched claims, for your
    review before milestone research.
  - **Decided (2026-11-05):** new concepts with fewer than 3 matched claims are cut and their
    claims are `no_concept` again; one duplicate is merged. Both are rows in
    `concept_review.jsonl` (`gap_min_claims`, `gap_merge`), applied by `matches-collect`;
    `concepts_gap.jsonl` stays as built. 669 new concepts are kept.
- **Size:** 1,200–2,000 concepts for tranche A is my estimate.
- **Checkpoint 1 (a stop):** you see the registry before matching runs:
  - counts by domain and type;
  - the 50 largest concepts;
  - every merge and split;
  - every definition the consolidation flagged as a possible bundle but kept.

  Your changes go in as review rows (§5).

## 4. Matching

- **Input per claim:** id, quote, description and domain only. No year and no book.
- **Match on the quote** (DESIGN §12, question 21). The description is a helper for telling
  concepts apart; a match the quote doesn't support is not a match.
- **Output per claim:**
  - at most two concept ids, each with a one-line reason;
  - `quote_carries`: yes or no;
  - for no match, a code: `no_concept` (a real prediction the registry lacks),
    `untestable` (a metaphor, a private state, or unfalsifiable), or `too_vague`. The
    `untestable` resolution of DESIGN §8a comes from this code; nothing else produces it.
- **Against the claim's own domain registry,** plus the cross-domain concepts listed in that
  domain. A claim coded `no_concept` is tried once more against the whole registry's names
  and definitions before 3c.
- **Batches:** 350 claims, mixed across books with a fixed seed.
- **Checked in code:** every id resolves, at most two concepts, the codes are valid, and a
  batch whose reasons are mostly identical is redone.
- **Measured:** a second agent re-matches 300 random claims; agreement goes in the report.

## 5. Milestones

The researchers see concept definitions only, never claims.

- **Tools:** `page_text3.py`, `ia_search3.py` and `net.py` move from `pilot/computing/scripts/`
  into one `pipeline/sources.py`, including:
  - the PubMed Central route through E-utilities;
  - the item-restricted archive.org search for lending-library books.

  Every quote is at most 25 words and checked on the fetched page, and the merge checks all
  of them again in code (DESIGN §6). WebSearch is for finding pages only. Blocks are never
  worked around.
- **As built (2026-11-05):** `pipeline/sources.py` (`text`, `check`, `date`, `search`);
  `match.py research-plan` and `verify`. The research covers every concept with a matched
  claim after the gap review (1,087 approved and 669 new), except the pilot's 101 concepts
  with reviewed milestones and unchanged definitions: 1,188 concepts in 80 batches of 15, and
  467 guessed "no" in 12 quick-check batches of 40, in domain order. `verify` writes
  `runs/match/milestones.jsonl` (the pilot's rows plus the verified tier-1 rows) and
  `milestone_notes.jsonl`. Hosts that refused scripted access on 2026-11-05: Britannica,
  HathiTrust, loc.gov, newspapers.com, nytimes.com, science.org, ScienceDirect, IEEE Xplore,
  worldradiohistory.com; the Google Books API was out of quota.
- **Tier 1 done (2026-11-06):** 98 batches (12 checks, 80 tier-1, 6 from the checks' 86
  "fits"); 101 agents, 13.2M tokens, 4% to 12% of the week. `verify`: 1,736 milestones for 970
  of the 1,274 concepts (967 with a scoring milestone), every source fetched again (2,346 ok,
  1 quote not on its page, 11 contemporary sources downgraded). Confidence high 67, medium 590,
  low 1,079; 547 contemporary sources; 1,030 milestones rest on Wikipedia alone. Agents used
  about 3.5 tool calls per concept, not the 8-12 asked, and often dated the famous example.
  The checks answered from knowledge, without searches. Of 67,487 claim-concept pairs, 33,345
  have a scoring milestone and 34,142 are open; 1,541 open claims belong to 79 concepts
  guessed "came true" (some real misses, e.g. electrification, stellar evolution, air taxis,
  bunkers). Prompt v3 (from tier1-044) lets a year BC be written `-YYYY`; `verify` sorts
  dates by year. Notes in `rejected_batches.tsv`.
- **Second look done (2026-11-06):** the 79 concepts guessed "came true" with no scoring
  milestone went to 16 `recheck` batches of 5 (`prompts/milestones_recheck.md`: the tier-1
  prompt with the first pass's note as a lead, 10–15 tool calls per concept). 34 gained a
  scoring milestone (swamp drainage −0600, helmet-contact speech 1882, self-erasing ink 1866,
  biocontainment labs 1965, air taxis 1911, plant-growth lighting 1880, ...); 45 still have
  none, each with a note on what was searched and the closest event. 18 agent runs, 2.0M tokens.
  `verify`: 1,788 milestones for 1,003 concepts (1,001 with a scoring milestone; 2,434 sources
  ok, 11 downgraded, 1 quote not on its page). Of the 67,487 pairs, 17,201 have a positive
  lead and go to judging, 16,838 score 0 by rule (lead ≤ 0), 3 have no year, and 33,445 are
  open (654 concepts: 273 researched without a fitting event, and 381 the checks found none for).
  The agents reported that the session's WebSearch budget ran out during the pass.
- **Tier 1: every concept with a matched claim.** One researcher per about 15 concepts gives
  each milestone a verified source, a `fit` sentence and a confidence, preferring a source
  from the time of the event. That is pass 3's prompt with tier-1 effort.
  - Concepts guessed "no" get a quick check instead, one agent per 40: does any real event
    fit? If one does, the concept goes to full research.
- **First scoring:** tier 1 is judged (§7) and scored (§8). That shows which milestones
  decide the rankings.
- **Tier 2: the deciding concepts.** These are the concepts whose milestone carries:
  - one of the top 300 single predictions;
  - the best entry of a top-100 book or author;
  - a top-50 entry of any era;
  - more than 40 years of lead for 20 or more claims.

  Each gets contemporary-source research, and its scoring milestone gets the
  earliest-event check. Pairs whose milestone changes are judged again by both judges.
- **Tier 2 as built (2026-11-16):** `prompts/milestones_tier2.md` (the pilot's
  earliest-event check with tier 1's tools and source rules, plus Wikipedia's own citations
  through `action=raw` as the route to contemporary sources, a search for the practical use of
  demonstration-only technologies, and a fallback when WebSearch is used up). The 165
  concepts of `deciding.jsonl` are 33 `tier2-NNN` batches of 5, most points first, in
  `research/batches.json`; each input holds the definition, the current demonstration and
  practical use with their sources, and the earlier notes (no claims, leads or points).
  Every given milestone gets `confirmed`, `replaced` or `removed`, and a missing kind can be
  `added`; `mass_adoption` is left alone. `verify` applies them over tier 1: a verified answer
  replaces the milestone (`tier` 2, `previous_date`, `checked`), `removed` drops it, and an
  answer with no verified source leaves the earlier one, marked. It then writes the
  checkpoint-3 table, `runs/match/deciding_milestones.md`, with the pairs whose id changes.
  Test batch tier2-001 (181K tokens, 59 tool calls, 9 minutes; WebSearch worked): 5 confirmed,
  4 replaced, all 21 quotes verified; death ray's practical use 2014 → 2003 (Zeus-HLONS
  against mines and unexploded munitions, flagged as a judgment call), closed-loop life support
  2014 → 1972 (BIOS-3), spacecraft radio 1958 → 1957 (Sputnik 2), spacesuit practical use
  1965 → 1969 (Soyuz 4/5 transfer; umbilical-fed Gemini suits rejected on "own air supply").
- **Tier 2 done (2026-11-16):** 33 agents, 4.9M tokens, 11 tool calls per concept, 5.4
  agent-hours; week usage 60% → 63%. 274 verdicts: 163 confirmed, 97 replaced, 14 added, none
  removed; every answer kept a verified source (2,965 quotes ok, 17 contemporary sources
  downgraded, 1 fetch failed on a 429 and is retried on the next `verify`). The scoring
  milestone changed for 90 of the 165 concepts (50 earlier, 13 later, 27 only in month or
  kind). Confidence of the scoring milestones: high 27, medium 90, low 48 (was 10, 56, 99);
  137 have a contemporary source (was 65), 7 rest on Wikipedia alone (was 82), 53 are
  demonstrations only (was 66). 4,091 pairs are new and 4,392 drop out; 853 of the new ones
  belong to a milestone confirmed in the same year and kind (only the date got more precise).
  **Checkpoint 3 (a stop):** `runs/match/deciding_milestones.md`.
- **Checkpoint 3 (a stop):** you get the table of deciding milestones (old date, new date,
  event, sources, confidence, fit), as in report3 §3.1. Your decisions go in
  `runs/match/milestone_review.jsonl`, and the scripts apply them.
- **Checkpoint 3 decided (2026-11-18):** you took the recommendations. `milestone_review.jsonl`
  has one row per concept and kind (`decision` keep_previous or accept, the `tier2_date` it was
  made on, and a `reason`); `verify` applies it last, and a row whose tier-2 answer has another
  date stops it. Two answers are overruled and keep the earlier milestone, marked
  `tier2_overruled` (the overruled answer stays in `milestone_notes.jsonl`): sleep learning keeps
  the pilot's 2019-02 (tier 2 brought back LeShan's 1942 nail-biting study, which the pilot's
  review rejected; tier 2 was not given the pilot's review decisions), and wearable wings keeps
  its 1935 practical use (Sohn's exhibition flights, over the 1999 wingsuits on sale). Aquaculture
  1927 and increased human height 1860 are accepted on the record. The scoring milestone now
  changes for 88 of the 165 (49 earlier, 12 later, 27 in month or kind). The 2015 air-purification
  source that failed on a 429 verified on the retry.
- **Later tier-2 rounds (2026-11-18, the user: "go" at checkpoint 4, then "continue until all
  tokens are used", "use up to 20 agents"):** round 2 (tier2-034..039) checked the 26 concepts the
  re-scoring moved into the deciding set; round 3 (tier2-040) the one newcomer after that
  (electronic tracking tags). The check showed that the concepts tier 2 had checked carried only
  half the author points, so the selection was widened: `score` also selects every concept that
  adds `AUTHOR_MIN` (5) or more points to the author totals (each author's best entry on it,
  summed). Round 4 is the 451 concepts that adds (tier2-041..131), with up to 20 agents at a time.
  Rounds 2–4: 98 agents, 14.8M tokens; over all four rounds 643 concepts and 1,108 verdicts
  (667 confirmed, 373 replaced, 67 added, 1 removed), and the scoring milestone changed for 356.
  Seven batches marked a year change "confirmed" and were sent back to mark it "replaced". The
  re-scoring after round 4 selected no newcomers: all 588 deciding concepts are checked.
- **Review assist (2026-11-18, advisory):** `pipeline/review_assist.py plan full <base> 4` gives
  a second reader (`prompts/milestones_review_assist.md`, no web) every demonstration or practical
  use a round replaced, added or removed, beside the milestone before it (from `<base>`'s
  milestones.jsonl) and the definition; `collect` writes `runs/match/milestone_review_suggestions.md`.
  Round 4: 309 rows, 241 accept, 16 keep_previous, 52 unsure; 11 agents, 0.9M tokens. Nothing is
  applied: decisions go in `milestone_review.jsonl`. **Checkpoint 3 for rounds 2–4 (a stop).**
- **Concepts with only a demonstration** (DESIGN §12, question 20): the pilot's rule scores
  them on that demonstration. Proposed: keep the rule, and flag those entries in the
  rankings.

## 6. Pairs and rules (deterministic)

- **The scoring milestone:** `first_practical_use`, else `first_demonstration`.
- **Lead time:** milestone year minus publication year. Zero or less scores 0 by rule; no
  milestone means `open`.
- **`will_not` claims** (2,109) score no points. One judge scores them as usual, which
  asks whether the claim is about the same thing. At 0.5 or more, with the milestone after
  publication, they resolve as `contradicted_negative`.
- **Re-runs** copy every judgment whose claim, concept, milestone kind and date are
  unchanged.

## 7. Judging

- **The prompt:** `judge_prompt2.md`'s three amendments (DESIGN §7) go into
  `prompts/judge.md` as `judge_v1`, pinned by sha256.
- **Two independent judges on every judged pair** (DESIGN §12, question 19):
  - the same pairs in two different fixed-seed shuffles, in mixed batches of about 200;
  - the score is the mean of the two (steps of 0.125);
  - where they are two or more steps apart, a third judge decides and the median counts.
- **The lean variant,** for comparison: the second judge only on each book–concept entry's
  best pair, repeated until the best pairs stop changing. It saves about a fifth of the
  judging, but the single-judged pairs then compete with the averaged ones.
- **Checked in code:** every line parses, scores are on the scale, one line per pair, and at
  least 80% of rationales are distinct.
- **The report** gives agreement between the judges (the same score, one step apart,
  further) overall, by concept type, and on a random 300.
- **As built (2026-11-06):** `match.py judge-plan full [n] [A|B|C]` and `judge-collect full`.
  The pairs and batches are fixed once in `work/match/full/judge/` from the verified milestones
  (the plan refuses to start if any research output is newer than `milestones.jsonl`): 17,201
  pairs with a positive lead (17,065 `will`, 136 `will_not`), judge A on all of them in 87
  batches, judge B on the `will` pairs in 86, and C batches built once A and B are done.
  `judge-collect` writes `runs/match/judgments.jsonl` and `judging.md`. The pair id hashes
  claim, concept, milestone kind and date, so a re-run copies unchanged judgments.
- **Test (2026-11-06):** A-001 and B-001 each read their 200 pairs in four 50-line Read calls
  and wrote as they went (the first chunk with Write, the rest appended with `cat >>`), in 11
  tool calls, about 130K tokens and 3–4 minutes each; both pass the code checks, with 200
  distinct rationales. Scores: A 0 ×7, 0.25 ×51, 0.5 ×103, 0.75 ×38, 1 ×1; B 0 ×5, 0.25 ×46,
  0.5 ×106, 0.75 ×42, 1 ×1. The rationales name what each quotation says; the 0.75s are real
  function-and-mechanism matches with a stated difference. A-001's two `will_not` pairs (food
  pills 1895, lie detector 1910) were scored on subject, not on the denial (0.5 each). The two batches share only 2 pairs
  (both 0.5 from each judge), so agreement waits for the full run. Estimate for the rest: 171
  A/B batches at about 130K tokens, plus 10–20 C batches: 23–25M tokens, about 14–16 points of
  the week (13% used after the test).
- **Full run done (2026-11-15):** 174 agents (87 A, 86 B, 1 C), 22.2M tokens, 35% to 47% of
  the week; every batch passed the code checks the first time, none redone. 17,201 judgments in
  `work/match/full/judgments.jsonl` (9.9 MB, out of git as §11 says; `judge-collect` now writes
  it there) and `runs/match/judging.md`. The judges agree closely: on the 17,065 pairs both
  scored, 70% the same, 30% one step apart and 0.6% (96) two or more, which one C batch decided
  (C landed between A and B on 52, with A on 23, with B on 20). A random 300: 67%, 32%, 1%.
  Mean score 0.494 (A and B 0.494 and 0.496 on the shared pairs); 208 pairs at 0.875 or more.
  Judges differ in leniency at the 0.5/0.75 boundary (from 22 to 81 of 200 batch pairs at 0.75
  or more; A-068 the most lenient, e.g. 0.75 for a tube and mouthpiece as "painless death on
  demand"), and averaging absorbs it because the gaps are one step. 92 of the 136 `will_not`
  pairs score 0.5 or more: the `contradicted_negative` candidates (§6). Most judges appended
  chunks with `cat >>` or joined per-chunk part files instead of rewriting with Write; all read
  the input in four 50-line Reads.
- **Re-judging after tier 2 (2026-11-18):** `judge_batches` adds a round once every batch is
  done and the milestones have changed since the last round: the current pairs no round has go
  to `judge/pairs-2.jsonl`, and their batches continue the numbering (A-088–A-103, B-087–B-102,
  then C-002). A pair whose milestone tier 2 confirmed in the same kind and year copies its
  earlier pair's judgments (`reuse`; 853 of the 4,019 new pairs), since only the date got more
  precise and lead counts whole years. `judge-collect` scores the current pairs from every round.
  33 agents, 4.3M tokens, 64% to 66% of the week; every batch passed the code checks. 3,166 pairs
  judged: 71% the same score, 28% one step, 0.4% (14) two or more, which C-002 decided; mean
  0.462. Three replacements kept their date (cutting beam 1970, solar-thermal propulsion 1999,
  synthetic food 1939), so their 173 pairs keep round-1 judgments made against the earlier event.
  Round 3 (after tier-2 round 2): 61 pairs judged, 132 copied, 1 to C-003. Round 4 (after the
  widened round 4): 3,247 pairs judged by both judges and 1,513 copied (A-105–A-121, B-104–B-120,
  C-004 for 26 pairs); 67% the same, 32% one step, 0.8% further; 38 agents over rounds 3–4, 4.5M
  tokens.

## 8. Resolutions and scores (deterministic)

- **Resolutions** (DESIGN §8a):
  - `realized`;
  - `open`;
  - `untestable`, from the matcher's code;
  - `failed`:
    - `contradicted_negative`, as in §6;
    - `missed_deadline`, only where `stated_time` names a calendar year or a century
      ("by 1975", "the twenty-second century"), parsed by rule. The field is free text and
      mostly relative or story time ("two years", "eight-thirty sharp this morning"); those
      don't count.
- **Scores:** points, one count per book (by the opaque id) and per author, and the rankings
  of DESIGN §8. Authors are joined from the run directories at this step, never shown to a
  model.
- **As built (2026-11-16):** `match.py score full`, deterministic, about 2 seconds. It writes
  `work/match/full/books.jsonl` and `resolutions.jsonl` (out of git), and `runs/match/scoring.md`
  and `deciding.jsonl`. It refuses to run if a judging output is newer than the judgments or a
  pair with a positive lead is not judged. Decided here, for your review:
  - Points come from every judged score above 0, as DESIGN §8's formula and the pilot have it.
    Points only from 0.5 would drop 3,046 of the 11,811 entries and 15% of the points; 29 of the
    top 30 authors would stay (the report's sensitivity table).
  - `not_a_prediction` is a fifth resolution, for a claim whose milestone is in or before its
    publication year (15,735 claims). DESIGN §8a has no status for it.
  - A claim realized after its stated deadline is `realized`, and its timing error is recorded.
    `missed_deadline` needs a matched concept. A decade ends in its last year, a century in its
    hundredth.
  - Precision counts tranche-A claims only. Points per book divides by all the author's books
    in the corpus.
  - Every name the dating list gives for a book is credited; 56 books have more than one. A few
    are probably illustrators or writers of introductions (Henri Théophile Hildibrand, Ed
    Emshwiller, John W. Campbell Jr on *Venus Equilateral*) and need review rows before
    publishing. Religious texts rank by text, since the library's author there is the
    translator; so do Anonymous and Various.
- **First scoring (2026-11-16):**
  - Of 77,436 tranche-A claims: 16,420 realized (21%), 15,735 not a prediction, 31,486 open with
    no milestone, 10,692 open with no concept or too vague, 2,558 untestable, 170
    `missed_deadline`, 91 `contradicted_negative`.
  - 11,811 book–concept entries score, from 2,473 books and 773 authors. Top authors: E. E. Smith
    451, H. G. Wells 403, Murray Leinster 389, Jules Verne 364. Top book: *Limanora* (Godfrey
    Sweven, 1903), 250.
  - The deciding concepts for tier 2 are 165 (`deciding.jsonl`). Of their milestones, 99 are low
    confidence, 82 rest on Wikipedia alone and 66 are demonstrations only. The largest is the
    death ray: 606 points from 190 entries, dated by the 2014 LaWS laser.
  - Data issues: the dating pass dates two books 2009 and 2012 (H. P. Lovecraft's *Writings in
    the United Amateur, 1915–1922*; Harry Bates's *Astounding Stories* of January 1930).
    Translations carry the translation's year (Lucian 1780, the Mahabharata 1896), which
    understates their lead until DESIGN §1a's dates are built.
- **Scoring after tier 2 (2026-11-18):** 16,161 realized, 15,994 not a prediction, 81
  `contradicted_negative`; 11,585 entries from 2,457 books and 771 authors, 26,458 points (27,931
  at the first scoring). The top 30 authors are the same 30 and 29 of the top 30 books stay. Once
  tier 2 has run, `score` keeps `deciding.jsonl` as the first scoring's selection and lists the
  concepts that carry a top entry now but were not checked: 26 of 165, most small, some wrong
  (orbital docking dated by Apollo 11, which tier 2 later confirmed: the definition needs crew or
  cargo to pass). **Checkpoint 4 (a stop):** `runs/match/report.md`.
- **Scoring after tier-2 round 4 (2026-11-18):** 15,719 realized, 16,447 not a prediction, 82
  `contradicted_negative`; 11,319 entries from 2,458 books and 773 authors, 25,971 points. Against
  the first scoring the top 9 authors keep their places, 29 of the top 30 stay and 27 of the top 30
  books. The selection rule now also takes every concept adding `AUTHOR_MIN` points to the author
  totals; 588 concepts are deciding and all are checked. `runs/match/report.md` is updated.

## 9. Tranche B: events and social change

**Designed after tranche A reports.** The proposal now:

- **Concept types:** `event` (a war, a revolution, a discovery, a disaster) and `social` (a
  change in how people live or are governed).
- **Milestones use the same three fields, with type-specific meanings,** so the scoring rule
  doesn't change:
  - an event's `first_practical_use` is the event itself;
  - a social change's `first_practical_use` is the first place where it became law or common
    practice, and its `mass_adoption` is when it became widespread.
- **A pilot first:** about 2,500 society-politics claims end to end, with a checkpoint, before
  the rest of B. The 17 religious and prophecy texts are in B.

## 10. Orchestration

- **The driver:** `pipeline/match.py`, shaped like `extract.py`:
  - `plan`;
  - `next <stage> [n]`: claims batches, writes their input files, prints the subagent prompt;
  - `ingest <stage>`: validates the outputs and marks the batches done;
  - `verify`: checks milestone sources;
  - `status`.
- **Restartable at any point:** state lives in `work/match/<run>/`, one file per batch input
  and output, written atomically. Finished batches are skipped. Each stage pins its prompt's
  sha256 and refuses to mix versions.
- **The agents:** local Claude Code Sonnet subagents, up to 8 at a time, run in the
  background. Each writes its output after every item (the cloud restarts in pass 3 showed
  why). Research runs locally (DESIGN §12, question 22).
- **Usage cap:** the run shares the weekly limit with everything else, so you set a cap.
  - Before each wave of launches, the session reads the usage page.
  - At the cap it stops launching and picks up after the Thursday reset.
  - The usage-guard skill is a backstop at 90%.
- **Calibration:** the first 20 matching batches (about 7,000 claims) measure how much of the
  week a million tokens costs. Today 0.75M tokens left the usage page at 75%, so there is no
  rate yet. After calibration the session reports the projected number of weeks before going
  on.

## 11. Outputs

- **Committed:** the small, reviewable, public-safe files:
  - the concept registry and its merge and split mapping;
  - milestones with their sources (quotes of at most 25 words from public pages);
  - the review files, prompts and scripts;
  - the usage log and the run report.
- **Kept in `work/match/<run>/`:** the large files:
  - claims (about 65 MB for all 123,647);
  - matches;
  - pairs;
  - judgments (about 70 MB).

  They are published through the SQLite file and Parquet exports (DESIGN §10) as release
  assets, not as JSONL in git: GitHub refuses files over 100 MB, and every re-run would grow
  the repository. The quotes are from public-domain texts: Gutenberg, and predictive texts
  from before 1930.

## 12. Cost and time

Rates are from the pilot's usage logs, in tokens per item as Claude Code reports them.

| Stage | Pilot rate | Tranche A volume | Tranche A tokens |
|---|---|---|---|
| Concepts (sample, 3c, consolidation) | 90 per claim read | ~31K claims read | 3–5M |
| Matching | 300–450 per claim | 77,436 claims | 23–35M |
| Tier 1 milestones | ~9K per concept | 850–1,400 concepts | 8–13M |
| Tier 2 and earliest-event check | ~20K per concept | 150–300 concepts | 5–10M |
| Judging, two judges | 470–620 per judgment | ~42K pairs × 2 | 39–52M |
| Third judge, re-judging after tier 2 | | ~10–15% more | 4–8M |
| **Tranche A** | | | **~85–125M** |

- **Tranche B:** roughly 50–70M tokens on the same rates, since event research should be
  cheaper.
- **Both tranches:** about 135–195M tokens. That is 5.5–8 times the 24.1M that Stage 1's
  subagent batches took. Tranche A alone is 3.5–5 times.
- **The lean judging variant** saves about 10M in tranche A.
- **Time:** tranche A is about 45–115 agent-hours, most of it tier-1 research (the pilot's
  researchers took up to 3 minutes a concept). At 8 at a time, that is 6–14 hours of wall time
  if the usage cap allows; the cap decides the number of weeks.

## 13. Checkpoints (each one a stop)

1. **The registry** (§3): you approve it before matching.
2. **Calibration** (§10): the projected weeks, before matching goes on.
3. **The deciding milestones** (§5): your review before the final judging.
4. **The final rankings and report.**

## 14. Decisions (2026-11-03: the user took every recommendation)

1. **Tranches:** A (technology and science) first; B designed after A reports.
2. **Judging:** two independent judges on every judged pair, scored as their mean, with a third
   judge where they are two or more steps apart.
3. **Weekly usage cap:** stop launching agents at 85% of the week.
4. **Bundled concepts:** split by the rule in §3.
5. **Demonstration-only concepts:** scored on the demonstration and flagged in the rankings.
6. **Matching:** on the quote, with the description as a helper.
7. **Research:** runs locally.
8. **Changed years:** leads recomputed from the dating table; no re-extraction.
9. **Outputs:** the large files stay in `work/` and are published through the database
   exports, not in git.
