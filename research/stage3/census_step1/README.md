# census_step1: scripts and outputs of the night of 4 Nov 2026 (RS-011)

Run everything with `D:\second-sun\.venv\Scripts\python.exe` (pandas, scipy). Input folders: `data\census_targets_2m` (111 TESS 2-minute target lists, 65 MB, fetched by `fetch_targets.py`), `data\census_probe` (66 probe light curves, 113 MB), the G2 and G3 audit and recovery tables under `data\`, `targets\`. All scripts print aggregates only (no star IDs).

| script | question | output | note in research/stage3 |
|---|---|---|---|
| fetch_targets.py | download the target lists (arg: first sector) | data\census_targets_2m | CENSUS-STEP1-COUNTS |
| count_targets.py | stars with 2-minute data after sector 26 | step1-counts.txt | CENSUS-STEP1-COUNTS |
| crosscheck_counts.py | independent re-count of the above and of the G3 lost reads | crosscheck-counts.txt | Q5-LOST-READS |
| q5_lost_reads.py | what the 784 no-safe-window reads cost (Horizon what-if) | q5-lost-reads.txt | Q5-LOST-READS |
| q1_expected.py | expected detections under Armstrong 2014 with the Horizon maps | q1-expected.txt | Q1-EXPECTED-PLANETS |
| t138_geometry_probe.py | exactly-coplanar transit geometry per star (Martin and Triaud Eq. 26) | t138-geometry-probe.txt | Q1 update |
| t138_incl_probe.py | same with 0 to 3 degrees of mutual inclination | t138-incl-probe.txt | Q1 update 2 |
| q2_pool_value.py | star-equivalents per GB by pool | q2-pool-value.txt, .csv | Q2-POOL-VALUE |
| q3_gaia_counts.py | Gaia DR3 EB candidates, bright and slow (public TAP counts) | q3-gaia-counts.txt | Q3-Q7 |
| q7_completeness.py | what limits G3 completeness | q7-completeness.txt | Q3-Q7 |
| route_probe.py, route_parallel.py | fetch speed and file size (AWS bucket, MAST) | route-probe.txt, route-parallel.txt | CENSUS-STEP2-RESEARCH |
| (inline) scenario table | files, GB, hours per pool | route-scenarios.txt | CENSUS-STEP2-RESEARCH |
| eb_share_by_coverage.py | EB share by brightness and sectors; pilot pool yields | eb-share-by-coverage.txt | CENSUS-STEP2-RESEARCH update |
| g1_reach.py | Horizon reach for G1 (gap fill) | g1-reach.txt | Q1 update 3 |
| chain_recovery_shape.py + run_shapes.ps1 | FIX 28: completeness for other transit shapes (wrapper patches only signal()) | data\shape_*.log, rows_shape_*.pkl | FIX28-SHAPE-TEST (when done) |
| census_worth.py | what Census would add to the evidence | census-worth.txt | CENSUS-WORTH |

Run order if everything is rebuilt: fetch_targets.py 1, count_targets.py, eb_share_by_coverage.py, q5_lost_reads.py, q1_expected.py, t138_geometry_probe.py, t138_incl_probe.py, q2_pool_value.py, q7_completeness.py, census_worth.py. The reach runs take 2 to 6 minutes each. Q3 and the route probes need the network.

## Added 6 Nov 2026 (T138)
- `t138_g_reach.py` -> `t138-g-reach.txt`: Horizon reach with the transit chance g of R0 Amendment 4, four hunts, four scenarios, f 1.5, 1.8, 2.2.
- `census_worth2.py` -> `census-worth2.txt`: Census worth recomputed (replaces `census_worth.py`).
- `t138_geometry_probe.py` and `t138_incl_probe.py` (and their outputs) are SUPERSEDED: exploratory, flawed per the Opus audit (`../OPUS-TRIAL-AUDIT-2026-11-06.md`), kept for the record.
