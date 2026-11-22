"""RS-041 W1 (Claude, 22 Nov 2026, 11:10 pm): why do 316 of the 2,000 T156 planted dips stop at 'outside the searched windows'?
Exploratory measurement, design stars only (T156 draws are design-seen), no pass rule: it sizes a pool before any fix is designed.
For every T156 draw at stage 1 (safe windows exist, dip time outside them), load the selected product's light the way the search does
(S2.load, then the window rule of x4_faint.prep: own SPOC hard-quality windows, else the intersection of all neighbour SPOC stars'
windows with 0.5 d trimmed after each gap) and classify the dip time:
  nodata      no loaded cadence within the dip (orbit gap or sector edge: no method can see it)
  trim_only   inside the untrimmed intersection, removed only by the 0.5 d trim after a gap
  intersect   outside the intersection but inside the windows of at least half of the neighbour stars (majority)
  minority    covered by fewer than half of the neighbours (or own SPOC windows exclude it: SPOC dropped those cadences)
Prints counts by product and class. Rows with star ids stay under data/rs041/.
Run: .venv\\Scripts\\python.exe -B research\\stage3\\rs041\\w1_windows.py"""
import os, sys, json, glob, pathlib, collections
ROOT = r"D:/second-sun"; F2 = os.path.join(ROOT, "data", "fable", "f2"); OUT = pathlib.Path(ROOT) / "data" / "rs041"
sys.path.insert(0, F2)
import x4_faint as X


def windows_majority(lists, t):
    np = X.G["np"]
    cover = np.zeros(len(t), int)
    for w in lists:
        cover += X.G["S2"].in_windows(t, w)
    return cover, len(lists)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in glob.glob("D:/second-sun-astra/data/astra/003/workers/*/results-*.jsonl"):
        for l in open(p, encoding="utf-8"):
            if l.strip(): rows.append(json.loads(l))
    out = []
    for camp in ("g2", "g3"):
        X.init(camp); np, S2, A = X.G["np"], X.G["S2"], X.G["A"]
        for r in rows:
            if r["campaign"] != camp or r["dip"]["stage"] != 1: continue
            prod = str(r["product"]); c, half = r["time"], r["duration_h"] / 48
            files = []
            for f in glob.glob(f"{ROOT}/data/{camp}/{r['star']}/*.fits"):
                n = os.path.basename(f).lower()
                fp = "QLP" if "qlp" in n else "TESS-SPOC" if "tess-spoc" in n else "SPOC"
                if (prod == "nan" or fp == prod) and (f"s{r['sector']:04d}" in n or f"-s{r['sector']:04d}-" in n or f"_s{r['sector']:04d}" in n or f"s00{r['sector']:02d}" in n):
                    files.append((fp, f))
            res = dict(campaign=camp, star=r["star"], sector=r["sector"], product=prod, time=c, dur_h=r["duration_h"], cls="nofile")
            for fp, f in files:
                try:
                    t, fl, _, info = S2.load(f, info=True)
                except Exception as e:
                    res["cls"] = f"loaderror"; continue
                near = np.abs(t - c) <= half
                if near.sum() == 0:
                    res["cls"] = "nodata"; continue
                if not info["needs_windows"]:
                    res["cls"] = "spoc_quality"; continue
                sec, cam, ccd = A.head(pathlib.Path(f))
                lists = [w for tic, w in A.DB.get((sec, cam, ccd), {}).items() if tic != r["star"] and w]
                own = next(iter(glob.glob(f"{ROOT}/data/{camp}/{r['star']}/tess*-s{sec:04d}-{r['star']:016d}-*_lc.fits")), None)
                tt = t[near]
                if own:
                    res["cls"] = "own_spoc_excluded" if not S2.in_windows(tt, S2.good_windows(own)).any() else "own_spoc_inside?"
                    continue
                if len(lists) < 2:
                    res["cls"] = "fewer_than_2_neighbours"; continue
                inter0 = A.intersect_windows(lists, trim_start_d=0.0)
                cover, n = windows_majority(lists, tt)
                if S2.in_windows(tt, inter0).any(): res["cls"] = "trim_only"
                elif (cover >= n / 2).any(): res["cls"] = "intersect"
                else: res["cls"] = "minority"
                res.update(n_neigh=n, max_cover=int(cover.max()))
                break
            out.append(res)
        print(camp, "done", flush=True)
    json.dump(out, open(OUT / "w1_rows.json", "w"))
    cnt = collections.Counter((o["product"], o["cls"]) for o in out)
    print("stage-1 draws", len(out))
    for k, v in sorted(cnt.items()): print(k, v)


if __name__ == "__main__":
    main()
