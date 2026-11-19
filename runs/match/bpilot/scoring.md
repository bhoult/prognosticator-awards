# Scoring after tier 2, tranche A (PLAN §8)

Written by `match.py score bpilot`. Settings: weight log (w = log2(1 + min(L, 500))), the scoring milestone `first_practical_use` else `first_demonstration`, points from score 0.125 (every judged score above 0), precision from 0.5, `contradicted_negative` from 0.5, deadlines checked against 2026 with 10 years of grace. This scoring follows tier 2 (PLAN §5), which checked 23 deciding concepts, and checkpoint 3's review (`runs/match/milestone_review.jsonl`). Tranche B is not scored. † = scored on a demonstration only (PLAN §14.5).

## Resolutions

2,500 tranche-A claims from 1,062 books.

| resolution | claims | share |
|---|---|---|
| open: no_concept | 670 | 26.8% |
| open: no_milestone | 545 | 21.8% |
| not_a_prediction | 490 | 19.6% |
| open: too_vague | 434 | 17.4% |
| untestable | 268 | 10.7% |
| realized | 73 | 2.9% |
| failed: missed_deadline | 15 | 0.6% |
| open: not_matched | 3 | 0.1% |
| open: no_year | 2 | 0.1% |

Deadlines: 94 `will` claims with a concept have a stated time naming a year, decade or century after publication; 48 of those ended before 2016. Of these, 5 are realized anyway, 15 missed the deadline, and 28 are not a prediction. Of the 5 realized claims with a deadline, 4 came true by it and 1 after it (median 24 years late).

## The top 50 predictions

68 book–concept entries earn points (each book counts its best claim once per concept).

