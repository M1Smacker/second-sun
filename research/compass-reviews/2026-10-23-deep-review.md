# Compass review: the research Claude's deep review (2026-10-23)

*Review only, nothing in the pipeline changed. Source: `research/deep-review-2026-10-23/review.md` (written by a separate Claude research session from our brief `research/deep-research-brief-2026-10-23.md`, with its five scripts). Checked by Claude here: bugs re-run on this machine with our own scripts, counts re-made from our target files, all 20 arXiv ids looked up in ADS (API, key not printed), quoted numbers matched against the ADS abstracts. Labels: VERIFIED (re-run here, or the number is in the ADS abstract), LIKELY, UNVERIFIED, WRONG.*

## Verdict: APPROVE the findings, REVISE the odds

This is the most useful outside review so far. Unlike Gemini (7 of 12 citations bad), all 20 papers it cites are real, with correct authors, years and journals, including the 11 journal references it honestly marked as "from memory". Its two headline bugs are real and serious.

## Bugs: re-checked here

| Review item | Our check | Result |
|---|---|---|
| **B1** 30-minute data gives no events (`bin10` + `box_scores` `min_cover=0.8`) | Same 8 h, 1,500 ppm dip at 2, 3.3, 10, 30 min cadence | VERIFIED. SNR 21.0, 24.0, 24.7, then **no event**; only 33% of 10-min bins filled at 30 min |
| Impact: 890 of 5,081 QLP star-sectors (S14, 15, 16, 26), 333 TESS-SPOC, 596 with no SPOC fallback | Recounted from `targets/g1_coverage.csv` | VERIFIED (890, 333, 596). It also kills the Kepler re-find test (Kepler long cadence is about 30 min) |
| **B2** QLP before sector 56: loader picks `kspsap_flux` | Ran the selection on our own Kepler-16 S54 QLP file; read our installed lightkurve `io/qlp.py` | VERIFIED. S54 has no `sys_rm_flux`/`det_flux`; lightkurve says `kspsap_` (S1-55) and `det_` (S56+) are the same detrended column renamed. Our own note says `det_flux` lost about 70% of a 6 h dip. 2,845 of 5,081 QLP star-sectors are pre-56 (VERIFIED count) |
| B2 side check | Kepler-16 S54: deep 5.5 h primary eclipse in SAP vs KSPSAP | KSPSAP kept 101% of a 14% eclipse. Expected: spline fits clip deep points; the damage is to shallow dips. Does not weaken B2 |
| **B3** extra catalogue periods dropped, never masked | Re-ran on `research/wave-3-pipeline/g1_tmag.csv` | VERIFIED: KIC 4150611 (1.522 d) and KIC 7622486 (2.280 d, morph 0.59), exactly those two |
| **B4** upside-down match auto-deletes events, "contrary to the flags-not-deletions rule" | Read `veto()` and our brief | PARTLY. Our rule (brief §4 item 7) was about dumps and gap edges, so it is not a contradiction. But it is an untested deletion: our veto test had only 4 real crossings. Fair to make it a flag until tested |
| **B5** SPOC file with all-NaN PDCSAP returns no data, silently | Read `load()` lines 45-50 | VERIFIED by reading (path falls to `"flux"`, which is PDCSAP for SPOC files). Low impact, cheap fix |
| D3 eclipse drift is not the weakest link | Computed 3-sigma drift (1,950/P × period error) for all 552 rows from our Villanova copy | VERIFIED in spirit: only 8 rows over 2 h, 1 over 5 h. **KIC 6191945** (P 6.81 d) could drift about 16 h: flag it |
| "Your Villanova CSV may already have pwidth/sdepth/sep" | Read our copy | WRONG: ours has period, period error, epoch, morph, GLon/GLat, kmag, Teff only. Widths would come from STANLEY's MIT table (not downloaded) |
| D4 Kepler-16 secondary at phase offset 0.4885 | Needs that table | UNVERIFIED |
| Five known hosts in G1 (Kepler-16, 38, 64, 453, 1647) | Matched TICs in `g1_targets.csv` | VERIFIED. Good negative controls |
| Other counts: 237 stars with no SPOC/TESS-SPOC, median Tmag 12.45, median 9 QLP sectors | Recounted | VERIFIED. (Radius > 3 Rsun: 122 rows here, review says 121.) |

