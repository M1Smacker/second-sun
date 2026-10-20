"""Burn 1, task 3: injection-recovery smoke test of the wave-3 single-event method on TOI-1338 S98.

S98 SPOC 2-min (hard mask), eclipses masked once from the real data (method.eclipse_mask), the real event
(BTJD 4025.30-4025.95) removed. Inject batman single transits (b = 0.4, 6.4 h, TOI-1338 A LD, R* = 1.313 R_sun)
at 8 spread-out out-of-eclipse times for each radius 2-8 R_earth; run method.find_events (1-d biweight).
Recovered = an event centred within 0.25 d of the injected mid-time. Fixed seed.
"""
import json, pathlib, numpy as np, lightkurve as lk, batman
from method import eclipse_mask, find_events

DL = pathlib.Path(r"D:\second-sun\data\wave-3\lk")
lc = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=98)[0] \
    .download(download_dir=str(DL), quality_bitmask="hard").remove_nans().normalize()
t, f = lc.time.value, lc.flux.value
keep, info = eclipse_mask(t, f)
keep &= ~((t > 4025.30) & (t < 4025.95))
t, f = t[keep], f[keep]

u = [2 * np.sqrt(0.17) * 0.478, np.sqrt(0.17) * (1 - 2 * 0.478)]
B, T14 = 0.4, 6.4 / 24
ARS = np.sqrt(1.03 ** 2 - B ** 2) / np.sin(np.pi * T14 / 95.4)  # a/R* giving ~T14 (k ~ 0.03)


def inject(t0, rp):
    p = batman.TransitParams()
    p.t0, p.per, p.rp, p.a, p.inc = t0, 95.4, rp, ARS, np.degrees(np.arccos(B / ARS))
    p.ecc, p.w, p.u, p.limb_dark = 0.0, 90.0, u, "quadratic"
    return f * batman.TransitModel(p, t).light_curve(p)


_tt = np.linspace(4000, 4001, 20001)
_p = batman.TransitParams(); _p.t0, _p.per, _p.rp, _p.a, _p.inc = 4000.5, 95.4, 0.03, ARS, np.degrees(np.arccos(B / ARS))
_p.ecc, _p.w, _p.u, _p.limb_dark = 0.0, 90.0, u, "quadratic"
_m = batman.TransitModel(_p, _tt).light_curve(_p)
_dur = np.ptp(_tt[_m < 1]) * 24
assert abs(_dur - 6.4) < 0.3, f"injected duration {_dur:.2f} h, expected 6.4 h"
print(f"injection check: a/R* = {ARS:.1f}, duration = {_dur:.2f} h")

# candidate mid-times: >=90% of the in-transit 2-min cadences present, >=1 d from data edges
cand = [x for x in np.arange(t.min() + 1, t.max() - 1, 0.05)
        if np.sum(np.abs(t - x) < T14 / 2) >= 0.9 * T14 / (2 / 1440)]
rng = np.random.default_rng(42)
times = np.sort(rng.choice(cand, 8, replace=False))
base_events, mad, _, _ = find_events(t, f)
print(f"{len(cand)} usable mid-times; chosen {np.round(times, 2)}; MAD {mad*1e6:.0f} ppm; "
      f"events with no injection: {[(round(e['center'], 2), round(e['depth_ppm'])) for e in base_events]}")

RSTAR_RE = 1.313 * 109.08
rows = []
for re_ in (2, 3, 4, 5, 6, 7, 8):
    rp = re_ / RSTAR_RE
    rec = []
    for t0 in times:
        ev, _, _, _ = find_events(t, inject(t0, rp))
        hit = [e for e in ev if abs(e["center"] - t0) < 0.25]
        rec.append(bool(hit))
    rows.append(dict(R_earth=re_, depth_ppm=round(rp ** 2 * 1e6), recovered=int(sum(rec)), n=len(rec), per_time=rec))
    print(rows[-1])
out = dict(mad_ppm=mad * 1e6, times=times.tolist(), n_candidates=len(cand), ars=ARS,
           false_events_no_injection=[(e["center"], e["depth_ppm"]) for e in base_events], rows=rows)
pathlib.Path(__file__).with_name("inject_results.json").write_text(json.dumps(out, indent=1, default=float))
