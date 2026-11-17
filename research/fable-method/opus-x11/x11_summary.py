"""X11 lever 1 summary (Opus, 17 Nov 2026): C1 to C4 against the rule preregistered in WORK-LOG-X11.md.
Same bootstrap as x5_rule4.py; rule (c) = 023/027 own dip-minus-bump per bin (99%); (d) = 023 T156 reference R."""
import json, csv, math, glob, sys
import numpy as np
O = "D:/second-sun/data/opus-x11/out"
def load(prefix, mode, bench="planets"):
    rows, bg, conf = {}, [], None
    for c in ("g2", "g3"):
        d = json.load(open(f"{O}/{prefix}-{bench}-{c}-{mode}.json")); conf = d["configs"]; bg += d["background"]
        for r in d["rows"]: rows[r["campaign"], r["trial"]] = r
    return rows, bg, conf
v0, bg0, conf = load("x11", "V0"); v2, bg2, _ = load("x11", "V2")
f0, _, _ = load("x11f", "V0"); f2, _, _ = load("x11fm", "V2")
t0, _, _ = load("x11", "V0", "T156")
assert len(conf) == 36 and len(v0) == 1098 and len(t0) == 2000
cls = {(r["campaign"], r["trial"]): r["cat"] for r in json.load(open("D:/second-sun/data/fable/f1/f1_trial_classes.json"))}
radii = {}
for r in csv.DictReader(open("D:/second-sun/targets/host_radii_g2_g3.csv", encoding="utf-8-sig")):
    if r["radius_rsun"]:
        v = float(r["radius_rsun"])
        if v > 0 and math.isfinite(v): radii[r["set"], int(r["tic"])] = v
depth = {}
for j in glob.glob("D:/second-sun-astra/data/astra/fable-fresh/planet-*-*-*-g*/results.jsonl"):
    for l in open(j, encoding="utf-8"):
        if l.strip():
            d = json.loads(l); depth[d["campaign"], d["trial"]] = d["depth_ppm"]
def fcat(k):
    rad = radii.get((k[0], f0[k]["star"])); cap = None if rad is None else min(1., (.2009 / rad) ** 2) * 1e6
    return "unknown" if cap is None else "above" if depth[k] > cap else "within"
fcls = {k: fcat(k) for k in f0}
def key(e): return (e["campaign"], e["tic"], e["sector"], e["kind"], e["product"])
Bref = {}
for e in bg0:
    if e["options"][0]: Bref.setdefault(key(e), []).append(e)
assert sum(1 for v in Bref.values() for e in v if e["kind"] == "real") == 174 and sum(1 for v in Bref.values() for e in v if e["kind"] == "flip") == 79
def is_new(e): return not any(abs(e["center"] - b["center"]) <= 0.1 + max(e["dur_h"], b["dur_h"]) / 48 for b in Bref.get(key(e), ()))
def rule4(bg, idx):
    R = [e for e in bg if e["kind"] == "real" and e["options"][idx]]; F = [e for e in bg if e["kind"] == "flip" and e["options"][idx]]
    nr = [e for e in R if is_new(e)]; nf = [e for e in F if is_new(e)]
    return len(R), len(F), len(nr), len(nf), len(nr) - 2.3 * len(nf)
def pstats(rows, cols, sel, seed):
    keys = sorted(k for k in rows if sel(k))
    stars = sorted({(k[0], rows[k]["star"]) for k in keys}); pos = {s: i for i, s in enumerate(stars)}
    den = np.zeros((len(stars), 5)); suc = np.zeros((len(stars), 5, 2, len(cols)))
    for k in keys:
        i = pos[k[0], rows[k]["star"]]; b = rows[k]["bin"]; den[i, b] += 1
        for j, (src, idx) in enumerate(cols):
            suc[i, b, 0, j] += src[k]["real"][idx]; suc[i, b, 1, j] += src[k]["flip"][idx]
    rate = (suc.sum(0) / den.sum(0)[:, None, None]).mean(0)
    rng = np.random.default_rng(seed); w = rng.multinomial(len(stars), np.full(len(stars), 1 / len(stars)), size=8000)
    dd = w @ den; ok = (dd > 0).all(1)
    br = (w[ok] @ suc.reshape(len(stars), -1)).reshape(-1, 5, 2, len(cols)) / dd[ok][:, :, None, None]
    s = br.mean(1); out = []
    for j in range(len(cols)):
        d = s[:, 0, j] - s[:, 0, 0]
        own = np.quantile(br[:, :, 0, j] - br[:, :, 1, j], [.005, .995], axis=0)
        gain = np.quantile((br[:, :, 0, j] - br[:, :, 0, 0]) - (br[:, :, 1, j] - br[:, :, 1, 0]), [.005, .995], axis=0)
        out.append(dict(P=100 * rate[0, j], dP=100 * (rate[0, j] - rate[0, 0]), lo=100 * np.quantile(d, .025), hi=100 * np.quantile(d, .975),
                        Plo=100 * np.quantile(s[:, 0, j], .025), Phi=100 * np.quantile(s[:, 0, j], .975),
                        own=bool(((own[0] <= 0) & (own[1] >= 0)).all()), gain=bool(((gain[0] <= 0) & (gain[1] >= 0)).all())))
    return out
