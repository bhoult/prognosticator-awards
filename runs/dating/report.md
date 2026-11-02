# Dating the Gutenberg sci-fi books with ISFDB, 2026-11-02

**Source:** the ISFDB MySQL backup of 2026-10-31 (`backup-MySQL-55-2026-10-31.zip`, sha256 `bcbcd700a556…`), from the ISFDB Downloads page (wiki login required). ISFDB data is available under Creative Commons (the wiki gives CC BY 4.0). `pipeline/isfdb.py` copies six tables into SQLite (titles 2,562,192, authors 305,299, title–author links 2,861,816, pseudonyms 37,606, alternate titles 195,569, alternate author names 24,082). Nothing else in the dump is read.

**Method** (`pipeline/dating.py`; no model calls; result in `lists/gutenberg-sf-dates.tsv`):
- **Title:** normalized; also tried without a parenthesis, a subtitle, an "or" alternative, or a "Part N" / "Volume N" suffix, and against ISFDB titles without their subtitles and against alternate titles.
- **Author:** the same surname, plus the same first initial, the same full name, or (for "Mrs. Loudon") the surname alone. Pseudonyms and alternate names count both ways.
- **Year:** the earliest year among the matched work and its variants (magazine serials, retitlings, translations).
- **Several works with one title** (a story and its later novel expansion, or a collection named after a story): the one whose length fits the book's word count. Collections and anthologies only fit book-length texts. If several fit, the earliest is taken and the row is marked `ambiguous`; if none fit, ISFDB's year is shown but not used.
- **Checks:** against the transcriber's note in the text ("produced from *Galaxy* June 1956"), and the library's year.
- **Year used:** ISFDB's, unless the note gives an earlier one (an etext can't be older than the magazine it was made from); then the library's; then a year in the title of a magazine issue.

## Results (3,234 books)

| ISFDB match | Books |
|---|---|
| One work | 3,029 |
| Several works, settled by length | 75 |
| Several works that fit, earliest taken (`ambiguous`) | 71 |
| A work whose length doesn't fit (year not used) | 1 |
| No match | 58 |

| Year from | Books |
|---|---|
| ISFDB | 3,174 |
| Transcriber's note | 24 |
| Library | 21 |
| Magazine issue title | 8 |
| None | 7 |

- **Against the transcriber's notes:** 2,335 give the same year. In 51 ISFDB's year is earlier (first printed somewhere else, the etext made from a reprint). In 1 the note is earlier (1959 against 1960); the note's year is used.
- **The 277 books with no year:** 261 dated from ISFDB, 1 from a note, 8 from an issue title; 7 remain undated (*The Professor's Experiment*, *Reinstern*, *Rondah*, *The Revolutions of Time*, *The Automatic Maid-of-All-Work*, *Dave Dashaway and His Hydroplane*, *The Messiah of the Cylinder*).
- **Changed years:** 165 of the books the library had dated get another year: 145 earlier, 20 later, 59 by more than ten years. Most are 1920s–30s stories that the library had dated by a 1950s–60s magazine reprint (Keller's "The Rat Racket": 1931, not 1956; Nowlan's "The Airlords of Han": 1929, not 1962).

## Effect on Stage 1

- **Passages judged against the old year:** 1,423 Stage 1 passages (8.4M words, 164 books) come from books whose year changed, 397 of them by more than ten years. Their claims' `speculative_at_time` was judged against the old year. Lead time will be computed from the new year; whether to re-judge those claims is open.
- **Lucian:** ISFDB's dates for Lucian are translation years (1780, 1905), not c. AD 160. Ancient texts are to be dated like scripture (DESIGN §1a), so the undated *Works of Lucian* volumes are not extracted yet.
