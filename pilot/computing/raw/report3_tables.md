## Network check

| Host | Status | Seconds |
|---|---|---|
| books.google.com | 404 | 0.2 |
| www.googleapis.com/books/v1 | 429 | 0.3 |
| www.worldradiohistory.com | 200 | 0.5 |
| www.worldradiohistory.com (PDF) | 200 | 1.3 |
| bitsavers.org | 200 | 1.3 |
| bitsavers.org (PDF) | 200 | 0.5 |
| archive.computerhistory.org | 404 | 1.2 |
| www.computerhistory.org | 200 | 0.5 |
| ethw.org | 200 | 0.3 |
| spectrum.ieee.org | 200 | 0.3 |
| ieeexplore.ieee.org | 202 | 0.2 |
| *.si.edu (www.si.edu) | 403 | 0.2 |
| *.si.edu (airandspace.si.edu) | 200 | 0.3 |
| *.nasa.gov | 200 | 0.2 |
| ntrs.nasa.gov | 200 | 0.4 |
| pmc.ncbi.nlm.nih.gov | 200 | 0.3 |
| pubmed.ncbi.nlm.nih.gov | 200 | 1.0 |
| www.nature.com | -1 | 0.6 |
| api.crossref.org | 200 | 0.4 |
| api.semanticscholar.org | 429 | 0.2 |
| babel.hathitrust.org | 403 | 0.2 |
| archive.org (OCR text) | 200 | 2.4 |
| archive.org | 200 | 0.6 |
| archive.org full-text | 200 | 0.4 |
| www.smithsonianmag.com | 403 | 0.3 |
| www.aip.org | 200 | 0.9 |
| www.hagley.org | 200 | 0.6 |
| www.thehenryford.org | 200 | 0.9 |
| www.nobelprize.org | 200 | 0.6 |
| *.mit.edu | 200 | 0.2 |
| www.britannica.com (expected 403) | 403 | 0.2 |

Hosts of the verified sources of the target milestones (all kinds):

| Host | Sources |
|---|---|
| archive.org | 61 |
| en.wikipedia.org | 40 |
| api.crossref.org | 6 |
| unicog.org | 2 |
| pmc.ncbi.nlm.nih.gov | 2 |
| archive.computerhistory.org | 1 |
| api.semanticscholar.org | 1 |

## The 33 target concepts: the ranking's milestone

R = decided in raw/review3.jsonl; C = confirmed and X = replaced by the earliest-event check.

