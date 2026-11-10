"""Re-search 1 star list (Petrova 1.0.0 preregistration, step A1, 11 Nov 2026).

Rule (fixed before any light is read with Petrova): every row of g1_targets.csv, g2_targets.csv (development AND
sealed slices) and g3_targets.csv, all of which already have a catalogue binary period of 5 d or more. Each star
is marked design_seen = 1 when it appears in ANY of the private mask-design test files under data/fable_audit_mask
(real-light samples that were looked at as counts while the mask was designed). Catalogue columns only; no light
is read and no event is touched. The private files are used for their star ids, never printed.

Writes targets/r1_targets.csv and prints counts only.
"""
import glob
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "targets"
OUT = T / "r1_targets.csv"
EDGES = [5.0, 10.0, 14.0, 20.0, 27.4, 1e9]
LABELS = ["5-10", "10-14", "14-20", "20-27", "27+"]


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    g1 = pd.read_csv(T / "g1_targets.csv", comment="#")
    g2 = pd.read_csv(T / "g2_targets.csv", comment="#")
    g3 = pd.read_csv(T / "g3_targets.csv", comment="#")
    print("columns g1", list(g1.columns)); print("columns g2", list(g2.columns)); print("columns g3", list(g3.columns))
    parts = []
    for name, d in (("g1", g1), ("g2", g2), ("g3", g3)):
        x = d[["tic", "tmag", "p_bin_d"]].copy()
        x["list"] = name
        x["g2_slice"] = d["slice"] if name == "g2" else ""
        parts.append(x)
    a = pd.concat(parts, ignore_index=True)
    a["tic"] = a["tic"].astype("int64")
    assert (a["p_bin_d"] >= 5.0).all(), "a row below 5 d"
    a["pbin"] = pd.cut(a["p_bin_d"], EDGES, labels=LABELS, right=False).astype(str)
    seen = set()
    for p in glob.glob(str(ROOT / "data" / "fable_audit_mask" / "rows_*.pkl")):
        seen |= set(pd.read_pickle(p)["tic"].astype("int64"))
    a["design_seen"] = a["tic"].isin(seen).astype(int)
    seen_hash = hashlib.sha256(",".join(str(t) for t in sorted(seen & set(a["tic"]))).encode()).hexdigest()
    a = a[["tic", "list", "tmag", "p_bin_d", "pbin", "g2_slice", "design_seen"]].sort_values(["list", "tic", "p_bin_d"])
    hdr = [
        "# Re-search 1 star list, 11 Nov 2026 (research/stage3/PLAN-2026-11-11-FREEZE-HUNT-LEARNING.md, step A1)",
        "# rule: every row of g1_targets, g2_targets (dev and sealed) and g3_targets; catalogue binary period 5 d or more; one row per (tic, period)",
        f"# g1_targets sha256 {sha_file(T / 'g1_targets.csv')}",
        f"# g2_targets sha256 {sha_file(T / 'g2_targets.csv')}",
        f"# g3_targets sha256 {sha_file(T / 'g3_targets.csv')}",
        "# design_seen = 1: the star is in a real-light sample whose counts were looked at while the mask was designed (the sealed run's pass or fail uses design_seen = 0 only)",
        f"# design_seen star-list sha256 (sorted tic ids joined by commas) {seen_hash}",
        f"# rows {len(a)}, unique stars {a['tic'].nunique()}",
    ]
    OUT.write_text("\n".join(hdr) + "\n" + a.to_csv(index=False, lineterminator="\n"), encoding="utf-8", newline="")
    print("written", OUT.name, "sha256", sha_file(OUT))
    print("rows", len(a), "unique stars", a["tic"].nunique())
    u = a.drop_duplicates("tic")
    print(u.groupby(["list", "design_seen"]).size().unstack(fill_value=0).to_string())
    print(a.groupby(["pbin", "design_seen"]).size().unstack(fill_value=0).reindex(LABELS).to_string())
    print("stars in two lists:", int(a.groupby("tic")["list"].nunique().gt(1).sum()))


if __name__ == "__main__":
    main()
