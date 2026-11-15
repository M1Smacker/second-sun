# Brief 023 (big run A1): the full candidate matrix for Petrova 1.1 (Claude, 15 Nov 2026, 5:30 pm Kuwait; Ahmed's go 5:28 pm)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why this matters
Ahmed asked for the strongest use of Astra and Fable this weekend: a real step towards finding a planet. Our planet-level chance is P 0.48 (adopted set B, 48.11%); a G1 GO needs **P at least 0.50 and its lower 95% bound at least 0.40** (`research/stage3/G1-PLANET-BAR.md`). Every candidate fix so far was scored alone or in pairs. Your 014 part 3 showed the FIX 96 depth cap (2 Jupiter radii on the TIC radius) removes 50 real and 26 upside-down background events and costs 0 of 264 planted dips. That freed upside-down budget may now pay for planet-freeing changes that were held for adding a few upside-down alarms (DS, FIX 94). Nobody has scored them together on the same benches. Fable decides Petrova 1.1 on Monday evening from YOUR table: this is her main input.

## The configurations (all on your harness copies; frozen pipeline files untouched)
- **B** = adopted set: repeater rule b + symmetric FIX 91 + OAE + known spacecraft events K (must reproduce P 48.11%, T156 reference R 34.21%, background 174 real / 79 upside-down; if your code differs, report both and explain).
- **C96** = FIX 96 depth cap as in your 014 part 3 (2 Jupiter radii on the TIC radius).
- **DS** = the dump-shape rule as in your 013.
- **M1, M2** = FIX 94 mask timing V1 (padding off) and V2 (recentred and capped) as in 010 and 011.
- Score these eight: **B; B+C96; B+DS; B+C96+DS; B+C96+M1; B+C96+M2; B+C96+DS+M1; B+C96+DS+M2.** Do not add the 014 part 2 eclipse times (they failed their preregistered controls).

## Measures, for every configuration
1. Planet bench: P on the 1,098 (equal-bin, as 006 and 013) with its whole-star bootstrap 95% interval (10,000, fixed seed); planets gained and lost against B, per binary-period bin.
2. T156 reference R with its interval.
3. Untouched design light, both arms, both campaigns (as 013): tier-1 background real and upside-down; the spare upside-down budget = 79 minus the count.
4. Paired dip-against-bump control per bin (99%, 10,000 whole-star bootstraps, fixed seed), pass or fail per bin.
5. **Blind-spot checks (the upside-down arm cannot see these):** for every real tier-1 background event that is new against B: hours to the nearest momentum dump (your 014 part 1 map and its excess window), and whether it sits within one eclipse width of a catalogue eclipse time (eclipse leftover, RS-027). Count both per configuration.

## Pass rule (copy it into the report BEFORE scoring; nothing tuned after seeing outputs)
A configuration is a **GO candidate** only if ALL hold: (a) P at least 0.50 and lower bound at least 0.40; (b) upside-down background at most 79; (c) the paired control passes in every bin; (d) real background at most 174; (e) new real events in the dump excess window or at eclipse leftovers number at most 5. Rank GO candidates by the P lower bound. If none passes, say which rule each configuration fails and by how much: that is just as useful to Fable.

## Also (your method, for the skill Ahmed wants)
Keep `research/astra/reports/023-worklog.md` WHILE you work, short dated lines: what you looked at first and why; what you deliberately did not do; the check that could have proven you wrong and whether you ran it; when you stopped reading and started computing; each decision (options, evidence, choice); where you changed your mind. Steps, choices and evidence only. Fable will read it next to her own logs to write one method skill for every Claude and Codex model.

## Rules
Branch `astra/023-candidate-matrix` from the latest main. Cap: 60 five-hour points; machine time free; long fits in the background; one blocking wait at most; never poll. Star-level rows only under `data\astra\023\`. Fence A and fence B stars never; no G1 or sealed data; never push, never publish; nothing outward.

## Report
`research/astra/reports/023-candidate-matrix.md`: the plain verdict line first (how many GO candidates, the best one with P and its interval); the eight-row table (P and interval, R and interval, real, upside-down, spare budget, control bins failed, dump-window and eclipse-leftover new real events); the pass rule as written before scoring; what you did NOT check; usage.
