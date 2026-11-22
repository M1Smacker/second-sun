"""RS-042 T1 (Claude, 22 Nov 2026, 11:15 pm): is QLP light from Sector 94 on (TGLC photometry, QLP DRN 004) quieter on OUR stars?
Own data only (Fable X4 rows: per planted-crossing white noise per hour and red factor, 160+ design stars, 2 campaigns).
Era split: QLP sectors < 56, 56 to 93, 94+. Control for era effects (the spacecraft and scattered light change over the years):
the same split for SPOC and TESS-SPOC, whose photometry did not change at Sector 94. Matched per 0.5-mag Tmag bin; ratio of
medians, then the median over bins weighted by count. A TGLC gain shows as a QLP 94+ / 56-93 ratio well below the SPOC ratio.
Prediction: QLP ratio about 0.8 at Tmag 11 to 13 (DRN 004: better for 10.5 < T < 13.5), SPOC ratio about 1.0."""
import json, csv, collections, math
import numpy as np
H = "D:/second-sun/data/fable/f2"
tm = {}
for r in csv.DictReader(open("D:/second-sun/targets/host_radii_g2_g3.csv", encoding="utf-8-sig")):
    try: tm[int(r["tic"])] = float(r["tmag"])
    except (ValueError, TypeError): pass
fam = lambda p: "QLP" if p.startswith("QLP") else ("TESS-SPOC" if p.startswith("TESS-SPOC") else "SPOC")
era = lambda s: "<56" if s < 56 else ("56-93" if s < 94 else "94+")
G = collections.defaultdict(list)
for camp in ("g2", "g3"):
    for l in open(f"{H}/x4-{camp}.jsonl", encoding="utf-8"):
        if not l.strip(): continue
        r = json.loads(l); t = tm.get(r["star"])
        if t is None: continue
        for x in r["rows"]:
            if x["snr"] is None or not x["sbin_ppm"] or not x["red"]: continue
            hr = x["sbin_ppm"] * math.sqrt(x["bin_min"] / 60)
            G[(fam(x["prod"]), era(x["sec"]), math.floor(t * 2) / 2)].append((hr, x["red"], r["star"]))
for f in ("QLP", "SPOC", "TESS-SPOC"):
    print(f"\n{f}: rows per era", {e: sum(len(v) for k, v in G.items() if k[0] == f and k[1] == e) for e in ("<56", "56-93", "94+")},
          "stars 94+", len({s for k, v in G.items() if k[0] == f and k[1] == "94+" for _, _, s in v}))
    for a, b in (("94+", "56-93"), ("94+", "<56"), ("56-93", "<56")):
        rw, rr, w = [], [], []
        for tb in sorted({k[2] for k in G if k[0] == f}):
            A, B = G.get((f, a, tb), []), G.get((f, b, tb), [])
            if len(A) >= 8 and len(B) >= 8:
                rw.append(np.median([x[0] for x in A]) / np.median([x[0] for x in B]))
                rr.append(np.median([x[1] for x in A]) / np.median([x[1] for x in B])); w.append(min(len(A), len(B)))
                if f == "QLP" and a == "94+" and b == "56-93":
                    print(f"   T{tb}: white {np.median([x[0] for x in A]):.0f} vs {np.median([x[0] for x in B]):.0f} ppm/h (n {len(A)}, {len(B)}), red {np.median([x[1] for x in A]):.2f} vs {np.median([x[1] for x in B]):.2f}")
        if w:
            print(f"  {a} over {b}: white-noise ratio {np.average(rw, weights=w):.2f}, red-factor ratio {np.average(rr, weights=w):.2f} ({len(w)} Tmag bins)")
