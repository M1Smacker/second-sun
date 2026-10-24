# Second Sun feedback engine: research report and working prototype

*For Claude Code. Written 2026-10-24. Tags: `[READ]` primary source opened in this session; `[READ-2]` secondary page opened (summary, press page, encyclopaedia, citing paper); `[MEMORY]` from training, not opened; `[INFERRED]` my reasoning or recommendation; `[RAN]` output of the prototype code shipped with this report (`feedback-engine/`). Thresholds come from my own simulator, which imitates your card kinds but is not your generator: **recalibrate everything with `calibrate.js` and `table.js` on your real decks before trusting a number.***

## What is in the bundle

| File | What it does |
|---|---|
| `engine.js` | The engine: `measure(y)` returns about 40 facts; `compose(facts, ctx)` returns three lines; `newLearner()` and `record()` keep the adaptive state. Plain JavaScript, no dependencies, about 33 KB unminified, 362 lines |
| `sim.js` | My card simulator (13 kinds, seeded and deterministic) |
| `calibrate.js`, `table.js` | Feature distributions per kind, separation scores (AUC), lesson firing and precision |
| `test.js` | 4,160 compositions: same input gives the same text; every number in the text is a computed number; 36 to 44 words; no dashes; no verdict words in real mode; plus a 34-card habit round |
| `examples.js`, `habits.js`, `assemble.js` | Produce the 50 worked examples in section 4 |

Current results `[RAN]`: 4,160 compositions, 0 failures, 38 to 44 words each. Generating and measuring a card takes about 4 ms in Node 22 (most of that is generating hard-noise cards, which searches a whole simulated sector). Over a 60-card session of hard-noise cards the engine used 7 different lead lessons and 46 different first lines, never the same lead more than twice in a row.

---

## 1. What the research says makes feedback teach

### 1.1 Solid findings

**Feedback helps on average, but often hurts.** Kluger and DeNisi's meta-analysis (607 effects) found a mean d of 0.41, yet more than a third of feedback interventions made performance worse; feedback backfires when it pulls attention from the task to the self (praise, comparisons, judgements of the person) `[READ-2: psychsafety.com summary of Kluger and DeNisi 1996, Psychological Bulletin 119, 254]`. A 2020 meta-analysis of 435 studies found d = 0.48 overall, with "high-information" feedback (task, process and some self-regulation information) at d = 0.99, corrective feedback at 0.46, and reinforcement or punishment at 0.24 `[READ: Wisniewski, Zierer and Hattie 2020, Frontiers in Psychology 10]`. That paper summarises Hattie and Timperley's model: feed up (where am I going), feed back (how am I doing), feed forward (what next), at task, process, self-regulation and self levels, with self level (praise) the weakest `[READ-2: via Wisniewski et al. 2020]`. *For you:* every line about the card, nothing about Ahmed as a person; a "what to check next time" line is the feed-forward part.

**Elaborated beats verdict-only, if it stays short.** Shute's review: response-specific elaboration improves learning efficiency more than simple verification; "if feedback is too long or too complicated, many learners will simply not pay attention to it"; give elaboration "in small enough pieces"; focus on the task, not the learner; use praise sparingly, if at all; avoid comparisons with other students `[READ: Shute 2008, Review of Educational Research 78, 153, Tables 2 to 5]`. Your 40-word, three-line limit fits this.

**Timing: immediate for novices and hard tasks.** Shute recommends immediate feedback for difficult tasks and for low-achieving learners, delayed feedback for simple tasks and high achievers `[READ: Shute 2008 Tables 4 and 5]`. In category learning where the rule is hard to put into words ("information-integration" tasks, which judging noisy curves resembles), deferring feedback until after a block of six trials impaired learning, while easy verbal-rule tasks were unaffected `[READ-2: a 2024 bioRxiv replication summarising Smith et al. 2014; the original Maddox, Ashby and Bohil 2003 study is MEMORY]`. *For you:* reveal right after he locks, not at the end of a round.

**Perceptual learning needs easy cases first.** Training only on difficult cases "typically" produces no learning; easy cases start the learning process and transfer more widely, whereas difficult conditions are learned in a more specific way `[READ: Ahissar and Hochstein 2004, Trends in Cognitive Sciences 8(10)]`. Gravity Spy introduces glitch classes in levels of 2, 6, 10 and then all 22, and volunteers trained this way with machine-learning-chosen easy examples were 90% accurate against 54% for volunteers given all 22 at once `[READ-2: Zooniverse blog, December 2020, summarising two papers it links but does not name]`.

**Perceptual learning works by classification with feedback, many varied items, and contrast.** Kellman's principles: many brief classification trials with feedback; items rarely repeat; positive examples vary in irrelevant features; and "negative instances must share with positive instances the values and dimensions of irrelevant properties", so learners attend to what actually differs; adaptive sequencing brings missed items back soon and retires them on accuracy plus speed. In histopathology, year-1 accuracy went from 54% to 66% and response time from about 15.8 to 6.2 s `[READ: Kellman 2013, Military Medicine 178(10S), 98]`. *For you:* near-twin contrasts (a hard-noise card next to a limit planet with the same noise level, duration and gap layout) are the single most research-backed format for your hardest confusion.

**Interleave the confusable classes.** Interleaving paintings by different artists gave 0.61 against 0.35 accuracy on new paintings, yet most learners believed blocking worked better `[READ: Kornell and Bjork 2008, Psychological Science 19(6)]`. Interleaving helps when categories are very similar (it draws attention to differences); blocking helps when they are dissimilar (it draws attention to what members share) `[READ: Carvalho and Goldstone 2014, Frontiers in Psychology 5, 936]`. *For you:* interleave hard noise with limit planets; it is fine to block the obviously different kinds (eclipses, spikes) early.

**Feedback mostly fixes bias, which is exactly Ahmed's problem.** Perceptual learning occurs "even without feedback"; in Petrov, Dosher and Lu's experiments feedback's main role was "to induce more stringent criterion (bias) control" rather than change the learning rate `[READ: Petrov, Dosher and Lu 2006, Vision Research 46, 3177]`. They report that Herzog and Fahle found block feedback can be "as efficient as trial-by-trial feedback" when learning without feedback fails `[READ-2: via Petrov et al. 2006]`. Ahmed "calls even weak noise a dip": that is a liberal criterion, not poor sight. Aggregated "pattern" messages (section 5) are the block-feedback mechanism for shifting it.

**Radiology and image reading.** Expertise comes from deliberate practice "with accurate and detailed immediate feedback and opportunities for repetition"; "simply informing radiologists about potential errors does not improve their perception"; PALM gains persisted about 6 months; novices trained for about 52 minutes matched board-certified radiologists on hip-fracture detection in one study `[READ: Waite et al. 2019, Frontiers in Human Neuroscience 13, 213]`. *For you:* telling him "gap dips are artifacts" is not enough; he needs many gap-dip cards with measured feedback.

**How Planet Hunters TESS and Space Warps train.** Planet Hunters TESS mixed simulated transits into 30% of a volunteer's first 10 subjects, falling to 1% by 100, showed only simulations above SNR 7 (later 4), and always told the volunteer afterwards `[READ: Eisner et al. 2021, MNRAS 501, 4669, §2.1]`. Space Warps started at about 2 in 5 training images, never below 10% "to keep volunteers alert", gave pop-up feedback after each, and kept a confusion matrix per volunteer `[READ: Marshall et al. 2016, arXiv:1504.06148, §2.2.2, §4]`. Both gave verdict feedback ("you spotted a simulated lens"), not measured explanations `[READ]`; your engine goes further than either.

### 1.2 Weaker or mixed evidence

**Fading feedback (the "guidance hypothesis").** In motor learning, feedback on every attempt is said to create dependency (Salmoni, Schmidt and Walter 1984; Winstein and Schmidt 1990), but the paper I opened that tests it found the 100% feedback group did not do worse as the hypothesis predicts `[READ-2: Nunes et al. 2014, Frontiers in Psychology 5, 1454]`. Treat "fade feedback" as plausible, not proven, for perception.

**Expertise reversal.** Guidance that helps novices can hurt once they know the material, so guidance should fade with expertise; an adaptive tutorial based on quick diagnostic checks gave a knowledge-gain effect size of 0.46 over non-adapted instruction `[READ: Kalyuga 2007, Educational Psychology Review 19, 509]`. This supports fading a lesson he has mastered, but it comes from problem-solving instruction, not perception.

**Confidence.** Errors made with high confidence are more likely to be corrected after feedback (the "hypercorrection" effect) `[READ-2: Wikipedia, citing Butterfield and Metcalfe 2001, JEP:LMC 27, 1491]`. When you add confidence, a confident wrong answer should get the fullest lesson, not a softer one `[INFERRED]`.

