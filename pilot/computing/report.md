# Pilot report: concepts, milestones, matching and judging for the computing claims

Run 2026-11-02, branch `pilot-computing`, following [`RUN.md`](RUN.md). Every output file
is JSON lines and passes `scripts/validate.py`. All scripts are in [`scripts/`](scripts/);
raw subagent outputs are in [`raw/`](raw/).

## Summary

The pipeline works end to end. Every one of the 2,656 claims has a match row, 2,116
claim–milestone pairs have a score, and all of it was done with 33 Sonnet subagents in
about half an hour of wall-clock time. Three findings matter more than the numbers:

1. **Milestones are the weak link.** The network policy blocked Wikidata, Wikipedia and
   every news archive, so no milestone has a verbatim source quote. Search summaries also
   gave wrong dates: the hand-check found a robot-mower milestone 32 years late, and the
   fingerprint, retina and 3D-display milestones are probably decades late too. Because
   points grow with lead time, **a late milestone goes straight to the top of the
   ranking.** Of the 20 best predictions, 8 owe their place partly to a milestone
   that is too late.
2. **The judge is reasonable but generous, and drifts between runs.** In the 30-judgment
   hand-check I would change 4, each by one step and each downward. Re-judging one batch
   gave the same score 54% of the time, and a score one step away 97% of the time. The
   second run never scored lower, and its mean was 0.12 higher. No pair scored 1.0.
3. **Matching on the description over-matches.** The matcher sees the quote and the
   extractor's one-line summary. When the quote is a thin fragment ("He put the figures
   into the computer."), the summary drives the match, and the judge, told to trust the
   quote, then scores it low. Of the judge's 141 zeros, about half (64) say the quotation
   does not carry the claim.

## Counts

| | |
|---|---|
| Claims | 2,656 (specificity 1: 7, 2: 363, 3: 1,139, 4: 1,040, 5: 107) |
| Concepts | 131 (101 expected to have come true, 30 "still waiting") |
| Concepts with at least one milestone | 99 |
| Milestones | 118 (60 first demonstration, 53 first practical use, 5 mass adoption) |
| Milestone sources | 148, all reference pages seen only as search summaries; 0 verbatim quotes |
| Matched claims | 2,419 (91%); 578 of them to two concepts |
| Unmatched claims | 237 (9%) |
| Claim–concept links | 2,997; 881 of them to a concept without a milestone |
| Claims whose concepts have no milestone at all | 649 (the "still waiting" set, e.g. knowledge downloads 83, lifelike androids 75, household robot servants 62, sentient machines 59) |
| Judged pairs | 2,116 = 1,424 by the judge + 692 scored 0 by rule (milestone not after publication) |
| Claims with at least one judged pair | 1,770 |

**Score distribution** (all 2,116 pairs; judge-only in brackets):

| Score | 0 | 0.25 | 0.5 | 0.75 | 1 |
|---|---|---|---|---|---|
| Pairs | 833 (141) | 636 | 540 | 107 | 0 |

618 claims have a best score of at least 0.5 and 105 at least 0.75. The mean best score
rises steadily with the extractor's specificity: 0.19 at specificity 2, 0.25 at 3, 0.30
at 4 and 0.35 at 5. That is a useful sanity check on both stages. The median lead time
among judged pairs is 23 years (range 1–132). The concepts that collect the most credit
are the spacecraft guidance computer (105 pairs), information retrieval, brain–computer
interfaces, humanoid and service robots, mind reading, machine-readable ID cards and VR.

## Best predictions

The best claims by `score × log2(1 + lead years)`, one row per claim. Every one scores
0.75, so lead time decides the order, and lead time depends on the milestone date. The
notes after the table matter as much as the table.

