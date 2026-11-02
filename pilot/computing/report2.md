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
