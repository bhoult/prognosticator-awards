# Pilot, third pass: the milestones that decide the ranking, and a second judge

Run 2026-11-03, branch `pilot-computing`, following [`RUN3.md`](RUN3.md). Steps 1–3 ran in a
Claude Code cloud session (about 00:15–02:12 UTC) and stopped there when its credit ran out; steps 4–8
ran on a local machine (about 02:15–03:00 and 12:40–13:50 UTC) with local Sonnet subagents. The first-
and second-pass files are unchanged; every new output has a `3` in its name and passes
`scripts/validate3.py`. Scripts are in [`scripts/`](scripts/), raw agent output in [`raw/`](raw/).

## Summary

- **Sources from the time of the event, at last.** Of the 55 demonstration and practical-use
  milestones of the 33 target concepts, 46 now have a source published within two years of the
  event; in the second pass 1 of 47 did. Most are scanned magazines, technical reports and books
  on archive.org (61 of the 113 verified sources); Wikipedia supplies 40. Every quote was fetched
  again and checked in code.
- **The deciding milestones moved, mostly earlier.** For the 33 target concepts the ranking's
  milestone moved earlier for 10, later for 3, and kept its year for 15. Four concepts have a
  milestone again (service robot 1985, speaker recognition 1974, consumer analytics 1961, sleep
  learning 2019); computerized personnel selection still has none. The largest moves: robot
  guards 2015 → 1986, central robot control 2007 → 1974, speech recognition 1984 → 1972,
  machine-readable ID 1968 → 1961, machine learning 1951 → 1929, thought-to-text 2020 → 2006;
  later: the holographic display 1972 → 2009 (a static hologram is not a display).
- **Eight decisions were taken in review after the research**, each with its reason in
  [`raw/review3.jsonl`](raw/review3.jsonl), which the merge and the check step apply (section 3.2).
- **The second judge shows that the top of the ranking was inflated.** On the top 100 it scored
  lower than the first judge 56 times and higher once; on 50 random pairs it was 11 lower and 7
  higher. The first judge is not generous across the board: the top is chosen from the highest of
  noisy scores, so it collects the generous ones. Combining (lower of two; median of three) lowered
  78 of the 148 pairs judged twice. Only one pair still had a 1.0 after re-judging, and the second
  judge lowered it to 0.75.
- **The new ranking is flatter and better founded.** The top entry has 4.23 points (second pass:
  6.85). Four of the second pass's top 20 are still in it. All of the top 20 and 79 of the top 100
  have two judges.
- **Cost:** 17 subagents. The cloud part (9 agents, two lost to container restarts) used about
  $20 of the cloud credit; the local part used 8 agents and 0.75M tokens of plan usage.

## 1. How the run went

**In the cloud (steps 1–3).** The network check and fetch helpers went as planned (section 2).
The research did not: the container restarted twice and killed the research agents. The first
three agents wrote nothing before the first restart; of the three retries, batch 1 again wrote
nothing, batches 2 and 3 had saved 10 and 9 of their 11 concepts. The unfinished concepts were
split into two more batches, stopped early when the credit ran low, and a ninth agent finished the
last 8 concepts. The session then stopped with $3 of credit left and 9 of its 12 subagents spent
([`RUN3_STATUS.md`](RUN3_STATUS.md)).

**Locally (steps 4–8).** The rest ran on a local machine, with the user's go-ahead for up to 20
more subagents; 8 were used. What differs from `RUN3.md`:

1. **Network.** Local agents had an open network; they were told to fetch and check pages only
   through `scripts/page_text3.py` and `scripts/ia_search3.py` (descriptive User-Agent), and to
   use WebSearch only to find pages.
2. **Two new source forms in `page_text3.py`.** PubMed Central articles are read through NCBI's
   E-utilities, because the article pages answered this machine with a captcha. Lending-library
   books on archive.org, whose text answers 401, are cited through archive.org's full-text search
   restricted to the one item (`user_query = "<phrase>" AND identifier:<id>`): the quote must lie in
   a returned snippet, and the date is the item's metadata date.
3. **A fix in the merge and the check step.** A source date written `19520610` was not read as
   1952, so a contemporary source was demoted to `reference`.
4. **Review decisions** ([`raw/review3.jsonl`](raw/review3.jsonl)), not foreseen by the run sheet:
   drop, add, add a source, restore the second-pass milestone, keep, or reject a checker's
   replacement. New milestones and sources added there are verified in code like the agents'.
5. **The earliest-event check** covered only the ranking's milestone of each concept (13 of the 28
   that `select_checks3.py` first listed; the others are mass-adoption dates or a kind that doesn't
   score), split across two agents.
6. **Second judge, round 2:** 4 of the random-50 pairs entered the top 100 in round 1 and were
   judged again in round 2; their round-1 second score counts only in the agreement table.
7. **17 subagents** in all, not the 12 of the run sheet.

## 2. What the network allowed

