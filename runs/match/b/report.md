# Tranche B: events and social change (run `b`)

Run 2026-11-19 under [`../PLAN.md`](../PLAN.md) §9, seeded from the pilot
([`../bpilot/report.md`](../bpilot/report.md)), on a local machine with Claude Code Sonnet subagents
and no API calls. The rankings and resolutions are in [`scoring.md`](scoring.md), the milestones in
[`milestones.jsonl`](milestones.jsonl) (tranche A's, the pilot's and this run's), the tier-2 table in
[`deciding_milestones.md`](deciding_milestones.md). The combined awards of both tranches are
[`../awards.html`](../awards.html).

## Summary

- **46,211 claims about events, politics, economics and ways of living** from 3,182 books, every
  tranche-B claim of the export (the pilot's 2,500 among them, matched again). 3,644 came true
  (7.9%), against 20.4% in tranche A and 2.9% in the pilot; 8,474 came after their event (not a
  prediction), 30,079 are open (16,372 with no milestone, 7,445 too vague, 6,149 with no concept),
  3,669 are untestable, and 328 missed a deadline they named.
- **2,493 book entries from 1,097 books and 504 authors score, 5,914 points.** H. G. Wells leads
  (250 points), then George Griffith (126), Jules Verne (108), George O. Smith and Murray Leinster.
  The top books are Bellamy's *Equality* (1897), More's *Utopia* (1516), Donnelly's *Cæsar's Column*
  (1890) and Wells's *Anticipations* (1901). *Utopia* has the five best single predictions: a
  painless death for those who choose it (1985), the abolition of money (1975) and of private
  property (1918), a welfare state (1883) and communal dining (1958).
- **The yield is highest where tranche A's concepts reach:** 35.6% of computing claims, 17.8% of
  transport and 14.2% of space came true, against 5.7% of society and politics (20,232 claims).
- **Combined with tranche A** (the awards): 123,647 claims, 19,441 realized, 13,471 book entries,
  31,216 points (a book counts an idea once, from its best claim in either tranche). Wells passes
  E. E. Smith as Grand Prognosticator, 549.5 points to 467.5, and Thomas More's *Utopia* takes the
  best single prediction and the longest view.
- **Cost:** 360 agents, 50.6M tokens and 22 agent-hours, inside the pilot's 50–65M estimate. Weekly
  usage went from 16% to 29% at the last check.

## How it ran

| Stage | Agents | Tokens | Result |
|---|---|---|---|
| First pass against the registry (1,884 concepts) | 139 | 16.1M | 38.8% matched; 14,889 no concept, 7,389 too vague, 6,016 untestable |
| Gap proposals for every unmatched claim | 24 | 5.3M | 1,322 proposals |
| Consolidation by domain group, then a global merge | 9 | 2.1M | 540 new concepts; 70 proposals mapped to existing ones |
| Gap matching | 81 | 14.7M | 62.6% matched in all (11,031 by the gap pass); 15 concepts under three claims cut |
| Quick checks, tier 1, second look | 36 | 3.8M | 324 milestones for 281 of the 525 new concepts |
| Judging, two judges and a third | 48 | 5.7M | 3,812 pairs; 69% same score, 30% one step apart |
| Tier 2 on the deciding concepts | 22 | 2.8M | 102 checked: 80 confirmed, 30 replaced, 3 added |
| Negative check | 1 | 0.1M | 56 denials: 0 contradicted, 17 vindicated, 39 about something else |
| **Total** | **360** | **50.6M** | |

Every source was fetched and checked again by `verify`. The re-judging after tier 2 took 209 pairs
in four batches; 88 more pairs copied the scores of their first-round pair, where tier 2 only dated
the same event more precisely.

## What tier 2 changed

Tranche B's deciding concepts are 238, of which tier 2 checks only its own: tranche A's concepts
keep tranche A's verified milestones, and the pilot's 23 were checked in the pilot. Of the 102
checked, 38 scoring milestones changed. Seven tranche-A concepts that only tranche B's claims made
deciding were checked in tranche A's run (tier2-136, tier2-137) and carried into B's seed
(`milestones_seed.jsonl`), so every one of the 780 concepts that decide the combined awards has
been checked. Most moved earlier with a contemporary source: Tambora (1815)
for a volcano destroying a town, the 1913 Dayton flood for a region-wide blackout, the 1911 census
for London's first fall in population, Armitage's party on the Polar Plateau (January 1903) for the
Antarctic interior. Two answers were overruled on review
([`milestone_review.jsonl`](milestone_review.jsonl)), keeping the earlier milestone:

- **The end of the gold standard:** tier 2 moved it to Sweden's 1745 suspension, a copper standard;
  the definition asks for gold or silver, so the Bank Restriction Act of 1797 stands.
- **Official concealment of a world-changing secret:** tier 2 moved it to the 1900 San Francisco
  plague denial, a local outbreak hidden for business reasons; the Manhattan Project (1942) stands.

Judgment calls kept, each named in its note: air power deciding a war dated to Japan's surrender
(1945, after the Strategic Bombing Survey; the second look had preferred Kosovo, 1999); compulsory
sterilization to Connecticut's 1895 marriage law, which the definition's "forbids or penalizes
reproduction" covers; the first socialist electoral victory to Finland's 1907 election (largest
party, not a majority); whistled speech to Le Canarien (1402), which says only that the Gomerans
speak "as if they had no tongue".

## What is still doubtful

1. **Tier 1 leaned on Wikipedia.** Most researchers used fewer calls than asked and found few
   contemporary sources; most tier-1 milestones are low confidence. Tier 2 fixed the deciding ones
   (it added contemporary sources to most), but the open and low-point concepts rest on reference
   pages.
2. **Many events are matters of reading.** When a war counts as begun, whether a commune of a few
   hundred is a "classless society", whether Italy's 1995 caretaker cabinet is government by experts:
   the judges score such pairs low, which limits the damage, but tranche B's points are softer than
   tranche A's.
3. **The prophecy and sacred texts score with their composition dates,** in one translation each
   (DESIGN §1a's second-translation check is not built). *The Sibylline Oracles* (700) and the
   *Mahabharata* (400) earn points for a sweeping fire and the end of property; the awards keep the
   ancient texts in their own category.
4. **The quick checks answered from memory.** The six check batches (219 concepts guessed never to
   have come true) ran no searches; their 54 "fits" went on to tier 1, but a real event they missed
   leaves its claims open.
5. **The negative check found no real "never" in tranche B.** Of 56 denials the pipeline flagged, 17
   came true as written (Norman Angell's case that conquest no longer pays, against the European Coal
   and Steel Community) and 39 deny something else. The Famous Last Words award stays with tranche A.

## For a next run

- Propose concepts from a sample before matching, as the pilot advised: the first pass against
  tranche A's registry cost 16M tokens to match 39%, and the gap pass did the rest.
- Ask the quick checks to search, and tier 1 to cite one contemporary source per milestone.
- State in the tier-2 prompt that a named place ("Britain") comes true only for that place; one
  answer read England as Britain.
