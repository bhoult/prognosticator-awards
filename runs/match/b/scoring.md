# Scoring after tier 2, tranche B (PLAN §8, §9)

Written by `match.py score b`. Settings: weight log (w = log2(1 + min(L, 500))), the scoring milestone `first_practical_use` else `first_demonstration`, points from score 0.125 (every judged score above 0), precision from 0.5, `contradicted_negative` from 0.5, deadlines checked against 2026 with 10 years of grace. This scoring follows tier 2 (PLAN §5), which checked 102 deciding concepts, and checkpoint 3's review (`runs/match/milestone_review.jsonl`). Tranche A is scored on its own (runs/match/scoring.md). † = scored on a demonstration only (PLAN §14.5).

## Resolutions

46,211 tranche-B claims from 3,182 books.

| resolution | claims | share |
|---|---|---|
| open: no_milestone | 16,372 | 35.4% |
| not_a_prediction | 8,474 | 18.3% |
| open: too_vague | 7,445 | 16.1% |
| open: no_concept | 6,149 | 13.3% |
| untestable | 3,669 | 7.9% |
| realized | 3,644 | 7.9% |
| failed: missed_deadline | 328 | 0.7% |
| open: no_year | 45 | 0.1% |
| open: not_contradicted | 39 | 0.1% |
| open: not_matched | 29 | 0.1% |
| vindicated | 17 | 0.0% |

Deadlines: 1,732 `will` claims with a concept have a stated time naming a year, decade or century after publication; 969 of those ended before 2016. Of these, 216 are realized anyway, 328 missed the deadline, and 425 are not a prediction. Of the 307 realized claims with a deadline, 242 came true by it and 65 after it (median 17 years late).

## The top 50 predictions

2,493 book–concept entries earn points (each book counts its best claim once per concept).

| # | points | score | lead | author | book | concept | milestone | quote |
|---|---|---|---|---|---|---|---|---|
| 1 | 6.66 | 0.75 | 469 | Thomas More | *Utopia* (1516) | Painless death on demand | 1985 | Such as are wrought on by these persuasions either starve themselves of their own accord, or take opium, and… |
| 2 | 6.63 | 0.75 | 459 | Thomas More | *Utopia* (1516) | Abolition of money | 1975 | they have no use for money among themselves, but keep it as a provision against events which seldom happen |
| 3 | 6.49 | 0.75 | 402 | Thomas More | *Utopia* (1516) | Abolition of private property | 1918-06 | the setting all upon a level was the only way to make a nation happy; which cannot be obtained so long as the… |
| 4 | 6.39 | 0.75 | 367 | Thomas More | *Utopia* (1516) | Welfare state | 1883 | there is no less care taken of those who were once engaged in labour, but grow afterwards unable to follow it… |
| 5 | 6.09 | 0.75 | 278 | Cyrano de Bergerac | *A Voyage to the Moon* (1657) | Audiobook player | 1935 | they may have in their Pockets, or at their Girdles, Thirty of these Books, where they need but wind up a Spr… |
| 6 | 6.05 | 0.75 | 267 | Tommaso Campanella | *The City of the Sun* (1602) | Eugenic breeding of humans | 1869 | Love is foremost in attending to the charge of the race. He sees that men and women are so joined together, t… |
| 7 | 5.61 | 0.625 | 1218 | (text) | *The Sibylline Oracles* (700) | Abolition of private property | 1918-06 | For deceitful gold Shall no more be nor silver, nor acquiring Of the earth, nor much-laboring servitude; But… |
| 8 | 5.61 | 0.625 | 1425 | (text) | *The Mahabharata, Volume 4 (Books 13-18)* (400) | Vast forest fire | 1825-10-07 | The fire thus cast off grew in the woods. It then produced a general conflagration in the forest. |
| 9 | 5.49 | 0.625 | 442 | Thomas More | *Utopia* (1516) | Communal dining replaces home cooking | 1958 | the whole Syphogranty being called together by sound of trumpet, they meet and eat together |
| 10 | 5.36 | 0.75 | 141 | George Tucker | *A Voyage to the Moon* (1827) | Earth seen from space or another world † | 1968-12-21 | As the earth turned round its axis, during their ascent, every part of its surface came successively under vi… |
| 11 | 5.31 | 0.75 | 134 | Adam Seaborn | *Symzonia* (1820) | Nuclear deterrence | 1954-01-12 | I would abolish war by ensuring inevitable destruction to all who engaged in it |
| 12 | 5.24 | 0.625 | 332 | Thomas More | *Utopia* (1516) | Compulsory or make-work employment | 1848-02-25 | The chief, and almost the only, business of the Syphogrants is to take care that no man may live idle, but th… |
| 13 | 5.19 | 0.625 | 316 | Tommaso Campanella | *The City of the Sun* (1602) | Abolition of private property | 1918-06 | All things are common with them, and their dispensation is by the authority of the magistrates. Arts and hono… |
| 14 | 5.19 | 0.75 | 120 | George Tucker | *A Voyage to the Moon* (1827) | Indian independence from Britain | 1947-08-15 | the whole of Hindostan would be emancipated from its European masters, and assume that rank among nations to… |
| 15 | 5.18 | 0.625 | 313 | Tommaso Campanella | *The City of the Sun* (1602) | Women in all occupations and war work | 1915 | The women also are taught these arts under their own magistrates and mistresses, so that they may be able if… |
| 16 | 5.18 | 0.625 | 313 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Abolition of money | 1975 | money was among the fabulous stories of the World of the Moon whence I came and I had practically lost all me… |
| 17 | 5.15 | 0.75 | 116 | George Chetwynd Griffith | *The World Peril of 1910* (1906) | Planetary defense against comets and as… † | 2022-09-26 | day by day the Invader from Space grew bigger and brighter in the great reflector, and day by day the huge ca… |
| 18 | 5.15 | 0.75 | 116 | H. G. Wells | *When the Sleeper Wakes* (1899) | Cash replaced by cheques and accounts | 2015 | The common traffic of the city, the common currency indeed of all the world, was conducted by means of the li… |
| 19 | 5.06 | 0.75 | 106 | Arthur Cheney Train; Robert W… | *The Moon Maker* (1916) | Planetary defense against comets and as… † | 2022-09-26 | Professor Benjamin Hooker and his daring companions have achieved their stupendous object of diverting the fa… |
| 20 | 5.04 | 0.75 | 104 | Hugo Gernsback | *Ralph 124C 41+* (1911) | Cash replaced by cheques and accounts | 2015 | Therefore, when gold and silver became practically valueless, nothing happened, because actual coins were no… |
| 21 | 5.03 | 0.75 | 103 | Charles Wilder Glass | *Ruth's Marriage in Mars* (1912) | Cash replaced by cheques and accounts | 2015 | We are taught to give the laborer all he earns; each has all he can earn, all are paid in checks and no money… |
| 22 | 4.99 | 0.75 | 100 | Camille Flammarion | *Omega* (1893) | European political union | 1993-11-01 | the president of the United States of Europe, the director of the French republic, the directors of the Itali… |
| 23 | 4.99 | 0.75 | 100 | H. G. Wells | *When the Sleeper Wakes* (1899) | Common currency across many states | 1999-01-01 | The common traffic of the city, the common currency indeed of all the world, was conducted by means of the li… |
| 24 | 4.99 | 0.75 | 100 | Guy Thorne | *The Soul Stealer* (1906) | Mind-reading machine † | 2006 | No one will lie any more because every one will realize that lying will be useless, when your machine can sea… |
| 25 | 4.97 | 0.75 | 98 | Jules Verne | *All Around the Moon* (1870) | Crewed flight around the Moon and back | 1968-12-24 | At half past two in the morning of December 6th, the travellers crossed the 30th northern parallel, at a dist… |
| 26 | 4.96 | 0.75 | 97 | Jules Verne | *The Moon-Voyage* (1872) | Crewed Moon landing † | 1969-07-20 | They have arrived, sir," exclaimed a young midshipman, "and they are doing what all travellers do in a new co… |
| 27 | 4.95 | 0.75 | 96 | Jules Verne | *The Moon-Voyage* (1872) | Crewed flight around the Moon and back | 1968-12-24 | At the moment this phenomenon took place the projectile was grazing the moon's North Pole, at less that twent… |
| 28 | 4.95 | 0.75 | 96 | Jules Verne | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Crewed flight around the Moon and back | 1968-12-24 | The expedition of Barbicane and his friends round the moon had enabled them to correct the many admitted theo… |
| 29 | 4.94 | 0.75 | 95 | Ignatius Donnelly | *Cæsar's Column* (1890) | Painless death on demand | 1985 | in this city they actually facilitate suicide! A race of philosophers has arisen in the last fifty years who… |
| 30 | 4.93 | 0.75 | 94 | H. G. Wells | *Anticipations* (1901) | Rule by scientists or experts | 1995-01 | The suppression of the party machine in the purely democratic countries and of the official choice of the ric… |
| 31 | 4.90 | 0.75 | 92 | H. G. Wells | *Anticipations* (1901) | European political union | 1993-11-01 | The splendid dream of a Federal Europe, which opened the nineteenth century for France, may perhaps, after al… |
| 32 | 4.90 | 0.625 | 229 | Nostradamus | *Oracles of Nostradamus* (1568) | End of the gold standard and metallic m… | 1797-02 | A properly regulated paper-money issue, based on the taxation of a State, having absolutely no intrinsic valu… |
| 33 | 4.89 | 0.75 | 91 | Jules Verne | *All Around the Moon* (1870) | Black sky filled with stars seen from s… † | 1961-04-12 | We are driving through space! Look at the stars glittering all around! Brighter, but smaller than we have eve… |
| 34 | 4.87 | 0.625 | 221 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Welfare state | 1883 | as soon as a woman is delivered in the city, the treasury furnishes an annual sum for the education of the ch… |
| 35 | 4.87 | 0.75 | 89 | Jules Verne | *The Moon-Voyage* (1872) | Spaceflight as mass spectacle and merch… | 1961-05-05 | It was already easy to foresee that the day of the experiment the concourse of spectators would be counted by… |
| 36 | 4.84 | 0.75 | 87 | Mary Wollstonecraft Shelley | *The Last Man* (1826) | Reorganization of the Balkans | 1913-05-30 | to eradicate from Europe a power which, while every other nation advanced in civilization, stood still, a mon… |
| 37 | 4.84 | 0.75 | 87 | Edward Bellamy | *Looking Backward* (1888) | Abolition of money | 1975 | Nevertheless, here I wake up to find myself among a people of whom a cartload of gold will not procure a loaf… |
| 38 | 4.83 | 0.75 | 86 | H. G. Wells | *Tales of Space and Time* (1899) | Painless death on demand | 1985 | You'd better go right away," said the medical man, "and make the Euthanasia. The sooner the better. |
| 39 | 4.83 | 0.75 | 86 | H. G. Wells | *When the Sleeper Wakes* (1899) | Painless death on demand | 1985 | And we have an institution called Euthanasy. |
| 40 | 4.82 | 0.75 | 85 | William Morris | *News from Nowhere* (1890) | Abolition of money | 1975 | as there is no buying and selling, it would be mere insanity to make goods on the chance of their being wante… |
| 41 | 4.82 | 0.75 | 85 | Edward Bellamy | *Equality* (1897) | Guaranteed basic income or citizen divi… | 1982 | Prices or cost estimates are put on these commodities and services, and the aggregate sum of the prices being… |
| 42 | 4.79 | 0.75 | 83 | Edward Bulwer Lytton | *The Coming Race* (1871) | Nuclear deterrence | 1954-01-12 | If army met army, and both had command of this agency, it could be but to the annihilation of each. The age o… |
| 43 | 4.77 | 0.75 | 81 | Godfrey Sweven | *Riallaro* (1901) | Guaranteed basic income or citizen divi… | 1982 | By our constitution every citizen was entitled to a certain minimum of food and clothing in the year. |
| 44 | 4.74 | 0.75 | 79 | Mary Griffith | *Camperdown* (1836) | End of the working horse | 1915 | It is upwards of a hundred years since horses were used either for the saddle or carriage; and full two hundr… |
| 45 | 4.74 | 0.75 | 79 | Mary Griffith | *Camperdown* (1836) | Prohibition of alcohol | 1915-01-01 | for spirituous liquors have been prohibited by law for upwards of two hundred years. |
| 46 | 4.73 | 0.75 | 78 | Percy Greg | *Across the Zodiac* (1880) | Communal dining replaces home cooking | 1958 | all but the very simplest cookery is performed by professional confectioners, who supply twice a day the hous… |
| 47 | 4.73 | 0.75 | 78 | Robert Hugh Benson | *Lord of the World* (1907) | Painless death on demand | 1985 | They were the ministers of euthanasia. Then she felt herself taken by the shoulder |
| 48 | 4.73 | 0.75 | 78 | George Gordon Hastings | *The First American King* (1904) | Guaranteed basic income or citizen divi… | 1982 | It could, if necessary, pay out dividends to its citizens, as the big corporations do to their share-holders. |
| 49 | 4.69 | 0.75 | 75 | L. P. Gratacap | *The Mayor of New York* (1910) | Painless death on demand | 1985 | Euthanasia, although a forbidden crime as the enemy of the state, is secretly practised and from day to day s… |
| 50 | 4.67 | 0.75 | 74 | Godfrey Sweven | *Riallaro* (1901) | Abolition of money | 1975 | Money had been abolished, but everything that was substituted for it—labour ticket, token, bread, fruit—came… |

