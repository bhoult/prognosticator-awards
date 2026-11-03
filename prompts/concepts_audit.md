# Audit the concept registry (full matching run, tranche A)

The registry of concepts was built by several agents. Each concept will get one dated
milestone, the first real event that fits its definition, and every claim matched to it is
scored against that date. Two kinds of mistake would give wrong dates:

- **Over-merged:** two things joined into one concept that came true at different times (or
  one came true and the other never did). Examples: stealth aircraft (1980s) and an
  invisibility cloak (not yet); a military bunker (1910s) and an underground city; a laser
  weapon on a ship (2014) and a handheld disintegrator (never).
- **Bundled definitions:** one definition that lists alternatives with different first dates
  ("laser, heat ray or disintegrator"; "a factory, mine or power plant").

**The test:** would one real event date both halves within about ten years? If not, they
are separate concepts. Alternatives of one thing ("holes in cards or tape"), or things that
have both never happened and are the same idea (life on Mars and life on Jupiter's moons are
both "native life on other worlds"), may stay together.

Work in `{workdir}` and run commands from there. If you write helper scripts, keep them in
`{tmpdir}` (other agents work in parallel).

## Input

- `{merges}`: JSON lines, one cross-domain merge per line: `keep` and `drop`, each with its
  `concept_id`, `name` and `definition`.
- `{concepts}`: JSON lines, the concepts to check for bundles: the 200 largest, and every
  one with a `bundle_check` note.

Read both files to the end, in chunks.

## Output

Write with the Write tool to `{out}`: JSON lines only, no prose, one decision per line:

- A merge that fails the test, wholly or for some of its `drop` concepts:
  `{"op": "reject_merge", "keep": "<id>", "drop": ["<id>", ...], "reason": "..."}`
  (the listed `drop` concepts stay separate; any other `drop` of that merge stays merged).
- A bundled concept to split:
  `{"op": "split", "concept_id": "<id>", "into": [{"concept_id", "name", "definition", "type", "came_true_guess"}, ...], "reason": "..."}`
  Each new concept has one function and its own definition (one sentence, what it does and
  how). The new ids must not already be in use.

Write nothing for merges and concepts that pass. Write in parts as you go (rewrite the file
with everything so far). At the end check that it parses
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{out}')]))"`). Don't
edit any other file, don't search the web, and don't run git. Reply with one line: how many
merges rejected (wholly or partly) and how many concepts split.
