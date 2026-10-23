"""Regression proof for the B1/B2/B5 fixes (2026-10-23): old vs new detect_v2 on every light curve on disk.
Usage: python regress_detect_v2.py <folder holding detect_v2_old.py>   (the old file = `git show e66aac4:pipeline/detect_v2.py`).
Expected: identical loads and identical events everywhere EXCEPT pre-56 QLP (column change by design) and
non-SPOC/QLP products (now SAP instead of lightkurve's default flux)."""
import sys, glob, importlib.util, warnings
import numpy as np
import detect_v2 as new
warnings.filterwarnings("ignore")
spec = importlib.util.spec_from_file_location("old", sys.argv[1] + r"\detect_v2_old.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

same = diff = 0
for p in sorted(glob.glob(r"D:\second-sun\data\**\*.fits", recursive=True)):
    try:
        to, fo, no = old.load(p)
    except Exception as e:
        print("old load fails (skip):", p.split("\\")[-1][:60], type(e).__name__); continue
    tn, fn, nn, info = new.load(p, info=True)
    load_same = len(to) == len(tn) and np.array_equal(to, tn) and np.allclose(fo, fn, equal_nan=True) and no == nn
    if len(tn) < 50:
        print(f"tiny: {p[-60:]}"); continue
    eo, en = old.find_events(to, fo), new.find_events(tn, fn)
    ev_same = eo == en
    tag = f"S{info['sector']} {info['product']} {info['column']} {info['cadence_min']} min"
    if load_same and ev_same:
        same += 1
    else:
        diff += 1
        print(f"DIFF {tag}: load same={load_same}, events old {len(eo)} new {len(en)}  {p.split(chr(92))[-1][:55]}")
print(f"identical: {same}, different: {diff}")
