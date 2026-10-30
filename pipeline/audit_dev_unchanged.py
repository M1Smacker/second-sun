"""After the sealed audit steps: did anything about the DEVELOPMENT stars change in the shared G2 audit tables? Compares data/g2/audit (now) with the copy made before (audit_dev_only_2026-10-30).
Checks: audit_all.csv rows of development files identical; best_per_star_sector.csv rows of development star-sectors identical; spoc_windows.pkl entries of development stars identical.
Prints aggregates only. Usage: SS_SET=g2 python audit_dev_unchanged.py"""
import pickle, pandas as pd
import dataset as DS

NEW, OLD = DS.AUDIT, DS.AUDIT.with_name("audit_dev_only_2026-10-30")
dev = set(pd.read_csv(DS.TARGETS, comment="#").drop_duplicates("tic").query("slice == 'dev'").tic.astype(int))
for name, key in (("audit_all.csv", "file"), ("best_per_star_sector.csv", None)):
    a, b = pd.read_csv(OLD / name), pd.read_csv(NEW / name)
    a, b = a[a.tic.isin(dev)].reset_index(drop=True), b[b.tic.isin(dev)].reset_index(drop=True)
    cols = [c for c in a.columns if c in b.columns]
    key_cols = ["tic", "file"] if key else ["tic", "sector"]
    m = a[cols].merge(b[cols], on=key_cols, how="outer", suffixes=("_old", "_new"), indicator=True)
    same = int((m["_merge"] == "both").sum()); diff = 0
    for c in cols:
        if c in key_cols:
            continue
        x, y = m[c + "_old"], m[c + "_new"]
        diff += int((~((x == y) | (x.isna() & y.isna()))).sum())
    print(f"{name}: {len(a)} development rows before, {len(b)} after; matched {same}; only-before {int((m['_merge'] == 'left_only').sum())}; only-after {int((m['_merge'] == 'right_only').sum())}; cell differences {diff}")
wa, wb = pickle.load(open(OLD / "spoc_windows.pkl", "rb")), pickle.load(open(NEW / "spoc_windows.pkl", "rb"))
n = d = 0
for k, v in wa.items():
    for tic, w in v.items():
        if tic in dev:
            n += 1; d += int(wb.get(k, {}).get(tic) != w)
print(f"spoc_windows.pkl: {n} development window entries before; {d} differ after")
