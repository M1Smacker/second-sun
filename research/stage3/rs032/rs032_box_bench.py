"""T35 bench price (Claude, 14 Nov 2026): options B and B3 (3 h box held). Rule in T35-BOX-RULE-2026-11-14.md, written before running."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs031"))
import pandas as pd
import rs031_dsp_bench as D
O, K = D.O, D.K


def tier_under(df, groups, idx, opt, C):
    row = df.loc[idx]
    d = row.to_dict(); d["dominated"] = O.dominated(row, idx, groups, "OAE")
    if K.touches(d["sector"], float(d["center"]), float(d.get("dur_h") or 0) / 24):
        d["gap_dump"] = True
    t = C.tier_of(d)
    if opt == "B3" and float(d.get("dur_h") or 0) <= 3.0 and t in O.PR.T1:
        return "2box"
    return t


O.tier_under, O.OPTS = tier_under, ("B", "B3")
if __name__ == "__main__":
    dd_ = O.PR.ROOT / "data" / "rs032"; dd_.mkdir(exist_ok=True)
    O.__file__ = str(HERE / "rs024_options_shadow.py")
    _tc = pd.DataFrame.to_csv
    def to_csv(self, path=None, *a, **k):
        if path is not None and "options-trials" in str(path):
            path = dd_ / "box-trials.csv"
        return _tc(self, path, *a, **k)
    pd.DataFrame.to_csv = to_csv
    O.main(None)
    (HERE / "options.json").replace(HERE / "box.json")
