# Scoring after tier 2, tranche A (PLAN §8)

Written by `match.py score full`. Settings: weight log (w = log2(1 + min(L, 500))), the scoring milestone `first_practical_use` else `first_demonstration`, points from score 0.125 (every judged score above 0), precision from 0.5, `contradicted_negative` from 0.5, deadlines checked against 2026 with 10 years of grace. This scoring follows tier 2 (PLAN §5), which checked the 165 deciding concepts of the first scoring, and checkpoint 3's review (`runs/match/milestone_review.jsonl`). Tranche B is not scored. † = scored on a demonstration only (PLAN §14.5).

## Resolutions

77,436 tranche-A claims from 3,224 books.

| resolution | claims | share |
|---|---|---|
| open: no_milestone | 31,486 | 40.7% |
| realized | 16,161 | 20.9% |
| not_a_prediction | 15,994 | 20.7% |
| open: no_concept | 6,795 | 8.8% |
| open: too_vague | 3,897 | 5.0% |
| untestable | 2,558 | 3.3% |
| open: not_matched | 288 | 0.4% |
| failed: missed_deadline | 170 | 0.2% |
| failed: contradicted_negative | 81 | 0.1% |
| open: no_year | 6 | 0.0% |

Deadlines: 1,741 `will` claims with a concept have a stated time naming a year, decade or century after publication; 765 of those ended before 2016. Of these, 309 are realized anyway, 170 missed the deadline, and 286 are not a prediction. Of the 598 realized claims with a deadline, 526 came true by it and 72 after it (median 15 years late).

## The top 50 predictions

11,585 book–concept entries earn points (each book counts its best claim once per concept).