## Authors: total points

Each author counts a concept once, from their best book. 504 authors score.

| # | author | points | concepts | books | points per book | precision |
|---|---|---|---|---|---|---|
| 1 | H. G. Wells | 249.7 | 89 | 27 | 9.2 | 13% of 1963 |
| 2 | George Chetwynd Griffith | 125.8 | 39 | 6 | 21.0 | 21% of 594 |
| 3 | Jules Verne | 107.5 | 36 | 16 | 6.7 | 11% of 506 |
| 4 | George O. Smith | 95.7 | 43 | 57 | 1.7 | 7% of 718 |
| 5 | Murray Leinster | 94.4 | 47 | 58 | 1.6 | 6% of 962 |
| 6 | Edward Bellamy | 82.4 | 28 | 5 | 16.5 | 27% of 451 |
| 7 | Ray Cummings | 80.4 | 30 | 36 | 2.2 | 6% of 664 |
| 8 | Edmond Hamilton | 69.9 | 26 | 34 | 2.1 | 6% of 434 |
| 9 | Godfrey Sweven | 69.5 | 26 | 2 | 34.8 | 9% of 308 |
| 10 | Thomas More | 66.7 | 14 | 1 | 66.7 | 26% of 74 |
| 11 | Ignatius Donnelly | 65.5 | 21 | 1 | 65.5 | 15% of 156 |
| 12 | E. E. Smith | 55.7 | 22 | 20 | 2.8 | 4% of 591 |
| 13 | M. P. Shiel | 49.5 | 19 | 3 | 16.5 | 7% of 381 |
| 14 | John W. Campbell Jr | 45.8 | 19 | 11 | 4.2 | 9% of 183 |
| 15 | Mack Reynolds | 45.2 | 17 | 35 | 1.3 | 4% of 590 |
| 16 | Robert Hugh Benson | 45.0 | 19 | 2 | 22.5 | 8% of 350 |
| 17 | Randall Garrett | 44.4 | 20 | 78 | 0.6 | 3% of 623 |
| 18 | Camille Flammarion | 43.6 | 15 | 3 | 14.5 | 14% of 134 |
| 19 | Garrett Putman Serviss | 41.1 | 15 | 6 | 6.8 | 8% of 210 |
| 20 | Alexis de Tocqueville | 38.3 | 12 | 2 | 19.1 | 4% of 453 |
| 21 | Richard M. Elam | 37.7 | 19 | 3 | 12.6 | 16% of 92 |
| 22 | William Morris | 37.0 | 12 | 1 | 37.0 | 16% of 148 |
| 23 | Edgar Rice Burroughs | 35.7 | 13 | 21 | 1.7 | 2% of 521 |
| 24 | Raymond Z. Gallun | 35.6 | 17 | 17 | 2.1 | 4% of 289 |
| 25 | Milo Hastings | 35.5 | 14 | 2 | 17.8 | 12% of 179 |
| 26 | Carey Rockwell | 35.4 | 18 | 6 | 5.9 | 8% of 229 |
| 27 | Olaf Stapledon | 34.9 | 14 | 1 | 34.9 | 5% of 168 |
| 28 | Nelson S. Bond | 33.9 | 14 | 37 | 0.9 | 5% of 309 |
| 29 | George Allan England | 33.6 | 16 | 3 | 11.2 | 6% of 303 |
| 30 | Arthur Cheney Train | 33.6 | 12 | 2 | 16.8 | 18% of 76 |

## Books: total points

