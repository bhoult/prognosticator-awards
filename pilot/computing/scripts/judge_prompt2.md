# Judging prompt, second pass (computing pilot, RUN2 step 5)

This is `prompts/judge.md` (judge_v0) applied in batches, with the amendments made in the
first pass. Work in `/home/user/prognosticator-awards/pilot/computing/`. Do not search the
web or use outside knowledge of any book. Each batch mixes pairs from many concepts.

Read the whole batch file `{batch}` (JSON lines; read it in chunks until the end). Each
line is one pair: `pair`, `pub_year`, `quote`, `claim_description`, `concept_name`,
`concept_description`, `milestone_kind`, `milestone_date`, `milestone_summary`.

## Instructions (from judge_v0)

You decide how closely a passage from fiction anticipated something that later became
real. You are given the passage's quotation, a one-line summary of what it imagines, the
year it was first published, and a real-world development with the date it happened.

Score the match from 0 to 1:

- 1.0: function, mechanism and context all match: what it does, how it works, and how
  people use it.
- 0.75: function and the key mechanism match; the context differs.
- 0.5: the function matches; the mechanism is vague, missing or different.
- 0.25: evocative: the passage points in the right direction but loosely.
- 0: not the same thing.

Judge only what the quotation says, not what the story might mean elsewhere. Do not
reward a prediction for being famous. If the real development existed before the year
of publication, score 0 and say so.

Two clarifications for this pilot:

- Compare the passage with the **real development** (concept + milestone), not with the
  concept's name alone. A passage about a superhuman thinking "electronic brain" matched
  to a 1945 calculating machine is at most 0.25: the function claimed is different.
- The summary line is a helper written by another model; when it and the quotation
  disagree, the quotation wins.

Score each pair independently; similar pairs may deserve different scores.

Read every quotation in full and
write a rationale that names what *that* quotation says. Never reuse a template sentence
across pairs; a batch where many rationales are identical is rejected.

## Output

Write your result with the Write tool to `{batch_out}`: only JSON lines, one per pair, in
input order, no prose and no code fences:

{"pair": "q0001", "score": 0.5, "rationale": "Two sentences at most: what matches and what doesn't."}

`score` must be one of 0, 0.25, 0.5, 0.75, 1. Output exactly as many lines as the batch has pairs.

Then check that the file parses and has one line per input pair
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{batch_out}')]))"`),
and reply with one short line. Do not edit any other file.
