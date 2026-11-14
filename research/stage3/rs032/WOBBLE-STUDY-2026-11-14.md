# RS-032: does the telescope's wobble separate dump artefacts from planets? (Claude, 14 Nov 2026, Opus 5.5 medium)

**Why:** RS-031 found the dump-shape rule DS frees 30 real against 4 upside-down untouched events, mostly just before a momentum dump, and its planet gain sits in the same place. The literature says the fake dips come from pointing scatter (the star wobbling in its aperture). Every light-curve file we hold records where the star's light centre is at each moment (SPOC and TESS-SPOC: MOM_CENTR1/2; QLP: SAP_X/SAP_Y). If the wobble inside an event's box is larger for the fake dips than for planted planets, it is an independent false-alarm check for DS that does not use the upside-down meter. Feeds Fable's task 2 (Monday).

**Cap, written first:** 1.5 weekly points, about 40 tool calls. Own data only, no downloads. Design stars of G2 and G3 only (no fence A or B star is opened).

## Method (written 14 Nov 2026 before any number was computed; nothing below is changed after seeing outputs)
- **Dump zone:** as the momentum-dump flag (C7): a dump between 0.25 d before and 0.5 d after the box centre. Dump times from QUALITY bit 32 of design stars' SPOC or TESS-SPOC files (as RS-031).
- **Wobble J of a box** (centre c, duration d) in one light-curve file: good cadences (QUALITY 0, finite centroid). Cadence-to-cadence steps of the column and row centroid; robust scatter s = 1.4826 x median absolute deviation, combined as sqrt(s_col^2 + s_row^2). s_box over the box (widened to at least 2 h); s_ref over the whole file excluding 1 d either side of every dump. **J = s_box / s_ref.** Secondary measure (reported, not used for the guard): drift D = distance between the median centroid inside the box and the median in the 1 d around it, over s_ref.
- **Groups:**
  - A (real) and F (upside-down): untouched-light background events, primary, SNR 7+, that DS frees (tier 1 under B+DS, not under B). Same harness as RS-029 and RS-031.
  - Pl2: every planted transit crossing of the 006 planet bench that falls in the dump zone (all trials with a crossing), J measured on the unplanted file of the star's best product for that sector. This is where planets land, unselected.
  - Pl: the subset of Pl2 crossings in trials DS gains (real-arm new under B+DS, not under B).
- **Guard (derived on G2 from planets only, never from A or F):** Jt = 90th percentile of J over G2 Pl2. Guard: DS relief only when J <= Jt.
- **Checks on G3 (scored once):** share of A held by the guard; share of F held; share of Pl and Pl2 kept. Also reported on G2 for description.
- **Pass (written first):** the wobble is a USEFUL separator if on G2 the A and Pl2 distributions differ (Mann-Whitney one-sided, A larger, p < 0.01) AND on G3 the guard holds at least half of A while keeping at least 80% of Pl2. Otherwise NOT USEFUL as built. Either way it is a measurement; no rule is adopted (Fable designs, Ahmed decides).
- **Not tested here:** the full bench under a DS + wobble rule (P and T156); only if the pass holds, as a follow-up.

## Results (14 Nov 2026, 11:05 pm; `rs032_wobble.py`, `wobble.json`, rows in `data/rs032/wobble-rows.csv`)
**Verdict: NOT USEFUL as built (preregistered pass fails). CONFIRMED on our data: the centroid wobble we can measure does not separate the DS-freed real events from where planets land.**
- **Run defect, fixed before reading any result as final:** the first run read SPOC file names "tess2019..." as sector 2019 (a trap the auditor skill lists) and did not map "-SAP" product names to their files, so SPOC events had no J. Only the file lookup changed; method, threshold rule and pass check unchanged. Numbers below are the second run.
- **Groups:** G2: A 27 real and F 4 upside-down DS-freed events (G3: A 3, F 0; total 30 and 4, as RS-029 and Codex 013), Pl2 422 planted crossings in the dump zone (G3 118).
- **Threshold** Jt = 1.897 (90th percentile of J over G2 Pl2).
- **G2:** J median A 0.98 (25 measured), Pl2 1.08 (415). Mann-Whitney A larger than Pl2: **p = 0.53** (needs under 0.01). The guard would hold 4 of 25 A events and 42 of 415 planet crossings (10% by construction): no better than chance. The 24 crossings in trials DS gains: J median 1.14.
- **G3:** only 3 A events (J median 1.32); the guard holds 1 of 3 (needs at least 2) and keeps 113 of 116 Pl2 crossings. Fails on A held.
- **Exploratory, NOT preregistered (secondary measure, reported only):** drift of the light centre inside the box against the half day around it: A median 0.82 against Pl2 0.45 on G2 (one-sided p = 0.05), G3 2.88 against 0.37 (3 events). A guard at the planets' 90th percentile would hold only 4 of 25 G2 events. A weak hint, not a separator.

## Why it fails (LIKELY, physics)
The pointing jitter the papers describe is fast (seconds), inside each exposure. Our centroids are averages over 2 min (SPOC), 10 or 30 min (TESS-SPOC, QLP): they show slow drifts, not the fast jitter that spills light out of the aperture. So the meter that could see the artefacts is not in our light-curve files. It exists elsewhere: the spacecraft's pointing records (engineering quaternions, 2-second cadence, published per sector at MAST; LIKELY, not yet opened). That is a download and a new study, not tonight's.

## What it changes
- DS stays held. A wobble guard from our files is ruled out (cheaply).
- For Fable (task 2): the only independent separator left is the 2-second pointing record, or an injection test of artefact shapes; RS-032 is the evidence that centroids are not enough.
- Filed as a lead, not a build: T164 idea on node 1.6 (pointing quaternions near dumps), waits for Fable's design.
