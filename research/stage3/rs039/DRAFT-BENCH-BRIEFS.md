# RS-039 Part C: draft bench briefs (DRAFTS ONLY; nothing runs without Ahmed's go; Codex numbers 030 on)

Each brief follows the F1 freeze-test style: rules written before any result, the paired bench on the 968 possible planets, the fresh bench for confirmation, and both false-alarm meters.

## Brief W: the witness-star meter (build first; it judges everything after)
**Why:** our only false-alarm meter, the upside-down copy, cannot see dips that have no mirror (thruster wobble, scattered light, eclipse leftovers). That blindness is why rule 4 had to block DS, M2 and R2, and why any new detrend or tier rule will be hard to judge. Kepler DR25 used a second meter (scrambled light plus Skye) for the same reason; Planet Hunters TESS and mono-cbp used cross-star coincidence on TESS.
**What:** for every sector and CCD in our G2 and G3 lists, take N random non-target stars of similar brightness (QLP and TESS-SPOC light curves; N about 100 to 300, priced first), run the exact frozen search on them (both arms), and keep their event times.
**Outputs:** (1) a per-sector, per-CCD artefact-time map: 1-day bins (Skye) and finer 0.1 d bins, with an excess threshold fixed on half of the sectors and checked on the other half; (2) the dip-only artefact rate, measured directly: real-arm minus upside-down-arm events on witness stars, per 100 days, by time from momentum dump and from gap edge; (3) a third count for every bench run: target-star real events that coincide with a witness pile-up.
**Pass rule (written first):** the map must flag at least half of the real-arm-only excess near dumps on witness stars, while flagging at most 3% of planted crossings on the planet bench.
**Cost:** a download (size to be priced and told to Ahmed), machine hours, about 3 to 5 Codex points.

## Brief N: a statistic that never puts the dip in its own baseline
**Why:** the red factor is 3 for weak crossings and the frozen detrend keeps 0.74 of their depth (RS-039 A2). The white-noise and full-depth ceiling is 84 against 64.7 today (A1). c1a (3 x box window) got the detections but lost them to the mirror flag because short windows carve side bumps.
**What:** depends on RS-039 A6 and A8 results (filled after they end). Candidates: (a) notch-style flank statistic; (b) STANLEY-style per-star window chosen by a whiteness test; (c) Oddo-style window per box length; each with the mirror flag re-specified for that statistic (match only bumps at the same time, not on the flanks).
**Pass rule (written first):** at an equal alarm budget on BOTH meters (upside-down at most 79, witness-coincident and real alarms at most B's), a paired gain of at least +2.0 on the fresh bench with the interval above zero; zero-planet identity on untouched light where the switch is off; T156 R not below B.

## Brief S: one calibrated score instead of the hard holds
**Why:** 16.7 points of possible planets are detected and then held (A3). DR25 ranked by one disposition score and chose the cut on the completeness/reliability curve; Foreman-Mackey 2016 used model comparison for single events.
**What:** event features already in our groups files (shape against step and ramp models, flank lift, coverage, dump and gap distance, mirror match, repeat, eclipse distance) plus witness coincidence (Brief W); a simple, inspectable model (logistic or a small tree), trained on half the design planets (positives) against BOTH meters' events (negatives), threshold set on that half at a fixed alarm budget, judged on the other half and the fresh bench.
**Pass rule (written first):** as Brief N, plus: no single feature may carry more than half the score's weight (guards against one flag sneaking back).
**Risk:** a learned score can learn the bench, not the sky. Guard: positives only from planted planets, negatives only from the two meters, never real-arm events of target stars.

## The scoreboard upgrade (small, first)
Every bench run reports, besides P: per-crossing tier-1 rate (A7), alarms at thresholds 7, 7.5, 8, 8.5, 9, 10 on both arms, and the witness-coincident count. Freeze decisions then compare recipes at equal alarms, not at one fixed threshold.
