# Deep analysis after the sealed search (30 Oct 2026)

Written by Claude for Ahmed, the night the sealed search was scored. Everything marked **CONFIRMED** was measured on our own files and can be reproduced with the scripts in `research/stage3/post-sealed-analysis/`. Everything marked **exploratory** was computed after the scorecard was read, so it is not preregistered and does not change the scorecard. Labels used: CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED. No outside source was read for this file; every outside claim is parked as a question in `research/RESEARCH-QUESTIONS-2026-10-30.md`.

## 0. The answer in six lines
1. **The sealed result is a clean null on the rule we wrote first.** Real light kept 26 tier-1 dips, the upside-down copy kept 59, noise alone predicted about 42 real. NO EXCESS. CONFIRMED.
2. **The null has limited power.** A planted dip 14 times the noise is found 98% of the time but kept as tier 1 only 48% of the time. The filter throws away about half of what it finds. CONFIRMED.
3. **The development "excess" (78 real against 21 expected) did not replicate, and it was mostly clusters.** Those 78 events sat on 21 stars, up to 14 on one star. With the orbit-locked flag (c6) the development slice drops to 34 events on 18 stars against 20 upside-down events on 16 stars, and the star-level interval spans zero. CONFIRMED, exploratory.
4. **The test we preregistered counts events as if they were independent. They are not.** Next time the unit should be the star. LIKELY needed.
5. **The upside-down control is not a clean copy of noise.** Its ratio to the real light rises with signal-to-noise and differs between the two slices, and its surviving false alarms are short and deep (flare-like). The reason is UNCERTAIN.
6. **The one known planet, TOI-1338 b, was found in 1 of 7 strong tests.** That is about what the fake-planet tests predict for a faint single transit (LIKELY). In five later sectors the search saw real dips 0.6 to 1.4 days after the published prediction (UNCERTAIN, not counted).

## 1. What we did, in numbers
| Item | Number |
|---|---|
| Sealed stars searched, once | 594 (6,877 star-sectors; 6,734 with a best product) |
| Vesper version and fingerprint | 0.8.0 (0.7.1 plus orbit-locked flag c6), 5f73692944aa, matched the frozen hash |
| Wall time | search 19:28 to about 20:21; asymmetry test 6 min; completeness on 300 star-sectors 23 min; scorecard 10 s |
| Files read | 24,639 ok, 223 no safe windows, 3 too little data, 0 errors |
| Raw events (primary light curve, cleaned-light half) | 2,764 (1,265 real, 1,499 upside-down) |
| Tier 1 kept | 85 (26 real, 59 upside-down) |
| Confirmed (tier 1A, second light curve agrees) | 65 (17 real, 48 upside-down) |
| Leads (stars, known hosts removed, one per star) | 6 real stars, 25 upside-down stars |
| Planted dips in the completeness test | 14,508 rows from 300 star-sectors; 9,472 in the K 8 to 14 range |
| Cost to Ahmed's weekly usage | 3 points for the analysis, the two bug fixes and the leads section |

## 2. The scorecard, one line each
| Line | Result | Label |
|---|---|---|
| S1 excess of real over noise | NO EXCESS: real 26, upside-down 59, expected 41.8 (bars 8, 10, 12 also below expected) | CONFIRMED |
| S2 false alarms | 8.91 per 1,000 star-sectors against a mark of 8: FAIL on the point estimate; 95% interval 6.80 to 11.47 includes 8 | CONFIRMED |
| S3 mirror test | dips 37.5%, bumps 37.3%, gap +0.1 points: PASS (development slice: 38.1 against 39.9) | CONFIRMED |
| S4 completeness | 4 h 41.0%, 8 h 46.8%, 14 h 34.1%, 20 h 28.0% (K 8 to 14); only the 20 h box differs beyond both intervals, in the good direction (28.0 against 21.3) | CONFIRMED |
| S5 orbit-locked flag | 13 real events on 4 stars moved to tier 2, 0 upside-down; offline cost 0.51% of planted dips (development 0.81%) | CONFIRMED |
| S6 TOI-1338 b | 1 of 7 strong tests found (sector 37, 3 h box, SNR 8.0, tier 1L); 0 of 4 weak tests | CONFIRMED |
| S7 labels | no group shows an excess; after fixing the script: professionals' table 18 real against 44 upside-down (expected 31.2), TOI hosts 7 against 18 (12.8), not in their table 8 against 15 (10.6), none of the three 7 against 9 (6.4) | CONFIRMED |
| S8 machine health | all 6,877 star-sectors read, no errors | CONFIRMED |

## 3. What we learned about the filter

