"""RS-040 A12 (Claude, 22 Nov 2026, 9:52 pm; written before any result): detection-level test of a per-box-length detrending window,
the field's rule (wotan: best window 3 x T14, Hippke et al. 2019; STANLEY and Oddo 2026b use duration-matched windows), on the same
160 design stars and seed as RS-039 A8b (90 G2, 70 G3), planted crossings and untouched light, both arms.
Statistics: frozen (2-day biweight, box SNR, reference); notch (A8b lower-flank notch on 5-day detrend, the 030/D1 statistic);
w3 (biweight window 3 x box length per box length, then the frozen box SNR); w3notch (biweight window 5 x box length, at least 1 day,
so the notch's 4.5 D span fits, then the lower-flank notch).
Measured: per planted crossing the best SNR near it on each statistic and on the upside-down copy (mirror, box-overlap 0.25 D);
untouched alarms on both arms at thresholds 4.5 to 12. Comparison rule (written first): for each statistic take the LOWEST threshold
whose untouched alarms are at most frozen-at-7 on BOTH arms; compare planted crossings detected at that threshold. A statistic is a
lead for a Codex bench if it beats the notch at its own equal-alarm point by at least +2 points of crossings.
Prediction before running: w3 detects more than frozen at 7 (+5 to +8, as c1a) but its alarms rise; at equal alarms it ties the notch
within 2 points; w3notch is the unknown.
Run: .venv\\Scripts\\python.exe -B data\\rs039\\a12_window.py g2 3 90   (then g3 3 70)"""
import os, sys, json, glob, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = r"D:/second-sun"; F2 = os.path.join(ROOT, "data", "fable", "f2")
sys.path.insert(0, F2); sys.path.insert(0, HERE)
import x4_faint as X
import a8b_notchmin as N
A006 = X.A006
THR = (4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 9, 10, 12)


def notch_on(tt, ff, d_h):
    np, S2 = X.G["np"], X.G["S2"]
    bd = S2.bin_width(tt); bt, bf = S2.bin10(tt, ff, bd)
    w = max(int(round(d_h * 60 / (bd * 1440))), 1)
    g = max(int(round(0.25 * w)), 1); fl = max(int(round(1.5 * w)), 1)
    v = np.isfinite(bf); cn = np.concatenate([[0], np.cumsum(v)]); cf = np.concatenate([[0], np.cumsum(np.where(v, bf, 0.0))])
    n = len(bf)
    def mean(a, b):
        a = np.clip(a, 0, n); b = np.clip(b, 0, n)
        k = cn[b] - cn[a]; return np.where(k > 0, (cf[b] - cf[a]) / np.maximum(k, 1), np.nan), k
    i = np.arange(n)
    box, kb = mean(i, i + w); lf, kl = mean(i - g - fl, i - g); rf, kr = mean(i + w + g, i + w + g + fl)
    good = (kb >= 0.8 * w) & (kl >= 0.6 * fl) & (kr >= 0.6 * fl)
    depth = np.where(good, np.fmin(lf, rf) - box, np.nan)
    centre = bt + (w - 1) * bd / 2; gd = np.isfinite(depth)
    if gd.sum() < 20: return centre, np.full(n, np.nan)
    sig = 1.4826 * np.nanmedian(np.abs(depth[gd] - np.nanmedian(depth[gd])))
    return centre, (depth - np.nanmedian(depth[gd])) / sig


def flat(t, f, win):
    np = X.G["np"]
    from wotan import flatten
    ff = flatten(t, f, method="biweight", window_length=win); ok = np.isfinite(ff)
    return t[ok], ff[ok]


def w3_scores(t, f, d_h):
    S2 = X.G["S2"]
    tt, ff = flat(t, f, 3 * d_h / 24); bd = S2.bin_width(tt); bt, bf = S2.bin10(tt, ff, bd)
    c, s, _ = S2.box_scores(bt, bf, d_h, bin_d=bd); return c, s


def w3notch_scores(t, f, d_h):
    tt, ff = flat(t, f, max(5 * d_h / 24, 1.0)); return notch_on(tt, ff, d_h)


N.STATS.update(w3=w3_scores, w3notch=w3notch_scores)


def n_events(sc):
    np = X.G["np"]; cands = []
    for h, (cen, s) in sc.items():
        for i in np.flatnonzero(np.nan_to_num(s) >= min(THR)): cands.append((s[i], cen[i], h))
    cands.sort(reverse=True); ev = []
    for s, c, h in cands:
        if all(abs(c - e[1]) > 0.5 * max(h, e[2]) / 24 + 0.1 for e in ev): ev.append((s, c, h))
    return {str(t): sum(1 for e in ev if e[0] >= t) for t in THR}


N.n_events = n_events


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
    with mp.Pool(workers, initializer=init, initargs=(camp,)) as pool, open(f"{HERE}/a12-{camp}.jsonl", "w", encoding="utf-8") as fh:
        for i, res in enumerate(pool.imap_unordered(N.star_job, todo)):
            fh.write(json.dumps(res) + "\n"); fh.flush()
            print(i, res["star"], len(res["rows"]), len(res["bg"]), res["errors"][:1], flush=True)
    print("complete", camp, flush=True)


def init(camp):
    X.init(camp)
    N.STATS.update(w3=w3_scores, w3notch=w3notch_scores); N.n_events = n_events


if __name__ == "__main__":
    main()
