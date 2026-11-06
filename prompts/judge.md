# Judging, judge_v1 (full run, tranche A; runs/match/PLAN.md §7)

You decide how closely a passage from fiction or futurist writing anticipated something
that later became real. Work in `{workdir}` and run commands from there. Keep every file you
write (scripts, notes) in `{tmpdir}`, never in any other temporary or scratchpad directory:
other agents work in parallel and would overwrite them. Don't search the web, and don't use
outside knowledge of any book or author.

## Input

`{batch_in}`: {n} pairs, JSON lines `{"pair", "pub_year", "quote", "claim_description",
"polarity", "concept_name", "concept_description", "milestone_kind", "milestone_date",
"milestone_summary"}`. Each pair joins one passage (its quotation, a one-line summary another
model wrote, and the year it was first published) to one real development (a concept and the
milestone that dates it). The batch mixes pairs from many concepts.

Read the file with the Read tool in chunks of 50 lines (lines 1–50, 51–100, and so on to the
end). Read every quotation in full: don't print shortened lines or only some fields with a
script. A pair can only be scored on a quotation you have read.

## Scoring

Score each match from 0 to 1:

- 1.0: function, mechanism and context all match: what it does, how it works, and how
  people use it.
- 0.75: function and the key mechanism match; the context differs.
- 0.5: the function matches; the mechanism is vague, missing or different.
- 0.25: evocative: the passage points in the right direction but loosely.
- 0: not the same thing.

Rules:

- Judge only what the quotation says, not what the story might mean elsewhere. Don't reward
  a prediction for being famous.
- Compare the passage with the **real development** (the concept and its milestone), not
  with the concept's name alone. A passage about a superhuman thinking "electronic brain"
  matched to a 1945 calculating machine is at most 0.25: the function it claims is different.
- The summary line is a helper; when it and the quotation disagree, the quotation wins.
- Every milestone here is dated after the passage's year; take the date as given.
- If the passage is a translation of an ancient text, judge the plain meaning of the words,
  not the translator's modern vocabulary, and not readings from commentary, allegory,
  numerology or apologetic and polemical literature. A claim that matches only under such a
  reading scores 0.
- `polarity` `will_not` means the passage says the thing will never happen or can't be done.
  Score it the same way: how closely the passage is about this development, whatever it says
  about whether it will happen.
- Score each pair on its own; similar pairs may deserve different scores.
- Write a rationale that names what *that* quotation says. Never reuse a template sentence
  across pairs: a batch where more than a fifth of the rationales repeat is redone.

## Output

**Write as you go.** After each chunk of 50 pairs, write `{batch_out}` again with the Write
tool, holding every line so far. If the file already exists when you start, read it first and
continue with the pairs it lacks.

`{batch_out}` holds JSON lines only, one per pair, in input order, no prose and no code fences:

{"pair": "p3f2a9c41d0", "score": 0.5, "rationale": "Two sentences at most: what matches and what doesn't."}

`score` is one of 0, 0.25, 0.5, 0.75, 1. When all {n} lines are written, check the file
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{batch_out}')]))"` must
print {n}). Don't edit any other file, and don't run git. Reply with one short line: how many
pairs you scored, and how many at 0.75 or more.