## Citations (20 checked in ADS)

All 20 real and correctly attributed. Numbers found in the abstracts (VERIFIED): Davies 2026 at least 50% / over 75% for 9 of 14; Martin 2017 "additional ∼17-30" hidden planets that "will ultimately transit someday"; Armstrong 2014 10.0 (+18, −6.5)% for R > 6 R⊕, P < 300 d; Oddo et al. 2026 (Martin a co-author) 33% upper limit at 95%, one candidate; Kostov 2020 pair method shown on four Kepler planets; Kostov 2021 one TESS sector; Borkovits 2025 243 triple candidates; Borkovits 2026 two binaries whose eclipses vanished, seven with depth changes; Kristiansen 2022 69 peer-reviewed papers.
Body text only, so UNVERIFIED by us: TESS Ten Thousand 1,371 of 2,458; Battley "Kepler-34 not again until 2066"; QLP 0.3-day spline sentence; Davies "up to Sector 79" and SAP preference (the 512 and S79 we had already, wave 1 A21); the 30-star overlap list (needs mono-cbp's GPL repo CSV; reading it is fine, copying is not).
2027 return: sectors 119 (3 to 29 July 2027) and 120 (29 July to 23 August 2027) are northern: dates VERIFIED (MIT sector pages via search). Camera 2 positions not seen by us; if as quoted, part of the Kepler field is inside: LIKELY, check star by star with tess-point.

## Where Claude disagrees or adds

1. **The odds lean on a noise level we have not measured on G1.** The yield model uses noise factor β 1.0 to 1.4, tuned on TOI-1338 (not a G1 star). The one G1 star we measured, Kepler-16, implies β ≈ 2.8 (the review's own number). Re-running the scaling with our own script (`research/deep-review-2026-10-23/our-checks/noise_scaling.py`): β 1.4 → about 29% for at least one candidate; β 2.0 → 22%; β 2.8 → 17%. So the honest answer is **15 to 30%, decided mostly by G1's real noise**, after B1 and B2 are fixed. Claude's estimate moves from 15% to **about 20% (range 5 to 45%)**. Caveats kept: Martin's E has a possible typo (the review flagged it), and the model counts primary-star transits only.
2. **My earlier Gemini review missed a paper.** "Oddo and Dragomir 2026" (the paper Gemini cited, ApJ 996, 82) is indeed the M-dwarf EB catalogue, as I said; but the same team posted the occurrence-rate paper this month (arXiv:2610.22625). It does not support Gemini's "1 to 2%" either. Logged in mistakes.
3. **The common-time veto, pair search and short/long boxes are standard and cheap**: agreed. They come after the data path is fixed, because each depends on it.
4. **Credit**: agree the upper-limit paper is the most realistic credited result, and that it needs the per-star sensitivity map the audit would produce.

## Decisions taken in this review (Claude)
1. Filed this review and saved the source review and its scripts in `research/deep-review-2026-10-23/` (scripts are the author's, MIT; we did not run them here; we re-did each check with our own code).
2. No pipeline code changed. The hunt stays on hold; the B1/B2 fixes need Ahmed's go.
3. Odds updated to about 20% (5 to 45%) in RESUME.
4. KIC 6191945 flagged for eclipse drift; KIC 4150611 and KIC 7622486 flagged for missing extra periods.

## Proposed next step (Ahmed's go needed)
**The data-path audit**, as the review recommends, with B1 and B2 fixed first:
1. Fix B1 (bin to the data's own cadence when it is slower than 10 min) and B2 (pre-56 QLP: use `sap_flux` plus our detrend plus borrowed windows), each with a self-check that fails on the old code. Also B5 (explicit SAP fallback) and record the chosen flux column in every result row.
2. Audit script: for every G1 star-sector, record product, cadence, column, cadences kept, noise per box length, and whether one injected standard transit comes back. This measures G1's real noise, which settles the odds question above.
3. Then the Kepler re-find test (now possible once B1 is fixed), then the common-time veto and eclipse-phase check.

## Lesson
A reviewer that can run code found what three rounds of reading could not: a filter that silently returns nothing looks exactly like a quiet star. Every data path needs a test that injects a known signal through the real loader at every cadence and product we use.
