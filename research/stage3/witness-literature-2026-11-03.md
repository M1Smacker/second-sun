# Witness research, RS-003 (3 Nov 2026, Sonnet 5.5 Extra, cap 1.5 weekly points)

Method: `research/RESEARCH-BLUEPRINT.md`. Brief: `NEW-SYSTEMS-RESEARCH-BRIEF-2026-11-02.md` section 3 (W1 to W12). Script and aggregate outputs: `research/stage3/witness-research/` (no star IDs in the outputs). Nothing in the pipeline, the frozen files or the book was changed. Labels as in `vigil-literature-2026-11-03.md`.

## 0. Plain verdict: Witness is NO-GO for now (it narrowly fails its own kill rule)

The kill rule was written inside the script's docstring before the first run (W10). Applied as written, Witness is killed:
- **Rule (a):** among upside-down control events that survive Vesper's flags (tier 1), pooled G1 and G2 development, the share whose housekeeping channels show an unusual excursion (p < 0.05) must beat the 5% chance level with a one-sided binomial p below 0.01. **Result: 6 of 40 (15%), p = 0.0139. Not below 0.01, so the rule says kill.** The miss is narrow and the sample is small (power to see a true 15% share with 40 events is only 57%), so it is "not shown", not "shown false".
- **Rule (b):** half or more of the TOI-1338 b transits with a SPOC file show a channel excursion. **Result: 2 of 9 (22%). Not triggered.** But 22% is the same as, or higher than, the 15% of the false alarms (Fisher exact p = 0.63): the channels flag real transits as readily as false alarms, which is the failure Hveto's safety test exists to catch.
- **Why it would not pay even if alive:** the strong coincidences (45% of tier 2 and 3 control events) are the events the existing flags already catch (momentum dumps, gap edges, steps, ramps). Among the tier-1 survivors a perfect veto could remove at most about 15% of false alarms, while vetoing about 22% of real transits.
- **Reopen condition:** when Vigil has produced 150 or more tier-1 control events (they arrive free, sector by sector) and at least 3 known circumbinary planets can be tested for safety. Until then nothing is built. Cost saved: about 3 to 4 points of build.

## 1. W1 [P1] Own-data kill test: answered, CONFIRMED

`w1_channel_coincidence.py`, output `w1_results_aggregates.txt`. Control events with a SPOC 2-minute file, SNR 7 or more, SPOC and SPOC-SAP duplicates removed. Statistic: five channels (SAP_BKG, POS_CORR1, POS_CORR2, MOM_CENTR1, MOM_CENTR2), good-quality cadences, 30-minute bins, 1 day running median removed; event value = mean inside the box; null = 40 random windows of the same length in the same file; statistic = maximum over the five channels of |z|, p by rank (the maximum over channels already pays for the channel trials).

| Group | n | p < 0.05 | share | one-sided binomial p |
|---|---|---|---|---|
| G1, upside-down, tier 1 | 10 | 0 | 0% | 1 |
| G2 development, upside-down, tier 1 | 30 | 6 | 20% | 0.0033 |
| **Pooled upside-down, tier 1** | **40** | **6** | **15%** | **0.0139** |
| Upside-down, tier 2 or 3 (both sets) | 1,467 | 670 | 46% | below 1e-200 |
| Real, tier 1 (G1, G2 dev) | 13, 89 | 2, 8 | 15%, 9% | 0.135, 0.077 |
| TOI-1338 b transits (W6) | 9 | 2 | 22% | 0.071 |

The G1 control sample is 32 tier-1 events by the scorecard definition, 10 with a usable SPOC file; G2 development 25 events, 30 with SPOC duplicates counted by product. Pre-condition of the brief (about 30 control events) is met when pooled.

## 2. W2 [P1] Is it just standard decorrelation? Answered, LIKELY (search summaries; abstracts not opened)