| Host | Status | Seconds |
|---|---|---|
| books.google.com | 404 | 0.2 |
| www.googleapis.com/books/v1 | 429 | 0.3 |
| www.worldradiohistory.com | 200 | 0.5 |
| www.worldradiohistory.com (PDF) | 200 | 1.3 |
| bitsavers.org | 200 | 1.3 |
| bitsavers.org (PDF) | 200 | 0.5 |
| archive.computerhistory.org | 404 | 1.2 |
| www.computerhistory.org | 200 | 0.5 |
| ethw.org | 200 | 0.3 |
| spectrum.ieee.org | 200 | 0.3 |
| ieeexplore.ieee.org | 202 | 0.2 |
| *.si.edu (www.si.edu) | 403 | 0.2 |
| *.si.edu (airandspace.si.edu) | 200 | 0.3 |
| *.nasa.gov | 200 | 0.2 |
| ntrs.nasa.gov | 200 | 0.4 |
| pmc.ncbi.nlm.nih.gov | 200 | 0.3 |
| pubmed.ncbi.nlm.nih.gov | 200 | 1.0 |
| www.nature.com | -1 | 0.6 |
| api.crossref.org | 200 | 0.4 |
| api.semanticscholar.org | 429 | 0.2 |
| babel.hathitrust.org | 403 | 0.2 |
| archive.org (OCR text) | 200 | 2.4 |
| archive.org | 200 | 0.6 |
| archive.org full-text | 200 | 0.4 |
| www.smithsonianmag.com | 403 | 0.3 |
| www.aip.org | 200 | 0.9 |
| www.hagley.org | 200 | 0.6 |
| www.thehenryford.org | 200 | 0.9 |
| www.nobelprize.org | 200 | 0.6 |
| *.mit.edu | 200 | 0.2 |
| www.britannica.com (expected 403) | 403 | 0.2 |

Hosts of the verified sources of the target milestones (all kinds):

| Host | Sources |
|---|---|
| archive.org | 61 |
| en.wikipedia.org | 40 |
| api.crossref.org | 6 |
| unicog.org | 2 |
| pmc.ncbi.nlm.nih.gov | 2 |
| archive.computerhistory.org | 1 |
| api.semanticscholar.org | 1 |

- **Used in practice:** archive.org (full-text search, OCR text of scanned *Computerworld*,
  *Science*, *American Machinist*, DTIC, NTRS and ERIC reports, local newspapers), Wikipedia,
  Crossref, PubMed Central (through E-utilities), one Semantic Scholar record, one Computer History
  Museum PDF, one university PDF.
