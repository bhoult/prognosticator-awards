"""The award winners (DESIGN §8, §12 question 13), from a finished scoring. Deterministic: every winner
follows from `match.py score`'s outputs by the rules in CATEGORIES; only the prose of why each one won is
written by hand, in runs/match/awards_notes.jsonl, keyed by category and winner (a note whose winner has
changed is left out and reported, so a re-score never shows a stale reason).

    python -I pipeline/awards.py data <run>    -> runs/match/awards.json (winners, runners-up, their best hits)
    python -I pipeline/awards.py page <run>    -> runs/match/awards.html (awards.json + the notes, in
                                                  pipeline/awards_template.html)

Inputs, from work/match/<run>/ (out of git): books.jsonl, entries.jsonl and resolutions.jsonl, written by
`score`; claims.jsonl; and runs/match/'s registry and milestones.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match

TOP_HITS, RUNNERS = 5, 4
ANCIENT = 1500  # works written before this year have their own award (their lead reaches the 500-year cap)
GROUP_AWARDS = (  # award id, title, rule, which books; the texts rank by work, authors where they have one
    ('futurism', 'Best forecaster (non-fiction)', 'the futurist essays and forecasts',
     lambda b: b['group'] == 'Futurism'),
    ('classics', 'Best early-modern utopia', 'the classic utopias (More, Campanella, Bacon)',
     lambda b: b['group'] == 'Classics'),
    ('politics', 'Best political or historical forecast', 'the works of politics and philosophy',
     lambda b: b['group'] in ('Politics', 'Philosophy')),
    ('ancient', 'Best ancient, sacred or prophetic text', f'the sacred and prophetic texts and the works written before {ANCIENT}',
     lambda b: b['group'] in ('Religion', 'Prophecy') or (b['year'] is not None and b['year'] < ANCIENT)),
    ('fiction', 'Best general fiction', 'the general (not science) fiction', lambda b: b['group'] == 'Fiction'),
)
DOMAIN_TITLES = {'computing': 'Computing', 'communication': 'Communication', 'transport': 'Transport',
                 'energy': 'Energy', 'medicine-biology': 'Medicine and biology', 'weapons-war': 'Weapons and war',
                 'space': 'Space', 'environment': 'Environment', 'economy': 'Economy',
                 'society-politics': 'Society and politics', 'other': 'Everything else'}
ERA_TITLES = {'pre-1900': 'Victorian visionary (before 1900)', '1900–1945': 'Pulp-era visionary (1900–1945)',
              '1946–1979': 'Atomic-age visionary (1946–1979)', '1980+': 'Modern visionary (1980 on)'}
LONG_MIN, ONTIME_MIN, ONTIME_LEAD, ORIGIN_MIN = 0.75, 0.75, 10, 0.5


def load(run):
    rd = lambda f: match.read_jsonl(match.rd(run, f))[0]
    books = {b['book']: b for b in rd('books.jsonl')}
    entries = rd('entries.jsonl')
    res = rd('resolutions.jsonl')
    cl = {c['id']: c for c in match.claims(run)}
    reg = {c['concept_id']: c for c in match.final_registry(run)}
    ms = match.scoring_milestones()
    return books, entries, res, cl, reg, ms


def ideas(n):
    return f"{n} idea{'s' * (n != 1)}"


def work(b):
    """The name a work ranks under when it has no author: its title, with the library's volume split undone."""
    return b['title'].split(', Volume')[0]


def label(b):
    return ' and '.join(b['authors']) or work(b)


def modern(b):
    return b['year'] is not None and b['year'] >= ANCIENT and b['group'] not in ('Religion', 'Prophecy')


def joint(ranked, hits):
    """Co-authors whose credits are the same books tie exactly: they share the place."""
    out = []
    for a, p in ranked:
        if out and out[-1][1] == p and [e['claim'] for e in hits[out[-1][0].split(' & ')[0]]] == [e['claim'] for e in hits[a]]:
            out[-1] = (out[-1][0] + ' & ' + a, p)  # shown as "and"; titles can hold "and" 
        else:
            out.append((a, p))
    return out


def totals(entries, books, keep=lambda e: True):
    """Author (or, for a text without one, the work's) totals: each counts a concept once, from its best
    book (DESIGN §8), over the entries `keep` passes. Entries come best first, as `score` writes them."""
    best, tot, hits = {}, collections.Counter(), collections.defaultdict(list)
    for e in entries:
        if not keep(e):
            continue
        for a in books[e['book']]['authors'] or [work(books[e['book']])]:
            if (a, e['concept_id']) not in best:
                best[a, e['concept_id']] = e
                tot[a] += e['points']
                hits[a].append(e)
    return sorted(tot.items(), key=lambda t: (-t[1], t[0])), hits


