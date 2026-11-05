# Propose concepts for the claims nothing matched (full matching run, tranche A, gap pass)

You are adding to a list of canonical concepts for a database of predictions made in old
science fiction and futurist writing. Each claim you read is a one-line summary of something a
text imagined. Every claim in your file was checked twice against the existing concepts and
matched none of them, though the matchers judged it a real prediction. A **concept** is the
real-world thing that many claims point to, at the level where one could date when it first
came true: "video telephone", "crewed Moon landing", "heart transplant". Not a whole field
("medicine", "space travel"), and not one story's gadget ("Professor Zarnak's red ray").

Work in `{workdir}` and run commands from there. Keep every file you write (scripts, notes)
in `{tmpdir}`, never in any other temporary or scratchpad directory: other agents work in
parallel and would overwrite them.

## Input

- `{shard_in}`: JSON lines `{"id", "description"}`, {n} claims from the domain group
  `{domain}`. Read the whole file with the Read tool, in parts of 300 lines, until the end.
- `{registry}`: the {n_concepts} concepts that already exist, JSON lines `{"concept_id",
  "name"}`. Read it all with the Read tool (lines 1–600, then the rest). Don't propose these
  again.

## Task

Propose the concepts that **at least 3 claims of this file** return to. Most of these claims
are one-off gadgets and need no concept: each concept gets milestone research later, so
propose only what recurs. Concepts that never came true are welcome (they are the "still
waiting" predictions). A claim that is a metaphor, or not a prediction at all, needs no
concept.

For each concept:

- `concept_id`: kebab-case, specific, unique, and not an id in `{registry}`.
- `name`: short.
- `definition`: one sentence saying what it does and how (its function and mechanism), so
  that someone can decide whether a real event fits it.
  **One function per concept.** If the definition joins alternatives that could have come
  true at different times ("a factory, mine or power plant"; "reads thoughts or displays
  them"), make two concepts. Alternatives of one thing ("holes in cards or tape") are fine.
- `type`: `technology` (a device, technique, material, medical or scientific achievement).
  If a concept is clearly an event or a social change instead, use `event` or `social`.
- `aliases`: the words the texts use for it.
- `came_true_guess`: `yes`, `no` or `unsure`: has something that fits the definition
  happened in the real world by 2026? Your best guess; it only decides how much research the
  concept gets.
- `est_claims`: about how many claims in this file it covers (3 or more).
- `examples`: up to 5 claim ids from this file that it covers.

## Output

Write with the Write tool to `{shard_out}`: JSON lines only, one concept per line, no prose,
no code fences:

{"concept_id": "video-telephone", "name": "Video telephone", "definition": "A telephone that sends a live picture of each caller along with the voice, so that people at a distance see each other as they talk.", "type": "technology", "aliases": ["televisor", "telephote", "vision phone"], "came_true_guess": "yes", "est_claims": 14, "examples": ["stage1-sonnet/p00012#3"]}

Write in parts: after every 300 claims read, rewrite the file with all concepts so far,
refining earlier ones as you learn more. At the end check that it parses
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{shard_out}')]))"`).
Don't edit any other file, don't search the web, and don't run git.

Reply with one line: how many concepts, and about what share of the claims they cover.
