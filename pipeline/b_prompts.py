"""Write prompts/b/: the tranche-B variants of tranche A's prompts (PLAN §9), made from them by the
substitutions below, so a change to an A prompt carries over when this is run again. match.py reads
prompts/b/<name> for a tranche-B run where one exists (match.template).

    python -I pipeline/b_prompts.py
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
P = os.path.join(ROOT, 'prompts')

TEXTS = 'old science fiction, futurist writing, prophecy or scripture about events, social change, politics or the economy'
CHECKABLE = (
    '3b. **Events and social changes** count when the quotation imagines something that could be checked in the real '
    'world: a war between real powers, women voting, a world government, a planned economy, a city under one roof. A '
    "story's invented particulars (a named ruler's coup, the hero's revolution on Mars) match a concept only at the "
    'level that can be checked (a world war, a crewed Mars colony); one book\'s plot is not a concept.\n')
EVENTS = (
    "- **Events and social changes** (`type` `event` or `social`):\n"
    "  - an **event** (a war, a revolution, a collapse, a disaster, a discovery made public) has only\n"
    "    `first_practical_use`: the date it first actually happened (a war's start), at the scale the definition\n"
    "    names. No demonstration.\n"
    "  - a **social change** (a law, an institution, a custom, a way of living or governing): `first_practical_use`\n"
    "    is the first time it was in force or common practice somewhere real (a country, a state or province, a\n"
    "    large city), not a proposal, a manifesto, a bill that failed or one person's experiment;\n"
    "    `first_demonstration` is the first organized trial on a real community (a pilot program, an experimental\n"
    "    colony that ran), not a scheme on paper; `mass_adoption` when it became law or common practice in many\n"
    "    countries or most of one large one.\n"
    "  - a political or economic **prediction about a named place** (\"England will be a republic\") comes true\n"
    "    only for that place.\n")
JUDGE = (
    '- For an event or a social change, read the scale this way: *function* is what happens or changes, '
    '*mechanism* is how it comes about (the means, the actors), and *context* is where, when and to whom. '
    '"Women will vote" matched to the first national women\'s suffrage law is 1.0 on function; a passage about '
    'women ruling the state, matched to the same law, is at most 0.5.\n')

SUBS = {  # file: [(old, new), ...]; every `old` must occur
    'match.md': [('(full matching run, tranche A)', '(tranche B: events and social change)'),
                 ('old science fiction or futurist writing', TEXTS),
                 ('4. **No match**', CHECKABLE + '4. **No match**')],
    'rematch.md': [('(full matching run, tranche A)', '(tranche B: events and social change)'),
                   ('old science fiction or futurist writing', TEXTS)],
    'gapmatch.md': [('(full matching run, tranche A)', '(tranche B: events and social change)'),
                    ('old science fiction or futurist writing', TEXTS),
                    ('In two earlier passes each was checked against the\nwhole registry and got `no_concept`: a real prediction the registry lacked.',
                     'In an earlier pass each was checked against a list of\nmostly technology concepts and got no match.'),
                    ('3. Take the most specific', CHECKABLE.replace('3b.', '3b.') + '3. Take the most specific')],
    'concepts_gap_propose.md': [
        ('(full matching run, tranche A, gap pass)', '(tranche B: events and social change)'),
        ('Every claim in your file was checked twice against the existing concepts and\nmatched none of them, though the matchers judged it a real prediction.',
         'Every claim in your file was checked against the existing concepts, which are\nmostly technology, and matched none. Some are not real predictions (a metaphor, a feeling, one\nstory\'s private events): leave those out.'),
        ('predictions made in old\nscience fiction and futurist writing', 'predictions made in\n' + TEXTS),
        ('"video telephone", "crewed Moon landing", "heart transplant"',
         '"women\'s suffrage", "a world government", "a war between the United States and Japan", '
         '"a universal basic income", "crewed Moon landing"'),
        ('"medicine", "space travel"', '"politics", "war", "the future of society"'),
        ("- `type`: `technology` (a device, technique, material, medical or scientific achievement).\n"
         "  If a concept is clearly an event or a social change instead, use `event` or `social`.",
         "- `type`: `event` (something that happens: a war, a revolution, a collapse, a disaster) or `social`\n"
         "  (a change in how people live, work or are governed: a law, an institution, a custom); `technology`\n"
         "  for a device or technique. For a social change, the definition says what counts as it having\n"
         "  happened (a law in force, a practice common in one country); for an event, which powers or places\n"
         "  and at what scale.")],
    'concepts_gap_consolidate.md': [('(full matching run, tranche A, gap pass)', '(tranche B: events and social change)')],
    'concepts_gap_global.md': [('(full matching run, tranche A, gap pass)', '(tranche B: events and social change)')],
    'milestones_tier1.md': [
        ('(full run, tranche A;', '(tranche B: events and social change;'),
        ('technologies and scientific ideas that old science fiction and\nfuturist writing imagined',
         'events, social changes and technologies that old science fiction,\nfuturist writing and prophecy imagined'),
        ("- **Events and social changes** (`type` `event` or `social`): `first_practical_use` is when\n"
         "  it first actually happened; `mass_adoption` when it became widespread, if that applies.\n", EVENTS)],
    'milestones_recheck.md': [
        ('(full run, tranche A;', '(tranche B: events and social change;'),
        ('technologies and scientific ideas that old science fiction and\nfuturist writing imagined',
         'events, social changes and technologies that old science fiction,\nfuturist writing and prophecy imagined'),
        ("- **Events and social changes** (`type` `event` or `social`): `first_practical_use` is when\n"
         "  it first actually happened; `mass_adoption` when it became widespread, if that applies.\n", EVENTS)],
    'milestones_tier2.md': [
        ('(full run, tranche A;', '(tranche B: events and social change;'),
        ('technologies and scientific ideas that old science fiction and futurist\nwriting imagined',
         'events, social changes and technologies that old science fiction, futurist\nwriting and prophecy imagined'),
        ("- **Events and social changes** (`type` `event` or `social`): `first_practical_use` is when it\n"
         "  first actually happened.\n", EVENTS)],
    'milestones_check.md': [('(full run, tranche A;', '(tranche B: events and social change;'),
                            ('old science fiction and futurist writing imagined', 'old science fiction, futurist writing and prophecy imagined')],
    'judge.md': [('(full run, tranche A;', '(tranche B: events and social change;'),
                 ('a passage from fiction or futurist writing', 'a passage from fiction, futurist writing or prophecy'),
                 ('- The summary line is a helper;', JUDGE + '- The summary line is a helper;')],
}


def main():
    os.makedirs(os.path.join(P, 'b'), exist_ok=True)
    for name, subs in SUBS.items():
        text = open(os.path.join(P, name), encoding='utf-8').read()
        for old, new in subs:
            if old not in text:
                raise SystemExit(f'{name}: not found: {old[:60]!r}')
            text = text.replace(old, new)
        open(os.path.join(P, 'b', name), 'w', encoding='utf-8').write(text)
    print(len(SUBS), 'prompts -> prompts/b/')


if __name__ == '__main__':
    main()
