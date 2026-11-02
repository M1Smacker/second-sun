# Scorecard amendments (the G2 test; dated, never edits of the rules above them)

## Amendment 2, 2 Nov 2026: "scorecard plus" (written before any further sealed-style run)

Status: in force for every run after the first sealed run (30 Oct 2026). For the first sealed run these lines are POST HOC: they were computed after the result was unblinded, and are labelled so in the output. Code: `pipeline/scorecard_plus.py`, checks: `pipeline/test_scorecard_plus.py` (17 checks, reproduce the 31 Oct numbers from the one-off research scripts, plus a mutation). Output for the first run: `research/stage3/scorecard-plus-sealed.txt`.

### What does NOT change
S1 to S8, their pass marks, `pipeline/benchmark_g2.py`, the frozen settings (Vesper 0.8.0, hash 5f73692944aa) and the preregistered S6 line (TOI-1338 b, Kostov 2020 epochs, 1 of 7 strong). The first run's preregistered S2 verdict stays "above the mark of 8 (8.76 per 1,000)".

### What is added (each its own line in the output)
- **A (T38, T39).** Star-level counts beside event counts (tier-1 real and upside-down, with the number of stars they sit on). The control's ratio per bar with a 95% star bootstrap. The expected real count, real minus expected with its interval, the one-sided 95% upper limit, the variance inflation from clustering (deff), and the **detectable excess at 80% power** (2.49 x the bootstrap sd). The ratio after dropping the 1, 5, 10 and 25 heaviest stars. Rule for wording any null from now on: "nothing seen above chance; this run could have shown N or more kept dips" (N is the detectable excess). A count of events alone never states a result.
- **B (T103).** The price of every safety check: drop one alone and count the planted dips regained (tier-1 points, both slices) against the real and upside-down events let into tier 1. Printed in every scorecard.
- **C (T105).** Efficiency: the expected tier-1 detections of one planet-bearing star over its sectors by depth and period, and the limit on (planets per binary x geometry factor). Uses a 1 solar radius host with no dilution until T107 adds real host radii.
- **D (T40, T41, T42).** (T40) A borderline reading is called BORDERLINE when the 95% interval of the S2 rate includes the mark; neither a pass nor a fail is claimed from the point value alone; the pooled 895-star rate waits for the census run (T43). (T41) A difference between slices is called better, worse or no clear difference by non-overlapping 95% intervals, never only "did not generalise". (T42) S4 shows "found at all" beside "kept" (the gap is what the safety checks cost).
- **E (T44, T102).** TOI-1338 b against the later published times (Wang and Liu 2024: observed times for sectors up to 68, a photodynamical forecast published before sectors 89 to 98 were observed), with the flags that fired on every event near each transit. Labelled post hoc for the first run; for later runs the updated times are used as given in the dated amendment that fixes them before the run.

### Honest limits (written now)
- B is leave-one-check-out: checks overlap, so the prices do not add up and two checks dropped together cost more than their sum suggests (NOT TESTED).
- C uses a 1 solar radius host, no dilution, a 26 d window per sector and a mean sector count; real host radii come with T107. It does not use the 3 hour box effect on long transits.
- The star bootstrap treats stars as independent; two sectors of one binary are not.
- Everything for the first run was computed on data that had already been unblinded. It describes that run; it is not evidence for or against a planet.
- The labels CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED in `post-sealed-literature-2026-10-31.md` still apply to the sources.
