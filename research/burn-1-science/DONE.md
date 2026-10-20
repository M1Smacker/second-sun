# Burn 1 (science): DONE

Finished 2026-10-19 ~21:06 UTC, well before the 21:55 hard stop. Nothing committed or pushed (the coordinating session commits).

## Done
- [x] **Task 1**: found the published prediction. Wang & Liu 2024, arXiv:2404.18415 (ID verified), Table 3: TOI-1338 b transit at BTJD 4025.5927 ± 0.0159 (2025-12-16 02:13 UTC), 6.31 h. Our fit: BTJD 4025.632, ~6.4-6.5 h, i.e. +57 min (2.4σ). **The ~80% prediction was RIGHT**; the dated outcome line is appended to `research/predictions.md`. The rebound fallback was not needed (an explicit dynamical prediction exists).
- [x] **Task 2**: recovery test on the published sectors (S6, S10, S27, S30, S34, S37, S62, S65, S68; S3 has only 30-min FFI). Recovered 3/6 testable (S6, S65, S68). Every miss is diagnosed: eclipse-mask confusion (S10), threshold rule too weak / 1-d detrend (S27, S34, S37), PDCSAP NaN (S30, S62).
- [x] **Task 3**: injection-recovery smoke test on S98: 0/8 at 2-6 R⊕, 7/8 at 7 R⊕, 8/8 at 8 R⊕; 0 false alarms.
- [x] Phone PNG: `burn1_summary.png` (1080×1920, checked visually for overlaps).
- [x] `report.md` (plain words first), `claims.md`, `sources.md`, `open-questions.md`, `friction.md`.
- [x] 10 downloads (17 MB total) logged in `research/downloads.csv`, under `data/burn-1/`. No TESScut used.

## Not done
- [ ] Red-noise error on the S98 mid-time (so the +57 min offset is not yet trustworthy as a timing measurement).
- [ ] Kostov+2020's own predictions were not read (only the arXiv ID/title was checked).
- [ ] S97 coverage of the 2025-09-14 predicted transit with other masks/products.
- [ ] Method fixes (matched filter, global eclipse ephemeris, longer detrend, SAP fallback): recommended, not attempted (out of scope).

## Key finding for the coordinator
The wave-3 single-event rule only sees single transits deeper than ~2,000-2,400 ppm (~4× the 30-min MAD; ~7 R⊕ on TOI-1338 A). The wave-3 feasibility table (2-5 R⊕ at Tmag 10-13) describes the data's potential, **not the current pipeline's**. Fix the detector before any G1 null result is quoted.
