# Prognosticator Awards: design draft

Status: draft for discussion, 2026-11-01. Nothing here has been run yet.

The award ranks authors and texts by how much of the future they got right.
Science fiction is the core, but the corpus is any text that makes predictions:
scripture and prophecy, futurist essays and forecasts, newspaper "the year 2000"
pieces, interviews. For every text we extract the technologies, events and social
changes it imagined, match them to the dated real-world events that fulfilled
them, score how closely each one was predicted, and weight it by how far ahead
of the event it was published. The results are an open database and a ranked
list.

The pipeline is built so that the parts that decide the ranking are
rule-based and reproducible. Models do the reading and the judging; code does
the verifying, dating and arithmetic.

```
library .md files
   │
   ├─ 1. corpus      which books count, and when each was FIRST published
   ├─ 2. chunk       chapter-sized pieces with stable ids and offsets
   ├─ 3. extract     model lists every speculative claim, with a verbatim quote
   ├─ 4. verify      code checks every quote is really in the text  ← rejects hallucinations
   ├─ 5. concepts    claims map to canonical ideas ("video telephone")
   ├─ 6. evidence    each realized idea gets dated milestones + a news source
   ├─ 7. judge       model scores claim ↔ concept closeness 0–1, blind to author
   └─ 8. score       code: points = closeness × lead-time weight → rankings
```

---

## 1. Corpus

**Which books.** The genre folders are not enough: *The War of the Worlds* and
Jules Verne are filed under `Classics`, and Gutenberg's early SF is mixed in
with adventure fiction. The corpus is every book in the library that matches a
speculative-fiction title in [ISFDB](https://www.isfdb.org) (the Internet
Speculative Fiction Database), plus the `Science-Fiction*` folders. Current
size: about 4,700 books, 187 M words:

| Source | Books | Words |
|---|---|---|
| `Science-Fiction*` folders (Kindle library) | 1,412 | ~121 M |
| Project Gutenberg sci-fi (downloading now) | ~3,300 | ~66 M |
| SF filed under other genres | to be found via ISFDB | |

**Tie-in novels.** 874 of the 1,412 Kindle sci-fi books are Doctor Who, Star
Trek or Star Wars novels. Their technology belongs to the franchise, not the
novelist, and was usually invented decades earlier on screen. Default: tag them
`tie_in` and leave them out of the main ranking (they can have their own
table).

**First publication date: the field everything depends on.** Lead time is
measured from when the idea first appeared in print. The years in the library
are edition dates (Calibre gives *The Wee Free Men* as 2004; the Kindle files are
mostly 2000s reprints), and many SF stories ran in magazines years before the
book. ISFDB records the first appearance of each title, including magazine
serializations. We use that, and store its source. Before republishing ISFDB
data, check ISFDB's license terms.

> **Done for the Gutenberg sci-fi books (2026-11-02):** `pipeline/isfdb.py` and
> `pipeline/dating.py` match each book to ISFDB (2026-10-31 backup; CC BY 4.0) by
> title and author and take the work's earliest year, checked against the
> transcriber's "produced from <magazine>" notes. 3,175 of 3,234 matched; 165
> library years change, mostly to the first printing of a reprinted story.
> Result: `lists/gutenberg-sf-dates.tsv`; report: `runs/dating/report.md`.

### 1a. Religious and ancient texts

Scripture and other ancient texts are in the corpus too. They are already in
the library:

| Text | Edition in library |
|---|---|
| Bible | King James Version |
| Tanakh | JPS 1917 |
| Quran | Pickthall 1930 |
| Bhagavad Gita | Arnold 1885 |
| Upanishads | Müller 1879 |
| Rig Veda | Griffith 1896 |
| Book of Mormon | 1830 |
| Analects | Legge 1861 |
| Tao Te Ching | |
| Dhammapada | |
| Pali suttas | |
| Kojiki | Chamberlain 1882 |
| Apocrypha, Dead Sea Scrolls, Egyptian Book of the Dead | inside the *Holy Books Compendium* |

