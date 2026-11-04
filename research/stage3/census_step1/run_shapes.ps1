# Runs the shape variants one after the other at Normal priority, 8 workers (Ahmed away; 70% CPU rule). Logs to data\shape_*.log
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"; $env:NUMBA_NUM_THREADS = "1"; $env:PYTHONUNBUFFERED = "1"
$env:SS_SET = "g3"; $env:VESPER_OPTS = "c6"; $env:SS_RUN = "g3_e7886a71a61f"
$py = "D:\second-sun\.venv\Scripts\python.exe"
foreach ($s in @("sym", "skew", "stretch", "box")) {
    $env:SHAPE = $s
    & $py -W ignore D:\second-sun\research\stage3\census_step1\chain_recovery_shape.py run 300 8 ("shape_" + $s) 2>&1 | Out-File ("D:\second-sun\data\shape_" + $s + ".log") -Encoding utf8
}
"ALL SHAPES DONE" | Out-File D:\second-sun\data\shape_done.txt -Encoding utf8
