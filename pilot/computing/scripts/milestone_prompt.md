# Milestone research prompt (computing pilot)

You are researching when computing technologies first became real. The concepts are in
`{batch}` (JSON lines: `concept_id`, `name`, `definition`, `aliases`). Do not edit any
files; return your results as text.

For **each** concept, find up to three dated milestones:

| kind | meaning |
|---|---|
| `first_demonstration` | shown to work at all (lab demo, prototype, published working system) |
| `first_practical_use` | used for its real purpose outside the lab (first service, first deployment, first product in use) |
| `mass_adoption` | ordinary people use it routinely |

Rules:

- The milestone must match the concept's **definition** (function and mechanism), not
  a loose analogue. Example: a 1960s mainframe database is not "mind uploading". If the
  concept has never become real (mind uploading, a sentient machine, telepathy
  machines), give it **no** milestones. Do not stretch.
- Prefer the earliest milestone that really fits. Dates as `YYYY` or `YYYY-MM-DD`.
- Each milestone needs 1–2 `sources`, each `{url, publisher, date, title, quote, kind}`:
  - `kind` is `contemporary` (a news report or paper from the time of the event) or
    `reference` (encyclopedia, museum, university or company history page). Reference
    sources are fine for this pilot; contemporary ones are better when you find them.
  - `quote`: **at most 25 words copied verbatim** from the page as you saw it, supporting
    the date. Use WebSearch (mode "standard") and, if it works for you, WebFetch to read
    the page. If you only saw a search-result summary and not the page text, set `quote`
    to `""` and `kind` to `search_summary`. Never invent or paraphrase a quote.
  - `date` is the source's publication date if known, else `""`.
- Keep it efficient: one or two searches per concept is usually enough; you know most of
  these dates already, so search to confirm and to get a URL, not to explore.
- Also give the concept's Wikidata item QID if a search result shows it to you
  (a wikidata.org URL or page); otherwise null. Do not guess QIDs from memory.

Output **only** JSON lines, no prose, no code fences. One line per milestone:

{"concept_id": "...", "kind": "first_practical_use", "date": "1951-06-14", "what": "one line: what happened, where, by whom", "sources": [{"url": "...", "publisher": "...", "date": "", "title": "...", "quote": "...", "kind": "reference"}]}

then one line per concept (every concept in the batch, including those with no milestones):

{"concept_id": "...", "wikidata": "Q123" or null, "note": "short note, e.g. why no milestone"}

and finally one line: {"_tools": "did WebFetch work? yes/no; anything else that went wrong"}
