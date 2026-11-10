"""Transcription test (11 Nov 2026): pipeline/petrova_mask.remove must give exactly the same removed cadences as the tested C1f mask (c1_mask.remove with C0_REFIT=0 C1_PSLOW=1e9 C1_Z=5) on real star-sector light.
Counts only: prints how many files agree. Usage: SS_SET=g2|g3 python p1_vs_c1f_equal.py N_PER"""
import os, sys, pathlib
os.environ.update(C0_REFIT="0", C1_PSLOW="1e9", C1_Z="5")
sys.path.insert(0, str(pathlib.Path(__file__).parent)); sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np
import wo_f01a_mask_loss as H, c1_mask as C1, c0_catalogue_mask as C0, petrova_mask as PM
H.init()
jobs, _ = H.sample(int(sys.argv[1]))
same = diff = skip = 0; rem = []
for j in jobs:
    path, tic = j[0], j[1]
    try:
        tf, meta, st = H.load_windowed(path)
        if tf is None:
            skip += 1; continue
        t, f = tf; per = H.A.PER.get(tic, [])
        a = C1.remove(t, f, per, tic); b = PM.remove(t, f, per, PM.cat().get(int(tic)))
        same += int((a == b).all()); diff += int(not (a == b).all()); rem.append(float(b.mean()))
    except Exception as e:
        skip += 1; print("skip", type(e).__name__, str(e)[:80])
print(f"set {H.SET}: files compared {same + diff}, identical removed cadences {same}, different {diff}, skipped {skip}; median share of cadences removed {np.median(rem):.3f}")
