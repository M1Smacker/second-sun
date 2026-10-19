# Wave queue (night of 2026-10-19)

Queue runners take the **first wave in this order whose folder does not yet exist** under `D:\second-sun\research\`, create that folder plus `CLAIMED.md` immediately, then run the wave.

Every wave follows `research\WAVE-BRIEF-COMMON.md`, its own section 5 entry in `RESEARCH-PLAN.md`, and the extras below. Read `research\wave-1-gap-check\GAP-REPORT.md` first in every wave.

**Hard stop for all waves: 21:50 UTC on 2026-10-19 (00:50 Kuwait).** Checkpoint and finish before it, even if work remains; list what remains in open-questions.md. At the end, write `DONE.md` with the finish time and `complete` or `partial`.

**Separate Python environments tonight** (to avoid two installs colliding):

| Wave | Environment |
|---|---|
| 2 | `D:\second-sun\.venv` |
| 3 | `D:\second-sun\.venv-w3` |
| 9 | `D:\second-sun\.venv-docs` |
| all others | none (reading only) |

---

## 1. `wave-2-data` (Wave 2: data and archives)
Hands-on allowed: create `D:\second-sun\.venv` with `py -3.12 -m venv`, and install **only** lightkurve and astroquery. Download cap: 1 GB total.

Extra questions:
1. TESS hardware and observing:
   - cameras, and pixel size (why big pixels cause blended-star fakes)
   - full-frame-image cadence history and the 2-min and 20-s targets
   - continuous viewing zones, and how many stars have many sectors.
2. Every light-curve product, for each: who makes it, which stars, cadence, quality, gaps, file sizes, and how to download it. Products: SPOC, TESS-SPOC FFI, QLP, TGLC, eleanor / GSFC-ELEANOR-LITE, CDIPS, and others you find. Wave 1c already covered brightness limits and sector coverage: cite it, don't redo it.
3. Systematics: quality flags, momentum dumps, scattered light, sector edges, and where the per-sector data release notes live.
4. Access routes: lightkurve, astroquery, MAST bulk scripts, TESScut, and the TESS data on AWS open data (free? anonymous? rate limits?).
5. Kepler/K2: products, precision versus TESS, value for us.
6. Gaia: which DR3 tables matter (RUWE, non-single-star catalogue, astrophysical parameters, neighbours). Is DR4's date confirmed, and what does it add?
7. Ground surveys: ZTF (IRSA), ASAS-SN Sky Patrol, ATLAS. What each gives, and how to query it without an account.
8. A DATA BUDGET TABLE from measured sizes: GB per 1,000 stars per product, and GB for each gap in GAP-REPORT.md (G1, G2, G3).

Hands-on:
- For TOI-1338, download one SPOC light curve, one target pixel file and one small TESScut cutout.
- Time each download and record each size.
- Prove that no cache lands on C: (check `%USERPROFILE%\.lightkurve`, `%USERPROFILE%\.astropy` and pip's default cache before and after).

## 2. `wave-4-vetting` (Wave 4: vetting and false positives)
Reading only.

Extra questions:
1. A CATALOGUE OF FAKES: every way a non-planet mimics a transit in TESS data. Cover:
   - eclipsing binaries (grazing; secondary-only)
   - blended background binaries (~21-arcsecond pixels)
   - hierarchical triples
   - stellar variability (spots, pulsations, flares)
   - spacecraft systematics (momentum dumps, scattered light, sector edges, jitter)
   - cosmic rays and single-cadence events
   - asteroids.
   Then the CIRCUMBINARY-SPECIFIC fakes: third light, tertiary eclipses, eclipse residuals after modelling the binary, spot crossings. For each fake: what it looks like and why.
2. The tests and thresholds professionals use, with numbers and sources:
   - SPOC data validation reports
   - the TOI vetting criteria (e.g. Guerrero+ 2021)
   - MES / signal-to-noise; odd/even; secondary eclipse; centroid / difference imaging
   - Gaia neighbours and contamination; V vs U shape; duration vs stellar density
   - TRICERATOPS FPP/NFPP thresholds, plus alternatives
   - vetting software: LATTE, DAVE, exovetter, LEO-vetter, and others maintained in 2026 (record each one's last release).
3. How TOI-1338 b and TIC 172900988 b were vetted (use wave 1 sources).
4. OUR "VERY STRICT" BAR: numeric pass/fail criteria for (a) a normal transit candidate and (b) a circumbinary single-dip candidate. Every threshold is sourced, or marked as our own conservative choice.
5. A PHONE-FRIENDLY VETTING SHEET SPEC: panels, numbers and order for an iPhone, plus a beginner pass/fail checklist. Describe it; don't build it.

## 3. `wave-3-pipeline` (Wave 3: methods and tools)
Hands-on allowed, in `D:\second-sun\.venv-w3` only. Download cap: 1 GB total.

Extra questions:
1. Plan section 5, Wave 3, questions 1-8.
2. **Install tests on Windows + Python 3.12**, each recorded in the compatibility matrix (pass/fail + exact error):
   - lightkurve, wotan, transitleastsquares
   - batman-package, rebound
   - **stanley_cbp** (MIT; Tufts)
   - **mono-cbp** (GPL-3.0: install as a tool only, never copy its code into our repo)
   - triceratops, LEO-Vetter (if installable)
   - ellc / PHOEBE 2 (note whether Linux-only).

   Give the **WSL verdict**: is a must-have tool Linux-only?
3. **Ground truth:**
   - Recover TOI-1338 b's known transits (Sectors 3, 6, 10).
   - **Practice target:** check TOI-1338 b in Sectors 97-98 for a transit. Report it as a *preliminary internal check*, never as a discovery.
   - Time the processing per star, to set batch sizes.
4. **G1 feasibility:** cross-match the Villanova Kepler EB list (data\wave-1) to TIC IDs and get the TESS magnitude distribution. For ~5 Kepler-field binaries spanning that range, measure the TESS noise level (e.g. CDPP or the scatter in 1-hour bins). Estimate the smallest circumbinary planet detectable at each brightness. Is G1 feasible?
5. One injection-recovery smoke test on one light curve.

## 4. `wave-5-credit` (Wave 5: credit, submission, publishing)
Reading only. Plan section 5, Wave 5, plus:
1. **Can a single-transit circumbinary candidate be submitted as a CTOI** (the form expects a period)? Find ExoFOP's exact CTOI rules and field list, and any precedents of single-transit CTOIs.
2. Do AAS journals, MNRAS and RNAAS charge independent authors, and are there waivers? What are arXiv's endorsement rules for an independent first-time author?
3. The exact AI-use policy wording of AAS, MNRAS, A&A and arXiv.
4. How the Planet Hunters TESS and Visual Survey Group amateurs get co-authorship in practice.
5. AAVSO VSX rules for submitting a new eclipsing binary or variable star.
6. An account schedule (ADS, ORCID, ExoFOP, AAVSO, Zooniverse, arXiv) with why and when for each.

## 5. `wave-9-tech` (Wave 9: book and infrastructure tech)
Hands-on allowed, in `D:\second-sun\.venv-docs` only: build a tiny local test site in `research\wave-9-tech\site-test\`. Push nothing; no GitHub Pages yet.

Plan section 5, Wave 9, plus:
1. **Material for MkDocs' status in 2026**: maintenance mode? a successor ("Zensical"?)? Choose the engine.
2. iPhone offline / home-screen install: service-worker options for a static MkDocs site, and iOS storage rules.
3. Gamification on a static site: XP, levels, achievements, a sky-coverage map, quizzes.
4. Interactive demos in MkDocs (e.g. Plotly or plain JS).
5. A "night observatory" theme.
6. noindex / robots settings.
7. The GitHub Pages deploy via Actions.
8. **Free phone push alerts**: ntfy or alternatives. Do they work on iPhone? Account needed? Privacy?
9. Scheduled sessions plus Windows Task Scheduler for scripts; a design for a resumable batch runner.

## 6. `wave-6-quests` (Wave 6: training quest + habitable zone + white dwarfs)
Reading only. Plan section 5, Wave 6.

## 7. `wave-7-anomalies` (Wave 7: the anomalies side quest)
Reading only. Plan section 5, Wave 7.
