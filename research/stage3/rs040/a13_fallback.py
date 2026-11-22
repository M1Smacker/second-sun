"""RS-040 A13 (Claude, 22 Nov 2026, 10:46 pm; written and committed before any A13 result).
Why: A12 showed RS-039's notch gain (+7.7 detection at equal alarms) was measured only on crossings the notch could score. 110 of
1,427 crossings (7.7%) have NO notch score (a flank lacks data, mostly next to gaps); the frozen box SNR detects about half of them.
Over all crossings the notch gain is about +2.9, not +7.7.
Test: 'notchF' = the notch SNR where the notch is defined at that box and centre; where it is not, the frozen box SNR at the same box
length and nearest centre, compared against its OWN threshold scale (frozen SNR minus 2: frozen 7 corresponds to notch 5 at equal
alarms in A8c/A12; written now, not tuned). Same 160 design stars and seed as A8b/A12, planted crossings and untouched light,
both arms, thresholds 4.5 to 12.
Comparison rule (same as A12, written first): each statistic at the lowest threshold whose untouched alarms are at most frozen-at-7
on both arms; detected share over ALL crossings (best product per crossing, unscored = missed). notchF is a lead for D2 (a Codex
tier-level bench) if it beats the notch by at least +2.0 points with the whole-star 95% interval above zero.
Prediction: +2 to +4 points over the notch at equal alarms if fallback alarms near gaps stay small; real-arm alarms rise more than
upside-down (gap artefacts are dip-only), which this detection-level test can only partly see.
Run (from repo root): .venv\\Scripts\\python.exe -B research\\stage3\\rs040\\a13_fallback.py g2 3 90   (then g3 3 70)"""
import os, sys, json, glob, random, collections
ROOT = r"D:/second-sun"; RS = os.path.join(ROOT, "data", "rs039"); F2 = os.path.join(ROOT, "data", "fable", "f2")
sys.path.insert(0, F2); sys.path.insert(0, RS)
import x4_faint as X
import a8b_notchmin as N
A006 = X.A006
THR = (4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 9, 10, 12)
SHIFT = 2.0


def notchF_scores(t, f, d_h):
    np = X.G["np"]
    cn, sn = N.notch_scores(t, f, d_h)
    cf, sf = N.frozen_scores(t, f, d_h)
    out = sn.copy()
    miss = ~np.isfinite(sn)
    if miss.any() and len(cf):
        j = np.clip(np.searchsorted(cf, cn[miss]), 0, len(cf) - 1)
        j0 = np.clip(j - 1, 0, len(cf) - 1)
        jj = np.where(np.abs(cf[j0] - cn[miss]) < np.abs(cf[j] - cn[miss]), j0, j)
        close = np.abs(cf[jj] - cn[miss]) <= 0.25 * d_h / 24
        out[miss] = np.where(close, sf[jj] - SHIFT, np.nan)
    return cn, out


def n_events(sc):
    np = X.G["np"]; cands = []
    for h, (cen, s) in sc.items():
        for i in np.flatnonzero(np.nan_to_num(s, nan=-99) >= min(THR)): cands.append((s[i], cen[i], h))
    cands.sort(reverse=True); ev = []
    for s, c, h in cands:
        if all(abs(c - e[1]) > 0.5 * max(h, e[2]) / 24 + 0.1 for e in ev): ev.append((s, c, h))
    return {str(t): sum(1 for e in ev if e[0] >= t) for t in THR}


def init(camp):
    X.init(camp)
    N.STATS.clear(); N.STATS.update(notchF=notchF_scores); N.n_events = n_events   # notch and frozen rows come from A12 (same light, same rows)


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
                if fr["st"] == "ok": jobs[r["star"]][fr["prod"], fr["sec"]][x["trial"]].append((x["c"], x["d"], depth[camp, x["trial"]]))
    stars = sorted(jobs); random.Random(20261118).shuffle(stars); stars = stars[:nst]
    todo = [(s, {k: dict(v) for k, v in jobs[s].items()}) for s in stars]
    print(camp, "stars", len(todo), flush=True)
    import multiprocessing as mp
    with mp.Pool(workers, initializer=init, initargs=(camp,)) as pool, open(f"{RS}/a13-{camp}.jsonl", "w", encoding="utf-8") as fh:
        for i, res in enumerate(pool.imap_unordered(N.star_job, todo)):
            fh.write(json.dumps(res) + "\n"); fh.flush()
            print(i, res["star"], len(res["rows"]), len(res["bg"]), res["errors"][:1], flush=True)
    print("complete", camp, flush=True)


if __name__ == "__main__":
    main()
