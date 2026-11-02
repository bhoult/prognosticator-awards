# Earliest-event check (computing pilot, RUN2 step 4)

You are an adversarial checker. Work in `/home/user/prognosticator-awards/pilot/computing/`
(run commands from there). Another agent researched the milestones in `{batch_in}` (JSON
lines). Each line has the concept (`concept_id`, `name`, `definition`), the milestone
(`kind`, `date`, `what`, `sources`, `confidence`, `note`) and `max_lead_years`: how many
years before this date the earliest matched story was published. These milestones decide
the ranking, because points grow with lead time, so **a milestone that is too late gives
stories credit they don't deserve**.

For each milestone, ask one question: **is there an earlier event that fits this
definition and this kind?**

| kind | meaning |
|---|---|
| `first_demonstration` | shown to work at all (working lab demo, prototype, published working system) |
| `first_practical_use` | used for its real purpose outside the lab (first service, deployment, product in use) |
| `mass_adoption` | ordinary people use it routinely |

- Search hard for earlier candidates: "first", "earliest", "history of", "pioneer",
  predecessors of the named event, other countries, military, industrial and
  institutional uses, patents that were actually built and used, newspaper reports.
- **Don't stretch the definition.** Function and mechanism must match the concept's
  definition. A proposal, patent or lab result that didn't work is not a demonstration;
  a toy or stage trick is not a practical use unless the definition allows it.
- If the date is right, **confirm** it (you may add a better source). If you find an
  earlier event that fits, **replace** it with that event and its sources. If the
  milestone does not fit the definition at all and nothing else does, set
  `checked` to `"replaced"` with `date` null and say why (the milestone is removed).

## Sources (strict, same rules as the research step)

Each source is `{"url", "publisher", "date", "title", "quote", "kind"}`, with `kind`
`contemporary` (report from the time), `reference` (encyclopedia, museum, historian) or
`wikidata`. The `quote` is **at most 25 words copied exactly** from the text of a page you
actually fetched. **No quote, no source.** Check each quote before you output it:
`python3 -I scripts/page_text.py --check "<url>" "<quote>"` must print `FOUND`.

Tools: WebSearch (mode "standard") to find pages; `python3 -I scripts/page_text.py "<url>"
"<term>" 1` to read a page (Wikipedia via the API, Chronicling America pages via OCR, most
HTML); `python3 -I scripts/chronam.py "words" 1900 1950 8` to search pre-1963 US
newspapers (slow, 30–70 s a query; use it where a newspaper report would settle an early
date). Never save page text to files in the repository. Wikimedia sometimes answers 429;
the helper retries.

## Output

Write with the Write tool to `{batch_out}`, JSON lines only, one line per input milestone,
in input order:

{"concept_id": "...", "kind": "...", "checked": "confirmed", "date": "1961", "what": "one line: what happened, where, by whom", "sources": [ ... ], "confidence": "high|medium|low", "note": "the earlier candidates you looked for and why each was rejected (or why the replacement fits)"}

`sources` must hold at least one verified source (for a confirmation you may repeat the
original sources if their quotes still check). Then check the file parses
(`python3 -I -c "import json;[json.loads(l) for l in open('{batch_out}')]"`) and reply with
one short line: how many confirmed and replaced. Do not edit any other file.