| # | points | score | lead | author | book | concept | milestone | quote |
|---|---|---|---|---|---|---|---|---|
| 1 | 4.32 | 0.75 | 53 | Milo Hastings | *City of Endless Night* (1919) | State-enforced limits on births | 1972 | The Eugenic Staff would cut down the birth rates so that there would only be enough soldiers and workers to f… |
| 2 | 4.23 | 0.75 | 49 | H. G. Wells | *Anticipations* (1901) | Continuous urban megalopolis | 1950 | Practically, by a process of confluence, the whole of Great Britain south of the Highlands seems destined to… |
| 3 | 4.19 | 0.5 | 332 | Thomas More | *Utopia* (1516) | Compulsory or make-work employment | 1848-02-25 | there are no idle persons among them, nor pretences of excusing any from labour. There are no taverns, no ale… |
| 4 | 4.12 | 0.75 | 44 | M. P. Shiel | *The Yellow Danger* (1898) | Anglo-American union or alliance | 1942-01 | The terms of the league proposed by Hardy were occupying the attention of the two Governments, and nearing co… |
| 5 | 4.07 | 0.75 | 42 | E. E. Smith | *Skylark Three* (1930) | State-enforced limits on births | 1972 | Our population must not be allowed to increase, therefore each couple can have only two children. |
| 6 | 3.72 | 0.75 | 30 | P. H. Colomb; Archibald Forbe… | *The Great War of 189-* (1892) | General disarmament | 1922-02-06 | A general disarmament was discussed, and some steps for reducing the armaments on all sides were actually ado… |
| 7 | 3.51 | 0.625 | 48 | George Chetwynd Griffith | *Olga Romanoff* (1894) | Anglo-American union or alliance | 1942-01 | as first President of the Anglo-Saxon Federation, had ensured the victory of the Western races over the Easte… |
| 8 | 3.45 | 0.625 | 45 | Godfrey Sweven | *Limanora* (1903) | Dissent treated as mental illness | 1948 | he was haled before the medicists, and his system was minutely examined for the source of the malady, and for… |
| 9 | 3.43 | 0.625 | 44 | Stanton A. Coblentz | *The Sunken World* (1928) | State-enforced limits on births | 1972 | the Milares Compulsory Population Law |
| 10 | 3.35 | 0.625 | 40 | April Smith | *Birthright* (1955) | Rule by scientists or experts | 1995-01 | Technical ability and sound training in administration had long ago been decided upon as more important than… |
| 11 | 3.28 | 0.5 | 94 | H. G. Wells | *Anticipations* (1901) | Rule by scientists or experts | 1995-01 | to foster the power that will finally supersede democracy and monarchy altogether, the power of the scientifi… |
| 12 | 3.16 | 0.5 | 79 | H. G. Wells | *What Is Coming (A Forecast of Things after the War)* (1916) | Rule by scientists or experts | 1995-01 | some clumsy proposals or even attempts to leave him out, and use "business men," soldiers, admirals, dictator… |
| 13 | 3.10 | 0.625 | 30 | Walter Besant | *The Inner House* (1888) | Abolition of private property | 1918-06 | When the People grew gradually to understand that the welfare of all was the only rule of the governing body,… |
| 14 | 3.06 | 0.5 | 69 | Godfrey Sweven | *Limanora* (1903) | State-enforced limits on births | 1972 | For they had complete command of their own birth-rate and death-rate, and kept the numbers commensurate with… |
| 15 | 3.04 | 0.5 | 67 | H. G. Wells | *A Modern Utopia* (1905) | State-enforced limits on births | 1972 | A state whose population continues to increase in obedience to unchecked instinct, can progress only from bad… |
| 16 | 2.97 | 0.5 | 60 | Edgar Rice Burroughs | *A Princess of Mars* (1912) | State-enforced limits on births | 1972 | By careful selection they rear only the hardiest specimens of each species, and with almost supernatural fore… |
| 17 | 2.93 | 0.75 | 14 | L. J. Stecher Jr. | *Man in a Quandary* (1958) | State-enforced limits on births | 1972 | My parents had been fortunate enough to be selected to have three children and I was to be their first. |
| 18 | 2.93 | 0.5 | 57 | Charlotte Perkins Gilman | *Herland* (1915) | State-enforced limits on births | 1972 | They did effectually and permanently limit the population in numbers, so that the country furnished plenty fo… |
| 19 | 2.79 | 0.5 | 47 | M. P. Shiel | *The Lord of the Sea* (1901) | Jewish state in Palestine | 1948-05-14 | the Sanhedrim being short of funds for a railway, a syndicate of five merchant-princes had offered to buy fro… |
| 20 | 2.77 | 0.875 | 8 | Fritz Leiber | *The Last Letter* (1958) | Disposable paper clothing and strong pa… | 1966 | a head of hair that would have graced a museum beauty, while across the back and—well, "chest" is an inadequa… |
| 21 | 2.75 | 0.625 | 20 | Walter M. Miller | *Conditionally Human* (1952) | State-enforced limits on births | 1972 | Because by keeping the population at five billions, the Federation could insure a decent living standard for… |
| 22 | 2.75 | 0.625 | 20 | George Chetwynd Griffith | *The Angel of the Revolution* (1893) | Reorganization of the Balkans | 1913-05-30 | after four centuries and a half the Turkish dominion in Europe died in its first stronghold. |
| 23 | 2.70 | 0.5 | 41 | Poul Anderson | *The Sensitive Man* (1954) | Rule by scientists or experts | 1995-01 | The last century saw the dictatorship of the elite and the dictatorship of the proletariat. This one seems to… |
| 24 | 2.70 | 0.5 | 41 | George Chetwynd Griffith | *A Honeymoon in Space* (1901) | Anglo-American union or alliance | 1942-01 | She is the first concrete symbol of the Anglo-American Alliance |
| 25 | 2.64 | 0.5 | 38 | Charles A. Stearns | *Even Stephen* (1957) | Rule by scientists or experts | 1995-01 | The Molein barrier exists—let the Technocracy legislate against us until it is blue in the face. |
| 26 | 2.59 | 0.75 | 10 | T. Baron Russell | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | Prohibition of alcohol | 1915-01-01 | it is morally certain that intoxicants will have been legislated out of existence already |
| 27 | 2.59 | 0.375 | 120 | T. R. Malthus | *An Essay on the Principle of Population* (1798) | Abolition of private property | 1918-06 | No man being obliged to guard his little store or provide with anxiety and pain for his restless wants, each… |
| 28 | 2.50 | 0.625 | 15 | Anna Bowman Dodd | *The Republic of the Future* (1887) | Votes and office for women | 1902-06-12 | Probably the comparatively recent emancipation of the women, their new political and social freedom, adds a z… |
| 29 | 2.49 | 0.75 | 9 | George Chetwynd Griffith | *The World Peril of 1910* (1906) | Women in all occupations and war work | 1915 | In thousands of cases, especially in the north, the places of the men were taken by the women; and, in additi… |
| 30 | 2.48 | 0.5 | 30 | Rose Macaulay | *What Not* (1918) | Jewish state in Palestine | 1948-05-14 | It was in consequence of this that Jews—such Jews as had not yet been forcibly repatriated in the Holy City—w… |
| 31 | 2.43 | 0.5 | 28 | William Morris | *News from Nowhere* (1890) | Abolition of private property | 1918-06 | the only reasonable condition of Society was that of pure Communism (such as you now see around you) |
| 32 | 2.38 | 0.625 | 13 | Green Peyton | *The Coming of the Ice* (1926) | Compulsory killing of the old or unfit | 1939-09 | they put to death all the perverts, the criminals, and the insane, ridding the world of the scum for which th… |
| 33 | 2.34 | 0.375 | 74 | Austin Hall; Homer Eon Flint | *The Blind Spot* (1921) | Rule by scientists or experts | 1995-01 | They are the heads of—of the Thomahlia; not the nominal nor political nor religious heads—they are neither ju… |
| 34 | 2.32 | 0.5 | 24 | James William Barlow | *History of a World of Immortals Without a God* (1891) | Women in all occupations and war work | 1915 | as a consequence of the female sex being exempt from the cares of maternity, they take a much larger share in… |
| 35 | 2.24 | 0.625 | 11 | Sam McClatchie | *Mother America* (1961) | State-enforced limits on births | 1972 | Naturally, since those parents are in the genetically superior group, it wouldn't be fair to pit them against… |
| 36 | 2.24 | 0.625 | 11 | E. E. Smith; E. Everett Evans | *Masters of Space* (1961) | State-enforced limits on births | 1972 | Let's see ... say we want a stationary population of a hundred million on our planet. Each couple to have two… |
| 37 | 2.23 | 0.5 | 21 | George Chetwynd Griffith | *The Angel of the Revolution* (1893) | World war between great powers | 1914-08-04 | America was the one great Power not involved in the tremendous struggle that was being waged. |
| 38 | 2.23 | 0.5 | 21 | Poul Anderson | *Inside Earth* (1951) | State-enforced limits on births | 1972 | Only now that we've eliminated famine, plague, and war, they'd breed beyond reason, breed till all the old ev… |
| 39 | 2.16 | 0.5 | 19 | Paul Ernst | *The Planetoid of Peril* (1931) | Continuous urban megalopolis | 1950 | before the United States had fused together into one vast city |
| 40 | 2.16 | 0.25 | 399 | Thomas More | *Utopia* (1516) | Prohibition of alcohol | 1915-01-01 | there are no idle persons among them, nor pretences of excusing any from labour. There are no taverns, no ale… |
| 41 | 2.15 | 0.25 | 384 | (text) | *The Sibylline Oracles* (700) | The papacy removed from Rome | 1084 | And Rome is no more to be seen or hoard, Such as of late another traveler saw; For all these things shall in… |
| 42 | 2.14 | 0.375 | 51 | Walter Besant | *The Inner House* (1888) | Compulsory killing of the old or unfit | 1939-09 | he opposed the extinction of property, and would have had everybody win what he could, and keep it as long as… |
| 43 | 2.04 | 0.25 | 282 | Nostradamus | *The True Prophecies or Prognostications of Michael Nostrada…* (1568) | Mass famine from war or breakdown of su… | 1850 | Father of son shall be Antropophage, |
| 44 | 2.00 | 0.5 | 15 | J. B. S. Haldane | *Daedalus, or Science and the Future* (1924) | Synthetic food | 1939 | This will mean that agriculture will become a luxury, and that mankind will be completely urbanized. |
| 45 | 1.98 | 0.375 | 38 | Tom Godwin | *The Last Victory* (1957) | Rule by scientists or experts | 1995-01 | The Outlanders, refusing to come under Technograte domination, lived as best they could in the deserts, plate… |
| 46 | 1.95 | 0.5 | 14 | Godfrey Sweven | *Limanora* (1903) | Official rating of citizens by aptitude… | 1917 | it has become the custom to test scientifically the nature of every inhabitant of our island every week |
| 47 | 1.90 | 0.5 | 13 | T. Baron Russell | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | Abolition of private property | 1918-06 | the example of some single nation, drifting thus far, and setting up a socialistic State, may serve as a usef… |
| 48 | 1.90 | 0.5 | 13 | M. P. Shiel | *The Lord of the Sea* (1901) | World war between great powers | 1914-08-04 | war between the four Powers had been declared that day at noon from the Stock Exchange steps |
| 49 | 1.88 | 0.625 | 7 | A. Garland Mears | *Mercia, the Astronomer Royal* (1895) | Votes and office for women | 1902-06-12 | These were composed of lady members of Parliament together with the wives of the peers and nobles who in one… |
| 50 | 1.73 | 0.5 | 10 | Kurt Vonnegut | *2 B R 0 2 B* (1962) | State-enforced limits on births | 1972 | The population of the United States was stabilized at forty-million souls. |