Nostradamus's *Prophecies* (1555) is the obvious companion if a "prophecy"
group is wanted. Four rules differ from fiction:

**The unit is the individual book, not the anthology.** Genesis, Daniel and
Revelation were written centuries apart, so each biblical book (and each
Upanishad, each Pali sutta collection) is its own `work`, with a parent work
for the anthology.

**Dates come from a curated table, using the latest date scholars allow.**
There is no first-publication date. Each text gets a scholarly composition
range and its traditional date, both with a citation. Lead time is measured
from the **end** of the scholarly range: a prediction only counts from the
latest point the text could have been written.

**Source: each book's English Wikipedia article** (decided 2026-11-02). The
article is pinned to the revision read, and the permalink
(`https://en.wikipedia.org/w/index.php?oldid=<revision>`) is saved in
`works.date_citation`, so anyone can see exactly what the range came from. It
is one public source that covers every tradition, and its articles summarize
the scholarly consensus with citations. When an article gives several
scholarly ranges, the one it presents as the consensus is used. Examples (to
be checked against those articles):

| Text | Range used | Lead-time date |
|---|---|---|
| Rig Veda | c. 1500–1200 BCE | 1200 BCE |
| Daniel | 6th century BCE (traditional) / c. 165 BCE (scholarly) | 165 BCE |
| Revelation | c. 95 CE | 95 CE |
| Quran | 610–632 CE | 632 CE |
| Kojiki | 712 CE | 712 CE |
| Book of Mormon | published 1830 | 1830 |

This also handles prophecies written after the event (*vaticinium ex
eventu*). If the scholarly date falls after the event, L ≤ 0 and the claim
scores nothing. The traditional date is stored but not scored, and a
`date_basis` setting can switch to it for comparison.

**We read translations, so a match must survive a second one.** A 1930
translation can use modern words the original didn't imply. Any claim scoring
0.5 or higher is re-judged against the same verse in an independent
translation, and the lower of the two scores is used:

- Quran: Yusuf Ali or Shakir. Both are in the same Gutenberg file as Pickthall.
- Hebrew Bible: JPS 1917 against the KJV.
- Gita and the other texts: a second public-domain translation, once one is found.

Each claim also records the translation and its year.

**Literal reading only.** These texts carry centuries of commentary, and
modern apologetic and polemical literature makes strong "scripture predicted
X" claims in both directions. Models have read all of it. The extractor and
judge prompts score only what the quoted words state, with no allegory,
numerology or tradition-supplied meaning. Blinding to author and title is weak
here (the KJV is unmistakable), so the second-translation rule and a sample of
hand checks carry more of the weight.

**Lead time capped at 500 years.** Uncapped, w = log2(1 + L) gives 2,000 years of lead
time gives w ≈ 11, against at most about 7 for 19th-century fiction. Many
loose 0.25 matches across that span could outrank precise sci-fi hits without
meaning much. The weight is therefore capped at 500 years of lead time
(w ≤ log2(501) ≈ 9.0; §8), and rankings are published per corpus group (§1b),
including **Scripture and ancient texts**, plus a **combined all-time list**.
Many ancient texts have no known author, so their rankings are by text, not by
author.

### 1b. Any text that predicts the future

The extractor doesn't care whether a text is fiction. It lists speculative
claims either way, so the corpus is any text that looks ahead. Each work gets a
`corpus_group`, and rankings are published per group and combined:

