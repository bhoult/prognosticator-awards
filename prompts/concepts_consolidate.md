# Consolidate concepts (full matching run, tranche A)

Several agents each read a random sample of claims from the domain `{domain}` and proposed
concepts. Their lists overlap. Your job is to turn them into one clean list for the domain.
A **concept** is a real-world thing many predictions point to, at the level where one could
date when it first came true ("video telephone", "heart transplant"): not a whole field, and
not one story's gadget.

Work in `{workdir}` and run commands from there.

## Input

- `{proposals}`: JSON lines, the proposals of every sample of this domain, each with `shard`,
  `concept_id`, `name`, `definition`, `type`, `aliases`, `came_true_guess`, `est_claims` and
  `examples` (claim ids). Read the whole file, in chunks, until the end.
- `{registry}`: concepts that already exist (`concept_id`, `name`, `definition`).

## Rules

1. **Merge** proposals that are the same concept (the same function and mechanism) into one.
   Keep the clearest id, name and definition; join the aliases; add up `est_claims`; keep up
   to 3 examples. List every proposal merged in `merged_from`, as `"<shard>:<concept_id>"`.
2. **Existing concepts:** a proposal that is the same as an existing concept is not kept as a
   new one. Write it as `{"concept_id": "<existing id>", "existing": true, "merged_from":
   [...]}` so that its claims are mapped there.
3. **Split bundles:** a definition names one function. When it joins alternatives that could
   have come true at different times ("a factory, mine or power plant"; "reads thoughts or
   displays them"), make separate concepts and list the original in `split_from`.
   Alternatives of one thing ("holes in cards or tape") are not bundles.
4. **Too broad** (a whole field): replace it with the specific concepts its examples need, or
   drop it. **Too narrow:** merge it into the concept it belongs to.
5. For every concept you keep, `bundle_check`: `"ok"`, or a short note if it might still join
   two things you decided to keep together.
6. Each definition is one sentence on what it does and how, precise enough to decide whether
   a real event fits.

## Output

Write with the Write tool to `{out}`: JSON lines only, one concept per line, no prose, no
code fences. Fields: `concept_id`, `name`, `definition`, `type`, `aliases`,
`came_true_guess`, `est_claims`, `examples`, `merged_from`, `split_from` (only if split),
`bundle_check`, and `domains` (`["{domain}"]`). Every proposal must appear in exactly one
`merged_from` or `split_from`, unless you dropped it; list dropped ones as
`{"dropped": "<shard>:<concept_id>", "reason": "..."}`.

Write in parts as you go (rewrite the file with everything so far). At the end check that it
parses (`python3 -I -c "import json;print(len([json.loads(l) for l in open('{out}')]))"`).
Don't edit any other file, don't search the web, and don't run git. Reply with one line:
how many concepts, how many merged, split and dropped.
