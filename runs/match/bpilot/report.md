# Tranche B pilot: 2,500 society-politics claims (PLAN §9)

Run 2026-11-19 as run `bpilot`, end to end, before the rest of tranche B. It is a checkpoint (a
stop for your review). The design as built is in PLAN §9; the scores are in
[`scoring.md`](scoring.md), the milestones in [`milestones.jsonl`](milestones.jsonl) (tranche A's
plus the pilot's) and the tier-2 table in [`deciding_milestones.md`](deciding_milestones.md).

## Summary

- **The sample:** 2,500 tranche-B claims from the society-politics domain, a fixed-seed sample
  (`match.py b-init bpilot 2500`), from 1,062 books, including the prophecy and sacred texts, now dated by
  composition.
- **73 claims came true (2.9%)**, against 20.4% in tranche A. 490 came after their event (not a
  prediction), 545 are open because their idea never happened or has no milestone, 1,372 have no
  concept, are too vague or untestable, and 15 missed a deadline they named.
- **68 book entries from 53 authors score, 158 points in all.** The best: Milo Hastings's *City of
  Endless Night* (1919) on state limits on births (Singapore, 1972); Wells's *Anticipations* (1901)
  on Britain merging into one urban region (1950); More's *Utopia* (1516) on work found for everyone
  (the French decree of February 1848); M. P. Shiel's *The Yellow Danger* (1898) on an Anglo-American
  alliance (1942); *The Great War of 189-* (1892) on general disarmament (the Washington Naval
  Treaty, 1922).
- **The judges agree more than in tranche A:** 80% of the 82 pairs two judges scored got the same
  score and 20% were one step apart (tranche A: 69% and 30%). No pair needed a third judge.
- **Cost:** 39 agents, 4.3M tokens and 2.1 agent-hours, about 2% of the week.

## How it ran

| Stage | Agents | Tokens | Result |
|---|---|---|---|
| Matching against tranche A's registry (first pass) | 8 | 0.70M | 3.2% matched; 1,650 no concept, 560 untestable, 211 too vague |
| Gap proposals for every unmatched claim | 2 | 0.46M | 213 concepts proposed |
| Consolidation against tranche A's registry | 1 | 0.26M | 151 new concepts; 7 proposals mapped to tranche-A concepts |
| Gap matching | 7 | 0.95M | 45.1% matched; 23 concepts under 3 claims cut |
| Tier 1, checks, second look | 12 | 1.06M | 99 milestones for 82 of the 128 kept concepts |
| Judging, two rounds | 4 | 0.28M | 83 pairs, then 12 after tier 2 |
| Tier 2 on the 23 deciding concepts of the pilot | 5 | 0.61M | 20 confirmed, 6 replaced, 1 added |
| **Total** | **39** | **4.31M** | |

The cross-group merge had nothing to merge (one domain group) and was skipped with an empty merge
file. Every source was fetched and checked again by `verify` (220 checks, all found).

## What the pilot found

1. **The first pass is wasted for this tranche.** Against a registry of technology, 3% of social
   claims matched, and the agents coded the rest carelessly: one batch called 29 claims
   untestable, another 114. The gap pass, which proposes concepts for every unmatched claim,
   did the real work (45% matched). For the rest of B, proposing concepts from a sample first and
   matching once (tranche A's own order) would save the first pass and its noise.
2. **Most social predictions are either still waiting or already old.** Of the 1,128 matched
   claims, 545 point at ideas that never happened (a world government, permanent peace, an
   interplanetary federation) and 490 at ideas that were real before the book (revolutions,
   censorship, secret police, slavery). About half of the new milestones are before 1800 and nearly a
   quarter before the common era. Only 73 claims score.
3. **Literal readings recur.** "Telepaths or psychics used by police" was dated by Scotland Yard
   consulting a stage psychic in 1951; technocracy by Italy's 1995 caretaker cabinet. The judges
   then score such pairs low, which limits the damage, but tier 2 and a review assist should read
   the definitions as tranche A's did.
4. **Tier 1 was thin, tier 2 fixed what decides.** The researchers used Wikipedia only, by their
   own report; 61 of the 100 new milestones are low confidence. Tier 2 added contemporary sources
   for 19 of the 23 deciding concepts and changed 7 scoring milestones (women's suffrage and office
   to Australia's 1902 franchise act, from Finland 1906; megalopolis to 1950; the First World War
   to 4 August 1914).
5. **Tranche A's concepts keep tranche A's milestones.** 143 pilot claims matched tranche-A concepts
   (a galactic federation, a space patrol, eugenic breeding). They are scored on tranche A's verified
   milestones and never researched again in B, so the two tranches agree.
6. **The prophecy texts score with their composition dates,** for example the Sibylline Oracles
   (700 CE) on a pope driven from Rome (1084). DESIGN §1a's second-translation check is not built,
   and 4,018 tranche-B claims come from prophecy and sacred texts.

## What the rest of tranche B would cost

At the pilot's rates (1,700 tokens a claim, with the concept stages growing less than linearly),
the other 43,711 claims would take about 50–65M tokens, 25–35% of a week at today's rate, and
6–10 hours at 20 agents. The pilot covered society and politics only. The event claims about
space (6,331) and war (6,069) will often match tranche A's concepts, whose milestones exist, so
their yield should be higher than 2.9%; the pilot cannot say how much higher. At the pilot's
yield the whole tranche would add about 1,300 realized claims and 2,900 points to tranche A's
15,803 and 26,129, most of it to the futurists and the writers of utopias.

## Decisions for this checkpoint

1. Run the rest of tranche B as piloted, run it only on the event domains first, redesign its
   first stage (propose concepts from a sample, then match once) and run a second pilot, or leave
   tranche B and publish tranche A (DESIGN §10).
2. Whether the prophecy and sacred texts wait for the second-translation check.
3. Whether tranche B's winners join the awards page as their own categories (society and
   politics, war, the future of nations) or only once the whole tranche has run.
