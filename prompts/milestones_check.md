# Quick check: did any of these ever come true? (full run, tranche A; runs/match/PLAN.md §5)

Each concept below is a thing old science fiction and futurist writing imagined, which an
earlier pass guessed has **never** come true. Your job is a quick check of that guess: has
any real event, by 2026, fit the concept's definition? The concepts you find a fitting event
for get full milestone research afterwards; the rest are recorded as not come true. A wrong
"none" loses a prediction that came true, so check each one; a wrong "fits" only costs a
second look.

Work in `{workdir}` and run commands from there. Keep every file you write (scripts, notes)
in `{tmpdir}`, never in any other temporary or scratchpad directory: other agents work in
parallel and would overwrite them.

## Input

`{batch_in}`: {n} concepts, JSON lines `{"concept_id", "name", "definition", "type",
"aliases", "came_true_guess"}`.

## Rules

- **Fits** means a real event matches the definition's function *and* mechanism: a working
  demonstration, a real use, or (for a fact about the world) an observation that established
  it. A proposal, a patent, a design study, a failed attempt, fiction, a hoax or a loose
  analogue doesn't fit.
- **Denials.** A concept that says something will never happen or does not exist fits only
  if that was confirmed (the Moon has no life: established by the first missions); if it
  was refuted, it is `none`, and the note names the refuting event.
- Use your knowledge first, then WebSearch (mode "standard") for anything you are not sure
  of: one to three searches per concept is enough. No sources are needed here.

## Output

Write with the Write tool to `{batch_out}`: JSON lines only, one per concept, in input
order, no prose and no code fences:

{"concept_id": "...", "verdict": "fits", "event": "what happened, where, when (the earliest you know)", "note": "why it fits the function and mechanism"}
{"concept_id": "...", "verdict": "none", "event": "", "note": "the closest real thing, and why it doesn't fit"}

Write the file again after every 10 concepts, holding every line so far; if it already
exists when you start, read it first and continue with the concepts it lacks. Then check it
(`python3 -I -c "import json;print(len([json.loads(l) for l in open('{batch_out}')]))"` must
print {n}). Don't edit any other file, and don't run git. Reply with one line: how many fit.
