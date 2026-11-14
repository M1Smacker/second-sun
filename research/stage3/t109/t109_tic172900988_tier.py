"""T109: TIC 172900988 b sector 21, full Petrova 1.0.0 event chain replicated step by step from stage2_search.do_group and
stage3.add_step / do_group3 / stage3_core.enrich_group (frozen code imported, not edited): Petrova catalogue mask (entry built from
Kostov et al. 2021, widths measured from the binary's own eclipses), real and upside-down detection, veto flags (gap edge, momentum
dump: dump times from a sector-21 SPOC file of another star, the dumps are spacecraft-wide), second product SNR (c8), step lifts,
ramp distance, dominance, then tier_of. Not replicated: QLP borrowed windows (no neighbour table for this star: best case), burst /
common (needs other stars: 0 assumed), the cross-sector p1 veto (needs other sectors with events at the same phase: none here),
apply_v7 merge with SAP twins (no SAP twin run). Output data/t109/. Run from pipeline/."""
import json, os, sys
from pathlib import Path
os.environ.update(SS_SET="g2", VESPER_OPTS="c6,p1", NUMBA_NUM_THREADS="4")
ROOT = Path(r"D:\second-sun"); sys.path.insert(0, str(ROOT / "pipeline"))
import numpy as np
import lightkurve as lk
import detect_v2 as D
import petrova_mask as PM
import stage2_search as S2
import stage3_core as C

K = ROOT / "data" / "known" / "172900988"; OUT = ROOT / "data" / "t109"
P, T0 = 19.658025, 1878.33860
PHS = (((1890.23 - T0) / P) % 1 + ((1870.57 - T0) / P) % 1) / 2
TRANSITS = [1883.37, 1888.30]
saved = json.loads((OUT / "tic172900988.json").read_text(encoding="utf-8"))
SPOC21 = ROOT / "data" / "g2" / "8200343" / "tess2020020091053-s0021-0000000008200343-0167-s_lc.fits"
lc = lk.read(str(SPOC21), quality_bitmask="none"); tq = lc.time.value; q = np.asarray(lc.quality.value, int)
dumps = tq[(q & 32) > 0]; dumps = dumps[np.isfinite(dumps)]
print("sector-21 momentum dumps (BTJD):", np.round(dumps, 2))


class Eph:  # the transits sit days from any eclipse: c5 / overlap measured directly from the catalogue entry
    def __init__(self, c): self.c = c
    def dist(self, tic, t):
        d = []
        for off in (0.0, self.c["phs"]):
            n = np.round((t - T0) / P - off); d.append(abs(t - (T0 + (n + off) * P)))
        return min(d)
    def overlap(self, tic, t, dur_h):
        return bool(PM.windows(np.array([t - dur_h / 48, t, t + dur_h / 48]), self.c)[0].any())


def measure_width(t, f, centre):
    near = np.abs(t - centre) < 1.5; base = near & (np.abs(t - centre) > 0.6)
    b = np.nanmedian(f[base]); s = 1.4826 * np.nanmedian(np.abs(f[base] - b))
    low = near & (f < b - 3 * s); tt = t[low]; i0 = np.argmin(np.abs(tt - centre)); lo = hi = i0; cad = np.median(np.diff(t))
    while lo > 0 and tt[lo] - tt[lo - 1] < 3 * cad: lo -= 1
    while hi < len(tt) - 1 and tt[hi + 1] - tt[hi] < 3 * cad: hi += 1
    return float(tt[hi] - tt[lo] + cad)


files = {"QLP": next(K.glob("hlsp_qlp*s0021*.fits")), "TESS-SPOC": next(K.glob("hlsp_tess-spoc*s0021*.fits"))}
tq0, fq0 = D.load(str(files["QLP"]))[:2]
c = dict(P=P, T0=T0, eT0=np.nan, eP=np.nan, wp=measure_width(tq0, fq0, T0), ws=measure_width(tq0, fq0, 1890.23), phs=PHS)
eph = Eph(c)
prods = {}
for name, path in files.items():
    t, f = D.load(str(path))[:2]
    dt = np.diff(t); edges = np.concatenate([t[:-1][dt > 0.25], t[1:][dt > 0.25], [t.min(), t.max()]])
    rm = PM.remove(t, f, [P], c)
    tk, fk = t[~rm], f[~rm]
    prods[name] = dict(t=tk, f=fk, edges=edges, real=S2.Prod(tk, fk), flip=S2.Prod(tk, fk, -1))
events = []
for name, d in prods.items():
    real, flip = d["real"].events(), d["flip"].events()
    kr, _ = D.veto(real, d["edges"], dumps, flip, flip_action="flag")
    kf, _ = D.veto(flip, d["edges"], dumps, [], flip_action="flag")
    for kind, evs in (("real", kr), ("flip", kf)):
        for e in evs:
            c8 = [o[kind].snr_near(e["center"], e["dur_h"]) for n2, o in prods.items() if n2 != name]
            c8 = [x for x in c8 if np.isfinite(x)]
            ev = dict(kind=kind, tic=172900988, sector=21, product=name, center=round(e["center"], 4), dur_h=e["dur_h"], snr=round(e["snr"], 2),
                      depth_ppm=round(e["depth_ppm"]), flags="; ".join(e["flags"]), c8_best=max(c8) if c8 else None, c8_n=len(c8), burst_n=0)
            Pr = d[kind]
            ev.update(C.step_stats(Pr.bt, Pr.bf, Pr.bd, Pr.med, ev["center"], ev["dur_h"], ev["depth_ppm"]))
            before = d["edges"][d["edges"] <= ev["center"]]
            ev["ramp_d"] = float(ev["center"] - before.max()) if len(before) else None
            events.append(ev)
g = dict(events=events)
enriched = C.enrich_group(g, eph, set())
rows = []
for e in enriched:
    tr = next((x for x in TRANSITS if abs(e["center"] - x) <= 0.3), None)
    fired = [k for k in ("gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated") if e.get(k)]
    rows.append(dict(kind=e["kind"], product=e["product"], center=e["center"], transit=tr, dur_h=e["dur_h"], snr=e["snr"], depth=e["depth_ppm"],
                     c8_best=None if e["c8_best"] is None else round(e["c8_best"], 1), ramp_d=None if e["ramp_d"] is None else round(e["ramp_d"], 2),
                     lift_pre=e.get("lift_pre"), lift_post=e.get("lift_post"), cover=(e.get("cover_pre"), e.get("cover_post")), flags=e["flags"], fired=fired, tier=e["tier"]))
(OUT / "tic172900988_tier.json").write_text(json.dumps(dict(widths_h=(c["wp"] * 24, c["ws"] * 24), dumps=dumps.tolist(), rows=rows), indent=1, default=str), encoding="utf-8")
for r in rows:
    print(r)
