# Scoring after tier 2, tranche A (PLAN §8)

Written by `match.py score full`. Settings: weight log (w = log2(1 + min(L, 500))), the scoring milestone `first_practical_use` else `first_demonstration`, points from score 0.125 (every judged score above 0), precision from 0.5, `contradicted_negative` from 0.5, deadlines checked against 2026 with 10 years of grace. This scoring follows tier 2 (PLAN §5), which checked 650 deciding concepts, and checkpoint 3's review (`runs/match/milestone_review.jsonl`). Tranche B is not scored. † = scored on a demonstration only (PLAN §14.5).

## Resolutions

77,436 tranche-A claims from 3,224 books.

| resolution | claims | share |
|---|---|---|
| open: no_milestone | 31,442 | 40.6% |
| not_a_prediction | 16,411 | 21.2% |
| realized | 15,803 | 20.4% |
| open: no_concept | 6,795 | 8.8% |
| open: too_vague | 3,897 | 5.0% |
| untestable | 2,558 | 3.3% |
| open: not_matched | 272 | 0.4% |
| failed: missed_deadline | 170 | 0.2% |
| open: not_contradicted | 51 | 0.1% |
| failed: contradicted_negative | 24 | 0.0% |
| vindicated | 7 | 0.0% |
| open: no_year | 6 | 0.0% |

Deadlines: 1,741 `will` claims with a concept have a stated time naming a year, decade or century after publication; 765 of those ended before 2016. Of these, 302 are realized anyway, 170 missed the deadline, and 293 are not a prediction. Of the 581 realized claims with a deadline, 511 came true by it and 70 after it (median 18 years late).

## The top 50 predictions

11,375 book–concept entries earn points (each book counts its best claim once per concept).

