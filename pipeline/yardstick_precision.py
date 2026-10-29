"""Vesper study: how precisely does one chain_recovery run measure K50 (the depth, in units of the 8 h box noise, at which half of injected dips reach tier 1)? Bootstrap over star-sectors (the unit that
was sampled), per box length, for G1 (rows_v7) and G2 dev (rows_g2dev). Also the PAIRED design: when two versions see the SAME injections, the difference in tier-1 recovery is measured per injection,
so the noise of the comparison is set by the injections whose outcome changes, not by the whole sample. Here we estimate how many changed outcomes a 10% K50 shift needs to be seen.
Usage: python yardstick_precision.py   (writes research\\stage3\\yardstick-precision.txt)"""
import pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(r"D:\second-sun")
T1 = ("1A", "1L", "1B")


def k50(d):
    """Linear interpolation of tier-1 share against K; NaN if 50% is never reached."""
    s = d.groupby("K").tier1.mean().sort_index()
    ks, v = s.index.values, s.values
    for i in range(1, len(v)):
        if v[i - 1] < 0.5 <= v[i]:
            return ks[i - 1] + (0.5 - v[i - 1]) / (v[i] - v[i - 1]) * (ks[i] - ks[i - 1])
    return 0.0 if len(v) and v[0] >= 0.5 else np.nan


def boot(rows, name, nb=1000):
    r = rows[rows.get("error").isna()] if "error" in rows else rows
    d = r[(r.sign == 1) & r.K.notna()].copy()
    d["tier1"] = d.tier.isin(T1)
    keys = d[["tic", "sector"]].drop_duplicates().values
    rng = np.random.default_rng(1)
    out = [f"{name}: {len(keys)} star-sectors, {len(d)} dip injections"]
    for dur, g in d.groupby("dur"):
        by = {tuple(k): x for k, x in g.groupby(["tic", "sector"])}
        ks = list(by)
        est = k50(g)
        bs = []
        for _ in range(nb):
            pick = rng.integers(0, len(ks), len(ks))
            bs.append(k50(pd.concat([by[ks[i]] for i in pick])))
        bs = np.array(bs)
        ok = np.isfinite(bs)
        lo, hi = (np.percentile(bs[ok], [2.5, 97.5]) if ok.mean() > 0.5 else (np.nan, np.nan))
        out.append(f"  box {dur:4.0f} h: K50 {est:5.2f}; 95% range {lo:5.2f} to {hi:5.2f} (+-{100 * (hi - lo) / 2 / est if est == est and est else float('nan'):.0f}%); share of resamples where 50% is reached {100 * ok.mean():.0f}%")
        sl = g.groupby("K").tier1.mean()
        out.append(f"    tier-1 share by K: " + ", ".join(f"{k:g}: {100 * v:.0f}%" for k, v in sl.items()))
    return out


def paired_note():
    """A 10% lower K50 at K about 10 moves the recovery curve by about one K step's worth of slope. With slope s (share per unit K) near K50, a 10% K50 shift (about 1 K unit) changes the
    tier-1 share by about s. With n injections at K 8 to 12, the paired test sees about n x s changed outcomes in one direction, against about sqrt(n x f) noise where f is the share that flips either way."""
    return ["Paired design (same injections through both versions): a 10% K50 shift near K = 10 changes the tier-1 share by roughly the curve's slope per K unit (about 5 to 8 points per K on these curves),",
            "so about 5 to 8% of the injections at K 8 to 12 change outcome in one direction. With the 300-star-sector design (about 3,400 dips at K 8 to 12 per run) that is 170 to 270 one-way changes,",
            "far above the random flips seen between dip and mirror bump (about 250 to 340 of 3,400 each way, which is the noise of a comparison between two DIFFERENT shapes, an upper bound).",
            "Conclusion to test in C: compare versions on the SAME injections (paired, exact binomial on the changed outcomes), not by two separate K50 numbers."]


if __name__ == "__main__":
    txt = ["Precision of the Vesper yardstick (29 Oct 2026). Bootstrap over star-sectors, 1,000 resamples.", ""]
    txt += boot(pd.read_pickle(ROOT / "data" / "chain_recovery" / "rows_v7.pkl"), "G1 rows_v7") + [""]
    txt += boot(pd.read_pickle(ROOT / "data" / "chain_recovery_g2" / "rows_g2dev.pkl"), "G2 dev rows_g2dev") + [""]
    txt += paired_note()
    print("\n".join(txt))
    (ROOT / "research" / "stage3" / "yardstick-precision.txt").write_text("\n".join(txt), encoding="utf-8")
