# RS-046: how many stars can the Census really reach? (the star side of the coming fork; Claude Opus 5.5 high, 24 Nov 2026, 11:25 pm)

**Question (decision it feeds):** after D1, Ahmed's likely fork (P75-REESTIMATE, 22 Nov) is (a) keep building expensive levers for P, or (b) freeze the best tool and search many more stars. Option (b) is only as good as the number of stars it can reach. **Cap written first: 0.5 weekly points, own data only, no web.** Inputs: tonight's union (`research/stage3/census_union/T139-UNION-RESULT-2026-11-24.md`), the 8 Nov FFI door counts, RS-039 A5.

**Plain line: the Census can plausibly reach 3,000 to 5,000 bright slow binaries, but only about 600 of them are ready to search today. The rest need two builds first: our own period finder (Codex 035, queued) and full-frame light for the Gaia pool (T152). By RS-039's arithmetic, 3,000 stars at today's P is worth more than raising P from 48 to 75 on 1,400 stars.**

## The pools, from our own counts
| Pool | Stars (bright, P over 5 d) | Ready to search? | What it needs | Label |
|---|---|---|---|---|
| Catalogues (Prsa, TTC), unsearched, with times and widths | 582 (21 over 10 d) | yes, after the usual gates (a) to (c) | nothing new | CONFIRMED count |
| CALNet, no period anywhere | about 600 to 1,700 of 8,296 bright (if 7% to 20% are over 5 d) | no | period finder (035); 9,547 CALNet stars have 2-minute light from sector 27 on | UNCERTAIN share |
| Gaia DR3 slow pool not in any list (G5) | 5,382 counted, about 3,700 truly over 5 d (68.5% of matched bright ones are) | no | TIC cross-match; full-frame light (QLP, TESS-SPOC FFI, T152); period finder | count CONFIRMED, share UNCERTAIN |
| **Total, if every build works** | **about 4,900 to 6,000** | | | UNCERTAIN |

Overlaps between CALNet and the Gaia pool are already removed (the Gaia count excludes every union star). A realistic Census, after losses to gates, crowding and FFI coverage (only 22.7% of star-sectors had both FFI products on 8 Nov), is lower: **about 3,000 to 5,000** (my judgement, UNCERTAIN).

## What that is worth (RS-039 A5's arithmetic, extended)
The transit-geometry factor (T138) is already inside these numbers: A5 rests on the 8 Nov recount of `CENSUS-WORTH-2026-11-04.md`, which uses Horizon R0 Amendment 4's transit chance (`census_step1/census_worth2.py`).

RS-039 A5 (LIKELY, Kepler-like prior, today's completeness): 1,400 stars give a 36% to 52% chance of at least one planet; 3,000 give 59% to 76%. Treating planets as rare events spread evenly over stars (Poisson), the 3,000-star anchor gives a per-star rate of 0.00030 to 0.00048, so **5,000 stars would give about 77% to 91%**. That assumes full-frame stars are searched as well as 2-minute ones; they are not (30- and 10-minute cadence, more noise), so the true value is lower. **UNCERTAIN; NOT TESTED** on FFI light.

For comparison, RS-039 A5: raising P from 48 to 75 on 1,400 stars gives about 50% to 68%. Going from 1,400 to 3,000 stars at today's P (59% to 76%) is worth more, and the star builds (period finder, FFI path) are concrete, while the P levers past about 55 are not (P75-REESTIMATE).

## What it changes
1. It strengthens Claude's lean for the fork, (b), and names its real cost: Codex 035 (period finder), T152 (FFI light path), a TIC cross-match for the Gaia pool, then gates (a) to (c) on samples of each new source (spec note rule 4).
2. It does not decide the fork. D1's result, and Ahmed's word, still come first. Nothing is started on the strength of this note beyond 035, which serves both branches.

## Update 25 Nov 2026, 1:11 am: TIC cross-match done (`census_union/gaia_tic_xmatch.py`, `data/census_tic_xmatch/`, MAST TIC v8.2, 2.65 MB)
Of the 5,382 bright Gaia slow-pool binaries in none of our lists: **5,192 (96.5%) have a TIC id** (42 Gaia ids map to two TIC rows; 190 unmatched, likely DR2/DR3 id changes, NOT TESTED), and **only 96 (1.8%) were 2-minute targets in any sector from 27 on**. CONFIRMED: the G5 pool is full-frame-only in practice, as assumed above. Its Census value therefore rests on T152 (the full-frame path) and on how well Petrova searches 30-, 10- and 3.3-minute light: NOT TESTED.