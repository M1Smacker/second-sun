# The G3 search and its follow-ups, one after the other. RUN ONLY AFTER Ahmed's explicit go: g3_run.py refuses without research\stage3\G3-GO.txt, and this script stops at the first step that fails.
# 1 the one G3 search through g3_run.py (hash guard); 2 the asymmetry ratio of this run; 3 completeness on 300 random G3 star-sectors (chain_recovery.py, unchanged logic); 4 the scorecard (benchmark_g3.py).
# Each step logs to data\g3_*_log.txt. Start it detached with the priority that fits (BelowNormal while Ahmed is at the PC; Normal with 8 workers while he is away). Usage: .\g3_go.ps1 [workers]
param([int]$n = 8)
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"; $env:NUMBA_NUM_THREADS = "1"; $env:PYTHONUNBUFFERED = "1"
$env:SS_SET = "g3"; $env:VESPER_OPTS = "c6"
$py = "D:\second-sun\.venv\Scripts\python.exe"; $log = "D:\second-sun\data"; Set-Location D:\second-sun\pipeline
$fz = Get-Content D:\second-sun\research\stage3\SETTINGS_FROZEN_V81.json -Raw | ConvertFrom-Json; $run = "g3_" + $fz.hash.Substring(0, 12)
function Say($m) { "$(Get-Date -Format HH:mm:ss) $m" | Add-Content "$log\g3_steps_log.txt" }
Say "1 G3 search start ($run, $n workers)"
& $py -W ignore g3_run.py run $n 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\g3_run_log.txt" -Encoding utf8
Say "1 G3 search exit $LASTEXITCODE"
if (-not (Select-String -Path "$log\g3_run_log.txt" -Pattern "G3 SEARCH DONE" -Quiet)) { Say "STOP: the search did not finish"; exit 1 }
Say "2 asymmetry start"
& $py -W ignore asymmetry_test.py 1500 v5 $run 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\g3_asym_log.txt" -Encoding utf8
Say "2 asymmetry exit $LASTEXITCODE"
Say "3 completeness start"
$env:SS_RUN = $run
& $py -W ignore chain_recovery.py run 300 $n g3 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\g3_chain_log.txt" -Encoding utf8
Say "3 completeness exit $LASTEXITCODE"
Remove-Item Env:SS_RUN -ErrorAction SilentlyContinue
Say "4 scorecard start"
& $py -W ignore benchmark_g3.py $run g3 "D:\second-sun\data\chain_recovery_g3\rows_g3.pkl" 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\g3_benchmark_log.txt" -Encoding utf8
Say "4 scorecard exit $LASTEXITCODE; ALL STEPS DONE"
