# Pilot, second pass: milestones from real sources

Run 2026-11-02, branch `pilot-computing`, following [`RUN2.md`](RUN2.md). (Sections are
filled in as the steps finish.)

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
- **Sources are reference pages, almost all Wikipedia.** 200 sources are `reference`
  (Wikipedia, plus a few computerhistory.org pages) and 4 are `wikidata`. None are
  `contemporary`. The agents found that most other hosts (Britannica, the Smithsonian,
  NASA, IEEE, Nature, museum sites) were refused by the environment's egress proxy or
  timed out. No agent used the Chronicling America helper; it worked when I tested it
  but is slow (30–70 s a query). So the quotes are real and verified, but the evidence
  is still one encyclopedia, not the hierarchy of DESIGN §6.
- **Confidence:** 2 high, 70 medium, 106 low. The agents were told to mark a milestone
  `low` when an earlier event may exist or the date is uncertain, and they did so often.
- 19 milestones are `mass_adoption` (first pass: 5), 87 `first_demonstration` and 72
  `first_practical_use`.