def hit(e, books, cl, reg, ms):
    c, b, m, k = cl[e['claim']], books[e['book']], ms[e['concept_id']], reg[e['concept_id']]
    return {'concept': k['name'], 'concept_id': e['concept_id'], 'definition': k['definition'],
            'quote': c['quote'], 'title': b['title'], 'year': b['year'], 'authors': b['authors'],
            'came_true': m['date'], 'kind': m['kind'], 'event': m.get('what', ''), 'confidence': m.get('confidence'),
            'lead': e['lead'], 'score': e['score'], 'points': round(e['points'], 2),
            'demonstration_only': m['kind'] == 'first_demonstration'}


def data(run):
    books, entries, res, cl, reg, ms = load(run)
    H = lambda e: hit(e, books, cl, reg, ms)
    nbooks = collections.Counter(a for b in books.values() for a in b['authors'])
    nclaims, nstrict = collections.Counter(), collections.Counter()
    for b in books.values():
        for a in b['authors']:
            nclaims[a] += b.get('claims', 0)
            nstrict[a] += b.get('strict', 0)
    era = lambda y: next((n for n, lo, hi in match.ERAS if y is not None and lo <= y <= hi), None)
    awards = []

    def person(cat, title, rule, ranked, hits, stat, extra=lambda a: {}):
        ranked = joint(ranked, hits)
        if not ranked:
            return
        win = [{'name': a.replace(' & ', ' and '), 'key': a.split(' & ')[0], 'points': round(p, 1), 'stat': stat(a.split(' & ')[0], p),
                **extra(a)} for a, p in ranked[:RUNNERS + 1]]
        awards.append({'id': cat, 'title': title, 'rule': rule, 'winner': win[0], 'runners_up': win[1:],
                       'hits': [H(e) for e in hits[win[0]['key']][:TOP_HITS]]})

    author_rank, author_hits = totals(entries, books, lambda e: books[e['book']]['authors'])
    pts = dict(author_rank)
    person('grand', 'Grand Prognosticator', 'The most points: each realized idea scores closeness × log2(1 + years of '
           'lead), counted once per author from their best book.', author_rank, author_hits,
           lambda a, p: f'{p:.1f} points from {ideas(len(author_hits[a]))} in {nbooks[a]} books')

    book_pts = collections.Counter()
    book_hits = collections.defaultdict(list)
    for e in entries:
        book_pts[e['book']] += e['points']
        book_hits[e['book']].append(e)
    br = sorted(book_pts.items(), key=lambda t: (-t[1], t[0]))
    awards.append({'id': 'book', 'title': 'Book of the Future', 'rule': 'The single work with the most points.',
                   'winner': {'name': books[br[0][0]]['title'], 'by': label(books[br[0][0]]), 'year': books[br[0][0]]['year'],
                              'points': round(br[0][1], 1), 'stat': f'{br[0][1]:.1f} points from {len(book_hits[br[0][0]])} ideas'},
                   'runners_up': [{'name': books[b]['title'], 'by': label(books[b]), 'year': books[b]['year'],
                                   'points': round(p, 1), 'stat': f'{p:.1f} points'} for b, p in br[1:RUNNERS + 1]],
                   'hits': [H(e) for e in book_hits[br[0][0]][:TOP_HITS]]})

    def by_author(es):  # each author's best prediction once
        seen, out = set(), []
        for e in es:
            if label(books[e['book']]) not in seen:
                seen.add(label(books[e['book']]))
                out.append(e)
        return out

    top = by_author(e for e in entries if modern(books[e['book']]))[:RUNNERS + 1]
    awards.append({'id': 'prediction', 'title': 'Prediction of the Age', 'rule': 'The single prediction worth the '
                   f'most points, the closest match with the longest lead, in a work published since {ANCIENT}.',
                   'winner': {'name': label(books[top[0]['book']]), 'points': round(top[0]['points'], 2),
                              'stat': f"{reg[top[0]['concept_id']]['name']}, {top[0]['lead']} years early"},
                   'runners_up': [{'name': label(books[e['book']]), 'points': round(e['points'], 2),
                                   'stat': f"{reg[e['concept_id']]['name']}, {e['lead']} years early"} for e in top[1:]],
                   'hits': [H(e) for e in top]})

    prec = sorted(((nstrict[a] / nclaims[a], a) for a in nclaims if nclaims[a] >= match.PRECISION_CLAIMS and a in pts),
                  key=lambda t: (-t[0], t[1]))
    if prec:
        share = {a: p for p, a in prec}
        ranked = joint([(a, share[a]) for _, a in prec], author_hits)
        first = lambda a: a.split(' & ')[0]
        win = [{'name': a.replace(' & ', ' and '), 'key': first(a), 'points': round(pts[first(a)], 1),
                'stat': f'{share[first(a)]:.0%} of {nclaims[first(a)]:,} predictions came true (score {match.STRICT_MIN:g}+)'}
               for a, _ in ranked[:RUNNERS + 1]]
        awards.append({'id': 'precision', 'title': 'Sharpest Eye', 'rule': f'The highest share of predictions that came '
                       f'true at a judged closeness of {match.STRICT_MIN:g} or more, among authors with '
                       f'{match.PRECISION_CLAIMS}+ predictions.', 'winner': win[0], 'runners_up': win[1:],
                       'hits': [H(e) for e in author_hits[win[0]['key']][:TOP_HITS]]})

    ppb = sorted(((p / nbooks[a], a) for a, p in author_rank if nbooks[a] >= match.PPB_BOOKS), key=lambda t: (-t[0], t[1]))
    person('per_book', 'Most Prescient per Book', f'Points per book in the corpus, among authors with '
           f'{match.PPB_BOOKS}+ books, so volume alone does not win.',
           [(a, pts[a]) for _, a in ppb], author_hits, lambda a, p: f'{p / nbooks[a]:.1f} points per book over {nbooks[a]} books')

    for name, _, _ in match.ERAS:
        r, h = totals(entries, books, lambda e, n=name: books[e['book']]['authors'] and era(books[e['book']]['year']) == n)
        person('era-' + name, ERA_TITLES[name], f'The most points from books first published {name}.', r, h,
               lambda a, p, h=h: f'{p:.1f} points from {ideas(len(h[a]))}')

    for gid, title, which, keep in GROUP_AWARDS:
        r, h = totals(entries, books, lambda e, keep=keep: keep(books[e['book']]))
        person('group-' + gid, title, f'The most points among {which}.', r, h,
               lambda a, p, h=h: f'{p:.1f} points from {ideas(len(h[a]))}')

    dom = lambda e: cl[e['claim']]['domain'] if cl[e['claim']].get('domain') in DOMAIN_TITLES else 'other'
    for d, title in DOMAIN_TITLES.items():
        r, h = totals(entries, books, lambda e, d=d: books[e['book']]['authors'] and dom(e) == d)
        person('domain-' + d, title, f'The most points from ideas in {title.lower()}.', r, h,
               lambda a, p, h=h: f'{p:.1f} points from {ideas(len(h[a]))}')

    longs = by_author(sorted((e for e in entries if e['score'] >= LONG_MIN and modern(books[e['book']])),
                             key=lambda e: (-e['lead'], -e['score'], e['claim'])))
    if longs:
        awards.append({'id': 'long_view', 'title': 'The Long View', 'rule': f'The longest lead of any prediction judged '
                       f'{LONG_MIN:g} or closer, in a work published since {ANCIENT} (older texts have their own award).',
                       'winner': {'name': label(books[longs[0]['book']]), 'points': round(longs[0]['points'], 2),
                                  'stat': f"{longs[0]['lead']} years ahead"},
                       'runners_up': [{'name': label(books[e['book']]), 'points': round(e['points'], 2),
                                       'stat': f"{e['lead']} years ahead"} for e in longs[1:RUNNERS + 1]],
                       'hits': [H(e) for e in longs[:RUNNERS + 1]]})

    first = {}
    for e in sorted(entries, key=lambda e: (books[e['book']]['year'], e['claim'])):
        if e['score'] >= ORIGIN_MIN and books[e['book']]['authors'] and e['concept_id'] not in first:
            first[e['concept_id']] = e
    origin = collections.defaultdict(list)
    for e in first.values():
        for a in books[e['book']]['authors']:
            origin[a].append(e)
    orank = sorted(origin.items(), key=lambda t: (-len(t[1]), -pts.get(t[0], 0), t[0]))
    if orank:
        oh = {a: sorted(es, key=lambda e: -e['points']) for a, es in orank}
        person('originator', 'The Originator', f'The most ideas this author was the first in the corpus to predict '
               f'(judged {ORIGIN_MIN:g} or closer), that later came true.', [(a, pts.get(a, 0)) for a, _ in orank], oh,
               lambda a, p: f'first to predict {len(origin[a])} ideas that came true')

    npath = os.path.join(match.OUT, 'negative_review.jsonl')  # prompts/negative_check.md: which skeptics were really proved wrong
    proved = {r['id'] for r in match.read_jsonl(npath)[0] if r['verdict'] == 'contradicted'} if os.path.exists(npath) else set()
    nonfiction = lambda r: books[r['book']]['group'] in ('Science', 'Futurism', 'Politics', 'Philosophy')
    neg = sorted((r for r in res if r['resolution'] == 'failed' and r['why'] == 'contradicted_negative' and r['id'] in proved
                  and cl[r['id']]['voice'] == 'narrator'),
                 key=lambda r: (-r['score'], r['lead'], not nonfiction(r), r['id']))
    if neg:
        nh = lambda r: dict(hit({'claim': r['id'], 'book': r['book'], 'concept_id': r['concept_id'], 'lead': r['lead'],
                                 'score': r['score'], 'points': 0}, books, cl, reg, ms))
        awards.append({'id': 'last_words', 'title': 'Famous Last Words', 'rule': 'A confident "it will never happen" in '
                       "the book's own narration, judged closest to what then happened, and proved wrong soonest (a check "
                       'confirmed each skeptic was really proved wrong).',
                       'winner': {'name': label(books[neg[0]['book']]), 'points': 0,
                                  'stat': f"{reg[neg[0]['concept_id']]['name']}, {neg[0]['lead']} years later"},
                       'runners_up': [{'name': label(books[r['book']]), 'points': 0,
                                       'stat': f"{reg[r['concept_id']]['name']}, {r['lead']} years later"} for r in neg[1:RUNNERS + 1]],
                       'hits': [nh(r) for r in neg[:RUNNERS + 1]]})

    timed = sorted((r for r in res if r.get('timing_error') is not None and r['resolution'] == 'realized'
                    and r['score'] >= ONTIME_MIN and r['lead'] >= ONTIME_LEAD),
                   key=lambda r: (abs(r['timing_error']), -r['lead'], r['id']))
    off = lambda r: 'on the year' if not r['timing_error'] else f"off by {abs(r['timing_error'])} year{'s' * (abs(r['timing_error']) != 1)}"
    if timed:
        th = lambda r: dict(hit({'claim': r['id'], 'book': r['book'], 'concept_id': r['concept_id'], 'lead': r['lead'],
                                 'score': r['score'], 'points': r['points']}, books, cl, reg, ms),
                            stated_time=cl[r['id']]['stated_time'], timing_error=r['timing_error'])
        awards.append({'id': 'on_time', 'title': 'Right on Schedule', 'rule': f'A prediction that named its year and came '
                       f'true closest to it, judged {ONTIME_MIN:g} or closer, at least {ONTIME_LEAD} years ahead.',
                       'winner': {'name': label(books[timed[0]['book']]), 'points': round(timed[0]['points'], 2),
                                  'stat': off(timed[0])},
                       'runners_up': [{'name': label(books[r['book']]), 'points': round(r['points'], 2),
                                       'stat': off(r)} for r in timed[1:RUNNERS + 1]],
                       'hits': [th(r) for r in timed[:RUNNERS + 1]]})

    waiting = collections.defaultdict(list)  # concept -> its claims, for concepts with no milestone
    for c in match.read_jsonl(match.rd(run, 'matches.jsonl'))[0]:
        if c['concepts'] and c['id'] in cl:
            for k in c['concepts']:
                if k not in ms and reg.get(k, {}).get('came_true_guess') != 'yes':
                    waiting[k].append(c['id'])
    still = []
    for k, ids in sorted(waiting.items(), key=lambda t: (-len({cl[i]['book'] for i in t[1]}), t[0]))[:8]:
        dated = sorted((i for i in ids if cl[i]['year'] is not None), key=lambda i: (cl[i]['year'], i))
        e = cl[dated[0]]
        still.append({'concept': reg[k]['name'], 'definition': reg[k]['definition'], 'books': len({cl[i]['book'] for i in ids}),
                      'claims': len(ids), 'first_title': books[e['book']]['title'], 'first_by': label(books[e['book']]),
                      'first_year': e['year'], 'quote': e['quote']})
    awards.append({'id': 'still_waiting', 'title': 'Still Waiting', 'rule': 'The ideas the most books predicted that '
                   'have not come true, with the earliest book in the corpus to predict each.', 'waiting': still,
                   'winner': {'name': still[0]['concept'], 'points': 0,
                              'stat': f"predicted in {still[0]['books']} books, first in {still[0]['first_title']}"}})

    counts = collections.Counter(r['resolution'] for r in res)
    out = {'run': run, 'claims': len(res), 'books': len({r['book'] for r in res}), 'resolutions': dict(counts),
           'points': round(sum(e['points'] for e in entries), 1), 'entries': len(entries),
           'authors': len(author_rank), 'awards': awards}
    match.write_atomic(os.path.join(match.OUT, 'awards.json'), json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(f"{len(awards)} awards -> runs/match/awards.json")
    for a in awards:
        w = a.get('winner')
        print(f"{a['id']:28} {w['name'] if w else '-':40} {w['stat'] if w else ''}")


NOTES = os.path.join(match.OUT, 'awards_notes.jsonl')  # {"id", "winner", "why"}: the hand-written reason for each award
REPO = 'https://github.com/bhoult/prognosticator-awards'


def page(run, edition='First awards, 2026 · technology and science', scored='2026-11-19'):
    d = json.load(open(os.path.join(match.OUT, 'awards.json'), encoding='utf-8'))
    notes = {(n['id'], n['winner']): n['why'] for n in match.read_jsonl(NOTES)[0]} if os.path.exists(NOTES) else {}
    stale = []
    for a in d['awards']:
        w = a.get('winner')
        if w and (a['id'], w['name']) in notes:
            a['why'] = notes[a['id'], w['name']]
        elif w:
            stale.append(f"{a['id']}: {w['name']}")
    r = d['resolutions']
    nreg = len(match.final_registry(run))
    ndec = len(match.read_jsonl(os.path.join(match.OUT, 'deciding.jsonl'))[0])
    d.update(edition=edition, scored=scored,
             dek='For the science fiction, forecasts and old texts that saw the future first. Every prediction was '
                 'read from the book itself, matched to the dated event that made it come true, and scored by how '
                 'close it came and how far ahead it was written.',
             method=f"Closeness is the mean of two independent judges' scores on a five-step scale from 0 to 1 (a third "
                    f"judge where they differ by two steps). Years early run from first publication to the first practical "
                    f"use (or, where there is none yet, the first demonstration), capped at 500. An idea counts once per "
                    f"book and once per author, from their best book.",
             notes=[
                 ('How it was made', [
                     f"{d['books']:,} books and texts: Project Gutenberg's science fiction with a known year, and 47 "
                     f"forecasts, utopias, prophecies and sacred texts. Sonnet subagents read every page and listed "
                     f"{d['claims']:,} technology and science predictions, each with a verbatim quote that code checked "
                     f"against the book.",
                     f'The predictions were matched to {nreg:,} ideas, and each idea that came true was dated from public '
                     f'sources by researchers who never saw the books, the claims or the authors. The {ndec} ideas that '
                     'decide the rankings were researched a second time. Judges saw the passage and the event, never '
                     'the author or the title.']),
                 ('What to keep in mind', [
                     f"Ideas dated only by a demonstration are marked <i>demo only</i>; dates from a single, weak source "
                     f"are marked <i>low confidence</i>. {r.get('not_a_prediction', 0):,} passages described things that "
                     f"already existed when they were written and score nothing.",
                     'Ancient texts are dated by the end of the scholarly range for their composition, from each '
                     "text's English Wikipedia article, and read in one translation each; the plan's second-translation "
                     'check is not built yet.',
                     'Social, political and historical predictions (tranche B, 46,211 more claims) are scored separately '
                     'and are not in these awards yet.']),
                 ('The data', [
                     f'Code, prompts, every milestone with its sources, the review decisions and the full reports are in '
                     f'the public repository: <a href="{REPO}">{REPO.replace("https://", "")}</a> '
                     f'(<code>runs/match/report.md</code>).',
                     'Code under GPL-3.0-or-later; data under CC BY 4.0.'])])
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'awards_template.html'), encoding='utf-8').read()
    html = tpl.replace('__AWARDS_JSON__', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))
    match.write_atomic(os.path.join(match.OUT, 'awards.html'), html)
    print(f"{len(d['awards'])} awards -> runs/match/awards.html; no reason written for {len(stale)}: {stale}")


if __name__ == '__main__':
    {'data': data, 'page': page}[sys.argv[1]](*sys.argv[2:])