| # | points | score | lead | author | book | concept | milestone | quote |
|---|---|---|---|---|---|---|---|---|
| 1 | 6.32 | 0.875 | 148 | Richard Adams Locke; J. N. Ni… | *The Moon Hoax* (1835) | Meteorites that came from the Moon † | 1983-03 | If we had before retained any doubt of the power of lunar volcanoes to throw fragments of their craters so fa… |
| 2 | 6.13 | 0.75 | 287 | Cyrano de Bergerac | *A Voyage to the Moon* (1657) | Multistage rocket | 1944-11 | For so soon as the Flame had devoured one tier of Squibs, which were ranked by six and six, by means of a Tra… |
| 3 | 6.11 | 0.875 | 125 | Voltaire | *Micromegas* (1752) | Phobos and Deimos, the two moons of Mars † | 1877-08 | they swung by two moons that cater to this planet but have escaped the notice of our astronomers. |
| 4 | 6.09 | 0.75 | 278 | Cyrano de Bergerac | *A Voyage to the Moon* (1657) | Audiobook player | 1935 | it was a Book made wholly for the Ears, and not the Eyes. So that when any Body has a mind to read in it, he… |
| 5 | 6.07 | 0.75 | 273 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Audiobook player | 1935 | It is a book indeed, but a miraculous book without pages or letters; in fine, it is a book to learn from whic… |
| 6 | 5.98 | 1 | 62 | Luis Senarens | *The Sunken Isthmus* (1896) | Submarine air supply | 1958-10 | Under the pilot-house there was placed a generator which was capable of manufacturing pure oxygen, and also o… |
| 7 | 5.81 | 1 | 55 | Charles L. Fontenay | *Blow the Man Down* (1955) | Solar sail or solar-driven spacecraft † | 2010-06-09 | The wind that blows between the worlds," said Carrel solemnly. "Solar radiation. Its pressure will move a shi… |
| 8 | 5.68 | 0.875 | 89 | Jules Verne; Henri Théophile… | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Weightlessness in spaceflight † | 1961-04-12 | Nicholl having accidentally let a glass slip from his hand, the glass, instead of falling, remained suspended… |
| 9 | 5.68 | 0.875 | 89 | Jules Verne | *The Moon-Voyage* (1872) | Weightlessness in spaceflight † | 1961-04-12 | Nicholl having let a tumbler escape from his hand, instead of falling, it remained suspended in the air. |
| 10 | 5.61 | 0.875 | 84 | Percy Greg | *Across the Zodiac* (1880) | Pressurized spacecraft cabin and atmosp… | 1964-10-12 | I had first, by means of the air pump, to fill the vessel with an atmosphere as dense as that in which I had… |
| 11 | 5.58 | 1 | 47 | Edmond Hamilton | *The Sargasso of Space* (1931) | Refueling spacecraft in orbit | 1978-02 | A Pluto liner a quarter-mile back, and we can pump the fuel over here by connecting tube-lines. |
| 12 | 5.58 | 0.875 | 82 | Garrett Putman Serviss | *Other Worlds* (1901) | Meteorites that came from the Moon † | 1983-03 | It has led to the theory that meteorites may have originally been shot out of the moon's great volcanoes, whe… |
| 13 | 5.55 | 0.875 | 80 | Edgar Rice Burroughs | *A Fighting Man of Mars* (1930) | Invisibility † | 2010-12 | The compound of invisibility merely bows outward the reflected light, which, entering our eyes and impinging… |
| 14 | 5.55 | 0.875 | 80 | (text) | *Astounding Stories of Super-Science September 1930* (1930) | Invisibility † | 2010-12 | The walls of the ship are double, the inner one of metal and the outer one of vitrolene or some similar perfe… |
| 15 | 5.52 | 1 | 45 | Arthur Cheney Train; Robert W… | *The Moon Maker* (1916) | Black sky filled with stars seen from s… † | 1961-04-12 | Yet, in spite of the fact that the universe was filled with light, the sky remained as black as midnight and… |
| 16 | 5.46 | 0.75 | 155 | of Samosata Lucian | *Trips to the Moon* (1780) | Wearable wings | 1935 | I took, you must know, a very large eagle and a vulture also, one of the strongest I could get, and cut off t… |
| 17 | 5.45 | 0.875 | 74 | Garrett Putman Serviss | *Curiosities of the Sky* (1909) | Meteorites that came from the Moon † | 1983-03 | For similar reasons it seems not impossible that the theory mentioned in a former chapter—that some of the me… |
| 18 | 5.43 | 0.875 | 73 | George Chetwynd Griffith | *The Angel of the Revolution* (1893) | Tidal power | 1966-11-26 | The ebb and flow in the Thames had at last been turned to account, and worked huge turbines which perpetually… |
| 19 | 5.36 | 1 | 40 | Fritz Leiber | *The Green Millennium* (1953) | Orbital mirrors lighting cities † | 1993-02-04 | the false sunlight from the sodium mirror circling the earth to make evening light for this city |
| 20 | 5.32 | 0.75 | 136 | Jules Verne | *All Around the Moon* (1870) | Second natural moon of Earth † | 2006-09-14 | It is a simple bolide, but one of such enormous dimensions that the Earth's attraction has made it a satellit… |
| 21 | 5.31 | 0.875 | 66 | T. Baron Russell | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | Self-service rental cars | 1971 | automatic motor-cars will exist, coin-worked. A man who wishes to travel will step into a motor-car, drop int… |
| 22 | 5.31 | 0.75 | 134 | Jules Verne | *The Moon-Voyage* (1872) | Second natural moon of Earth † | 2006-09-14 | Yes, my friend, two moons, though she is generally supposed to have but one. But this second moon is so small… |
| 23 | 5.25 | 0.625 | 337 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Solar-powered rocket † | 1999 | I have told you that the sun beat vigorously upon my concave mirrors, and uniting its rays in the middle of t… |
| 24 | 5.25 | 0.875 | 63 | Godfrey Sweven | *Limanora* (1903) | Tidal power | 1966-11-26 | In another series of caves they cooped up the water of the full tides by means of gigantic dams and sluice-ga… |
| 25 | 5.25 | 1 | 37 | Fritz Leiber | *The Snowbank Orbit* (1962) | Solar-powered rocket † | 1999 | A huge paraboloid mirror, its diameter four times the length of the ship's hull, superheated at its focus the… |
| 26 | 5.23 | 0.875 | 62 | Frank Belknap Long | *Woman from Another Planet* (1960) | Three-dimensional telepresence | 2022 | Within the disk the screen glowed brightly and Loring's image was life size. It stood out with a startling, t… |
| 27 | 5.22 | 0.75 | 123 | John Jacob Astor | *A Journey in Other Worlds* (1894) | Evacuated tube train † | 2017-05-12 | the atmospheric resistance is about to be reduced by running the cars hermetically sealed through a partial v… |
| 28 | 5.21 | 1 | 36 | E. E. Smith | *Triplanetary* (1948) | Retina and iris recognition | 1984 | Kinnison dashed up to an apparently blank wall, turned his back upon four commissioned officers holding cocke… |
| 29 | 5.21 | 0.75 | 122 | Adam Seaborn | *Symzonia* (1820) | Jet-propelled boat | 1942 | devised a plan for accelerating their motion, by means of a number of tubes which perforated the after part o… |
| 30 | 5.17 | 0.75 | 118 | E. Douglas Fawcett | *Hartmann, the Anarchist* (1893) | Ultralight metal † | 2011-11 | Why, it is as light or lighter than cardboard. What an extraordinary combination of attributes! |
| 31 | 5.17 | 1 | 35 | Charles Willard Diffin | *Brood of the Dark Moon* (1931) | Powered rocket landing | 1966-06-02 | Down there, where the fires ceased, there would be water; he would land there! And the ship from Earth slippe… |
| 32 | 5.16 | 0.75 | 117 | M. P. Shiel | *The Purple Cloud* (1901) | Liquid air as energy source or engine f… | 2018-04 | She was evidently one of those many ships of late years which have substituted liquid air for steam, yet reta… |
| 33 | 5.15 | 0.875 | 58 | Manly Wade Wellman | *Warrior of Two Worlds* (1944) | Sleep and incapacitating gas | 2002-10-26 | Gederr himself who squirted anaesthetic gas upon you and felled you, senseless. |
| 34 | 5.15 | 0.875 | 58 | Stephen Marlowe | *Recruit for Andromeda* (1959) | Iris diaphragm door | 2017 | A door irised open for them in a solid wall of metal. Irised was the only word Temple could think of, for a t… |
| 35 | 5.14 | 0.75 | 115 | Herbert D. Ward | *A Republic Without a President, and Other Stories* (1891) | Thought-to-text and thought display † | 2006 | Authors would only need to fix their attention upon the plot; the delicate instrument would record it indelib… |
| 36 | 5.14 | 0.75 | 115 | Godfrey Sweven | *Limanora* (1903) | Liquid air as energy source or engine f… | 2018-04 | Another that was near at hand was the use of the expansion of their liquefied and solidified air for purposes… |
| 37 | 5.14 | 0.75 | 115 | Mrs. Loudon | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Undersea tunnel | 1942-07-01 | it had nearly advanced through the whole of the tunnel under the sea, which separates the two kingdoms, witho… |
| 38 | 5.13 | 1 | 34 | Edwin K. Sloat | *Loot of the Void* (1932) | Astronaut maneuvering gun or pack | 1966-07-19 | while the long flame of his Sextle rocket-pistol showed that he was checking his forward momentum as rapidly… |
| 39 | 5.12 | 0.75 | 112 | David Franklin Powell | *The Wolf-Men* (1906) | Liquid air as energy source or engine f… | 2018-04 | liquid air engines, a patent of Wilson’s, maximum speed of which is forty-five knots per hour upon the surfac… |
| 40 | 5.11 | 0.75 | 111 | Hugo Gernsback | *Ralph 124C 41+* (1911) | Planetary defense against comets and as… † | 2022-09-26 | The gravitational action of his machine on the comet would deflect the course of the latter enough—even a few… |
| 41 | 5.11 | 0.75 | 111 | Herbert D. Ward | *A Republic Without a President, and Other Stories* (1891) | Sleep and incapacitating gas | 2002-10-26 | This preparation was warranted to "make a man who smelled it lose consciousness in less time that it takes to… |
| 42 | 5.10 | 0.75 | 110 | Simon Newcomb | *Side-Lights on Astronomy* (1906) | Large astrometric surveys of star posit… † | 2016-09-14 | At the end of the twentieth century we may expect that the work will be repeated. Then, by comparing the char… |
| 43 | 5.10 | 0.75 | 110 | Luis Senarens | *From Zone to Zone* (1894) | Electric-powered aircraft | 2004 | The engine-room held the powerful electric engines which formed the motive power of the airship. |
| 44 | 5.09 | 0.625 | 282 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Rocket-powered aircraft | 1944 | they ought to bind around it a number of rockets because their rapid ascent would lift it high in the air, th… |
| 45 | 5.08 | 0.75 | 108 | Jules Verne | *All Around the Moon* (1870) | Gravity-neutral (Lagrange) point betwee… | 1978-11-20 | Suppose it to be animated by just sufficient velocity to reach the neutral point, but not to pass it. In that… |
| 46 | 5.06 | 0.75 | 106 | William Wallace Cook | *Adrift in the Unknown* (1904) | Spray-on protective body coating † | 2010-09 | we are coated, and our clothing impregnated, with my anti-temperature fluid. |
| 47 | 5.06 | 0.75 | 106 | Jules Verne | *The Moon-Voyage* (1872) | Gravity-neutral (Lagrange) point betwee… | 1978-11-20 | Either the velocity of the projectile will then be insufficient, and it will remain entirely motionless on th… |
| 48 | 5.04 | 0.75 | 104 | Murray Leinster | *The Mad Planet* (1920) | Glowing plants and animals | 2024-04 | the shining mushrooms that gave out light at night |
| 49 | 5.03 | 0.75 | 103 | Jules Verne | *Five Weeks in a Balloon* (1863) | Hydrogen and oxygen engines and heating | 1966-05-30 | I decompose it by means of a powerful Buntzen battery. Water, as you know, consists of two parts of hydrogen… |
| 50 | 5.03 | 0.75 | 103 | Hugo Gernsback | *Ralph 124C 41+* (1911) | Accelerated aging and curing | 2014-12 | The leaves had been aged rapidly by dry heat in a partial vacuum. |

