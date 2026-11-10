#!/bin/bash
# FINAL zero-difference proofs for Petrova 1.0.0 with the switch p1 OFF, re-run on the committed code before the freeze (11 Nov 2026). Same three proofs as p1_off_proofs.sh, 3 workers (the gate run uses the other cores; his 70 percent CPU rule).
# The proof files research/stage3/zero-diff-P1-off*.txt are overwritten; r1_run.py freeze reads them.
cd /d/second-sun/pipeline
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1
PY=/d/second-sun/.venv/Scripts/python.exe
LOG=/d/second-sun/data/p1_off_proofs_final.log
echo "start $(date '+%H:%M:%S') git $(git -C /d/second-sun rev-parse --short HEAD)" > $LOG
env -u VESPER_OPTS -u SS_SET $PY -W ignore zero_diff.py 300 3 P1-off >> $LOG 2>&1
echo "done1 $(date '+%H:%M:%S')" >> $LOG
env -u SS_SET VESPER_OPTS=c6 $PY -W ignore zero_diff.py 300 3 P1-off-c6 >> $LOG 2>&1
echo "done2 $(date '+%H:%M:%S')" >> $LOG
SS_SET=g2 SS_RUN=sealed_5f73692944aa VESPER_OPTS=c6 $PY -W ignore zero_diff.py 300 3 P1-off-g2-sealed-c6 >> $LOG 2>&1
echo "ALLDONE $(date '+%H:%M:%S')" >> $LOG
