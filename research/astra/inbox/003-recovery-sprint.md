# Brief 003: how much does the whole chain really find? (T156, with T158 on the same planted planets)

**From:** Claude Code (first key), 13 Nov 2026, Kuwait 16:42. Ahmed said go the same day.
**Branch:** `astra/003-recovery-sprint` (already made from main in your folder). **Writes allowed:** `research/astra/reports/003-*.md`, `research/astra/scripts/003_*.py`, `research/astra/scripts/harness/` (only to add what you need; note every change), `data\astra\003\`, `research/astra/USAGE.md`. Read-only on every frozen file, every preregistration and every filed result.
**Stars allowed:** only the 704 `design_seen == 1` rows of `targets/r1_targets.csv`, synthetic light, and the published systems. Fence A (G1) and fence B (803 hold-out) exactly as in AGENTS.md. Machine inputs (burst table, reference SPOC files, manifests) as in rule 2. Your brief 002 harness and guard are the starting point: reuse them.
**Read first:** `research/stage3/G1-RECOVERY-BAR.md`. It was written before you start and says what each result makes us do. **Do not look at it as a target**: you measure, it decides.

## Run mode (same as brief 002)
Do the whole brief in ONE working session. Commit after each part and keep going; do not stop for a checkpoint. Stop early ONLY for: the total cap; a failed zero-injection identity; anything that would read fenced light or events; a possible planet; the five-hour bar near 90% (write where you stopped at the top of the report so "continue" resumes exactly there). Everything else goes in the report and you carry on.
**Budget:** total **25 weekly points** of Ahmed's Codex bar (part 1: 18, part 2: 5, report: 2). Predict before each part in USAGE.md, write the actual after. **Model:** Astra High for design and judgement, Sol for running and bookkeeping (Ahmed sets it in the app; if you are on another one, say so and carry on).
**Machine:** machine time is free; Ahmed's rule is up to 70% CPU when he is away. Cap Numba threads (`NUMBA_NUM_THREADS`) so workers times threads is at most 8 of his 12 cores. Long runs go in the background with a progress file in `data\astra\003\` (trials done, trials planned, last update time); Claude reads that file to show the progress bar on the book.

## Your core mission (Ahmed's words still rule: find bugs, improve the filter, raise our chances)
Measure, with enough trials to be a rate, how often a real circumbinary transit in our data reaches tier 1, and **where the rest are lost**. Every stage that loses planets is a candidate improvement; report it with its size. Report every bug you meet, as in brief 002.

## Part 1: T156, the unconditional recovery sprint (cap 18)
**Design (write it into the report and commit BEFORE the first real trial; it may not change after you see recovery numbers):**
- **Where:** a random draw of design-seen groups (star and sector), seed written down, stratified so each of the five binary-period bins (5 to 10, 10 to 14, 14 to 20, 20 to 27.4, over 27.4 days) gets the same number of trials. Use the same "best product" rule the search used, and also record the product.
- **When:** the transit centre is uniform over the WHOLE sector span of the raw loaded file (first to last time stamp), before windows, eclipse mask and detrending. Trials that land in a gap, outside every window or in a file with no safe windows stay in the denominator.
- **What:** one trapezoid transit per trial (ingress plus egress 20% of the duration), injected into the raw loaded flux exactly where your pilot did (`S2.load` wrapper). Depth log-uniform 1,000 to 10,000 ppm; duration log-uniform 3 to 18 hours. Check that this range covers the published circumbinary planets' depths and durations (NASA Exoplanet Archive table, one line per planet with the exact link), and say so; do not change the range after the first trial.
- **Controls, same draws:** (a) the same trial with the sign flipped (a bump) run through the upside-down arm, to test the two arms treat it the same; (b) zero injection on every drawn group, which must give exactly the stored events (zero-difference identity); a mismatch is a stop.
- **Size:** first time 20 trials and write the seconds per trial. Then plan the full run to fit the cap and the machine: aim for at least 2,000 trials (at least 400 per period bin) plus their bump controls. If that cannot fit, say what fits and why, and run that.
- **Outcome per trial:** furthest stage reached, in order: file has safe windows; centre inside a searched window; survives the eclipse mask (enough in-transit points kept); event found at any tier within half the duration of the true centre; tier 1 (1A, 1L or 1B) at SNR at least 7. A trial counts as recovered only at the last step.

**Report (bins only, never a star id, time or depth of a real event):**
1. R as defined in `G1-RECOVERY-BAR.md`, with its star-clustered bootstrap 95% interval, and R per period bin, per product and per sector era (before 56, 56 to 93, 94 on).
2. A loss table: share of all trials lost at each stage, per period bin.
3. Recovery against depth and duration (a table of cells, each with its count; and a smooth curve if you like, labelled as a fit).
4. Dip versus bump recovery per bin with a test; any difference outside counting error is a bug.
5. The stage with the largest loss, why it loses (read the code: file and line), and one to three concrete changes for a future Petrova version, each with what it would gain on these same trials (if you can rerun cheaply on harness copies, do it and label it a design study; never edit the frozen files).
6. A comparison with every earlier recovery number in the project that was measured after the mask or windows (find them in `research/stage3/` and RESUME.md), saying which ones the new number replaces.

## Part 2: T158, other teams' methods on the same planted planets (cap 5)
- Read STANLEY (Martin and Fabrycky, arXiv 2101.03186) and mono-cbp (Davies et al., arXiv 2604.09435) through their abstract and HTML pages; pull the exact sentences on how each finds a transit and detrends. Find whether their code is public and under which licence.
- **No installs.** Using only the venv we have: build the smallest fair version of mono-cbp's multi-window detrending idea you can (a harness copy or a new `003_*.py`), and run it on the Part 1 trials that were lost at the detrending or window stage. Report how many it would recover, labelled as a design study.
- For STANLEY: a one-page feasibility note only (what data and runtime a restricted stack over our multi-sector stars would need, and on how many design-seen stars it could run). No build.

## Stop signs
As AGENTS.md and the auditor skill, plus: you are about to change the trial design after seeing a recovery number; the zero-injection identity fails; anything looks like a possible planet (write nothing about it outside `data\astra\003\`, claim nothing, tell Claude).

## Report
`reports/003-recovery-sprint.md` in the mailbox format. Top: the plain verdict line (for example "R = x [a, b]: the chain finds about one in N reference planets"), then **Bugs found**, then parts 1 and 2 with labels CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED and file and line for every code claim. Close with **"What I would do next and why"**, given the bar in `G1-RECOVERY-BAR.md`. Your final message to Ahmed: the verdict line, the bugs, and the next step, in a few short lines.