| # | points | score | lead | author | book | concept | milestone | quote |
|---|---|---|---|---|---|---|---|---|
| 1 | 6.73 | 0.75 | 1735 | Lucian of Samosata | *Trips to the Moon* (200) | Wearable wings | 1935 | I took, you must know, a very large eagle and a vulture also, one of the strongest I could get, and cut off t… |
| 2 | 6.32 | 0.875 | 148 | Richard Adams Locke | *The Moon Hoax* (1835) | Meteorites that came from the Moon † | 1983-03 | If we had before retained any doubt of the power of lunar volcanoes to throw fragments of their craters so fa… |
| 3 | 6.13 | 0.75 | 287 | Cyrano de Bergerac | *A Voyage to the Moon* (1657) | Multistage rocket | 1944-11 | For so soon as the Flame had devoured one tier of Squibs, which were ranked by six and six, by means of a Tra… |
| 4 | 6.11 | 0.875 | 125 | Voltaire | *Micromegas* (1752) | Phobos and Deimos, the two moons of Mars † | 1877-08 | they swung by two moons that cater to this planet but have escaped the notice of our astronomers. |
| 5 | 6.09 | 0.75 | 278 | Cyrano de Bergerac | *A Voyage to the Moon* (1657) | Audiobook player | 1935 | it was a Book made wholly for the Ears, and not the Eyes. So that when any Body has a mind to read in it, he… |
| 6 | 6.07 | 0.75 | 273 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Audiobook player | 1935 | It is a book indeed, but a miraculous book without pages or letters; in fine, it is a book to learn from whic… |
| 7 | 6.07 | 0.75 | 273 | Francis Bacon | *New Atlantis* (1627) | Hearing aid | 1900 | We have certain helps which set to the ear do further the hearing greatly. |
| 8 | 5.98 | 1 | 62 | Luis Senarens | *The Sunken Isthmus* (1896) | Submarine air supply | 1958-10 | Under the pilot-house there was placed a generator which was capable of manufacturing pure oxygen, and also o… |
| 9 | 5.81 | 1 | 55 | Charles L. Fontenay | *Blow the Man Down* (1955) | Solar sail or solar-driven spacecraft † | 2010-06-09 | The wind that blows between the worlds," said Carrel solemnly. "Solar radiation. Its pressure will move a shi… |
| 10 | 5.68 | 0.875 | 89 | Jules Verne | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Weightlessness in spaceflight † | 1961-04-12 | Nicholl having accidentally let a glass slip from his hand, the glass, instead of falling, remained suspended… |
| 11 | 5.68 | 0.875 | 89 | Jules Verne | *The Moon-Voyage* (1872) | Weightlessness in spaceflight † | 1961-04-12 | Nicholl having let a tumbler escape from his hand, instead of falling, it remained suspended in the air. |
| 12 | 5.61 | 0.875 | 84 | Percy Greg | *Across the Zodiac* (1880) | Pressurized spacecraft cabin and atmosp… | 1964-10-12 | I had first, by means of the air pump, to fill the vessel with an atmosphere as dense as that in which I had… |
| 13 | 5.58 | 1 | 47 | Edmond Hamilton | *The Sargasso of Space* (1931) | Refueling spacecraft in orbit | 1978-02 | A Pluto liner a quarter-mile back, and we can pump the fuel over here by connecting tube-lines. |
| 14 | 5.58 | 0.875 | 82 | Garrett Putman Serviss | *Other Worlds* (1901) | Meteorites that came from the Moon † | 1983-03 | It has led to the theory that meteorites may have originally been shot out of the moon's great volcanoes, whe… |
| 15 | 5.55 | 0.875 | 80 | Edgar Rice Burroughs | *A Fighting Man of Mars* (1930) | Invisibility † | 2010-12 | The compound of invisibility merely bows outward the reflected light, which, entering our eyes and impinging… |
| 16 | 5.55 | 0.875 | 80 | (text) | *Astounding Stories of Super-Science September 1930* (1930) | Invisibility † | 2010-12 | The walls of the ship are double, the inner one of metal and the outer one of vitrolene or some similar perfe… |
| 17 | 5.52 | 1 | 45 | Arthur Cheney Train; Robert W… | *The Moon Maker* (1916) | Black sky filled with stars seen from s… † | 1961-04-12 | Yet, in spite of the fact that the universe was filled with light, the sky remained as black as midnight and… |
| 18 | 5.45 | 0.875 | 74 | Garrett Putman Serviss | *Curiosities of the Sky* (1909) | Meteorites that came from the Moon † | 1983-03 | For similar reasons it seems not impossible that the theory mentioned in a former chapter—that some of the me… |
| 19 | 5.43 | 0.875 | 73 | George Chetwynd Griffith | *The Angel of the Revolution* (1893) | Tidal power | 1966-11-26 | The ebb and flow in the Thames had at last been turned to account, and worked huge turbines which perpetually… |
| 20 | 5.36 | 1 | 40 | Fritz Leiber | *The Green Millennium* (1953) | Orbital mirrors lighting cities † | 1993-02-04 | the false sunlight from the sodium mirror circling the earth to make evening light for this city |
| 21 | 5.32 | 0.75 | 136 | Jules Verne | *All Around the Moon* (1870) | Second natural moon of Earth † | 2006-09-14 | It is a simple bolide, but one of such enormous dimensions that the Earth's attraction has made it a satellit… |
| 22 | 5.31 | 0.875 | 66 | T. Baron Russell | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | Self-service rental cars | 1971 | automatic motor-cars will exist, coin-worked. A man who wishes to travel will step into a motor-car, drop int… |
| 23 | 5.31 | 0.75 | 134 | Jules Verne | *The Moon-Voyage* (1872) | Second natural moon of Earth † | 2006-09-14 | Yes, my friend, two moons, though she is generally supposed to have but one. But this second moon is so small… |
| 24 | 5.25 | 0.625 | 337 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Solar-powered rocket † | 1999 | I have told you that the sun beat vigorously upon my concave mirrors, and uniting its rays in the middle of t… |
| 25 | 5.25 | 0.875 | 63 | Godfrey Sweven | *Limanora* (1903) | Tidal power | 1966-11-26 | In another series of caves they cooped up the water of the full tides by means of gigantic dams and sluice-ga… |
| 26 | 5.25 | 1 | 37 | Fritz Leiber | *The Snowbank Orbit* (1962) | Solar-powered rocket † | 1999 | A huge paraboloid mirror, its diameter four times the length of the ship's hull, superheated at its focus the… |
| 27 | 5.23 | 0.875 | 62 | Frank Belknap Long | *Woman from Another Planet* (1960) | Three-dimensional telepresence | 2022 | Within the disk the screen glowed brightly and Loring's image was life size. It stood out with a startling, t… |
| 28 | 5.22 | 0.75 | 123 | John Jacob Astor | *A Journey in Other Worlds* (1894) | Evacuated tube train † | 2017-05-12 | the atmospheric resistance is about to be reduced by running the cars hermetically sealed through a partial v… |
| 29 | 5.21 | 1 | 36 | E. E. Smith | *Triplanetary* (1948) | Retina and iris recognition | 1984 | Kinnison dashed up to an apparently blank wall, turned his back upon four commissioned officers holding cocke… |
| 30 | 5.21 | 0.75 | 122 | Adam Seaborn | *Symzonia* (1820) | Jet-propelled boat | 1942 | devised a plan for accelerating their motion, by means of a number of tubes which perforated the after part o… |
| 31 | 5.19 | 0.875 | 60 | John Munro | *A Trip to Venus* (1897) | Rocket thrust in a vacuum | 1957-10-04 | A jet of gas, at a very high pressure, escaping from an orifice into the vacuum or ether, would give us a ver… |
| 32 | 5.17 | 0.75 | 118 | E. Douglas Fawcett | *Hartmann, the Anarchist* (1893) | Ultralight metal † | 2011-11 | Why, it is as light or lighter than cardboard. What an extraordinary combination of attributes! |
| 33 | 5.17 | 1 | 35 | Charles Willard Diffin | *Brood of the Dark Moon* (1931) | Powered rocket landing | 1966-06-02 | Down there, where the fires ceased, there would be water; he would land there! And the ship from Earth slippe… |
| 34 | 5.16 | 0.75 | 117 | M. P. Shiel | *The Purple Cloud* (1901) | Liquid air as energy source or engine f… | 2018-04 | She was evidently one of those many ships of late years which have substituted liquid air for steam, yet reta… |
| 35 | 5.15 | 0.875 | 58 | Manly Wade Wellman | *Warrior of Two Worlds* (1944) | Sleep and incapacitating gas | 2002-10-26 | Gederr himself who squirted anaesthetic gas upon you and felled you, senseless. |
| 36 | 5.15 | 0.875 | 58 | Stephen Marlowe | *Recruit for Andromeda* (1959) | Iris diaphragm door | 2017 | A door irised open for them in a solid wall of metal. Irised was the only word Temple could think of, for a t… |
| 37 | 5.14 | 0.75 | 115 | Herbert D. Ward | *A Republic Without a President, and Other Stories* (1891) | Thought-to-text and thought display † | 2006 | Authors would only need to fix their attention upon the plot; the delicate instrument would record it indelib… |
| 38 | 5.14 | 0.75 | 115 | Godfrey Sweven | *Limanora* (1903) | Liquid air as energy source or engine f… | 2018-04 | Another that was near at hand was the use of the expansion of their liquefied and solidified air for purposes… |
| 39 | 5.14 | 0.75 | 115 | Mrs. Loudon | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Undersea tunnel | 1942-07-01 | it had nearly advanced through the whole of the tunnel under the sea, which separates the two kingdoms, witho… |
| 40 | 5.13 | 1 | 34 | Edwin K. Sloat | *Loot of the Void* (1932) | Astronaut maneuvering gun or pack | 1966-07-19 | while the long flame of his Sextle rocket-pistol showed that he was checking his forward momentum as rapidly… |
| 41 | 5.12 | 0.75 | 112 | David Franklin Powell | *The Wolf-Men* (1906) | Liquid air as energy source or engine f… | 2018-04 | liquid air engines, a patent of Wilson’s, maximum speed of which is forty-five knots per hour upon the surfac… |
| 42 | 5.11 | 0.75 | 111 | Hugo Gernsback | *Ralph 124C 41+* (1911) | Planetary defense against comets and as… † | 2022-09-26 | The gravitational action of his machine on the comet would deflect the course of the latter enough—even a few… |
| 43 | 5.11 | 0.75 | 111 | Herbert D. Ward | *A Republic Without a President, and Other Stories* (1891) | Sleep and incapacitating gas | 2002-10-26 | This preparation was warranted to "make a man who smelled it lose consciousness in less time that it takes to… |
| 44 | 5.10 | 0.75 | 110 | Simon Newcomb | *Side-Lights on Astronomy* (1906) | Large astrometric surveys of star posit… † | 2016-09-14 | At the end of the twentieth century we may expect that the work will be repeated. Then, by comparing the char… |
| 45 | 5.10 | 0.75 | 110 | Luis Senarens | *From Zone to Zone* (1894) | Electric-powered aircraft | 2004 | The engine-room held the powerful electric engines which formed the motive power of the airship. |
| 46 | 5.09 | 0.625 | 282 | Cyrano de Bergerac | *Voyages to the Moon and the Sun* (1662) | Rocket-powered aircraft | 1944 | they ought to bind around it a number of rockets because their rapid ascent would lift it high in the air, th… |
| 47 | 5.09 | 0.75 | 109 | Robert Hugh Benson | *The Dawn of All* (1911) | Self-driving car | 2020-10-08 | the great car, with no driver visible in front through the clear-glass windows, moved off southward. |
| 48 | 5.08 | 0.75 | 108 | Jules Verne | *All Around the Moon* (1870) | Gravity-neutral (Lagrange) point betwee… | 1978-11-20 | Suppose it to be animated by just sufficient velocity to reach the neutral point, but not to pass it. In that… |
| 49 | 5.06 | 0.75 | 106 | William Wallace Cook | *Adrift in the Unknown* (1904) | Spray-on protective body coating † | 2010-09 | we are coated, and our clothing impregnated, with my anti-temperature fluid. |
| 50 | 5.06 | 0.75 | 106 | Jules Verne | *The Moon-Voyage* (1872) | Gravity-neutral (Lagrange) point betwee… | 1978-11-20 | Either the velocity of the projectile will then be insufficient, and it will remain entirely motionless on th… |

