"""P-01b (Fable audit): counts only, no star names. In the stored G2 sealed, G2 dev (latest) and G3 runs, count events per arm (real / upside-down)
by binary period bin and SNR bin, for all events and for first-tier events (tier field as stored in groups/*.json).
If the eclipse mask cuts strong dips in slow binaries, the real arm should fall short of the upside-down arm at long period and high SNR.
Also prints the period distribution of each star list and of the known transiting circumbinary hosts.
Usage: python p01b_real_vs_flip_by_period.py"""
import json, glob, pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(r"D:\second-sun")
RUNS = {"G3": (ROOT / "data/stage3_g3/g3_e7886a71a61f", ROOT / "targets/g3_chain_targets.csv"),
        "G2 sealed": (ROOT / "data/stage3_g2/sealed_5f73692944aa", ROOT / "targets/g2_chain_targets.csv")}
PB = [0, 10, 14, 20, 27.4, 1e4]; PL = ["<10", "10-14", "14-20", "20-27", ">27"]
SB = [7, 9, 12, 20, 1e9]; SL = ["7-9", "9-12", "12-20", ">20"]

for name, (run, tgf) in RUNS.items():
    tg = pd.read_csv(tgf, comment="#").drop_duplicates("tic")
    P = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    pb = pd.cut(tg.p_bin_d, PB, labels=PL).value_counts().reindex(PL)
    print(f"\n===== {name}: {len(tg)} stars; stars per period bin: {pb.to_dict()}")
    rows = []; ngroups = 0; gper = []
    for fn in glob.glob(str(run / "groups" / "*.json")):
        g = json.load(open(fn)); ngroups += 1; gper.append(P.get(int(g["tic"]), np.nan))
        for e in g["events"]:
            rows.append((e["kind"], P.get(int(e["tic"]), np.nan), e["snr"], str(e.get("tier")), e["product"], e.get("dur_h")))
    E = pd.DataFrame(rows, columns=["kind", "P", "snr", "tier", "product", "dur"])
    gp = pd.cut(pd.Series(gper), PB, labels=PL).value_counts().reindex(PL)
    print(f"star-sector groups {ngroups}; per period bin {gp.to_dict()}; events {len(E)}")
    E["pb"] = pd.cut(E.P, PB, labels=PL); E["sb"] = pd.cut(E.snr, SB, labels=SL, right=False)
    for label, sub in (("ALL events", E), ("FIRST-TIER events (1A, 1L, 1B)", E[E.tier.isin(["1A", "1L", "1B"])])):
        print(f"-- {label}: real / upside-down per period bin (rows) and SNR bin (columns)")
        r = sub[sub.kind == "real"].groupby(["pb", "sb"], observed=False).size().unstack(fill_value=0)
        f = sub[sub.kind == "flip"].groupby(["pb", "sb"], observed=False).size().unstack(fill_value=0)
        for p in PL:
            print(f"   P {p:>6}: " + "   ".join(f"{s}: {int(r.loc[p, s])}/{int(f.loc[p, s])}" for s in SL) + f"   total {int(r.loc[p].sum())}/{int(f.loc[p].sum())}   per 1000 groups {1000*r.loc[p].sum()/max(gp[p],1):.1f}/{1000*f.loc[p].sum()/max(gp[p],1):.1f}")
        print(f"   all P: real {int((sub.kind=='real').sum())}, upside-down {int((sub.kind=='flip').sum())}")

print("\nKnown transiting circumbinary hosts, binary period (d): Kepler-16 41.1, -34 27.8, -35 20.7, -38 18.8, -47 7.4, -64 20.0, -413 10.1, -453 27.3, -1647 11.3, -1661 28.2, TOI-1338 14.6, TIC 172900988 19.7")
print("  with binary period over 18 d: 8 of 12; over 14 d: 9 of 12")
