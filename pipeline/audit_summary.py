"""Summarise an audit CSV: red-noise factor beta per star-sector (measured 6.5 h noise / Stassun et al. 2018 white-noise
prediction for that Tmag) and whether the injected dip came back when it should have. Usage: python audit_summary.py <audit.csv>"""
import sys, csv
import numpy as np
import pandas as pd
c = [3.29685004771, 0.850021465753, -0.285041632435, 0.0395908321369, -0.0022308015894, 4.73508403525e-5]
sig1h = lambda T: np.exp(sum(ci * T**i for i, ci in enumerate(c)))       # ppm in 1 h (tessgi/ticgen form)
a = pd.read_csv(sys.argv[1]).drop_duplicates(["tic", "sector", "product"])
tm = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").drop_duplicates("tic")[["tic", "tmag"]]
a = a.merge(tm, on="tic")
a["beta"] = a["noise_6.5h_ppm"] / (sig1h(a.tmag) / np.sqrt(6.5))
a["inj_expected"] = 3000 / a["noise_6.5h_ppm"] * 0.9 >= 7          # 8 h dip in a 6.5 h-noise frame, ~10% margin
cols = ["tic", "tmag", "sector", "product", "column", "windows", "noise_6.5h_ppm", "beta", "rmin7_rearth",
        "inj_expected", "inj_found", "inj_snr", "flipped_events"]
print(a[cols].round(2).to_string(index=False))
sp = a[a["product"] == "SPOC"]
print(f"\nSPOC star-sectors: {len(sp)}; beta median {sp.beta.median():.2f} (quartiles {sp.beta.quantile(.25):.2f}-{sp.beta.quantile(.75):.2f})")
print("per star median beta:", sp.groupby("tic").beta.median().round(2).to_dict())
mis = a[a.inj_expected & ~a.inj_found.astype(bool)]
print("injected dip missed where it should have been found:", len(mis), mis[["tic", "sector", "product"]].values.tolist())
print("flipped events per star-sector:", round(a.flipped_events.mean(), 2))
