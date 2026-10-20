r"""Step A of the smallest circumbinary injection-recovery test (Compass review 2026-10-20, priority 1).

Uses STANLEY's own N-body injector (stanley_cbp.Stanley_Functions.InjectTransits, MIT) so transit TIMES and
DURATIONS follow a real three-body orbit (irregular, as for a circumbinary planet). Injects one planet at a time
into TOI-1338's raw 40-sector SPOC light curve (saved by STANLEY stage 1), and saves, per planet:
  data/stanley/inj/<name>.npz  -> injected flux (float32) + STANLEY's injected transit list (BTJD, duration h)
Run with the STANLEY venv python. Step B (recovery) runs in the main venv: pipeline/recover_cbp.py.

Known simplification in STANLEY's injector (read from its code): every transit gets a central-crossing batman
shape scaled to the N-body duration, with depth (Rp/R_A)^2 / (1 + flux ratio), i.e. crossings of the SMALL star
get the big star's depth. Assumption here: flux ratio fB/fA = 0.01 (an M dwarf next to a ~1.1 M_sun star).
"""
import os, pathlib, numpy as np
if not hasattr(np, "product"):
    np.product = np.prod
from stanley_cbp import Stanley_Functions as AC
# STANLEY's Search_CreateTransitMask defaults to maxCompTime=1 s and InjectTransits never raises it, so a
# 7-year N-body integration silently times out and injects ZERO transits (found 2026-10-20). Raise it here.
_orig_mask = AC.Search_CreateTransitMask
AC.Search_CreateTransitMask = lambda *a, **k: _orig_mask(*a, **{**k, "maxCompTime": 600})

BASE = pathlib.Path(os.environ["STANLEY_WORKDIR"])          # D:\second-sun\data\stanley
DB = BASE / ".." / "stanley_cbp" / "Databases"              # where InjectTransits looks for parameter files
DB.mkdir(parents=True, exist_ok=True)
OUT = BASE / "inj"; OUT.mkdir(exist_ok=True)
TIC = 260128333
D2S, MSUN, RSUN, REARTH = 86400.0, 1.98847e30, 6.957e8, 6.371e6

raw = np.loadtxt(BASE / "LightCurves" / "Raw" / f"{TIC}_raw.csv")
t_s, f = raw[:, 0], raw[:, 1]
bp = dict(l.strip().split(",") for l in open(BASE / "LightCurves" / "Processed" / "ss_toi1338" / f"TIC_{TIC}_ss_toi1338_binaryStartingParams.csv"))
orbit = dict(Pbin=float(bp["Pbin (days)"]) * D2S, e=float(bp["ecc"]), omega=np.radians(float(bp["omega (deg)"])),
             sep=np.radians(float(bp["theta (deg)"])))
stellar = dict(mA=float(bp["mA (mSun)"]) * MSUN, mB=float(bp["mB (mSun)"]) * MSUN, rA=float(bp["RA (RSun)"]) * RSUN,
               rB=float(bp["RB (RSun)"]) * RSUN, met=0.0, frat=0.01)

PLANETS = [(rp, pp) for pp in (130.0, 200.0) for rp in (4.0, 6.0, 8.0)]   # Earth radii, days; away from TOI-1338 b (95 d)
for rp, pp in PLANETS:
    name = f"rp{rp:g}_p{pp:g}"
    (DB / "ss_inj.csv").write_text(f"TIC,ep,omegap,thetap,Pp_days,Rp_rEarth\n{TIC},0.0,0.0,1.0,{pp},{rp}\n")
    ti, fi = AC.InjectTransits(t_s.copy(), f.copy(), str(TIC), "ss_inj", orbit, stellar, "manual_tess",
                               injection_param_file="ss_inj.csv")
    lst = np.atleast_2d(np.loadtxt(BASE / "LightCurves" / "Injections" / "ss_inj" / f"{TIC}_injectedTransitList.txt"))
    tt_btjd = lst[:, 0] + 55000 if lst.size else np.array([])   # STANLEY writes TT/day - 55000; its time is BTJD*86400
    np.savez_compressed(OUT / f"{name}.npz", flux=fi.astype(np.float32), tt=tt_btjd,
                        dur_h=lst[:, 1] if lst.size else np.array([]), rp=rp, pp=pp)
    changed = np.sum(fi != f)
    print(f"{name}: {len(tt_btjd)} transits injected, {changed} cadences changed, "
          f"durations {np.round(lst[:, 1], 1).tolist() if lst.size else []} h", flush=True)
np.save(OUT / "time_btjd.npy", t_s / D2S); np.save(OUT / "flux_orig.npy", f.astype(np.float32))
print("done")
