# How far can P go? Re-estimate after 22 Nov 2026 (Claude, 11:15 pm; A13 and D1 still running)

**Plain line (updated 11:24 pm after A13 and T2): with every lever we know, P looks headed for about 51 to 55, not 75. RS-039's range (61 to 75) leaned on two numbers that tonight's checks cut down: the notch's detection gain (+7.7 measured only on crossings it could score; +2.9 over all) and the one-score lever (+4 to +8 estimated; measured +0.5 and unfair). This is an estimate (LIKELY for the direction, UNCERTAIN for the size); D1 and A13 will sharpen it within a day.**

## Lever by lever (points of P on the 968 possible planets; today 48.4)
| Lever | What we know now | Realistic gain |
|---|---|---|
| Notch for short dips, box for long (D1, Codex 031) | N1 alone gained +2.09 on the fresh bench but lost T156 on long dips; D1 removes the long-dip loss | +2 to +3 (pending) |
| Notch with fallback where it cannot score (A13) | DONE 11:23 pm: the fallback adds gap-side alarms; at equal alarms -1.7 vs the notch | 0 |
| Better photometry (TGLC, RS-042) | QLP 94+ looks 0.8 x the noise, but the MAST TGLC light for older sectors is not quieter than our QLP on the same star-sectors (0.97, n 13) | 0 now; later if QLP reprocesses all sectors |
| One learned score for held planets | S0: +0.5 real, +3.4 upside-down | about 0 |
| Release holds DS, M2, R2 (rule 4) | +2.6 to +4.1 on the bench, but each adds many more real than upside-down alarms; needs a meter for dip-only alarms; the cross-star witness meter (W0) and simple per-star features (M1) did not work | 0 until a dip-only meter exists |
| Window rules (one-neighbour, majority; Fable F2) | intersection costs about 1.2; never benched | +0.5 to +1.5 |
| Stray-light cadences under the notch | 025 failed under the box score; untested under the notch; load losses about 1 point | 0 to +1 |
| Stacking crossings | under 1 (Codex 028) | 0 to +1 |
| **Sum (overlaps ignored; updated 11:24 pm after A13 and T2)** | | **about +2.5 to +6.5: P about 51 to 55** |

## What it would take to reach 75
About 20 more points than the known levers give. Two things could, and neither is cheap:
1. **A meter for dip-only false alarms.** Every remaining big pool (held 16.7, mask timing 5.3) is blocked by one fact: next to gaps, dumps and steps, fake dips outnumber fake bumps, and the upside-down copy cannot see them. The field's answers (Kepler's scrambled light, cross-star pile-ups, pixel-level tests) either did not work on our data (W0, RS-032) or need pixel files we have not pulled (target pixel files, not priced).
2. **Better light.** The white-noise ceiling is 79.5 (A1); our noise is 1.6 to 1.9 times the photon floor at Tmag 9 to 11 and 2 to 3 times at 12 to 13. Gaia-based photometry is the published route, but RS-042 T2 found the MAST TGLC release no quieter than our QLP on the same star-sectors; only QLP's own TGLC from Sector 94 looks better (T1, LIKELY). Waits for QLP's announced reprocessing.

## The decision RS-039 wrote down for this point
RS-039's stop-or-rethink rule (written 18 Nov, before any of this): *"if after Phases 0 and 1 the fresh-bench P is under 52, the cheap levers are spent; stop building and decide with Ahmed whether to run Census with the tool as it is."* RS-039 A5 also measured that P and the number of stars searched multiply: 1,400 Census stars at today's P give a 36% to 52% chance of at least one planet; 3,000 stars give 59% to 76% (Kepler-like prior, LIKELY). Raising P from 48 to 55 is worth about the same as searching about 15% more stars.

So after D1 the real fork for Ahmed is LIKELY to be: (a) keep building the expensive levers (pixel data or new photometry, weeks, uncertain), or (b) freeze the best tool we have (Petrova 2.0 with D1 if it passes) and spend the effort on searching many more stars (Census). Claude's lean, to be confirmed by D1: (b), with (a) as a slower side track. This is Ahmed's call; nothing is started.
