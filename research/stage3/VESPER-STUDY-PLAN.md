# Vesper study: why it only finds giants, and how to find smaller circumbinary planets

Written 29 Oct 2026 by Claude with Ahmed ("your defaults"). Status: PLAN, approved in outline. No experiment has run under it yet.
Scope: G1 (549 stars) and the G2 development slice (301 stars) only. The 594 sealed G2 stars are not touched by anything in this plan.

## 0. Ahmed's decisions (29 Oct)
1. Order: first get everything single dips can give (the losses in the filters, and the long dips), then try stacking several transits.
2. Budget (updated 29 Oct, evening): weekly cap 60%, spent whenever Ahmed sits down to work, not split over days. No real star hunt during the study: only the filter is improved. Research: by Claude, up to 2 hours, and it stops as soon as everything needed is found and filed.
3. Yardstick false-alarm level: today's rate, about 6 to 8 upside-down tier-1 survivors per 1,000 star-sectors (G1 32 of about 5,064; G2 dev 25 of 3,253).
4. Models and stops: phases A and B on Opus 5.5 (Ahmed's choice: medium for B, C and the v8 design). STOP after A and B so Ahmed can switch to Sonnet 5.5 extra for phases C and D. STOP again before the v8 design so he can switch back to Opus 5.5 medium. Opus usage is tracked in its own ledger table (`research/usage-ledger.md`), never assumed equal to Sonnet's.
5. Version numbers and the before/after record: `research/stage3/VESPER-VERSIONS.md` (Vesper 0.7.1 is the baseline this study starts from).

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
### Phase A (29 Oct, Vesper 0.7.1; files `loss-ledger-0.7.1.txt`, `step-causes-0.7.1-g2.txt`)
- **Flags, not detection, lose the planets.** Fake dips at 10 x noise or more are seen at SNR 7 in 77 to 96% of cases, but only 38 to 57% reach tier 1. Lost to flags (primary but tier 2): 38% (G1), 45% (G2 dev). CONFIRMED.
- **The step (flat-baseline) flag is the biggest single cost and the biggest single guard.** As the ONLY flag it loses 5.8% (G1) and 11.3% (G2 dev) of all fakes; as the only flag it also removes 46 (G1) and 52 (G2 dev) upside-down events, more than any other flag. So it cannot simply be dropped; it must be made fair. CONFIRMED.
- **Why it fires on true transit shapes (H3, CONFIRMED on 150 G2 dev star-sectors, depth 12 x noise):**
  - 8 h dips: flagged 19%, every one because a side window has under half its data (a gap nearby). The lift part never fired. So for short dips the step flag is a second gap flag.
  - 20 h dips: flagged 49%: 34 for data cover, 27 for lift alone. The lifts are POSITIVE (median +0.21 of the depth even on unflagged events, 68% positive on flagged ones): the 2 d biweight bends down under a long dip and leaves raised shoulders. The same smoothing keeps only 68% of the depth (8 h: 91%) and the best box comes out at 15 h instead of 20 h. H2 and H3 are one problem: the smoothing makes the shoulders the step test then punishes.
- **Gap and dump flag:** on 34 to 37% of lost fakes, the only flag on 2.8% (G1) and 5.4% (G2 dev) of all fakes, but as the only flag it removes few false alarms (4 G1, 13 G2 dev upside-down). Poor value as it stands; candidate to scale with the box length (C3).
- **Repeater:** costs 1.2% (G1) and 3.9% (G2 dev) of fakes alone; prevents 32 and 5 upside-down alone. Must allow 2 to 3 transits in one conjunction (literature Q3).
- **Common moment:** costs 2.4% on G1 alone (Kepler field, crowded cameras), 0% on G2; prevents 26 upside-down on G1.
- **Long dips:** detection is NOT the main problem (90% seen at 10 x noise at 20 h); tier 1 falls from 56% (8 h) to 26% (20 h) on G2 dev, with the step flag on 47% of 20 h primaries against 11% at 4 h.
- **Stacking (H4):** G2 dev stars have a median 6 usable sectors (1 to 45). A planet of period 50 d gives a median 3 transits per star (113 of 301 stars get 4 or more); at 100 d a median 1.5; at 200 d and above stacking reaches no star at 16 transits. Stacking can help only short-period planets on many-sector stars. CONFIRMED arithmetic with an assumed 25 usable days per sector.
### Phase B (29 Oct; `vesper-study-literature-2026-10-29.md`)
- Smoothing window about 3 x the transit duration is the published guidance (wotan); Vesper uses one 2 d window for all boxes.
- Circumbinary transits vary in timing by days and in duration by hours, and can come 2 to 3 times in one conjunction: the repeater and orbit-locked rules and the injections must allow for this.
- Small circumbinary planets (under 3 Earth radii) have been reachable only by stacking with N-body timing on 4 years of Kepler data; for TESS single-sector stars "smaller" realistically means Saturn to Neptune on quiet stars.
- Kepler calibrated its vetting with inverted light curves (like our upside-down control) and offered a soft Disposition Score: supports C4.
### Before phase C (29 Oct, Opus; Ahmed: "do 1 to 3 and yes to download")
**1. Yardstick precision (`yardstick-precision.txt`, bootstrap over star-sectors).** One 300-star-sector run measures the 8 h K50 to about +-6% (G1) and +-10% (G2 dev) at 95%; the 4 h K50 to +-8 to 10%; the 14 h and 20 h K50 are not defined (recovery never reaches 50%: 14 h tops at 45 to 51%, 20 h at 28 to 44%). So the "10% better K50" rule of section 3 is at the edge of the noise, and useless for long dips.
**AMENDMENT to section 3 (29 Oct, written before any phase C experiment ran):** options are compared on the SAME injections (same star-sectors, times, depths, durations, seeds) through both versions. Primary measure per box length: injections gained (tier 1 in the option, not in the baseline) against injections lost (the reverse), at K 8 to 14; an option PASSES sensitivity if gained exceeds lost with an exact two-sided binomial p under 0.01 for the 8 h box OR for the 14 and 20 h boxes together, and no box length shows a significant net loss (p under 0.01). Reported alongside: the tier-1 share averaged over K 8 to 14 (the "recovery area") per box length, and the K50 where defined. The false-alarm rule (8 or fewer upside-down tier-1 per 1,000 star-sectors on full G1 and G2 dev runs) and the mirror rule (within 3 points) are unchanged.
**2. Primary sources read (details in `vesper-study-literature-2026-10-29.md`, addendum).** Wotan paper CONFIRMED: optimal biweight window about 3 x the searched duration, at least 2.2 x in white noise, and one fixed window for all durations loses sensitivity (a fixed window chosen for the longest transit lost 13% of Kepler test planets, mostly short ones on variable stars). Kostov et al. 2020 (multiple transits in one conjunction) and Oddo et al. 2026 (TESS M-dwarf eclipsing binaries, a published clean null: occurrence below 33% at 95% for 2 to 16 Earth radii, periods up to 600 d) CONFIRMED at the abstract or full text. Oddo et al.'s method: a predicted transit duration at EVERY moment from the binary's own motion (planet assumed at 6.27 x the binary period), a biweight window of 3 x that predicted duration chosen per moment (48 smoothed copies), an iterative cosine detrend, SNR 10 single-event search, automated vetting with LEO-vetter (pass/fail metrics), injection and recovery for completeness.
**New hypothesis H7:** our single 2 d window is 2.4 x a 20 h box but 8 x a 6 h box and 16 x a 3 h box, so for short dips it leaves stellar variability in the curve (more noise, more false alarms) while for long dips it bends under the dip. Both ends lose.
**3. Known-planet test set.** TIC 172900988 b (Kostov et al. 2021: Jupiter size, binary period 19.7 d with eccentricity 0.45, two transits 5 days apart in sector 21, one over each star; not in G1 or G2): 14 files downloaded to `data/known/172900988` (10.3 MB; sector 21 in QLP and TESS-SPOC 30 min, sectors 44 to 47 in all three products; logged). **TOI-1338 is in the SEALED G2 slice (TIC 260128333): it must NOT be used in phase C** (its B-lite results from 28 Oct stay as history only).

### Designs for phase C (for Sonnet to build; each option is a separate switch, default off, so 0.7.1 stays reproducible)
**C1 + C2: smoothing and a fair step test.**
- C1a (window per box length): for each box length d, smooth with a biweight window w = 3 d (at least 0.5 d) and search box d only on that curve; the real and the upside-down copies get exactly the same treatment. Cost: one smoothing per box length (9), about 2 to 3 times the search time.
- C1b (re-smooth around each event): after the search, mask the event (centre +- 0.75 x its box length) in the unsmoothed flux, smooth again with w = 3 x the box length, and re-measure depth, SNR and the step lifts on that curve. Cheap (events only). This removes the shoulders without changing the search.
- C2 (step test made fair): measure the lifts on the C1b curve; drop the data-cover part of the step rule (it duplicates the gap rule: phase A showed every 8 h step flag came from it) and let C3 own gaps; keep the 0.5 lift limit (no tuning).
- Order of tests: C1b + C2 first (cheap, events only), then C1a (changes the search), then both.
- Checks: paired injections on G1 and G2 dev (amended section 3); full G1 and G2 dev runs for false alarms; mirror test; TIC 172900988 b: report which of its two sector 21 transits each version finds (a report line, not a pass rule).
**C3: gap and dump rule scaled with the box length.** Today an event is flagged if it sits near a gap edge or dump by a fixed amount. Option: flag only if the gap or dump falls INSIDE the box or within half a box length of it, and if under half of the box itself has data. Same checks.
**C4: one calibrated score instead of nine yes/no flags.**
- Features per event (continuous, no kind label): SNR; second-product SNR (or none); step lifts and side cover; distance to the nearest gap or dump in box lengths; time since data resumed; distance to catalogue eclipse phases in eclipse widths; events of the same kind in the same product and sector; other stars with an event within 0.1 d; own SNR divided by the strongest opposite-kind SNR in the same curve; box length.
- Model: logistic regression (few, readable weights; no deep learning). Positives: injected planet-shaped dips that came out as primary events (chain_recovery harness). Negatives: upside-down primary events of the full runs. Train on G1, test on G2 dev, and the reverse; never use a real event.
- Operating point: the score cut that gives 8 upside-down tier-1 per 1,000 star-sectors on the held-out set. SAP-only events stay outside the score (no fair negatives for the SAP half, FIX-QUEUE 18).
- Checks: paired injections, mirror test (the score is blind to the kind, so bumps and dips must pass alike), and a printed weight table so a reader can see what the score rewards.
**C5 (later): physical transit duration per moment, as in Oddo et al.** Needs the stars' masses and radii (G2 has none; TIC radii need a MAST query, a download that needs Ahmed's yes). Without them, use a wide default range.
**C6: orbit-locked flag** (FIX-QUEUE 30) with the exception for 2 or 3 transits within one conjunction; tested with injected same-conjunction pairs and on TIC 172900988 b.

