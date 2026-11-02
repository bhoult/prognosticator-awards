# Pilot, second pass: milestones from real sources

Run 2026-11-02 (18:21–20:50 UTC), branch `pilot-computing`, following [`RUN2.md`](RUN2.md).
The first-pass files are unchanged; every new output has a `2` in its name and passes
`scripts/validate2.py`. Scripts are in [`scripts/`](scripts/), raw agent output in [`raw/`](raw/).

## Summary

- **The network allowed Wikidata and Wikipedia** (with rate-limit retries), and
  Chronicling America at its new loc.gov address. Most other reference sites were
  refused by the environment's egress proxy, so in practice **every milestone source is a
  Wikipedia article** (plus 4 Wikidata statements). Every quote was re-fetched and checked
  in code; none is invented. There are still no contemporary sources.
- **Milestones moved a lot, and mostly earlier.** Of 107 concept–kind milestones that
  exist in both passes, 60 moved earlier, 8 later, 9 changed date within the same year and
  30 kept their date. 71 milestones are new and 11 are gone. The second pass has 178
  milestones for 97 concepts.
- **The ranking changed almost completely.** Only 4 of the first pass's top 20 (counted
  the same way, one entry per book and concept) are still in the top 20. The fingerprint,
  3D-display, Geminoid, e-paper and service-robot entries that the first report doubted
  have all dropped out: their milestones moved 39–44 years earlier or vanished, or (e-paper) the passage was re-judged lower.
- **The new top is not trustworthy yet, for two new reasons.** The re-judging gave seven
  scores of 1.0 (the first pass gave none), and six of them sit in the new top 6; I
  would lower most of them. And several milestones that now decide the ranking are still
  doubtful: a few moved *later* (automated factory 1981 → 2001, central robot control
  2006 → 2007), and some of the new ones stretch their definitions (section 6).

## 1. What the network allowed

Checked 2026-11-02 18:46 UTC by `scripts/netcheck.py` (results in `raw/netcheck.jsonl`).

