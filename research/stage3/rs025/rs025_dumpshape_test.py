"""RS-025 Q1 price of each holding flag cleared alone (diagnostic, not a fix; copy of the RS-024 option test with the rule swapped).
RS-024 option test (Claude, 14 Nov 2026). Planet-level P, the paired dip-against-bump control and the untouched-light background,
under four 'dominated' rules written down BEFORE this ran (DOMINATED-RESEARCH-2026-11-14.md, test plan):
  O0  frozen rule recomputed (identity check: must give the 006 two-key recount, 531 dips / 486 bumps 'new')
  OE  opposite sign, whole light curve, but rivals labelled eclipse or repeat (c5, ecl_overlap, orbit_lock, p1_veto, repeater) do not count
  OA  either sign, within 6.85 d, outside the candidate's own 1.5 durations (Kepler Chases exclusion), margin zero
  OAE OA and OE together
Same trials, matching and tiering as research/stage3/006-check/p_recount.py (its bench, frame and matching are copied, the frozen code is
imported read-only). Only the 'dominated' flag of the candidate rows is recomputed; tiers are recomputed with stage3_core.tier_of.
Known limit: orbit_lock partners are judged on the stored tiers (second order). Counts only to research/stage3/rs024/options.json;
trial rows to data/rs024/options-trials.csv.
Usage (from pipeline/): python -B ../research/stage3/rs024/rs024_options.py [--limit N]"""
import argparse, json, math, os, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "006-check"))
import p_recount as PR                      # sets SS_SET, VESPER_OPTS=c6,p1, NUMBA threads and the pipeline path
import numpy as np, pandas as pd

OPTS = ("base", "dump_shape")
CLEAR = {"base": (), "no_step": ("step",), "no_gap": ("gap_dump",), "no_ramp": ("ramp",), "no_three": ("step", "gap_dump", "ramp")}
WIN_D = 6.85
EXPL = ("c5", "ecl_overlap", "orbit_lock", "p1_veto", "repeater")
LAB = {0: "5-10", 1: "10-14", 2: "14-20", 3: "20-27.4", 4: "27.4+"}


def truthy(v):
    try:
        return bool(v) and v == v
    except Exception:
        return False


def prep(df):
    """Arrays per light curve (tic, sector, product) for fast rival look-ups."""
    df = df.copy()
    df["_expl"] = np.zeros(len(df), bool)
    for c in EXPL:
        if c in df:
            df["_expl"] |= df[c].map(truthy).values
    groups = {k: (g.index.values, g.kind.values, g.snr.fillna(0).values.astype(float), g.center.values.astype(float), g._expl.values)
              for k, g in df.groupby(["tic", "sector", "product"])}
    return df, groups


def dominated(row, idx, groups, opt):
    ix, kind, snr, t, ex = groups[(row.tic, row.sector, row["product"])]
    s = row.snr
    if s is None or s != s:
        return False
    if opt in ("O0", "OE"):
        m = kind != row.kind
    else:
        dt = np.abs(t - row.center)
        m = (ix != idx) & (dt <= WIN_D) & (dt >= 1.5 * float(row.dur_h or 0) / 24)
    if opt in ("OE", "OAE"):
        m = m & ~ex
    return bool(m.any() and snr[m].max() >= s)


def tier_under(df, groups, idx, opt, C):
    d = df.loc[idx].to_dict()
    fl = str(d.get("flags") or "")
    if opt == "dump_shape":                     # dump zone holds only an uneven baseline (largest side lift > 0.25 of the depth, or unmeasured)
        lp, lq = d.get("lift_pre"), d.get("lift_post")
        uneven = any(l is None or l != l or abs(l) > 0.25 for l in (lp, lq))
        d["gap_dump"] = ("gap edge" in fl) or ("momentum dump" in fl and uneven)
    elif opt == "dump_only":                    # the gap-edge half switched off
        d["gap_dump"] = "momentum dump" in fl
    return C.tier_of(d)


def hits(df, groups, star, arm, obs, opt, C):
    """Matched candidate rows near any crossing, re-tiered under opt; returns set of crossing indices hit at tier 1."""
    if df is None or df.empty:
        return set()
    cand = df[(df.tic == star) & (df.kind == arm) & df.primary & (df.snr >= 7)]
    out = set()
    for k, (c, d) in enumerate(obs):
        for idx in cand.index[(cand.center - c).abs() <= d / 2]:
            if tier_under(df, groups, idx, opt, C) in PR.T1:
                out.add(k); break
    return out


