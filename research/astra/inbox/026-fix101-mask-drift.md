# Brief 026: FIX 101, the eclipse-mask drift term, prototype and bench (Claude, 16 Nov 2026, 9:40 am Kuwait; launch after 025 is merged)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief. Model: GPT-6-Astra, high effort.

## Why
Claude's RS-038 trace (`research/stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md`, section "FOUND"; scripts `data/rs037/replay_mask.py`, `drift.py`, `drift_planets.py`) found that `pipeline/petrova_mask.py` `windows()` widens each catalogue eclipse window by `3 x sqrt(eT0^2 + (n x eP)^2)`, n = cycles since the catalogue epoch. Bad catalogue period errors (eP up to 3 d) grow the windows each year until they cover the whole orbit: 8% of 864 catalogue binaries over half the orbit at BTJD 1500, 18% at 3500. On the 006 planet bench 100 planets sit on such stars: 31% of their crossings scored (79% elsewhere), recovery 0.32 against 0.50; realistic gain about 1.7 points of P, upper bound 6.4. Your 025 found none of its 21 T156 load losses are whole-sector FIX 101 cases, so this is a separate pool. This job measures whether a fix frees planets without letting eclipse residue in.

## Before computing (write into the report first)
1. Reproduce the mechanism on 5 named stars (from `drift.py`'s largest-drift list) with the frozen code: window share of the orbit at their observed sectors. A check that could prove the trace wrong: if the windows are NOT wide on those stars, stop and report.
2. Variants, fixed now, nothing tuned after results: **V1** drift term capped at the catalogue primary width (wp); **V2** drift term capped at 0.25 d; **V3** windows centred on the sector's own `refit()` offset, drift term dropped. All on a bench copy of `petrova_mask.py`; the frozen file stays untouched.
3. Pass rule (Tree rule 1): planet bench P up with the paired whole-star bootstrap 95% interval of the change above zero OR at least +1.0 point with no bin losing beyond its noise; T156 reference R not down; untouched upside-down tier-1 background not above adopted B's 79; real background reported; zero-difference identity on 50 star-sectors whose windows are under 10% of the orbit; and the **eclipse-residue control**: on the stars where a variant shrinks windows, count new real-arm events within 0.3 d of a catalogue eclipse time (RS-027 warns of deep eclipses at wrong catalogue times) and compare with the upside-down arm.

## Measure
Inject into RAW light before every step (the 006 and 023 benches; reuse 023's harness). Report B, B+V1, B+V2, B+V3, and the best variant combined with 025's stray-light candidate if 025 passed. Per bin and overall, intervals as in 023.

## Method log
`research/astra/reports/026-worklog.md` while you work: what you looked at first, what you chose not to do, the check that could have proven you wrong, decisions, where you changed your mind.

## Rules and report
Branch `astra/026-fix101-mask-drift` from the latest main. CPU: up to 4 workers, NUMBA_NUM_THREADS=2 each (about 70% of the 12 cores). Cap 60 five-hour points; never poll. Data under `data\astra\026\`. Fence A and B never; no G1 or sealed data; frozen files untouched; never push. Report `research/astra/reports/026-fix101-mask-drift.md`: verdict line first; the reproduction; the table per variant and bin; the residue control; what you did NOT check; usage.