## Authors: total points

Each author counts a concept once, from their best book. 53 authors score.

| # | author | points | concepts | books | points per book | precision |
|---|---|---|---|---|---|---|
| 1 | George Chetwynd Griffith | 11.0 | 4 | 6 | 1.8 | 23% of 35 |
| 2 | H. G. Wells | 10.6 | 3 | 27 | 0.4 | 3% of 125 |
| 3 | M. P. Shiel | 8.8 | 3 | 3 | 2.9 | 18% of 17 |
| 4 | Godfrey Sweven | 8.5 | 3 | 2 | 4.2 | 7% of 45 |
| 5 | Thomas More | 6.4 | 2 | 1 | 6.4 | 17% of 6 |
| 6 | Milo Hastings | 6.2 | 3 | 2 | 3.1 | 24% of 17 |
| 7 | Walter Besant | 5.2 | 2 | 1 | 5.2 | 40% of 5 |
| 8 | Poul Anderson | 4.9 | 2 | 24 | 0.2 | 14% of 14 |
| 9 | T. Baron Russell | 4.5 | 2 | 1 | 4.5 | 22% of 9 |
| 10 | E. E. Smith | 4.1 | 1 | 20 | 0.2 | 7% of 29 |
| 11 | Archibald Forbes | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 12 | Charles Lowe | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 13 | David Christie Murray | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 14 | F. N. Maude | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 15 | Frank Scudamore | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 16 | John Frederick Maurice | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 17 | P. H. Colomb | 3.7 | 1 | 1 | 3.7 | 33% of 3 |
| 18 | Stanton A. Coblentz | 3.4 | 1 | 6 | 0.6 | 11% of 9 |
| 19 | April Smith | 3.3 | 1 | 1 | 3.3 | 25% of 4 |
| 20 | Edgar Rice Burroughs | 3.0 | 1 | 21 | 0.1 | 2% of 43 |
| 21 | L. J. Stecher Jr. | 2.9 | 1 | 9 | 0.3 | 33% of 3 |
| 22 | Charlotte Perkins Gilman | 2.9 | 1 | 1 | 2.9 | 10% of 10 |
| 23 | Fritz Leiber | 2.8 | 1 | 29 | 0.1 | 5% of 20 |
| 24 | Walter M. Miller | 2.7 | 1 | 7 | 0.4 | 33% of 3 |
| 25 | Charles A. Stearns | 2.6 | 1 | 8 | 0.3 | 50% of 2 |
| 26 | A. Garland Mears | 2.6 | 2 | 1 | 2.6 | 17% of 12 |
| 27 | T. R. Malthus | 2.6 | 1 | 1 | 2.6 | 0% of 6 |
| 28 | Anna Bowman Dodd | 2.5 | 1 | 1 | 2.5 | 50% of 2 |
| 29 | Rose Macaulay | 2.5 | 1 | 1 | 2.5 | 6% of 16 |
| 30 | William Morris | 2.4 | 1 | 1 | 2.4 | 9% of 11 |

