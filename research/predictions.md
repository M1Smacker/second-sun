# Claude's prediction scoreboard

Each time Claude rates a candidate or makes a forecast, log it here; fill in the outcome later. Over time this shows how far to trust Claude's calls.

| Date | Prediction | Confidence | Outcome | Right? |
|---|---|---|---|---|
| 2026-10-19 | The transit-like dip in TOI-1338 Sector 98 at BTJD ≈ 4025.5-4025.8 (≈ 2025-12-16, ~0.22-0.25% deep) is a transit of the known planet TOI-1338 b (not a systematic, blend or new body) | ~70% | pending (pixel/centroid check + comparison with published transit-time predictions) | |
| 2026-10-19 (update after pixel check) | Same TOI-1338 S98 event is a TOI-1338 b transit | ~80% (raised from 70% after C6 pass: on-target dimming, no centroid shift) | pending (published-ephemeris comparison) | |
| 2026-10-19 (outcome, burn-1) | Same TOI-1338 S98 event is a TOI-1338 b transit | ~80% | **RIGHT.** Wang & Liu 2024 (arXiv:2404.18415, Table 3) predicted a TOI-1338 b transit on 2025-12-16 02:13 UTC = BTJD 4025.5927 +- 0.0159, lasting 6.31 +- 0.15 h. Our fit: mid-time BTJD 4025.632 (white-noise +-0.002 d; true error likely larger), duration ~6.4-6.5 h. Same night, same duration; ours is ~57 min later than predicted (~2.4 sigma using the paper error). Depth ~0.24% matches. See research/burn-1-science/report.md | yes (timing offset ~1 h noted) |
