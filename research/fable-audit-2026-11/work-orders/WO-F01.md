# WO-F01: measure the eclipse-mask loss through the whole chain, then design the Petrova 1.0 mask

**Model and cost:** Part A Sonnet 5.5 Extra, about 1 to 1.5 points. Part B design Opus 5.5 (or Fable), about 2 points. Part C (build and freeze) Sonnet with Opus review, about 3 to 5 points.
**Needs Ahmed's yes?** Part A: no (read-only re-runs into `data\fable_audit_*`, counts only). Parts B and C: YES (a Petrova change, a new version).

## Goal
Know, per binary-period bin and dip strength, what share of real dips the frozen 0.8.1 chain deletes in `eclipse_mask_auto`, and replace the mask in Petrova 1.0 so that share is near zero.

## Why it matters
The mask treats any low phase bin in ONE sector as an eclipse. In slow binaries each phase bin is seen once, so a planet's dip is masked before the search. On real G2 light a strong 8 h dip is found 0 times in 25 for binaries slower than 20 d. Eight of the twelve known transiting circumbinary hosts are slower than 18 d. All our completeness numbers were measured after the mask and miss this.

## Exact location (commit c9b9aca)
- `pipeline/detect_v2.py` lines 129 to 161 `eclipse_mask_auto`; lines 164 to 170 `mask_all_periods`.
- `pipeline/stage2_search.py` lines 87 to 92 `mask_runs`; line 163 (called in `prepare`); lines 183 and 190 to 191 (both arms built from the SAME masked light); line 212 (injection after the mask).
- `pipeline/chain_recovery.py` lines 38 to 42 (wraps `S2.prepare`, injects into prepared flux).
- `pipeline/stage3_core.py` lines 82 to 99 `eb_widths()` (catalogue eclipse widths, already loaded for G2 and G3).

## Evidence and how to reproduce
```
cd D:\second-sun
$env:PYTHONUTF8=1
.\.venv\Scripts\python.exe research\fable-audit-2026-11\scripts\p01_mask_eats_transits.py 30        # synthetic, about 5 min
.\.venv\Scripts\python.exe research\fable-audit-2026-11\scripts\p01b_real_vs_flip_by_period.py     # stored events, counts
$env:SS_SET="g2"; .\.venv\Scripts\python.exe research\fable-audit-2026-11\scripts\p01c_real_light_premask_injection.py 25   # real light, about 6 min
```
Expected outputs are saved in `research/fable-audit-2026-11/evidence/p01_synthetic.txt`, `p01b_real_vs_flip.txt`, `p01c_real_light.txt`. Key line: `P 20 to 27.4: K 25 | before 0.00 | after 1.00 | cut 1.00`.

## Part A: measure (Sonnet)
1. Copy `p01c_real_light_premask_injection.py` to a new script in `research/fable-audit-2026-11/scripts/` and extend it. Do NOT edit anything in `pipeline/`.
2. Sample: 100 files per period bin (5-10, 10-14, 14-20, 20-27.4, over 27.4 d), for G2 (`SS_SET=g2`) and G3 (`SS_SET=g3`), both SPOC-family and QLP. For QLP you must apply the windows exactly as `stage2_search.prepare` lines 150 to 159 does BEFORE the mask; easiest is to copy `prepare` into your script and add an optional `inject(t, f)` hook between line 162 and line 163. Right result at this step: with no injection your copy returns exactly the same `n_searched` as the stored group JSON `meta` for 20 test star-sectors.
3. Injection: trapezoid as `chain_recovery.signal` (20% ingress and egress), durations 4, 8, 14, 20 h, K = 8, 10, 12, 14, 18, 25 (units of the 8 h noise measured after the mask, as `audit_paths.noise`), random time at least 1.5 d from the ends, both signs (dip, and bump read on the upside-down arm).
4. For each injection record: found at SNR 7 when injected before the mask; found when injected after; share of in-transit cadences cut. Save rows to `data\fable_audit_mask\rows.pkl` (private) and a counts table to `research/fable-audit-2026-11/evidence/`.
5. Output table: m(period bin, K, duration, product family) = found-before / found-after. Then weight by the star-sector shares of each hunt to give one m per hunt, and by Horizon's per-star E if you can read it from `t138_g_reach.py` outputs.
6. Known planets (this is also WO-F06): for every file in `data\known` of TOI-1338 and TIC 172900988, run `mask_runs` and report the share of cadences inside each published transit window that the mask removes.
**Proof test for Part A:** bumps must give m = 1.00 within error in every bin (they did in the synthetic run). If bumps are also lost, your injection is wrong.

## Part B: design (Opus or Fable; Ahmed's yes first)
Candidates, to be compared on the Part A harness:
- (a) Catalogue mask: primary at the catalogue ephemeris, secondary found once per STAR (all sectors folded together), widths from `eb_widths()`, padded.
- (b) Repeat rule: fold ALL sectors of the star together; a phase bin is masked only if it is low in at least 2 separate cycles. Single-visit phases are never masked by depth alone.
- (c) For binaries with too few cycles for (b): mask only dips deeper than a physical planet limit AND matching the eclipse width; flag the rest instead of deleting.
- In every candidate, build the upside-down arm by the mirrored rule so the arms stay exchangeable, and fold FIX 11 and FIX 14 (detrend window, mask before detrend) into the same version.
**Proof test for the design:** on the Part A harness, m at least 0.9 in every period bin for dips; real-to-upside-down event ratio on real light between 0.8 and 1.25 in every period bin; eclipses still removed (no rise in events within the catalogue eclipse windows).

## Traps
- Do not "fix" `detect_v2.py` in place. 0.8.1 is frozen and hashed; `g3_run.py guard` will refuse and the sealed results lose their provenance.
- Do not judge by the pooled count. The loss hides in the slow bins; always print per period bin.
- K must be in units of noise measured the same way in both arms of the test (after the baseline mask), or the two columns are not comparable.
- A dip placed inside a masked eclipse proves nothing; place it in light the baseline mask keeps (the script does this).
- Small samples: 25 files give plus or minus 0.15. Use 100.
- Do not re-score G2 or G3 with any new mask. Their verdicts stand. A re-search is a new preregistered hunt (F-11).

## Do not touch
`pipeline/*` (frozen), `research/stage3/SETTINGS_FROZEN*.json`, anything under `data\stage3*`, the sealed and G3 run folders (read only).

## Stop signs
Stop and ask Ahmed (flag for Opus or Fable) if: Part A shows m under 0.5 for G3 or G2 as a whole (the nulls then need a public correction note, his wording); any step would need a change in `pipeline/`; a real-arm event appears in light the old mask removed that looks like a transit (private lead, two-key rule, write it only under `data\fable_audit_private\`).
