# Second Sun audit: VarWISE, VARnet, mono-cbp and a faster circumbinary-planet search (28 Oct 2026)

Independent research audit, read-only on the detector. Passes 1 and 2 notes with sources are in `audit-2026-10-28-varwise-mono-cbp.md`. Labels: VERIFIED (read in a source or recomputed here), LIKELY (reasoned or read through a summary), UNCERTAIN, NOT TESTED. Nothing here is a planet claim.

## 1. Executive recommendation
**Do not build a VarWISE-style machine-learning detection engine now. Improve our own pipeline (option A) and use mono-cbp as a small, bounded yardstick (option B-lite).**

Why, in four lines:
1. VarWISE is not a planet search. It is an infrared, six-month-cadence catalogue of 1.9 million variable objects with no transit or planet class, and VARnet was checked on 231 real objects (VERIFIED, pass 2). No evidence in it supports an ML detector for TESS circumbinary transits.
2. Speed is not our bottleneck. Our whole 549-star search takes 30 to 40 minutes of machine time (VERIFIED, our notes and ledger). What limits us is what we cannot yet measure: faint-dip recovery, long durations, and false alarms we cannot compare fairly.
3. We lack labels. We have 6 known hosts in our list and mono-cbp tested 14. A learned model would train on invented planets and inherit the lopsided noise our upside-down control already shows (LIKELY).
4. mono-cbp is open and runnable, but it shares only 30 of our 549 stars, so it can check us on a small slice, not replace us.

## 2. Source-verified findings (short; details in the pass notes)
- mono-cbp (Davies et al. 2026, arXiv:2604.09435; code github.com/bdrdavies/mono-cbp): GPL-3.0; 512 eclipsing binaries, 3,808 TESS-SPOC light curves, one unconfirmed candidate; masks eclipses before detrending, requires an event to survive many detrending windows (18 of 21), compares transit, step, sinusoid and linear shapes. VERIFIED. The repository appears to use a least-squares fit where the paper describes MCMC: LIKELY. Runtime: not reported (VERIFIED absent).
- Overlap: 30 of our 549 stars are in their 591-star table; one known host (Kepler-1647) is in both lists. VERIFIED (recomputed).
- VARnet (arXiv:2409.15499) and VarWISE (arXiv:2605.19059): see the pass 2 notes. VERIFIED: infrared NEOWISE data, epochs about six months apart, no planet class, trained on about 1.06 million synthetic curves, validated on 231 real objects, no false-alarm rate, completeness not quantified, no code release found (UNCERTAIN that none exists).
- The audit prompt had the two arXiv numbers swapped (VERIFIED).

## 3. Our pipeline today (read from `research/stage3/` and the frozen settings, hash d5767e66c4d2)
What it does: load the best of three TESS products per star-sector (QLP, SPOC, TESS-SPOC) -> flatten with a 2 day biweight -> bin to 10 minutes -> slide boxes of 3, 4, 5, 6.5, 8, 10, 12, 15 hours -> keep events at signal-to-noise 7 or more, where the noise is the measured scatter of the box statistic itself -> run the same search on upside-down copies as a control -> add flags, never deletions: data gap or dump, burst, matched upside-down, eclipse overlap (physical length or measured width), repeater (3 or more in a sector), flat-baseline step, 1 day orbit-start ramp, dominated by a stronger other-kind event -> second-product check -> tiers 1A, 1L, 1B, 2, 3 -> labels (TOI, known host, eclipsing-binary catalogue, repeater depth scatter).

Strengths (VERIFIED, our files): settings frozen under a hash before each run; regression test that reproduces Stage 2 exactly; flags are tested and mutation-tested; results judged as real minus upside-down per tier; injection harness with 1,548 injections; honest labels on every claim.

Measured state: 5,064 star-sectors searched. Raw events 604 real and 869 upside-down, which is 11.9 and 17.2 per 100 star-sectors. Tier 1: 12 real (0.24 per 100) and 33 upside-down (0.65 per 100). Real is below the control at every signal-to-noise bar. Upside-down finds 1.25 to 2.5 times more raw dips than real at every strength, so the control overstates false alarms and "real below control" says nothing either way (VERIFIED as a measurement; cause LIKELY, upward spikes).

