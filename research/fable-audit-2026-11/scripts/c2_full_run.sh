#!/bin/bash
# C2 full-size test: C1f cadence mask + event-stage cross-sector veto (slow binaries), TOL 1 h, NMIN 2, Z 5, 50 files per bin and family, G2 then G3. Counts only in the summaries.
cd /d/second-sun/research/fable-audit-2026-11/scripts || exit 1
export PYTHONUTF8=1 NUMBA_NUM_THREADS=1 C0_REFIT=0 C1_PSLOW=1e9 C1_Z=5 C2_TOL_H=1 C2_NMIN=2
PY=/d/second-sun/.venv/Scripts/python.exe
for S in g2 g3; do
  export SS_SET=$S
  echo "start $S $(date +%H:%M:%S)"
  $PY c2_mask_loss.py run 50 6 2>/dev/null | tail -1
  $PY c2_mask_loss.py summary 2>/dev/null > ../evidence/c2_mask_loss_${S}_full.txt
  echo "done $S $(date +%H:%M:%S)"
done
