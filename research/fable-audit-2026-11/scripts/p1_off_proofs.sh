#!/bin/bash
# Zero-difference proofs for Petrova 1.0.0 with the switch p1 OFF (the dormant code must not change Vesper 0.8.1): the same three proofs as 0.8.1 (g3_run.py PROOFS).
cd /d/second-sun/pipeline
PY=/d/second-sun/.venv/Scripts/python.exe
echo "start $(date '+%H:%M:%S')" > /d/second-sun/data/p1_off_proofs.log
env -u VESPER_OPTS -u SS_SET $PY -W ignore zero_diff.py 300 6 P1-off >> /d/second-sun/data/p1_off_proofs.log 2>&1
echo "done1 $(date '+%H:%M:%S')" >> /d/second-sun/data/p1_off_proofs.log
env -u SS_SET VESPER_OPTS=c6 $PY -W ignore zero_diff.py 300 6 P1-off-c6 >> /d/second-sun/data/p1_off_proofs.log 2>&1
echo "done2 $(date '+%H:%M:%S')" >> /d/second-sun/data/p1_off_proofs.log
SS_SET=g2 SS_RUN=sealed_5f73692944aa VESPER_OPTS=c6 $PY -W ignore zero_diff.py 300 6 P1-off-g2-sealed-c6 >> /d/second-sun/data/p1_off_proofs.log 2>&1
echo "ALLDONE $(date '+%H:%M:%S')" >> /d/second-sun/data/p1_off_proofs.log
