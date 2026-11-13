# 005 part 0. Combined baseline, node 1.1 (GPT-6.1 Sol, effort unverified)

**Verdict: combined baseline passes all three 004 gates. R 33.34% [25.88%, 40.10%]. Background real 176 and upside-down 83.**

| Configuration | Reference R and 95% interval | All-depth dip / bump | Background real / upside-down |
|---|---|---|---|
| Petrova 1.0.0 | 27.47% [20.72, 33.71] | 394 / 400 | 123 / 70 |
| Repeater alone | 33.34% [25.88, 40.10] | 496 / 483 | 176 / 85 |
| FIX 91 alone | 27.47% [20.72, 33.71] | 394 / 399 | 123 / 68 |
| Combined | 33.34% [25.88, 40.10] | 496 / 482 | 176 / 83 |

| Binary period (days) | Reference dips recovered / n | All-depth dip / bump of 400 | Paired dip-minus-bump 99% interval (points) |
|---|---|---|---|
| 5 to 10 | 7 / 48 | 60 / 63 | [-3.83, 2.30] |
| 10 to 14 | 11 / 35 | 97 / 93 | [-2.32, 4.27] |
| 14 to 20 | 16 / 46 | 92 / 95 | [-4.41, 2.98] |
| 20 to 27.4 | 23 / 47 | 113 / 94 | [-0.67, 12.21] |
| 27.4+ | 17 / 46 | 134 / 137 | [-5.11, 3.84] |

PASS R rises from 27.47%. PASS background upside-down 83 is within 86.85. PASS all five paired 99% intervals contain zero. The combined candidate still falls below the filed G1 threshold.

CONFIRMED runtime replay on 14,835 baseline group files, 37,105 stored pre-union tiers, 4,000 final recovery decisions and 2,000 paired draws. Old outcomes and stored tiers agree, and the old bootstrap matches 003. No unresolved rounded-centre cases. Individual 004 results came from the saved 004 summaries. The original matching and prior-event exclusion are fixed. The one-hour rule and reverse coincidence logic follow 004. No full final-tier oracle exists for individual saved events.

Harness changes: 12 sprint003 copies verified and copied to sprint005. Four output-path literals moved to 005 (audit_all, dataset, stage2_search, stage3_report). Science code copies are otherwise identical to sprint003. Both adopted flags are applied to saved events in 005_replay.py, then SAP merge and downstream tiering run. Part B uses this same copied detection path since both changes act after detection. No pipeline source edits or version freeze.

STOP SIGNS: none for this replay. QUEUE PROPOSALS: node 1.1, file the combined baseline and track the real-side rise. IDEAS: none. Questions for Ahmed: none. Usage shared with A and B and logged in the combined report. Branch astra/005-three-diagnoses.
