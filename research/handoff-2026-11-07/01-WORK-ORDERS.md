# Work orders from the outside review (7 Nov 2026; WO-21 and WO-22 added later the same day)

*Ranked by value for Census and for Ahmed. Each order says where it goes (FIX or BUILD queue), the evidence, the steps, how to know it is done, a rough cost in weekly points (my guess, calibrate against `research/usage-ledger.md`), and whether it needs Ahmed's go. "Go: no" means it is a bug fix or a measurement the standing rules already let you schedule; it still waits for his weekly cap.*

Labels: CONFIRMED (I ran it or read it), LIKELY, UNCERTAIN, NOT TESTED.

---

## Group A. Correctness first (cheap, do before anything else)

### WO-1. Forward-looking Census odds (FIX-QUEUE, new item)
- **Evidence (CONFIRMED):** `research/stage3/census_step1/census_worth2.py` line 15 prints `chance of at least one = 1 - exp(-tot)` with `tot = E0 + Census E`. E0 belongs to G1, G2 and G3, which are finished and found 0. `CENSUS-WORTH-2026-11-04.md` line 20 and 33 turn this into "Census at 1,400 stars very likely finds one" (87% to 100%).
- **Steps:** (1) add two columns: "Census alone, at exactly 10%" = `1 - exp(-Ec)`; and "Census alone, rate updated by the three nulls" (posterior over the rate, script in `05-SCRIPTS.md`, two priors). (2) Keep the "95% ceiling if none" column, it is correct as a combined limit. (3) Correction banner on `CENSUS-WORTH-2026-11-04.md`, `LESSON-2-...`, and any book page or claim that quotes the old chance (I found none in `book/` by grep; check again). (4) Log in `mistakes.md` (pattern: "counting evidence already spent").
- **Done when:** the new table reproduces, within rounding, Census 1,400: 36% to 52% (Kepler-like prior) and 21% to 31% (broad prior); Census 3,000: 59% to 76% and 38% to 52% (completeness trimmed by 0.9 for FIX 28).
- **Cost:** about 0.3 to 0.5. **Go:** no (bug), but tell Ahmed in one line, because he was told "very likely".

