# Milestone research, tier 2: the deciding milestones (full run, tranche A; runs/match/PLAN.md §5)

You are checking when technologies and scientific ideas that old science fiction and futurist
writing imagined first became real. Each concept below is a thing many old texts predicted,
and its milestone decides a large share of the ranking: points grow with the years between a
story and the milestone, so **a milestone dated too late gives stories credit they don't
deserve, and one that doesn't really fit the definition gives credit for the wrong thing**.
An earlier researcher dated each concept, mostly from Wikipedia and at low confidence. You are
the adversarial second check, with five concepts and time to dig.

Work in `{workdir}` and run every command from there. Keep every file you write (scripts,
notes) in `{tmpdir}`, never in any other temporary or scratchpad directory: other agents work
in parallel and would overwrite them.

## Input

`{batch_in}`: {n} concepts, JSON lines `{"concept_id", "name", "definition", "type", "aliases",
"milestones", "earlier_notes"}`. `milestones` holds the concept's current `first_demonstration`
and `first_practical_use` (each with `date`, `what`, `fit`, `sources`, `confidence`, `note`,
`searched`); `earlier_notes` are the earlier researchers' notes on the concept. Read them as
leads, not verdicts.

## Task

For each concept, check both kinds:

| kind | meaning |
|---|---|
| `first_demonstration` | shown to work at all (working lab demonstration, prototype, published working system) |
| `first_practical_use` | used for its real purpose outside the lab (first service, deployment, product in use) |

Ask three questions of each given milestone:

1. **Does it strictly fit?** Function *and* mechanism must match the concept's **definition**,
   and the concept as its name gives it. A proposal, a patent, a design study, or a lab attempt
   that did not work is not a demonstration; a fictional, staged or hoax event is not an
   event; a toy or stage trick is not a practical use unless the definition allows it. A
   loose, partial or stand-in event is not a milestone.
2. **Is there an earlier event that strictly fits?** Search hard past the famous example:
   "first", "earliest", "history of", "pioneer", "invented", predecessors of the named event,
   other countries, and military, industrial, police, medical and institutional uses. Don't
   stretch the definition to reach an earlier date.
3. **Can you back it with a contemporary source?** A report from the time (a magazine,
   newspaper, paper or official document published within two years of the event) is what this
   tier is for. Make a real attempt for every milestone you keep or give, and say in `searched`
   what you tried.

Then:

- If the milestone is right, **confirm** it: same event (you may make the date more precise).
  Keep its sources if their quotes still check, and add a contemporary one if you find it.
- If an earlier event fits, or the given one doesn't fit and another (earlier or later) does,
  **replace** it with that event and its sources.
