# Tranche A: the full run's report

Run 2026-11-03 to 2026-11-18 under [`PLAN.md`](PLAN.md), on a local machine with Claude Code
Sonnet subagents and no API calls. The full rankings and resolutions are in
[`scoring.md`](scoring.md); this report says how they were made, what changed when the deciding
milestones were checked, and what is still doubtful. It is checkpoint 4 (PLAN §13), a stop for
your review.

## Summary

- **77,436 technology and science claims from 3,224 books** were matched against a registry of
  1,756 concepts and scored against 1,994 verified milestones for 1,104 concepts. 16,161 claims
  are realized (20.9%), 15,994 came after their milestone (not a prediction), 42,472 are open
  (31,486 with no milestone, 6,795 with no concept, 3,897 too vague, 294 other), 2,558 are
  untestable and 251 failed (170 missed a stated deadline, 81 denials were contradicted).
- **The leaders:** E. E. Smith 440 points, H. G. Wells 394, Murray Leinster 369, Jules Verne 356,
  George O. Smith 338. The top book is *Limanora* (Godfrey Sweven, 1903) with 245, then *Across
  the Zodiac* (Percy Greg, 1880) and *Ralph 124C 41+* (Hugo Gernsback, 1911). The top single
  prediction is *The Moon Hoax* (1835) on rocks thrown from the Moon to the Earth (lunar
  meteorites, 1983).
- **Tier 2 moved the milestones a lot and the rankings little.** It changed the scoring milestone
  of 88 of the 165 deciding concepts (49 earlier, 12 later, 27 in month or kind), and 138 of them
  now have a source from the time of the event (65 before). After re-judging, the top 30 authors
  are the same 30 people (none moved more than three places), 29 of the top 30 books stay, and
  the points fall 5% (27,931 to 26,458), mostly because 281 realized claims now come after
  their concept's earlier milestone.
- **The judges agree closely:** of the 16,803 pairs two judges scored, 70% got the same score,
  30% were one step apart and 0.6% were two or more (98, decided by a third judge). Round 2's
  3,138 new pairs agree in the same way (71%, 28%, 0.4%).
- **Cost:** 734 subagents, 94.7M tokens and 52 agent-hours, inside the plan's 85–125M
  estimate. Re-judging after tier 2 took 4.3M tokens, 64% to 66% of the week.
- **Still doubtful** (section 6): 26 concepts that carry a top entry after the re-scoring were
  never checked by tier 2, and some of them are plainly wrong. For example, orbital rendezvous
  and docking is dated by Apollo 11 (1969), but Gemini 8 docked with an Agena target in March
  1966.

## 1. How the run went

| Stage | Agents | Tokens | Agent-hours | Result |
|---|---|---|---|---|
| Concepts: propose, consolidate, cross-domain, audit (§3) | 24 | 2.8M | 1.4 | 1,087 concepts, approved at checkpoint 1 |
| Matching, two passes (§4) | 291 | 34.8M | 12.3 | every claim matched or coded |
| Gap concepts and their matching (§3c) | 59 | 10.3M | 3.2 | 669 new concepts kept |
| Matching agreement (§4) | 1 | 0.2M | 0.1 | 300 random claims matched again |
| Tier 1 research, checks, second look (§5) | 119 | 15.1M | 20.7 | 1,788 milestones for 1,003 concepts |
| Tier 2, the deciding concepts (§5) | 33 | 4.9M | 5.4 | 274 verdicts on 165 concepts |
| Judging, round 1 (§7) | 174 | 22.2M | 7.8 | 17,201 pairs |
| Judging, round 2 (§7) | 33 | 4.3M | 1.3 | 3,166 new pairs |
| **Total** | **734** | **94.7M** | **52.1** | |

Every batch ran as a background subagent with its own input and output file, so the run was
stopped and restarted many times without losing work. Each stage pins its prompt by sha256, and
every output passed the checks in code before it counted. Every log is in
[`usage.tsv`](usage.tsv).

- **Checkpoint 1, the registry:** approved 2026-11-04; the gap concepts were reviewed
  2026-11-05 ([`gap_review.md`](gap_review.md), [`concept_review.jsonl`](concept_review.jsonl)).
- **Checkpoint 2, calibration:** done in the matching stage ([`calibration.txt`](calibration.txt)).
- **Checkpoint 3, the deciding milestones:** decided 2026-11-18 ([`deciding_milestones.md`](deciding_milestones.md),
  [`milestone_review.jsonl`](milestone_review.jsonl)).
