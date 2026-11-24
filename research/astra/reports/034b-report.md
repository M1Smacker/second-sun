# 034b fact-check finish, AS-034b (Codex, 24 Nov 2026, 23:20 Kuwait)

**Model:** Runtime model and effort independently unverified; brief specifies neither.
**Plain verdict:** 5 issues need correction or qualification. All six requested audit groups are completed, with limitations below. The principal measured numbers and both new plots check out. This is an audit completion, not a claim that the book is fixed.
**Branch:** `astra/034b-factcheck-finish`, unchanged; zero git writes or commits. Book and frozen code unchanged. Existing `.codex_run.lock` preserved.
**Tree:** Node 4.1 for every finding and proposed fix.
**Decision:** What Claude must address before removing the four lessons' fact-check-pending labels.
**Budget:** Predicted 45 five-hour / 8 weekly points; cap 60 five-hour / 10 weekly points consumed, with the standing stop near 80% five-hour. Research cap 16 web calls; used 11. Initial observed meter 2% / 31%; pre-report 44% / 38%. Final reading is in USAGE.md. These are rounded account-wide meters, not isolated billing for this run.

## Findings

Paths below are relative to `book/docs/learn/`, except where specified. CONFIRMED means the stated defect or counterexample was demonstrated, not that a proposed fix has been implemented. No new search settings or filter changes are proposed.

| ID | Lesson and line | What | Evidence | Proposed fix | Severity / label |
|---|---|---|---|---|---|
| F1 | 3.4, `u3/l4-doppler.md`:104 | Says a future dip would require a spectrograph's speeds before it could be a planet with a known mass. This makes one useful follow-up method a universal requirement. | Doyle 2011, PDF p. 3, obtains a planetary mass constraint from binary eclipse timing. Kostov 2021 also explains mass constraints from dynamical eclipse timing. A single isolated transit does not measure mass, but time series photometry can contain gravitational information. Sources S2 and S3. | Say spectra are a common and valuable route; repeated transit/eclipse timing plus a dynamical model can also constrain mass, given the necessary stellar information. Retain the warning that one dip alone does not establish mass. | Medium, CONFIRMED |
| F2 | 4.4, `u4/l4-planets-around-two-suns.md`:49, 53, 56, 84 | Calls 56 and 78 km/s the largest permitted relative speeds without stating that the planet is treated as a point or defining the duration's contacts. | `geometry.json`: point-planet central chords give 55.744 and 78.288 km/s. If the quoted durations mean first to fourth contact, a central finite planet travels `2(Rstar + Rp)`, giving 59.893 and 84.434 km/s for the lesson's Rp. Source S1 distinguishes total, full and halfway-contact duration. | Explicitly call these small-planet, steady-speed estimates. Define duration before claiming a bound. If teaching total contact duration, include Rp and update answers and the conditional star-speed examples together. Do not relabel the paper's approximate durations as precisely defined measurements. | Medium, CONFIRMED |
| F3 | 4.1, `u4/l1-eclipsing-binaries.md`:24, 66; 4.4, `u4/l4-planets-around-two-suns.md`:80 | Uses total luminosities and the temperature-to-the-fourth-power rule directly as TESS light fractions, without stating the bandpass approximation. | NASA describes a roughly 600 to 1000 nm detector band. `caveats_payloads.json`: a blackbody calculation through the existing response curve gives surface ratio 1.03748, versus bolometric 1.04555; primary light share 0.53585, versus the adopted 0.53721. This calculation is illustrative, not an atmosphere-model measurement. | Define L as light in the observing band for eclipse calculations; say the bolometric fractions are a close approximation here because the two temperatures are similar. The temperature argument remains qualitatively supported; do not replace it with a claim of an exact TESS surface-brightness ratio. | Low, CONFIRMED missing qualification |
| F4 | 4.2, `u4/l2-how-two-stars-orbit.md`:68; `book/tools/lesson_plots_u4b.py`:5 and 50 | The explanation treats the longer eclipse as a sufficient direction test. Chord length, including grazing geometry, can reverse that test. The code's ratio-only guard is not generally sufficient. | At the published inclination, independent finite-disc geometry gives secondary/primary half-depth-width ratio 2.647 for the plotted sign and 0.378 for the opposite sign. So this system supports the plot. But with the same positive sign and inclination 87.35 degrees, both eclipses still occur and the ratio becomes 0.618, passing the producer's opposite-sign threshold. This counterexample's secondary is very shallow, unlike the observed one. `geometry.json`, S1. | Say that duration depends on both speed and chord, and that the observed deep eclipses plus geometry support the sign here. Include depth/impact constraints in any reusable guard. No reason found to flip or redraw this plot. | Low for this lesson; Medium if reused as a general guard, CONFIRMED |
| F5 | 4.2, `u4/l2-how-two-stars-orbit.md`:124; 4.4, `u4/l4-planets-around-two-suns.md`:88; shared `assets/learn.js`:128 | Correct fractional forms are rejected. | Extracted, unmodified `num` and `same` functions executed in Node: `1/2` rejected for equal-mass share; `1/4` rejected for the quarter-orbit answer, while 0.5 and 0.25 pass. `Yes!` is also rejected in 3.4 problem 5, a smaller punctuation limitation. `grader.json`. | Add explicit fraction aliases for these answers or a deliberately restricted fraction parser. Alternatively explicitly request decimal answers. Avoid evaluating arbitrary input as JavaScript. | Low, CONFIRMED |