| # | book | author | group | points | concepts |
|---|---|---|---|---|---|
| 1 | *Equality* (1897) | Edward Bellamy | Science-Fiction | 68.4 | 23 |
| 2 | *Utopia* (1516) | Thomas More | Classics | 66.7 | 14 |
| 3 | *Cæsar's Column* (1890) | Ignatius Donnelly | Science-Fiction | 65.5 | 21 |
| 4 | *Anticipations* (1901) | H. G. Wells | Futurism | 64.2 | 22 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | Science-Fiction | 54.1 | 18 |
| 6 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | Science-Fiction | 49.6 | 16 |
| 7 | *Looking Backward* (1888) | Edward Bellamy | Science-Fiction | 49.5 | 15 |
| 8 | *Omega* (1893) | Camille Flammarion | Science-Fiction | 43.5 | 15 |
| 9 | *A Modern Utopia* (1905) | H. G. Wells | Science-Fiction | 43.2 | 16 |
| 10 | *Tales of Space and Time* (1899) | H. G. Wells | Science-Fiction | 39.8 | 13 |
| 11 | *The Moon-Voyage* (1872) | Jules Verne | Science-Fiction | 38.9 | 11 |
| 12 | *Riallaro* (1901) | Godfrey Sweven | Science-Fiction | 38.3 | 15 |
| 13 | *News from Nowhere* (1890) | William Morris | Science-Fiction | 37.0 | 12 |
| 14 | *The Yellow Danger* (1898) | M. P. Shiel | Science-Fiction | 35.4 | 14 |
| 15 | *Last and First Men* (1930) | Olaf Stapledon | Science-Fiction | 34.9 | 14 |
| 16 | *Lord of the World* (1907) | Robert Hugh Benson | Science-Fiction | 34.2 | 14 |
| 17 | *Limanora* (1903) | Godfrey Sweven | Science-Fiction | 33.9 | 13 |
| 18 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | Futurism | 32.9 | 13 |
| 19 | *The Inner House* (1888) | Walter Besant | Science-Fiction | 32.8 | 10 |
| 20 | *All Around the Moon* (1870) | Jules Verne | Science-Fiction | 31.2 | 10 |
| 21 | *What Is Coming (A Forecast of Things after the War)* (1916) | H. G. Wells | Futurism | 30.1 | 15 |
| 22 | *When the Sleeper Wakes* (1899) | H. G. Wells | Science-Fiction | 29.7 | 8 |
| 23 | *Mercia, the Astronomer Royal* (1895) | A. Garland Mears | Science-Fiction | 29.3 | 10 |
| 24 | *The World Peril of 1910* (1906) | George Chetwynd Griffith | Science-Fiction | 28.1 | 12 |
| 25 | *The Sleeper Awakes* (1899) | H. G. Wells | Science-Fiction | 27.3 | 10 |
| 26 | *Democracy in America, Volume 2* (1840) | Alexis de Tocqueville | Politics | 26.9 | 9 |
| 27 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | Science-Fiction | 26.7 | 8 |
| 28 | *The World Set Free* (1913) | H. G. Wells | Science-Fiction | 26.7 | 12 |
| 29 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | Science-Fiction | 26.6 | 13 |
| 30 | *Across the Zodiac* (1880) | Percy Greg | Science-Fiction | 26.5 | 9 |

## Precision

Claims realized at a score of 0.5 or more, of all tranche-B claims by the author; authors with 50 or more (214).

| # | author | precision | claims | points |
|---|---|---|---|---|
| 1 | Rose Macaulay | 31% | 108 | 25.7 |
| 2 | Edward Bellamy | 27% | 451 | 82.4 |
| 3 | Ferdinand Heinrich Grautoff | 26% | 114 | 11.1 |
| 4 | Thomas More | 26% | 74 | 66.7 |
| 5 | Walter Besant | 23% | 78 | 32.8 |
| 6 | Jeff Sutton | 21% | 56 | 14.3 |
| 7 | George Chetwynd Griffith | 21% | 594 | 125.8 |
| 8 | A. Garland Mears | 20% | 80 | 29.3 |
| 9 | Arthur Cheney Train | 18% | 76 | 33.6 |
| 10 | Robert Williams Wood | 18% | 76 | 33.6 |
| 11 | Ellison Harding | 17% | 103 | 21.1 |
| 12 | Roy Rockwood | 17% | 78 | 18.3 |
| 13 | Donald A. Wollheim | 16% | 73 | 14.4 |
| 14 | Richard M. Elam | 16% | 92 | 37.7 |
| 15 | William Morris | 16% | 148 | 37.0 |
| 16 | Mary E. Bradley Lane | 15% | 72 | 22.4 |
| 17 | Guy Thorne | 15% | 92 | 22.3 |
| 18 | Norman Angell | 15% | 198 | 20.4 |
| 19 | George S. Schuyler | 15% | 60 | 3.4 |
| 20 | Ignatius Donnelly | 15% | 156 | 65.5 |

## Points per book

Authors with 3 or more books in the corpus (212); every book counts, including those with no tranche-A points.

| # | author | points per book | books | points |
|---|---|---|---|---|
| 1 | George Chetwynd Griffith | 21.0 | 6 | 125.8 |
| 2 | M. P. Shiel | 16.5 | 3 | 49.5 |
| 3 | Edward Bellamy | 16.5 | 5 | 82.4 |
| 4 | Camille Flammarion | 14.5 | 3 | 43.6 |
| 5 | Richard M. Elam | 12.6 | 3 | 37.7 |
| 6 | George Allan England | 11.2 | 3 | 33.6 |
| 7 | H. G. Wells | 9.2 | 27 | 249.7 |
| 8 | Jack London | 9.0 | 3 | 27.1 |
| 9 | Guy Thorne | 7.4 | 3 | 22.3 |
| 10 | Garrett Putman Serviss | 6.8 | 6 | 41.1 |
| 11 | Jules Verne | 6.7 | 16 | 107.5 |
| 12 | Carey Rockwell | 5.9 | 6 | 35.4 |
| 13 | Charles Willard Diffin | 5.7 | 4 | 22.8 |
| 14 | J. D. Beresford | 5.1 | 3 | 15.2 |
| 15 | William Hope Hodgson | 4.7 | 4 | 18.8 |
| 16 | John W. Campbell Jr | 4.2 | 11 | 45.8 |
| 17 | E. Everett Evans | 3.8 | 4 | 15.1 |
| 18 | Leigh Richmond | 3.7 | 3 | 11.0 |
| 19 | Ray Palmer | 3.5 | 3 | 10.5 |
| 20 | Robert Bloch | 3.5 | 3 | 10.5 |

## By era

The best books of each era, by publication year.