## Authors: total points

Each author counts a concept once, from their best book. 767 authors score.

| # | author | points | concepts | books | points per book | precision |
|---|---|---|---|---|---|---|
| 1 | E. E. Smith | 426.8 | 163 | 20 | 21.3 | 11% of 2868 |
| 2 | H. G. Wells | 360.2 | 128 | 27 | 13.3 | 18% of 1515 |
| 3 | Murray Leinster | 358.4 | 152 | 58 | 6.2 | 17% of 2144 |
| 4 | Jules Verne | 344.2 | 108 | 16 | 21.5 | 19% of 1082 |
| 5 | George O. Smith | 319.2 | 131 | 57 | 5.6 | 11% of 2076 |
| 6 | Ray Cummings | 317.1 | 128 | 36 | 8.8 | 11% of 1907 |
| 7 | Edmond Hamilton | 285.6 | 106 | 34 | 8.4 | 16% of 959 |
| 8 | Randall Garrett | 260.0 | 111 | 78 | 3.3 | 12% of 1590 |
| 9 | George Chetwynd Griffith | 257.7 | 92 | 6 | 43.0 | 28% of 803 |
| 10 | Raymond Z. Gallun | 254.8 | 99 | 17 | 15.0 | 22% of 701 |
| 11 | John W. Campbell Jr | 250.3 | 102 | 11 | 22.8 | 15% of 963 |
| 12 | Godfrey Sweven | 246.6 | 88 | 2 | 123.3 | 17% of 568 |
| 13 | Fritz Leiber | 225.5 | 94 | 29 | 7.8 | 18% of 657 |
| 14 | H. Beam Piper | 217.3 | 100 | 32 | 6.8 | 14% of 1180 |
| 15 | F. L. Wallace | 202.4 | 87 | 18 | 11.2 | 17% of 551 |
| 16 | Garrett Putman Serviss | 200.7 | 72 | 6 | 33.5 | 14% of 585 |
| 17 | Edgar Rice Burroughs | 196.4 | 78 | 21 | 9.4 | 10% of 1200 |
| 18 | Nelson S. Bond | 186.1 | 74 | 37 | 5.0 | 15% of 741 |
| 19 | Stephen Marlowe | 179.6 | 73 | 53 | 3.4 | 14% of 750 |
| 20 | Bryce Walton | 162.1 | 69 | 38 | 4.3 | 14% of 536 |
| 21 | Robert Silverberg | 157.6 | 73 | 42 | 3.8 | 13% of 720 |
| 22 | Jack Williamson | 156.1 | 59 | 11 | 14.2 | 15% of 391 |
| 23 | Alan Edward Nourse | 150.9 | 70 | 33 | 4.6 | 15% of 541 |
| 24 | Percy Greg | 147.0 | 47 | 1 | 147.0 | 27% of 248 |
| 25 | Hugo Gernsback | 143.4 | 44 | 1 | 143.4 | 31% of 183 |
| 26 | Carey Rockwell | 136.1 | 59 | 6 | 22.7 | 21% of 535 |
| 27 | Richard M. Elam | 134.6 | 59 | 3 | 44.9 | 31% of 307 |
| 28 | Roy Rockwood | 123.5 | 49 | 7 | 17.6 | 16% of 404 |
| 29 | Leigh Brackett | 122.2 | 50 | 21 | 5.8 | 11% of 501 |
| 30 | Alfred Coppel | 113.1 | 52 | 24 | 4.7 | 19% of 262 |