def main(limit=None):
    import stage3_core as C, stage3_report as R
    rows, bg = [], defaultdict(int)
    for camp in ("g2", "g3"):
        os.environ["SS_SET"] = camp
        import importlib, dataset as DS
        importlib.reload(DS); importlib.reload(C)
        best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
        tg = pd.read_csv(PR.ROOT / "targets" / "r1_targets.csv", comment="#")
        tg = tg[(tg["list"] == camp) & (tg.design_seen == 1)].drop_duplicates("tic")
        Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
        src = PR.ROOT / "data" / f"stage3_{camp}" / "r1dev_{}_seen_bcd29c7aabb0".format(camp)
        base = defaultdict(list)
        for kind in ("groups", "groups_sap"):
            for p in (src / kind).glob("*.json"):
                tic, sec = map(int, p.stem.split("_"))
                if tic in Pb:
                    base[tic, sec].extend(json.loads(p.read_text(encoding="utf-8"))["events"])
        base = {k: PR.bench(v, Pb.get(k[0], math.nan), C) for k, v in base.items()}
        cams = {k: {e["camera"] for e in v} for k, v in base.items()}

        def frame(evs):
            if not evs:
                return pd.DataFrame(columns=["tic", "sector", "kind", "primary", "tier", "snr", "center", "product", "dur_h"])
            df = pd.DataFrame(evs).merge(best, on=["tic", "sector"], how="left")
            df["primary"] = df["product"] == df["best"]
            df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
            return R.apply_v7(R.merge_sap(df.reset_index(drop=True)))

        # background: untouched design light, primary SNR 7+ events at tier 1, per option, kind and binary-period bin
        if not limit:
            allb, ag = prep(frame([e for v in base.values() for e in v]))
            pb = tg.set_index("tic").p_bin_d
            for idx in allb.index[allb.primary & (allb.snr >= 7)]:
                r = allb.loc[idx]
                b = int(np.digitize(pb.get(r.tic, np.nan), [10, 14, 20, 27.4]))
                for opt in OPTS:
                    if tier_under(allb, ag, idx, opt, C) in PR.T1:
                        bg[opt, r.kind, b] += 1
            print(camp, "background done", flush=True)

        n = 0
        for j in sorted(PR.OUT6.glob(f"planet-*-*-*-{camp}/results.jsonl")):
            for line in j.read_text(encoding="utf-8").splitlines():
                if limit and n >= limit:
                    break
                n += 1
                r = json.loads(line); star = r["star"]; obs = r["observed"]
                rec = dict(campaign=camp, trial=r["trial"], star=star, bin=r["bin"], n_cross=len(obs))
                if obs:
                    secs = set(r["changed"])
                    neigh = [e for (t, s), v in base.items() if s in secs and (t == star or cams.get((t, s), set()) & cams.get((star, s), set())) and not (t == star and s in secs) for e in v]
                    neigh += [e for (t, s), v in base.items() if t == star and s not in secs for e in v]
                    tdir = j.parent / f"trial-{r['trial']}"
                    before, bgp = prep(frame([e for (t, s), v in base.items() if (t == star and s in secs) or (s in secs and cams.get((t, s), set()) & cams.get((star, s), set())) for e in v]))
                    for sign, arm in ((1, "real"), (-1, "flip")):
                        ev = []
                        for s in secs:
                            for kind in ("groups", "groups_sap"):
                                p = tdir / str(sign) / kind / f"{star}_{s}.json"
                                if p.exists():
                                    ev.extend(json.loads(p.read_text(encoding="utf-8"))["events"])
                        own, og = prep(frame(neigh + PR.bench(ev, Pb.get(star, math.nan), C))) if ev else (None, None)
                        for opt in OPTS:
                            h = hits(own, og, star, arm, obs, opt, C) if own is not None else set()
                            pre = hits(before, bgp, star, arm, obs, opt, C)
                            rec[f"{opt}_{arm}_all"] = bool(h)
                            rec[f"{opt}_{arm}_new"] = bool(h - pre)
                rows.append(rec)
            if limit and n >= limit:
                break
        print(camp, "trials done", flush=True)
    df = pd.DataFrame(rows)
    seen = df[df.n_cross > 0].copy()
    rng = np.random.default_rng(20261114)
    out = dict(trials=len(df), with_crossing=len(seen))
    for opt in OPTS:
        o = {}
        for arm in ("real", "flip"):
            col = f"{opt}_{arm}_new"
            o[f"{arm}_new"] = int(seen[col].sum())
            o[f"{arm}_all"] = int(seen[f"{opt}_{arm}_all"].sum())
            o[f"P_{arm}_equal_weight"] = round(float(seen.groupby("bin")[col].mean().mean()), 4)
        pc = {}
        for b, g in seen.groupby("bin"):
            stars = g.star.unique(); by = {s: g[g.star == s] for s in stars}
            diffs = []
            for _ in range(2000):
                sub = pd.concat([by[s] for s in rng.choice(stars, len(stars))])
                diffs.append(sub[f"{opt}_real_new"].mean() - sub[f"{opt}_flip_new"].mean())
            lo, hi = np.percentile(diffs, [0.5, 99.5])
            pc[LAB[int(b)]] = dict(n=len(g), dip=int(g[f"{opt}_real_new"].sum()), bump=int(g[f"{opt}_flip_new"].sum()), diff_99=[round(float(lo) * 100, 2), round(float(hi) * 100, 2)],
                                   passes=bool(lo <= 0 <= hi))
        o["paired_control"] = pc
        o["paired_control_passes_all_bins"] = all(v["passes"] for v in pc.values())
        if bg:
            o["background_tier1"] = {k: sum(v for (op, kk, b), v in bg.items() if op == opt and kk == k) for k in ("real", "flip")}
            o["background_tier1_by_bin"] = {LAB[b]: {k: bg.get((opt, k, b), 0) for k in ("real", "flip")} for b in range(5)}
        out[opt] = o
    tag = f"-prefix{limit}" if limit else ""
    (Path(__file__).parent / f"../rs025/dump-shape{tag}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    df.to_csv(PR.ROOT / "data" / "rs024" / f"rs025-dump-shape-trials{tag}.csv", index=False)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); main(a.parse_args().limit)
