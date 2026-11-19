# Review assist: does tier 2's new milestone fit its concept? (review_assist_v1)

You are checking milestone changes for a project that scores old science-fiction predictions
against the date each idea first came true. For each concept a researcher (tier 2) looked for
the earliest real event of two kinds and sometimes replaced the earlier answer:

- `first_demonstration`: the first time the thing was shown to work, even in a lab or a trial.
- `first_practical_use`: the first time it was used for its real purpose, outside a test.

A milestone is only right if the event is the thing the concept's **definition** describes:
its function and its mechanism, not a distant ancestor, a different technology that does a
similar job, or a literal reading of one word that misses what the concept means. An earlier
date that fits strictly is better; an earlier date that is a stretch is worse than a later date
that fits. A date the researcher inferred or bounded is weaker than one a source gives.

Your rows are in `{input}` (JSON lines). Each has the concept's `name`, `definition` and
`aliases`, the `kind`, the `old` milestone (before tier 2; may be null when tier 2 added the
kind) and the `new` one (tier 2's answer, with its fit, note, confidence and the kinds of its
sources; `new` is null when tier 2 removed the milestone).

Read the file with the Read tool in chunks of 15 lines (`offset` 1, 16, 31, ...). For each row
decide, from what you know, one of:

- `accept`: the new milestone fits the definition and kind at least as well as the old one,
  and its date is credible.
- `keep_previous`: the new milestone is a stretch (another technology, a precursor, a literal
  reading, the wrong kind) or less credible than the old one, and the old one fits.
- `unsure`: neither is clearly right, or the question needs a source you don't have. Say what
  would settle it.

Do not search the web or fetch pages; this is a reading review. Do not try to find another date
yourself, but name a clearly better-known earlier or later event in the reason when you know one.

Write one JSON line per input row, in input order, to `{output}`:

```
{{"concept_id": "...", "kind": "first_practical_use", "recommendation": "keep_previous", "reason": "one or two sentences: why, naming the event that fits"}}
```

Write the file after every chunk (rewrite it whole with the Write tool, or append), so that no
work is lost. When done, check it: `python3 -c "import json; r=[json.loads(l) for l in open('{output}')]; print(len(r))"`
must print {n}. Then reply with one line: how many of each recommendation.