## Books: total points

| # | book | author | group | points | concepts |
|---|---|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | Science-Fiction | 226.9 | 81 |
| 2 | *Across the Zodiac* (1880) | Percy Greg | Science-Fiction | 147.0 | 47 |
| 3 | *Ralph 124C 41+* (1911) | Hugo Gernsback | Science-Fiction | 143.4 | 44 |
| 4 | *Spacehounds of IPC* (1931) | E. E. Smith | Science-Fiction | 117.7 | 43 |
| 5 | *Olga Romanoff* (1894) | George Chetwynd Griffith | Science-Fiction | 114.0 | 43 |
| 6 | *The Moon-Voyage* (1872) | Jules Verne | Science-Fiction | 112.8 | 35 |
| 7 | *Skylark Three* (1930) | E. E. Smith | Science-Fiction | 110.9 | 38 |
| 8 | *All Around the Moon* (1870) | Jules Verne | Science-Fiction | 110.5 | 32 |
| 9 | *A Journey in Other Worlds* (1894) | John Jacob Astor | Science-Fiction | 105.6 | 40 |
| 10 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | Science-Fiction | 104.6 | 37 |
| 11 | *When the Sleeper Wakes* (1899) | H. G. Wells | Science-Fiction | 102.7 | 40 |
| 12 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | Futurism | 100.3 | 32 |
| 13 | *Maza of the Moon* (1929) | Otis Adelbert Kline | Science-Fiction | 91.5 | 33 |
| 14 | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Mrs. Loudon | Science-Fiction | 90.3 | 30 |
| 15 | *Through the Sun in an Airship* (1909) | John Mastin | Science-Fiction | 88.0 | 37 |
| 16 | *The Skylark of Valeron* (1934) | E. E. Smith | Science-Fiction | 87.7 | 33 |
| 17 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | Science-Fiction | 85.9 | 33 |
| 18 | *Space Tug* (1953) | Murray Leinster | Science-Fiction | 83.8 | 38 |
| 19 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | Science-Fiction | 82.8 | 41 |
| 20 | *The Green Millennium* (1953) | Fritz Leiber | Science-Fiction | 80.5 | 33 |
| 21 | *A Trip to Venus* (1897) | John Munro | Science-Fiction | 80.2 | 26 |
| 22 | *Pharaoh's Broker* (1899) | Ellsworth Douglass | Science-Fiction | 79.8 | 26 |
| 23 | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Jules Verne | Science-Fiction | 79.6 | 25 |
| 24 | *Tarrano the Conqueror* (1925) | Ray Cummings | Science-Fiction | 78.1 | 31 |
| 25 | *The Angel of the Revolution* (1893) | George Chetwynd Griffith | Science-Fiction | 75.2 | 25 |
| 26 | *To Mars Via the Moon* (1911) | Mark Wicks | Science-Fiction | 75.1 | 27 |
| 27 | *Venus Equilateral* (1947) | George O. Smith | Science-Fiction | 74.4 | 32 |
| 28 | *Triplanetary* (1948) | E. E. Smith | Science-Fiction | 73.7 | 33 |
| 29 | *Last and First Men* (1930) | Olaf Stapledon | Science-Fiction | 73.3 | 29 |
| 30 | *Voyages to the Moon and the Sun* (1662) | Cyrano de Bergerac | Science-Fiction | 73.2 | 21 |

## Precision

Claims realized at a score of 0.5 or more, of all tranche-A claims by the author; authors with 50 or more (309).

