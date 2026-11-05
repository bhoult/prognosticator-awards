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
- **Checkpoint 3 (a stop):** you get the table of deciding milestones (old date, new date,
  event, sources, confidence, fit), as in report3 §3.1. Your decisions go in
  `review.jsonl`, and the scripts apply them.
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
