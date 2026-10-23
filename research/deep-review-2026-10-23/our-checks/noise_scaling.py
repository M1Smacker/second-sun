"""Own check (not the review's code): how does the expected yield scale if G1 noise is like Kepler-16 (beta ~2.8)
instead of TOI-1338 (beta ~1.4)? For each known-planet type, the share of G1 stars (real Tmag) where one transit
reaches SNR 7, at each beta. Noise model: Stassun et al. 2018 polynomial for 1-hour TESS noise (as in tessgi/ticgen)."""
import numpy as np, pandas as pd
c = [3.29685004771, 0.850021465753, -0.285041632435, 0.0395908321369, -0.0022308015894, 4.73508403525e-5]
sig1h = lambda T: np.exp(sum(ci * T**i for i, ci in enumerate(c)))  # ppm
tm = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").drop_duplicates("tic").tmag.values
# type: (mean depth %, duration range d) from Davies et al. 2026 Table 2 as quoted; review's base contribution at beta 1.4
types = {"K16": (1.80, (.31, .43), 0.18), "K34": (0.28, (.16, .47), 0.096), "K35": (0.40, (.18, .49), 0.059),
         "K64": (0.11, (.45, .51), 0.055), "K453": (0.50, (.29, .57), 0.18)}
def frac(dep, dur, beta, rscale=1.0):
    D = np.mean(dur) * 24 * rscale
    snr = dep / 100 / rscale**2 * 1e6 / (beta * sig1h(tm) / np.sqrt(D))
    return (snr >= 7).mean()
base = sum(v[2] for v in types.values())
print(f"review's base (beta 1.4): lambda_raw = {base:.2f}")
for beta in (1.0, 1.4, 2.0, 2.8):
    lam = sum(cb * frac(dep, dur, beta) / frac(dep, dur, 1.4) for dep, dur, cb in types.values())
    row = " ".join(f"{k} {frac(v[0], v[1], beta):.2f}" for k, v in types.items())
    after = lam * 0.7 - 0.5 * 0.7 * types["K16"][2] * frac(*types["K16"][:2], beta) / frac(*types["K16"][:2], 1.4)
    print(f"beta {beta}: detectable share [{row}] -> lambda_raw {lam:.2f}, after vetting x0.7 and halving K16 "
          f"{after:.2f} -> P(>=1) {100*(1-np.exp(-after)):.0f}%")
print("G1 Tmag quartiles:", np.percentile(tm, [25, 50, 75]).round(2))
