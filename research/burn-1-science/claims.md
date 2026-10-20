# Burn 1 claims

| # | Claim | Source ID + link | Label | Date checked |
|---|---|---|---|---|
| B1 | arXiv:2404.18415 is "Photo-dynamical Analysis of Circumbinary Multi-planet system TOI-1338: a Fully Coplanar Configuration with a Puffy Planet" by Mu-Tian Wang & Hui-Gen Liu (2024-04-29) | arXiv API + https://arxiv.org/html/2404.18415v1 | VERIFIED | 2026-10-19 |
| B2 | Wang & Liu 2024 Table 3 predicts a TOI-1338 b primary transit at BJD−2455000 = 6025.5927 ± 0.0159 (2025-12-16 02:13:28.3 UTC), duration 6.31 ± 0.15 h, b = 0.428 ± 0.050 | arXiv:2404.18415 HTML, raw text grep | VERIFIED | 2026-10-19 |
| B3 | Same table: a predicted transit at 5932.7322 ± 0.0183 (2025-09-14 05:34 UTC, 10.00 h); our S97 hard-mask 2-min LC starts at BTJD 3936.42, so it was not observed in it | arXiv:2404.18415 + fit_event.py | VERIFIED | 2026-10-19 |
| B4 | Wang & Liu 2024 Table 1 TESS mid-times of b (BTJD): S3 1391.2516, S6 1483.9048, S10 1579.0423, S27 2049.9515, S34 2238.2258, S37 2331.0148, S62 2989.6356, S65 3085.4243, S68 3178.2853; S30 not fitted (damaged egress) | arXiv:2404.18415 HTML, raw-text grep (every row appeared in the grep output and matches the WebFetch summary) | VERIFIED | 2026-10-19 |
| B5 | Wang & Liu 2024 state TOI-1338 b will keep transiting the primary at all precession phases | arXiv:2404.18415 (WebFetch summary; the word "permanently" was not found by my raw-text grep, so the wording is unconfirmed) | LIKELY | 2026-10-19 |
| B6 | Our S98 event: best mid-time BTJD 4025.632 (white-noise ±0.002 d), duration 6.4-6.5 h, i.e. +57 min vs the prediction (2.4σ using the prediction error); transit vs none Δχ² ≈ 230 | hands-on: chi2_grid.py | VERIFIED (measurement); the real error bar is larger than white noise (red noise not assessed) | 2026-10-19 |
| B7 | The prediction "the S98 event is a TOI-1338 b transit" (Claude, ~80%) was RIGHT | B2 + B6 | VERIFIED | 2026-10-19 |
| B8 | The wave-3 method, run per sector, recovers 3 of 6 testable published TOI-1338 b transits (S6, S65, S68); misses S10 (masked as an eclipse), S27, S34, S37 (below threshold); S3, S30, S62 not testable (30-min only / PDCSAP NaN) | hands-on: recovery.py, diagnose_misses.py, mask_check.py | VERIFIED | 2026-10-19 |
| B9 | No SPOC 2-min light curve of TIC 260128333 for Sector 3 on MAST via lightkurve; only 30-min FFI HLSPs (GSFC-ELEANOR-LITE, TASOC ×2, TARS) | hands-on: lightkurve search | VERIFIED | 2026-10-19 |
| B10 | Injection-recovery on S98 (8 times per size, b = 0.4, 6.4 h): 0/8 at 2, 3, 4, 5, 6 R⊕; 7/8 at 7 R⊕; 8/8 at 8 R⊕; 0 false events with no injection | hands-on: inject.py | VERIFIED | 2026-10-19 |
| B11 | Wang & Liu Table 1 lists earlier predicted mid-times "from ref. 29" that differ from observed ones by 0.02-0.61 d; ref. 29 is probably Kostov+2020 (not checked) | arXiv:2404.18415 raw text | VERIFIED (numbers) / UNVERIFIED (ref 29 identity) | 2026-10-19 |
