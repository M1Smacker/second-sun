"""RS-040 A13 summary (Claude, 22 Nov 2026, written before any A13 result). Best product per crossing, ALL crossings (unscored = missed).
Reference alarms frozen-at-7 from A12 (1171 / 784, same light). notchF threshold = lowest with alarms at most that on both arms.
Paired against the notch at 5 (A12 rows, same crossings). Whole-star bootstrap seed 2026112242, 2,000 draws.
Lead for D2 if notchF minus notch >= +2.0 with the 95% interval above zero."""
import json, collections
import numpy as np
H = "D:/second-sun/data/rs039"
THR = ("4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "9", "10", "12")
def load(prefix, stats):
    best = collections.defaultdict(lambda: {s: -99.0 for s in stats}); star = {}; al = {s: {a: collections.Counter() for a in "ru"} for s in stats}
    for c in ("g2", "g3"):
        for l in open(f"{H}/{prefix}-{c}.jsonl", encoding="utf-8"):
            if not l.strip(): continue
            r = json.loads(l)
            for x in r["rows"]:
                k = (c, x["trial"], round(x["c"], 3)); star[k] = (c, r["star"])
                for s in stats:
                    if x.get(s) is not None and x[s] > best[k][s]: best[k][s] = x[s]
            for b in r["bg"]:
                for s in stats:
                    for a in "ru": al[s][a].update(b[f"{s}_{a}"])
    return best, star, al
b12, star, al12 = load("a12", ("frozen", "notch"))
b13, _, al13 = load("a13", ("notchF",))
ref = (al12["frozen"]["r"]["7"], al12["frozen"]["u"]["7"])
print("notchF alarms real/upside-down:", " ".join(f"{t}:{al13['notchF']['r'][t]}/{al13['notchF']['u'][t]}" for t in THR))
ok = [t for t in THR if al13["notchF"]["r"][t] <= ref[0] and al13["notchF"]["u"][t] <= ref[1]]
t = ok[0] if ok else None
K = [k for k in b12 if k in b13]
print(f"crossings paired {len(K)} (A12 {len(b12)}, A13 {len(b13)}); frozen@7 alarms {ref}; notchF equal-alarm threshold {t}"
      + (f" (alarms {al13['notchF']['r'][t]}/{al13['notchF']['u'][t]})" if t else ""))
if t:
    det = lambda KK, s, th, B: np.mean([B[k][s] >= th for k in KK])
    print(f"frozen@7 {100*det(K,'frozen',7,b12):.1f}  notch@5 {100*det(K,'notch',5,b12):.1f}  notchF@{t} {100*det(K,'notchF',float(t),b13):.1f}")
    by = collections.defaultdict(list)
    for k in K: by[star[k]].append(k)
    S = list(by); rng = np.random.default_rng(2026112242); d = []
    for _ in range(2000):
        KK = [k for j in rng.integers(0, len(S), len(S)) for k in by[S[j]]]
        d.append(100 * (det(KK, "notchF", float(t), b13) - det(KK, "notch", 5, b12)))
    print(f"notchF minus notch: {np.mean(d):+.1f} (95% {np.quantile(d,.025):+.1f} to {np.quantile(d,.975):+.1f}); lead for D2: {np.mean(d) >= 2 and np.quantile(d,.025) > 0}")
