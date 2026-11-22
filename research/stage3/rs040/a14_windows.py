"""RS-040 A14 (Claude, 22 Nov 2026, 11:52 pm; rules written and committed before any result): what do Fable F2's window rules cost in
false alarms? QLP light of design stars WITHOUT their own SPOC file is searched only inside the intersection of all SPOC neighbours'
good-time windows (0.5 d trimmed after each gap); with fewer than 2 neighbours the star-sector is dropped. Two alternatives:
  maj: time inside the windows of at least half of the neighbours, then the same 0.5 d trim after each gap (needs >= 2 neighbours)
  nn1: a star-sector with exactly 1 neighbour uses that neighbour's windows, trimmed the same way
Statistic: the lower-flank notch (RS-039 A8b), threshold 5 (its equal-alarm point against frozen at 7, A8c/A12), on light windowed by
the WIDER rule; events are counted by where their centre falls: 'old' time (current rule) or 'extra' time (only the new rule).
Untouched light, both arms: alarms per 100 days in old and in extra time. Planted crossings (006 design trials, census crossings in
these files): share detected at 5 for crossings centred in old time and in extra time.
Rule (written first): a window rule is a lead for the Petrova 2.0 bench if, in extra time, alarms per 100 days on BOTH arms are at most
1.5 x the old-time rate AND planted crossings there are detected at least 0.8 x the old-time share.
Same 160 design stars and seed as A8b/A12. Run: .venv\\Scripts\\python.exe -B research\\stage3\\rs040\\a14_windows.py g2 3 90  (then g3 3 70)"""
import os, sys, json, glob, random, collections, pathlib
ROOT = r"D:/second-sun"; RS = os.path.join(ROOT, "data", "rs039"); F2 = os.path.join(ROOT, "data", "fable", "f2")
sys.path.insert(0, F2); sys.path.insert(0, RS)
import x4_faint as X
import a8b_notchmin as N
A006 = X.A006
THR = 5.0


def trim(windows, d=0.5):
    return [(a + d, b) for a, b in windows if b - a > d]


def majority(lists, t):
    np, S2 = X.G["np"], X.G["S2"]
    cover = sum(S2.in_windows(t, w).astype(int) for w in lists)
    keep = cover * 2 >= len(lists)
    if not keep.any(): return []
    tk = t[keep]; gi = np.where(np.diff(tk) > 0.25)[0]
    return trim(list(zip(np.r_[tk[0], tk[gi + 1]], np.r_[tk[gi], tk[-1]])))


def events(t, f):
    np = X.G["np"]; out = []
    for h in X.G["S2"].DURS_H:
        c, s = N.notch_scores(t, f, h)
        for i in np.flatnonzero(np.nan_to_num(s, nan=-99) >= THR): out.append((s[i], c[i], h))
    out.sort(reverse=True); ev = []
    for s, c, h in out:
        if all(abs(c - e[1]) > 0.5 * max(h, e[2]) / 24 + 0.1 for e in ev): ev.append((s, c, h))
    return ev


def star_job(args):
    star, want = args
    np, S2, A = X.G["np"], X.G["S2"], X.G["A"]
    res = dict(star=star, files=[], errors=[])
    for p in sorted(glob.glob(f"{ROOT}/data/{X.G['camp']}/{star}/hlsp_qlp_*.fits")):
        try:
            t0, f0, _, info = S2.load(p, info=True)
            sec, cam, ccd = A.head(pathlib.Path(p))
            if glob.glob(f"{ROOT}/data/{X.G['camp']}/{star}/tess*-s{sec:04d}-{star:016d}-*_lc.fits"): continue
            lists = [w for tic, w in A.DB.get((sec, cam, ccd), {}).items() if tic != star and w]
            if len(lists) >= 2:
                old = A.intersect_windows(lists); new = majority(lists, t0); rule = "maj"
            elif len(lists) == 1:
                old = []; new = trim(lists[0]); rule = "nn1"
            else: continue
            k = S2.in_windows(t0, new) | S2.in_windows(t0, old)
            if k.sum() < 200: continue
            t, f = t0[k], f0[k]
            in_old = lambda c: bool(old) and S2.in_windows(np.array([c]), old)[0]
            dt = np.diff(t); live = dt[dt < 0.1].sum()
            told = t[S2.in_windows(t, old)] if old else np.array([])
            dold = np.diff(told)[np.diff(told) < 0.1].sum() if len(told) > 1 else 0.0
            rec = dict(sec=int(sec), rule=rule, days_old=round(float(dold), 2), days_extra=round(float(live - dold), 2))
            for arm, ff in (("r", f), ("u", 2 - f)):
                ev = events(t, ff)
                rec[arm + "_old"] = sum(1 for e in ev if in_old(e[1])); rec[arm + "_extra"] = sum(1 for e in ev if not in_old(e[1]))
            rows = []
            for trial, plant in want.get(("QLP", int(sec)), {}).items():
                fp = f.copy()
                for c, d, depth in plant:
                    fp -= depth * np.clip((d / 2 - np.abs(t - c)) / (.1 * d), 0, 1)
                ev = events(t, fp)
                for c, d, depth in plant:
                    if not S2.in_windows(np.array([c]), new + old)[0]: continue
                    rows.append(dict(trial=trial, where="old" if in_old(c) else "extra", hit=any(abs(e[1] - c) <= d / 2 for e in ev)))
            rec["planted"] = rows
            res["files"].append(rec)
        except Exception as e:
            res["errors"].append(f"{os.path.basename(p)}: {type(e).__name__}: {str(e)[:120]}")
    return res


def main():
    camp, workers = sys.argv[1], int(sys.argv[2]); nst = int(sys.argv[3]) if len(sys.argv) > 3 else 80
    depth = {(t["campaign"], t["trial"]): t["depth_ppm"] * 1e-6 for t in json.load(open(A006 + "/planet-design.json"))["trials"]}
    jobs = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    for l in open(f"{F2}/census-{camp}.jsonl", encoding="utf-8"):
        if not l.strip(): continue
        r = json.loads(l)
        for x in r["crossings"]:
            if x["kind"] != "P": continue
            for fr in x["files"]:
                if fr["prod"] == "QLP": jobs[r["star"]][fr["prod"], fr["sec"]][x["trial"]].append((x["c"], x["d"], depth[camp, x["trial"]]))
    stars = sorted(jobs); random.Random(20261118).shuffle(stars); stars = stars[:nst]
    todo = [(s, {k: dict(v) for k, v in jobs[s].items()}) for s in stars]
    print(camp, "stars", len(todo), flush=True)
    import multiprocessing as mp
    with mp.Pool(workers, initializer=X.init, initargs=(camp,)) as pool, open(f"{RS}/a14-{camp}.jsonl", "w", encoding="utf-8") as fh:
        for i, res in enumerate(pool.imap_unordered(star_job, todo)):
            fh.write(json.dumps(res) + "\n"); fh.flush()
            print(i, res["star"], len(res["files"]), res["errors"][:1], flush=True)
    print("complete", camp, flush=True)


if __name__ == "__main__":
    main()
