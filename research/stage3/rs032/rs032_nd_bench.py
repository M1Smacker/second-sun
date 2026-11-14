"""T32 nd and T31 dg priced under B (Claude, 14 Nov 2026). Rule in ND-DG-RULE-2026-11-14.md, written before running.
Options B, Bnd, Bnddg on the RS-024 harness; json next to this script, trials csv to data/rs032."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs031"))
import numpy as np, pandas as pd
import rs031_dsp_bench as D
O, K = D.O, D.K


def unphysical(dep):
    return dep is None or dep != dep or not np.isfinite(dep) or dep > 300_000


def dominated_nd(df, row, idx, groups):
    key = (row.tic, row.sector, row["product"])
    ix, kind, snr, t, ex = groups[key]
    un = np.array([unphysical(v) for v in pd.to_numeric(df.loc[ix, "depth_ppm"], errors="coerce").values])   # no cache: index sets differ per frame
    s = row.snr
    if s is None or s != s:
        return False
    dt = np.abs(t - row.center)
    m = (ix != idx) & (dt <= O.WIN_D) & (dt >= 1.5 * float(row.dur_h or 0) / 24) & ~ex & ~un
    return bool(m.any() and snr[m].max() >= s)


def tier_under(df, groups, idx, opt, C):
    row = df.loc[idx]
    d = row.to_dict()
    d["dominated"] = dominated_nd(df, row, idx, groups) if opt in ("Bnd", "Bnddg") else O.dominated(row, idx, groups, "OAE")
    if opt == "Bnddg" and unphysical(pd.to_numeric(d.get("depth_ppm"), errors="coerce")):
        d["too_deep"] = True
    if K.touches(d["sector"], float(d["center"]), float(d.get("dur_h") or 0) / 24):
        d["gap_dump"] = True
    return C.tier_of(d)


O.tier_under, O.OPTS = tier_under, ("B", "Bnd", "Bnddg")
if __name__ == "__main__":
    dd_ = O.PR.ROOT / "data" / "rs032"; dd_.mkdir(exist_ok=True)
    O.__file__ = str(HERE / "rs024_options_shadow.py")
    _tc = pd.DataFrame.to_csv
    def to_csv(self, path=None, *a, **k):
        if path is not None and "options-trials" in str(path):
            path = dd_ / "nd-trials.csv"
        return _tc(self, path, *a, **k)
    pd.DataFrame.to_csv = to_csv
    O.main(None)
    (HERE / "options.json").replace(HERE / "nd.json")
