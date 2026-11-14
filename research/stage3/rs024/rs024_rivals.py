"""RS-024 copy of 006-check/p_competitor.py that also writes every rival row privately to data/rs024/rivals.csv (Claude, 14 Nov 2026)."""
"""p_competitor.py (14 Nov 09:40): for every crossing held by 'dominated', which event beat it? Records the strongest opposite-arm event in the same light curve (same star, sector, product): its c5 / ecl_overlap flags and distance to the catalogue eclipse (ph_d). Based on p_flags.py. Why do planted dips beat planted bumps in the slow-binary bins? (Claude, 14 Nov 2026; Codex 006 next-work item 1, tree node 1.1/1.6).
Same trials, same matching and same tiering as p_recount.py (imported from it). For every trial with an observed crossing and for each arm
(real = planted dip on the real curve; flip = planted bump read by the upside-down arm), take the best primary SNR>=7 event within half a
duration of any observed crossing and record: found (any tier), tier 1, and the flags of the best held event. Prints per bin, per arm:
found, tier 1, and how often each flag sits on a found-but-held crossing. Counts only to research/stage3/006-check/p-flags.json.
Usage (from pipeline/): python -B ../research/stage3/006-check/p_flags.py [--limit N]"""
import argparse, json, math, os, sys
from collections import defaultdict, Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "006-check"))
import p_recount as PR                      # sets SS_SET, VESPER_OPTS, NUMBA threads and the pipeline path
import pandas as pd

FLAGS = ["gap_dump", "common", "burst", "flipmatch", "c5", "ecl_overlap", "repeater", "orbit_lock", "step", "ramp", "dominated", "too_deep", "flare", "p1_veto"]


def on(v):
    if isinstance(v, (list, tuple, set, dict)):
        return len(v) > 0
    try:
        return bool(v) and v == v
    except Exception:
        return False


def main(limit=None):
    import stage3_core as C, stage3_report as R
    RIV = []
    stat = defaultdict(lambda: dict(n=0, found=0, t1=0, held=0, flags=Counter(), only=Counter(), comp=Counter(), phd=[]))
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
                for sign, arm in ((1, "real"), (-1, "flip")):
                    st = stat[r["bin"], arm]; st["n"] += 1
                    ev = []
                    for s in secs:
                        for kind in ("groups", "groups_sap"):
                            p = tdir / str(sign) / kind / f"{star}_{s}.json"
                            if p.exists():
                                ev.extend(json.loads(p.read_text(encoding="utf-8"))["events"])
                    if not ev:
                        continue
                    own = frame(neigh + PR.bench(ev, Pb.get(star, math.nan), C))
                    mine = own[(own.tic == star) & (own.kind == arm) & own.primary & (own.snr >= 7)]
                    near = mine[mine.center.apply(lambda c: any(abs(c - x) <= d / 2 for x, d in obs))]
                    if near.empty:
                        continue
                    st["found"] += 1
                    if near.tier.isin(PR.T1).any():
                        st["t1"] += 1; continue
                    st["held"] += 1
                    e = near.sort_values("snr").iloc[-1]
                    fl = [f for f in FLAGS if f in e.index and on(e[f])]
                    if "common" in fl and "burst" in fl:
                        fl.remove("burst")
                    st["flags"].update(fl)
                    if "dominated" in fl:
                        other = "flip" if arm == "real" else "real"
                        rival = own[(own.tic == star) & (own.sector == e["sector"]) & (own["product"] == e["product"]) & (own.kind == other)]
                        if rival.empty:
                            st["comp"]["no rival found"] += 1
                        else:
                            c = rival.sort_values("snr").iloc[-1]
                            RIV.append(dict(camp=camp, bin=r['bin'], arm=arm, star=star, sector=int(e['sector']), product=e['product'], held_t=float(e['center']), held_snr=float(e['snr']), rival_t=float(c['center']), rival_snr=float(c['snr']), rival_c5=bool(on(c.get('c5'))), rival_ov=bool(on(c.get('ecl_overlap'))), rival_step=bool(on(c.get('step'))), rival_gap=bool(on(c.get('gap_dump'))), rival_ramp=bool(on(c.get('ramp'))), rival_p1_veto=bool(on(c.get('p1_veto'))), rival_orbit_lock=bool(on(c.get('orbit_lock'))), rival_repeater=bool(on(c.get('repeater'))), rival_tier=str(c.get('tier')), rival_P=Pb.get(star, math.nan), rival_dur_h=c.get('dur_h'), rival_depth=c.get('depth_ppm')))
                            on_ecl = bool(on(c.get("c5")) or on(c.get("ecl_overlap")))
                            st["comp"]["rival on an eclipse (c5 or ecl_overlap)" if on_ecl else "rival off eclipses"] += 1
                            st["comp"]["rival is a repeater or orbit-locked"] += int(on(c.get("repeater")) or on(c.get("orbit_lock")))
                            dx = min(abs(float(c["center"]) - x) for x, d in obs)
                            st["comp"]["rival within 1 d of a planted crossing" if dx <= 1 else ("rival 1 to 3 d away" if dx <= 3 else "rival over 3 d away")] += 1
                            st["comp"]["rival stronger by under 20%"] += int(float(c["snr"]) < 1.2 * float(e["snr"]))
                            if c.get("ph_d") is not None and c.get("ph_d") == c.get("ph_d"):
                                st["phd"].append(float(c["ph_d"]))
                    if len(fl) == 1:
                        st["only"][fl[0]] += 1
    out = {}
    for (b, arm), s in sorted(stat.items()):
        out[f"bin{b}_{arm}"] = dict(n=s["n"], found=s["found"], tier1=s["t1"], held=s["held"], flags=dict(s["flags"].most_common()), only_flag=dict(s["only"].most_common()), rival=dict(s["comp"]), rival_ph_d_median=(sorted(s["phd"])[len(s["phd"]) // 2] if s["phd"] else None), rival_ph_d_n=len(s["phd"]))
    pd.DataFrame(RIV).to_csv(PR.ROOT / "data" / "rs024" / "rivals.csv", index=False)
    tag = f"-prefix{limit}" if limit else ""
    (Path(__file__).parent / f"rivals-summary{tag}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, "held", v["held"], "dominated", v["flags"].get("dominated", 0), "| rival", v["rival"], "| rival ph_d median", v["rival_ph_d_median"], "n", v["rival_ph_d_n"])


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); main(a.parse_args().limit)
