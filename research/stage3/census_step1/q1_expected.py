"""RS-010 Q1 (night of 4 Nov 2026): how many circumbinary planets should hunts of our size have found, if Armstrong et al. 2014 is right?
E = sum over cells (occurrence per star in the cell x Horizon sum of detection chance in the cell). Horizon main scenario (floor 5.6, no dilution), recovery tables from the G2 dev split.
Occurrence anchor (Armstrong 2014 abstract, CONFIRMED): 10.0 (+18, -6.5)% for R_p > 6 Earth radii, P_p < 300 d, coplanar. How the rate is spread over the cells is MY assumption (three rules).
Aggregates only."""
import sys; sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np
import horizon_reach as H
tabs = H.recovery_tables()
res = {}
for sset in ("g2sealed", "g2dev", "g3"):
    star, ss, nvalid, med = H.sector_table(sset)
    S, NS = H.reach(star, ss, tabs, 5.6, 1.0)
    res[sset] = (S, NS, len(star))
RC, PC = H.RAD_C, H.PER_C
ri = [i for i, r in enumerate(RC) if r > 6]            # 7, 9, 11, 13, 15
small = [i for i, r in enumerate(RC) if 6 < r < 10]    # 7, 9
pi = [j for j, p in enumerate(PC) if p < 300]          # 13..250 (bins 1-6)
print("radius bins >6:", [int(RC[i]) for i in ri], "; period bins <300 d:", [int(PC[j]) for j in pi])
def cells_A(): return [(i, j) for i in ri for j in pi]                                    # uniform over all 30 cells, even where no star is stable
def cells_B(NS, n): return [(i, j) for i in ri for j in pi if NS[i, j] >= 0.5 * n]        # only cells where at least half the stars are allowed (stable)
def cells_C(): return [(i, j) for i in small for j in (3, 4)]                             # concentrated: 6-10 Re, P 77 and 139 d
rates = {"central 10.0%": 0.100, "low 3.5%": 0.035, "high 28%": 0.280}
print()
tot = {k: {r: 0.0 for r in rates} for k in "ABC"}
for sset, (S, NS, n) in res.items():
    print(f"{sset}: {n} stars")
    for k, cells in (("A", cells_A()), ("B", cells_B(NS, n)), ("C", cells_C())):
        m = np.mean([S[i, j] for i, j in cells])
        row = []
        for rn, r in rates.items():
            E = r * m; tot[k][rn] += E; row.append(f"{rn}: E={E:.2f} (P0={100*np.exp(-E):.0f}%)")
        print(f"  rule {k} ({len(cells)} cells, mean sum {m:.1f}): " + "; ".join(row))
print("\nCOMBINED G2 dev + G2 sealed + G3 (disjoint stars; G1 has no reach map):")
for k in "ABC":
    print(f"  rule {k}: " + "; ".join(f"{rn}: E={tot[k][rn]:.2f}, chance of seeing none {100*np.exp(-tot[k][rn]):.0f}%" for rn in rates))
# Census what-if: N G2-sealed-like stars (same brightness, same coverage as the sealed bright set)
S, NS, n = res["g2sealed"]
print("\nCENSUS WHAT-IF (per 1,000 stars like the G2 sealed set; expected detections at the central rate):")
for k, cells in (("A", cells_A()), ("B", cells_B(NS, n)), ("C", cells_C())):
    m = np.mean([S[i, j] for i, j in cells]); print(f"  rule {k}: {0.1*m/n*1000:.2f} per 1,000 stars; stars needed for E=3 (95% chance to see at least one if the rate is right): {3/(0.1*m/n):,.0f}")

# ---- second part: the geometry factor g (probability that a coplanar planet transits at all; Horizon R0 sets g = 1) and what Census needs
print("\nSENSITIVITY TO g (transit geometry; Horizon uses g = 1, UNCERTAIN; for a planet at 10 binary periods g is roughly a_bin/a_planet = 0.2 to 0.3 -- my estimate, NOT looked up):")
mA = {k: np.mean([res[k][0][i, j] for i, j in cells_A()]) for k in res}
mB = {k: np.mean([res[k][0][i, j] for i, j in cells_B(res[k][1], res[k][2])]) for k in res}
SA, SB = sum(mA.values()), sum(mB.values())
print(f"sum over the three hunts of the mean cell sums: rule A {SA:.0f}, rule B {SB:.0f}")
for g in (1.0, 0.5, 0.25, 0.1):
    print(f"  g={g}: expected at central 10%: rule A E={0.1*g*SA:.2f} (none seen {100*np.exp(-0.1*g*SA):.1f}%), rule B E={0.1*g*SB:.2f} (none seen {100*np.exp(-0.1*g*SB):.1f}%); 95% ceiling on the total rate from our zero: rule A {100*3/(g*SA):.1f}%, rule B {100*3/(g*SB):.1f}%")
print("\nKEPLER CROSS-CHECK (Armstrong 2014: 1735 Kepler binaries in the initial sample, 7 known systems; 10% central rate):")
print(f"  4 to 7 detections / 10% = 40 to 70 star-equivalents of Kepler for this region (some of the 7 known planets are smaller than 6 Earth radii; which ones is from memory, UNCERTAIN; the 95% range of the rate, 3.5% to 28%, would widen it to 15 to 200). Ours by Horizon with g = 1: rule A {SA:.0f}, rule B {SB:.0f}.")
print("\nCENSUS: stars like the G2 sealed set needed to push the 95% ceiling on the total rate (R>6 Earth radii, P<300 d, coplanar) down to a target, if nothing is found:")
perstar = {"A": mA["g2sealed"] / 594, "B": mB["g2sealed"] / 594}
for g in (1.0, 0.5, 0.25):
    print("  g=%s: " % g + "; ".join(f"ceiling {int(t*100)}%: rule A {3/(t*g*perstar['A']):,.0f} stars, rule B {3/(t*g*perstar['B']):,.0f} stars" for t in (0.10, 0.05, 0.035)))
