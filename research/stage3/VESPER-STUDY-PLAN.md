# Vesper study: why it only finds giants, and how to find smaller circumbinary planets

Written 29 Oct 2026 by Claude with Ahmed ("your defaults"). Status: PLAN, approved in outline. No experiment has run under it yet.
Scope: G1 (549 stars) and the G2 development slice (301 stars) only. The 594 sealed G2 stars are not touched by anything in this plan.

## 0. Ahmed's decisions (29 Oct)
1. Order: first get everything single dips can give (the losses in the filters, and the long dips), then try stacking several transits.
2. Budget: about 3 weekly points per day for about 3 days, inside his daily stop line. Research: up to 2 hours, by Claude.
3. Yardstick false-alarm level: today's rate, about 6 to 8 upside-down tier-1 survivors per 1,000 star-sectors (G1 32 of about 5,064; G2 dev 25 of 3,253).

## 1. What we already know (measured, our own files)
| Fact | Number | Source |
|---|---|---|
| Fake 8 h dips seen at SNR 7 in some product | 26% at 6 x noise, 53% at 8 x, 80% at 10 x | `chain_recovery_g2dev.txt` section 3 |
| Fake dips at 10 x noise or more that end in tier 1 | 45%; 45% are thrown out by flags; 7% never seen; 3% not primary | same, section 2 |
| Flags on those thrown-out fakes | flat-baseline step 55%, gap or dump 34%, 1 d ramp 18%, repeater 15%, C5 12%, eclipse overlap 10%, dominated 8% | same |
| Half found (K50) | about 10.5 x the 8 h noise for 8 h dips (about 3,500 ppm on the median G2 star); never reached up to 18 x for 14 h and 20 h dips | same, section 4 |
| 2 d smoothing keeps of a dip's depth | 57% at 20 h, 68% at 15 h (3 d window: 72%, 79%) | FIX-QUEUE 11 |
| Control fairness for planet shapes | dip 35% vs mirror bump 37% (G2 dev), 32% vs 34% (G1) | chain recovery files |
| Apparent G2 excess | 90 real vs 25 upside-down tier 1; 54 of the 90 are orbit-locked on 8 stars | `g2-dev-results-2026-10-29.md` |
| Known circumbinary planet periods (NASA table) | 53 rows, shortest 43 d, middle 934 d | `data/xmatch/cbp.csv` (no radii in our copy) |