## Authors: total points

Each author counts a concept once, from their best book. 771 authors score.

| # | author | points | concepts | books | points per book | precision |
|---|---|---|---|---|---|---|
| 1 | E. E. Smith | 439.9 | 170 | 20 | 22.0 | 11% of 2868 |
| 2 | H. G. Wells | 393.5 | 137 | 27 | 14.6 | 22% of 1515 |
| 3 | Murray Leinster | 368.6 | 159 | 58 | 6.4 | 17% of 2144 |
| 4 | Jules Verne | 355.9 | 110 | 16 | 22.2 | 19% of 1082 |
| 5 | George O. Smith | 337.8 | 138 | 57 | 5.9 | 12% of 2076 |
| 6 | Ray Cummings | 320.2 | 130 | 36 | 8.9 | 12% of 1907 |
| 7 | Edmond Hamilton | 291.5 | 107 | 34 | 8.6 | 16% of 959 |
| 8 | John W. Campbell Jr | 291.2 | 117 | 12 | 24.3 | 16% of 1241 |
| 9 | Godfrey Sweven | 265.1 | 93 | 2 | 132.5 | 20% of 568 |
| 10 | George Chetwynd Griffith | 257.9 | 92 | 6 | 43.0 | 30% of 803 |
| 11 | Raymond Z. Gallun | 253.1 | 102 | 17 | 14.9 | 22% of 701 |
| 12 | Randall Garrett | 249.9 | 110 | 78 | 3.2 | 11% of 1590 |
| 13 | Fritz Leiber | 232.7 | 97 | 29 | 8.0 | 19% of 657 |
| 14 | H. Beam Piper | 221.7 | 102 | 32 | 6.9 | 14% of 1180 |
| 15 | Edgar Rice Burroughs | 209.5 | 81 | 21 | 10.0 | 9% of 1200 |
| 16 | F. L. Wallace | 209.4 | 95 | 18 | 11.6 | 17% of 551 |
| 17 | Garrett Putman Serviss | 205.3 | 75 | 6 | 34.2 | 15% of 585 |
| 18 | Nelson S. Bond | 192.2 | 76 | 37 | 5.2 | 15% of 741 |
| 19 | Stephen Marlowe | 176.2 | 74 | 53 | 3.3 | 14% of 750 |
| 20 | Hugo Gernsback | 167.6 | 53 | 2 | 83.8 | 30% of 223 |
| 21 | Bryce Walton | 158.9 | 69 | 38 | 4.2 | 14% of 536 |
| 22 | Robert Silverberg | 158.4 | 74 | 42 | 3.8 | 13% of 720 |
| 23 | Alan Edward Nourse | 151.8 | 71 | 33 | 4.6 | 15% of 541 |
| 24 | Percy Greg | 151.6 | 48 | 1 | 151.6 | 27% of 248 |
| 25 | Jack Williamson | 148.7 | 58 | 11 | 13.5 | 14% of 391 |
| 26 | Carey Rockwell | 146.7 | 63 | 6 | 24.4 | 22% of 535 |
| 27 | Roy Rockwood | 140.1 | 54 | 7 | 20.0 | 20% of 404 |
| 28 | Richard M. Elam | 136.0 | 61 | 3 | 45.3 | 32% of 307 |
| 29 | Leigh Brackett | 118.8 | 49 | 21 | 5.7 | 11% of 501 |
| 30 | John Jacob Astor | 114.1 | 42 | 1 | 114.1 | 20% of 202 |

## Books: total points

