"""T109: TIC 172900988 b (Kostov et al. 2021, arXiv:2105.08614) through the Petrova 1.0.0 mask and the frozen detector.
Transits (paper section 2): BTJD 1883.37 (over the primary) and 1888.30 (over the secondary), depth about 3000 ppm.
Binary ephemeris (paper section 5): P = 19.658025 d, T0 = 3878.33860 (BJD-2455000) = BTJD 1878.33860. Secondary phase measured
from the paper's Figure 1 eclipse times (1870.57, 1890.23). Eclipse widths: NOT in the paper; measured here from the binary's own
eclipses (the catalogue way), then tested at 0.75x, 1x and 1.5x so the verdict does not rest on one width.
Sectors 44 to 47 hold no forecast transit (paper Table 7: forecasts Aug/Sep 2021 and Feb 2022), so every event there is a
false alarm on a planet host: a negative control. Windows step skipped (best case for QLP, as in the Fable audit k03 test).
Pipeline code is imported read-only. Output data/t109/. Run from pipeline/: .venv python -B this.py"""
import json, os, sys
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1", NUMBA_NUM_THREADS="4")
ROOT = Path(r"D:\second-sun"); sys.path.insert(0, str(ROOT / "pipeline"))
import numpy as np
import detect_v2 as D
import petrova_mask as PM
import stage2_search as S2

K = ROOT / "data" / "known" / "172900988"; OUT = ROOT / "data" / "t109"; OUT.mkdir(exist_ok=True)
P, T0 = 19.658025, 1878.33860
PHS = (((1890.23 - T0) / P) % 1 + ((1870.57 - T0) / P) % 1) / 2
TRANSITS = [1883.37, 1888.30]


def measure_width(t, f, centre):
    """Full width (d) of the eclipse at `centre`: contiguous cadences below baseline - 3 sigma (baseline from 0.6 to 1.5 d away)."""
    near = np.abs(t - centre) < 1.5; base = near & (np.abs(t - centre) > 0.6)
    b = np.nanmedian(f[base]); s = 1.4826 * np.nanmedian(np.abs(f[base] - b))
    low = near & (f < b - 3 * s)
    if low.sum() < 3:
        return np.nan
    tt = t[low]; i0 = np.argmin(np.abs(tt - centre))
    lo = hi = i0; cad = np.median(np.diff(t))
    while lo > 0 and tt[lo] - tt[lo - 1] < 3 * cad: lo -= 1
    while hi < len(tt) - 1 and tt[hi + 1] - tt[hi] < 3 * cad: hi += 1
    return float(tt[hi] - tt[lo] + cad)


files = sorted(K.glob("*.fits"))
def sector_of(p):
    import re
    m = re.search(r"s00(\d\d)", p.name); return int(m.group(1))
def product_of(p):
    return "QLP" if "qlp" in p.name else ("TESS-SPOC" if "tess-spoc" in p.name else "SPOC")

q21 = [p for p in files if sector_of(p) == 21 and product_of(p) == "QLP"][0]
t, f = D.load(str(q21))[:2]
wp = measure_width(t, f, T0); ws = measure_width(t, f, 1890.23)
print(f"measured widths from S21 QLP: primary {wp*24:.2f} h, secondary {ws*24:.2f} h; secondary phase {PHS:.4f}")

rows = []
for scale in (0.75, 1.0, 1.5, None):          # None = no catalogue entry (repeat lane only)
    c = None if scale is None else dict(P=P, T0=T0, eT0=np.nan, eP=np.nan, wp=wp * scale, ws=ws * scale, phs=PHS)
    for p in files:
        sec, prod = sector_of(p), product_of(p)
        t, f = D.load(str(p))[:2]
        if len(t) < 50:
            rows.append(dict(scale=scale, sector=sec, product=prod, status="too little data")); continue
        rm = PM.remove(t, f, [P], c)
        tk, fk = t[~rm], f[~rm]
        rec = dict(scale=scale, sector=sec, product=prod, n=len(t), removed=int(rm.sum()))
        for tr in TRANSITS:
            w = np.abs(t - tr) <= 0.2
            if w.any():
                rec[f"in_window_{tr}"] = int(w.sum()); rec[f"removed_share_{tr}"] = round(float(rm[w].mean()), 3)
        evs = {}
        for sign, arm in ((1, "real"), (-1, "flip")):
            try:
                pr = S2.Prod(tk, fk, sign)
                ev = pr.events(7.0)
            except Exception as exc:
                ev = []; rec[f"err_{arm}"] = type(exc).__name__
            evs[arm] = ev
            rec[f"n_{arm}"] = len(ev)
            if sign == 1:
                for tr in TRANSITS:
                    hit = [e for e in ev if abs(e["center"] - tr) <= 0.3]
                    rec[f"hit_{tr}"] = (round(max(e["snr"] for e in hit), 1), hit[0]["dur_h"]) if hit else None
                    rec[f"snr_at_{tr}"] = round(pr.snr_near_any(tr), 1) if np.any(np.abs(tk - tr) < 0.3) else None
        rec["events"] = {a: [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1), round(e["depth_ppm"])) for e in v] for a, v in evs.items()}
        rows.append(rec)

(OUT / "tic172900988.json").write_text(json.dumps(rows, indent=1, default=str), encoding="utf-8")
for r in rows:
    if r.get("status"):
        print(r); continue
    s = r["scale"]
    line = f"scale {s} S{r['sector']} {r['product']:9s} n {r['n']} removed {r['removed']} real {r['n_real']} flip {r['n_flip']}"
    if r["sector"] == 21:
        line += " | " + " ; ".join(f"{tr}: removed {r.get('removed_share_'+str(tr))} hit {r.get('hit_'+str(tr))} snr_here {r.get('snr_at_'+str(tr))}" for tr in TRANSITS)
    print(line)
    if r["sector"] == 21:
        print("    real events", r["events"]["real"][:8]); print("    flip events", r["events"]["flip"][:8])