- **Not usable:** Google Books (the API's daily quota was exhausted all day: 429), HathiTrust,
  smithsonianmag.com and www.si.edu (403), nature.com (redirects to a blocked login host), IEEE
  Xplore (bot check), Britannica (403). Nothing was worked around.

## 3. The 33 target milestones

### 3.1 The ranking's milestone of each target concept

The milestone that scores is the concept's `first_practical_use`, else its `first_demonstration`.
Every row and every source is in [`milestones3.jsonl`](milestones3.jsonl) (`target3: true`); the
other milestones of each concept, the researchers' notes and what they searched are there and in
[`raw/ms3_concept_notes.jsonl`](raw/ms3_concept_notes.jsonl).

R = decided in raw/review3.jsonl; C = confirmed and X = replaced by the earliest-event check.

| Concept | Kind | Second pass | Third pass | Event | Sources | Confidence | Fit |
|---|---|---|---|---|---|---|---|
| Mind-reading machine | demonstration | 2008 (demo.) | **2006** R | Thirion, Duchesnay, Hubbard, Dubois, Poline, Lebihan and Dehaene (NeuroSpin, France) decoded fMRI activity to reconstruct the visual pattern that subjects were only imagining, using inverse retinotopy and supervised classifiers (NeuroImage 33(4), 2006). | 1 contemporary | low | From brain activity alone, a machine reconstructed the specific pattern a person was imagining (crude flickering-pattern shapes from a small set), not just its category. |
| Thought-to-text and thought display | demonstration | 2020 (demo.) | **2006** RX | Thirion, Duchesnay, Hubbard, Dubois, Poline, Lebihan and Dehaene (NeuroSpin, France) decoded fMRI activity to reconstruct the visual pattern that subjects were only imagining, using inverse retinotopy and supervised classifiers (NeuroImage 33(4), 2006). | 1 contemporary | low | From brain activity alone, the machine reconstructed an image the person was holding in mind (a mental image, not a displayed stimulus), shown as a reconstructed pattern; the images were crude flickering-pattern shapes. |
| Central computer directing many robots | practical use | 2007 (prac.) | **1974** RC | Volvo Kalmar assembly plant in regular production use of its fleet of computer-guided carriers. | 2 contemporary | low | The plant's fleet of computer-guided carriers did its production work, and all of them could be directed from one central computer. |
| Brain-computer interface | practical use | 1998 (prac.) | **1998**  | Philip Kennedy and Roy Bakay implanted a neurotrophic-cone electrode in the motor cortex of the locked-in patient Johnny Ray, who learned to control a computer cursor to communicate. | 1 contemporary, 1 reference | medium | A paralyzed person used signals from his own brain, via an implanted electrode, to control a computer, for the real purpose of communicating when he could not move. |
| Automatic dictation transcription | practical use | 1990 (prac.) | **1986-12** C | Kurzweil Applied Intelligence officially released its 1,000-word Voicerad system in Boston in December 1986; a radiologist was already writing his reports with it by voice. Dragon Systems had announced Voicescribe-1000 'automatic dictation transcription system' in June 1986. | 2 contemporary | medium | A computer listens to a user's spoken dictation of reports and produces the edited, printed text, used by a working radiologist. |
| Immersive virtual reality | practical use | 1990 (prac.) | **1990**  | VPL Research's Reality Built for Two (EyePhone head-mounted display plus DataGlove) was sold and in use at outside sites, and W Industries' Virtuality 1000SU VR systems were launched and sold to corporations such as BT, Ford and IBM. | 1 contemporary, 1 reference | medium | Commercial head-mounted systems that put a user inside a computer-generated, head-tracked 3D world were delivered to paying customers for research, design and training. |
| Retina and iris recognition | practical use | 1981 (demo.) | **1984**  | EyeDentify 7.5 retinal scanner in use as an access-control device; a 1985 Naval Postgraduate School thesis tested the 7.5 system (dated 1984 model) and Computerworld 1986 reports a Dallas vault firm using it at its guard door. | 2 reference | low | Machine identifies people at an entrance by scanning retinal vessel patterns, used for real access control. |
| Speech recognition and voice command | practical use | 1984 (prac.) | **1972** C | Threshold Technology (Delran/Cinnaminson, NJ) brought out the VIP-100 isolated-word recognizer and had voice-input terminals working in industrial, government and military 'real-world' use from late 1972. | 1 contemporary, 1 reference | medium | Spoken words were recognized by a commercial machine and used to enter data and give commands to a computer in working environments, outside the laboratory. |
| Automated face recognition | practical use | 1997 (prac.) | **1994** C | By 1994 facial-recognition biometric products had reached the marketplace (access control); the DMV offices of West Virginia and New Mexico followed, using automated face recognition against duplicate licences after the 1993 FERET test. | 1 contemporary, 1 reference | low | Commercial systems used cameras and computers to match a person's face against an enrolled stored image for entry control and identity checks. |
| Computerized information retrieval | practical use | 1966 (prac.) | **1967-05**  | Ames Research Center began using a DIALOG-fed remote terminal linked by telephone to Lockheed's computer (Summit's project under NASA contract). | 1 contemporary | low | Real users (NASA Ames) searched a large technical-literature file by remote terminal and got references in minutes. |
| Fully automated factory or plant | practical use | 2001 (prac.) | **2001** R | Fanuc's robot plant near Mount Fuji runs lights-out, robots building robots, unsupervised for up to 30 days. | 1 reference | low | Fanuc's robots built robots in a plant that ran unsupervised for up to 30 days: a factory that runs with few or no human workers, though people still maintain it. |
| Speech synthesis | practical use | 1976 (prac.) | **1976**  | The Kurzweil Reading Machine (scanner plus Votrax synthesizer reading printed pages aloud to blind people) was introduced in early 1976, the same year as Telesensory Systems' Speech+ talking calculator for the blind. | 1 contemporary, 1 reference | low | A computer converted text into phonetic commands for an electronic voice synthesizer that spoke the text aloud, for blind users' real reading needs. |
| Robot police and security guards | practical use | 2015 (prac.) | **1986** C | Denning Mobile Robotics' Sentry, marketed as an autonomous mobile security robot guard patrolling warehouses; prison units ordered by Southern Steel (600 ordered, 8 in advanced testing in late 1985). | 2 contemporary | low | A robot that patrols facilities on its own and alerts authorities to intruders, sold to customers for real guard duty. |
| Machine-readable identity and access card | practical use | 1968 (prac.) | **1961** C | Line Material Industries (McGraw-Edison) used the IBM 357 data collection system in which each employee inserts his identification card at a station, the machine records who he is and his time and attendance. | 1 contemporary | low | A machine reads each employee's ID card in daily factory use to identify him and record attendance and production against his name. |
| Companion or sex robot | practical use | 1999-06-01 (prac.) | **1998-10-02** C | Furby went on general sale in the United States (launched 2 October 1998, with a press event at FAO Schwarz, New York), selling 1.8 million in 1998. | 2 contemporary, 1 reference | low | The robotic pet toy was bought and kept by ordinary families as a companion that responds to touch and sound. |
| Question-answering computer | practical use | 1993 (demo.) | **1993** C | MIT's START went online on the Internet in 1993 and answered English questions from the public on many topics (Boris Katz) | 1 reference | low | A publicly reachable computer answering ordinary-language factual questions on many topics, used by outside people for that purpose; knowledge is hand-annotated so breadth is limited. |
| Machine-generated writing | practical use | 1990 (prac.) | **1990**  | Environment Canada used FoG, a system that generated weather forecast texts in English and French from numeric weather data, in its forecast operations. | 1 contemporary | low | Software wrote finished forecast texts from data with no human writer, in daily operational service. |
| Three-dimensional holographic display | practical use | 1972 (prac.) | **2009** RC | The Actuality Systems Perspecta Spatial 3D volumetric display was integrated with a clinical radiation-therapy planning system (Pinnacle) so that planners could view patient anatomy and beams in 3D from any side. | 2 reference | low | A swept-volume display showing changing patient-derived 3-D images in a 25 cm volume viewable from any side, used for its real purpose in treatment planning. |
| Touchscreen and gesture interface | practical use | 1972 (prac.) | **1972**  | PLATO IV terminals at the University of Illinois (1972) had a built-in 16x16 infrared touch panel that students used to answer questions in lessons | 1 contemporary, 1 reference | medium | Students controlled a teaching computer by touching its screen, a touch-panel input used for its real purpose (instruction) outside the lab. |
| Computer screen display | practical use | 1951 (prac.) | **1951**  | Project Whirlwind at MIT, operational from 1951, plotted letters, figures and graphics on CRT scopes for its users and showed radar data for the Cape Cod air-defence tests. | 1 contemporary, 1 reference | low | A real-time computer shows its results as text and graphics on screens to working users in place of printouts and dials. |
| Machine learning | demonstration | 1951 (demo.) | **1929-07** X | Clark L. Hull and H. D. Baernstein (Yale) built an electrochemical machine (polarizable cells and mercury-toluene thermal regulators, switches as receptors, a flashlight bulb as responder) that acquired conditioned responses from the sequence of stimuli it received, reported in Science, 5 July 1929. | 2 contemporary | medium | The machine changed its response from the experience of paired stimuli (a neutral switch came to light the bulb after training, with extinction, forgetting and spontaneous recovery) instead of being wired for that response. |
| Robot vacuum cleaner and lawn mower | practical use | 1969 (prac.) | **1969**  | MowBot went on sale to the public in 1969 (about $800), first commercial autonomous lawn mower | 1 contemporary, 1 reference | medium | Customers used the machine for its real purpose, mowing lawns without being driven. |
| Electronic book reader | practical use | 1990 (prac.) | **1990-07** C | The same Sony Data Discman DD-1 went on sale in Japan in July 1990 as an 'electronic book' player for reference works. | 1 contemporary, 1 reference | medium | A pocket-size battery device with its own LCD that shows the text of books and reference works stored on a 3-inch CD, replacing paper. |
| 3D printing | practical use | 1987 (prac.) | **1987-05**  | 3D Systems announced its stereolithography system (laser-cured acrylic resin, computer-controlled platform) as a product letting architects make detailed building models in minutes (Progressive Architecture, May 1987). | 1 contemporary, 1 reference | medium | A commercial machine built solid models automatically from computer sections of a design, layer by layer in photo-curing resin, for real design work. |
| Real-time computerized situation display | practical use | 1958-06-26 (prac.) | **1958-06**  | The SAGE New York Air Defense Sector, with its AN/FSQ-7 computer and operator display consoles at McGuire Air Force Base, was declared operational (27 June 1958 per Bell Telephone Magazine, 26 June per Wikipedia). | 1 contemporary, 1 reference | medium | An operational air-defense centre in which a computer fed by radar showed live aircraft tracks on operators' screens for real interception control. |
| Neural implant and cyborg augmentation | practical use | 1977-12 (prac.) | **1977-12**  | Hochmair's multichannel cochlear implant was first implanted in a person in Vienna in December 1977; Clark's followed in 1978 and was commercialized as Nucleus. | 1 reference | low | Implanted electronic device used in patients to restore hearing for real-world use. |
| Spacecraft guidance and navigation computer | practical use | 1965-03-23 (prac.) | **1965-03-23**  | The same Gemini III flight used the computer on a real crewed mission for navigation and reentry guidance; routine mission use (rendezvous burns) followed on Gemini 6A/7 in December 1965. | 1 contemporary | low | An onboard digital computer navigated the spacecraft and computed steering (bank) commands, which the crew flew, to fly the entry path to a landing target; on Gemini III it also generated the data for orbit-changing burns, so it calculates and steers, with the crew closing the loop. |
| Computer-run space station | practical use | 1973-05-14 (demo.) | **1973-05-25**  | The first Skylab crew (Skylab 2) arrived 25 May 1973 to a station whose onboard computer was handling attitude control and pointing; the computer kept running the station through all three crewed missions (e.g. it reconfigured to two control gyros after a gyro failure in 1973). | 1 contemporary, 1 reference | low | The computer-run systems were used for the station's real purpose with crews aboard, including automatic reconfiguration on failure; same partial fit as the demonstration. |
| Service robot for the public | practical use | none | **1985** R | The Two Panda Robot Restaurant in Pasadena, California, used two robots, Tanbo R-1 and Tanbo R-2, as waiters that took orders from diners (described in a 1985 National Geographic Society book). | 2 contemporary | low | Robots served a restaurant's customers as waiters, for the restaurant's real business. |
| Computerized personnel selection and aptitude testing | | none | none | | | | |
| Sleep learning | demonstration | none | **2019-02** R | Zust et al. (University of Bern) played recorded pseudoword/German word pairs to young adults in slow-wave sleep and found they had formed and kept new word associations that showed up on an implicit test after waking. | 1 contemporary | low | Recorded vocabulary was played to sleeping people and they retained new verbal associations from it, so teaching by recorded sound during sleep worked, though only for implicit word-pair associations and not for general lessons. |
| Computerized marketing and consumer analytics | practical use | none | **1961-08**  | American Investment Company (St. Louis), with Fair, Isaac and Company, announced a credit-scoring system for rating consumer loan risks, made practical by an electronic computer installed at its headquarters. | 1 contemporary | low | A computer-based statistical model scores customers (loan applicants) to predict their behaviour (repayment), i.e. the 'score customers' part of the definition; it does not cover audience measurement or purchase prediction. |
| Voiceprint speaker recognition | practical use | none | **1974** R | Texas Instruments controlled access to its Corporate Computer Center by automatic voice authentication (speaker verification), in operation 24 hours a day; a 1977 report says it had done so for the past three years. | 1 reference | low | A machine verified each person's identity from their voice to admit them to a computer center, in real daily use. |

