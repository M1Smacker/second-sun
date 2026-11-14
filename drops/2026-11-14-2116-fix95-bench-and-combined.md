---
type: finding
node: 1.6
date: 2026-11-14 21:16
label: CONFIRMED
status: open
by: Claude
links: [research/stage3/rs029/FIX95-AND-COMBINED-RULE-2026-11-14.md, research/stage3/rs029/bench.json, research/stage3/rs029/rs029_bench.py]
ids: [RS-029 (bench pricing of FIX 95, the combined test, FIX 91 and FIX 92), FIX 95 (known spacecraft events not flagged), OAE (the adopted fairness fix for the 'dominated' flag), DS (dump zone judged by baseline shape, RS-025)]
supersedes: []
---
**Plain:** Flagging NASA's known spacecraft trouble moments passes our rule: it costs almost nothing and removes 4 false alarms. Combined with the dump-shape rule, it lifts planet recovery to 49.98% with no more upside-down alarms, just under the 50% line G1 needs.
**Why it matters:** the first combination that gains planets without more upside-down alarms; it goes to Fable's round on Monday and Codex's second key.
**Explanation:** On its own, the known-events flag loses 2 planets out of about 1,100 and removes 4 upside-down and 2 real false alarms. The dump-shape rule alone adds 20 planets but also 4 upside-down alarms; the known-events flag cancels exactly those. Caution: the real-light alarms rise by 28, and the upside-down meter is partly blind near dumps, so the real cost may be higher than it looks.
**Technical:** P (equal weight) OAE 0.4828, OAEk 0.4811, OAED 0.5016, OAEkD 0.4998; tier-1 background real/upside-down 176/83, 174/79, 207/87, 204/83; paired control passes in all 5 bins for all four. Rules written before the run.
