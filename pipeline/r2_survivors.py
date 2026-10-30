"""Vesper study R2: what are the upside-down tier-1 survivors (the false alarms the nine flags let through)? Upside-down events only, aggregates only; no real event is read.
Questions: (1) is their SNR shape a white-noise tail? (2) how many sit just inside a flag threshold (a soft edge a better cleaning could move) against deep inside the clean zone? (3) what share of ALL upside-down events does each flag block, by SNR?
Near-miss zones (a factor 2 from the frozen thresholds, chosen before looking): step lift 0.25 to 0.5 of the depth, side cover 0.5 to 0.75, ramp distance 1 to 2 d, eclipse-phase distance 0.35 to 0.7 d, repeat count 2, common-moment count 2.
Usage: python r2_survivors.py   (writes research\\stage3\\r2-survivors.txt)"""
import os
import numpy as np, pandas as pd
from scipy.stats import norm

SETS = {"g1": "fd788be04650", "g2": "dev_73f62615e365"}
T1 = ["1A", "1L", "1B"]
FLAGS = ["gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated", "common"]


def run(name):
    os.environ["SS_SET"] = name
    import dataset as DS; import importlib; importlib.reload(DS)
    import stage3_core as C, stage3_report as R
    importlib.reload(C); importlib.reload(R)
    ev, meta = R.load(str(C.DS.RUNS / SETS[name] / "groups"))
    ss = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]); n = len(ss)
    F = ev[ev.primary & (ev.kind == "flip") & (ev.snr >= 7)].copy(); S = F[F.tier.isin(T1)].copy()
    out = [f"{C.DS.NAME} run {SETS[name]}: {n} star-sectors; upside-down primary events at SNR 7 or more: {len(F)} (all tiers), tier-1 survivors {len(S)}"]
    bins = [(7, 8), (8, 10), (10, 12), (12, 1e9)]
    out.append("   SNR band | all upside-down | survivors | survivor share | white-noise expectation for the whole set")
    # white noise: about (27 d / 10 min bins ~ 3900) x 9 box lengths trials per star-sector, a one-sided tail (order of magnitude only)
    trials = 3900 * 9
    for lo, hi in bins:
        a = int(((F.snr >= lo) & (F.snr < hi)).sum()); s = int(((S.snr >= lo) & (S.snr < hi)).sum())
        exp = n * trials * (norm.sf(lo) - (norm.sf(hi) if hi < 1e8 else 0))
        out.append(f"   {lo:>3} to {'up' if hi > 1e8 else int(hi):>2} | {a:5d} | {s:3d} | {100 * s / max(a, 1):4.1f}% | {exp:.2g}")
    g = lambda c: pd.to_numeric(S[c], errors="coerce")
    lift = np.maximum(g("lift_pre").abs().fillna(0), g("lift_post").abs().fillna(0)); cover = np.minimum(g("cover_pre").fillna(1), g("cover_post").fillna(1))
    near = pd.DataFrame({"step lift 0.25 to 0.5": (lift >= 0.25) & (lift < 0.5), "side cover 0.5 to 0.75": (cover >= 0.5) & (cover < 0.75),
                         "ramp distance 1 to 2 d": (g("ramp_d") >= 1.0) & (g("ramp_d") < 2.0), "eclipse phase 0.35 to 0.7 d": (g("ph_d") >= 0.35) & (g("ph_d") < 0.7),
                         "repeat count 2": g("repeat_n") == 2, "common count 2": g("common_n") == 2})
    out.append("   survivors just inside a flag threshold (one survivor can be near several): " + ", ".join(f"{c} {int(near[c].sum())}" for c in near.columns))
    anyn = near.any(axis=1)
    out.append(f"   survivors near at least one threshold {int(anyn.sum())} of {len(S)}; deep inside the clean zone {int((~anyn).sum())}; near at SNR 10 or more {int((anyn & (S.snr >= 10)).sum())} of {int((S.snr >= 10).sum())}")
    out.append("   share of ALL upside-down events (SNR 7 or more) that each flag blocks, and the same at SNR 10 or more: " +
               ", ".join(f"{f} {100 * F[f].astype(bool).mean():.0f}% / {100 * F[F.snr >= 10][f].astype(bool).mean():.0f}%" for f in FLAGS))
    out.append(f"   survivors by box length h: " + ", ".join(f"{int(d) if d == int(d) else d} h: {int((S.dur_h == d).sum())}" for d in sorted(S.dur_h.unique())) +
               "; all upside-down by box length: " + ", ".join(f"{int(d) if d == int(d) else d} h: {int((F.dur_h == d).sum())}" for d in sorted(F.dur_h.unique())))
    return out


if __name__ == "__main__":
    txt = []
    for s in SETS:
        txt += run(s)
    print("\n".join(txt)); open("../research/stage3/r2-survivors.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")
