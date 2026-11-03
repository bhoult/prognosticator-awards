# Pilot: concepts, milestones, matching and judging for the computing claims

You are running a pilot of the second half of the Prognosticator Awards pipeline (read `README.md`, then `DESIGN.md` §5–§8 and `prompts/judge.md` before starting). The extraction is finished; this pilot takes one subject, computing, through the rest of the design, so that the method can be fixed before it runs on all 92K claims. A useful pilot is one whose report says clearly what worked, what didn't and what it cost.

**Input:** `pilot/computing/claims.jsonl`: 2,656 claims from public-domain books (1627–2012), one per line: `id`, `year` (first publication of the book), the verbatim `quote`, a one-line `description`, and the extraction fields. Authors and titles are deliberately absent; don't try to find them, and don't let a quotation's fame affect a score.

**Work on this branch and push after every step**, so nothing is lost if the session stops. All outputs go in `pilot/computing/`. Use the Agent tool with `model: "sonnet"` for the bulk work (research, matching, judging). Spend at most **40 subagents in total**; if you would need more, shrink the scope (fewer concepts, only specificity ≥ 3) rather than exceed it, and say so in the report. Keep a log of every subagent (purpose, tokens, seconds) in `pilot/computing/usage.tsv`.

## Steps

1. **Concepts** → `concepts.jsonl`, one per line: `concept_id` (kebab-case), `name`, `definition` (one sentence: what it does and how), `wikidata` (QID or null), `aliases`. Seed from Wikidata where you can (items with an invention, discovery, inception or first-occurrence date: P575, P571, P606, P1619…; use the public SPARQL endpoint with a descriptive User-Agent), and from the claims themselves: read the descriptions and propose the concepts they keep returning to (computers, thinking machines, robots, networks, databases, automated government, surveillance, machine translation, and so on). Aim for 60–150 concepts that together cover most claims. Concepts that never came true are allowed: they are the "still waiting" predictions.
2. **Milestones** → `milestones.jsonl`: for each concept, up to three dated milestones as in DESIGN §6 (`first_demonstration`, `first_practical_use`, `mass_adoption`), each with `date` (YYYY, or YYYY-MM-DD), a one-line `what`, and `sources`: a list of `{url, publisher, date, title, quote}` with quotes of at most 25 words. Follow the evidence hierarchy (contemporary report, then a reference source); for this pilot, reliable reference sources are fine, but record which kind each source is. Never store article text. A concept with no real-world milestone gets none.
3. **Matching** → `matches.jsonl`: each claim mapped to at most two concept ids, or to none, with a one-line reason. Give subagents batches of claims plus the full concept list; ask for JSON lines only.
4. **Judging** → `judgments.jsonl`: for every match whose concept has a `first_practical_use` milestone (or, failing that, a `first_demonstration`), score the claim against that milestone with the rubric in `prompts/judge.md` (0, 0.25, 0.5, 0.75, 1), with a one-line rationale. Blind: the judge sees the quote, the description, the year and the milestone, nothing else. A milestone dated before the claim's year scores 0.
5. **Report** → `report.md`:
   - **Counts:** claims, concepts, milestones, matched and unmatched claims, and the score distribution.
   - **Best predictions:** the 20 best by score × log2(1 + years of lead time), with year, quote, concept, milestone and score.
   - **Quality:** a hand-check of 30 random judgments, with how many you would change.
   - **Problems found**, cost (subagents and tokens) and time.
   - **Recommendations** for the full run: concept seeding, batch sizes, prompt changes, and whether the judge needs Opus.

## Rules

- Don't change anything outside `pilot/computing/`. In particular, leave the extraction data, `pipeline/` and `prompts/` alone; put any scripts you write under `pilot/computing/scripts/`.
- Every output is JSON lines, valid and parseable; check them with a short script before each push.
- If something in the design turns out not to work, do the simplest thing that does, and write it down in the report.
