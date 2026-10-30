"""Vesper study C6 (FIX-QUEUE 30), offline on the frozen runs: the orbit-locked flag. An event is LOCKED if a partner event of the SAME kind on the same star, in a different sector, lies within
0.5 x the longer box + 0.1 d (the chain's own match window) of a whole number of the star's catalogue binary periods. A planet's transits are not locked to the binary's clock; a leftover eclipse is.
Applied to real and upside-down alike. Three partner pools (VARIANTS): A any primary event (FIX-QUEUE wording, run first), B tier-1 events only, C tier-1 events with matched box length and depth.
Reports (aggregates only): tier-1 real and upside-down before and after; stars involved; and the cost on injected planet-shaped dips (paired rows): the share of tier-1 fakes whose injection time sits at a whole
number of periods from a partner of the same star in another sector (chance coincidence), by binary period.
Usage: python c6_orbit_lock.py   (writes research\\stage3\\c6-orbit-lock.txt)"""
import os
import numpy as np, pandas as pd

SETS = {"g1": ("fd788be04650", "../data/chain_recovery/rows_v7.pkl"), "g2": ("dev_73f62615e365", "../data/chain_recovery_g2/rows_g2dev.pkl")}
T1 = ["1A", "1L", "1B"]
# partner pools (A was run first; its cost on injected dips decided that B and C were needed, so the choice among them is made on G2 DEVELOPMENT data and confirmed on G1; the sealed slice stays untouched)
VARIANTS = {"A any primary event as partner": (None, False), "B tier-1 events only as partners": (T1, False), "C tier-1 partners with matched box length (x1.6) and depth (x2)": (T1, True)}


def match(d1, p1, d2, p2):
    return 1 / 1.6 <= d1 / d2 <= 1.6 and 0.5 <= p1 / p2 <= 2.0


def locked_pair(c1, d1, c2, d2, P):
    r = abs(c1 - c2) / P
    return round(r) >= 1 and abs(r - round(r)) * P <= 0.5 * max(d1, d2) / 24 + 0.1


def run(name):
    os.environ["SS_SET"] = name
    import dataset as DS; import importlib; importlib.reload(DS)
    import stage3_core as C, stage3_report as R
    importlib.reload(C); importlib.reload(R)
    eph = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths())
    ev, meta = R.load(str(C.DS.RUNS / SETS[name][0] / "groups"))
    E = ev[ev.primary].reset_index(drop=True)
    rows = pd.read_pickle(SETS[name][1]); rows = rows[rows["error"].isna()] if "error" in rows else rows
    rows = rows[rows.K.isin((8., 10., 12., 14.)) & (rows.sign == 1) & rows.tc.notna() & rows.tier1.astype(bool)].reset_index(drop=True)
    per = {int(t): [P for _, P, _ in eph.by.get(int(t), [])] for t in set(E.tic) | set(rows.tic)}
    rows["P"] = [min(per[int(t)]) if per[int(t)] else np.nan for t in rows.tic]
    out = [f"{C.DS.NAME} run {SETS[name][0]}:"]
    for vname, (pool, matched) in VARIANTS.items():
        E["locked"] = False
        for (tic, kind), g in E.groupby(["tic", "kind"]):
            periods = per[int(tic)]
            if not periods or len(g) < 2:
                continue
            idx, c, d, s, dp, tr = g.index.values, g.center.values, g.dur_h.values, g.sector.values, g.depth_ppm.values, g.tier.values
            for a in range(len(g)):
                for b in range(a + 1, len(g)):
                    if s[a] == s[b] or (pool is not None and not (tr[a] in pool and tr[b] in pool)) or (matched and not match(d[a], dp[a], d[b], dp[b])):
                        continue
                    if any(locked_pair(c[a], d[a], c[b], d[b], P) for P in periods):
                        E.loc[idx[a], "locked"] = True; E.loc[idx[b], "locked"] = True
        out.append(f"  variant {vname}:")
        for kind, lab in (("real", "real"), ("flip", "upside-down")):
            t = E[(E.kind == kind) & E.tier.isin(T1)]
            out.append(f"   {lab:11s} tier-1: {len(t)} before, {len(t) - int(t.locked.sum())} after ({int(t.locked.sum())} locked, on {t[t.locked].tic.nunique()} stars; tier-1 events sit on {t.tic.nunique()} stars)")
        t = E[(E.kind == "real") & E.tier.isin(T1)]
        out.append("   real tier-1 by SNR bar, before-after: " + " / ".join(f"{b}: {int((t.snr >= b).sum())}-{int(((t.snr >= b) & ~t.locked).sum())}" for b in (7, 8, 10, 12)))
        t = E[(E.kind == "flip") & E.tier.isin(T1)]
        out.append("   upside-down tier-1 by SNR bar, before-after: " + " / ".join(f"{b}: {int((t.snr >= b).sum())}-{int(((t.snr >= b) & ~t.locked).sum())}" for b in (7, 8, 10, 12)))
        real = E[(E.kind == "real") & (E.tier.isin(pool) if pool else True)]; by = {t: g for t, g in real.groupby("tic")}
        hit = []
        for r in rows.itertuples():
            g = by.get(int(r.tic)); periods = per[int(r.tic)]
            hit.append(bool(g is not None and periods and any(locked_pair(r.tc, r.dur, c, d, P) and (not matched or match(r.dur, r.depth_ppm, d, dp))
                                                              for c, d, dp, s_ in zip(g.center.values, g.dur_h.values, g.depth_ppm.values, g.sector.values) if s_ != r.sector for P in periods)))
        rr = rows.assign(hit=hit)
        out.append(f"   cost: injected dips that were tier-1 {len(rr)}; flagged locked by chance {int(rr.hit.sum())} = {100 * rr.hit.mean():.2f}%")
        for lo, hi in ((0, 5), (5, 10), (10, 20), (20, 1e9)):
            g = rr[(rr.P >= lo) & (rr.P < hi)]
            if len(g):
                out.append(f"      binary period {lo} to {hi if hi < 1e8 else 'over'} d: {len(g)} fakes, {100 * g.hit.mean():.2f}% flagged by chance")
    return out


if __name__ == "__main__":
    txt = []
    for n in SETS:
        txt += run(n)
    print("\n".join(txt)); open("../research/stage3/c6-orbit-lock.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")