The useful engineering distinction is between checking a number and checking the rule used to infer it. The orbit plot is numerically right for this system, while its duration-only justification still needs a condition. Similarly, checking a parser's listed answers does not show that every valid way a learner writes the answer is accepted.

## Checks actually performed, in brief order

### 1. Grading

Executed `check_034b_grader.cjs`. It reads all four current lesson files and extracts the actual `num` and `same` functions from `learn.js`; it does not translate them into Python. The surrounding answer split, default tolerance and unit selection match `problems()`.

- 28 problems, 67 answer variants, 32 hints, 283 cases: zero unexpected outcomes in that declared test matrix.
- All independently calculated answers passed. Every hinted mistake was rejected. Tested explicit correct units, wrong units, scientific notation, zero, factors of 1,000 and 10% errors where meaningful. The plot-reading question deliberately allows 12%, so its 10% case is expected to pass.
- Separate valid-notation probes exposed F5. These are not counted as successful acceptance tests.
- An in-memory mutation reversed the numeric comparison; the exact-answer control then failed, demonstrating that this check can detect a broken comparison. No book source was mutated.
- Read and checked the wording of hints, worked arithmetic, unit choices and tolerances. No incorrect answer key or hinted arithmetic mistake found. This is finite coverage, not a proof about all possible strings.

### 2. Raw eclipse light

Before opening any FITS file, the script checked the requested identifier against the complete current R1 table: Fence A has 552 rows representing 549 unique stars; Fence B has 803 rows. The requested published system matches neither. This check does not use a published-system override to bypass a fence.

Read only the four authorized SPOC files, sectors 44 through 47. Verified each file's target header. Kept finite time/PDCSAP values with QUALITY equal to zero, and normalized each sector by its median. Kept counts were 15,243, 15,510, 16,717 and 16,824. No pipeline or plot module was imported.

The independent method detects deep intervals directly before folding, fits a local quadratic bottom, and interpolates half-depth crossings per event. It found five primary and four secondary eclipses. Absolute centres and individual depths are saved only in `data/astra/034b/eclipses.json`.

Aggregate checks on this published teaching example:

| Quantity | Independent result | Assessment |
|---|---:|---|
| Median primary depth | 43.500% | Agrees with 43.5% |
| Median secondary depth | 35.776% | Agrees with 35.8% |
| Primary-to-secondary separation | 11.88048 d | Agrees with about 11.88 d; individual secondary estimates span 11.87922 to 11.88177 d |
| Width using a fitted peak depth | 2.791 / 7.255 h | Similar to the stated 2.74 / 7.27 h; estimator-dependent |
| Width using the median bottom over 0.04 d | 2.845 / 7.283 h | A shallower definition of the bottom widens the primary's half-depth interval |
| Separate replay of the producer's folded smoothing definition | 2.738 / 7.266 h | Reproduces 2.74 / 7.27 h |

CONFIRMED agreement at the lesson's practical precision. The replay of the producer's definition is explicitly not an independent measurement. Event-to-event ranges are not formal confidence intervals. No precision dispute or width correction is proposed.

