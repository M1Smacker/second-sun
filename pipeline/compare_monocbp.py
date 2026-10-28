"""Compare mono-cbp's events with ours on the stars both searches looked at. PRINTS AGGREGATES ONLY (no TIC, no time), safe to paste into notes.
mono-cbp (GPL-3.0) is run OUTSIDE this repository (D:\\ss-external); this script only reads its output files, it imports none of its code.
Their events: TIC SECTOR TIME DEPTH DURATION SNR ... DET_DEPENDENCE (0 = robust to the detrending window) and, if vetted, a model-comparison class
(T transit, AT ambiguous transit, A ambiguous, Sin/L/St = sinusoid/linear/step). Their SNR scale is not ours: they search down to about SNR 3.
Ours: the frozen Stage 3 events (SNR >= 7), best product per star-sector, real curves and upside-down copies.
Two events match if they are in the same star-sector and their centres differ by at most MATCH_D days (fixed before any result was read).
Usage: python compare_monocbp.py <mono results dir, real> <mono results dir, upside-down> [stage3 hash]"""
import sys, glob, pathlib
import pandas as pd
import stage3_report as R

ROOT = r"D:\second-sun\data\stage3"
MATCH_D = 0.5


def theirs(d):
    ev = pd.read_csv(pathlib.Path(d) / "transit_events.txt", sep=r"\s+")
    ev["n"] = ev.groupby(["TIC", "SECTOR"]).cumcount() + 1
    cls = pd.DataFrame(columns=["TIC", "SECTOR", "n", "cls"])
    mc = pathlib.Path(d) / "vetting_results.csv"
    if mc.exists():
        m = pd.read_csv(mc)
        parts = m.filename.str.replace(".npz", "", regex=False).str.split("_", expand=True)
        cls = pd.DataFrame(dict(TIC=parts[1].astype(int), SECTOR=parts[2].astype(int), n=parts[3].astype(int), cls=m.best_fit))
    return ev.merge(cls, on=["TIC", "SECTOR", "n"], how="left")


def near(a_tic, a_sec, a_t, b):
    """Boolean per row of a: b has an event in the same star-sector within MATCH_D days."""
    idx = b.groupby(["tic", "sector"]).center.apply(list).to_dict()
    return [any(abs(t - c) <= MATCH_D for c in idx.get((int(x), int(s)), [])) for x, s, t in zip(a_tic, a_sec, a_t)]


if __name__ == "__main__":
    real_dir, flip_dir = sys.argv[1], sys.argv[2]
    h = sys.argv[3] if len(sys.argv) > 3 else "5392f864e810"
    tr, tf = theirs(real_dir), theirs(flip_dir)
    files = list(pathlib.Path(real_dir).parent.glob("data/*.txt"))
    stars, n_sec = set(int(p.stem.split("_")[1]) for p in files), len(files)
    ev, meta = R.load(rf"{ROOT}\{h}\groups")
    ev, meta = ev[ev.primary & ev.tic.isin(stars)], meta[meta.tic.isin(stars)]
    ours = {k: ev[ev.kind == k].reset_index(drop=True) for k in ("real", "flip")}
    print(f"mono-cbp against Second Sun (frozen run {h}) on the {len(stars)} shared stars, {n_sec} star-sectors of TESS-SPOC data for mono-cbp. Aggregates only.")
    print(f"matching rule: same star-sector, centres within {MATCH_D} d. Their SNR scale differs from ours (they search down to about SNR 3, we store SNR 7 and above).")
    print("\n1. EVENTS FOUND (real curve | upside-down copy; per 100 star-sectors in brackets)")
    for lab, d in (("mono-cbp, all events", tr), ("mono-cbp, robust to detrending (DET_DEPENDENCE 0)", tr[tr.DET_DEPENDENCE == 0]),
                   ("mono-cbp, SNR >= 7 on their scale", tr[tr.SNR >= 7]), ("mono-cbp, model comparison says T or AT", tr[tr.cls.isin(["T", "AT"])])):
        f = {"mono-cbp, all events": tf, "mono-cbp, robust to detrending (DET_DEPENDENCE 0)": tf[tf.DET_DEPENDENCE == 0],
             "mono-cbp, SNR >= 7 on their scale": tf[tf.SNR >= 7], "mono-cbp, model comparison says T or AT": tf[tf.cls.isin(["T", "AT"])]}[lab]
        print(f"  {lab:52s}: {len(d):4d} ({100 * len(d) / n_sec:5.1f}) | {len(f):4d} ({100 * len(f) / n_sec:5.1f})")
    for lab, mask in (("Second Sun, all tiers", lambda x: x.tier.notna()), ("Second Sun, tier 1", lambda x: x.tier.isin(["1A", "1L", "1B"]))):
        r, f = ours["real"][mask(ours["real"])], ours["flip"][mask(ours["flip"])]
        print(f"  {lab:52s}: {len(r):4d} ({100 * len(r) / n_sec:5.1f}) | {len(f):4d} ({100 * len(f) / n_sec:5.1f})")
    print("\n2. AGREEMENT ON THE REAL CURVES")
    o = ours["real"]
    o_hit = near(o.tic, o.sector, o.center, tr.rename(columns={"TIC": "tic", "SECTOR": "sector", "TIME": "center"}))
    o_hit_rob = near(o.tic, o.sector, o.center, tr[tr.DET_DEPENDENCE == 0].rename(columns={"TIC": "tic", "SECTOR": "sector", "TIME": "center"}))
    o = o.assign(hit=o_hit, hit_rob=o_hit_rob)
    print(f"  our events also found by mono-cbp (any event)               : {int(o.hit.sum())} of {len(o)}   (tier 1: {int(o[o.tier.isin(['1A', '1L', '1B'])].hit.sum())} of {int(o.tier.isin(['1A', '1L', '1B']).sum())})")
    print(f"  our events also found by mono-cbp (robust to detrending)    : {int(o.hit_rob.sum())} of {len(o)}")
    o_f = ours["flip"]
    of_hit = near(o_f.tic, o_f.sector, o_f.center, tf.rename(columns={"TIC": "tic", "SECTOR": "sector", "TIME": "center"}))
    print(f"  our UPSIDE-DOWN events also found by mono-cbp on its upside-down curves: {sum(of_hit)} of {len(o_f)}")
    t7 = tr[tr.SNR >= 7]
    t_hit = near(t7.TIC, t7.SECTOR, t7.TIME, ours["real"])
    print(f"  mono-cbp events at SNR >= 7 (their scale) also found by us  : {sum(t_hit)} of {len(t7)}")
    tt = tr[tr.cls.isin(["T", "AT"])]
    tt_hit = near(tt.TIC, tt.SECTOR, tt.TIME, ours["real"])
    print(f"  mono-cbp transit-like events (T or AT) also found by us     : {sum(tt_hit)} of {len(tt)}")
    print("\n3. THEIR EVENTS BY MODEL-COMPARISON CLASS (real | upside-down)")
    cl = lambda d: d.cls.fillna("not vetted").value_counts()
    a, b = cl(tr), cl(tf)
    for k in sorted(set(a.index) | set(b.index)):
        print(f"  {k:12s}: {int(a.get(k, 0)):4d} | {int(b.get(k, 0)):4d}")