| Concept | Kind | Second pass | Third pass | Event | Sources | Confidence | Fit |
|---|---|---|---|---|---|---|---|
| Mind-reading machine | demonstration | 2008 (demo.) | **2006** R | Thirion, Duchesnay, Hubbard, Dubois, Poline, Lebihan and Dehaene (NeuroSpin, France) decoded fMRI activity to reconstruct the visual pattern that subjects were only imagining, using inverse retinotopy and supervised classifiers (NeuroImage 33(4), 2006). | 1 contemporary | low | From brain activity alone, a machine reconstructed the specific pattern a person was imagining (crude flickering-pattern shapes from a small set), not just its category. |
| Thought-to-text and thought display | demonstration | 2020 (demo.) | **2006** RX | Thirion, Duchesnay, Hubbard, Dubois, Poline, Lebihan and Dehaene (NeuroSpin, France) decoded fMRI activity to reconstruct the visual pattern that subjects were only imagining, using inverse retinotopy and supervised classifiers (NeuroImage 33(4), 2006). | 1 contemporary | low | From brain activity alone, the machine reconstructed an image the person was holding in mind (a mental image, not a displayed stimulus), shown as a reconstructed pattern; the images were crude flickering-pattern shapes. |
| Central computer directing many robots | practical use | 2007 (prac.) | **1974** RC | Volvo Kalmar assembly plant in regular production use of its fleet of computer-guided carriers. | 2 contemporary | low | The plant's fleet of computer-guided carriers did its production work, and all of them could be directed from one central computer. |
| Brain-computer interface | practical use | 1998 (prac.) | **1998**  | Philip Kennedy and Roy Bakay implanted a neurotrophic-cone electrode in the motor cortex of the locked-in patient Johnny Ray, who learned to control a computer cursor to communicate. | 1 contemporary, 1 reference | medium | A paralyzed person used signals from his own brain, via an implanted electrode, to control a computer, for the real purpose of communicating when he could not move. |
| Automatic dictation transcription | practical use | 1990 (prac.) | **1986-12** C | Kurzweil Applied Intelligence officially released its 1,000-word Voicerad system in Boston in December 1986; a radiologist was already writing his reports with it by voice. Dragon Systems had announced Voicescribe-1000 'automatic dictation transcription system' in June 1986. | 2 contemporary | medium | A computer listens to a user's spoken dictation of reports and produces the edited, printed text, used by a working radiologist. |
| Immersive virtual reality | practical use | 1990 (prac.) | **1990**  | VPL Research's Reality Built for Two (EyePhone head-mounted display plus DataGlove) was sold and in use at outside sites, and W Industries' Virtuality 1000SU VR systems were launched and sold to corporations such as BT, Ford and IBM. | 1 contemporary, 1 reference | medium | Commercial head-mounted systems that put a user inside a computer-generated, head-tracked 3D world were delivered to paying customers for research, design and training. |
| Retina and iris recognition | practical use | 1981 (demo.) | **1984**  | EyeDentify 7.5 retinal scanner in use as an access-control device; a 1985 Naval Postgraduate School thesis tested the 7.5 system (dated 1984 model) and Computerworld 1986 reports a Dallas vault firm using it at its guard door. | 2 reference | low | Machine identifies people at an entrance by scanning retinal vessel patterns, used for real access control. |
| Speech recognition and voice command | practical use | 1984 (prac.) | **1972** C | Threshold Technology (Delran/Cinnaminson, NJ) brought out the VIP-100 isolated-word recognizer and had voice-input terminals working in industrial, government and military 'real-world' use from late 1972. | 1 contemporary, 1 reference | medium | Spoken words were recognized by a commercial machine and used to enter data and give commands to a computer in working environments, outside the laboratory. |
| Automated face recognition | practical use | 1997 (prac.) | **1994** C | By 1994 facial-recognition biometric products had reached the marketplace (access control); the DMV offices of West Virginia and New Mexico followed, using automated face recognition against duplicate licences after the 1993 FERET test. | 1 contemporary, 1 reference | low | Commercial systems used cameras and computers to match a person's face against an enrolled stored image for entry control and identity checks. |
| Computerized information retrieval | practical use | 1966 (prac.) | **1967-05**  | Ames Research Center began using a DIALOG-fed remote terminal linked by telephone to Lockheed's computer (Summit's project under NASA contract). | 1 contemporary | low | Real users (NASA Ames) searched a large technical-literature file by remote terminal and got references in minutes. |
| Fully automated factory or plant | practical use | 2001 (prac.) | **2001** R | Fanuc's robot plant near Mount Fuji runs lights-out, robots building robots, unsupervised for up to 30 days. | 1 reference | low | Fanuc's robots built robots in a plant that ran unsupervised for up to 30 days: a factory that runs with few or no human workers, though people still maintain it. |
| Speech synthesis | practical use | 1976 (prac.) | **1976**  | The Kurzweil Reading Machine (scanner plus Votrax synthesizer reading printed pages aloud to blind people) was introduced in early 1976, the same year as Telesensory Systems' Speech+ talking calculator for the blind. | 1 contemporary, 1 reference | low | A computer converted text into phonetic commands for an electronic voice synthesizer that spoke the text aloud, for blind users' real reading needs. |
| Robot police and security guards | practical use | 2015 (prac.) | **1986** C | Denning Mobile Robotics' Sentry, marketed as an autonomous mobile security robot guard patrolling warehouses; prison units ordered by Southern Steel (600 ordered, 8 in advanced testing in late 1985). | 2 contemporary | low | A robot that patrols facilities on its own and alerts authorities to intruders, sold to customers for real guard duty. |
| Machine-readable identity and access card | practical use | 1968 (prac.) | **1961** C | Line Material Industries (McGraw-Edison) used the IBM 357 data collection system in which each employee inserts his identification card at a station, the machine records who he is and his time and attendance. | 1 contemporary | low | A machine reads each employee's ID card in daily factory use to identify him and record attendance and production against his name. |
| Companion or sex robot | practical use | 1999-06-01 (prac.) | **1998-10-02** C | Furby went on general sale in the United States (launched 2 October 1998, with a press event at FAO Schwarz, New York), selling 1.8 million in 1998. | 2 contemporary, 1 reference | low | The robotic pet toy was bought and kept by ordinary families as a companion that responds to touch and sound. |
| Question-answering computer | practical use | 1993 (demo.) | **1993** C | MIT's START went online on the Internet in 1993 and answered English questions from the public on many topics (Boris Katz) | 1 reference | low | A publicly reachable computer answering ordinary-language factual questions on many topics, used by outside people for that purpose; knowledge is hand-annotated so breadth is limited. |
| Machine-generated writing | practical use | 1990 (prac.) | **1990**  | Environment Canada used FoG, a system that generated weather forecast texts in English and French from numeric weather data, in its forecast operations. | 1 contemporary | low | Software wrote finished forecast texts from data with no human writer, in daily operational service. |
| Three-dimensional holographic display | practical use | 1972 (prac.) | **2009** RC | The Actuality Systems Perspecta Spatial 3D volumetric display was integrated with a clinical radiation-therapy planning system (Pinnacle) so that planners could view patient anatomy and beams in 3D from any side. | 2 reference | low | A swept-volume display showing changing patient-derived 3-D images in a 25 cm volume viewable from any side, used for its real purpose in treatment planning. |
| Touchscreen and gesture interface | practical use | 1972 (prac.) | **1972**  | PLATO IV terminals at the University of Illinois (1972) had a built-in 16x16 infrared touch panel that students used to answer questions in lessons | 1 contemporary, 1 reference | medium | Students controlled a teaching computer by touching its screen, a touch-panel input used for its real purpose (instruction) outside the lab. |
| Computer screen display | practical use | 1951 (prac.) | **1951**  | Project Whirlwind at MIT, operational from 1951, plotted letters, figures and graphics on CRT scopes for its users and showed radar data for the Cape Cod air-defence tests. | 1 contemporary, 1 reference | low | A real-time computer shows its results as text and graphics on screens to working users in place of printouts and dials. |
| Machine learning | demonstration | 1951 (demo.) | **1929-07** X | Clark L. Hull and H. D. Baernstein (Yale) built an electrochemical machine (polarizable cells and mercury-toluene thermal regulators, switches as receptors, a flashlight bulb as responder) that acquired conditioned responses from the sequence of stimuli it received, reported in Science, 5 July 1929. | 2 contemporary | medium | The machine changed its response from the experience of paired stimuli (a neutral switch came to light the bulb after training, with extinction, forgetting and spontaneous recovery) instead of being wired for that response. |
| Robot vacuum cleaner and lawn mower | practical use | 1969 (prac.) | **1969**  | MowBot went on sale to the public in 1969 (about $800), first commercial autonomous lawn mower | 1 contemporary, 1 reference | medium | Customers used the machine for its real purpose, mowing lawns without being driven. |
| Electronic book reader | practical use | 1990 (prac.) | **1990-07** C | The same Sony Data Discman DD-1 went on sale in Japan in July 1990 as an 'electronic book' player for reference works. | 1 contemporary, 1 reference | medium | A pocket-size battery device with its own LCD that shows the text of books and reference works stored on a 3-inch CD, replacing paper. |
| 3D printing | practical use | 1987 (prac.) | **1987-05**  | 3D Systems announced its stereolithography system (laser-cured acrylic resin, computer-controlled platform) as a product letting architects make detailed building models in minutes (Progressive Architecture, May 1987). | 1 contemporary, 1 reference | medium | A commercial machine built solid models automatically from computer sections of a design, layer by layer in photo-curing resin, for real design work. |
| Real-time computerized situation display | practical use | 1958-06-26 (prac.) | **1958-06**  | The SAGE New York Air Defense Sector, with its AN/FSQ-7 computer and operator display consoles at McGuire Air Force Base, was declared operational (27 June 1958 per Bell Telephone Magazine, 26 June per Wikipedia). | 1 contemporary, 1 reference | medium | An operational air-defense centre in which a computer fed by radar showed live aircraft tracks on operators' screens for real interception control. |
| Neural implant and cyborg augmentation | practical use | 1977-12 (prac.) | **1977-12**  | Hochmair's multichannel cochlear implant was first implanted in a person in Vienna in December 1977; Clark's followed in 1978 and was commercialized as Nucleus. | 1 reference | low | Implanted electronic device used in patients to restore hearing for real-world use. |
| Spacecraft guidance and navigation computer | practical use | 1965-03-23 (prac.) | **1965-03-23**  | The same Gemini III flight used the computer on a real crewed mission for navigation and reentry guidance; routine mission use (rendezvous burns) followed on Gemini 6A/7 in December 1965. | 1 contemporary | low | An onboard digital computer navigated the spacecraft and computed steering (bank) commands, which the crew flew, to fly the entry path to a landing target; on Gemini III it also generated the data for orbit-changing burns, so it calculates and steers, with the crew closing the loop. |
| Computer-run space station | practical use | 1973-05-14 (demo.) | **1973-05-25**  | The first Skylab crew (Skylab 2) arrived 25 May 1973 to a station whose onboard computer was handling attitude control and pointing; the computer kept running the station through all three crewed missions (e.g. it reconfigured to two control gyros after a gyro failure in 1973). | 1 contemporary, 1 reference | low | The computer-run systems were used for the station's real purpose with crews aboard, including automatic reconfiguration on failure; same partial fit as the demonstration. |
| Service robot for the public | practical use | none | **1985** R | The Two Panda Robot Restaurant in Pasadena, California, used two robots, Tanbo R-1 and Tanbo R-2, as waiters that took orders from diners (described in a 1985 National Geographic Society book). | 2 contemporary | low | Robots served a restaurant's customers as waiters, for the restaurant's real business. |
| Computerized personnel selection and aptitude testing | | none | none | | | | |
| Sleep learning | demonstration | none | **2019-02** R | Zust et al. (University of Bern) played recorded pseudoword/German word pairs to young adults in slow-wave sleep and found they had formed and kept new word associations that showed up on an implicit test after waking. | 1 contemporary | low | Recorded vocabulary was played to sleeping people and they retained new verbal associations from it, so teaching by recorded sound during sleep worked, though only for implicit word-pair associations and not for general lessons. |
| Computerized marketing and consumer analytics | practical use | none | **1961-08**  | American Investment Company (St. Louis), with Fair, Isaac and Company, announced a credit-scoring system for rating consumer loan risks, made practical by an electronic computer installed at its headquarters. | 1 contemporary | low | A computer-based statistical model scores customers (loan applicants) to predict their behaviour (repayment), i.e. the 'score customers' part of the definition; it does not cover audience measurement or purchase prediction. |
| Voiceprint speaker recognition | practical use | none | **1974** R | Texas Instruments controlled access to its Corporate Computer Center by automatic voice authentication (speaker verification), in operation 24 hours a day; a 1977 report says it had done so for the past three years. | 1 reference | low | A machine verified each person's identity from their voice to admit them to a computer center, in real daily use. |