### 3.1 The funnel does not treat real and upside-down alike, and not the same way in the two slices
Retention from raw events to tier 1 (cleaned-light half, primary light curve):
| Slice | Real: raw to tier 1 | Upside-down: raw to tier 1 |
|---|---|---|
| Sealed, Vesper 0.8.0 | 1,265 to 26 (2.1%) | 1,499 to 59 (3.9%) |
| Development, 0.8.0 flags (c6 applied offline) | 773 to 34 (4.4%) | 711 to 20 (2.8%) |
So the filter keeps proportionally more upside-down events in the sealed slice and more real events in the development slice. No stable rule of thumb survives. CONFIRMED. The likely reason is in section 3.5: a few stars carry many events.

### 3.2 The filter costs about half of the true signal, even when the signal is strong
Planted dips, sealed slice, K 8 to 14 (depth in noise multiples):
| K | Found at all | Kept as tier 1 |
|---|---|---|
| 8 | 51.0% | 20.9% |
| 10 | 79.1% | 36.4% |
| 12 | 94.8% | 44.8% |
| 14 | 98.1% | 47.6% |
By box length: 4 h found 73.3%, kept 41.0%; 8 h 84.8% and 46.8%; 14 h 83.5% and 34.1%; 20 h 81.3% and 28.0%. Of 3,824 planted dips that were found, 2,050 (54%) were not tier 1: 1,836 stopped by a safety check, 25 by the second light curve, 189 with no tier recorded (UNCERTAIN, see 7).
Flags that fired on the lost planted dips (a dip can carry several): step 51.4%, gap or momentum dump 34.0%, ramp 18.0%, dominated 14.8%, catalogue-eclipse phase (c5) 10.7%, repeater 9.1%, eclipse overlap 6.6%, shared moment 1.2%, flip match 0%. The development slice gives the same picture (step 50.1%, gap 31.2%). CONFIRMED.
Meaning: the safety checks are the purity of the search, and their price is a completeness ceiling near 48% for tier 1. The earlier C-study measured the same trade: each option that adds recovery adds about one false alarm per 1,000 for each point gained. The planted dips are also not an upper bound on what a planet looks like (they are boxes pasted into real light curves), so the ceiling for a real circumbinary transit may be lower. LIKELY.

### 3.3 What the flags do to real and to upside-down events
Share of all events (SNR 7 or more, sealed) carrying each flag:
| Flag | Real | Upside-down |
|---|---|---|
| gap or momentum dump | 53.6% | 70.6% |
| step | 81.6% | 90.3% |
| ramp after a gap | 29.6% | 41.5% |
| repeater | 33.0% | 32.7% |
| dominated by a stronger event of the other kind | 26.6% | 21.5% |
| catalogue-eclipse phase (c5) | 12.9% | 7.2% |
| eclipse overlap | 8.1% | 4.3% |
| flip match | 2.5% | 0.0% |
| orbit-locked (c6) | 1.0% | 0.0% |
Reading: upside-down events sit more often at data gaps, steps and ramps (instrument edges, flipped), real events sit more often near the binary's own eclipses. The checks are doing what they were built for. The step flag fires on about 82% to 90% of all raw events, which makes it the single most active check and the one that costs the most planted dips. CONFIRMED (table), LIKELY (reading).

