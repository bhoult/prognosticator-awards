# Pilot, second pass: milestones from real sources

The first pass ([`report.md`](report.md)) worked end to end, but its milestone dates came only from web-search summaries: the environment blocked Wikidata, Wikipedia and the newspaper archives. Some dates were decades late, and because points grow with lead time, late milestones went straight to the top of the ranking. This session runs in an environment that should allow those sites. Its job is to redo the milestones from real sources, check the dates that decide the ranking, and re-score only what changes.

Read `report.md`, `DESIGN.md` §6–§8 and `prompts/judge.md` first. `claims.jsonl` now also has `book`, an opaque book id (no author or title), for counting each book once.

**Work on this branch and push after every step.** Outputs go in `pilot/computing/` with a `2` in the name; leave the first-pass files (`concepts.jsonl`, `milestones.jsonl`, `matches.jsonl`, `judgments.jsonl`, `report.md`) unchanged. Use the Agent tool with `model: "sonnet"` for the research and judging. Spend at most **25 subagents** in total, and log each (purpose, tokens, seconds) in `usage2.tsv`. Scripts go in `scripts/`.

## Steps

1. **Check the network** before anything else: a Wikidata SPARQL query (`https://query.wikidata.org/sparql`, with a descriptive User-Agent), the Wikipedia API (`https://en.wikipedia.org/w/api.php`), and Chronicling America (`https://chroniclingamerica.loc.gov/search/pages/results/?andtext=...&format=json`). Record which work in `report2.md`. If Wikidata and Wikipedia are both blocked, stop: write that in `report2.md`, push, and end.
2. **Wikidata** → `concepts2.jsonl` (the concepts unchanged, with `wikidata` filled in where an item truly matches the definition) and `raw/wikidata_dates.jsonl`. For each concept, find candidate items (`wbsearchentities`), keep only one that matches the concept's definition, and fetch its dated statements (P575 discovery or invention, P571 inception, P1619 official opening, P606 first flight, P580 start time, and any other date that fits). Do this in code, not with subagents.
3. **Milestones** → `milestones2.jsonl`: the same fields as `milestones.jsonl`, plus `confidence` (`high`, `medium`, `low`). Each source now has `kind` (`contemporary`, `reference` or `wikidata`) and a `quote` of at most 25 words copied exactly from a page the agent actually fetched; no quote, no source. For every concept and every milestone kind, look for the **earliest** event that fits the concept's definition. Don't stretch the definition (a lab result that didn't work is not a demonstration), and don't settle for the best-known event. Give each research subagent 10–15 concepts, the Wikidata dates from step 2, and the first-pass milestone with the reason it was doubted, if any.
4. **Earliest-event check.** For every milestone in `milestones2.jsonl` that gives any matched claim more than 40 years of lead (claims from `matches.jsonl`, years from `claims.jsonl`), a separate subagent asks: is there an earlier event that fits this definition? It confirms the date or replaces it, with sources. Record the outcome in the milestone (`checked: "confirmed" | "replaced"`).
5. **Re-score** → `judgments2.jsonl`: all the first-pass pairs, updated. Where the milestone's date and description are unchanged, copy the first-pass judgment. Where the new milestone is in or before the claim's year, score 0 by rule. Otherwise re-judge with the judge prompt as amended in the first pass (the quotation wins over the summary; mixed concepts in each batch; no template sentences). Pairs for concepts that gained a milestone are judged for the first time.
6. **Report** → `report2.md`:
   - What the network allowed.
   - How many milestone dates changed, earlier and later: the 30 largest changes with old and new dates, and the source for each new one.
   - The new top 20 by `score × log2(1 + lead years)`, **counting each book once** (its best claim per concept).
   - How the ranking moved compared with the first pass.
   - Which milestones are still doubtful, and why.
   - Cost and time.

## Rules

- Don't change anything outside `pilot/computing/`, and don't edit the first-pass files.
- Every output is JSON lines, valid and parseable; check them before each push.
- Never store article text; quotes of at most 25 words only.
- If a step can't be done as written, do the simplest thing that works and say so in the report.
