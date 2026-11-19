# Did a "never" come true? (negative_check_v1)

A project scores old predictions against the date each idea came true. Some passages say that a thing
will **not** happen, cannot be done, or is impossible. Each row in `{input}` (JSON lines) is such a
passage (`quote`, written in `pub_year`, with the extractor's one-line `claim_description`), paired with
an idea from the project's list (`concept_name`, `concept_definition`) and the dated event that made the
idea come true (`milestone_date`, `milestone`).

The pipeline counted every row as a skeptic proved wrong. That is right only if the passage denies the
very thing the milestone shows happening. Decide for each row, from the words of the quote:

- `contradicted`: the passage says the thing will not or cannot happen (or will never be seen, made,
  reached), and the milestone is that thing happening. The skeptic was proved wrong.
- `vindicated`: the passage's negative statement turned out true, or the milestone confirms what the
  passage said (it denied a popular belief that was in fact false, say).
- `unrelated`: the passage denies something else, or is not a prediction of the future (a character's
  opinion about the story's own world, a statement about the past, a joke).

Read the file with the Read tool in chunks of 20 lines (`offset` 1, 21, 41, ...). Do not search the web.
Write one JSON line per row, in input order, to `{output}`:

```
{{"id": "...", "verdict": "contradicted", "reason": "one sentence"}}
```

Write the file after every chunk, so no work is lost. When done, check it:
`python3 -c "import json; r=[json.loads(l) for l in open('{output}')]; print(len(r))"` must print {n}.
Then reply with one line: how many of each verdict.
