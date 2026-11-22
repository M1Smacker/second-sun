"""RS-040 A12 summary (Claude, 22 Nov 2026, written while the run was going, before reading any a12 row).
For each statistic: untouched alarms per arm at each threshold (summed over star-sectors); the equal-alarm threshold = lowest threshold
whose alarms on BOTH arms are at most frozen-at-7's; at that threshold the share of planted crossings detected (SNR >= thr) and
'clean' (also no upside-down box-overlap event >= thr, which the mirror rule would hold). Whole-star bootstrap (seed 2026112241,
2,000 draws) of each statistic's clean share minus the notch's. Prints only counts and shares."""
import json, collections
import numpy as np
H = "D:/second-sun/data/rs039"
THR = ("4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "9", "10", "12")
ST = ("frozen", "notch", "w3", "w3notch")
rows, alarms, days = [], {s: {a: collections.Counter() for a in "ru"} for s in ST}, 0.0
for c in ("g2", "g3"):
    for l in open(f"{H}/a12-{c}.jsonl", encoding="utf-8"):
        if not l.strip(): continue
        r = json.loads(l)
        for x in r["rows"]: rows.append(dict(x, star=(c, r["star"])))
        for b in r["bg"]:
            days += b["days"]
            for s in ST:
                for a in "ru": alarms[s][a].update(b[f"{s}_{a}"])
print(f"crossing rows {len(rows)}, stars {len({x['star'] for x in rows})}, untouched days {days:.0f}")
for s in ST: print(s, "alarms real/upside-down:", " ".join(f"{t}:{alarms[s]['r'][t]}/{alarms[s]['u'][t]}" for t in THR))
ref = (alarms["frozen"]["r"]["7"], alarms["frozen"]["u"]["7"])
pick = {}
for s in ST:
    ok = [t for t in THR if alarms[s]["r"][t] <= ref[0] and alarms[s]["u"][t] <= ref[1]]
    pick[s] = ok[0] if ok else None
def share(sel, s, t, clean):
    hit = [(x[s] is not None and x[s] >= float(t)) and (not clean or x[s + "_mirror_box"] is None or x[s + "_mirror_box"] < float(t)) for x in sel]
    return np.mean(hit) if sel else np.nan
for s in ST:
    t = pick[s]
    if t is None: print(s, "no threshold meets the alarm limit"); continue
    print(f"{s}: equal-alarm threshold {t} (alarms {alarms[s]['r'][t]}/{alarms[s]['u'][t]} vs frozen@7 {ref[0]}/{ref[1]}): "
          f"detected {100*share(rows, s, t, False):.1f}%, clean {100*share(rows, s, t, True):.1f}%")
by = collections.defaultdict(list)
for x in rows: by[x["star"]].append(x)
stars = list(by); rng = np.random.default_rng(2026112241)
if pick["notch"]:
    for s in ("frozen", "w3", "w3notch"):
        if not pick[s]: continue
        d = []
        for _ in range(2000):
            sel = [x for j in rng.integers(0, len(stars), len(stars)) for x in by[stars[j]]]
            d.append(100 * (share(sel, s, pick[s], True) - share(sel, "notch", pick["notch"], True)))
        print(f"{s} minus notch, clean, at equal alarms: {np.mean(d):+.1f} (95% {np.quantile(d,.025):+.1f} to {np.quantile(d,.975):+.1f})")
