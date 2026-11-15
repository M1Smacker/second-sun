# 017 Twinlight check

Codex, runtime model and effort unverified. The brief specifies neither. Started 15 Nov 2026 at 04:33 Kuwait time, read from Get-Date.

**Plain verdict** Found lesson errors and 2 browser layout defects. The fact-check and requested test implementation are complete, with final runtime measurements below.

Branch `astra/017-twinlight-check`. No commits. Tree node 4.1.

## Scope and choices

Independently check the lessons before Ahmed learns from them, and add repeatable local reader tests. Predicted usage 30 five-hour points and 6 weekly points. AS-017 literature cap 8 web calls. Usage meter unavailable in this headless session.

The brief authorizes the one published-system FITS file and the local build and headless browser procedure from 016. Exact event times and measured depths stay in `data/astra/017/facts.json`, following AGENTS.md's counts-only rule. The table identifies the lesson lines without reproducing those event details. Quiet-day start is also in that private output. The fact script extracts the authorized input path from the brief.

## Deliverables and reproduction

- `research/astra/scripts/017-facts.py` independently loads FITS with Astropy and recomputes arithmetic with NumPy. It imports no pipeline or lesson plotting code.
- `research/astra/scripts/017-build.ps1` builds strictly and redirects generated Tree and learning JSON into `data/astra/017/`. It copies the Book 2 archive into the local build.
- `research/astra/scripts/017-run.mjs` serves port 8495, runs one browser at a time, puts profiles and logs under `data/astra/017/`, and stops its own server.
- `research/burn-3-book/tools/site_check.mjs` gains `learn`. Publish step 4b includes it.

Run from the worktree root, using the authorized interpreters.

```powershell
& 'D:\second-sun\.venv\Scripts\python.exe' -B research/astra/scripts/017-facts.py
powershell -NoProfile -ExecutionPolicy Bypass -File research/astra/scripts/017-build.ps1
node research/astra/scripts/017-run.mjs learn tree layout textfloor
```

ExecutionPolicy Bypass applies to this child process. The first direct script invocation was refused by Windows. A scriptblock retry then failed to resolve PSScriptRoot. The normal child-process invocation completed the strict build. No persistent policy was changed.

## Fact-check table

Line numbers refer to the checked source lessons. F means `017-facts.py` and `data/astra/017/facts.json`. P1 to P6 refer to the primary sources below. WRONG identifies a correction, and CONFIRMED may still carry a beginner-facing qualification.

### Lesson 1.1, `l1-a-light-curve.md`