Gaps (all from our own files):
1. Faint-dip recovery was NOT TESTED when this report was written; v5 measured it the same day (`stage3/faint_recovery_v5.txt`): an 8 h dip is found 61% at 10 x the 8 h box noise, 22% at 8 x, 2% at 6 x. Correction: the 82.7 to 86.4% above was the share of DETECTED deep (12 x) dips that survive the flags; only 72% were detected, so the chain keeps about 62% of such dips.
2. Boxes stop at 15 hours, but long circumbinary transits can be longer (LIKELY). A 20 hour grid is queued (v5).
3. More than half of all events sit at the edge of a data segment (VERIFIED: the step flag fired on 400 of 604 real events, 305 only because one side had no data). A planet near an edge cannot be verified by a flat-baseline test.
4. One sector-wide noise level cannot describe heavy tails or noise that changes along a sector (VERIFIED by reading the code, learnings section 11).
5. No pair search; no linking of single events across sectors.
6. Eclipses are handled by flags after the search, not by masking before detrending (the flag covers a median 12% of the timeline).
7. 3 of 12 tier-1 real events sit on QLP-only stars, so no second product can check them.
8. Nobody has looked at the 12 tier-1 events yet (gated behind your Eyes practice).
9. The injected shape is a fixed trapezoid; real circumbinary transits change in time and duration (LIKELY, not simulated).

## 4. Decision matrix
| | A: improve our pipeline | B-lite: mono-cbp as yardstick | C: VarWISE-inspired ML engine |
|---|---|---|---|
| What it is | v5 and later: faint-dip test, 20 h boxes, per-star false-alarm level, mask-before-detrend, multi-window check | Run mono-cbp in a separate environment on the 30 shared stars plus injections and TOI-1338; compare | Train a neural model on simulated light curves to detect dips |
| Chance to improve the science soon | High: fills measured gaps | Medium: second opinion on 30 stars, borrowed ideas | Low: no evidence it fits this job |
| Evidence it works for our job | Our own measurements | Peer-reviewed, 14 known planets, at least 50% recovered | None (VARnet validated on 231 mixed objects, 48 eclipsing binaries) |
| Cost (our ledger) | About 0.6 point per version plus 40 to 60 min machine | About 1.0 to 1.5 points in total, runtime unknown (UNCERTAIN) | Not estimated; a generator, training, validation and fixes (UNCERTAIN, much larger) |
| Main risk | Tuning on the 549 stars (we freeze before each run) | GPL (keep it outside our code), repo differs from paper, scipy conflict, tiny overlap | Learns the fakes, inherits lopsided noise, few real labels |
| Reproducible | Yes, hashed | Depends on their version | Seeds, weights and data to store |
| Learning value for Ahmed | High: each step is a book lesson | High: read a professional pipeline | Medium: harder to check himself |
| Fits the scale (549 stars) | Yes | Yes | No: VARnet's job is hundreds of millions of sources |

Verdict: **A first, B-lite alongside, C not now.** Triggers to reopen C (my judgment, LIKELY): the sample grows past tens of thousands of light curves; or we hold a few hundred human-labelled real events (your Eyes answers and reviews) to train a triage model; or the benchmark shows a recall gap that rules cannot close.

## 5. Small benchmark plan (B-lite)
Goal: a fair, cheap comparison of our frozen v4 and mono-cbp on the same light curves. Nothing tuned on results.
- **Data:** the 30 shared stars' TESS-SPOC light curves (224 files, the same product mono-cbp uses; each of the 30 also has QLP and SPOC). Add TOI-1338 to both tools (we already ran it in earlier recovery experiments).
- **Tests:**
  1. *Known planets.* Kepler-1647 and TOI-1338 first; the other four known hosts only where a transit falls inside a TESS observation (NOT TESTED; Kepler-1660 had no usable ephemeris). Sanity check, not statistics.
  2. *Injection and recovery.* Same injected files for both tools: single trapezoid dips, depth 0.1 to 1%, 3 to 20 h, middle of a segment and near a segment edge, including faint ones. Report recovery by depth, duration and position.
  3. *Negative controls.* Inverted curves, plus quiet stars. Report false alarms per 100 star-sectors for each tool, kept apart from real counts.
  4. *Agreement.* Which real events each tool finds, which both find; do not call any a candidate.
  5. *Speed and reproducibility.* Wall-clock per star-sector; run twice and compare outputs; record versions and hashes.
