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

## Result (read 9:16 pm, 14 Nov 2026; Claude, one key; `bench.json`, trials `data/rs029/bench-trials.csv`)
Identity: OAE reproduces RS-024 exactly (527 dips / 514 bumps new, P 0.4828, background 176 / 83). The rs024 files were backed up and restored (no diff).

| Option | Dips new | Bumps new | P (equal weight) | Paired control, all 5 bins | Tier-1 background real / upside-down |
|---|---|---|---|---|---|
| OAE (baseline) | 527 | 514 | 0.4828 | passes | 176 / 83 |
| OAEk (FIX 95) | 525 | 513 | 0.4811 | passes | 174 / 79 |
| OAED (DS) | 547 | 532 | 0.5016 | passes | 207 / 87 |
| OAEkD (both) | 545 | 531 | 0.4998 | passes | 204 / 83 |

**Verdicts under the rules written before the run:**
1. **OAEk PASSES rule 1** (P -0.17 points, under the 0.5 limit; paired control passes; upside-down 83 to 79; real 176 to 174). Candidate for Petrova 1.1. CONFIRMED on the design bench (one key).
2. **OAED FAILS rule 2** (upside-down 83 to 87).
3. **OAEkD PASSES rule 2 as written** (P 0.4828 to 0.4998, +18 dips; upside-down 83 to 83, not higher; paired control passes). By rule 3 the combination is the candidate, not DS alone: the known-events hold pays for DS's 4 extra upside-down alarms.
**Honest cautions (not a change of verdict):** (a) the upside-down count is EQUAL, not lower: a knife edge, inside counting error either way (Poisson sd about 9); (b) the REAL background rises 176 to 204 (+28, +16%), mostly in the 5 to 10 d and 27.4+ d bins; RS-025 showed the upside-down meter is partly blind near dumps and gaps, so some of those 28 may be dump artefacts the control cannot see; (c) P 0.4998 is 0.0002 under the G1 GO line of 0.50: this does not reach G1 by itself; (d) the DS threshold 0.25 was chosen after seeing design-bench shapes (RS-025 note). So OAEkD goes to Fable's trade-off round (Monday) and Codex's T156 second key with these cautions written on it; OAEk alone can go forward as a safety fix.

## Second key: Codex 013 (report 10:02 pm, read 10:14 pm; branch astra/013-known-events-ds, fence check clean for 013, not merged)
- **Identity CONFIRMED:** Codex's independent code reproduces every RS-029 count (B 527/514, P 48.2837%, 176/83; B+K 525/513, 174/79; B+K+DS 545/531, 204/83).
- **T156 (2,000 draws):** B 500 dips / 509 bumps; B+K 499 / 507; B+K+DS 536 / 545. Reference (222): R 34.64% (B), 34.21% (B+K, loss 0.43 points, inside the 0.5 limit by 0.065), 35.50% (B+K+DS).
- **Gates:** B+K passes all six; B+K+DS passes all five. Two keys now agree on both.
- **Root cause of the real rise (CONFIRMED counts, LIKELY reading):** on untouched light DS frees 30 real and 4 upside-down tier-1 events (7.5 to 1; the baseline background is about 2.1 to 1); 12 of the 30 real boxes contain a dump and 23 of 30 sit BEFORE the nearest dump (the C7 pattern: pointing jitter before a dump fakes dips). Planted signals are freed evenly (T156: 37 dips, 38 bumps). So a good part of the +28 real events are LIKELY dump artefacts that the upside-down meter cannot see; the gates pass because their false-alarm meter is blind exactly there. Half the 30 are more than 3 h from any dump, so timing alone cannot sort them (UNCERTAIN fraction).
- **Claude's recommendation:** adopt K (FIX 95) for Petrova 1.1 now (two keys, every gate). Hold DS for Fable's round: the rule passes as written, but its root cause shows a blind spot in the rule itself; any DS variant (for example keeping the hold for boxes before and near a dump) must be preregistered and tested on T156, not tuned on these 30 events.
