"""T130 check of the correction-box sentence 'almost all of them in binaries slower than 20 days' (14 Nov 2026).
Share of strong dips (K 25, 8 h) lost to the old mask that comes from each binary-period bin, weighted by the files of each bin in the
hunt manifest (the same weighting as WO-F01 Part A Result 2). Inputs: the before/after cells of evidence/wo_f01a_mask_loss_g2.txt and
_g3.txt (K 25, 8 h, both families pooled) and the manifests with each star's catalogue period. Counts only."""
import pandas as pd
from pathlib import Path
ROOT = Path(r"D:\second-sun")
BINS = [(5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e9)]
CELLS = {"g2": [(0.66, 1.00), (0.26, 1.00), (0.07, 1.00), (0.01, 1.00), (0.02, 0.99)],      # wo_f01a_mask_loss_g2.txt, B, K 25 dur 8 h
         "g3": [(0.45, 1.00), (0.16, 1.00), (0.09, 1.00), (0.04, 1.00), (0.00, 1.00)]}      # WO-F01-PART-A-RESULT, G3 K 25, 8 h (after taken as 1.00)
TG = {"g2": ROOT / "targets" / "g2_chain_targets.csv", "g3": ROOT / "targets" / "g3_chain_targets.csv"}
for s in ("g2", "g3"):
    man = pd.read_csv(ROOT / "data" / s / "manifest.csv").drop_duplicates("file")
    per = pd.read_csv(TG[s], comment="#").drop_duplicates("tic").set_index("tic").p_bin_d
    man["P"] = man.tic.map(per)
    w = [int(((man.P >= lo) & (man.P < hi)).sum()) for lo, hi in BINS]
    lost = [wi * (a - b) for wi, (b, a) in zip(w, CELLS[s])]
    tot = sum(lost)
    print(f"{s}: files per bin {w} (no period {int(man.P.isna().sum())}); share of lost strong dips by bin " +
          " ".join(f"{100 * x / tot:.0f}%" for x in lost) + f"; slower than 20 d: {100 * sum(lost[3:]) / tot:.0f}%; slower than 14 d: {100 * sum(lost[2:]) / tot:.0f}%")
