# Scoring after tier 2, tranche A (PLAN §8)

Written by `match.py score full`. Settings: weight log (w = log2(1 + min(L, 500))), the scoring milestone `first_practical_use` else `first_demonstration`, points from score 0.125 (every judged score above 0), precision from 0.5, `contradicted_negative` from 0.5, deadlines checked against 2026 with 10 years of grace. This scoring follows tier 2 (PLAN §5), which checked 191 deciding concepts, and checkpoint 3's review (`runs/match/milestone_review.jsonl`). Tranche B is not scored. † = scored on a demonstration only (PLAN §14.5).

## Resolutions

77,436 tranche-A claims from 3,224 books.

| resolution | claims | share |
|---|---|---|
| open: no_milestone | 31,486 | 40.7% |
| realized | 16,095 | 20.8% |
| not_a_prediction | 16,063 | 20.7% |
| open: no_concept | 6,795 | 8.8% |
| open: too_vague | 3,897 | 5.0% |
| untestable | 2,558 | 3.3% |
| open: not_matched | 285 | 0.4% |
| failed: missed_deadline | 170 | 0.2% |
| failed: contradicted_negative | 81 | 0.1% |
| open: no_year | 6 | 0.0% |

Deadlines: 1,741 `will` claims with a concept have a stated time naming a year, decade or century after publication; 765 of those ended before 2016. Of these, 308 are realized anyway, 170 missed the deadline, and 287 are not a prediction. Of the 594 realized claims with a deadline, 522 came true by it and 72 after it (median 15 years late).

## The top 50 predictions

11,534 book–concept entries earn points (each book counts its best claim once per concept).

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

Each author counts a concept once, from their best book. 770 authors score.

| # | author | points | concepts | books | points per book | precision |
|---|---|---|---|---|---|---|
| 1 | E. E. Smith | 435.7 | 169 | 20 | 21.8 | 11% of 2868 |
| 2 | H. G. Wells | 391.1 | 137 | 27 | 14.5 | 22% of 1515 |
| 3 | Murray Leinster | 364.7 | 156 | 58 | 6.3 | 17% of 2144 |
| 4 | Jules Verne | 356.7 | 110 | 16 | 22.3 | 19% of 1082 |
| 5 | George O. Smith | 333.1 | 137 | 57 | 5.8 | 12% of 2076 |
| 6 | Ray Cummings | 320.2 | 130 | 36 | 8.9 | 12% of 1907 |
| 7 | Edmond Hamilton | 291.5 | 107 | 34 | 8.6 | 16% of 959 |
| 8 | John W. Campbell Jr | 290.7 | 117 | 12 | 24.2 | 16% of 1241 |
| 9 | Godfrey Sweven | 264.6 | 93 | 2 | 132.3 | 20% of 568 |
| 10 | George Chetwynd Griffith | 257.9 | 92 | 6 | 43.0 | 30% of 803 |
| 11 | Raymond Z. Gallun | 253.1 | 102 | 17 | 14.9 | 22% of 701 |
| 12 | Randall Garrett | 249.9 | 110 | 78 | 3.2 | 11% of 1590 |
| 13 | Fritz Leiber | 232.8 | 97 | 29 | 8.0 | 19% of 657 |
| 14 | H. Beam Piper | 221.7 | 102 | 32 | 6.9 | 14% of 1180 |
| 15 | F. L. Wallace | 207.5 | 94 | 18 | 11.5 | 17% of 551 |
| 16 | Edgar Rice Burroughs | 205.4 | 80 | 21 | 9.8 | 9% of 1200 |
| 17 | Garrett Putman Serviss | 205.3 | 75 | 6 | 34.2 | 15% of 585 |
| 18 | Nelson S. Bond | 192.2 | 76 | 37 | 5.2 | 15% of 741 |
| 19 | Stephen Marlowe | 173.9 | 73 | 53 | 3.3 | 14% of 750 |
| 20 | Hugo Gernsback | 163.8 | 52 | 2 | 81.9 | 30% of 223 |
| 21 | Bryce Walton | 158.9 | 69 | 38 | 4.2 | 14% of 536 |
| 22 | Robert Silverberg | 156.5 | 73 | 42 | 3.7 | 13% of 720 |
| 23 | Alan Edward Nourse | 151.8 | 71 | 33 | 4.6 | 15% of 541 |
| 24 | Jack Williamson | 148.7 | 58 | 11 | 13.5 | 14% of 391 |
| 25 | Percy Greg | 147.1 | 47 | 1 | 147.1 | 26% of 248 |
| 26 | Carey Rockwell | 146.7 | 63 | 6 | 24.4 | 22% of 535 |
| 27 | Roy Rockwood | 139.4 | 54 | 7 | 19.9 | 20% of 404 |
| 28 | Richard M. Elam | 134.4 | 60 | 3 | 44.8 | 32% of 307 |
| 29 | Leigh Brackett | 118.8 | 49 | 21 | 5.7 | 11% of 501 |
| 30 | John Jacob Astor | 114.1 | 42 | 1 | 114.1 | 20% of 202 |

## Books: total points

| # | book | author | group | points | concepts |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | Science-Fiction | 245.0 | 86 |
| 2 | *Across the Zodiac* (1880) | Percy Greg | Science-Fiction | 147.1 | 47 |
| 3 | *Ralph 124C 41+* (1911) | Hugo Gernsback | Science-Fiction | 145.7 | 44 |
| 4 | *Skylark Three* (1930) | E. E. Smith | Science-Fiction | 118.4 | 40 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | Science-Fiction | 115.1 | 43 |
| 6 | *Spacehounds of IPC* (1931) | E. E. Smith | Science-Fiction | 114.4 | 43 |
| 7 | *A Journey in Other Worlds* (1894) | John Jacob Astor | Science-Fiction | 114.1 | 42 |
| 8 | *All Around the Moon* (1870) | Jules Verne | Science-Fiction | 112.6 | 33 |
| 9 | *The Moon-Voyage* (1872) | Jules Verne | Science-Fiction | 111.4 | 35 |
| 10 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | Futurism | 110.5 | 35 |
| 11 | *When the Sleeper Wakes* (1899) | H. G. Wells | Science-Fiction | 107.9 | 42 |
| 12 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | Science-Fiction | 105.0 | 37 |
| 13 | *Maza of the Moon* (1929) | Otis Adelbert Kline | Science-Fiction | 91.5 | 33 |
| 14 | *Through the Sun in an Airship* (1909) | John Mastin | Science-Fiction | 90.6 | 38 |
| 15 | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Mrs. Loudon | Science-Fiction | 90.5 | 30 |
| 16 | *The Skylark of Valeron* (1934) | E. E. Smith | Science-Fiction | 87.7 | 34 |
| 17 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | Science-Fiction | 86.5 | 33 |
| 18 | *Space Tug* (1953) | Murray Leinster | Science-Fiction | 85.4 | 38 |
| 19 | *The Green Millennium* (1953) | Fritz Leiber | Science-Fiction | 83.4 | 33 |
| 20 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | Science-Fiction | 82.0 | 41 |
| 21 | *Pharaoh's Broker* (1899) | Ellsworth Douglass | Science-Fiction | 80.8 | 26 |
| 22 | *The Sleeper Awakes* (1899) | H. G. Wells | Science-Fiction | 80.6 | 32 |
| 23 | *Tarrano the Conqueror* (1925) | Ray Cummings | Science-Fiction | 78.6 | 31 |
| 24 | *A Trip to Venus* (1897) | John Munro | Science-Fiction | 78.5 | 26 |
| 25 | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Jules Verne; Henri Théophile Hildibrand | Science-Fiction | 78.1 | 25 |
| 26 | *Triplanetary* (1948) | E. E. Smith | Science-Fiction | 77.8 | 34 |
| 27 | *The World Set Free* (1913) | H. G. Wells | Science-Fiction | 77.6 | 32 |
| 28 | *Last and First Men* (1930) | Olaf Stapledon | Science-Fiction | 74.4 | 29 |
| 29 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | Science-Fiction | 74.2 | 25 |
| 30 | *To Mars Via the Moon* (1911) | Mark Wicks | Science-Fiction | 73.9 | 27 |

## Precision

Claims realized at a score of 0.5 or more, of all tranche-A claims by the author; authors with 50 or more (314).

| # | author | precision | claims | points |
|---|---|---|---|---|
| 1 | Edwin Balmer | 46% | 54 | 13.1 |
| 2 | William MacHarg | 46% | 54 | 13.1 |
| 3 | Harold L. Goodwin | 40% | 208 | 74.0 |
| 4 | Ignatius Donnelly | 34% | 90 | 68.0 |
| 5 | Jeff Sutton | 33% | 85 | 35.4 |
| 6 | Richard M. Elam | 32% | 307 | 134.4 |
| 7 | Nikola Tesla | 32% | 66 | 44.6 |
| 8 | Walter M. Miller | 32% | 85 | 55.3 |
| 9 | George Gordon Hastings | 32% | 73 | 36.0 |
| 10 | Mary E. Bradley Lane | 31% | 104 | 59.1 |
| 11 | George Chetwynd Griffith | 30% | 803 | 257.9 |
| 12 | Luis Senarens | 30% | 395 | 91.9 |
| 13 | Hugo Gernsback | 30% | 223 | 163.8 |
| 14 | Rudyard Kipling | 29% | 118 | 65.5 |
| 15 | Wilbur Finley Fauley | 29% | 80 | 38.0 |
| 16 | Arthur Cheney Train | 29% | 112 | 86.7 |
| 17 | Robert Williams Wood | 29% | 112 | 86.7 |
| 18 | John Munro | 27% | 95 | 78.5 |
| 19 | T. Baron Russell | 27% | 139 | 110.5 |
| 20 | Philip Francis Nowlan | 27% | 172 | 90.7 |

## Points per book

Authors with 3 or more books in the corpus (257); every book counts, including those with no tranche-A points.

| # | author | points per book | books | points |
|---|---|---|---|---|
| 1 | Richard M. Elam | 44.8 | 3 | 134.4 |
| 2 | George Chetwynd Griffith | 43.0 | 6 | 257.9 |
| 3 | Garrett Putman Serviss | 34.2 | 6 | 205.3 |
| 4 | Camille Flammarion | 34.2 | 3 | 102.5 |
| 5 | George Allan England | 33.6 | 3 | 100.9 |
| 6 | Carey Rockwell | 24.4 | 6 | 146.7 |
| 7 | John W. Campbell Jr | 24.2 | 12 | 290.7 |
| 8 | Charles Willard Diffin | 22.4 | 4 | 89.5 |
| 9 | Otis Adelbert Kline | 22.4 | 5 | 111.8 |
| 10 | Jules Verne | 22.3 | 16 | 356.7 |
| 11 | Roman Frederick Starzl | 22.3 | 3 | 66.8 |
| 12 | Rudyard Kipling | 21.8 | 3 | 65.5 |
| 13 | E. E. Smith | 21.8 | 20 | 435.7 |
| 14 | Roy Rockwood | 19.9 | 7 | 139.4 |
| 15 | E. Everett Evans | 18.7 | 4 | 75.0 |
| 16 | Guy Thorne | 17.2 | 3 | 51.5 |
| 17 | Neil R. Jones | 15.4 | 5 | 76.8 |
| 18 | Anthony Gilmore | 15.1 | 4 | 60.4 |
| 19 | Ralph Milne Farley | 15.0 | 4 | 59.8 |
| 20 | Raymond Z. Gallun | 14.9 | 17 | 253.1 |

## By era

The best books of each era, by publication year.

