---
type: fix
node: 3.1
date: 2026-11-14 21:09
label: CONFIRMED
status: done
by: Claude
links: [pipeline/gate_judge.py, pipeline/test_gate_judge.py, pipeline/r1_gate.py, pipeline/s1_sensitivity.py, pipeline/test_s1_sensitivity.py, pipeline/r1_readout.py, research/stage3/FIX-QUEUE.md]
ids: [FIX 86 (the readout's power line used the wrong test), FIX 87 (gates said PASS on untested period bins)]
supersedes: []
---
**Plain:** Two of our statistics tools told small untruths; both are fixed and tested before G1 uses them.
**Why it matters:** G1's verdict will be printed by these tools, so they must say exactly what was tested and what a null can and cannot rule out.
**Explanation:** The gate tool said PASS for the slow-binary bins even when no test dips had been planted there; it now says "PASS ON TESTED BINS (3 of 5)". The readout's "power" line used a simpler test than the real verdict and called its result an exclusion; it now runs the real rule on simulated strong signals and calls the result a sensitivity.
**Technical:** gate_judge: PASS, FAIL, PASS ON TESTED BINS, INCOMPLETE; rerun on sealed G3 rows: numbers identical. s1_sensitivity: 8 filed chances reproduced; crossings G3 55 and 60 added, G2 60 and 70 (equal to Codex 002); mutation red. Filed results unchanged.
