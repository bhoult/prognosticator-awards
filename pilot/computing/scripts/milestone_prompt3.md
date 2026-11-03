# Milestone research prompt, third pass (computing pilot, RUN3 step 3)

You are researching when computing technologies first became real. Work in
`/home/user/prognosticator-awards/pilot/computing/` (run every command from there).

Your concepts are in `{batch_in}` (JSON lines). Each line has `concept_id`, `name`,
`definition`, `aliases`, `realizable` (the concept list's guess whether it ever came true),
`earliest_claim_year` (the earliest story matched to the concept: a milestone date only
matters for stories published before it), `milestones2` (the second pass's milestones,
with their sources and notes), `doubt` (why the second pass is doubted, if it is) and
`search_hints` (things you must search explicitly, if any).

**Leads** (if `{leads}` is given): quotes that an earlier agent on this batch had already
checked as FOUND before the container restarted and its work was lost. They are leads,
not results: use them if they fit, re-check them, and don't rely on them alone.

**The second pass is not the answer; check it.** It rests almost entirely on Wikipedia
(the only site that worked then). Some of its dates are too late (it settled for the
best-known or only quotable event), some stretch the definition, and five concepts
(`milestones2` empty) lost their milestone only because no page could be fetched.

## Task

For **every** concept and **every** milestone kind, find the **earliest** real event that
**strictly fits** the concept's **definition**:

| kind | meaning |
|---|---|
| `first_demonstration` | shown to work at all (working lab demo, prototype, published working system) |
| `first_practical_use` | used for its real purpose outside the lab (first service, deployment, product in use) |
| `mass_adoption` | ordinary people use it routinely (the year it became common) |

Rules:

- **Fit.** Function *and* mechanism must match the definition. Every milestone gets
  `fit`: one sentence on how the event matches the definition's function and mechanism.
  If only a loose analogue exists, give **no milestone** for that kind and say so in the
  concept note. A concept with no milestone at all is fine. Test cases: decoding
  attempted or imagined *speech* is not displaying *thoughts*; reconstructing an image a
  person is *seeing* is not reading their memories or thoughts; a static hologram is not
  a display of changing images; a concert piece driven by EEG is a borderline BCI (say
  why you accept or reject it). A lab result that did not work is not a demonstration;
  a proposal or a patent is not a demonstration.
- **Earliest, strictly fitting.** For each kind, search for "first", "earliest",
  "pioneer", "history of", predecessors of the famous example, other countries,
  military, industrial and institutional uses. In `note`, name the earlier candidates you
  considered and why each was rejected (or why it replaced the second pass). In
  `searched`, say explicitly what you searched and where (sites, queries, years) —
  especially for every item in `search_hints`.
- A `first_practical_use` cannot be earlier than the `first_demonstration`; if one event
  is both, give both kinds with the same date.
- Dates as `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, only as precise as the sources.
- If a site refuses (403, captcha, "Just a moment", login wall, 429 that does not clear),
  move on. **Never change the User-Agent, never pretend to be a browser, never work around
  a block.**

## Sources: prefer contemporary ones

Each milestone needs 1–3 `sources`, each
`{"url", "publisher", "date", "title", "quote", "kind"}`.

- **Prefer contemporary sources**: a magazine, newspaper, paper or official document
  from the year of the event. `kind: "contemporary"` **only** for a source published
  within two years of the event (its `date` must show that). Otherwise `kind:
  "reference"` (encyclopedia, museum, agency history page, retrospective article, book).
- A milestone with a contemporary source **and** a reference source that agree may be
  `high`.
- `quote`: **at most 25 words copied exactly** from the text of a page you actually
  fetched with the helper, supporting the date or the event. **No quote, no source.**
  A search-result snippet is not a fetched page. Never paraphrase or invent. OCR text is
  messy: copy it exactly as the helper prints it (the check ignores whitespace, case,
  curly quotes and OCR soft hyphens `¬`).
- Check every quote before you output it:
  `python3 -I scripts/page_text3.py --check "<url>" "<quote>"` must print `FOUND`. If it
  doesn't, fix the quote from the page text or drop the source. For archive.org,
  NTRS, Crossref and Semantic Scholar the check also prints the record's date: use it
  as the source's `date`.
- `date` is the source's publication date (`YYYY`, `YYYY-MM` or `YYYY-MM-DD`), else `""`.

## Tools

All print to stdout; **never save page text to files in the repository**.

- **Full-text search of scanned magazines and books (archive.org)** — the best route to
  contemporary sources:
  `python3 -I scripts/ia_search3.py '"exact phrase"' 1980 1989 10 [collection]`
  prints item URLs, years, titles and short snippets. Collections worth trying:
  `computerworld` (weekly, 1967–), `infoworld`, `byte-magazine`, `popular-science-magazine`
  (or none: `sim_*` periodical microfilm, DTIC and NASA reports are also indexed). Most
  hits in children's books and games are fiction: ignore them. Library-lending books
  (`inlibrary`) give 403 when read: skip them.
- **Read a page or item**: `python3 -I scripts/page_text3.py "<url>" "<term>" [chars]`
  prints each place a term occurs with context (default 300 characters), in
  whitespace-flattened text; without a term it prints everything (pipe through `head`).
  It reads Wikipedia (API), archive.org items (`https://archive.org/details/<id>`, the
  OCR text; date from metadata), PDFs (bitsavers.org, worldradiohistory.com, NTRS
  downloads: any URL ending `.pdf`), NASA NTRS records (`https://ntrs.nasa.gov/citations/<id>`),
  Crossref (`https://api.crossref.org/works/<doi>`), Semantic Scholar
  (`https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>`; often 429, retries itself)
  and ordinary HTML (computerhistory.org, ethw.org, spectrum.ieee.org, nasa.gov,
  airandspace.si.edu, pubmed/pmc, aip.org, hagley.org, thehenryford.org, nobelprize.org,
  *.mit.edu, …).
