# Gold set

A small, fixed sample used to compare models and to regression-test prompts.

| File | What it is |
|---|---|
| `texts.json` | the 14 known-prediction texts (with first-publication years) and the rule for 3 random books |
| `answer_key.json` | 38 entries: known predictions (realized or failed) and traps (already-existing technology, later introductions), each anchored to an exact phrase |
| `chunks/` | what a model reads: `cNNN.txt` = year + blanked passage (author, title and story headings replaced by […]) |
| `chunks.jsonl` | private map from chunk id to text and character range |
| `anchors.jsonl` | each answer-key entry with the chunk and offset of its anchor |
| `batches.json` | chunk ids grouped into one batch per subagent, identical for every model |

Rebuild with `python -I pipeline/gold.py gold` (deterministic; seed in `texts.json`).
`chunks/` is book text, some of it in copyright, so it is never committed (`.gitignore`); rebuild it locally.
Score a run with `python -I pipeline/evaluate.py gold runs` (needs `rapidfuzz`).

Matching rule: an answer-key entry counts as found when a verified claim (its
quote located in the chunk, exactly or ≥ 90% fuzzy) falls within the anchor's
paragraph, ±300 characters. A trap is handled when no such claim exists or every
such claim is marked `speculative_at_time: false`.
