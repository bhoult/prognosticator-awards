# Milestone research prompt, second pass (computing pilot, RUN2 step 3)

You are researching when computing technologies first became real. Work in
`/home/user/prognosticator-awards/pilot/computing/` (run commands from there).

Your concepts are in `{batch_in}` (JSON lines). Each line has `concept_id`, `name`,
`definition`, `aliases`, `realizable` (the concept list's guess whether it ever came
true), `wikidata` (the matched Wikidata item and its dated statements, or null),
`first_pass` (the milestones a first, shallow pass found, from search summaries only)
and `doubt` / `first_pass_note` (why those were doubted or what was left unchecked).
The first pass is often wrong, and usually **too late**: it settled for the best-known
event. Do not trust it; check it.

## Task

For **every** concept and **every** milestone kind, find the **earliest** real event that
fits the concept's **definition**:

| kind | meaning |
|---|---|
| `first_demonstration` | shown to work at all (working lab demo, prototype, published working system) |
| `first_practical_use` | used for its real purpose outside the lab (first service, deployment, product in use) |
| `mass_adoption` | ordinary people use it routinely (give the year it became common, with a source) |

Rules:

- **Fit the definition, don't stretch it.** Function and mechanism must match. A lab
  result that didn't work is not a demonstration; a loose analogue is not the thing.
  If a concept never became real, give it no milestone for that kind and say why in the
  concept note. It is fine, and common, to have no `mass_adoption`.
- **Earliest, not best-known.** For each kind, search explicitly for "first", "earliest",
  "pioneer", "history of" and for predecessors of the famous example (earlier
  prototypes, other countries, military or industrial uses). Before you settle, ask:
  is there an earlier event that fits? Say in `note` which earlier candidates you
  considered and why you rejected them.
- A `first_practical_use` cannot be earlier than the `first_demonstration`; if the
  same event is both, give both kinds with the same date.
- Dates as `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, only as precise as the sources.

## Sources (strict)

Each milestone needs 1–3 `sources`, each
`{"url", "publisher", "date", "title", "quote", "kind"}`:

- `kind`: `contemporary` (news report, paper or official document from the time of the
  event), `reference` (encyclopedia, museum, university, company or historian's page),
  or `wikidata` (one of the dated statements given to you in the input).
- `quote`: **at most 25 words copied exactly** from the text of a page you actually
  fetched, supporting the date or the event. **No quote, no source.** A search-result
  snippet is not a fetched page. Never paraphrase or invent. For a `wikidata` source the
  quote is the statement as given, e.g. `"inception: 1946-02-15"`, and the url is the
  item's URL.
- Check every non-Wikidata quote before you output it:
  `python3 -I scripts/page_text.py --check "<url>" "<quote>"` must print `FOUND`.
  If it doesn't, fix the quote from the page text or drop the source.
- A milestone with no remaining source is dropped.
- `date` is the source's publication date if known, else `""`.

How to read pages (all print to stdout; never save page text to files in the repo):

- Find pages with WebSearch (mode "standard").
- Read a page: `python3 -I scripts/page_text.py "<url>" "<term>" 1` prints the lines
  containing a term (with one line of context); without a term it prints the whole text
  (pipe through `head`/`grep`). It reads Wikipedia articles through the API, Chronicling
  America pages through their OCR, and most other HTML pages. WebFetch may also work;
  if you use it, still run the `--check`.
- Wikimedia sometimes answers 429 (rate limit); the helper retries by itself.
- **Contemporary newspapers before 1963:** `python3 -I scripts/chronam.py "words" 1945 1950 8`
  searches Chronicling America (slow: 30–70 s per query). Use it for the few milestones
  in your batch where a newspaper report would settle an early date (a few queries,
  not dozens). OCR text is messy: copy the quote exactly as the OCR has it.

## Confidence

Give each milestone `confidence`:

- `high`: the event clearly fits the definition, the date is supported by a contemporary
  source or by two independent sources that agree, and you searched for earlier events.
- `medium`: fits, one good reference source, earlier search done but not exhaustive.
- `low`: the fit or the date is uncertain, or an earlier event may well exist.

## Output

Write your result with the Write tool to `{batch_out}` (JSON lines, no prose, no code
fences). One line per milestone:

{"concept_id": "...", "kind": "first_demonstration", "date": "1946-02-15", "what": "one line: what happened, where, by whom", "sources": [{"url": "...", "publisher": "...", "date": "", "title": "...", "quote": "...", "kind": "reference"}], "confidence": "medium", "note": "earlier candidates considered and why rejected; how it fits the definition"}

then one line per concept (every concept in the batch, including those with no milestones):

{"concept_id": "...", "concept_note": "short: what changed from the first pass and why; why a kind has no milestone"}

and finally one line: {"_tools": "which tools worked (WebFetch? page_text? chronam?), anything that went wrong"}

Then check the file parses (`python3 -I -c "import json;[json.loads(l) for l in open('{batch_out}')]"`)
and reply with one short line: how many milestones and concepts you wrote. Do not edit any
other file.
