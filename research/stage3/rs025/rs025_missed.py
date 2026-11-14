"""RS-025 Q3 (Claude, 14 Nov 2026): why are about 4 in 10 planted planets never found (no SNR 7+ real event within half a duration of any
observed crossing in the star's best product or its SAP twin)? Reads Codex 006 journals, trial groups and the detector's own box scores at
every planted crossing (trial-N/scores.json: sector, arm, template, crossing centre, box centre, SNR), plus the design-light group
metadata (light-curve status). Each never-found planet gets ONE cause, first match wins:
  1 not_searched: every sector with a crossing has no 'ok' light curve in the best product (status says why)
  2 not_scored: searched, but the detector scored no box at any crossing (data missing or masked there)
  3 scored_7plus_lost: a box at a crossing scored SNR 7+ but no event was written near it
  4 near_miss: best crossing SNR 5 to 7
  5 weak: best crossing SNR under 5
For 4 and 5 also: planted depth, best-product mix, crossings per planet, and whether the best crossing sits in a catalogue eclipse window
(primary at phase 0, secondary at 0.5, widths from stage3_core.eb_widths; approximate for eccentric binaries).
Counts only to rs025/missed.json; private rows to data/rs025/missed.csv."""
import json, math, os, sys
from collections import Counter, defaultdict
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1")
sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
ROOT = Path(r"D:\second-sun"); OUT6 = ROOT / "data" / "astra" / "006"
LAB = {0: "5-10", 1: "10-14", 2: "14-20", 3: "20-27.4", 4: "27.4+"}


def main():
    import importlib, dataset as DS, stage3_core as C
    rows = []
    for camp in ("g2", "g3"):
        os.environ["SS_SET"] = camp; importlib.reload(DS); importlib.reload(C)
        best = {(int(r.tic), int(r.sector)): r["product"] for _, r in pd.read_csv(C.BEST).iterrows()}
        widths = C.eb_widths()
        src = ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0" / "groups"
        status = {}
        for p in src.glob("*.json"):
            tic, sec = map(int, p.stem.split("_"))
            g = json.loads(p.read_text(encoding="utf-8"))
            prod = best.get((tic, sec))
            st = [m.get("status") for m in g["meta"] if m.get("product") == prod]
            status[tic, sec] = ("ok" if "ok" in st else (st[0] if st else "no best-product file"), prod)
        for j in sorted(OUT6.glob(f"planet-*-*-*-{camp}/results.jsonl")):
            for line in j.read_text(encoding="utf-8").splitlines():
                r = json.loads(line); obs = r["observed"]
                if not obs:
                    continue
                star, trial = r["star"], r["trial"]; tdir = j.parent / f"trial-{trial}"
                found = False
                for s in r["changed"]:
                    prod = best.get((star, int(s)))
                    for kind in ("groups", "groups_sap"):
                        p = tdir / "1" / kind / f"{star}_{s}.json"
                        if not p.exists():
                            continue
                        for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
                            if e["kind"] == "real" and (e.get("snr") or 0) >= 7 and e["product"] in (prod, f"{prod}-SAP") and any(abs(e["center"] - c) <= d / 2 for c, d in obs):
                                found = True; break
                        if found: break
                    if found: break
                rec = dict(campaign=camp, trial=trial, star=star, bin=r["bin"], n_cross=len(obs), depth_ppm=r["depth_ppm"], found=found)
                if not found:
                    sc = json.loads((tdir / "scores.json").read_text(encoding="utf-8")).get("1", [])
                    best_snr, best_c, best_sec = -1e9, None, None
                    for sector, arm, template, centre, box_centre, snr in sc:
                        if arm != 1 or template != trial or snr is None or snr != snr:
                            continue
                        if any(abs(centre - c) < 1e-6 for c, d in obs) and snr > best_snr:
                            best_snr, best_c, best_sec = snr, centre, sector
                    secs = {int(s) for s in r["changed"]}
                    st = [status.get((star, s), ("no group file", None)) for s in secs]
                    prods = Counter(p for _, p in st)
                    rec.update(best_snr=(None if best_c is None else round(best_snr, 2)), best_sector=best_sec, products=dict(prods),
                               searched_sectors=sum(1 for x, _ in st if x == "ok"), statuses=dict(Counter(x for x, _ in st)))
                    if rec["searched_sectors"] == 0:
                        cause = "1 not_searched"
                    elif best_c is None:
                        cause = "2 not_scored"
                    elif best_snr >= 7:
                        cause = "3 scored_7plus_lost"
                    elif best_snr >= 5:
                        cause = "4 near_miss"
                    else:
                        cause = "5 weak"
                    rec["cause"] = cause
                    if best_c is not None and star in widths and r.get("binary_period"):
                        ph = ((best_c - r["binary_epoch"]) / r["binary_period"]) % 1.0
                        wp, ws = widths[star]
                        rec["in_eclipse_window"] = bool(min(ph, 1 - ph) <= wp / 2 or abs(ph - 0.5) <= ws / 2)
                rows.append(rec)
        print(camp, "done", flush=True)
    D = pd.DataFrame(rows)
    pdir = ROOT / "data" / "rs025"; pdir.mkdir(exist_ok=True); D.to_csv(pdir / "missed.csv", index=False)
    M = D[~D.found]
    out = dict(planets_with_crossings=int(len(D)), found=int(D.found.sum()), never_found=int(len(M)),
               cause=dict(sorted(Counter(M.cause).items())),
               cause_by_bin={LAB[int(b)]: dict(sorted(Counter(g.cause).items())) for b, g in M.groupby("bin")},
               never_found_share_by_bin={LAB[int(b)]: round(float((~g.found).mean()), 3) for b, g in D.groupby("bin")})
    ns = M[M.cause == "1 not_searched"]
    out["not_searched_statuses"] = dict(Counter(k for d in ns.statuses for k in d))
    for c in ("4 near_miss", "5 weak", "2 not_scored"):
        g = M[M.cause == c]
        if len(g):
            out[c] = dict(n=int(len(g)), median_depth_ppm=round(float(g.depth_ppm.median())), median_crossings=float(g.n_cross.median()),
                          one_crossing=int((g.n_cross == 1).sum()), in_eclipse_window=int(g.get("in_eclipse_window", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()),
                          best_product_mix=dict(Counter(k for d in g.products for k in d)), statuses=dict(Counter(k for d in g.statuses for k in d)))
    f = D[D.found]
    out["found_for_comparison"] = dict(median_depth_ppm=round(float(f.depth_ppm.median())), median_crossings=float(f.n_cross.median()), one_crossing_share=round(float((f.n_cross == 1).mean()), 3))
    out["never_found_one_crossing_share"] = round(float((M.n_cross == 1).mean()), 3)
    (ROOT / "research/stage3/rs025/missed.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
