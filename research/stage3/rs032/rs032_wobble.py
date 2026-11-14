"""RS-032 wobble study (Claude, 14 Nov 2026). Method in WOBBLE-STUDY-2026-11-14.md, written before running.
Measures centroid wobble J inside boxes: DS-freed background events (real A, upside-down F) and planted bench crossings in the
dump zone (Pl2 all, Pl in DS-gained trials). Guard threshold from G2 Pl2 only; scored on G3. Writes rows to data/rs032."""
import json, math, os, re, sys, importlib
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rs031"))
import numpy as np, pandas as pd
from astropy.io import fits
from scipy.stats import mannwhitneyu
import rs031_dsp_bench as D          # dumps, tier_under for B / BDS (imports harness + known events)
O, PR = D.O, D.O.PR
ROOT = PR.ROOT
OUT = ROOT / "data" / "rs032"; OUT.mkdir(exist_ok=True)
DUMPS, DUMP_D, PRE_D = D.DUMPS, D.DUMP_D, D.PRE_DUMP_D


def in_zone(sec, c):
    v = DUMPS.get(int(sec))
    return v is not None and v.size > 0 and bool((((v - c) > -DUMP_D) & ((v - c) < PRE_D)).any())


def prod_of(name):
    return "QLP" if "qlp" in name else ("TESS-SPOC" if "tess-spoc" in name else "SPOC")


FILES = {}


def file_for(camp, tic, sec, prod):
    prod = str(prod).replace("-SAP", "")              # SAP-flux events live in the same file
    key = (camp, tic, sec, prod)
    if key not in FILES:
        FILES[key] = None
        for p in (ROOT / "data" / camp / str(tic)).glob("*lc.fits"):
            if "fast" in p.name:
                continue
            m = re.search(r"(?:^|[-_])s(\d{4})(?=[-_])", p.name)   # fixed: "tess2019..." no longer read as sector 2019
            if m and int(m.group(1)) == sec and prod_of(p.name) == prod:
                FILES[key] = p; break
    return FILES[key]


CEN = {}


def centroid(p):
    if p not in CEN:
        with fits.open(p, memmap=False) as h:
            d = h[1].data; names = h[1].columns.names
            t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"], int)
            cx, cy = ("MOM_CENTR1", "MOM_CENTR2") if "MOM_CENTR1" in names else ("SAP_X", "SAP_Y")
            x = np.asarray(d[cx], float); y = np.asarray(d[cy], float)
        ok = (q == 0) & np.isfinite(t) & np.isfinite(x) & np.isfinite(y)
        CEN[p] = (t[ok], x[ok], y[ok])
    return CEN[p]


def rs(a):
    return 1.4826 * np.median(np.abs(a - np.median(a))) if a.size >= 3 else np.nan


def scat(t, x, y, m):
    i = np.flatnonzero(m)
    if i.size < 4:
        return np.nan
    i = i[:-1][np.diff(i) == 1]                      # consecutive good cadences only
    return math.hypot(rs(x[i + 1] - x[i]), rs(y[i + 1] - y[i]))


def wobble(p, sec, c, dur_d):
    t, x, y = centroid(p)
    if t.size < 50:
        return np.nan, np.nan
    v = DUMPS.get(int(sec), np.array([]))
    far = np.ones(t.size, bool)
    for dv in v:
        far &= np.abs(t - dv) > 1.0
    sref = scat(t, x, y, far)
    h = max(dur_d, 2 / 24) / 2
    box = np.abs(t - c) <= h
    sb = scat(t, x, y, box)
    ring = (np.abs(t - c) > h) & (np.abs(t - c) <= h + 0.5)
    if not (sref and sref == sref) or box.sum() < 3 or ring.sum() < 3:
        return sb / sref if sref else np.nan, np.nan
    dr = math.hypot(np.median(x[box]) - np.median(x[ring]), np.median(y[box]) - np.median(y[ring]))
    return sb / sref, dr / sref


