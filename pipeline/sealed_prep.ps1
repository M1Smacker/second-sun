# Sealed-slice DATA PREPARATION (not the search). Run AFTER the sealed download has finished (data\g2_sealed_download_log.txt ends with ALL DONE).
# Same steps as for the development slice (RESUME 29 Oct, "HOW TO RUN"): audit windows, audit run, audit summary. They read the light-curve files in bulk (headers, windows, the Stage 1 self-test and the
# UPSIDE-DOWN control events); no REAL event is listed or looked at. Low priority, 6 workers, 1 thread each. Makes a backup of the development-era audit tables first and checks afterwards that
# the development rows did not change.
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"; $env:NUMBA_NUM_THREADS = "1"
$env:SS_SET = "g2"; $env:VESPER_OPTS = "c6"
(Get-Process -Id $PID).PriorityClass = 'Normal'      # Ahmed 30 Oct: normal priority, he is not using the computer
$py = "D:\second-sun\.venv\Scripts\python.exe"; Set-Location D:\second-sun\pipeline
if (-not (Select-String -Path D:\second-sun\data\g2_sealed_download_log.txt -Pattern "ALL DONE" -Quiet)) { throw "the sealed download has not finished" }
if (-not (Test-Path D:\second-sun\data\g2\audit_dev_only_2026-10-30)) { Copy-Item -Recurse D:\second-sun\data\g2\audit D:\second-sun\data\g2\audit_dev_only_2026-10-30 }
& $py -W ignore audit_all.py windows 6
& $py -W ignore audit_all.py run 6
& $py -W ignore audit_all_summary.py 2>&1 | Select-Object -First 12      # its last print crashes AFTER best_per_star_sector.csv is written; harmless (RESUME 29 Oct)
& $py -W ignore audit_dev_unchanged.py
& $py -W ignore toi1338b_expected.py
& $py -W ignore sealed_run.py check
