# Vesper 0.9 study runs on the DEVELOPMENT slice only (research/stage3/V9-STUDY-PLAN.md; rules written before this ran).
# 1. full dev chain with VESPER_OPTS=c6,dg,nd,fl   2. planted-dip recovery (chain_recovery.py) on 300 development star-sectors with the same options.
# BelowNormal, 5 processes, one numba thread each. Writes status lines to research\stage3\v9-study-status.txt (DONE or FAILED at the end). Resumable: rerun the same command.
# Usage (PowerShell):  .\run_v9_study.ps1 [-Options "c6,dg,nd,fl"] [-Label v9dev] [-Procs 5]
param([string]$Options = "c6,dg,nd,fl", [string]$Label = "v9dev", [int]$Procs = 5)
$ErrorActionPreference = "Continue"
$root = "D:\second-sun"; $pipe = "$root\pipeline"; $py = "$root\.venv\Scripts\python.exe"; $status = "$root\research\stage3\v9-study-status.txt"
$env:SS_SET = "g2"; $env:VESPER_OPTS = $Options; $env:NUMBA_NUM_THREADS = "1"; $env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"
(Get-Process -Id $PID).PriorityClass = "BelowNormal"
function Say($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $m" | Add-Content $status; Write-Host $m }
Set-Location $pipe
Say "START options=$Options label=$Label procs=$Procs"
$log1 = "$root\research\stage3\v9-devrun.log"
& $py stage3.py devrun $Procs *> $log1
$line = Select-String -Path $log1 -Pattern "G2 DEVELOPMENT RUN" | Select-Object -First 1
if (-not $line) { Say "FAILED: devrun printed no run folder (see $log1)"; exit 1 }
$run = ($line.Line -split "->")[1].Trim() | Split-Path -Leaf
Say "devrun done: $run"
$env:SS_RUN = $run
$log2 = "$root\research\stage3\v9-chainrecovery.log"
& $py chain_recovery.py run 300 $Procs $Label *> $log2
if (Select-String -Path $log2 -Pattern "CHAIN RECOVERY DONE" -Quiet) { Say "DONE run=$run rows=rows_$Label.pkl" } else { Say "FAILED: chain_recovery did not finish (see $log2)"; exit 1 }
