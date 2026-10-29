"""Vesper study, phase C: the PAIRED comparison (VESPER-STUDY-PLAN.md section 3 amendment). Re-injects EXACTLY the injections of a baseline chain_recovery run (same star-sector, time, duration, depth, sign)
through the chain with the current VESPER_OPTS switches, and compares outcomes injection by injection.
  python paired_recovery.py run <baseline rows.pkl> <label> [procs] [max_groups]   (SS_SET and SS_RUN as for chain_recovery.py; writes data\\<PREP>\\paired_<label>.pkl)
  python paired_recovery.py compare <baseline rows.pkl> <label>                   (writes research\\stage3\\paired-<label>-<set>.txt; aggregates only)
Only K 8, 10, 12, 14 are re-injected (the range the pass rule uses), both signs (dip and mirror bump)."""
import os, sys, glob, multiprocessing as mp
import numpy as np, pandas as pd
from scipy.stats import binomtest
import chain_recovery as X, stage3_core as C, vopts as V

KEEP_K = (8.0, 10.0, 12.0, 14.0)
T1 = ("1A", "1L", "1B")
FEAT = os.environ.get("PAIRED_FEATURES") == "1"      # C4: also keep the continuous numbers of the found event; injects dips only (sign 1)
FEAT_COLS = ["dur_h", "depth_ppm", "lift_pre", "lift_post", "cover_pre", "cover_post", "ramp_d", "ecl_d", "ecl_w", "c8_n", "burst_n", "common_n", "repeat_n", "ph_d", "second_product", "pdc_snr", "sap_burst_n"]


def row_feat(ev, kind, tc, dur, **meta):
    row = X.row_of(ev, kind, tc, dur, **meta)
    if row["found_primary"]:
        near = ev[(ev.kind == kind) & ev.primary & (np.abs(ev.center - tc) <= 0.5 * np.maximum(dur, ev.dur_h) / 24 + 0.1)]
        r = near.sort_values("snr", ascending=False).iloc[0]
        row.update({("ev_" + c): r.get(c) for c in FEAT_COLS})
    return row


def job(args):
    tic, sec, inj = args
    try:
        paths, best, base, prods = X.baseline(tic, sec)
        out = []
        for r in inj:
            if FEAT and r["sign"] != 1:
                continue
            X.INJ.update(tc=r["tc"], dur_h=r["dur"], depth_ppm=r["depth_ppm"], sign=r["sign"])
            evs, _ = X.chain(tic, sec, paths, best)
            row = (row_feat if FEAT else X.row_of)(X.merged(evs, tic, sec, best), "real" if r["sign"] == 1 else "flip", r["tc"], r["dur"], tic=tic, sector=sec, K=r["K"], sign=r["sign"], depth_ppm=r["depth_ppm"])
            out.append(row)
        X.INJ.clear()
        return out
    except Exception as e:
        return [dict(tic=tic, sector=sec, error=f"{type(e).__name__}: {str(e)[:100]}")]


def load_base(path):
    b = pd.read_pickle(path)
    b = b[b["error"].isna()] if "error" in b else b
    b = b[b.K.isin(KEEP_K) & b.sign.notna() & b.tc.notna()].copy()
    return b


def run(base_path, label, procs, maxg):
    b = load_base(base_path)
    groups = [(int(t), int(s), g[["tc", "dur", "K", "sign", "depth_ppm"]].to_dict("records")) for (t, s), g in b.groupby(["tic", "sector"])]
    if maxg:
        groups = groups[:maxg]
    X.PREP.mkdir(parents=True, exist_ok=True); X.TMP.mkdir(parents=True, exist_ok=True)
    raw = X.PREP / f"raw_{X.RUN.name}.pkl"
    if not raw.exists():
        X.build_raw(raw)
    print(f"options {sorted(V.ON)}; {len(groups)} star-sectors, {sum(len(g[2]) for g in groups)} injections", flush=True)
    rows = []
    with mp.Pool(procs, initializer=X.init, initargs=(str(raw),)) as pool:
        for i, r in enumerate(pool.imap_unordered(job, groups), 1):
            rows += r
            if i % 25 == 0:
                print(f"{i}/{len(groups)}", flush=True)
    pd.DataFrame(rows).to_pickle(X.PREP / f"paired_{label}.pkl")
    print("PAIRED DONE", len(rows), flush=True)


def compare(base_path, label):
    b = load_base(base_path); b["t1_base"] = b.tier.isin(T1)
    o = pd.read_pickle(X.PREP / f"paired_{label}.pkl")
    o = o[o["error"].isna()] if "error" in o else o
    o["t1_opt"] = o.tier.isin(T1)
    m = b.merge(o[["tic", "sector", "dur", "K", "sign", "t1_opt", "tier"]], on=["tic", "sector", "dur", "K", "sign"], suffixes=("", "_opt"))
    txt = [f"Paired comparison, set {C.DS.NAME}, options {label} against baseline 0.7.1 ({len(m)} matched injections of {len(b)}; {m.groupby(['tic', 'sector']).ngroups} star-sectors; K 8 to 14)."]
    txt.append("box h | sign | n | base tier1 | option tier1 | gained | lost | exact p (two-sided)")
    verdict = {}
    for (dur, sign), g in m.groupby(["dur", "sign"]):
        gain, lost = int((g.t1_opt & ~g.t1_base).sum()), int((~g.t1_opt & g.t1_base).sum())
        p = binomtest(gain, gain + lost, 0.5).pvalue if gain + lost else 1.0
        verdict[(dur, sign)] = (gain, lost, p)
        txt.append(f"{dur:5.0f} | {'dip' if sign == 1 else 'bump'} | {len(g):4d} | {100 * g.t1_base.mean():4.1f}% | {100 * g.t1_opt.mean():4.1f}% | {gain:4d} | {lost:4d} | {p:.4f}")
    d = m[m.sign == 1]
    for name, sel in (("8 h box", d.dur == 8.0), ("14 and 20 h boxes", d.dur >= 14.0), ("4 h box", d.dur == 4.0)):
        g = d[sel]; gain, lost = int((g.t1_opt & ~g.t1_base).sum()), int((~g.t1_opt & g.t1_base).sum())
        p = binomtest(gain, gain + lost, 0.5).pvalue if gain + lost else 1.0
        txt.append(f"DIPS, {name}: gained {gain}, lost {lost}, exact p {p:.5f}, net {gain - lost:+d} ({100 * (gain - lost) / max(len(g), 1):+.1f} points of recovery)")
    dp, bp = m[m.sign == 1].t1_opt.mean(), m[m.sign == -1].t1_opt.mean()
    dpb, bpb = m[m.sign == 1].t1_base.mean(), m[m.sign == -1].t1_base.mean()
    txt.append(f"Mirror test, all boxes: baseline dip {100 * dpb:.1f}% vs bump {100 * bpb:.1f}% (gap {100 * (bpb - dpb):+.1f}); option dip {100 * dp:.1f}% vs bump {100 * bp:.1f}% (gap {100 * (bp - dp):+.1f}); rule: gap within 3 points")
    (C.ROOT / "research" / "stage3" / f"paired-{label}-{C.DS.NAME}.txt").write_text("\n".join(txt), encoding="utf-8")
    print("\n".join(txt))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "run":
        run(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 6, int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    else:
        compare(sys.argv[2], sys.argv[3])
