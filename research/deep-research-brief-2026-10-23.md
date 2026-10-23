# Second Sun: deep research brief (for a research-focused Claude)

*Written 2026-10-23 by Claude Code (the assistant that writes and runs our code) for Ahmed Hanzala to give to Claude with research and web search. Take hours if you need them. This is the last outside review before the real search starts, so be thorough and be hard on us.*

---

## 0. Who we are and what we need from you

I am Ahmed, a beginner citizen scientist. With an AI coding assistant (Claude Code, which has limited web access) I am searching public NASA TESS data for a **new transiting circumbinary planet**: a planet that orbits two stars and passes in front of one of them as seen from Earth.

We have built a pipeline, tested it honestly on one known planet, written a teaching book and kept careful records. Before we search our 549 real target stars, we want a **second, independent mind** to find what we have missed: wrong assumptions, bugs, better methods, overlapping work by professionals, data we have not used, and realistic ways to produce something publishable even if no planet turns up.

**You can do things our coding assistant cannot:** read full papers, follow citations, open catalogues (VizieR, MAST, ExoFOP, NASA Exoplanet Archive), read our public code on GitHub, and spend hours cross-checking.

## 1. Rules for your answer (please follow exactly)

1. **Tag every factual statement**: `[READ]` = you opened the primary source in this session and it says this; `[MEMORY]` = from training, not opened now; `[INFERRED]` = your own reasoning. Never invent a citation, number, URL, author or quote. If you cannot open something, say "could not open" and give the exact search.
2. **For every source**: authors, year, title, journal, ADS bibcode or arXiv id or DOI, URL, and the table, figure, section or sentence you relied on. We will check every citation in ADS. Another AI recently gave us 12 citations; 1 was invented and 6 had a wrong identifier or wrong content. Please do better.
3. **When you criticise our code**, name the file and the function (and line numbers if you can), say what is wrong, why, and how you would test it. Separate "this is a bug" from "this is a design choice I would make differently".
4. **No flattery.** We would rather hear "this will not work because..." now.
5. **Plain English** where possible (I am learning), but keep the technical precision. Equations are fine if each symbol is explained.
6. **Do not contact anyone, post anything or submit anything anywhere.** Research only.
7. **Do not paste GPL-licensed code** into suggestions; our repo is MIT. Linking to GPL tools is fine.
8. Long is fine. Structure it with the headings in section 9.

## 2. Where everything is (public)

- Repo (MIT): https://github.com/M1Smacker/second-sun
- Teaching book (public, not indexed by search engines): https://m1smacker.github.io/second-sun/
- Most important files (all under `https://github.com/M1Smacker/second-sun/blob/main/`):

| File | What it is |
|---|---|
| `RESEARCH-PLAN.md` | Founding decisions and goals |
| `RESUME.md` | Current status and what is on hold |
| `pipeline/detect_v2.py` | **The detector** (load, eclipse mask, detrend, box search, events, vetoes). Read this first. |
| `pipeline/accept_v2.py`, `pipeline/accept_v2_results.json` | Acceptance tests of the detector on TOI-1338 (known planet, injections, flipped-data false alarms) |
| `pipeline/diag_v2.py`, `pipeline/veto_test.py`, `pipeline/veto_dist.py` | Diagnostics and the veto (flag) tests |
| `pipeline/dryrun_kepler16.py`, `pipeline/dryrun_kepler16_results.json` | First dry run on a real G1 star (Kepler-16) |
| `pipeline/stanley/inject_cbp.py`, `pipeline/stanley/run_search.py`, `pipeline/recover_cbp.py` | Realistic fake circumbinary planets (N-body timing via STANLEY) and recovery |
| `pipeline/targets_g1.py`, `targets/g1_targets.csv`, `targets/g1_coverage.csv` | **Our 549-star target list** (KIC, TIC, Tmag, binary period, epoch, morphology) and which TESS products exist for each |
| `pipeline/qlp_check.py`, `pipeline/borrow_windows_check*.py` | Handling of QLP light curves (fainter stars) |
| `experiments/quality_mask/SPEC.md` and `results/.../summary.md` | Pre-registered experiment: PDCSAP vs SAP flux and quality masks |
| `research/overnight-science/report.md` | The main science report (detector v2, injections, false alarms) |
| `research/wave-1-gap-check/*/report.md` | Census of known circumbinary planets, who else searches, catalogues |
| `research/burn-2-reading/report.md` | Competition and overlap analysis (Davies et al. 2026, Tufts/Martin XRP project) |
| `research/wave-4-vetting/report.md` | Vetting methods and tools we mapped |
| `research/wave-5-credit/report.md` | Credit, publishing, citizen-science norms |
| `book/data/claims.csv` | Our fact register (every number with source and label) |
| `research/mistakes.md`, `research/decisions.md`, `research/predictions.md` | Our mistakes, decisions and dated predictions |
| `research/compass-reviews/` | Our internal reviews, including of Gemini's advice |

