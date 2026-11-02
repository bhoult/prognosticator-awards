-- Prognosticator Awards: working database (SQLite). Draft v0.
-- Rows written by a model carry the run that produced them; everything else is code.

PRAGMA foreign_keys = ON;

CREATE TABLE runs (                      -- one model pass (extract, judge, concept-propose, evidence)
    id              INTEGER PRIMARY KEY,
    stage           TEXT NOT NULL CHECK (stage IN ('extract','judge','concept','evidence')),
    model           TEXT NOT NULL,       -- pinned id, e.g. claude-haiku-5-5
    effort          TEXT,                -- low | medium | high | ...
    prompt_version  TEXT NOT NULL,       -- e.g. extract_v1
    batch_id        TEXT,                -- Message Batches id, when batched
    started_at      TEXT NOT NULL,
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    cost_usd        REAL,
    notes           TEXT
);

CREATE TABLE authors (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,       -- display name, "H. G. Wells"
    isfdb_id        INTEGER UNIQUE,
    wikidata_id     TEXT,
    birth_year      INTEGER,
    death_year      INTEGER,
    profession      TEXT,                -- scientist | engineer | journalist | clergy | novelist | ... (Wikidata)
    nationality     TEXT,
    gender          TEXT
);

CREATE TABLE works (                     -- the published work, independent of any file
    id              INTEGER PRIMARY KEY,
    title           TEXT NOT NULL,
    isfdb_id        INTEGER UNIQUE,
    first_pub_date  TEXT,                -- ISO date; precision in first_pub_precision
    first_pub_precision TEXT CHECK (first_pub_precision IN ('day','month','year')),
    first_pub_venue TEXT,                -- "Astounding Science Fiction, March 1957" or publisher
    first_pub_source TEXT,               -- isfdb | openlibrary | manual
    length_class    TEXT CHECK (length_class IN ('novel','novella','novelette','short story','collection','scripture',
                                                 'book','essay','article','interview','speech')),
    tie_in          TEXT,                -- NULL, or franchise name ("Star Trek")
    public_domain_us INTEGER NOT NULL DEFAULT 0,
    corpus_group    TEXT NOT NULL DEFAULT 'sf' CHECK (corpus_group IN ('sf','fiction','scripture','prophecy','nonfiction')),
    setting_year    INTEGER,             -- the story's own year, when stated
    parent_work_id  INTEGER REFERENCES works(id),   -- Daniel -> Bible; Katha -> Upanishads
    -- Ancient texts have no first-publication date: a cited composition range instead.
    composed_earliest INTEGER,           -- year, negative = BCE
    composed_latest   INTEGER,           -- lead time is measured from here by default
    traditional_year  INTEGER,           -- stored, not scored unless date_basis = 'traditional'
    date_citation   TEXT                 -- reference work and page for the range
);