| # | Year | Quote | Concept | Milestone | Lead | Score | Points |
|---|---|---|---|---|---|---|---|
| 1 | 1948 | "They're robots, not men. That makes it harder, since they're undoubtedly connected direct to Roger's desk and will give an alarm at the first hint of abnormal performance." | Robot police and security guards | 2015: Knightscope shipped its first K5 autonomous security patrol robot to a customer (first practical use) | 67 | 0.75 | 4.57 |
| 2 | 1948 | "[…] has read your mind and it has retranslated these readings into visual images. We are now going to watch the shapes of your own thoughts." | Mind-reading machine | 2011: Nishimoto, Gallant et al. (UC Berkeley) reconstructed approximate movie clips a subject had watched from fMRI … (first demonstration) | 63 | 0.75 | 4.50 |
| 3 | 1939 | "the tank was seven hundred feet in diameter and eighty feet thick in the middle—over seventeen million cubic feet of space in which more than two million tiny lights crawled hither and thither in hopeless confusion." | Three-dimensional holographic display | 2001: Actuality Systems' Perspecta, a swept-volume display showing a 3D image viewable from all sides, appeared … (first demonstration) | 62 | 0.75 | 4.48 |
| 4 | 1955 | "the only hotel staffed entirely with robot servants" | Service robot for the public | 2014-08: Savioke's Relay delivery robot went into continuous service at the Aloft Cupertino hotel, carrying items to … (first practical use) | 59 | 0.75 | 4.43 |
| 5 | 1960 | "A robot redcap came gliding along. Inevitably, it was gilded, and looked absolutely brand new." | Service robot for the public | 2014-08: Savioke's Relay delivery robot went into continuous service at the Aloft Cupertino hotel, carrying items to … (first practical use) | 54 | 0.75 | 4.34 |
| 6 | 1954 | "Nor had he guessed that Revanche would then employ Bioid's competitor to fashion an electronic proxy of himself." | Robot copy of a particular person | 2006: Hiroshi Ishiguro and Kokoro unveiled Geminoid HI-1, a teleoperated android modelled on Ishiguro himself. It … (first demonstration) | 52 | 0.75 | 4.30 |
| 7 | 1954 | "Every Robot in North and South America has its own particular wavelength, although the master intelligence is in tune with all of them." | Central computer directing many robots | 2006: Staples deployed Kiva Systems' fleet of warehouse drive-unit robots, coordinated by control software, at its … (first practical use) | 52 | 0.75 | 4.30 |
| 8 | 1955 | "Clifford Ainsley. The prototype, that is, in the flesh and not a roboid. He nodded at the body on the floor. "Ainsley the Second. Strictly a lab job."" | Robot copy of a particular person | 2006: Hiroshi Ishiguro and Kokoro unveiled Geminoid HI-1, a teleoperated android modelled on Ishiguro himself. It … (first demonstration) | 51 | 0.75 | 4.28 |
| 9 | 1953 | "She pressed it and the slab, at first gay orange, turned pale blue; on it appeared three lines of squiggly characters" | Electronic paper and rewritable display surface | 2004-04: Sony's Librie in Japan was the first consumer product to use an E Ink electronic paper module. (first practical use) | 51 | 0.75 | 4.28 |
| 10 | 1950 | "They brought a three-dimensional map out of the air, I guess; I couldn't tell. It hung in the air like it was glued to nothingness." | Three-dimensional holographic display | 2001: Actuality Systems' Perspecta, a swept-volume display showing a 3D image viewable from all sides, appeared … (first demonstration) | 51 | 0.75 | 4.28 |
| 11 | 1957 | "George Prime had remote controls, as well as a completely recorded neurological analogue of his boss, who was me." | Robot copy of a particular person | 2006: Hiroshi Ishiguro and Kokoro unveiled Geminoid HI-1, a teleoperated android modelled on Ishiguro himself. It … (first demonstration) | 49 | 0.75 | 4.23 |
| 12 | 1962 | "Everything that's happening around here is being fed back to them at the moment," he said. "When they heard about our invite to Lyad's dinner party, and who was to be present, they came up with a honey." | Computer crime detection and predictive policing | 2011: The LAPD deployed PredPol, a UCLA-developed algorithm for predicting where crime will happen, in its Foothill … (first practical use) | 49 | 0.75 | 4.23 |
| 13 | 1950 | "As she was leaving, Jerry came into the pharmacy, recorded his thumbprint and took a box of aspirin from the machine." | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the earliest automated … (first practical use) | 49 | 0.75 | 4.23 |
| 14 | 1957 | "The waiters—remote-control humanoids guided by the vast robot brain in the basement—were dressed in the fluffy, bright, fluorescent clothing of a style that had been worn two centuries before" | Central computer directing many robots | 2006: Staples deployed Kiva Systems' fleet of warehouse drive-unit robots, coordinated by control software, at its … (first practical use) | 49 | 0.75 | 4.23 |
| 15 | 1958 | "Of course! Radio! I'll bet anything they're automatically controlled by the camp computer. That's where their brain is!" | Central computer directing many robots | 2006: Staples deployed Kiva Systems' fleet of warehouse drive-unit robots, coordinated by control software, at its … (first practical use) | 48 | 0.75 | 4.21 |
| 16 | 1952 | "The whorls at the tips of my fingers set off a light-switch mechanism within the stone," she explained. "It's better than any key." | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the earliest automated … (first practical use) | 47 | 0.75 | 4.19 |
| 17 | 1948 | "Kinnison dashed up to an apparently blank wall, turned his back upon four commissioned officers holding cocked forty-fives at the ready, and fitted his right eye into a cup. Unlike fingerprints, retinal patterns cannot …" | Retina and iris recognition | 1995: The FBI's iris recognition overview says the first commercial iris recognition products became available in … (first practical use) | 47 | 0.75 | 4.19 |
| 18 | 1953 | "The Identifier, beyond the door, began to hum. That meant somebody was putting his hand to the opaque screen, and if the scanner recognized the fingerprints the door would open." | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the earliest automated … (first practical use) | 46 | 0.75 | 4.17 |
| 19 | 1955 | "In the center of the cabin an image flickered, swarming flecks of light and shadow that filled out a three-dimensional form, complete and detailed." | Three-dimensional holographic display | 2001: Actuality Systems' Perspecta, a swept-volume display showing a 3D image viewable from all sides, appeared … (first demonstration) | 46 | 0.75 | 4.17 |
| 20 | 1954 | "A hidden device checked the pattern and whorls of the militiaman's fingerprints. The effect was the same as the Open Sesame of the Arabian Nights, for a great slab-like section of the escarpment rolled ponderously aside" | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the earliest automated … (first practical use) | 45 | 0.75 | 4.14 |

