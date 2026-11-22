"""Claude's independent recount of Codex 031 (D1), first key. Written 22 Nov 2026, 11:26 pm, BEFORE any 031 score existed
(the bench stopped at records; relaunch 2:37 am). No Codex import. Reads only Codex's saved records and scored rows:
  data/astra/031/records/{phase}-{c}.json      (trial, star, bin, depth_ppm; T156: duration_h)
  data/astra/031/scored/{phase}-{c}-{v}.json    (rows: trial, real[0], flip[0]); v in B, N1, D1
  data/astra/031/scored/{phase}-{c}-{v}-background.json (background events: kind, options[0], tic, sector, center)
Phases: choosing, fresh_old, fresh_new, T156_old, T156_new. Planet P = equal weight per binary-period bin, possible planets only
(no radius, or depth_ppm <= 1e6 x min(1, (0.2009/R)^2), radii targets/host_radii_g2_g3.csv). T156 R = reference subset
3,000 to 6,000 ppm and 6 to 12 h, equal-bin. Whole-star bootstrap seed 2026112250, 4,000 draws (Codex uses its own seed).
Rules recounted: (a) fresh_new D1 - B >= +2.0 with interval above 0; (b) background real <= 174, upside-down <= 79;
(c) dip minus bump per bin for B and D1; (e) new real - 2.3 x new upside-down <= 5 (same tic, sector, kind, centre within 0.25 d);
(f) T156_new R(D1) >= R(B). (d) and (g) are Codex's. Missing files are reported, not guessed."""
import json, csv, math, collections, pathlib
import numpy as np
A = pathlib.Path("D:/second-sun-astra/data/astra/031"); AS = "D:/second-sun-astra"
rad = {}
for r in csv.DictReader(open(AS + "/targets/host_radii_g2_g3.csv", encoding="utf-8-sig")):
    try:
        x = float(r["radius_rsun"])
        if math.isfinite(x) and x > 0: rad[(r["set"], int(r["tic"]))] = x
    except ValueError: pass
def possible(c, star, dep):
    R = rad.get((c, star)); return R is None or dep <= 1e6 * min(1.0, (0.2009 / R) ** 2)
def load(path):
    return json.load(open(path)) if path.is_file() else None
def rows(phase, v):
    out = {}
    for c in ("g2", "g3"):
        rec = load(A / "records" / f"{phase}-{c}.json"); sc = load(A / "scored" / f"{phase}-{c}-{v}.json")
        if rec is None or sc is None: return None
        R = {r["trial"]: r for r in rec}
        for s in sc["rows"]:
            r = R[s["trial"]]; assert r["star"] == s["star"] and r["bin"] == s["bin"], (phase, v, s["trial"])
            out[(c, s["trial"])] = dict(c=c, star=r["star"], bin=r["bin"], dep=r["depth_ppm"], dur=r.get("duration_h"),
                                        real=bool(s["real"][0]), flip=bool(s["flip"][0]))
    return out
def P(sel, k):
    return 100 * np.mean([np.mean([r[k] for r in sel if r["bin"] == b]) for b in range(5) if any(r["bin"] == b for r in sel)])
def boot(pairs, fn, seed=2026112250, n=4000):
    st = collections.defaultdict(list)
    for p in pairs: st[(p[0]["c"], p[0]["star"])].append(p)
    S = list(st); rng = np.random.default_rng(seed); d = []
    for _ in range(n):
        s = [p for j in rng.integers(0, len(S), len(S)) for p in st[S[j]]]
        d.append(fn([p[1] for p in s]) - fn([p[0] for p in s]))
    return np.quantile(d, .025), np.quantile(d, .975)
res = {}
for phase in ("choosing", "fresh_old", "fresh_new", "T156_old", "T156_new"):
    V = {v: rows(phase, v) for v in ("B", "N1", "D1")}
    if V["B"] is None or V["D1"] is None:
        print(phase, "files missing"); continue
    keys = sorted(set(V["B"]) & set(V["D1"]))
    if phase.startswith("T156"):
        sel = [k for k in keys if 3000 <= V["B"][k]["dep"] <= 6000 and 6 <= V["B"][k]["dur"] <= 12]
        f = lambda s: P(s, "real")
        line = {v: round(f([V[v][k] for k in sel]), 3) for v in V if V[v] is not None}
        lo, hi = boot([(V["B"][k], V["D1"][k]) for k in sel], f)
        print(f"{phase}: reference {len(sel)} of {len(keys)}; R {line}; D1 - B 95% {lo:+.2f} to {hi:+.2f}")
        res[phase] = line
    else:
        sel = [k for k in keys if possible(V["B"][k]["c"], V["B"][k]["star"], V["B"][k]["dep"])]
        f = lambda s: P(s, "real")
        line = {v: round(f([V[v][k] for k in sel]), 3) for v in V if V[v] is not None}
        lo, hi = boot([(V["B"][k], V["D1"][k]) for k in sel], f)
        gap = {v: [round(np.mean([V[v][k]["real"] for k in sel if V[v][k]["bin"] == b]) - np.mean([V[v][k]["flip"] for k in sel if V[v][k]["bin"] == b]), 3) for b in range(5)] for v in ("B", "D1")}
        print(f"{phase}: possible {len(sel)} of {len(keys)}; P {line}; D1 - B {line['D1'] - line['B']:+.2f} (95% {lo:+.2f} to {hi:+.2f}); dip-bump per bin {gap}")
        res[phase] = line
bg = {}
for v in ("B", "N1", "D1"):
    ev = []
    for c in ("g2", "g3"):
        s = load(A / "scored" / f"choosing-{c}-{v}-background.json")
        if s is None: ev = None; break
        ev += [e for e in s["background"] if e["options"][0]]
    bg[v] = ev
if bg["B"] is not None and bg["D1"] is not None:
    same = lambda e, o: e["tic"] == o["tic"] and e["sector"] == o["sector"] and e["kind"] == o["kind"] and abs(e["center"] - o["center"]) <= 0.25
    for v in ("B", "D1"): print(f"(b) {v}: real {sum(e['kind'] == 'real' for e in bg[v])}, upside-down {sum(e['kind'] == 'flip' for e in bg[v])}")
    new = [e for e in bg["D1"] if not any(same(e, o) for o in bg["B"])]
    nr, nf = sum(e["kind"] == "real" for e in new), sum(e["kind"] == "flip" for e in new)
    print(f"(e) new real {nr}, new upside-down {nf}: {nr - 2.3 * nf:+.1f} (rule <= 5)")
else:
    print("background files missing")