### What phase C should test first (proposal for Ahmed)
1. **C1 + C2 together:** smoothing window scaled to about 3 x the box length (or the box masked before the smoothing), and the step test measured on that flux, with its cover rule merged into the gap rule. Expected: most of the 20 h loss back, short dips unchanged. Pass rule: section 3.
2. **C3:** gap and dump window scaled with the box length.
3. **C4:** one calibrated score instead of nine yes/no flags.
4. **C6** orbit-locked flag with the same-conjunction exception; **C5** physical box range last.

## 7. Phase C results (30 Oct 2026, Sonnet 5.5 extra)
**C1b and C2 (switches `c1b`, `c2`, default off; `pipeline/vopts.py`, `stage3_core.resmooth_stats`, `test_vopts.py` PASS; default-off identity proved on 300 of 300 star-sectors).**
- **Sensitivity (paired, same injections, K 8 to 14; files `paired-c2-g1/g2.txt`, `paired-c1bc2-g1/g2.txt`): PASS.** c2 alone never loses a fake (gained 135 and lost 0 on G1; 330 and 0 on G2 dev). Long dips (14 and 20 h): c2 net +53 (G1), +139 (G2 dev); c1b+c2 net +90 (G1), +195 (G2 dev) but it also loses 67 and 51 that the baseline kept (8 h box: no significant loss). Mirror gap +1.8 to +2.2 (rule within 3): pass.
- **False alarms (full runs, `fa-counts.txt`): FAIL.** Upside-down tier-1 per 1,000 star-sectors (rule 8 or fewer): baseline 6.32 (G1), 7.69 (G2 dev); c2 9.28 and 12.60; c1b+c2 9.28 and 12.30. Real tier-1 rose too (G1 21 to 47 or 36; G2 dev 90 to 125 or 112), but about half of what the option adds is noise-like.
- **Same false-alarm budget (`bar_budget.py`, `paired-bar.txt`; the yardstick is sensitivity at a fixed budget).** The lowest SNR bar that restores 8 per 1,000 is 7.5 (G1) and 8.25 (G2 dev) for c2, 7.5 and 8.5 for c1b+c2; one version needs one bar, so 8.25 and 8.5. At those bars both options LOSE sensitivity against the baseline at 7: c2 net -360 (G1) and -138 (G2 dev) of about 9,000 dips; c1b+c2 net -441 and -164. Only the 14 and 20 h boxes on G2 dev hold even (c2 +7, c1b+c2 +27, not significant). **VERDICT: NOT ACCEPTED (CONFIRMED on our own paired numbers, G1 and G2 dev).** The step flag costs sensitivity but blocks upside-down events at a better rate than a higher bar would; raising the bar is a worse trade. Reading of the data, not a tested cause (UNCERTAIN): the extra upside-down survivors are probably level steps and long-period systematics that the flag was catching.
- What this settles: the flat-baseline flag is NOT a free lunch to remove; any fix has to keep what it catches. The data-cover rule alone (c2) is the cheap part, and its removal alone gave +14 to +139 dips with the false-alarm rise above; the question for C4 is whether a score can keep the guard and still give the dips back.
**C4-lite: reweigh the existing flags (`flag_patterns.py`, `flag-patterns.txt`; pattern = the 9 flags plus "second product disagrees"; patterns passed best-ratio first until 8 per 1,000 upside-down on the TRAINING set; trained on one set, scored on the other).**
- Train G1, score G2 dev: passes the clean pattern plus ramp, gap-edge and two mixes; fakes recovered +377 net, 0 lost (38.1% to 46.4%), BUT upside-down tier-1 on G2 dev is **15.4 per 1,000** (rule 8). The budget does not transfer: the same flags leak about 4 times more upside-down events per 1,000 star-sectors on G2 dev than on G1 (gap edge 4.0 against 0.8, ramp 2.5 against 0.2 per 1,000).
- Train G2 dev, score G1: only "c5 + step" is added to the clean pattern; recovery +2 of 9,568 (nothing). In-sample on G2 dev: +1.0 point.
- **Reading (LIKELY, from these two directions only, small counts): at the current false-alarm level the nine yes/no flags are close to the best possible use of their own information; the waivers that buy sensitivity (ramp, gap edge) only work if we accept about 2 times the false alarms on G2-like data.** Exchange rate seen on G2 dev: about +1 point of dip recovery for each +1 upside-down tier-1 per 1,000 star-sectors. Whether to spend that is a policy call (the budget of 8 was my pre-written yardstick, not a physical limit), so it goes to Ahmed at the v8 design as a real fork with this slope attached.
- Calibrate on G2 dev for the sealed slice (same population by construction, hash split); G1 is a different population for this purpose.
**C4: one calibrated score (`score_c4.py`, `score-c4.txt`; features harvested by `paired_recovery.py` with `PAIRED_FEATURES=1`: lifts, side cover, ramp distance, eclipse distance, burst, common, repeat, phase distance, box length; trained on SNR 7 to 10 only; cut set for 8 per 1,000 on the training set from out-of-fold scores).**
- Across sets: logistic G1 to G2 dev gives +312 dips but 11.4 false alarms per 1,000; G2 dev to G1 gives -352 dips and 8.3 per 1,000. Boosting (the ceiling check): G1 to G2 dev 6.8 per 1,000 and -43 dips (p 0.16); G2 dev to G1 6.1 per 1,000 and -126 dips. Nothing beats the flags while holding the budget on the other set.
- Within G2 dev (two different half splits, both directions, both models; the sealed slice is G2-like): false alarms on the held-out half range from 3.1 to 17.1 per 1,000 (target 8) and net dips from -518 to +127. **UNCERTAIN whether a G2 calibration would hold on the sealed slice; the data we have cannot say, because a cut calibrated on about 25 upside-down survivors is noise (Poisson spread about +-5).** NOT ACCEPTED.
**Strong dips do not escape the flags (`snr_waiver.py`, `snr-waiver.txt`).** Waiving the flags for events at SNR 16 or more would still pass 65 to 75 upside-down events on G1 (12.8 to 14.8 per 1,000) and 123 to 157 on G2 dev (38 to 48 per 1,000): strong upside-down events are mostly systematics that the flags catch, not noise. Waiving only the step flag at SNR 10 or more: G1 8.1 and G2 dev 10.8 per 1,000 for +1.8 and +5.7 points of dip recovery. CONFIRMED on our own data (G1 and G2 dev). **So the ceiling on tier-1 recovery (44 to 64% even for deep dips) is the price of symmetric systematics (gaps, ramps, steps, repeats): they hit planet-shaped dips and upside-down dips alike. Flags cannot be loosened for free; the only ways up are a better systematics correction before the search (the upside-down control keeps us honest) or more data per candidate (stacking, phase D).**
**C1a: each box length gets its own smoothing window, 3 x the box (at least 0.5 d) (switch `c1a`; `paired-c1a-g1/g2.txt`, `fa-counts.txt`; test PASS; switches-off identity 300 of 300 star-sectors).**
- **Sensitivity: FAIL.** 8 h dips: net -73 (G1) and -163 (G2 dev) of about 1,200 each, exact p below 0.0001, i.e. -6.1 and -14.3 points of recovery. 14 and 20 h: about even (-14, -8). 4 h dips: +54 on G1 (p below 0.0001) but -3 on G2 dev. A gain on one set that does not appear on the other is not a result.
- **False alarms: FAIL on G2 dev.** Upside-down tier-1 per 1,000: G1 6.32 (same as baseline), G2 dev 9.84 (baseline 7.69; rule 8). **Mirror test: FAIL on G2 dev** (dip against bump gap +5.6 points, rule within 3; G1 +2.2 pass).
- Fixed-budget run not needed: raising the SNR bar can only remove passes of the option, so a net loss at the same bar can only grow. **VERDICT: NOT ACCEPTED (CONFIRMED on our paired numbers).**
- **Why (CONFIRMED on a synthetic star, `window_depth_kept.py`, `window-depth-kept.txt`):** a biweight window of 3 x the dip is too short; on a quiet star it eats 25% of an 8 h dip (the 8 h dip keeps 96% with the 2 d window, 75% with the 1 d window) and about 26% of a 4 h dip. The 3 x rule of thumb belongs to a detrend that masks the transit; ours does not (the dip is the thing we search for). The step flag also fires on far more events with the short windows (real events flagged: G1 857 to 1,165, G2 dev 1,103 to 2,126), LIKELY a second cost: the flags were set on the 2 d curve.
- **The same table shows the real weak spot of the 2 d window: it keeps only 82% of a 14 h dip and 62% of a 20 h dip** (matches phase A: 20 h dips keep 68%). A window of 5 x the box keeps 96% (14 h) and 97% (20 h); 4 x keeps 89% and 92%; 3 x keeps 82% and 77%.
**C1c: a longer window for the long boxes only (switch `c1c`). PRE-REGISTERED 30 Oct 2026 BEFORE any c1c run on real data.**
- Rule: for boxes of 10, 12, 15 and 20 h the curve is smoothed with a biweight window of 5 x the box (2.08, 2.5, 3.1, 4.2 d); boxes up to 8 h keep the 2 d curve (bit-identical by construction; `test_vopts.py` checks it); the step test keeps the 2 d curve (as in c1a). Why 5: the smallest tested multiplier (3, 4, 5, 6, 8) that keeps at least 95% of the depth at both 14 h and 20 h on the synthetic star; chosen from the synthetic table above, NOT from any real-data result.
- Expected: more depth and SNR for 14 to 20 h dips (about +15% SNR on a quiet synthetic 20 h dip, `test_vopts.py`). Risk: a longer window lets slow stellar variability and systematics through in the long boxes, so upside-down events may rise there. The upside-down control decides.
- Same yardstick as every option: paired gain with no box losing significantly, upside-down tier-1 at most 8 per 1,000 star-sectors on G1 and on G2 dev, mirror gap within 3 points. Fixed-budget bar check only if the false alarms exceed 8.
