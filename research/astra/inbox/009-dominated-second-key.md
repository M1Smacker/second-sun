# Brief 009: second key on RS-024 and the fairness fix (note from Claude, 14 Nov 2026, 12:30 Kuwait). Replaces 008.

**What changed since 008:** your 008 is read (branch astra/008-after-006, fence check clean 11:50, not merged). Claude ran research stint RS-024 on the root cause of "dominated": `research/stage3/rs024/DOMINATED-RESEARCH-2026-11-14.md` (read it all). In short:
- The rule assumes sign-symmetric light; in our binaries the strongest dip beats the strongest bump in 58% of light curves, 62 to 64% in slow binaries (`rs024_symmetry.py`).
- Clean strong off-catalogue dips recur at the binary phase far above chance (missed eclipses); bumps do not (`rs024_phase_null.py`).
- Of the rivals holding planted bumps in the slow bins, 13 of 21 and 9 of 23 carry the chain's own eclipse or repeat labels (p1_veto, orbit_lock, repeater), which are set AFTER dominance is computed (`rs024_rivals.py`).
- Literature (Kepler DR25 Chases and model-shift, LEO-Vetter, mono-cbp) in the file.
- Preregistered planet-bench test (`rs024_options.py`, identity exact on 1,250 trials): OAE (rivals labelled eclipse or repeat ignored, plus either-sign comparison within 6.85 d outside 1.5 durations) passes the paired control in every bin, background 176/83 unchanged, -2 of 1,098 planets.
- **Ahmed amended the Tree rule (14 Nov):** a fairness fix counts when it makes a failing paired control pass, adds no upside-down false alarms, and costs at most about 0.5 points of P.

**Your order (cap 40 five-hour points, one blocking wait at most, never poll):**
1. **Second key on RS-024, your own code** (read-only on main's files; do not import Claude's rs024 scripts): reproduce (a) the per-bin dip-beats-bump share in untouched design light, (b) binary-phase recurrence of clean strong off-catalogue dips against a chance level you choose and state first, (c) the eclipse or repeat labels on the rivals that hold planted bumps. Agree or disagree with numbers.
2. **Measure OE, OA and OAE exactly as defined in the file's test plan** on the T156 bench (2,000 paired draws, with the 222 reference draws) AND your 008 harness for the planet bench and background. Report per option: R, P, gains and losses each arm, upside-down and real background, paired control per bin (99%). Verdict under the amended rule.
3. No new fix designs this round. The next fixes (step, gap/dump, ramp, FIX 92) wait for Claude's research stint RS-025.
4. Write `reports/009-dominated-second-key.md` on a new branch `astra/009-dominated` from main. Do not push. Usage in every reply. Say in the report if you stop any process of your own.

Fences, push ban, frozen files unchanged. Fence A and fence B stars: never.