| Source | Result |
|---|---|
| Wikidata SPARQL (`query.wikidata.org/sparql`) | **works**, fast (≈1 s) |
| Wikidata API (`www.wikidata.org/w/api.php`, `wbsearchentities`, `Special:EntityData`) | **works**, but often answers 429 "too many requests" (the environment's egress IP is shared); retrying with back-off gets through |
| Wikipedia API (`en.wikipedia.org/w/api.php`, REST summary) | **works**, same intermittent 429s |
| Chronicling America, old URL (`chroniclingamerica.loc.gov/search/pages/results/?…&format=json`) | **gone**: redirects (308) to `www.loc.gov/chroniclingamerica/…`, which is 404. The site has moved into loc.gov |
| Chronicling America, new API (`www.loc.gov/collections/chronicling-america/?q=…&fo=json`) | **works**, but slow (30–70 s per query) |

Two practical notes: Python's `urllib` hung behind the environment's proxy while `curl`
was instant, so `scripts/net.py` calls curl; and every request carries a descriptive
User-Agent and backs off on 429.

## 2. Wikidata

`scripts/wd_candidates.py` searched Wikidata for each concept's name, its parts and its
first aliases (through the SPARQL endpoint's `EntitySearch` service, which is not
rate-limited the way `wbsearchentities` is), and `scripts/wd_search_terms.py` ran a second
round with hand-chosen terms where the name search missed the obvious item (it never
offered Q68 "computer" for "Electronic digital computer"). I then chose, by hand, at most
one item per concept whose description matches the concept's definition, with the reason
in `raw/wikidata_picks.jsonl`. The step was otherwise done in code.

- **96 of 131 concepts** have an item (`concepts2.jsonl`); 35 have none, mostly fictional
  ideas (machine religion, psionic machines) or classes Wikidata only has as fiction
  themes, games or patents (robot police, codebreaking machines, a war-planning
  computer). Fictional items (universal translator, Three Laws of Robotics) were not used.
  Many picks are broader or narrower than the concept, and the pick file says so (e.g.
  `algorithmic trading` covers only the market half of computerized economic planning).
- **Only 9 dated statements** came back (`raw/wikidata_dates.jsonl`): concept-level items
  rarely carry P575/P571/P580 dates. They are: computer 1945 (P575), integrated circuit
  1958, calculator "1960s" (decade precision), personal computer 1957 (P575; an odd
  date), Internet 1969-10-29 (P571), email 1971, speech recognition 1952 (P580), robotic
  vacuum 1990 (P571) and teaching machine "1920s". So Wikidata is a weak source of dates
  here; it gave the research agents a cross-check, not a milestone.

## 3. Milestones from real sources

Nine Sonnet research agents, 11–15 concepts each, got the concept, its Wikidata item and
dates, the first-pass milestones and the reason each was doubted (`raw/doubts1.jsonl`),
and the prompt `scripts/milestone_prompt2.md`. Their raw output is in
`raw/ms2_b01–09.jsonl` and their per-concept notes in `raw/ms2_concept_notes.jsonl`.
`scripts/merge_milestones2.py` then checked **every source again, independently of the
agents**: it fetched each page anew and kept a source only if its quote (≤ 25 words)
occurs in the page text, and a Wikidata source only if its date is one of the item's
statements. The verdicts are in `raw/quote_check.jsonl`.

- 183 milestones came back; **178 for 97 concepts survived** (first pass: 118 for 99).
  204 sources passed, 4 were dropped for quotes over 25 words and 1 because the quote
  was not on the page. That left 5 milestones with no source, so they were dropped:
  personal-computer mass adoption (1977), e-mail first demonstration (1965), Siri as
  question-answering practical use (2011), Hero of Alexandria's vending machine
  (AD 62) and Luna 3 as a probe's practical use (1959).
- **Sources are reference pages, all from Wikipedia.** 200 sources are `reference`
  pages, all of them English Wikipedia, and 4 are `wikidata`. None are
  `contemporary`. The agents found that most other hosts (Britannica, the Smithsonian,
  NASA, IEEE, Nature, museum sites) were refused by the environment's egress proxy or
  timed out. No agent used the Chronicling America helper; it worked when I tested it
  but is slow (30–70 s a query). So the quotes are real and verified, but the evidence
  is still one encyclopedia, not the hierarchy of DESIGN §6.
- **Confidence:** 2 high, 70 medium, 106 low. The agents were told to mark a milestone
  `low` when an earlier event may exist or the date is uncertain, and they did so often.
- 19 milestones are `mass_adoption` (first pass: 5), 87 `first_demonstration` and 72
  `first_practical_use`.

## 4. Earliest-event check

`scripts/select_checks.py` found **67 milestones** that give at least one matched claim
more than 40 years of lead (lead = milestone year − claim year, over every claim matched
to the concept). Six Sonnet checker agents (11–12 milestones each, prompt
`scripts/earliest_prompt.md`) asked of each one: is there an earlier event that fits
this definition? `scripts/apply_checks.py` then verified every source they gave, the same
way as in step 3 (all passed), and wrote the outcome into `milestones2.jsonl`
(`checked`, plus `replaced_date` for the old date). The log is `raw/check_applied.jsonl`.

- **49 confirmed, 18 replaced, 0 removed.** Every replacement moved the date earlier, by
  1 to 61 years (median 12.5).
- One hand fix (`scripts/fix_milestones2.py`): the check moved hacking's practical use
  to 1967 (Evanston students breaking into an IBM network), which made it earlier than
  its demonstration (Creeper, 1971). The demonstration now uses the same 1967 event.
- After the check, 62 milestones still give more than 40 years of lead, and every one
  carries `checked`.

| Concept | Kind | Before | After | New event |
|---|---|---|---|---|
| office-automation | demonstration | 1951 | 1890 | Hollerith tabulators process the 1890 US census |
| computerized-economic-planning | practical use | 1972 | 1951 | LEO I runs bakery and tea-shop calculations at J. Lyons |
| artificial-senses | demonstration | 1982 | 1952 | Bell Labs' Audrey recognizes spoken digits |
| robot-pet | practical use | 1998-10 | 1962 | Ideal Toy's Gaylord battery-powered robot dog on sale |
| speech-to-text-dictation | demonstration | 1985 | 1961 | Kyoto University's Sonotype phonetic typewriter |
| computer-security-hacking | practical use | 1988-11-02 | 1967 | Evanston high-school students penetrate IBM's APL network |
| brain-computer-interface | demonstration | 1977 | 1965 | Lucier's *Music for Solo Performer*: EEG alpha waves drive percussion |
| machine-readable-id-card | practical use | 1975 | 1968 | RIT's VALI-DINE punched-card meal-access system |
| iris-retina-recognition | demonstration | 1994 | 1981 | EyeDentify retinal scanner on the market |
| question-answering-computer | demonstration | 2011-02 | 1993 | MIT's START answers English questions online |
| holographic-3d-display | practical use | 1989 | 1972 | Lloyd Cross's multiplex hologram (a moving 3D image) |
| face-recognition | practical use | 2000 | 1997 | Bochum system sold commercially |
| information-retrieval | practical use | 1971-12 | 1966 | Lockheed's Dialog used on NASA's database |
| electronic-book-reader | practical use | 1998 | 1990 | Sony Data Discman on sale |
| touch-gesture-interface | practical use | 1973 | 1972 | PLATO IV terminals with touch panels |
| computer-video-display | demonstration | 1949 | 1948-06 | Manchester Baby's CRT output |
| unmanned-aerial-vehicle | mass adoption | 2013 | 2010 | Parrot AR.Drone |
| virtual-reality | practical use | 1991 | 1990 | Virtuality systems sold to companies |

Some replacements are themselves stretches, and section 6 lists them as still doubtful
(LEO I as "economic planning", Lucier's concert piece as a brain-computer interface,
the 1890 census as "office automation").

## 5. Re-scoring

`scripts/make_pairs2.py` rebuilt the pairs with the first pass's rule (a concept's
`first_practical_use` milestone, else its `first_demonstration`) and decided how to score
each one. `scripts/make_judgments2.py` merged the result into `judgments2.jsonl`, one row
per pair with the first pass's fields plus `action`, `first_pass_milestone_date` and
`first_pass_score`.

