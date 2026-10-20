# Burn 1 open questions

1. **Is the +57 min offset real?** The white-noise error (±3 min) is surely too small. It needs a red-noise error (residual permutation or time-averaging β factor) and a detrending-choice check before the offset means anything. If it holds, it is a new timing point for the TOI-1338 b dynamical model (it could constrain planet c). Internal only.
2. **Did S97 catch the 2025-09-14 predicted transit at all?** Our hard-mask S97 LC starts at BTJD 3936.42. Not checked: the default mask, SAP, QLP/FFI coverage of 3932.73.
3. **Method upgrade** (matched-filter single-transit SNR, global eclipse ephemeris, longer/iterative detrend, SAP fallback): after it, re-run recovery.py + inject.py as acceptance tests. Target: all 6 testable published transits, and ≤5 R⊕ at Tmag ~11.
4. **False events at S6 1471.56 (3,754 ppm) and S65 3090.20 (4,200 ppm)** in the 1-d-window run: what are they (eclipse-mask edges, systematics)? Not investigated.
5. Kostov+2020's own transit-time predictions were not read. Wang & Liu's "ref. 29" column is probably them (not checked).
6. Injection test used one sector, 8 times per size, one duration (6.4 h), one impact parameter. A real completeness map needs durations 3-15 h and more trials.