## Books: total points

| # | book | author | group | points | concepts |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | Science-Fiction | 8.5 | 3 |
| 2 | *Anticipations* (1901) | H. G. Wells | Futurism | 7.5 | 2 |
| 3 | *Utopia* (1516) | Thomas More | Classics | 6.4 | 2 |
| 4 | *The Inner House* (1888) | Walter Besant | Science-Fiction | 5.2 | 2 |
| 5 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | Science-Fiction | 5.0 | 2 |
| 6 | *City of Endless Night* (1919) | Milo Hastings | Science-Fiction | 4.8 | 2 |
| 7 | *The Lord of the Sea* (1901) | M. P. Shiel | Science-Fiction | 4.7 | 2 |
| 8 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | Futurism | 4.5 | 2 |
| 9 | *The Yellow Danger* (1898) | M. P. Shiel | Science-Fiction | 4.1 | 1 |
| 10 | *The World Peril of 1910* (1906) | George Chetwynd Griffith | Science-Fiction | 4.1 | 2 |
| 11 | *Skylark Three* (1930) | E. E. Smith | Science-Fiction | 4.1 | 1 |
| 12 | *The Great War of 189-* (1892) | P. H. Colomb; Archibald Forbes; Charles… | Science-Fiction | 3.7 | 1 |
| 13 | *Olga Romanoff* (1894) | George Chetwynd Griffith | Science-Fiction | 3.5 | 1 |
| 14 | *The Sunken World* (1928) | Stanton A. Coblentz | Science-Fiction | 3.4 | 1 |
| 15 | *Birthright* (1955) | April Smith | Science-Fiction | 3.3 | 1 |
| 16 | *What Is Coming (A Forecast of Things after the War)* (1916) | H. G. Wells | Futurism | 3.2 | 1 |
| 17 | *A Modern Utopia* (1905) | H. G. Wells | Science-Fiction | 3.0 | 1 |
| 18 | *A Princess of Mars* (1912) | Edgar Rice Burroughs | Science-Fiction | 3.0 | 1 |
| 19 | *Man in a Quandary* (1958) | L. J. Stecher Jr. | Science-Fiction | 2.9 | 1 |
| 20 | *Herland* (1915) | Charlotte Perkins Gilman | Science-Fiction | 2.9 | 1 |
| 21 | *The Last Letter* (1958) | Fritz Leiber | Science-Fiction | 2.8 | 1 |
| 22 | *Conditionally Human* (1952) | Walter M. Miller | Science-Fiction | 2.7 | 1 |
| 23 | *The Sensitive Man* (1954) | Poul Anderson | Science-Fiction | 2.7 | 1 |
| 24 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | Science-Fiction | 2.7 | 1 |
| 25 | *Even Stephen* (1957) | Charles A. Stearns | Science-Fiction | 2.6 | 1 |
| 26 | *Mercia, the Astronomer Royal* (1895) | A. Garland Mears | Science-Fiction | 2.6 | 2 |
| 27 | *An Essay on the Principle of Population* (1798) | T. R. Malthus | Futurism | 2.6 | 1 |
| 28 | *The Republic of the Future* (1887) | Anna Bowman Dodd | Science-Fiction | 2.5 | 1 |
| 29 | *What Not* (1918) | Rose Macaulay | Science-Fiction | 2.5 | 1 |
| 30 | *News from Nowhere* (1890) | William Morris | Science-Fiction | 2.4 | 1 |