**No milestone: computerized personnel selection** (34 pairs score 0). Computer interpretation of
the MMPI (1960s) had only a lending-library snippet; the Labor Department's Job Bank (1968–70)
lists job openings rather than testing or choosing people. The full run should look for computer
scoring or selection of pilots, astronauts or students in the 1950s–60s.

**Source kinds** (target concepts, demonstration and practical-use milestones):

| Pass | Milestones | With a contemporary source | Sources by kind |
|---|---|---|---|
| second | 47 | 1 | contemporary 1, reference 56, wikidata 1 |
| third | 55 | 46 | contemporary 58, reference 39 |

Of the 122 sources (the agents' and the review's), 114 verified in code; the other 8 had quotes of 26–29 words and were
dropped (with them the 1952 demonstration of machine-generated writing and the 1999 mass adoption
of the companion robot). Those quotes, and one of 27 words in the checker's output, remain in the
raw agent files (`raw/ms3_b02.jsonl`, `raw/ms3_b03.jsonl`, `raw/check3_out*.jsonl`); nothing longer
is stored.

### 3.2 Decisions taken in review

| Concept | Research gave | Decision | Why |
|---|---|---|---|
| Fully automated factory or plant | 1916, an unattended hydroelectric station | **2001** (second pass restored: Fanuc's lights-out plant) | Fits only the definition's "power plant", and "maintains itself" only partly; most claims are about factories. The concept mixes factories and power plants and should be split. |
| Mind-reading machine | 2005, the category of a recalled item read by fMRI | **2006** (Thirion et al.: imagined patterns reconstructed) | Category only is not "specific thoughts or images". The 2006 study, found by the check for thought-to-text, reads a specific imagined image; used for both concepts so they agree. |
| Voiceprint speaker recognition | 1962 and 1966 voiceprints | **1974** (Texas Instruments' voice authentication at its computer center) | People, not a machine, compared the 1960s voiceprints. TI's system ran 24 hours a day; dated from "for the past three years" in a 1977 report. |
| Service robot for the public | 2014, Pepper in SoftBank shops | **1985** (Two Panda Robot Restaurant, Pasadena) | Robot waiters described in a 1985 National Geographic book; 1985 is the latest the event can be (it probably opened about 1983). |
| Central computer directing many robots | 1974, Volvo Kalmar, central control not sourced | **1974**, with a 1975 book: all carriers "can be controlled from a central data computer" | The fit now has a source. |
| Thought-to-text and thought display | 2025, "mind captioning" | 2023 (imagined speech decoded to text), then **2006** by the earliest-event check | 2023 was the earlier strict fit; the check found 2006. |
| Three-dimensional holographic display | 2009, Perspecta in treatment planning | **2009** kept | Use is reported from late 2008 and the device was sold from about 2002, so the date may be several years late, but nothing earlier was verified. |
| Sleep learning | (check) LeShan 1942, nail-biting suggestion | **2019** kept; the check's replacement rejected | A suggestion, not a lesson; sleep was not established; later studies that measured sleep found no learning. |

## 4. Earliest-event check

Two Sonnet agents checked the 13 ranking milestones that give a claim more than 40 years of lead
and changed since the second pass ([`raw/check3_out.jsonl`](raw/check3_out.jsonl), applied by
`scripts/apply_checks3.py`, log [`raw/check3_applied.jsonl`](raw/check3_applied.jsonl)):
**10 confirmed, 2 replaced, 1 rejected in review.**

- **Replaced:** machine learning 1950 → 1929 (Hull and Baernstein's electrochemical machine that
  acquired conditioned responses, *Science*, 5 July 1929); thought-to-text 2023 → 2006 (Thirion et
  al., *NeuroImage*: patterns that subjects only imagined, reconstructed from fMRI; crude, low
  confidence).
- **Rejected:** sleep learning 2019 → 1942 (section 3.2).
- **Confirmed, with the earlier candidates the checkers rejected:** question answering 1993 (START
  answered JPL journalists in 1989, but on three topics; Baseball and Lunar each one domain);
  dictation December 1986 (Threshold's 1972 terminals took commands, not dictation); face
  recognition 1994 (AFIT's 1985 machine a prototype); robot guards 1986 (Quasar's robots
  promotional, Prowler experimental); ID card 1961 (IBM's 357 badge reader announced October 1960);
  e-book reader July 1990 (pocket dictionaries hold one book, one line at a time); speech
  recognition 1972, companion robot October 1998, central robot control 1974, holographic display
  2009.

## 5. Re-scoring

Same rules as the second pass ([`raw/pairs3.jsonl`](raw/pairs3.jsonl),
[`judgments3.jsonl`](judgments3.jsonl)): 2,147 pairs, of which 796 copied (same milestone kind and
date as the second pass), 765 scored 0 by rule (milestone in or before the claim's year), 34 with
no milestone, and **552 re-judged** by three Sonnet agents with `judge_prompt2.md`, in batches of
184 mixed across concepts. Every rationale in every batch is distinct.

Against the second pass, the re-judged pairs that had a judged score before kept it 253 times,
went lower 146 times and higher 64 times; 89 had scored 0 by rule or for lack of a milestone. The
second pass had seven scores of 1.0; after re-judging one is left (immersive virtual reality,
copied because its milestone did not change), and the second judge lowered it to 0.75. The others
went to 0.5 or 0.75 when their milestones changed, or to 0 by rule (ID card, now 1961).

## 6. Second judge

The best pair of each top-100 entry (from step 6's scores) and 50 random judged pairs went to a
different Sonnet agent, shuffled, without the first score or rationale. Pairs two or more steps
apart went to a third agent. The combined score (top 100 only): same, kept; one step apart, the
lower; further apart, the median of three. The top 100 was then recomputed and its 48 new entries
had one more round. Every score is in `judges`, the outcome in `action2`
([`raw/judge3b_round1.jsonl`](raw/judge3b_round1.jsonl), `raw/judge3c_round1.jsonl`,
`raw/judge3b_round2.jsonl`).

| Group | Pairs | Same score | One step apart | Two or more apart | Second judge lower | Second judge higher |
|---|---|---|---|---|---|---|
| top100 | 100 | 43 | 52 | 5 | 56 | 1 |
| top100_new | 48 | 24 | 24 | 0 | 22 | 2 |
| random50 | 50 | 32 | 18 | 0 | 11 | 7 |

Outcome for the top-100 and 1.0 pairs: agreed 67, lower 76, median 5.
Scores changed (first judge -> final): 0.5 -> 0.25: 33, 0.75 -> 0.25: 4, 0.75 -> 0.5: 40, 1 -> 0.75: 1.

- **On random pairs the two judges disagree without a direction:** a third of the time by one
  step, never by more, about as often lower as higher.
- **On the top they disagree in one direction:** 78 of the 148 top pairs were scored lower by the
  second judge and 3 higher. The ranking selects the pairs the first judge happened to score high,
  so a single judge's noise becomes the ranking. "The lower of two" corrects that crudely: it also
  pushes down pairs where the first judge was right.
- **Third judge:** 5 pairs in round 1, none in round 2. One was the second pass's judge error
  (#7: numbered knobs on a mirror wired to a kitchen, taken as a touch screen), now 0.25.
- **Not finished:** after round 2, 21 entries in the top 100 (ranks 79–100) have a single judge.
  The run sheet stops after two rounds; each round lowers scores and lets new entries in.

## 7. Results

### 7.1 The new top 20

Each book counted once per concept, by its best claim; points = score × log2(1 + lead years).
"Was" is the entry's rank in the second pass. The whole top 100 is in
[`raw/top100_3.tsv`](raw/top100_3.tsv).

| # | Was | Year | Concept | Milestone | Lead | Judges | Score | Points | Quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 19 | 1952 | Fully automated factory or plant | 2001 | 49 | 0.75/0.75 | 0.75 | 4.23 | It was powered by an atomic pile, stocked with materials which, when combined with the returning, worn-out robots, enabled it to keep producing indefinitely. |
| 2 | 22 | 1953 | Brain-computer interface | 1998 | 45 | 0.75/0.75 | 0.75 | 4.14 | even mechanisms which would react selectively to the electrical impulses generated by the cells of the human brain! |
| 3 | 23 | 1954 | Brain-computer interface | 1998 | 44 | 0.75/0.75 | 0.75 | 4.12 | What the helmet did was detect and sidetrack the motor impulses from my brain, broadcasting their pulsations by short wave radio to the robot, which … |
| 4 | 3 | 1949 | Immersive virtual reality | 1990 | 41 | 1/0.75 | 0.75 | 4.04 | a movie that gives one sight and sound. Suppose now I add taste, smell, even touch, if your interest is taken by the story. Suppose … |
| 5 | 29 | 1960 | Brain-computer interface | 1998 | 38 | 0.75/0.75 | 0.75 | 3.96 | As he did this, the electro-chemical change in a nervous tract triggered a tiny implanted device that sent its imperceptible signal to the mataform transceiver. |
| 6 | 44 | 1948 | Retina and iris recognition | 1984 | 36 | 0.75/1.0 | 0.75 | 3.91 | Kinnison dashed up to an apparently blank wall, turned his back upon four commissioned officers holding cocked forty-fives at the ready, and fitted his right … |
| 7 | 51 | 1952 | Retina and iris recognition | 1984 | 32 | 0.75/0.75 | 0.75 | 3.78 | Hold this up to your left eye for twenty seconds." He extended a flat, glittering little metal disk. "It's already sensitized and filled out. It … |
| 8 | 5 | 1962 | Automated face recognition | 1994 | 32 | 0.75/0.75 | 0.75 | 3.78 | a scanning device in the wall fastened its attention on them, simultaneously checking through a large store of previously registered human images and data associated … |
| 9 | 48 | 1958 | Automatic dictation transcription | 1986-12 | 28 | 0.75/0.75 | 0.75 | 3.64 | Jean-Jean turned away and began furiously talking at the Speak-a-Type, which rattled and stuttered as the type keys tried to keep up with her. |
| 10 | new | 1958 | Service robot for the public | 1985 | 27 | 0.75/0.75 | 0.75 | 3.61 | A robowaiter approached them, holding a menu board in its metal hands. |
| 11 | 55 | 1962 | Automatic dictation transcription | 1986-12 | 24 | 0.75/0.75 | 0.75 | 3.48 | An earphone reproduced Smith's dictation from his tape. As she listened, she edited mentally and spoke into the microphone of her typing machine, which transcribed … |
| 12 | new | 1953 | Voiceprint speaker recognition | 1974 | 21 | 0.75/0.75 | 0.75 | 3.34 | The living voice can't be imitated so as to get past the sound analyzers. Humans must be on the flagship. |
| 13 | new | 1953 | Voiceprint speaker recognition | 1974 | 21 | 0.75/0.75 | 0.75 | 3.34 | Old Rubberarm's got your voice pattern. Just ask for Juno Jones. |
| 14 | 46 | 1951 | Speech recognition and voice command | 1972 | 21 | 0.75/0.75 | 0.75 | 3.34 | We get in the elevator, and I say "first" to it. It gives out a coughing noise and the basement openings begin to click by … |
| 15 | 69 | 1897 | Brain-computer interface | 1998 | 101 | 0.5/0.5 | 0.5 | 3.34 | father says some day we may be able to work by sheer will power directly and have no need of hands at all. |
| 16 | 1 | 1906 | Thought-to-text and thought display | 2006 | 100 | 0.5/0.5 | 0.5 | 3.33 | I find that the thought images thrown upon the screen in room "D" are more vivid when the subject is kept in darkness. |
| 17 | 68 | 1906 | Mind-reading machine | 2006 | 100 | 0.5/0.5 | 0.5 | 3.33 | I am going to show you how thought can be collected in the form of vibrations, in the form of fluid electric current, and collected … |
| 18 | 74 | 1912 | Brain-computer interface | 1998 | 86 | 0.5/0.5 | 0.5 | 3.22 | the outer doors are manipulated by telepathic means. The locks are so finely adjusted that the doors are released by the action of a certain … |
| 19 | 50 | 1954 | Speech recognition and voice command | 1972 | 18 | 0.75/0.75 | 0.75 | 3.19 | He learned about saying 'Open' to a lock and having the electronic device 'recognize' him and let him in. |
| 20 | 75 | 1905 | Automatic dictation transcription | 1986-12 | 81 | 0.5/0.5 | 0.5 | 3.18 | we may essay the more difficult task of conceiving a means by which the spoken word may be directly translatable into print or typewriting. |

### 7.2 Where the second pass's top 20 went

| Second pass | Concept | Milestone then → now | Score then → now | Rank now |
|---|---|---|---|---|
| 1 | Thought-to-text and thought display | 2020 → 2006 | 1 → 0.5 | **16** |
| 2 | Automated face recognition | 1997 → 1994 | 1 → 0.5 | 96 |
| 3 | Immersive virtual reality | 1990 → 1990 | 1 → 0.75 | **4** |
| 4 | Computerized information retrieval | 1966 → 1967-05 | 1 → 0.5 | 114 |
| 5 | Automated face recognition | 1997 → 1994 | 1 → 0.75 | **8** |
| 6 | Retina and iris recognition | 1981 → 1984 | 1 → 0.5 | 160 |
| 7 | Touchscreen and gesture interface | 1972 → 1972 | 0.75 → 0.25 | 422 |
| 8 | Mind-reading machine | 2008 → 2006 | 0.75 → 0.25 | 448 |
| 9 | Robot police and security guards | 2015 → 1986 | 0.75 → 0.25 | 591 |
| 10 | Thought-to-text and thought display | 2020 → 2006 | 0.75 → 0.5 | 67 |
| 11 | Computer screen display | 1951 → 1951 | 0.75 → 0.5 | 36 |
| 12 | Mind-reading machine | 2008 → 2006 | 0.75 → 0.5 | 44 |
| 13 | Central computer directing many robots | 2007 → 1974 | 0.75 → 0.5 | 218 |
| 14 | Central computer directing many robots | 2007 → 1974 | 0.75 → 0.5 | 236 |
| 15 | Mind-reading machine | 2008 → 2006 | 0.75 → 0.5 | 57 |
| 16 | Machine learning | 1951 → 1929-07 | 0.75 → 0.5 | 188 |
| 17 | Central computer directing many robots | 2007 → 1974 | 0.75 → 0.5 | 299 |
| 18 | Central computer directing many robots | 2007 → 1974 | 0.75 → 0.5 | 308 |
| 19 | Fully automated factory or plant | 2001 → 2001 | 0.75 → 0.75 | **1** |
| 20 | Fully automated factory or plant | 2001 → 2001 | 0.75 → 0.5 | 69 |

Only four of the second pass's top 20 are still in it. The entries that fell were held up by a
1.0 that a changed milestone or the second judge lowered, or by a milestone that moved decades
earlier (central robot control, robot guards).

### 7.3 What carries the top 100

| Concept | Entries in the top 100 | Milestone | Confidence |
|---|---|---|---|
| Brain-computer interface | 18 | 1998 (practical use) | medium |
| Three-dimensional holographic display | 11 | 2009 (practical use) | low |
| Fully automated factory or plant | 10 | 2001 (practical use) | low |
| Mind-reading machine | 10 | 2006 (demonstration) | low |
| Thought-to-text and thought display | 8 | 2006 (demonstration) | low |
| Automatic dictation transcription | 5 | 1986-12 (practical use) | medium |
| Speech recognition and voice command | 4 | 1972 (practical use) | medium |
| Sleep learning | 4 | 2019-02 (demonstration) | low |
| Question-answering computer | 3 | 1993 (practical use) | low |
| Immersive virtual reality | 2 | 1990 (practical use) | medium |
| Retina and iris recognition | 2 | 1984 (practical use) | low |
| Automated face recognition | 2 | 1994 (practical use) | low |
| Voiceprint speaker recognition | 2 | 1974 (practical use) | low |
| Spacecraft guidance and navigation computer | 2 | 1965-03-23 (practical use) | low |
| Touchscreen and gesture interface | 2 | 1972 (practical use) | medium |
| Robot vacuum cleaner and lawn mower | 2 | 1969 (practical use) | medium |
| Service robot for the public | 1 | 1985 (practical use) | low |
| Computer screen display | 1 | 1951 (practical use) | low |
| Electronic voting and vote counting | 1 | 1964 (practical use) | low |
| Automated eavesdropping | 1 | 1971 (practical use) | low |
| Electronic paper and rewritable display surface | 1 | 2004 (practical use) | low |
| Automated scientific discovery | 1 | 2009 (demonstration) | low |
| Office automation | 1 | 1951 (practical use) | medium |
| Lie detector | 1 | 1921 (practical use) | medium |
| Optical character recognition | 1 | 1965 (practical use) | low |
| Computer-aided design and engineering | 1 | 1963-04 (practical use) | medium |
| Automated fingerprint recognition | 1 | 1965 (demonstration) | low |
| Robot police and security guards | 1 | 1986 (practical use) | low |
| Industrial robot | 1 | 1961 (practical use) | high |

Scores in the top 100: 25 at 0.75 and 75 at 0.5; none at 1.0.

## 8. What is still doubtful

- **Milestones on one low-confidence source that carry many entries:** mind-reading and
  thought-to-text 2006 (crude imagined patterns; 18 of the top 100); the holographic display 2009
  (probably several years late, which adds lead; 11); the automated factory 2001 (a concept that
  mixes factories and power plants; 10); service robot 1985 (an upper bound); speaker recognition
  1974 (dated from "for the past three years"); central robot control 1974 (carriers on tracks as
  "robots").
- **Concepts dated by a laboratory result**: mind-reading, thought-to-text, machine learning and
  sleep learning have only a demonstration, so a crude lab result decides their lead.
- **21 of the top 100 have one judge**, and those at the bottom of it may fall when judged again.

## 9. What the full run should do differently

- **Split concepts that bundle different things before dating them** (factories and power plants;
  mind-reading and thought display overlap).
- **Look for contemporary sources first in archive.org's full text** (magazines, DTIC, NTRS and
  ERIC reports, newspapers); cite lending-only books through item-restricted search snippets.
- **Have researchers write their output after every concept.** The cloud restarts cost two whole
  batches before the retry prompt said so.
- **Judge every pair that could reach the top twice, independently, and average** instead of a
  second judge on the top only: the top is selected on the first judge's noise.
- **Check only the ranking's milestones** for earlier events.
- **Keep review decisions as data** with their reasons, applied by the scripts, as
  `raw/review3.jsonl` does here.
- **Run research locally** when plan usage allows: open network, no container restarts.

## 10. Cost and time

| Part | Steps with agents | Subagents | Tokens | Time |
|---|---|---|---|---|
| cloud | 3 | 9 | 1,505,178 | 234 agent-minutes |
| local | 5, 6, 7 | 8 | 748,875 | 27 agent-minutes |
| total | | 17 | 2,254,053 | 261 agent-minutes |

The cloud part also used about $20 of cloud credit ($23 → $3), which includes the session's own
turns. The local part's own session is not counted in the tokens. Per agent:
[`usage3.tsv`](usage3.tsv).
