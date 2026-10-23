"""D3: how far could catalogue period errors smear each G1 star's eclipses across the TESS baseline (~1,950 d)?
eclipse_mask_auto folds all TESS sectors at the catalogue period, so drift = (1950 / P) * dP."""
import glob, csv, numpy as np, pandas as pd
f = glob.glob(r"D:\second-sun\data\wave-1\villanova_kepler-ebs_live\*.csv")[0]
rows = [l for l in open(f) if l.strip() and not l.startswith("#")]
v = pd.DataFrame([r for r in csv.reader(rows)]).iloc[:, :3]
v.columns = ["kic", "p", "ep"]
v = v.astype(float)
tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#")
m = tg.merge(v, left_on=["kic"], right_on=["kic"])
m = m[np.isclose(m.p, m.p_bin_d, rtol=1e-5)]
m["drift_1s_h"] = 1950 / m.p * m.ep * 24
m["drift_3s_h"] = 3 * m.drift_1s_h
print("matched rows:", len(m))
for h in (0.5, 1, 2, 5):
    print(f"  rows with 3-sigma drift > {h} h: {(m.drift_3s_h > h).sum()}")
print(m.sort_values("drift_3s_h", ascending=False)[["kic", "tic", "tmag", "p_bin_d", "ep", "drift_3s_h"]].head(12).round(4).to_string(index=False))
print("Kepler-16 row:", m[m.kic == 12644769][["p_bin_d", "ep", "drift_3s_h"]].round(4).values.tolist())