**pre-1900** (120 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Across the Zodiac* (1880) | Percy Greg | 147.1 |
| 2 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 115.1 |
| 3 | *A Journey in Other Worlds* (1894) | John Jacob Astor | 114.1 |
| 4 | *All Around the Moon* (1870) | Jules Verne | 112.6 |
| 5 | *The Moon-Voyage* (1872) | Jules Verne | 111.4 |
| 6 | *When the Sleeper Wakes* (1899) | H. G. Wells | 107.9 |
| 7 | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Mrs. Loudon | 90.5 |
| 8 | *Pharaoh's Broker* (1899) | Ellsworth Douglass | 80.8 |
| 9 | *The Sleeper Awakes* (1899) | H. G. Wells | 80.6 |
| 10 | *A Trip to Venus* (1897) | John Munro | 78.5 |

**1900–1945** (629 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 245.0 |
| 2 | *Ralph 124C 41+* (1911) | Hugo Gernsback | 145.7 |
| 3 | *Skylark Three* (1930) | E. E. Smith | 118.4 |
| 4 | *Spacehounds of IPC* (1931) | E. E. Smith | 114.4 |
| 5 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 110.5 |
| 6 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | 105.0 |
| 7 | *Maza of the Moon* (1929) | Otis Adelbert Kline | 91.5 |
| 8 | *Through the Sun in an Airship* (1909) | John Mastin | 90.6 |
| 9 | *The Skylark of Valeron* (1934) | E. E. Smith | 87.7 |
| 10 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | 86.5 |

**1946–1979** (1703 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Space Tug* (1953) | Murray Leinster | 85.4 |
| 2 | *The Green Millennium* (1953) | Fritz Leiber | 83.4 |
| 3 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | 82.0 |
| 4 | *Triplanetary* (1948) | E. E. Smith | 77.8 |
| 5 | *Venus Equilateral* (1947) | George O. Smith; John W. Campbell Jr | 73.4 |
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
| Classics | *Utopia* (1516) | Thomas More | 5.0 | 1427 |
| Classics | *The City of the Sun* (1602) | Tommaso Campanella | 3.8 | 1646 |
| Fiction | *A Diversity of Creatures* (1917) | Rudyard Kipling | 27.3 | 202 |
| Fiction | *Actions and Reactions* (1909) | Rudyard Kipling | 27.3 | 205 |
| Fiction | *Futility (The Wreck of the Titan)* (1898) | Morgan Robertson | 16.7 | 390 |
| Futurism | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 110.5 | 10 |
| Futurism | *Anticipations* (1901) | H. G. Wells | 59.3 | 51 |
| Futurism | *The Problem of Increasing Human Energy* (1900) | Nikola Tesla | 44.6 | 79 |
| Prophecy | *The True Prophecies or Prognostications of Michael Nostrada…* (1672) | Nostradamus | 2.9 | 1863 |
| Prophecy | *The Sibylline Oracles* (1899) | (text) | 2.3 | 2000 |
| Religion | *The Mahabharata, Volume 1 (Books 1-3)* (1896) | (text) | 17.9 | 357 |
| Religion | *The Mahabharata, Volume 2 (Books 4-7)* (1896) | (text) | 12.6 | 579 |
| Religion | *The Elder Eddas and the Younger Eddas* (1866) | (text) | 10.6 | 698 |
| Science | *Side-Lights on Astronomy* (1906) | Simon Newcomb | 37.8 | 118 |

## Sensitivity: points only from a score of 0.5

5,450 of 16,735 judged `will` pairs score below 0.5; without them 3,195 entries and 4,385 of 26,312 points go. Of the top 30 authors, 29 stay in the top 30; of the top 30 books, 28.

| # | author (default) | points | author (from 0.5) | points |
|---|---|---|---|---|
| 1 | E. E. Smith | 435.7 | E. E. Smith | 386.1 |
| 2 | H. G. Wells | 391.1 | H. G. Wells | 350.0 |
| 3 | Murray Leinster | 364.7 | Murray Leinster | 338.4 |
| 4 | Jules Verne | 356.7 | Jules Verne | 321.9 |
| 5 | George O. Smith | 333.1 | George O. Smith | 293.4 |
| 6 | Ray Cummings | 320.2 | Ray Cummings | 271.3 |
| 7 | Edmond Hamilton | 291.5 | Edmond Hamilton | 265.3 |
| 8 | John W. Campbell Jr | 290.7 | John W. Campbell Jr | 258.0 |
| 9 | Godfrey Sweven | 264.6 | Godfrey Sweven | 233.3 |
| 10 | George Chetwynd Griffith | 257.9 | Randall Garrett | 232.6 |
| 11 | Raymond Z. Gallun | 253.1 | Raymond Z. Gallun | 229.5 |
| 12 | Randall Garrett | 249.9 | Fritz Leiber | 220.7 |
| 13 | Fritz Leiber | 232.8 | George Chetwynd Griffith | 220.2 |
| 14 | H. Beam Piper | 221.7 | H. Beam Piper | 201.1 |
| 15 | F. L. Wallace | 207.5 | Edgar Rice Burroughs | 173.8 |
| 16 | Edgar Rice Burroughs | 205.4 | Nelson S. Bond | 171.9 |
| 17 | Garrett Putman Serviss | 205.3 | F. L. Wallace | 171.7 |
| 18 | Nelson S. Bond | 192.2 | Garrett Putman Serviss | 169.8 |
| 19 | Stephen Marlowe | 173.9 | Hugo Gernsback | 151.9 |
| 20 | Hugo Gernsback | 163.8 | Stephen Marlowe | 151.8 |

## The deciding concepts after tier 2 (PLAN §5)

628 concepts carry a top entry or add 5+ points to the author totals now; tier 2 checked 176 of them (`runs/match/deciding.jsonl` lists every concept selected for it, by round). By criterion (a concept can meet several):

- adds 5+ points to the author totals: 624
- best entry of a top-100 author: 64
- best entry of a top-100 book: 70
- lead over 40 years for 20+ claims: 60
- top-300 prediction: 120
- top-50 entry, 1900–1945: 29
- top-50 entry, 1946–1979: 18
- top-50 entry, 1980+: 1
- top-50 entry, pre-1900: 38

Their milestones: confidence high 55, low 310, medium 263; 315 have a contemporary source, 249 rest on Wikipedia alone, 197 are demonstrations only.

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
| Crewed spaceship | 260.1 | 160 | 16 | 1961-04-12: Vostok 1 with Yuri Gagarin aboard was launched on a rocket from Baiko… | medium | Wikipedia only | Leigh Brackett, *A World Is Born* (1941) | **not checked** |
| Video link with spacecraft and other wo… | 252.4 | 104 | 24 | 1979-03-24: The same Salyut 6 two-way TV link was used for the crew to see ground… | medium | contemporary | Otis Adelbert Kline, *Maza of the Moon* (1929) | checked |
| Electric discharge weapon | 238.8 | 112 | 48 | 1963-06-18: Alabama state troopers under Col. Albert Lingo used night sticks and… | low | contemporary | Percy Greg, *Across the Zodiac* (1880) | checked |
| Atomic or nuclear-fission rocket | 226.7 | 140 | 3 | 1959-07 †: Los Alamos fired the Kiwi-A reactor at the Nevada Test Site, heating… | medium | Wikipedia only | Nelson S. Bond, *When Freemen Shall Stand* (1942) | **not checked** |
| Crewed orbital space station | 211.3 | 90 | 0 | 1971-06: Salyut 1 was used as a science station by the Soyuz 11 crew for 23 da… | medium | Wikipedia only | Damon Knight, *The Avenger* (1944) | **not checked** |
| Walking and leaping in low gravity | 197.3 | 70 | 41 | 1969-07-21: The same Apollo 11 moonwalk was real exploration work: the crew loped… | low | contemporary | Jules Verne, *All Around the Moon* (1870) | checked |
| Spacecraft escape boat or lifeboat | 193.7 | 81 | 0 | 1970-04: Apollo 13 lunar module used as lifeboat. | medium | contemporary | Raymond Z. Gallun, *The Revolt of the Star Men* (1931) | **not checked** |
| Spacecraft navigation instruments | 192.0 | 95 | 16 | 1968-12: Apollo 8: Lovell navigated with a spacecraft-mounted sextant by star… | low | Wikipedia only | Ray Cummings, *Tama of the Light Country* (1930) | **not checked** |
| Physical conditions on the Moon and inn… | 190.9 | 123 | 97 | 1962-12-14 †: NASA's Mariner 2 flew past Venus at 21,000 miles; its microwave and i… | medium | contemporary | Charles Napier Richards, *Atalanta* (1900) | checked |
| Crewed Moon landing | 182.2 | 92 | 41 | 1969-07-20 †: Apollo 11's lunar module Eagle landed Neil Armstrong and Buzz Aldrin… | high | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Mind-reading machine | 178.4 | 65 | 96 | 2006 †: Thirion et al. (NeuroSpin, France) decoded fMRI activity to reconstru… | medium | contemporary | Guy Thorne, *The Soul Stealer* (1906) | checked |
| Brain-computer interface | 172.9 | 62 | 55 | 1999-03: Niels Birbaumer's Tubingen group reported that completely paralysed A… | medium | contemporary | Joe Gibson, *The Machine That Floats* (1953) | checked |
| Powered rocket landing | 167.9 | 81 | 10 | 1966-06-02: NASA's Surveyor 1 landed on the Moon in Oceanus Procellarum on 2 June… | high | contemporary | Charles Willard Diffin, *Brood of the Dark Moon* (1931) | checked |
| New or sharpened human senses | 167.3 | 74 | 124 | 2004: Neil Harbisson has worn a skull-anchored antenna since 2004 that give… | low | Wikipedia only | Camille Flammarion, *Lumen* (1873) | checked |
| Brain-to-brain link | 161.4 | 54 | 67 | 2013-08-12 †: At the University of Washington on 12 Aug 2013, Rajesh Rao's EEG-read… | medium | contemporary | E. E. Smith; Lee Hawkins…, *The Skylark of Space* (1928) | checked |
| Weightlessness in spaceflight | 159.0 | 63 | 36 | 1961-04-12 †: Yuri Gagarin orbited the Earth in Vostok 1 and floated weightless in… | high | contemporary | Jules Verne; Henri Théop…, *From the Earth to the Moon, Direct…* (1872) | checked |
| Three-dimensional telepresence | 154.2 | 48 | 67 | 2022: Google began testing Project Starline with partner companies such as… | low | Wikipedia only | Frank Belknap Long, *Woman from Another Planet* (1960) | checked |
| Spaceport | 150.7 | 113 | 0 | 1957-10-04: Baikonur Cosmodrome (founded 1955) launched Sputnik 1, the first spac… | low | Wikipedia only | Raymond F. Jones, *The Seven Jewels of Chamar* (1946) | **not checked** |
| Service robot for the public | 150.0 | 51 | 2 | 1985: The Two Panda Robot Restaurant in Pasadena, California, used two robo… | low | contemporary | Frank Riley, *Abbr.* (1957) | **not checked** |
| Space-suit helmet radio | 147.1 | 57 | 2 | 1965-03-18 †: Alexei Leonov, outside Voskhod 2 in his suit, stayed in radio contact… | medium | contemporary | Philip Francis Nowlan, *Armageddon—2419 A.D.* (1928) | checked |
| Growing food in space | 145.0 | 54 | 8 | 1975-07-08 †: Salyut 4 cosmonauts Klimuk and Sevastyanov ate onions grown in the Oa… | medium | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Machinery-disabling ray | 140.2 | 69 | 15 | 1962-07 †: The Starfish Prime high-altitude nuclear test over Johnston Atoll (9… | low | Wikipedia only | George Allan England, *The Flying Legion* (1919) | **not checked** |
| Automated kitchen | 138.4 | 50 | 55 | 2016-04: Spyce's robotic kitchen, built by MIT students, was cooking and servi… | low | contemporary | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | checked |
| Nerve-attacking weapon | 138.2 | 57 | 11 | 1975-03: Taser Public Defender first marketed in March 1975 by Taser Systems /… | medium | contemporary | Owen Johnson, *The Coming of the Amazons* (1931) | checked |
| Astronaut maneuvering gun or pack | 137.4 | 53 | 1 | 1966-07-19: Michael Collins used the nitrogen-fed HHMU on Gemini 10 to transfer f… | medium | contemporary | Edwin K. Sloat, *Loot of the Void* (1932) | checked |
| Physiological effects of spaceflight | 136.7 | 83 | 15 | 1961-08 †: Gherman Titov, in Vostok 2 (6 August 1961), became the first human to… | high | contemporary | Hugo Gernsback, *Ralph 124C 41+* (1911) | **not checked** |
| Sleep learning | 136.5 | 38 | 44 | 2019-02 †: Zust et al. (University of Bern) played recorded pseudoword/German wo… | low | contemporary | Fritz Leiber, *Appointment In Tomorrow* (1951) | checked |
| Search for extraterrestrial signals | 136.0 | 67 | 65 | 1960-04: Frank Drake's Project Ozma used the 85-foot Green Bank radio telescop… | medium | contemporary | Garrett Putman Serviss, *Other Worlds* (1901) | checked |
| Using local resources in space | 135.0 | 35 | 39 | 2021-04-20 †: NASA's MOXIE instrument on the Perseverance rover made 5.37 g of oxyg… | medium | contemporary | Raymond Z. Gallun, *Eyes That Watch* (1940) | checked |
| Worldwide simultaneous broadcast | 133.5 | 50 | 18 | 1967-06-25 †: Our World, a two-hour live program coordinated by the EBU and BBC, wa… | medium | contemporary | Camille Flammarion, *Omega* (1893) | checked |
| Spacecraft guidance and navigation comp… | 132.6 | 71 | 0 | 1965-03-23: The same Gemini III flight used the computer on a real crewed mission… | low | contemporary | John W. Campbell Jr, *Islands of Space* (1931) | **not checked** |
| Speech synthesis | 115.7 | 43 | 9 | 1976: The Kurzweil Reading Machine (scanner plus Votrax synthesizer reading… | low | contemporary | D. L. James, *Exit From Asteroid 60* (1940) | **not checked** |
| See-through-wall imaging | 112.4 | 47 | 13 | 1970 †: Luis Alvarez's team produced the first muogram, using cosmic-ray muon… | low | contemporary | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Self-driving car | 106.5 | 46 | 5 | 1977 †: Tsukuba Mechanical Engineering Laboratory (Japan) vehicle drove itsel… | medium | Wikipedia only | E. E. Smith, *The Skylark of Valeron* (1934) | **not checked** |
| Orbiting or lunar telescope | 96.2 | 40 | 8 | 1968-12-07: NASA's Orbiting Astronomical Observatory 2 (OAO-2) launched with 11 u… | high | contemporary | E. E. Smith, *Skylark Three* (1930) | **not checked** |
| Jetpack or flying suit | 95.8 | 43 | 15 | 1961-04-20 †: Harold Graham made the first free (untethered) flight of the Bell Roc… | medium | Wikipedia only | Frances Trego Montgomery, *On a Lark to the Planets* (1904) | **not checked** |
| Landing craft carried by a mother ship | 90.0 | 49 | 0 | 1969-07-20: Apollo 11: Lunar Module Eagle, carried by the Apollo spacecraft to lu… | high | contemporary | John Victor Peterson, *Lost in the Future* (1954) | **not checked** |
| Flying car | 86.9 | 46 | 16 | 1937-02-21 †: Waldo Waterman's Arrowbile, a roadable aircraft with a Studebaker eng… | medium | Wikipedia only | Jules Verne, *The Master of the World* (1904) | **not checked** |
| Robot police and security guards | 86.4 | 32 | 9 | 1986: Denning Mobile Robotics' Sentry, marketed as an autonomous mobile sec… | low | contemporary | (text), *Astounding Stories, March, 1931* (1931) | **not checked** |
| Meteoroid-resistant and self-sealing hu… | 85.4 | 41 | 3 | 1966: Lunar Orbiter spacecraft (from August 1966): the thermal-blanket bump… | low | reference | Mark Wicks, *To Mars Via the Moon* (1911) | **not checked** |
| Ion engine | 84.1 | 36 | 6 | 1971-12: The first Hall-type stationary plasma thruster (SPT-50) operated in s… | low | Wikipedia only | John W. Campbell Jr, *The Ultimate Weapon* (1936) | **not checked** |
| Trajectory planning and coasting flight | 84.0 | 46 | 15 | 1959-01-02 †: Luna 1 was launched to Earth escape velocity and coasted into solar o… | low | Wikipedia only | Arthur Cheney Train; Rob…, *The Moon Maker* (1916) | **not checked** |
| Planetary surface rover | 83.6 | 42 | 0 | 1970-11: Lunokhod 1, carried by Luna 17, landed on the Moon in November 1970 (… | high | contemporary | Jack Williamson, *The Green Girl* (1930) | **not checked** |
| Computerized information retrieval | 82.8 | 47 | 2 | 1967-05: Ames Research Center began using a DIALOG-fed remote terminal linked… | low | contemporary | H. Beam Piper, *Police Operation* (1948) | **not checked** |
| Assembly of structures in orbit | 78.5 | 32 | 1 | 1983-03-10: Kosmos 1443, a heavy module launched 2 March 1983, docked to Salyut 7… | low | Wikipedia only | Dean Ing, *Tight Squeeze* (1955) | **not checked** |
| Magnetic boots and grapples | 78.0 | 39 | 0 | 1959 †: The USAF Wright Air Development Center Aero Medical Laboratory built… | medium | contemporary | Jack Williamson, *Salvage in Space* (1933) | **not checked** |
| Transmutation of elements | 77.5 | 39 | 11 | 1941 †: Sherr, Bainbridge and Anderson at Harvard turned mercury into gold is… | medium | contemporary | Margaret Cavendish Newca…, *The Description of a New World, Ca…* (1666) | **not checked** |
| Speech recognition and voice command | 77.5 | 32 | 6 | 1972: Threshold Technology (Delran/Cinnaminson, NJ) brought out the VIP-100… | medium | contemporary | Green Peyton, *The Chamber of Life* (1929) | **not checked** |
| Dirigible airship | 76.7 | 48 | 1 | 1910-06: DELAG, the first airline using aircraft in revenue service, began Zep… | low | Wikipedia only | Jules Verne, *Robur the Conqueror* (1886) | **not checked** |
| Aerial bombing | 75.2 | 28 | 0 | 1911-11-01: Lt. Giulio Gavotti, Italy, dropped hand-thrown grenades from an Etric… | medium | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Airplane | 74.5 | 46 | 2 | 1911-10-23: Italian Captain Carlo Piazza flew the first airplane reconnaissance m… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Rescue of people stranded in space | 74.4 | 42 | 1 | 1970-04: Apollo 13: after the service module explosion the crew used the lunar… | low | Wikipedia only | Carey Rockwell, *Danger in Deep Space* (1953) | **not checked** |
| Detecting planets of other stars | 73.7 | 30 | 17 | 1992-01 †: Aleksander Wolszczan and Dale Frail announced two planets around the… | high | contemporary | A. Garland Mears, *Mercia, the Astronomer Royal* (1895) | **not checked** |
| Television broadcasting | 73.5 | 42 | 3 | 1935-03-22: Fernsehsender Paul Nipkow in Berlin started the world's first regular… | medium | Wikipedia only | H. G. Wells, *The Sleeper Awakes* (1899) | **not checked** |
| Ornithopter | 73.4 | 27 | 12 | 1942 †: Adalbert Schmid flew a human-powered flapping-wing aircraft 900 m at… | low | Wikipedia only | Mary Wollstonecraft Shel…, *The Last Man* (1826) | **not checked** |
| Man-portable nuclear weapon | 69.7 | 42 | 1 | 1962-07-17 †: The U.S. Army fired a Davy Crockett M388 round with a W54 nuclear war… | medium | Wikipedia only | Sewell Peaslee Wright, *The Death-Traps of FX-31* (1933) | **not checked** |
| Video intercom and door viewer | 69.4 | 44 | 1 | 1954 †: Kay Lab of San Diego developed a TV-telephone intercom: stations like… | medium | contemporary | Roman Frederick Starzl, *In the Orbit of Saturn* (1931) | **not checked** |
| Immersive virtual reality | 69.1 | 25 | 6 | 1990: VPL Research's Reality Built for Two (EyePhone head-mounted display p… | medium | contemporary | Stanley G. Weinbaum, *Pygmalion's Spectacles* (1935) | **not checked** |
| Electronic location tracking of people | 68.5 | 28 | 5 | 1982: Judge Jack Love persuaded Michael Goss to found NIMCOS, which built r… | low | Wikipedia only | Stanley Mullen, *The Pit of Nympthons* (1951) | **not checked** |
| Closed-circuit video surveillance | 67.7 | 32 | 8 | 1942: Siemens installed a closed-circuit television system at Test Stand VI… | medium | Wikipedia only | Edward Bellamy, *Equality* (1897) | **not checked** |
| Photographing and mapping planets from… | 67.2 | 35 | 9 | 1966-08: Lunar Orbiter 1 photographed the Moon from lunar orbit (August 1966)… | low | Wikipedia only | Jack Williamson, *The Prince of Space* (1931) | **not checked** |
| Machine translation | 65.4 | 45 | 6 | 1959: IBM's Automatic Language Translator (AN/GSQ-16) was installed at the… | low | Wikipedia only | David R. Sparks, *The Winged Men of Orcon* (1932) | **not checked** |
| Space beacons and navigation aids | 64.8 | 34 | 0 | 1965-12-15 †: Gemini VI-A's rendezvous radar locked on the transponder carried by G… | low | contemporary | Edmond Hamilton, *Outside the Universe* (1929) | **not checked** |
| Nuclear missile and ICBM | 63.5 | 43 | 0 | 1959-02-09: First Soviet strategic-missile unit with R-7 became operational at Pl… | low | Wikipedia only | Rog Phillips, *Cube Root of Conquest* (1948) | **not checked** |
| Atomic bomb | 62.5 | 30 | 0 | 1945-08-06: The US B-29 Enola Gay dropped the uranium bomb Little Boy on Hiroshim… | high | contemporary | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Portable two-way radio | 61.3 | 27 | 0 | 1941: SCR-536 was in mass production by July 1941 for the US Army Signal Co… | low | Wikipedia only | George Allan England, *The Flying Legion* (1919) | **not checked** |
| Night vision | 60.7 | 27 | 2 | 1945: German Panther tanks fitted with FG 1250 infrared night sights (about… | low | Wikipedia only | Cyrano de Bergerac, *Voyages to the Moon and the Sun* (1662) | **not checked** |
| Military space station or lunar weapons… | 60.0 | 30 | 1 | 1974-07: Almaz military station Salyut 3 (launched 1974-06-25) was crewed by S… | medium | Wikipedia only | Michael Shaara, *The Vanisher* (1954) | **not checked** |
| Spacecraft attitude control | 60.0 | 31 | 5 | 1959-10: Luna 3 used gas jets and gyroscopic units to orient itself three-axis… | low | Wikipedia only | Arthur Cheney Train; Rob…, *The Moon Maker* (1916) | **not checked** |
| Needle and dart gun | 59.3 | 38 | 2 | 1953: University of Georgia scientists darted seven free-ranging deer with… | low | Wikipedia only | Otis Adelbert Kline, *The Planet of Peril* (1929) | **not checked** |
| Spacecraft flown by one or two people | 56.9 | 33 | 1 | 1961-04-12: Yuri Gagarin flew one orbit in Vostok 1, a spacecraft designed for on… | high | contemporary | Jack Williamson, *Salvage in Space* (1933) | **not checked** |
| Pain ray | 55.5 | 20 | 18 | 1999 †: An Active Denial System millimeter-wave beam that heats skin to produ… | low | contemporary | Fritz Leiber, *Destiny Times Three* (1945) | **not checked** |
| News on a home screen | 54.1 | 25 | 13 | 1974-09-23: The BBC began an experimental public Ceefax service with thirty pages… | medium | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Engineered microorganisms | 53.8 | 22 | 6 | 1982: Eli Lilly marketed Humulin, human insulin made by engineered E. coli,… | medium | Wikipedia only | Olaf Stapledon, *Last and First Men* (1930) | **not checked** |
| Smart home and home automation | 52.3 | 27 | 2 | 1966: ECHO IV served the Sutherland household's daily routines in his home… | low | Wikipedia only | George Allan England, *The Flying Legion* (1919) | **not checked** |
| Self-destruct device | 52.2 | 24 | 1 | 1960-12: Korabl-Sputnik 3 (Vostok 1K No.5), launched 1960-12-01: after a faile… | low | reference | J. U. Giesy, *Jason, Son of Jason* (1921) | **not checked** |
| Light strong aircraft materials | 52.0 | 24 | 1 | 1918: The all-duralumin Junkers D.I fighter brought all-duralumin aircraft… | low | Wikipedia only | Jules Verne, *Robur the Conqueror* (1886) | **not checked** |
| Radiation protection and resistance | 52.0 | 22 | 4 | 1986-04: Poland gave potassium iodide to 10.5 million children and 7 million a… | low | Wikipedia only | Walt Richmond; Leigh Ric…, *Where I Wasn't Going* (1963) | **not checked** |
| Automated fingerprint recognition | 51.3 | 25 | 4 | 1965 †: J. H. Wegstein at the US National Bureau of Standards developed compu… | low | Wikipedia only | Walter J. Sheldon, *Brink of Madness* (1953) | **not checked** |
| Jet-powered car | 49.9 | 31 | 0 | 1963: Craig Breedlove's jet-powered Spirit of America set an FIM-validated… | medium | Wikipedia only | Robert Sheckley, *Cost of Living* (1952) | **not checked** |
| First controlled nuclear chain reaction | 49.1 | 32 | 2 | 1942-12-02 †: Enrico Fermi's team made Chicago Pile-1 critical at the University of… | medium | reference | Garrett Putman Serviss, *A Columbus of Space* (1909) | **not checked** |
| Radioisotope power source | 48.9 | 27 | 4 | 1961-06: Transit 4A, launched 29 June 1961, was the first satellite powered by… | high | contemporary | Rudyard Kipling, *With the Night Mail* (1905) | **not checked** |
| Industrial laser and cutting tool | 48.3 | 24 | 2 | 1965: Western Electric's Engineering Research Center used a laser productio… | low | contemporary | John W. Campbell Jr, *The Metal Horde* (1930) | **not checked** |
| Portable news reporting gear | 48.2 | 22 | 6 | 1974: KMOX-TV St. Louis switched entirely to ENG in 1974. | low | Wikipedia only | Carey Rockwell, *Treachery in Outer Space* (1954) | **not checked** |
| Transatlantic flight | 48.0 | 22 | 0 | 1928-10: The Graf Zeppelin carried 20 passengers from Friedrichshafen to Lakeh… | medium | contemporary | George Chetwynd Griffith, *The World Peril of 1910* (1906) | **not checked** |
| Flight to the poles | 47.7 | 19 | 1 | 1926-05-12 †: The airship Norge, led by Amundsen, Ellsworth and Nobile, flew over t… | medium | Wikipedia only | S. E. Chapman, *Doctor Jones' Picnic* (1898) | **not checked** |
| Message capsule between worlds | 47.4 | 22 | 8 | 1969-07: The Apollo 11 astronauts left a silicon disc bearing goodwill message… | low | Wikipedia only | Herbert M. Vaughan, *Meleager* (1916) | **not checked** |
| Self-repairing machine | 47.3 | 27 | 2 | 1969-03 †: The JPL STAR (Self-Testing And Repairing) computer, designed by Avizi… | medium | contemporary | Bryce Walton, *The Ultimate World* (1945) | **not checked** |
| Anti-nausea drug for spaceflight | 46.7 | 18 | 2 | 1973-07: Same event: Skylab 3 crew took scopolamine/dextroamphetamine to treat… | low | contemporary | George O. Smith, *Off the Beam* (1944) | **not checked** |
| Rooftop landing stage | 46.7 | 19 | 1 | 1935-05: The autogiro carried US air mail to the roof of the new Philadelphia… | low | contemporary | Camille Flammarion, *Omega* (1893) | **not checked** |
| Exotic fuel mineral | 46.6 | 30 | 8 | 1954-06: Obninsk, USSR, became the first nuclear power plant to feed electrici… | medium | Wikipedia only | Roy Rockwood, *Through Space to Mars* (1910) | **not checked** |
| Communications relay satellite | 46.2 | 21 | 0 | 1962-07: Telstar 1 (launched 10 July 1962) relayed the first live transatlanti… | medium | contemporary | George O. Smith, *Recoil* (1943) | **not checked** |
| Question-answering computer | 45.9 | 18 | 3 | 1993: MIT's START went online on the Internet in 1993 and answered English… | low | Wikipedia only | Neil P. Ruzic, *The Deep One* (1957) | **not checked** |
| Ultra-deep drilling machine | 44.1 | 19 | 14 | 1974 †: Bertha Rogers No. 1-27 (Lone Star Producing, Washita County, Oklahoma… | low | Wikipedia only | Charles Willard Diffin, *Two Thousand Miles Below* (1932) | **not checked** |
| Compact portable nuclear power unit | 44.0 | 25 | 0 | 1960-10: PM-2A at Camp Century, Greenland, powered and heated the camp from Oc… | medium | contemporary | Sewell Peaslee Wright, *The God in the Box* (1931) | **not checked** |
| Thinning atmosphere | 42.9 | 16 | 17 | 1989 †: Phobos 2's ion instrument measured oxygen and other ions escaping fro… | low | contemporary | Jules Verne, *Off on a Comet! a Journey Through…* (1877) | **not checked** |
| Portable movie and video recorder | 42.7 | 24 | 2 | 1967: Sony's Portapak (DV-2400) battery video camera and recorder, carried… | low | Wikipedia only | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Central computer directing many robots | 42.4 | 18 | 0 | 1974: Volvo Kalmar assembly plant in regular production use of its fleet of… | low | contemporary | F. L. Wallace, *The Music Master* (1953) | **not checked** |
| Artificial rainmaking | 42.2 | 14 | 14 | 1948: Irving Krick began offering commercial cloud seeding and ran airborne… | low | Wikipedia only | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | **not checked** |
| Orbital launch rocket | 40.9 | 30 | 1 | 1957-10-04: The Soviet Union launched Sputnik 1 into Earth orbit on a modified R-… | high | contemporary | Jack Williamson, *The Alien Intelligence* (1929) | **not checked** |
| Robot copy of a particular person | 40.0 | 24 | 1 | 1964 †: Disney's Audio-Animatronic Abraham Lincoln shown in 'Great Moments wi… | low | Wikipedia only | Charles Hannan, *The Electric Man* (1910) | **not checked** |
| Poison gas weapon | 39.5 | 15 | 0 | 1915-04-22: Germany released chlorine from cylinders against French and Algerian… | medium | contemporary | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Nuclear fission power plant | 39.2 | 36 | 0 | 1954-06: The Obninsk plant in the Soviet Union was connected to the power grid… | medium | Wikipedia only | Stanton A. Coblentz, *The Sunken World* (1928) | **not checked** |
| Homing guided missile | 39.2 | 17 | 4 | 1943-08-25: Same event: Hs 293 operational use, sinking HMS Egret on 27 August 19… | medium | Wikipedia only | Ray Cummings, *The Man Who Mastered Time* (1924) | **not checked** |
| Military airship | 38.8 | 18 | 0 | 1912-03-10: Italian dirigibles used for military purposes in the Italo-Turkish Wa… | medium | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Companion or sex robot | 38.2 | 15 | 12 | 1998-10-02: Furby went on general sale in the United States (launched 2 October 1… | low | contemporary | H. L. Gold, *Never Come Midnight* (1958) | **not checked** |
| Acceleration couches and suits | 38.1 | 21 | 9 | 1942: Franks g-suits were first used operationally in 1942 by 807 Squadron… | medium | Wikipedia only | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| Supersonic passenger aircraft | 38.0 | 14 | 6 | 1976-01-21: Concorde entered passenger service with Air France (Paris-Rio route)… | medium | Wikipedia only | Edmond Hamilton, *Cities in the Air* (1929) | **not checked** |
| Density and hazards of the asteroid belt | 37.9 | 20 | 3 | 1973-02 †: Pioneer 10 traversed the asteroid belt (1972-07-15 to 1973-02-15) wit… | medium | contemporary | Raymond Z. Gallun, *Asteroid of Fear* (1951) | **not checked** |
| Industrial robot | 37.7 | 26 | 2 | 1961: First Unimate installed at GM Inland Fisher Guide plant, Ewing Townsh… | high | Wikipedia only | Edward Bulwer Lytton, *The Coming Race* (1871) | **not checked** |
| Change in Earth's rotation | 37.1 | 19 | 6 | 1939 †: Harold Spencer Jones showed that fluctuations in the apparent longitu… | low | contemporary | H. G. Wells, *The Time Machine* (1894) | **not checked** |
| Robot nanny and child carer | 37.1 | 14 | 16 | 2005-03 †: NEC publicly demonstrated the 'Childcare Robot PaPeRo' prototype, des… | low | contemporary | F. L. Wallace, *The Impossible Voyage Home* (1954) | **not checked** |
| Anti-eavesdropping device | 35.9 | 19 | 0 | 1952: At the US ambassador's residence in Moscow, State Department technici… | low | Wikipedia only | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Neural implant and cyborg augmentation | 35.9 | 18 | 2 | 1977-12: Hochmair's multichannel cochlear implant was first implanted in a per… | low | Wikipedia only | Michael Shaara, *Wainer* (1954) | **not checked** |
| Powered exoskeleton | 35.7 | 13 | 14 | 2004 †: UC Berkeley's BLEEX (DARPA-funded, Kazerooni's lab) was shown at the… | low | Wikipedia only | E. E. Smith, *Children of the Lens* (1947) | **not checked** |
| Unattended automatic power plant | 35.7 | 16 | 0 | 1966: The same Fairway Rock radioisotope generator powered the Navy's ocean… | low | contemporary | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Self-adjusting furniture | 35.2 | 25 | 6 | 1954: Family Fujiryoki in Japan began selling robotic massage chairs, in wh… | low | Wikipedia only | S. Fowler Wright, *The World Below* (1925) | **not checked** |
| Central citizen database and mass surve… | 35.0 | 20 | 4 | 1964: Statistics Norway established a computerized central population regis… | low | reference | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Robotic and automated surgery | 34.8 | 15 | 5 | 1985: A Puma robot arm positioned a needle for a CT-guided brain biopsy on… | low | Wikipedia only | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | **not checked** |
| Home air conditioning and climate contr… | 34.8 | 15 | 5 | 1929: Frigidaire's room cooler went on the market for home use. | low | reference | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Drug that removes will or emotion | 34.4 | 19 | 11 | 1952: Chlorpromazine was used to calm and manage patients in French psychia… | low | Wikipedia only | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Air-to-air combat | 34.1 | 19 | 0 | 1914-10-05: Sgt. Joseph Frantz and gunner Louis Quenault in a Voisin biplane with… | medium | contemporary | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Powerful microscope | 33.3 | 13 | 15 | 1939: Siemens began producing commercial electron microscopes (one source s… | low | Wikipedia only | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Lab-grown whole organs | 33.2 | 12 | 13 | 2005-06: The first engineered vaginal organ was implanted in a patient with va… | low | reference | Raymond Z. Gallun, *Dawn of the Demigods* (1954) | **not checked** |
| Electrostatic charging of spacecraft | 33.2 | 11 | 1 | 1969 †: ATS-5 (launched 1969) at geosynchronous orbit showed spacecraft charg… | low | reference | George O. Smith, *Recoil* (1943) | **not checked** |
| Super-long-range gun | 32.7 | 18 | 4 | 1918-03-23: The Paris Gun's first shell hit Paris, killing 15 on the first day. | medium | Wikipedia only | Michel Verne; Jules Verne, *In the Year 2889* (1889) | **not checked** |
| Teleoperated robot and telepresence | 32.5 | 22 | 1 | 1954: Modified Goertz master-slave manipulator (CRL Model 8) went into comm… | low | Wikipedia only | (text), *Astounding Stories, March, 1931* (1931) | **not checked** |
| Live television from space | 32.5 | 21 | 0 | 1962-07-23: Telstar 1 relayed the first publicly available live transatlantic tel… | medium | Wikipedia only | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Radar | 32.2 | 16 | 2 | 1938-08: The first five Chain Home radar stations were declared operational in… | medium | Wikipedia only | Hugo Gernsback, *Ralph 124C 41+* (1911) | **not checked** |
| Invisible craft | 32.0 | 16 | 9 | 1983-10: Lockheed F-117 Nighthawk reached initial operating capability, the fi… | low | Wikipedia only | Fritz Leiber, *The Green Millennium* (1953) | **not checked** |
| Emotion-recognition machine | 32.0 | 13 | 2 | 1993 †: Kobayashi and Hara (Tokyo University of Science) built a face robot w… | low | reference | Larry Eisenberg, *The Fastest Draw* (1963) | **not checked** |
| Machine-generated writing | 31.9 | 11 | 5 | 1990: Environment Canada used FoG, a system that generated weather forecast… | low | contemporary | Boyd Ellanby, *What Do You Read?* (1953) | **not checked** |
| Aircraft and spacecraft autopilot | 31.6 | 14 | 0 | 1922: Standard Oil tanker J.A. Moffet became the first ship to use an autop… | low | Wikipedia only | Charles Willing Beale, *The Secret of the Earth* (1899) | **not checked** |
| Personal helicopter | 31.6 | 20 | 0 | 1953-02-21 †: The Brantly B-2, a two-seat light helicopter designed for private buy… | low | Wikipedia only | Ray Cummings, *Tarrano the Conqueror* (1925) | **not checked** |
| Machine-readable identity and access ca… | 31.2 | 18 | 0 | 1961: Line Material Industries (McGraw-Edison) used the IBM 357 data collec… | low | contemporary | H. Beam Piper, *Police Operation* (1948) | **not checked** |
| Laser or heat-beam weapon | 31.1 | 10 | 10 | 2014-12: The US Navy declared the 30 kW Laser Weapon System aboard USS Ponce i… | medium | contemporary | Morgan Robertson, *Futility (The Wreck of the Titan)* (1898) | **not checked** |
| Emotion removal | 31.1 | 18 | 6 | 1961: Same event: amygdalotomy was used clinically on patients from its dev… | low | Wikipedia only | Marie Corelli, *The Young Diana* (1918) | **not checked** |
| Teaching machine and computer-assisted… | 30.7 | 21 | 3 | 1960: PLATO I began operating on the University of Illinois ILLIAC I comput… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Spacecraft viewport and observation win… | 30.0 | 12 | 1 | 1961-04-12: Yuri Gagarin looked out of Vostok 1's window at the Earth during the… | low | Wikipedia only | Otis Adelbert Kline, *Maza of the Moon* (1929) | **not checked** |
| Powered prosthetic limbs | 29.6 | 17 | 1 | 1960: Kobrinski's Russian myoelectric hand presented at the 1960 Moscow IFA… | medium | reference | Clare Winger Harris, *The Artificial Man* (1929) | **not checked** |
| Remote-detonated bomb | 29.5 | 15 | 3 | 1941: Soviet engineers under Ilya Starinov planted R-10 radio mines in Khar… | medium | Wikipedia only | George Allan England, *The Flying Legion* (1919) | **not checked** |
| Planetary protection and contamination… | 29.5 | 17 | 0 | 1960-12: NASA adopted spacecraft sterilization and decontamination as national… | low | contemporary | E. E. Smith, *Galactic Patrol* (1937) | **not checked** |
| Biological energy harvesting | 28.9 | 10 | 11 | 2008 †: Strik and colleagues (Wageningen) generated electricity from living r… | low | contemporary | Ray Cummings, *Beyond the Stars* (1928) | **not checked** |
| Planets in double and multiple star sys… | 28.9 | 8 | 5 | 1996 †: A planet was found orbiting 16 Cygni B, one of a pair of Sun-like sta… | low | contemporary | Nelson S. Bond, *Phantom Out of Time* (1943) | **not checked** |
| Geothermal and volcanic power | 28.5 | 11 | 0 | 1911: The world's first commercial geothermal power station was built at La… | medium | Wikipedia only | Ralph Centennius, *The Dominion in 1983* (1883) | **not checked** |
| Nuclear-powered ship or submarine | 28.5 | 13 | 1 | 1955-01-17: USS Nautilus left her pier at Groton, Connecticut and signaled 'Under… | high | contemporary | Stanton A. Coblentz, *The Sunken World* (1928) | **not checked** |
| New recreational and mood drugs | 28.4 | 15 | 4 | 1936: Benzedrine sulfate tablets reached the market, and within a couple of… | low | contemporary | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | **not checked** |
| Robot memory wipe | 28.2 | 10 | 6 | 1998-10: Furby owners could clear a Furby's memory from the first retail launc… | low | contemporary | Mari Wolf, *Robots of the World! Arise!* (1952) | **not checked** |
| Passenger airship service | 28.2 | 15 | 1 | 1910-06: DELAG began commercial Zeppelin passenger service with LZ 7 Deutschla… | low | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Robot vacuum cleaner and lawn mower | 28.1 | 12 | 0 | 1969: MowBot went on sale to the public in 1969 (about $800), first commerc… | medium | contemporary | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Ground control of spaceflight | 27.8 | 21 | 0 | 1959-10-04 †: Luna 3 photographed the Moon's far side and the Soviet ground station… | low | Wikipedia only | Edgar Rice Burroughs, *The Moon Maid* (1923) | **not checked** |
| Temperature and contents of interplanet… | 27.8 | 9 | 6 | 1962 †: Mariner 2 measured the solar wind's speed and temperature in interpla… | low | contemporary | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| Society's dependence on fallible comput… | 27.7 | 12 | 11 | 1999: Same event: the prosecutions started in 1999. | low | Wikipedia only | E. G. Von Wald, *Easy Does It* (1955) | **not checked** |
| Other stars with many planets | 27.6 | 9 | 9 | 2017-02 †: TRAPPIST-1 was found (Gillon et al., Nature, 22 Feb 2017) to have sev… | medium | contemporary | John Jacob Astor, *A Journey in Other Worlds* (1894) | **not checked** |
| Sahara greening by irrigation or planti… | 27.5 | 12 | 6 | 1969 †: Libya's Kufra scheme, with Occidental Petroleum, sprinkled irrigation… | low | contemporary | Frank Koester, *Under the Desert Stars* (1923) | **not checked** |
| Cosmic catastrophe changing the Earth | 27.4 | 13 | 15 | 1980-06 †: Alvarez, Alvarez, Asaro and Michel reported iridium spikes in Italy,… | low | contemporary | Garrett Putman Serviss, *The Second Deluge* (1911) | **not checked** |
| Artificially induced atomic disintegrat… | 27.4 | 13 | 2 | 1945-08-06: The United States dropped a uranium fission bomb ('Little Boy') on Hi… | medium | contemporary | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Electrified barrier | 27.2 | 11 | 0 | 1905: Russian army improvised electric fences at Port Arthur | low | Wikipedia only | Luis Senarens, *Frank Reade and His Steam Horse* (1876) | **not checked** |
| Hovercraft | 27.1 | 18 | 4 | 1962: Vickers-Armstrongs VA-3 started a small-scale ferry service. | medium | Wikipedia only | George Allan England, *The Flying Legion* (1919) | **not checked** |
| Robot bomb and cruise missile | 26.8 | 12 | 6 | 1944-06-13: Germany launched V-1 flying bombs against London one week after D-Day. | high | contemporary | Frank R. Stockton, *The Great War Syndicate* (1888) | **not checked** |
| Scheduled passenger air service | 26.5 | 15 | 0 | 1914-01-01: Same service; it ran from January to May 1914 at $5 per one-way fligh… | medium | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Ultra-strong thin cable or fiber | 26.3 | 10 | 4 | 1971: DuPont introduced Kevlar, first used commercially in the early 1970s… | low | Wikipedia only | R. Elton Smile, *The Manatitlans* (1877) | **not checked** |
| Storm and tornado control | 26.2 | 10 | 15 | 2021 †: A terawatt laser on the Santis summit in Switzerland guided an upward… | medium | contemporary | Gardner F. Fox, *Engines of the Gods* (1946) | **not checked** |
| Synthetic diamond | 26.1 | 9 | 11 | 1957: General Electric's Detroit pilot plant produced man-made industrial d… | medium | contemporary | H. G. Wells, *The Door in the Wall, and Other St…* (1911) | **not checked** |
| Autonomous farm robot | 26.0 | 11 | 3 | 1983 †: Prof. N. Kawamura (Kyoto University) presented an intelligent tomato-… | medium | contemporary | Edmond Hamilton, *Battle for the Stars* (1956) | **not checked** |
| Gas-turbine car | 26.0 | 16 | 0 | 1963-10: Chrysler lent 50 turbine coupes to 203 ordinary drivers in 133 US cit… | medium | Wikipedia only | Fritz Leiber, *Coming Attraction* (1950) | **not checked** |
| Checkpoint weapon and contraband scanner | 25.9 | 10 | 0 | 1970-07-17: New Orleans International airport used magnetometers on departing pas… | medium | reference | Alfred Coppel, *The Last Two Alive!* (1950) | **not checked** |
| Eradication of a named infectious disea… | 25.9 | 10 | 5 | 1980-05: On 8 May 1980 the World Health Assembly declared the world free of sm… | high | contemporary | Mary Griffith, *Camperdown* (1836) | **not checked** |
| Polar motor sledge | 25.4 | 8 | 1 | 1934: A tractor party reached Byrd's Advance Base over the ice shelf in 193… | low | Wikipedia only | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Biological computer | 25.4 | 11 | 6 | 1994 †: Leonard Adleman (USC) solved a seven-node directed Hamiltonian path p… | medium | Wikipedia only | Robertson Osborne, *Action on Azura* (1949) | **not checked** |
| Seeing the far side of the Moon | 25.3 | 11 | 13 | 1959-10-07 †: The Soviet probe Luna 3 photographed the Moon's far side on 7 October… | high | contemporary | Charles Napier Richards, *Atalanta* (1900) | **not checked** |
| Automated scientific discovery | 25.3 | 11 | 13 | 2009 †: Robot Scientist 'Adam' (Aberystwyth/Cambridge, Ross King) autonomousl… | low | Wikipedia only | John W. Campbell Jr, *When the Atoms Failed* (1930) | **not checked** |
| Touchscreen and gesture interface | 25.3 | 9 | 1 | 1972: PLATO IV terminals at the University of Illinois (1972) had a built-i… | medium | contemporary | Robert Wilson, *Vandals of the Void* (1945) | **not checked** |
| Air travel replaces sea travel | 25.3 | 8 | 5 | 1957: Summer 1957: as many passengers crossed the North Atlantic by airline… | low | Wikipedia only | Murray Leinster, *The Silver Menace* (1919) | **not checked** |
| Power systems for colonies | 25.2 | 15 | 0 | 1969-11-19: The Apollo 12 SNAP-27 generator powered the ALSEP experiments on the… | low | Wikipedia only | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Crewed orbital spaceflight | 25.2 | 21 | 0 | 1961-04-12 †: Yuri Gagarin made one orbit of the Earth in Vostok 1, launched from B… | high | contemporary | Algis Budrys, *Desire No More* (1954) | **not checked** |
| Automated face recognition | 25.1 | 8 | 3 | 1994: By 1994 facial-recognition biometric products had reached the marketp… | low | contemporary | Charles E. Fritch, *Breathes There a Man* (1953) | **not checked** |
| Hydrofoil or skimming craft | 25.0 | 11 | 12 | 1952: Supramar launched the first commercial hydrofoil, PT10 Freccia d'Oro,… | medium | Wikipedia only | Rudyard Kipling, *With the Night Mail* (1905) | **not checked** |
| Public address system | 24.8 | 13 | 0 | 1912-08: Same Chicago water carnival installation announced races and speeches… | low | Wikipedia only | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Broadcast hijacking | 24.5 | 11 | 1 | 1966: Same event as above: the hoax broadcast actually reached listeners in… | low | Wikipedia only | Ray Cummings, *Tarrano the Conqueror* (1925) | **not checked** |
| Steam power abandoned | 24.5 | 9 | 3 | 1925: The Central Railroad of New Jersey put an ALCO diesel-electric boxcab… | low | Wikipedia only | T. Baron Russell, *A Hundred Years Hence (The Expecta…* (1905) | **not checked** |
| Stratospheric passenger flight | 24.4 | 9 | 0 | 1976-01-21: Concorde entered passenger service with Air France and British Airway… | medium | Wikipedia only | Albert dePina, *The Star Guardsman* (1943) | **not checked** |
| Stealth against radar and sonar | 24.4 | 15 | 1 | 1941: U-67 became the first operational U-boat fitted with the Alberich coa… | low | Wikipedia only | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Anti-missile defense | 23.9 | 13 | 0 | 1944-06-14: RAF fighters, radar-cued, intercepted and destroyed German V-1 flying… | medium | Wikipedia only | Ray Cummings, *Tarrano the Conqueror* (1925) | **not checked** |
| Large public video screen | 23.9 | 10 | 0 | 1928-11: On election night, 6 Nov 1928, the New York Times flashed returns on… | medium | contemporary | Will N. Harben, *The Land of the Changing Sun* (1894) | **not checked** |
| Multi-planet timekeeping | 23.4 | 8 | 9 | 2004-01: Members of NASA's Mars Exploration Rover team wore watches calibrated… | medium | contemporary | T. D. Hamm, *Native Son* (1953) | **not checked** |
| Flying platform | 23.3 | 13 | 0 | 1954-11-22 †: The de Lackner HZ-1 Aerocycle made its first tethered flight in the U… | low | Wikipedia only | Ray Cummings, *Tarrano the Conqueror* (1925) | **not checked** |
| Robot manufacturing industry | 23.2 | 15 | 0 | 1961: Unimation, called the world's first robotics company, shipped its fir… | medium | Wikipedia only | Nelson S. Bond, *The Madness of Lancelot Biggs* (1940) | **not checked** |
| Mathematical science of society | 23.1 | 12 | 1 | 1971 †: Jay Forrester published World Dynamics, a system-dynamics model of wo… | low | Wikipedia only | Dick Hetschel, *Is That You Xeluchli?* (1952) | **not checked** |
| Cutting and welding torch for use in sp… | 23.1 | 8 | 0 | 1969-10-16 †: On Soyuz 6, Kubasov ran the automatic Vulkan apparatus in the depress… | medium | reference | Edmond Hamilton, *The Universe Wreckers* (1930) | **not checked** |
| Automatic sensor door | 22.9 | 12 | 1 | 1931: The Stanley optical door was installed in a West Haven, Connecticut r… | medium | Wikipedia only | Charles Dixon, *Fifteen Hundred Miles an Hour* (1895) | **not checked** |
| Color-changing camouflage skin | 22.8 | 7 | 9 | 2012-08 †: August 2012, Harvard (Morin, Whitesides et al., Science): soft robots… | low | contemporary | Paul W. Fairman; Stephen…, *Quest of the Golden Ape* (1957) | **not checked** |
| Computerized courts and legal decisions | 22.7 | 13 | 1 | 1973-04-02: Mead Data Central publicly launched LEXIS in New York as a commercial… | low | Wikipedia only | Robert Silverberg; Randa…, *The Inquisitor* (1956) | **not checked** |
| Airborne warship | 22.6 | 13 | 0 | 1912-03-05: Italian army airships P.2 and P.3 flew their first war mission over Z… | low | reference | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Nerve-controlled prosthetic | 22.6 | 7 | 9 | 2004 †: Todd Kuiken's team (Rehabilitation Institute of Chicago) published a… | low | contemporary | Randall Garrett; Robert…, *Bleekman's Planet* (1957) | **not checked** |
| Reviving extinct species | 22.6 | 8 | 9 | 2003-07 †: A cloned Pyrenean ibex (bucardo), made from cryopreserved skin cells… | medium | Wikipedia only | H. G. Wells, *The Country of the Blind, and Othe…* (1911) | **not checked** |
| Portable personal video viewer | 22.5 | 9 | 2 | 1988: Sony GV-8 Video Walkman, a portable 8 mm video player with built-in L… | low | reference | Walter J. Sheldon, *Brink of Madness* (1953) | **not checked** |
| Faster-growing and engineered crops | 22.5 | 11 | 8 | 1936 †: Gustafson (US) induced seedless (parthenocarpic) fruit on tomatoes, p… | low | contemporary | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Artificial soil creation | 22.2 | 9 | 5 | 1971 †: Chicago's Metropolitan Sanitary District, with University of Illinois… | low | contemporary | Garrett Putman Serviss, *The Second Deluge* (1911) | **not checked** |
| Robotic exploration probe | 22.1 | 16 | 0 | 1959-01 †: Luna 1 (USSR), launched 2 Jan 1959, left Earth orbit, passed the Moon… | medium | Wikipedia only | Isabel Hornibrook, *Pemrose Lorry, Camp Fire Girl* (1921) | **not checked** |
| Genetic prediction of traits | 22.1 | 17 | 3 | 1963: Newborn PKU screening started as a public-health program in the Unite… | low | Wikipedia only | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Seas of non-water liquids on other worl… | 22.0 | 7 | 7 | 2006-07 †: Cassini radar on 22 July 2006 imaged smooth dark regions near Titan's… | medium | contemporary | E. E. Smith; Lee Hawkins…, *The Skylark of Space* (1928) | **not checked** |
| Wearable computer and personal digital… | 22.0 | 8 | 0 | 1984: Psion Organiser sold in the UK as a pocket diary and database compute… | low | Wikipedia only | Robert Abernathy, *The Laugh* (1956) | **not checked** |
| Transparent vehicle body | 21.9 | 10 | 1 | 1939 †: General Motors showed a Pontiac with a body of clear Plexiglas (the '… | low | contemporary | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Computer crime detection and predictive… | 21.6 | 15 | 0 | 1967: The FBI's National Crime Information Center, a computerized national… | low | Wikipedia only | Randall Garrett; Laurenc…, *The Impossibles* (1960) | **not checked** |
| Transparent living bodies | 21.5 | 6 | 8 | 2008-02 †: Richard White, Leonard Zon and colleagues (Children's Hospital Boston… | low | contemporary | Alex James, *The Shining Cow* (1957) | **not checked** |
| Camera screen in place of window or mir… | 21.2 | 6 | 3 | 1987: The 1987 Toyota Crown, sold only in Japan, was the first production c… | medium | Wikipedia only | Harry Bates, *Seed of the Arctic Ice* (1932) | **not checked** |
| Piped background music | 21.0 | 8 | 3 | 1936-03: Muzak began its paid wired music service to New York hotels, restaura… | medium | contemporary | Will N. Harben, *The Land of the Changing Sun* (1894) | **not checked** |
| Scent broadcasting | 20.9 | 11 | 2 | 1959-12-09: AromaRama released Behind the Great Wall in New York with more than 1… | medium | Wikipedia only | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Conversational natural-language computer | 20.8 | 13 | 0 | 1966 †: Joseph Weizenbaum's ELIZA, developed at MIT 1964-67 and first publish… | medium | Wikipedia only | Jim Harmon, *The Upside-Down Captain* (1960) | **not checked** |
| Space tourism and orbital resorts | 20.7 | 7 | 7 | 2001-04-28: Dennis Tito paid Russia about $20 million to fly on Soyuz TM-32, laun… | high | contemporary | Raymond Z. Gallun, *The Planet Strappers* (1961) | **not checked** |
| Spacecraft telemetry link | 20.6 | 12 | 2 | 1958-01-31: Explorer 1 returned cosmic-ray measurements that led to the Van Allen… | low | Wikipedia only | Frank R. Stockton, *The Great Stone of Sardis* (1897) | **not checked** |
| Remotely controlled uncrewed spacecraft | 20.4 | 11 | 0 | 1966-03-16 †: Gemini 8 docked with the uncrewed Agena target vehicle, which was com… | low | Wikipedia only | Robert Sheckley, *The Leech* (1952) | **not checked** |
| Zone that disables instruments, radio o… | 20.1 | 11 | 1 | 1958-02 †: Explorer 1's Geiger counter read zero when passing through intense tr… | low | contemporary | Rudyard Kipling, *Actions and Reactions* (1909) | **not checked** |
| Radioactive fallout wasteland | 20.0 | 15 | 3 | 1954-03: The 1 March 1954 Castle Bravo H-bomb test dropped fallout on Rongelap… | low | contemporary | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Pressurized aircraft cabin | 19.9 | 10 | 2 | 1940-07: Boeing 307 Stratoliner entered TWA revenue service in July 1940, the… | medium | Wikipedia only | Luis Senarens, *The Transient Lake* (1896) | **not checked** |
| Military strategy computer | 19.8 | 14 | 0 | 1958: SAGE air-defence computers (IBM AN/FSQ-7) became operational in the l… | low | Wikipedia only | Stanley G. Weinbaum, *The Worlds of If* (1935) | **not checked** |
| Giant multi-engine airliner | 19.6 | 12 | 0 | 1930-05-02: Deutsche Luft Hansa put the four-engined Junkers G 38 into scheduled… | low | Wikipedia only | Guy Thorne, *The Air Pirate* (1919) | **not checked** |
| Sunken lost continent | 19.6 | 7 | 8 | 2017-02 †: A team of eleven geologists (Mortimer et al.) concluded in GSA Today… | low | contemporary | M. P. Shiel, *The Purple Cloud* (1901) | **not checked** |
| Artificial sound in silent vehicles | 19.6 | 5 | 5 | 2009 †: Lotus Engineering and Harman Becker began developing a system that si… | low | Wikipedia only | Murray Leinster, *Pariah Planet* (1961) | **not checked** |
| Anti-aircraft gun | 19.5 | 10 | 0 | 1915-09-30: Serbian private Radoje Ljutovac shot down an Austro-Hungarian aircraf… | medium | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Radio and beam guidance for landing | 19.5 | 10 | 0 | 1934: Lorenz blind-landing beam (developed from 1932 at Berlin-Tempelhof) a… | low | Wikipedia only | Rudyard Kipling, *With the Night Mail* (1905) | **not checked** |
| Electronic book reader | 19.3 | 8 | 2 | 1990-07: The same Sony Data Discman DD-1 went on sale in Japan in July 1990 as… | medium | contemporary | Murray Leinster, *Planet Explorer* (1957) | **not checked** |
| Innate sense of direction | 19.3 | 6 | 4 | 1958 †: A. C. Perdeck displaced more than 11,000 migrating starlings from the… | low | contemporary | Edgar Rice Burroughs, *Pellucidar* (1915) | **not checked** |
| Interior and surface of the giant plane… | 19.1 | 7 | 4 | 1966 †: Frank J. Low measured Jupiter's infrared emission with a germanium bo… | low | contemporary | Roman Frederick Starzl;…, *The Metal Moon* (1931) | **not checked** |
| Artificial heart | 19.0 | 9 | 0 | 1963: Domingo Liotta and E. Stanley Crawford implanted the first left ventr… | low | Wikipedia only | Clare Winger Harris, *The Artificial Man* (1929) | **not checked** |
| All matter built from one primitive sub… | 18.9 | 7 | 5 | 1968 †: Deep inelastic electron-proton scattering at SLAC (SLAC-MIT group) in… | medium | contemporary | Camille Flammarion, *Urania* (1889) | **not checked** |
| Plastic buildings | 18.8 | 8 | 0 | 1968: Matti Suuronen's Futuro, a fiberglass-reinforced polyester house desi… | low | Wikipedia only | John Murray Reynolds, *Goddess of the Moon* (1940) | **not checked** |
| New contraception | 18.6 | 12 | 4 | 1960: 1960, United States: the FDA approved the first oral contraceptive, E… | medium | Wikipedia only | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Stored air, water and food for spacefli… | 18.5 | 7 | 4 | 1961-04-12: Vostok 1: Gagarin flew with stored food and oxygen to survive up to t… | medium | Wikipedia only | William Wallace Cook, *Adrift in the Unknown* (1904) | **not checked** |
| Decontamination of radioactive or poiso… | 18.1 | 7 | 2 | 1966: After a B-52 crash at Palomares, Spain (Jan 1966), US and Spanish tea… | low | reference | H. G. Wells, *The Food of the Gods and How It Ca…* (1903) | **not checked** |
| Underground water passages linking seas | 18.0 | 6 | 7 | 1963 †: Maurin and Zötl poured dye into the Argostoli sinkholes (katavothres)… | low | reference | Edgar Rice Burroughs, *Out of Time's Abyss* (1918) | **not checked** |
| Automated eavesdropping | 17.9 | 7 | 1 | 1971: The NSA/GCHQ ECHELON network was formally established to intercept sa… | low | Wikipedia only | Evgenii Ivanovich Zamiat…, *We* (1921) | **not checked** |
| Mass military air force | 17.9 | 11 | 0 | 1918-04: The Royal Air Force formed on 1 April 1918 from the RFC and RNAS as t… | low | Wikipedia only | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Improvised refining of crude oil into f… | 17.9 | 5 | 4 | 1969: Biafra, cut off by the Nigerian blockade during the civil war, ran do… | low | contemporary | George Allan England, *Darkness and Dawn* (1912) | **not checked** |
| Lab-grown skin and simple tissue | 17.8 | 8 | 1 | 1981: The same 1981 Lancet report treated burn patients with cultured autol… | medium | contemporary | H. Beam Piper, *Four-Day Planet* (1961) | **not checked** |
| Lunar volcanism | 17.8 | 7 | 6 | 1967-09 †: Surveyor 5 soft-landed in Mare Tranquillitatis on 1967-09-11 and its… | medium | contemporary | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| Anti-satellite weapon | 17.8 | 7 | 0 | 1973-02: The Soviet IS co-orbital anti-satellite system was declared operation… | low | Wikipedia only | Kris Neville, *Earth Alert!* (1953) | **not checked** |
| Gravity-wave communication | 17.6 | 6 | 7 | 2025-11-20 †: Groszek, Woffinden, Harvey, White and Davis (Univ. of Queensland) pos… | low | contemporary | George O. Smith, *The Fixer* (1945) | **not checked** |
| Retrorocket braking | 17.6 | 6 | 1 | 1971-11-14: The same braking burn put Mariner 9 into orbit for the Mars mapping m… | medium | contemporary | Donald A. Wollheim, *The Planet That Time Forgot* (1940) | **not checked** |
| Interoceanic ship canal | 17.5 | 6 | 0 | 1914-08-15: Canal opened to commercial shipping with its first full transit. | medium | Wikipedia only | William Richard Bradshaw, *The Goddess of Atvatabar* (1892) | **not checked** |
| Personalized medicine | 17.4 | 6 | 4 | 1998-09: Trastuzumab (Herceptin) approved by the FDA in September 1998 for bre… | low | Wikipedia only | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Artificial scenery and illusion rooms | 17.3 | 9 | 1 | 1923: Same: the Houston theatre operated as a paying cinema/vaudeville hous… | low | Wikipedia only | Will N. Harben, *The Land of the Changing Sun* (1894) | **not checked** |
| Orbital debris | 17.1 | 7 | 0 | 1983-06 †: On Space Shuttle Challenger's STS-7 flight (18-24 June 1983) a fleck… | low | Wikipedia only | William Carroll, *Solomon's Orbit* (1962) | **not checked** |
| Undersea habitat or city | 17.1 | 8 | 3 | 1970: Hydrolab, built in 1966, was used as a research station from 1970 wit… | low | Wikipedia only | Frederik Pohl; C. M. Kor…, *The Engineer* (1956) | **not checked** |
| Color photography | 17.1 | 8 | 0 | 1907: The Lumiere Autochrome plate, a single-plate color process using dyed… | medium | contemporary | Frances Power Cobbe, *The Age of Science* (1877) | **not checked** |
| Controlled-access highway | 17.1 | 8 | 0 | 1921-09: AVUS in Berlin opened on 24 September 1921 as a road for fast motor t… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Implanted communication device | 17.0 | 11 | 0 | 1957 †: Andre Djourno and Charles Eyries (France) invented and implanted the… | low | Wikipedia only | Arthur J. Burks, *The Mind Master* (1932) | **not checked** |
| Falling oceans exposing seabed | 16.9 | 6 | 19 | 1970 †: Deep Sea Drilling Project Leg 13 aboard the Glomar Challenger (co-chi… | low | Wikipedia only | Jules Verne, *Topsy-Turvy* (1889) | **not checked** |
| Real-time computerized situation display | 16.9 | 10 | 0 | 1958-06: The SAGE New York Air Defense Sector, with its AN/FSQ-7 computer and… | medium | contemporary | Edmond Hamilton, *Cities in the Air* (1929) | **not checked** |
| Robot pet or animal | 16.8 | 10 | 1 | 1962: Ideal Toy Company sold Gaylord, a battery-powered toy dog steered by… | low | Wikipedia only | Rog Phillips, *One for the Robot—Two for the Same* (1950) | **not checked** |
| Rocket thrust in a vacuum | 16.8 | 6 | 5 | 1915 †: Robert Goddard at Clark University tested a rocket in a vacuum and sh… | medium | reference | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| Machine vision | 16.6 | 12 | 0 | 1963 †: Larry Roberts's MIT PhD thesis 'Machine Perception of Three-Dimension… | low | Wikipedia only | John W. Campbell Jr, *The Metal Horde* (1930) | **not checked** |
| Peaceful nuclear explosive | 16.6 | 8 | 1 | 1966-09-30: The Soviet Union detonated a 30 kt nuclear device in a borehole besid… | low | Wikipedia only | H. Beam Piper, *Uller Uprising* (1952) | **not checked** |
| Covert listening device | 16.6 | 7 | 1 | 1912: By early 1912 the Dictograph was in use by detective agencies (Burns,… | low | contemporary | of Samosata Lucian; Char…, *Lucian's True History* (1780) | **not checked** |
| Atomic-powered furnaces and heating | 16.4 | 7 | 0 | 1964: Agesta nuclear plant near Stockholm began delivering reactor heat as… | medium | reference | Fletcher Pratt; Laurence…, *Expedition to Pluto* (1939) | **not checked** |
| Hospital and nursing robot | 16.4 | 7 | 1 | 1989: The first HelpMate prototype was installed in a hospital in 1989; com… | low | reference | Harry Harrison, *The Stainless Steel Rat* (1961) | **not checked** |
| Implanted body monitor and regulator | 16.2 | 15 | 2 | 1960-04: Wilson Greatbatch's implantable pacemakers (with Chardack) entered us… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Recreation and sport in space | 16.0 | 11 | 1 | 1970-06 †: Soyuz 9 cosmonauts Nikolayev and Sevastyanov played a consultation ch… | low | Wikipedia only | Fritz Leiber, *The Green Millennium* (1953) | **not checked** |
| Earthquake prediction | 16.0 | 6 | 6 | 1975-02-04: Chinese authorities evacuated Haicheng, Liaoning, hours before the ma… | medium | contemporary | C. J. Cutcliffe Hyne, *The Lost Continent* (1899) | **not checked** |
| Personal electric mobility device | 16.0 | 6 | 0 | 1919 †: Levitt Luzern Custer built an electric wheelchair at the Dayton Soldi… | low | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Repair and inspection of spacecraft in… | 15.9 | 7 | 0 | 1973-05: Skylab 2: after launch damage, the crew deployed a sunshade and later… | medium | contemporary | Alan Edward Nourse, *Derelict* (1953) | **not checked** |
| Metal cloth clothing | 15.8 | 6 | 1 | 1966-06: Same event: the Chromel-R layer was worn for a real spacewalk test of… | low | Wikipedia only | E. E. Smith; Lee Hawkins…, *The Skylark of Space* (1928) | **not checked** |
| Multi-level city traffic | 15.5 | 6 | 0 | 1926: Chicago opened the double-decked Wacker Drive along the river, with s… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Electronic aids for blind people | 15.5 | 11 | 1 | 1971: Telesensory Systems began making the Optacon, a handheld scanner that… | low | Wikipedia only | Con Blomberg, *Sales Talk* (1959) | **not checked** |
| Computer psychological analysis and the… | 15.4 | 10 | 0 | 1966 †: Weizenbaum's ELIZA/DOCTOR script, a computer program imitating a Roge… | low | Wikipedia only | F. L. Wallace, *Accidental Flight* (1952) | **not checked** |
| Silent firearm | 15.3 | 8 | 0 | 1909-02: The Maxim silencer went on sale to riflemen and hunters in 1909 and w… | medium | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Robotic spy and scout | 15.1 | 6 | 2 | 1974 †: CIA Office of Research and Development flew the Insectothopter, a dra… | low | reference | Raymond Z. Gallun, *The Revolt of the Star Men* (1931) | **not checked** |
| Aircraft radio communication | 15.1 | 10 | 0 | 1914-09-24: Lieutenants D.S. Lewis and B.T. James of No. 4 Squadron, Royal Flying… | medium | reference | Albert Bigelow Paine, *The Great White Way* (1901) | **not checked** |
| Aerobraking | 14.9 | 5 | 1 | 1993-05: Magellan at Venus used repeated atmospheric drag passes from May 1993… | medium | Wikipedia only | Allan Howard, *It's a Small Solar System* (1957) | **not checked** |
| Biocontainment laboratory and suits | 14.8 | 9 | 0 | 1965: By 1965 Fort Detrick described air-tight, negative-pressure rooms for… | low | contemporary | Irving E. Cox Jr., *The Guardians* (1955) | **not checked** |
| Electrification of homes and farms | 14.8 | 10 | 0 | 1898: German estates ran electric farm machinery: the Dahlwitz farm (owner… | low | contemporary | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Automatic machine fault diagnosis | 14.7 | 6 | 2 | 1971-12 †: The US Army's UH-1H AIDAPS Test Bed Program (Hamilton Standard, Corpu… | low | contemporary | Rowland Walker, *The Phantom Airman* (1920) | **not checked** |
| Structure of the Milky Way and universe | 14.6 | 11 | 4 | 1918 †: Harlow Shapley used the distribution of globular clusters to find the… | low | Wikipedia only | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| Immunity to interrogation | 14.5 | 13 | 0 | 1955: After the Korean War POW experience the US military adopted the Code… | low | Wikipedia only | George O. Smith, *Nomad* (1944) | **not checked** |
| Voice projected from nowhere | 14.5 | 5 | 4 | 1998 †: The first modern device projecting sound into air as a narrow beam (t… | low | Wikipedia only | William Conover, *The Soul Eaters* (1944) | **not checked** |
| Compact solid data storage medium | 14.4 | 8 | 1 | 1968-10 †: Bell Telephone Laboratories (F. S. Chen, J. T. LaMacchia, D. B. Frase… | medium | contemporary | Herbert M. Vaughan, *Meleager* (1916) | **not checked** |
| Hydrogen bomb | 14.3 | 15 | 0 | 1954: Emergency-capability thermonuclear bombs (EC 17, EC 24) entered the U… | medium | Wikipedia only | George O. Smith, *Operation Interstellar* (1950) | **not checked** |
| Temperate regions warming toward semitr… | 14.2 | 5 | 6 | 2003: A 2003 American Horticultural Society draft hardiness map, from 1986-… | low | Wikipedia only | George Allan England, *Darkness and Dawn* (1912) | **not checked** |
| Computer matchmaking | 14.1 | 10 | 1 | 1964: Joan Ball's St. James Computer Dating Service (later Com-Pat) in Lond… | low | Wikipedia only | Robert F. Young, *Pilgrims' Project* (1957) | **not checked** |
| Electric car | 13.8 | 11 | 1 | 1897: Bersey electric cabs began carrying fares in London; New York also ra… | medium | Wikipedia only | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Painless or fast-acting lethal poison | 13.8 | 9 | 0 | 1924-02: Gee Jon was executed with hydrogen cyanide gas at Nevada State Prison… | low | Wikipedia only | Edgar Rice Burroughs, *At the Earth's Core* (1914) | **not checked** |
| Inoculation by a living carrier or self… | 13.7 | 5 | 4 | 2000-02 †: Spanish researchers (Barcena and colleagues) showed that a recombinan… | low | contemporary | Sam McClatchie, *The Last Vial* (1960) | **not checked** |
| Sleep-inducing spray or device | 13.7 | 9 | 6 | 1948: By 1948 electric sleep (electronarcosis) was being applied to psychia… | low | contemporary | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Small ferry craft between ships and pla… | 13.7 | 7 | 0 | 1969-07-20: The Lunar Module Eagle carried Armstrong and Aldrin from lunar orbit… | medium | Wikipedia only | Carey Rockwell, *The Space Pioneers* (1953) | **not checked** |
| Distance learning by broadcast | 13.6 | 5 | 0 | 1925-02: Same event: enrolled students, some at distant points, took radio cou… | low | reference | Edward Bellamy, *Equality* (1897) | **not checked** |
| Surfaces and ices of giant-planet moons | 13.5 | 14 | 0 | 1957 †: Gerard Kuiper's ground-based infrared observations revealed water ice… | low | Wikipedia only | Raymond Z. Gallun, *The Raiders of Saturn's Ring* (1941) | **not checked** |
| Computer-run space station | 13.4 | 6 | 0 | 1973-05-25: The first Skylab crew (Skylab 2) arrived 25 May 1973 to a station who… | low | contemporary | Randall Garrett, *Satellite of Death* (1957) | **not checked** |
| Non-tobacco cigarette substitute | 13.3 | 8 | 2 | 1986: Favor sold in test markets in California and the Southwest to smokers… | medium | contemporary | Rosel George Brown, *From an Unseen Censor* (1958) | **not checked** |
| Live remote-viewing screen | 13.3 | 7 | 0 | 1928-07-02: Jenkins Television Corporation's W3XK in Washington, D.C., the first… | low | Wikipedia only | Charles Romyn Dake, *A Strange Discovery* (1899) | **not checked** |
| News on tape, plastic or foil | 13.3 | 5 | 2 | 1970: Ronald Sturt produced the first news tape of the UK Talking Newspaper… | low | reference | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Voiceprint speaker recognition | 13.2 | 4 | 0 | 1974: Texas Instruments controlled access to its Corporate Computer Center… | low | reference | Rog Phillips, *The Cosmic Junkman* (1953) | **not checked** |
| Computerized medical records and diagno… | 13.2 | 6 | 1 | 1972 †: MYCIN, a Stanford expert system for diagnosing infections, was develo… | low | Wikipedia only | Winston K. Marks, *John's Other Practice* (1954) | **not checked** |
| Exotic surface of Pluto | 13.2 | 5 | 0 | 1976-11 †: Cruikshank, Pilcher and Morrison reported infrared photometry of Plut… | medium | contemporary | Charles A. Stearns, *The Pluto Lamp* (1954) | **not checked** |
| Weapon that kills life but spares struc… | 13.1 | 4 | 1 | 1975: W66 neutron warheads for the Sprint missile (Safeguard ABM) were prod… | low | Wikipedia only | Ray Cummings, *Tarrano the Conqueror* (1925) | **not checked** |
| Surveillance satellite | 13.1 | 8 | 0 | 1960-08-19: Same event: Discoverer 14's imagery was usable intelligence photograp… | medium | Wikipedia only | Frank Koester, *Under the Desert Stars* (1923) | **not checked** |
| Cure for tuberculosis | 13.1 | 8 | 3 | 1945: Mayo Clinic physicians treated tuberculosis patients with streptomyci… | low | contemporary | Ralph Centennius, *The Dominion in 1983* (1883) | **not checked** |
| Firearms used in vacuum and low gravity | 13.0 | 6 | 3 | 1975-01 †: Soviet Salyut 3 (Almaz) military station's fixed Rikhter R-23 autocan… | low | Wikipedia only | (text), *Astounding Stories of Super-Scienc…* (1930) | **not checked** |
| End of the working horse | 12.9 | 5 | 2 | 1915: The US land used to feed horses and mules peaked, after which tractor… | low | reference | Mary Griffith, *Camperdown* (1836) | **not checked** |
| Personality modification treatment | 12.9 | 5 | 4 | 1998-03 †: Knutson and colleagues (NIH/Georgetown) gave healthy volunteers the S… | low | contemporary | John Buchan, *The Moon Endureth* (1912) | **not checked** |
| Atmosphere and clouds of the giant plan… | 12.8 | 9 | 2 | 1932 †: Rupert Wildt identified absorption bands of ammonia and methane in th… | medium | reference | Garrett Putman Serviss, *Other Worlds* (1901) | **not checked** |
| Unbreakable or flexible glass | 12.7 | 7 | 3 | 1914: Laminated glass was widely used in gas-mask eyepieces during World Wa… | low | Wikipedia only | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | **not checked** |
| Cable car or aerial tramway | 12.6 | 6 | 1 | 1908: The Wetterhorn Elevator opened at Grindelwald, Switzerland, carrying… | low | Wikipedia only | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | **not checked** |
| Aircraft escape system | 12.5 | 5 | 1 | 1942-01-13: Heinkel test pilot Helmut Schenk ejected from a stricken He 280 jet (… | medium | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Gene repair against hereditary disease | 12.4 | 5 | 6 | 2012-11: The European Commission approved Glybera (alipogene tiparvovec) for h… | low | Wikipedia only | Alan Edward Nourse, *Star Surgeon* (1959) | **not checked** |
| Voluntary control of body functions | 12.4 | 6 | 0 | 1932: Johannes Schultz in Berlin published autogenic training, in which pat… | low | Wikipedia only | (text), *The Mahabharata, Volume 2 (Books 4…* (1896) | **not checked** |
| Relativistic effects on fast travelers | 12.4 | 6 | 1 | 1938 †: Ives and Stilwell measured the Doppler shift of hydrogen canal rays m… | low | Wikipedia only | Frank Koester, *Under the Desert Stars* (1923) | **not checked** |
| Spacecraft built from or reused as othe… | 12.3 | 7 | 0 | 1971-04-19 †: Salyut 1, the first space station, was built by adapting an Almaz sta… | low | Wikipedia only | Carey Rockwell, *The Space Pioneers* (1953) | **not checked** |
| Synthetic or exotic liquid fuel | 12.3 | 8 | 0 | 1923-02: Leaded 'ethyl' gasoline went on sale in Dayton, Ohio; a November 1924… | medium | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Shipboard automatic analysis of a new p… | 12.2 | 5 | 0 | 1967-10-18 †: Venera 4's descent capsule entered Venus's atmosphere on 18 Oct 1967… | low | contemporary | Nelson S. Bond, *That Worlds May Live* (1943) | **not checked** |
| Quick-setting repair sealant | 11.8 | 5 | 1 | 1956-11: National Fisherman reported Devcon Plastic Steel (steel-filled plasti… | low | contemporary | Roy Rockwood, *Through the Air to the North Pole* (1906) | **not checked** |
| Fast cure for mental illness | 11.8 | 10 | 0 | 1934: Meduna treated hospital patients with metrazol convulsions from 1934;… | low | Wikipedia only | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Sleeping restraints and bunks in spacec… | 11.7 | 4 | 1 | 1973-05: Skylab 2 crew slept in the sleep-restraint compartments. | low | contemporary | Murray Leinster, *Space Tug* (1953) | **not checked** |
| Moons warmed by internal radioactive he… | 11.4 | 3 | 0 | 1971 †: Apollo 15 heat flow experiment (Langseth, Columbia University), deplo… | medium | contemporary | E. E. Smith, *Spacehounds of IPC* (1931) | **not checked** |
| Liquid-fuel rocket | 11.4 | 7 | 0 | 1944-09-08: Germany's V-2 (liquid oxygen and alcohol) was first used operationall… | medium | Wikipedia only | (text), *Astounding Stories of Super-Scienc…* (1930) | **not checked** |
| Aircraft surveying and sampling the env… | 11.3 | 3 | 1 | 1944-09-14: Major Harry Wexler flew through the Great Atlantic Hurricane and reco… | low | Wikipedia only | John Munro, *A Trip to Venus* (1897) | **not checked** |
| Intravenous feeding | 11.3 | 5 | 0 | 1968: Stanley Dudrick and colleagues at the University of Pennsylvania fed… | medium | contemporary | F. L. Wallace, *Accidental Flight* (1952) | **not checked** |
| Surgery that ends need for glasses | 11.3 | 5 | 1 | 1974: Svyatoslav Fyodorov in Moscow developed radial keratotomy and perform… | low | reference | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Germ-free humans | 11.1 | 5 | 0 | 1971-09: Same event: the isolator kept the infant alive for its real purpose,… | medium | Wikipedia only | Allen Kim Lang, *World in a Bottle* (1960) | **not checked** |
| Lie detector | 11.1 | 5 | 0 | 1921: Larson's polygraph, recording blood pressure and breathing, was first… | medium | Wikipedia only | Edwin Balmer; William Ma…, *The Achievements of Luther Trant* (1910) | **not checked** |
| Artificial neural network | 11.0 | 5 | 3 | 1989: Bell Labs applied convolutional neural networks trained by backpropag… | low | Wikipedia only | Heinrich Hauser, *The Brain* (1948) | **not checked** |
| Theory of the Moon's origin | 10.9 | 4 | 7 | 1879 †: George Darwin proposed the fission theory, that the Moon was spun off… | low | Wikipedia only | George Tucker, *A Voyage to the Moon* (1827) | **not checked** |
| Weapon wiping memory or lowering intell… | 10.8 | 5 | 0 | 1962-03: US Army began mass production of the M43 BZ cluster bomb, a munition… | low | Wikipedia only | George O. Smith, *Pattern for Conquest* (1946) | **not checked** |
| Treatment changing skin color | 10.7 | 8 | 1 | 1953: Benoquin (20 percent monobenzyl ether of hydroquinone ointment) was u… | low | contemporary | George S. Schuyler, *Black No More* (1931) | **not checked** |
| Crewed flight around the Moon and back | 10.7 | 3 | 2 | 1968-12 †: Apollo 8 (Borman, Lovell, Anders) launched 21 Dec 1968, orbited the M… | high | contemporary | Jules Verne; Henri Théop…, *From the Earth to the Moon, Direct…* (1872) | **not checked** |
| Astronaut selection and conditioning | 10.6 | 9 | 0 | 1957: Man High I (June 1957) and II flew crews chosen and conditioned by th… | low | reference | Roger D. Aycock, *Palimpsest* (1951) | **not checked** |
| Spacecraft robotic arm | 10.6 | 4 | 0 | 1967: Surveyor 3 sampler arm used for soil mechanics measurements. | medium | Wikipedia only | Manly Wade Wellman, *The Invading Asteroid* (1932) | **not checked** |
| Optical character recognition | 10.5 | 6 | 0 | 1965: US Post Office put the first high-speed optical character reader into… | low | Wikipedia only | Fritz Leiber, *The Green Millennium* (1953) | **not checked** |
| Military helicopter | 10.4 | 11 | 0 | 1955: French field commanders in the Algerian War put machine gunners in Be… | low | Wikipedia only | Arthur Leo Zagat, *When the Sleepers Woke* (1932) | **not checked** |
| Spacecraft flying into the Sun's atmosp… | 10.4 | 4 | 6 | 2021-04-28 †: Parker Solar Probe crossed the Alfvén critical surface into the solar… | medium | contemporary | John Mastin, *Through the Sun in an Airship* (1909) | **not checked** |
| Equivalence of matter and energy | 10.3 | 3 | 0 | 1945-08: Atomic bombs, converting a small fraction of nuclear mass to energy,… | low | Wikipedia only | Jack London, *The Iron Heel* (1907) | **not checked** |
| Home video recording and playback | 10.3 | 4 | 2 | 1963: Telcan offered for sale as a unit or kit in 1963 (expensive, hard to… | low | Wikipedia only | H. G. Wells, *The Sleeper Awakes* (1899) | **not checked** |
| Radiological weapon | 10.3 | 6 | 1 | 1949 †: The US Army Chemical Corps began field-testing prototype radiological… | medium | reference | Stanton A. Coblentz, *In Caverns Below* (1935) | **not checked** |
| Computer prediction of sports and gambl… | 10.2 | 4 | 0 | 1988: Bill Benter and Alan Woods bet in Hong Kong on a computer model's hor… | low | Wikipedia only | Sam Merwin Jr., *The Ambassador* (1954) | **not checked** |
| Air-launched rocket | 10.2 | 3 | 0 | 1990-04-05: Orbital Sciences Pegasus released from a NASA B-52 over the Pacific o… | medium | Wikipedia only | Murray Leinster, *Space Platform* (1953) | **not checked** |
| Scientific supercomputing | 10.2 | 7 | 0 | 1955: NORC moved to the Naval Proving Ground at Dahlgren, Virginia and was… | low | Wikipedia only | John W. Campbell Jr, *When the Atoms Failed* (1930) | **not checked** |
| Warming and rising seas | 10.1 | 5 | 0 | 1938-04 †: G. S. Callendar showed with station records that world temperatures h… | medium | contemporary | H. G. Wells, *Tales of Space and Time* (1899) | **not checked** |
| Crewed suborbital rocket flight | 10.1 | 7 | 0 | 1961-05-05 †: Alan Shepard flew Mercury-Redstone 3 (Freedom 7) to about 115 miles a… | medium | contemporary | Jack Williamson, *After World's End* (1939) | **not checked** |
| Subscription or pay-per-view television | 10.1 | 4 | 1 | 1960-02-26: Telemeter pay television service began in Etobicoke, Ontario with 1,0… | low | Wikipedia only | Hugo Gernsback, *Ralph 124C 41+* (1911) | **not checked** |
| Office automation | 10.1 | 3 | 2 | 1951: LEO I did real clerical work for Lyons (bakery valuations, later payr… | medium | Wikipedia only | Edward Bellamy, *Equality* (1897) | **not checked** |
| Mathematics as language for alien conta… | 9.9 | 4 | 1 | 1972-03 †: Pioneer 10 was launched in March 1972 carrying a plaque that encodes… | medium | Wikipedia only | George Chetwynd Griffith, *A Honeymoon in Space* (1901) | **not checked** |
| Automatic road-vehicle collision avoida… | 9.9 | 3 | 3 | 2003: Same: Honda Inspire CMBS sold to customers in Japan in 2003. | low | Wikipedia only | H. B. Hickey, *Beyond The Thunder* (1948) | **not checked** |
| Origin of lunar craters and domes | 9.9 | 6 | 2 | 1970 †: Apollo 11 and 12 lunar samples showed shock effects from impact-induc… | low | contemporary | Jules Verne; Henri Théop…, *From the Earth to the Moon, Direct…* (1872) | **not checked** |
| Scent signals that control behavior | 9.9 | 6 | 0 | 1959 †: Adolf Butenandt characterized bombykol, the female silkworm moth sex… | medium | Wikipedia only | Henry Andrew Ackermann, *South to Propontis* (1941) | **not checked** |
| Return to horse or human-powered urban… | 9.9 | 4 | 1 | 1940: Paris under occupation: fuel restricted, horse-drawn vehicles and bic… | low | reference | J. D. Beresford, *Goslings* (1913) | **not checked** |
| Biometric clock-in and door access | 9.8 | 4 | 0 | 1975: Identimat hand-geometry machines were installed in over 100 locations. | low | contemporary | Henry Still, *Sales Resistance* (1956) | **not checked** |
| Extracting minerals from seawater | 9.8 | 3 | 1 | 1934-01-10: The Ethyl-Dow (Dow Chemical) plant at Kure Beach, North Carolina, ope… | medium | reference | C. J. Cutcliffe Hyne, *The Lost Continent* (1899) | **not checked** |
| Prenatal conditioning | 9.7 | 6 | 5 | 1948 †: David K. Spelt (Muhlenberg College) conditioned human fetuses in uter… | medium | contemporary | (text), *The Mahabharata, Volume 2 (Books 4…* (1896) | **not checked** |
| Climate swings of a planet from its sta… | 9.7 | 5 | 0 | 1976 †: Hays, Imbrie and Shackleton showed in deep-sea sediment cores that Ea… | medium | contemporary | Murray Leinster, *Planet Explorer* (1957) | **not checked** |
| Giant lens in space | 9.6 | 4 | 0 | 1979-05 †: Walsh, Carswell and Weymann found the double quasar 0957+561, the fir… | medium | contemporary | George O. Smith, *Redevelopment* (1944) | **not checked** |
| Polar navigation instrument | 9.6 | 3 | 0 | 1926-05 †: The Bumstead sun compass was used on Byrd's North Pole flight, where… | low | contemporary | Charles Willing Beale, *The Secret of the Earth* (1899) | **not checked** |
| Tidal locking and spin-down | 9.6 | 4 | 1 | 1919 †: G. I. Taylor (read at the Royal Society 20 March 1919, published Nove… | low | contemporary | Garrett Putman Serviss, *Other Worlds* (1901) | **not checked** |
| Interactive projection surface | 9.5 | 4 | 4 | 2008: Microsoft Surface 1.0, a 30-inch rear-projection tabletop display wit… | low | Wikipedia only | Frank M. Robinson, *The Girls From Earth* (1952) | **not checked** |
| Dead-man's switch weapon | 9.5 | 3 | 0 | 1973-05-10: Kenora, Ontario, 1973-05-10: bank robber's strapped dynamite bomb was… | medium | contemporary | Keith Laumer, *A Trace of Memory* (1962) | **not checked** |
| Extraction of resources from seawater | 9.4 | 3 | 2 | 1934: The Ethyl-Dow Chemical Co. plant at Kure Beach, North Carolina, began… | medium | contemporary | T. Baron Russell, *A Hundred Years Hence (The Expecta…* (1905) | **not checked** |
| Subsurface scanning | 9.4 | 4 | 0 | 1924: Mintrop's company Seismos, hired for seismic exploration in Texas and… | low | Wikipedia only | John Jacob Astor, *A Journey in Other Worlds* (1894) | **not checked** |
| Eradication of insect pests | 9.4 | 3 | 0 | 1940: Same campaign: the eradication of Anopheles gambiae from northeastern… | medium | Wikipedia only | H. G. Wells, *The World Set Free* (1913) | **not checked** |
| Electronic and light-based musical inst… | 9.3 | 9 | 1 | 1895: Alexander Wallace Rimington demonstrated his Colour-Organ at St James… | low | Wikipedia only | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Novel waste disposal | 9.3 | 4 | 3 | 1946: The first dumping of radioactive waste in drums at sea, in the Northe… | low | Wikipedia only | Godfrey Sweven, *Riallaro* (1901) | **not checked** |
| State propaganda broadcasting | 9.3 | 4 | 0 | 1933: Nazi Germany's propaganda ministry had the cheap Volksempfanger radio… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Dispersed infantry tactics replace mass… | 9.3 | 5 | 0 | 1915: Captain Willy Rohr's German Pionier detachment at Hartmannswillerkopf… | low | Wikipedia only | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Rapid vaccine production | 9.2 | 7 | 2 | 1957: Asian influenza vaccine was released to the public in the US from Aug… | medium | contemporary | Fred M. White, *The Doom of London* (1903) | **not checked** |
| Seasickness prevention | 9.1 | 3 | 0 | 1932-11: Italian liner Conte di Savoia, the first major liner fitted with larg… | low | Wikipedia only | Frank R. Stockton, *The Great Stone of Sardis* (1897) | **not checked** |
| Piloted aircraft at several times sound… | 9.1 | 5 | 0 | 1958-02-26: Lockheed F-104A Starfighter (Mach 2 class) became operational with th… | low | Wikipedia only | Robert Wilson, *Vandals of the Void* (1945) | **not checked** |
| Solar thermal power | 9.0 | 3 | 0 | 1913: Frank Shuman's 50-55 horsepower sun-power plant at Maadi near Cairo p… | medium | reference | John Jacob Astor, *A Journey in Other Worlds* (1894) | **not checked** |
| Space medicine and astronaut medical sc… | 9.0 | 9 | 1 | 1959: NASA's Mercury astronaut candidates underwent a grueling series of ph… | low | Wikipedia only | Charles Dixon, *Fifteen Hundred Miles an Hour* (1895) | **not checked** |
| Derelict spacecraft drifting in space | 9.0 | 4 | 1 | 1984-11: Shuttle Discovery (STS-51-A) astronauts Allen and Gardner captured th… | medium | contemporary | Joseph Samachson, *Bedside Manner* (1954) | **not checked** |
| Insulated buildings and gear for cold w… | 9.0 | 3 | 0 | 1969-07-21: Apollo 11 astronauts walked on the Moon (UTC 21 July 1969, local miss… | low | Wikipedia only | Stanley G. Weinbaum, *A Martian Odyssey* (1934) | **not checked** |
| Remote spectroscopy of planets | 8.9 | 6 | 1 | 1932 †: W. S. Adams and T. Dunham identified carbon dioxide in the atmosphere… | medium | reference | Mark Wicks, *To Mars Via the Moon* (1911) | **not checked** |
| Air traffic lanes and control | 8.9 | 6 | 0 | 1920-02-25: Croydon Airport near London commissioned the world's first aerodrome… | low | Wikipedia only | Ignatius Donnelly, *Cæsar's Column* (1890) | **not checked** |
| Artificial blood or blood replacement | 8.9 | 6 | 1 | 1968 †: Robert Geyer and colleagues at Harvard totally perfused rats with a f… | low | reference | Albert Teichner, *Man Made* (1960) | **not checked** |
| Radio broadcasting | 8.9 | 5 | 0 | 1919-11: Hans Idzerda's station PCGG at The Hague began broadcasting on 6 Nove… | low | Wikipedia only | Mary E. Bradley Lane, *Mizora* (1890) | **not checked** |
| Uranium and radium deposits on other wo… | 8.7 | 4 | 0 | 1971 †: Apollo 15's orbiting gamma-ray spectrometer (July-August 1971) detect… | low | contemporary | Nelson S. Bond, *Wanderers of the Wolf-Moon* (1944) | **not checked** |
| Helmet head-up display | 8.7 | 3 | 0 | 1986-04: The AH-64A Apache, whose Honeywell IHADSS helmet shows FLIR video and… | low | Wikipedia only | Jim Harmon, *The Spicy Sound of Success* (1959) | **not checked** |
| Cargo submarine | 8.7 | 4 | 0 | 1916-07-09: Deutschland delivered its commercial cargo at Baltimore. | medium | Wikipedia only | Edward Bellamy, *Equality* (1897) | **not checked** |
| Super-strong plastic | 8.7 | 3 | 0 | 1973: Kevlar fibers were in commercial use by the early 1970s (first as a s… | low | contemporary | Albert dePina, *Minions of the Crystal Sphere* (1944) | **not checked** |
| Robot soldiers and autonomous weapons | 8.7 | 7 | 1 | 1943-05: Mark 24 mine entered Allied service in March 1943; first U-boat kills… | medium | Wikipedia only | Nikola Tesla, *The Problem of Increasing Human En…* (1900) | **not checked** |
| Identification transponder | 8.6 | 4 | 1 | 1940: The IFF Mark II, with stepped tuners and automatic gain control, ente… | medium | Wikipedia only | (text), *Astounding Stories of Super-Scienc…* (1930) | **not checked** |
| Cultured brain tissue | 8.6 | 3 | 3 | 2001 †: Shahaf and Marom (Weizmann Institute) showed a network of cortical ne… | low | contemporary | Thornton DeKy, *The Ultimate Experiment* (1941) | **not checked** |
| Piloted flight to extreme altitude | 8.5 | 4 | 0 | 1932-08-18 †: Auguste Piccard and Max Cosyns reached 16,201 m (53,150 ft) in a pres… | low | contemporary | George Chetwynd Griffith, *A Honeymoon in Space* (1901) | **not checked** |
| Humanoid robot | 8.5 | 6 | 0 | 1939 †: Westinghouse's Elektro (built 1937-38) shown at the 1939 New York Wor… | low | Wikipedia only | Anna Adolph, *Arqtiq* (1899) | **not checked** |
| Mid-air transfer of people | 8.5 | 4 | 1 | 1962-06: Project Coldfeet: Fulton Skyhook surface-to-air pickup of an agent fr… | medium | Wikipedia only | Roy Rockwood, *On a Torn-Away World* (1913) | **not checked** |
| Reactor meltdown or runaway accident | 8.5 | 5 | 0 | 1952-12-12: NRX reactor at Chalk River, Ontario: power surge, fuel melted, alumin… | medium | reference | E. E. Smith, *Storm Cloud on Deka* (1942) | **not checked** |
| Forced experiments on captive humans | 8.4 | 3 | 0 | 1933: Japanese Army physicians under Shiro Ishii began experiments on capti… | low | Wikipedia only | Guy Thorne, *The Soul Stealer* (1906) | **not checked** |
| Rocket-propelled small arms | 8.4 | 5 | 0 | 1942-11: Early M1 bazooka launchers with M6 rockets were issued to U.S. forces… | medium | Wikipedia only | Philip Francis Nowlan, *Armageddon—2419 A.D.* (1928) | **not checked** |
| Weapons-to-energy conversion and arms c… | 8.3 | 2 | 2 | 1998: Cooper Nuclear Station in Nebraska became the first US power plant to… | medium | Wikipedia only | Fritz Leiber, *A Pail of Air* (1951) | **not checked** |
| Spacecraft landing and operating in wat… | 8.2 | 4 | 0 | 1964-06-09 †: Donald Reid's Reid Flying Submarine RFS-1 made a full cycle: airborne… | low | Wikipedia only | Jack Williamson, *After World's End* (1939) | **not checked** |
| Nuclear artillery cannon | 8.2 | 5 | 0 | 1953-10: The first M65 Atomic Cannon battalion, six guns, arrived in Europe (G… | medium | contemporary | Paul Ernst, *The Planetoid of Peril* (1931) | **not checked** |
| Audio recording and playback | 8.2 | 4 | 1 | 1889: Phonographs were put to commercial use: coin-operated machines in pub… | low | contemporary | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| 3D printing | 8.2 | 3 | 0 | 1987-05: 3D Systems announced its stereolithography system (laser-cured acryli… | medium | contemporary | C. M. Kornbluth, *With These Hands* (1951) | **not checked** |
| Remote control of engines from the brid… | 8.1 | 3 | 0 | 1911 †: US Navy collier Neptune, fitted with Westinghouse geared turbines, ha… | low | contemporary | George Chetwynd Griffith, *The Angel of the Revolution* (1893) | **not checked** |
| Artificial senses of touch, taste and s… | 8.0 | 5 | 0 | 1952 †: Bell Labs (Balashek, Biddulph, Davis) built Audrey, a single-speaker… | low | Wikipedia only | Karel Čapek, *R.U.R. (Rossum's Universal Robots)* (1920) | **not checked** |
| Rocket sent to strike the Moon | 8.0 | 3 | 0 | 1959-09-13: The Soviet Luna 2 struck the Moon's surface near Mare Imbrium on 13 S… | high | contemporary | Isabel Hornibrook, *Pemrose Lorry, Camp Fire Girl* (1921) | **not checked** |
| Astronaut training devices | 7.8 | 8 | 0 | 1958-06: NASA engineers took a contoured Mercury capsule couch to the Navy's 5… | low | contemporary | Stanley G. Weinbaum, *A Martian Odyssey* (1934) | **not checked** |
| Planets changing orbits | 7.8 | 6 | 0 | 1944 †: B. P. Sharpless found from observations that Phobos's orbit is changi… | low | Wikipedia only | William Hope Hodgson, *The House on the Borderland* (1908) | **not checked** |
| Submarine | 7.8 | 2 | 3 | 1864-02-17: CSS H. L. Hunley sank USS Housatonic off Charleston, the first combat… | medium | Wikipedia only | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Deceptive or manipulative AI | 7.7 | 3 | 3 | 2024-12 †: Anthropic and Redwood Research showed Claude 3 Opus selectively compl… | medium | contemporary | Heinrich Hauser, *The Brain* (1948) | **not checked** |
| Power-assisted flight controls | 7.6 | 2 | 0 | 1944: Lockheed P-38J-25-LO Lightning fighters entered service with hydrauli… | low | Wikipedia only | Guy Thorne, *The Air Pirate* (1919) | **not checked** |
| Anti-submarine warfare | 7.6 | 5 | 0 | 1916-03-22: The Q-ship Farnborough sank the German submarine U-68 off County Kerr… | low | Wikipedia only | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Animals in spaceflight | 7.5 | 3 | 4 | 1947-02-20: Fruit flies flown in the warhead of a captured V-2 from White Sands,… | high | contemporary | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| Compact powerful motor | 7.5 | 3 | 0 | 1903-12-17 †: Charlie Taylor built a lightweight 12 hp gasoline engine of 180 lb fo… | low | Wikipedia only | Jules Verne, *Robur the Conqueror* (1886) | **not checked** |
| Automatic visitor announcer | 7.4 | 3 | 1 | 1955-02 †: Popular Electronics (Feb 1955) published a build-it photoelectric rel… | low | contemporary | Zona Gale, *Romance Island* (1906) | **not checked** |
| Airlifted prefabricated buildings | 7.4 | 2 | 1 | 1961-07 †: At the July 1961 Tushino air display in Moscow the Soviet Mil flying-… | medium | contemporary | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Computerized marketing and consumer ana… | 7.3 | 6 | 0 | 1961-08: American Investment Company (St. Louis), with Fair, Isaac and Company… | low | contemporary | Dave Dryfoos, *New Hire* (1953) | **not checked** |
| Uranium and radioactive ore mining | 7.2 | 6 | 0 | 1942-12: Uranium metal refined from ore by the Ames Process (Iowa State) and b… | low | Wikipedia only | Ed Earl Repp, *The Radium Pool* (1929) | **not checked** |
| Mechanized farm machinery | 7.1 | 2 | 0 | 1858: John Fowler's steam ploughing tackle won the Royal Agricultural Socie… | low | reference | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | **not checked** |
| Wired broadcast service | 7.1 | 4 | 0 | 1890: Compagnie du Theatrophone began a paid service in Paris offering thea… | medium | contemporary | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Space traffic surveillance network | 7.0 | 3 | 0 | 1961: The Air Force's Space Track system and the Navy's Spasur fence were p… | medium | contemporary | S. P. Meek, *Giants on the Earth* (1931) | **not checked** |
| Static discharge protection for aircraft | 7.0 | 3 | 1 | 1937 †: United Air Lines' flying laboratory tested a trailing discharge wire… | medium | contemporary | Luis Senarens, *Frank Reade Jr.'s Submarine Boat* (1893) | **not checked** |
| Robotic hunter or tracking hound | 7.0 | 4 | 5 | 2020: Same event: Kargu-2 used operationally in Libya against retreating fo… | low | Wikipedia only | Stanley G. Weinbaum, *The Ideal* (1935) | **not checked** |
| Integrated circuit and microminiaturize… | 7.0 | 5 | 0 | 1961: Integrated circuits entered use in products and in the US space and m… | low | Wikipedia only | Walter M. Miller, *Check and Checkmate* (1953) | **not checked** |
| Volcanic eruption forecasting | 7.0 | 3 | 1 | 1910-07: Same event: the police chief's forecast was acted on by evacuating re… | low | reference | Jules Verne, *A Journey to the Centre of the Ear…* (1864) | **not checked** |
| Selecting small or elderly astronauts | 6.9 | 4 | 0 | 1959-04: NASA chose the Mercury Seven (announced 1959-04-09) under a height li… | medium | contemporary | Murray Leinster, *Space Tug* (1953) | **not checked** |
| Central and district heating | 6.9 | 2 | 3 | 1877: Birdsill Holly launched the first commercially successful district st… | medium | Wikipedia only | Mary Griffith, *Camperdown* (1836) | **not checked** |
| Fuel-free electrolytic metal making | 6.8 | 2 | 0 | 1915: Chuquicamata oxide plant in Chile began leaching copper oxide ore and… | low | reference | Ralph Centennius, *The Dominion in 1983* (1883) | **not checked** |
| Reproduction in space or low gravity | 6.7 | 2 | 0 | 1983-12 †: Ten pregnant rats flew on the Soviet Kosmos 1514 (Bion 6) mission, la… | medium | reference | Winston K. Marks, *The Geisha Memory* (1954) | **not checked** |
| Electric depth sounder | 6.6 | 2 | 0 | 1922-02: Harvey Hayes's sonic depth finder was installed on the U.S.S. Ohio an… | medium | reference | Frank R. Stockton, *The Great Stone of Sardis* (1897) | **not checked** |
| Biological data storage | 6.5 | 2 | 1 | 1988 †: Artist Joe Davis with Harvard researchers encoded a 5x7-bit image in… | medium | Wikipedia only | Jack Williamson, *The Masked World* (1963) | **not checked** |
| Radio direction finding | 6.5 | 6 | 0 | 1914-04: United Fruit Company ordered Marconi direction finders for its passen… | low | contemporary | Hollis Godfrey, *The Man Who Ended War* (1908) | **not checked** |
| Landing cushion or braking device | 6.5 | 2 | 1 | 1908: The Bleriot VIII aeroplane (France) used a main landing gear whose sh… | low | Wikipedia only | Cyrano de Bergerac, *A Voyage to the Moon* (1657) | **not checked** |
| Home and telephone banking | 6.5 | 2 | 1 | 1980-12: Same service launched to paying customers; thousands paid $25-30 per… | medium | Wikipedia only | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Explanation of what powers the Sun | 6.5 | 3 | 0 | 1939 †: Hans Bethe's 'Energy Production in Stars' (Physical Review, 1 March 1… | medium | contemporary | Simon Newcomb, *Side-Lights on Astronomy* (1906) | **not checked** |
| Nuclear deterrence | 6.4 | 4 | 2 | 1954-01: The US adopted massive retaliation as declared policy, announced by J… | low | Wikipedia only | Godfrey Sweven, *Riallaro* (1901) | **not checked** |
| Immersive surround cinema | 6.4 | 5 | 1 | 1952-09-30: This Is Cinerama opened on Broadway on 30 September 1952: three proje… | medium | contemporary | Owen Johnson, *The Coming of the Amazons* (1931) | **not checked** |
| Aerial police patrol | 6.4 | 3 | 0 | 1929-09-26: New York Police Department established its Air Service Division. | low | reference | Robert Hugh Benson, *The Dawn of All* (1911) | **not checked** |
| Airborne troop transport | 6.4 | 3 | 0 | 1923: RAF Iraq Command aircraft flew 280 Sikh troops from Kingarban to Kirk… | low | Wikipedia only | H. G. Wells, *When the Sleeper Wakes* (1899) | **not checked** |
| Wireless telegraphy | 6.3 | 4 | 0 | 1898-07: Marconi's apparatus on the steamer Flying Huntress sent reports of th… | medium | contemporary | Jules Verne, *All Around the Moon* (1870) | **not checked** |
| Protective goggles and ear gear against… | 6.2 | 2 | 0 | 1945-08-06: Crews of the Hiroshima bombing mission were told to expect a blinding… | low | Wikipedia only | Ray Cummings, *A Brand New World* (1928) | **not checked** |
| Hearing aid | 6.2 | 2 | 1 | 1896 †: Miller Reese Hutchison's Akouphone, the first electric hearing aid, u… | low | Wikipedia only | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Sex change treatment | 6.2 | 5 | 1 | 1931: The 1931 operations were performed on real patients under care at the… | low | Wikipedia only | Gregory Casparian, *An Anglo-American Alliance* (1906) | **not checked** |
| Seaplane and flying boat | 6.1 | 4 | 0 | 1914-01-01: St. Petersburg-Tampa Airboat Line began the first scheduled airline s… | medium | Wikipedia only | George Chetwynd Griffith, *The World Peril of 1910* (1906) | **not checked** |
| Martian dust storms and global winds | 6.1 | 3 | 1 | 1971-11 †: Mariner 9, the first Mars orbiter, arrived 14 November 1971 and obser… | medium | contemporary | Robert Moore Williams, *New Lamps* (1957) | **not checked** |
| Radiation hazard zone in space | 6.1 | 3 | 0 | 1958 †: Explorer 1 (launched 1958-01-31, US Army/JPL, James Van Allen's Geige… | high | contemporary | Edmond Hamilton, *Outside the Universe* (1929) | **not checked** |
| Accurate weather forecasting | 6.0 | 2 | 2 | 1861: The Times published the first daily weather forecasts, from FitzRoy's… | low | Wikipedia only | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Central electric fire control of guns | 6.0 | 3 | 0 | 1912: HMS Thunderer, the second ship fitted with Scott's director, entered… | low | contemporary | M. P. Shiel, *The Lord of the Sea* (1901) | **not checked** |
| Finite speed of gravity | 6.0 | 2 | 3 | 2017-10 †: LIGO/Virgo and Fermi/INTEGRAL published that gravitational waves from… | medium | contemporary | George O. Smith; John W.…, *Venus Equilateral* (1947) | **not checked** |
| Growth-stunting treatment | 6.0 | 5 | 0 | 1960: Estrogen growth attenuation has been used routinely since the 1960s o… | low | Wikipedia only | Richard S. Shaver, *Of Stegner's Folly* (1952) | **not checked** |
| Growth-stimulating agent | 6.0 | 4 | 0 | 1921 †: H. M. Evans and J. A. Long injected a bovine anterior-pituitary extra… | low | reference | H. G. Wells, *The Food of the Gods and How It Ca…* (1903) | **not checked** |
| Secure scrambled communication | 6.0 | 4 | 0 | 1919 †: French engineers Jules Carpentier and Eugene Poirson built and patent… | low | reference | Morgan Robertson, *Futility (The Wreck of the Titan)* (1898) | **not checked** |
| Haptic alert wearable | 5.9 | 3 | 1 | 1960-04: Vibracall silent paging system listed as a commercial product (AC Spa… | low | contemporary | Edgar Rice Burroughs, *The Warlord of Mars* (1913) | **not checked** |
| Discovery of aging mechanisms | 5.9 | 2 | 1 | 1988 †: Friedman and Johnson found that a mutation in the age-1 gene of the r… | low | contemporary | Poul Anderson, *What Shall It Profit?* (1956) | **not checked** |
| Iceberg detection instrument | 5.9 | 3 | 0 | 1914-04 †: Reginald Fessenden's electric oscillator got echoes from an iceberg a… | medium | contemporary | Morgan Robertson, *Futility (The Wreck of the Titan)* (1898) | **not checked** |
| Wall-climbing vehicle | 5.9 | 3 | 1 | 1961-09 †: Esso Research and Engineering showed a preliminary model of a magneti… | low | contemporary | Frank R. Stockton, *The Great Stone of Sardis* (1897) | **not checked** |
| Personal summoning device | 5.9 | 3 | 1 | 1950: Paging service for New York physicians using a carried radio pager, b… | low | Wikipedia only | Ray Cummings, *Brigands of the Moon* (1930) | **not checked** |
| How alcohol acts on the brain | 5.8 | 3 | 0 | 1977-05 †: Chin and Goldstein showed that low concentrations of ethanol increase… | low | reference | C. M. Kornbluth, *The Syndic* (1953) | **not checked** |
| Sea-based spaceport | 5.8 | 4 | 0 | 1967-04: San Marco 2 (San Marco B), an Italian-US atmospheric-density satellit… | medium | contemporary | Joseph E. Kelleam, *Hunters Out of Space* (1960) | **not checked** |
| Tank | 5.8 | 3 | 0 | 1911: The Spanish Schneider-Brillie armored vehicle, with two machine guns… | low | Wikipedia only | H. G. Wells, *Anticipations* (1901) | **not checked** |
| Moon-bounce communication | 5.7 | 2 | 0 | 1960-01: The Navy's Washington-Hawaii Moon Relay teletype and facsimile circui… | high | contemporary | Wilbur Finley Fauley, *Shuddering Castle* (1936) | **not checked** |
| New super-powerful explosive | 5.7 | 2 | 1 | 1867: Alfred Nobel patented dynamite (stabilized nitroglycerin) in 1867 and… | low | Wikipedia only | Francis Bacon, *New Atlantis* (1627) | **not checked** |
| Engines run on plant or animal-derived… | 5.6 | 3 | 0 | 1930: Sugarcane ethanol began to be used as motor fuel in Brazil in the lat… | low | Wikipedia only | H. G. Wells, *The Food of the Gods and How It Ca…* (1903) | **not checked** |
| Gene manipulation of an existing person | 5.6 | 2 | 3 | 2003: China's SFDA approved Gendicine (recombinant adenovirus p53) for head… | medium | Wikipedia only | Leigh Brackett, *Enchantress of Venus* (1949) | **not checked** |
| Magnetically propelled vessel | 5.5 | 2 | 4 | 1966 †: Stewart Way's EMS-1, a 3 m magnetohydrodynamic submarine, was designe… | medium | Wikipedia only | William Richard Bradshaw, *The Goddess of Atvatabar* (1892) | **not checked** |
| Automated freight and package handling | 5.5 | 3 | 1 | 1956: The US Post Office Department introduced its first semi-automatic par… | low | reference | T. Baron Russell, *A Hundred Years Hence (The Expecta…* (1905) | **not checked** |
| Industrial nitrogen fixation for fertil… | 5.5 | 2 | 0 | 1905: First full-scale cyanamide fertilizer factories at Piano d'Orta (Ital… | medium | Wikipedia only | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Computer forecasting of social behaviour | 5.5 | 4 | 0 | 1952-11-04: Same broadcast: the forecast was used on live television for the real… | medium | Wikipedia only | Alfred Bester, *The Push of a Finger* (1942) | **not checked** |
| Radio time synchronization | 5.4 | 2 | 0 | 1904-08-09: Regular scheduled Navy time signals from Boston were used by ships an… | low | reference | Percy Greg, *Across the Zodiac* (1880) | **not checked** |
| Controlled nuclear fusion achieved | 5.4 | 4 | 0 | 1958 †: Scylla I theta-pinch at Los Alamos (James Tuck's group) produced deut… | medium | contemporary | H. Beam Piper, *Operation R.S.V.P.* (1951) | **not checked** |
| Bank of spare body parts | 5.4 | 2 | 0 | 1944: The Eye-Bank supplied banked corneas to hospitals for corneal graftin… | low | contemporary | Edgar Rice Burroughs, *The Master Mind of Mars* (1927) | **not checked** |
| Cross-species tissue grafting | 5.4 | 3 | 2 | 1963-11 †: Keith Reemtsma's Tulane team in New Orleans transplanted a chimpanzee… | low | Wikipedia only | Maurice Renard, *New Bodies for Old* (1908) | **not checked** |
| Vehicle crash occupant protection | 5.2 | 2 | 1 | 1949: The 1949 Nash belts were offered to buyers on production cars and use… | low | Wikipedia only | Rudyard Kipling, *With the Night Mail* (1905) | **not checked** |
| Radio noise from the Sun and planets | 5.2 | 2 | 0 | 1942-02 †: J. S. Hey, studying British Army radar jamming reports from sites acr… | medium | reference | Godfrey Sweven, *Limanora* (1903) | **not checked** |
| Nature and observation of the solar cor… | 5.2 | 3 | 0 | 1930 †: Bernard Lyot, working at the Pic du Midi observatory in summer 1930,… | medium | contemporary | Garrett Putman Serviss, *Curiosities of the Sky* (1909) | **not checked** |
| Exotic super-strong armor material | 5.1 | 4 | 1 | 1889-07-16 †: The first firing trial of a nickel-steel armor plate (9.33 in thick)… | medium | reference | Jules Verne, *The Moon-Voyage* (1872) | **not checked** |
| Air defense and early-warning network | 5.1 | 2 | 1 | 1938: The first Chain Home stations began full-time operation in 1938 for c… | low | Wikipedia only | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Computer chess | 5.1 | 2 | 0 | 1977-03: Fidelity Electronics released Chess Challenger, the first dedicated c… | medium | Wikipedia only | Fritz Leiber, *The 64-Square Madhouse* (1962) | **not checked** |
| Very fast surface ship | 5.1 | 3 | 0 | 1900 †: On trials in 1900 the turbine destroyer HMS Viper was reported at 35.… | low | Wikipedia only | Herbert D. Ward, *A Republic Without a President, an…* (1891) | **not checked** |
| Electronic digital computer | 4.7 | 3 | 1 | 1944-02-05: Colossus Mark 1, installed at Bletchley Park, attacked its first Lore… | medium | Wikipedia only | Michel Verne; Jules Verne, *In the Year 2889* (1889) | **not checked** |
| Shared virtual world | 4.6 | 2 | 0 | 1980: MUD1 opened over the Internet to outside players, the first Internet… | low | Wikipedia only | Erik Fennel, *Black Priestess of Varda* (1947) | **not checked** |
| Truth serum | 4.6 | 2 | 0 | 1922: Scopolamine interrogation of prisoners in Dallas was used for questio… | medium | contemporary | George Chetwynd Griffith, *Olga Romanoff* (1894) | **not checked** |
| Tether in space | 3.8 | 2 | 0 | 1966-09 †: On Gemini 11, Pete Conrad and Richard Gordon connected their spacecra… | high | contemporary | Charles L. Fontenay, *Atom Drive* (1956) | **not checked** |
| Computer hacking and sabotage | 3.5 | 2 | 0 | 1967: Students at Evanston Township High School (Chicago suburb) penetrated… | low | Wikipedia only | Frederik Pohl; C. M. Kor…, *Wolfbane* (1957) | **not checked** |
| Composition of Saturn's rings | 3.3 | 2 | 2 | 1895 †: James Keeler (Allegheny Observatory) and Aristarkh Belopolsky (Pulkov… | medium | contemporary | Richard Adams Locke; J.…, *The Moon Hoax* (1835) | **not checked** |
| Automated prison confinement | 3.1 | 1 | 0 | 1901: Same installation: the Jefferson County Jail at Louisville, working j… | low | reference | Robert Grant; John Boyle…, *The King's Men* (1884) | **not checked** |