Notes on the list:

- **Late milestones push claims up.** Rows 13, 16, 18 and 20 are fingerprint locks
  scored against the FBI's 1999 IAFIS database, a different kind of system. Electronic
  fingerprint and hand-geometry access control is decades older, but the research agent
  could not confirm a date. The 3D-display rows (3, 10, 19) use a 2001 swept-volume
  display, and volumetric displays existed well before that. Row 17 (a retina scanner)
  uses a 1995 iris product; commercial retina scanners are older. All of these are
  search-summary dates that nobody checked against a primary source.
- **Some scores are generous.** Row 4 is the whole quote "the only hotel staffed entirely
  with robot servants", and row 12's quote says nothing about predicting crime; the
  match comes from the extractor's summary. I would give both 0.25–0.5.
- **The rows are unique by claim, not by book.** Rows 6, 8 and 11 and rows 14 and 15 may
  come from the same book or series. The pilot data has passage ids but not book ids, so
  the per-book de-duplication in DESIGN §8 could not be applied.
- One milestone was corrected after the hand-check. The robot vacuum and mower concept
  first carried the 2001 Trilobite vacuum. The MowBot robotic mower was sold in 1969, so
  the 7 affected pairs were re-judged against 1969. A 1931 robot-mower claim was ranked
  first before the correction and now falls below the top 20.

## Quality: hand-check of 30 random judgments