**Highlighting on the plot.** Signalling (cues that highlight relevant parts of a display) has a strong effect on retention and a moderate one on transfer in multimedia learning, with inconsistent moderation by prior knowledge `[READ-2: QIC-WD umbrella summary of Schneider et al. 2018 and Alpizar et al. 2020]`. That research is about diagrams and text, not noisy data, so the evidence for overlays on light curves is indirect.

**What I did not find.** No controlled study of *feedback content* for light-curve classification by volunteers. Planet Hunters TESS reports that volunteers improved with practice `[READ]`, but not which feedback caused it.

---

## 2. Ranked measurable features of a 36-hour window

All formulas are in `engine.js` (`measure`). Notation: `y` is the array (ppm, `null` for missing), `n = 216`, one point per 10 minutes. Robust helpers: `median`, `mad`. Ranking is by how well each feature separates classes in my simulator (AUC: 0.5 = useless, 0 or 1 = perfect) `[RAN: table.js, 150 cards per kind]`; typical values per class are in the tables after this list.

1. **Strength.** `sigPt = 1.4826 * mad(diff(y)) / sqrt(2)` (point scatter from point-to-point differences, so slow trends do not inflate it); `beta` = red-noise factor (item 12); for every box length `D` in {12, 18, 24, 30, 36, 48, 60, 72} points (2 to 12 hours) and every start, with at least 80% of points present: `s = (base - boxMean) / (sigPt * beta / sqrt(k))` where `base` = median outside the best event and `k` = points in the box. Strength = max `s`. AUC planet vs noise 0.98, limit planet vs hard noise 0.86 `[RAN]`. Threshold 7 (your hunt's line). **Important:** your deck already has a "strength"; the engine must use the *same function* as the generator, or the card and the feedback will disagree `[INFERRED]`.
2. **Depth in point-scatters** (`(base - boxMean) / sigPt`): eclipses 40 (18 to 74) against 1 to 3 for planets; above 8 means visible point by point, so eclipse `[RAN]`.
3. **Uniqueness ratio** (`strength / strength of the best non-overlapping box`): planets 5.5 (clear) and 2.7 (limit), hard noise 1.9, quiet noise 1.2; AUC 0.96, and 0.76 for limit vs hard noise `[RAN]`. Thresholds: under 1.35 "not unique", over 1.6 "stands out".
4. **Pre-gap sag** (for every hole of 2 or more missing points: mean of the 12 points before it, as a strength against `base`): gap dips 4.2 (2.2 to 7.6), everything else about 0; AUC 0.01 against planets, i.e. near-perfect `[RAN]`. Threshold 3.
5. **Distance from the event to the nearest hole** (hours; card edges reported separately): gap dips 0 (0 to 0.7), planets about 9.5 `[RAN]`. Threshold 1 hour.
6. **Short rise** (best 1 to 3 point upward box, with plain point noise, away from card edges, and falling back to half within 2 hours): spikes 9.9 (5.4 to 13.9), all else about 3; threshold 5 `[RAN]`.
7. **Lasting step** (best split point comparing medians of 6 hours either side, plain point noise; "stays" if the far halves also differ by at least 60% of the jump): fires on 70% of steps and 52% of ramps (ramps often contain a step-like edge) `[RAN]`. Threshold 6 plus "stays".
8. **Shape difference** (least-squares trapezoid fits with ingress fraction 0 to 0.5 and three durations; `(SSE of V − SSE of near-box) / sigPt²`): positive means a flat floor fits better. Clear planets 26, limit planets 5.5, hard noise 3.5 `[RAN]`. Rule: under 4 in absolute value the shape cannot be decided; at strength under about 9 this is usually the case `[RAN]`, so **do not teach "flat floor = planet" on faint cards**.
9. **Biggest single-point deviation** (in point scatters): planets 4.9, noise 3.0 to 3.2, eclipses 52, spikes 7.6 `[RAN]`.
10. **Lumpiness** (`beta` = scatter of 1-hour means outside the event ÷ (sigPt / √6), clipped 1 to 3): white noise 1.0, my red noise about 1.2, variables 2.5, ramps and steps about 2 `[RAN]`. Threshold 1.5. It is a symptom (raised by artifacts too) more than a class; precision only 23% as a class detector `[RAN]`.
11. **Wobble** (first autocorrelation peak at lags 2 to 18 hours of the detrended residual, plus amplitude of 1-hour means): variables 0.26 (0.14 to 0.46) against 0.13 for everything else; threshold 0.25 and amplitude at least 1.5 × the 1-hour noise `[RAN]`. Fires on 52% of my variables.
12. **Edge ramp** (median of the first or last 3 hours minus the median of the middle, excluding the event): fires on 63% of ramps `[RAN]`. Threshold: 6 times its noise, and the event within 4 hours of that edge.
13. **Duration** of the best box: steps and ramps hit the 12-hour maximum, gap dips 2 hours, planets 4 to 10 `[RAN]`.
14. **Points inside the event**: gap dips 13, planets 36 to 48, steps 83 `[RAN]`. Under 18 = "a handful".
15. **Number of rival dips** (non-overlapping boxes at least 70% as strong): planets 0, quiet noise and variables 1 (up to 3) `[RAN]`.
16. **Ingress time and V-ness** (fitted ingress fraction × duration; fraction / 0.5): eclipses 0.7, planets 0.1 `[RAN]`. A grazing-eclipse lesson exists but never fired correctly in my simulator, which has no shallow V eclipses `[RAN]`; untested.
17. **Return level** (median 1 to 7 hours after minus 1 to 7 hours before, as a fraction of depth): steps ±1, planets 0 `[RAN]`.
18. **Symmetry** (first half against second half of the event, in noise units): gap dips 1.2 (second half deeper) `[RAN]`; weak on its own.
19. **Coverage** of the event (points present ÷ duration): gap dips 0.92 `[RAN]`.
20. **Depth needed to reach 7** (`7 * sigPt * beta / sqrt(k)`): not a classifier but the most useful comparison sentence ("to reach 7 over 4 hours it would need about 1,600 ppm; it has 900") and the size of the ghost planet (section 6) `[INFERRED, RAN]`.
21. **Distance to card edges** (hours): needed for the ramp test and to avoid calling an edge a hole `[INFERRED]`.

Context features for real mode (not in the prototype): phase relative to the two stars' eclipses, time to the nearest thruster firing (especially the 0.5 day before it, your rule C7), and agreement with the second data product `[INFERRED]`.

**An honest result.** Limit planets against hard noise are separated well only by strength (0.86) and uniqueness (0.76); shape, symmetry and return level are close to useless at that strength (0.45 to 0.63) `[RAN]`. The engine should not pretend otherwise. It says so (lesson `shape_unclear`), and that is itself a valuable lesson.


### Calibration tables from the simulator `[RAN]`

#### Medians (10th to 90th percentile) by card group, 150 simulated cards per kind

| feature | planet_clear | planet_limit | hardnoise | quiet | eclipse | spike | step | gapdip | ramp | variable |
|---|---|---|---|---|---|---|---|---|---|---|
| strength | 13.6 (9.39 to 19.34) | 6.32 (4.49 to 9.3) | 4.2 (3 to 5.68) | 2.74 (2 to 3.57) | 164 (73.76 to 335) | 2.06 (1.38 to 3.37) | 8.28 (3.87 to 21.82) | 4.72 (2.9 to 7.93) | 5.26 (2.76 to 12.58) | 3.65 (2.68 to 5.77) |
| gap_ratio | 5.53 (3.72 to 8.72) | 2.68 (1.61 to 4.26) | 1.88 (1.27 to 2.79) | 1.24 (1.05 to 1.77) | 11.08 (7.25 to 19.62) | 1.33 (1.07 to 1.84) | 1.95 (1.23 to 7.79) | 1.96 (1.21 to 3.47) | 2.04 (1.26 to 4.16) | 1.13 (1.01 to 1.5) |
| n_similar | 0 (0 to 0) | 0 (0 to 0) | 0 (0 to 1) | 1 (0 to 3) | 0 (0 to 0) | 1 (0 to 2) | 0 (0 to 1) | 0 (0 to 1) | 0 (0 to 1) | 1 (0 to 3) |
| depth_pts | 2.56 (1.78 to 3.5) | 1.35 (0.87 to 1.93) | 0.89 (0.61 to 1.31) | 0.68 (0.44 to 1.01) | 40.02 (17.71 to 73.77) | 0.8 (0.55 to 1.06) | 2.02 (1 to 3.92) | 1.49 (0.79 to 2.66) | 1.53 (0.78 to 3.34) | 1.62 (0.87 to 2.88) |
| dur_h | 8 (4 to 10) | 6 (4 to 10) | 5 (2 to 12) | 3 (2 to 8) | 4 (2 to 5) | 3 (2 to 10) | 12 (10 to 12) | 2 (2 to 6) | 10 (4 to 12) | 5 (2 to 8) |
| n_in | 48 (30 to 72) | 36 (24 to 60) | 30 (12 to 72) | 18 (12 to 48) | 30 (15 to 37) | 18 (12 to 60) | 83 (60 to 90) | 13 (10 to 36) | 67 (24 to 90) | 30 (15 to 60) |
| vness | 0.1 (0 to 0.5) | 0 (0 to 0.5) | 0 (0 to 0.2) | 0 (0 to 0.3) | 0.7 (0.5 to 0.8) | 0 (0 to 0.2) | 0 (0 to 0.3) | 0.1 (0 to 0.7) | 0.1 (0 to 0.3) | 0.2 (0 to 0.8) |
| shape_dchi2 | 25.55 (5.89 to 56.42) | 5.51 (0.06 to 15.66) | 3.5 (0.43 to 7.8) | 1.62 (-0.14 to 3.63) | -920 (-4853 to 290) | 1.92 (-0.11 to 6.19) | 46.22 (6.36 to 186) | 2.9 (-0.67 to 10.09) | 21.67 (3.1 to 101) | 2.93 (-8.84 to 12.61) |
| ingress_h | 0.5 (0 to 2) | 0 (0 to 1.6) | 0 (0 to 0.56) | 0 (0 to 0.4) | 1.5 (0.88 to 2.25) | 0 (0 to 0.25) | 0 (0 to 1.88) | 0.2 (0 to 1) | 0.25 (0 to 1.5) | 0.38 (0 to 3) |
| rebound_frac | -0.01 (-0.16 to 0.2) | -0.04 (-0.4 to 0.36) | 0.03 (-0.46 to 0.63) | -0.01 (-0.79 to 0.68) | 0 (-0.01 to 0.02) | 0.03 (-0.73 to 0.69) | 0.15 (-1.3 to 1.25) | 0.03 (-0.36 to 0.41) | -0.27 (-1.15 to 0.41) | -0.01 (-0.46 to 0.5) |
| asym_z | -0.08 (-1.47 to 1.6) | 0.01 (-1.21 to 1.25) | 0.12 (-0.83 to 1.04) | -0.02 (-0.85 to 1.03) | -0.6 (-7.07 to 15.3) | -0.01 (-0.51 to 0.69) | 0 (-1.07 to 0.92) | 1.21 (-0.26 to 2.74) | -0.22 (-3.62 to 0.69) | -0.02 (-0.78 to 0.61) |
| gap_dist_h | 9.33 (6 to 13.17) | 9.67 (6 to 13.83) | 10.5 (6.83 to 14.5) | 3.67 (0.17 to 12.5) | 10.5 (5.83 to 14.17) | 7.33 (0.67 to 14.33) | 5.67 (0 to 22.5) | 0 (0 to 0.67) | 12 (0 to 29.33) | 7.83 (1.33 to 13.83) |
| pregap_z | 0 (0 to 0) | 0 (0 to 0) | 0 (0 to 0) | 0 (0 to 1.39) | 0 (0 to 0) | 0 (0 to 0) | 0 (0 to 0) | 4.18 (2.19 to 7.6) | 0 (0 to 0) | 0 (0 to 0) |
| rise_z | 2.97 (2.42 to 3.82) | 3.05 (2.52 to 3.91) | 3.03 (2.47 to 3.81) | 2.94 (2.49 to 3.61) | 2.71 (2.15 to 3.43) | 9.87 (5.4 to 13.86) | 3.39 (2.54 to 4.77) | 3.03 (2.57 to 3.89) | 3.83 (2.86 to 7.03) | 4.1 (2.96 to 5.73) |
| stepw_z | 5.97 (-11.28 to 11.02) | 3.01 (-6.08 to 5.78) | 2.6 (-3.74 to 4.29) | -1.62 (-3.05 to 2.85) | -17.75 (-169 to 136) | 1.79 (-3.99 to 3.86) | -2.54 (-12.85 to 13.23) | -2.1 (-4.78 to 4.85) | -3.61 (-9.09 to 8.54) | 3.65 (-9.48 to 12.49) |
| ramp_z | 0.44 (-2.13 to 2.38) | 0.3 (-2.17 to 2.03) | -0.48 (-2.01 to 2.06) | -0.48 (-2.07 to 1.62) | 0.41 (-2.04 to 1.71) | -0.97 (-2.61 to 1.46) | -5.69 (-12.9 to 5.65) | 0.59 (-1.85 to 2.2) | 3.57 (-14.18 to 13.94) | -2.38 (-8.21 to 3.98) |
| wobble_acf | 0.13 (0.1 to 0.16) | 0.13 (0.1 to 0.16) | 0.13 (0.1 to 0.16) | 0.13 (0.1 to 0.17) | 0.16 (0.11 to 0.31) | 0.12 (0.09 to 0.16) | 0.15 (0.11 to 0.23) | 0.13 (0.1 to 0.16) | 0.16 (0.12 to 0.24) | 0.26 (0.14 to 0.46) |
| beta | 1.18 (1 to 1.49) | 1.24 (1 to 1.51) | 1.16 (1 to 1.38) | 1.03 (1 to 1.3) | 1.08 (1 to 1.31) | 1.76 (1.2 to 2.6) | 2.02 (1.1 to 3) | 1.2 (1 to 1.48) | 2.14 (1.2 to 3) | 2.54 (1.44 to 3) |
| max_point_z | 4.87 (3.8 to 6.04) | 3.54 (2.87 to 4.42) | 3.19 (2.79 to 3.86) | 2.98 (2.56 to 3.63) | 52.32 (22.93 to 98.17) | 7.64 (4.52 to 10.94) | 4.65 (3.35 to 6.47) | 3.69 (2.9 to 5) | 4.7 (3.25 to 7.43) | 4.16 (2.95 to 5.46) |
| depth7_ppm | 1594 (1078 to 3831) | 1922 (1215 to 5003) | 2027 (1039 to 4592) | 2290 (1330 to 6169) | 2192 (1639 to 5616) | 3775 (1885 to 9721) | 2480 (1091 to 4512) | 2707 (1802 to 6758) | 2556 (1517 to 4827) | 4548 (2904 to 7651) |

#### AUC (0.5 = useless, 0 or 1 = perfect separation)

| feature | planet vs noise | limit planet vs hard noise | planet vs eclipse | planet vs spike | planet vs step | planet vs gap dip | planet vs ramp | planet vs variable |
|---|---|---|---|---|---|---|---|---|
| strength | 0.98 | 0.86 | 0.00 | 1.00 | 0.64 | 0.90 | 0.81 | 0.96 |
| gap_ratio | 0.96 | 0.76 | 0.05 | 0.98 | 0.79 | 0.88 | 0.84 | 0.99 |
| n_similar | 0.24 | 0.42 | 0.51 | 0.21 | 0.40 | 0.40 | 0.42 | 0.07 |
| depth_pts | 0.96 | 0.82 | 0.00 | 0.97 | 0.51 | 0.69 | 0.66 | 0.64 |
| dur_h | 0.76 | 0.56 | 0.88 | 0.78 | 0.07 | 0.89 | 0.30 | 0.72 |
| n_in | 0.79 | 0.58 | 0.81 | 0.81 | 0.07 | 0.92 | 0.30 | 0.70 |
| vness | 0.66 | 0.62 | 0.05 | 0.70 | 0.61 | 0.47 | 0.57 | 0.42 |
| shape_dchi2 | 0.88 | 0.63 | 0.85 | 0.88 | 0.26 | 0.83 | 0.42 | 0.81 |
| ingress_h | 0.71 | 0.64 | 0.18 | 0.74 | 0.54 | 0.61 | 0.53 | 0.46 |
| rebound_frac | 0.48 | 0.45 | 0.48 | 0.49 | 0.46 | 0.48 | 0.64 | 0.51 |
| asym_z | 0.48 | 0.49 | 0.52 | 0.48 | 0.49 | 0.23 | 0.62 | 0.50 |
| gap_dist_h | 0.65 | 0.42 | 0.44 | 0.63 | 0.60 | 0.99 | 0.45 | 0.61 |
| pregap_z | 0.37 | 0.50 | 0.50 | 0.50 | 0.50 | 0.01 | 0.50 | 0.50 |
| rise_z | 0.51 | 0.53 | 0.68 | 0.00 | 0.35 | 0.48 | 0.21 | 0.17 |
| stepw_z | 0.52 | 0.49 | 0.55 | 0.52 | 0.51 | 0.52 | 0.54 | 0.46 |
| ramp_z | 0.55 | 0.50 | 0.51 | 0.64 | 0.78 | 0.47 | 0.43 | 0.65 |
| wobble_acf | 0.45 | 0.51 | 0.26 | 0.57 | 0.33 | 0.48 | 0.22 | 0.10 |
| beta | 0.66 | 0.61 | 0.68 | 0.13 | 0.17 | 0.51 | 0.13 | 0.06 |
| max_point_z | 0.90 | 0.70 | 0.00 | 0.12 | 0.43 | 0.70 | 0.42 | 0.59 |
| depth7_ppm | 0.40 | 0.51 | 0.32 | 0.19 | 0.39 | 0.27 | 0.32 | 0.11 |

#### Lesson firing and precision

| lesson | fires on (% of cards of each truth) | precision: truth is in its "for" list |
|---|---|---|
| deep | planet 0, noise 0, eclipse 100, flare 0, step 0, gapdip 0, ramp 0, variable 0 | 100% |
| rise | planet 0, noise 0, eclipse 0, flare 94, step 6, gapdip 0, ramp 28, variable 20 | 60% |
| step | planet 3, noise 0, eclipse 0, flare 0, step 70, gapdip 0, ramp 52, variable 9 | 67% |
| gap_touch | planet 0, noise 3, eclipse 0, flare 0, step 0, gapdip 83, ramp 0, variable 0 | 91% |
| drift | planet 0, noise 0, eclipse 0, flare 0, step 23, gapdip 0, ramp 63, variable 1 | 57% |
| wobble | planet 0, noise 0, eclipse 0, flare 0, step 4, gapdip 0, ramp 7, variable 52 | 77% |
| strong_flat | planet 61, noise 0, eclipse 0, flare 0, step 2, gapdip 1, ramp 0, variable 1 | 97% |
| unique | planet 84, noise 1, eclipse 0, flare 0, step 5, gapdip 32, ramp 1, variable 0 | 85% |
| not_unique | planet 1, noise 47, eclipse 0, flare 51, step 16, gapdip 19, ramp 14, variable 84 | 41% |
| many | planet 0, noise 23, eclipse 0, flare 24, step 0, gapdip 7, ramp 2, variable 37 | 76% |
| weak | planet 22, noise 100, eclipse 0, flare 100, step 40, gapdip 83, ramp 68, variable 97 | 38% |
| near_limit | planet 28, noise 11, eclipse 0, flare 1, step 33, gapdip 43, ramp 32, variable 3 | 32% |
| v_shape | planet 1, noise 0, eclipse 0, flare 0, step 0, gapdip 1, ramp 0, variable 4 | 0% |
| shape_unclear | planet 11, noise 80, eclipse 0, flare 76, step 6, gapdip 62, ramp 16, variable 44 | 56% |
| few_points | planet 3, noise 49, eclipse 0, flare 51, step 1, gapdip 73, ramp 5, variable 21 | 48% |
| lumpy | planet 9, noise 3, eclipse 1, flare 69, step 68, gapdip 9, ramp 70, variable 86 | 23% |
| returns | planet 75, noise 1, eclipse 0, flare 0, step 0, gapdip 31, ramp 0, variable 8 | 85% |
| pregap | planet 0, noise 0, eclipse 0, flare 0, step 0, gapdip 77, ramp 0, variable 0 | 98% |


---

## 3. The feedback grammar

**Three slots, always in this order** `[INFERRED, following Shute 2008 and Hattie and Timperley's feed back and feed forward]`:

| Slot | Content | Source of every number |
|---|---|---|
| Line 1: MEASURE | One measured fact about this card, with a gloss the first 3 times a term appears | `display(F)` |
| Line 2: MEANING | Why that fact separates planet from noise or artifact; or, if the lesson repeats, a second measured fact; or, at most once in 6 cards, a pattern line about his own answers | `display(F)` or his history |
| Line 3: YOUR ANSWER + NEXT | Practice: his answer, the truth, one thing to check next time. Real mode: "locked, these are measurements, not a verdict", plus which other panel to compare | truth from the deck (practice only) |

**Lessons.** Each of the 22 lessons is a test on facts (`when`), the classes it argues for and against, a measurement sentence, a meaning sentence, a short meaning sentence and, for real mode, a hedged meaning sentence. Four "anchor" lessons (faint step, faint flare, gap, faint planet) are used only in practice, only when nothing stronger argues for the true class, and are worded as faint, never as clear.

**Selection rule** (`rankLessons`), deterministic:

| Term | Value | Why |
|---|---|---|
| Base | +1 (anchors −1, or +5 when no real lesson argues for the truth) | anchors are a last resort |
| Priority | lesson priority (deep 10, rise, step, gap 9, drift 8, wobble 7, ... lumpy 2) × 0.05 in practice, × 0.5 in real mode | in real mode the specific artifact detectors must lead |
| Diagnostic for truth (practice) | +3 if the truth is in `for`, −4 if in `against` | never teach a fact that points the wrong way |
| His mistake | +2 if the lesson argues against the class he chose | Shute's "addressing the response" |
| Mastered | −2 if he has shown this lesson for this truth (4 of the last 5 right) and is right now | fading, expertise reversal |
| Kind mastered | −1 per earlier use of this lesson on this kind | push new facts on kinds he already gets |
| Recently used | −1.5 per use as lead in the last 4 cards | anti-repetition |
| Tie break | hash of card id and lesson id | deterministic variety |

**Line 2 rules.** If the lead repeats within 4 cards, or he has mastered this kind and answered right, line 2 becomes a second measured fact from the next-ranked lesson that shares no number with line 1, or the "depth needed to reach 7" comparison. A pattern line replaces line 2, never adds a line.

**Line 3 cue** ("next time, check ..."): the cue of the best lesson that argues *for the truth*, so it points at the feature that would have got the answer right.

**Length control.** Every combination of {gloss or none} × {meaning, short meaning, swap} × {three wordings of line 3} is scored by distance from 40 words, with +100 for anything outside 36 to 44 and small penalties for dropping a needed gloss or a planned swap; the cheapest wins `[RAN: range 38 to 44]`. Right, wrong and unsure wordings of line 3 have near-equal length, so length cannot leak the verdict.

**Glossing.** "(how far it stands out from the noise)" follows "strength" the first 3 times, then is dropped. Every other line uses plain words only `[INFERRED]`.

---

## 4. Worked examples (50, all produced by the code)

Cards 1 to 33 cover the 11 practice kinds × right, wrong and Not sure; each was composed with a fresh learner state. Cards 34 to 41 are real mode on hidden-truth cards. Cards 42 to 50 come from one 34-card round played by a simulated Ahmed with your reported habits (calls anything with strength 3.5 or more a dip, calls lumpy or crowded noise Odd, calls every gap dip a dip, never says Not sure, finds the clear planets), so they show state, patterns and swaps. "*In*" lists the measured values that drove the text `[RAN]`.

**1. clear, answered dip (right), card clear-777**  
*In:* strength 12.4, next wiggle 2.2, depth 4702 ppm (2.5 point scatters), 8 h, shape difference 1.0, lumpiness 1.41, gap distance 8.67 h, pre-gap sag 0.0, rise 3.1, step 8.4. *Lead lesson:* unique, 42 words.  
> The best dip scores 12.4; the next best wiggle only 2.2.  
> One dip standing well above every other wiggle is what a real crossing does.  
> You said Dip, and it was a hidden planet. Next time, also check the next best wiggle.

**2. clear, answered nodip (wrong), card clear-778**  
*In:* strength 10.4, next wiggle 2.1, depth 2392 ppm (2.4 point scatters), 5 h, shape difference -0.1, lumpiness 1.28, gap distance 14.83 h, pre-gap sag 0.0, rise 3.5, step -7.7. *Lead lesson:* unique, 39 words.  
> The best dip scores 10.4; the next best wiggle only 2.1.  
> One dip standing well above every other wiggle is what a real crossing does.  
> No dip missed: it was a hidden planet. Check the next best wiggle first.

**3. clear, answered unsure (unsure), card clear-779**  
*In:* strength 7.9, next wiggle 2.2, depth 1538 ppm (1.3 point scatters), 8 h, shape difference 1.5, lumpiness 1.11, gap distance 9.50 h, pre-gap sag 0.0, rise 2.7, step -5.5. *Lead lesson:* unique, 41 words.  
> The best dip scores 7.9; the next best wiggle only 2.2.  
> One dip standing well above every other wiggle is what a real crossing does.  
> You chose Not sure; it was a hidden planet. Next time, check the next best wiggle.

**4. limit, answered dip (right), card limit-787**  
*In:* strength 7.8, next wiggle 2.2, depth 1543 ppm (1.4 point scatters), 6 h, shape difference 8.5, lumpiness 1.08, gap distance 9.83 h, pre-gap sag 0.0, rise 3.0, step -5.1. *Lead lesson:* unique, 42 words.  
> The best dip scores 7.8; the next best wiggle only 2.2.  
> One dip standing well above every other wiggle is what a real crossing does.  
> You said Dip, and it was a hidden planet. Next time, also check the next best wiggle.

**5. limit, answered nodip (wrong), card limit-788**  
*In:* strength 5.1, next wiggle 1.7, depth 1222 ppm (1.4 point scatters), 4 h, shape difference 5.9, lumpiness 1.39, gap distance 8.17 h, pre-gap sag 0.0, rise 4.4, step 3.6. *Lead lesson:* near_limit, 40 words.  
> Strength 5.1, close to the hunt's line of 7, lasting about 4 hours.  
> Near the line, how unique the dip is matters more than how deep it looks.  
> Missed: it was a hidden planet. Check how unique it is first.

**6. limit, answered unsure (unsure), card limit-789**  
*In:* strength 4.8, next wiggle 2.9, depth 727 ppm (0.7 point scatters), 12 h, shape difference 1.0, lumpiness 1.28, gap distance 11.67 h, pre-gap sag 0.0, rise 2.6, step -3.8. *Lead lesson:* shape_unclear, 40 words.  
> At strength 4.8, a flat floor and a V fit this dip about equally well.  
> So shape cannot decide it; judge by strength and the next best wiggle.  
> Not sure; it was a hidden planet. Check the next best wiggle.

**7. easybox, answered dip (right), card easybox-797**  
*In:* strength 16.8, next wiggle 2.2, depth 9464 ppm (3.0 point scatters), 8 h, shape difference 55.8, lumpiness 1.22, gap distance 7.50 h, pre-gap sag 0.0, rise 3.0, step -12.4. *Lead lesson:* strong_flat, 38 words.  
> Strength 16.8 (how far it stands out from the noise), with a flat floor and 1 hour slopes.  
> Flat floor, short slopes: a planet crossing.  
> Dip was right: a hidden planet. Also check the floor and the slopes.

**8. easybox, answered nodip (wrong), card easybox-798**  
*In:* strength 10.3, next wiggle 2.8, depth 5265 ppm (1.8 point scatters), 10 h, shape difference 23.9, lumpiness 1.37, gap distance 7.00 h, pre-gap sag 0.0, rise 3.1, step -8.7 (stays). *Lead lesson:* strong_flat, 40 words.  
> Strength 10.3 (how far it stands out from the noise), with a flat floor and very steep sides.  
> Flat floor, short slopes: a planet crossing.  
> No dip missed: it was a hidden planet. Check the floor and the slopes first.

**9. easybox, answered unsure (unsure), card easybox-799**  
*In:* strength 22.1, next wiggle 3.2, depth 7079 ppm (3.2 point scatters), 8 h, shape difference 46.6, lumpiness 1.00, gap distance 6.67 h, pre-gap sag 0.0, rise 2.3, step 11.8. *Lead lesson:* strong_flat, 42 words.  
> Strength 22.1 (how far it stands out from the noise), with a flat floor and 1 hour slopes.  
> Flat floor, short slopes: a planet crossing.  
> You chose Not sure; it was a hidden planet. Next time, check the floor and the slopes.

**10. hardnoise, answered nodip (right), card hardnoise-807**  
*In:* strength 3.9, next wiggle 2.4, depth 948 ppm (1.0 point scatters), 5 h, shape difference 3.1, lumpiness 1.34, gap distance 14.17 h, pre-gap sag 0.0, rise 3.2, step -5.1. *Lead lesson:* weak, 40 words.  
> Strength 3.9 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Searching a whole month of pure noise often turns up one dip this strong.  
> Right: only noise. Also check the strength against 7.

**11. hardnoise, answered dip (wrong), card hardnoise-808**  
*In:* strength 6.1, next wiggle 2.1, depth 2442 ppm (1.3 point scatters), 5 h, shape difference 7.1, lumpiness 1.14, gap distance 8.17 h, pre-gap sag 0.0, rise 3.3, step 4.1. *Lead lesson:* weak, 40 words.  
> Strength 6.1 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> A month of pure noise often gives one dip this strong.  
> Dip missed: it was only noise. Check the strength against 7 first.

**12. hardnoise, answered unsure (unsure), card hardnoise-809**  
*In:* strength 2.6, next wiggle 2.5, depth 784 ppm (0.7 point scatters), 2 h, shape difference 0.0, lumpiness 1.00, gap distance 13.33 h, pre-gap sag 0.0, rise 2.6, step 2.3 (stays). *Lead lesson:* many, 39 words.  
> 2 other dips in this card are at least 70 percent as strong.  
> A real crossing stands alone; a crowd of similar dips is the noise itself.  
> Not sure; it was only noise. Check how many wiggles look alike.

**13. quiet, answered nodip (right), card quiet-817**  
*In:* strength 3.0, next wiggle 2.0, depth 472 ppm (0.5 point scatters), 8 h, shape difference 2.1, lumpiness 1.08, gap distance 4.00 h, pre-gap sag 0.0, rise 2.6, step 2.0. *Lead lesson:* weak, 40 words.  
> Strength 3.0 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Searching a whole month of pure noise often turns up one dip this strong.  
> Right: only noise. Also check the strength against 7.

**14. quiet, answered dip (wrong), card quiet-818**  
*In:* strength 3.1, next wiggle 3.0, depth 440 ppm (0.5 point scatters), 8 h, shape difference 1.8, lumpiness 1.04, gap distance 11.50 h, pre-gap sag 0.0, rise 3.2, step 2.5 (stays). *Lead lesson:* not_unique, 42 words.  
> The best dip scores 3.1, but the next best wiggle scores 3.0.  
> When other wiggles are nearly as strong, the best one is usually just noise.  
> You said Dip, but it was only noise. Next time, check the next best wiggle first.

**15. quiet, answered unsure (unsure), card quiet-819**  
*In:* strength 1.8, next wiggle 1.4, depth 1570 ppm (0.5 point scatters), 2 h, shape difference 0.2, lumpiness 1.00, gap distance 14.00 h, pre-gap sag 0.0, rise 3.3, step -2.4. *Lead lesson:* not_unique, 41 words.  
> The best dip scores 1.8, but the next best wiggle scores 1.4.  
> When other wiggles are nearly as strong, the best one is usually just noise.  
> You chose Not sure; it was only noise. Next time, check the next best wiggle.

**16. gapdecoy, answered nodip (right), card gapdecoy-827**  
*In:* strength 2.5, next wiggle 2.2, depth 752 ppm (0.7 point scatters), 2 h, shape difference 2.1, lumpiness 1.00, gap distance 5.67 h, pre-gap sag 0.0, rise 2.3, step -2.0 (stays). *Lead lesson:* not_unique, 39 words.  
> The best dip scores 2.5, but the next best wiggle scores 2.2.  
> Nearly equal rivals mean the best one is likely noise.  
> You said No dip, and it was only noise. Next time, also check the next best wiggle.

**17. gapdecoy, answered dip (wrong), card gapdecoy-828**  
*In:* strength 3.5, next wiggle 2.0, depth 889 ppm (0.8 point scatters), 3 h, shape difference 1.3, lumpiness 1.00, gap distance 4.83 h, pre-gap sag 0.7, rise 2.8, step -2.4 (stays). *Lead lesson:* weak, 40 words.  
> Strength 3.5 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> A month of pure noise often gives one dip this strong.  
> Dip missed: it was only noise. Check the strength against 7 first.

**18. gapdecoy, answered unsure (unsure), card gapdecoy-829**  
*In:* strength 3.8, next wiggle 2.1, depth 3871 ppm (1.3 point scatters), 2 h, shape difference 1.3, lumpiness 1.21, gap distance 4.83 h, pre-gap sag 1.2, rise 2.9, step 2.6 (stays). *Lead lesson:* weak, 39 words.  
> Strength 3.8 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> A month of pure noise often gives one dip this strong.  
> Not sure; it was only noise. Check the strength against 7.

**19. eclipse, answered odd (right), card eclipse-837**  
*In:* strength 102.8, next wiggle 4.6, depth 26407 ppm (24.2 point scatters), 3 h, shape difference -716.7, lumpiness 1.00, gap distance 14.33 h, pre-gap sag 0.0, rise 2.7, step -32.5. *Lead lesson:* deep, 39 words.  
> It is 26,400 ppm deep, 24 times the scatter of single points.  
> Far too deep for a planet: one star is hiding the other.  
> Odd was right: an eclipse. Also check how deep it is next to the noise.

**20. eclipse, answered dip (wrong), card eclipse-838**  
*In:* strength 71.6, next wiggle 7.2, depth 34129 ppm (17.5 point scatters), 5 h, shape difference -650.0, lumpiness 1.34, gap distance 8.00 h, pre-gap sag 0.0, rise 3.6, step -54.1. *Lead lesson:* deep, 40 words.  
> It is 34,100 ppm deep, 18 times the scatter of single points.  
> Far too deep for a planet: one star is hiding the other.  
> Dip missed: it was an eclipse. Check how deep it is next to the noise first.

**21. eclipse, answered unsure (unsure), card eclipse-839**  
*In:* strength 121.5, next wiggle 17.2, depth 73490 ppm (22.2 point scatters), 5 h, shape difference 125.1, lumpiness 1.00, gap distance 10.00 h, pre-gap sag 0.0, rise 2.5, step -73.8. *Lead lesson:* deep, 39 words.  
> It is 73,500 ppm deep, 22 times the scatter of single points.  
> Far too deep for a planet: one star is hiding the other.  
> Not sure; it was an eclipse. Check how deep it is next to the noise.

**22. spike, answered odd (right), card spike-847**  
*In:* strength 2.0, next wiggle 1.2, depth 465 ppm (0.4 point scatters), 10 h, shape difference 0.9, lumpiness 1.70, gap distance 0.00 h, pre-gap sag 0.0, rise 9.8, step 2.6. *Lead lesson:* rise, 41 words.  
> The biggest change is a rise of 7,400 ppm lasting about 20 minutes.  
> A planet can only block light, so a brightening is the star or the camera.  
> Right: a spike up. Also check whether the change goes up or down.

**23. spike, answered nodip (wrong), card spike-848**  
*In:* strength 2.6, next wiggle 2.1, depth 2600 ppm (0.7 point scatters), 2 h, shape difference 0.8, lumpiness 1.00, gap distance 13.17 h, pre-gap sag 0.0, rise 3.7, step -1.7. *Lead lesson:* flare_faint, 40 words.  
> The biggest rise here is 13,100 ppm, lasting about 10 minutes.  
> In this much noise it is hard to see; any short upward jump is worth a look.  
> Missed: it was a spike up. Check for short jumps up first.

**24. spike, answered unsure (unsure), card spike-849**  
*In:* strength 1.4, next wiggle 1.0, depth 2791 ppm (1.0 point scatters), 2 h, shape difference 3.0, lumpiness 2.56, gap distance 11.00 h, pre-gap sag 0.0, rise 15.9, step 4.7. *Lead lesson:* rise, 41 words.  
> The biggest change is a rise of 25,000 ppm lasting about 30 minutes.  
> Planets only block light; a brightening is something else.  
> You chose Not sure; it was a spike up. Next time, check whether the change goes up or down.

**25. stepup, answered odd (right), card stepup-857**  
*In:* strength 3.6, next wiggle 2.1, depth 2402 ppm (0.7 point scatters), 6 h, shape difference 1.7, lumpiness 1.24, gap distance 11.83 h, pre-gap sag 0.0, rise 3.0, step 3.1 (stays). *Lead lesson:* step_faint, 38 words.  
> The biggest lasting change is 2,900 ppm, about 19 hours in.  
> That step is small next to the noise; compare the left and right halves.  
> Odd was right: a lasting step. Also check the left and right halves.

**26. stepup, answered nodip (wrong), card stepup-858**  
*In:* strength 4.7, next wiggle 3.5, depth 1642 ppm (1.7 point scatters), 12 h, shape difference 11.4, lumpiness 3.00, gap distance 10.17 h, pre-gap sag 0.0, rise 6.3, step 17.2 (stays). *Lead lesson:* step, 40 words.  
> The level jumps by 5,100 ppm about 25 hours in and stays there.  
> Dips come back up; a jump that stays is usually the instrument.  
> No dip missed: it was a lasting step. Check whether the level comes back first.

**27. stepup, answered unsure (unsure), card stepup-859**  
*In:* strength 6.8, next wiggle 4.0, depth 3508 ppm (1.9 point scatters), 12 h, shape difference 30.3, lumpiness 2.33, gap distance 4.67 h, pre-gap sag 0.0, rise 3.0, step 7.2 (stays). *Lead lesson:* step, 42 words.  
> The level jumps by 4,000 ppm about 18.5 hours in and stays there.  
> A planet's dip returns to the old level; a jump that stays is usually the instrument.  
> Not sure; it was a lasting step. Check whether the level comes back.

**28. stepdown, answered odd (right), card stepdown-867**  
*In:* strength 12.4, next wiggle 6.3, depth 4889 ppm (4.4 point scatters), 12 h, shape difference 357.2, lumpiness 3.00, gap distance 1.67 h, pre-gap sag 0.0, rise 2.4, step -15.8 (stays). *Lead lesson:* step, 40 words.  
> The level jumps by 5,200 ppm about 19.5 hours in and stays there.  
> A planet's dip returns to the old level; a jump that stays is usually the instrument.  
> Right: a lasting step. Also check whether the level comes back.

**29. stepdown, answered dip (wrong), card stepdown-868**  
*In:* strength 34.2, next wiggle 1.7, depth 4163 ppm (4.0 point scatters), 12 h, shape difference 207.6, lumpiness 1.00, gap distance 21.83 h, pre-gap sag 0.0, rise 2.8, step -14.5 (stays). *Lead lesson:* step, 39 words.  
> The level jumps by 4,400 ppm about 23.5 hours in and stays there.  
> Dips come back up; a jump that stays is usually the instrument.  
> Dip missed: it was a lasting step. Check whether the level comes back first.

**30. stepdown, answered unsure (unsure), card stepdown-869**  
*In:* strength 3.9, next wiggle 2.5, depth 2552 ppm (0.8 point scatters), 10 h, shape difference 13.0, lumpiness 1.54, gap distance 1.33 h, pre-gap sag 0.0, rise 3.4, step -3.5 (stays). *Lead lesson:* step_faint, 42 words.  
> The biggest lasting change is 3,300 ppm, about 8.5 hours in.  
> That step is small next to the noise; compare the left and right halves.  
> You chose Not sure; it was a lasting step. Next time, check the left and right halves.

**31. gapdip, answered odd (right), card gapdip-877**  
*In:* strength 3.5, next wiggle 2.4, depth 2505 ppm (1.4 point scatters), 2 h, shape difference 2.6, lumpiness 1.26, gap distance 0.00 h, pre-gap sag 3.5, rise 3.4, step -2.1 (stays). *Lead lesson:* pregap, 40 words.  
> In the 2 hours before the hole at 28.5 hours, light sags by 2,300 ppm.  
> A sag ending at a hole is a thruster fake.  
> Right: a fake dip at a hole. Also check the last points before a hole.

**32. gapdip, answered dip (wrong), card gapdip-878**  
*In:* strength 3.5, next wiggle 2.5, depth 2266 ppm (1.0 point scatters), 2 h, shape difference 0.3, lumpiness 1.00, gap distance 0.00 h, pre-gap sag 3.5, rise 2.4, step -3.3. *Lead lesson:* pregap, 42 words.  
> In the 2 hours before the hole at 29.5 hours, light sags by 2,300 ppm.  
> A sag ending at a hole is a thruster fake.  
> Missed: it was a fake dip at a hole. Check the last points before a hole first.

**33. gapdip, answered unsure (unsure), card gapdip-879**  
*In:* strength 3.1, next wiggle 2.4, depth 804 ppm (0.7 point scatters), 6 h, shape difference 2.7, lumpiness 1.38, gap distance 5.33 h, pre-gap sag 2.3, rise 3.5, step 4.2. *Lead lesson:* gap_faint, 40 words.  
> Just before the hole at 21 hours the light sags by 1,000 ppm.  
> Dips next to holes are suspect.  
> You chose Not sure; it was a fake dip at a hole. Next time, check the last points before a hole.

**34. REAL MODE, truth hidden (simulated clear), card clear-4242**  
*In:* strength 9.5, next wiggle 2.6, depth 1898 ppm (1.9 point scatters), 8 h, shape difference 9.7, lumpiness 1.40, gap distance 9.33 h, pre-gap sag 0.0, rise 4.0, step 8.5. *Lead lesson:* strong_flat, 44 words.  
> Strength 9.5 (how far it stands out from the noise), with a flat floor and very steep sides.  
> A flat floor between short slopes is what a planet crossing looks like, among other things.  
> Locked. Measurements, not a verdict; compare the second light curve.

**35. REAL MODE, truth hidden (simulated hardnoise), card hardnoise-4244**  
*In:* strength 2.3, next wiggle 1.2, depth 792 ppm (0.3 point scatters), 10 h, shape difference 2.4, lumpiness 1.16, gap distance 11.33 h, pre-gap sag 0.0, rise 3.6, step -2.2. *Lead lesson:* weak, 41 words.  
> Strength 2.3 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Searching a whole month of pure noise often turns up one dip this strong.  
> Locked. Measurements, not a verdict; compare the second light curve.

**36. REAL MODE, truth hidden (simulated eclipse), card eclipse-4245**  
*In:* strength 144.3, next wiggle 15.7, depth 100208 ppm (43.1 point scatters), 2 h, shape difference 1514.1, lumpiness 1.03, gap distance 8.83 h, pre-gap sag 0.0, rise 2.3, step 10.6. *Lead lesson:* deep, 40 words.  
> It is 100,200 ppm deep, 43 times the scatter of single points.  
> Planets are rarely this deep; an eclipse of the two stars usually is.  
> Your answer is locked. These are measurements, not a verdict; now compare the eclipse timing.

**37. REAL MODE, truth hidden (simulated gapdip), card gapdip-4246**  
*In:* strength 7.9, next wiggle 2.2, depth 2164 ppm (2.5 point scatters), 3 h, shape difference 7.4, lumpiness 1.24, gap distance 0.00 h, pre-gap sag 7.5, rise 3.2, step -6.3. *Lead lesson:* gap_touch, 43 words.  
> The dip runs straight into a hole in the data and ends exactly there.  
> Holes often mark thruster firings, and the camera can wobble just before them.  
> Your answer is locked. These are measurements, not a verdict; now compare the thruster firing times.

**38. REAL MODE, truth hidden (simulated spike), card spike-4248**  
*In:* strength 2.2, next wiggle 1.6, depth 827 ppm (0.8 point scatters), 3 h, shape difference 1.4, lumpiness 1.52, gap distance 16.83 h, pre-gap sag 0.0, rise 5.6, step -3.1. *Lead lesson:* rise, 38 words.  
> The biggest change is a rise of 3,400 ppm lasting about 30 minutes.  
> A planet can only block light, so a brightening points to the star or camera.  
> Locked. Measurements, not a verdict; compare the second light curve.

**39. REAL MODE, truth hidden (simulated stepdown), card stepdown-4247**  
*In:* strength 4.9, next wiggle 3.4, depth 2957 ppm (0.9 point scatters), 12 h, shape difference 30.2, lumpiness 1.58, gap distance 8.50 h, pre-gap sag 0.0, rise 2.7, step -5.6 (stays). *Lead lesson:* weak, 41 words.  
> Strength 4.9 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Searching a whole month of pure noise often turns up one dip this strong.  
> Locked. Measurements, not a verdict; compare the second light curve.

**40. REAL MODE, truth hidden (simulated variable), card variable-4249**  
*In:* strength 4.8, next wiggle 2.5, depth 3741 ppm (1.0 point scatters), 4 h, shape difference 4.2, lumpiness 1.04, gap distance 15.67 h, pre-gap sag 0.0, rise 2.5, step -3.8. *Lead lesson:* weak, 41 words.  
> Strength 4.8 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Searching a whole month of pure noise often turns up one dip this strong.  
> Locked. Measurements, not a verdict; compare the second light curve.

**41. REAL MODE, truth hidden (simulated ramp), card ramp-4250**  
*In:* strength 4.1, next wiggle 2.2, depth 5274 ppm (1.7 point scatters), 2 h, shape difference 3.3, lumpiness 1.38, gap distance 0.00 h, pre-gap sag 0.0, rise 2.9, step 3.8 (stays). *Lead lesson:* weak, 41 words.  
> Strength 4.1 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Searching a whole month of pure noise often turns up one dip this strong.  
> Locked. Measurements, not a verdict; compare the second light curve.

**42. Habit round, card 9 of 34: hardnoise, answered odd (wrong)**  
*Lead lesson:* lumpy, 39 words.  
> The noise is lumpy: hour averages scatter 1.5 times more than random points predict.  
> Lumpy noise makes slow wiggles; they are still noise, not something odd.  
> Odd missed: it was only noise. Check how lumpy the noise is first.

**43. Habit round, card 14 of 34: quiet, answered nodip (right), pattern line shown**  
*Lead lesson:* weak, 42 words.  
> Strength 2.6 (how far it stands out from the noise); the hunt only keeps 7 or more.  
> Pattern: 4 wrong and 0 Not sure in 12 cards; Not sure is a fair answer.  
> Right: only noise. Also check the strength against 7.

**44. Habit round, card 18 of 34: gapdip, answered dip (wrong)**  
*Lead lesson:* gap_faint, 41 words.  
> Just before the hole at 12.5 hours the light sags by 700 ppm.  
> Dips next to holes are suspect.  
> You said Dip, but it was a fake dip at a hole. Next time, check the last points before a hole first.

**45. Habit round, card 21 of 34: eclipse, answered odd (right), pattern line shown**  
*Lead lesson:* deep, 40 words.  
> It is 59,200 ppm deep, 58 times the scatter of single points.  
> Pattern: 3 of your recent Odd answers were plain noise; lumpy noise is still noise.  
> Right: an eclipse. Also check how deep it is next to the noise.

**46. Habit round, card 25 of 34: hardnoise, answered odd (wrong)**  
*Lead lesson:* lumpy, 39 words.  
> The noise is lumpy: hour averages scatter 1.8 times more than random points predict.  
> Lumpy noise makes slow wiggles; they are still noise, not something odd.  
> Odd missed: it was only noise. Check how lumpy the noise is first.

**47. Habit round, card 26 of 34: hardnoise, answered dip (wrong)**  
*Lead lesson:* weak, 41 words.  
> Strength 4.2; the hunt only keeps 7 or more.  
> To reach 7 over 4 hours it would need about 1,600 ppm; it has 900 ppm.  
> You said Dip, but it was only noise. Next time, check the strength against 7 first.

**48. Habit round, card 28 of 34: gapdip, answered dip (wrong), pattern line shown**  
*Lead lesson:* pregap, 41 words.  
> In the 2 hours before the hole at 13.5 hours, light sags by 1,300 ppm.  
> Pattern: 4 of 4 false alarms scored under 7.  
> Missed: it was a fake dip at a hole. Check the last points before a hole first.

**49. Habit round, card 29 of 34: hardnoise, answered dip (wrong)**  
*Lead lesson:* weak, 41 words.  
> Strength 5.6; the hunt only keeps 7 or more.  
> To reach 7 over 5 hours it would need about 1,500 ppm; it has 1,200 ppm.  
> You said Dip, but it was only noise. Next time, check the strength against 7 first.

**50. Habit round, card 31 of 34: clear, answered dip (right)**  
*Lead lesson:* unique, 42 words.  
> The best dip scores 14.5; the next best wiggle only 3.0.  
> One dip standing well above every other wiggle is what a real crossing does.  
> You said Dip, and it was a hidden planet. Next time, also check the next best wiggle.



**What the examples show, including faults** `[RAN, INFERRED]`. Hard noise now gets different text each time because the measured facts differ (examples 10 to 12, 46, 47, 49). The habit round shows the false-alarm pattern line (example 48: "4 of 4 false alarms scored under 7"), the "Odd for noise" pattern (45) and the "never Not sure" pattern (43). Faults I left visible: in real mode, faint steps, variables and ramps (39 to 41) were not caught by their detectors, so the engine fell back to strength, which is true but not the main story; practice examples 25 and 30 used the "faint step" anchor for the same reason. Fix by calibrating on your real decks and by adding context lessons in real mode.

---

## 5. Adaptive layer

**Per learner** (`newLearner`, `record`): history of (kind, truth, answer, right, strength band, near a hole, lumpy, lead lesson); recent leads; per (lesson, truth) a right or wrong log with mastery at 4 of the last 5 right and loss of mastery after 2 misses in a row; per kind a right or wrong log with kind mastery at 4 of the last 5; how many times each gloss has been shown; when the last pattern line appeared `[RAN]`. Add, when you collect it: confidence per answer, time per card, and a confusion matrix of kind × answer for the round `[INFERRED]`.

**Pattern lines** (`patternLine`): at most once every 6 cards, from the last 12 answers. Order: (1) at least 4 false alarms and 60% or more of them with strength under 7; (2) 3 or more missed gap dips; (3) 3 or more Odd answers on plain noise; (4) 12 answers, at least 4 wrong, none Not sure `[RAN]`. These are the block feedback that Petrov et al. report can work where trial feedback fails `[READ-2]`, and they target his real habits. Keep them about his answers, never about him ("4 of your last 4 false alarms scored under 7", not "you are too eager") `[READ: Kluger and DeNisi via summary; Shute 2008]`.

**Fading**: a mastered lesson stops leading when he is right (it returns at once if he errs); on a mastered kind, the engine prefers facts not yet shown for that kind; glosses disappear after 3 showings `[RAN]`. Supported in spirit by expertise reversal `[READ: Kalyuga 2007]`, weakly by the guidance hypothesis `[READ-2]`.

**Sequencing** (not in the prototype, recommended): easy to hard (Ahissar and Hochstein; Gravity Spy levels); interleave the confusable pair (hard noise, limit planets); bring back a missed kind within 3 to 5 cards and retire a kind's easy cards once mastered, as Kellman's adaptive sequencing does `[READ]`. Keep enough real dips in every round: rare targets are missed more (7% errors at 50% prevalence, 30% under 1%) `[READ-2: Wikipedia summary of Wolfe et al. 2005]`.

**Near-twin pairs** (recommended): after a hard-noise false alarm, the next card is sometimes its twin: the same noise with a planet of strength 7 to 9 injected at the same place. Kellman's contrast principle is the reason `[READ]`.

---

## 6. Overlays for the reveal

| Overlay | How to draw it | Evidence |
|---|---|---|
| Baseline band | Shaded band at ±1 box noise around `base` for the best box's length, so "strength 4" is visible as "4 band widths deep" | `[INFERRED]` |
| Best box | Light orange column over the best event, with its strength printed above | signalling helps retention `[READ-2]` |
| Second-best wiggle | Thin outline box, same colour family, its strength printed | makes the uniqueness lesson visible `[INFERRED]` |
| Ghost planet | Dashed trapezoid of the depth needed for strength 7 at the same duration (feature 20), drawn at the same place | Kellman's contrastive instances `[READ]`; the text sentence already says the numbers |
| Holes and thruster times | Hatched holes; vermillion ticks for firings, with the half day before each shaded | your rule C7 `[INFERRED]` |

**Cautions.** Show overlays only after he locks, never while he answers; an aid that is always there can become a crutch (guidance hypothesis, weak evidence) `[READ-2]`. At most two overlays at once by default (best box plus one), the rest behind one toggle; never cover data points with filled shapes on a 390-pixel-wide screen; overlay lines at least 2 px and at least 3:1 contrast against the background `[MEMORY: WCAG 2.1 non-text contrast]`; every number printed on the plot must equal the number in the text, so both come from `display(F)` `[INFERRED]`.

---

## 7. Extending the engine to real data

1. **No truth, no anchors**: `compose` with `mode: "real"` skips the four anchor lessons, ranks by priority instead of truth, uses hedged meaning lines ("Planets are rarely this deep; an eclipse of the two stars usually is"), and its line 3 says "These are measurements, not a verdict" `[RAN]`. `test.js` fails the build if real-mode text contains verdict words such as "it was", "missed", "definitely" or "hidden planet" `[RAN]`.
2. **Order of events**: Ahmed locks his class and confidence; the engine's measured lines appear; only then is Claude's sealed verdict revealed. Wrong AI suggestions cut correct readings by inexperienced radiologists from nearly 80% to under 20% `[READ-2: RSNA release on Dratsch et al. 2023, Radiology]`, so neither the verdict nor its confidence may appear before he locks.
3. **Balanced facts**: in real mode, prefer one fact for "planet-like" and one against when both exist, so the text cannot read as a verdict by selection `[INFERRED]`.
4. **New context lessons**: "the dip is X days from a primary eclipse"; "it ends Y hours before a thruster firing"; "the second light curve shows Z ppm at the same time". All are measurements, so they fit the same grammar `[INFERRED]`.
5. **New answers** (planet-like, eclipse, flare, step, instrument, unclear): map each to the classes in `ANS_CLASS`; "unclear" behaves like Not sure `[INFERRED]`.

---

## 8. Testing the engine and measuring whether it teaches

**Engine tests** (in `test.js`) `[RAN]`: determinism; every number in the text equals a computed display value; 36 to 44 words; no dash characters and no hyphenated words; no verdict words in real mode; the habit round respects the same rules. Add golden files (store 200 card id → text pairs and diff them on every change) `[INFERRED]`.

**Generator-quirk audit** `[INFERRED]`: if a feature that should be irrelevant predicts the truth on your decks, Ahmed will learn the quirk instead of the skill. Check at least: are holes only ever in noise decoys and gap dips (then "hole means no planet")? Is the event always in the middle third? Is the noise level the same across kinds? Do planets have exact box edges in easy mode? Fit a simple logistic model on irrelevant features; any AUC well above 0.5 is a leak.

**Measuring his improvement** `[INFERRED]`: a fixed held-out set of about 60 cards (never used in practice, same kinds, new seeds), given without feedback at the start and after every few sessions. Report hit rate and false-alarm rate for Dip, the signal-detection sensitivity d′ and criterion c (the criterion is where you expect the change, given Petrov et al.), per-kind recall, the Not sure rate, and later the confidence calibration. For a within-learner comparison, use a *multiple-baseline* design: turn on measured feedback for some kinds (say gap dips and hard noise) first and others later, and see whether held-out accuracy moves when, and only when, each kind's feedback starts `[MEMORY: single-case research design]`. Expect wide error bars: 45 of 50 correct is a 95% interval of 0.79 to 0.96 (computed in the previous Second Sun brief).

**Pitfalls** `[INFERRED]`. False precision: strength is itself uncertain by about ±1, so never make a sentence hinge on 6.8 against 7. Learning the generator: see the audit. Overload: three lines, two overlays, no charts inside the feedback. Too clever: if a sentence needs a second gloss, cut it. Mismatched numbers: the plot, the deck and the text must call the same functions.

---

## What I could not verify

Kluger and DeNisi 1996, Hattie and Timperley 2007, Herzog and Fahle 1997, Butterfield and Metcalfe 2001, Smith et al. 2014 and Wolfe et al. 2005 were read only through secondary pages (tagged READ-2). The Gravity Spy accuracy numbers come from the Zooniverse blog, and I could not confirm the authors and journals of the two papers it links. Kellman's PALM papers on the UCLA site blocked automated access, so I used his 2013 review. Maddox, Ashby and Bohil 2003 and the WCAG non-text contrast rule are from memory. Every threshold in sections 2 to 5 comes from my simulator, not your generator.

## Sources
- [Shute 2008, Focus on formative feedback (PDF)](https://myweb.fsu.edu/vshute/pdf/shute%202008_b.pdf)
- [Wisniewski, Zierer and Hattie 2020, The power of feedback revisited](https://www.frontiersin.org/articles/10.3389/fpsyg.2019.03087/full)
- [Summary of Kluger and DeNisi 1996](https://explore.psychsafety.com/n/kluger-denisi-1996/)
- [Ahissar and Hochstein 2004, Reverse hierarchy theory (PDF)](https://www.cs.princeton.edu/courses/archive/spring08/cos598B/Readings/AhissarHochstein_TCS2004.pdf)
- [Petrov, Dosher and Lu 2006 (PDF)](https://www.socsci.uci.edu/maplab/personal/webdocs/petrovdosherlu06.pdf)
- [Kellman 2013, Adaptive and perceptual learning technologies (PDF)](https://kellmanlab.psych.ucla.edu/wp-content/uploads/sites/357/2025/09/kellman_2013.pdf) · [Kellman lab PALM page](https://kellmanlab.psych.ucla.edu/research-perceptual-and-adaptive-learning-in-medicine.php)
- [Kornell and Bjork 2008 (PDF)](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/Kornell_Bjork_2008_PsychScience.pdf)
- [Carvalho and Goldstone 2014 (PDF)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00936/pdf)
- [Deferred feedback in category learning, bioRxiv 2024](https://www.biorxiv.org/content/10.1101/2024.10.31.621443.full.pdf)
- [Nunes et al. 2014, feedback frequency (guidance hypothesis)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01454/pdf)
- [Kalyuga 2007, Expertise reversal effect (PDF)](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- [Hypercorrection (Wikipedia)](https://en.wikipedia.org/wiki/Hypercorrection_(psychology))
- [Signalling umbrella summary (QIC-WD)](https://www.qic-wd.org/sites/default/files/Umbrella%20Summary%20-%20Signaling%20in%20Training%20111021.pdf)
- [Waite et al. 2019, Perceptual expertise in radiology](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2019.00213/pdf)
- [Zooniverse blog on Gravity Spy training, December 2020](https://blog.zooniverse.org/2020/12/)
- [Eisner et al. 2021, Planet Hunters TESS II](https://ora.ox.ac.uk/objects/uuid:b2e7db4a-dd3a-4996-aeab-bc050616947d/files/rbn999706m)
- [Marshall et al. 2016, Space Warps I](https://arxiv.org/pdf/1504.06148)
- [RSNA release on Dratsch et al. 2023](https://www.rsna.org/media/press/i/2432)
- [Prevalence effect (Wikipedia)](https://en.wikipedia.org/wiki/Prevalence_effect)