| Lines | Claim | Independent evidence or correction | Label |
|---|---|---|---|
| 8, 16, 19 | Light curve is brightness against time, shown over about 24 days | FITS retained endpoints span 24.0482 days. This is elapsed span. Actual retained exposure totals 21.1708 days. F | CONFIRMED |
| 22 | NASA TESS, launched 2018, sectors about four weeks, sector 44 in Oct and Nov 2021 | NASA launch page gives 18 April 2018. P3 gives 27.4 days per nominal sector. P5 gives sector dates in those months. | CONFIRMED |
| 25 | This sector has 24 days of good data because of downlink gap | F finds a 24.0482-day span containing a 2.8183-day gap, with 21.1708 days of retained exposure. A gap removes coverage inside the span. It does not explain a nominal 27-day sector becoming a 24-day span. P5 gives 22.78 mission-wide science days and 1.47 paused days. | WRONG |
| 28 | Catalogue identifier, unresolved binary, 19.7-day orbit, invisible naked-eye but accessible to small telescopes | P1 describes an eclipsing binary with that period and V magnitude 10.141. Naked-eye invisibility is reasonable under ordinary observing conditions. Small-telescope ease depends on aperture and sky. | CONFIRMED / LIKELY for observing ease |
| 28, 31 | Eclipses block light, once per orbit | Blocking is correct. This binary has a primary and secondary eclipse per orbit. Each kind repeats once per orbit. Clarify the wording. P1 and P2. | CONFIRMED with qualification |
| 34 | Jupiter-sized circumbinary planet discovered in 2021 | P1 submission date is 2021. Reported planet size is 1.004 Jupiter radii and it orbits the binary. | CONFIRMED |
| 34 | Planet does not transit in sector 44 | No photodynamical propagation was run. Absence of an obvious dip cannot establish absence of transit. The 2021 paper predates these sector observations. | UNCERTAIN |
| 38 | Two-minute measurements and normal count about 22,437 each second | F gives 2.00019-minute median cadence and median PDCSAP flux 22,437.119 electrons/s. PDCSAP is corrected aperture flux. Explain that these are electrons/s rather than literal photon counts. P3 supports target cadence. | CONFIRMED with qualification |
| 40, 42, 48 | Fraction and percentage normalization | F/Fnormal is dimensionless. Subtracting one and multiplying by 100 gives percentage change. Zero is the chosen baseline. | CONFIRMED |
| 40, 88 | Anything below normal means blocked light | Flares, spots, intrinsic variability, detector noise and pointing also change measured light. P2 explicitly allows stellar flux variability. Lesson 1.3 itself demonstrates below-normal noise without an eclipse. | WRONG |
| 45 | Median resists a few odd points | A small number of extreme values cannot drive the median arbitrarily, though eclipses and variability can shift it. It is an estimated baseline. | CONFIRMED with qualification |
| 51, 53, 55, 57 | First trough counts and three arithmetic steps | F independently reproduces the quoted flux counts and rounded ratio, subtraction and percentage. Measured depth stored privately. | CONFIRMED |
| 59, 71 | Nearly equal-sized stars can hide much of each other's light and produce different depths | P1 gives stellar radii 1.3827 and 1.3124 solar radii. Depth also depends on surface brightness, overlap and dilution. | CONFIRMED |
| 62, 64, 69 | Second eclipse ratio and answer | F independently reproduces the rounded ratio and the stated negative percentage. Measured depth stored privately. | CONFIRMED |
| 78 | Ten-minute plot points are averaged | `lesson_plots.py:binned` takes medians. An arithmetic mean and a median are different operations. | WRONG |
| 84 | Eclipse shape carries size and viewing-angle information | P2 geometry and contact-duration equations support this. Several parameters are coupled, so a shape alone does not uniquely give both sizes. | CONFIRMED with qualification |
| 88, 141 | Planetary dips much smaller than stellar eclipses | Correct for this Jupiter-sized planet and these Sun-sized stars. Generalizing to every planet and star would include large planets crossing very small stars. | CONFIRMED for this system |
| 92 to 97 | 20,000 to 19,800 example | F computes ratio 0.99, fractional change -0.01 and -1%. | CONFIRMED |
| 102 to 107 | Ratio 0.97 example | F computes -0.03 and -3%. | CONFIRMED |
| 112 to 119 | Two-minute day, 720 points, sector 15,243 points and 17,280 nominal points | F counts exactly 15,243, and computes 1,440/2=720 and 24*720=17,280. The main gap also accounts for missing measurements. Attributing the entire deficit to rejected quality flags is misleading. | CONFIRMED counts, WRONG explanation |
| 122 to 129 | Quoted eclipse times and 11.87-day separation | Subtraction of the printed times is correct. The first raw minimum differs from its printed time by about 0.0054 day, the second by about 0.0063 day. Raw trough separation is 11.8817 days. Printed times need a stated estimator, such as fitted center or minimum bin. | UNCERTAIN measurement, CONFIRMED arithmetic |
| 131 | Half-period 9.85 days, uneven spacing implies eccentric orbit | 19.7/2=9.85. P2 equation 33 constrains eccentricity times the cosine of orientation. The gap alone cannot uniquely determine eccentricity or the full oval. | CONFIRMED with qualification |
| 136 to 141 | A planet crossing produces a dip | Occulted stellar area reduces observed light under the stated transit assumptions. Word alternatives accepted by the reader are checked separately. P2. | CONFIRMED |
| 148 to 150 | Source description and system parameters | F confirms quality-zero PDCSAP selection and sector/cadence. P1 confirms period, eccentricity 0.45 and Jupiter-like radius. | CONFIRMED |

