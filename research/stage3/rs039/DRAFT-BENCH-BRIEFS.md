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
**What (filled 11:15 am from A8b to A8d):** the lower-flank notch: light detrended with a 5-day biweight (slow trends only); for every box centre and box length D, baseline = the LOWER of the two flank means (each 1.5 D wide, 0.25 D outside the box); SNR = (depth - median depth) / (1.4826 MAD of depths) per star-sector and D; threshold about 5 at equal alarms. Mirror rule re-specified: an upside-down match counts only if it overlaps the box itself (within 0.25 D). Measured on 160 design stars: +7.7 points of crossings and +11.4 points of planets detected at equal alarms on both arms; dip-against-bump gap -0.1. The bench must now measure the TIER level (our holds were tuned at SNR 7+). Candidates: (a) notch-style flank statistic; (b) STANLEY-style per-star window chosen by a whiteness test; (c) Oddo-style window per box length; each with the mirror flag re-specified for that statistic (match only bumps at the same time, not on the flanks).
**Pass rule (written first):** at an equal alarm budget on BOTH meters (upside-down at most 79, witness-coincident and real alarms at most B's), a paired gain of at least +2.0 on the fresh bench with the interval above zero; zero-planet identity on untouched light where the switch is off; T156 R not below B.

## Brief S: one calibrated score instead of the hard holds
**Why:** 16.7 points of possible planets are detected and then held (A3). DR25 ranked by one disposition score and chose the cut on the completeness/reliability curve; Foreman-Mackey 2016 used model comparison for single events.
**What:** event features already in our groups files (shape against step and ramp models, flank lift, coverage, dump and gap distance, mirror match, repeat, eclipse distance) plus witness coincidence (Brief W); a simple, inspectable model (logistic or a small tree), trained on half the design planets (positives) against BOTH meters' events (negatives), threshold set on that half at a fixed alarm budget, judged on the other half and the fresh bench.
**Pass rule (written first):** as Brief N, plus: no single feature may carry more than half the score's weight (guards against one flag sneaking back).
**Risk:** a learned score can learn the bench, not the sky. Guard: positives only from planted planets, negatives only from the two meters, never real-arm events of target stars.

## The scoreboard upgrade (small, first)
Every bench run reports, besides P: per-crossing tier-1 rate (A7), alarms at thresholds 7, 7.5, 8, 8.5, 9, 10 on both arms, and the witness-coincident count. Freeze decisions then compare recipes at equal alarms, not at one fixed threshold.

## Price of Brief W (Claude, 18 Nov 2026, 10:06 am; CONFIRMED as counted from the Astra 006 planet-bench group files)
- Our planet bench touches about 1,150 distinct sector-camera-CCD combinations (one odd sector value seen, so about 1,150 is approximate).
- Witness stars at 100 per CCD-sector: about 115,000 FFI light curves, about 200 GB at 1.8 MB each (200 per CCD-sector: 406 GB). Processed and deleted as we go, the disk need is small; at the 3 files per second measured from the public AWS bucket (Census note, 4 Nov) it is about 11 hours of download for 100 per CCD-sector.
- Over 20 GB, so it needs Ahmed's yes (standing rule from 19 Oct 2026), even though Second Sun downloads are otherwise free. A first slice (10 sectors, about 1,000 files, about 2 GB) can test the meter before the full pull.

## W0 RESULT (Claude, 18 Nov 2026, 12:30 pm; CONFIRMED as computed; `data/witness/w0_meter.txt`, `w0_diag.txt`, `w0_dumps.txt`)
Test slice: 1,000 bystander 2-minute stars (10 sectors x 2 CCDs x 50), 27,079 star-days, 0 errors.
- Preregistered readout: bystanders show a large dip-only excess (frozen at 7: real 1,271 vs upside-down 261 events; 4.69 vs 0.96 per 100 days), but only **2%** of the excess sits in cross-star pile-ups (k = 8 other stars within 0.1 d, fixed by the 1% upside-down rule); notch at 5: 0%. Our own untouched target events in these sectors: 0 of 24 real and 0 of 26 upside-down at a pile-up.
- Exploratory: the excess is **per star**: the 10% most active dipping stars carry 58% of real events; without the 10% most active stars, real 42 vs upside-down 0 (frozen). Cross-star coincidence is not dip-only: upside-down events coincide with 3+ other stars MORE often (24.9%) than real ones (15.1%).
- Exploratory: near momentum dumps (within 0.25 d), without the most active stars: frozen real 26 vs upside-down 17; **notch 5 vs 9** (no dip excess near dumps with the notch; small numbers, LIKELY).
- **Verdict on brief W: the cross-star witness meter, as designed, does not catch our dip-only alarms. The full 200 GB pull is NOT justified now.** Dip-only alarms are star-specific (in our binaries: eclipse leftovers and star variability), so the second meter must be per star: same star, binary phase of the event (eclipse leftovers sit at fixed binary phase), concentration of events in a few stars, and the star's own other sectors. Redesign NOT TESTED; it needs no download (our own target files).
