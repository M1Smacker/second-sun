# Wave 3 claims (P-numbers)

| # | Claim | Source | Label | Checked |
|---|---|---|---|---|
| P1 | On Windows 11 + Python 3.12.10, these install from PyPI: wotan 2.0, transitleastsquares 2.0.1, batman-package 2.5.3, rebound 5.2.2, triceratops 1.1.0, exovetter 0.0.16 (main venv); stanley_cbp 0.2.8 and ellc 1.8.15 (separate venvs) | hands-on (install_results*.txt) | VERIFIED | 2026-10-19 |
| P2 | mono-cbp 0.1.9 fails to install on Windows / Py 3.12 ("Compiler cython cannot transpile programs" during a source build caused by its scipy<1.13 pin) | hands-on | VERIFIED | 2026-10-19 |
| P3 | Installing triceratops 1.1.0 downgrades numpy 2.5.4 → 1.26.4, scipy 1.18.1 → 1.13.1, astropy 8.0.2 → 7.2.3; all tools still import together | hands-on | VERIFIED | 2026-10-19 |
| P4 | Licences (package metadata): lightkurve MIT, astroquery BSD, wotan MIT, TLS MIT, batman GPLv3, rebound GPL-3.0-only, triceratops MIT, exovetter BSD-3, PyTransit GPLv2, stanley_cbp MIT, ellc GPLv3 | importlib.metadata | VERIFIED | 2026-10-19 |
| P5 | A sitecustomize-level `truststore.inject_into_ssl()` makes pip crash with RecursionError (pip injects its own vendored truststore); skipping it for pip fixes it | hands-on | VERIFIED | 2026-10-19 |
| P6 | 2,888 of 2,920 Villanova Kepler EBs match a TIC entry by KIC; all EBs: median Tmag 13.58, 48% ≤ 13.5; detached (morph < 0.5) with P_bin > 5 d: n = 1,112, median 13.51, 552 (50%) ≤ 13.5 | hands-on (g1_tmag.csv) | VERIFIED | 2026-10-19 |
| P7 | Measured 1-h CDPP (eclipses masked, SPOC 2-min): Tmag 10.0 → 120 ppm; 11.0 → 267; 12.0 → 412; 13.0 → 716. No LC product found for the Tmag 14 and 15 sample stars | hands-on (g1_noise.csv) | VERIFIED (one star per bin) | 2026-10-19 |
| P8 | TOI-1338 binary from S97-98 data: P = 14.6084 d, T0 = BTJD 3937.1450, primary 4.7 h / 5.13%, secondary at phase 0.454, 6.1 h / 0.40% | hands-on (BLS) | VERIFIED | 2026-10-19 |
| P9 | A transit-like event at BTJD ≈ 4025.5-4025.8 (≈ 2025-12-16), depth ~0.22-0.25%, present in SPOC PDCSAP, SAP, 20-s and QLP light curves; robust in 21/21 detrendings; no quality flags within ±1 d; nearest momentum dump 1 d earlier | hands-on (toi1338_event_check.py/.png) | VERIFIED (as a signal in the data); interpretation as TOI-1338 b = Claude's ~70% prediction | 2026-10-19 |
