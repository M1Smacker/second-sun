# Wave 7: anomalies side quest (PARTIAL)

*Second Sun research, wave 7. Run inline by the main session (Claude, Opus 5.5) on 2026-10-19 from 17:38 UTC. Reading wave (abstract level). Claims A7-1… in `claims.md`.*

---

## In plain words (read this first)

People *have* started hunting weird things in TESS with "let the computer find the odd ones" methods, but the field is young:
- **Unsupervised anomaly searches** exist: one in 2023 linked odd light curves to star properties, and CLARA (2025) is an unsupervised transit finder (A7-1, A7-2).
- **Exocomets:** a 2025 search looked for comet-shaped dips (sharp drop, slow recovery) across TESS's first two years (sectors 1-26) only (A7-3). **Years 3-8 of TESS data haven't been searched that way**, as far as tonight's search shows. That's a gap that fits our "newest sectors" theme.
- **Disintegrating planets:** TESS found **BD+05 4868 Ab** (2025), a rocky planet falling apart with comet-like tails around a bright star (A7-4). These are rare, and each new one makes news.

**What this means for us:** the side quest is real. A first concrete version would be an **exocomet / asymmetric-dip search in sectors 27+** on the same light curves we download for the main quest. It costs almost no extra data, and the cool finds feed the gallery and the VSX side wins.

## Sources found (abstract level)
| ID | What | Year |
|---|---|---|
| arXiv:2301.10264 | Crake et al.: unsupervised exploration of anomalous TESS light curves, linked to stellar properties | 2023 |
| arXiv:2508.04722 | Dasgupta et al.: CLARA, unsupervised random forests for transit detection in TESS | 2025 |
| arXiv:2508.04673 | Norazman et al.: search for single exocomet transits in TESS Sectors 1-26 (magnitude-limited sample) | 2025 |
| arXiv:2501.05431 | Hon et al.: BD+05 4868 Ab, a disintegrating rocky planet with comet-like tails, P = 1.27 d, V = 10.16 K dwarf, found by TESS | 2025 |

## Not done (carry over)
- Read Norazman+ 2025 in full: method, sample, results, occurrence rate, and whether its code is public.
- Beta Pictoris exocomets in TESS (Zieba+ 2019?); the search hit was cut off by a console encoding error.
- Tabby's-Star-like "dipper" searches in TESS.
- Hardware fit: which anomaly methods run on 16 GB RAM + CPU.
