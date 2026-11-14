"""Second key on Codex 014 part 3 (deep-planet bench and the measured-depth cap). Claude, 15 Nov 2026.
Reads only Codex's own result files (deep-g2.json, deep-g3.json) and main's host radius table. Imports none of Codex's code:
the band split, the equal-bin mean, the cap and the guard are written again here, with Jupiter's mean radius taken from
69,911 km / 695,700 km instead of Codex's 0.10045. Also bins the background guard by period bin, product and depth so a
pooled ratio cannot hide a split (auditor rule). Writes deep_key.json beside this file."""
import csv, json, math, pathlib, collections

A = pathlib.Path(r"D:\second-sun-astra\data\astra\014")
HERE = pathlib.Path(__file__).resolve().parent
RJ = 69911 / 695700                                     # Jupiter mean radius in solar radii
BANDS = [(0, 6000), (6000, 15000), (15000, 30000), (30000, math.inf)]

rows, bg = [], []
for c in ("g2", "g3"):
    d = json.loads((A / f"deep-{c}.json").read_text(encoding="utf-8"))
    rows += d["rows"]; bg += d["background"]
radius = {}
with open(r"D:\second-sun\targets\host_radii_g2_g3.csv", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        try:
            v = float(r["radius_rsun"])
        except ValueError:
            continue
        if v > 0 and math.isfinite(v):
            radius[(r["set"], int(r["tic"]))] = v

def cap(R):
    return 1e6 * min(1.0, (2 * RJ / R) ** 2)

out = {"draws": len(rows), "unique_trials": len({r["trial"] for r in rows}),
       "per_bin": dict(sorted(collections.Counter(r["bin"] for r in rows).items())),
       "observable": sum(bool(r["observed"]) for r in rows),
       "planted_over_cap_codex": sum(r["depth_ppm"] > r["maximum_depth_ppm"] for r in rows),
       "planted_over_cap_mine": sum(r["depth_ppm"] > cap(radius[(r["campaign"], int(r["star"]))]) for r in rows
                                    if (r["campaign"], int(r["star"])) in radius),
       "planted_star_without_radius_mine": sum((r["campaign"], int(r["star"])) not in radius for r in rows),
       "bands": []}
for lo, hi in BANDS:
    x = [r for r in rows if lo <= r["depth_ppm"] < hi]
    seen = [r for r in x if r["observed"]]
    band = {"band": f"{lo}-{hi}", "drawn": len(x), "observable": len(seen)}
    for arm in ("real", "flip"):
        caught = [r for r in seen if r[arm][1]]
        per = collections.defaultdict(lambda: [0, 0])
        for r in seen:
            per[r["bin"]][0] += 1; per[r["bin"]][1] += bool(r[arm][1])
        band[arm] = {"recovered": len(caught), "equal_bin_P": round(sum(b / a for a, b in per.values()) / len(per), 4),
                     "lost_to_cap": sum(not r[f"{arm}_guard_survives"] for r in caught),
                     "guarded_full": sum(bool(r[f"{arm}_guard_full"]) for r in seen)}
    out["bands"].append(band)
for arm in ("real", "flip"):
    out[f"{arm}_recovered_total"] = sum(b[arm]["recovered"] for b in out["bands"])
    out[f"{arm}_lost_to_cap_total"] = sum(b[arm]["lost_to_cap"] for b in out["bands"])

B = [r for r in bg if r["options"][1]]
g = {}
for r in B:
    R = radius.get((r["campaign"], int(r["tic"])))
    g[id(r)] = None if R is None else r["depth_ppm"] > cap(R)
bgo = {}
for kind in ("real", "flip"):
    k = [r for r in B if r["kind"] == kind]
    bgo[kind] = {"events": len(k), "held_mine": sum(g[id(r)] is True for r in k), "unknown_mine": sum(g[id(r)] is None for r in k),
                 "held_codex": sum(r["guard"] is True for r in k), "unknown_codex": sum(r["guard"] is None for r in k),
                 "disagree_with_codex": sum(g[id(r)] != r["guard"] for r in k)}
out["background_B"] = bgo

def split(key):
    t = collections.defaultdict(lambda: {"real": [0, 0], "flip": [0, 0]})
    for r in B:
        if g[id(r)] is None:
            continue
        t[key(r)][r["kind"]][0] += 1; t[key(r)][r["kind"]][1] += g[id(r)]
    return {str(k): {a: f"{v[a][1]}/{v[a][0]}" for a in v} for k, v in sorted(t.items(), key=lambda kv: str(kv[0]))}
out["held_by_period_bin"] = split(lambda r: r["bin"])
out["held_by_product"] = split(lambda r: r["product"])
out["held_by_depth"] = split(lambda r: "<6000" if r["depth_ppm"] < 6000 else "6000-15000" if r["depth_ppm"] < 15000 else ">=15000")
(HERE / "deep_key.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
