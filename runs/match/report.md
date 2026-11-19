# Tranche A: the full run's report

Run 2026-11-03 to 2026-11-18 under [`PLAN.md`](PLAN.md), on a local machine with Claude Code
Sonnet subagents and no API calls. The full rankings and resolutions are in
[`scoring.md`](scoring.md); this report says how they were made, what changed when the deciding
milestones were checked, and what is still doubtful. It is checkpoint 4 (PLAN §13), a stop for
your review. This version follows the later tier-2 rounds of 2026-11-18 and your review of them
(2026-11-19: the review assist's suggestions taken, and a recheck round on its objections).

## Summary

- **77,436 technology and science claims from 3,224 books** were matched against a registry of
  1,756 concepts and scored against 2,047 verified milestones for 1,104 concepts. 15,820 claims
  are realized (20.4%), 16,393 came after their milestone (not a prediction), 42,413 are open
  (31,442 with no milestone, 6,795 with no concept, 3,897 too vague, 279 other), 2,558 are
  untestable and 252 failed (170 missed a stated deadline, 82 denials were contradicted).
- **The leaders:** E. E. Smith 427 points, H. G. Wells 360, Murray Leinster 358, Jules Verne 344,
  George O. Smith 319. The top book is *Limanora* (Godfrey Sweven, 1903) with 227, then *Across
  the Zodiac* (Percy Greg, 1880) and *Ralph 124C 41+* (Hugo Gernsback, 1911). The top single
  prediction is *The Moon Hoax* (1835) on rocks thrown from the Moon to the Earth (lunar
  meteorites, 1983).
- **Every concept that decides the rankings has now been checked by tier 2.** The first check
  covered the 165 concepts that carry a top entry. A recount showed those carried only half the
  author points, so the selection was widened to every concept that adds 5 or more points to the
  author totals: 643 concepts in four rounds, then a recheck of 11 the second reader questioned;
  1,126 verdicts in all. Your review kept the earlier milestone for 21 answers.
- **The rankings held.** Against the first scoring, the top 9 authors keep their places, 29 of
  the top 30 stay (John Jacob Astor leaves, Alfred Coppel enters), and 27 of the top 30 books
  stay. Points fall 7% (27,931 to 26,090), mostly because 898 realized claims now come after an
  earlier milestone.
- **The judges agree closely:** of the 16,335 current pairs two judges scored, 69% got the same
  score, 30% were one step apart and about 1% two or more (decided by a third judge). Each later
  round agrees the same way (round 4: 67%, 32%, 0.8%).
- **Cost:** 914 subagents, 117.4M tokens and 72 agent-hours, inside the plan's 85–125M
  estimate. The later tier-2 rounds, their re-judging and the review assist took 22.1M tokens on
  2026-11-18, 66% to 77% of that week; the recheck and its judging 0.6M on 2026-11-19.
- **Your review** (section 2): the 18 keep_previous suggestions of the second reader are applied,
  with one more for consistency, and every other answer of rounds 2–4 is accepted. The 10 confirmed
  answers it questioned and its one candidate concept went back to tier 2; 7 of the 10 changed, and
  brain transplant got its first milestones on a judgment call (section 6).

## 1. How the run went

| Stage | Agents | Tokens | Agent-hours | Result |
|---|---|---|---|---|
| Concepts: propose, consolidate, cross-domain, audit (§3) | 24 | 2.8M | 1.4 | 1,087 concepts, approved at checkpoint 1 |
| Matching, two passes (§4) | 291 | 34.8M | 12.3 | every claim matched or coded |
| Gap concepts and their matching (§3c) | 59 | 10.3M | 3.2 | 669 new concepts kept |
| Matching agreement (§4) | 1 | 0.2M | 0.1 | 300 random claims matched again |
| Tier 1 research, checks, second look (§5) | 119 | 15.1M | 20.7 | 1,788 milestones for 1,003 concepts |
| Tier 2, round 1: the 165 deciding concepts (§5) | 33 | 4.9M | 5.4 | 274 verdicts |
| Tier 2, rounds 2–4: newcomers and the widened set (§5) | 98 | 14.8M | 17.3 | 834 verdicts on 478 concepts |
| Tier 2, round 5: the recheck (§5) | 2 | 0.4M | 0.4 | 18 verdicts on 10 concepts |
| Judging, rounds 1–2 (§7) | 207 | 26.5M | 9.1 | 17,201 pairs, then 3,166 new ones |
| Judging, rounds 3–5 (§7) | 40 | 4.7M | 1.4 | 3,418 new pairs |
| Review assist (section 6) | 40 | 2.8M | 0.4 | second readings of 834 milestones and 242 concepts with none |
| **Total** | **914** | **117.4M** | **71.6** | |

Every batch ran as a background subagent with its own input and output file, so the run was
stopped and restarted many times without losing work. Each stage pins its prompt by sha256, and
every output passed the checks in code or was redone; the few early matching batches accepted with
notes are in [`rejected_batches.tsv`](rejected_batches.tsv). Every log is in
[`usage.tsv`](usage.tsv). The last rounds ran 20 agents at a time, the most a session allows.

- **Checkpoint 1, the registry:** approved 2026-11-03; the gap concepts were reviewed
  2026-11-05 ([`gap_review.md`](gap_review.md), [`concept_review.jsonl`](concept_review.jsonl)).
- **Checkpoint 2, calibration:** 2026-11-03, on the first 20 matching batches ([`calibration.txt`](calibration.txt)).
- **Checkpoint 3, the deciding milestones:** the first round decided 2026-11-18 ([`deciding_milestones.md`](deciding_milestones.md),
  [`milestone_review.jsonl`](milestone_review.jsonl)); rounds 2–4 decided 2026-11-19, on the review
  assist's suggestions.
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
- **The deciding concepts** ([`deciding.jsonl`](deciding.jsonl)), in the order the scorings
  selected them:
  - round 1, the first scoring's 165: those carrying a top-300 prediction, the best entry of a
    top-100 book or author, a top-50 entry of an era, or more than 40 years of lead for 20 or
    more claims;
  - rounds 2 and 3, 27 concepts that the re-scorings moved over those thresholds;
  - round 4, 451 concepts that add 5 or more points to the author totals (`AUTHOR_MIN`, each
    author's best entry on the concept, summed). Before it, the concepts tier 2 had checked
    carried 50% of the author points; now every concept above the line is checked.
- **Tier 2** gave each one an adversarial earliest-event check of its demonstration and practical
  use, with a search for sources from the time
  ([`prompts/milestones_tier2.md`](../../prompts/milestones_tier2.md)). Of 1,108 verdicts, 667
  confirmed the milestone, 373 replaced it, 67 added a missing kind and 1 removed one
  (radioactive ore on other worlds: Apollo 15 mapped thorium-rich ground, not ore). Of the 588
  concepts that decided the rankings after round 4, 117 milestones were high confidence, 313 medium
  and 158 low; 483 had a contemporary source, 38 rested on Wikipedia alone and 149 were
  demonstrations only.
- **Checkpoint 3** overruled two answers of the first round and kept the earlier milestone:
  - **Sleep learning:** stays at 2019. Tier 2 brought back LeShan's 1942 nail-biting study, which
    the pilot's review had rejected; tier 2 was never given that review. Later rounds were given
    every review decision.
  - **Wearable wings:** keeps its 1935 practical use (Clem Sohn's exhibition flights) rather than
    1999, when the wingsuits went on sale.
- **The review of rounds 2–4** (2026-11-19, you took the recommendation):
  `milestone_review.jsonl` keeps the earlier milestone for the review assist's 18 keep_previous
  suggestions (among them central heating's 1853 and 1877 over the Roman hypocaust, the 1928
  Motograph over an 1872 stereopticon, and tuberculosis's 1944–45 streptomycin trials) and for
  the airlifted-buildings practical use, which would have come before its kept demonstration;
  the 310 other answers are accepted on the record.
- **Round 5, the recheck:** tier 2 checked again, with the objection in hand and its own earlier
  answer as input (`runs/match/tier2_recheck.jsonl`), the 10 confirmed answers the second reader
  questioned and the one concept it thought had happened:
  - replaced: industrial robot (1937 Meccano model to the Unimate's 1961 forging-press demonstration),
    geothermal power (to Boise district heating, 1892, both kinds), anti-satellite weapon (to Nike
    Zeus at Kwajalein, 1963, low confidence), repurposed spacecraft structures (Salyut 1 to Skylab,
    1973), astronaut training (1955 centrifuge simulation; the Mercury Seven's centrifuge training,
    1959), seaplane practical use (the Greek Navy's Dardanelles sortie, 1913-02) and crash
    protection's demonstration (Tucker's padded dash, 1948);
  - confirmed: Starfish Prime as the machinery-disabling ray (low), electrification's 1898 (low; no
    dated earlier first event was found) and Nash's 1949 belts as crash protection's practical use;
  - brain transplant, which had none: Thompson's 1890 graft of brain tissue between animals and the
    first fetal brain-tissue graft into a patient (Lund, 1987), on the definition's "or part of one".
- **The final milestones** ([`milestones.jsonl`](milestones.jsonl)): 2,047 rows for 1,104
  concepts (1,052 demonstrations, 831 practical uses and 164 mass adoptions). The candidates the
  researchers rejected and what they searched are in [`milestone_notes.jsonl`](milestone_notes.jsonl).

## 3. Judging

Two judges score every pair of a claim and a concept whose milestone came after the claim, each
in a different fixed-seed shuffle, in batches of 200
([`prompts/judge.md`](../../prompts/judge.md), `judge_v1`). The score is their mean, or the
median of three when they are two or more steps apart; a `will_not` pair has one judge.

- **Round 1** (2026-11-15) judged 17,201 pairs, and every batch passed the checks the first time.
- **Rounds 2–5** (2026-11-18 and 19) are the pairs whose milestone tier 2 changed. Their id hashes the
  claim, the concept and the milestone's kind and date, so a changed milestone is a new pair. A
  new pair copies the judgments of its earlier pair when tier 2 confirmed the same event in the
  same kind and year and only the date got more precise.

  | Round | New pairs | Copied | Judged by both | Same | One step | Further |
  |---|---|---|---|---|---|---|
  | 2 | 4,019 | 853 | 3,166 | 71% | 28% | 0.4% |
  | 3 | 193 | 132 | 61 | | | 1 pair |
  | 4 | 4,760 | 1,513 | 3,247 | 67% | 32% | 0.8% |
  | 5 | 110 | 0 | 110 | 77% | 23% | 0 |

- **Three replacements of round 1 kept their date** (cutting beam 1970, solar-thermal propulsion
  1999, synthetic food 1939), so their 173 pairs keep judgments made against the earlier event.
  Each new event is the same kind of thing in the same year, so I left them.
- **Agreement and scores** ([`judging.md`](judging.md)): on the 16,440 current pairs judged twice,
  69% the same score, 30% one step apart, about 1% further, with the same shares by concept type
  and on a random 300. Round 4's pairs score 0.473 on average.

## 4. Results

Points are DESIGN §8's: for each book's best claim per concept, the score times
log2(1 + lead), where lead is the milestone's year minus the publication year (at most 500). An
author counts each concept once, from their best book. The full tables (precision, points per
book, eras, the other corpus groups and the sensitivity to scores below 0.5) are in
[`scoring.md`](scoring.md).

| # | Author | Points | Concepts | Books | First scoring |
|---|---|---|---|---|---|
| 1 | E. E. Smith | 426.8 | 163 | 20 | 1 |
| 2 | H. G. Wells | 360.2 | 128 | 27 | 2 |
| 3 | Murray Leinster | 358.4 | 152 | 58 | 3 |
| 4 | Jules Verne | 344.2 | 108 | 16 | 4 |
| 5 | George O. Smith | 319.2 | 131 | 57 | 5 |
| 6 | Ray Cummings | 317.1 | 128 | 36 | 6 |
| 7 | John W. Campbell Jr | 290.2 | 117 | 12 | 7 |
| 8 | Edmond Hamilton | 285.6 | 106 | 34 | 8 |
| 9 | Randall Garrett | 260.0 | 111 | 78 | 9 |
| 10 | George Chetwynd Griffith | 257.7 | 92 | 6 | 11 |
| 11 | Raymond Z. Gallun | 254.8 | 99 | 17 | 12 |
| 12 | Godfrey Sweven | 246.6 | 88 | 2 | 10 |
| 13 | Fritz Leiber | 225.5 | 94 | 29 | 13 |
| 14 | H. Beam Piper | 217.3 | 100 | 32 | 14 |
| 15 | F. L. Wallace | 206.2 | 88 | 18 | 16 |

| # | Book | Author | Points | Concepts | First scoring |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 226.9 | 81 | 1 |
| 2 | *Across the Zodiac* (1880) | Percy Greg | 147.0 | 47 | 3 |
| 3 | *Ralph 124C 41+* (1911) | Hugo Gernsback | 143.4 | 44 | 2 |
| 4 | *Spacehounds of IPC* (1931) | E. E. Smith | 117.7 | 43 | 7 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 114.0 | 43 | 6 |
| 6 | *The Moon-Voyage* (1872) | Jules Verne | 112.8 | 35 | 11 |
| 7 | *Skylark Three* (1930) | E. E. Smith | 110.9 | 38 | 5 |
| 8 | *All Around the Moon* (1870) | Jules Verne | 110.5 | 32 | 9 |
| 9 | *A Journey in Other Worlds* (1894) | John Jacob Astor | 105.6 | 40 | 4 |
| 10 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | 104.6 | 37 | 12 |

The best single predictions are old texts with long leads and a close match:

- *The Moon Hoax* (1835): lunar volcanoes throwing rocks to the Earth (1983).
- Cyrano de Bergerac, *A Voyage to the Moon* (1657): a rocket of tiers of squibs that burn one
  after another (multistage rocket, 1944).
- Voltaire, *Micromegas* (1752): the two moons of Mars (1877).
- Cyrano again: a book "made wholly for the Ears" (audiobook player, 1935).
- Francis Bacon, *New Atlantis* (1627): "helps which set to the ear do further the hearing"
  (hearing aid, 1900). That practical use is new in round 4 and low confidence.

## 5. What tier 2 changed in the scores

| Resolution | First scoring | After round 1 | Now |
|---|---|---|---|
| realized | 16,420 | 16,161 | 15,820 |
| not a prediction | 15,735 | 15,994 | 16,393 |
| open: not matched (all judged pairs score 0) | 278 | 288 | 273 |
| failed: contradicted negative | 91 | 81 | 82 |

Since the first scoring, 1,310 claims changed resolution: 898 from realized to not a prediction
(their concept's milestone moved before them), 261 the other way, and the rest between open,
failed and realized as their re-judged scores changed. Round 1 moved the most points per concept:

| Concept | Points lost | Milestone moved |
|---|---|---|
| Physical conditions on the Moon and inner planets | 190 | 1974 to 1962 (Mariner 2 at Venus) |
| Death ray | 171 | 2014 to 2003 (Zeus-HLONS against munitions) |
| Electric discharge weapon | 157 | 1993 to 1963 (electric prods used by Alabama troopers) |
| Closed-loop life support | 157 | 2014 to 1972 (BIOS-3) |
| Electronic lock and key | 150 | 1973 to 1949 (the Card-Key entrance lock) |
| Automated factory | 141 | 2001 to 1916 (an unattended power plant) |

Round 4 (the widened set) moved 886 claims and 617 claim points (2%). Its largest moves:

| Concept | Points | Milestone moved |
|---|---|---|
| Humanoid robot | +125 | 1939 Elektro to 1973 WABOT-1 (the definition asks for a robot that walks, talks and handles objects) |
| Implanted communication device | +86 | practical use added: the 1972 cochlear implant |
| Airship | −100 | practical use 1910 (DELAG) to 1906 (the Lebaudy *Patrie* for the French army) |
| Jetpack or flying suit | +62 | practical use added: the Manned Maneuvering Unit, 1984 |
| Element transmutation | −60 | 1941 to 1919 (Rutherford's nitrogen disintegration) |
| Closed-circuit video surveillance | −58 | practical use 1942 to 1927 (Theremin's Kremlin camera, year inferred) |
| Self-driving car | +54 | practical use added: Waymo's driverless service, 2020 |
| Structure of the galaxy | −53 | 1918 (Shapley) to 1785 (Herschel) |

Your review and the recheck moved 137 claims and added 232 claim points: brain transplant +135
(its new milestones), closed-circuit video surveillance +57 and the large public video screen
+32 (earlier milestones kept), geothermal power −32 (Boise, 1892).

The largest gain of round 1 is submarine life support, +78 points, from 1867 to 1958: the
definition requires staying sealed for long periods. A later milestone adds lead, so every
later move was checked against the definition; in round 4 they are in the review assist.

## 6. What is still doubtful

1. **Brain transplant, a judgment call from the recheck:** tier 2 dated it by Thompson's 1890
   graft of brain tissue between animals and the first fetal brain-tissue graft into a Parkinson's
   patient (Lund, 1987), reading the definition's "or part of one" literally. The novels mean
   moving a mind, so this is generous: it adds 135 claim points. The stricter answers are White's
   1970 monkey head transplant (the second reader's candidate) as a demonstration and no practical
   use. A keep_previous row on either kind removes it.
2. **The review assist's unsure rows were accepted.** Of the 55 changed answers the second reader
   was unsure of (`milestone_review_suggestions.md`), the review took tier 2's answer. Among them:
   personalized medicine (1907 crossmatched transfusion), self-spreading vaccine (Jenner's
   arm-to-arm transfer, 1796, under the "living carrier" alias), decontamination of poisoned
   ground (the 1917 mustard-gas clean-up), the USB flash drive as compact crystal storage, and the
   cochlear implant as an implanted transmitter. Any of them can still be reversed by a row in
   `milestone_review.jsonl`. The 75 confirmed answers it was unsure of
   ([`milestone_review_confirmed.md`](milestone_review_confirmed.md)) were not rechecked.
3. **Concepts with no milestone:** 31,442 claims (41%) are open because their concept has none. A
   third pass of the review assist
   ([`prompts/milestones_missing_check.md`](../../prompts/milestones_missing_check.md)) read the
   242 such concepts with 30 or more open claims: 200 never happened, 41 unsure, 1 happened (brain
   transplant, now researched) ([`no_milestone_candidates.md`](no_milestone_candidates.md)). The
   unsure ones are close relatives that may not fit (artificial gravity by Gemini 11's tethered
   spin, the Taser as a paralysis ray, habitable-zone exoplanets): a research queue, not
   milestones.
4. **Scored on a demonstration only:** 150 of the 590 deciding concepts have no practical use
   (marked † in the rankings, PLAN §14.5), among them invisibility (2010 metamaterial cloak),
   the crewed Moon landing and sleep learning. Tier 2 split these into discoveries (no use to
   find) and technologies whose use it searched for.
5. **Low confidence:** 152 of the 590 deciding milestones are low confidence and 40 rest on
   Wikipedia alone.
6. **Judgment calls accepted at checkpoint 3:**
   - the death ray dated by a laser that destroyed munitions rather than people;
   - the electric discharge weapon dated by the cattle prods Alabama troopers used in 1963;
   - increased human height dated by the start of a trend (1860);
   - aquaculture dated 1927, though the 1860s French oyster parks may be earlier.
7. **Data issues from the first scoring, still open:**
   - The dating pass dates two books 2009 and 2012 (H. P. Lovecraft's *Writings in the United
     Amateur, 1915–1922* and Harry Bates's *Astounding Stories* of January 1930).
   - Translations carry the translation's year (Lucian 1780), which understates their lead
     until DESIGN §1a's composition dates are built.
   - 56 books credit more than one name, and some of the names are illustrators or writers of
     introductions (Henri Théophile Hildibrand appears in the top predictions, beside Jules
     Verne). They need review rows before publishing.
8. **Points from every score above 0:** as DESIGN §8 has it. Counting only scores of 0.5 or more
   drops 17% of the points (4,455 of 26,090) and keeps 29 of the top 30 authors and 27 of the top
   30 books (`scoring.md`, sensitivity).

## 7. For tranche B

- **Select the checked set by its share of the author totals from the start,** not only by top
  entries: the first selection left half the author points unchecked. Re-select after re-judging
  and check the newcomers in the same pass.
- **Give tier 2 every earlier review decision.** The pilot's nine concepts went in without their
  review, which is how sleep learning's rejected 1942 study came back.
- **State the verdict rule in the tier-2 prompt:** seven batches marked a milestone "confirmed"
  while changing its year, and the check sent each back to be marked "replaced".
- **Send the review assist's objections back to tier 2 with the objection in hand** (the recheck
  round): 7 of the 10 confirmed answers it questioned changed.
- **Run the review assist before the human review.** At 0.9M tokens for 309 rows it is cheap,
  and it catches the literal readings (one word of a definition taken alone) that tier 2 makes
  when it hunts for the earliest event.
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
| Tier 2 and the earliest-event check | 5–10M | 20.1M (643 concepts, not 150–300, and a recheck) |
| Judging, two judges | 39–52M | 22.2M (17,201 pairs, not the ~42,000 estimated) |
| Third judge and re-judging after tier 2 | 4–8M | 9.0M (the third judge decided 98 current pairs) |
| Review assist | | 2.8M |
| **Tranche A** | **85–125M** | **117.4M** |
