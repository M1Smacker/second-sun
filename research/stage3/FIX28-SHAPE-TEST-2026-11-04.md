# FIX 28: does completeness depend on the shape of the injected dip? (night of 4 Nov 2026; own data, report only; no frozen file touched)

Method: the unchanged frozen chain (Vesper 0.8.1, `VESPER_OPTS=c6`), the same 300 G3 star-sectors and seeds as the official completeness run, 6,024 positive injections per variant (4 box lengths x 6 depths K = 6 to 18 times the 8 h noise x 251 star-sectors with a prepared product). Only the injected shape changes, through a wrapper (`census_step1/chain_recovery_shape.py`) that replaces `signal()` of `pipeline/chain_recovery.py` and nothing else. Shapes are fractions of the total width spent in ingress and egress: sym 0.2 and 0.2 (the harness's own, baseline), skew 0.1 and 0.5, stretch 0.4 and 0.4, box 0.05 and 0.05. Depth K is the plateau depth, the same for every shape. Script `fix28_compare.py`, output `fix28-compare.txt`.

## Plain verdict
**Shape matters, mostly in one direction: a rounder, V-like dip is found and kept far less often than our trapezoid.** At the same plateau depth and total width, kept share at K 8 to 14 falls from 30.5% (sym) to 26.1% (skewed, minus 4.4 points, 95% interval minus 5.6 to minus 3.0), to 21.5% (stretched, minus 9.0 points, minus 10.6 to minus 7.5) and to 29.1% (box, minus 1.4 points, minus 2.5 to minus 0.2). So the completeness we have been quoting (33.8%, 43.7%, 40.0%, 24.6% for G3 and similar for G2) is probably generous by about 1 to 9 points for real transits, depending on how round they are.

## Identity check (CONFIRMED)
The sym variant reproduces the official G3 completeness run exactly: 12,348 rows, 6,024 positive injections, tier-1 and seen identical in 100.0% (kept 33.1% in both, all K 6 to 18). So the wrapper changes nothing but the shape.

## Numbers (kept in tier 1, share of injections, K 8 to 14 unless stated)
| box length | sym | skew | stretch | box |
|---|---|---|---|---|
| 4 h | 26.2% | 17.7% | 9.8% | 31.9% |
| 8 h | 38.4% | 34.1% | 25.2% | 39.7% |
| 14 h | 36.0% | 31.6% | 30.1% | 32.1% |
| 20 h | 21.4% | 21.0% | 20.7% | 12.5% |
By depth (all box lengths): K 8: 14.1 / 10.3 / 8.1 / 13.7; K 10: 32.1 / 26.1 / 20.1 / 30.5; K 12: 45.2 / 41.9 / 36.3 / 42.9; K 14: 50.7 / 49.6 / 48.0 / 46.4 (sym / skew / stretch / box). The shape loss shrinks as the dip gets deeper (a loud dip survives any shape) and is worst for short boxes and shallow dips.

## What it means
- A 4 hour dip with long ramps (0.4 each side, so only 20% of the width is flat) is kept 9.8% of the time against 26.2% for the trapezoid: the search's box-shaped matched filter loses signal when the dip is round. That is the likely mechanism (LIKELY, not tested separately): at the same plateau depth the V-like dip has a smaller area.
- The 20 h box loses most from the sharp box (12.5% against 21.4%): a very sharp-edged 20 h dip interacts with the detrending (cause NOT tested).
- Real circumbinary transits: ingress and egress are short for a planet much smaller than its star (ingress fraction about the radius ratio, 5% to 10% for Jupiter-size planets, shorter for smaller ones), but limb darkening rounds the bottom and the duration changes with the stars' motion. So reality likely sits between sym and stretch for large planets and near box for small ones. We do not know; keep it as an uncertainty range on every completeness number: minus 1 to minus 9 points (relative minus 3% to minus 30%).
- This also means the Horizon reach sums (which use the sym recovery tables) are generous: another reason to treat them as upper bounds (the shape factor is in the same direction as the geometry factor).

## Plan changes
1. FIX 28 is answered as a measurement (not a code fix): shape sensitivity quantified. A further cheap step would be an injected shape from a physical transit model (limb-darkened, with a radius ratio), which would pin the number; costs about 0.3 and needs the same harness.
2. Add a "shape range" line to the completeness table in future benchmark reports.
3. Census sizing in `CENSUS-WORTH-2026-11-04.md` used the sym recovery tables; with a 10% to 20% relative loss in recovery the Census evidence numbers fall by that much (a small shift beside the geometry range).

## Labels
CONFIRMED: all rates (own run), the identity check, the paired differences and intervals. LIKELY: the mechanism (matched-filter mismatch), the real-world range. UNCERTAIN: where real transits fall between the shapes. NOT TESTED: a physical limb-darkened shape; duration changes during the transit.
