# FIX 95 bench pricing and the combined test (Claude Opus 5.5 high, written 14 Nov 2026, 9:02 pm Kuwait, BEFORE any run)

**What is tested (one run, same harness as RS-024, `research/stage3/rs029/rs029_bench.py`):**
- **OAE** (baseline, the adopted fairness fix): must reproduce RS-024's OAE row (527 dips / 514 bumps new, P 0.4828, background 176 / 83). Identity check.
- **OAEk** = OAE plus the known spacecraft-events hold (FIX 95): an event whose box touches a known interval of `research/stage3/rs028/known_events.csv` (19 intervals from the HEASARC sector notes, padded 0.1 d) is held like a gap or dump event (both arms, same rule).
- **OAED** = OAE plus DS (RS-025: the dump zone holds only an uneven baseline, side lift over 0.25 of the depth or unmeasured).
- **OAEkD** = all three together.

**Pass rules (written now, not tuned on the result):**
1. OAEk is a safety fix, not a planet fix. It is adopted for Petrova 1.1 if (a) P falls by at most 0.5 points against OAE, (b) the paired control still passes in all five bins, (c) the tier-1 upside-down background is not higher than OAE's, and the real background is not higher either.
2. OAED and OAEkD are planet fixes: Tree rule 1. Adopted only if P rises against OAE AND the upside-down background is not higher than OAE's AND the paired control passes in all five bins.
3. If OAEkD passes rule 2 and OAED does not, the combination is the candidate (the known-events hold pays for DS's extra false alarms). If neither passes, DS stays filed for Fable's trade-off round (Monday) and only OAEk can go forward.
4. Every result is a bench number on the design stars (one key, Claude); Codex's T156 bench is the second key before any freeze.