## Precision

Claims realized at a score of 0.5 or more, of all tranche-A claims by the author; authors with 50 or more (3).

| # | author | precision | claims | points |
|---|---|---|---|---|
| 1 | H. G. Wells | 3% | 125 | 10.6 |
| 2 | H. Beam Piper | 2% | 52 | 0.5 |
| 3 | Murray Leinster | 0% | 55 | 0.0 |

## Points per book

Authors with 3 or more books in the corpus (19); every book counts, including those with no tranche-A points.

| # | author | points per book | books | points |
|---|---|---|---|---|
| 1 | M. P. Shiel | 2.9 | 3 | 8.8 |
| 2 | George Chetwynd Griffith | 1.8 | 6 | 11.0 |
| 3 | Homer Eon Flint | 0.6 | 4 | 2.3 |
| 4 | Stanton A. Coblentz | 0.6 | 6 | 3.4 |
| 5 | E. Everett Evans | 0.6 | 4 | 2.2 |
| 6 | Paul Ernst | 0.4 | 5 | 2.2 |
| 7 | Walter M. Miller | 0.4 | 7 | 2.7 |
| 8 | H. G. Wells | 0.4 | 27 | 10.6 |
| 9 | Charles A. Stearns | 0.3 | 8 | 2.6 |
| 10 | L. J. Stecher Jr. | 0.3 | 9 | 2.9 |
| 11 | Tom Godwin | 0.2 | 8 | 2.0 |
| 12 | Edgar Pangborn | 0.2 | 4 | 1.0 |
| 13 | Poul Anderson | 0.2 | 24 | 4.9 |
| 14 | E. E. Smith | 0.2 | 20 | 4.1 |
| 15 | Edgar Rice Burroughs | 0.1 | 21 | 3.0 |
| 16 | Damon Knight | 0.1 | 10 | 1.1 |
| 17 | Fritz Leiber | 0.1 | 29 | 2.8 |
| 18 | Bryce Walton | 0.0 | 38 | 0.8 |
| 19 | H. Beam Piper | 0.0 | 32 | 0.5 |

