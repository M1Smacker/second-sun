"""RS-001 V-B4 (own data): planet to binary period ratio for the known transiting circumbinary planets that sit in our own tables.
Inputs: data/xmatch/cbp.csv (planet periods), binary periods from data/xmatch/ebs.csv (Prsa+ 2022, column Per) and from targets/g1_targets.csv (p_bin_d). Counts and ratios only. Usage: python v_b4_period_ratios.py"""
import pandas as pd, re
R = r"D:\second-sun"
cbp = pd.read_csv(R + r"\data\xmatch\cbp.csv")
cbp["tic"] = cbp.tic_id.map(lambda s: int(re.sub(r"\D", "", str(s))) if isinstance(s, str) and re.search(r"\d", s) else None)
ebs = pd.read_csv(R + r"\data\xmatch\ebs.csv", usecols=["TIC", "Per"]).drop_duplicates("TIC").set_index("TIC").Per
g1 = pd.read_csv(R + r"\targets\g1_targets.csv", comment="#").drop_duplicates("tic").set_index("tic").p_bin_d
rows = []
for _, r in cbp.dropna(subset=["tic", "pl_orbper"]).iterrows():
    t = int(r.tic); pb = ebs.get(t, g1.get(t))
    if pb == pb and pb is not None:
        rows.append((r.pl_name, t, r.pl_orbper, pb, r.pl_orbper / pb, "ebs" if t in ebs.index else "g1"))
d = pd.DataFrame(rows, columns=["planet", "tic", "P_planet_d", "P_binary_d", "ratio", "binary_period_from"]).sort_values("ratio")
pd.set_option("display.width", 200); print(d.to_string(index=False))
print(f"\nn = {len(d)} known planets with both periods in our tables; ratio min {d.ratio.min():.2f}, median {d.ratio.median():.2f}, max {d.ratio.max():.2f}; transiting-sized (P_planet under 1000 d): {int((d.P_planet_d < 1000).sum())}")
