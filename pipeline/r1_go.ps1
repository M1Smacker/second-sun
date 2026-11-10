# Re-search 1 (Petrova 1.0.0), the ONE sealed search of the unseen stars, in two parts: G3 first (328 stars), then G2 (475 stars). G1 (549 Kepler-field stars) waits for its own eclipse widths (preregistration section 8).
# RUN ONLY AFTER Ahmed's fresh explicit one-word go: r1_run.py refuses without research\stage3\R1-GO-unseen.txt, without SETTINGS_FROZEN_P100.json and without a clean tree, and this script stops at the first step that fails.
# The analysis (S1 to S4, counts first) is a separate step (B4) and is not started here. Each step logs to data\r1_*_log.txt. Usage: .\r1_go.ps1 [workers]   (Ahmed's rule: 70 percent CPU, so 6 workers on his 12 cores)
param([int]$n = 6)
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"; $env:NUMBA_NUM_THREADS = "1"; $env:PYTHONUNBUFFERED = "1"
$env:VESPER_OPTS = "c6,p1"
$py = "D:\second-sun\.venv\Scripts\python.exe"; $log = "D:\second-sun\data"; Set-Location D:\second-sun\pipeline
$fz = Get-Content D:\second-sun\research\stage3\SETTINGS_FROZEN_P100.json -Raw | ConvertFrom-Json; $h12 = $fz.hash.Substring(0, 12)
function Say($m) { "$(Get-Date -Format HH:mm:ss) $m" | Add-Content "$log\r1_steps_log.txt" }
# the exact library versions are saved BEFORE the search starts and copied into each run folder (as for G3, T128)
$fr = "$log\r1_pip_freeze.txt"
("python " + (& $py -c "import sys,platform;print(sys.version.split()[0], platform.platform())")) | Out-File $fr -Encoding utf8
& $py -m pip freeze 2>$null | Add-Content $fr -Encoding utf8
$frh = (Get-FileHash $fr -Algorithm SHA256).Hash.Substring(0, 16); Say "0 library versions saved to $fr (sha256 $frh, $((Get-Content $fr).Count) lines)"
$parts = @(@{ set = "g3"; no = 1; stars = 328 }, @{ set = "g2"; no = 2; stars = 475 })
foreach ($p in $parts) {
  $set = $p.set; $run = "r1_${set}_unseen_$h12"; $env:SS_SET = $set
  $label = "RE-SEARCH 1, part $($p.no) of 2: Petrova 1.0.0 on the $($p.stars) $($set.ToUpper()) stars that were not looked at while the filter was designed (blind, counts only)"
  # the Search window feed: counts only, blind, waits for the run folder (watch_export.py --wait); stops by itself when all three passes of this part are done
  Start-Process -FilePath $py -ArgumentList "-W", "ignore", "D:\second-sun\pipeline\watch_export.py", "D:\second-sun\data\stage3_$set\$run", "--blind", "--counts-only", "--wait", "--loop", "60", "--push", "--label", "`"$label`"" -WindowStyle Hidden
  Say "1.$($p.no) $set sealed search start ($run, $n workers)"
  & $py -W ignore r1_run.py run unseen $n 2>&1 | Where-Object { $_ -notmatch "Warning|warn|^\s*$" } | Out-File "$log\r1_${set}_run_log.txt" -Encoding utf8
  Say "1.$($p.no) $set sealed search exit $LASTEXITCODE"
  if (Test-Path "$log\stage3_$set\$run") { Copy-Item $fr "$log\stage3_$set\$run\pip-freeze.txt" -Force; Say "0 library versions copied into $run" }
  if (-not (Select-String -Path "$log\r1_${set}_run_log.txt" -Pattern "^SEARCH DONE" -Quiet)) { Say "STOP: the $set search did not finish"; exit 1 }
}
Say "ALL SEARCH STEPS DONE (both parts). Next: the counts-first analysis (B4); nothing is opened before it."