These 30 pairs were sampled with a fixed seed (`scripts/stats.py sample`) from the 1,424
pairs the judge scored. For each one I read the quote, the summary and the milestone and
scored it again under the same rubric. My notes are in `raw/handcheck.jsonl`.

| Pair | Year | Concept | Judge | Mine | Note |
|---|---|---|---|---|---|
| q1680 | 1946 | `spacecraft-guidance-computer` | 0.5 | **0.25** | Quote is only "He put the figures into the computer"; the navigation detail is in the summary, not the words. |
| q0220 | 1947 | `brain-computer-interface` | 0.5 | 0.5 | Agree: a machine searched by thought. |
| q1167 | 1941 | `military-strategy-computer` | 0.25 | 0.25 | Agree (0 also defensible). |
| q1882 | 1955 | `speech-to-text-dictation` | 0.25 | 0.25 | Agree: name only. |
| q1920 | 1948 | `supercomputer-scientific-calculation` | 0 | 0 | Agree. |
| q0479 | 1962 | `computerized-economic-planning` | 0.5 | 0.5 | Agree, generous. |
| q0365 | 1957 | `computer-network` | 0.5 | 0.5 | Agree; really networked e-voting, matched to computer-network. |
| q1263 | 1962 | `mind-reading-machine` | 0.25 | 0.25 | Agree. |
| q0106 | 1953 | `automatic-door` | 0.25 | 0.25 | Agree; matcher put a fingerprint lock under automatic-door, the judge caught it. |
| q1969 | 1945 | `teleoperated-robot` | 0 | 0 | Agree; quote does not carry the claim. |
| q0693 | 1939 | `holographic-3d-display` | 0.75 | **0.5** | Crawling lights in a tank is a volumetric display only in function; mechanism absent. Also the 2001 milestone is late (volumetric displays existed decades earlier). |
| q1243 | 1957 | `mind-reading-machine` | 0.25 | 0.25 | Agree. |
| q1525 | 1960 | `robotic-space-probe` | 0.25 | 0.25 | Agree; matcher error (planet-selecting computer is not a probe). |
| q1783 | 1962 | `speaker-recognition` | 0.25 | 0.25 | Agree. |
| q1422 | 1955 | `robot-manufacturing-industry` | 0.5 | 0.5 | Agree. |
| q0633 | 1905 | `fingerprint-recognition` | 0.25 | 0.25 | Agree on score; but the 1999 IAFIS milestone gives it 94 years of lead. |
| q1745 | 1959 | `spacecraft-guidance-computer` | 0 | 0 | Agree; quote does not carry the claim. |
| q0613 | 1963 | `electronic-voting` | 0.5 | 0.5 | Agree. |
| q1630 | 1942 | `social-forecasting-computer` | 0.25 | 0.25 | Agree. |
| q1248 | 1957 | `mind-reading-machine` | 0.25 | 0.25 | Agree. |
| q1677 | 1942 | `spacecraft-guidance-computer` | 0.25 | 0.25 | Agree. |
| q1363 | 1958 | `question-answering-computer` | 0.25 | 0.25 | Agree. |
| q1733 | 1957 | `spacecraft-guidance-computer` | 0.5 | 0.5 | Agree. |
| q1012 | 1948 | `machine-readable-id-card` | 0.75 | 0.75 | Agree. |
| q0647 | 1960 | `fingerprint-recognition` | 0.75 | 0.75 | Agree on score; milestone (1999 FBI database) is the wrong kind of event for a fingerprint lock. |
| q1587 | 1963 | `service-robot` | 0.5 | **0.25** | Quote is only "Take us to Miss Horton's Unit at once."; escort function comes from the summary. |
| q2068 | 1945 | `virtual-reality` | 0.25 | 0.25 | Agree. |
| q1495 | 1956 | `robot-supervisor-hierarchy` | 0.25 | 0.25 | Agree. |
| q0198 | 1957 | `biological-computer` | 0.25 | **0** | A human operating sluice gates in binary is not a biological computer in the DNA-computing sense. |
| q1889 | 1957 | `speech-to-text-dictation` | 0.25 | 0.25 | Agree. |