### 3. Timing, inclination and orientation

CONFIRMED: Winn's textbook chapter, equation 33, gives `Delta t / P = 1/2 + (2/pi) e cos(omega)` to first order in eccentricity. Its equations 5 to 8 provide the projected-separation geometry. This supplies an exact locatable source in place of the lesson's generic textbook attribution.

Independently integrated the areal law between minima of projected separation, instead of using the producer's eccentric-anomaly solver. With the measured timing and adopted e = 0.4479:

- Edge-on: omega 70.5340 degrees and e cos(omega) 0.149261.
- At the published Family 1 inclination 89.4182 degrees: omega 70.5360 degrees and e cos(omega) 0.149247. Other published families are similarly close to edge-on.
- Holding omega fixed, the inclination changes the eclipse separation by 16.46 seconds. The first-order inclination multiplier is `1 + cot(i)^2/2 = 1.00005156`. The correction is negligible for this lesson's rounded values, but the word exact should remain qualified as exact edge-on geometry.
- The positive-sine branch gives separations 0.10787 / 0.26556 AU at eclipses. The opposite sign reverses which eclipse is long in the model at the published inclination. F4 explains why duration order is not a universal proof.
- Independently reconstructed all 400 separation-plot samples by numerical time integration and interpolation. Maximum difference 0.0000559 AU, consistent with the plot's time and radius rounding. Its convention places the primary at true anomaly `pi/2 - omega`; there is no sign-convention mismatch in the plot.

The timing-only lower bound of at least 0.15 is conservative, not a determination of e = 0.448. The quoted exact e cos(omega) adopts that published eccentricity; the revised problem 5 now correctly says so. A complete binary fit was not performed.

### 4. Lick 51 Peg velocities

CONFIRMED: independently parsed 354 velocities spanning 16.0002 years, with detector groups of 45, 129 and 180 points. Used Lomb-Scargle for the broad 1 to 10 d search, then scalar minimization and weighted normal equations. This differs from the producer's trial-frequency SVD loop.

| Fit | Period, days | K, m/s | Unweighted residual RMS, m/s |
|---|---:|---:|---:|
| Producer's stated preprocessing, independently fitted | 4.230798894 | 55.5084 | 7.7881 |
| Same preprocessing at published period | 4.2307966 | 55.5043 | 7.7870 |
| Sinusoid and detector offsets fitted jointly | 4.230797336 | 55.6075 | 7.5943 |

The lesson's 4.230799 d, 55.50 m/s and about 8 m/s agree. Independent plot phase and velocity reconstruction agree within the stored rounding: 0.000050 d and 0.00349 m/s. The retained outlier is +111.36 m/s, about +56.22 m/s above the fitted curve. Weighted residual RMS is 6.557 m/s, so the lesson's 8 m/s is the ordinary RMS, not that weighted statistic.

Joint detector-offset fitting is statistically cleaner than subtracting each detector's mean first, because the detector groups need not sample identical orbital phases. Here it changes K by only 0.103 m/s and does not invalidate the teaching result. The paper supports handling detector offsets; it does not require this exact pre-demeaning recipe.

Historical discovery, 2019 Nobel sharing, the iodine method and non-transiting status are supported by opened primary sources S4 to S8. Cont 2026 directly supplies P = 4.2307966, K = 55.77 and stellar mass 1.07. Its newer true-mass estimate is distinct from the lesson's minimum mass; there is no contradiction. Lick's actual iodine analysis uses roughly 501 to 580 nm chunks for this release, so H-alpha is a numerical illustration rather than the literal line used in the iodine fit.

### 5. Physical caveats

F1 to F4 cover the actionable qualifications. The near-equal temperatures alone do not establish exact observed depths, since limb darkening and overlapping areas matter. A uniform-disc calculation at the published inclination gives about 45.1% and 35.5%; it supports the direction of the overlap explanation but is not a replacement fit. The real TESS surface-brightness ratio remains UNCERTAIN without stellar atmosphere and limb-darkening modeling. The lesson already states its uniform-disc assumption.

Doyle 2011, pp. 4 to 5, explicitly predicts orbital-inclination variation and periods without observable transits. Kostov 2021 independently describes a roughly 44 to 54 year precession cycle for this lesson's binary system. The citation and qualitative slow-turning statement are CONFIRMED. Neither source implies that every circumbinary planet has the same timescale.