## By era

The best books of each era, by publication year.

**pre-1900** (16 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Utopia* (1516) | Thomas More | 6.4 |
| 2 | *The Inner House* (1888) | Walter Besant | 5.2 |
| 3 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | 5.0 |
| 4 | *The Yellow Danger* (1898) | M. P. Shiel | 4.1 |
| 5 | *The Great War of 189-* (1892) | P. H. Colomb; Archibald Forbes; Charles… | 3.7 |
| 6 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 3.5 |
| 7 | *Mercia, the Astronomer Royal* (1895) | A. Garland Mears | 2.6 |
| 8 | *An Essay on the Principle of Population* (1798) | T. R. Malthus | 2.6 |
| 9 | *The Republic of the Future* (1887) | Anna Bowman Dodd | 2.5 |
| 10 | *News from Nowhere* (1890) | William Morris | 2.4 |

**1900–1945** (26 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 8.5 |
| 2 | *Anticipations* (1901) | H. G. Wells | 7.5 |
| 3 | *City of Endless Night* (1919) | Milo Hastings | 4.8 |
| 4 | *The Lord of the Sea* (1901) | M. P. Shiel | 4.7 |
| 5 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 4.5 |
| 6 | *The World Peril of 1910* (1906) | George Chetwynd Griffith | 4.1 |
| 7 | *Skylark Three* (1930) | E. E. Smith | 4.1 |
| 8 | *The Sunken World* (1928) | Stanton A. Coblentz | 3.4 |
| 9 | *What Is Coming (A Forecast of Things after the War)* (1916) | H. G. Wells | 3.2 |
| 10 | *A Modern Utopia* (1905) | H. G. Wells | 3.0 |

**1946–1979** (15 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Birthright* (1955) | April Smith | 3.3 |
| 2 | *Man in a Quandary* (1958) | L. J. Stecher Jr. | 2.9 |
| 3 | *The Last Letter* (1958) | Fritz Leiber | 2.8 |
| 4 | *Conditionally Human* (1952) | Walter M. Miller | 2.7 |
| 5 | *The Sensitive Man* (1954) | Poul Anderson | 2.7 |
| 6 | *Even Stephen* (1957) | Charles A. Stearns | 2.6 |
| 7 | *Masters of Space* (1961) | E. E. Smith; E. Everett Evans | 2.2 |
| 8 | *Mother America* (1961) | Sam McClatchie | 2.2 |
| 9 | *Inside Earth* (1951) | Poul Anderson | 2.2 |
| 10 | *The Last Victory* (1957) | Tom Godwin | 2.0 |

**1980+** (0 books score)

| # | book | author | points |
|---|---|---|---|

## Other corpus groups

The non-fiction, classics, prophecy and religious texts. Ancient and translated texts are dated by composition, the end of the scholarly range in each text's English Wikipedia article, pinned to a revision (DESIGN §1a; `runs/match/book_review.jsonl`); the second-translation re-judging of §1a is not built. Religious texts rank by text, not by translator.

| group | book | author | points | rank |
|---|---|---|---|---|
| Classics | *Utopia* (1516) | Thomas More | 6.4 | 3 |
| Futurism | *Anticipations* (1901) | H. G. Wells | 7.5 | 2 |
| Futurism | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 4.5 | 8 |
| Futurism | *What Is Coming (A Forecast of Things after the War)* (1916) | H. G. Wells | 3.2 | 16 |
| Politics | *The Economic Consequences of the Peace* (1919) | John Maynard Keynes | 0.8 | 55 |
| Prophecy | *The Sibylline Oracles* (700) | (text) | 2.1 | 38 |
| Prophecy | *The True Prophecies or Prognostications of Michael Nostrada…* (1568) | Nostradamus | 2.0 | 39 |

## Sensitivity: points only from a score of 0.5

19 of 77 judged `will` pairs score below 0.5; without them 17 entries and 28 of 158 points go. Of the top 30 authors, 28 stay in the top 30; of the top 30 books, 28.

| # | author (default) | points | author (from 0.5) | points |
|---|---|---|---|---|
| 1 | George Chetwynd Griffith | 11.0 | George Chetwynd Griffith | 11.0 |
| 2 | H. G. Wells | 10.6 | H. G. Wells | 10.6 |
| 3 | M. P. Shiel | 8.8 | M. P. Shiel | 8.8 |
| 4 | Godfrey Sweven | 8.5 | Godfrey Sweven | 8.5 |
| 5 | Thomas More | 6.4 | Milo Hastings | 6.2 |
| 6 | Milo Hastings | 6.2 | Poul Anderson | 4.9 |
| 7 | Walter Besant | 5.2 | T. Baron Russell | 4.5 |
| 8 | Poul Anderson | 4.9 | Thomas More | 4.2 |
| 9 | T. Baron Russell | 4.5 | E. E. Smith | 4.1 |
| 10 | E. E. Smith | 4.1 | Archibald Forbes | 3.7 |
| 11 | Archibald Forbes | 3.7 | Charles Lowe | 3.7 |
| 12 | Charles Lowe | 3.7 | David Christie Murray | 3.7 |
| 13 | David Christie Murray | 3.7 | F. N. Maude | 3.7 |
| 14 | F. N. Maude | 3.7 | Frank Scudamore | 3.7 |
| 15 | Frank Scudamore | 3.7 | John Frederick Maurice | 3.7 |
| 16 | John Frederick Maurice | 3.7 | P. H. Colomb | 3.7 |
| 17 | P. H. Colomb | 3.7 | Stanton A. Coblentz | 3.4 |
| 18 | Stanton A. Coblentz | 3.4 | April Smith | 3.3 |
| 19 | April Smith | 3.3 | Walter Besant | 3.1 |
| 20 | Edgar Rice Burroughs | 3.0 | Edgar Rice Burroughs | 3.0 |

## The deciding concepts after tier 2 (PLAN §5)

24 concepts carry a top entry or add 5+ points to the author totals now; tier 2 checked 22 of them (`runs/match/deciding.jsonl` lists every concept selected for it, by round). By criterion (a concept can meet several):

- adds 5+ points to the author totals: 10
- best entry of a top-100 author: 19
- best entry of a top-100 book: 21
- top-300 prediction: 24
- top-50 entry, 1900–1945: 16
- top-50 entry, 1946–1979: 5
- top-50 entry, pre-1900: 15

Their milestones: confidence high 7, low 3, medium 14; 20 have a contemporary source, 2 rest on Wikipedia alone, 0 are demonstrations only.

The 40 that carry the most points, and every one tier 2 did not check:

| concept | points | entries | lead > 40 | milestone | confidence | sources | best entry | tier 2 |
|---|---|---|---|---|---|---|---|---|
| State-enforced limits on births | 40.5 | 15 | 9 | 1972: Singapore's 'Stop at Two' policy: from 1972 (debated in Parliament 24… | medium | contemporary | Milo Hastings, *City of Endless Night* (1919) | checked |
| Rule by scientists or experts | 21.1 | 8 | 5 | 1995-01: Italy: in January 1995 President Scalfaro appointed the central banke… | medium | contemporary | April Smith, *Birthright* (1955) | checked |
| Anglo-American union or alliance | 10.3 | 3 | 4 | 1942-01: At the Arcadia Conference in Washington (22 Dec 1941 - 14 Jan 1942) B… | medium | contemporary | M. P. Shiel, *The Yellow Danger* (1898) | checked |
| Abolition of private property | 10.0 | 4 | 1 | 1918-06: Soviet Russia abolished private ownership of land (Decree on Land, No… | medium | contemporary | Walter Besant, *The Inner House* (1888) | checked |
| Continuous urban megalopolis | 7.8 | 3 | 2 | 1950: By the 1950 census the continuous urbanized belt of the US northeaste… | medium | reference | H. G. Wells, *Anticipations* (1901) | checked |
| Jewish state in Palestine | 6.6 | 3 | 2 | 1948-05-14: David Ben-Gurion read the Declaration of the Establishment of the Sta… | high | contemporary | M. P. Shiel, *The Lord of the Sea* (1901) | checked |
| Votes and office for women | 6.0 | 3 | 1 | 1902-06-12: The Commonwealth of Australia's Commonwealth Franchise Act 1902 (No.… | medium | contemporary | Anna Bowman Dodd, *The Republic of the Future* (1887) | checked |
| Dissent treated as mental illness | 5.7 | 3 | 2 | 1948: The Soviet state, from the late 1940s, began confining political diss… | low | reference | Godfrey Sweven, *Limanora* (1903) | checked |
| World war between great powers | 5.7 | 3 | 0 | 1914-08-04: World War I became a war of most great powers on 4 August 1914, when… | high | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | checked |
| Prohibition of alcohol | 5.6 | 3 | 1 | 1915-01-01: Iceland's nationwide prohibition law, adopted by referendum on 10 Sep… | high | contemporary | T. Baron Russell, *A Hundred Years Hence (The Expecta…* (1905) | checked |
| Women in all occupations and war work | 4.8 | 2 | 0 | 1915: In Britain during the first year of World War I, women began to repla… | medium | contemporary | George Chetwynd Griffith, *The World Peril of 1910* (1906) | checked |
| Compulsory killing of the old or unfit | 4.5 | 2 | 1 | 1939-09: After the German invasion of Poland on 1 September 1939, SS units (Ei… | medium | contemporary | Green Peyton, *The Coming of the Ice* (1926) | checked |
| Reorganization of the Balkans | 4.4 | 2 | 0 | 1913-05-30: By the Treaty of London (30 May 1913) the Ottoman Empire ceded all Eu… | high | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | checked |
| Compulsory or make-work employment | 4.2 | 1 | 1 | 1848-02-25: On 25 February 1848 the French provisional government of the Second R… | high | contemporary | Thomas More, *Utopia* (1516) | checked |
| General disarmament | 3.7 | 1 | 0 | 1922-02-06: The Washington Naval Treaty, signed 6 February 1922 by the United Sta… | medium | contemporary | P. H. Colomb; Archibald…, *The Great War of 189-* (1892) | checked |
| Disposable paper clothing and strong pa… | 2.8 | 1 | 0 | 1966: Scott Paper Company offered a wear-it-once paper dress to the public… | medium | contemporary | Fritz Leiber, *The Last Letter* (1958) | **not checked** |
| International organization to prevent w… | 2.4 | 3 | 0 | 1920-01-10: The Covenant of the League of Nations took effect on 10 January 1920… | high | contemporary | Thomas Dixon Jr., *The Fall of a Nation* (1916) | checked |
| The papacy removed from Rome | 2.1 | 1 | 1 | 1084: In May 1084 Guiscard's Normans relieved Pope Gregory VII and sacked R… | low | Wikipedia only | (text), *The Sibylline Oracles* (700) | checked |
| Mass famine from war or breakdown of su… | 2.0 | 1 | 2 | 1850: The Taiping Rebellion began in China in 1850-51; its 20-30 million de… | low | Wikipedia only | Nostradamus, *The True Prophecies or Prognostica…* (1568) | checked |
| Synthetic food | 2.0 | 1 | 0 | 1939: After the Reich health office cleared synthetic fat for food in Septe… | medium | contemporary | J. B. S. Haldane, *Daedalus, or Science and the Future* (1924) | **not checked** |
| Official rating of citizens by aptitude… | 1.9 | 1 | 0 | 1917: From September 1917 the US Army (Surgeon General) put recruits throug… | high | contemporary | Godfrey Sweven, *Limanora* (1903) | checked |
| Union of Islamic or Arab states, or rev… | 1.5 | 2 | 0 | 1958-02-01: Egypt and Syria merged into the United Arab Republic on 1 February 19… | medium | contemporary | Edgar Pangborn, *West of the Sun* (1953) | checked |
| Mass civilian evacuation and air-raid p… | 1.4 | 1 | 0 | 1917-09: During the German Gotha and Giant night raids on London in late Septe… | medium | contemporary | Milo Hastings, *In the Clutch of the War-God* (1911) | checked |
| International court and war-crimes tria… | 0.8 | 1 | 0 | 1902-09: The Permanent Court of Arbitration at The Hague opened its first form… | medium | contemporary | A. Garland Mears, *Mercia, the Astronomer Royal* (1895) | checked |
