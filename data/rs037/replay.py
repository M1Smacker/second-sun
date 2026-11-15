"""RS-038 trace (read-only replay of the frozen chain): for every planted crossing that got no score, find the FIRST step that removes it.
Steps as in stage2_search.prepare + Prod.scores: L load (hard quality mask, finite flux) -> W safe windows (QLP only) -> M eclipse mask
(Petrova p1 mask_runs) -> S score at the box nearest the crossing length. Also: was the crossing kept to S by another product
(the capture records only the table's best product). Run: SS_SET=g2|g3 python -I -B replay.py g2"""
import os, sys, json, glob, collections, math
camp=sys.argv[1]
os.environ.update(SS_SET=camp, VESPER_OPTS="c6,p1", NUMBA_NUM_THREADS="2")
sys.path.insert(0, os.path.abspath("pipeline"))
import numpy as np, pandas as pd, tempfile
import stage2_search as S2, stage3 as S3, stage3_core as C
S3._init3(tempfile.mkdtemp(), camp, C.GRID_V5)
A, V = S2.A, S2.V
import petrova_mask as PM
best = {(r.tic, r.sector): r.product for r in pd.read_csv(C.BEST).itertuples()}
R = "D:/second-sun-astra/data/astra/006"
filecache = {}
def star_files(tic):
    if tic in filecache: return filecache[tic]
    out = []
    for p in sorted(glob.glob(f"data/{camp}/{tic}/*.fits")):
        try:
            t, f, n, info = S2.load(p, info=True)
            sec, cam, ccd = A.head(__import__("pathlib").Path(p))
            out.append(dict(p=p, t=t, f=f, info=info, sec=sec, cam=cam, ccd=ccd))
        except Exception as e:
            out.append(dict(p=p, err=str(e)[:60]))
    filecache[tic] = out; return out
prepcache = {}
def stages(tic, x):
    key = x["p"]
    if key in prepcache: return prepcache[key]
    t, f, info = x["t"], x["f"], x["info"]; st = {"L": t}
    if info["needs_windows"]:
        nbw, nn = A.neighbour_windows(x["sec"], x["cam"], x["ccd"], tic)
        own = next(iter(glob.glob(f"data/{camp}/{tic}/tess*-s{x['sec']:04d}-{tic:016d}-*_lc.fits")), None)
        if own: k = S2.in_windows(t, S2.good_windows(own))
        elif nn >= 2: k = S2.in_windows(t, nbw)
        else: k = np.zeros(len(t), bool)
        t, f = t[k], f[k]
    st["W"] = t
    if len(t) >= 200:
        tm, fm, runs, _ = PM.mask_runs(t, f, A.PER.get(tic, []), tic)
    else: tm, fm = t[:0], f[:0]
    st["M"] = tm
    st["prod"] = S2.Prod(tm, fm) if len(tm) >= 200 else None
    prepcache[key] = st; return st
lost = collections.Counter(); byprod = collections.Counter(); other_ok = 0; n = 0; examples = collections.defaultdict(list)
for d in glob.glob(R + f"/planet-*-{camp}"):
    if "short" in d: continue
    for l in open(d + "/results.jsonl", encoding="utf-8"):
        r = json.loads(l); tic = r["star"]
        try: sc = json.load(open(f"{d}/trial-{r['trial']}/scores.json"))
        except FileNotFoundError: continue
        capt = {round(c, 3) for s, a, tm, c, t, v in sc["1"] if tm == r["trial"] and a == 1}
        for c, du in r["observed"]:
            if round(c, 3) in capt: continue
            n += 1; hw = du / 2
            box = min(S2.DURS_H, key=lambda h: abs(math.log(h / (24 * du))))
            files = [x for x in star_files(tic) if "t" in x and len(x["t"]) and x["t"].min() - 1 <= c <= x["t"].max() + 1]
            secs = {x["sec"] for x in files}
            bp = None
            for s in secs: bp = best.get((tic, s), bp)
            res = {}
            for x in files:
                st = stages(tic, x); first = None
                for k in ("L", "W", "M"):
                    if (np.abs(st[k] - c) <= hw).sum() < 3: first = k; break
                if first is None:
                    if st["prod"] is None: first = "M"
                    else:
                        bt, snr, _ = st["prod"].scores(box)
                        ok = np.isfinite(snr) & (np.abs(bt - c) <= hw)
                        first = "S" if not ok.any() else "kept"
                res[x["info"]["product"]] = first
            if not res: cause = "no file covers the time"
            else:
                b = res.get(bp)
                if b is None: cause = f"best product ({bp}) has no file here"
                elif b == "kept": cause = "kept to the score step in the best product (capture mismatch)"
                else: cause = {"L": "load (hard quality mask, NaN flux)", "W": "safe windows (QLP)", "M": "eclipse mask or too little data", "S": "no finite score (edge, gap, box)"}[b]
                if b != "kept" and any(v == "kept" for k, v in res.items() if k != bp): other_ok += 1; cause += " | another product kept it"
            lost[cause] += 1; byprod[bp] += 1
            if len(examples[cause]) < 3: examples[cause].append((tic, round(c, 2), round(du, 2), bp, res))
print(camp, "never-scored crossings replayed:", n)
for k, v in lost.most_common(): print(f"  {v:5d}  {k}")
print("  best product of those crossings:", dict(byprod)); print("  another product kept it to the score step:", other_ok)
json.dump({k: v for k, v in examples.items()}, open(f"data/rs037/replay-examples-{camp}.json", "w"), default=str)
