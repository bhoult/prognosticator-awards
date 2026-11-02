# Sonnet extraction pilot, 2026-11-02

**Setup**
- **Driver:** `pipeline/extract.py`; run directory `work/extract/pilot-sonnet` (local only).
- **Prompt:** `prompts/extract_subagent.md`, sha256 `aa4fc1b87368…`.
- **Model:** Claude Code general-purpose subagents, `model: sonnet`, the same launch method as the gold run.
- **Books:** 20 random Gutenberg sci-fi books (seed 2026), all with a known year and none from the gold set. 467,633 words in 83 passages and 13 batches.
- **Waves:** two, to test restarting. After the first 7 batches, `next` listed only the remaining 6.

## Results

| | Pilot | Gold set, Sonnet |
|---|---|---|
| Claims | 1,025 | 501 |
| Claims per 10K words | 21.9 | 23.6 |
| Quotes found in the passage | 1,024 / 1,025 (1,022 exact, 2 fuzzy) | 100% |
| Claims written into the wrong passage's file | 0 | 0 |
| Claims with a field outside its allowed values | 17 (1.7%): `category` set to a domain value | – |
| Marked not speculative | 3 | – |

The one rejected quote: "Graed Garroway's cruel empire" (p00050).

## Usage

| | 13 subagents (pilot) | Gutenberg sci-fi stage, scaled ×115.7 (3,234 books, 54.1M words) |
|---|---|---|
| Subagents | 13 | about 1,500 |
| Tokens, as Claude Code reports them (final context per subagent) | 1.91M (38K–48K per 10K words) | 221M (range 208M–258M) |
| API calls | 134 | about 15,500 |
| Prompt-cache writes | 1.80M | about 208M |
| Prompt-cache reads | 11.33M | about 1.31B |
| Output tokens | 0.26M | about 31M |
| Agent time | 30 agent-minutes; 107–193 s per subagent | about 57 agent-hours: 8–11 h of wall-clock time at 7 subagents in parallel |

Claude Code's notification figure matches the gold run's measure: the gold Sonnet run used 0.88M tokens for 212,553 words, or 41K per 10K words. How the plan's usage limits count cache reads, compared with writes and output, isn't visible from here.

## Before Stage 1

- **Orchestration is the limit, not tokens.** The pilot ran in two waves launched by hand from the main session. At about 1,500 subagents, that would be around 215 waves, and every launch and notification would land in the orchestrating conversation. Stage 1 needs a scripted orchestrator, or several sittings.
- **`next` lists batches that are still running.** It lists every batch that isn't verified, including ones being read at that moment. An orchestrator that calls it mid-wave would need a claim marker for each batch, or a `--batch N` option.
- **Usage limits will set the wall-clock time.** Cache reads in the billions will likely hit the 5-hour and weekly usage windows more than once. `/usage-guard` pauses when less than 10% of a limit is left and resumes after the reset.
- **Fix wrong field values when loading the database.** The 17 claims with a domain value in `category` can be remapped then, with no re-run.

## Caveats

- **The scaling factor is rough.** 20 books is about 0.9% of the stage. The range per batch was narrow (38K–48K per 10K words), though, because each batch is a fixed 40K words.
- **The passage year is the year in the file name.** That is the magazine date or the Open Library first-publication year, not ISFDB. `speculative_at_time` relies on it, so the ISFDB dating pass is still needed before scoring.