Standard practice corrects the flux using pointing: [Vanderburg and Johnson 2014, arXiv:1408.3853](https://arxiv.org/abs/1408.3853) (K2SFF, flux against centroid motion), [Luger et al. 2016, arXiv:1607.00524](https://arxiv.org/abs/1607.00524) (EVEREST, pixel-level decorrelation), and Kepler/TESS data validation runs per-candidate centroid and difference-image tests ([Twicken et al. 2018, arXiv:1803.04526](https://arxiv.org/abs/1803.04526)). TESS PDCSAP already removes common systematics with cotrending basis vectors, and Vesper's `gap_dump`, `step` and `ramp` flags already act as crude veto channels at dumps and gaps (the 46% of tier 2 and 3 events above). Hveto differs in kind: it removes events, not trends, and ranks channels by coincidence significance. Verdict: the idea is not a duplicate of regression, but the part it could add (tier-1 survivors) is small (section 1).

## 3. W3 [P1] Hveto itself: answered, CONFIRMED (ar5iv text of arXiv:1107.2948 read)

[Smith et al. 2011](https://arxiv.org/abs/1107.2948). Channels with negligible sensitivity to the signal are ranked by how unlikely the number of coincidences between triggers in the main output and triggers in the auxiliary channel is, by Poisson statistics; the method is hierarchical (take the best veto, remove its triggers, repeat) until the significance falls under a threshold. Utility is judged by efficiency (percent of noise transients vetoed) divided by deadtime (percent of analysis time removed): "if the ratio is close to one, the veto performs no better than time removed at random"; a second indicator is the use percentage. Settings come from a configuration file: SNR thresholds, a list of coincidence time windows, a stopping significance. **Safety:** hardware injections are compared with auxiliary-channel triggers; "for a channel to be considered safe, it should not respond to hardware injections". Our analogue of a hardware injection is a real known planet, not a planted dip (planted dips are added to the flux only and are safe by construction, a trap). Our numbers in this vocabulary: efficiency 15% at deadtime 5% gives a ratio of 3 on false alarms and 4 on the real planet, so no separation.

## 4. W4, W5 [P2] Channels per product and their meaning: answered, CONFIRMED (one star's files and FITS headers)

SPOC 2-minute file: SAP_BKG ("aperture phot. background flux", e-/s), POS_CORR1 and POS_CORR2 ("column / row position correction", pixels), MOM_CENTR1 and MOM_CENTR2 ("moment-derived column / row centroid", pixels), PSF_CENTR1 and 2, QUALITY. TESS-SPOC full-frame file: SAP_BKG, PSF_CENTR and the same family (list seen to PSF_CENTR1). **QLP file: only SAP_X, SAP_Y (position), SAP_BKG, QUALITY, ORBITID**, so QLP has no POS_CORR or MOM_CENTR and any veto would be SPOC-only, which is the thin product (about 1.1% to 1.7% of our stars per sector lately, see RS-001).

## 5. W6 [P1] Do real transits move the channels? Answered, CONFIRMED on n = 9, thin

Updated TOI-1338 b transit times (published epochs plus the shifts in section E of the sealed scorecard) in 9 sectors that have a SPOC file: 2 show p < 0.05, both in the pointing channels (POS_CORR and MOM_CENTR), one also in SAP_BKG. Only one known planet; a veto would need several. Planted dips remain the wrong safety test.

## 6. W7 to W12

- **W7 partly, reasoning (UNCERTAIN):** the tier 2 and 3 coincidences are pointing and background events at momentum dumps and gap edges, which the flags already see. No pictures of the 6 tier-1 coincidences were looked at.
- **W8 answered:** trials are paid by the maximum over five channels with a per-file null; a real build would also pay for thresholds and windows and train on development data only, testing on Vigil's future sectors.
- **W9 answered:** at p < 0.05 the deadtime is 5% by construction (random windows in the same file); efficiency 15% on false alarms, 22% on the real planet.
- **W10 answered:** the kill rule was written before the run and applied as written (section 0).
- **W11 answered, reasoning:** any Witness veto is a new switch, forces a new Vigil line, and is not allowed inside the frozen 0.8.0 or the 0.9 plan; it could only be used as an analysis beside a run.
- **W12 answered, rough:** about 3,400 events with 40 null windows each ran in a few minutes on a laptop, so reading channels is cheap; caching them in the Loom is not needed.

## 7. What changes in the plan

1. T121 Witness: NO-GO for now; reopen when Vigil has 150 or more tier-1 control events and at least 3 known circumbinary planets can test safety.
2. The existing flags are the useful part of the idea: no new work.
3. Evidence ladder: this was an E2 check (a control that could have failed, and it nearly did); the verdict does not rest on my reasoning alone.

## 8. Not done

No pictures of the coincident tier-1 events; the three standard-decorrelation papers were not opened (IDs seen in search results); channels of TESS-SPOC files not scanned for all-NaN columns; QUALITY bits not decomposed.