def main():
    import stage3_core as C, stage3_report as R
    rows = []
    trials = pd.read_csv(ROOT / "data" / "rs031" / "dsp-trials.csv")
    gained = {(r.campaign, int(r.trial)) for r in trials.itertuples() if r.BDS_real_new and not r.B_real_new}
    for camp in ("g2", "g3"):
        os.environ["SS_SET"] = camp
        import dataset as DSm
        importlib.reload(DSm); importlib.reload(C)
        best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
        bestd = {(int(a), int(b)): c for a, b, c in best.itertuples(index=False)}
        tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
        tg = tg[(tg["list"] == camp) & (tg.design_seen == 1)].drop_duplicates("tic")
        Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
        src = ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0"
        base = defaultdict(list)
        for kind in ("groups", "groups_sap"):
            for p in (src / kind).glob("*.json"):
                tic, sec = map(int, p.stem.split("_"))
                if tic in Pb:
                    base[tic, sec].extend(json.loads(p.read_text(encoding="utf-8"))["events"])
        base = {k: PR.bench(v, Pb.get(k[0], math.nan), C) for k, v in base.items()}
        df = pd.DataFrame([e for v in base.values() for e in v]).merge(best, on=["tic", "sector"], how="left")
        df["primary"] = df["product"] == df["best"]
        df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
        allb, ag = O.prep(R.apply_v7(R.merge_sap(df.reset_index(drop=True))))
        nfree = 0
        for idx in allb.index[allb.primary & (allb.snr >= 7)]:
            if D.tier_under(allb, ag, idx, "BDS", C) in PR.T1 and D.tier_under(allb, ag, idx, "B", C) not in PR.T1:
                r = allb.loc[idx]; nfree += 1
                p = file_for(camp, int(r.tic), int(r.sector), r["product"])
                dd = float(r.dur_h or 0) / 24
                J, Dr = wobble(p, r.sector, float(r.center), dd) if p else (np.nan, np.nan)
                rows.append(dict(campaign=camp, group="A" if r.kind == "real" else "F", tic=int(r.tic), sector=int(r.sector),
                                 product=r["product"], center=float(r.center), dur_d=dd, in_zone=in_zone(r.sector, float(r.center)), J=J, drift=Dr))
        print(camp, "freed events", nfree, flush=True)
        nc = 0
        for j in sorted(PR.OUT6.glob(f"planet-*-*-*-{camp}/results.jsonl")):
            for line in j.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                for c, dd in r["observed"]:
                    for s in r["changed"]:
                        if not in_zone(s, c):
                            continue
                        prod = bestd.get((r["star"], s))
                        p = file_for(camp, r["star"], s, prod) if prod else None
                        if p is None:
                            continue
                        t, _, _ = centroid(p)
                        if not t.size or not (t[0] - 0.1 <= c <= t[-1] + 0.1):
                            continue
                        J, Dr = wobble(p, s, c, dd)
                        nc += 1
                        rows.append(dict(campaign=camp, group="Pl2", tic=r["star"], sector=s, product=prod, center=c, dur_d=dd,
                                         in_zone=True, J=J, drift=Dr, trial=r["trial"], ds_gained=(camp, r["trial"]) in gained))
        print(camp, "planted crossings in dump zone", nc, flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "wobble-rows.csv", index=False)
    res = {}
    g2p = out[(out.campaign == "g2") & (out.group == "Pl2")].J.dropna()
    Jt = float(np.percentile(g2p, 90)); res["Jt_g2_pl2_p90"] = round(Jt, 3)
    for camp in ("g2", "g3"):
        o = out[out.campaign == camp]
        A, F = o[o.group == "A"], o[o.group == "F"]
        P2 = o[o.group == "Pl2"]; P1 = P2[P2.ds_gained == True]
        d = {}
        for nm, g in (("A", A), ("A_in_zone", A[A.in_zone]), ("F", F), ("Pl2", P2), ("Pl", P1)):
            j = g.J.dropna()
            d[nm] = dict(n=len(g), n_J=len(j), J_median=round(float(j.median()), 3) if len(j) else None,
                         J_p75=round(float(j.quantile(.75)), 3) if len(j) else None,
                         held=int((j > Jt).sum()), drift_median=round(float(g.drift.dropna().median()), 3) if g.drift.notna().any() else None)
        a, b = A.J.dropna(), P2.J.dropna()
        d["mannwhitney_A_gt_Pl2_p"] = float(mannwhitneyu(a, b, alternative="greater").pvalue) if len(a) and len(b) else None
        d["by_product_A"] = A.groupby("product").J.median().round(3).to_dict()
        d["by_product_Pl2"] = P2.groupby("product").J.median().round(3).to_dict()
        res[camp] = d
    g3 = res["g3"]
    res["pass"] = bool(res["g2"]["mannwhitney_A_gt_Pl2_p"] is not None and res["g2"]["mannwhitney_A_gt_Pl2_p"] < 0.01
                       and g3["A"]["n_J"] and g3["A"]["held"] >= 0.5 * g3["A"]["n_J"]
                       and g3["Pl2"]["n_J"] and (g3["Pl2"]["n_J"] - g3["Pl2"]["held"]) >= 0.8 * g3["Pl2"]["n_J"])
    (HERE / "wobble.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
