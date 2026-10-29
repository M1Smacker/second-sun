# Vesper briefing: where the Second Sun planet search stands, what is weak, and what to do next

Written by Claude (the AI coding assistant that built the pipeline with Ahmed, the owner) on 28 October 2026, for a stronger reviewer or collaborator. Everything below is taken from the repository's own result files and notes unless it says "my judgment". Labels used throughout: VERIFIED (a tool or a source backs it), LIKELY (reasoned or partly checked), UNCERTAIN, NOT TESTED. Nothing here was invented to sound better; where I made a mistake or a judgment call, section 12 lists it.

Repository: https://github.com/M1Smacker/second-sun (public). Public book: https://m1smacker.github.io/second-sun/

---

## 0. How to use this file

- Read sections 1, 6, 8 and 15 first if you have ten minutes. They hold the situation, the numbers, the core scientific problem and the plan.
- Section 16 lists the questions I most want a stronger mind to answer.
- Section 17 lists the rules you must respect if you touch the code or the data.
- If you have the repo: start with `RESUME.md`, `research/stage3/learnings-2026-10-27.md` (sections 11 to 17), `research/stage3/FIX-QUEUE.md`, `research/stage3/aggregate_v7.txt`, `research/stage3/SETTINGS_FROZEN.json`.
- If you do not have the repo, this file is meant to be enough to critique the method and propose the next steps.

## 1. The situation in one paragraph

We built a single-transit search ("Vesper", the name Ahmed chose on 28 Oct 2026) for planets that orbit two stars (circumbinary planets) in TESS light curves of 549 Kepler-field eclipsing binaries. We ran it, then improved it through seven frozen versions in about ten days. After the full rule set (version 7) the search leaves 21 first-tier dips from real light curves on 17 stars, against 32 first-tier dips from the same search run on the upside-down light curves, which cannot contain planets. None of the 21 sits on a known TESS planet candidate, a known planet host or a known circumbinary host; 3 are on stars in the TESS eclipsing-binary catalogue. Nobody (human or AI) has looked at any of them. The honest result is: no sign of a planet at this strength. The larger result is a measurement of our blind spot: the search finds an 8-hour dip only about 61 times in 100 when the dip is 10 times the normal 8-hour noise, 22 in 100 at 8 times, and 2 in 100 at 6 times. A faint planet could easily be hiding in these 549 stars. Our target list is faint (median TESS magnitude 12.45), our judge (the upside-down copy) is biased, and our scripts grew by accretion. This file lays all of that out and proposes a plan.

## 2. Context and constraints

