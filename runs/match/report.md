# Tranche A: the full run's report

Run 2026-11-03 to 2026-11-18 under [`PLAN.md`](PLAN.md), on a local machine with Claude Code
Sonnet subagents and no API calls. The full rankings and resolutions are in
[`scoring.md`](scoring.md); this report says how they were made, what changed when the deciding
milestones were checked, and what is still doubtful. It is checkpoint 4 (PLAN §13), a stop for
your review. This version follows the later tier-2 rounds of 2026-11-18 (section 5).

## Summary

- **77,436 technology and science claims from 3,224 books** were matched against a registry of
  1,756 concepts and scored against 2,046 verified milestones for 1,103 concepts. 15,719 claims
  are realized (20.3%), 16,447 came after their milestone (not a prediction), 42,460 are open
  (31,493 with no milestone, 6,795 with no concept, 3,897 too vague, 275 other), 2,558 are
  untestable and 252 failed (170 missed a stated deadline, 82 denials were contradicted).
- **The leaders:** E. E. Smith 424 points, H. G. Wells 356, Murray Leinster 352, Jules Verne 345,
  George O. Smith 319. The top book is *Limanora* (Godfrey Sweven, 1903) with 231, then *Across
  the Zodiac* (Percy Greg, 1880) and *Ralph 124C 41+* (Hugo Gernsback, 1911). The top single
  prediction is *The Moon Hoax* (1835) on rocks thrown from the Moon to the Earth (lunar
  meteorites, 1983).
- **Every concept that decides the rankings has now been checked by tier 2.** The first check
  covered the 165 concepts that carry a top entry. A recount showed those carried only half the
  author points, so the selection was widened to every concept that adds 5 or more points to the
  author totals: 643 concepts in four rounds, 1,108 verdicts. The scoring milestone changed for
  356 of them (169 earlier, 71 later, 115 in month or kind, 1 removed), and 522 now have a source
  from the time of the event.
- **The rankings held.** Against the first scoring, the top 9 authors keep their places, 29 of
  the top 30 stay (John Jacob Astor leaves, Alfred Coppel enters), and 27 of the top 30 books
  stay. Points fall 7% (27,931 to 25,971), mostly because 948 realized claims now come after an
  earlier milestone.
- **The judges agree closely:** of the 16,335 current pairs two judges scored, 69% got the same
  score, 30% were one step apart and about 1% two or more (decided by a third judge). Each later
  round agrees the same way (round 4: 67%, 32%, 0.8%).
- **Cost:** 910 subagents, 116.9M tokens and 71 agent-hours, inside the plan's 85–125M
  estimate. The later tier-2 rounds, their re-judging and the review assist took 22.1M tokens on
  2026-11-18, 66% to 77% of the week.
- **For your review** (section 6): an independent second reading of the milestones the later
  tier-2 rounds replaced or added suggests keeping the earlier one for 18 and is unsure of 55
  ([`milestone_review_suggestions.md`](milestone_review_suggestions.md)); a reading of the ones
  they confirmed names 10 to research again, and one of the concepts with no milestone looks like
  a miss. None is applied.

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
| Judging, rounds 1–2 (§7) | 207 | 26.5M | 9.1 | 17,201 pairs, then 3,166 new ones |
| Judging, rounds 3–4 (§7) | 38 | 4.5M | 1.4 | 3,308 new pairs |
| Review assist (section 6) | 40 | 2.8M | 0.4 | second readings of 834 milestones and 242 concepts with none |
| **Total** | **910** | **116.9M** | **71.2** | |

Every batch ran as a background subagent with its own input and output file, so the run was
stopped and restarted many times without losing work. Each stage pins its prompt by sha256, and
every output passed the checks in code or was redone; the few early matching batches accepted with
notes are in [`rejected_batches.tsv`](rejected_batches.tsv). Every log is in
[`usage.tsv`](usage.tsv). The last rounds ran 20 agents at a time, the most a session allows.

- **Checkpoint 1, the registry:** approved 2026-11-03; the gap concepts were reviewed
  2026-11-05 ([`gap_review.md`](gap_review.md), [`concept_review.jsonl`](concept_review.jsonl)).
- **Checkpoint 2, calibration:** 2026-11-03, on the first 20 matching batches ([`calibration.txt`](calibration.txt)).
- **Checkpoint 3, the deciding milestones:** the first round decided 2026-11-18 ([`deciding_milestones.md`](deciding_milestones.md),
  [`milestone_review.jsonl`](milestone_review.jsonl)); the later rounds wait for your review.
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
  concepts that decide the rankings now, 117 milestones are high confidence, 313 medium and 158
  low; 483 have a contemporary source, 38 rest on Wikipedia alone and 149 are demonstrations only.
