# Compass review: outside AI's review of VESPER-BRIEFING.md (28 Oct 2026)

Reviewer of the review: Claude (fresh session, D:\second-sun). Review only: no code, no search, no download, no real event opened. The pasted text also contained a prompt for Claude Code ("give Claude Code right now", answers A to E); it was NOT run. This pass is the Compass check Ahmed asked for.

**Verdict: REVISE.** The outside review is mostly sound and close to our own plan in the briefing (section 15). Five changes below.

## Checked (labels: CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED)
- CONFIRMED: 4,584 eclipsing binaries in TESS sectors 1 to 26, Prsa et al. 2022, https://arxiv.org/abs/2110.13382 (abstract opened 28 Oct). The 28 Oct handoff had this as UNCERTAIN; our audit note `research/audit-2026-10-28-varwise-mono-cbp.md` line 7 already had it. The title says "short cadence", so G2 stars very likely have 2 minute data (LIKELY; the abstract does not say 2 minute).
- CONFIRMED (our note, from the Davies et al. paper read on 28 Oct): the professionals cut the 4,584 to 1,790 detached, 591 with period over 7 d, 512 searched, 1 weak candidate. So a G2 built with their cuts is mostly stars they already searched with a different tool. The outside review does not say this. Discovery prospects there: UNCERTAIN.
- CONFIRMED: `targets/g1_targets.csv` holds only kic, tic, tmag, p_bin_d, bjd0, morph, tic_radius_rsun. No light ratio and no radius ratio, so dilution cannot be computed from what we hold.
- CONFIRMED: `pipeline/faint_recovery.py` and `pipeline/sap_recovery.py` have no upward (bump) injection and no sign option.
- CONFIRMED: swallowed errors are small: "not measurable" 10 of 550 real and 9 of 488 upside-down raw-light-only dips (`aggregate_v7.txt` section 8). SAP fill measured in one file only (FIX-QUEUE 21a).
- NOT OPENED (LIKELY from memory): Kepler DR25 completeness and reliability are separate properties (Thompson et al. 2018); Transit Least Squares warns that white-noise false alarm levels are too optimistic for correlated noise. UNCERTAIN: the claim that the mono-cbp authors manually inspected survivors (not in our notes; our B-lite found its default vetting calls TOI-1338 b's transits sinusoids, `research/monocbp-b-lite-2026-10-28.md`).
- Slip of mine, caught: I first wrote the Prsa arXiv number from memory; it was a quantum Hall paper. The right ID was already in `research/wave-1-gap-check/c-catalogues/sources.md`. Rule kept: open the source, never trust a remembered ID.

## What is correct
1. Seven versions on the same 549 stars, rules chosen as results came in: true (briefing section 12, item 12).
2. Order: sensitivity first, then G2, then the statistical judge, then a frozen v8 run on G2, then the blind look. Matches our plan, with the judge as its own step.
3. Radius caveat: depth = (planet radius / radius of the star crossed) squared times that star's share of the light. A TIC radius describes the blended point (LIKELY). The briefing's "use the TIC radius" was too simple. Report depth and duration first; radius only as a labelled range.
4. Inject dips and mirror bumps through the same flag chain: the best new idea. It directly tests the assumption behind report line 5b that the flags act equally on both sides (NOT TESTED so far). Cheap: the search already runs the flipped curve.
5. Keep SNR 7 as the historical bar; do not lower it to collect events; completeness and false alarms are measured separately.

## What needs changing, and why
1. **Do not make the audit a separate first phase.** The swallowed errors touch about 2% of raw-light-only dips, and the fill is queued. Fold both into step 1 as a step 0 (count filled cadences over the whole run, print every swallowed error), because injecting into the cleaned light would otherwise carry the fill.
2. **Matched comparison stars come later.** They need a new download of the size of G1 (5.4 GB for 549 stars) and have no eclipses, so the three eclipse flags cannot be tested on them. Needs Ahmed's yes.
3. **Block bootstrap tests the SNR bar only.** Gaps, orbit starts, the common moment and the eclipse phase depend on the timeline and on other stars, which resampling destroys. Our FIX-QUEUE 5 rejected an earlier bootstrap for lack of a null; this version (mask dips, resample residual blocks) is worth a try for the SNR bar, not for the flags.
4. **The "specific flaw" in the blind review is a misreading.** The briefing asks for an equal number of upside-down plots from the 32 cleaned-light ones, not from the raw-light half. The underlying point is right: no control exists for the 7. Use upside-down raw-light dips from earlier rungs where both sides exist (ladder in `VESPER-BRIEFING.md` section 8: 51 against 18 after the repeater flag, 14 against 2 after the flat-baseline flag), matched on strength, duration, sector and camera, drawn by the same code with no labels, plus random segments. This is a later phase and needs Ahmed's explicit yes; Ahmed himself waits for the Eyes readiness ladder.
5. **"Keep G2 out of tuning" needs teeth.** Commit a preregistration file (rules, hash, success criteria, what counts as an excess) before any G2 file is searched; consider a development slice of G2 and a sealed test slice. G1 cannot be the final test: the v1 to v4 rules were chosen after seeing it.

## The single best next step
Plan step 1 stays first, with three additions: step 0 (fill and error audit), results by depth and duration first with radius as a range, and mirror-bump injections. G2 second (a small catalogue table and a coverage query; needs a download yes). Cost estimate from `research/usage-ledger.md`: step 1 about 2 to 3.5 weekly points (uncalibrated; nearest rows v5 0.9, v6 1.6, v7 plus bug hunt 4.0); G2 catalogue 0.5 to 1.
