"""RS-001 V-B2 (own data): does the upside-down control stay a stable null from sector to sector? For each run (G2 development 0.7.1 run, G2 sealed 0.8.0 run) and each sector: tier-1 events (1A, 1L, 1B) at SNR 7 or more,
primary product, real versus upside-down ('flip'), per 1,000 star-sectors. Then a dispersion index: chi-square of the per-sector real share around the pooled share, divided by its degrees of freedom
(1 = pure counting noise; well above 1 = the sectors differ more than chance). Aggregates only; no star IDs are printed. Usage: python v_b2_control_wobble.py"""
import os, sys, warnings
warnings.filterwarnings("ignore")
os.environ["SS_SET"] = "g2"
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import dataset as DS, stage3_core as C, stage3_report as R
T1 = ("1A", "1L", "1B")
for label, run, MIN in (("G2 development (0.7.1 run)", "dev_73f62615e365", 10), ("G2 sealed (0.8.0 run, opened after scoring)", "sealed_5f73692944aa", 50)):
    p = C.DS.RUNS / run / "groups"
    if not p.exists():
        print(label, "folder not found:", p); continue
    ev, meta = R.load(str(p))
    ok = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
    ns = ok.groupby("sector").size()
    e = ev[ev.primary & (ev.snr >= 7) & ev.tier.isin(T1)]
    real = e[e.kind == "real"].groupby("sector").size().reindex(ns.index, fill_value=0)
    flip = e[e.kind == "flip"].groupby("sector").size().reindex(ns.index, fill_value=0)
    d = pd.DataFrame({"star_sectors": ns, "real": real, "flip": flip})
    d = d[d.star_sectors >= MIN]                                # sectors with a usable number of star-sectors (10 for the smaller development slice, 50 for the sealed run)
    d["flip_per_1000"] = 1000 * d.flip / d.star_sectors
    d["real_per_1000"] = 1000 * d.real / d.star_sectors
    n = d.real + d.flip; share = d.real.sum() / n.sum()
    ok_rows = n > 0
    chi2 = (((d.real - n * share) ** 2) / (n * share * (1 - share)))[ok_rows].sum(); df = int(ok_rows.sum()) - 1
    # same for the control rate against star-sectors (Poisson dispersion of flips per star-sector)
    lam = d.flip.sum() / d.star_sectors.sum(); chi2f = (((d.flip - d.star_sectors * lam) ** 2) / (d.star_sectors * lam)).sum(); dff = len(d) - 1
    print(f"\n{label}: {len(d)} sectors with enough star-sectors, {int(d.star_sectors.sum())} star-sectors, tier-1 SNR 7+ events: real {int(d.real.sum())}, upside-down {int(d.flip.sum())}")
    print(f"  pooled real share of tier-1 events {share:.3f}; dispersion index of the real share {chi2 / df:.2f} (chi2 {chi2:.1f}, df {df})")
    print(f"  upside-down tier-1 per 1,000 star-sectors: pooled {1000 * lam:.2f}; per-sector min {d.flip_per_1000.min():.1f}, median {d.flip_per_1000.median():.1f}, max {d.flip_per_1000.max():.1f}; dispersion index {chi2f / dff:.2f} (chi2 {chi2f:.1f}, df {dff})")
    print("  sector | star-sectors | real | upside-down | upside-down per 1,000")
    for s, r in d.iterrows():
        print(f"  {int(s):4d} | {int(r.star_sectors):5d} | {int(r.real):3d} | {int(r.flip):3d} | {r.flip_per_1000:5.1f}")