## 2. Root-cause hypotheses (each gets a test)
- **H1. The filters are blunt vetoes.** Each flag is yes or no, so a planet that trips any one is lost. Expected gain if fixed: half-found point from about 10.5 x to about 8 x noise, planets about 15% smaller (LIKELY, arithmetic on section 1).
- **H2. The smoothing eats long dips.** A 2 d biweight window is too short for 14 to 20 h transits, and the flat-baseline flag then fires on the shoulders the smoothing leaves. Expected gain: large for long dips, none for short ones (LIKELY).
- **H3. The flat-baseline test misfires on true transits.** It trips on 55% of the flagged fakes, through too little data on a side, through variability, or through smoothing shoulders. Which one is NOT TESTED.
- **H4. Single dips have a physical floor.** One transit at SNR 7 means giants on most stars. Stacking N transits lowers the needed depth by the square root of N, so the planet radius only falls with N to the power 1/4 (4 transits: about 30% smaller; halving the radius: 16 transits). Long-period circumbinary planets give few transits in TESS (CONFIRMED arithmetic; the transit counts per star are NOT TESTED).
- **H5. Too many trials.** We search every box length 3 to 20 h on every star. A physical limit on the transit length per star (from the binary period and the stars' size) cuts trials, so a lower bar costs no extra false alarms (UNCERTAIN size of the gain).
- **H6. Binary leaks pose as planets.** Shallow secondary eclipses of eccentric binaries pass the catalogue phase test (FIX-QUEUE 24, 30). This hurts purity, not sensitivity, but it decides what false-alarm level we can afford.

## 3. The yardstick (decided before any experiment)
One scoreboard, run the same way for every option:
- **Sensitivity:** K50 and the ppm depth at which half of injected planet-shaped dips reach tier 1, per box length (4, 8, 14, 20 h) and brightness class. Same injection grid and seeds as `chain_recovery.py` (300 star-sectors from G1 and 300 from G2 dev, seed 20261029).
- **False alarms:** upside-down tier-1 survivors per 1,000 star-sectors on the full G1 run and the full G2 dev run.
- **Fairness:** the mirror-bump test (dip against bump recovery, paired) must stay within 3 percentage points, and real raw counts must stay consistent with the measured asymmetry ratio.
- **A change is ACCEPTED only if** the 8 h K50 or the 14 to 20 h K50 improves by at least 10%, the false-alarm rate does not rise above 8 per 1,000 star-sectors on either set, and the mirror test still passes. Anything else is recorded as a negative result, not discarded.
- Never judged by: the number of real tier-1 events, or any single real event.

## 4. Phases
### Phase A: loss ledger (no new search; about 1 point)
1. Per flag, the planets it costs (from `rows_v7.pkl` and `rows_g2dev.pkl`) against the false alarms it removes (upside-down ladder, both sets). Output: one table, "flag, planets lost per 100, false alarms removed per 100".
2. Split the flat-baseline flag by cause (data cover, lift before, lift after) on injections. Needs one small re-run that stores the lift values: about 15 minutes of machine time.
3. Split the long-dip loss into smoothing (depth kept) and flags.
4. Count transits per star that a circumbinary planet could give in our data (sectors per star, planet periods from physics), to size the stacking idea (H4).

### Phase B: research (Claude, up to 2 hours, public sources, CONFIRMED or UNCERTAIN labels with links)
Questions, each with the decision it feeds:
1. Sizes, periods and transit durations of the known transiting circumbinary planets (NASA Exoplanet Archive, discovery papers). Feeds: what "smaller" can mean for TESS.
2. How published searches detrend around long transits (wotan paper guidance on window length, iterative masking, GP methods). Feeds H2.
3. How circumbinary searches link single transits across time (mono-cbp, Davies et al. 2026; the TESS discoveries; Kepler searches). Feeds H4.
4. How vetting is done without hard vetoes (Kepler Robovetter style metrics, scores, machine-learning vetters) and how false alarms are calibrated. Feeds H1 and H3.
5. Expected transit duration for circumbinary planets as a function of binary period and stellar size. Feeds H5.
Output: `research/stage3/vesper-study-literature-2026-10-29.md`, one section per question, each with its source and label.

### Phase C: experiments (about 3 to 4 points; each one scored on section 3)
- C1 smoothing: window 2 d against 3 d against mask-and-refit around each candidate box (and one GP option if Phase B supports it).
- C2 flat-baseline test made fair: scale its windows and its cover rule with the box length, and measure the lift on the unsmoothed flux.
- C3 gap and ramp rules scaled with box length.
- C4 soft score: replace the yes or no flags by one planet-likeness score, calibrated on fakes (positives) and upside-down events (negatives); pick the cut that holds the yardstick false-alarm rate.
- C5 physical box-length limit per star (H5).
- C6 orbit-locked flag (FIX-QUEUE 30) and eclipse phases from the masked runs (FIX-QUEUE 24).
Each run on the development data only; each option is a separate measured line, not a pile of changes.

### Phase D: stacking (only after C; about 2 to 3 points)
Lower the single-dip bar to SNR 5, link dips of one star across sectors with timing slack, and judge the links against links made of upside-down dips. Accept only if the yardstick improves.

### Phase E: v8 (needs Ahmed's go)
Combine the accepted options, prove G1 regression and mutation tests as for v7, write the result into the book, freeze under a new hash. The sealed G2 run still needs its own go.

## 5. Guard rails
- Real events are never opened; aggregates only. The sealed slice is untouched.
- Every option and every negative result is logged in this file's results section and in the ledger.
- Heavy jobs at BelowNormal with thread caps (about 68% CPU).
- If a step takes more than 1.5 times its estimate, stop and tell Ahmed.

## 6. Results
(filled as phases finish)