### Lesson 1.2, `l2-percent-and-ppm.md`

| Lines | Claim | Independent evidence or correction | Label |
|---|---|---|---|
| 8 | One star hid the quoted percentage of the other's light | Lesson 1.1 measured the combined pair's light. The denominator changes in this sentence. It must say pair's light. | WRONG |
| 12, 72 | Quiet points wander about plus or minus 0.3%, no object crossing | F range is -3,346.7 to +3,639.5 ppm, consistent with the approximate spread. No stellar eclipse is present. Absence of a planetary crossing has not been established by a system model. | CONFIRMED range, UNCERTAIN absence claim |
| 16, 18, 21, 25 | Depth equals squared radius ratio, twice the radius gives four times depth | Divide pi*Rp^2 by pi*Rs^2. Requires a fully overlapping planet disc and uniform stellar surface brightness, normalized to that star alone. P2. | CONFIRMED under assumptions |
| 28 | Limb darkening makes rounded transits | P2 section 2.5 supports brighter center and fainter edge. Ingress and egress are curved even for uniform discs because overlap area changes nonlinearly. | CONFIRMED with qualification |
| 30, 33, 36, 38 | Earth/Sun ratio, fraction, percent, ppm | F gives ratio about 0.009168, depth 84.0446 ppm and 0.00840446%. One percent is exactly 10,000 ppm. | CONFIRMED |
| 41, 43, 45, 47, 49 | Planet 11.25 Earth radii, star 1.3827 Sun radii, example steps | P1 supplies radii. F computes 0.103135 solar radii, radius ratio about 0.074588 and 5,563.638 ppm, 0.556364%. Quoted intermediate rounding is appropriate. | CONFIRMED |
| 51 | Second star roughly halves depth, comparison about 80 times smaller | Combined-light depth is single-star depth times F1/(F1+F2). Similar temperatures and radii in P1 support roughly half. 45/0.56 is about 80. The final comparison uses the hypothetical undiluted planet, while the preceding sentence describes its diluted depth. Label that comparison clearly. | LIKELY dilution, CONFIRMED arithmetic |
| 54 to 63 | Jupiter ratio and 10,570 ppm | F gives 10,561.39 ppm from the original radii. Squaring the rounded 0.1028 gives 10,567.84 ppm, so 10,570 is consistent with the rounded example. Jupiter/Earth depth ratio is about 126. | CONFIRMED |
| 70 | Flux ratio conversion | F gives 0.0012 deficit, 0.12% and 1,200 ppm. | CONFIRMED |
| 72 | Earth-sized dip under 100 ppm around these stars | Squared-radius depth is about 44 ppm for the larger star alone, further reduced in combined light. This is well below 933 ppm single-point scatter. | CONFIRMED under model |
| 76 | Summary formula and Jupiter/Earth values | Same assumptions and arithmetic as above. Add the single-star normalization assumption to prevent applying it directly to blended binary light. | CONFIRMED with qualification |
| 80 to 85 | 0.25% problem and solution | F gives exactly 2,500 ppm. | CONFIRMED |
| 90 to 95 | 300 ppm problem and solution | F gives exactly 0.03%. | CONFIRMED |
| 100 to 105 | Flux ratio problem and solution | F gives 1,200 ppm within floating-point precision. | CONFIRMED |
| 110 to 115 | One-tenth radius problem and solution | F gives 0.01 fraction and 10,000 ppm. | CONFIRMED |
| 120 to 127 | Half-Sun star problem, fourfold depth, easier small planets | F gives 54.54 Earth radii, ratio about 0.018336 and 336.178 ppm. The fourfold scaling is exact under the model. Easier detection assumes comparable measurement precision and observing coverage. | CONFIRMED with qualification |
| 134 to 137 | Radius and source constants | P6 nominal radii give 695,700/6,378.1=109.0764 and 71,492/6,378.1=11.20898. Quoted 109.08 and 11.21 are appropriate rounded ratios. | CONFIRMED |