- **Checkpoint 3** overruled two answers of the first round and kept the earlier milestone:
  - **Sleep learning:** stays at 2019. Tier 2 brought back LeShan's 1942 nail-biting study, which
    the pilot's review had rejected; tier 2 was never given that review. Later rounds were given
    every review decision.
  - **Wearable wings:** keeps its 1935 practical use (Clem Sohn's exhibition flights) rather than
    1999, when the wingsuits went on sale.
- **The final milestones** ([`milestones.jsonl`](milestones.jsonl)): 2,046 rows for 1,103
  concepts (1,051 demonstrations, 831 practical uses and 164 mass adoptions). The candidates the
  researchers rejected and what they searched are in [`milestone_notes.jsonl`](milestone_notes.jsonl).

## 3. Judging

Two judges score every pair of a claim and a concept whose milestone came after the claim, each
in a different fixed-seed shuffle, in batches of 200
([`prompts/judge.md`](../../prompts/judge.md), `judge_v1`). The score is their mean, or the
median of three when they are two or more steps apart; a `will_not` pair has one judge.

- **Round 1** (2026-11-15) judged 17,201 pairs, and every batch passed the checks the first time.
- **Rounds 2–4** (2026-11-18) are the pairs whose milestone tier 2 changed. Their id hashes the
  claim, the concept and the milestone's kind and date, so a changed milestone is a new pair. A
  new pair copies the judgments of its earlier pair when tier 2 confirmed the same event in the
  same kind and year and only the date got more precise.

  | Round | New pairs | Copied | Judged by both | Same | One step | Further |
  |---|---|---|---|---|---|---|
  | 2 | 4,019 | 853 | 3,166 | 71% | 28% | 0.4% |
  | 3 | 193 | 132 | 61 | | | 1 pair |
  | 4 | 4,760 | 1,513 | 3,247 | 67% | 32% | 0.8% |

- **Three replacements of round 1 kept their date** (cutting beam 1970, solar-thermal propulsion
  1999, synthetic food 1939), so their 173 pairs keep judgments made against the earlier event.
  Each new event is the same kind of thing in the same year, so I left them.
- **Agreement and scores** ([`judging.md`](judging.md)): on the 16,335 current pairs judged twice,
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
| 1 | E. E. Smith | 423.6 | 161 | 20 | 1 |
| 2 | H. G. Wells | 356.1 | 127 | 27 | 2 |
| 3 | Murray Leinster | 352.1 | 149 | 58 | 3 |
| 4 | Jules Verne | 345.3 | 108 | 16 | 4 |
| 5 | George O. Smith | 319.2 | 131 | 57 | 5 |
| 6 | Ray Cummings | 315.4 | 127 | 36 | 6 |
| 7 | John W. Campbell Jr | 287.6 | 116 | 12 | 7 |
| 8 | Edmond Hamilton | 282.4 | 104 | 34 | 8 |
| 9 | Randall Garrett | 259.5 | 111 | 78 | 9 |
| 10 | George Chetwynd Griffith | 257.4 | 92 | 6 | 11 |
| 11 | Raymond Z. Gallun | 254.8 | 99 | 17 | 12 |
| 12 | Godfrey Sweven | 250.3 | 89 | 2 | 10 |
| 13 | Fritz Leiber | 226.8 | 94 | 29 | 13 |
| 14 | H. Beam Piper | 217.2 | 100 | 32 | 14 |
| 15 | F. L. Wallace | 201.7 | 87 | 18 | 16 |

| # | Book | Author | Points | Concepts | First scoring |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 230.6 | 82 | 1 |
| 2 | *Across the Zodiac* (1880) | Percy Greg | 147.0 | 47 | 3 |
| 3 | *Ralph 124C 41+* (1911) | Hugo Gernsback | 142.7 | 45 | 2 |
| 4 | *Spacehounds of IPC* (1931) | E. E. Smith | 115.9 | 42 | 7 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 114.0 | 43 | 6 |
| 6 | *The Moon-Voyage* (1872) | Jules Verne | 112.8 | 35 | 11 |
| 7 | *Skylark Three* (1930) | E. E. Smith | 110.9 | 38 | 5 |
| 8 | *All Around the Moon* (1870) | Jules Verne | 110.5 | 32 | 9 |
| 9 | *A Journey in Other Worlds* (1894) | John Jacob Astor | 108.5 | 41 | 4 |
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
| realized | 16,420 | 16,161 | 15,719 |
| not a prediction | 15,735 | 15,994 | 16,447 |
| open: not matched (all judged pairs score 0) | 278 | 288 | 269 |
| failed: contradicted negative | 91 | 81 | 82 |

Since the first scoring, 1,310 claims changed resolution: 948 from realized to not a prediction
(their concept's milestone moved before them), 258 the other way, and the rest between open,
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

The largest gain of round 1 is submarine life support, +78 points, from 1867 to 1958: the
definition requires staying sealed for long periods. A later milestone adds lead, so every
later move was checked against the definition; in round 4 they are in the review assist.

## 6. What is still doubtful

1. **Round 4's answers have not had your review.** Round 1's went through checkpoint 3; rounds
   2–4 have not. The review assist ([`pipeline/review_assist.py`](../../pipeline/review_assist.py),
   [`prompts/milestones_review_assist.md`](../../prompts/milestones_review_assist.md)) gave a
   second reader, with no web access, every demonstration or practical use that round 4
   replaced, added or removed, beside the one before it and the concept's definition:
   241 accept, 16 keep the earlier milestone, 52 unsure
   ([`milestone_review_suggestions.md`](milestone_review_suggestions.md); with rounds 2–3, 330
   rows: 257 accept, 18 keep_previous, 55 unsure). Round 4's 16 include:
   - central and district heating dated by the Roman hypocaust (−80), which heats one building,
     not many through pipes; this would turn every claim on it into "not a prediction";
   - the large public video screen dated by an 1872 stereopticon projecting election returns;
   - tuberculosis cure moved later, from 1944–45 streptomycin trials to an inferred 1946;
   - closed-circuit video surveillance in 1927 on an inferred year;
   - a practical use added for a natural impact (planet collision), which has none (keep_previous
     on a kind tier 2 added removes it);
   - transatlantic flight's practical use moved from the 1928 Graf Zeppelin passengers to the
     1919 Alcock and Brown mail bag.

   Among the unsure: personalized medicine (1907 crossmatched transfusion), self-spreading
   vaccine (Jenner's arm-to-arm transfer of 1796, under the "living carrier" alias),
   decontamination of poisoned ground (1917 mustard-gas clean-up), the USB flash drive as compact
   crystal storage, and the cochlear implant as an implanted transmitter. A decision goes in
   `milestone_review.jsonl` as keep_previous or accept, and `verify` applies it.
2. **Answers tier 2 confirmed:** a second pass of the review assist
   ([`prompts/milestones_review_confirmed.md`](../../prompts/milestones_review_confirmed.md)) read
   the 504 milestones rounds 2–4 confirmed: 419 accept, 6 earlier_exists, 4 does_not_fit, 75
   unsure ([`milestone_review_confirmed.md`](milestone_review_confirmed.md)). The earlier events
   it names: electrification's 1898 practical use (Pearl Street's customers ran motors from 1882),
   geothermal power (Boise district heating 1892), the anti-satellite weapon (US Program 505 and
   437, 1963–64), the seaplane (the Greek Navy's sortie of January 1913) and crash protection
   (aircraft seat belts from 1910). The misfits: Starfish Prime as a machinery-disabling ray, a 1937
   Meccano model as the industrial robot, Salyut 1 as a repurposed structure, and a couch test as
   astronaut training. These need sourced research before a decision; keep_previous can't fix a
   confirmed milestone.
3. **Concepts with no milestone:** 31,493 claims (41%) are open because their concept has none. A
   third pass ([`prompts/milestones_missing_check.md`](../../prompts/milestones_missing_check.md))
   read the 242 such concepts with 30 or more open claims: 200 never happened, 41 unsure, 1
   happened (brain transplant: Robert White's monkey head transplant, 1970)
   ([`no_milestone_candidates.md`](no_milestone_candidates.md)). The unsure ones are close
   relatives that may not fit (artificial gravity by Gemini 11's tethered spin, the Taser as a
   paralysis ray, habitable-zone exoplanets); they are a research queue, not milestones.
4. **Scored on a demonstration only:** 149 of the 588 deciding concepts have no practical use
   (marked † in the rankings, PLAN §14.5), among them invisibility (2010 metamaterial cloak),
   the crewed Moon landing and sleep learning. Tier 2 split these into discoveries (no use to
   find) and technologies whose use it searched for.
5. **Low confidence:** 158 of the 588 deciding milestones are low confidence and 38 rest on
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
   drops 17% of the points (4,436 of 25,971) and keeps 29 of the top 30 authors and 27 of the top
   30 books (`scoring.md`, sensitivity).

## 7. For tranche B

- **Select the checked set by its share of the author totals from the start,** not only by top
  entries: the first selection left half the author points unchecked. Re-select after re-judging
  and check the newcomers in the same pass.
- **Give tier 2 every earlier review decision.** The pilot's nine concepts went in without their
  review, which is how sleep learning's rejected 1942 study came back.
- **State the verdict rule in the tier-2 prompt:** seven batches marked a milestone "confirmed"
  while changing its year, and the check sent each back to be marked "replaced".
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
| Tier 2 and the earliest-event check | 5–10M | 19.7M (643 concepts, not 150–300) |
| Judging, two judges | 39–52M | 22.2M (17,201 pairs, not the ~42,000 estimated) |
| Third judge and re-judging after tier 2 | 4–8M | 8.8M (the third judge decided 98 current pairs) |
| Review assist | | 2.8M |
| **Tranche A** | **85–125M** | **116.9M** |
