# RS-024: the "dominated" flag, deep research (started 14 Nov 2026, 11:59 Kuwait, Opus 5.5 medium)

**Why (Ahmed, 14 Nov 2026):** Codex 008 tried three one-change fixes for "dominated" and all failed the adoption rule. Ahmed: do not guess again; research it, learn everything, then say whether tests are needed first.

**Cap, written before the start:** 8 weekly points, about 150 tool calls. No helpers. Own data first, then primary sources.

**The rule as frozen** (`pipeline/stage3_core.py` 288 to 294): an event is "dominated" (tier 2) if the strongest event of the OTHER arm (real dip against upside-down, in the same product and star-sector) is at least as strong. The code comment's assumption: "under noise alone real and upside-down dominate each other equally often."

## Questions (each tied to a decision)
| # | Question | Decision it feeds | What our data already says |
|---|---|---|---|
| Q1 | What does the flag buy and cost today (Petrova, T156 + planet bench)? | keep, replace or drop | Codex 008: dropping it gives P +1.1 points (13 dips, 1 lost) and +21 real, +23 upside-down background tier-1 events |
| Q2 | What are the strong natural dips that hold planted bumps in slow binaries? | which replacement can separate them | Codex 008: 42 of 44 already in the untouched light; 0 of 22 in catalogue eclipse windows; 22 with no secondary geometry |
| Q3 | Is "noise alone" the right model? Is the light of eclipsing binaries sign-symmetric off eclipse? | whether ANY whole-curve opposite-arm comparison can be fair | 27 Oct: dominated hit 22% of real and 13% of upside-down events (pre-mask chain) |
| Q4 | How do professional vetters decide that one transit stands out (Kepler Robovetter model-shift, Chases, Marshall; LEO-vetter; single-transit vetting)? | replacement design | NOT TESTED |
| Q5 | How did Kepler DR25 and TESS teams treat inverted light curves of eclipsing binaries and other sign-asymmetric stars? | whether the paired dip-against-bump control is the right gate for this flag | NOT TESTED |
| Q6 | Can any dominance change alone lift P to 0.50? | where the next fix effort goes | Codex 008: dropping it entirely gives 49.5%, so no |

## Findings
(filled below as answered)

### Q3. Is our light sign-symmetric, as the rule assumes? NO. CONFIRMED (own data)
`rs024_symmetry.py` (design stars only, 2,446 light curves with both arms, 21,100 events): the strongest dip beats the strongest bump in 57.8% of light curves (noise alone: 50%). By binary period: 5 to 10 d 54.8%, 10 to 14 d 56.0%, 14 to 20 d 56.4%, **20 to 27.4 d 63.5%, 27.4 d and up 61.9%**; median ratio of strongest dip to strongest bump 1.06 rising to 1.19 and 1.23. So a whole-curve opposite-sign comparison holds planted bumps (compared against natural dips) more often than planted dips (compared against natural bumps), most in the slow bins: exactly the 21 against 6 and 23 against 3 of the planet bench. The code comment's premise ("under noise alone") does not hold for eclipsing-binary light. (Event-level counts; star clustering not bootstrapped; the slow-bin excess, 255 and 509 curves, is far outside binomial error of about 3 to 4 points.)

