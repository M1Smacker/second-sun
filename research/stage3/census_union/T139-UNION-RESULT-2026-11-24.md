# T139 Census stage 2, part 1: the public eclipsing-binary lists merged (Claude, 24 Nov 2026, 11:13 pm Kuwait)

**Plain line: the catalogues are nearly used up for us. Only 21 bright binaries with periods over 10 days remain unsearched in them. The Census's real pool is CALNet's 10,531 new bright binaries, and 8,814 of those have no period anywhere, so our own period fit on TESS light is now the Census's critical path.**

Scripts: `build_union.py` (merge), `pool_counts.py` (counts), this folder. Output (git-ignored): `data/census_union/eb_union.csv` (one row per star, best ephemeris and every source listed), `sources.csv` (one row per source row, units normalised), `summary.json`.

## How it was built
| Source | Rows | What it gives | Units, as read from the file headers |
|---|---|---|---|
| Prsa et al. 2022 (`data/xmatch/ebs.csv`) | 4,584 | period, epoch, widths, secondary phase, morphology | epoch already BTJD (about 1411); widths in phase, times P |
| TESS Ten Thousand table 3 (new EBs) | 7,936 | period, epoch, eclipse durations, secondary phase | epoch BJD minus 2457000; durations in hours |
| TESS Ten Thousand table 4 (known EBs) | 2,065 | TESS period and epoch only | BJD minus 2457000 |
| CALNet (`data/calnet_2026-11-07`) | 10,531 | which stars; Gaia DR3 period for 1,559 | Gaia durations in phase (about 1.38 times Prsa's, C1-C2 result) |

Best ephemeris per star: TTC table 3, then table 4, then Prsa, then Gaia (newest TESS fit first). Each width keeps its convention in `width_conv` (spec note rule 1). No width is guessed from data (rule 3).

## Checks (each could have failed)
| Check | Result | Label |
|---|---|---|
| Our reading of the G2 rule (Prsa, morphology 0 to under 0.5, P over 5 d, Tmag 13.5 or brighter, not G1) reproduces the frozen G2 list | 895 of 895, exact | CONFIRMED |
| Prsa and TTC table 4 periods for the same star | 50 of 50 agree within 1% | CONFIRMED |
| TTC table 4 and Gaia DR3 periods (CALNet stars) | 10 of 37 agree, 5 are half or double | CONFIRMED; Gaia periods unreliable, as C2 found |
| CALNet overlaps Prsa or TTC table 3 | 0 stars (CALNet lists only binaries new to earlier catalogues) | CONFIRMED |

## The pool
| Group | Stars |
|---|---|
| All stars in the union | 24,902 |
| Not yet searched (not in G1, G2, G3) | 23,291 |
| Not searched, P over 5 d, with epoch and width | 2,147 |
| ...and Tmag 13.5 or brighter | 582 (561 at 5 to 10 d, mostly TTC 5 to 7 d stars below G3's 7-day rule; 18 at 10 to 20 d; 3 over 20 d) |
| ...and with 2-minute TESS light from sector 27 on | 94 |
| CALNet stars with no period anywhere | 8,814 |
| CALNet stars with 2-minute light from sector 27 on | 9,547 |
| CALNet brightness | median Gaia G 11.7; 8,296 at G 13.5 or brighter |

CALNet periods we do know (Gaia DR3, 1,559 stars) have median 0.89 d and only 114 over 5 d. That sample is biased toward short periods, because Gaia's sparse visits catch short binaries more easily: the 8,814 with no Gaia period may hold more long ones. **UNCERTAIN** until we fit them. If 7% to 20% of the 8,296 bright ones are over 5 d, that is about 600 to 1,700 Census stars, matching the 4 Nov estimate of about 1,000.

## What it changes
1. The catalogue part of the Census is small (about 580 bright, mostly short-period stars). The big part needs our own period from TESS light.
2. Eclipse timer v3 (Codex 032) times eclipses when a period is known; it does not find periods. **Next Census build: a period finder for one star's TESS light (box search on eclipses, then v3's half-period check), tested on the Prsa and TTC stars where the answer is known.** Size: a Codex brief, after 034b.
3. On 2 Dec, Gaia DR4 rows join through the same merge (`source = gaia_dr4`) and C2 is rerun on them before any DR4 period is trusted.
