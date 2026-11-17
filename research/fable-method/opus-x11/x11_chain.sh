#!/bin/bash
# X11 lever 1: two queues, NUMBA_NUM_THREADS=1 set inside the scorers. Checkpoint = one output JSON per run in out/.
PY=/d/second-sun/.venv/Scripts/python.exe; X=/d/second-sun/data/opus-x11; L=$X/logs; mkdir -p $L
run() { [ -f $X/out/$1 ] && { echo "skip $1"; return; }; $PY -I -B $X/$2 $3 $4 $5 > $L/$1.log 2>&1; echo "done $1 $?"; }
( run x11-planets-g2-V0.json x11_score_orig.py g2 planets V0
  run x11-planets-g2-V2.json x11_score_orig.py g2 planets V2
  run x11f-planets-g2-V0.json x11_score_fresh.py g2 planets V0
  run x11fm-planets-g2-V2.json x11_score_freshm2.py g2 planets V2 ) > $L/queue1.txt &
( run x11-planets-g3-V0.json x11_score_orig.py g3 planets V0
  run x11-planets-g3-V2.json x11_score_orig.py g3 planets V2
  run x11f-planets-g3-V0.json x11_score_fresh.py g3 planets V0
  run x11fm-planets-g3-V2.json x11_score_freshm2.py g3 planets V2
  run x11-T156-g3-V0.json x11_score_orig.py g3 T156 V0
  run x11-T156-g2-V0.json x11_score_orig.py g2 T156 V0 ) > $L/queue2.txt &
wait; echo ALL DONE > $L/all-done.txt
