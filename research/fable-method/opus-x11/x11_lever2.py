"""X11 lever 2 (Opus, 17 Nov 2026): which stored hold flags sit on the planted-arm event of T156 single dips that
B finds at tier 1 and B+c1a does not (and the reverse). Reads Codex 027 and 003 saved files only."""
import json, glob, math
from collections import Counter
A = "D:/second-sun/data/astra"
FL = ["step", "ramp", "gap_dump", "repeater", "dominated", "ecl_overlap", "c5", "flipmatch", "burst"]
draw, folder = {}, {}
for p in glob.glob(f"{A}/003/workers/*/results-*.jsonl"):
    for l in open(p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); draw[r["campaign"], r["trial"]] = r; folder[r["campaign"], r["trial"]] = p.rsplit("/", 1)[0].rsplit("\\", 1)[0]
def rows(name):
    out = {}
    for c in ("g2", "g3"):
        for r in json.load(open(f"{A}/027/{name}T156-{c}-V0.json"))["rows"]: out[c, r["trial"]] = r
    return out
base, c1a = rows("baseline-"), rows("")
assert base.keys() == c1a.keys() and len(base) == 2000
def events(path_glob):
    ev = []
    for p in glob.glob(path_glob):
        ev += json.load(open(p, encoding="utf-8"))["events"]
    return ev
def matched(ev, d):
    t, half = d["time"], d["duration_h"] / 48
    m = [e for e in ev if e["kind"] == "real" and e["product"] == d["product"] and e["sector"] == d["sector"]
         and e["snr"] >= 7 and abs(e["center"] - t) <= half]
    return max(m, key=lambda e: e["snr"]) if m else None
def describe(e):
    if e is None: return "no SNR7 event"
    on = [f for f in FL if e.get(f)]
    if "momentum dump" in str(e.get("flags")): on.append("dump-text")
    if "gap edge" in str(e.get("flags")): on.append("gap-edge-text")
    return "+".join(sorted(set(on))) or f"no stored hold (tier {e.get('tier')})"
res = {"lost": Counter(), "gained": Counter()}; single = {"lost": Counter(), "gained": Counter()}; n = Counter()
for k in sorted(base):
    b, c = base[k]["real"][0], c1a[k]["real"][0]
    if b == c: continue
    kind = "lost" if b else "gained"; d = draw[k]
    ev_c = events(f"{A}/027/generated-{k[0]}/T156/trial-{k[1]}/1/groups*/*.json")
    ev_b = events(f"{folder[k]}/trial-{k[1]}-1/groups*/*.json")
    who = ev_c if kind == "lost" else ev_b      # the run that does NOT reach tier 1: what holds it there
    e = matched(who, d); res[kind][describe(e)] += 1; n[kind] += 1
    if e is not None:
        for f in FL + ["dump-text"]:
            if (f == "dump-text" and "momentum dump" in str(e.get("flags"))) or (f != "dump-text" and e.get(f)): single[kind][f] += 1
    n[kind, "dur"] = n[kind, "dur"]
for kind in ("lost", "gained"):
    print(f"\n== {kind} at tier 1 with c1a: {n[kind]} trials. Holding run = {'c1a' if kind == 'lost' else 'B'}")
    for f, v in single[kind].most_common(): print(f"  flag {f:12s} {v:4d}  {100 * v / n[kind]:5.1f}%")
    print("  combinations:")
    for f, v in res[kind].most_common(12): print(f"   {v:4d}  {f}")
# c1a new upside-down candidates: share of each flag (027 saved candidates list, if present)
for c in ("g2", "g3"):
    d = json.load(open(f"{A}/027/planets-{c}-V0.json"))
    if c == "g2": print("\nplanets file keys:", list(d.keys()), "candidates type:", type(d.get("candidates")).__name__, (len(d["candidates"]) if d.get("candidates") is not None else None))

# mechanism: for lost trials held by flipmatch, the flip-arm events in the SAME c1a run (sign 1) near the dip
import numpy as np
offs, ratios, nflip = [], [], []
for k in sorted(base):
    if not (base[k]["real"][0] and not c1a[k]["real"][0]): continue
    d = draw[k]; ev = events(f"{A}/027/generated-{k[0]}/T156/trial-{k[1]}/1/groups*/*.json")
    e = matched(ev, d)
    if e is None or not e.get("flipmatch"): continue
    fl = [f for f in ev if f["kind"] == "flip" and f["product"] == e["product"] and abs(f["center"] - e["center"]) < 1.0]
    nflip.append(len(fl))
    if fl:
        f = min(fl, key=lambda f: abs(f["center"] - e["center"]))
        offs.append(24 * (f["center"] - e["center"]) / e["dur_h"]); ratios.append(f["depth_ppm"] / e["depth_ppm"])
offs, ratios = np.array(offs), np.array(ratios)
print(f"\nflipmatch-held lost dips: {len(nflip)}; with a flip event within 1 d: {len(offs)}")
print("offset of nearest flip event, in units of the dip length: quantiles 10/50/90 of |off|", np.quantile(abs(offs), [.1, .5, .9]).round(2))
print("depth of that flip event / dip depth: quantiles 10/50/90", np.quantile(ratios, [.1, .5, .9]).round(2))
print("flip SNR not stored here; flip events per held dip, median", np.median(nflip))