| # | book | author | group | points | concepts |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | Science-Fiction | 245.4 | 86 |
| 2 | *Across the Zodiac* (1880) | Percy Greg | Science-Fiction | 151.6 | 48 |
| 3 | *Ralph 124C 41+* (1911) | Hugo Gernsback | Science-Fiction | 149.4 | 45 |
| 4 | *Skylark Three* (1930) | E. E. Smith | Science-Fiction | 118.4 | 40 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | Science-Fiction | 115.1 | 43 |
| 6 | *Spacehounds of IPC* (1931) | E. E. Smith | Science-Fiction | 114.4 | 43 |
| 7 | *A Journey in Other Worlds* (1894) | John Jacob Astor | Science-Fiction | 114.1 | 42 |
| 8 | *All Around the Moon* (1870) | Jules Verne | Science-Fiction | 112.6 | 33 |
| 9 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | Futurism | 112.0 | 35 |
| 10 | *When the Sleeper Wakes* (1899) | H. G. Wells | Science-Fiction | 110.6 | 42 |
| 11 | *The Moon-Voyage* (1872) | Jules Verne | Science-Fiction | 110.6 | 35 |
| 12 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | Science-Fiction | 105.0 | 37 |
| 13 | *Maza of the Moon* (1929) | Otis Adelbert Kline | Science-Fiction | 91.5 | 33 |
| 14 | *Through the Sun in an Airship* (1909) | John Mastin | Science-Fiction | 90.6 | 38 |
| 15 | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Mrs. Loudon | Science-Fiction | 90.5 | 30 |
| 16 | *The Skylark of Valeron* (1934) | E. E. Smith | Science-Fiction | 87.7 | 34 |
| 17 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | Science-Fiction | 86.5 | 33 |
| 18 | *Space Tug* (1953) | Murray Leinster | Science-Fiction | 85.4 | 38 |
| 19 | *The Green Millennium* (1953) | Fritz Leiber | Science-Fiction | 83.3 | 33 |
| 20 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | Science-Fiction | 82.8 | 42 |
| 21 | *Pharaoh's Broker* (1899) | Ellsworth Douglass | Science-Fiction | 82.3 | 26 |
| 22 | *A Trip to Venus* (1897) | John Munro | Science-Fiction | 80.7 | 26 |
| 23 | *The Sleeper Awakes* (1899) | H. G. Wells | Science-Fiction | 80.6 | 32 |
| 24 | *Tarrano the Conqueror* (1925) | Ray Cummings | Science-Fiction | 78.6 | 31 |
| 25 | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Jules Verne; Henri Théophile Hildibrand | Science-Fiction | 78.1 | 25 |
| 26 | *Triplanetary* (1948) | E. E. Smith | Science-Fiction | 77.8 | 34 |
| 27 | *The World Set Free* (1913) | H. G. Wells | Science-Fiction | 77.6 | 32 |
| 28 | *Last and First Men* (1930) | Olaf Stapledon | Science-Fiction | 74.4 | 29 |
| 29 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | Science-Fiction | 74.2 | 25 |
| 30 | *Venus Equilateral* (1947) | George O. Smith; John W. Campbell Jr | Science-Fiction | 74.1 | 32 |

## Precision

Claims realized at a score of 0.5 or more, of all tranche-A claims by the author; authors with 50 or more (314).

| # | author | precision | claims | points |
|---|---|---|---|---|
| 1 | Edwin Balmer | 46% | 54 | 13.1 |
| 2 | William MacHarg | 46% | 54 | 13.1 |
| 3 | Harold L. Goodwin | 40% | 208 | 74.0 |
| 4 | Ignatius Donnelly | 34% | 90 | 68.0 |
| 5 | Jeff Sutton | 33% | 85 | 35.4 |
| 6 | Richard M. Elam | 32% | 307 | 136.0 |
| 7 | Nikola Tesla | 32% | 66 | 44.6 |
| 8 | Walter M. Miller | 32% | 85 | 55.3 |
| 9 | George Gordon Hastings | 32% | 73 | 36.0 |
| 10 | Mary E. Bradley Lane | 31% | 104 | 59.1 |
| 11 | George Chetwynd Griffith | 30% | 803 | 257.9 |
| 12 | Hugo Gernsback | 30% | 223 | 167.6 |
| 13 | Luis Senarens | 30% | 395 | 91.9 |
| 14 | Rudyard Kipling | 29% | 118 | 65.6 |
| 15 | Wilbur Finley Fauley | 29% | 80 | 38.0 |
| 16 | Arthur Cheney Train | 29% | 112 | 86.7 |
| 17 | Robert Williams Wood | 29% | 112 | 86.7 |
| 18 | Walt Richmond | 28% | 101 | 42.6 |
| 19 | John Munro | 27% | 95 | 80.7 |
| 20 | T. Baron Russell | 27% | 139 | 112.0 |

## Points per book

Authors with 3 or more books in the corpus (257); every book counts, including those with no tranche-A points.

| # | author | points per book | books | points |
|---|---|---|---|---|
| 1 | Richard M. Elam | 45.3 | 3 | 136.0 |
| 2 | George Chetwynd Griffith | 43.0 | 6 | 257.9 |
| 3 | Garrett Putman Serviss | 34.2 | 6 | 205.3 |
| 4 | Camille Flammarion | 34.2 | 3 | 102.5 |
| 5 | George Allan England | 33.6 | 3 | 100.9 |
| 6 | Carey Rockwell | 24.4 | 6 | 146.7 |
| 7 | John W. Campbell Jr | 24.3 | 12 | 291.2 |
| 8 | Charles Willard Diffin | 22.5 | 4 | 90.1 |
| 9 | Otis Adelbert Kline | 22.4 | 5 | 111.8 |
| 10 | Roman Frederick Starzl | 22.3 | 3 | 66.8 |
| 11 | Jules Verne | 22.2 | 16 | 355.9 |
| 12 | E. E. Smith | 22.0 | 20 | 439.9 |
| 13 | Rudyard Kipling | 21.9 | 3 | 65.6 |
| 14 | Roy Rockwood | 20.0 | 7 | 140.1 |
| 15 | E. Everett Evans | 18.7 | 4 | 75.0 |
| 16 | Guy Thorne | 17.2 | 3 | 51.5 |
| 17 | Ralph Milne Farley | 15.6 | 4 | 62.5 |
| 18 | Neil R. Jones | 15.4 | 5 | 76.8 |
| 19 | Anthony Gilmore | 15.1 | 4 | 60.4 |
| 20 | Raymond Z. Gallun | 14.9 | 17 | 253.1 |