**pre-1900** (105 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Equality* (1897) | Edward Bellamy | 68.4 |
| 2 | *Utopia* (1516) | Thomas More | 66.7 |
| 3 | *Cæsar's Column* (1890) | Ignatius Donnelly | 65.5 |
| 4 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 54.1 |
| 5 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | 49.6 |
| 6 | *Looking Backward* (1888) | Edward Bellamy | 49.5 |
| 7 | *Omega* (1893) | Camille Flammarion | 43.5 |
| 8 | *Tales of Space and Time* (1899) | H. G. Wells | 39.8 |
| 9 | *The Moon-Voyage* (1872) | Jules Verne | 38.9 |
| 10 | *News from Nowhere* (1890) | William Morris | 37.0 |

**1900–1945** (341 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Anticipations* (1901) | H. G. Wells | 64.2 |
| 2 | *A Modern Utopia* (1905) | H. G. Wells | 43.2 |
| 3 | *Riallaro* (1901) | Godfrey Sweven | 38.3 |
| 4 | *Last and First Men* (1930) | Olaf Stapledon | 34.9 |
| 5 | *Lord of the World* (1907) | Robert Hugh Benson | 34.2 |
| 6 | *Limanora* (1903) | Godfrey Sweven | 33.9 |
| 7 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 32.9 |
| 8 | *What Is Coming (A Forecast of Things after the War)* (1916) | H. G. Wells | 30.1 |
| 9 | *The World Peril of 1910* (1906) | George Chetwynd Griffith | 28.1 |
| 10 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | 26.7 |

**1946–1979** (651 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | 26.6 |
| 2 | *The Planet Strappers* (1961) | Raymond Z. Gallun | 18.7 |
| 3 | *Space Tug* (1953) | Murray Leinster | 16.2 |
| 4 | *Men Into Space* (1960) | Murray Leinster | 16.0 |
| 5 | *Hellflower* (1952) | George O. Smith | 14.6 |
| 6 | *Space Station 1* (1957) | Frank Belknap Long | 13.9 |
| 7 | *Treachery in Outer Space* (1954) | Carey Rockwell | 13.7 |
| 8 | *Space Platform* (1953) | Murray Leinster | 13.1 |
| 9 | *The Man Who Staked the Stars* (1952) | Katherine MacLean | 13.0 |
| 10 | *First on the Moon* (1958) | Jeff Sutton | 12.8 |

**1980+** (0 books score)

| # | book | author | points |
|---|---|---|---|

## Other corpus groups

The non-fiction, classics, prophecy and religious texts. Ancient and translated texts are dated by composition, the end of the scholarly range in each text's English Wikipedia article, pinned to a revision (DESIGN §1a; `runs/match/book_review.jsonl`); the second-translation re-judging of §1a is not built. Religious texts rank by text, not by translator.

| group | book | author | points | rank |
|---|---|---|---|---|
| Classics | *Utopia* (1516) | Thomas More | 66.7 | 2 |
| Classics | *The City of the Sun* (1602) | Tommaso Campanella | 21.4 | 38 |
| Classics | *New Atlantis* (1627) | Francis Bacon | 7.0 | 210 |
| Fiction | *The Strength of the Strong* (1914) | Jack London | 7.4 | 202 |
| Fiction | *Futility (The Wreck of the Titan)* (1898) | Morgan Robertson | 4.1 | 391 |
| Fiction | *Actions and Reactions* (1909) | Rudyard Kipling | 2.7 | 613 |
| Futurism | *Anticipations* (1901) | H. G. Wells | 64.2 | 4 |
| Futurism | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 32.9 | 18 |
| Futurism | *What Is Coming (A Forecast of Things after the War)* (1916) | H. G. Wells | 30.1 | 21 |
| Philosophy | *The Decline of the West, Volume 2* (1928) | Oswald Spengler | 11.7 | 112 |
| Philosophy | *The Decline of the West, Volume 1* (1926) | Oswald Spengler | 7.5 | 196 |
| Politics | *Democracy in America, Volume 2* (1840) | Alexis de Tocqueville | 26.9 | 26 |
| Politics | *Democracy in America, Volume 1* (1835) | Alexis de Tocqueville | 17.6 | 60 |
| Politics | *The Economic Consequences of the Peace* (1919) | John Maynard Keynes | 10.0 | 138 |
| Prophecy | *The Sibylline Oracles* (700) | (text) | 16.7 | 65 |
| Prophecy | *The True Prophecies or Prognostications of Michael Nostrada…* (1568) | Nostradamus | 14.1 | 85 |
| Prophecy | *Oracles of Nostradamus* (1568) | Nostradamus | 13.2 | 95 |
| Religion | *The Mahabharata, Volume 1 (Books 1-3)* (400) | (text) | 13.5 | 91 |
| Religion | *The Mahabharata, Volume 4 (Books 13-18)* (400) | (text) | 12.3 | 106 |
| Religion | *The Mahabharata, Volume 2 (Books 4-7)* (400) | (text) | 9.0 | 155 |
| Science | *Side-Lights on Astronomy* (1906) | Simon Newcomb | 6.1 | 245 |

## Sensitivity: points only from a score of 0.5

1,049 of 3,747 judged `will` pairs score below 0.5; without them 624 entries and 902 of 5,914 points go. Of the top 30 authors, 26 stay in the top 30; of the top 30 books, 29.

| # | author (default) | points | author (from 0.5) | points |
|---|---|---|---|---|
| 1 | H. G. Wells | 249.7 | H. G. Wells | 231.1 |
| 2 | George Chetwynd Griffith | 125.8 | George Chetwynd Griffith | 123.5 |
| 3 | Jules Verne | 107.5 | George O. Smith | 85.9 |
| 4 | George O. Smith | 95.7 | Murray Leinster | 82.5 |
| 5 | Murray Leinster | 94.4 | Jules Verne | 82.3 |
| 6 | Edward Bellamy | 82.4 | Edward Bellamy | 75.5 |
| 7 | Ray Cummings | 80.4 | Edmond Hamilton | 66.4 |
| 8 | Edmond Hamilton | 69.9 | Ray Cummings | 64.9 |
| 9 | Godfrey Sweven | 69.5 | Ignatius Donnelly | 64.0 |
| 10 | Thomas More | 66.7 | Godfrey Sweven | 62.9 |
| 11 | Ignatius Donnelly | 65.5 | Thomas More | 61.3 |
| 12 | E. E. Smith | 55.7 | E. E. Smith | 53.3 |
| 13 | M. P. Shiel | 49.5 | Mack Reynolds | 43.2 |
| 14 | John W. Campbell Jr | 45.8 | Robert Hugh Benson | 42.3 |
| 15 | Mack Reynolds | 45.2 | M. P. Shiel | 40.7 |
| 16 | Robert Hugh Benson | 45.0 | John W. Campbell Jr | 40.4 |
| 17 | Randall Garrett | 44.4 | Garrett Putman Serviss | 38.1 |
| 18 | Camille Flammarion | 43.6 | Camille Flammarion | 35.6 |
| 19 | Garrett Putman Serviss | 41.1 | Alexis de Tocqueville | 35.2 |
| 20 | Alexis de Tocqueville | 38.3 | William Morris | 34.7 |

## The deciding concepts after tier 2 (PLAN §5)

238 concepts carry a top entry or add 5+ points to the author totals now; tier 2 checked 93 of them (`runs/match/deciding.jsonl` lists every concept selected for it, by round). By criterion (a concept can meet several):

- adds 5+ points to the author totals: 223
- best entry of a top-100 author: 57
- best entry of a top-100 book: 63
- lead over 40 years for 20+ claims: 16
- top-300 prediction: 118
- top-50 entry, 1900–1945: 30
- top-50 entry, 1946–1979: 24
- top-50 entry, pre-1900: 34

Their milestones: confidence high 74, low 47, medium 117; 197 have a contemporary source, 18 rest on Wikipedia alone, 40 are demonstrations only.

The 40 that carry the most points, and every one tier 2 did not check:

| concept | points | entries | lead > 40 | milestone | confidence | sources | best entry | tier 2 |
|---|---|---|---|---|---|---|---|---|
| Crewed Moon landing | 303.6 | 135 | 48 | 1969-07-20 †: Apollo 11's lunar module Eagle landed Neil Armstrong and Buzz Aldrin… | high | contemporary | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| State-enforced limits on births | 170.1 | 70 | 49 | 1972: Singapore's 'Stop at Two' policy: from 1972 (debated in Parliament 24… | medium | contemporary | H. G. Wells, *A Modern Utopia* (1905) | **not checked** |
| Space tourism and orbital resorts | 125.0 | 42 | 45 | 2001-04-28: Dennis Tito paid Russia about $20 million to fly on Soyuz TM-32, laun… | high | contemporary | Jack Williamson, *The Prince of Space* (1931) | **not checked** |
| Abolition of private property | 104.9 | 39 | 12 | 1918-06: Soviet Russia abolished private ownership of land (Decree on Land, No… | medium | contemporary | Thomas More, *Utopia* (1516) | **not checked** |
| Rule by scientists or experts | 103.0 | 36 | 38 | 1995-01: Italy: in January 1995 President Scalfaro appointed the central banke… | medium | contemporary | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Abolition of money | 97.2 | 27 | 40 | 1975: After taking Phnom Penh in April 1975 the Khmer Rouge abolished curre… | high | contemporary | Thomas More, *Utopia* (1516) | checked |
| Private and personal spacecraft | 96.7 | 34 | 36 | 2021-07-20: Blue Origin NS-16: New Shepard carried Bezos, his brother Mark, Wally… | medium | contemporary | Mark Reinsberg, *The Vicious Delinquents* (1958) | **not checked** |
| Private companies in the space industry | 93.0 | 35 | 7 | 1984-05-23: Arianespace, the first commercial launch services company, launched G… | medium | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Rescue of people stranded in space | 77.6 | 24 | 25 | 2025-03-18: SpaceX Crew-9 Dragon Freedom, launched 2024-09-28 with two seats left… | medium | contemporary | Stephen Bartholomew, *Far Enough to Touch* (1962) | **not checked** |
| Painless death on demand | 76.7 | 23 | 28 | 1985: Exit Deutsche Schweiz, a Swiss right-to-die society founded in 1982,… | low | reference | Thomas More, *Utopia* (1516) | **not checked** |
| Military space service branch | 74.4 | 30 | 7 | 1992-08-10: By order of the Russian Minister of Defense of 10 August 1992 the Mil… | medium | contemporary | Keith Bennett, *The Rocketeers Have Shaggy Ears* (1950) | checked |
| European political union | 70.7 | 22 | 24 | 1993-11-01: The Maastricht Treaty on European Union entered into force after rati… | medium | contemporary | Camille Flammarion, *Omega* (1893) | checked |
| Classless egalitarian society | 66.5 | 25 | 19 | 1936-07: In Barcelona and Catalonia, controlled by anarchist and syndicalist u… | low | contemporary | (text), *The Mahabharata, Volume 1 (Books 1…* (400) | checked |
| Nationalization of industry | 62.4 | 27 | 1 | 1918-06-28: The Soviet government's decree of 28 June 1918 nationalized all large… | medium | contemporary | Alexis de Tocqueville, *Democracy in America, Volume 2* (1840) | checked |
| Communal dining replaces home cooking | 62.2 | 18 | 21 | 1958: In China's 1958 people's communes, communal kitchens and mess halls r… | medium | contemporary | Thomas More, *Utopia* (1516) | checked |
| Major attack on or destruction of New Y… | 59.2 | 25 | 26 | 2001-09-11: Hijackers crashed two airliners into the World Trade Center towers in… | medium | contemporary | H. G. Wells, *The War in the Air* (1908) | checked |
| Search for extraterrestrial signals | 59.0 | 29 | 20 | 1960-04: Frank Drake's Project Ozma used the 85-foot Green Bank radio telescop… | medium | contemporary | Camille Flammarion, *Urania* (1889) | **not checked** |
| Government regulator of spaceflight | 54.9 | 22 | 4 | 1984-10-30: The US Commercial Space Launch Act of 1984 (Public Law 98-575, signed… | high | contemporary | David C. Knight, *The Love of Frank Nineteen* (1957) | checked |
| Nuclear deterrence | 53.9 | 20 | 6 | 1954-01-12: Secretary of State John Foster Dulles announced to the Council on For… | medium | contemporary | Adam Seaborn, *Symzonia* (1820) | **not checked** |
| Free partner choice and loosened marria… | 50.7 | 22 | 4 | 1917-12: Soviet Russia's decrees of December 1917 made civil marriage the only… | medium | contemporary | T. R. Malthus, *An Essay on the Principle of Popul…* (1798) | checked |
| Earth seen from space or another world | 48.6 | 15 | 9 | 1968-12-21 †: Apollo 8 crew (Borman, Lovell, Anders) saw the whole Earth at once af… | medium | contemporary | George Tucker, *A Voyage to the Moon* (1827) | **not checked** |
| Derelict spacecraft drifting in space | 48.3 | 20 | 6 | 1984-11: Same event: the two salvaged satellites were returned to Earth for re… | medium | contemporary | George O. Smith, *Nomad* (1944) | **not checked** |
| Crewed flight around the Moon and back | 48.1 | 16 | 16 | 1968-12-24: Apollo 8 first actually carried a crew around the Moon and back (even… | high | contemporary | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| United States as leading world power | 44.6 | 15 | 11 | 1945: With the end of World War II the United States stood as the dominant… | medium | Wikipedia only | H. G. Wells, *Anticipations* (1901) | checked |
| Falling oceans exposing seabed | 44.6 | 14 | 31 | 1970 †: Deep Sea Drilling Project Leg 13 (Glomar Challenger, Aug-Oct 1970, co… | medium | contemporary | Austin Hall, *The Man Who Saved the Earth* (1919) | **not checked** |
| Cosmic catastrophe changing the Earth | 42.4 | 15 | 17 | 1991 †: The Chicxulub structure in Yucatan was identified as the Cretaceous-T… | medium | contemporary | H. G. Wells, *The Star* (1897) | **not checked** |
| Crewed orbital space station | 42.2 | 24 | 0 | 1971-06-07: Salyut 1 was used as a science station by the Soyuz 11 crew for 23 da… | high | contemporary | Dean Ing, *Tight Squeeze* (1955) | **not checked** |
| Women in all occupations and war work | 41.9 | 19 | 4 | 1915: In Britain during the first year of World War I, women began to repla… | medium | contemporary | Tommaso Campanella, *The City of the Sun* (1602) | **not checked** |
| Invisibility | 41.2 | 15 | 28 | 2010-12 †: Baile Zhang, Yuan Luo, Xiaogang Liu and George Barbastathis (MIT/SMAR… | medium | contemporary | (text), *The Mahabharata, Volume 4 (Books 1…* (400) | **not checked** |
| Guaranteed basic income or citizen divi… | 40.3 | 11 | 14 | 1982: Alaska paid the first Permanent Fund Dividend in 1982: a $1,000 check… | medium | contemporary | Edward Bellamy, *Equality* (1897) | checked |
| Compulsory killing of the old or unfit | 40.2 | 16 | 9 | 1939-09: After the German invasion of Poland on 1 September 1939, SS units (Ei… | medium | contemporary | Walter Besant, *The Inner House* (1888) | **not checked** |
| Military space station or lunar weapons… | 39.5 | 21 | 0 | 1974-07-04: Soyuz 14 crew operated the Salyut 3 Earth-observation cameras and loa… | medium | contemporary | William Tenn, *Project Hush* (1954) | **not checked** |
| Breakdown of urban infrastructure and o… | 39.4 | 14 | 9 | 1977-07-13: Lightning strikes on 13 July 1977 blacked out New York City for about… | medium | contemporary | Fred M. White, *The Doom of London* (1903) | checked |
| English as the world language | 38.8 | 10 | 9 | 1950: By about 1950 English had replaced French and German as the leading i… | low | contemporary | Ralph Centennius, *The Dominion in 1983* (1883) | checked |
| General disarmament | 38.2 | 16 | 1 | 1922-02-06: The Washington Naval Treaty, signed 6 February 1922 by the United Sta… | medium | contemporary | P. H. Colomb; Archibald…, *The Great War of 189-* (1892) | **not checked** |
| World war between great powers | 37.4 | 19 | 2 | 1914-08-04: World War I became a war of most great powers on 4 August 1914, when… | high | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Anglo-American union or alliance | 36.4 | 12 | 24 | 1942-01: At the Arcadia Conference in Washington (22 Dec 1941 - 14 Jan 1942) B… | medium | contemporary | Frank R. Stockton, *The Great War Syndicate* (1888) | **not checked** |
| Spaceflight halted or abandoned | 36.3 | 17 | 2 | 1972-12: Apollo 17 (launched 7 Dec, returned 19 Dec 1972) was the last crewed… | high | contemporary | Irving E. Cox Jr., *The Pioneer* (1955) | checked |
| Death ray | 35.3 | 12 | 14 | 2003-03: The US Army deployed the Zeus-HLONS, a Humvee-mounted laser, to Bagra… | medium | reference | James H. Schmitz, *Watch the Sky* (1962) | **not checked** |
| Continuous urban megalopolis | 34.8 | 14 | 16 | 1950: By the 1950 census the continuous urbanized belt of the US northeaste… | medium | reference | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Rogue planet wandering between stars | 34.4 | 10 | 13 | 2000-10 †: Zapatero Osorio et al. (Science, 6 Oct 2000) reported spectroscopy of… | medium | contemporary | Ray Cummings, *Wandl the Invader* (1932) | **not checked** |
| International organization to prevent w… | 30.7 | 17 | 0 | 1920-01-10: The Covenant of the League of Nations took effect on 10 January 1920… | high | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Crewed orbital spaceflight | 29.7 | 22 | 0 | 1961-04-12 †: Yuri Gagarin made one orbit of the Earth in Vostok 1, launched from B… | high | contemporary | John W. Campbell Jr, *The Black Star Passes* (1953) | **not checked** |
| Sunken lost continent | 29.3 | 10 | 13 | 2017-02 †: Mortimer and ten co-authors published 'Zealandia: Earth's Hidden Cont… | medium | contemporary | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Thinning atmosphere | 28.1 | 11 | 6 | 1989 †: Phobos 2's plasma instruments measured ions escaping from Mars's uppe… | low | contemporary | H. G. Wells, *The First Men in the Moon* (1900) | **not checked** |
| Spaceport | 28.0 | 20 | 0 | 1957-10-04: Baikonur Cosmodrome (founded 1955) launched Sputnik 1, the first spac… | medium | contemporary | Nelson S. Bond, *The Return of Lancelot Biggs* (1942) | **not checked** |
| Flight to the poles | 27.7 | 10 | 5 | 1937-05: Soviet aviation units under Mark Shevelev airlifted Otto Schmidt's ex… | medium | contemporary | Luis Senarens, *From Zone to Zone* (1894) | **not checked** |
| End of the working horse | 27.3 | 10 | 1 | 1915: US cropland used to feed horses and mules peaked in 1915; after that… | low | reference | Mary Griffith, *Camperdown* (1836) | **not checked** |
| Votes and office for women | 26.0 | 12 | 4 | 1902-06-12: The Commonwealth of Australia's Commonwealth Franchise Act 1902 (No.… | medium | contemporary | Adam Seaborn, *Symzonia* (1820) | **not checked** |
| Multi-planet timekeeping | 25.3 | 8 | 8 | 2004-01: Members of NASA's Mars Exploration Rover team wore analog 'Mars watch… | medium | contemporary | Raymond F. Jones, *The Colonists* (1954) | **not checked** |
| Burial or cemetery in space | 25.1 | 10 | 5 | 1997-04-21: Celestis's Earthview 01 was a paid commercial service ($4,800 per cus… | high | contemporary | Algis Budrys, *Desire No More* (1954) | **not checked** |
| Spacecraft flying into the Sun's atmosp… | 25.1 | 10 | 13 | 2021-04-28 †: Parker Solar Probe crossed the Alfven critical surface into the solar… | high | contemporary | John Mastin, *Through the Sun in an Airship* (1909) | **not checked** |
| Prohibition of alcohol | 24.6 | 10 | 2 | 1915-01-01: Iceland's nationwide prohibition law, adopted by referendum on 10 Sep… | high | contemporary | Mary Griffith, *Camperdown* (1836) | **not checked** |
| Forced experiments on captive humans | 23.7 | 8 | 4 | 1933: Shiro Ishii's Japanese Army unit began experiments on captive Chinese… | low | Wikipedia only | Frances Power Cobbe, *The Age of Science* (1877) | **not checked** |
| Radioactive fallout wasteland | 22.6 | 21 | 1 | 1954-03-01: The Castle Bravo H-bomb test at Bikini on 1 March 1954 dropped fallou… | medium | contemporary | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Density and hazards of the asteroid belt | 22.1 | 9 | 1 | 1973-02 †: Pioneer 10 became the first spacecraft to cross the asteroid belt (19… | high | contemporary | Edmond Hamilton, *The Universe Wreckers* (1930) | **not checked** |
| Seeing the far side of the Moon | 22.0 | 9 | 5 | 1959-10-07 †: Luna 3 photographed the Moon's far side on 7 October 1959 and returne… | high | contemporary | Charles Napier Richards, *Atalanta* (1900) | **not checked** |
| Planetary protection and contamination… | 21.6 | 15 | 0 | 1962-01-26: Ranger 3 was launched on 26 January 1962 toward the Moon with a heat-… | low | Wikipedia only | Philip K. Dick, *Piper in the Woods* (1953) | **not checked** |
| Near-real-time worldwide news | 21.6 | 6 | 6 | 1963-11-22: News of President Kennedy's shooting (1963-11-22) reached nearly all… | low | contemporary | Guy Thorne, *The Soul Stealer* (1906) | **not checked** |
| Dissent treated as mental illness | 20.9 | 11 | 9 | 1948: The Soviet state, from the late 1940s, began confining political diss… | low | reference | Jack London, *The Iron Heel* (1907) | **not checked** |
| Aerial bombing | 19.1 | 8 | 1 | 1911-11-01: Lt. Giulio Gavotti, Italy, dropped grenades from an Etrich Taube airc… | medium | contemporary | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Government space agency | 18.4 | 16 | 1 | 1958-10-01: NASA began operations as the US civilian government agency organizing… | medium | contemporary | Ray Cummings, *A Brand New World* (1928) | **not checked** |
| Nuclear missile and ICBM | 18.1 | 12 | 0 | 1959-10: The US Air Force 576th Strategic Missile Squadron went on operational… | medium | contemporary | E. E. Smith, *Triplanetary* (1948) | **not checked** |
| Physical conditions on the Moon and inn… | 17.8 | 13 | 3 | 1962-12-14 †: NASA's Mariner 2 flew past Venus at 21,000 miles; its microwave and i… | medium | contemporary | George O. Smith, *Home Is the Spaceman* (1953) | **not checked** |
| Air-to-air combat | 17.6 | 10 | 0 | 1914-10-05: Sgt. Joseph Frantz and gunner Louis Quenault in a Voisin biplane with… | high | contemporary | Jules Verne, *Robur the Conqueror* (1886) | **not checked** |
| Planetary defense battery | 17.4 | 5 | 5 | 2007-01-11 †: China destroyed its own Fengyun-1C weather satellite with a ground-la… | high | contemporary | George O. Smith, *Nomad* (1944) | **not checked** |
| Rocket sent to strike the Moon | 17.0 | 6 | 0 | 1959-09-13: The Soviet Luna 2 probe struck the Moon's surface near Mare Imbrium o… | high | contemporary | Isabel Hornibrook, *Pemrose Lorry, Camp Fire Girl* (1921) | **not checked** |
| Planetary defense against comets and as… | 16.6 | 4 | 7 | 2022-09-26 †: NASA's DART hit Dimorphos, shortening its orbit around Didymos by abo… | high | contemporary | George Chetwynd Griffith, *The World Peril of 1910* (1906) | **not checked** |
| Society's dependence on fallible comput… | 16.0 | 6 | 5 | 1999: Same event: the Horizon-based prosecutions began in 1999. | medium | reference | Walter J. Sheldon, *Two Plus Two Makes Crazy* (1954) | **not checked** |
| Machinery-disabling ray | 16.0 | 8 | 1 | 1962-07-09 †: Starfish Prime high-altitude nuclear test (Johnston Atoll, 9 July 196… | low | reference | Ray Cummings, *Wandl the Invader* (1932) | **not checked** |
| Planets in double and multiple star sys… | 15.8 | 5 | 3 | 1996-10-22 †: At the American Astronomical Society planetary sciences meeting, Coch… | high | contemporary | Marion Zimmer Bradley, *Falcons of Narabedla* (1957) | **not checked** |
| Synthetic food | 15.5 | 7 | 0 | 1939: After the Reich health office cleared synthetic fat for food in Septe… | medium | contemporary | L. P. Gratacap, *The Certainty of a Future Life in…* (1903) | **not checked** |
| Bodily injury from vacuum exposure | 15.3 | 6 | 0 | 1966-12-14 †: At NASA's Manned Spacecraft Center, Houston, a test subject (Jim LeBl… | high | contemporary | Anthony Gilmore, *The Passing of Ku Sui* (1932) | **not checked** |
| Walking and leaping in low gravity | 14.9 | 7 | 1 | 1969-07-21: The same Apollo 11 moonwalk was real exploration work: the crew loped… | low | contemporary | Robert Emmett McDowell, *Moon of Treason* (1950) | **not checked** |
| Radio communication with spacecraft and… | 14.9 | 9 | 1 | 1957-11-03: Sputnik 2, carrying the dog Laika, radioed telemetry of her heartbeat… | medium | contemporary | L. P. Gratacap, *The Certainty of a Future Life in…* (1903) | **not checked** |
| Crewed suborbital rocket flight | 14.6 | 5 | 5 | 2021-07-20: Blue Origin NS-16: New Shepard carried four people to space from West… | medium | contemporary | Dean Evans, *The Very Black* (1953) | **not checked** |
| Mass civilian evacuation and air-raid p… | 14.6 | 10 | 0 | 1917-09: During the German Gotha and Giant night raids on London in late Septe… | medium | contemporary | M. P. Shiel, *The Yellow Danger* (1898) | **not checked** |
| Artificial satellite | 14.6 | 6 | 3 | 1957-10-04: Sputnik 1 in orbit transmitted radio signals; tracking its orbital dr… | medium | contemporary | Ray Cummings, *Tama of the Light Country* (1930) | **not checked** |
| Jewish state in Palestine | 14.2 | 6 | 12 | 1948-05-14: David Ben-Gurion read the Declaration of the Establishment of the Sta… | high | contemporary | M. P. Shiel, *The Lord of the Sea* (1901) | **not checked** |
| Mass military air force | 13.9 | 5 | 0 | 1918-04: The Royal Air Force formed on 1 April 1918 from the RFC and RNAS as t… | low | Wikipedia only | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Black sky filled with stars seen from s… | 13.5 | 4 | 1 | 1961-04-12 †: Yuri Gagarin, orbiting in Vostok 1 on 12 April 1961, reported a pitch… | medium | contemporary | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| Official rating of citizens by aptitude… | 12.6 | 6 | 1 | 1917: From September 1917 the US Army (Surgeon General) put recruits throug… | high | contemporary | Tommaso Campanella, *The City of the Sun* (1602) | **not checked** |
| Mind-reading machine | 12.1 | 3 | 9 | 2006 †: Thirion et al. (NeuroSpin, France) decoded fMRI activity to reconstru… | medium | contemporary | Guy Thorne, *The Soul Stealer* (1906) | **not checked** |
| Synthetic diamond | 12.1 | 3 | 3 | 1957: General Electric's Detroit plant made man-made industrial diamonds in… | medium | contemporary | H. G. Wells, *The Stolen Bacillus and Other Inci…* (1895) | **not checked** |
| Stored air, water and food for spacefli… | 12.0 | 4 | 3 | 1961-04-12: Vostok 1: Yuri Gagarin flew with food, water and regeneration supplie… | high | contemporary | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| Engineered manipulation of public opini… | 11.7 | 6 | 0 | 1929-03-31: Edward Bernays arranged for women, led by Bertha Hunt, to smoke in th… | low | contemporary | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Hydrogen bomb | 11.6 | 12 | 0 | 1954: Emergency-capability thermonuclear bombs (EC 17, EC 24) entered the U… | medium | Wikipedia only | Lester Del Rey, *And There Was Light* (1951) | **not checked** |
| Totalitarian dictatorship over a nation | 11.5 | 6 | 1 | 1918-09: Bolshevik Soviet Russia: one-party rule, with the Sovnarkom decree of… | low | contemporary | Alexis de Tocqueville, *Democracy in America, Volume 2* (1840) | **not checked** |
| Moving an asteroid into a new orbit | 11.5 | 4 | 5 | 2022-09-26 †: NASA's DART spacecraft struck the asteroid moonlet Dimorphos on 26 Se… | high | contemporary | Harold L. Goodwin, *Rip Foster in Ride the Gray Planet* (1952) | **not checked** |
| Reorganization of the Balkans | 11.2 | 4 | 3 | 1913-05-30: By the Treaty of London (30 May 1913) the Ottoman Empire ceded all Eu… | high | contemporary | Mary Wollstonecraft Shel…, *The Last Man* (1826) | **not checked** |
| Assembly of structures in orbit | 11.2 | 5 | 0 | 1983-03-10: Kosmos 1443, a heavy module launched 2 March 1983, docked to Salyut 7… | high | contemporary | Richard Wilson, *Double Take* (1954) | **not checked** |
| Growing food in space | 11.1 | 6 | 1 | 1975-07-08 †: Salyut 4 cosmonauts Klimuk and Sevastyanov ate onions grown in the Oa… | medium | contemporary | Jules Verne, *From the Earth to the Moon, Direct…* (1872) | **not checked** |
| Mass famine from war or breakdown of su… | 10.9 | 3 | 8 | 1850: The Taiping Rebellion began in China in 1850-51; its 20-30 million de… | low | Wikipedia only | (text), *The Sibylline Oracles* (700) | **not checked** |
| Space medicine and astronaut medical sc… | 10.8 | 9 | 0 | 1959-02: NASA's 32 Mercury astronaut candidates underwent medical, physiologic… | high | contemporary | Rog Phillips, *Unthinkable* (1949) | **not checked** |
| Spacewalk | 10.8 | 5 | 0 | 1966-07-20: Michael Collins, outside Gemini 10 in his second EVA, used a handheld… | medium | contemporary | Edmond Hamilton, *Outside the Universe* (1929) | **not checked** |
| Military airship | 10.7 | 5 | 0 | 1912-03-05: Italian Navy airships P.2 and P.3 began operating in Libya during the… | medium | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Other stars with many planets | 10.7 | 4 | 4 | 2017-02-22 †: Gillon et al. (Nature, 22 Feb 2017) and NASA announced seven Earth-si… | medium | contemporary | E. Everett Evans, *The Planet Mappers* (1955) | **not checked** |
| Union of Islamic or Arab states, or rev… | 10.6 | 7 | 3 | 1958-02-01: Egypt and Syria merged into the United Arab Republic on 1 February 19… | medium | contemporary | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Stellar life cycle and novae | 10.6 | 8 | 5 | 1962 †: Robert Kraft (Mount Wilson and Palomar) showed from spectroscopy that… | low | contemporary | Camille Flammarion, *Omega* (1893) | **not checked** |
| Food pills and concentrated rations | 10.3 | 6 | 2 | 1953: Mead Johnson & Co. (Evansville, Indiana) introduced Sustagen in mid-1… | medium | contemporary | Walter Besant, *The Inner House* (1888) | **not checked** |
| Second natural moon of Earth | 10.3 | 3 | 4 | 2006-09-14 †: Catalina Sky Survey (Arizona) discovered 6R10DB9, later 2006 RH120, a… | medium | contemporary | (text), *Astounding Stories of Super-Scienc…* (1930) | **not checked** |
| Atomic bomb | 10.2 | 5 | 0 | 1945-08-06: The US B-29 Enola Gay dropped the uranium bomb Little Boy on Hiroshim… | high | contemporary | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Sonic weapon | 10.1 | 3 | 3 | 2005-11-05: The cruise ship Seabourn Spirit used a long-range acoustic device (LR… | medium | contemporary | Sax Rohmer, *The Day the World Ended* (1929) | **not checked** |
| Spacecraft emergency safety systems | 10.0 | 4 | 4 | 1997-06-25: Progress M-34 punctured Mir's Spektr module; the crew cut cables and… | medium | contemporary | John Murray Reynolds, *Goddess of the Moon* (1940) | **not checked** |
| Audiobook player | 10.0 | 2 | 1 | 1935: Talking Books on long-playing discs, played on special reading machin… | medium | contemporary | Cyrano de Bergerac, *A Voyage to the Moon* (1657) | **not checked** |
| Gravity assist navigation | 9.8 | 4 | 3 | 1973-12-03: Pioneer 10 passed Jupiter on 3 December 1973 and used its gravity to… | medium | contemporary | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| Undersea habitat or city | 9.7 | 5 | 1 | 1963-06: Conshelf II in the Red Sea off Sudan: five oceanauts lived a month in… | medium | contemporary | Stanton A. Coblentz, *The Sunken World* (1928) | **not checked** |
| Physiological effects of spaceflight | 9.6 | 8 | 0 | 1961-08-06 †: Gherman Titov, in Vostok 2 (launched 6 August 1961), became the first… | high | contemporary | E. E. Smith, *Robot Nemesis* (1934) | **not checked** |
| Change in Earth's rotation | 9.6 | 5 | 1 | 1939: The Earth's rotation was shown to be changing in speed (day length va… | low | contemporary | H. G. Wells, *Tales of Space and Time* (1899) | **not checked** |
| Air purification | 9.6 | 4 | 4 | 2015-03 †: Arup and Sino Green unveiled and trialled a bus-shelter-shaped City A… | medium | contemporary | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Spacecraft viewport and observation win… | 9.6 | 4 | 0 | 1961-04-12: Yuri Gagarin looked out of Vostok 1's portholes at Earth and the star… | medium | contemporary | Raymond Z. Gallun, *The Revolt of the Star Men* (1931) | **not checked** |
| Atomic or nuclear-fission rocket | 9.5 | 7 | 0 | 1959-07-01 †: Los Alamos fired the Kiwi-A reactor at the Nevada Test Site (Jackass… | high | contemporary | Fritz Leiber, *Appointment In Tomorrow* (1951) | **not checked** |
| Weightlessness in spaceflight | 9.5 | 4 | 0 | 1961-04-12 †: Yuri Gagarin orbited the Earth in Vostok 1 and floated weightless in… | high | contemporary | George O. Smith, *Off the Beam* (1944) | **not checked** |
| Orbital launch rocket | 9.5 | 8 | 0 | 1957-10-04: The Soviet Union launched Sputnik 1 into Earth orbit on a modified R-… | high | contemporary | Isabel Hornibrook, *Pemrose Lorry, Camp Fire Girl* (1921) | **not checked** |
| Radiation sickness in space | 9.4 | 5 | 3 | 2001-11 †: Cucinotta et al. (Radiation Research) linked higher space-radiation l… | low | contemporary | Walt Richmond; Leigh Ric…, *Where I Wasn't Going* (1963) | **not checked** |
| Warming and rising seas | 9.2 | 4 | 2 | 1938-04 †: G. S. Callendar showed from about 200 station records that world temp… | high | contemporary | H. G. Wells, *The Star* (1897) | **not checked** |
| Continental-scale water engineering | 9.0 | 4 | 4 | 2013-11: Water diversion on the first phase of the East route started in Novem… | high | contemporary | H. G. Wells, *Tono-Bungay* (1909) | **not checked** |
| Live television from space | 8.7 | 5 | 0 | 1962-07-23: Telstar 1 relayed the first public live transatlantic television, sho… | high | contemporary | Arthur Leo Zagat, *The Great Dome on Mercury* (1932) | **not checked** |
| Eugenic breeding of humans | 8.3 | 2 | 3 | 1869: Same event: the committee approved parents and children were born und… | medium | contemporary | Tommaso Campanella, *The City of the Sun* (1602) | **not checked** |
| Under-ice polar submarine | 8.2 | 3 | 6 | 1959-03-17: USS Skate, on a 12-day winter Arctic cruise under the ice, surfaced a… | low | contemporary | Luis Senarens, *Frank Reade Jr.'s Submarine Boat* (1893) | **not checked** |
| Routine mass health screening | 8.1 | 4 | 2 | 1937: Thoracic Census Centers in Rio de Janeiro screened asymptomatic peopl… | medium | reference | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Compulsory or make-work employment | 8.1 | 2 | 3 | 1848-02-25: On 25 February 1848 the French provisional government of the Second R… | high | contemporary | Thomas More, *Utopia* (1516) | **not checked** |
| Air travel replaces sea travel | 8.0 | 2 | 1 | 1951: By 1951 airlines carried 52 percent of all commercial transpacific (U… | low | reference | Ralph Centennius, *The Dominion in 1983* (1883) | **not checked** |
| Planets changing orbits | 7.9 | 5 | 1 | 1945-11 †: B. P. Sharpless of the US Naval Observatory published the first compu… | medium | contemporary | Ray Cummings, *The Princess of the Atom* (1929) | **not checked** |
| Creating life from nonliving matter | 7.9 | 3 | 3 | 2010-05-20 †: J. Craig Venter Institute (Gibson et al.) assembled a Mycoplasma myco… | medium | contemporary | Harle Oren Cummins, *Welsh Rarebit Tales* (1902) | **not checked** |
| Gravity-neutral (Lagrange) point betwee… | 7.7 | 2 | 2 | 1978-11-20: ISEE-3 in its L1 halo orbit began measuring the solar wind upstream o… | low | contemporary | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| Spacecraft escape boat or lifeboat | 7.7 | 4 | 0 | 1969-07-20: Apollo 11: astronauts Armstrong and Aldrin left Columbia in the lunar… | medium | contemporary | Murray Leinster, *The Forgotten Planet* (1954) | **not checked** |
| Air traffic lanes and control | 7.7 | 3 | 0 | 1920-02-25: Croydon Airport, near London, commissioned the world's first aerodrom… | medium | contemporary | Rudyard Kipling, *With the Night Mail* (1905) | **not checked** |
| Inflatable space habitat | 7.3 | 3 | 3 | 2016-06-06: After BEAM was expanded on the ISS on 28 May 2016, astronauts Jeff Wi… | high | contemporary | Raymond Z. Gallun, *Comet's Burial* (1953) | **not checked** |
| Spacecraft cruising at tens of miles pe… | 7.3 | 4 | 1 | 1962-12: Mariner 2 carried radiometers and particle instruments to Venus and r… | low | Wikipedia only | John Jacob Astor, *A Journey in Other Worlds* (1894) | **not checked** |
| Spacesuit | 7.0 | 4 | 0 | 1969-01-16: Yevgeny Khrunov and Alexei Yeliseyev, wearing Yastreb suits with ches… | high | contemporary | Judith Merril, *The Tomorrow People* (1960) | **not checked** |
| Glowing plants and animals | 6.8 | 2 | 2 | 2024-04: Light Bio began shipping Firefly Petunias (fungal bioluminescence pat… | medium | contemporary | John Munro, *A Trip to Venus* (1897) | **not checked** |
| Uncrewed cargo spacecraft | 6.7 | 4 | 0 | 1978-01-22: Progress 1 delivered fuel and supplies to the crew of Salyut 6 (Roman… | high | contemporary | Richard M. Elam, *Young Visitor to Mars* (1953) | **not checked** |
| Non-lethal stun gun | 6.4 | 3 | 1 | 1975-03: The Taser Public Defender, a flashlight-shaped dart stun gun made by… | medium | contemporary | Frank Aubrey, *A Trip to Mars* (1909) | **not checked** |
| Spacecraft built from or reused as othe… | 6.4 | 3 | 0 | 1973-05-25: The Skylab 2 crew was launched to Skylab and lived and worked in the… | medium | contemporary | Murray Leinster, *Planet Explorer* (1957) | **not checked** |
| Sealed knowledge repository | 6.4 | 3 | 1 | 1938-09-23: Same event: the capsule was sealed and buried as a repository for peo… | high | contemporary | Pierre Benoît, *Atlantida* (1919) | **not checked** |
| Automated construction | 6.2 | 3 | 1 | 1991: Shimizu Corporation introduced its SMART automated construction syste… | medium | reference | Mark Meadows, *Joy Ride* (1954) | **not checked** |
| Credit card payment | 6.1 | 2 | 1 | 1950-02: Diners Club began operating in February 1950 and within the year had… | medium | contemporary | Edward Bellamy, *Looking Backward* (1888) | **not checked** |
| Brain-to-brain link | 6.0 | 3 | 3 | 2013-08-12 †: At the University of Washington on 12 Aug 2013, Rajesh Rao's EEG-read… | medium | contemporary | Mike Lewis, *Collectivum* (1953) | **not checked** |
| Space beacons and navigation aids | 6.0 | 4 | 0 | 1965-12-15: Gemini VI-A's rendezvous radar locked on the transponder carried by G… | low | contemporary | D. W. Barefoot, *Morley's Weapon* (1954) | **not checked** |
| Orbital rendezvous and docking | 5.8 | 3 | 0 | 1969-07-21: Apollo 11 Lunar Module Eagle rendezvoused with and docked to Columbia… | high | contemporary | Ray Cummings, *Tama of the Light Country* (1930) | **not checked** |
| Round-the-world flight | 5.8 | 2 | 1 | 1947-06-17: Pan American Clipper America left New York on the first commercial ro… | medium | contemporary | Luis Senarens, *From Zone to Zone* (1894) | **not checked** |
| Selling or owning land on the Moon | 5.7 | 3 | 2 | 1955: Robert R. Coles, former chairman of the Hayden Planetarium, ran the I… | medium | contemporary | Ellsworth Douglass, *Pharaoh's Broker* (1899) | **not checked** |
| Solar electric power generation | 5.6 | 2 | 1 | 1973-07: The Solar One experimental house at the University of Delaware began… | medium | contemporary | John Jacob Astor, *A Journey in Other Worlds* (1894) | **not checked** |
| Disposable paper clothing and strong pa… | 5.5 | 3 | 1 | 1966: Scott Paper Company offered a wear-it-once paper dress to the public… | medium | contemporary | Fritz Leiber, *The Last Letter* (1958) | **not checked** |
| Airborne troop transport | 5.3 | 2 | 0 | 1923: RAF Vernons flew Sikh troops from Kingarban to Kirkuk in a real opera… | medium | contemporary | H. G. Wells, *The Sleeper Awakes* (1899) | **not checked** |
| Reproduction in space or low gravity | 5.3 | 2 | 1 | 1983-12 †: Ten pregnant rats flew on Kosmos 1514 (Bion 6), launched 14 December… | high | contemporary | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Engineered microorganisms | 5.3 | 3 | 0 | 1982-10: The US Food and Drug Administration approved sale of Humulin, human i… | high | contemporary | Arnold Castle, *A Mixture of Genius* (1958) | **not checked** |
| Detecting planets of other stars | 5.2 | 2 | 0 | 1992-01-09 †: Aleksander Wolszczan and Dale Frail published two planets around the… | high | contemporary | E. Everett Evans, *The Planet Mappers* (1955) | **not checked** |
| Emotion-recognition machine | 5.2 | 2 | 3 | 2015-06: SoftBank's Pepper, a humanoid robot that reads emotions from words, v… | low | contemporary | Dean Evans, *The Furious Rose* (1952) | **not checked** |
| Unattended automatic power plant | 5.0 | 2 | 1 | 1966: The US Navy installed a radioisotope generator on uninhabited Fairway… | medium | contemporary | Van Tassel Sutphen, *The Doomsman* (1906) | **not checked** |
| Exotic surface of Pluto | 4.8 | 2 | 0 | 1976-11 †: Cruikshank, Pilcher and Morrison (Univ. of Hawaii) reported infrared… | medium | contemporary | Fletcher Pratt; Laurence…, *Expedition to Pluto* (1939) | **not checked** |
| Weapons-to-energy conversion and arms c… | 4.2 | 1 | 1 | 1998: Cooper Nuclear Station in Nebraska became the first US power plant to… | low | Wikipedia only | George O. Smith, *The Incredible Invasion* (1948) | **not checked** |
| Origin of lunar craters and domes | 4.0 | 1 | 0 | 1970-01 †: First Apollo 11 lunar samples studied at the Apollo 11 Lunar Science… | medium | contemporary | Robert H. Wilson, *Out Around Rigel* (1931) | **not checked** |
| Volcanic eruption forecasting | 3.9 | 1 | 0 | 1910-07: Same event: the police chief's forecast was acted on by evacuating re… | high | contemporary | Jules Verne, *The Secret of the Island* (1874) | **not checked** |
| Wall-climbing vehicle | 3.8 | 1 | 1 | 1961-09 †: Esso Research and Engineering showed a preliminary model of a magneti… | low | contemporary | Frank R. Stockton, *The Great Stone of Sardis* (1897) | **not checked** |
| Sahara greening by irrigation or planti… | 3.6 | 1 | 1 | 1955: Same project: Liberation Province was a government settlement scheme… | low | contemporary | Nikola Tesla, *The Problem of Increasing Human En…* (1900) | **not checked** |
| Refueling spacecraft in orbit | 3.5 | 1 | 0 | 1978-02: Progress 1 freighter, docked to Salyut 6 (Romanenko and Grechko aboar… | high | contemporary | Murray Leinster, *Space Platform* (1953) | **not checked** |
| Transatlantic flight | 2.9 | 1 | 0 | 1928-10: The Graf Zeppelin carried 20 passengers from Friedrichshafen to Lakeh… | medium | contemporary | Arthur Cheney Train; Rob…, *The Man Who Rocked the Earth* (1914) | **not checked** |
| Dispersed infantry tactics replace mass… | 1.5 | 1 | 0 | 1899-12-11: Battle of Magersfontein, South Africa: Boer riflemen with long-range… | low | contemporary | P. H. Colomb; Archibald…, *The Great War of 189-* (1892) | **not checked** |