- **Matching agreement** ([`agreement.md`](agreement.md)): of 300 random claims matched again by
  a second agent, 205 were matched by both. 133 got the same concepts, 26 overlapping ones and
  46 different ones; 45 were unmatched by both.

## 2. Milestones

The researchers saw concept definitions only, never claims, books or points. Every source quote
(at most 25 words) was fetched again and checked on its page in code by `match.py verify`.

- **Tier 1** covered every concept with a matched claim, one researcher per 15 concepts. Concepts
  guessed never to have come true got a quick check, and those guessed yes but left undated got
  a second look. It mostly dated the famous example from Wikipedia: of 1,736 milestones, 1,079
  were low confidence and 1,030 rested on Wikipedia alone.
- **The first scoring** (2026-11-16) found 165 deciding concepts: those carrying a top-300
  prediction, the best entry of a top-100 book or author, a top-50 entry of an era, or more than
  40 years of lead for 20 or more claims ([`deciding.jsonl`](deciding.jsonl)).
- **Tier 2** gave each of the 165 an adversarial earliest-event check of its demonstration and
  practical use, with a search for sources from the time
  ([`prompts/milestones_tier2.md`](../../prompts/milestones_tier2.md)). Of 274 verdicts, 163
  confirmed the milestone, 97 replaced it and 14 added a missing kind; none removed one.
  Confidence of the scoring milestones went from 10 high, 56 medium and 99 low to 27, 90 and 48.
  Six rest on Wikipedia alone (82 before), and 53 are demonstrations only (66 before). Every
  answer kept a verified source.
