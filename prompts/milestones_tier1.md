# Milestone research, tier 1 (full run, tranche A; runs/match/PLAN.md §5)

You are researching when technologies and scientific ideas that old science fiction and
futurist writing imagined first became real. Each concept below is a thing many old texts
predicted; your dates decide how far ahead of reality those texts were, so the date must be
the **earliest real event that strictly fits the definition**, backed by a page you fetched.

Work in `{workdir}` and run every command from there. Keep every file you write (scripts,
notes) in `{tmpdir}`, never in any other temporary or scratchpad directory: other agents work
in parallel and would overwrite them.

## Input

`{batch_in}`: {n} concepts, JSON lines `{"concept_id", "name", "definition", "type",
"aliases", "came_true_guess"}`. `came_true_guess` is an earlier guess whether it ever came
true (`yes` or `unsure`); check it, don't trust it. The concepts share a domain, so searches
and sources often serve several of them.

## Task

For **every** concept and **every** milestone kind, find the **earliest** real event that
**strictly fits** the concept's **definition**:

| kind | meaning |
|---|---|
| `first_demonstration` | shown to work at all (working lab demonstration, prototype, published working system) |
| `first_practical_use` | used for its real purpose outside the lab (first service, deployment, product in use) |
| `mass_adoption` | ordinary people use it routinely (the year it became common) |

- **Fit.** Function *and* mechanism must match the definition. Every milestone gets `fit`:
  one sentence on how the event matches the definition's function and mechanism. If only a
  loose analogue exists, give **no milestone** for that kind and say so in the concept note.
  A concept with no milestone at all is a fine answer. A proposal, a patent, a design study
  or a lab attempt that did not work is not a demonstration; a fictional, staged or hoax event
  is not an event.
- **Discoveries.** When the concept is a fact about the world rather than something built
  (what lies under Jupiter's clouds, whether a planet has life, how lunar craters formed),
  `first_demonstration` is the first observation or measurement that established it; the
  other kinds don't apply.
- **Events and social changes** (`type` `event` or `social`): `first_practical_use` is when
  it first actually happened; `mass_adoption` when it became widespread, if that applies.
- **Denials.** A concept that says something will never happen or does not exist comes true
  only when that is confirmed (the Moon has no life: the first missions that established it).
  If it was refuted instead (aircraft did fly), give no milestone and name the refuting
  event and its date in the concept note.
- **Earliest, strictly fitting.** For each kind, look past the famous example: search for
  "first", "earliest", "pioneer", "history of", predecessors, other countries, and military,
  industrial and institutional uses. In `note`, name the earlier candidates you considered
  and why each was rejected; in `searched`, what you searched and where.
- A `first_practical_use` cannot be earlier than the `first_demonstration`; if one event is
  both, give both kinds with the same date. `mass_adoption` only if it happened.
- Dates as `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, only as precise as the sources. Nothing else in
  the field: no "c.", ranges or words.

**Effort (tier 1):** about 8–12 tool calls per concept, and never more than 15 fetches on
one. One verified source per milestone is enough; a second, contemporary one is better when
you find it quickly. A sourced reference milestone is better than none.

## Sources

Each milestone needs 1–3 `sources`, each `{"url", "publisher", "date", "title", "quote", "kind"}`.

- **Prefer contemporary sources** when you can find them quickly: a magazine, newspaper,
  paper or official document from the year of the event (archive.org's scanned magazines,
  papers through Crossref or PubMed Central, NASA reports). `kind: "contemporary"` **only**
  for a source published within two years of the event (its `date` must show that);
  otherwise `kind: "reference"` (encyclopedia, museum, agency history page, retrospective
  article, book). `high` confidence needs a contemporary and a reference source that agree.
- `quote`: **at most 25 words copied exactly** from the text `pipeline/sources.py` printed for
  that URL, supporting the date or the event. **No quote, no source.** A search-result
  snippet is not a fetched page. Never paraphrase or invent. OCR text is messy: copy it as
  printed (the check ignores whitespace, case, curly quotes and OCR soft hyphens `¬`).
- **Check every quote before you write it:**
  `python3 -I pipeline/sources.py check "<url>" "<quote>"` must print `FOUND`. If it doesn't,
  fix the quote from the page text or drop the source. For archive.org, NTRS, Crossref,
  Semantic Scholar and PubMed Central the check also prints the record's date: use it as the
  source's `date`. Every quote is checked again in code afterwards; one that fails drops.
- `date` is the source's publication date (`YYYY`, `YYYY-MM` or `YYYY-MM-DD`), else `""`.

## Tools

Everything prints to stdout; never save page text to files.

- **Find pages** with WebSearch (mode "standard").
- **Read a page:** `python3 -I pipeline/sources.py text "<url>" "<term>" [chars]` prints each
  place the term occurs with context (default 300 characters); without a term it prints the
  whole text (pipe it through `head`). It reads Wikipedia (through its API), archive.org items
  (`https://archive.org/details/<id>`: the OCR text, date from the metadata), PDFs (any URL
  ending `.pdf`), NASA NTRS records (`https://ntrs.nasa.gov/citations/<id>`), Crossref
  (`https://api.crossref.org/works/<doi>`), Semantic Scholar
  (`https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>`), PubMed Central
  (`https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/`) and ordinary HTML pages (museum, agency,
  university and magazine sites). Don't use WebFetch to read a source: it rewrites the page,
  so quotes taken from it fail the check.
