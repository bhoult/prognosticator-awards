# Review assist: is tier 2's confirmed milestone the earliest that fits? (review_confirmed_v1)

You are checking milestones for a project that scores old science-fiction predictions against
the date each idea first came true. For each concept a researcher (tier 2) looked for the
earliest real event of two kinds and, in these rows, **confirmed** the answer it was given:

- `first_demonstration`: the first time the thing was shown to work, even in a lab or a trial.
- `first_practical_use`: the first time it was used for its real purpose, outside a test.

A milestone is only right if the event is the thing the concept's **definition** describes:
its function and its mechanism, not a distant ancestor, a different technology that does a
similar job, or a literal reading of one word that misses what the concept means. An earlier
event that fits strictly beats a later one; an earlier event that is a stretch does not.

Your rows are in `{input}` (JSON lines). Each has the concept's `name`, `definition` and
`aliases`, the `kind`, and the confirmed milestone (`new`: date, event, fit, note, confidence,
the kinds of its sources), with `old` the same milestone as it stood before tier 2.

Read the file with the Read tool in chunks of 15 lines (`offset` 1, 16, 31, ...). For each row
decide, from what you know, one of:

- `accept`: the event fits the definition and kind, and you know of no clearly earlier event
  that fits as well.
- `earlier_exists`: you know a clearly earlier, well-documented event that fits the definition
  and kind strictly. Name it and its year.
- `does_not_fit`: the event is not what the definition describes (another technology, a
  precursor, the wrong kind). Say what would fit, if you know.
- `unsure`: you can't tell without a source. Say what would settle it.

Do not search the web or fetch pages; this is a reading review. Be strict: `accept` is the
default when you know of nothing better, and a vague memory is `unsure`, not `earlier_exists`.

Write one JSON line per input row, in input order, to `{output}`:

```
{{"concept_id": "...", "kind": "first_practical_use", "recommendation": "earlier_exists", "reason": "one or two sentences naming the event and its year"}}
```

Write the file after every chunk (rewrite it whole with the Write tool, or append), so that no
work is lost. When done, check it: `python3 -c "import json; r=[json.loads(l) for l in open('{output}')]; print(len(r))"`
must print {n}. Then reply with one line: how many of each recommendation.