**I would change 4 of 30 (13%)**, all by one step and all downward: q1680, q0693, q1587
and q0198. In two of them the judge scored the summary instead of the quote. Another 3
scores are right, but the milestone gives the claim too much lead time (q0693, q0633,
q0647). In 3 more the matcher sent the claim to a nearby but wrong concept. For two of them
(q0106, q1525) the judge saw the mismatch and scored low; the third (q0365, a networked
voting machine filed under computer network) is still a fair 0.5.

**Consistency.** Judge batch 05 had to be re-run (see Problems). Re-judging its 120 pairs
with the same prompt gave the same score in 65 cases (54%), a score 0.25 higher in 51
and a score 0.5 higher in 4. No score went down. Single-run scores therefore carry about
±0.25 of noise, and the run-to-run bias can be as large as the rubric's step size.

## Problems found

1. **No access to the evidence sources.** The network policy denied query.wikidata.org,
   www.wikidata.org, en.wikipedia.org and chroniclingamerica.loc.gov (403 at the proxy),
   and WebFetch failed DNS for every host the agents tried. Only WebSearch worked.
   Consequences:
   - No Wikidata seeding: the concept list comes entirely from the claims.
   - Every `wikidata` field is null; no search result showed a QID.
   - No source has a verbatim quote: all 148 are `kind: "search_summary"` with
     `quote: ""`. The rule against invented quotes held.
   - No contemporary sources, only reference pages.
2. **Milestone research was shallow and sometimes wrong.** Six agents covered 131
   concepts with one or two searches each. Most concepts got only one milestone, and
   only 5 got a mass-adoption date. Several agents picked a later, better-documented
   event over the earliest one that fits; the MowBot correction shows the size of the
   error. Some agents also stretched a definition to find a milestone: a 2011 fMRI
   movie reconstruction stands in for a "mind-reading machine", a 1927 sleep-learning
   gadget that did not work counts as a demonstration, and a teleoperated Geminoid
   stands in for an android copy of a person. Others refused reasonable ones, so
   mass surveillance databases, self-repairing machines and space-station automation
   have no milestone.
3. **One judge batch was boilerplate.** Batch 05 (humanoid robots, industrial robots,
   information retrieval) returned only 15 distinct rationales for 120 pairs, and its
   mean score (0.26) was the lowest of any batch. I added a sentence to the judge prompt
   ("never reuse a template sentence") and re-ran it with one extra subagent. The new
   run gave 127 distinct rationales. The old scores are kept in `raw/judge_05.jsonl`.
4. **Two concept scopes were too narrow or wrong.**
   - `electronic-digital-computer` collected vague "giant brain" claims. These were then
     judged against ENIAC as a calculator, so they mostly score 0.25.
   - `internet-global-information-network` and `electronic-mail` were never matched; the
     matcher used `computer-network` instead.
   - The concept proposals also suggested 8 themes, such as "human intuition beats the
     machine" and "machines cannot handle the unexpected". These are claims about
     machines' limits, not technologies with a date, so I left them out. Their claims
     are among the 237 unmatched.
5. **The judge prompt lacked a rule for summary versus quote.** judge_v0 gives the judge
   both. I added two clarifications: the quotation wins when they disagree, and a claim
   is compared with the milestone, not with the concept's name. The judges applied
   both, so claims that rest only on the summary score 0 or 0.25.
6. **The milestone-before-publication rule was applied in code.** 692 pairs, a third of
   all pairs, had a milestone in or before the year of publication. They score 0 by rule
   (`judged_by: "rule"`) without a model call. This saves a third of the judge's
   workload and gives the same result DESIGN §8 does (L ≤ 0 earns no points).
7. **Data quirks.**
   - One matching agent emitted a row with a wrong claim id and the reason
     "placeholder"; I matched that claim by hand (`raw/matches_fixes.jsonl`).
   - One judgment came back with no rationale.
   - There are no book or author ids, so no per-book de-duplication.