### Q2. What are the strong natural dips? Mostly missed eclipses plus artefacts. CONFIRMED (own data) and matches the closest published search
- Strong (SNR 7+) winners off the catalogue eclipses carry step, gap or ramp flags in most cases on BOTH sides (artefacts near gaps); the difference between the sides is in the **clean** ones: 139 clean dip winners against 41 clean bump winners (`symmetry.json`, part B).
- **Clean strong off-eclipse dips repeat at the same binary phase (within 0.01) in another sector far above chance; bumps do not** (`rs024_phase_null.py`, chance from 200 random per-sector phase shifts): 20 to 27.4 d: 257 of 298 dips against 155 by chance (34 stars); 27.4 d+: 284 of 365 against 160 (37 stars); 14 to 20 d: 492 against 418; 5 to 10 d: 263 against 213. Clean bumps sit at chance in every bin (20 to 27.4 d: 4 against 10.7; 27.4 d+: 48 against 43.7). So about a third or more of the clean strong off-catalogue dips in slow binaries are the stars' own eclipses at a phase the catalogue windows do not cover (secondaries without catalogue geometry, eccentric offsets, or widths too narrow). The rest: non-periodic dips (blends, detrending leftovers, systematics). Event counts are dominated by a few stars with many events (22 and 28 recurring stars).
- **Literature, CONFIRMED (primary text):** mono-cbp, the closest published TESS search (Davies, Brown, Gill, French 2026, [arXiv 2604.09435](https://arxiv.org/html/2604.09435), section 4.1): of 1,647 transit-like single events that passed its automatic vetting in TESS EB light, 1,084 were stellar eclipses ("There are several binaries in our sample that do not have secondary eclipse parameters. For these targets, secondary eclipses are not processed by the eclipse masking procedure"), 258 detrending artefacts, 135 systematics, 138 contamination from a nearby short-period EB. Their rule: 3 or more events at one binary phase = secondary eclipse.
- **Order problem in our chain, CONFIRMED (code):** `enrich_group` computes "dominated" on the raw event list (stage3_core 288 to 294); Petrova recognises repeating eclipses only later (`apply_v7`: orbit_lock (c6) and the Petrova phase veto p1_veto). An eclipse the chain itself later labels can still dominate a planted bump. Codex's "eclipse" option used catalogue windows only, which these eclipses are outside (0 of 22).

### Q4. How professionals test that a transit stands out. CONFIRMED (primary text)
- **Kepler DR25 Chases** (Thompson et al. 2018, [arXiv 1710.06758](https://ar5iv.labs.arxiv.org/html/1710.06758), A.3.7.3): for each single transit, the closest feature in the absolute value of the detection statistic (|SES| > f x SES_max), searched from 1.5 durations out to Delta t_max = P_orb/10; metric = distance / Delta t_max; used only for 5 or fewer transits. It is LOCAL and compares against BOTH signs ("Because Chases uses the absolute value of the SES").
- **LEO-Vetter for TESS** (Kunimoto et al. 2025, [arXiv 2509.10619](https://arxiv.org/html/2509.10619v1), III.8): same, |SES| > 0.7 SES_i, from 1 duration to P/10 either side; fail if the mean Chases < 0.78.
- **Model-shift uniqueness** (DR25 A.3.4; LEO III.9): the primary is compared to the next negative event (tertiary, MS2) AND to the most positive event (MS3), each with a significance margin FA2, not "at least as strong".
- **mono-cbp** (single transits in TESS EBs): no opposite-arm comparison at all; shape model comparison (transit against step, sinusoid, linear; AIC) plus the binary-phase rule above.
- **Difference from ours:** ours is whole light curve, opposite sign only, margin zero. Every published version is local, either sign (or both tested separately), with a margin. Codex 008 tested "local" but kept "opposite sign only".

### Q5. Inverted light as a control in EB and TESS light. CONFIRMED (primary text)
- DR25 (II.3.3, II.3.2): "In order for inversion to exactly reproduce the false alarm population, the false alarms would need to be perfectly symmetric (in shape and frequency) under flux inversion, which is not true." They removed every inverted detection on stars with a detached EB of morphology above 0.6 or a known KOI, because inverted eclipses "have no corresponding false alarm in the original, un-inverted light curves".
- LEO-Vetter (V.4): "We initially considered light curve inversion, but found that the most problematic TESS false alarms were due to scattered light which is not symmetric under inversion"; they used scrambled light only, and also removed light curves on the TESS EB catalogue from the scrambled set (V.5).
- **My reasoning, NOT TESTED:** scrambling (re-ordering orbits and sectors) breaks the ephemeris of a periodic signal but only moves a single transit, so it cannot remove a real single event; it does not fit a single-transit search. That supports dropping T101 (14 Nov triage). The upside-down arm stays our only practical meter, with a known bias in EB light that must be measured, not assumed away.

## Test plan, written BEFORE any option is measured (14 Nov 2026, 12:08 Kuwait)
Options come from the literature and the order problem above; none is tuned on results. All are symmetric in rule (the same code for both arms). Measured with `rs024_options.py`, a copy of the two-key P recount (`006-check/p_recount.py`) that recomputes "dominated" inside the frame and re-tiers; frozen files untouched; design stars only.
- **O0 baseline:** the frozen rule recomputed. Must reproduce the recount exactly (531 dips, 486 bumps): the identity check. If it does not, nothing below is read.
- **OE, eclipse-explained rivals do not count:** opposite sign, whole light curve, margin zero, but a rival that the chain itself labels a stellar eclipse or a repeat (c5, ecl_overlap, orbit_lock, p1_veto, repeater) is ignored. From mono-cbp's finding and our order problem.
- **OA, Chases-like:** rivals of EITHER sign within 6.85 d (the span Codex's local option used, so OA differs from it in one thing only), excluding the candidate's own 1.5 durations (Kepler's exclusion), margin zero.
- **OAE:** OA and OE together.
**Adoption rule (the Tree's, unchanged):** an option counts only if planet P rises with NO increase in upside-down tier-1 background events in the untouched design light, and the paired dip-against-bump control passes (no bin whose 99% star-bootstrap interval of the difference excludes zero). T156 and the 008 harness are Codex's second key and come after. Also reported, not used for adoption: the real-arm background count, to show what each option does to the meter's bias.

### Q2 addendum: the rivals that actually held planted bumps (rs024_rivals.py, 12:40). CONFIRMED (own data)
Slow bins, upside-down arm (planted bumps held by "dominated"): 20 to 27.4 d: 21 rivals, of which 13 carry an eclipse or repeat label the chain sets itself (p1_veto 9, orbit_lock 1, repeater 4), 15 carry an artefact flag (step, gap, ramp), only 1 has neither, only 1 is itself tier 1. 27.4 d and up: 23 rivals, 9 eclipse or repeat (p1_veto 8, orbit_lock 5), 9 artefact, 7 neither, 5 tier 1. **So most blocking dips are events the chain itself already rejects; the rule lets a rejected event veto a planet.** Idea for a later round (NOT in the preregistered set, so not measured now): only rivals that are themselves tier-1 eligible count.

## Results of the preregistered test (`rs024_options.py`, finished 12:21; `options.json`)
**Identity check PASSED:** O0 reproduces the two-key recount row by row on all 1,250 trials (dips 529 "new" / 531 "all", bumps 486 / 488; zero differing rows).

| Rule | Planets found (new, of 1,098) | P equal weight | Bumps found | Paired control (99%, 5 bins) | Background tier 1, real / upside-down |
|---|---:|---:|---:|---|---|
| O0 frozen | 529 | 0.4845 | 486 | **FAIL** in 20 to 27.4 d (+3.8 to +18.7) and 27.4 d+ (+0.4 to +14.5) | 176 / 83 |
| OE eclipse-labelled rivals ignored | 531 (+2) | 0.4863 | 509 | PASS all bins | 178 / 87 (+4 upside-down, in 5 to 20 d) |
| OA Chases-like (either sign, 6.85 d) | 515 (-14) | 0.4714 | 503 | PASS all bins | 171 / 80 |
| OAE both | 527 (-2) | 0.4828 | 514 | PASS all bins | 176 / 83 (identical) |

**Verdict under the Tree's adoption rule: no option is adopted.** OE adds 2 planets but 4 upside-down background events; OA and OAE lose planets. CONFIRMED (one key; Codex's T156 second key not run).

**What it means:**
1. **The paired-control failure is understood and fixable.** It came from the rule, not from the light being searched unfairly: every rule that stops rejected eclipses from vetoing, or compares against both signs, passes the control in every bin. OAE does it with the false-alarm background exactly unchanged (176 / 83) at a cost of 2 planets of 1,098 (0.17 points). CONFIRMED.
2. **"Dominated" is not where the missing planets are.** The best any rule here gains is 2 planets; dropping the flag entirely (Codex 008) gives 49.5% with 23 extra false alarms. The route to P 0.50 runs through the other holding flags (step, gap/dump, ramp; FIX 92), not this one. CONFIRMED.
3. **Decision for Ahmed:** the Tree rule asks every change to gain planets. A change whose job is fairness (OAE: control fixed, background unchanged, 2 planets lost) cannot pass it by design. Either keep the rule (OAE stays a note, the control stays failing in two bins) or allow fairness fixes that leave the background unchanged and cost under about 0.5 point of P.
