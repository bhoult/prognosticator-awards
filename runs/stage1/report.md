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
| Passages verified | 1,101 | 8,318 | 9,419 of 9,419 |
| Words | 6,183,089 | 46,268,332 | 52,451,421 |
| Claims | 11,363 | 104,093 | 115,456 |
| Claims per 10K words | 18.4 | 22.5 | 22.0 |
| Quotes found exactly | 11,315 | 100,277 | 111,592 |
| Quotes found at ≥ 90% similarity | 44 | 2,876 | 2,920 |
| Quotes rejected (not in the passage) | 4 (0.04%) | 940 (0.90%) | 944 |
| Claims with a field outside its allowed values | 144 (1.3%) | 5,653 (5.4%) | 5,797 |

- **Field problems:** `category` holding a domain value such as `economy` (5,319 claims), `voice` (395), `domain` (58), empty `description` (43). They are to be remapped when the claims are loaded into the database.
- **Rejected quotes** are mostly quotes that join separate pieces of text with "...", which the prompt forbids. Verification drops them.
- **Retries:** 7 passages had no usable reply the first time: two refusals, and five replies with JSON typos (a stray quote after `false`, an escaped quote around a value, a line break inside a string). A second request succeeded for six of them after the spend limit was raised.
- **p01439,** refused twice through the API, was done by a subagent in the cloud session (below): 4 claims.

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
| Batches | 10 (1,000 passages to measure the rate, then 7,331, then a 6-passage retry), plus the gold set's 1 |
| Replies | 8,337 (8,334 complete, 3 refused) |
| Input tokens | 89.4M uncached; 7.9M read from the prompt cache; 31K written to it |
| Output tokens | 17.7M (2,127 per passage) |
| Cost at Batch API prices | $178.45, or $0.038 per 10K words (gold set: $0.98) |
| Time | 20 minutes from the first batch to the last result |

- **Tokens per word:** the Sonnet 5.5 tokenizer counted 2.05 tokens per word on these passages, prompt included (measured with the free token-counting endpoint before sending).
- **The organization's $100 monthly spend limit** is checked when a batch is created, not while it runs: the 7,331-passage round was sent at $21.56 and finished at $178.33. The retry round was refused ("You have reached your specified API usage limits") until the limit was raised. The Console's figure for the month, $179.29, matches the tracked $179.31 (gold set included).
- **Subagents, for comparison:** the 1,100 passages done by subagents took 24.1M tokens as Claude Code reports them, and 352 agent-minutes.

## Stage 1b: the books that had no year

The 259 Gutenberg sci-fi books the library had no year for were dated from ISFDB (`runs/dating/report.md`) and planned as their own run, `work/extract/stage1b-sonnet`, with those years in the passage headers: 981 passages, 5,599,014 words.

| | |
|---|---|
| Through the Batch API, $18 budget | 836 passages, 4,753,583 words, $17.95 ($0.038 per 10K words) |
| Claims | 10,239 (21.5 per 10K words) |
| Quotes | 9,805 exact, 337 at ≥ 90% similarity, 97 rejected |
| Claims with a field outside its allowed values | 484 |
| By subagents in a cloud session | 145 passages, 845,431 words, 1,266 claims |
| All | 981 passages, 11,505 claims |

## Stage 1c, and the cloud session

Stage 1c is the 10 books dated by the final version of the dating pass (*A Connecticut Yankee in King Arthur's Court*, *The Mummy!*, eight magazine issues): 115 passages, 681,623 words, in `work/extract/stage1c-sonnet`. The *Works of Lucian* volumes wait for ancient-text dating.

The last 261 passages (p01439 from Stage 1, the 145 left in Stage 1b, all of Stage 1c) were run in a Claude Code cloud session, paid from a cloud-session credit. The passages, all from Project Gutenberg books, went into a temporary private GitHub repository with the subagent prompt (`prompts/extract_subagent.md`, unchanged) and a run sheet; the session ran 44 Sonnet subagents, one per batch, and pushed the result files, which were then verified here as usual.

| | Cloud subagents |
|---|---|
| Passages | 261 (1,533,077 words) |
| Claims | 2,390 (15.6 per 10K words) |
| Quotes | 2,380 exact, 10 at ≥ 90% similarity, 0 rejected |
| Claims with a field outside its allowed values | 12 |
| Tokens, as Claude Code reports them | 6.17M for 44 subagents |

## Totals

| | Passages | Words | Claims |
|---|---|---|---|
| Stage 1 | 9,419 | 52,451,421 | 115,456 |
| Stage 1b | 981 | 5,599,014 | 11,505 |
| Stage 1c | 115 | 681,623 | 1,120 |
| All | 10,515 | 58,732,058 | 128,081 |
