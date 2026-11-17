"""X5 (Opus, 17 Nov 2026): every saved Fable configuration scored on the five freeze rules that saved outputs allow.
Reads only Fable's saved scorer outputs (x6/x10 choosing bench, x1/x1m fresh bench). Writes nothing but stdout and a JSON.
Rule 4: new real minus 2.3 x new upside-down at most 5, new = tier-1 untouched-background event of the configuration with no
match among B's (no M2) tier-1 events: same campaign, star, sector, arm, product, centres within 0.1 d plus half the longer box
(the match of Claude's 027 addendum)."""
import json, csv, math, glob, sys
import numpy as np
A = "D:/second-sun-astra/data/astra/fable-f4"
def load(prefix, mode):
    rows, bg, conf = {}, [], None
    for c in ("g2", "g3"):
        d = json.load(open(f"{A}/{prefix}-planets-{c}-{mode}.json")); conf = d["configs"]; bg += d["background"]
        for r in d["rows"]: rows[r["campaign"], r["trial"]] = r
    return rows, bg, conf
v0, bg0, conf = load("x6", "V0"); v2, bg2, conf2 = load("x10", "V2")
f0, fb0, _ = load("x1", "V0"); f2, fb2, _ = load("x1m", "V2")
assert conf == conf2 and len(conf) == 34
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

# --- background and rule 4
def t1(bg, idx, kind): return [e for e in bg if e["kind"] == kind and e["options"][idx]]
def key(e): return (e["campaign"], e["tic"], e["sector"], e["kind"], e["product"])
Bref = {}
for e in bg0:
    if e["options"][0]: Bref.setdefault(key(e), []).append(e)
assert sum(len(v) for v in Bref.values()) == 174 + 79
def is_new(e):
    for b in Bref.get(key(e), ()):
        if abs(e["center"] - b["center"]) <= 0.1 + max(e["dur_h"], b["dur_h"]) / 48: return False
    return True
def rule4(bg, idx):
    nr = [e for e in t1(bg, idx, "real") if is_new(e)]; nf = [e for e in t1(bg, idx, "flip") if is_new(e)]
    dump = sum("momentum dump" in str(e["flags"]) for e in nr)
    return len(t1(bg, idx, "real")), len(t1(bg, idx, "flip")), len(nr), len(nf), len(nr) - 2.3 * len(nf), dump

# --- P with paired whole-star bootstrap, and per-bin dip-minus-bump control (99%)
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
    binr = (w[ok] @ suc.reshape(len(stars), -1)).reshape(-1, 5, 2, len(cols)) / dd[ok][:, :, None, None]
    s = binr.mean(1)
    out = []
    for j in range(len(cols)):
        d = s[:, 0, j] - s[:, 0, 0]
        # control: per bin, (dip gain vs B) minus (bump gain vs B), 99% interval must contain zero
        g = (binr[:, :, 0, j] - binr[:, :, 0, 0]) - (binr[:, :, 1, j] - binr[:, :, 1, 0])
        lo, hi = np.quantile(g, [.005, .995], axis=0)
        ctrl = bool(((lo <= 0) & (hi >= 0)).all())
        out.append(dict(P=100 * rate[0, j], dP=100 * (rate[0, j] - rate[0, 0]), lo=100 * np.quantile(d, .025),
                        hi=100 * np.quantile(d, .975), Plo=100 * np.quantile(s[:, 0, j], .025), Phi=100 * np.quantile(s[:, 0, j], .975), ctrl=ctrl))
    return out, len(keys)

idxs = [i for i, n in enumerate(conf) if n == "B" or "C96" in n]
cols0 = [(v0, 0)] + [(v0, i) for i in idxs] + [(v2, i) for i in idxs]
names = ["B"] + [conf[i] for i in idxs] + [conf[i] + " +M2" for i in idxs]
bgs = [bg0] + [bg0] * len(idxs) + [bg2] * len(idxs)
bidx = [0] + idxs + idxs
pos_, npos = pstats(v0, cols0, lambda k: cls[k] != "above", 20261116)
all_, nall = pstats(v0, cols0, lambda k: True, 20261116)
fcols = [(f0, 0)] + [(f0, i) for i in idxs] + [(f2, i) for i in idxs]
fpos, nfp = pstats(f0, fcols, lambda k: fcls[k] != "above", 20261117)
print(f"choosing bench possible n={npos}, all n={nall}; fresh possible n={nfp}")
print(f"{'config':24s} {'P968':>6s} {'dP968 [95%]':>20s} {'dP1098':>7s} {'fresh dP [95%]':>20s} {'ctrl':>4s} {'ctrlF':>5s} {'real':>4s} {'ud':>3s} {'nR':>3s} {'nU':>3s} {'exc':>6s} {'nRdump':>6s}  pass")
res = []
for j, n in enumerate(names):
    r, f, nr, nf, exc, dump = rule4(bgs[j], bidx[j])
    p, a, fr = pos_[j], all_[j], fpos[j]
    ok = dict(a=bool(p["lo"] > 0 and fr["lo"] > 0), b=bool(r <= 174 and f <= 79), c=bool(p["ctrl"] and fr["ctrl"]), e=bool(exc <= 5))
    res.append(dict(config=n, P968=p["P"], P968_lo=p["Plo"], P968_hi=p["Phi"], dP968=p["dP"], dP968_lo=p["lo"], dP968_hi=p["hi"],
                    P1098=a["P"], dP1098=a["dP"], dP1098_lo=a["lo"], dP1098_hi=a["hi"], Pfresh=fr["P"], Pfresh_lo=fr["Plo"], Pfresh_hi=fr["Phi"],
                    dPfresh=fr["dP"], dPfresh_lo=fr["lo"], dPfresh_hi=fr["hi"], ctrl=bool(p["ctrl"]), ctrl_fresh=bool(fr["ctrl"]),
                    real=r, ud=f, new_real=nr, new_ud=nf, excess=exc, new_real_dump=dump, rules=ok))
    print(f"{n:24s} {p['P']:6.2f} {p['dP']:+6.2f} [{p['lo']:+5.2f},{p['hi']:+5.2f}] {a['dP']:+7.2f} {fr['dP']:+6.2f} [{fr['lo']:+5.2f},{fr['hi']:+5.2f}] {str(p['ctrl'])[0]:>4s} {str(fr['ctrl'])[0]:>5s} {r:4d} {f:3d} {nr:3d} {nf:3d} {exc:6.1f} {dump:6d}  {''.join(k for k, v in ok.items() if v)}")
json.dump(res, open("D:/second-sun/data/opus-x11/x5_rule4.json", "w"), indent=1)