## By era

The best books of each era, by publication year.

**pre-1900** (121 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Across the Zodiac* (1880) | Percy Greg | 151.6 |
| 2 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 115.1 |
| 3 | *A Journey in Other Worlds* (1894) | John Jacob Astor | 114.1 |
| 4 | *All Around the Moon* (1870) | Jules Verne | 112.6 |
| 5 | *When the Sleeper Wakes* (1899) | H. G. Wells | 110.6 |
| 6 | *The Moon-Voyage* (1872) | Jules Verne | 110.6 |
| 7 | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Mrs. Loudon | 90.5 |
| 8 | *Pharaoh's Broker* (1899) | Ellsworth Douglass | 82.3 |
| 9 | *A Trip to Venus* (1897) | John Munro | 80.7 |
| 10 | *The Sleeper Awakes* (1899) | H. G. Wells | 80.6 |

**1900–1945** (630 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 245.4 |
| 2 | *Ralph 124C 41+* (1911) | Hugo Gernsback | 149.4 |
| 3 | *Skylark Three* (1930) | E. E. Smith | 118.4 |
| 4 | *Spacehounds of IPC* (1931) | E. E. Smith | 114.4 |
| 5 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 112.0 |
| 6 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | 105.0 |
| 7 | *Maza of the Moon* (1929) | Otis Adelbert Kline | 91.5 |
| 8 | *Through the Sun in an Airship* (1909) | John Mastin | 90.6 |
| 9 | *The Skylark of Valeron* (1934) | E. E. Smith | 87.7 |
| 10 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | 86.5 |

**1946–1979** (1705 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Space Tug* (1953) | Murray Leinster | 85.4 |
| 2 | *The Green Millennium* (1953) | Fritz Leiber | 83.3 |
| 3 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | 82.8 |
| 4 | *Triplanetary* (1948) | E. E. Smith | 77.8 |
| 5 | *Venus Equilateral* (1947) | George O. Smith; John W. Campbell Jr | 74.1 |
| 6 | *The Planet Strappers* (1961) | Raymond Z. Gallun | 67.2 |
| 7 | *People Minus X* (1957) | Raymond Z. Gallun | 60.0 |
| 8 | *Pioneers of Space* (1949) | George Adamski | 57.8 |
| 9 | *Rip Foster in Ride the Gray Planet* (1952) | Harold L. Goodwin | 56.4 |
| 10 | *Space Platform* (1953) | Murray Leinster | 55.7 |

**1980+** (1 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Astounding Stories of Super-Science January 1930* (2012) | Harry Bates | 1.9 |

## Other corpus groups

The non-fiction, classics, prophecy and religious texts. Their years are the library's, which for translations is the translation's year (lead is then understated); the curated composition dates and the second-translation re-judging of DESIGN §1a are not built. Religious texts rank by text, not by translator.

| group | book | author | points | rank |
|---|---|---|---|---|
| Classics | *New Atlantis* (1627) | Francis Bacon | 61.9 | 47 |
| Classics | *Utopia* (1516) | Thomas More | 5.0 | 1432 |
| Classics | *The City of the Sun* (1602) | Tommaso Campanella | 3.8 | 1653 |
| Fiction | *A Diversity of Creatures* (1917) | Rudyard Kipling | 27.3 | 203 |
| Fiction | *Actions and Reactions* (1909) | Rudyard Kipling | 27.3 | 206 |
| Fiction | *Futility (The Wreck of the Titan)* (1898) | Morgan Robertson | 16.7 | 392 |
| Futurism | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 112.0 | 9 |
| Futurism | *Anticipations* (1901) | H. G. Wells | 60.1 | 49 |
| Futurism | *The Problem of Increasing Human Energy* (1900) | Nikola Tesla | 44.6 | 81 |
| Prophecy | *The True Prophecies or Prognostications of Michael Nostrada…* (1672) | Nostradamus | 2.9 | 1869 |
| Prophecy | *The Sibylline Oracles* (1899) | (text) | 2.3 | 2007 |
| Religion | *The Mahabharata, Volume 1 (Books 1-3)* (1896) | (text) | 17.9 | 360 |
| Religion | *The Mahabharata, Volume 2 (Books 4-7)* (1896) | (text) | 12.6 | 581 |
| Religion | *The Elder Eddas and the Younger Eddas* (1866) | (text) | 10.6 | 704 |
| Science | *Side-Lights on Astronomy* (1906) | Simon Newcomb | 37.8 | 119 |

## Sensitivity: points only from a score of 0.5

5,471 of 16,803 judged `will` pairs score below 0.5; without them 3,206 entries and 4,405 of 26,458 points go. Of the top 30 authors, 28 stay in the top 30; of the top 30 books, 28.

| # | author (default) | points | author (from 0.5) | points |
|---|---|---|---|---|
| 1 | E. E. Smith | 439.9 | E. E. Smith | 392.7 |
| 2 | H. G. Wells | 393.5 | H. G. Wells | 354.0 |
| 3 | Murray Leinster | 368.6 | Murray Leinster | 340.8 |
| 4 | Jules Verne | 355.9 | Jules Verne | 318.7 |
| 5 | George O. Smith | 337.8 | George O. Smith | 298.1 |
| 6 | Ray Cummings | 320.2 | Ray Cummings | 271.3 |
| 7 | Edmond Hamilton | 291.5 | Edmond Hamilton | 265.3 |
| 8 | John W. Campbell Jr | 291.2 | John W. Campbell Jr | 258.7 |
| 9 | Godfrey Sweven | 265.1 | Godfrey Sweven | 233.8 |
| 10 | George Chetwynd Griffith | 257.9 | Randall Garrett | 232.6 |
| 11 | Raymond Z. Gallun | 253.1 | Raymond Z. Gallun | 229.5 |
| 12 | Randall Garrett | 249.9 | Fritz Leiber | 220.6 |
| 13 | Fritz Leiber | 232.7 | George Chetwynd Griffith | 220.2 |
| 14 | H. Beam Piper | 221.7 | H. Beam Piper | 201.1 |
| 15 | Edgar Rice Burroughs | 209.5 | Edgar Rice Burroughs | 177.9 |
| 16 | F. L. Wallace | 209.4 | F. L. Wallace | 172.3 |
| 17 | Garrett Putman Serviss | 205.3 | Nelson S. Bond | 171.9 |
| 18 | Nelson S. Bond | 192.2 | Garrett Putman Serviss | 169.8 |
| 19 | Stephen Marlowe | 176.2 | Hugo Gernsback | 155.7 |
| 20 | Hugo Gernsback | 167.6 | Stephen Marlowe | 154.2 |

## The deciding concepts after tier 2 (PLAN §5)

165 concepts carry a top entry now, by the first scoring's criteria; tier 2 checked 139 of them (`runs/match/deciding.jsonl` keeps the first scoring's 165). By criterion (a concept can meet several):

- best entry of a top-100 author: 63
- best entry of a top-100 book: 71
- lead over 40 years for 20+ claims: 60
- top-300 prediction: 125
- top-50 entry, 1900–1945: 29
- top-50 entry, 1946–1979: 19
- top-50 entry, 1980+: 1
- top-50 entry, pre-1900: 38

Their milestones: confidence high 27, low 49, medium 89; 127 have a contemporary source, 22 rest on Wikipedia alone, 59 are demonstrations only.

The 40 that carry the most points, and every one tier 2 did not check:

| concept | points | entries | lead > 40 | milestone | confidence | sources | best entry | tier 2 |
|---|---|---|---|---|---|---|---|---|
| Death ray | 502.9 | 189 | 333 | 2003-03: The US Army deployed the Zeus-HLONS, a Humvee-mounted laser, to Bagra… | medium | reference | Ray Cummings, *The Sea Girl* (1929) | checked |
| Spacesuit | 406.7 | 177 | 11 | 1969-01-16: Yevgeny Khrunov and Alexei Yeliseyev, wearing Yastreb suits with ches… | high | contemporary | Jules Verne, *All Around the Moon* (1870) | checked |
| Sleep and incapacitating gas | 376.5 | 104 | 144 | 2002-10-26: Russian special forces pumped an aerosol anesthetic (believed to be a… | high | contemporary | Manly Wade Wellman, *Warrior of Two Worlds* (1944) | checked |
| Private and personal spacecraft | 351.8 | 133 | 153 | 2021-07-20: Blue Origin NS-16: New Shepard carried Bezos, his brother Mark, Wally… | medium | contemporary | Murray Leinster, *If You Was a Moklin* (1951) | checked |
| Closed-loop life support | 337.2 | 138 | 72 | 1972-12 †: BIOS-3, Institute of Biophysics, Krasnoyarsk: crewed closure experime… | medium | reference | Hugo Gernsback, *Ralph 124C 41+* (1911) | checked |
| Radio communication with spacecraft and… | 332.5 | 208 | 25 | 1957-11-03: Sputnik 2, carrying the dog Laika, radioed telemetry of her heartbeat… | medium | contemporary | Hugo Gernsback, *Ralph 124C 41+* (1911) | checked |
| Sonic weapon | 324.5 | 99 | 155 | 2005-11-05: The cruise ship Seabourn Spirit used a long-range acoustic device (LR… | medium | contemporary | Sax Rohmer, *The Day the World Ended* (1929) | checked |
| Non-lethal stun gun | 299.1 | 123 | 16 | 1975-03: The Taser Public Defender, a flashlight-shaped dart stun gun made by… | medium | contemporary | Garrett Putman Serviss, *Edison's Conquest of Mars* (1898) | checked |
| Invisibility | 295.5 | 104 | 255 | 2010-12 †: Baile Zhang, Yuan Luo, Xiaogang Liu and George Barbastathis (MIT/SMAR… | medium | contemporary | Edgar Rice Burroughs, *A Fighting Man of Mars* (1930) | checked |
| Spacecraft video cameras and viewscreens | 273.4 | 125 | 35 | 1973: Skylab crews used the Apollo Telescope Mount video monitors in real t… | low | contemporary | (text), *Astounding Stories of Super-Scienc…* (1931) | checked |
| Video link with spacecraft and other wo… | 252.4 | 104 | 24 | 1979-03-24: The same Salyut 6 two-way TV link was used for the crew to see ground… | medium | contemporary | Otis Adelbert Kline, *Maza of the Moon* (1929) | checked |
| Electric discharge weapon | 238.8 | 112 | 48 | 1963-06-18: Alabama state troopers under Col. Albert Lingo used night sticks and… | low | contemporary | Percy Greg, *Across the Zodiac* (1880) | checked |
| Walking and leaping in low gravity | 197.3 | 70 | 41 | 1969-07-21: The same Apollo 11 moonwalk was real exploration work: the crew loped… | low | contemporary | Jules Verne, *All Around the Moon* (1870) | checked |
| Physical conditions on the Moon and inn… | 190.9 | 123 | 97 | 1962-12-14 †: NASA's Mariner 2 flew past Venus at 21,000 miles; its microwave and i… | medium | contemporary | Charles Napier Richards, *Atalanta* (1900) | checked |
| Crewed Moon landing | 182.2 | 92 | 41 | 1969-07-20 †: Apollo 11's lunar module Eagle landed Neil Armstrong and Buzz Aldrin… | high | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Mind-reading machine | 178.4 | 65 | 96 | 2006 †: Thirion et al. (NeuroSpin, France) decoded fMRI activity to reconstru… | medium | contemporary | Guy Thorne, *The Soul Stealer* (1906) | checked |
| Brain-computer interface | 172.9 | 62 | 55 | 1999-03: Niels Birbaumer's Tubingen group reported that completely paralysed A… | medium | contemporary | Joe Gibson, *The Machine That Floats* (1953) | checked |
| Powered rocket landing | 167.9 | 81 | 10 | 1966-06-02: NASA's Surveyor 1 landed on the Moon in Oceanus Procellarum on 2 June… | high | contemporary | Charles Willard Diffin, *Brood of the Dark Moon* (1931) | checked |
| New or sharpened human senses | 167.3 | 74 | 124 | 2004: Neil Harbisson has worn a skull-anchored antenna since 2004 that give… | low | Wikipedia only | Camille Flammarion, *Lumen* (1873) | checked |
| Brain-to-brain link | 161.4 | 54 | 67 | 2013-08-12 †: At the University of Washington on 12 Aug 2013, Rajesh Rao's EEG-read… | medium | contemporary | E. E. Smith; Lee Hawkins…, *The Skylark of Space* (1928) | checked |
| Weightlessness in spaceflight | 159.0 | 63 | 36 | 1961-04-12 †: Yuri Gagarin orbited the Earth in Vostok 1 and floated weightless in… | high | contemporary | Jules Verne; Henri Théop…, *From the Earth to the Moon, Direct…* (1872) | checked |
| Three-dimensional telepresence | 154.2 | 48 | 67 | 2022: Google began testing Project Starline with partner companies such as… | low | Wikipedia only | Frank Belknap Long, *Woman from Another Planet* (1960) | checked |
| Space-suit helmet radio | 147.1 | 57 | 2 | 1965-03-18 †: Alexei Leonov, outside Voskhod 2 in his suit, stayed in radio contact… | medium | contemporary | Philip Francis Nowlan, *Armageddon—2419 A.D.* (1928) | checked |
| Growing food in space | 145.0 | 54 | 8 | 1975-07-08 †: Salyut 4 cosmonauts Klimuk and Sevastyanov ate onions grown in the Oa… | medium | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Automated kitchen | 138.4 | 50 | 55 | 2016-04: Spyce's robotic kitchen, built by MIT students, was cooking and servi… | low | contemporary | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | checked |
| Nerve-attacking weapon | 138.2 | 57 | 11 | 1975: Taser Public Defender first marketed in March 1975 by Advanced Chemic… | low | contemporary | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Astronaut maneuvering gun or pack | 137.4 | 53 | 1 | 1966-07-19: Michael Collins used the nitrogen-fed HHMU on Gemini 10 to transfer f… | medium | contemporary | Edwin K. Sloat, *Loot of the Void* (1932) | checked |
| Sleep learning | 136.5 | 38 | 44 | 2019-02 †: Zust et al. (University of Bern) played recorded pseudoword/German wo… | low | contemporary | Fritz Leiber, *Appointment In Tomorrow* (1951) | checked |
| Search for extraterrestrial signals | 136.0 | 67 | 65 | 1960-04: Frank Drake's Project Ozma used the 85-foot Green Bank radio telescop… | medium | contemporary | Garrett Putman Serviss, *Other Worlds* (1901) | checked |
| Using local resources in space | 135.0 | 35 | 39 | 2021-04-20 †: NASA's MOXIE instrument on the Perseverance rover made 5.37 g of oxyg… | medium | contemporary | Raymond Z. Gallun, *Eyes That Watch* (1940) | checked |
| Worldwide simultaneous broadcast | 133.5 | 50 | 18 | 1967-06-25 †: Our World, a two-hour live program coordinated by the EBU and BBC, wa… | medium | contemporary | Camille Flammarion, *Omega* (1893) | checked |
| Glowing plants and animals | 133.3 | 41 | 51 | 2024-04: Light Bio began shipping Firefly Petunias (fungal bioluminescence pat… | medium | contemporary | Murray Leinster, *The Mad Planet* (1920) | checked |
| Laboratory-created animal species | 124.2 | 49 | 68 | 2003: Taikong Corp of Taiwan sold genetically modified fluorescent medaka (… | medium | contemporary | Francis Bacon, *New Atlantis* (1627) | checked |
| Pocket wireless telephone | 123.7 | 44 | 24 | 1983-10-13: First commercial wireless call on a Motorola DynaTAC at Ameritech Mob… | medium | Wikipedia only | Mark Wicks, *To Mars Via the Moon* (1911) | checked |
| Smart adaptive clothing | 123.3 | 52 | 22 | 1989: Spyder sold ski wear in a new fabric that changes color with temperat… | low | contemporary | H. G. Wells, *Tales of Space and Time* (1899) | checked |
| Solar electric power generation | 121.3 | 50 | 23 | 1973-07: The Solar One experimental house at the University of Delaware began… | medium | contemporary | Hugo Gernsback, *Ralph 124C 41+* (1911) | checked |
| Automatic house cleaning | 121.2 | 53 | 18 | 1985: A floor-cleaning robot was in use in supermarkets, and the US Navy ha… | low | contemporary | Mary E. Bradley Lane, *Mizora* (1890) | checked |
| Cutting beam or shearing ray | 120.0 | 46 | 5 | 1970: BOC supplied the first true laser cutting machine tool in 1970 to die… | low | reference | Otis Adelbert Kline, *Maza of the Moon* (1929) | checked |
| Creating life from nonliving matter | 119.7 | 50 | 78 | 2010-05-20 †: J. Craig Venter Institute (Gibson et al.) assembled a Mycoplasma myco… | medium | contemporary | Garrett Putman Serviss, *The Second Deluge* (1911) | checked |
| Thought-to-text and thought display | 118.9 | 34 | 47 | 2006 †: Thirion, Duchesnay, Hubbard, Dubois, Poline, Lebihan and Dehaene (Neu… | medium | contemporary | Herbert D. Ward, *A Republic Without a President, an…* (1891) | checked |
| Orbital rendezvous and docking | 113.3 | 46 | 4 | 1969-07-21: Apollo 11 Lunar Module Eagle rendezvoused with and docked to Columbia… | low | Wikipedia only | Hugo Gernsback, *Ralph 124C 41+* (1911) | **not checked** |
| Spacecraft thermal control and insulati… | 102.3 | 41 | 17 | 1961-04-12: Vostok 1: Gagarin reported a cockpit temperature of 20 degrees during… | low | Wikipedia only | Ellsworth Douglass, *Pharaoh's Broker* (1899) | **not checked** |
| Futuristic cosmetics | 92.6 | 39 | 18 | 1988: 1988: topical minoxidil (Rogaine) was approved for treating hair loss… | medium | Wikipedia only | George O. Smith, *Nomad* (1944) | **not checked** |
| Reusable winged spaceplane or shuttle | 81.7 | 37 | 4 | 1982-11: STS-5 (Columbia) was the first operational shuttle flight and deploye… | medium | Wikipedia only | Carey Rockwell, *Treachery in Outer Space* (1954) | **not checked** |
| Uncrewed cargo spacecraft | 63.8 | 23 | 0 | 1978-01-22: Progress 1 launched on 1978-01-20 and docked automatically with Salyu… | medium | Wikipedia only | Edmond Hamilton, *Proxy Planeteers* (1947) | **not checked** |
| Reentry heat protection | 55.6 | 27 | 10 | 1960-08-11: Discoverer 13's reentry capsule (with heat shield) came down from orb… | low | Wikipedia only | Ellsworth Douglass, *Pharaoh's Broker* (1899) | **not checked** |
| Lab-grown or synthetic meat | 44.3 | 11 | 16 | 2020-12: Cultured chicken from Eat Just was sold at restaurant 1880 in Singapo… | medium | Wikipedia only | F. L. Wallace, *Mezzerow Loves Company* (1956) | **not checked** |
| Capsule parachute or sea-splashdown rec… | 34.5 | 16 | 2 | 1961-04-12: Vostok 1's capsule returned the first human from orbit and landed by… | low | Wikipedia only | John Munro, *A Trip to Venus* (1897) | **not checked** |
| Handheld medical analyzer | 33.8 | 14 | 2 | 1981-11: Same event: the Glucometer was sold for home and clinical use. | low | Wikipedia only | Stanton A. Coblentz, *In Caverns Below* (1935) | **not checked** |
| Automatic body-cleaning machine | 33.2 | 14 | 2 | 1970 †: Sanyo showed its Ultrasonic Bath at Expo 70 in Osaka: an enclosed cha… | low | reference | T. Baron Russell, *A Hundred Years Hence (The Expecta…* (1905) | **not checked** |
| Spacecraft cruising at tens of miles pe… | 26.2 | 9 | 5 | 1959-01 †: Luna 1 (launched 2 January 1959) became the first object to reach Ear… | low | Wikipedia only | Ellsworth Douglass, *Pharaoh's Broker* (1899) | **not checked** |
| Manufacturing in space vacuum | 19.5 | 6 | 4 | 1994-02 †: Wake Shield Facility (STS-60) grew crystalline semiconductor thin fil… | medium | Wikipedia only | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Electronic voting and vote counting | 19.5 | 7 | 3 | 1964: Seven US counties switched to punched-card voting with computer tally… | low | Wikipedia only | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Flight data recorder | 16.1 | 5 | 2 | 1954-12: General Mills marketed a Flight Recorder that etched heading, airspee… | low | contemporary | Rudyard Kipling, *With the Night Mail* (1905) | **not checked** |
| Paralyzing drug or venom | 15.7 | 5 | 1 | 1942-01: Harold Griffith and Enid Johnson gave a standardized curare preparati… | low | Wikipedia only | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Giant or supposedly extinct birds survi… | 15.5 | 5 | 9 | 1948-11-20 †: Geoffrey Orbell's expedition rediscovered the South Island takahe, pr… | medium | contemporary | James De Mille, *A Strange Manuscript Found in a Co…* (1888) | **not checked** |
| Large power switch | 13.0 | 4 | 4 | 2012-11 †: ABB announced a hybrid HVDC breaker combining fast mechanics with pow… | low | contemporary | George O. Smith; John W.…, *Venus Equilateral* (1947) | **not checked** |
| Magnetic levitation train | 10.5 | 3 | 3 | 1984: The Birmingham Maglev people mover opened as the first commercial mag… | medium | Wikipedia only | Philip Francis Nowlan, *The Airlords of Han* (1929) | **not checked** |
| Battery-powered spacecraft | 9.7 | 3 | 4 | 1964-07-20 †: NASA Lewis flew SERT-1 on a suborbital rocket; its mercury electron-b… | low | contemporary | Ellsworth Douglass, *Pharaoh's Broker* (1899) | **not checked** |
| Robot combat sport | 9.2 | 3 | 0 | 1987: Same event: an actual held robot combat competition. | low | Wikipedia only | H. Beam Piper, *The Cosmic Computer* (1963) | **not checked** |
| Space weather forecasting | 8.7 | 5 | 2 | 1965: The Space Disturbances Laboratory of the Central Radio Propagation La… | low | reference | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Robot mannequin | 8.6 | 2 | 3 | 2005-02 †: Flower Robotics (Tatsuya Matsui, with SGI Japan) unveiled Palette at… | medium | contemporary | F. L. Wallace, *Tangle Hold* (1953) | **not checked** |
| Credit card payment | 8.1 | 2 | 5 | 1950: Diners Club began issuing cards to members, who signed restaurant tab… | medium | contemporary | Edward Bellamy, *Looking Backward* (1888) | **not checked** |
| Skip reentry | 7.3 | 3 | 0 | 1968-11-17 †: The Soviet Zond 6 lunar-circling capsule returned using a skip reentr… | medium | contemporary | R. R. Winterbotham, *Message from Venus* (1941) | **not checked** |
| Vertical farm | 4.4 | 1 | 1 | 2012: Sky Greens opened in Singapore, billed as the world's first commercia… | low | Wikipedia only | F. L. Wallace, *The Music Master* (1953) | **not checked** |
