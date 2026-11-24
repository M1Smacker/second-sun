# 034 lesson fact-check, AS-034 (Codex, 23 Nov 2026, 11:45 Kuwait)

**Model:** Runtime model and effort independently unverified; brief specifies neither.
**Plain verdict:** 5 confirmed teaching/physics issues need a fix. PARTIAL: raw-data checks, grading checks and most source checks remain unfinished.
**Branch:** `astra/034-factcheck-3-4-4-1`, unchanged. No git writes or commits. Book left unchanged.
**Tree:** Node 4.1 for every finding below.
**Decision:** Which statements Claude should correct before removing the four lessons' fact-check-pending labels.
**Budget:** Predicted 8 five-hour points / 2 weekly points from the first meter reading; research cap 4 web calls. Used 2 web calls. First observed meter 71% / 29%; pre-report meter 78% / 30%. Stop near 80% required by AGENTS.md section 7. This is a bounded first pass, not a completed research stint.

## Findings

Line numbers refer to the unchanged lesson sources under `book/docs/learn/`. All five findings are **CONFIRMED** within the stated mathematical models, not measurements of the real system. Evidence is the independently written and executed `research/astra/scripts/check_034.py`; machine output is `data/astra/034/arithmetic.json`.

| Lesson, line | What is wrong | Evidence | Suggested fix | Severity |
|---|---|---|---|---|
| 4.2 `u4/l2-how-two-stars-orbit.md`:23, also 17, 43, 54 | Calls the semi-major axis the stars' average distance without defining the average. It is not the time average. | Integrating radius over time gives 0.211169 AU, versus semi-major axis 0.191918 AU. Ratio is 1 + e squared / 2 = 1.100307. | Define a as half the long axis, or the mean of nearest and farthest separations. Use semi-major axis throughout the mass-share explanation. | Medium |
| 4.2 `u4/l2-how-two-stars-orbit.md`:72 | Calls 2 pi a / P the average relative speed of this eccentric orbit. This uses a circle's circumference. | Independent ellipse-perimeter quadrature gives time-average relative speed 100.664 km/s; 2 pi a / P gives 106.210 km/s. | Call 106 km/s the circular-orbit speed scale. If retaining an actual mean speed, use approximately 101 km/s and explain circumference divided by period. | Medium |
| 4.4 `u4/l4-planets-around-two-suns.md`:30 | The transit-duration denominator is a signed difference, so the equation can give a negative duration. It also needs projected motion across the sky. | In the stated one-dimensional approximation, a star moving at +60 km/s and planet at +49 gives negative duration with the displayed formula. A speed is the magnitude of relative velocity. | Use T approximately chord divided by the magnitude of projected relative velocity. Say the scalar absolute difference assumes collinear, approximately constant velocities. | Medium |
| 4.4 `u4/l4-planets-around-two-suns.md`:63 | The conditional central-crossing explanation says star 1 moves almost with the planet, but its own numbers imply the opposite sign under its overtaking model. | Script: planet 49.0109 km/s; first central point-planet crossing requires 55.7444 km/s relative speed. Hence star 1 = 49.0109 - 55.7444 = -6.7336 km/s. The other scalar branch is +104.7553 km/s, outside the lesson's quoted stellar-speed range. Star 2 is -29.2772 km/s on the overtaking branch. | Remove the claim that star 1 moves with the planet. Under this simplified central-crossing model both stars move against it, the first more slowly. Do not claim actual directions without projected orbit geometry and chords. | Medium |
| 4.1 `u4/l1-eclipsing-binaries.md`:137 | Problem 5 gives only another pair's secondary phase, then calls 0.15 its exact answer. That value also assumes this system's published e; it does not follow from the new pair's timing alone. | Areal-law quadrature, independent of the producer's anomaly conversion: quoted phase 0.604278 with e = 0.4479 gives omega 70.549 degrees and e cos omega = 0.149150. The identical phase with omega = 0 is produced by e = 0.164545. Thus identical timing does not fix exact e cos omega. | End the solution at the first-order 0.163 estimate. Alternatively explicitly return to the observed system and state the adopted e = 0.4479. | Medium |

The useful distinction is between a model's scale and a measured or averaged quantity: a and 2 pi a / P are valid orbital scales, but labeling them time averages changes their meaning. Similarly, a result conditional on an assumed eccentricity is not an inference from timing alone.

## Checks actually performed

**Runtime, independent arithmetic and ideal geometry:** Executed the script with the approved interpreter:

```powershell
& D:/second-sun/.venv/Scripts/python.exe research/astra/scripts/check_034.py
```

It prints effective paths before work, imports no project pipeline or plot script, and writes only under `data/astra/034/`. Exit code 0. Five mathematical sanity assertions completed: circular timing, analytic time-mean radius, both timing solutions, and the first-star sign. These validate this calculation, not the producer or a real-data fit. No mutation test or independent reviewer was used.

Selected results agreeing with the lessons' rounded arithmetic:

| Calculation | Independent result |
|---|---:|
| Doppler shift at 15 km/s | 0.0328368 nm |
| Worked blueshift velocity | -5.99584 km/s |
| Half-done Doppler speed | 899.377 m/s |
| Jupiter-driven solar speed | 12.5 m/s |
| Earth-driven solar speed | 0.0894294 m/s |
| Line shift at 55.5 m/s | 0.000121496 nm |
| Circular, low-planet-mass minimum mass | 0.462047 Jupiter masses |
| Fully hidden second-star light, stated luminosities | 46.2791% |
| 80% of first-star disc, stated uniform model | 42.9767% |
| Temperature fourth-power ratio | 1.04555 |
| First-order timing expression, quoted separation | 0.163799 |
| Nearest / farthest separation | 0.105958 / 0.277878 AU |
| Barycentric semi-major axes from rounded inputs | 0.0945641 / 0.0974359 AU |
| Near/far speed ratio from rounded distances | 2.62264 |
| Apastron speed from supplied 172 km/s | 65.5827 km/s |
| Planet speed in circular example | 49.0109 km/s |
| Two central, point-planet chord/time estimates | 55.7444 / 78.2881 km/s |
| Uniform-disc dilution exercise | 2974.24 ppm |
| Dip separation / binary period | 0.249237 |

These calculations use the lesson inputs. They do not establish those inputs from observations, and are not a check of every number or grading tolerance. The 0.149 result is independently re-derived only conditional on the quoted eclipse separation and published eccentricity. It does not verify the omega sign argument from the observed durations.

**Static:** Read all four lessons, both Unit 4 plot scripts, and the first 100 lines of the Doppler plot script. Located the grader's tolerance initialization in `book/docs/assets/learn.js:152`, but did not test grading. Script scanned all four lessons: zero en/em dash characters. Source lists are present in all four. `rg` was unavailable; used PowerShell searches. Initial git read-only status showed `.codex_run.lock` as an existing untracked runner file, left untouched.

**Primary source:** Opened the [Kostov et al. abstract](https://arxiv.org/abs/2105.08614) and [full HTML, section II.1](https://arxiv.org/html/2105.08614v2). The latter reports durations of "approximately" 0.4 and 0.27 days (rendered with mathematical approximation signs), consistent with the lesson's inputs; the abstract supports the approximate period range and planet radius. Source checks establish the provenance of these approximate inputs, not the lesson's inferred stellar directions. No files downloaded.

## What I did NOT check

The following remain required before this brief is complete:

1. Refit the 354 Lick velocities independently: count, span, dewar handling, period, amplitude, residual scatter, outlier and phase convention. Verify archive values, non-transiting status, iodine method, historical discovery and Nobel claims against primary sources.
2. Check the published-system identifiers against fences before any raw-light access. Then independently measure eclipse depths, centres, separation and half-depth widths from the four permitted sectors. No raw-light or target-list data were read in this pass.
3. Verify the first-order timing formula and inclination correction in a primary/textbook source, then evaluate the actual system. Test the duration-based omega sign argument including impact parameters, limb darkening and the separation plot convention. No claim here confirms that argument.
4. Complete all numerical statements, hints, answer variants and tolerances against actual grading behavior. Test correct answers and common wrong answers. Review finite planet radius and contact definitions in the claimed maximum transit speeds.
5. Finish physical caveats: TESS-band flux versus bolometric luminosity, temperature/overlap explanation, photometric mass constraints versus mandatory spectroscopy, transverse Doppler wording, and Doyle et al. citation and precession claims. These are review questions, not confirmed additional findings.
6. Complete fence/identifier audit of lessons and their plot payloads, plus final review of any later evidence. No book build, browser test, plot regeneration, pipeline run, frozen-code edit or live-site visit performed.

## STOP SIGNS hit

Usage stop: first observed meter was already 71% five-hour after initial instruction reads; reached 78% before writing this report. AGENTS.md section 7 requires stopping near 80%. Safe checkpoint only from this point. The brief stays PARTIAL. The serious research stint's full depth and duration requirement was not met before this stop.

No scientific fence was crossed and no raw target light was opened. Git read-only status emitted permission warnings for an external global-ignore path; no file contents were obtained or changed there. No write authorization was requested or bypassed.

## QUEUE PROPOSALS

FIX, node 4.1: the five rows above, after Claude reviews the derivations. Keep the fact-check-pending labels until the remaining checks are complete. Do not file the untested questions as confirmed bugs. No queue files edited.

## IDEAS

None beyond the requested audit.

## Disagreements with Claude

The five rows are evidence-backed corrections to the lesson explanations. No lesson was silently changed; Claude reviews them under the two-key protocol.

## Questions for Ahmed

None. The scope is clear; remaining work needs a fresh usage window.

## Usage

Prediction logged before lesson review: 8 five-hour / 2 weekly points. First observed 71% / 29%; pre-report 78% / 30%, approximately +7 / +1 rounded account-wide points, excluding initial instruction reads. Final meter is appended to `research/astra/USAGE.md`. Lesson: check the meter before lengthy instruction batches, and do not turn a bounded arithmetic pass into a claim of full scientific verification.

Next: Codex resumes the six remaining check groups after the usage reset, to finish the fact-check; new usage estimate required at resumption, no new scope approval needed.