- NASA NTRS search: `https://ntrs.nasa.gov/api/citations/search?q=<words>` (JSON; read it
  with `curl -s -A "prognosticator-awards-pilot/0.3"` piped to python, or the helper).
- Find pages with WebSearch (mode "standard").
- **Not available (checked at the start of this run):** Google Books (the API's shared
  daily quota is exhausted: 429; books.google.com answers 404), HathiTrust, Smithsonian
  Magazine and www.si.edu (403 challenge pages), nature.com (redirects to a blocked
  login host; use Crossref for Nature papers), IEEE Xplore (202 bot check), Britannica
  (403). Don't use them.

## Output

**Write as you go.** The container can restart and lose an agent's work (it happened to the
first three agents of this step). After you finish each concept, write the file
`{batch_out}` again with the Write tool, holding every line so far (the concept's milestone
lines and its concept_note line), so that finished concepts are never lost. If the file
already exists when you start, read it first and continue with the concepts it lacks.

`{batch_out}` holds JSON lines only (no prose, no code fences). One line per milestone:

{"concept_id": "...", "kind": "first_demonstration", "date": "1985-10", "what": "one line: what happened, where, by whom", "fit": "one sentence: how the event matches the definition's function and mechanism", "sources": [{"url": "...", "publisher": "...", "date": "1985-10-07", "title": "...", "quote": "...", "kind": "contemporary"}], "confidence": "medium", "note": "earlier candidates considered and why each was rejected; agreement with or difference from the second pass", "searched": "what you searched and where"}

then one line per concept (every concept in the batch, including those with no milestone):

{"concept_id": "...", "concept_note": "short: what changed from the second pass and why; why a kind has no milestone"}

and finally one line: {"_tools": "which tools and hosts worked or failed, anything that went wrong"}

Then check the file parses (`python3 -I -c "import json;[json.loads(l) for l in open('{batch_out}')]"`)
and reply with one short line: how many milestones and concepts you wrote. Do not edit any
other file.

Budget: about 3–4 concepts per hour of work is fine, but don't spend more than ~20 fetches
on one concept; a sourced reference milestone is better than none.
