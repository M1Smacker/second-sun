"""Vesper study: the false-alarm yardstick of a full run folder. Upside-down tier-1 events per 1,000 best-product star-sectors (rule: 8 or fewer on G1 and on G2 dev), with real tier-1 beside it.
Usage: SS_SET=g1|g2 python fa_count.py <run folder name under data\\stage3 or data\\stage3_g2> [label]   (appends to research\\stage3\\fa-counts.txt; aggregates only)"""
import sys, pathlib
import numpy as np, pandas as pd
import stage3_core as C, stage3_report as R, vopts as V

run = sys.argv[1]; label = sys.argv[2] if len(sys.argv) > 2 else run
ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
pr = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
E = ev[ev.primary]; T1 = ["1A", "1L", "1B"]
r, f = E[(E.kind == "real") & E.tier.isin(T1)], E[(E.kind == "flip") & E.tier.isin(T1)]
n = len(pr)
bars = " / ".join(f"{t}: {int((r.snr >= t).sum())}-{int((f.snr >= t).sum())}" for t in (7, 8, 10, 12))
line = (f"{C.DS.NAME} {label} (options {sorted(V.ON) or 'none'}; run {run}): star-sectors {n}; tier-1 real {len(r)}, upside-down {len(f)}; upside-down per 1,000 star-sectors {1000 * len(f) / n:.2f} "
        f"(rule: 8 or fewer); real-upside-down by SNR bar {bars}; flagged by step: real {int(E[E.kind == 'real'].step.sum())}, upside-down {int(E[E.kind == 'flip'].step.sum())}")
print(line)
with open(C.ROOT / "research" / "stage3" / "fa-counts.txt", "a", encoding="utf-8") as fh:
    fh.write(line + "\n")
