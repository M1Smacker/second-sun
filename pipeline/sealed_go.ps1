# The sealed G2 run and its follow-ups, one after the other (Ahmed's go, 30 Oct 2026; preregistration Amendment 1; G2-SEALED-PLAN.md section 7 steps 4 and 5).
# 1 the one sealed search through sealed_run.py (hash guard; blind live page); 2 the asymmetry ratio of this slice (the development file is restored afterwards);
# 3 completeness on 300 random sealed star-sectors; 4 the scorecard. Each step logs to data\sealed_*_log.txt. Normal priority, 6 workers, 1 thread each (Ahmed is not using the computer).
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"; $env:NUMBA_NUM_THREADS = "1"; $env:PYTHONUNBUFFERED = "1"
$env:SS_SET = "g2"; $env:VESPER_OPTS = "c6"
$py = "D:\second-sun\.venv\Scripts\python.exe"; $log = "D:\second-sun\data"; Set-Location D:\second-sun\pipeline
$run = "sealed_5f73692944aa"
function Say($m) { "$(Get-Date -Format HH:mm:ss) $m" | Add-Content "$log\sealed_steps_log.txt" }
Say "1 sealed search start"
& $py -W ignore sealed_run.py run 6 --watch 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\sealed_run_log.txt" -Encoding utf8
Say "1 sealed search exit $LASTEXITCODE"
if (-not (Select-String -Path "$log\sealed_run_log.txt" -Pattern "SEALED SEARCH DONE" -Quiet)) { Say "STOP: the search did not finish"; exit 1 }
Say "2 asymmetry start"
& $py -W ignore asymmetry_test.py 1500 v5 $run 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\sealed_asym_log.txt" -Encoding utf8
Copy-Item D:\second-sun\research\stage3\asymmetry_g2_v5.txt D:\second-sun\research\stage3\asymmetry_g2_sealed_v5.txt -Force
Set-Location D:\second-sun; git checkout -- research/stage3/asymmetry_g2_v5.txt; Set-Location D:\second-sun\pipeline
Say "2 asymmetry done (sealed file saved, development file restored)"
Say "3 completeness start"
$env:SS_RUN = $run
& $py -W ignore chain_recovery.py run 300 6 sealed 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\sealed_chain_log.txt" -Encoding utf8
Say "3 completeness exit $LASTEXITCODE"
Remove-Item Env:SS_RUN -ErrorAction SilentlyContinue
Say "4 scorecard start"
& $py -W ignore benchmark_g2.py $run sealed "D:\second-sun\data\chain_recovery_g2\rows_sealed.pkl" "D:\second-sun\data\chain_recovery_g2\rows_g2dev.pkl" 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\sealed_benchmark_log.txt" -Encoding utf8
Say "4 scorecard exit $LASTEXITCODE; ALL STEPS DONE"
