# F2: silent losses, the hunt for a second F-01 (Fable, 16 Nov 2026)

**Verdict in one line: found something, but not a free win. (1) The planet bench that defines P cannot see the first step of the chain: it only counts a crossing if the light is still there AFTER the quality mask. Counted from the raw archive, one planted crossing in four (1,525 of 5,914) is lost before the search starts, a ceiling of about 9.7 points of P. (2) The biggest single cause is one quality bit, "scattered light" (value 4096), which removes crossings twice: in SPOC files at load and in QLP files through the safe windows. (3) Simply dropping that bit is NOT safe: the light it guards makes 6 to 9 times more strong events per day, on both arms. (4) One small rule is safe at detector level and can go to the bench now: QLP star-sectors with exactly one SPOC neighbour are thrown away for no measured reason.**

Scripts and outputs: `data/fable/f2/` (`census.py`, `summary.py`, `prototype.py`, `proto_summary.py`, `orbits006.py`). Design stars only; the frozen pipeline is read, never edited.

## 1. The blind spot in the bench (CONFIRMED by reading the code and by count)
Codex 006's generator (`006_planet_generate.py`, branch astra/006-branch-one) keeps a planted crossing as "observed" only when the LOADED light of the best product has a cadence there, and loading applies the hard quality mask. So:
- 606 planted crossings that have raw cadences are not in the bench at all (399 lost at load, 129 at the safe windows, 78 others);
- 30 planets with raw crossings are outside the 1,098; on the 1,128 raw-observable planets B's P is **46.8**, not 48.1;
- worse for the future: a fix at load ADDS crossings and planets to the denominator, so the bench can show a true gain as no gain or as a loss.
This is the same kind of fault as F-01 on 10 Nov (planets planted after the step that kills them), one step earlier in the chain. T156 plants at random times and did see part of it (Codex 025: 21 of 222 at load).
**Proposal:** the next bar file (Ahmed's, see F1) should define "observable" from raw cadences (any product, no quality mask), so load and window fixes can be scored.

## 2. Where planted crossings stop, from raw data (CONFIRMED as computed)
`census.py` follows all 1,250 drawn planets (and the 2,000 T156 dips) through every product. 5,914 crossings have raw cadences.

| First step that loses the crossing (best product) | Crossings | Planets touched | Planets with no scored crossing today | Ceiling, planets | Ceiling, points of P |
|---|---|---|---|---|---|
| Reaches a box score | 4,389 | | | | |
| Eclipse mask | 507 | 260 | 63 | 42.7 | 3.8 |
| QLP safe windows | 511 | 348 | 56 | 41.7 | 3.7 |
| Load (quality mask) | 404 | 305 | 46 | 30.7 | 2.7 |
| No finite score (gap or edge) | 103 | 89 | 9 | 6.5 | 0.6 |
| All four | 1,525 | | | 109.8 | **9.7** |

Ceiling = planets gained if every such crossing were scored, using B's own measured curve (found with 0 scored crossings 0%, 1: 29%, 2: 51%, 3: 59%, 4: 59%, 5 or more: 75%). It is an upper bound: it assumes rescued crossings are as clean as the rest.

Checks that could have failed: no planet in P lacks raw crossings (passed); file errors 0 of 654 stars; T156 Saturn-like dips by the trial's own product give load 17, windows 8, no raw data 18, mask 9, against the Tree's 21, 23, 15 and 15: the same order of size, not identical (my test needs 3 cadences inside the dip and files "too little data" under mask). Label for the table: CONFIRMED as counted, LIKELY as a forecast.

## 3. Ranked silent losses
| Rank | Loss | Crossings | Ceiling (points) | Physics or rule? | State |
|---|---|---|---|---|---|
| 1 | **Scattered-light bit 4096 in the hard mask**: 269 at load in SPOC files, plus 175 QLP crossings cut because the QLP star takes its windows from its own SPOC file's hard mask | about 444 to 579 | about 4 | a rule over real dirt | prototype below: gain 1.0 to 3.1 points, but the admitted light is 6 to 9 times dirtier |
| 2 | **Eclipse-mask padding** (FIX 94 = FIX 101): 241 crossings in sectors where the mask removed over half the light; another 159 truly sit at an eclipse time (physics) | 241 | about 1.8 | a rule | benched three times already (M1, M2: +1.4 points measured); design in F1 section 4 |
| 3 | **"No safe windows"**: a QLP star-sector with fewer than two SPOC neighbours on its CCD is dropped whole | 168 (one neighbour 126, none 42) | about 1.2 | a rule, never measured | prototype below: clean; ready for the tier bench |
| 4 | **Neighbour intersection**: QLP light is kept only where EVERY SPOC neighbour has good time, minus half a day after each gap | 168 | about 1.2 | a rule | a majority rule would keep 198 of the 336 crossings in ranks 3 and 4; not prototyped, because rebuilding the window table opens other stars' files (fence) |
| 5 | QLP's own bad-quality flag at load | 180 | about 1.2 | unknown | NOT TESTED |
| 6 | No finite score: 29 at the end of the light, 69 inside gaps (the 80% coverage rule) | 103 | 0.6 | mostly physics | leave |

A warning that belongs with rank 4 (LIKELY, not measured): the intersection shrinks as a campaign holds more SPOC stars per CCD. G1 has many more stars than the benches, so G1 would lose more QLP light than any bench shows. FIX 70 ("QLP events depend on which files are in the manifest") is the same weakness seen from the other side.

## 4. Prototype for rank 1 and rank 3 (detector level)
Variant LW1, fixed before the run (`prototype.py`, a wrapper, no pipeline file edited): (1) SPOC and TESS-SPOC read with the hard mask minus bit 4096; (2) a QLP star with its own SPOC file takes its windows from that file read the same way; (3) a QLP star-sector with exactly one SPOC neighbour uses that neighbour's windows.

**Failing-first test:** for all 1,055 crossing-and-file pairs, the frozen chain with the planet planted gives no score at the crossing: 0 of 1,055 scored. Under LW1:

| Family | Pairs | Scored | SNR 7 or more | SNR 7 or more and nothing there before planting |
|---|---|---|---|---|
| SPOC load, bit 4096 | 754 | 610 | 323 | 215 |
| QLP, windows from own SPOC | 175 | 147 | 79 | 63 |
| QLP, one neighbour | 126 | 106 | 29 | 24 |

605 different crossings tested, 498 scored, 185 detected cleanly. 16 planets that have no scored crossing today get a clean detection. Expected gain with B's recovery curve: **1.0 point of P counting only clean detections, 3.1 points if every scored crossing counts** (LIKELY; detector level, not tier 1).

**The cost (untouched light, SNR 7 or more events per 100 days, real / upside-down):**

| | Light searched today | Newly admitted light |
|---|---|---|
| SPOC and TESS-SPOC (679 files, +3,018 days) | 1.9 / 1.6 | **16.9 / 15.5** |
| QLP with own SPOC windows (155 files, +664 days) | 2.2 / 1.9 | **13.3 / 12.0** |
| QLP with one neighbour (94 files, +1,600 days, all new) | | 2.3 / 3.1 |

Reading:
- The scattered-light flag is not empty caution. The light it removes throws strong events about 8 times as often, equally on both arms (so it is instrument dirt, and the upside-down meter does see it). In 82 of 754 pairs there was already an SNR 7 "dip" at the planted time before any planet was added. **Dropping bit 4096 as it stands would very likely fail Tree rule 1.** Whether the tier flags (step, ramp, common moment) absorb the extra events is exactly what Codex 025's tier-level bench measures; Claude is finishing it. My numbers say: expect many more upside-down alarms unless a guard is added.
- A guard worth testing (NOT TESTED): admit a flagged stretch only when the star's own detrended scatter inside it is no more than 1.5 times its scatter in the unflagged light of the same sector; same rule on both arms; pass rule as in F1 section 5 with upside-down alarms not above B.
- **The one-neighbour rule is the clean one:** 1,600 days of light come back at a normal event rate (2.3 real per 100 days against 1.9 to 2.2; upside-down 3.1 against 1.6 to 1.9, a little high on 49 events). Gain about 0.1 to 0.6 point. Small, safe, and it removes a rule nobody had measured. Ready for the tier-level bench.

## 5. What I did not find
No second F-01 of the "pure bug" kind in the steps I followed (load, safe windows, mask, box score). Every large loss sits behind a rule that guards against something real; the faults are that two of the rules are cruder than they need to be (ranks 3 and 4), one was already known (rank 2), and the bench was blind to the first step (section 1). Not followed in F2: detrending and the tier flags (F4 covers the flags), the 20-second products, and QLP sectors 94 on (a new quality bit, value 2^30, removes about 22% of some files: 30 crossings here).

## 6. For Claude
- Brief 026 (FIX 101): see F1 section 6. Its three variants repeat M1 and M2; its eclipse-residue control cannot fail on stars whose catalogue period is wrong.
- Codex 025's stray-light candidate: judge it on upside-down alarms first; and do not judge it on P as defined today (section 1), use T156 or a raw-observable denominator.
- Next bench job from F2, in order: (a) the one-neighbour rule at tier level; (b) the scatter guard for bit 4096; (c) a majority-window rule built from spacecraft-level times only.

## Labels
CONFIRMED: sections 1 and 2 as counted; the failing-first test; the event rates in section 4. LIKELY: ceilings and gains in points (recovery-curve estimates, detector level). NOT TESTED: tier-level effect of any variant, the scatter guard, the majority rule, the G1 scaling of rank 4.
