# 003 final tables

CONFIRMED: independent journal aggregation, no pipeline imports or new searches. Counts are dip recoveries unless stated. Intervals are the saved star-cluster bootstrap, not independently recomputed.

## Period and paired control

| Period d | Ref recovered/n | Ref R, 95% CI | All dip/bump (n=400) | Dip-only / bump-only | Paired difference 99% CI, points |
|---|---|---|---|---|---|
| 5 to 10 | 6/48 | 12.5% [4.0%, 23.1%] | 47/55 | 9/17 | [-5.25, 1.26] |
| 10 to 14 | 9/35 | 25.7% [11.1%, 40.0%] | 78/69 | 15/6 | [-0.78, 5.21] |
| 14 to 20 | 12/46 | 26.1% [14.0%, 39.0%] | 71/80 | 10/19 | [-5.53, 1.18] |
| 20 to 27.4 | 19/47 | 40.4% [20.0%, 57.9%] | 91/80 | 21/10 | [-1.41, 8.26] |
| 27.4+ | 15/46 | 32.6% [18.9%, 46.2%] | 107/116 | 12/21 | [-6.93, 2.52] |

All five paired, star-clustered 99% intervals include zero (Bonferroni across five bins). This is no detected aggregate difference, not proof of equivalence or absence of a structural bug. Reference totals: 61 dips, 62 bumps.

## Sequential losses

### Reference

| Period d | n | No windows | Outside/gap | Mask/support | No event | Below tier 1 | Caught |
|---|---|---|---|---|---|---|---|
| 5 to 10 | 48 | 3 (6.2%) | 9 (18.8%) | 5 (10.4%) | 19 (39.6%) | 6 (12.5%) | 6 |
| 10 to 14 | 35 | 1 (2.9%) | 6 (17.1%) | 2 (5.7%) | 10 (28.6%) | 7 (20.0%) | 9 |
| 14 to 20 | 46 | 2 (4.3%) | 8 (17.4%) | 2 (4.3%) | 6 (13.0%) | 16 (34.8%) | 12 |
| 20 to 27.4 | 47 | 1 (2.1%) | 10 (21.3%) | 3 (6.4%) | 5 (10.6%) | 9 (19.1%) | 19 |
| 27.4+ | 46 | 0 (0.0%) | 12 (26.1%) | 3 (6.5%) | 1 (2.2%) | 15 (32.6%) | 15 |

### All depths/durations

| Period d | n | No windows | Outside/gap | Mask/support | No event | Below tier 1 | Caught |
|---|---|---|---|---|---|---|---|
| 5 to 10 | 400 | 16 (4.0%) | 66 (16.5%) | 57 (14.2%) | 137 (34.2%) | 77 (19.2%) | 47 |
| 10 to 14 | 400 | 16 (4.0%) | 68 (17.0%) | 36 (9.0%) | 119 (29.8%) | 83 (20.8%) | 78 |
| 14 to 20 | 400 | 10 (2.5%) | 61 (15.2%) | 32 (8.0%) | 126 (31.5%) | 100 (25.0%) | 71 |
| 20 to 27.4 | 400 | 17 (4.2%) | 55 (13.8%) | 51 (12.8%) | 107 (26.8%) | 79 (19.8%) | 91 |
| 27.4+ | 400 | 0 (0.0%) | 66 (16.5%) | 42 (10.5%) | 81 (20.2%) | 104 (26.0%) | 107 |

## Product, era, campaign and brightness

Equal-bin R standardizes over five period bins; pooled reference fractions are also shown. Missing-best groups stay in the denominator. Sparse subgroup rates are descriptive, not separately calibrated decisions.

### product

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| QLP | 852 | 114/123 | 19/90 | 22.4% |
| SPOC | 470 | 120/125 | 17/57 | 32.5% |
| TESS-SPOC | 599 | 160/152 | 25/68 | 34.9% |
| nan | 79 | 0/0 | 0/7 | Unavailable |

### campaign

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| g3 | 421 | 35/35 | 9/45 | 20.3% |
| g2 | 1579 | 359/365 | 52/177 | 28.5% |

### era

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| 56-93 | 757 | 132/137 | 22/87 | 26.8% |
| <56 | 1070 | 240/241 | 36/114 | 30.4% |
| >=94 | 173 | 22/22 | 3/21 | 15.7% |

### brightness

| Group | All n | Dip / bump | Ref recovered/n | Equal-bin R |
|---|---|---|---|---|
| 12-14 | 486 | 29/33 | 5/49 | 12.3% |
| 11-12 | 476 | 98/100 | 23/57 | 37.4% |
| <11 | 1038 | 267/267 | 33/116 | 28.4% |

## Depth and duration cells

| Depth ppm | Duration h | n | Dip | Bump | Dip rate |
|---|---|---|---|---|---|
| 1000 to 2000 | 3 to 6 | 232 | 23 | 20 | 9.9% |
| 1000 to 2000 | 6 to 12 | 231 | 28 | 24 | 12.1% |
| 1000 to 2000 | 12 to 18 | 158 | 18 | 16 | 11.4% |
| 2000 to 3000 | 3 to 6 | 147 | 20 | 22 | 13.6% |
| 2000 to 3000 | 6 to 12 | 136 | 32 | 33 | 23.5% |
| 2000 to 3000 | 12 to 18 | 77 | 14 | 14 | 18.2% |
| 3000 to 6000 | 3 to 6 | 224 | 64 | 64 | 28.6% |
| 3000 to 6000 | 6 to 12 | 222 | 61 | 62 | 27.5% |
| 3000 to 6000 | 12 to 18 | 134 | 15 | 19 | 11.2% |
| 6000 to 10000 | 3 to 6 | 173 | 68 | 65 | 39.3% |
| 6000 to 10000 | 6 to 12 | 174 | 44 | 52 | 25.3% |
| 6000 to 10000 | 12 to 18 | 92 | 7 | 9 | 7.6% |

## Saved-window alternatives (exploratory post hoc reading)

No new settings were run. Agreement is a post hoc diagnostic, not a validated selected rule. Bump gains below are newly recovered injected bumps, not background false alarms.

| Rule on selected failures | New dips | New planted bumps |
|---|---|---|
| 2+1 day union | 40 | 30 |
| 2+3 day union | 2 | 3 |
| 2+1+3 day union | 41 | 33 |
| 2 plus agreement of 1 and 3 | 1 | 0 |

## Short-period context

| Split | Group | 5 to 10 d recovery | Other bins pooled |
|---|---|---|---|
| product | QLP | 2/25 | 17/65 |
| product | SPOC | 3/12 | 14/45 |
| product | TESS-SPOC | 1/8 | 24/60 |
| product | nan | 0/3 | 0/4 |
| campaign | g2 | 5/32 | 47/145 |
| campaign | g3 | 1/16 | 8/29 |
| brightness | 11-12 | 0/7 | 23/50 |
| brightness | 12+ | 1/15 | 4/34 |
| brightness | <11 | 5/26 | 28/90 |

