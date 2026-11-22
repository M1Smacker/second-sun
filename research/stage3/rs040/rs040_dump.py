"""RS-040 S0 (Claude, 22 Nov 2026): dump per-event features for a one-score test, from the 006 planet bench (same loop as
research/stage3/006-check/p_recount.py, frozen code imported read-only). Writes rows with star ids under data/rs040/ only.
planted.csv: every primary event of the planted arm (real and upside-down) at SNR 7+ within half a duration of an observed crossing,
  any tier, with features; 'pre' = the un-injected light already had a tier-1 event of that arm there (crossing not new).
background.csv: every primary event of the un-injected design-seen light at SNR 7+, both arms, with features and tier.
Usage (from pipeline/): python -B ../research/stage3/rs040/rs040_dump.py [--limit N]"""
import argparse, json, math, os, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "006-check"))
import p_recount as PR
import pandas as pd

OUT = Path(r"D:\second-sun\data\rs040"); OUT.mkdir(parents=True, exist_ok=True)
KEEP = ["tic", "sector", "kind", "product", "center", "dur_h", "snr", "depth_ppm", "lift_pre", "lift_post", "cover_pre", "cover_post",
        "ramp_d", "ph_d", "c8_best", "c8_n", "burst_n", "repeat_n", "gap_dump", "flipmatch", "burst", "common", "c5", "ecl_overlap",
        "repeater", "orbit_lock", "step", "ramp", "dominated", "p1_veto", "pdc_snr", "tier", "flags"]


def pick(df):
    return df[[c for c in KEEP if c in df.columns]]


def main(limit=None):
    import stage3_core as C, stage3_report as R
    planted, background = [], []
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
            df = pd.DataFrame(evs).merge(best, on=["tic", "sector"], how="left")
            df["primary"] = df["product"] == df["best"]
            df["c8_best"] = pd.to_numeric(df["c8_best"], errors="coerce")
            return R.apply_v7(R.merge_sap(df.reset_index(drop=True)))

        allbg = frame([e for v in base.values() for e in v])
        bg = allbg[allbg.primary & (allbg.snr >= 7)]
        b = pick(bg).copy(); b["campaign"] = camp; b["bin"] = b.tic.map(dict(zip(tg.tic.astype(int), tg.get("p_bin", pd.Series(dtype=float)))))
        background.append(b)
        n = 0
        for j in sorted(PR.OUT6.glob(f"planet-*-*-*-{camp}/results.jsonl")):
            for line in j.read_text(encoding="utf-8").splitlines():
                if limit and n >= limit:
                    break
                n += 1
                r = json.loads(line); star = r["star"]; obs = r["observed"]
                if not obs:
                    continue
                secs = set(r["changed"])
                neigh = [e for (t, s), v in base.items() if s in secs and (t == star or cams.get((t, s), set()) & cams.get((star, s), set())) and not (t == star and s in secs) for e in v]
                neigh += [e for (t, s), v in base.items() if t == star and s not in secs for e in v]
                tdir = j.parent / f"trial-{r['trial']}"
                bev = [e for (t, s), v in base.items() if (t == star and s in secs) or (s in secs and cams.get((t, s), set()) & cams.get((star, s), set())) for e in v]
                before = frame(bev) if bev else None
                for sign, arm in ((1, "real"), (-1, "flip")):
                    ev = []
                    for s in secs:
                        for kind in ("groups", "groups_sap"):
                            p = tdir / str(sign) / kind / f"{star}_{s}.json"
                            if p.exists():
                                ev.extend(json.loads(p.read_text(encoding="utf-8"))["events"])
                    if not ev:
                        continue
                    own = frame(neigh + PR.bench(ev, Pb.get(star, math.nan), C))
                    for ci, (c, d) in enumerate(obs):
                        pre = False
                        if before is not None:
                            pre = bool(len(before[(before.tic == star) & (before.kind == arm) & before.primary & before.tier.isin(PR.T1) & (before.snr >= 7) & ((before.center - c).abs() <= d / 2)]))
                        m = own[(own.tic == star) & (own.kind == arm) & own.primary & (own.snr >= 7) & ((own.center - c).abs() <= d / 2)]
                        for _, e in pick(m).iterrows():
                            planted.append(dict(e, campaign=camp, trial=r["trial"], star=star, bin=r["bin"], arm=arm, crossing=ci, pre=pre))
        print(camp, "trials read", n, flush=True)
    pd.DataFrame(planted).to_csv(OUT / f"planted{'-' + str(limit) if limit else ''}.csv", index=False)
    pd.concat(background).to_csv(OUT / f"background{'-' + str(limit) if limit else ''}.csv", index=False)
    print("planted rows", len(planted), "background rows", sum(len(b) for b in background))


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); main(a.parse_args().limit)