8. **Token log caveat.** `usage.tsv` logs each subagent's final context size, which is
   what the harness reports. The full token use, read from the transcripts, is larger;
   both figures are under Cost below.

## Cost and time

| Step | Subagents | Final context (tokens, as logged) | Agent time (s) |
|---|---|---|---|
| 1 Concepts | 2 | 240,469 | 283 |
| 2 Milestones | 6 | 558,499 | 714 |
| 3 Matching | 12 | 1,213,102 | 1,459 |
| 4 Judging (incl. 1 re-run) | 13 | 1,157,795 | 1,177 |
| **Total** | **33 of 40** | **3,169,865** | **3,633** |

Full use from the 33 transcripts: 500,300 output tokens, 1,821,143 cache-write tokens,
12,520,868 cache-read tokens and 456 uncached input tokens. The input is mostly cache
reads because each agent re-reads its growing context on every turn. Wall-clock time was
about 30 minutes (17:40–18:10 UTC), since most agents ran in parallel. The
orchestration (merging, checking, the hand-check and this report) ran in the main
session and is not in these figures.

Scope was not cut: every claim was matched and every eligible pair judged, at every
specificity level.

## Recommendations for the full run (92K claims)

**Concept seeding.**
- Allow query.wikidata.org and en.wikipedia.org (and Chronicling America and the NYT
  archive for contemporary sources) in the environment's network settings before the
  full run. Without them the evidence step cannot meet DESIGN §6.
- Seed from Wikidata *and* from the claims, as here. Two agents reading 1,328
  descriptions each proposed 107 and 112 concepts, which overlapped heavily and merged
  to 131. For the full run, propose concepts per domain on a sample of about 3,000
  descriptions per domain, then merge by hand or with one Opus pass. Expect 1,000–1,500
  concepts.
- Leave out "theme" concepts (machine limits, skepticism) and say so in the matcher
  prompt, so that their claims are unmatched on purpose.

**Milestones.**
- Give each research agent 10–15 concepts, not 22, and require a search for "first" and
  "earliest" for each milestone kind.
- Add a second, adversarial pass that asks "is there an earlier event that fits this
  definition?" for every milestone with more than 40 years of lead time to any claim.
  Those are the milestones that decide the ranking.
- Have a human review the 200 most-used milestones. That would have caught the MowBot,
  fingerprint and 3D-display problems.
- Store a confidence for each milestone. Consider capping the lead time for milestones
  with only search-summary sources until a real source is attached.

**Matching.**
- Batches of 222 claims plus the full concept list worked well: each agent produced
  exactly one row per claim, apart from one wrong id. Keep batches at about 200–250.
- Either drop the extractor's summary from the matcher's input, or tell the matcher to
  match only what the quotation itself says. Most 0 scores trace back to summary-driven
  matches.

**Judging.**
- Batches of 120 pairs worked. Sorting pairs by concept made the judge consistent within
  a concept, but it also made one judge settle into a template. Mix concepts in each
  batch, or keep 120 and add the no-template rule.
- Add an automated check that rejects a batch with fewer than about 80% distinct
  rationales.
- Score 1.0 was never given. Either the anchor is too strict for fiction (which rarely
  describes "how people use it"), or the 0.75/1.0 line needs a worked example in the
  prompt.

**Does the judge need Opus?** Not for most pairs. Sonnet's judgments were sensible and
the errors I found were one step, mostly generosity. The ranking, though, is decided by
a few hundred pairs scored 0.75 with a long lead time. I recommend Sonnet for every
pair, then a second judge on every pair that could reach the top of the ranking (score
≥ 0.5 and lead ≥ 30 years: 271 pairs here, roughly 10K in the full run), using Opus
if the gold-set test supports it. Average the two judgments and flag disagreements.
That buys the precision where it counts at a small fraction of an all-Opus run.
