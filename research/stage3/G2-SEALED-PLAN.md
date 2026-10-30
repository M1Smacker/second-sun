# Plan: the one-time search of the 594 sealed G2 stars as the Vesper benchmark (DRAFT, 30 Oct 2026; not started)

Status: **draft for Ahmed.** Nothing here runs until he says go. The locked rules in `G2-PREREGISTRATION.md` stay as they are; the benchmark items below that the preregistration does not already contain go in as a dated amendment (section 6) BEFORE any sealed file is downloaded. Version searched: Vesper 0.8.0 (frozen, hash 5f73692944aa), nothing else.

## 1. What we look for (the scorecard; every line has a pass mark or a report-only label written now)
| # | Question | How it is measured | Pass mark (written before the run) |
|---|---|---|---|
| S1 | Is there an excess of real dips over noise? | Preregistration section 5 unchanged: real tier 1 against noise-expected (upside-down tier 1 / asymmetry ratio of the same slice), per flux half, SNR bars 7, 8, 10, 12 | Excess only if Poisson chance 0.01 or less at bar 7 and real above expected at 8, 10, 12. Otherwise "no excess" (the expected and wished-for result: a clean null) |
| S2 | Do the false alarms hold on stars Vesper never saw? | Upside-down tier 1 per 1,000 star-sectors, with its 95% Poisson interval | 8 or fewer (development slice gave 7.07). Above 8 = "v8 did not generalise", reported, not fixed |
| S3 | Is the control still fair? | Mirror test: injected dips against injected bumps through the whole chain | Gap within 3 points (development +1.8) |
| S4 | How small a planet could we have found? | Preregistration section 6: `chain_recovery.py` on 300 random sealed star-sectors after the search; depth and length first, 50% depth, planet size as a labelled range | Report-only, next to the development numbers; a difference beyond the two binomial intervals is labelled "did not generalise" |
| S5 | The c6 price on these stars | `c6_orbit_lock.py` method (the harness cannot see other sectors, V8-DESIGN section 4) | Report-only; development was 0.81% |
| S6 | Does Vesper find a real known planet? | TOI-1338 b (TIC 260128333, the one NASA-listed circumbinary host, sealed). Before the run: count from the PUBLISHED ephemeris (paper, not our data) how many of its transits fall in the downloaded sectors. After: how many were found, what tier, and which flag stopped each one | Report-only; every transit in the data is accounted for (found and tier 1, found and flagged with the flag named, or missed with the reason) |
| S7 | The professionals' cross-check | Every result split by the labels clause (section 7): in the Davies et al. 2026 table, not in it, TOIs, none of these | Report-only |
| S8 | Did the machine work? | Files read, files skipped and why, errors, star-sectors searched | 0 unexplained errors; every skip has a reason |

S1 is the science; S2 to S8 are the benchmark. Together they are the "Vesper 0.8.0 on G2 sealed" scorecard. A script `benchmark_g2.py` prints it, written and tested on the development slice BEFORE the sealed search, frozen with its own hash, so v9 and later versions are scored by the same code.

## 2. What we keep and what we drop
Nothing is deleted. "Drop" means the event is labelled and left out of the tier 1 count; it stays in the files and in the report's counts by reason.

**Never searched (cut before the search):** cadences with bad TESS quality flags; the binary's own eclipses (masked from the catalogue ephemeris); data gaps.

**Found but moved to tier 2 (flagged, counted by reason):**
- `gap_dump`: within a day after a data gap or a momentum dump (spacecraft settling, scattered light)
- `common`: 3 or more other stars show an event at the same moment on the same camera (a spacecraft or camera glitch)
- `flipmatch`: the upside-down copy has an event at the same time (a symmetric wiggle, not a dip)
- `c5`: sits at a catalogue eclipse phase (an eclipse edge)
- `ecl_overlap`: overlaps a predicted eclipse
- `repeater`: many similar dips in the same light curve (likely another eclipsing pair in the pixels)
- `step`: the baseline jumps across the dip (a level change, not a dip)
- `ramp`: sits on a slow ramp near the start or end of an orbit
- `dominated`: a stronger event of the other kind in the same light curve
- `orbit_lock` (new in v8): repeats in another sector at a whole number of binary orbits with a similar length and depth (a leftover eclipse)

**Tier 3:** a second light curve of the same star and time exists and does not show the dip; or a raw-light-only dip that the cleaned light of the same file does not show.

**Kept (tier 1, the count):** 1A a second product agrees; 1L agrees weakly; 1B no second product exists. Tier 1 is a list of dips with no known innocent cause. It is not a list of planets.

**What a tier 1 dip gets next:** nothing is opened or plotted. Only an S1 excess opens two-key vetting (pixels, centroids, known-object lookup), and a human look only with Ahmed's yes and the Eyes ladder.

## 3. Order of work after Ahmed's go
1. Amendment (section 6) committed to the preregistration; `benchmark_g2.py` written, run on the development slice, frozen.
2. Sealed-run mode in `stage3.py`: refuses to run unless the rules-and-code hash equals 5f73692944aa and the slice is "sealed".
3. TOI-1338 b expected transit count from the published ephemeris (S6, before any sealed file is read).
4. Download the sealed light curves (size measured first and shown to Ahmed; G2 in all was about 28 GB, the sealed part is about two thirds; NOT measured exactly yet). Low priority, at most 6 threads.
5. One search, then the scorecard, then completeness on 300 sealed star-sectors, then the report (aggregates only), field note, book chapter and learning-track check.
If a bug is found afterwards: fix, run again, report both with the reason (preregistration section 3).

## 4. Cost (estimate, from the ledger)
Claude usage: about 3 to 5 points of weekly meter (amendment and scorecard 1 to 1.5; run supervision and report 1.5 to 2.5; book 0.5). Machine: download several hours; search about 1 hour (the whole development run, 301 stars, took 15 to 17 minutes); completeness 1 to 2 hours. Weekly meter now 58%, cap 70%.

## 5. Known limits, said now
- 594 stars give little power for a rare planet: a null is the likely outcome and is the win.
- TOI-1338 b was found in TESS data by others, so S6 is a check of our chain against a known answer, not a discovery test; it is one planet, so it shows a pass or a miss, not a rate.
- The asymmetry ratio for S1 comes from the same slice (preregistration rule); for the raw-light half there is no fair control (reported on its own line).
- c6 cost is measured offline, not by the harness.

## 6. Proposed amendment text (to be appended to G2-PREREGISTRATION.md only on Ahmed's go)
"Amendment 1, [date], before any sealed file is downloaded: the sealed search is also the Vesper benchmark. Added report lines S2 to S8 of G2-SEALED-PLAN.md with their pass marks; they change no list, split or excess rule. Version: Vesper 0.8.0, hash 5f73692944aa."