want = ["B", "B+C96", "B+C96-dominated", "B+C96-ramp", "B+C96-gap-edge", "B+C96*C1", "B+C96*C2", "B+C96*C3", "B+C96*C4", "B*C4"]
idx = [conf.index(n) for n in want]
cols = [(v0, 0)] + [(v0, i) for i in idx] + [(v2, i) for i in idx]
fcols = [(f0, 0)] + [(f0, i) for i in idx] + [(f2, i) for i in idx]
names = ["B"] + want + [n + " +M2" for n in want]
bgs = [bg0] + [bg0] * len(idx) + [bg2] * len(idx); bi = [0] + idx + idx
P968 = pstats(v0, cols, lambda k: cls[k] != "above", 20261116)
P1098 = pstats(v0, cols, lambda k: True, 20261116)
PF = pstats(f0, fcols, lambda k: fcls[k] != "above", 20261117)
ref = {k: r for k, r in t0.items() if 3000 <= r["depth_ppm"] <= 6000 and 6 <= r["duration_h"] <= 12}
assert len(ref) == 222
tcols = [(t0, 0)] + [(t0, i) for i in idx]
RT = pstats(ref, tcols, lambda k: True, 20261117)
assert abs(RT[0]["P"] - 34.207) < 0.01, RT[0]["P"]
print("B T156 reference R reproduced:", round(RT[0]["P"], 3))
print(f"{'config':22s} {'P968':>6s} {'dP968 [95%]':>21s} {'dP1098':>7s} {'fresh dP [95%]':>21s} {'own':>3s} {'ownF':>4s} {'gain':>4s} {'R':>6s} real  ud  nR  nU   exc  pass")
res = []
for j, n in enumerate(names):
    r, f, nr, nf, exc = rule4(bgs[j], bi[j]); a, b, fr = P968[j], P1098[j], PF[j]
    R = RT[j]["P"] if j < len(tcols) else float("nan")
    ok = dict(a=a["dP"] >= 2.0 and a["lo"] > 0, a2=fr["lo"] > 0 and fr["dP"] >= a["dP"] / 2, b=r <= 174 and f <= 79,
              c=a["own"] and b["own"] and fr["own"], d=R >= RT[0]["P"] - 1e-9, e=exc <= 5, notM2="+M2" not in n)
    allp = all(ok.values()) and j > 0
    res.append(dict(config=n, P968=a, P1098=b, fresh=fr, R=R, real=r, ud=f, new_real=nr, new_ud=nf, excess=exc, rules=ok, passes=allp))
    print(f"{n:22s} {a['P']:6.2f} {a['dP']:+6.2f} [{a['lo']:+5.2f},{a['hi']:+5.2f}] {b['dP']:+7.2f} {fr['dP']:+6.2f} [{fr['lo']:+5.2f},{fr['hi']:+5.2f}] {str(a['own'] and b['own'])[0]:>3s} {str(fr['own'])[0]:>4s} {str(a['gain'])[0]:>4s} {R:6.2f} {r:4d} {f:3d} {nr:3d} {nf:3d} {exc:5.1f}  {'PASS' if allp else 'fail: ' + ','.join(k for k, v in ok.items() if not v)}")
json.dump(res, open("D:/second-sun/data/opus-x11/x11_lever1.json", "w"), indent=1, default=lambda v: bool(v) if isinstance(v, np.bool_) else float(v))