CREATE TABLE translations (              -- which translation a source is, for the second-translation check
    id              INTEGER PRIMARY KEY,
    work_id         INTEGER NOT NULL REFERENCES works(id),
    translator      TEXT NOT NULL,       -- "Marmaduke Pickthall"
    year            INTEGER NOT NULL,
    public_domain_us INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE work_authors (
    work_id         INTEGER NOT NULL REFERENCES works(id),
    author_id       INTEGER NOT NULL REFERENCES authors(id),
    position        INTEGER NOT NULL DEFAULT 1,
    role            TEXT NOT NULL DEFAULT 'author' CHECK (role IN ('author','speaker','attributed')),
                                         -- speaker: an interviewee; attributed: traditional authorship
    PRIMARY KEY (work_id, author_id)
);

CREATE TABLE sources (                   -- PRIVATE: the text we actually read (not published)
    id              INTEGER PRIMARY KEY,
    work_id         INTEGER NOT NULL REFERENCES works(id),
    translation_id  INTEGER REFERENCES translations(id),
    path            TEXT NOT NULL,       -- library .md path
    sha256          TEXT NOT NULL,
    words           INTEGER,
    source_url      TEXT                 -- public URL of the text (Gutenberg, Wikisource, ...); NULL otherwise.
                                         -- The only provenance that is recorded or published.
);

CREATE TABLE chunks (
    id              INTEGER PRIMARY KEY,
    source_id       INTEGER NOT NULL REFERENCES sources(id),
    seq             INTEGER NOT NULL,
    char_start      INTEGER NOT NULL,
    char_end        INTEGER NOT NULL,
    heading         TEXT,
    UNIQUE (source_id, seq)
);

CREATE TABLE claims (                    -- every speculative element the extractor found
    id              INTEGER PRIMARY KEY,
    work_id         INTEGER NOT NULL REFERENCES works(id),
    chunk_id        INTEGER NOT NULL REFERENCES chunks(id),
    run_id          INTEGER NOT NULL REFERENCES runs(id),
    quote           TEXT NOT NULL,       -- verbatim, as returned
    char_offset     INTEGER,             -- where verification found it (NULL if not found)
    verify_status   TEXT NOT NULL CHECK (verify_status IN ('pending','exact','fuzzy','rejected')),
    verify_similarity REAL,
    description     TEXT NOT NULL,       -- one line: what is imagined
    category        TEXT NOT NULL,       -- technology | science | social | political | event | other
    specificity     INTEGER CHECK (specificity BETWEEN 1 AND 5),
    speculative_at_time INTEGER NOT NULL,-- extractor's view: not yet real when written
    public_excerpt  INTEGER NOT NULL DEFAULT 0, -- may this quote appear in the public export?
    -- Recorded for later analysis (DESIGN.md §8b); none of these affect the award score.
    stated_time_text TEXT,               -- the text's own date or horizon, as written: "within fifty years"
    stated_year     INTEGER,             -- parsed from stated_time_text (absolute year), NULL if none
    polarity        TEXT NOT NULL DEFAULT 'will' CHECK (polarity IN ('will','will_not')),
    confidence      TEXT CHECK (confidence IN ('asserted','hedged')),
    valence         TEXT CHECK (valence IN ('positive','negative','neutral','mixed')),
    voice           TEXT CHECK (voice IN ('narrator','sympathetic','antagonist','document')),
    domain          TEXT CHECK (domain IN ('computing','communication','transport','energy','medicine-biology',
                                           'weapons-war','space','society-politics','economy','environment','other')),
    second_order    INTEGER NOT NULL DEFAULT 0  -- predicts a consequence of a technology, not the technology
);

CREATE TABLE resolutions (               -- what became of each claim; recomputed as milestones are added
    claim_id        INTEGER NOT NULL REFERENCES claims(id),
    status          TEXT NOT NULL CHECK (status IN ('realized','failed','open','untestable')),
    failure_kind    TEXT CHECK (failure_kind IN ('missed_deadline','contradicted_negative','wrong_outcome')),
    decided_by      TEXT NOT NULL CHECK (decided_by IN ('rule','judge','manual')),
    run_id          INTEGER REFERENCES runs(id),
    milestone_id    INTEGER REFERENCES milestones(id),   -- the event that realized or contradicted it
    evidence_id     INTEGER REFERENCES evidence(id),
    as_of           TEXT NOT NULL,       -- date the resolution was computed
    PRIMARY KEY (claim_id, as_of)
);

CREATE TABLE influences (                -- documented cases of a work inspiring the real thing
    id              INTEGER PRIMARY KEY,
    work_id         INTEGER NOT NULL REFERENCES works(id),
    concept_id      INTEGER REFERENCES concepts(id),
    person          TEXT NOT NULL,       -- "Leo Szilard"
    statement       TEXT NOT NULL,       -- short quote or summary
    url             TEXT NOT NULL
);

CREATE TABLE prior_art (                 -- earliest non-fiction proposal of a concept (novelty analysis, later)
    id              INTEGER PRIMARY KEY,
    concept_id      INTEGER NOT NULL REFERENCES concepts(id),
    date            TEXT NOT NULL,
    description     TEXT NOT NULL,
    url             TEXT
);

CREATE TABLE popularity (                -- fame proxies, sampled over time
    work_id         INTEGER NOT NULL REFERENCES works(id),
    metric          TEXT NOT NULL,       -- wikipedia_pageviews_year | gutenberg_downloads_30d | ...
    value           REAL NOT NULL,
    as_of           TEXT NOT NULL,
    PRIMARY KEY (work_id, metric, as_of)
);

CREATE TABLE concepts (                  -- canonical ideas: "video telephone"
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT NOT NULL,
    wikidata_id     TEXT,
    origin          TEXT NOT NULL CHECK (origin IN ('wikidata','timeline','model-proposed','manual')),
    review_status   TEXT NOT NULL DEFAULT 'accepted' CHECK (review_status IN ('proposed','accepted','rejected'))
);

CREATE TABLE milestones (                -- when a concept came true, three ways
    id              INTEGER PRIMARY KEY,
    concept_id      INTEGER NOT NULL REFERENCES concepts(id),
    kind            TEXT NOT NULL CHECK (kind IN ('first_demonstration','first_practical_use','mass_adoption')),
    date            TEXT NOT NULL,       -- ISO date
    date_precision  TEXT NOT NULL CHECK (date_precision IN ('day','month','year')),
    summary         TEXT NOT NULL,       -- "AT&T demonstrates two-way TV telephone, New York–Washington"
    UNIQUE (concept_id, kind)
);

CREATE TABLE evidence (                  -- sources for a milestone: metadata + short quote, never full text
    id              INTEGER PRIMARY KEY,
    milestone_id    INTEGER NOT NULL REFERENCES milestones(id),
    kind            TEXT NOT NULL CHECK (kind IN ('news','reference','patent','other')),
    url             TEXT NOT NULL,
    publisher       TEXT,
    published       TEXT,                -- ISO date of the article/source
    headline        TEXT,
    quote           TEXT,                -- short
    run_id          INTEGER REFERENCES runs(id)
);

CREATE TABLE claim_concepts (            -- candidate mapping, before judging
    claim_id        INTEGER NOT NULL REFERENCES claims(id),
    concept_id      INTEGER NOT NULL REFERENCES concepts(id),
    run_id          INTEGER REFERENCES runs(id),
    PRIMARY KEY (claim_id, concept_id)
);

CREATE TABLE judgments (                 -- judge's closeness score for a claim against a concept
    id              INTEGER PRIMARY KEY,
    claim_id        INTEGER NOT NULL REFERENCES claims(id),
    concept_id      INTEGER NOT NULL REFERENCES concepts(id),
    run_id          INTEGER NOT NULL REFERENCES runs(id),
    score           REAL NOT NULL CHECK (score BETWEEN 0 AND 1),
    rationale       TEXT NOT NULL,
    second_translation_id INTEGER REFERENCES translations(id),  -- set when this is the cross-check
    UNIQUE (claim_id, concept_id, run_id)
);

CREATE TABLE overrides (                 -- manual corrections, always with a reason
    id              INTEGER PRIMARY KEY,
    table_name      TEXT NOT NULL,
    row_id          INTEGER NOT NULL,
    field           TEXT NOT NULL,
    old_value       TEXT,
    new_value       TEXT,
    reason          TEXT NOT NULL,
    made_at         TEXT NOT NULL
);

-- Scoring is a view, so changing the weight function or milestone kind re-ranks
-- without touching stored data. Default: first_practical_use, w = log2(1 + L).
CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
INSERT INTO settings VALUES ('milestone_kind', 'first_practical_use'), ('weight', 'log2'),
                            ('lead_cap_years', '500'),           -- w = log2(1 + min(L, cap))
                            ('date_basis', 'composed_latest');   -- or 'traditional', for ancient texts

-- The date a work's lead time counts from: first publication for modern works,
-- the end of the scholarly composition range (or the traditional year) for ancient ones.
CREATE VIEW work_dates AS
SELECT id AS work_id,
       CASE WHEN first_pub_date IS NOT NULL THEN julianday(first_pub_date)
            WHEN (SELECT value FROM settings WHERE key = 'date_basis') = 'traditional'
                 AND traditional_year IS NOT NULL THEN julianday('0000-01-01') + traditional_year * 365.25
            ELSE julianday('0000-01-01') + composed_latest * 365.25
       END AS jd
FROM works;

CREATE VIEW scored_claims AS
SELECT
    j.claim_id, c.work_id, j.concept_id, j.score, w.corpus_group,
    m.date AS milestone_date,
    (julianday(m.date) - d.jd) / 365.25 AS lead_years
FROM judgments j
JOIN claims c      ON c.id = j.claim_id AND c.verify_status IN ('exact','fuzzy')
JOIN works w       ON w.id = c.work_id
JOIN work_dates d  ON d.work_id = c.work_id
JOIN milestones m  ON m.concept_id = j.concept_id
                  AND m.kind = (SELECT value FROM settings WHERE key = 'milestone_kind');
-- Points (score × weight), best-per-concept-per-book and once-per-author
-- de-duplication are computed in the scoring script, which needs log2.
