"""T138 groundwork (night of 4 Nov 2026), EXPLORATORY and report-only: Horizon does not amend R0 here.
Adds the transit geometry for an exactly coplanar planet around an ECLIPSING binary of known eclipse width, from the sky-overlap condition of
Martin and Triaud 2015 (arXiv:1501.03631, Eq. 26: coplanar transitability P = R/(a_p - a_A) for a randomly oriented binary).
For a binary known to eclipse, with impact parameter b (in units of R_sum, from the eclipse width as in Oddo et al. 2026 Eq. 7 and 8), cos(i) = b R_sum / a_b, and the coplanar
planet transits star A iff cos(i) (a_p - a_A) < R_A, i.e. b < R_A a_b / (R_sum (a_p - a_A)). (My step from their Eq. 26; LIKELY, not independently checked.)
Inputs per star: binary period, primary eclipse width, TIC radius R_A (set median where missing), R_sum = f R_A (f = 1.5, 1.8, 2.2), a_A = a_b / 2 (equal masses), total mass 2 Msun for both orbits (as Horizon R0).
Then S_g(cell) = sum over stars of g_star(P_cell) x (Horizon chance of tier-1 detection given a transit), and E = rate x mean over the cells of a rule. Aggregates only."""
import sys; sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import horizon_reach as H
R = "D:/second-sun"
tabs = H.recovery_tables()
RC, PC = H.RAD_C, H.PER_C
ebs = pd.read_csv(f"{R}/data/xmatch/ebs.csv").drop_duplicates("TIC").set_index("TIC")
def durations(sset, star):
    if sset == "g3":
        t = pd.read_csv(f"{R}/targets/g3_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
        return t.dur_pri_h.reindex(star.index)
    t = pd.read_csv(f"{R}/targets/g2_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
    w = ebs["Wp-pf"].reindex(star.index) * ebs["Per"].reindex(star.index) * 24.0
    return w
def a_rsun(P):  # total mass 2 Msun, as Horizon R0
    return 215.03 * (2.0 * (np.asarray(P, float) / 365.25) ** 2) ** (1 / 3)
def g_matrix(star, dur_h, fsum):
    """per star x period-cell 0/1: does a coplanar planet transit star A given the binary eclipses with this width?"""
    P = star.pbin.values; ab = a_rsun(P); Rs = star.rad.values; Rsum = fsum * Rs
    x = np.pi * ab * (dur_h.values / 24.0) / (P * Rsum)           # = sqrt(1-b^2)
    b = np.sqrt(np.clip(1 - np.clip(x, 0, 1) ** 2, 0, 1))
    b = np.where(np.isfinite(b), b, np.nanmedian(b))               # missing width: set median
    G = np.zeros((len(star), len(PC)))
    for j, Pp in enumerate(PC):
        ap = a_rsun(Pp); aA = 0.5 * ab
        bmax = Rs * ab / (Rsum * (ap - aA))
        G[:, j] = (b < bmax).astype(float)
    return G, b
res = {}
for sset in ("g2sealed", "g2dev", "g3"):
    star, ss, nvalid, med = H.sector_table(sset)
    store = {}
    S0, NS = H.reach(star, ss, tabs, 5.6, 1.0, store=store)
    dur = durations(sset, star)
    print(f"{sset}: {len(star)} stars; eclipse width known for {int(dur.notna().sum())}; median width {dur.median():.1f} h; median binary period {star.pbin.median():.1f} d", flush=True)
    res[sset] = (star, store, S0, NS, dur)
ri = [i for i, r in enumerate(RC) if r > 6]; pi = [j for j, p in enumerate(PC) if p < 300]; small = [i for i, r in enumerate(RC) if 6 < r < 10]
def cells(rule, NS, n):
    if rule == "A": return [(i, j) for i in ri for j in pi]
    if rule == "B": return [(i, j) for i in ri for j in pi if NS[i, j] >= 0.5 * n]
    return [(i, j) for i in small for j in (3, 4)]
for fsum in (1.5, 1.8, 2.2):
    print(f"\n=== R_sum = {fsum} x R_A ===")
    tot = {r: 0.0 for r in "ABC"}
    for sset, (star, store, S0, NS, dur) in res.items():
        G, b = g_matrix(star, dur, fsum)
        Sg = np.zeros_like(S0)
        for k, tic in enumerate(star.index):
            if tic in store:
                a = np.nan_to_num(store[tic], nan=0.0)
                Sg += a * G[k][None, :]
        gm = [float(G[:, j].mean()) for j in range(len(PC))]
        print(f"{sset}: mean g by period cell P = {', '.join(f'{p:.0f}:{g:.2f}' for p, g in zip(PC, gm))}")
        for rule in "ABC":
            cs = cells(rule, NS, len(star))
            m0 = np.mean([S0[i, j] for i, j in cs]); mg = np.mean([Sg[i, j] for i, j in cs])
            tot[rule] += 0.10 * mg
            print(f"   rule {rule}: mean sum without g {m0:.1f}, with g {mg:.1f} (effective g {mg/m0:.2f}); E at 10% = {0.1*mg:.2f}")
    print("COMBINED three hunts, central 10%: " + "; ".join(f"rule {r}: E = {tot[r]:.2f}, chance of none {100*np.exp(-tot[r]):.1f}%, 95% ceiling on total rate {100*3*0.10/tot[r]:.1f}%" for r in "ABC"))