The sideways-motion sentence in 3.4 is acceptable only within the already stated first-order, low-speed approximation. A transverse relativistic shift exists at second order; at 55.5 m/s its equivalent velocity is about 0.00000514 m/s. This is an optional wording clarification, not an additional material finding. The proposed explanation of the small first planet dip through limb darkening remains explicitly untested in the lesson; I did not promote it to a measured cause.

### 6. Fence and identifier audit

CONFIRMED for the four requested lesson sources and all five directly referenced JSON payloads: zero Fence A or B matches. Explicit target fields, textual target labels, and long integer tokens in JSON were checked. The only explicit TIC identifier is the authorized published binary; 51 Peg's HD designation is a published source label. No new identifier was written into the scripts or this report.

All five JSON files have equal-length, finite, sorted coordinate arrays: 33, 64, 354, 944 and 400 points respectively. This is a content check, not a browser/rendering check. The two older planet-transit JSON files contain published-system absolute timestamps; they are not sealed-target leaks. They were not regenerated or remeasured from sector 21 in this brief.

## Primary-source ledger

Short quotations below are evidence locators. Interpretations and computations are distinguished above.

| Source | Exact short text or equation locator | Claim and decision |
|---|---|---|
| S1: [Winn, Transits and Occultations, full textbook chapter](https://arxiv.org/html/1001.2010v5) | Equation 33: first-order timing; equations 5 to 8: projected separation; section 2.3: duration contacts. Text: "To first order in e". | Confirms timing approximation and supports F2/F4 qualifications. |
| S2: [Doyle et al. 2011, paper record](https://arxiv.org/abs/1109.3432); full paper downloaded and text inspected | PDF p. 3: "constrain the mass of the third body by fitting the eclipse data". Pages 4 to 5: inclination evolution and disappearing transits. | Supports F1 and the precession citation. Original paper, not a later summary. |
| S3: [Kostov et al. 2021, full paper](https://arxiv.org/html/2105.08614v2) | Section IV.3: "its mass is measurable by the pattern it produces in the ETVs". Tables 5/6: inclination and omega; section IV.4: precession. | Published parameters support the conditional geometry; timing can constrain mass. |
| S4: [Fischer et al., The Twenty-Five Year Lick Planet Search](https://arxiv.org/html/1310.7315v1) | Section II.1: "imprinting thousands of narrow iodine absorption lines"; III.5 discusses detector offsets. | Confirms the method and the need to handle changing zero points. |
| S5: [Royal Swedish Academy, 2019 award announcement](https://www.kva.se/en/news/nobelpriset-i-fysik-2019-2/) | "the other half jointly to Michel Mayor"; announcement names Queloz as co-recipient. | Confirms the half-prize sharing, Sun-like-star discovery and Haute-Provence account. |
| S6: [NASA/JPL interviews with the Lick confirmers](https://science.nasa.gov/universe/exoplanets/exoplanets-2020-looking-back-to-the-future/) | "The groundbreaking discovery had been announced less than a week earlier". | First-person recollections support prompt Lick confirmation; no correction to "within weeks". |
| S7: [Birkby et al. 2017, full paper](https://arxiv.org/html/1701.07257v1) | Section III.2.1: "There are no transit events within the scatter of the data". | Direct photometric support for no observed transit. |
| S8: [Cont et al. 2026, full paper](https://arxiv.org/html/2605.23582v1) | Abstract: "non-transiting hot Jupiter"; Table 2 gives P and K. | Current confirmation of non-transiting status and the cited numerical reference. |
| S9: [NASA TESS telescope information](https://heasarc.gsfc.nasa.gov/docs/tess/telescope_information.html) | "The TESS detector bandpass spans from 600 - 1000 nm". | Supports F3: total emitted power and detector-band light differ. |

Also opened the NASA Exoplanet Archive overview and the University of Geneva's 2019 announcement. The Nature discovery page and NobelPrize.org pages/PDF returned access errors; the archive, discoverers' institution, awarding academy and firsthand confirmation account supplied accessible primary evidence. No conclusion depends only on a search summary.

## Reproduction and outputs

Run from this worktree, one worker:

```powershell
node research/astra/scripts/check_034b_grader.cjs
& D:/second-sun/.venv/Scripts/python.exe research/astra/scripts/check_034b.py
& D:/second-sun/.venv/Scripts/python.exe research/astra/scripts/sources_034b.py
```

All three final commands completed with exit code 0. The science script sets NUMBA_NUM_THREADS, OPENBLAS_NUM_THREADS and OMP_NUM_THREADS to 1 in its own process, not persistent machine settings. No heavy background run was launched. Every script prints its effective worktree and output paths.

Final static checks: both Python files parsed with `ast.parse`; Node `--check` accepted the grader harness; report structure and dash scan passed; saved grader and all nine lesson/payload fence rows passed consistency assertions. `git diff --check` found no tracked whitespace errors. Read-only status showed only USAGE.md plus this report and three new audit scripts, alongside the pre-existing runner lock. No book or frozen-code modification appeared. Git's whitespace check does not cover untracked files.

Evidence is under `data/astra/034b/`: `grader.json`, `fence.json`, `eclipses.json`, `geometry.json`, `rv.json`, `caveats_payloads.json`, and `sources/downloads.json`. The download is the Doyle PDF from `https://arxiv.org/pdf/1109.3432`, 334,033 bytes, stored at `sources/doyle2011.pdf`; extracted UTF-8 text is adjacent. The brief's data-only-under-034b instruction takes precedence over the general downloads-folder default.

Initial harness errors were corrected and rerun: unavailable pypdf was replaced with the already installed pdftotext executable; its output encoding was made explicitly UTF-8; NumPy lacked `trapezoid`, so the already installed SciPy implementation was used. Nothing installed or changed in the venv. The failed Nobel download produced no saved PDF. No plot or pipeline script was run as-is.

## What I did NOT check

- No browser interaction, book build, mobile layout, storage behavior, accessibility or live-site check. Only the extracted comparison logic was executed, not the complete DOM submit handler.
- No new planet search, injection campaign, frozen-filter edit, sealed-run interpretation or independent reviewer. My independently written calculations are independent of the producer's implementation, not an independent human/model review of my own work.
- No full photodynamical, stellar-atmosphere or limb-darkening fit; no new confidence intervals, robust RV planet-model selection or red-noise analysis. The textbook examples do not require those to identify the qualifications above.
- No raw sector-21 transit remeasurement. Its two published payloads were checked for identifiers and structural validity; the brief requested raw eclipse measurements in sectors 44 to 47.
- The source PDFs were inspected by text extraction for scientific statements, not visually audited for page layout.

## STOP SIGNS hit

No scientific fence or frozen-code stop. The missing optional PDF Python dependency stopped that implementation path; an installed reader completed the same task without installing anything. Website access failures were resolved through alternate primary sources. Initial read-only git status emitted a permission warning for the global-ignore path; no contents were obtained or changed there. No git-writing command was attempted.

## QUEUE PROPOSALS

FIX, node 4.1: F1 to F5, with the severities and scope in the table. Claude should review and apply them together with their corresponding answer/hint changes if the physical example is changed. The present audit is complete; the book is still read-only and not certified fixed. Queue files were not edited.

## IDEAS

None beyond the requested audit. Joint RV offsets are recorded as a method comparison, not a request for a new fitting project.

## Disagreements with Claude

F1 and F2 dispute unconditional teaching statements; F4 disputes the sufficiency of the general duration-sign argument, not this system's inferred sign. Evidence is above. No decision or source was silently changed; Claude reviews the proposals and Ahmed decides any unresolved disagreement.

## Questions for Ahmed

None. The work was authorized and no new direction decision is needed.

## Usage

Prediction: 45 five-hour / 8 weekly points. Initial meter 2% / 31%; close-out reading at 23:23 Kuwait was 47% / 38%, approximately +45 / +7 rounded account-wide points, excluding initial instruction reads and final bookkeeping. Weekly actual/predicted ratio is about 0.88. Final measured row is appended to `research/astra/USAGE.md`. Lesson: reproduce a measurement's definition before treating a small numerical difference as a physical error; use a geometry counterexample to test whether a teaching rule is generally valid.

Next: Claude reviews these five proposed corrections before changing the lessons or clearing their pending labels; review cost is not measured here, and no additional Ahmed approval is needed for that review.
