# Gold-set extraction run, 2026-11-01

Three Claude Code subagent models, each given the same 6 batches (37 chunks, 212,553
words, 17 texts) and the same prompt (`runs/<model>/batch_<n>.md`). Scored by
`pipeline/evaluate.py`; full numbers in `report.md` / `report.json`.

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| Claims recorded | 444 | 501 | 1,137 |
| Claims per 10K words | 20.9 | 23.6 | 53.5 |
| Quotes found in the text | 100% | 100% | 100% |
| Claims written into the wrong chunk's file | 104 (23%) | 0 | 0 |
| Recall, strict (quote overlaps the anchor sentence) | 55% (18/33) | 73% (24/33) | 82% (27/33) |
| Field checks (will_not, hedged, stated date) | 2/3 | 5/5 | 5/5 |
| Traps handled (pre-existing tech, later introductions) | 3/5 | 3/5 | 3/5 |
| Claims marked not speculative | 14 | 14 | 107 |
| Subagent tokens, all 6 batches | 1.04 M | 0.88 M | 1.34 M |
| Time per batch | 2–5 min | 1.5–3.5 min | 10–21 min |

Findings:

1. **No invented quotes from any model.** Every quote was located in the text,
   so the hallucination guard (verbatim quotes, checked by code) works.
2. **Haiku misfiles when given several files.** A quarter of its claims landed
   in a neighbouring passage's file. The evaluator repairs this by searching
   the other chunks in the batch, but the full run should put the passage id
   inside each chunk file, or give Haiku one passage per call. Given two
   chunks in the smoke test, Haiku found every known prediction in them; with
   six or seven per batch it skimmed (15 Watkins claims, against 88).
3. **Strict recall understates every model.** The misses that all three share
   (atomic bombs, Verne's Florida site and aluminium shell, Forster's video
   calls) were captured by quoting a different sentence about the same idea:
   Sonnet, for instance, recorded "the possibilities of atomic energy that
   Holsten had opened for mankind". Concept-level recall needs the judge
   stage.
4. **Opus is the most thorough, Sonnet the most efficient.** Opus finds the
   most and splits finely (2.3× Sonnet's claims), and is the only model to use
   `speculative_at_time: false` often. Sonnet matches Opus on field accuracy
   with 0.66× the tokens and about a sixth of the time.
5. **Two traps fooled every model**, and both are debatable. Wells's motor
   trucks "already in evidence" (he is predicting their spread, which arguably
   is speculative) and Bacon's submarines (Drebbel's 1620 boat is obscure).
   The trap set needs clearer cases before it can separate models.
6. **Subagent overhead dominates.** Haiku used about as many tokens as Sonnet,
   because each subagent re-reads its instructions and writes long JSON. With
   subagents, Haiku saves usage only to the extent the plan weights its tokens
   lower.

Scale: the gold set is about 1/880 of the sci-fi corpus (187 M words), so a
full Sonnet pass through subagents would be on the order of 800 M subagent tokens.