- **Success lines, fixed before the run:** recovery of deep dips within 10 points of each other; every difference in recovery or false alarms explained by a named design choice; no tuning of either tool afterwards.
- **Limits stated now:** 30 stars is small; the two tools define "event" differently; mono-cbp uses 30 minute binned flux and ours 10 minutes; their repository may not reproduce their paper.

## 6. Recommended architecture (keeps the current spine)
Detect -> flag -> tier -> label, with these additions, each as a flag or a measurement and never a deletion, each tested and frozen under a new hash after the Stage 2 regression is re-proved:
1. Faint-dip and edge-position recovery test (biggest open measurement).
2. Duration grid to 20 hours (a 2 day window is 2.4 times 20 h, above the 2.2 rule).
3. Mask known eclipses before detrending (idea from mono-cbp, NOT TESTED here).
4. Multi-window check: an event must survive three detrending windows (1, 2, 3 days) or it is flagged (idea from mono-cbp).
5. Shape comparison flag: transit against step, sinusoid and linear, by AIC (extends our step test).
6. Per-star bootstrap false-alarm level (Kepler style) and a report of real against upside-down divided by the measured asymmetry ratio.
7. A shared export so any outside tool can be run on exactly our files, and a one-command benchmark table.
No neural network in the detector. If C is ever reopened, use machine learning only as a triage layer over events that already passed these steps.

## 7. Learning opportunities for Ahmed
- Why detrending can eat or fake a transit, and what masking an eclipse before detrending changes (Chapters 7 and 8).
- Injection and recovery: what "completeness" means, and why deep and faint dips differ (Chapter 9).
- Why a control can be unfair (the asymmetry test) and how to correct for it.
- Licences: GPL against MIT, running a tool against copying its code.
- Reading a paper against its code, and a model against a validation set that shares its source (VARnet's 231 objects).
- Your Eyes answers are labelled human judgments, a possible future training set for triage; this is the honest path from "human" to "machine" later.

## 8. Implementation roadmap and cost (from our ledger; nothing started)
0. **Decisions from Ahmed (text):** go on A; go on B-lite including a separate mono-cbp environment (installs a GPL package outside our repo, needs his OK); pair search stays "not built" unless he says otherwise.
1. **v5 (A):** faint-dip test, 20 h boxes, per-star false-alarm level, asymmetry-corrected report. About 0.6 point plus 40 to 60 minutes of machine time.
2. **Benchmark prep:** shared export for the 30 stars and TOI-1338, injection set. About 0.3 point.
3. **B-lite run:** separate environment, run both tools, compare. About 0.5 to 0.8 point, plus mono-cbp's unknown runtime (UNCERTAIN).
4. **Borrow what works:** mask-before-detrend and multi-window as v6 flags if the benchmark supports them. About 0.6 point.
5. **Revisit C** only if a trigger in section 4 fires.
Audit cost: about 0.4 (pass 1) + 0.25 (pass 2) + 0.3 (pass 3) = roughly 1 point in total, against estimates of 0.6 to 1.5, 0.4 to 1.0 and 0.5 to 1.0 for the three passes.

## 9. Sources and uncertainties
Sources: [mono-cbp paper](https://arxiv.org/abs/2604.09435), [mono-cbp repo](https://github.com/bdrdavies/mono-cbp), [GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.html), [VARnet](https://arxiv.org/abs/2409.15499), [VarWISE](https://arxiv.org/abs/2605.19059), [IRSA VarWISE overview](https://irsa.ipac.caltech.edu/data/WISE/VarWISE/overview.html), our `research/stage3/learnings-2026-10-27.md`, `FIX-QUEUE.md`, `aggregate_v4.txt`, `SETTINGS_FROZEN.json`.
Uncertain or not done:
- mono-cbp was not installed or run; its runtime and its repo-versus-paper differences are unmeasured.
- Fetches were summarised by a small model, so exact figures should be checked against the paper tables before they are published as claims; the last 59,000 characters of the VarWISE paper were not read.
- No code release for VARnet was found; that does not prove none exists.
- The cost of option C is a judgment, not a ledger number.
- Which of our six known hosts have a transit inside TESS data is NOT TESTED.
- This audit is not a legal opinion on licences.