| # | author | precision | claims | points |
|---|---|---|---|---|
| 1 | Edwin Balmer | 46% | 54 | 13.1 |
| 2 | William MacHarg | 46% | 54 | 13.1 |
| 3 | Harold L. Goodwin | 39% | 208 | 73.7 |
| 4 | Ignatius Donnelly | 34% | 90 | 64.6 |
| 5 | Walter M. Miller | 33% | 85 | 56.5 |
| 6 | Jeff Sutton | 32% | 85 | 37.4 |
| 7 | Richard M. Elam | 31% | 307 | 134.6 |
| 8 | Arthur Cheney Train | 31% | 112 | 88.7 |
| 9 | Robert Williams Wood | 31% | 112 | 88.7 |
| 10 | Mary E. Bradley Lane | 31% | 104 | 58.8 |
| 11 | Hugo Gernsback | 31% | 183 | 143.4 |
| 12 | Wilbur Finley Fauley | 29% | 80 | 37.2 |
| 13 | John Munro | 28% | 95 | 80.2 |
| 14 | George Chetwynd Griffith | 28% | 803 | 257.7 |
| 15 | Luis Senarens | 28% | 395 | 88.1 |
| 16 | George Gordon Hastings | 27% | 73 | 33.4 |
| 17 | Philip Francis Nowlan | 27% | 172 | 89.5 |
| 18 | Walt Richmond | 27% | 101 | 44.3 |
| 19 | Percy Greg | 27% | 248 | 147.0 |
| 20 | Nikola Tesla | 26% | 66 | 37.0 |

## Points per book

Authors with 3 or more books in the corpus (256); every book counts, including those with no tranche-A points.

| # | author | points per book | books | points |
|---|---|---|---|---|
| 1 | Richard M. Elam | 44.9 | 3 | 134.6 |
| 2 | George Chetwynd Griffith | 43.0 | 6 | 257.7 |
| 3 | Garrett Putman Serviss | 33.5 | 6 | 200.7 |
| 4 | George Allan England | 32.0 | 3 | 96.0 |
| 5 | Camille Flammarion | 30.7 | 3 | 92.0 |
| 6 | John W. Campbell Jr | 22.8 | 11 | 250.3 |
| 7 | Carey Rockwell | 22.7 | 6 | 136.1 |
| 8 | Charles Willard Diffin | 22.6 | 4 | 90.3 |
| 9 | Otis Adelbert Kline | 22.3 | 5 | 111.6 |
| 10 | Roman Frederick Starzl | 21.9 | 3 | 65.8 |
| 11 | Rudyard Kipling | 21.9 | 3 | 65.7 |
| 12 | Jules Verne | 21.5 | 16 | 344.2 |
| 13 | E. E. Smith | 21.3 | 20 | 426.8 |
| 14 | E. Everett Evans | 20.1 | 4 | 80.4 |
| 15 | Roy Rockwood | 17.6 | 7 | 123.5 |
| 16 | Guy Thorne | 16.5 | 3 | 49.5 |
| 17 | Leigh Richmond | 15.3 | 3 | 45.9 |
| 18 | Neil R. Jones | 15.2 | 5 | 76.2 |
| 19 | Anthony Gilmore | 15.0 | 4 | 60.0 |
| 20 | Raymond Z. Gallun | 15.0 | 17 | 254.8 |

## By era

The best books of each era, by publication year.

