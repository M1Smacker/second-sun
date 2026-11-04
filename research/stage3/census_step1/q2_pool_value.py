"""RS-010 Q2 (night of 4 Nov 2026): rank the candidate pools by Horizon star-equivalents per gigabyte, on catalogue-level inputs, BEFORE any download.
Reuses pipeline/horizon_reach.py (rule R0 unchanged). g (transit geometry) is not in Horizon; it multiplies every pool alike, so the RANKING does not depend on it (LIKELY).
Pools are built by re-using real star-sectors of G3 (QLP, faint) and G2 sealed (SPOC family) and changing only what the pool really changes
(brightness through a fitted noise-vs-Tmag slope, binary period, number of sectors per star). Disk cost: measured MB per star-sector on our disk.
The OCCURRENCE prior is NOT in these numbers (Hamers 2016: no known Kepler circumbinary planet below a 7 day binary), see the note. Aggregates only."""
import sys; sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import horizon_reach as H
rng = np.random.default_rng(20261104)
tabs = H.recovery_tables()
R = "D:/second-sun"
out = []
def region_sum(S, NS, n):
    """mean over the 15 'stable' cells of rule B (R>6, P<300, at least half the stars allowed): comparable single number; plus the Kepler-16-size cell."""
    cells = [(i, j) for i, r in enumerate(H.RAD_C) if r > 6 for j, p in enumerate(H.PER_C) if p < 300 and NS[i, j] >= 0.5 * n]
    return float(np.mean([S[i, j] for i, j in cells])), float(0.5 * (S[2, 3] + S[2, 4]))
def run(name, star, ss, mb_per_ss, note=""):
    S, NS = H.reach(star, ss, tabs, 5.6, 1.0)
    n = len(star)
    reg, k16 = region_sum(S, NS, n)
    nss = len(ss)
    gb = nss * mb_per_ss / 1000.0
    out.append(dict(pool=name, stars=n, star_sectors=nss, GB=gb, region=reg, k16=k16, reg_per_star=reg / n, reg_per_GB=reg / gb, k16_per_GB=k16 / gb, note=note))
    print(f"{name}: {n} stars, {nss} star-sectors, {gb:.1f} GB, region sum {reg:.1f} ({reg/n:.3f}/star, {reg/gb:.1f}/GB), K16 cell {k16:.1f}", flush=True)
# ---- bases
g3_star, g3_ss, _, _ = H.sector_table("g3")
g2_star, g2_ss, _, _ = H.sector_table("g2sealed")
tg3 = pd.read_csv(f"{R}/targets/g3_chain_targets.csv", comment="#").drop_duplicates("tic").set_index("tic").tmag
# noise-vs-Tmag slope on G3 QLP star-sectors (log10 noise8 on Tmag, per-star median)
m = g3_ss.merge(tg3.rename("tmag"), left_on="tic", right_index=True)
m = m.groupby("tic").agg(noise=("noise8", "median"), tmag=("tmag", "first")).dropna()
b, a = np.polyfit(m.tmag, np.log10(m.noise), 1)
print(f"G3 fit: log10(noise8 ppm) = {a:.2f} + {b:.3f} x Tmag over {len(m)} stars (photon-noise expectation 0.2)")
MB_G3, MB_G2 = 2200 / 4080, 14600 / 6877     # measured disk per star-sector (G3 all products 2.2 GB; G2 sealed stars 14.6 GB)
print(f"disk: G3 {MB_G3:.2f} MB per star-sector; G2 sealed {MB_G2:.2f} MB per star-sector")
# ---- reference pools as searched
run("G3 as searched (faint TTC, QLP)", g3_star, g3_ss, MB_G3)
run("G2 sealed as searched (bright, 2-min)", g2_star, g2_ss, MB_G2)
# ---- A: fainter TTC (13.5 to 15.5, median about 14.2): G3 stars made 1.25 mag fainter, scaled to 785 stars
dT = 14.2 - float(m.tmag.median())
ssF = g3_ss.copy(); ssF["noise8"] = ssF.noise8 * 10 ** (b * dT)
run(f"A. TTC fainter 13.5-15.5 (+{dT:.2f} mag), 785 stars", g3_star, ssF, MB_G3, "scaled from 612 to 785 below")
# ---- B/C/D: shorter binaries, same light as G3 (reach only; the occurrence prior is not here)
for nm, pb, N in (("B. TTC 5-7 d, 495 stars", 6.0, 495), ("C. TTC 2-5 d, 1,205 stars", 3.5, 1205), ("D. TTC under 2 d, 634 stars", 1.2, 634)):
    st = g3_star.copy(); st["pbin"] = pb
    run(nm, st, g3_ss, MB_G3, f"P_bin set to {pb} d; scaled to {N} stars below")
# ---- E: post-sector-26 two-minute bright stars of the G2 type: G2 sealed stars with only k sectors each (random draws, averaged over 4 draws)
for k in (3, 6):
    parts = []
    for d in range(4):
        keep = g2_ss.groupby("tic", group_keys=False).apply(lambda g: g.sample(min(k, len(g)), random_state=int(rng.integers(1e9))))
        S, NS = H.reach(g2_star, keep, tabs, 5.6, 1.0)
        reg, k16 = region_sum(S, NS, len(g2_star)); parts.append((reg, k16, len(keep)))
    reg, k16, nss = np.mean(parts, axis=0)
    gb = nss * MB_G2 / 1000
    out.append(dict(pool=f"E{k}. post-26 two-minute bright stars of the G2 type, {k} sectors each (594 shown)", stars=594, star_sectors=nss, GB=gb, region=reg, k16=k16, reg_per_star=reg / 594, reg_per_GB=reg / gb, k16_per_GB=k16 / gb, note="G2 sealed stars cut to k random sectors"))
    print(f"E{k}: region sum {reg:.1f} ({reg/594:.3f}/star, {reg/gb:.1f}/GB), K16 {k16:.1f}, {gb:.1f} GB", flush=True)
df = pd.DataFrame(out)
df.to_csv(r"D:\second-sun\research\stage3\census_step1\q2-pool-value.csv", index=False)
print("\nPER 1,000 STARS (region star-equivalents; GB):")
for _, r in df.iterrows():
    print(f"  {r.pool[:62]:62s} {1000*r.reg_per_star:7.1f} star-eq per 1,000 stars; {1000*r.GB/r.stars:6.1f} GB per 1,000 stars; {r.reg_per_GB:7.1f} per GB")
