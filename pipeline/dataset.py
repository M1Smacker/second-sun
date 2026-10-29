"""Which star set the chain reads (G2 preregistration section 4: the data paths switch, no rule changes). SS_SET=g1 (the default) gives exactly the paths the frozen v7 code used before
this file existed; SS_SET=g2 points the same code at data/g2 and the G2 tables. Set it in the environment, not in code: worker processes inherit it. No rule, number or threshold lives here."""
import os, pathlib

ROOT = pathlib.Path(r"D:\second-sun")
NAME = os.environ.get("SS_SET", "g1")
if NAME == "g1":
    DATA = ROOT / "data" / "g1"
    TARGETS = ROOT / "targets" / "g1_targets.csv"
    AUDIT = ROOT / "research" / "audit-2026-10-23"          # audit_all.csv, spoc_windows.pkl, best_per_star_sector.csv, per_star.csv
    RUNS = ROOT / "data" / "stage3"
    PREP = ROOT / "data" / "stage3_prep"
    TIC_LIST = ROOT / "targets" / "g1_coverage.csv"         # every star of the set (column tic)
elif NAME == "g2":
    DATA = ROOT / "data" / "g2"
    TARGETS = ROOT / "targets" / "g2_chain_targets.csv"     # g2_targets.csv plus the catalogue ephemeris, made by targets_g2_chain.py
    AUDIT = DATA / "audit"
    RUNS = ROOT / "data" / "stage3_g2"
    PREP = ROOT / "data" / "stage3_g2_prep"
    TIC_LIST = ROOT / "targets" / "g2_targets.csv"
else:
    raise SystemExit(f"SS_SET must be g1 or g2, not {NAME!r}")
MANIFEST = DATA / "manifest.csv"
BEST = AUDIT / "best_per_star_sector.csv"
