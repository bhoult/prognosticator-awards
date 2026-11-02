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
