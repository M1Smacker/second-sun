# Outside check of the Petrova 1.0.0 pass marks and freeze list (brief for a nested Opus 5.5 medium, written 11 Nov 2026)

You are an independent checker. You do NOT fix, edit, commit or run searches. You read, run small read-only scripts if you must, and report. **Stop after 30 tool calls** and report what you have, even if unfinished. Before reading anything, write down your PREDICTION: which of the marks do you expect to be weak, and why (3 lines). Then check it.

## What this is
Second Sun searches TESS light for planets orbiting two stars. The old filter (Vesper 0.8.1) deleted planet dips in slow binaries (audit F-01). The new filter (Petrova 1.0.0, a switch `p1` on top of 0.8.1, run as `VESPER_OPTS=c6,p1`) keeps them. Nothing is frozen yet. Ahmed (the owner) reads on a phone and knows little jargon, so your report must be plain. The rules were written BEFORE the search in `research/stage3/R1-PREREGISTRATION.md` (read section 4, 5 and Amendment 1). The test code is `pipeline/r1_gate.py`, the mask and veto code is `pipeline/petrova_mask.py`, the freeze code is `pipeline/r1_run.py` (function `freeze`).

## Results to judge (counts only; never open an event)
- `research/stage3/R1-GATE-RESULT-g3.txt` (done) and `research/stage3/R1-GATE-RESULT-g2.txt` (must exist before you start; if it does not exist, stop and say so).
- Facts I already see in the G3 file (check them, do not just repeat them): (a) and (b) pass with m 0.99 to 1.00 in every bin; (c) is judged in ONE bin only (5 to 10 d, 23 events, ratio 1.09) because every other bin has fewer than 20 events, so it passes almost by default; the unjudged bins read 14 to 20 d real 13 / upside-down 2, 20 to 27 d 4 / 0, over 27 d 5 / 0; (d) vetoed events real 95, upside-down 10; tier-1 events in recovered light real 33, upside-down 8.

## Questions (answer each in 2 to 4 lines, with a label CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED)
1. **Can gate (a) fail?** Does the "after the mask" comparison go through the same veto, flags and tiers as the "before the mask" one? If a dip that the veto kills is killed in both, m would hide it. Is there any path by which the mask or veto could delete injected dips and still give m of 1.00? (Read `r1_gate.py` `install`, `baseline`, `_run_group`.) Is the recovery of 38 to 52 percent plausible for K 8 to 25 and the stated durations, or does it show something wrong?
2. **Is the mirror rule kept in the test?** Same cadences, same windows, same injection for `f` and `2 - f`; is the flip applied after the injection correctly (a bump of the same size)?
3. **Gate (c):** with only one judged bin, is the pass meaningful? I do NOT want to change the preregistered mark. I want to know: does the pooled picture (all bins together, both G3 and G2) show a real-arm excess that the marks did not judge, and would that endanger the sealed run's meaning (S1 uses the upside-down count scaled by the real-to-upside-down ratio measured on the run itself)? Say whether the 14 to 20 d bin (13 vs 2) is a problem or noise (a plain binomial probability is fine).
4. **Veto asymmetry (d):** 95 real against 10 upside-down vetoed. Is that what a correct veto should give (real-arm eclipse leftovers repeat at the same binary phase in other sectors, upside-down bumps do not)? Or does it show the mirror rule broken? Only an argument you can support from the code or a small count; no story.
5. **Recovered light, 33 vs 8:** this is a RESULT to report, not a reason to change the definition (Amendment 1 says so). Is there anything in the code that would make the real arm get more events in recovered light for a reason other than the planet-free noise or the eclipse residuals? One paragraph.
6. **Freeze list:** list every file that differs between Vesper 0.8.1 and the current tree that the freeze hashes (see `pipeline/stage3.py` `current_settings`, `pipeline/r1_run.py` CHANGED_FILES) and say whether anything that changes search results is NOT in the hash list (for example `r1_gate.py` is test code and should not change results; `targets_r1.py`, `targets/r1_targets.csv`, the catalogue tables `data/xmatch/ebs.csv` and the TTC table: are they hashed or at least pinned?). What would change the events silently after the freeze?
7. **Anything else** that could make the sealed run answer a different question than the one written in section 6 of the preregistration. Max 3 items, ranked.

## Rules
- Do not edit any file under `pipeline/`, `research/stage3/` or `targets/`. Do not commit. Write your report only as your reply (I will file it).
- Do not print or list real events, star ids or event times; counts only.
- Use `D:\second-sun\.venv\Scripts\python.exe` for Python. No downloads. No web.
- Plain words, short. No en or em dashes. Start with a verdict line: "Freeze can go ahead", "Freeze can go ahead after these N fixes", or "Do not freeze", then the answers. Report the number of tool calls you used.