- **Checkpoint 3** overruled two answers and kept the earlier milestone:
  - **Sleep learning:** stays at 2019. Tier 2 brought back LeShan's 1942 nail-biting study, which
    the pilot's review had rejected; tier 2 was never given that review.
  - **Wearable wings:** keeps its 1935 practical use (Clem Sohn's exhibition flights) rather than
    1999, when the wingsuits went on sale.

  The other answers were accepted, including the two you left to me: aquaculture 1927 and
  increased human height 1860. The 12 moves to a later date add credit and were checked against
  the definitions, for example the spacesuit 1965 to 1969 ("own air supply") and aircraft
  collision avoidance 1998 to 2014 (avoidance that is automatic, not a warning).
- **The final milestones** ([`milestones.jsonl`](milestones.jsonl)): 1,994 rows for 1,104
  concepts (1,046 demonstrations, 784 practical uses and 164 mass adoptions). The candidates the
  researchers rejected and what they searched are in [`milestone_notes.jsonl`](milestone_notes.jsonl).

## 3. Judging

Two judges score every pair of a claim and a concept whose milestone came after the claim, each
in a different fixed-seed shuffle, in batches of 200
([`prompts/judge.md`](../../prompts/judge.md), `judge_v1`). The score is their mean, or the
median of three when they are two or more steps apart; a `will_not` pair has one judge.

- **Round 1** (2026-11-15) judged 17,201 pairs, and every batch passed the checks the first time.
- **Round 2** (2026-11-18) is the pairs whose milestone tier 2 changed. Their id hashes the claim,
  the concept and the milestone's kind and date, so a changed milestone is a new pair.
  - Of the 4,019 new pairs, 853 copy the judgments of their round-1 pair, because tier 2
    confirmed the same event in the same kind and year and only the date got more precise.
  - The other 3,166 were judged by both judges in 32 batches; the 14 two or more steps apart
    went to a third.
  - 4,282 round-1 pairs left the set: 3,993 are the same claim and concept under the new
    milestone's id, and 289 now have their milestone in or before the claim's year.
  - The two overruled answers put their concepts back on pairs already judged, at no cost.
- **Three replacements kept their date** (cutting beam 1970, solar-thermal propulsion 1999,
  synthetic food 1939), so their 173 pairs keep round-1 judgments that were made against the
  earlier event. Each new event is the same kind of thing in the same year (laser cutting in
  production, a ground test of a solar-thermal thruster, synthetic margarine), so I left them.
- **Agreement and scores** ([`judging.md`](judging.md)): on all pairs judged twice, 70% the same
  score, 30% one step apart, under 1% further, with the same shares by concept type and on a
  random 300. The mean score is 0.484, and 176 pairs score 0.875 or more. Round 2's pairs score a
  little lower (0.462).

## 4. Results

Points are DESIGN §8's: for each book's best claim per concept, the score times
log2(1 + lead), where lead is the milestone's year minus the publication year (at most 500). An
author counts each concept once, from their best book. The full tables (precision, points per
book, eras, the other corpus groups and the sensitivity to scores below 0.5) are in
[`scoring.md`](scoring.md).

| # | Author | Points | Concepts | Books | First scoring |
|---|---|---|---|---|---|
| 1 | E. E. Smith | 439.9 | 170 | 20 | 1 |
| 2 | H. G. Wells | 393.5 | 137 | 27 | 2 |
| 3 | Murray Leinster | 368.6 | 159 | 58 | 3 |
| 4 | Jules Verne | 355.9 | 110 | 16 | 4 |
| 5 | George O. Smith | 337.8 | 138 | 57 | 5 |
| 6 | Ray Cummings | 320.2 | 130 | 36 | 6 |
| 7 | Edmond Hamilton | 291.5 | 107 | 34 | 8 |
| 8 | John W. Campbell Jr | 291.2 | 117 | 12 | 7 |
| 9 | Godfrey Sweven | 265.1 | 93 | 2 | 10 |
| 10 | George Chetwynd Griffith | 257.9 | 92 | 6 | 11 |
| 11 | Raymond Z. Gallun | 253.1 | 102 | 17 | 12 |
| 12 | Randall Garrett | 249.9 | 110 | 78 | 9 |
| 13 | Fritz Leiber | 232.7 | 97 | 29 | 13 |
| 14 | H. Beam Piper | 221.7 | 102 | 32 | 14 |
| 15 | Edgar Rice Burroughs | 209.5 | 81 | 21 | 15 |

| # | Book | Author | Points | Concepts | First scoring |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 245.4 | 86 | 1 |
| 2 | *Across the Zodiac* (1880) | Percy Greg | 151.6 | 48 | 3 |
| 3 | *Ralph 124C 41+* (1911) | Hugo Gernsback | 149.4 | 45 | 2 |
| 4 | *Skylark Three* (1930) | E. E. Smith | 118.4 | 40 | 5 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 115.1 | 43 | 6 |
| 6 | *Spacehounds of IPC* (1931) | E. E. Smith | 114.4 | 43 | 7 |
| 7 | *A Journey in Other Worlds* (1894) | John Jacob Astor | 114.1 | 42 | 4 |
| 8 | *All Around the Moon* (1870) | Jules Verne | 112.6 | 33 | 9 |
| 9 | *A Hundred Years Hence* (1905) | T. Baron Russell | 112.0 | 35 | 8 |
| 10 | *When the Sleeper Wakes* (1899) | H. G. Wells | 110.6 | 42 | 10 |

The best single predictions are old texts with long leads and a close match:

- *The Moon Hoax* (1835): lunar volcanoes throwing rocks to the Earth (1983).
- Cyrano de Bergerac, *A Voyage to the Moon* (1657): a rocket of tiers of squibs that burn one
  after another (multistage rocket, 1944).
- Voltaire, *Micromegas* (1752): the two moons of Mars (1877).
- Cyrano again: a book "made wholly for the Ears" (audiobook player, 1935).
- Luis Senarens, *The Sunken Isthmus* (1896): oxygen made aboard a submarine (1958), the largest
  gain from tier 2.

## 5. What tier 2 changed in the scores

| Resolution | First scoring | Now |
|---|---|---|
| realized | 16,420 | 16,161 |
| not a prediction | 15,735 | 15,994 |
| open: not matched (all judged pairs score 0) | 278 | 288 |
| failed: contradicted negative | 91 | 81 |

354 claims changed resolution: 281 from realized to not a prediction (their concept's milestone
moved before them), 26 the other way, and 47 between open, failed and realized as their
re-judged scores changed. The concepts whose claims lost the most points:

| Concept | Points lost | Milestone moved |
|---|---|---|
| Physical conditions on the Moon and inner planets | 190 | 1974 to 1962 (Mariner 2 at Venus) |
| Death ray | 171 | 2014 to 2003 (Zeus-HLONS against munitions) |
| Electric discharge weapon | 157 | 1993 to 1963 (electric prods used by Alabama troopers) |
| Closed-loop life support | 157 | 2014 to 1972 (BIOS-3) |
| Electronic lock and key | 150 | 1973 to 1949 (the Card-Key entrance lock) |
| Automated factory | 141 | 2001 to 1916 (an unattended power plant) |
| Smart glass window | 127 | 1987 to 1938 (Polaroid windows on a passenger train) |
| Food pills | 95 | 1959 to 1953 (Sustagen, a concentrated nutrient powder) |

The largest gain is submarine life support, +78 points, from 1867 to 1958: the definition
requires staying sealed for long periods. Of the 12 later moves, only that one gains many
points; the others' longer leads were offset by their re-judged scores.

## 6. What is still doubtful

1. **26 deciding concepts that tier 2 didn't check.** Re-scored by the first scoring's criteria,
   165 concepts carry a top entry, but 26 of them are new to that set: the small shifts moved
   them over a threshold. Most carry little (18 have under 35 points), but they include:
   - nerve-attacking weapon (138 points), dated by the 1975 Taser, the same event as the stun
     gun's;
   - orbital rendezvous and docking (113), dated 1969 by Apollo 11, which is wrong: Gemini 8
     docked in March 1966;
   - spacecraft thermal control (102), futuristic cosmetics (93) and the reusable spaceplane (82).

   All 26 are flagged **not checked** in `scoring.md` §"The deciding concepts after tier 2",
   most on Wikipedia alone. Checking them is about six tier-2 batches (0.9M tokens) plus their
   re-judging (perhaps 1–2M), about 1–1.5 points of a week. It could move another few concepts
   over the line.
2. **Scored on a demonstration only:** 59 of the 165 deciding concepts have no practical use
   (marked † in the rankings, PLAN §14.5), among them invisibility (2010 metamaterial cloak),
   the crewed Moon landing and sleep learning. Tier 2 split these into discoveries (no use to
   find) and technologies whose use it searched for.
3. **Low confidence:** 49 of the 165 deciding milestones are low confidence and 22 rest on
   Wikipedia alone, most of them among the 26 unchecked.
4. **Judgment calls accepted at checkpoint 3:**
   - the death ray dated by a laser that destroyed munitions rather than people;
   - the electric discharge weapon dated by the cattle prods Alabama troopers used in 1963;
   - increased human height dated by the start of a trend (1860);
   - aquaculture dated 1927, though the 1860s French oyster parks may be earlier.
5. **Data issues from the first scoring, still open:**
   - The dating pass dates two books 2009 and 2012 (H. P. Lovecraft's *Writings in the United
     Amateur, 1915–1922* and Harry Bates's *Astounding Stories* of January 1930).
   - Translations carry the translation's year (Lucian 1780), which understates their lead
     until DESIGN §1a's composition dates are built.
   - 56 books credit more than one name, and some of the names are illustrators or writers of
     introductions (Henri Théophile Hildibrand appears in the top 10 predictions, beside Jules
     Verne). They need review rows before publishing.
6. **Points from every score above 0:** as DESIGN §8 has it. Counting only scores of 0.5 or more
   drops a sixth of the points (4,405 of 26,458) and keeps 28 of the top 30 authors
   (`scoring.md`, sensitivity).

## 7. For tranche B

- **Give tier 2 every earlier review decision.** The pilot's nine concepts went in without their
  review, which is how sleep learning's rejected 1942 study came back.
- **Re-select the deciding set after re-judging and check the newcomers in the same pass,** or
  select with a margin (the top 400 rather than the top 300), so that small shifts stay inside
  the checked set.
- **Hash the event into the pair id, not only the kind and date,** so that a replaced event with
  an unchanged date is judged again.
- **Judges:** the four 50-line reads worked every time. Several judges appended chunks with
  `cat >>` or wrote the file once at the end instead of after each chunk. The checks found
  nothing wrong, but the write-as-you-go rule is only partly followed.

## 8. Cost against the plan

| Stage | Plan (PLAN §12) | Actual |
|---|---|---|
| Concepts | 3–5M | 2.8M, plus 10.3M for the gap concepts and their matching (not in the plan) |
| Matching | 23–35M | 34.8M (two passes) |
| Tier 1 milestones | 8–13M | 15.1M |
| Tier 2 and the earliest-event check | 5–10M | 4.9M |
| Judging, two judges | 39–52M | 22.2M (17,201 pairs, not the ~42,000 estimated) |
| Third judge and re-judging after tier 2 | 4–8M | 4.3M (the third judge decided 110 pairs over both rounds) |
| **Tranche A** | **85–125M** | **94.7M** |
