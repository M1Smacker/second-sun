# Census list: columns the next filter needs (spec note, 11 Nov 2026)

Why now: Petrova 1.0.0 masks eclipses from a catalogue in TIME (not from the data), so every binary it searches needs an ephemeris and eclipse widths. G1 (549 Kepler-field stars) could not join Re-search 1 because its list has a period and an epoch but no widths (`targets/g1_targets.csv`, preregistration section 8). The Census list (our own eclipsing-binary list from post-sector-26 TESS data) must not repeat that gap.

## Columns the Census list should carry (one row per binary, one per star if it has two binaries)
| Column | Meaning | Used by | Where the old lists stand |
|---|---|---|---|
| `tic`, `p_bin_d` | binary period in days, with its error `p_err_d` | window position, period bins, the veto (P of 13 d or more) | in G2, G3; G1 has `period` |
| `t0_btjd`, `t0_err_d` | epoch of primary eclipse in BTJD (BJD minus 2457000), with its error | window position; drift over many cycles | G1 `bjd0` is BJD minus 2400000: convert (minus 57000); the unit slip is a known trap |
| `w_prim_d` | primary eclipse full width in days (first to last contact, or a stated convention) | window width (1.5 x width plus a drift term) | G2, G3 via the catalogue tables; G1 none |
| `w_sec_d`, `phase_sec` | secondary eclipse width and its phase (0.5 for circular orbits; the real value when eccentric) | secondary windows | G2, G3 where known; else 0.5 and the primary width is used |
| `ecc_flag`, `source` | eccentric or not, and which table the row came from | reading the null, mixing sources | not stored today |
| `n_sectors`, `visits_per_sector` | how many TESS sectors and how many times each binary phase is visited per sector | the single-visit lane (S3), the veto's NMIN rule | computed from P today |

## Rules for the Census build
1. Say which convention each width uses (Prsa 2022 table, TTC table 3, Villanova): they differ and the mask must know.
2. Keep period, epoch and width errors; the drift term needs them.
3. Do not guess a width from the data (the old mask did, and that is audit F-01).
4. Test the Petrova conventions on a sample of each new source BEFORE it is searched (gates (a) to (c) on a few hundred star-sectors), as G1 will need.
5. No search result is stored in this list.

Cost: this note is the only Census work this week (about 0.1 points). The build waits for his go (BUILD-QUEUE).
