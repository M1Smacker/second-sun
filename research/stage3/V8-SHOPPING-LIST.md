# Vesper v8 shopping list (started 30 Oct 2026, Sonnet 5.5 extra; for the Opus 5.5 medium design session)

Rules for v8 are still: settings frozen per version, never tuned on results, the 594 sealed G2 stars untouched until v8 is frozen, the preregistration is met and Ahmed says go. Every item below has its evidence in `VESPER-STUDY-PLAN.md` (sections 6 to 8) and `VESPER-VERSIONS.md`.

## A. Ready to take (measured)
1. **C6 orbit-locked flag, variant C** (tier-1 partners with matched box length and depth). Removes 47 locked real tier-1 events on 7 stars on G2 dev; real minus upside-down excess goes +65 to +20 (bar 7) and 0 (bar 12). Cost 0.81% of injected tier-1 dips. G1 unchanged. Purity option, not a sensitivity one. BUILT 30 Oct as switch `c6` (stage3_report.apply_v7); reproduces the offline numbers exactly; G1 unchanged; tests PASS. See `V8-DESIGN.md`.
(C5a box floor `bf4` was here: tested 30 Oct, NOT ACCEPTED, see section C.)

## B. Real forks for Ahmed (policy, not science)
1. **False-alarm budget.** 8 per 1,000 star-sectors was my pre-written yardstick, not a physical limit. Measured exchange: about +1 point of dip recovery per +1 false alarm per 1,000 on G2 dev. Spend more false alarms for more planets, or hold? The cleanest purchase on the shelf is c2 alone (no dip lost in any box): G2 dev 7.7 to 12.6 false alarms buys +3.1 (4 h), +2.4 (8 h), +6.1 (14 and 20 h) points; G1 6.3 to 9.3 buys +1.2, +1.2, +2.2 (`paired-c2-g1/g2.txt`, `fa-counts.txt`).
2. **Price of the short end.** Measured 30 Oct: dropping the 3 h box does NOT free false-alarm room (the short glitches move to the 4 h box) and costs 7 to 8 points of 4 h recovery, so the box floor is not a trade, it is a loss. The same short glitches and the injected 4 to 5 h dips look alike, so any rule aimed at them is expected to cost about 1 point of recovery per false alarm saved (UNCERTAIN, not tested). The fork: is a 3 to 5 h transit worth its share of the false alarms?
3. **Yardstick weight.** The four injected boxes (4, 8, 14, 20 h) count equally. A physical weight (known circumbinary transits run about 6 to 12 h) would change what "better" means.

## C. Tested and NOT taken (do not redo)
C5a box floor `bf4`, alone and with c2 and with c1b+c2 (30 Oct: no significant gain alone; with c2 the false alarms stay at 10 to 12 per 1,000 because the 3 h events just move to the 4 h box), c2 and c1b+c2 alone (false alarms too high), flag reweighting and calibrated scores (do not transfer between sets), strong-dip flag waiver (strong false alarms are glitches), c1a window 3 x box (eats 25% of an 8 h dip), c1c window 5 x box (no gain), "repeat count 2" flag (worse than 1 to 1), phase D stacking step 1 (skipped by its gate: known periods are mostly over 100 d).

## D. Open or needs a yes
- C3 gap and ramp rules scaled to the box (predicted to fail: little false-alarm headroom).
- C5 full physical duration per star: needs TIC radii and masses (a download, needs Ahmed's yes); STANLEY and Martin 2017 as the physics leads.
- Detrending-independence check from the mono-cbp paper (event must survive several biweight windows): published cost is up to 67% of shallow 1 d dips; not tested here.
- Stacking for the short-period end (about 15% of known planets are at or under 75 d).
- The v8 build: switches into the chain, G1 regression and mutation tests, hash, book (Vesper rename and F-090 update with the next publish), same-day Field Note.
