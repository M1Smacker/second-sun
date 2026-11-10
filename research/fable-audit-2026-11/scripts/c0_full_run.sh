#!/bin/bash
# C0 full-size test: time-only catalogue mask (no refit, two-Gaussian width fallback), 50 files per period bin and product family, G2 then G3, 6 workers.
# Rows (private) -> data\fable_audit_mask\rows_<set>_c0_full.pkl ; summaries -> evidence/c0_mask_loss_<set>_full.txt (counts only).
cd /d/second-sun/research/fable-audit-2026-11/scripts || exit 1
export PYTHONUTF8=1 NUMBA_NUM_THREADS=1 C0_REFIT=0 C0_TAG=_full
PY=/d/second-sun/.venv/Scripts/python.exe
for S in g2 g3; do
  export SS_SET=$S
  echo "start $S $(date +%H:%M:%S)"
  $PY c0_mask_loss.py run 50 6 2>/dev/null | tail -1
  $PY c0_mask_loss.py summary 2>/dev/null > ../evidence/c0_mask_loss_${S}_full.txt
  echo "done $S $(date +%H:%M:%S)"
done