### 3.4 The upside-down control is not a clean mirror of noise
- **The ratio moves with signal-to-noise and with the slice.** Upside-down to real raw dips (1,500 random star-sectors, all products): sealed 1.09 at SNR 4.5, 1.27 at 6, 1.41 at 7, 1.78 at 10. Development 0.89, 0.96, 0.98, 1.04. CONFIRMED.
- **The preregistered estimate of the ratio is noisy.** On the full sealed run (primary light curve) the ratio at bar 7 is 1.18, not 1.41; development 0.92, not 0.98. With 1.18 the sealed expected real count is about 50 instead of 41.8, so the verdict does not change (26 against 50). CONFIRMED.
- **The false alarms that survive are short and deep.** Sealed upside-down tier 1: 44 of 59 in the 3 h box, 23 of 59 deeper than 1%, deepest 1.0e7 ppm (a spike ten times the star's flux). Real tier 1: 16 of 26 in the 3 h box, 3 of 26 deeper than 1%, deepest 265,216 ppm (26%). CONFIRMED.
- **Flares are the obvious suspect.** A flare is a fast upward spike; flipped it becomes a short deep dip that no instrument-edge check catches. LIKELY, NOT TESTED (needs a shape measurement; research question Q3).

### 3.5 Events cluster on stars, so the event-count test overstates certainty
Tier-1 events and the stars that carry them, cluster bootstrap over stars (20,000 draws, exploratory):
| Slice and version | Real events / stars | Upside-down events / stars | Real minus expected, 95% interval |
|---|---|---|---|
| Sealed, 0.8.0 | 26 / 17 | 59 / 36 | -15.8 (-42.2 to +8.3) |
| Development, 0.8.0 flags | 34 / 18 | 20 / 16 | +13.6 (-8.4 to +37.6) |
| Development, 0.7.1 | 78 / 21 | 21 / 16 | +56.6 (+13.2 to +108.6) |
In the development slice under 0.7.1, 78 events sat on 21 stars (3.7 per star, up to 14 on one star, the top three stars held 45%). With c6 the same slice gives 34 events on 18 stars and the interval spans zero. Counting stars with at least one tier-1 event: development 18 real against 16 upside-down; sealed 17 real against 36 upside-down; together 35 real against 52 upside-down over 895 stars. Raw events cluster too: in the sealed run one star carries 56 raw real events and the top ten stars hold 22% of them (development: 73 on one star, top ten 41%). CONFIRMED (counts), exploratory (the bootstrap).
Meaning: the development "EXCESS" under 0.7.1 was real in the sense of being repeatable on those stars, but it came from a few stars with repeated events at binary-locked times, which is exactly what c6 was designed to remove. The sealed slice was the honest test and it said null. This is what a sealed slice is for.
Concrete ceiling: with the cluster-robust interval, an excess larger than about 8 kept dips in 594 stars is excluded at 95%. Exploratory, but it is the most useful single number for the sentence "what did the null rule out".

### 3.6 The orbit-locked flag (c6) did its job
Sealed: 13 events on 4 stars moved to tier 2, all real (0 upside-down). Development: it flags 5.7% of real events and 0.1% of upside-down events. Offline cost on planted dips 0.51% to 0.81%. The harness cannot see other sectors, so the cost is an estimate. CONFIRMED.

### 3.7 TOI-1338 b, the one known planet in the sealed stars
By the preregistered rule (window 3 sigma plus 0.1 d, strong where the model transit share is 50% or more): 11 expected transits, 7 strong, 1 found (sector 37, 3 h box, SNR 8.0, tier 1L), 0 of 4 weak. Sealed completeness at K 8 for 4 to 8 h boxes is 22% to 27%, so 1 of 7 is about what a per-transit signal near K 8 would give (LIKELY; the K of TOI-1338 b itself is NOT TESTED).
After the fact, not part of the test (UNCERTAIN): the star's group files hold real events at sectors 65 (+0.6 d, two at tier 1A, SNR 9 to 10), 89 (+0.86 d, two at tier 1A), 93 (+0.92 d, one at tier 1A), 96 (+1.34 d) and 98 (+1.0 d), plus a tier-2 event at +0.26 d in sector 27. The offsets mostly grow with time. The prediction is an extrapolation from a 2020 fit, so a drifting ephemeris could explain it. Upside-down events also appear within a day of some epochs, so chance coincidence is not excluded.

### 3.8 Two absurd numbers that show missing guards
One star-sector (TIC 392536805, sector 76, QLP product, 15 h box) has a dip score of 3.5e26 (the noise estimate was close to zero); it was stopped by the gap and repeater checks. One upside-down event has depth 1.0e7 ppm. Neither changed a result, but nothing in the search refuses a depth above 100% or a near-zero noise estimate. CONFIRMED.

## 4. What the null does and does not mean
- **Supports:** in these 594 stars, Vesper keeps no more dips in the real light than noise predicts. The cluster-robust interval excludes an excess above about +8 kept dips.
- **Does not say "no circumbinary planets here".** Reasons, in order of size: (1) the filter keeps about half of the strong signals and about a fifth of the faint ones; (2) one TESS sector is about 27 days, while circumbinary periods in our own table are 95 days (TOI-1338 b), 187 and 303 days (Kepler-47 d and c), 229 days (Kepler-16 b), so most stars give 0 or 1 transit per sector; (3) the control is not clean (section 3.4); (4) the star list is eclipsing binaries, which also carry the most stray signals. Reasons (2) and (4) are NOT TESTED quantitatively (research question Q2).
- **Is it still a win?** Yes in the sense we defined on 29 Oct: a clean measured null, preregistered, sealed, frozen, reproducible. It is "clean" with two honest footnotes: the S2 false-alarm rate sits at the mark (8.91 against 8, interval includes 8), and the known-planet test shows modest sensitivity.

## 5. What worked
- **Preregistration, the sealed split and the frozen fingerprint.** The development slice said EXCESS, the sealed slice said NO EXCESS. Without the seal we would have believed the first one.
- **The upside-down control.** Imperfect, but it is the only reason the development excess could be questioned at all.
- **The planted-dip harness and the mirror test.** Dips and bumps are treated the same (gap +0.1 and -1.8 points): no sign bias in the chain.
- **Completeness generalised** from development to sealed within the intervals (one box better, none worse).
- **c6** removed repeated events on a few stars at a tiny cost.
- **The known-planet test written before the run** kept us from fitting the answer afterwards.
- **Data work:** 594 stars downloaded and audited with no errors; the search ran at 6 workers, about 50 minutes.
- **The live page and the leads rules,** including their own bug and the amendment written in the open.
- **Reproduction by an independent route:** the leads funnel rebuilt from the scorecard's loader gives 26 and 59 exactly.

## 6. What should be improved (items 31 to 60 in `FIX-QUEUE.md`)
- **The filter (needs a new Vesper version and a re-freeze):** depth and noise sanity guards; a flare-shape check; a review of the step check; a decision on the 3 h box; keep c6.
- **The scorecard (needs an amendment before the next run):** star-level counts and a cluster bootstrap beside the event count; a bar-specific asymmetry ratio from the whole run with an interval; a "found at all and kept" line in S4; clearer wording for S2 and the "did not generalise" label; an updated-ephemeris line for TOI-1338 b labelled post hoc.
- **Census:** run 0.8.0 over the 301 development stars so all 895 stars share one version and one lead list.
- **Leads and vetting:** the by-eye record, a crowding and pixel check, a "too deep for a planet" tag, both light curves on the card.
- **Harness and process:** read the data set and options from each run's own settings instead of environment variables; write a finished-marker file; add a regression test that the funnel equals the scorecard; fix the commit message of the data branch; note the preview tool's reload loop.
- **Book and learning:** chapter and learning-track checks for this result, a teaching note on clusters and on what a null means, the Downloads page, the real-time channel, F4, the unbuilt Eyes pages.

## 7. What we still do not know
- Why the sealed raw ratio (1.41) differs so much from development (0.98): activity of the stars, a few heavy stars, or something in the data. UNCERTAIN.
- Whether the short deep upside-down survivors are flares. LIKELY, NOT TESTED.
- Why 189 planted dips that were found have no tier recorded. UNCERTAIN (probably the harness records an empty tier when the event lies outside the primary product; to check).
- Whether TOI-1338 b's later events are the planet. UNCERTAIN.
- What detection probability a single sector gives for the circumbinary periods we care about. NOT TESTED.
- What the real tier-1 stars are (the 17 sealed and 18 development stars): probably other eclipsing binaries and variables, NOT TESTED beyond a look at the first two lead pictures (the first lead dips about 12% in its deepest bin, almost certainly an eclipse by a stellar companion, LIKELY).
- The Eyes-mode readiness numbers were last checked on 30 Oct and were not re-read for this file.

## 8. Process lessons (ours, not the filter's)
- Counting first-pass files instead of the scorecard's events produced a wrong funnel (129 against 72 where the scorecard said 26 against 59). Always count a finished run with the same loader the scorecard uses.
- A swallowed exception made the page wait for a file it could never read. Report unreadable files, and write an explicit finished marker.
- Scripts that depend on environment variables (data set, study options) silently use the wrong data when a variable is missing. Read them from the run's own settings.
- The labels report used the development noise file for the sealed run; every step that has a "which slice" choice should take it from the run name.
- Long jobs cost about 0.3 point per step in a fresh or compacted context and about 1 point per step at 500K tokens. Start analysis work in a fresh session.
- The Browser pane's preview of the book reloads in a loop because of the offline service worker; use the plain test page (`--no-livereload` or a static copy).

## 9. Files
- Scorecard: `research/stage3/benchmark-g2-sealed.txt`; labels `g2-by-label-sealed.txt`; asymmetry `asymmetry_g2_sealed_v5.txt`.
- Scripts and raw outputs of the exploratory analyses: `research/stage3/post-sealed-analysis/` (`analyse2.py` flag and cluster tables, `analyse3.py` planted-dip fate, `analyse4.py` star-level bootstrap, `toi1338_why.py` events near each expected transit; outputs next to them).
- Rules for the lead cards and their amendment: `research/stage3/LEADS-RULES.md`.
- Fixes: `research/stage3/FIX-QUEUE.md`, items 31 to 60. Research questions waiting for approval: `research/RESEARCH-QUESTIONS-2026-10-30.md`.
