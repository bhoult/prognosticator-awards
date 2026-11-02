# Stage 1 extraction, 2026-11-02

**Setup**
- **Books:** 2,979: Gutenberg sci-fi with a known year, plus the 47 predictive texts in `lists/predictive-texts.txt`, minus the pilot's 20. 52,451,421 words in 9,419 passages of about 6,000 words, shuffled (seed 2026).
- **Run directory:** `work/extract/stage1-sonnet` (local only: passages are book text).
- **Two methods, recorded per passage** (`method` in each verified record):
  - **Subagents** (`pipeline/extract.py`, `prompts/extract_subagent.md`, sha256 `aa4fc1b87368…`): Claude Code Sonnet subagents on the Claude plan, 40,000-word batches. Batches 1–167.
  - **Batch API** (`pipeline/batch_api.py`, `prompts/extract_api.md`, sha256 `230ab05b1060…`): one Message Batches request per passage, `claude-sonnet-5-5` with thinking off (`between_tools`), paid from a $200 promotional API credit. Everything else.
- Because the passages were shuffled before batching, the two methods are spread evenly across books, not split book by book.

## Results

| | Subagents | Batch API | Stage 1 |
|---|---|---|---|
| Passages verified | 1,100 | 8,312 | 9,412 of 9,419 |
| Words | 6,177,066 | 46,232,822 | 52,409,888 of 52,451,421 |
| Claims | 11,359 | 104,039 | 115,398 |
| Claims per 10K words | 18.4 | 22.5 | 22.0 |
| Quotes found exactly | 11,311 | 100,226 | 111,537 |
| Quotes found at ≥ 90% similarity | 44 | 2,873 | 2,917 |
| Quotes rejected (not in the passage) | 4 (0.04%) | 940 (0.90%) | 944 |
| Claims with a field outside its allowed values | 144 (1.3%) | 5,651 (5.4%) | 5,795 |

- **Field problems:** `category` holding a domain value such as `economy` (5,317 claims), `voice` (395), `domain` (58), empty `description` (43). They are to be remapped when the claims are loaded into the database.
- **Rejected quotes** are mostly quotes that join separate pieces of text with "...", which the prompt forbids. Verification drops them.
- **Left for subagents:** 7 passages. Two were refused by the model (three refusals in all), and five replies had JSON typos (a stray quote after `false`, an escaped quote around a value, a line break inside a string).

## Gold-set check before the Batch API run

The same prompt rules, sent through the Batch API, were first scored on the gold set (`runs/sonnet-batch`; `runs/report.md`):

| | Sonnet subagents | Sonnet, Batch API |
|---|---|---|
| Claims | 501 | 661 |
| Recall of known predictions | 73% | 76% |
| Traps handled | 3/5 | 2/5 (also missed L3, an editorial introduction) |
| Quotes | 501 exact | 638 exact, 22 fuzzy, 1 rejected |
| Cost | Claude plan | $0.98 |

## Batch API usage

| | |
|---|---|
| Batches | 9 (1,000 passages to measure the rate, then 7,331), plus the gold set's 1 |
| Replies | 8,331 (8,328 complete, 3 refused) |
| Input tokens | 89.3M uncached; 7.9M read from the prompt cache; 30K written to it |
| Output tokens | 17.7M (2,127 per passage) |
| Cost at Batch API prices | $178.33, or $0.038 per 10K words (gold set: $0.98) |
| Time | 20 minutes from the first batch to the last result |

- **Tokens per word:** the Sonnet 5.5 tokenizer counted 2.05 tokens per word on these passages, prompt included (measured with the free token-counting endpoint before sending).
- **Stopped by the Console's usage limit:** a final 6-passage retry was refused with "You have reached your specified API usage limits", after $179.31 of tracked spend in all. Access returns on 2026-12-01, after the credit expires (2026-11-21).
- **Subagents, for comparison:** the 1,100 passages done by subagents took 24.1M tokens as Claude Code reports them, and 352 agent-minutes.
