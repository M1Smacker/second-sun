"""T138 groundwork 2 (night of 4 Nov 2026), exploratory, report only: add a small mutual inclination Delta (planet plane against binary plane) to the exactly-coplanar geometry condition of t138_geometry_probe.py.
Small-angle argument (mine, LIKELY; follows Martin and Triaud 2015 where transitability rises with mutual inclination, and Li, Holman and Tao 2016 who find systems within about 3 degrees of coplanar):
cos(i_planet) = cos(i_binary) + Delta cos(phi), phi = the node angle, taken uniform and fixed over the observation. The planet transits star A at some epoch if |cos i_p| (a_p - a_A) < R_A.
Effective bound on the binary impact parameter b (units of R_sum): b_max(Delta) = (R_A / (a_p - a_A) + 0.5 Delta_rad) * a_b / R_sum, where the factor 0.5 is a cautious average over the node angle. Aggregates only."""
import sys; sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import horizon_reach as H
R = "D:/second-sun"; RC, PC = H.RAD_C, H.PER_C
tabs = H.recovery_tables()
ebs = pd.read_csv(f"{R}/data/xmatch/ebs.csv").drop_duplicates("TIC").set_index("TIC")
def durations(sset, star):
    if sset == "g3":
        t = pd.read_csv(f"{R}/targets/g3_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic"); return t.dur_pri_h.reindex(star.index)
    return ebs["Wp-pf"].reindex(star.index) * ebs["Per"].reindex(star.index) * 24.0
def a_rsun(P): return 215.03 * (2.0 * (np.asarray(P, float) / 365.25) ** 2) ** (1 / 3)
def g_matrix(star, dur_h, fsum, delta_deg):
    P = star.pbin.values; ab = a_rsun(P); Rs = star.rad.values; Rsum = fsum * Rs
    x = np.pi * ab * (dur_h.values / 24.0) / (P * Rsum); b = np.sqrt(np.clip(1 - np.clip(x, 0, 1) ** 2, 0, 1)); b = np.where(np.isfinite(b), b, np.nanmedian(b))
    G = np.zeros((len(star), len(PC)))
    for j, Pp in enumerate(PC):
        ap = a_rsun(Pp); aA = 0.5 * ab
        bmax = (Rs / (ap - aA) + 0.5 * np.radians(delta_deg)) * ab / Rsum
        G[:, j] = (b < bmax).astype(float)
    return G
res = {}
for sset in ("g2sealed", "g2dev", "g3"):
    star, ss, nv, med = H.sector_table(sset); store = {}
    S0, NS = H.reach(star, ss, tabs, 5.6, 1.0, store=store); res[sset] = (star, store, S0, NS, durations(sset, star)); print(sset, "reach done", flush=True)
ri = [i for i, r in enumerate(RC) if r > 6]; pi = [j for j, p in enumerate(PC) if p < 300]
def cells(rule, NS, n):
    return [(i, j) for i in ri for j in pi] if rule == "A" else [(i, j) for i in ri for j in pi if NS[i, j] >= 0.5 * n]
print("\nAll three hunts at Kepler's central 10%; E = expected detections, none = chance of finding none, ceil = 95% ceiling on the total rate from our null")
for fsum in (1.5, 1.8, 2.2):
    for d in (0, 1, 2, 3):
        tot = {"A": 0.0, "B": 0.0}; gl = []
        for sset, (star, store, S0, NS, dur) in res.items():
            G = g_matrix(star, dur, fsum, d); Sg = np.zeros_like(S0)
            for k, tic in enumerate(star.index):
                if tic in store: Sg += np.nan_to_num(store[tic], nan=0.0) * G[k][None, :]
            for rule in "AB":
                cs = cells(rule, NS, len(star)); tot[rule] += 0.10 * np.mean([Sg[i, j] for i, j in cs])
            gl.append(float(np.mean([G[:, j].mean() for j in (3, 4)])))
        print(f"  R_sum {fsum}, Delta {d} deg: mean g at P 77-139 d {np.mean(gl):.2f}; rule A E={tot['A']:.2f} none={100*np.exp(-tot['A']):.0f}% ceil={100*0.3/tot['A']:.1f}% | rule B E={tot['B']:.2f} none={100*np.exp(-tot['B']):.0f}% ceil={100*0.3/tot['B']:.1f}%", flush=True)
