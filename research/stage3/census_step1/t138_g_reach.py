"""T138 (6 Nov 2026): Horizon reach WITH the geometric transit chance g of R0 Amendment 4 (committed de2e951 before this script was run).
g(P_b, P_p) = min(1, (P_b / P_p)^(2/3) / f), f = R_sum / R_A in {1.5, 1.8, 2.2}; coplanar planet, circular orbits; no radius, mass or eclipse width enters g.
For every scenario of Amendment 1 (main F=5.6, F=3, F=6.9, dilution 0.5) and every set (G1, G2 development, G2 sealed, G3):
 mean cell sum without g, with g (rule A = all cells of the Armstrong region R>6 Earth radii and P<300 d, rule B = cells reachable for at least half the stars), E at Kepler's central 10%,
then the combined E, chance of finding none and 95% ceiling for three hunts (G2 dev, G2 sealed, G3) and four (plus G1). Aggregates only; no star IDs, no events.
G1 was searched with an older Vesper than 0.8, so its recovery table is an approximation (UNCERTAIN, probably generous), as in g1_reach.py."""
import sys, time
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import horizon_reach as H
R = "D:/second-sun"
tabs = H.recovery_tables(); RC, PC = H.RAD_C, H.PER_C
ri = [i for i, r in enumerate(RC) if r > 6]; pi = [j for j, p in enumerate(PC) if p < 300]
SCEN = [("main", 5.6, 1.0), ("floor3", 3.0, 1.0), ("floor6.9", 6.9, 1.0), ("dilute0.5", 5.6, 0.5)]
FS = (1.5, 1.8, 2.2)
RATE = 0.10

def g1_inputs():
    tg = pd.read_csv(f"{R}/targets/g1_targets.csv", comment="#").drop_duplicates("tic")
    star = pd.DataFrame(dict(tic=tg.tic.values, rad=tg.tic_radius_rsun.values, pbin=tg.p_bin_d.values)).set_index("tic")
    med = float(star.rad[star.rad > 0].median()); star["rad"] = star.rad.where(star.rad > 0, med)
    b = pd.read_csv(f"{R}/research/audit-2026-10-23/best_per_star_sector.csv"); b = b[b.tic.isin(star.index)][["tic", "sector", "product"]]
    au = pd.read_csv(f"{R}/research/audit-2026-10-23/audit_all.csv")
    au = au[(au.status == "ok") & (au["noise_6.5h_ppm"] > 0) & (au["noise_15h_ppm"] > 0)].copy()
    a = np.log(au["noise_15h_ppm"] / au["noise_6.5h_ppm"]) / np.log(15 / 6.5)
    au["noise8"] = au["noise_6.5h_ppm"] * (8 / 6.5) ** a
    au["covered_d"] = au.n_searched * au.cadence_min / 1440.0
    au = au.sort_values("covered_d", ascending=False).drop_duplicates(["tic", "sector"])[["tic", "sector", "noise8", "covered_d"]]
    ss = b.merge(au, on=["tic", "sector"], how="inner"); ss["fam"] = ss["product"].isin(H.FAMILY)
    return star, ss[["tic", "sector", "fam", "noise8", "covered_d"]]

def inputs(sset):
    if sset == "g1": return g1_inputs()
    star, ss, nv, med = H.sector_table(sset); return star, ss

def gmat(pbin, f): return np.minimum(1.0, (np.asarray(pbin, float)[:, None] / np.asarray(PC, float)[None, :]) ** (2.0 / 3.0) / f)

SETS = ["g1", "g2dev", "g2sealed", "g3"]
cache = {s: inputs(s) for s in SETS}
for s in SETS: print(f"{s}: {len(cache[s][0])} stars, {len(cache[s][1])} star-sectors, median binary period {cache[s][0].pbin.median():.1f} d", flush=True)
for name, fl, dl in SCEN:
    t0 = time.time(); E = {}   # E[(set, f, rule)] with g ; E0[(set, rule)] without g
    E0 = {}; perstar = {}
    print(f"\n=== scenario {name}: stability floor F = {fl}, dilution = {dl} ===", flush=True)
    for s in SETS:
        star, ss = cache[s]; store = {}
        S0, NS = H.reach(star, ss, tabs, fl, dl, store=store)
        n = len(star)
        cells = {"A": [(i, j) for i in ri for j in pi], "B": [(i, j) for i in ri for j in pi if NS[i, j] >= 0.5 * n]}
        for rule, cs in cells.items(): E0[(s, rule)] = RATE * np.mean([S0[i, j] for i, j in cs])
        for f in FS:
            G = gmat(star.pbin.values, f); Sg = np.zeros_like(S0)
            for k, tic in enumerate(star.index):
                if tic in store: Sg += np.nan_to_num(store[tic], nan=0.0) * G[k][None, :]
            for rule, cs in cells.items():
                m = np.mean([Sg[i, j] for i, j in cs]); E[(s, f, rule)] = RATE * m; perstar[(s, f, rule)] = m / n
        gm = {f: float(np.mean([gmat(star.pbin.values, f)[:, j].mean() for j in (3, 4)])) for f in FS}
        print(f"  {s}: mean g at P 77 and 139 d: " + ", ".join(f"f {f}: {gm[f]:.3f}" for f in FS) + f"; E no geometry A {E0[(s,'A')]:.2f}, B {E0[(s,'B')]:.2f}", flush=True)
    for f in FS:
        for rule in "AB":
            row = " | ".join(f"{s} {E[(s,f,rule)]:.2f}" for s in SETS)
            e3 = sum(E[(s, f, rule)] for s in SETS if s != "g1"); e4 = e3 + E[("g1", f, rule)]
            print(f"  f {f}, rule {rule}: E with g: {row} | three hunts {e3:.2f} (none {100*np.exp(-e3):.0f}%, ceiling {100*0.3/e3:.1f}%) | four hunts {e4:.2f} (none {100*np.exp(-e4):.0f}%, ceiling {100*0.3/e4:.1f}%)", flush=True)
    e30 = {rule: sum(E0[(s, rule)] for s in SETS if s != "g1") for rule in "AB"}; e40 = {rule: e30[rule] + E0[("g1", rule)] for rule in "AB"}
    print(f"  NO GEOMETRY (old, too generous): three hunts E rule A {e30['A']:.1f}, B {e30['B']:.1f}; four hunts A {e40['A']:.1f}, B {e40['B']:.1f}", flush=True)
    if name == "main":
        print("  per-star mean sum in G2 sealed (for Census sizing, stars needed = 3 / (rate x per-star sum)):", ", ".join(f"f {f} rule {r}: {perstar[('g2sealed', f, r)]:.4f}" for f in FS for r in "AB"), flush=True)
    print(f"  ({time.time()-t0:.0f} s)", flush=True)