| Action | Pairs | How |
|---|---|---|
| `copied` | 235 | same milestone kind and date as in the first pass: first-pass judgment copied |
| `rule` | 747 | milestone in or before the claim's year: score 0 |
| `no_milestone` | 125 | the concept lost its milestone: score 0 (service robot 63, personnel selection 34, sleep learning 16, consumer analytics 7, speaker recognition 5) |
| `rejudged` | 1,025 | first-pass pair, new milestone: judged again |
| `new` | 15 | concept gained a milestone: judged for the first time (superconducting computer, space-station automation, automated eavesdropping) |
| **Total** | **2,147** | all 2,116 first-pass pairs, plus 31 new pairs (16 of them 0 by rule) |

**Deviation.** RUN2 says to copy a judgment where "the milestone's date and
description are unchanged". The research agents re-worded every description, so no
description is literally unchanged. I copied where the kind and the exact date string
are unchanged, and checked by eye that each of these 235 pairs describes the same event
(e.g. the MowBot, LEXIS, Adleman's DNA computer). Every other pair was re-judged.

**Judging.** Seven Sonnet judges each took about 150 pairs, mixed across concepts with a
fixed seed. They used `scripts/judge_prompt2.md`: judge_v0 with the first pass's
amendments (the quotation wins over the summary; compare against the milestone, not the
concept name; no template sentences). Every batch had 100% distinct rationales, and no
pair was missing.

**Scores went up.** The mean score of re-judged pairs rose from 0.32 to 0.40 (500 same,
366 higher, 159 lower). Part of that is real: many milestones now describe an earlier
and closer event. But in the 85 re-judged pairs whose milestone kept its year, ups and
downs balance (20 up, 17 down, 48 same). Overall the judge gave **seven 1.0 scores**,
where the first pass gave none. The table:

| Change | Pairs |
|---|---|
| -0.50 | 7 |
| -0.25 | 152 |
| +0.00 | 500 |
| +0.25 | 264 |
| +0.50 | 88 |
| +0.75 | 14 |

Actions: {'rule': 747, 'rejudged': 1025, 'copied': 235, 'no_milestone': 125, 'new': 15}. Score distribution (all pairs): {0: 988, 0.25: 499, 0.5: 512, 0.75: 141, 1: 7}.

## 6. Results

### 6.1 How many milestone dates changed

| Change | Milestones |
|---|---|
| earlier | 60 |
| later | 8 |
| same year, different date | 9 |
| unchanged | 30 |
| new | 71 |
| removed | 11 |

Years moved, among the 68 that moved: median 10, earlier 60, later 8.

"Earlier" and "later" compare the year; "new" and "removed" are concept–kind milestones
that exist in only one pass.

**The 30 largest changes**, with the second pass's source for the new date (each is a
Wikipedia article, or Wikidata, whose quote was checked in code):