### Lesson 1.3, `l3-noise.md`

| Lines | Claim | Independent evidence or correction | Label |
|---|---|---|---|
| 8, 12 | Quiet day, no transit, fluctuating points | F gives 720 good points with finite scatter. Absence of a stellar eclipse is apparent from the full curve. A planetary non-transit is not independently established. | CONFIRMED data, UNCERTAIN transit claim |
| 16, 19 | Photon, detector, pointing and stellar variability as noise | Photon counting has Poisson variance. P3 noise budget includes photon, detector and pointing terms. Noise is defined relative to the signal sought, so stellar variability can be noise for this task. Specific contributions to this day remain unseparated. | CONFIRMED mechanisms, UNCERTAIN attribution |
| 22, 25, 28, 30 | Standard deviation recipe and typical distance | The formula is root-mean-square distance from the mean. Calling it typical distance is an accessible approximation, while mean absolute distance is a different statistic. | CONFIRMED with qualification |
| 25 | About two thirds within one sigma | This needs approximately Gaussian errors. Standard deviation alone guarantees no such fraction. A distribution concentrated equally at -2,-1,1,2 has only half its points inside one sigma. | WRONG as unconditional claim |
| 33 | N versus N-1, tiny difference for many points | Ratio is sqrt(N/(N-1)), about 1.00070 for 720 points. N-1 estimates population variance from a sample. It is not simply an interchangeable definition in every use. | CONFIRMED with qualification |
| 37, 39, 41, 43, 45, 47 | Five-point worked solution | F mean 1, square sum 0.0000025, mean square 0.0000005, sigma 707.1068 ppm. Differences and their squares reproduce. | CONFIRMED |
| 49, 68 | 720 points, about 930 ppm | F gives exactly 720, sigma 932.136 ppm relative to full-sector median or 933.098 ppm relative to quiet-day median. Both round to about 930. Slow drift contributes to this scatter, so attributing all of it to chance is too strong. | CONFIRMED number, qualification needed |
| 53, 55, 58 | Averaging reduces noise by sqrt(N), four points halves it | Var(mean)=sum variances/N^2 for uncorrelated equal-variance errors. With covariance terms present, the rule changes. Random errors can still be correlated. State independent or uncorrelated, equal-variance errors. | CONFIRMED under assumptions |
| 61, 70, 74 | Fifteen points per 30-minute average, measured 362 ppm | F gives 48 groups of 15. Arithmetic-mean scatter is 356.847 ppm. Median scatter is 361.634 ppm. The 362 number describes medians. The displayed formula predicts arithmetic means. | WRONG statistic comparison |
| 70, 72 | sqrt(15)=3.87 and 930/3.87 about 240 ppm | F exact calculation gives 240.125 ppm. | CONFIRMED |
| 76 | Drift a few hundred ppm/day, detrended scatter 266, white prediction 230 | F fitted drift is 936.984 ppm/day, nearly 1,000. Detrended arithmetic means give 232.774 ppm, medians 267.270 ppm, white prediction 230.578 ppm. The 266 value is near the median result but is not reproduced exactly. | WRONG drift scale and estimator interpretation, UNCERTAIN exact 266 method |
| 76, 79, 82 | Shared drift cannot cancel like independent noise, red noise hurt survey yields | Covariance contributes to variance of an average. Removing the fitted line substantially reduces this day's binned scatter, though the physical source of the drift is unmeasured. P4 supports survey consequences. | CONFIRMED effect, UNCERTAIN physical cause |
| 85, 87, 92 | One-hour 30 points, sqrt(30)=5.48, about 170 ppm | F computes 169.794 ppm. | CONFIRMED |
| 94 | This day's real one-hour noise exceeds white prediction | F arithmetic-mean hourly scatter is 318.920 ppm. | CONFIRMED |
| 101, 144 | Red noise cannot average away and must be removed first | Short averages are less effective against positive correlations. Averaging can still reduce correlated noise over longer intervals. Modelling its covariance is another valid detection method. Removal can distort real signals. | WRONG as absolute statement |
| 105 to 110 | 1,000 ppm, 25 points, 200 ppm | F gives exactly 200. | CONFIRMED |
| 115 to 122 | 1,200 to 300 ppm needs 16 points, halving costs fourfold points | F computes (1200/300)^2=16. Follows the stated white-noise model. | CONFIRMED |
| 127 to 134 | Four-point standard deviation, answers 1,414 and 1,633 | F gives population 1,414.214 and sample 1,632.993 ppm. Problem explicitly asks divide by N, so accepting the N-1 answer weakens that instruction. | CONFIRMED arithmetic, misleading acceptance |
| 139 to 144 | Slow shared fluctuations are red noise | Correct introductory description of positive time correlation. Randomness alone does not distinguish white from red. | CONFIRMED with qualification |
| 151, 152 | Noise/source summary | Recomputed values above identify the mean/median mismatch. P4 supports the quoted survey claims. | CONFIRMED source, correction needed |

