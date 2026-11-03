# Propose concepts (full matching run, tranche A)

You are building part of a list of canonical concepts for a database of predictions made in
old science fiction and futurist writing. Each claim you read is a one-line summary of
something a text imagined. A **concept** is the real-world thing that many claims point to,
at the level where one could date when it first came true: "video telephone", "crewed Moon
landing", "heart transplant", "jet airliner". Not a whole field ("medicine", "space travel"),
and not one story's gadget ("Professor Zarnak's red ray").

Work in `{workdir}` and run commands from there.

## Input

- `{shard_in}`: JSON lines `{"id", "description"}`, {n} claims from the domain `{domain}`,
  a random sample. Read the whole file, in chunks of 300 lines, until the end.
- `{registry}`: concepts that already exist, JSON lines `{"concept_id", "name",
  "definition"}`. Don't propose these again; a claim that fits one is covered.

## Task

Propose the concepts that these claims keep returning to, so that together with the existing
ones they cover at least 90% of the claims. A typical concept covers 10–25 claims of this
file; one with a single claim is fine only if it is a distinct thing that could be dated.
Concepts that never came true are welcome (time travel, faster-than-light travel,
invisibility): they are the "still waiting" predictions. A claim that is a metaphor, or not
a prediction at all, needs no concept.

For each concept:

- `concept_id`: kebab-case, specific, unique.
- `name`: short.
- `definition`: one sentence saying what it does and how (its function and mechanism), so
  that someone can decide whether a real event fits it.
  **One function per concept.** If the definition joins alternatives that could have come
  true at different times ("a factory, mine or power plant"; "reads thoughts or displays
  them"), make two concepts. Alternatives of one thing ("holes in cards or tape") are fine.
- `type`: `technology` (a device, technique, material, medical or scientific achievement).
  If a concept is clearly an event or a social change instead, use `event` or `social`; those
  are handled later.
- `aliases`: the words the texts use for it.
- `came_true_guess`: `yes`, `no` or `unsure`: has something that fits the definition
  happened in the real world by 2026? Your best guess; it only decides how much research the
  concept gets.
- `est_claims`: about how many claims in this file it covers.
- `examples`: up to 3 claim ids from this file that it covers.

## Output

Write with the Write tool to `{shard_out}`: JSON lines only, one concept per line, no prose,
no code fences:

{"concept_id": "video-telephone", "name": "Video telephone", "definition": "A telephone that sends a live picture of each caller along with the voice, so that people at a distance see each other as they talk.", "type": "technology", "aliases": ["televisor", "telephote", "vision phone"], "came_true_guess": "yes", "est_claims": 14, "examples": ["stage1-sonnet/p00012#3"]}

Write in parts: after every 300 claims read, rewrite the file with all concepts so far,
refining earlier ones as you learn more. At the end check that it parses
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{shard_out}')]))"`).
Don't edit any other file, don't search the web, and don't run git.

Reply with one line: how many concepts, and about what share of the claims they cover
together with the existing ones.