| # | Concept | Kind | Old | New | Change (years) | New event | Source |
|---|---|---|---|---|---|---|---|
| 1 | stored-program-control | demonstration | 1952 | 850 | -1102 | The Banu Musa brothers in Baghdad described an automatic flute player driven by a pinned barrel, in their Book | [Banu Musa](https://en.wikipedia.org/wiki/Banu_Musa) |
| 2 | clockwork-automaton | demonstration | 1206 | 1560 | +354 | Key-wound spring-driven clockwork monk, now in the Smithsonian, possibly dating as early as 1560 | [Automaton](https://en.wikipedia.org/wiki/Automaton) |
| 3 | vending-automat | practical use | 1895 | 1615 | -280 | Coin-operated brass tobacco dispensers operated in English taverns | [Vending machine](https://en.wikipedia.org/wiki/Vending_machine) |
| 4 | speech-synthesis | demonstration | 1939 | 1791 | -148 | Wolfgang von Kempelen's bellows-operated acoustic-mechanical speech machine, with models of tongue and lips pr | [Speech synthesis](https://en.wikipedia.org/wiki/Speech_synthesis) |
| 5 | machine-generated-writing | demonstration | 1953 | 1845 | -108 | John Clark's Eureka, a mechanical machine that generated Latin hexameter verses automatically (about one a min | [The Eureka](https://en.wikipedia.org/wiki/The_Eureka) |
| 6 | lethal-autonomous-weapon | practical use | 2020-03 | 1943-05 | -77 | Mark 24 mine entered Allied service in March 1943; first U-boat kills claimed in May 1943 | [Mark 24 mine](https://en.wikipedia.org/wiki/Mark_24_mine) |
| 7 | analog-computer | demonstration | 1931 | 1873 | -58 | Sir William Thomson's tide-predicting machine (built 1872-73 by Alexander Legé, with Edward Roberts); a model  | [Tide-predicting machine](https://en.wikipedia.org/wiki/Tide-predicting_machine) |
| 8 | microform-storage | practical use | 1928 | 1870 | -58 | During the Siege of Paris, Rene Dagron microphotographed dispatches on thin collodion film; carried by pigeon, | [Microform](https://en.wikipedia.org/wiki/Microform) |
| 9 | magnetic-data-storage | practical use | 1956-09-14 | 1903 | -53 | The American Telegraphone Company of Springfield, Massachusetts manufactured the Telegraphone, the first comme | [Wire recording](https://en.wikipedia.org/wiki/Wire_recording) |
| 10 | computer-crime-detection | practical use | 2011 | 1967 | -44 | The FBI's National Crime Information Center, a computerized national database of wanted persons and stolen pro | [National Crime Information Center](https://en.wikipedia.org/wiki/National_Crime_Information_Center) |
| 11 | android-duplicate-of-person | demonstration | 2006 | 1964 | -42 | Disney's Audio-Animatronic Abraham Lincoln shown in 'Great Moments with Mr. Lincoln' at the Illinois pavilion, | [Great Moments with Mr. Lincoln](https://en.wikipedia.org/wiki/Great_Moments_with_Mr._Lincoln) |
| 12 | holographic-3d-display | demonstration | 2001 | 1962 | -39 | First practical optical holograms recording 3D objects made by Denisyuk (USSR) and by Leith and Upatnieks (Mic | [Holography](https://en.wikipedia.org/wiki/Holography) |
| 13 | robot-pet | practical use | 1999-06-01 | 1962 | -37 | Ideal Toy Company sold Gaylord, a battery-powered toy dog steered by its leash. | [Robot dog](https://en.wikipedia.org/wiki/Robot_dog) |
| 14 | humanoid-robot | demonstration | 1973 | 1939 | -34 | Westinghouse's Elektro (built 1937-38) shown at the 1939 New York World's Fair; walked by voice command, spoke | [Elektro](https://en.wikipedia.org/wiki/Elektro) |
| 15 | artificial-senses | demonstration | 1982-09-23 | 1952 | -30 | Bell Labs (Balashek, Biddulph, Davis) built Audrey, a single-speaker spoken-digit recognizer: a machine sense  | [Speech recognition](https://en.wikipedia.org/wiki/Speech_recognition) |
| 16 | automatic-door | practical use | 1960 | 1931 | -29 | The Stanley optical door was installed in a West Haven, Connecticut restaurant for waiters carrying food. | [Automatic door](https://en.wikipedia.org/wiki/Automatic_door) |
| 17 | lie-detector | demonstration | 1921 | 1895 | -26 | Cesare Lombroso used a device measuring blood pressure changes on criminal suspects in police cases. | [Polygraph](https://en.wikipedia.org/wiki/Polygraph) |
| 18 | flight-simulator | practical use | 1934 | 1910 | -24 | Antoinette barrel used for military ground training of pilots in France | [Flight simulator](https://en.wikipedia.org/wiki/Flight_simulator) |
| 19 | internet-global-information-network | demonstration | 1991-08-06 | 1969-10-29 | -22 | First ARPANET message UCLA to SRI (Wikidata inception of the Internet) | [Internet](https://www.wikidata.org/wiki/Q75) |
| 20 | computer-security-hacking | practical use | 1988-11-02 | 1967 | -21 | Students at Evanston Township High School (Chicago suburb) penetrated IBM's APL network in fall 1967, the firs | [Timeline of computer security hacker history](https://en.wikipedia.org/wiki/Timeline_of_computer_security_hacker_history) |
| 21 | computerized-economic-planning | practical use | 1972 | 1951 | -21 | J. Lyons & Co's LEO I computer, in business use from 1951, calculated bakery and tea-shop overnight production | [LEO (computer)](https://en.wikipedia.org/wiki/LEO_(computer)) |
| 22 | automated-factory | practical use | 1981 | 2001 | +20 | Fanuc's robot plant near Mount Fuji runs lights-out, robots building robots, unsupervised for up to 30 days. | [Lights out (manufacturing)](https://en.wikipedia.org/wiki/Lights_out_(manufacturing)) |
| 23 | flight-simulator | demonstration | 1929 | 1910 | -19 | French military built the Antoinette barrel, a ground trainer for aircraft pilots | [Flight simulator](https://en.wikipedia.org/wiki/Flight_simulator) |
| 24 | nanorobot | demonstration | 2010-05-13 | 1991 | -19 | Stoddart's rotaxane molecular shuttle, the breakthrough in synthesising artificial molecular machines (first r | [Molecular machine](https://en.wikipedia.org/wiki/Molecular_machine) |
| 25 | computer-network | demonstration | 1969-10-29 | 1951-04-20 | -18 | Test at Bedford, Massachusetts: radar data sent over telephone lines to a computer (Whirlwind), showing detect | [Semi-Automatic Ground Environment](https://en.wikipedia.org/wiki/Semi-Automatic_Ground_Environment) |
| 26 | question-answering-computer | demonstration | 2011 | 1993 | -18 | MIT's START natural-language system went online on the Internet in 1993 and answered English questions on many | [Boris Katz](https://en.wikipedia.org/wiki/Boris_Katz) |
| 27 | emp-electronics-vulnerability | demonstration | 1962-07-09 | 1945-07-16 | -17 | Trinity, the first nuclear test (New Mexico): recording instruments were paralyzed by pickup at the moment of  | [Nuclear electromagnetic pulse](https://en.wikipedia.org/wiki/Nuclear_electromagnetic_pulse) |
| 28 | electronic-book-reader | practical use | 2004-04 | 1990 | -14 | Sony Data Discman DD-1, a handheld electronic book player reading books on mini-CD, sold in Japan in 1990 | [Sony Data Discman](https://en.wikipedia.org/wiki/Sony_Data_Discman) |
| 29 | iris-retina-recognition | demonstration | 1994 | 1981 | -13 | EyeDentify's retinal scanner went on the market as a commercial model in 1981 (specific scanner means patented | [Retinal scan](https://en.wikipedia.org/wiki/Retinal_scan) |
| 30 | brain-computer-interface | demonstration | 1977 | 1965 | -12 | Alvin Lucier's Music for Solo Performer (1965) used a performer's EEG alpha waves, via amplifiers and filters, | [Brain-computer interface](https://en.wikipedia.org/wiki/Brain%E2%80%93computer_interface) |

Two of these are moves *later*: the clockwork automaton (Al-Jazari's 1206 book was not
re-sourced, and the earliest surviving automaton with a fetchable source is a c. 1560
clockwork monk) and the automated factory (the first pass's 1981 Fanuc report found no
source, so the 2001 lights-out description replaced it).

### 6.2 The new top 20

Points = score × log2(1 + lead years), lead capped at 500 years (DESIGN §8). **Each
book is counted once per concept**, by its best claim (`book` in `claims.jsonl`). The
last column is the same entry's rank in the first pass, recomputed the same way.

| # | Year | Quote | Concept | Milestone | Lead | Score | Points | First-pass rank |
|---|---|---|---|---|---|---|---|---|
| 1 | 1906 | "From this lens I shall pour upon the screen in a minute or two for you all to see, without doubt and in simple view, the thoughts of the man or woman on whom…" | Thought-to-text and thought display | 2020: Chang and Makin at UCSF decoded spoken sentences from ECoG signals into text with 3% word  (demonstration) | 114 | 1 | 6.85 | 457 |
| 2 | 1953 | "In seconds, a giant machine could find a similar picture in its files, complete with every detail of information concerning him." | Automated face recognition | 1997: The Bochum face-recognition system, by 1997 outperforming other systems, was sold commerci (practical use) | 44 | 1 | 5.49 | 204 |
| 3 | 1949 | "a movie that gives one sight and sound. Suppose now I add taste, smell, even touch, if your interest is taken by the story. Suppose I make it so that you are…" | Immersive virtual reality | 1990: Virtuality 1000SU VR systems launched in London in 1990 and sold to corporations (Ford, IB (practical use) | 41 | 1 | 5.39 | 345 |
| 4 | 1928 | "the great central filing office of the Hans in Nu-yok, where the entire mass of official records was kept, constantly available for instant projectoscoping t…" | Computerized information retrieval | 1966: Lockheed's interactive Dialog system (Roger Summit) was tested on NASA's STAR database at  (practical use) | 38 | 1 | 5.29 | 26 |
| 5 | 1962 | "a scanning device in the wall fastened its attention on them, simultaneously checking through a large store of previously registered human images and data as…" | Automated face recognition | 1997: The Bochum face-recognition system, by 1997 outperforming other systems, was sold commerci (practical use) | 35 | 1 | 5.17 | 521 |
| 6 | 1951 | "That should serve unless somebody examines your retina patterns" | Retina and iris recognition | 1981: EyeDentify's retinal scanner went on the market as a commercial model in 1981 (specific sc (demonstration) | 30 | 1 | 4.95 | 215 |
| 7 | 1890 | "these were connected by electric wires with the kitchen of the hotel, and if I would observe the numbers attached to any articles in the bill of fare which I…" | Touchscreen and gesture interface | 1972: PLATO IV terminals, introduced at the University of Illinois in 1972, had a built-in 16x16 (practical use) | 82 | 0.75 | 4.78 | 488 |
| 8 | 1937 | "Why, they have a little memory-prober that can read a man's life history from his mind!" | Mind-reading machine | 2008: ATR labs in Kyoto reconstructed 10x10-pixel images a person viewed from brain signals. (demonstration) | 71 | 0.75 | 4.63 | 70 |
| 9 | 1948 | "They're robots, not men. That makes it harder, since they're undoubtedly connected direct to Roger's desk and will give an alarm at the first hint of abnorma…" | Robot police and security guards | 2015: Knightscope shipped its first autonomous security patrol robot (practical use) | 67 | 0.75 | 4.57 | 1 |
| 10 | 1957 | "watching the secretary sitting inside a totally enclosed desk, operating a Mento-Writer Machine, the electrical contact-buttons fixed to her temples." | Thought-to-text and thought display | 2020: Chang and Makin at UCSF decoded spoken sentences from ECoG signals into text with 3% word  (demonstration) | 63 | 0.75 | 4.50 | 89 |
| 11 | 1890 | "As I took my seat my weight set some machinery in motion. A few feet in front of me suddenly rose out of the table a large upright mirror, or such I took it …" | Computer screen display | 1951: Whirlwind became operational in 1951, real-time output on CRT displays used in Cape Cod ra (practical use) | 61 | 0.75 | 4.47 | 525 |
| 12 | 1948 | "[…] has read your mind and it has retranslated these readings into visual images. We are now going to watch the shapes of your own thoughts." | Mind-reading machine | 2008: ATR labs in Kyoto reconstructed 10x10-pixel images a person viewed from brain signals. (demonstration) | 60 | 0.75 | 4.45 | 2 |
| 13 | 1947 | "And there are a thousand plastico-mechanical creations which act positronically under World Brain to carry out its functions." | Central computer directing many robots | 2007: Walgreens installed a Kiva mobile-robot fulfilment system at Mount Vernon, Illinois (practical use) | 60 | 0.75 | 4.45 | 109 |
| 14 | 1950 | "Consider—any electronic system of control might be likened to a nervous system. No machine lacking such refinement and organization could hope to respond to …" | Central computer directing many robots | 2007: Walgreens installed a Kiva mobile-robot fulfilment system at Mount Vernon, Illinois (practical use) | 57 | 0.75 | 4.39 | 135 |
| 15 | 1954 | "Ruscar led Tedor to a chair, told him to sit down. Soon Ruscar had clamped an electrode to the side of Tedor's head, plugging the wire which led from it into…" | Mind-reading machine | 2008: ATR labs in Kyoto reconstructed 10x10-pixel images a person viewed from brain signals. (demonstration) | 54 | 0.75 | 4.34 | 132 |
| 16 | 1900 | "it will be capable of distinguishing between what it ought and what it ought not to do, and of making experiences or, otherwise stated, of recording impressi…" | Machine learning | 1951: Marvin Minsky and Dean Edmonds built SNARC at Princeton (funding summer 1951), a neural-ne (demonstration) | 51 | 0.75 | 4.28 | 104 |
| 17 | 1957 | "The waiters—remote-control humanoids guided by the vast robot brain in the basement—were dressed in the fluffy, bright, fluorescent clothing of a style that …" | Central computer directing many robots | 2007: Walgreens installed a Kiva mobile-robot fulfilment system at Mount Vernon, Illinois (practical use) | 50 | 0.75 | 4.25 | 12 |
| 18 | 1958 | "Of course! Radio! I'll bet anything they're automatically controlled by the camp computer. That's where their brain is!" | Central computer directing many robots | 2007: Walgreens installed a Kiva mobile-robot fulfilment system at Mount Vernon, Illinois (practical use) | 49 | 0.75 | 4.23 | 15 |
| 19 | 1952 | "It was powered by an atomic pile, stocked with materials which, when combined with the returning, worn-out robots, enabled it to keep producing indefinitely." | Fully automated factory or plant | 2001: Fanuc's robot plant near Mount Fuji runs lights-out, robots building robots, unsupervised  (practical use) | 49 | 0.75 | 4.23 | 40 |
| 20 | 1954 | "It was packed with expensive robotic equipment, and was designed to be completely self-sustaining, once its controls were properly set." | Fully automated factory or plant | 2001: Fanuc's robot plant near Mount Fuji runs lights-out, robots building robots, unsupervised  (practical use) | 47 | 0.75 | 4.19 | 293 |

My reading of the top 20, without changing the data:

- **The seven 1.0 scores are generous.** #6 is a single line that only names retina
  patterns as a check; by the rubric it is 0.25–0.5. #4 is a central filing office with
  records "available for instant projectoscoping", with no machine search described;
  0.5. #1 projects "thoughts" onto a screen. The milestone is a 2020 decoder of attempted
  speech, so 0.5–0.75 at most. #2, #3 and #5 are fair at 0.75 and arguably 1.0.
- **#7 is a judge error:** electric wires and numbered dishes on a menu are buttons, not
  a touchscreen.
- **Four entries (#13, #14, #17, #18) depend on the 2007 Walgreens/Kiva milestone**, and
  **two (#19, #20) on the 2001 lights-out factory**. Both are probably late (section 6.4).
- #9 (robot guards, 2015) is the first pass's #1, still on a milestone that could not be
  pushed earlier with a fetchable source.

### 6.3 How the ranking moved

| # | Year | Quote | Concept | Milestone | Lead | Score | Points | Second-pass rank |
|---|---|---|---|---|---|---|---|---|
| 1 | 1948 | "They're robots, not men. That makes it harder, since they're undoubtedly connected direct to Roger's desk and will give an alarm at the first hint of abnorma…" | Robot police and security guards | 2015: Knightscope shipped its first K5 autonomous security patrol robot to a customer (practical use) | 67 | 0.75 | 4.57 | 9 |
| 2 | 1948 | "[…] has read your mind and it has retranslated these readings into visual images. We are now going to watch the shapes of your own thoughts." | Mind-reading machine | 2011: Nishimoto, Gallant et al. (UC Berkeley) reconstructed approximate movie clips a subject ha (demonstration) | 63 | 0.75 | 4.50 | 12 |
| 3 | 1939 | "the tank was seven hundred feet in diameter and eighty feet thick in the middle—over seventeen million cubic feet of space in which more than two million tin…" | Three-dimensional holographic display | 2001: Actuality Systems' Perspecta, a swept-volume display showing a 3D image viewable from all  (demonstration) | 62 | 0.75 | 4.48 | 255 |
| 4 | 1955 | "the only hotel staffed entirely with robot servants" | Service robot for the public | 2014-08: Savioke's Relay delivery robot went into continuous service at the Aloft Cupertino hotel,  (practical use) | 59 | 0.75 | 4.43 | — |
| 5 | 1960 | "A robot redcap came gliding along. Inevitably, it was gilded, and looked absolutely brand new." | Service robot for the public | 2014-08: Savioke's Relay delivery robot went into continuous service at the Aloft Cupertino hotel,  (practical use) | 54 | 0.75 | 4.34 | — |
| 6 | 1954 | "Every Robot in North and South America has its own particular wavelength, although the master intelligence is in tune with all of them." | Central computer directing many robots | 2006: Staples deployed Kiva Systems' fleet of warehouse drive-unit robots, coordinated by contro (practical use) | 52 | 0.75 | 4.30 | 138 |
| 7 | 1954 | "Nor had he guessed that Revanche would then employ Bioid's competitor to fashion an electronic proxy of himself." | Robot copy of a particular person | 2006: Hiroshi Ishiguro and Kokoro unveiled Geminoid HI-1, a teleoperated android modelled on Ish (demonstration) | 52 | 0.75 | 4.30 | 433 |
| 8 | 1950 | "They brought a three-dimensional map out of the air, I guess; I couldn't tell. It hung in the air like it was glued to nothingness." | Three-dimensional holographic display | 2001: Actuality Systems' Perspecta, a swept-volume display showing a 3D image viewable from all  (demonstration) | 51 | 0.75 | 4.28 | 62 |
| 9 | 1955 | "Clifford Ainsley. The prototype, that is, in the flesh and not a roboid. He nodded at the body on the floor. "Ainsley the Second. Strictly a lab job."" | Robot copy of a particular person | 2006: Hiroshi Ishiguro and Kokoro unveiled Geminoid HI-1, a teleoperated android modelled on Ish (demonstration) | 51 | 0.75 | 4.28 | 449 |
| 10 | 1953 | "She pressed it and the slab, at first gay orange, turned pale blue; on it appeared three lines of squiggly characters" | Electronic paper and rewritable display surface | 2004-04: Sony's Librie in Japan was the first consumer product to use an E Ink electronic paper mod (practical use) | 51 | 0.75 | 4.28 | 154 |
| 11 | 1950 | "As she was leaving, Jerry came into the pharmacy, recorded his thumbprint and took a box of aspirin from the machine." | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the  (practical use) | 49 | 0.75 | 4.23 | 361 |
| 12 | 1957 | "The waiters—remote-control humanoids guided by the vast robot brain in the basement—were dressed in the fluffy, bright, fluorescent clothing of a style that …" | Central computer directing many robots | 2006: Staples deployed Kiva Systems' fleet of warehouse drive-unit robots, coordinated by contro (practical use) | 49 | 0.75 | 4.23 | 17 |
| 13 | 1957 | "George Prime had remote controls, as well as a completely recorded neurological analogue of his boss, who was me." | Robot copy of a particular person | 2006: Hiroshi Ishiguro and Kokoro unveiled Geminoid HI-1, a teleoperated android modelled on Ish (demonstration) | 49 | 0.75 | 4.23 | 504 |
| 14 | 1962 | "Everything that's happening around here is being fed back to them at the moment," he said. "When they heard about our invite to Lyad's dinner party, and who …" | Computer crime detection and predictive policing | 2011: The LAPD deployed PredPol, a UCLA-developed algorithm for predicting where crime will happ (practical use) | 49 | 0.75 | 4.23 | 379 |
| 15 | 1958 | "Of course! Radio! I'll bet anything they're automatically controlled by the camp computer. That's where their brain is!" | Central computer directing many robots | 2006: Staples deployed Kiva Systems' fleet of warehouse drive-unit robots, coordinated by contro (practical use) | 48 | 0.75 | 4.21 | 18 |
| 16 | 1948 | "Kinnison dashed up to an apparently blank wall, turned his back upon four commissioned officers holding cocked forty-fives at the ready, and fitted his right…" | Retina and iris recognition | 1995: The FBI's iris recognition overview says the first commercial iris recognition products be (practical use) | 47 | 0.75 | 4.19 | 44 |
| 17 | 1952 | "The whorls at the tips of my fingers set off a light-switch mechanism within the stone," she explained. "It's better than any key." | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the  (practical use) | 47 | 0.75 | 4.19 | 384 |
| 18 | 1955 | "In the center of the cabin an image flickered, swarming flecks of light and shadow that filled out a three-dimensional form, complete and detailed." | Three-dimensional holographic display | 2001: Actuality Systems' Perspecta, a swept-volume display showing a 3D image viewable from all  (demonstration) | 46 | 0.75 | 4.17 | 356 |
| 19 | 1953 | "The Identifier, beyond the door, began to hum. That meant somebody was putting his hand to the opaque screen, and if the scanner recognized the fingerprints …" | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the  (practical use) | 46 | 0.75 | 4.17 | 173 |
| 20 | 1954 | "A hidden device checked the pattern and whorls of the militiaman's fingerprints. The effect was the same as the Open Sesame of the Arabian Nights, for a grea…" | Automated fingerprint recognition | 1999-07: The FBI's IAFIS, built by Lockheed Martin, became operational in July 1999. It is not the  (practical use) | 45 | 0.75 | 4.14 | 205 |

In both top 20s: 4. Book-concept entries with points: first pass 1034, second 913.
Lead years in the top 20: first pass 45–67, second pass 30–114.


- **4 of the first pass's top 20 stay in the top 20**: robot guards (#1 → #9), the mind-reading
  passage (#2 → #12) and two central-computer passages (#12 → #17, #15 → #18).
- **The entries the first report doubted all fell**:
  - 3D display: the milestone moved from 2001 to 1962, the first holograms. The 1939 tank
    passage fell from #3 to #255, and the 1950 map that "hung in the air" to #62.
  - Robot copy of a person: Geminoid in 2006 became Disney's animatronic Lincoln in 1964,
    so #7, #9 and #13 fell to #433–#504.
  - Fingerprint locks: the 1999 FBI database is gone. The concept now has only a 1965
    research demonstration, so #11, #17, #19 and #20 fell to #173–#384.
  - Predictive policing: NCIC, 1967, replaced PredPol, 2011, so #14 fell to #379.
  - E-paper: still Librie in 2004 for practical use, but the passage was re-judged lower
    (#10 → #154).
  - Service robots: no milestone survived verification, so #4 and #5 now score 0. That
    is the opposite error; see 6.4.
- **What rose**: entries with a 1.0 score (face recognition, VR, information retrieval,
  retina) and entries whose concept gained a milestone with a long lead (thought display,
  touchscreen, computer display for an 1890 novel).
- The top 20's lead times now span 30–114 years (first pass 45–67), and 913 book–concept
  entries have points (first pass 1,034). Points fell because 125 pairs lost their
  milestone and many leads shrank.

### 6.4 Milestones that are still doubtful

Ranked by how much they matter to the ranking.

1. **Central computer directing robots, 2007 (Walgreens/Kiva).** It is one year later
   than the first pass's milestone, and it carries four of the top 20. Centrally
   dispatched AGV fleets in factories and warehouses date from the 1970s–80s, but the
   checker found no fetchable source.
2. **Automated factory, 2001.** The first pass had 1981 for Fanuc's unattended plant;
   only a later Wikipedia description could be quoted. It is probably about 20 years late
   and carries #19 and #20.
3. **Thought-to-text, 2020 (UCSF speech decoding).** The concept list itself expected this
   never to come true. Decoding attempted speech is not displaying thoughts, so it is
   both a stretch and #1.
4. **Mind-reading, 2008 (10×10-pixel images of what a person sees).** A stretch: it
   reconstructs what was seen, not specific thoughts or memories. It carries #8, #12
   and #15.
5. **Robot police and guards, 2015.** The checker named likely earlier security robots
   (1980s) but could not source them.
6. **Service robot: none.** Hospital delivery robots (late 1980s) and others exist, but no
   page could be fetched for them, so 63 pairs score 0. Personnel selection, consumer
   analytics (the first pass's 1958 credit scoring) and speaker recognition lost their
   milestones the same way. They are gaps in sourcing, not in history.
7. **Fingerprint recognition: only a 1965 research demonstration.** No practical use was
   sourced. Automated fingerprint access control and identification systems of the
   1970s–80s should be found.
8. **Stretches introduced by the research or the check:**
   - LEO I's bakery calculations (1951) as computerized economic planning;
   - Lucier's EEG concert piece (1965) as a brain-computer interface;
   - the 1890 census tabulators as office automation;
   - a leash-steered toy dog (1962) as a robot pet's practical use;
   - Elektro (1939) as a humanoid robot;
   - Disney's animatronic Lincoln (1964) as a robot copy of a particular person;
   - static holograms (1962) as a 3D display.
   Each is defensible on a literal reading of the definition, but none has been reviewed
   by a person.
9. **Dates the agents themselves called approximate:**
   - superconducting computer, 1960;
   - MYCIN, about 1972;
   - dictation, 1961 (RCA's 1956 phonetic typewriter is probably earlier, but unsourced);
   - "Adam", 2009 (no year on any fetched page);
   - midpoint dates in batch 7.
10. **All of it rests on one encyclopedia.** 106 of 178 milestones are marked `low`
    confidence, 70 `medium` and 2 `high`; no source is contemporary.

**Recommendations.**
- Before the full run, allow the reference hosts the agents needed (Britannica,
  computerhistory.org worked, Smithsonian, IEEE/ETHW, NASA NTRS, Nature/PMC) and give
  the agents a working newspaper search. Chronicling America works but no agent chose to
  wait 30–70 s per query, so it should be run in code, for example a search for each
  pre-1963 milestone.
- Have a person review the roughly 30 milestones that carry the top 100.
- Add a second judge for every pair scored 1.0 or reaching the top 100.

## 7. Cost and time

| Step | Subagents | Tokens (as reported per agent) | Agent time (s) |
|---|---|---|---|
| 3 Milestone research | 9 | 1,179,074 | 14,674 |
| 4 Earliest-event check | 6 | 554,957 | 7,580 |
| 5 Judging | 7 | 639,434 | 685 |
| **Total** | **22 of 25** | **2,373,465** | **22,939** |

Steps 1, 2 and 6 ran in code in the main session. Per-agent figures are in `usage2.tsv`.
The token figure is what the harness reports for each subagent, the same measure the
first pass logged as "final context". Wall-clock time was about 2.5 hours (18:21–20:50
UTC). Most of it went to the research agents: 25–45 minutes each, run in parallel,
mostly waiting on slow or failing page fetches. The judges took 1–2 minutes each.