### WO-2. Use the public eclipsing-binary lists for Census stage 2 (BUILD-QUEUE, amend T136)
- **Evidence (CONFIRMED):** `github.com/wangleon/CALNet`, MIT, README says 10,533 EBs validated from TESS sectors 1 to 88, 2-minute cadence, by manual inspection. I downloaded `outputs/newecl.dat` (1,263,960 bytes; raw URL `https://raw.githubusercontent.com/wangleon/CALNet/main/outputs/newecl.dat`): 10,531 unique TICs; columns TIC, m_TIC, Disp, RA, Dec, HIP, TYC, 2MASS, Gaia, Vmag, Gmag; no period; median G 11.68; 8,277 with G < 13.5. Overlap: G1 51, G2 0, G3 20; 10,460 never searched by us. Note the 0 overlap with G2 (Prsa-based) suggests CALNet's file holds only EBs new relative to its training set (LIKELY).
- **Also:** TESS Ten Thousand Catalog (arXiv:2506.05631) covers FFIs to sector 82 by its abstract (your G3 notes record that the paper also says "1 through 26" in one place, UNCERTAIN); Gao 2025 / arXiv:2412.06175 (already read by you).
- **Steps:** (1) download `newecl.dat` into a new folder under `data\`, log it (downloads rule). (2) Union with Prsa 2022, TTC, Gao 2025 and our G1 to G3 lists by TIC. (3) Periods: query Gaia DR3 `vari_eclipsing_binary` (frequency column, period = 1/frequency) by Gaia `source_id` from CALNet's Gaia column; read-only TAP, counts first. (4) Count how many are detached (Gaia model or depth ratio), P > 7 d, and Tmag brighter than about 13.5: this is the size of the ready-made part of Census. (5) Amend `CENSUS-PLAN-2026-11-04.md` stage 2: public lists first; our own finder only for the gap (one or two eclipses per sector); CALNet plus Prsa as a larger answer key for the finder's recall test. (6) Lesson for Ahmed before stage 2 runs (agreed way of working).
- **Done when:** a table "Census candidate pool by source" with counts by period and brightness, and the stage 2 plan rewritten with a smaller download estimate.
- **Cost:** about 1 to 2. **Go:** yes (Census stage 2 is his decision).
- **Watch out:** CALNet classifies each sector separately, so slow binaries with one eclipse in a sector are its weakest case (LIKELY from its own paper's example); do not assume it is complete for our targets.

### WO-3. Back-test Horizon against what professionals found (BUILD-QUEUE)
- **Evidence (NOT TESTED; reasoning):** Davies et al. 2026 searched 512 detached EBs and report one weak candidate; only a couple of transiting circumbinary planets found in TESS data are published (TOI-1338 b 2020, TIC 172900988 b 2021; my search was not exhaustive, UNCERTAIN). If Horizon run on those samples predicts several planets, Horizon is still generous.
- **Steps:** run `horizon_reach.py` with Amendment 4 on (a) Davies's sample if its table is public, (b) the Prsa list's long-period detached subset with typical sectors; compare predicted E with professional yields; report a scale factor with its uncertainty.
- **Done when:** a one-page note "Horizon against the professionals" with the factor, and every Census forecast quoted with it applied.
- **Cost:** about 1. **Go:** no for the study; yes before it changes any quoted number in the book.

---

## Group B. Petrova (Vesper) upgrades that pay for Census
*All of these change the search, so each one: development slice only, both arms (real and upside-down), planted-dip recovery measured, mutation-tested, frozen under a new hash, judged against the preregistered budget (at most 8 upside-down first-tier dips per 1,000 star-sectors, unless Ahmed changes it).*

### WO-4. Mask-and-redetrend second pass (FIX-QUEUE items 11 and 14)
- **Evidence (CONFIRMED in your own notes):** 2-day biweight keeps 57% of a 20 h dip's depth and 68% of 15 h; a 3-day window keeps 72% and 79% but admits more ramps. `detect_v2.detrend` masks nothing.
- **Steps:** after the first pass, for each event above a low bar (for example SNR 5), mask a window of 1.5 to 2 times its duration, detrend again from the original light, re-measure depth and SNR. Run identically on the upside-down copy.
- **Done when:** recovery of 8 to 20 h planted dips rises by a measured amount and the S2 false-alarm budget is still met; result table in the style of `faint_recovery_v5.txt`.
- **Cost:** about 2 to 3 including the freeze. **Go:** yes (search change).

### WO-5. Make QLP neighbour windows deterministic (FIX-QUEUE item 70)
- **Evidence (CONFIRMED in your notes):** a QLP-only star-sector's events depend on which other stars are in the run's manifest; 13% of groups changed when the manifest grew.
- **Steps:** freeze a per-sector "window source" table (this is T137) built from the public target lists, independent of what was downloaded; the run reads the table, never the manifest.
- **Done when:** the same star-sector gives identical events whatever else is in the manifest (test: run one sector with two different manifests, zero differences).
- **Cost:** about 1 to 1.5. **Go:** yes (search change; part of Census stage 4).

### WO-6. Settle S2 (open decision, his)
- **Evidence (from your Q6 note):** pooled 115 in 13,412 star-sectors = 8.57 per 1,000 (95% 7.08 to 10.29) against a mark of 8; a true 8 is not ruled out.
- **My view:** option A (accept, report the pooled rate and its interval, stop calling a 0.57 overshoot inside its own interval a failure). Spending 19% to 30% of completeness (option B) to move a number that is statistically consistent with the mark is a poor trade for a search whose main problem is completeness. Present this as one opinion among his options.
- **Cost:** about 0.2. **Go:** yes.

### WO-7. Two-dip linking inside one conjunction and across sectors (T106, Census idea 4)
- **Evidence:** a circumbinary planet can cross both stars within one conjunction (two dips days apart, different depths and durations); your own literature check found the concept published on Kepler data (STANLEY, Windemuth 2019) and possibly open only for sparse TESS sectors with an upside-down control. Keep the novelty claim at "possibly" until a wider check (T127).
- **Steps:** after WO-4, a linker that scores pairs and triples of sub-threshold dips by whether one stable orbit (outside the Holman and Wiegert limit) can produce their times and durations; null from the same linker on the upside-down copy and on time-shuffled pairings.
- **Cost:** about 3 to 5. **Go:** yes. This is the most plausible place for the "original method" Ahmed wants.

---

## Group C. Reproducibility and tests

### WO-8. One root for all paths (FIX-QUEUE)
- **Evidence (CONFIRMED):** 64 of 111 files in `pipeline/` contain `D:\` or `D:/` paths; `pipeline/dataset.py` already centralises some.
- **Steps:** a single `SS_ROOT` (environment variable, default `D:\second-sun`) read in `dataset.py`; replace hard-coded roots in the core chain first (`detect_v2`, `stage3_core`, `stage3`, `audit_all`, `vopts`, `chain_recovery`, `scorecard_plus`, `horizon_reach`, `leads_export`, `audit_paths`), studies later or never. Frozen files: this changes hashes, so do it as part of the next freeze, with the zero-difference proof you used for 0.8.1.
- **Done when:** `SS_ROOT=/somewhere python pipeline/test_*.py` runs on Linux with no `D:` error.
- **Cost:** about 1 to 2. **Go:** yes (it touches frozen code).

### WO-9. Honest test output and continuous testing (FIX-QUEUE)
- **Evidence (CONFIRMED by running them on Linux, Python 3.13, numpy, scipy, pandas, astropy, lightkurve, wotan installed):** pass: `test_hunt_prep` (all), `test_leads`, `test_scorecard_plus` (7 of 7, parts 2 and 3 skipped for missing sealed data), `test_detect_v2_paths` (cadences pass; B2 and B5 print "skip" and then "pass"); `test_recipe_diff` printed "no settings.json" and did nothing; fail on `D:` paths: `test_vopts` (via `audit_paths.py` line 17) and `test_stage3_prep`; not run because they hard-code `D:` as well: `test_g3_prep` (3 references) and `test_eyes_scores` (6).
- **Steps:** (1) a skipped check prints `SKIP` and is counted separately; a run with skips says so in its last line. (2) After WO-8, a GitHub Actions workflow on Ubuntu that installs `requirements.txt` (or a slim test subset) and runs every test file that needs no data; tests that need data skip honestly. (3) A badge or a line in the README.
- **Done when:** a push to main runs the tests automatically and a deliberately broken `box_scores` turns the run red (mutation proof).
- **Cost:** about 1. **Go:** no for (1); yes for (2) since it adds a system.

### WO-10. Run environment and data provenance per run (T128, partly done)
- Record for every run: git hash, frozen hash, Python and package versions, manifest hash, list of input files with sizes. You did this for G3; make it automatic for Census. **Cost:** about 0.5. **Go:** no.

---

## Group D. Process (saves the most tokens over the coming months)

### WO-11. Slim RESUME and the publish rhythm (Ahmed decides the rhythm)
- **Evidence (CONFIRMED):** RESUME.md is about 15,900 words; 141 of 305 commits are paperwork; on 6 Nov an evening went to claim upgrades that no decision rested on and to FIX 80 (a layout test failing about 1 in 40).
- **Steps:** RESUME = one screen (state, open decisions, running jobs, next step), with history moved to `RESUME-ARCHIVE.md` (nothing deleted, the "never delete" rule holds). Book publish at most once a day, batching changes. Claim verification only when a published sentence or a decision depends on it (already the CLAUDE.md rule, "proportionate to the usage cap"). Park FIX 80 until it fails in a real publish (the diagnostic is already in place).
- **Done when:** a cold-start session reads under 3,000 words before work. **Cost:** about 0.5 once, saves an estimated 1 to 2 points a week (UNCERTAIN). **Go:** yes (his rules: RESUME update rule of 4 Nov, daily recap rule of 3 Nov).

### WO-12. Queue triage (Ahmed decides)
- **Evidence:** BUILD-QUEUE has around 100 task lines and at least eight named systems.
- **Steps:** mark each task Census-critical, Census-helpful or Parked (one-line reason). Proposal: critical = T136, T137, T138 (done), WO-2, WO-4, WO-5, WO-7, T106, T108, T125, T127, T129; everything else parked until Census has run. Show him the list; he decides.
- **Cost:** about 0.5. **Go:** yes.

---

## Group E. Be ready for success

### WO-13. Build the candidate playbook before Census runs (T108 and T125)
- Contents: what counts as a lead at each stage (already written for the Search window); for a single circumbinary dip, which future TESS sectors will see the star again (TESS-point web tool, linked from the TESS Science Support Center), how predicted windows are made from one or two dips (orbit families allowed by stability, honest about how wide they are), what the write-up must contain (data, method, controls, completeness, what is not claimed, predicted windows; the book already records that NASA's candidate site now wants a publication first), where it goes, how Ahmed is credited, and what is never done (no public claims before two keys and his yes).
- **Also a by-product rule:** "too deep for a planet" events (T48) are not thrown away. Tertiary eclipses (a third star crossing the binary) are rarer than ordinary eclipses but much more common than circumbinary planets, and citizen scientists publish them regularly (Planet Hunters TESS papers). Keep them in a private list with the same two-key rule. **Cost:** about 1. **Go:** yes.

### WO-14. Orbit-locked dips: understand them, not just flag them (BUILD-QUEUE, study)
- **Evidence (from FIX-QUEUE item 30 and the sealed analysis):** 54 events on 8 stars locked to the binary orbit at phases away from the eclipses, median depth 822 ppm, periods 5.5 to 20.6 d; flagged by c6 and moved to tier 2. What they are is open: spots locked by tides, reflection or beaming, a third body on a resonant orbit, or a processing artefact tied to orbit phase.
- **Steps:** phase-fold the 8 stars, compare SAP and PDCSAP, check the pixels, read what Kepler EB studies say about out-of-eclipse features. Report only. This may be real astrophysics nobody has catalogued in these stars. **Cost:** about 1. **Go:** yes.

---

## Group F. Learning (Ahmed's mastery plan, `04-MASTERY-PLAN.md`)

### WO-15. Engine Room (BUILD-QUEUE, book)
Brief in `02-ENGINE-ROOM-BRIEF.md`. Build after Ahmed's boards (he starts Tier 2 in June 2027); the map page and ER1 can come earlier. **Go:** yes.

### WO-16. One name for Ahmed's key
The book says "second key" for Ahmed (learning track L6 check 3; `candidates.md`); Ahmed calls himself the first key. Ask him once, then fix every page in one publish. **Cost:** about 0.2. **Go:** yes.

### WO-17. Align Keystone (T134) with the Checker finish test
The mastery plan's Checker test (10 blind events, 8 right with written reasons) and Keystone are the same idea. Merge them so he sits one exam, not two. **Go:** yes.

---

## Group G. Research only (no builds; file as questions)

### WO-18. PLATO angle
ESA's PLATO page gives a planned launch in April 2027 (checked 7 Nov 2026). A vetted list of slow, detached EBs in PLATO's first field (LOPS2), with TESS single-transit search results, would be useful to PLATO circumbinary work (there is a paper on LOPS2 seen with TESS, arXiv:2409.13039, not read). Question: how many Census-pool binaries fall in LOPS2? Count only.

### WO-19. Is the upside-down asymmetry result new?
Your measurement that the upside-down control overstates dip false alarms by about 1.3 to 2.5 times (`asymmetry.txt`, the sealed analysis) is a methods result. Literature check (T127 style): has anyone published the size of this asymmetry for single-transit searches in TESS? If not, it is a short research note in its own right.

### WO-20. Eclipse timing as an independent second key (FIX-QUEUE item 27)
Thornton et al. 2026 (arXiv:2512.07934) found 27 candidates from apsidal precession; Jiang 2026 (arXiv:2608.13269) showed two of them are stellar effects once star-specific models are used. For our survivors only: does the binary's eclipse timing show anything? Design question only; no build before Census has survivors.

---

## Group H. Added 7 Nov 2026, later the same day (Ahmed asked)

### WO-21. The Annex: a sorted library of everything the filter flagged (BUILD-QUEUE, Ahmed's idea)
- **What Ahmed wants:** a safe, well organised place where every dip the search did not put in tier 1 is sorted by what it probably is, so he can work on other science with data we already have, without new downloads.
- **What the code says today (CONFIRMED by reading it; the files on D: NOT checked by me):** since Stage 2 nothing is deleted. `stage2_search.py` calls `veto(..., flip_action="flag")` and writes one JSON per star-sector (`GROUPS / f"{tic}_{sector}.json"`, under `D:\second-sun\data\stage2\groups` for G1 and under the G2 and G3 data paths) holding every event at SNR 7 or more, real AND upside-down, with its flags; `stage3_core.tier_of` puts flagged events in tier 2 and disagreeing second products in tier 3, kept and labelled. Only the old Lab 9 / Chapter 8 path defaults to `flip_action="reject"`.
- **What is NOT in the pile:** dips under SNR 7 (never stored); anything inside the eclipse masks (removed before the search by `mask_runs`); star-sectors with no safe windows or too little data (for G3 about 16% of reads); and there is no "too deep for a planet" tag (`DEPTH_MAX_PPM = 300_000` only catches broken curves; T48 is not built). The raw light curves are kept (G1 about 5.5 GB, G2 23 GB, G3 2.2 GB), so any of this can be re-searched.
- **Important for Ahmed:** tier 2 is not "not a planet". Your own planted-dip test (`Q3-Q7-GAIA-AND-COMPLETENESS-2026-11-04.md`) says about half of every dip the search sees is flagged, at any depth; among lost planted dips the step check fired 53%, gap-dump 28%, ramp 21%, dominated 21%. A real circumbinary transit can sit in tier 2.
- **Design:** an index, not copies. One table (CSV or SQLite in `data\annex\`, git-ignored) with one row per flagged event: campaign, version hash, TIC, sector, product, kind (real or upside-down), SNR, depth, duration, flags, tier, and a pointer to its group JSON. Shelves by flag, mapped to science:

| Shelf | Flags | What it could be | Branch |
|---|---|---|---|
| Deep dips | new tag: depth 1% to 30% (T48 widened) | a third star crossing the binary (tertiary eclipse), a background eclipsing binary | triple stars |
| Orbit-locked | `orbit_lock`, `c5`, `ecl_overlap` | spots, reflection, a third body, eclipse-shape changes | WO-14 |
| Repeaters | `repeater` | background eclipsing binaries, blends | contamination study, new EBs |
| Flares | `flare` | stellar flares in eclipsing binaries | stellar activity |
| Variability | `flipmatch`, `dominated` | pulsations, rotation | variable stars |
| Instrument | `step`, `ramp`, `gap_dump`, `burst` / `common` | TESS artefacts | negative examples for WO-22 |
| Second look | tier 2 with only one mild flag, tier 3 | possibly real transits caught by a strict check | circumbinary, after Census rules |

- **Rules (non-negotiable, from the project's own principles):** (1) every shelf holds the upside-down events too and shows real and upside-down mixed and unlabelled until a written rule says otherwise, or the shelves will "find" patterns that noise makes; (2) the Annex is never used to change Petrova's settings or to re-score a sealed campaign (that would break preregistration); a "second look" shelf study needs its own written rule before anyone opens it; (3) star IDs and times stay private (same rule as leads); (4) a private backup of the group JSONs (they are small), since today they live only on one disk (Ahmed decides where; never a public place).
- **Done when:** the index builds from the existing JSONs in one command, counts per shelf for real and upside-down are printed, and a test proves no event is lost (row count equals event count across all group files).
- **Cost:** about 1 to 1.5 for the index and shelves; each science branch is its own later task. **Go:** yes. Best after Census stage 2 is planned, or as a light task when Ahmed wants a break from Census.

### WO-22. Petrova dataset for machine learning (BUILD-QUEUE)
- Save every labelled event in one clean table: planted fakes (truth known), upside-down events (noise by construction), flagged instrumental events, and Ahmed's and Claude's Eyes labels, with the light-curve cut-out around each. This is a ready training and test set for a neural vetter later (Ahmed's ML roadmap; Shallue and Vanderburg 2018 is the classic example). Shares the index with WO-21. **Cost:** about 1. **Go:** yes. Not before the Annex index exists.

---

## Things I would NOT do

- Do not add new named systems until Census has run. The project's limit is completeness and fuel, not ideas.
- Do not tune any setting on G1 to G3 results to make Census forecasts look better.
- Do not quote any Census probability to Ahmed without the null update (WO-1).
- Do not claim "first" or "original" for the linker (WO-7) before T127's wider literature check.
