# Research orders for Sonnet 5.5 Extra or Opus 5.5 (written by Fable, 10 Nov 2026)

Fable did almost no web research in run 1 (budget). These are the questions worth asking, each tied to a decision. Run them as numbered stints in `research/research-sessions.md`.

## How to run every stint (short form of `research/RESEARCH-BLUEPRINT.md`)
1. Write the cap FIRST, in tool calls (not minutes): 25 calls is about 0.5 weekly points under 300K context. Stop at the cap, even mid-question.
2. Our own data first: if a script on files we hold can answer it, write the script instead.
3. Primary sources only: arXiv abstract and HTML pages, mission pages, archive documentation. A search summary is a lead, not a source. Never open a PDF link in the browser pane; fetch with Python into a new folder under `data\` and log it in `research/downloads.csv`.
4. For every answer: the exact sentence, the URL, the date read, a label (CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED).
5. End with: what changes in our plan, and which queue item it becomes. No plan change means the question was not worth asking; say so.
6. Fresh session per stint. One page of output.

## RS-013: unsearched archives (Sonnet, cap 25 calls) [decides: is there a second data source for 2027]
1. Has anyone published a systematic transit search for circumbinary planets in **K2** eclipsing binaries? Which K2 eclipsing-binary catalogues exist, and how many systems have period over 5 d and Kp under 14?
2. **PLATO:** current launch date; when is the first public data; does the LOPS2 field overlap the TESS southern continuous viewing zone; is a circumbinary programme already planned (so we would be late)?
3. Has anyone searched the **TESS continuous viewing zone** eclipsing binaries specifically for circumbinary transits beyond the TOI-1338 team (Kostov et al., the "TESS circumbinary" papers, Martin et al. BEBOP)? What did they cover and what did they leave?
Plan change if yes or no: whether K2 or the viewing zones go on the 2027 roadmap.

## RS-014: M-dwarf hosts (Sonnet, cap 20 calls) [decides: stratum or nothing in G5]
1. Any published transiting circumbinary planet or candidate around an M-dwarf eclipsing binary?
2. Giant-planet occurrence around single M dwarfs (one or two recent TESS or radial-velocity numbers with intervals).
3. How many detached M-dwarf eclipsing binaries with period over 5 d are known brighter than Tmag 14 (catalogue counts)?

## RS-016: how the professionals mask eclipses (Opus, cap 25 calls) [decides: the Petrova 1.0 mask design]
This is the most important stint. Our frozen mask deletes planet dips in slow binaries (audit F-01).
1. Kostov et al. 2020 (TOI-1338) and Kostov et al. 2021 (TIC 172900988): how were eclipses removed before looking for transits? Exact method sentences.
2. Martin and Fabrycky 2021 ("Searching for small circumbinary planets", the Stanley pipeline) and Windemuth et al. 2019: eclipse removal and detrending; how they treat a dip that appears once.
3. Armstrong et al. 2014: how eclipses were masked in the Kepler occurrence study, and how completeness was injected (before or after masking?).
4. Any paper that reports losing transits to an eclipse mask or to detrending near eclipses.
Deliver: a table "paper, mask method, single-dip handling, injection point". Compare with `design/PETROVA-1.0-MASK-DESIGN.md` and say what we should copy.

## RS-017: the occurrence anchor (Opus, cap 20 calls) [decides: every E and the Census odds]
1. Armstrong et al. 2014: the exact definition of the "about 10%" (radius range, planet period range, binary period range, coplanarity assumption).
2. Newer estimates: Martin and Triaud 2014, Li, Holman and Tao 2016, any 2020 to 2026 TESS-based rate. Does any give a rate as a function of BINARY period? (Known hosts cluster above 7 d; our stars are mostly 5 to 20 d.)
3. Is the pile-up of planets just outside the stability limit quantified (share of planets within a factor 1.5 of the limit)? This sets where to look in period.

## RS-018: transit duration against binary phase (Opus, cap 15 calls) [decides: WO-F22, a free vetting key]
1. Doyle et al. 2011 (Kepler-16) and Welsh et al. 2012 (Kepler-34, 35): the sentences and formula for how transit duration depends on the binary phase.
2. Has this been used as an automatic vetting test in any pipeline (Stanley; Kostov's by-eye work)?

## RS-019: Gaia DR4 contents (Sonnet, cap 15 calls, NOT before 2 December 2026) [decides: the G5 list, WO-F13]
1. Is there an eclipsing-binary table in DR4, with how many rows, and are epoch photometry time series public for all sources?
2. Stated period accuracy for long-period eclipsing binaries; known alias periods of the scanning law in DR4.

## RS-020: QLP flags from Sector 94 (Sonnet, cap 10 calls) [decides: WO-F02]
The meaning of QUALITY bit 29 (value 536870912) in TGLC-based QLP light curves; the full bit table for Sector 56+ and Sector 94+.

## RS-021: the leap-of-faith idea, "binaries that do not eclipse" (Opus, cap 30 calls) [decides: whether a whole new star pool opens]
Fable's closing note to Ahmed proposes a transit search for circumbinary planets around NON-eclipsing spectroscopic binaries (Gaia's catalogue of spectroscopic orbits), which are bright, far more numerous than eclipsing ones, and need no eclipse mask. A planet can transit one star even when the stars never eclipse each other, if the system is close to edge-on. Fable's numbers are rough and from memory (UNCERTAIN). Questions:
1. Martin and Triaud 2015 ("Circumbinary planets: why they are so likely to transit") and Martin 2017 ("when transits come and go"): the exact statements on transits in non-eclipsing binaries, the share of such planets that are transiting at a given time as a function of binary inclination and mutual inclination, and the time scale of the precession.
2. Is any transiting circumbinary planet known around a non-eclipsing binary? Has anyone published a transit search of spectroscopic binaries in Kepler, K2 or TESS for this purpose? (BEBOP is radial velocity; check its papers for a photometric arm.)
3. Gaia DR3 non-single-star tables: number of SB1 and SB2 orbits with period 5 to 50 d and G under 12 and under 13; stated reliability of those periods; which solutions give an inclination. After 2 Dec 2026: the same for DR4.
4. Arithmetic, in a script: expected detections per 1,000 such stars = (share within a few degrees of edge-on) x (planet rate 10%) x (share transiting now, from question 1) x (TESS window for a planet period of 5.6 binary periods or more) x (our completeness for giants at that brightness). Compare with our eclipsing value of about 1 per 1,000 G2-type stars.
5. The catch to test: a non-eclipsing binary gives no eclipse to prove the system is edge-on, and a single dip on a bright star has many other causes. What second key exists (radial velocities already in Gaia, the duration key of WO-F22, a second transit)?
Plan change: if question 4 gives under a fifth of the eclipsing value per star, the idea is dead; if it is within a factor 3, it becomes a pilot on a few thousand stars after Petrova 1.0. Do not physically assume the reverse idea (eclipse depth changes caused by a planet): a planet is too light to tilt the binary's orbit measurably; it is the planet's orbit that precesses.