## Source kinds (target concepts, demonstration and practical-use milestones)

| Pass | Milestones | With a contemporary source | Sources by kind |
|---|---|---|---|
| second | 47 | 1 | contemporary 1, reference 56, wikidata 1 |
| third | 55 | 46 | contemporary 58, reference 39 |

## Second judge: agreement with the first

| Group | Pairs | Same score | One step apart | Two or more apart | Second judge lower | Second judge higher |
|---|---|---|---|---|---|---|
| top100 | 100 | 43 | 52 | 5 | 56 | 1 |
| random50 | 50 | 32 | 18 | 0 | 11 | 7 |

Outcome for the top-100 and 1.0 pairs: agreed 43, lower 52, median 5.
Scores changed (first judge -> final): 0.5 -> 0.25: 15, 0.75 -> 0.25: 4, 0.75 -> 0.5: 36, 1 -> 0.75: 1.

## Top 20 (951 book-concept entries with points)

| # | Was | Year | Concept | Milestone | Lead | Judges | Score | Points | Quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 19 | 1952 | Fully automated factory or plant | 2001 | 49 | 0.75/0.75 | 0.75 | 4.23 | It was powered by an atomic pile, stocked with materials which, when combined with the returning, worn-out robots, enabled it to keep producing indefinitely. |
| 2 | 22 | 1953 | Brain-computer interface | 1998 | 45 | 0.75/0.75 | 0.75 | 4.14 | even mechanisms which would react selectively to the electrical impulses generated by the cells of the human brain! |
| 3 | 23 | 1954 | Brain-computer interface | 1998 | 44 | 0.75/0.75 | 0.75 | 4.12 | What the helmet did was detect and sidetrack the motor impulses from my brain, broadcasting their pulsations by short wave radio to the robot, which … |
| 4 | 3 | 1949 | Immersive virtual reality | 1990 | 41 | 1/0.75 | 0.75 | 4.04 | a movie that gives one sight and sound. Suppose now I add taste, smell, even touch, if your interest is taken by the story. Suppose … |
| 5 | 29 | 1960 | Brain-computer interface | 1998 | 38 | 0.75/0.75 | 0.75 | 3.96 | As he did this, the electro-chemical change in a nervous tract triggered a tiny implanted device that sent its imperceptible signal to the mataform transceiver. |
| 6 | 44 | 1948 | Retina and iris recognition | 1984 | 36 | 0.75/1.0 | 0.75 | 3.91 | Kinnison dashed up to an apparently blank wall, turned his back upon four commissioned officers holding cocked forty-fives at the ready, and fitted his right … |
| 7 | 51 | 1952 | Retina and iris recognition | 1984 | 32 | 0.75/0.75 | 0.75 | 3.78 | Hold this up to your left eye for twenty seconds." He extended a flat, glittering little metal disk. "It's already sensitized and filled out. It … |
| 8 | 5 | 1962 | Automated face recognition | 1994 | 32 | 0.75/0.75 | 0.75 | 3.78 | a scanning device in the wall fastened its attention on them, simultaneously checking through a large store of previously registered human images and data associated … |
| 9 | 48 | 1958 | Automatic dictation transcription | 1986-12 | 28 | 0.75/0.75 | 0.75 | 3.64 | Jean-Jean turned away and began furiously talking at the Speak-a-Type, which rattled and stuttered as the type keys tried to keep up with her. |
| 10 | new | 1958 | Service robot for the public | 1985 | 27 | 0.75/0.75 | 0.75 | 3.61 | A robowaiter approached them, holding a menu board in its metal hands. |
| 11 | 55 | 1962 | Automatic dictation transcription | 1986-12 | 24 | 0.75/0.75 | 0.75 | 3.48 | An earphone reproduced Smith's dictation from his tape. As she listened, she edited mentally and spoke into the microphone of her typing machine, which transcribed … |
| 12 | new | 1953 | Voiceprint speaker recognition | 1974 | 21 | 0.75/0.75 | 0.75 | 3.34 | The living voice can't be imitated so as to get past the sound analyzers. Humans must be on the flagship. |
| 13 | new | 1953 | Voiceprint speaker recognition | 1974 | 21 | 0.75/0.75 | 0.75 | 3.34 | Old Rubberarm's got your voice pattern. Just ask for Juno Jones. |
| 14 | 46 | 1951 | Speech recognition and voice command | 1972 | 21 | 0.75/0.75 | 0.75 | 3.34 | We get in the elevator, and I say "first" to it. It gives out a coughing noise and the basement openings begin to click by … |
| 15 | 69 | 1897 | Brain-computer interface | 1998 | 101 | 0.5/0.5 | 0.5 | 3.34 | father says some day we may be able to work by sheer will power directly and have no need of hands at all. |
| 16 | 1 | 1906 | Thought-to-text and thought display | 2006 | 100 | 0.5 | 0.5 | 3.33 | I find that the thought images thrown upon the screen in room "D" are more vivid when the subject is kept in darkness. |
| 17 | 68 | 1906 | Mind-reading machine | 2006 | 100 | 0.5/0.5 | 0.5 | 3.33 | I am going to show you how thought can be collected in the form of vibrations, in the form of fluid electric current, and collected … |
| 18 | 74 | 1912 | Brain-computer interface | 1998 | 86 | 0.5/0.5 | 0.5 | 3.22 | the outer doors are manipulated by telepathic means. The locks are so finely adjusted that the doors are released by the action of a certain … |
| 19 | 50 | 1954 | Speech recognition and voice command | 1972 | 18 | 0.75/0.75 | 0.75 | 3.19 | He learned about saying 'Open' to a lock and having the electronic device 'recognize' him and let him in. |
| 20 | 75 | 1905 | Automatic dictation transcription | 1986-12 | 81 | 0.5/0.5 | 0.5 | 3.18 | we may essay the more difficult task of conceiving a means by which the spoken word may be directly translatable into print or typewriting. |
