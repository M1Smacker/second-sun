# Vesper 0.9 study plan (written 2 Nov 2026 BEFORE any run; rules fixed here)

Purpose: decide which of the new switches, if any, become Vesper 0.9. Judged on the DEVELOPMENT slice (301 stars) only. The sealed slice is spent for 0.8.0 and G3 (the new star list) is the clean test of whatever is frozen, so sealed numbers are printed beside the development numbers for information and never decide anything. Base: Vesper 0.8.0 (git tag `vesper-0.8.0-g2-sealed`, frozen hash 5f73692944aa); every new switch defaults OFF and the default code path is proved identical by `zero_diff.py` before any run.

## The switches (each its own, `pipeline/vopts.py`)
- **dg (T31)** depth guard: an event deeper than 30% of the flux or with a non-finite depth goes to tier 2 (flag `too_deep`). Physics: a transit cannot remove more than about 30% of a star's light; the deepest real event of the first sealed run is 26.5%.
- **nd (T32, re-scoped 2 Nov 2026)** an unphysical event is left out of the dominance comparison. The old diagnosis ("near-zero scatter") was wrong: for the 3.5e26 SNR event the scatter is about 1,000 ppm; the cause is a baseline near zero (depth 3.7e29 ppm, a broken light curve). Its absurd SNR marks every real event of the same light curve as `dominated`, so real events are lost behind it.
- **fl (T33)** flare-shape check: asymmetry = (mean flux of the late third of the box minus the early third) / depth, in the search's orientation (dip down); about 0 for a box, positive for an abrupt start and slow recovery. Stored for every event (`asym`); above the threshold an event goes to tier 2 (flag `flare`). Same rule for real and upside-down events, so the control stays fair. Candidate thresholds 0.5, 1.0, 1.5.
- **T34 step check:** no new switch (c1a, c1b, c2 and variants were already NOT ACCEPTED). Report-only pricing of its two parts (coverage rule, lift rule) from the stored cover and lift of planted dips (T104).
- **T35 3 h box:** report-only split by box length.

## Runs (development slice, BelowNormal, at most 6 processes, NUMBA_NUM_THREADS=1)
1. Full dev chain with `VESPER_OPTS=c6,dg,nd,fl` (stores `asym`, `too_deep`, `flare`). The 0.8.0 baseline on the same events is read offline by ignoring the new flags (for nd, by comparing with the existing 0.8.0 dev run `dev_73f62615e365`).
2. `chain_recovery.py` on the same 300 development star-sectors as before, same seed, same options (rows now carry cover, lift, asymmetry and the new flags).
3. Paired fairness (mirror) test as in the earlier study.

## Yardstick (unchanged from VESPER-STUDY-PLAN section 3) plus the rule for removal switches
- Sensitivity: tier-1 recovery of planted dips (K 8 to 14, pooled, and K50 for the 8 h and 14 to 20 h boxes). False alarms: upside-down tier-1 per 1,000 star-sectors on the full dev run. Fairness: the mirror test stays within 3 points. Never judged by the number of real tier-1 events or any single real event.
- **dg and nd (guards): ACCEPT if** zero planted points are lost on development (by construction they cannot touch a dip under 30%), the mirror test holds, and no development event of depth 30% or less changes tier because of them. They are physics guards; they are rejected only if a defect shows.
- **fl (removal switch): ACCEPT if ALL of:** (1) upside-down tier-1 events on the development run fall by at least 20%; (2) upside-down events removed per planted tier-1 point lost is at least 6.8 (the price of the step check, the dearest check we keep, measured 31 Oct 2026); (3) the 8 h and 14 to 20 h K50 are each no more than 10% worse; (4) the mirror test holds. The threshold is the one among 0.5, 1.0, 1.5 with the largest fall in upside-down events that still satisfies (2) to (4). If none does, fl is REJECTED and recorded as a negative result.
- The planted dips use symmetric trapezoids (20% ingress and egress), so the shape check should cost little on them; that is a property of the test dips, not of real planets (a real planet's shape may differ slightly). Said now so the result is read with that limit.

## After the runs
- Accepted switches become Vesper 0.9 = 0.8.0 + those switches. Then: zero-difference with the switches off (300 of 300), a mutation test, freeze under a new hash (`freeze` mode), regression, and a written amendment to the scorecard (already: `SCORECARD-AMENDMENTS.md`, Amendment 2). Nothing accepted: keep 0.8.0 and write the negative result.
- The sealed-style test is the G3 run (T37b) with whichever version is frozen, after a preregistration written before any G3 light curve is read (T112).

Labels: the flare mechanism is LIKELY (cause of the survivors not confirmed against a flare catalogue); the 20% and 6.8 criteria are choices made now, before results.