- If the given one doesn't fit and nothing else does, **remove** it, with the reason.
- **Demonstration only.** When a concept has a `first_demonstration` but no
  `first_practical_use`, decide which case it is. A fact about the world (a discovery:
  what lies under Jupiter's clouds, whether Mars has canals) has no practical use; say so in
  the concept note. A technology whose practical use was missed: search for that use, and if
  you find one that strictly fits, **add** it.
- **Events and social changes** (`type` `event` or `social`): `first_practical_use` is when it
  first actually happened.
- **Denials.** A concept that says something will never happen or does not exist comes true
  only when that is confirmed. If it was refuted instead, remove the milestone and name the
  refuting event and date in the note.
- A `first_practical_use` cannot be earlier than the `first_demonstration`; if one event is
  both, give both kinds with the same date.
- In `note`, name every earlier candidate you considered and why each was rejected (or why the
  replacement fits). A bare "confirmed" with no candidates named is not a check.
- Dates as `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, only as precise as the sources. Nothing else in
  the field: no "c.", ranges or words. A year BC takes a minus sign (`-0602`).

**Effort (tier 2):** about 12–20 tool calls per concept, and never more than 25 fetches on one.
Work through the concepts in order and finish each before the next.

## Sources

Each kept, replaced or added milestone needs 1–3 `sources`, each `{"url", "publisher", "date",
"title", "quote", "kind"}`.

- `kind: "contemporary"` **only** for a source published within two years of the event (its
  `date` must show that); otherwise `kind: "reference"` (encyclopedia, museum, agency history
  page, retrospective article, book). `high` confidence needs a contemporary and a reference
  source that agree; `medium` needs at least one source that names the event and its date
  directly; otherwise `low`.
- `quote`: **at most 25 words copied exactly** from the text `pipeline/sources.py` printed for
  that URL, supporting the date or the event. **No quote, no source.** A search-result snippet
  is not a fetched page. Never paraphrase or invent. OCR text is messy: copy it as printed (the
  check ignores whitespace, case, curly quotes and OCR soft hyphens `¬`).
- **Check every quote before you write it:**
  `python3 -I pipeline/sources.py check "<url>" "<quote>"` must print `FOUND`. If it doesn't,
  fix the quote from the page text or drop the source. For archive.org, NTRS, Crossref,
  Semantic Scholar and PubMed Central the check also prints the record's date: use it as the
  source's `date`. Every quote is checked again in code afterwards; one that fails drops, and a
  milestone with no surviving source falls back to the earlier researcher's.
- `date` is the source's publication date (`YYYY`, `YYYY-MM` or `YYYY-MM-DD`), else `""`.

## Routes to contemporary sources

- **Wikipedia's own citations.** The fastest route from a Wikipedia-only milestone to a
  contemporary source: print the article's wikitext and its citations with
  `python3 -I pipeline/sources.py text "https://en.wikipedia.org/w/index.php?title=<Title>&action=raw" "cite"`
  (each `{{cite ...}}` shows the cited work's `url`, `date`, `journal` or `newspaper`, and
  `doi`). Then fetch the cited page itself and quote from it; never quote the wikitext. A dead
  link may still be on the Wayback Machine (`https://web.archive.org/web/<url>`). A DOI reads
  through Crossref (`https://api.crossref.org/works/<doi>`).
- **archive.org full-text search** of scanned magazines, newspapers, and NASA and DTIC reports:
  `python3 -I pipeline/sources.py search '"exact phrase"' 1950 1959 10 [collection]` prints item
  URLs, years, titles and snippets; read the item with `text` and copy the quote from there.
  Search the years around the event, with the words a report of the time would use. Hits in
  fiction, yearbooks and children's books are not evidence. A lending-library book
  (`inlibrary`) gives no text; for one, the source URL may be the search restricted to that
  item, `https://archive.org/services/search/beta/page_production/?user_query=%22<phrase>%22+AND+identifier:<id>&service_backend=fts`,
  whose snippets the check reads.
- NASA NTRS: `python3 -I pipeline/sources.py text "https://ntrs.nasa.gov/api/citations/search?q=<words>" | head -c 3000`.
- **WebSearch** (mode "standard") finds pages. If it fails or reports that its budget is used
  up, don't stop: keep going with the routes above, and say so in the `_tools` line.

## Tools

Everything prints to stdout; never save page text to files.

- **Read a page:** `python3 -I pipeline/sources.py text "<url>" "<term>" [chars]` prints each
  place the term occurs with context (default 300 characters); without a term it prints the
  whole text (pipe it through `head`). It reads Wikipedia (through its API), archive.org items
  (`https://archive.org/details/<id>`), PDFs (any URL ending `.pdf`), NASA NTRS records
  (`https://ntrs.nasa.gov/citations/<id>`), Crossref, Semantic Scholar
  (`https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>`), PubMed Central
  (`https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/`) and ordinary HTML pages. Don't use
  WebFetch to read a source: it rewrites the page, so quotes taken from it fail the check.
- **Refuse scripted access here (checked 2026-11-05), so don't use them:** Britannica,
  HathiTrust, loc.gov (Chronicling America), newspapers.com, nytimes.com, science.org,
  sciencedirect.com, IEEE Xplore, worldradiohistory.com and Google Books (its API is out of
  quota). If any other site refuses (403, captcha, "Just a moment", login wall, a 429 that
  does not clear), move on. **Never change the User-Agent, never pretend to be a browser,
  never work around a block.**

## Output

**Write as you go.** After you finish each concept, write `{batch_out}` again with the Write
tool, holding every line so far, so that finished concepts are never lost. If the file already
exists when you start, read it first and continue with the concepts it lacks.

`{batch_out}` holds JSON lines only (no prose, no code fences). For each concept, one line for
**each milestone in its input** (`checked` is `confirmed`, `replaced` or `removed`), one line for
each kind you add (`checked`: `added`), then the concept's note:

{"concept_id": "...", "kind": "first_practical_use", "checked": "replaced", "date": "1972-11", "what": "one line: what happened, where, by whom", "fit": "one sentence: how the event matches the definition's function and mechanism", "sources": [{"url": "...", "publisher": "...", "date": "1972-12", "title": "...", "quote": "...", "kind": "contemporary"}], "confidence": "medium", "note": "the earlier candidates considered and why each was rejected, or why the replacement fits", "searched": "what you searched and where, including the contemporary-source attempt"}

{"concept_id": "...", "kind": "first_demonstration", "checked": "removed", "note": "why it doesn't fit, and what else was considered", "searched": "..."}

{"concept_id": "...", "concept_note": "short: what changed and why; for a demonstration-only concept, whether it is a discovery or a technology whose use was searched for"}

and finally one line: {"_tools": "which tools and hosts worked or failed (say whether WebSearch worked), anything that went wrong"}

Then check that the file parses (`python3 -I -c "import json;[json.loads(l) for l in open('{batch_out}')]"`)
and reply with one short line: how many milestones you confirmed, replaced, removed and added.
Don't edit any other file, and don't run git.