**pre-1900** (121 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Across the Zodiac* (1880) | Percy Greg | 147.0 |
| 2 | *Olga Romanoff* (1894) | George Chetwynd Griffith | 114.0 |
| 3 | *The Moon-Voyage* (1872) | Jules Verne | 112.8 |
| 4 | *All Around the Moon* (1870) | Jules Verne | 110.5 |
| 5 | *A Journey in Other Worlds* (1894) | John Jacob Astor | 105.6 |
| 6 | *When the Sleeper Wakes* (1899) | H. G. Wells | 102.7 |
| 7 | *The Mummy! A Tale of the Twenty-Second Century* (1827) | Mrs. Loudon | 90.3 |
| 8 | *A Trip to Venus* (1897) | John Munro | 80.2 |
| 9 | *Pharaoh's Broker* (1899) | Ellsworth Douglass | 79.8 |
| 10 | *From the Earth to the Moon, Direct in Ninety-Seven Hours an…* (1872) | Jules Verne | 79.6 |

**1900–1945** (627 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Limanora* (1903) | Godfrey Sweven | 226.9 |
| 2 | *Ralph 124C 41+* (1911) | Hugo Gernsback | 143.4 |
| 3 | *Spacehounds of IPC* (1931) | E. E. Smith | 117.7 |
| 4 | *Skylark Three* (1930) | E. E. Smith | 110.9 |
| 5 | *The Skylark of Space* (1928) | E. E. Smith; Lee Hawkins Garby | 104.6 |
| 6 | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 100.3 |
| 7 | *Maza of the Moon* (1929) | Otis Adelbert Kline | 91.5 |
| 8 | *Through the Sun in an Airship* (1909) | John Mastin | 88.0 |
| 9 | *The Skylark of Valeron* (1934) | E. E. Smith | 87.7 |
| 10 | *A Honeymoon in Space* (1901) | George Chetwynd Griffith | 85.9 |

**1946–1979** (1711 books score)

| # | book | author | points |
|---|---|---|---|
| 1 | *Space Tug* (1953) | Murray Leinster | 83.8 |
| 2 | *Teen-age Super Science Stories* (1957) | Richard M. Elam | 82.8 |
| 3 | *The Green Millennium* (1953) | Fritz Leiber | 80.5 |
| 4 | *Venus Equilateral* (1947) | George O. Smith | 74.4 |
| 5 | *Triplanetary* (1948) | E. E. Smith | 73.7 |
| 6 | *The Planet Strappers* (1961) | Raymond Z. Gallun | 69.8 |
| 7 | *People Minus X* (1957) | Raymond Z. Gallun | 61.9 |
| 8 | *Pioneers of Space* (1949) | George Adamski | 58.8 |
| 9 | *Rip Foster in Ride the Gray Planet* (1952) | Harold L. Goodwin | 56.1 |
| 10 | *Space Platform* (1953) | Murray Leinster | 55.8 |

**1980+** (0 books score)

| # | book | author | points |
|---|---|---|---|

## Other corpus groups

The non-fiction, classics, prophecy and religious texts. Ancient and translated texts are dated by composition, the end of the scholarly range in each text's English Wikipedia article, pinned to a revision (DESIGN §1a; `runs/match/book_review.jsonl`); the second-translation re-judging of §1a is not built. Religious texts rank by text, not by translator.

| group | book | author | points | rank |
|---|---|---|---|---|
| Classics | *New Atlantis* (1627) | Francis Bacon | 63.9 | 42 |
| Classics | *Utopia* (1516) | Thomas More | 5.0 | 1414 |
| Classics | *The City of the Sun* (1602) | Tommaso Campanella | 3.8 | 1645 |
| Fiction | *Actions and Reactions* (1909) | Rudyard Kipling | 26.2 | 216 |
| Fiction | *A Diversity of Creatures* (1917) | Rudyard Kipling | 25.5 | 224 |
| Fiction | *Futility (The Wreck of the Titan)* (1898) | Morgan Robertson | 16.6 | 400 |
| Futurism | *A Hundred Years Hence (The Expectations of an Optimist)* (1905) | T. Baron Russell | 100.3 | 12 |
| Futurism | *Anticipations* (1901) | H. G. Wells | 52.2 | 62 |
| Futurism | *The Problem of Increasing Human Energy* (1900) | Nikola Tesla | 37.0 | 122 |
| Prophecy | *The Sibylline Oracles* (700) | (text) | 7.8 | 976 |
| Prophecy | *The True Prophecies or Prognostications of Michael Nostrada…* (1568) | Nostradamus | 2.0 | 2104 |
| Religion | *The Mahabharata, Volume 1 (Books 1-3)* (400) | (text) | 34.8 | 133 |
| Religion | *The Mahabharata, Volume 2 (Books 4-7)* (400) | (text) | 19.1 | 330 |
| Religion | *The Mahabharata, Volume 4 (Books 13-18)* (400) | (text) | 18.8 | 337 |
| Science | *Side-Lights on Astronomy* (1906) | Simon Newcomb | 33.9 | 140 |

## Sensitivity: points only from a score of 0.5

5,434 of 16,421 judged `will` pairs score below 0.5; without them 3,210 entries and 4,490 of 26,129 points go. Of the top 30 authors, 29 stay in the top 30; of the top 30 books, 27.

| # | author (default) | points | author (from 0.5) | points |
|---|---|---|---|---|
| 1 | E. E. Smith | 426.8 | E. E. Smith | 378.2 |
| 2 | H. G. Wells | 360.2 | Murray Leinster | 338.5 |
| 3 | Murray Leinster | 358.4 | H. G. Wells | 325.6 |
| 4 | Jules Verne | 344.2 | Jules Verne | 306.5 |
| 5 | George O. Smith | 319.2 | George O. Smith | 279.2 |
| 6 | Ray Cummings | 317.1 | Ray Cummings | 262.3 |
| 7 | Edmond Hamilton | 285.6 | Edmond Hamilton | 256.9 |
| 8 | Randall Garrett | 260.0 | Randall Garrett | 242.1 |
| 9 | George Chetwynd Griffith | 257.7 | Raymond Z. Gallun | 236.9 |
| 10 | Raymond Z. Gallun | 254.8 | John W. Campbell Jr | 220.2 |
| 11 | John W. Campbell Jr | 250.3 | George Chetwynd Griffith | 219.5 |
| 12 | Godfrey Sweven | 246.6 | Fritz Leiber | 213.2 |
| 13 | Fritz Leiber | 225.5 | Godfrey Sweven | 208.3 |
| 14 | H. Beam Piper | 217.3 | H. Beam Piper | 192.6 |
| 15 | F. L. Wallace | 202.4 | F. L. Wallace | 169.3 |
| 16 | Garrett Putman Serviss | 200.7 | Nelson S. Bond | 166.7 |
| 17 | Edgar Rice Burroughs | 196.4 | Garrett Putman Serviss | 163.9 |
| 18 | Nelson S. Bond | 186.1 | Edgar Rice Burroughs | 162.2 |
| 19 | Stephen Marlowe | 179.6 | Stephen Marlowe | 157.1 |
| 20 | Bryce Walton | 162.1 | Bryce Walton | 138.8 |

## The deciding concepts after tier 2 (PLAN §5)

592 concepts carry a top entry or add 5+ points to the author totals now; tier 2 checked 592 of them (`runs/match/deciding.jsonl` lists every concept selected for it, by round). By criterion (a concept can meet several):

- adds 5+ points to the author totals: 584
- best entry of a top-100 author: 65
- best entry of a top-100 book: 70
- lead over 40 years for 20+ claims: 64
- top-300 prediction: 129
- top-50 entry, 1900–1945: 30
- top-50 entry, 1946–1979: 20
- top-50 entry, pre-1900: 38

Their milestones: confidence high 119, low 154, medium 319; 483 have a contemporary source, 40 rest on Wikipedia alone, 148 are demonstrations only.

The 40 that carry the most points, and every one tier 2 did not check:

| concept | points | entries | lead > 40 | milestone | confidence | sources | best entry | tier 2 |
|---|---|---|---|---|---|---|---|---|
| Death ray | 506.0 | 190 | 340 | 2003-03: The US Army deployed the Zeus-HLONS, a Humvee-mounted laser, to Bagra… | medium | reference | Ray Cummings, *The Sea Girl* (1929) | checked |
| Spacesuit | 406.7 | 177 | 11 | 1969-01-16: Yevgeny Khrunov and Alexei Yeliseyev, wearing Yastreb suits with ches… | high | contemporary | Jules Verne, *All Around the Moon* (1870) | checked |
| Sleep and incapacitating gas | 376.5 | 104 | 144 | 2002-10-26: Russian special forces pumped an aerosol anesthetic (believed to be a… | high | contemporary | Manly Wade Wellman, *Warrior of Two Worlds* (1944) | checked |
| Private and personal spacecraft | 351.8 | 133 | 153 | 2021-07-20: Blue Origin NS-16: New Shepard carried Bezos, his brother Mark, Wally… | medium | contemporary | Murray Leinster, *If You Was a Moklin* (1951) | checked |
| Closed-loop life support | 337.2 | 138 | 72 | 1972-12 †: BIOS-3, Institute of Biophysics, Krasnoyarsk: crewed closure experime… | medium | reference | Hugo Gernsback, *Ralph 124C 41+* (1911) | checked |
| Radio communication with spacecraft and… | 332.5 | 208 | 25 | 1957-11-03: Sputnik 2, carrying the dog Laika, radioed telemetry of her heartbeat… | medium | contemporary | Hugo Gernsback, *Ralph 124C 41+* (1911) | checked |
| Sonic weapon | 325.6 | 99 | 155 | 2005-11-05: The cruise ship Seabourn Spirit used a long-range acoustic device (LR… | medium | contemporary | Sax Rohmer, *The Day the World Ended* (1929) | checked |
| Invisibility | 300.8 | 105 | 263 | 2010-12 †: Baile Zhang, Yuan Luo, Xiaogang Liu and George Barbastathis (MIT/SMAR… | medium | contemporary | Edgar Rice Burroughs, *A Fighting Man of Mars* (1930) | checked |
| Non-lethal stun gun | 300.4 | 123 | 16 | 1975-03: The Taser Public Defender, a flashlight-shaped dart stun gun made by… | medium | contemporary | Garrett Putman Serviss, *Edison's Conquest of Mars* (1898) | checked |
| Spacecraft video cameras and viewscreens | 273.4 | 125 | 35 | 1973: Skylab crews used the Apollo Telescope Mount video monitors in real t… | low | contemporary | (text), *Astounding Stories of Super-Scienc…* (1931) | checked |
| Crewed spaceship | 260.1 | 160 | 16 | 1961-04-12: Vostok 1 with Yuri Gagarin aboard was launched on a rocket from Baiko… | high | contemporary | Leigh Brackett, *A World Is Born* (1941) | checked |
| Video link with spacecraft and other wo… | 252.4 | 104 | 24 | 1979-03-24: The same Salyut 6 two-way TV link was used for the crew to see ground… | medium | contemporary | Otis Adelbert Kline, *Maza of the Moon* (1929) | checked |
| Electric discharge weapon | 238.8 | 112 | 48 | 1963-06-18: Alabama state troopers under Col. Albert Lingo used night sticks and… | low | contemporary | Percy Greg, *Across the Zodiac* (1880) | checked |
| Atomic or nuclear-fission rocket | 226.7 | 140 | 3 | 1959-07-01 †: Los Alamos fired the Kiwi-A reactor at the Nevada Test Site (Jackass… | high | contemporary | Nelson S. Bond, *When Freemen Shall Stand* (1942) | checked |
| Crewed orbital space station | 211.3 | 90 | 0 | 1971-06-07: Salyut 1 was used as a science station by the Soyuz 11 crew for 23 da… | high | contemporary | Damon Knight, *The Avenger* (1944) | checked |
| Walking and leaping in low gravity | 197.3 | 70 | 41 | 1969-07-21: The same Apollo 11 moonwalk was real exploration work: the crew loped… | low | contemporary | Jules Verne, *All Around the Moon* (1870) | checked |
| Spacecraft navigation instruments | 192.0 | 95 | 16 | 1968-12: Apollo 8: Lovell made over 200 sextant star and horizon navigation si… | high | contemporary | Ray Cummings, *Tama of the Light Country* (1930) | checked |
| Physical conditions on the Moon and inn… | 190.9 | 123 | 97 | 1962-12-14 †: NASA's Mariner 2 flew past Venus at 21,000 miles; its microwave and i… | medium | contemporary | Charles Napier Richards, *Atalanta* (1900) | checked |
| Crewed Moon landing | 182.2 | 92 | 41 | 1969-07-20 †: Apollo 11's lunar module Eagle landed Neil Armstrong and Buzz Aldrin… | high | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Spacecraft escape boat or lifeboat | 182.2 | 82 | 0 | 1969-07-20: Apollo 11: astronauts Armstrong and Aldrin left Columbia in the lunar… | medium | contemporary | Raymond Z. Gallun, *The Revolt of the Star Men* (1931) | checked |
| Mind-reading machine | 178.4 | 65 | 96 | 2006 †: Thirion et al. (NeuroSpin, France) decoded fMRI activity to reconstru… | medium | contemporary | Guy Thorne, *The Soul Stealer* (1906) | checked |
| Brain-computer interface | 172.9 | 62 | 55 | 1999-03: Niels Birbaumer's Tubingen group reported that completely paralysed A… | medium | contemporary | Joe Gibson, *The Machine That Floats* (1953) | checked |
| Powered rocket landing | 167.9 | 81 | 10 | 1966-06-02: NASA's Surveyor 1 landed on the Moon in Oceanus Procellarum on 2 June… | high | contemporary | Charles Willard Diffin, *Brood of the Dark Moon* (1931) | checked |
| New or sharpened human senses | 167.3 | 74 | 124 | 2004: Neil Harbisson has worn a skull-anchored antenna since 2004 that give… | low | Wikipedia only | Camille Flammarion, *Lumen* (1873) | checked |
| Brain-to-brain link | 161.4 | 54 | 67 | 2013-08-12 †: At the University of Washington on 12 Aug 2013, Rajesh Rao's EEG-read… | medium | contemporary | E. E. Smith; Lee Hawkins…, *The Skylark of Space* (1928) | checked |
| Weightlessness in spaceflight | 159.0 | 63 | 36 | 1961-04-12 †: Yuri Gagarin orbited the Earth in Vostok 1 and floated weightless in… | high | contemporary | Jules Verne, *From the Earth to the Moon, Direct…* (1872) | checked |
| Three-dimensional telepresence | 154.2 | 48 | 67 | 2022: Google began testing Project Starline with partner companies such as… | low | Wikipedia only | Frank Belknap Long, *Woman from Another Planet* (1960) | checked |
| Self-driving car | 150.8 | 46 | 56 | 2020-10-08: Waymo opened its fully driverless ride-hailing service (Waymo One, no… | medium | contemporary | Robert Hugh Benson, *The Dawn of All* (1911) | checked |
| Spaceport | 150.7 | 113 | 0 | 1957-10-04: Baikonur Cosmodrome (founded 1955) launched Sputnik 1, the first spac… | medium | contemporary | Raymond F. Jones, *The Seven Jewels of Chamar* (1946) | checked |
| Jetpack or flying suit | 147.8 | 53 | 41 | 1984-04-08: Astronaut George Nelson flew the Manned Maneuvering Unit (a worn nitr… | medium | contemporary | William Richard Bradshaw, *The Goddess of Atvatabar* (1892) | checked |
| Space-suit helmet radio | 147.1 | 57 | 2 | 1965-03-18 †: Alexei Leonov, outside Voskhod 2 in his suit, stayed in radio contact… | medium | contemporary | Philip Francis Nowlan, *Armageddon—2419 A.D.* (1928) | checked |
| Growing food in space | 145.0 | 54 | 8 | 1975-07-08 †: Salyut 4 cosmonauts Klimuk and Sevastyanov ate onions grown in the Oa… | medium | contemporary | Jules Verne, *The Moon-Voyage* (1872) | checked |
| Service robot for the public | 144.2 | 51 | 2 | 1983: The Two Panda Deli (Two Panda Robot Restaurant) in Pasadena, Californ… | medium | contemporary | Lloyd Biggle Jr., *Cronus of the D. F. C.* (1957) | checked |
| Machinery-disabling ray | 140.2 | 69 | 15 | 1962-07-09 †: Starfish Prime high-altitude nuclear test (Johnston Atoll, 9 July 196… | low | reference | George Allan England, *The Flying Legion* (1919) | checked |
| Automated kitchen | 138.4 | 50 | 55 | 2016-04: Spyce's robotic kitchen, built by MIT students, was cooking and servi… | low | contemporary | Mrs. Loudon, *The Mummy! A Tale of the Twenty-Se…* (1827) | checked |
| Nerve-attacking weapon | 138.2 | 57 | 11 | 1975-03: Taser Public Defender first marketed in March 1975 by Taser Systems /… | medium | contemporary | Owen Johnson, *The Coming of the Amazons* (1931) | checked |
| Astronaut maneuvering gun or pack | 137.4 | 53 | 1 | 1966-07-19: Michael Collins used the nitrogen-fed HHMU on Gemini 10 to transfer f… | medium | contemporary | Edwin K. Sloat, *Loot of the Void* (1932) | checked |
| Physiological effects of spaceflight | 136.7 | 83 | 15 | 1961-08-06 †: Gherman Titov, in Vostok 2 (launched 6 August 1961), became the first… | high | contemporary | Hugo Gernsback, *Ralph 124C 41+* (1911) | checked |
| Sleep learning | 136.5 | 38 | 44 | 2019-02 †: Zust et al. (University of Bern) played recorded pseudoword/German wo… | low | contemporary | Fritz Leiber, *Appointment In Tomorrow* (1951) | checked |
| Search for extraterrestrial signals | 136.0 | 67 | 65 | 1960-04: Frank Drake's Project Ozma used the 85-foot Green Bank radio telescop… | medium | contemporary | Garrett Putman Serviss, *Other Worlds* (1901) | checked |
