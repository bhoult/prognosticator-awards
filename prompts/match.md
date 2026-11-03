# Match claims to concepts (full matching run, tranche A)

Each claim is a quotation from old science fiction or futurist writing, with a one-line
summary of it that another model wrote. Your job is to say which real-world **concepts**
each claim predicts, from a fixed list.

Work in `{workdir}` and run commands from there. If you write helper scripts, keep them in
`{tmpdir}` (other agents work in parallel).

## Input

- `{registry}`: the concepts for the domain `{domain}`, JSON lines `{"concept_id", "name",
  "definition"}`. Read it all.
- `{batch_in}`: {n} claims, JSON lines `{"id", "quote", "description"}`. Read it in two
  parts: lines 1–{half}, then the rest.

## Rules

1. **Match on the quotation.** The description only helps you understand it. When the
   quotation doesn't support the description, go by the quotation.
2. A claim matches a concept when the quotation imagines that thing: what it does, even if it
   works differently. At most two concepts; most claims have one.
3. Take the most specific concept that fits. Don't match on a shared word, and don't stretch a
   concept's definition to cover a claim.
4. **No match** gets a code instead:
   - `no_concept`: a real prediction of something the list doesn't have;
   - `untestable`: a metaphor, a feeling, a private or spiritual state, or anything that
     can't be checked against the world;
   - `too_vague`: too general to tie to any one thing ("science will work wonders").
5. `quote_carries`: `true` if the quotation by itself shows the prediction, `false` if it only
   makes sense with the description.
6. `reason`: at most 12 words about *this* claim, not a template.

## Output

Write with the Write tool to `{batch_out}`: JSON lines only, one per claim, in input order, no
prose and no code fences:

{"id": "stage1-sonnet/p00012#3", "concepts": ["video-telephone"], "reason": "caller's face appears on a screen during the call", "quote_carries": true, "code": null}
{"id": "stage1-sonnet/p00012#4", "concepts": [], "reason": "a sense of cosmic dread, not a device", "quote_carries": true, "code": "untestable"}

Write the first part's lines as soon as you have read it; at the end, rewrite the file with
all {n} lines. Then check it (`python3 -I -c "import json;print(len([json.loads(l) for l in
open('{batch_out}')]))"` must print {n}). Don't edit any other file, don't search the web,
and don't run git. Reply with one line: how many claims matched, and how many of each code.
