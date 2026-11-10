#!/bin/bash
# C1f full-size test: C0 windows + within-sector repeat lane (P under 13 d only; no cross-sector lane), Z 5, 50 files per period bin and family, G2 then G3.
# Rows (private) -> data\fable_audit_mask\rows_<set>_c1_ff.pkl ; summaries -> evidence/c1f_mask_loss_<set>_full.txt (counts only).
cd /d/second-sun/research/fable-audit-2026-11/scripts || exit 1
export PYTHONUTF8=1 NUMBA_NUM_THREADS=1 C0_REFIT=0 C1_Z=5 C1_PSLOW=1e9 C1_TAG=_ff
PY=/d/second-sun/.venv/Scripts/python.exe
for S in g2 g3; do
  export SS_SET=$S
  echo "start $S $(date +%H:%M:%S)"
  $PY c1_mask_loss.py run 50 6 2>/dev/null | tail -1
  $PY c1_mask_loss.py summary 2>/dev/null > ../evidence/c1f_mask_loss_${S}_full.txt
  echo "done $S $(date +%H:%M:%S)"
done