## 3. The project in short

- **Goal**: find a new transiting circumbinary planet in public TESS data, write it up, and get credit, with Ahmed making the final yes/no on every candidate (two-key rule with the AI).
- **Known population**: 14 transiting circumbinary planets (12 Kepler, 2 TESS: TOI-1338 b and TIC 172900988 b), following Davies et al. 2026 (ADS 2026MNRAS.548ag743D).
- **Campaign G1 (the idea)**: the Kepler mission (2009 to 2013) catalogued thousands of eclipsing binaries in one patch of sky (Cygnus and Lyra). TESS has re-observed that patch in many sectors since 2019. Circumbinary orbits precess, so a planet that never crossed during Kepler may cross now. Kepler-453 b, for example, transits only about 8.9% of its roughly 103-year precession cycle (Welsh et al. 2015, ApJ 809, 26).
- **G1 list**: from the Villanova Kepler EB catalogue (revision 2019-08-08, 2,921 rows): morphology < 0.5 (detached), binary period > 5 days, TESS magnitude ≤ 13.5. Result: 552 rows, **549 stars**. All 549 have QLP light curves; 275 have SPOC 2-minute; 312 have TESS-SPOC. **136 rows have morphology = -1 ("not measured")**, which our cut let through by accident; we plan to keep them and measure their eclipses ourselves.
- **Status**: the real search of the 549 has NOT started (on hold by Ahmed's choice). Only TOI-1338 (a known planet host) and one dry run on Kepler-16 have been run.

## 4. How our detector works (please check this against the code)

`pipeline/detect_v2.py`, per TESS sector:
1. **Flux**: SPOC PDCSAP, with gaps filled from SAP scaled locally. QLP for stars without SPOC.
2. **Quality**: drop cadences using lightkurve's "hard" bitmask (24319). (Default is 17087; they differ in bits 64, 1024, 2048 "Straylight" and 4096 "Straylight2".)
3. **Eclipses**: masked using the **Kepler catalogue period**; the primary eclipse phase is re-found in each sector. For G1 stars without measured eclipse widths, `eclipse_mask_auto` folds at the catalogue period, finds phase bins more than 4 robust sigma low, and pads them by 1.5 times their width.
4. **Detrend**: wotan biweight, 2-day window (at least 3 times our longest searched duration).
5. **Search**: bin to 10 minutes; slide boxes of 3, 4, 5, 6.5, 8, 10, 12 and 15 hours; score SNR = (median - box mean) / robust scatter of all box means of that length (so correlated noise is included); events above SNR 7, merged across durations. **Each crossing is searched on its own: no period, no folding** (circumbinary transits do not keep time).
6. **Control**: the same search on the flipped light curve (1 - flux) to count false alarms.
7. **Flags, not deletions**: events near momentum dumps (0.5 d before) or data edges are flagged for a human, because deleting them also removed real transits.
8. **Long periods**: STANLEY (Martin and Fabrycky 2021, AJ 162, 84; MIT licence) stacks N-body-timed transits over many sectors. **Its scores are not calibrated** (28% of trial orbits scored above "5 sigma").

## 5. What we have measured (all ours, mostly ONE star, so thin)

| Result | Number | Where |
|---|---|---|
| Known planet TOI-1338 b re-found | 4 of 8 sectors with a crossing; missed ones had SNR 3.7 to 6.5 | claims F-014 |
| Fakes injected into TOI-1338 sector 98 | 6 Earth radii found 5 of 7, 7 Earth radii always, 5 and smaller never | F-015 |
| Realistic N-body fakes, 40 sectors | 0 of 10 at 4 Earth radii, 8 of 10 at 6, 10 of 10 at 8; 3 of 33 transits fell inside the eclipse mask; detrend kept 90 to 100% of depth | F-029 |
| False alarms on flipped data | 6 events at SNR ≥ 7 in 10 sectors (peaks to 12.6), about 0.6 per sector | F-016 |
| Noise is method-dependent (Kepler-16 S82, 1-hour) | 229 ppm lightkurve quick estimate; 542 ppm SPOC CDPP; 573 ppm after 0.25-day flatten; **908 ppm after our 2-day flatten** | F-039 |
| SAP vs PDCSAP (TOI-1338) | SAP gave a 2 to 3 times smaller noise estimate in sectors 6, 34, 37 with the same transit depth; **cause unknown**; SAP recovered 7 of 8 published transits vs 4 for PDCSAP | F-054, F-055 |
| Quality bit 4096 | PDCSAP is NaN on those cadences, SAP is finite; restoring them found 2 missed crossings but lowered SNR elsewhere (median -0.54) | F-056, F-057 |
| STANLEY on TOI-1338 | best score at 96.11 d (true 95.2 d); 20,482 orbits in 33 min; not calibrated | F-045 |
| Dry run Kepler-16 | one event, which was spacecraft wobble before a thruster firing | dryrun files |

## 6. Where we are weak or unsure (please dig into each)

### 6.1 Is our search still novel?
- **Davies et al. 2026** (mono-cbp) searched 512 detached EBs (P > 7 d) from the Prša et al. 2022 TESS EB catalogue, TESS-SPOC FFI data through Sector 79, and found 1 weak candidate. **How many of our 549 stars were in their sample?** If they published their target list (paper tables, VizieR, GitHub), please cross-match it with the TIC column of `targets/g1_targets.csv` and give the overlap count and list.
- **The Tufts / Martin XRP project** (2024) mentions "over 10,000 TESS binaries". Does it cover the Kepler field? Any results or papers?
- Planet Hunters TESS, the Visual Survey Group, Kostov and colleagues, Orosz and Welsh: any searches of Kepler-field EBs in TESS since 2022? Any announced candidates around our stars (check ExoFOP CTOIs and TOIs for our TICs if you can)?
- Which TESS sectors cover the Kepler field (we believe 14, 15, 26, 40, 41, 53 to 56, 73 to 76, 80 to 83, and later)? What has nobody searched yet (for example sectors after 79, or QLP-only faint stars)? That is where our edge would be.

### 6.2 Can we even see what we are looking for?
- Our floor is about 6 Earth radii at TESS magnitude about 11.5, on one star. Half of G1 is fainter, and many have only QLP (200-second to 30-minute FFI) data. **Estimate the detectable planet size versus TESS magnitude for SPOC and QLP**, with sources.
- Known Kepler circumbinary planets range from about 3 Earth radii up to Jupiter size. **What fraction of the known population would we detect** at our noise, around G1-like stars?
- Given occurrence rates (for example Armstrong et al. 2014; Martin and Triaud 2014; Li et al. 2016; Martin 2018), precession-gated visibility, our sample size, magnitudes and sector coverage: **what is a defensible expected number of detectable new planets in G1?** Our current guess is about 15% (range 4 to 35%) for at least one real candidate. Show your arithmetic.

### 6.3 Noise and data choices
- Why could **PDCSAP be noisier than SAP** for bright eclipsing binaries? (Cotrending basis vectors fitting eclipses? Crowding correction? Something else?) Is there published guidance? Should we search both and require agreement?
- What do **TESS quality bits 2048 and 4096** mean exactly in the SPOC data release notes, and what do professionals mask for transit searches of EBs?
- Is a **2-day biweight** right for 3 to 15 hour transits next to deep eclipses? Would masking eclipses before detrending, modelling and subtracting the binary, or a Gaussian process do better? Any comparison papers (for example Hippke et al. 2019, wotan)?
- **QLP pitfalls** for faint stars (scattered light, sector-edge ramps, aperture changes) and how others handle them.
- Is our **noise estimate** (robust scatter of box means of the same length) sound, or does it underestimate noise in sectors with gaps?

### 6.4 Eclipse masking (we suspect this is our weakest link)
- We fold TESS data at the **Kepler catalogue period**, measured about 10 to 15 years earlier. **How large can the accumulated ephemeris error be** after hundreds of cycles, given catalogue period uncertainties, and could the mask miss eclipses or eclipse wings? We re-find the primary phase per sector, but `eclipse_mask_auto` folds all sectors together.
- **Apsidal motion** in eccentric binaries moves the secondary eclipse. **Eclipse timing variations** from third bodies shift both. How big are these for detached Kepler EBs with P > 5 d (Orosz et al. long-period ETV catalogue? Borkovits et al. 2016)?
- **Eclipse wings as false alarms**: our flipped-data control turns eclipse residuals into bumps, so it **cannot count** false alarms caused by imperfect eclipse masking. What is the right control? (Our idea: plot detected events against binary phase and look for a pile-up near eclipses; or inject at random phases.)
- What happens to **eccentric binaries where only one eclipse is visible**, or binaries whose catalogue period is half or double the true one?

### 6.5 Detection method
- Circumbinary transits can be **shorter than 3 hours** when the planet and star move in opposite directions. What is the realistic minimum duration for planets around G1-like binaries? Davies et al. say recovery depends strongly on duration.
- At a conjunction, **2 or more transits within days** (one on each star, or repeated on one star) are common. Should we search for these pairs and stack them? Any published method?
- **Single-transit events** when the planet's period is longer than a 27-day sector: best practice?
- How should **STANLEY scores be calibrated** (injection-recovery on many stars? bootstrapping?) What did Martin and Fabrycky 2021 do?
- Is **SNR 7** sensible given 549 stars times about 15 sectors? What does the look-elsewhere effect imply for the number of false alarms we should expect across the whole campaign?

### 6.6 Vetting a candidate around two stars
- Which standard tests apply (odd-even, secondary, centroid, difference images, duration versus binary phase, photodynamical fit), and **which free tools work, or break, with two stars** (triceratops, LATTE, DAVE, VARTOOLS)?
- Circumbinary-specific false positives: background or hierarchical eclipsing binaries, starspots, flares, scattered light, momentum dumps. What fraction of past circumbinary candidates turned out false, and why?
- Our only pixel-level check so far is a lab on TOI-1338 (centroid moved 0.001 arcsec). Is a **pixel or difference-image test** essential before we call anything a candidate?

### 6.7 Validation we are about to run (please design it with us)
- **Re-find known Kepler circumbinary planets in the original Kepler data** (Kepler-16, 34, 35 first). Which Kepler product (long cadence PDCSAP?), which quarters, and **the published transit times** we should use as the answer key (with sources). How many transits does each have, and which are shallow?
- Davies et al. 2026 report, on Kepler long-cadence data, at least 50% recovery per planet and over 75% for 9 of 14. **Please extract their per-planet table** so we can compare like with like.
- Pitfalls of running a TESS-tuned detector on 29.4-minute Kepler data.

### 6.8 Ranking the 549 targets
- Could we rank stars by likelihood of a detectable circumbinary planet using: binary period (planets cluster just outside the stability limit, typically 4 to 7 times the binary period), eccentricity, mass ratio, magnitude, number of TESS sectors, published ETVs or tertiary eclipses, Gaia RUWE (as a flag only: PH1 b orbits in a four-star system), or unconfirmed Kepler circumbinary candidates? Please give sources for any rule you suggest.

### 6.9 If no planet turns up: what is still worth doing and publishable?
Ahmed wants, honestly, to contribute something real and have his name on it. Please research **realistic, credited outcomes for a careful amateur with this pipeline and data**, for example:
- Updated eclipse ephemerides or eclipse timing for many Kepler EBs using TESS (are these publishable in RNAAS or useful to catalogue maintainers?).
- Upper limits: "no planets larger than X Earth radii crossed in these sectors" for N binaries.
- New variable stars or anomalies found along the way (AAVSO VSX submissions).
- Contributions through Planet Hunters TESS or collaborations.
For each: what is needed, how long it takes, who publishes such things, and examples of amateurs who did it (with sources).

### 6.10 Anything else
- Read our code and reports and tell us **the three most likely ways this project fails silently**, and the cheapest test for each.
- Anything in our records (`research/mistakes.md`, `book/data/claims.csv`) that you think is wrong.

## 7. Things already settled (do not spend time re-arguing them unless you find evidence)
- Do not fold circumbinary light curves on one period (we agree).
- Human eyes make the final call (two-key rule).
- Lightkurve is used only to load data, not for our noise estimate.
- We will not drop high-RUWE stars.
- The "Popcorn et al. 2024, PASP 136, 024401" citation from another AI does not exist.

## 8. Our constraints (so suggestions fit)
- Free tools and public data only; a Windows PC; storage on a D: drive; about 6.3 GB for all G1 light curves.
- An AI writes the code; Ahmed reads and decides. Suggestions should be implementable in Python (numpy, astropy, lightkurve, wotan, batman, rebound are installed).
- Licence: MIT. GPL code may be used as a separate tool but not copied in.
- Nothing is published or uploaded until a write-up exists and both keys agree; ExoFOP now asks for publication first (please confirm the current ExoFOP rule).

## 9. How to structure your answer
1. **Top 10 findings**, ranked by how much they change our odds of a real, credited result. One paragraph each, with tags and sources.
2. **Bugs or likely bugs in our code** (file, function, why, test).
3. **Overlap and novelty** (section 6.1), with the overlap list if you can make it.
4. **Sensitivity and expected yield** (6.2), with arithmetic.
5. **Method improvements** (6.3 to 6.6), each with expected gain, effort and risk, marked standard practice or your own idea.
6. **Validation design** for the Kepler re-find test (6.7), including the answer key.
7. **Target ranking** (6.8).
8. **Credited outcomes even without a planet** (6.9).
9. **What you could not open or verify.**
10. **The one thing you would do next, and why.**

Thank you. We would rather be corrected now than wrong later.
