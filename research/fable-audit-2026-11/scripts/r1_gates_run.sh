#!/bin/bash
# Re-search 1 gate runs (r1_gate.py, 300 star-sectors per set, 60 per period bin) on the development runs of the seen stars. G3 starts when its development run is done (3 workers while G2 is still being
# searched); G2 starts when all development runs are done (6 workers). Summaries -> research/stage3/R1-GATE-RESULT-<set>.txt. Real events are not shown.
cd /d/second-sun/pipeline
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1
PY=/d/second-sun/.venv/Scripts/python.exe
DEV=/d/second-sun/data/r1_dev_runs.log; LOG=/d/second-sun/data/r1_gates.log
echo "start $(date '+%H:%M:%S')" > $LOG
until grep -q "end g3" $DEV; do sleep 10; done
RUN3=$(ls -d /d/second-sun/data/stage3_g3/r1dev_g3_seen_* | head -1 | xargs -n1 basename)
echo "g3 gate run on $RUN3 $(date '+%H:%M:%S')" >> $LOG
( SS_SET=g3 SS_RUN=$RUN3 VESPER_OPTS=c6,p1 $PY -W ignore r1_gate.py run 300 3 >> $LOG 2>&1; SS_SET=g3 SS_RUN=$RUN3 VESPER_OPTS=c6,p1 $PY -W ignore r1_gate.py summary >> $LOG 2>&1; echo "end g3 gates $(date '+%H:%M:%S')" >> $LOG ) &
until grep -q ALLDONE $DEV; do sleep 10; done
RUN2=$(ls -d /d/second-sun/data/stage3_g2/r1dev_g2_seen_* | head -1 | xargs -n1 basename)
echo "g2 gate run on $RUN2 $(date '+%H:%M:%S')" >> $LOG
SS_SET=g2 SS_RUN=$RUN2 VESPER_OPTS=c6,p1 $PY -W ignore r1_gate.py run 300 6 >> $LOG 2>&1
SS_SET=g2 SS_RUN=$RUN2 VESPER_OPTS=c6,p1 $PY -W ignore r1_gate.py summary >> $LOG 2>&1
echo "end g2 gates $(date '+%H:%M:%S')" >> $LOG
wait
echo "ALLDONE $(date '+%H:%M:%S')" >> $LOG