- **Project:** Second Sun. Goal: find and, if possible, help confirm a circumbinary planet from public TESS data, and teach Ahmed how the science works through a public book (MkDocs on GitHub Pages) with a browser training game called Eyes mode (Ahmed practises spotting dips by eye; scores are stored in the owner's own cloud database).
- **People and tools:** Ahmed is the owner, a student, busy with studies, who has not yet started the book's learning track. Claude Code (me) writes and runs the code, under a fixed usage budget (a Pro plan with a 5-hour window and a weekly window; Ahmed set a working cap of roughly 10 weekly points per day). That budget is one reason progress comes in small frozen increments.
- **Machine:** one Windows 11 PC, Python 3.12 virtual environment (`.venv`; the system Python lacks pandas), `lightkurve` and `wotan`. Local data is about 6.0 GB under `data\` and is not in git. A full re-search of 549 stars takes about 30 to 40 minutes of machine time (VERIFIED, usage ledger). Speed is not the bottleneck.
- **Status of human review:** none. By rule since 27 Oct, no one looks at any real event until the rules are frozen and Ahmed has finished Eyes practice. See sections 12 and 15 (step 6) for why this matters and how I propose to lift it safely.
- **Publication rule:** only aggregates (counts, no star IDs, no event times) go into the public book. Real events stay in `data\`.

## 3. The data and the 549 targets

- **Target list ("G1"):** built from the Villanova Kepler eclipsing-binary catalogue (revision 2019-08-08, 2,921 rows) with three cuts: morphology below 0.5 (detached), binary period above 5 days, TESS magnitude 13.5 or brighter. Result: 552 rows, 549 stars. 136 rows have morphology -1 ("not measured") and passed the cut by accident; we kept them. (`pipeline/targets_g1.py`, `targets/g1_targets.csv`.)
- **Brightness:** median TESS magnitude 12.45 (VERIFIED). Star-sectors by class: faint (12 or fainter) 3,196; middle (11 to 12) 1,067; bright (brighter than 11) 801; total 5,064 star-sectors with a usable best data product. Most of what we search is faint, noisy sky.
- **Data products:** every one of the 549 has QLP light curves (the quick-look pipeline's, from the MIT team); 275 have SPOC 2-minute light curves; 312 have TESS-SPOC full-frame light curves; 237 stars have QLP only, so there is no second product to check them against.
- **Known objects inside the list:** 6 are TESS Objects of Interest (5 known planets, 1 candidate), 6 are known circumbinary hosts (Kepler-16, 38, 453, 1647, PH1, Kepler-1660), 53 are in the TESS eclipsing-binary catalogue (Prsa et al. 2022). All labelled automatically; labels never remove an event.
- **Overlap with the professionals:** the mono-cbp team (Davies et al. 2026, arXiv:2604.09435) started from 591 long-period detached TESS eclipsing binaries, searched 512 of them, found 1 weak candidate. Only 30 of those 591 are in our 549 (VERIFIED, our recount). So about 560 stars of their starting table have never been searched by us.
- **Light curves per star:** several sectors each (5,082 star-sector groups over 549 stars, so about 9 per star on average; 5,064 have a best product).

## 4. How Vesper works (the chain)

The code is in `pipeline/`. Core idea: a matched-filter box search for single dips, run identically on the real light curve and on its upside-down copy (flux flipped around 1), with a long list of flags that sort dips into tiers. The settings of each version are frozen with hashes before any result is read.

1. **Load** (`detect_v2.load`): quality-masked, normalised flux. SPOC: PDCSAP flux, with cadences that PDC dropped filled from locally scaled SAP flux (a v2 design choice, see weakness 11.5). QLP: `sys_rm_flux` from sector 56 on (keeps long-dip depth), raw `sap_flux` before.
2. **Mask the binary's own eclipses** using the known catalogue period; each sector re-finds the primary's phase.
3. **Detrend:** `wotan` biweight with a 2-day window.
4. **Bin** to 10 minutes. **Slide boxes** of 3, 4, 5, 6.5, 8, 10, 12, 15 and (from v5) 20 hours. Score each box position: SNR = (median minus box mean) divided by the robust scatter of all box means of that length in that light curve (1.4826 times the median absolute deviation, so correlated noise in the bulk is included).
5. **Events:** peaks at SNR 7 or more, merged across box lengths (the strongest wins). Same run on the flipped curve gives the false-alarm control.
6. **Second product check:** does another data product of the same star and sector see it (SNR 3 lenient, 4 strict)?
7. **Flags** (never deletions): data gap or momentum dump; common moment (v7: three or more other stars with an event of either kind within 0.1 d, same sector and camera; replaced the Stage 2 "burst" flag, which counted only upside-down events); matched upside-down event at the same moment; eclipse phase (C5); eclipse overlap by physical length (or catalogue-measured width for 40 stars); repeater (three or more events of one kind in one product and sector, since a circumbinary planet must sit beyond about 3.7 binary periods, so at most two transits fit in a 27-day sector); flat baseline (a planet dip is a box, a ramp is not); orbit-start ramp (within 1 day after data resumes; costs 14.2% of the timeline); dominated (the strongest event of the other kind in the same light curve is at least as strong).
8. **Tiers:** 1A (second product agrees at 4 or more), 1L (3 to 4), 1B (no second product), 2 (flagged), 3 (second product disagrees, or v7: a raw-light-only dip not visible at SNR 3 in the cleaned light of the same file).
9. **Raw-light twin (v6):** for the 1,420 of 5,064 star-sectors whose best product is SPOC or TESS-SPOC, the SAP (raw) flux of the same file is also searched; a dip found by either counts once (`stage3_report.merge_sap`); v5 events are never changed; SAP-only dips are added.
10. **Reports:** `stage3_report.py` writes aggregates (no star IDs, no times): cut waterfall, tiers, real minus upside-down per tier and per SNR bar, noise-expected line, catalogue labels, SAP-twin and v7 sections.
11. **Measurement harnesses:** injected-dip recovery (`step_retention.py`, `faint_recovery.py`, `sap_recovery.py`), the asymmetry test (`asymmetry_test.py`), pair search across sectors (`pair_search.py`), SAP fairness (`sap_fairness.py`), version comparison (`compare_versions.py`), and a yardstick run of the professionals' tool mono-cbp (kept outside the repo because it is GPL).

## 5. History: seven frozen versions in about ten days

Tier 1 = real | upside-down, on the same 549 stars. These numbers are NOT a progress curve: rules changed what tier 1 means (see section 8).

| Version | Hash | What changed | Tier 1 real | Tier 1 upside-down |
|---|---|---|---|---|
| v1 | 04e917e5a7e9 | first full search of 549 stars, 2,642 events | 186 | 174 |
| v2 | 14c896421028 | eclipse overlap by physical length; repeater flag (rules chosen after seeing v1 results, not blind) | 64 | 90 |
| v3 | 23a74c021d8a | flat-baseline step test | 15 | 38 |
| v4 | d5767e66c4d2 | dominated flag, orbit-start ramp flag, measured eclipse widths | 12 | 33 |
| v5 | 5392f864e810 | 20-hour box added, faint-dip recovery test, noise-expected line | 14 | 35 |
| v6 | f366d3682843 | raw (SAP) twin search on 1,420 star-sectors, union of dips | 33 | 36 |
| v7 | fd788be04650 | pooled common-moment flag; raw-light-only dips must show in cleaned light; no new search | 21 | 32 |

Each version was regression-proved before running: with the old settings it must reproduce the earlier search on every old field (74 events on 54 groups for 5 known hosts; 298 events on 474 groups for the 50-star Stage 2 sample), and new rules were mutation-checked (deliberately broken to see that a test fails).

What each step taught (short):
- v1 to v3: more than half of everything the detector finds sits at data-segment edges (orbit starts, gaps). Most early "candidates" were eclipse edges, repeater stars, ramps.
- v4: my first diagnosis ("red noise inflates the SNR") was wrong: the SNR already divides by the measured scatter of the box statistic. The real issue is heavy tails and noise that changes along a sector.
- v4/v5: noise is lopsided (section 8); a scrambled control cannot remove single dips, so it was withdrawn.
- v5: events piled at 3 h and 15 h boxes; long circumbinary transits were not searched; 20 h box added. A 2-day window keeps only 57% of a 20 h dip's depth (68% at 15 h; 3 days keeps 72% and 79%).
- v6: the raw light finds transits the cleaned light misses (known planet TOI-1338 b: cleaned light 4 of 8 testable transits, raw 7 of 8, union 8 of 8; VERIFIED), but the list got longer, not better.
- v7: the old burst flag treated real and upside-down dips unequally; the pooled version fixes that. No fair null exists for the raw-light half from the upside-down copy.

## 6. Results today (frozen run fd788be04650, aggregates only)

- Best-product events: **1,192 real, 1,398 upside-down**. After the first four checks (gap/dump, common moment, matched upside-down, eclipse phase): 284 real, 234 upside-down. Tier 1 after all rules: **21 real, 32 upside-down**.
- Real minus upside-down at tier 1: -11 (SNR 7), -10 (8), -4 (10), -3 (12). Tier 1A alone: 7 real, 6 upside-down.
- Of the 21 real tier-1 dips: 14 are in the cleaned-light half (against 32 upside-down), 7 are raw-light-only (against 0). **Correction, 29 Oct 2026 (counted from the event files, counts only, `research/stage3/fill_audit_v7.txt`): the name "cleaned-light half" is misleading.** It means the v5 search of each star-sector's best file. By flux column the 14 real are: PDC flux 2, QLP cleaned column (`sys_rm_flux`, sector 56 and later) 2, and QLP raw `sap_flux` 10 (before sector 56 QLP has no usable cleaned column, so our loader reads its raw one; `detect_v2.load` docstring). The 32 upside-down are 9, 7 and 16. So only 4 of the 14 sit on cleaned flux. The comparison inside the half is still like for like (both sides use the same column), but "cleaned" is not the right word; the half is "main flux of the best file". CONFIRMED by counting; the QLP column meaning is from our own loader notes, QLP's data product description PDF was not read. They sit on 17 stars; 3 of 21 are on QLP-only stars. Labels: on a TOI 0, known circumbinary host 0, in the TESS eclipsing-binary catalogue 3.
- Noise-expected line for the cleaned-light half only (upside-down tier 1 divided by the measured asymmetry ratio): SNR 7: 14 real against 14.2 expected, chance of at least 14 from noise 0.56; SNR 8: 11 against 9.7 (0.39); SNR 10: 4 against 4.6 (0.67); SNR 12: 2 against 2.6 (0.72).
- Pair search across sectors (two similar dips on one star in different sectors): clean class 0 real pairs (0.86 expected from noise), soft class 7 real stars with a pair against 12 upside-down (15.2 expected). Nothing. It cannot say much: the frozen run stores only SNR 7 and above, so pairs of weaker dips are invisible.
- The 7 raw-light-only tier-1 dips: on 5 stars, strength 7.0 to 10.2, PDCSAP (cleaned-light) strength at the same place 3.2 to 6.0. In the cleaned light of the same file, 18.5% of real and 23.4% of upside-down raw-light-only dips are visible at SNR 3 (p = 0.07): real ones are not confirmed more often than their mirror images. I suspect camera or scattered-light effects, but I have NOT looked at them (see section 12); this is LIKELY from numbers, not from eyes.

## 7. How sensitive is the search? The blind spot

All measured on injected fake dips in random real light curves (VERIFIED as measurements; they are ceilings because gap, common-moment and repeater flags and the second-product check are not modelled in them).

- **Faint-dip recovery (v5, 240 random star-sectors, 17,088 injected trapezoids, SNR 7 bar).** Depth is in units of that light curve's 8-hour box noise. An 8 h dip is found 61% of the time at 10 times the noise, 22% at 8 times, 2% at 6 times, 0% at 4 to 5 times. At 10 times: 71% for 14 h dips, 69% for 20 h, 33% for 4 h. Near a segment start the found share is about the same as mid-segment.
- **Raw light vs cleaned light (v6 and v7, 240 star-sectors, 5,064 injections).** 8 h dip at 7 times the noise: found 10% in the cleaned light, 11% in the raw light, 16% in either; at 8 times 22%, 16%, 28%; at 10 times 64%, 35%, 66%. The union finds 1.3 to 2 times as many faint dips as the cleaned light alone. The v7 cleaned-light check passes 87% of the injected raw-light-only dips (193 of 222), 88 to 100% for dips at 7 times the noise or more; faint 4 h dips pass only 25 to 40%.
- **Flag chain on deep dips (v4).** 1,548 injections (4, 8, 14 h; box and trapezoid; 12 times the noise) in 160 random star-sectors: 1,120 detected, 82.7% of those survive the step, eclipse overlap, 0.35 d eclipse rule and dominance flag (86.4% before the ramp flag). So the chain keeps about 0.72 x 0.86 = 62% of deep dips, a ceiling.
- **Window loss.** A 2-day biweight window keeps 82% of an 8 h dip's depth, 68% of a 15 h dip's, 57% of a 20 h dip's (3 days: 86%, 79%, 72%). One noise draw, synthetic.
- **What it means in planet size: NOT TESTED.** The units are multiples of the 8 h noise; conversion to planet radius per star brightness has not been done (FIX-QUEUE 12 and 20). Rough statement: the search needs a dip near 10 times the 8 h box noise to find it half the time; a typical faint star at magnitude 12.5 therefore hides everything below roughly a Saturn or Neptune-size planet (my judgment, not measured).
- **Prior chance.** Before the search our yield model gave about 18 in 100 (range 5 to 40) of at least one findable planet in these 549 stars (LIKELY; `research/audit-2026-10-23/README.md`). A later rough figure of "about 1 in 10 that a findable planet is still hiding" was computed from strong fake planets and is too hopeful for faint ones (UNCERTAIN, no honest replacement yet).

## 8. The core scientific struggle: there is no fair judge

We judge detections by "real minus upside-down", the practice of the Kepler team (inverted light curves as a false-alarm estimator), because a planet makes a dip and an upside-down star has none. The trouble:

1. **Noise is lopsided.** Run raw dips with no flags on 900 random star-sectors (all products): upside-down over real = 1.25 at SNR 4.5, 1.34 at 5, 1.77 at 6, 2.30 at 7, 2.52 at 8, 2.07 at 10 (VERIFIED, `asymmetry.txt`; v5 on the 20 h grid: 1.20, then 2.25 at 7, 2.36 at 8, 1.96 at 10). The upside-down side always finds more. Likely cause (LIKELY, NOT TESTED): flares and scattered-light bumps push flux up, which become dips when flipped. So "real below upside-down" is expected from noise alone and proves nothing by itself. The honest statement is "no excess is visible", not "real is below noise".
2. **The raw (SAP) light is lopsided differently.** Raw dips with no flags: upside-down over real = 0.79 at SNR 4.5, 0.98 at 7, 1.22 at 8, 1.70 at 10. Then the flags (gap, common moment, repeater, flat baseline) remove a LARGER share of the upside-down events than of the real ones in the raw-light-only half (repeater flag 24.7% real against 55.5% upside-down; step 75.6 against 86.9; the two eclipse checks go the other way). Ladder in that half, real | upside-down: 550 | 488 raw, 164 | 112 after gap/dump, 74 | 47 after common moment, 68 | 43 after eclipse phase, 67 | 41 after eclipse overlap, 51 | 18 after the repeater flag, 14 | 2 after the flat-baseline flag, 14 | 0 after dominance and the second product, 7 | 0 after the cleaned-light check. The control runs out. Upside-down bumps cluster in a few bumpy light curves and carry ragged shoulders that shape and star-level flags hit hard, so the flag chain is not neutral between the two sides.
3. **Candidate fair nulls and why each fails:** a scrambled control (Kepler moved year-long blocks, which does not remove a single dip; withdrawn); a time-reversed copy (keeps every real dip as a dip, so not a null for planets); a per-star bootstrap false-alarm level in Kepler's style (would only restate the measured scatter the SNR already divides by; needs a null that removes dips and keeps the star's noise, which we do not have); equal-flag-pass-rate re-weighting of the control (fails when the control has no survivor, which is the raw-light half's case); inject-and-recover (measures power, not false alarms).
4. **What v7 did instead:** a pooled common-moment flag (counts other stars' events of either kind, so real and mirror are flagged alike; raw-light-only dips: 77.8% real against 74.8% upside-down flagged, p = 0.27, where the old burst flag gave 52.4% against 66.0%) and a symmetric cleaned-light check. The check is weak by itself: about 1 in 5 pure-noise events reaches SNR 3 by chance, and cleaner stretches agree more in both kinds. It is a filter, not a proof.
5. **Consequence:** the cleaned-light half can still be judged against the upside-down copy with the measured asymmetry ratio (assuming the flags act equally, which is NOT TESTED for that half). The raw-light half cannot be certified, so its 7 tier-1 dips are not evidence either way. Version-to-version tier counts are not comparable as progress because the rules change what tier 1 means.

## 9. Strengths (what is genuinely good)

- **Frozen, hashed versions.** Settings, input files (stars, manifest, targets, best-product table, eclipse widths) and code files are all hashed into `SETTINGS_FROZEN.json` before a run. Provenance records the git commit. Nothing is tuned on results.
- **Regression proofs and mutation checks.** Every version reproduces the earlier search exactly on the old fields; every new rule has tests and deliberate breaks; v7: 20 of 20 stage-3 tests pass and 16 of 16 real mutations were caught (a neutral control was missed, as designed).
- **A known-planet yardstick.** TOI-1338 b: union recovers all 8 testable published transits. Kepler-16, 38, 453, 1647, PH1 and Kepler-1660 sit in the list as controls.
- **Honest accounting.** A claims register (`book/data/claims.csv`, F-001 to F-085) labels each public number VERIFIED, LIKELY, UNCERTAIN or NOT TESTED with a source; corrections are written into the notes instead of hidden.
- **Aggregates only.** The public book never shows a star ID or event time from the real search.
- **Fast to re-run.** 30 to 40 minutes for the whole 549-star search; a regression dry run on 50 stars takes minutes.
- **A publish gate** (`research/burn-3-book/tools/publish_book.ps1`): fresh clone of committed main, strict build, mission, shape, contrast and Eyes tests, link checks, fonts, safety, browser tests. On 28 Oct two full dry runs and the real publish all passed it.
- **Independent yardstick work.** A run of the professionals' tool on 30 shared stars (437 real against 209 upside-down events under their definition; ours 41 against 46) showed the event counts of the two tools are not comparable, so a bigger number is not a better tool.

## 10. Weaknesses of the science (ranked by how much they limit discovery)

1. **Blind to faint dips.** Section 7. Half-recovery needs about 10 times the 8 h noise. This is the biggest limit.
2. **The target list is faint and narrow.** Median magnitude 12.45; 237 of 549 stars have only QLP data; all 549 come from one Kepler-field catalogue with three cuts. Every one of seven versions re-ran the same 549 stars. We have never searched anything else.
3. **No fair null for the raw-light half;** the cleaned-light half's null is biased and only corrected by a measured ratio whose flag-neutrality is NOT TESTED.
4. **Detrending loses depth on long dips** (2-day window keeps 57% of a 20 h dip). A longer window for long boxes is queued (FIX-QUEUE 11) but changes the search and needs a new freeze.
5. **No weak-dip pair search.** The frozen run keeps only SNR 7 or more, so two weak dips of one planet are invisible. Circumbinary transits are not strictly periodic, so an alias check is only a first filter.
6. **Single-sector view per dip.** No joint fit across sectors, no model of the binary's motion (transit timing and duration variations), no photodynamical modelling. We search for generic box dips.
7. **Box filter, not a transit-shaped filter.** A trapezoid or limb-darkened template would gain a few percent of SNR (my judgment, not measured).
8. **Vetting is shape-only.** No pixel-level or centroid tests (blends), no odd-even test on non-repeaters, no secondary-eclipse search; these are held back for survivors only.
9. **Faint-dip test does not include the flags or the second-product check, and is in noise units, not planet size.** So we do not know the true completeness of the whole chain in physical terms (FIX-QUEUE 20).
10. **No human has looked at anything.** Neither the 21 survivors, nor the 7 raw-light-only ones, nor a sample of what the flags removed. All "looks like noise" statements are inferences from counts.

## 11. Why the scripts are not better (engineering weaknesses, stated plainly)

How they got this way: ten days, seven frozen versions, each one answering the last result's problem, under a usage budget, with an explicit rule that anything frozen must keep reproducing. I put new measurements ahead of tidying, and refactoring a frozen pipeline felt risky, so the debt grew. That was a tradeoff I made without putting it to Ahmed.

1. **No single driver.** `pipeline/` holds about 65 scripts: the real chain (`detect_v2.py`, `stage2_search.py`, `audit_all.py`, `audit_paths.py`, `common_time.py`, `stage3.py`, `stage3_core.py`, `stage3_report.py`, `sap_twin.py`) next to one-off diagnostics and dry runs (`dryrun_kepler16*.py`, `diag_v2.py`, `borrow_windows_check*.py`, `kepler_refind*.py`, `veto_*.py`, `accept_v2.py`, `timing_s98.py`). Running a search means knowing which five commands to run in which order. (VERIFIED by listing.)
2. **Behaviour added by run-time patching.** The raw/cleaned-light switch works by `sap_twin.install` patching the loader, with module-level mode flags that are reset in a `finally`. It is tested (both suffixes route correctly), but it is fragile; the product should be a plain parameter of `detect_v2.load`.
3. **Freeze hash includes display code.** `stage3_report.py` is inside the settings hash, so after I corrected one display line (`pdc_half`) post-freeze, `stage3.py run` refuses to run the frozen settings. Nothing in the data changed (the tiers were rebuilt independently and match), but the coupling is wrong: the report should be outside the hash, with its own version.
4. **Silent failures.** `stage3.add_pdc` swallows per-file exceptions; they show up only as the "not measurable" counts (10 real, 9 upside-down) in report section 8. They should be counted and printed loudly.
5. **A design flaw inherited from v2.** `detect_v2.load` fills cadences that PDC dropped from locally scaled SAP flux. So the v5 "cleaned-light" half contains raw light in those stretches. It is rare in the one file I measured (134 of 10,395 cadences in one of 8 files, none in the other 7) but not measured over the whole run (FIX-QUEUE 21a). I caught it before freezing the v7 check by reading the cleaned light unfilled (`sap_twin.load_pdc`).
6. **Mutation checks are not in the repo.** The v7 mutation run lived in a scratch script outside the repository (VERIFIED from my session); the unit tests are in `test_stage3_prep.py`, but the "break the code and see the test fail" step is not reproducible by someone else. Earlier versions: not verified either way.
7. **A test that touches the owner's real database.** `pipeline/eyes_rules_test.py` writes to Ahmed's real Firestore. It must not be run casually. It should use an emulator or a test project.
8. **Reports grew by accretion.** `stage3_report.py` has eight numbered sections added version by version, with caveat lines that edit earlier sections' meaning.
9. **Environment fragmentation.** The repo venv, a separate docs venv, a separate venv for mono-cbp (GPL, kept outside the repo), pinned scipy and numpy versions. Plus quirks: `python - <<EOF` heredocs hang in this shell, so scripts must be files.
10. **Hard-wired assumptions about the 549.** The chain reads a star list, a manifest of cached files and a best-product table, but the download, manifest and coverage steps (`g1_download.py`, `coverage_g1.py`, `targets_g1.py`) assume the G1 layout. How many other places assume it is NOT TESTED. Running a new list will probably need work.
11. **Data not in git.** 6.0 GB under `data\` is local; the settings hash the inputs, but a second machine could not reproduce a run without re-downloading.
12. **Documentation is a diary.** `learnings-2026-10-27.md` is accurate and honest but chronological; there is no short architecture document, and `RESUME.md` is a long list of dated UPDATE paragraphs.

What I would keep: the frozen-version discipline, the regression guard, the aggregates-only rule, the claims register, `detect_v2`'s matched-filter core (read again on 28 Oct, no bug found).

## 12. An honest record of my own mistakes and judgment calls

Found by me or by review, all recorded in the notes. Included because a stronger reviewer should weigh my other conclusions accordingly.

1. v1 to v2 rules (eclipse overlap, repeater) were chosen after I had seen the v1 results. They are physics-based and applied identically to both sides, but they are not blind.
2. I diagnosed "red noise inflates SNR" (v3 era). Wrong; the SNR already used the measured scatter. Corrected in v4.
3. I proposed a scrambled control; it cannot remove single dips. Withdrawn.
4. I called 82.7 to 86.4% "completeness". It was the share of detected deep dips that survive the flags; only 72% were detected at all (about 62% overall, a ceiling).
5. My first pair search print counted every product and non-independent pairs (24 clean real dips, 10 real pairs on 2 stars); the fixed version shows 14 dips and 0 pairs. I saw the higher number first; both fixes lowered the real count.
6. The v6 report's "noise-expected real" line mixed the raw-light half into a statistic measured only on cleaned light, printing "33 real against 16.0 expected, chance 0.00". It is now restricted to the cleaned-light half (v6: 14 against 15.6, chance 0.69; v7: 14 against 14.2, 0.56). Nothing public quoted the bad line.
7. I wrote "every check removes more upside-down events". Wrong: the two eclipse checks remove more real ones. Fixed in all notes and the book.
8. The book's start pages still described version 4 after v7 existed. Fixed.
9. The v7 pooled common-moment flag was chosen on a symmetry argument, but I had already seen the same-kind (17 | 1) and no-burst (35 | 7) variants in the v6 data, so it is not a clean blind choice.
10. In chat I told Ahmed that the 7 raw-light-only dips "look like camera effects" and that the 21 "look like noise". Nobody has looked at them. That wording implied a look that did not happen; the book says "we think", labelled LIKELY, and my reasoning comes from counts. I also said "zero candidates"; more exact: zero I would call candidates, plus 7 I cannot test fairly.
11. The audit prompt that started the professional-tool comparison had two arXiv numbers swapped; caught on reading.
12. We kept circling the same 549 stars. I chose to repair the judge before widening the search, which is defensible, but the fix queue has no item at all for searching more stars, and I never put the breadth question to Ahmed. That gap is mine.

## 13. What we do not know (NOT TESTED list)

- The smallest planet (in Earth or Jupiter radii) found half the time, by star brightness, with every flag and the second-product check included.
- The cleaned-light half's flag neutrality (do the flags act equally on real and upside-down dips there?).
- How many true dips survive the whole chain in the raw-light half.
- The raw-light search in the 1,599 SPOC-family files that sit in QLP-best sectors, and the cross-file second-product rule (SPOC against TESS-SPOC).
- A control that keeps the raw light's lopsided noise.
- The effect of the SAP-filled cadences on the v5 cleaned-light half over the whole run.
- Anything about what a human sees in any event.
- The recovery of known planets other than TOI-1338 b (only that one had cached TESS data in a usable form).
- The actual number of planets in the unsearched part of the Kepler binary list and the TESS binary catalogue.

## 14. Probabilities (my judgment, UNCERTAIN, not measured)

- Before the search: about 18 in 100 of at least one findable planet in the 549 stars (model; range 5 to 40).
- Now, for "a dip worth a human look in the next 6 months": about 8 in 100 (range 3 to 15). For "a planet confirmed as real": about 1 in 100. These are gut numbers, lower than the prior because the 549 gave nothing and the blind spot is faint planets, and not zero because we now know where we are blind. The measured replacement is plan step 1.
- Progress: roughly 70% of the way to a search tool I would trust; about 5% of the way to a discovery. The book's own "readiness number" (48, last set 23 Oct) is stale.

## 15. The plan (work, in order; nothing in it has been started)

Effort is in the owner's AI-assistant budget points (the 28 Oct version-7 build plus a full bug hunt cost 4 weekly points, about 1.8 times my estimate) plus machine time. A stronger system will measure differently.

**Step 1. Measure the blind spot in planet size.** Extend `faint_recovery.py` and `sap_recovery.py` so injections run through the whole v7 chain (all flags, the second-product rule, the cleaned-light check) and report the dip depth converted to planet radius per star using the TIC radius and the brightness class (bright below 11, middle 11 to 12, faint 12 and fainter). Output: the smallest radius found 50% of the time per class; the share of the 549 stars where a Neptune, Saturn and Jupiter radius planet would be found. Then re-run the yield/chance model with the measured completeness to replace the 8-in-100 gut figure. Acceptance: with injections off it reproduces `aggregate_v7.txt`; fixed seeds; written to a result file. Effort 1.5 to 2.5 points, about an hour of machine. Risk: the injection shape and position conventions; document them.

**Step 2. Build a second target list ("G2").** Rebuild it ourselves from the public TESS eclipsing-binary catalogue (Prsa et al. 2022, VizieR) using the professionals' published cuts (detached, binary period above 7 days) minus G1; add Kepler-catalogue rows excluded by our cuts (fainter than 13.5, period below 5 days) for a separate "shorter period" pool. Do not copy the mono-cbp repository's table (GPL): rebuild from the primary catalogue. Check TESS magnitude, available sectors and products (QLP, SPOC, TESS-SPOC) through MAST. Output: counts by brightness class and data product, overlap with G1 and with their 591, and a reproducible script. Effort 0.5 to 1 point. Acceptance: list regenerates from a script; no network guesses. (From memory the catalogue has about 4,584 binaries in total: LIKELY, verify before use.)

**Step 3. Clean up the scripts behind a regression guard.** (a) One command `vesper run --stars <file> --version <hash>`; (b) data product (cleaned/raw) as a parameter of the loader, not a patch; (c) move the report outside the freeze hash with its own version; (d) count and print every swallowed error; (e) one `test` entry point that runs all test files and the mutation checks, with the mutation scripts committed; (f) move one-off diagnostics to `pipeline/old/`; (g) make the eyes rules test use an emulator; (h) a short `ARCHITECTURE.md`. **Guard:** after the refactor, v7 on the existing 5,082 groups must reproduce `aggregate_v7.txt` and all tier assignments byte for byte, and the Stage 2 regression (74 and 298 events) must stay identical. Effort 1.5 to 3 points. Risk: touching frozen code; no result may change.

**Step 4. Version 8: a sharper search for faint dips.** (a) A detrending window scaled to box length (target: keep at least 85% of a long dip's depth) with a measurement of the ramps a longer window admits; (b) store events down to SNR 5 (tiers still use 7) so pair search can link weak dips across sectors, plus an alias check; (c) optionally a trapezoid template. Regression: the old grid and window reproduce v7 exactly when selected; new tests with mutations; new freeze; judge by the cleaned-light half (where the control is usable) and by step-1 completeness gain. Adopt only if the planet-size gain is shown and false alarms (upside-down counts) do not rise faster than real ones. Effort 2 to 3 points, about 40 minutes of machine.

**Step 5. Run the frozen version on the new stars.** Rules frozen before any look; this is the first honest test because the earlier flags were shaped by what the 549 showed. About 1 to 2 points, a couple of hours of machine plus download time (data size not yet estimated).

**Step 6. A blind look at events.** Render plots of the 7 raw-light-only tier-1 dips, the 14 cleaned-light tier-1 dips, an equal number of upside-down tier-1 plots and matched random noise segments; shuffle with hidden labels; Ahmed (after Eyes practice) and I mark them in the Eyes style; then unblind. If the 7 are camera effects the shuffle should show it. This lifts the "nobody looks" rule for this set only and requires Ahmed's explicit yes (pending). Effort 0.5 to 1 point.

Total: about 8 to 13 points, two to three working days at Ahmed's 10-points-a-day rule. A quick alternative is steps 2 and 5 only, running v7 as it is on fresh stars (about 2 to 3 points).

Decisions: the name is **Vesper** (decided by Ahmed). Pending: the blind look; whether to start steps 1 and 2; renaming the pipeline in the book and notes (a small job I will do with the next publish).

## 16. Questions I most want a stronger mind to answer

1. **A fair null for single dips in skewed noise.** Given lopsided, correlated noise and a search that targets single dips, what null would you use? Options I have thought of and not tested: simulate noise that keeps skew and autocorrelation (block bootstrap of residuals after masking detected dips); run the identical search on a comparison population of non-binary TESS stars of equal brightness; calibrate reliability by injection and retrieval against the full flag chain and treat the vetting steps as a classifier (the Robovetter route). Which is defensible, and what are the traps?
2. **Sensitivity at low cost.** Which changes would move the half-recovery point from about 10 times the 8 h noise to something much lower: Gaussian-process or spline detrending with transit masking, a matched trapezoid filter, joint search across sectors, using 2-minute data where it exists, custom photometry from full-frame images, a model of the binary's eclipse-timing for circumbinary transit times? Which has the best gain per unit of effort and risk?
3. **Target selection.** Is the Prsa 2022 TESS binary catalogue, the unused Kepler rows or something else (for example Gaia eclipsing-binary candidates) the best next pool? What brightness and period cuts maximise expected discoveries? Should the next pool favour bright stars where small planets are visible?
4. **Detection statistics.** Is SNR 7 on a per-light-curve robust scatter a sound bar given about 5,000 star-sectors times many box positions? How should the look-elsewhere effect and the lopsided noise be handled in a threshold?
5. **Architecture.** Is the plan in step 3 right-sized? What would you restructure first so that a new star list, a new version, and a new data product are each a parameter and not a patch, while the frozen results stay reproducible?
6. **Review protocol.** Is the blind shuffled look in step 6 a sound way to lift the "nobody looks" rule without tuning to the answer? What would you add (pre-registered scoring rules, a second reviewer, the number of decoys)?
7. **What are we missing?** Anything a professional would do first that this document does not mention.

## 17. Rules you must respect

- **Frozen versions are never tuned on the 549 stars' results.** New rules are a new version, regression-proved first, frozen under a new hash, judged by real minus control per tier and by injection recovery, not by list length.
- **Real events stay private.** The public book gets aggregates only. No star IDs or event times in anything published.
- **Nobody looks at any real event** without Ahmed's explicit yes (step 6 asks for it).
- **GPL:** the mono-cbp repository stays outside our repo (`D:\ss-external`); do not copy its code or its table.
- **Label every claim** VERIFIED, LIKELY, UNCERTAIN or NOT TESTED with a source; never state a check as done when it was not. Prefer a script that can contradict you to a read of a plot.
- **No en or em dashes** in book text or replies; phone-first, short replies for Ahmed.
- **Do not run `pipeline/eyes_rules_test.py`** (it writes to Ahmed's real database), and never click the live Eyes page (answers upload to his real cloud).
- **Shell quirks (Windows):** use the repo venv's Python (`.venv\Scripts\python.exe`); write scripts to files; `python - <<EOF` heredocs hang.
- **Publishing the book:** push main first, then run `research\burn-3-book\tools\publish_book.ps1`; it builds a fresh clone and runs the gate.

## 18. File map (where to look)

| What | Where |
|---|---|
| Project status and dated updates | `RESUME.md`, `RESEARCH-PLAN.md`, `CLAUDE.md` |
| Diary of Stage 3 science and corrections | `research/stage3/learnings-2026-10-27.md` (17 sections) |
| Queue of open weaknesses | `research/stage3/FIX-QUEUE.md` (items 1 to 21) |
| Frozen settings, one per version | `research/stage3/SETTINGS_FROZEN.json` (v7), `SETTINGS_FROZEN_v1.json` to `_v6.json` |
| Result reports | `research/stage3/aggregate_main.txt`, `aggregate_v2.txt` to `aggregate_v7.txt` |
| Asymmetry, recovery, fairness, pairs | `asymmetry*.txt`, `faint_recovery_v5.txt`, `sap_recovery_v6.txt`, `sap_recovery_v7.txt`, `sap_fairness_fd788be04650.txt`, `pair_search_v5.txt` to `_v7.txt`, `step_retention.txt` |
| Yardstick against the professionals | `research/monocbp-b-lite-2026-10-28.md`, `research/stage3/monocbp_compare_30stars.txt`, `research/audit-2026-10-28-report.md` |
| Target list and coverage | `targets/g1_targets.csv`, `targets/g1_coverage.csv`, `pipeline/targets_g1.py` |
| Core detector | `pipeline/detect_v2.py` |
| Search driver and report | `pipeline/stage2_search.py`, `pipeline/stage3.py`, `pipeline/stage3_core.py`, `pipeline/stage3_report.py`, `pipeline/sap_twin.py` |
| Tests | `pipeline/test_stage3_prep.py`, `test_detect_v2_paths.py`, `test_hunt_prep.py`, `test_eyes_scores.py`, `regress_detect_v2.py` |
| Public claims register | `book/data/claims.csv` (F-001 to F-085) |
| Usage ledger (cost per task) | `research/usage-ledger.md` |
| Public pages most relevant | `book/docs/start/first-search.md`, `book/docs/start/story-so-far.md`, `book/docs/field-notes/2026-10-28.md` |

## 19. Glossary (our words)

- **Circumbinary planet:** a planet that orbits both stars of a binary.
- **Transit / dip:** the star's light drops a little when a planet crosses in front. We search for single dips because a planet around two moving stars does not repeat on a clean schedule.
- **Upside-down (flipped) control:** the same search run on 1 minus the flux. A planet is a dip, so the flipped curve has none; every dip found there is a false alarm.
- **PDCSAP / cleaned light:** NASA's systematics-corrected flux. **SAP / raw light:** the simple aperture flux before that correction. **SPOC:** NASA's 2-minute pipeline. **TESS-SPOC:** NASA's full-frame-image pipeline. **QLP:** the MIT quick-look pipeline.
- **Star-sector:** one star in one 27-day TESS observing stretch.
- **Tier:** a bin from best (1A) to flagged (2) to contradicted (3). Dips are sorted, never deleted.
- **Common moment:** many stars on the same camera having events at the same time, so the cause is the instrument or sky, not the star.
- **Repeater:** three or more events in one product and sector; a circumbinary planet cannot produce that.
- **Frozen:** settings, inputs and code fingerprinted before any result is read; a change is a new version.
- **Completeness / recovery:** the share of hidden fake dips the search finds.
- **Eyes mode:** the book's training game for spotting dips by eye.
