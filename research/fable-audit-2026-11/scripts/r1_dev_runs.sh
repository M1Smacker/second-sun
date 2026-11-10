#!/bin/bash
# Re-search 1 DEVELOPMENT runs on the design-seen stars (R1-PREREGISTRATION.md section 3; before the freeze): G3 then G2, Petrova code with the switch p1 on, 6 workers Normal priority.
cd /d/second-sun/pipeline
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1
PY=/d/second-sun/.venv/Scripts/python.exe
LOG=/d/second-sun/data/r1_dev_runs.log
echo "start $(date '+%H:%M:%S')" > $LOG
for s in g3 g2; do
  echo "begin $s $(date '+%H:%M:%S')" >> $LOG
  SS_SET=$s VESPER_OPTS=c6,p1 $PY -W ignore r1_run.py dev seen 6 >> $LOG 2>&1
  echo "end $s $(date '+%H:%M:%S')" >> $LOG
done
echo "ALLDONE $(date '+%H:%M:%S')" >> $LOG
