"""C1 sanity test (10 Nov 2026, Opus 5.5): c0_mask_loss.py (imported, NOT edited) with the C0 mask swapped for C1 (c1_mask.py). In its summary the column
labelled 'C0' is C1. Rows (private) -> data\\fable_audit_mask\\rows_<set>_c1<C1_TAG>.pkl.  Usage: SS_SET=g2 C1_Z=5 python c1_mask_loss.py run 8 6 | summary"""
import os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import c0_mask_loss as M
import c1_mask as C1

M.H.ROWS = M.H.OUT / f"rows_{M.H.SET}_c1{os.environ.get('C1_TAG', '')}.pkl"
M.C0.mask_runs = lambda t, f, p, tic=None: C1.mask_runs(t, f, p, tic=M.C0.CURRENT_TIC if tic is None else tic)

if __name__ == "__main__":
    if sys.argv[1] == "run":
        M.run(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("\n".join(M.summary()))