## Primary sources, AS-017

All four requested abstract pages were opened, followed by HTML where needed. Six web calls used against the eight-call cap. Quotes below stay short. No files were downloaded.

- P1. Kostov et al. abstract gives "a period of P = 19.7 days". Its reported stellar and planet radii support the size examples. Its discovery occurred in sector 21. The quoted sector-44 absence claim needs later observations or model propagation. [Abstract](https://arxiv.org/abs/2105.08614), [full text](https://arxiv.org/html/2105.08614v2).
- P2. Winn section 2.5 says stellar discs are "brighter in the middle and fainter at the edge". Equations 20 to 22 give the squared radius ratio under the stated approximations. Equation 33 constrains eccentricity with orientation. [Abstract](https://arxiv.org/abs/1001.2010), [full text](https://arxiv.org/html/1001.2010v5).
- P3. Ricker abstract states "Brightness measurements of preselected target stars will be recorded every 2 min". Section 7.2 describes 27.4-day sectors. Section 8.1 lists photon, detector and pointing noise sources. Its prelaunch date prediction is superseded by NASA's actual 2018 launch date. [Abstract](https://arxiv.org/abs/1406.0151), [full text](https://arxiv.org/html/1406.0151v3), [NASA mission](https://science.nasa.gov/mission/tess/).
- P4. Pont et al. abstract says "yield predictions assume uncorrelated noise" and red noise "cannot be neglected in typical ground-based surveys". This supports the survey-history sentence, while saying nothing about which instrument or stellar process caused this particular day's drift. [Abstract](https://arxiv.org/abs/astro-ph/0608597).
- P5. NASA sector-44 notes give "Days of Science Data Collection: 22.78". They date sector 44 to October and November 2021 and give 1.47 days paused. Mission-wide collection and this particular quality-filtered light curve have different totals. [NASA release notes](https://heasarc.gsfc.nasa.gov/docs/tess/data_release_notes.html).
- P6. IAU B3 defines nominal radii as exact conversion constants. Table values are solar radius 695,700 km, terrestrial equatorial radius 6,378.1 km, jovian equatorial radius 71,492 km. [Abstract](https://arxiv.org/abs/1510.07674), [resolution HTML](https://arxiv.org/html/1510.07674v1).

## Browser checks

Strict MkDocs build completed in 2.64 seconds, with 269 precache entries and 5,577 KB. Initial suite completed. Tree passed 13 checks, textfloor passed 15 pages. Layout failed solely on the Tree search input at 290 by 42 px in both themes and widths, against the existing 43.5 px minimum. No horizontal overflow or console errors were recorded. Initial learn run made 217 assertions. It exposed test-harness issues in selecting the non-highlightable kicker paragraph and mapping layout coordinates to the mobile visual viewport for pointer clicks. The harness now selects an eligible paragraph, waits for scroll positioning and applies the viewport scale and offsets. The completed unmodified-app rerun made 239 assertions. Its only failures were two measurements of the same 12 px phone overflow on lesson 1.3, before and after answering. Every answer alternative and hint passed in both sizes. Highlight and note persistence passed. Expected finish at first start was 04:52 Kuwait time, from the runner's 15-minute estimate. Machine output and browser profiles are confined to `data/astra/017/`.

## What I did NOT check

- Independent reviewer assessment of the new test code. These are producer checks.
- Sound output, voice pronunciation or real-device Safari behavior.
- Physical attribution of quiet-day drift or a propagated planetary orbit proving no sector-44 transit.
- `say()` conversion through the page. It is private inside the app closure and has no callable page API. The Listen sheet and voice menu are tested without playback.
- Live site, publishing, cloud scores, sealed stars or pipeline behavior.

## STOP SIGNS hit

AGENTS.md's committed-event-detail restriction takes priority over reproducing exact event times and measured depths in the fact-check table. Full values are in private machine output. No protected light was opened. The specifically authorized published-system FITS was the only light curve read.

## QUEUE PROPOSALS

All proposals belong to Tree node 4.1. Claude files them.

- FIX the mean/median noise comparison, the combined-light denominator, coverage explanation, unconditional Gaussian coverage statement, and absolute claims about below-normal light and red noise.
- FIX or qualify eclipse-time estimator, unsupported non-transit assertions, drift attribution and approximate drift scale.
- FIX the Tree search field height, 42 px against the 44 px touch target, at 390 and 1280 widths in both themes. CONFIRMED by layout mode.
- FIX lesson 1.3 phone overflow, 12 px at 390x844 with solutions opened, before and after answering. CONFIRMED by learn mode. The specific overflowing element is investigated in the mutation diagnostic below.

## IDEAS

None beyond the requested corrections and tests.

## Disagreements with Claude

The noise lesson attributes the excess above the mean-noise rule entirely to time correlation while plotting medians. Independent means after linear detrending give 232.8 ppm against a 230.6 ppm prediction. Medians give 267.3 ppm. The estimator difference must be accounted for before attributing the remainder to correlated noise. No book source was changed.

## Questions for Ahmed

None. Claude can review the measured corrections.

## Usage

Predicted 30 five-hour and 6 weekly points. Actual unavailable because the headless runner exposes no usage panel. Lesson learned, identify the averaging estimator before comparing its scatter with a theoretical mean-noise formula.


## Completed runtime evidence

The `learn` mode uses 390x844 and 1440x900, with reduced motion for deterministic interaction timing. It checks all three lessons and their worked solutions. Twenty accepted answer alternatives and 28 hint keys were exercised per size. There were no console errors. Home has Continue, three stats and seven units. Contents lists all 23 planned lessons. The first lesson plots have 1,020 and 171 points. The noise lesson's 30-minute plot correctly contains 48 points, so the 100-point requirement applies to the two lesson 1.1 plots.

The glossary Back operation changed scroll by zero pixels. All six unanswered lesson 1.1 problems entered the due list at completion. Continue restored a saved halfway position to about 0.498 on phone and 0.506 on desktop. Highlights and note text survived reloads. Six available English voices appeared in Listen on both sizes. Playback was never started. Ordinary visible text met 14 px across lessons, opened solutions, feedback and tool panels. KaTeX script glyphs measured 13.23 px on phone and 13.986 px on desktop, within the requested exception.

The existing `layout` mode covers 390 and 1280 widths in both themes, 60 page checks. Existing `textfloor` covers 15 pages at 375 px. `learn` supplies the requested lesson-specific 390 and 1440 checks. `tree` checks desktop 1440 and phone 390. The modes retain their distinct scopes.

### Mode output

#### learn, exit 1

```json
{"mode":"learn","checks":239,"fails":["390 learn/u1/l3-noise/: text floor or horizontal overflow","390 learn/u1/l3-noise/: feedback and solutions text floor or overflow"],"views":[{"width":390,"pages":[{"page":"learn/u1/l1-a-light-curve/","math":{"errors":0,"rendered":19,"raw":false},"plots":[1020,171],"text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]},"feedbackText":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}},{"page":"learn/u1/l2-percent-and-ppm/","math":{"errors":0,"rendered":30,"raw":false},"plots":[720],"text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[{"tag":"SPAN","class":"base","text":"fraction×","right":436.0625},{"tag":"SPAN","class":"mord text","text":"fraction","right":412.96875},{"tag":"SPAN","class":"mord","text":"fraction","right":412.96875},{"tag":"SPAN","class":"mspace","text":"","right":412.96875},{"tag":"SPAN","class":"mbin","text":"×","right":431.875},{"tag":"SPAN","class":"mspace","text":"","right":431.875}],"small":[],"katexScriptSizes":[13.23]},"feedbackText":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[{"tag":"SPAN","class":"base","text":"fraction×","right":436.0625},{"tag":"SPAN","class":"mord text","text":"fraction","right":412.96875},{"tag":"SPAN","class":"mord","text":"fraction","right":412.96875},{"tag":"SPAN","class":"mspace","text":"","right":412.96875},{"tag":"SPAN","class":"mbin","text":"×","right":431.875},{"tag":"SPAN","class":"mspace","text":"","right":431.875}],"small":[],"katexScriptSizes":[13.23]}},{"page":"learn/u1/l3-noise/","math":{"errors":0,"rendered":45,"raw":false},"plots":[720,48],"text":{"overflow":12,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]},"feedbackText":{"overflow":12,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}}],"accepted":20,"hints":28,"panels":[{"name":"glossary","text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}},{"name":"Contents","text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}},{"name":"highlight pill","text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}},{"name":"note editor","text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}},{"name":"Listen","text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.23]}}],"home":{"continue":true,"stats":3,"units":7,"text":{"overflow":0,"viewport":{"width":390,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[]}},"glossaryScrollDelta":0,"contents":{"expected":23,"missing":[]},"voices":{"available":["Microsoft David - English (United States)","Microsoft Mark - English (United States)","Microsoft Zira - English (United States)","Google US English","Google UK English Female","Google UK English Male"],"listed":["Microsoft David - English (United States)","Microsoft Mark - English (United States)","Microsoft Zira - English (United States)","Google US English","Google UK English Female","Google UK English Male"]},"finished":{"done":{"1.1":"2026-11-15"},"due":6,"problems":6},"savedFraction":0.5,"resumedFraction":0.4977027027027027},{"width":1440,"pages":[{"page":"learn/u1/l1-a-light-curve/","math":{"errors":0,"rendered":19,"raw":false},"plots":[1020,171],"text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]},"feedbackText":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}},{"page":"learn/u1/l2-percent-and-ppm/","math":{"errors":0,"rendered":30,"raw":false},"plots":[720],"text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]},"feedbackText":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}},{"page":"learn/u1/l3-noise/","math":{"errors":0,"rendered":45,"raw":false},"plots":[720,48],"text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]},"feedbackText":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}}],"accepted":20,"hints":28,"panels":[{"name":"glossary","text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}},{"name":"Contents","text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}},{"name":"highlight pill","text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}},{"name":"note editor","text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}},{"name":"Listen","text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[13.986]}}],"home":{"continue":true,"stats":3,"units":7,"text":{"overflow":0,"viewport":{"width":1425,"scale":1},"overflowElements":[],"small":[],"katexScriptSizes":[]}},"glossaryScrollDelta":0,"contents":{"expected":23,"missing":[]},"voices":{"available":["Microsoft David - English (United States)","Microsoft Mark - English (United States)","Microsoft Zira - English (United States)","Google US English","Google UK English Female","Google UK English Male"],"listed":["Microsoft David - English (United States)","Microsoft Mark - English (United States)","Microsoft Zira - English (United States)","Google US English","Google UK English Female","Google UK English Male"]},"finished":{"done":{"1.1":"2026-11-15"},"due":6,"problems":6},"savedFraction":0.5,"resumedFraction":0.5059677419354839}],"texToWords":"NOT TESTED: say() is private to learn.js; no page API exposes it","errors":[],"pass":false}
```

#### tree, exit 0

```json
{"mode":"tree","checks":13,"fails":[],"nodes":24,"journey":{"phases":5,"days":18},"search":{"word":"How","id":"1"},"phoneOverflowOpen":0,"phoneOverflowClosed":0,"errors":[],"pass":true}
```

#### layout, exit 1

```json
{"mode":"layout","checks":60,"overflow":[],"small":["390 slate /: input. 290x42 'Search the Tree'","1280 slate /: input. 290x42 'Search the Tree'","390 default /: input. 290x42 'Search the Tree'","1280 default /: input. 290x42 'Search the Tree'"],"schemeMismatch":[],"inlineExempt":["a","ss3-shelf__item ss-reveal is-in","ss3-deck__card ss-reveal is-in","ss-chip ss-chip--verified","ss-chip ss-chip--likely","ss-chip ss-chip--unverified"],"toggle":{"before":"default","after":"slate","changes":1,"ready":true,"bodyTransition":"0.2s, 0.2s, 0.2s"},"reducedMotion":{"body":"0.001s","content":"none","contentDuration":"0.001s","toolbar":"0.001s"},"normalMotion":{"content":"ss3-enter 0.52s","toolbar":"0.18s","link":"0.18s, 0.18s"},"hiddenShown":0,"paletteToggles":1,"errors":[],"pass":false}
```

#### textfloor, exit 0

```json
{"mode":"textfloor","checks":15,"fails":[],"pages":{},"errors":[],"pass":true}
```

## Defect interpretation and negative test

1. Tree home search field is 290 by 42 px. CONFIRMED. It misses the existing 44 px control target in both themes and both tested widths. LIKELY cause is the search-input sizing rule. `layout.log` records all four occurrences.
2. Lesson 1.3 has 12 px document-level horizontal overflow at 390x844 with solutions open. CONFIRMED before and after answer entry, across repeated runs. Lesson 1.1, lesson 1.2 and the learning home have zero overflow at that size. The exact offending element remains UNCERTAIN. The diagnostic element filter did not isolate it. Formula and layout containment are areas for Claude to inspect, without attributing the cause to them as fact. This failure is distinct from the text floor, which passes.

A deliberate negative test changed only the scratch site's correct-answer feedback label from Right to Changed. All 40 correct-answer checks rejected the mutation. `data/astra/017/mutation-status.json` records exit 1 and 40 rejected answers. The source app was untouched. The scratch asset was restored and compared byte-for-byte with the source asset. This verifies restoration, and does not establish semantic correctness. The unmodified-app evidence above was preserved separately from the mutation output.

## Final verification and handoff

- Runtime checks performed include the strict local MkDocs build, the independent FITS/arithmetic script, all four requested browser modes, and the scratch feedback mutation.
- Static checks performed include Node syntax checks for `site_check.mjs` and `017-run.mjs`, Python compilation without bytecode writes, PowerShell parsing, and `git diff --check`.
- Source comparison in `data/astra/017/source-check.json` found all three lesson files, `learn.js`, `learn.css` and `hooks.py` equal to HEAD after line-ending normalization. This comparison concerns source preservation.
- All runtime data, logs, browser profiles and generated assets are under `data/astra/017/`. The local server was stopped by its runner. The pre-existing `.codex_run.lock` was preserved.
- The TeX-to-words private function remains untested through the page. Usage-meter values remain unavailable. These exclusions also appear above.

**Next** Claude reviews this report and files the node 4.1 corrections. This is a low-cost reading step and requires Claude.

DONE, the requested independent audit and browser mode are delivered, with measured failures and exclusions recorded.