| Group | Examples |
|---|---|
| `sf` | the sci-fi corpus above |
| `fiction` | other fiction with forecasts. Morgan Robertson's *Futility* (1898) sinks an "unsinkable" liner, the *Titan*, after it hits an iceberg in April |
| `scripture` | §1a |
| `prophecy` | Nostradamus, the Sibylline Oracles, almanacs |
| `nonfiction` | futurist books and essays (Wells's *Anticipations* 1901, Vannevar Bush's "As We May Think" 1945, Clarke's *Profiles of the Future* 1962, Toffler's *Future Shock* 1970), forecasts in newspapers and magazines (John Elfreth Watkins's "What May Happen in the Next Hundred Years", *Ladies' Home Journal* 1900; Asimov's "Visit to the World's Fair of 2014", NYT 1964), interviews and speeches (Tesla in *Collier's*, 1926) |

What changes for non-fiction:

- **The work can be an article, essay, interview or speech**, and its date is
  usually exact (the issue date). The "author" of an interview is the person
  predicting, not the journalist, and the record says which.
- **Forecasts are explicit and often dated** ("by the year 2000..."), so the
  timing bonus (open question 4) matters more here, and so does precision:
  forecasters make many confident predictions that fail.
- **Sources beyond the library:**
  - Gutenberg non-fiction, found by the same catalog method as the sci-fi.
  - Chronicling America, searched for "year 2000", "a hundred years hence" and
    similar phrases in pre-1963 papers: a whole genre of turn-of-the-century
    forecasting.
  - Internet Archive scans of *Popular Science* and *Popular Mechanics*.
  - Paleofuture-style collections, used only as an index for finding the
    originals.

**Running the whole library is affordable.** Every book in it, about 8,500
books and 850 M words, costs roughly $90 for a Haiku pass via the Batch API.
Books with no forecasts (most romance and crime) simply return few claims, so
there's no need to hand-pick genres first. The `fiction` and `nonfiction`
groups can come from that run.

## 2. Chunking

Chapter-sized chunks (split on headings, about 5–15 K words; long chapters are
split at paragraph breaks). Each chunk has a stable id (`work_id` + sequence)
and character offsets into the book's markdown, so every excerpt can be traced
to an exact location. Smaller chunks give better recall from smaller models,
and they keep Haiku under its 100 K-token price step.

**Pre-filter: tested and dropped (decided 2026-11-02); every book is read in
full.** A rule-based filter (`pipeline/prefilter.py`) keeps only
paragraphs that contain learned cue words, so models read less. The cue words
were learned from the gold-set claims and tested leave-one-text-out.

- Keeping 95% of the models' claims meant keeping about 74% of a random
  sci-fi sample.
- On the gold set's two ordinary books, recall at that setting was 81–85%.
- Fiction often predicts by narrating without any cue word (the *Titan*'s
  lifeboats, Kipling's altitude lanes).
- Lower recall saves more: 90% keeps 58%, 85% keeps 44%.

Full trade-off in `runs/prefilter/report.md`.

## 3. Extraction

For each chunk, a model lists **every** speculative element: technologies,
inventions, scientific discoveries, political or social developments, and
events. That includes the ones that never came true (FTL drives, telepathy);
those become the denominator for precision and the list of open predictions
(§8).

What the extractor sees: the chunk text and the year of first publication.
What it does **not** see: author and title. Models already know the famous
predictions ("Verne predicted the Moon landing") and will report them from
memory if they know what book they are reading.

Each claim comes back as structured output (schema in `prompts/extract.md`):
a verbatim quote, a one-line description of what is imagined, a category,
specificity 1–5, and whether it was speculative when written (to drop things
that already existed: the Wright brothers had flown before 1910 novels put
aeroplanes in them).

## 4. Verification (deterministic)

Every quote is searched for in the source text: exact match first, then a
normalized fuzzy match (whitespace, punctuation and curly quotes folded) with a
0.9 similarity threshold. A claim whose quote isn't found is rejected and
logged. That rejection count is itself a quality metric for each model. The
stored excerpt is the quote plus its chunk id and character offset.

## 5. Concepts

Claims are mapped to canonical **concepts**, such as "video telephone",
"geostationary communications satellite", "atomic bomb", "credit card" or
"crewed Moon landing". Realization evidence is gathered once per concept, not
once per claim, and the same concept is scored once per book and once per
author (§8).

The concept list is seeded deterministically: Wikidata items with an invention,
inception or first-occurrence date (P575, P571, P606 and similar), plus
Wikipedia's invention and spaceflight timelines. Models may propose new concepts
for claims that fit nothing; proposals go into a review queue rather than
straight into scoring.

## 6. Evidence: when did it come true?

"Came true" is really three dates. Video calling: 1927 (AT&T demonstration),
1964 (Picturephone service), 2003–2010 (Skype and FaceTime in everyday use). Each
concept stores dated **milestones** of three types:

| Milestone | Meaning |
|---|---|
| `first_demonstration` | shown to work at all |
| `first_practical_use` | used for its purpose outside the lab |
| `mass_adoption` | ordinary people use it |

Scoring uses one type, set in config. Default: `first_practical_use`.

Evidence hierarchy for each milestone:

1. A contemporaneous news article. Pre-1963 events: Library of Congress
   [Chronicling America](https://chroniclingamerica.loc.gov) (free API). Later:
   the NYT Archive API and the Guardian Open Platform.
2. A reference source (encyclopedia, patent, museum record) when no article is
   found.

Stored per source: URL, publisher, date, headline and a short quote. Article
text is never stored.

## 7. Judging

A judge model scores each candidate pair (claim ↔ concept milestone) from 0 to
1, blind to author and title, with a short rationale. Rubric anchors (full
prompt in `prompts/judge.md`):

| Score | Meaning |
|---|---|
| 1.0 | function, mechanism and context all match (what it does, how, and how it's used) |
| 0.75 | function and the key mechanism match |
| 0.5 | function matches, mechanism vague or different |
| 0.25 | evocative: the right direction, but loose |
| 0 | not the same thing |

Only claims that map to a concept with a dated milestone reach the judge, so
the judge's workload is a small fraction of the extraction's.

## 8. Scoring (deterministic, parameterized)

```
lead_years L = milestone_date − first_publication_date      (L ≤ 0 → not a prediction, 0 points)
weight     w = log2(1 + min(L, 500))                         (default; config switch)
points       = closeness_score × w
```

| Lead time | log2(1+L), capped at 500 years | linear L |
|---|---|---|
| 1 year | 1.0 | 1 |
| 10 years | 3.5 | 10 |
| 50 years | 5.7 | 50 |
| 100 years | 6.7 | 100 |
| 500 years and more | 9.0 | 500 |

**The 500-year cap** (decided 2026-11-01) applies to every ranking, so ancient
texts and modern fiction share one formula and one combined list. A prediction
fulfilled 2,000 years later earns the same weight as one fulfilled 500 years
later. It only affects texts older than 500 years, since the latest text that
can reach the cap is Nostradamus (1555).

Recommendation: log. Linear makes one 100-year hit worth a hundred 1-year hits,
so the ranking would be decided by a handful of Victorian novels. Log still
rewards foresight strongly while letting breadth count.

De-duplication: a concept counts **once per book** (best-scoring claim) and
**once per author** (best-scoring book), so a series that keeps the same gadget
for twelve volumes doesn't score twelve times.

The formulas in full (c = claim, k = concept, b = book, a = author):

```
L(c,k)    = (milestone_date(k) − first_pub_date(b)) / 365.25         years of lead time
w(L)      = log2(1 + min(L, 500))  if L > 0,  else 0                 lead-time weight, capped at 500 years
p(c,k)    = s(c,k) × w(L(c,k))                                       s = judge score in {0, .25, .5, .75, 1}

P(b,k)    = max over claims c in b of p(c,k)                         one concept, one book: best claim
Book(b)   = Σ over concepts k of P(b,k)

A(a,k)    = max over books b by a of P(b,k)                          one concept, one author: best book
Author(a) = Σ over concepts k of A(a,k)

Precision(a)     = claims with best s ≥ 0.5  ÷  all verified speculative claims by a
PointsPerBook(a) = Author(a) ÷ number of a's books in the corpus
```

Worked examples (scores are illustrative):

| Prediction | Published | Came true (first practical use) | L | w | s | points |
|---|---|---|---|---|---|---|
| Verne, crewed flight to the Moon | 1865 | Apollo 11, 1969 | 103.8 | 6.71 | 0.75 | 5.03 |
| Bellamy, credit card | 1888 | Diners Club, 1950 | 62 | 5.98 | 0.5 | 2.99 |
| Wells, atomic bomb | 1914 | Hiroshima, 1945 | 31.4 | 5.02 | 0.75 | 3.77 |
| A 2008 novel, phone-sized AI assistant | 2008 | Siri, 2011 | 3 | 2.00 | 0.75 | 1.50 |

Published rankings:

1. **Total points** per author and per book.
2. **Precision**: matched claims ÷ all speculative claims. This keeps the award
   from simply rewarding authors who imagined everything.
3. **Points per book**, so prolific authors don't win on volume alone.
4. **By era**: pre-1900, 1900–1945, 1946–1979, 1980+.

### 8a. Every claim gets a resolution

Only `realized` claims enter the award score. The others are recorded for
later analysis: calibration, the most confidently wrong forecasters, and which
kinds of prediction fail.

| Status | Meaning | Example |
|---|---|---|
| `realized` | matched a dated milestone; scored | Wells, atomic bomb (1914 → 1945) |
| `failed` | contradicted on its own terms (see below) | Newcomb (1903): practical flying machines out of reach. The Wright Flyer flew that December |
| `open` | not realized, and its own deadline (if any) hasn't passed | FTL travel, "by 2100 …" |
| `untestable` | can't be checked: metaphor, private states, unfalsifiable | |

`failed` covers predictions that **failed as predicted**, not ones that are
merely still waiting. It has three kinds:

| Failure kind | Test | Decided by |
|---|---|---|
| `missed_deadline` | the text gave a date or horizon ("by the year 2000", "within fifty years"), it has passed by more than a grace period (default 10 years), and no milestone falls inside it | rule |
| `contradicted_negative` | the text said something would never or could not happen, and it did | rule: polarity `will_not` plus a realized milestone |
| `wrong_outcome` | the text predicted a specific outcome and the opposite or an incompatible one happened (a war that wasn't fought, a collapse that didn't come) | judge, with a news source, like a match |

Resolutions are recomputed as milestones are added, so an `open` claim can
later become `realized`, or `failed` once its deadline passes. That makes this
a living leaderboard rather than a one-off.

### 8b. Recorded for later analysis

None of these change the award score; they're there to answer questions later.

**Captured by the extractor in the same pass** (a few more output tokens per
claim):

| Field | Values | Lets us ask |
|---|---|---|
| `stated_time` | the text's own date or horizon, as written, plus a parsed year | were forecasters early or late (signed timing error), and by how much? |
| `polarity` | will / will not | the skeptics' record (`contradicted_negative`) |
| `confidence` | asserted / hedged ("perhaps", "it may be") | are confident predictions more accurate than hedged ones? |
| `valence` | presented as good / bad / neutral / mixed | do dystopian or utopian visions come true more often? |
| `voice` | narrator or author / sympathetic character / antagonist or skeptic / in-world document | did the author endorse it, or put it in a villain's mouth? |
| `domain` | computing, communication, transport, energy, medicine and biology, weapons and war, space, society and politics, economy, environment, other | which fields are foreseen best, and with how much lead time? |
| `second_order` | yes if it predicts a consequence of a technology rather than the technology itself ("cars empty the city centres") | second-order predictions are rarer and arguably worth more |
| `setting_year` | the story's own year, when stated (per work) | how far ahead authors imagine, compared with how far ahead things actually happen |

**Computed from the database:**

- **First to predict.** The earliest work with a claim on each concept. That
  gives an "originator" award, and a timeline of how each idea spread from
  author to author.
- **Timing error.** Actual year minus stated year, by author, era and domain.
- **Realization lag.** Lead-time curves for each domain.
- **Judge disagreement.** The spread of scores across judges and models, as an
  uncertainty measure for each match.

**Gathered separately** (later passes, mostly from open data):

- **Author facts**, from Wikidata (CC0): profession (scientist, engineer,
  journalist, clergy, ...), nationality, gender, birth year (and so age at
  writing). Do working scientists predict better than novelists?
- **Documented influence.** Inventors who credited a book, with sources:
  Szilárd and *The World Set Free*, Goddard and *The War of the Worlds*,
  Sikorsky and Verne, Martin Cooper and Star Trek's communicator.
  Self-fulfilling prophecy is a finding in itself.
- **Popularity**: Wikipedia page views, Gutenberg downloads. Does fame track
  accuracy, or only memorable hits?
- **Prior art**: the earliest non-fiction proposal of each concept (paper,
  patent). It feeds the novelty question (open question 5) without changing
  v1 scores.

## 9. Models: plan and cost

> **Decision (2026-11-01): Claude Code subagents, not the API.** Extraction and
> judging run as Claude Code subagents (Haiku, Sonnet, Opus) on the Claude Code
> subscription; the Anthropic API is not used, to avoid per-token billing. Two
> consequences: effort can't be set per run (each model runs at its default),
> and throughput is bounded by subscription usage limits. The gold-set
> comparison below therefore compares the three models at their defaults, and
> the full corpus will be run in stages within those limits. The API costs in
> this section are kept for comparison only.
>
> **Extraction driver (2026-11-02): `pipeline/extract.py`.**
>
> - **Plan:** books are split into 6,000-word passages, shuffled so that each
>   batch mixes books, and grouped into 40,000-word batches, one batch per
>   Sonnet subagent. These are the settings the gold set validated.
> - **Write as you go:** each subagent writes a passage's result as soon as
>   it finishes it.
> - **Verify:** `verify` checks every quote with `pipeline/quotes.py`, the
>   same code the gold evaluation uses.
> - **Restart:** all state lives under `work/extract/<run>/`, so a run can be
>   stopped at any point and resumed with `next`.
> - **Run settings:** each run records the prompt's sha256 and refuses to mix
>   prompt versions.
> - **Pilot (20 books, 467K words; `runs/pilot/report.md`):**
>   - 1,025 claims, and 99.9% of the quotes were verified.
>   - None were filed under the wrong passage, and the restart worked.
>   - It used 41K reported tokens per 10K words. Scaled to the Gutenberg
>     sci-fi stage, that is about 1,500 subagents, 221M reported tokens and
>     57 agent-hours.
>
> **Exception (2026-11-02): a promotional API credit, through the Batch API.**
> A $200 promotional credit (API and Batch API, not Claude Code; it expires
> 2026-11-21) paid for most of Stage 1, so that it did not use the Claude plan.
> No paid API use.
>
> - **Driver:** `pipeline/batch_api.py`. One Message Batches request per passage,
>   with `prompts/extract_api.md` (the subagent prompt without the file and
>   tool instructions) as the system prompt. Sonnet 5.5 with thinking off.
> - **Same checks:** replies are written to the run's `out/` and verified by
>   `extract.py`. Each verified record says which method produced it.
> - **Budget:** `auto` sends a first round to measure the cost per word, then
>   as many passages as fit in the budget, and stops on a billing error.
>   Passages it doesn't reach stay pending for subagents.
> - **Result:** 8,318 passages for $178.45; `runs/stage1/report.md`.
>
> **Editorial matter.** Modern editions add introductions that explain the
> book's predictions after the fact (the 1993 Bantam Verne: "Florida won, as
> […] predicted"). These are not the author's predictions. The extractor marks
> such passages `speculative_at_time: false`, and the gold set includes them
> as traps (answer-key entries with `expect: editorial`).

Prices (per 1 M tokens, standard / Batch API at 50%):

| Model | Input | Output | Notes |
|---|---|---|---|
| `claude-haiku-5-5` | $0.10 / $0.05 | $0.50 / $0.25 | prompts over 100 K tokens cost 5×, so keep chunks under that |
| `claude-sonnet-5-5` | $2 / $1 | $10 / $5 | |
| `claude-opus-5-5` | $4 / $2 | $20 / $10 | |

Full extraction pass over ~250 M tokens (Batch API, assuming output, including
thinking, is about 10% of input):

| Extractor | Approx. cost |
|---|---|
| Haiku 5.5 | ~$20 |
| Sonnet 5.5 | ~$375 |
| Opus 5.5 | ~$750 |

**Batch API, not subagents, for the bulk.** Even Sonnet over the whole corpus is
affordable, and the Message Batches API is half price, reproducible (pinned
model, versioned prompt, every raw output stored) and doesn't consume Claude
Code usage. Claude Code Haiku subagents are useful for prototyping prompts on a
few books and for QA, but running 4,700 books through them would cost more
and be harder to reproduce.

**The model comparison needs a gold set to mean anything.** About 25 books with
documented predictions, plus about 10 random books:

- Jules Verne, *From the Earth to the Moon* (1865): Florida launch site, three-person crew, ocean splashdown
- H. G. Wells, *The World Set Free* (1914): atomic bombs from chain reactions
- H. G. Wells, "The Land Ironclads" (1903): tanks
- Edward Bellamy, *Looking Backward* (1888): credit cards, piped-in broadcast music
- E. M. Forster, "The Machine Stops" (1909): video calls, a networked world
- Hugo Gernsback, *Ralph 124C 41+* (1911): radar, television, solar power
- Mark Twain, "From the London Times of 1904" (1898): a worldwide viewing network
- Rudyard Kipling, "With the Night Mail" (1905): scheduled transatlantic air mail
- and later in-copyright works in the library (Clarke, Heinlein, Brunner, Orwell, Huxley) for modern lead times

(Each still needs checking that it's in the corpus.)

For each gold book we hand-list the predictions it is known for. Metrics:

- **recall** of the known predictions;
- **verified-quote precision**: the share of quotes that pass §4;
- **true-speculative precision**, from a sample checked by hand;
- **cost per book**.

The matrix to run on identical chunks: Haiku 5.5 at low and medium effort,
Sonnet 5.5, and Opus 5.5 at low effort. A capable model at low effort sometimes
beats a cheap model at high effort, so that combination is tested before we
assume a cascade. The extractor and the judge are separate choices: a Haiku
extractor (broad recall, cheap) with a Sonnet or Opus judge (precise, much
smaller volume) is the likely winner. Estimated cost for the whole comparison:
$20–40.

## 10. The open database

- Working store: SQLite (`schema.sql`).
- **Where it's published** (decided 2026-11-02):
  1. **A public GitHub repository** for the code, prompts, the SQLite file,
     and CSV/Parquet exports.
  2. **An awards page on hoult.co** with the rankings, best predictions, and
     the "still waiting" list.
  3. **Datasette Lite**, which runs in the visitor's browser and loads the
     repository's SQLite file, so anyone can filter, query, and download the
     raw data. It needs no server.
  4. **Probably later:** an interactive browser built like writings.hoult.co.
     That would be one page served as static files from a Cloudflare Worker,
     loading JSON exports of the database.
- Data license: CC BY 4.0, keeping attribution for the sources (ISFDB,
  Wikidata, Chronicling America). Code license: GPL-3.0-or-later.
- **Full books never go in the repository** (decided 2026-11-02). Book text
  stays in the local library. The repository holds code, prompts, the
  database and exports, and short excerpts only. Anything derived from book
  text is rebuilt locally or stored as character offsets (`.gitignore`). This
  covers the gold passages, the raw model output that quotes them, and the
  pre-filter spans.
- **The legal line, stated plainly:**
  - The public database cites the published work (title, author, first
    publication, ISFDB id), never a file or the private library it came from.
  - Excerpts from books still in copyright stay short in the public export:
    at most about 50 words per excerpt and a few per book, the kind of
    quotation fair use covers. Longer context stays in the private working
    database, marked by a `public_excerpt` flag. Public-domain books have no
    limit.
  - News sources: metadata plus a short quote only.

**Provenance.** The only provenance recorded is a public URL for the text
(`sources.source_url`, and `source_url:` in each library file's header): the
Gutenberg, Wikisource, Sefaria or avesta.org page it came from. For every
other text it is null. (Decided 2026-11-01.)

## 11. Reproducibility

- Model IDs pinned (`claude-haiku-5-5`, etc.); prompts versioned (`extract_v1`);
  every raw model response stored with run id, model, prompt version, effort
  and token cost.
- Verification, dating, de-duplication and scoring are plain code over stored
  data. Changing the weight function or the milestone type re-ranks everything
  without calling a model.
- Every rejected claim and every manual override is logged with a reason.
- **Every long run can be paused and restarted at any point without losing
  work** (decided 2026-11-02). Each chunk (or book) gets its own output file,
  written to a temporary name and then renamed, so a file is either complete
  or absent. On restart, finished items are skipped. The run's settings (model,
  prompt version, filter) are recorded with each output, and an item is redone
  only if those change.

## 12. Decisions and open questions

Decided (2026-11-01):

- Lead-time weight capped at 500 years: w = log2(1 + min(L, 500)).
- Every default below is accepted as listed.
- Code license GPL-3.0-or-later; data CC BY 4.0.

- Published as a GitHub repository, an awards page on hoult.co, and Datasette
  Lite, with a writings.hoult.co-style browser probably to follow (2026-11-02,
  §10).

- Name: Prognosticator Awards (`prognosticator-awards`), the dictionary
  spelling (2026-11-02).
- Scripture dates come from each book's English Wikipedia article. The
  article is pinned to a revision, and the permalink is saved in
  `works.date_citation` (2026-11-02, §1a).

Nothing is left to settle.

The questions, each with its accepted default:

**Scoring**

1. **Weight shape**: log (default) or linear? The cap applies either way.
2. **Milestone for scoring**: first demonstration, first practical use
   (default), or mass adoption?
3. **Wrong predictions**: shown only as a separate precision column (default),
   or folded into the main score, e.g. points × precision?
4. **Hit threshold for precision**: a claim counts as a hit at s ≥ 0.5
   (default)?
5. **Novelty**: should a prediction that scientists had already proposed in
   print score less? (Arthur C. Clarke's satellites came from his own 1945
   paper; Tsiolkovsky's rockets predate most rocket fiction.) Default: no
   discount in v1, record prior art for later.
6. **Timing bonus**: Bellamy set *Looking Backward* in the year 2000. Should
   getting the date right earn a bonus? Default: no in v1, store the stated
   year.
7. **Co-authored works**: full points to each author (default), or split?

**Corpus**

8. **Tie-ins**: exclude from the main ranking (default), score separately, or
   score with franchise canon as prior art?
9. **Short stories vs novels**: same table (default), or separate awards?
10. **Scripture dating**: scholarly range end (default), range midpoint, or
    traditional date? Source: decided 2026-11-02, each book's English
    Wikipedia article, pinned to a revision (§1a).
11. **Other prophecy texts**: Nostradamus, the Sibylline Oracles, the
    Prophecy of the Popes? Default: yes, as a `prophecy` group.
12. **Scope of the first run**: decided 2026-11-02. The run is staged,
    using Sonnet. Stage 1 is the 3,234 Gutenberg sci-fi books
    (54.1M words) and the 47 predictive texts, after a 20-book pilot
    (`pipeline/extract.py`, §9). Done 2026-11-02 apart from 1 passage:
    12% by subagents, the rest through the Batch API on a promotional
    credit (`runs/stage1/report.md`).

**Publishing**

13. **Award categories**: overall, by era, by group, best single prediction,
    most accurate (precision), and "still waiting" (best open predictions)?
14. **Excerpt limit** for in-copyright books in the public export: 50 words,
    a few per book (default)?
15. **Code license**: GPL-3.0-or-later (like `ray`) or MIT? Data is CC BY 4.0.
16. **Where it lives**: decided 2026-11-02. All three: a GitHub repository,
    an awards page on hoult.co, and Datasette Lite; probably later, a
    writings.hoult.co-style browser (§10).
17. **Name**: decided 2026-11-02. The dictionary spelling: Prognosticator
    Awards (`prognosticator-awards`).
