"""Independent recount of brief 006's planet-level P (Claude, 14 Nov 2026), for the two-key check of Codex's result under
research/stage3/G1-PLANET-BAR.md. Written without importing Codex's scorer (006_planet_score.py): own repeater rule b, FIX 91 by
plain distance (no rounding-boundary recovery), own window matching, own star-cluster bootstrap. Reads Codex's injected group files
and journals under data/astra/006 and the design-seen development events; design-seen stars only (the trials are); writes counts
only to research/stage3/006-check/. Frozen pipeline code is imported read-only (stage3_core.tier_of, stage3_report.merge_sap/apply_v7).
P = share of reference planets with at least one observed crossing for which a primary event at tier 1A/1L/1B, SNR 7 or more, lies
within half a duration of an observed crossing (the T156 matching rule), on the real arm; the same on the upside-down arm is the control.
Two counts: 'all' and 'new' (excluding a crossing where the un-injected baseline already had a tier-1 event of that arm in the window).
Usage (from pipeline/): python -B ../research/stage3/006-check/p_recount.py [--limit N]   (N = only the first N journal rows, for a smoke test)"""
import argparse, json, math, os, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1", NUMBA_NUM_THREADS="2")
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd

ROOT = Path(r"D:\second-sun"); OUT6 = ROOT / "data" / "astra" / "006"; HERE = ROOT / "research" / "stage3" / "006-check"
T1 = {"1A", "1L", "1B"}; FLIP_D = 0.3


def binary_members(ev, P):
    if not (P == P) or P <= 0:
        return set(range(len(ev))) if len(ev) >= 3 else set()
    def lock(a, b):
        s = abs(a["center"] - b["center"]); c = round(s / P)
        return c >= 1 and abs(s - c * P) <= 1 / 24
    m = set()
    for tr in combinations(range(len(ev)), 3):
        if all(lock(ev[a], ev[b]) for a, b in combinations(tr, 2)):
            m.update(tr)
    return m


def bench(events, P, C):
    """Repeater rule b on both arms; FIX 91: an upside-down event is flipmatched if a real event of the same product is within FLIP_D."""
    parts = defaultdict(list)
    for e in events:
        parts[e["kind"], e["product"]].append(e)
    out = {}
    for (kind, prod), g in parts.items():
        mem = binary_members(g, P)
        reals = [r["center"] for r in parts.get(("real", prod), [])]
        for i, e in enumerate(g):
            u = dict(e); u["repeater"] = i in mem
            if kind == "flip":
                u["flipmatch"] = any(abs(e["center"] - c) < FLIP_D for c in reals)
            ti = dict(u); ti.pop("pdc_snr", None); u["tier"] = C.tier_of(ti)
            out[id(e)] = u
    return [out[id(e)] for e in events]


def main(limit=None):
    import stage3_core as C, stage3_report as R
    rows = []
    for camp in ("g2", "g3"):
        os.environ["SS_SET"] = camp
        import importlib, dataset as DS
        importlib.reload(DS); importlib.reload(C)
        best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
        tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
        tg = tg[(tg["list"] == camp) & (tg.design_seen == 1)].drop_duplicates("tic")
        Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
        src = ROOT / "data" / f"stage3_{camp}" / "r1dev_{}_seen_bcd29c7aabb0".format(camp)
        base = defaultdict(list)
        for kind in ("groups", "groups_sap"):
            for p in (src / kind).glob("*.json"):
                tic, sec = map(int, p.stem.split("_"))
                if tic in Pb:
                    base[tic, sec].extend(json.loads(p.read_text(encoding="utf-8"))["events"])
        base = {k: bench(v, Pb.get(k[0], math.nan), C) for k, v in base.items()}
        cams = {k: {e["camera"] for e in v} for k, v in base.items()}

        def frame(evs):
            if not evs:
                return pd.DataFrame(columns=["tic", "sector", "kind", "primary", "tier", "snr", "center"])
            df = pd.DataFrame(evs).merge(best, on=["tic", "sector"], how="left")
            df["primary"] = df["product"] == df["best"]
            df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
            return R.apply_v7(R.merge_sap(df.reset_index(drop=True)))

        journals = sorted(OUT6.glob(f"planet-*-*-*-{camp}/results.jsonl"))
        n = 0
        for j in journals:
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
                    before = frame([e for (t, s), v in base.items() if (t == star and s in secs) or (s in secs and cams.get((t, s), set()) & cams.get((star, s), set())) for e in v])
                    for sign, arm in ((1, "real"), (-1, "flip")):
                        ev = []
                        for s in secs:
                            for kind in ("groups", "groups_sap"):
                                p = tdir / str(sign) / kind / f"{star}_{s}.json"
                                if p.exists():
                                    ev.extend(json.loads(p.read_text(encoding="utf-8"))["events"])
                        own = frame(neigh + bench(ev, Pb.get(star, math.nan), C)) if ev else None
                        hit_all = hit_new = False
                        for c, d in obs:
                            pre = before[(before.tic == star) & (before.kind == arm) & before.primary & before.tier.isin(T1) & (before.snr >= 7) & ((before.center - c).abs() <= d / 2)]
                            if own is None:
                                continue
                            m = own[(own.tic == star) & (own.kind == arm) & own.primary & own.tier.isin(T1) & (own.snr >= 7) & ((own.center - c).abs() <= d / 2)]
                            if len(m):
                                hit_all = True
                                hit_new |= pre.empty
                        rec[f"{arm}_all"], rec[f"{arm}_new"] = hit_all, hit_new
                rows.append(rec)
    df = pd.DataFrame(rows)
    seen = df[df.n_cross > 0]
    rng = np.random.default_rng(20261114)
    stars = seen.star.unique(); by = {s: seen[seen.star == s] for s in stars}
    out = dict(trials=len(df), with_crossing=len(seen), never_transit=int((df.n_cross == 0).sum()))
    for col in ("real_all", "real_new", "flip_all", "flip_new"):
        k = int(seen[col].sum()); p = k / len(seen)
        boots = []
        for _ in range(4000):
            pick = rng.choice(stars, len(stars))
            sub = pd.concat([by[s] for s in pick])
            boots.append(sub[col].mean())
        out[col] = dict(k=k, P=round(p, 4), lo=round(float(np.percentile(boots, 2.5)), 4), hi=round(float(np.percentile(boots, 97.5)), 4))
    out["by_bin"] = {int(b): dict(n=len(g), real_all=round(g.real_all.mean(), 3), flip_all=round(g.flip_all.mean(), 3)) for b, g in seen.groupby("bin")}
    HERE.mkdir(parents=True, exist_ok=True)
    tag = f"-prefix{limit}" if limit else ""
    (HERE / f"p-recount{tag}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    df.to_csv(Path(r"D:\second-sun\data\astra") / f"claude-p-recount{tag}.csv", index=False)     # trial rows (star ids) stay under data\
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); main(a.parse_args().limit)
