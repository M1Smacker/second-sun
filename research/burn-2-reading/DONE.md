# DONE: burn-2-reading

Finished 2026-10-19 21:03 UTC, before the 21:50 stop. Nothing committed or pushed; the coordinator commits.

## Done
- [x] **Task 1: rivals watch via the NASA ADS API.**
  - Table of 11 efforts (report §1.1).
  - G1 check: no ADS record of a CBP transit search of Kepler-field EBs in TESS data (§1.2). Closest risk: the Tufts/Martin XRP 2024 STANLEY project.
  - 2026 discoveries: none confirmed in refereed ADS records; candidates only (§1.3).
- [x] **`ads_watch.py`:**
  - 11 saved queries, `--since` (ADS entdate), `--q`, `--abstracts`, `--selftest`;
  - the key is read only from the env var, never printed, and grep-checked absent from all files;
  - selftest passes, and a live run since 2026-10-01 completed (exit 0).
- [x] **Task 2: SPOC/QLP coverage** (report §2).
  - Read: Guerrero+ 2021 full text, SPOC DR113 release notes full text, MAST TCE page.
  - Conclusion on where room is left: single transits, FFI-only hosts, stacked newest sectors (south S97+, north S87+), sub-threshold signals.
- [x] **Task 3: Norazman+ 2025 read in full** (report §3): method, sample, cut funnel, results, code (public but unlicensed), and what an S27+ repeat needs.
- [x] **Task 4: short notes** (report §4): Zieba+ 2019 β Pic (abstract), TESS dipper searches (abstracts).
- [x] report.md ("In plain words" first), claims.md (R1-R27), sources.md, open-questions.md, friction.md.
- [x] 3 downloads logged in research/downloads.csv: Guerrero PDF, Norazman PDF, DRN113 PDF, all in D:\second-sun\data\burn-2-reading\.

## Not done
- [ ] Davies+ 2026 and Oddo+ 2026: did not re-read their sector coverage; relied on wave 1 (open question 7).
- [ ] arXiv-only sweep for 2026 CBP discoveries; ADS only (open question 6).
- [ ] Whether SPOC searches TESS-SPOC FFI light curves; QLP extended-mission thresholds (open questions 4-5).
- [ ] Zieba+ 2019 and the dipper papers: abstract level only (task 4 asked for short notes).

## Files written (all in research/burn-2-reading/ unless noted)
- report.md, claims.md, sources.md, open-questions.md, friction.md, DONE.md
- ads_watch.py
- Raw ADS outputs: ads_run_2025-01-01.txt, ads_run_2026-10-01.txt, ads_adhoc_1..5.txt
- data/burn-2-reading/: 2103.12538.pdf, 2508.04673.pdf, drn113_ms14-78.pdf, plus pdftotext .txt extracts
