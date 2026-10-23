"""Eclipse-phase check (rule C5) for Stage 2 survivors, LOCAL use: how far is each event from the star's own primary eclipse
and from phase 0.5 (a circular secondary)? Prints no star IDs or times. Usage: python stage2_phase.py"""
import pandas as pd

D = r"D:\second-sun\data\stage2"
s = pd.read_csv(D + r"\survivors_LOCAL.csv"); R = pd.read_csv(D + r"\events_real_LOCAL.csv")
c = R[(R.stratum == "control") & ~R.gap_dump & ~R.burst & ~R.flipmatch]
tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#")


def phase_info(r):
    out = []
    for q in tg[tg.tic == r.tic].itertuples():
        t0 = q.bjd0 - 57000.0                                   # Villanova BJD-2400000 -> BTJD
        ph = ((r.center - t0) / q.p_bin_d) % 1.0
        out.append(f"P={q.p_bin_d:.2f}d: {min(ph, 1 - ph) * q.p_bin_d:.2f} d from primary, {abs(ph - 0.5) * q.p_bin_d:.2f} d from phase 0.5")
    return " | ".join(out)


for name, X in (("SURVIVORS", s), ("CONTROL survivors", c)):
    print(name)
    for i, r in X.reset_index(drop=True).iterrows():
        print(f"  #{i} sector {r.sector} {r['product']} SNR {r.snr:.1f} {r.dur_h} h:", phase_info(r))
