# Matching prompt (computing pilot)

You map predictions from old fiction to canonical technology concepts. Do not edit any
files; return your results as text.

1. Read the concept list `{concepts}` (one per line: `concept_id | name | definition`).
2. Read the claims `{batch}` (JSON lines: `id`, `year`, `quote`, `description`). Read the
   whole file, in chunks if needed.

For **every** claim, choose **at most two** concepts that the claim actually imagines,
judged by the definition (what it does and how), or none:

- Match the thing the claim is about, not background scenery. "The ship's computer
  plotted the course" is `spacecraft-guidance-computer`, not also
  `electronic-digital-computer`. Use `electronic-digital-computer` only when the claim is
  about computers as such (size, speed, being built, what computers in general do).
- Prefer the more specific concept when two fit; give a second concept only when the
  claim really imagines two different things.
- Use `[]` when nothing fits: generic plot events, metaphors, statements about
  characters, or technologies outside the list. Do not force a match.
- Do not use outside knowledge of the book or author; judge the words given.

Output **only** JSON lines, one per claim, in input order, no prose and no code fences:

{"id": "<claim id, copied exactly>", "concepts": ["concept-id"], "reason": "one line"}

You must output exactly as many lines as there are claims in the batch file.
