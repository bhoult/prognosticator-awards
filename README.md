# Prognosticator Awards

An award for the writing that saw the future coming: science fiction first, and also
scripture, prophecy, and non-fiction forecasts (futurist books, "the year 2000" newspaper
pieces, interviews). For each text we find the technologies, events and social changes it
imagined, match them to the dated real-world developments that fulfilled them, score how
closely each one was predicted (0–1), and weight that by how far ahead of the event the
text was written. The result is an open database of predictions with short excerpts and
sources, and a ranked list of authors and books.

**Status (2026-11-02):**
- **Design:** done.
- **Model comparison:** done on the gold set; Sonnet was chosen for extraction.
- **Stage 1 extraction:** in progress on 2,979 public-domain science-fiction books and
  predictive texts. 167 of 1,413 batches are done, with 11,359 claims verified against
  the text.
- **Not started yet:** matching claims to real events, and scoring.

## How it works

1. **Extract.** Claude Code subagents (Sonnet) read each book in 6,000-word passages,
   with the author and title blanked out so a model can't fall back on what it knows
   about famous books. For every speculative claim they record a verbatim quote and a
   set of fields (category, domain, polarity, hedging, stated date…).
2. **Verify.** Code checks that every quote really is in the passage and rejects
   anything the model "remembered" rather than read.
3. **Match and judge** (planned). Claims map to canonical concepts ("video telephone"),
   and each concept gets dated milestones backed by sources. A judge model, blind to
   author and title, scores each match.
4. **Score** (planned). Code computes
   `points = closeness × log2(1 + years of lead time, capped at 500)`, counting each
   concept once per book and once per author. It then ranks authors and books by total
   points, precision and points per book.

Everything after the model calls is plain, deterministic code over stored data, so
changing a scoring rule re-ranks everything without calling a model again.
[DESIGN.md](DESIGN.md) has the full plan and every decision taken so far.

## Layout

| Path | What it is |
|---|---|
| [DESIGN.md](DESIGN.md) | The plan: corpus, pipeline, scoring formula, model tests, licensing, decisions |
| [schema.sql](schema.sql) | SQLite schema for the working database |
| [prompts/](prompts/) | `extract_subagent.md` is the extraction prompt in use; `extract.md` and `judge.md` are drafts |
| [pipeline/extract.py](pipeline/extract.py) | Extraction driver: plans passages and batches, verifies results, tracks usage; can be stopped and restarted at any point |
| [pipeline/quotes.py](pipeline/quotes.py) | Quote verification (exact, or ≥ 90% fuzzy match) |
| [pipeline/corpus.py](pipeline/corpus.py) | Reads library books with the author and title blanked; splits them into passages |
| [pipeline/gold.py](pipeline/gold.py), [pipeline/evaluate.py](pipeline/evaluate.py), [pipeline/make_prompts.py](pipeline/make_prompts.py) | Builds the gold set, writes its prompts, and scores model runs against it |
| [pipeline/prefilter.py](pipeline/prefilter.py) | Rule-based passage pre-filter: tested and not used ([report](runs/prefilter/report.md)) |
| [gold/](gold/) | Gold-set answer key and passage map |
| [runs/](runs/) | Gold-set model comparison ([findings](runs/findings.md)), [pilot report](runs/pilot/report.md), pre-filter tuning |
| [lists/predictive-texts.txt](lists/predictive-texts.txt) | The non-fiction and prophetic texts included in Stage 1 |

## What is not here

**No book text.** The books live in a local library and are never committed. Everything
built from them is regenerated locally and ignored by git (`.gitignore`):

- the gold-set passages (`gold/chunks/`);
- the extraction run state (`work/`);
- raw model output that quotes in-copyright books.

The public data will carry only short excerpts, as described in DESIGN.md §10.

## Running it

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -I pipeline/extract.py plan work/extract/<run> sonnet <library> <books.txt>
.venv/bin/python -I pipeline/extract.py next work/extract/<run> 20    # claim up to 20 batches
.venv/bin/python -I pipeline/extract.py status work/extract/<run>
```

`next` prints one prompt file per batch. Each prompt is given to a subagent ("Read
<file> and follow its instructions exactly"); the driver verifies the results as they
arrive. See the docstring at the top of `pipeline/extract.py` for details.

## License

- **Code:** GNU General Public License v3.0 or later. See [LICENSE](LICENSE).
- **Data and documentation:** prompts, answer key, run results, reports and the future
  database, under Creative Commons Attribution 4.0 International. See
  [LICENSE-DATA](LICENSE-DATA).
- **Quoted excerpts:** the model output kept here quotes only public-domain texts. The
  in-copyright editions used in the gold set appear only as short identifying anchors in
  `gold/answer_key.json`: three phrases of 3–14 words from the 1967 Bair translation of
  Verne.
