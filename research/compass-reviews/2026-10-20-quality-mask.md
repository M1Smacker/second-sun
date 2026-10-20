# Compass review: quality-mask experiment (HARD vs DEFAULT) and the six-point plan

*2026-10-20, Claude. Review only. Method: research/COMPASS.md. Two passes: (1) the experiment design, (2) Ahmed's six-point plan. Filed afterwards so the record is in the repo; the experiment itself is in `experiments/quality_mask/`.*

## Verdict: REVISE (both passes)
"HARD vs DEFAULT" as first stated cannot answer the question: with PDCSAP flux it is an exact no-op, and with the existing loader it silently becomes a switch to SAP flux. The design must separate flux from mask.

## VERIFIED (read from the repo and the cached files, 2026-10-20, repo at 2f3ca9a)
- HARD = 24319, DEFAULT = 17087; they differ only in bits 64, 1024, 2048, 4096. `detect_v2.load()` reads with `quality_bitmask="hard"`, uses PDCSAP, and fills PDCSAP-NaN cadences from locally scaled SAP.
- `accept_v2_results.json`: `sap_filled` is 0 in every sector (the fill path never ran); S30 and S62 have 0 cadences near the transit; recovered in S10, S65, S68, S98 (4 of 8 sectors with data); 6 flipped-data events in 10 sectors; 6 R_earth injections 5 of 7 recovered at SNR 7.2 to 7.9.
- Across the 10 sectors of `accept_v2`'s table, DEFAULT restores 45,502 cadences over HARD, all with bit 4096 only. **PDCSAP is NaN on every one; SAP is finite on every one.** In every sector the PDCSAP-NaN cadences that pass DEFAULT are exactly the restored set.
- Within +-3 h of the published times: S30 all 180 cadences flagged (bits 128 and 4096), PDCSAP NaN, 163 usable SAP cadences under DEFAULT; S62 all 180 bit 4096 only, PDCSAP NaN, 180 usable SAP; S68 40 flagged, DEFAULT restores 39. The PDCSAP-NaN stretches around the transits are 2.39 d (S30) and 1.38 d (S62); SAP background in S30's window is 6 times the sector median.
- S30's published time is a prediction (damaged egress); S62's is measured (Wang and Liu 2024, via research/burn-1-science/report.md). burn-1 had already noted that PDCSAP is NaN at both.
- `pipeline/accept_v2.py` has no `__main__` guard: importing it re-runs everything and overwrites tracked `accept_v2_results.json`. `diag_v2.py` writes into the current folder. `recover_cbp.py` writes nothing (prints only). STANLEY's saved curve is HARD + PDCSAP, so the STANLEY injection set cannot test the mask.

## Design adopted
Arms A0 (PDCSAP + HARD, reproduce the baseline), A1 (SAP + HARD), A2 (SAP + DEFAULT); A0 vs A1 isolates the flux, A1 vs A2 isolates the mask. Same sectors, published times, eclipse geometry (epoch held from A0), detector and bar; flipped control; S98 injections at the baseline's retained times; exploratory injections inside restored stretches; decision rules fixed in advance. Full text: `experiments/quality_mask/SPEC.md`.

## Failure modes named in advance
PDCSAP + HARD vs PDCSAP + DEFAULT is identical (a null that would mislead); the production loader's fill rule (needs more than 20 PDCSAP points within 1 day, else scale 1.0) silently mixes normalisations in long stretches; coverage gain at S30 and S62 is trivial (HARD has no data there), so the real question is whether restored SAP is trustworthy; the noise estimate is measured from all box means, so restored noisy data can lower SNR elsewhere; 7 injection trials per size and single-digit flipped counts cannot support significance claims; one star, one sky position, nothing transfers to G1 without replication.

## Pass 2: Ahmed's six-point plan
Right: finish the review; same transits, flipped control and 6 R_earth injection in isolated outputs; guard `accept_v2.py`; defer scale-up, STANLEY calibration and the 136-star decision; study the book first. Changes: name the flux in point 2; the run manifest comes before the run (fixing `accept_v2.py` can follow); `recover_cbp.py` needs saving added, not fixed; autonomy needs Ahmed's explicit bounds and a usage ceiling; the scale-up needs the QLP recipe automated and real fainter stars; flag the 136 rows in a derived file, not by editing the frozen target list; stale "coming" text and three label vocabularies in the book (fixed 2026-10-20, logged in mistakes.md).

## Single best next step
Freeze the spec, then reproduce A0 against the saved baseline before reading any other number. (Done 2026-10-20; see the Field Note.)
