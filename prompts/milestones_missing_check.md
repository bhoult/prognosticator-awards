# Review assist: has a concept with no milestone come true? (missing_check_v1)

You are checking concepts for a project that scores old science-fiction predictions against
the date each idea first came true. Earlier researchers found **no milestone** for the concepts
in your file: they judged that the idea has not happened yet, or found no dated event. Some of
those are right (faster-than-light travel), and some may be misses. Your reading flags the
misses for a later, sourced research pass.

Two kinds of milestone count:

- `first_demonstration`: the first time the thing was shown to work, even in a lab or a trial.
- `first_practical_use`: the first time it was used for its real purpose, outside a test.

A milestone is only right if the event is the thing the concept's **definition** describes:
its function and its mechanism, not a distant ancestor, a different technology that does a
similar job, or a literal reading of one word that misses what the concept means.

Your rows are in `{input}` (JSON lines). Each has the concept's `name`, `definition`,
`aliases`, `type`, the researchers' guess whether it came true, and their `notes`.

Read the file with the Read tool in chunks of 15 lines (`offset` 1, 16, 31, ...). For each row
decide, from what you know, one of:

- `never_happened`: nothing that strictly fits the definition has happened.
- `happened`: a well-documented event strictly fits. Give the earliest you know: its `kind`, its
  `year`, and the `event` in one line.
- `unsure`: something close exists but may not fit, or you can't place it. Say what it is.

Do not search the web or fetch pages; this is a reading review. Be strict: a partial or
metaphorical match (a drug that calms is not mind control) is `never_happened` or `unsure`.

Write one JSON line per input row, in input order, to `{output}`:

```
{{"concept_id": "...", "recommendation": "happened", "kind": "first_demonstration", "year": 1966, "event": "one line: what, where, by whom", "reason": "one sentence: why it fits the definition"}}
```

(`kind`, `year` and `event` only for `happened`.) Write the file after every chunk (rewrite it
whole with the Write tool, or append), so that no work is lost. When done, check it:
`python3 -c "import json; r=[json.loads(l) for l in open('{output}')]; print(len(r))"` must
print {n}. Then reply with one line: how many of each recommendation.