- **Full-text search of scanned magazines and books (archive.org)**, the best route to
  contemporary sources:
  `python3 -I pipeline/sources.py search '"exact phrase"' 1950 1959 10 [collection]` prints
  item URLs, years, titles and short snippets; then read the item with `text` and copy the
  quote from there. Leave out the collection as a rule: the search then covers the scanned
  periodicals (`sim_*` microfilm: Motor Trend, Science Digest, trade journals), newspapers,
  and NASA and DTIC reports; `computerworld` and `byte-magazine` are useful collections for
  computing. Hits in fiction, yearbooks and children's books are not evidence. A lending-library book
  (`inlibrary`) gives no text; for one, the source URL may be the search restricted to that
  item, `https://archive.org/services/search/beta/page_production/?user_query=%22<phrase>%22+AND+identifier:<id>&service_backend=fts`,
  whose snippets the check reads.
- NASA NTRS search: `python3 -I pipeline/sources.py text "https://ntrs.nasa.gov/api/citations/search?q=<words>" | head -c 3000`.
- **Refuse scripted access here (checked 2026-11-05), so don't use them:** Britannica,
  HathiTrust, loc.gov (Chronicling America), newspapers.com, nytimes.com, science.org,
  sciencedirect.com, IEEE Xplore, worldradiohistory.com and Google Books (its API is out of
  quota). If any other site refuses (403, captcha, "Just a moment", login wall, a 429 that
  does not clear), move on. **Never change the User-Agent, never pretend to be a browser,
  never work around a block.**

## Output

**Write as you go.** After you finish each concept, write `{batch_out}` again with the Write
tool, holding every line so far, so that finished concepts are never lost. If the file
already exists when you start, read it first and continue with the concepts it lacks.

`{batch_out}` holds JSON lines only (no prose, no code fences). One line per milestone:

{"concept_id": "...", "kind": "first_demonstration", "date": "1985-10", "what": "one line: what happened, where, by whom", "fit": "one sentence: how the event matches the definition's function and mechanism", "sources": [{"url": "...", "publisher": "...", "date": "1985-10-07", "title": "...", "quote": "...", "kind": "contemporary"}], "confidence": "medium", "note": "earlier candidates considered and why each was rejected", "searched": "what you searched and where"}

then one line per concept (every concept in the batch, including those with no milestone):

{"concept_id": "...", "concept_note": "short: why a kind has no milestone; for a denial that was refuted, the refuting event and date"}

and finally one line: {"_tools": "which tools and hosts worked or failed, anything that went wrong"}

Then check that the file parses (`python3 -I -c "import json;[json.loads(l) for l in open('{batch_out}')]"`)
and reply with one short line: how many milestones and concepts you wrote. Don't edit any
other file, and don't run git.
