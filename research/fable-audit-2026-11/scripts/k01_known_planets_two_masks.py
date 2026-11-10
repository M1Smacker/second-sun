"""K-01 (Fable, 10 Nov 2026): the two known TESS circumbinary planets on real light, frozen mask against the repeat-rule mask.
Public, published stars (TOI-1338 = TIC 260128333, binary 14.6 d; TIC 172900988, binary 19.66 d), so event times are printed.
For each star: all files of one product family; per sector the events at SNR 7 (v5 grid) on the real arm with (a) the frozen per-sector mask, (b) the repeat rule over all sectors (no catalogue window).
An event of (b) with no event of (a) within 0.3 d is a dip the frozen mask cut or weakened ("NEW"). Phase is relative to the deepest folded bin (primary eclipse = 0).
No published transit times are hard-coded: compare the NEW events with the discovery papers (Kostov et al. 2020, 2021) as a separate step.
Usage: python k01_known_planets_two_masks.py"""
import sys, glob, warnings
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np
from wotan import flatten
import detect_v2 as D
from d01_mask_v1_prototype import NB, GRID, ev
from d02_mask_v1_catalogue_lane import repeat_mask2, keep_from

STARS = [("TIC 172900988", 19.658, sorted(glob.glob(r"D:\second-sun\data\known\172900988\tess*_lc.fits")) + sorted(glob.glob(r"D:\second-sun\data\known\172900988\hlsp_tess-spoc*s0021*_lc.fits"))),
         ("TOI-1338", 14.608559, sorted(glob.glob(r"D:\second-sun\data\g2\260128333\tess*_lc.fits")))]
for name, P, paths in STARS:
    L = [D.load(p, info=True) for p in paths]
    ts = [x[0] for x in L]; fs = [x[1] for x in L]; secs = [x[3]["sector"] for x in L]
    flats = [flatten(t, f, method="biweight", window_length=2.0) for t, f in zip(ts, fs)]
    ecl, single = repeat_mask2(ts, flats, P)
    t_all = np.concatenate(ts); fl = np.concatenate(flats); ok = np.isfinite(fl)
    k = np.clip((((t_all % P) / P) * NB).astype(int), 0, NB - 1)
    med = np.array([np.median(fl[ok & (k == i)]) if np.any(ok & (k == i)) else np.nan for i in range(NB)])
    ph0 = (np.nanargmin(med) + 0.5) / NB
    print(f"\n===== {name}: P {P} d, {len(paths)} files, sectors {secs}; eclipse bins {int(ecl.sum())}, single-visit bins {int(single.sum())}")
    nf = nn = 0
    for t, f, s in zip(ts, fs, secs):
        k0, _ = D.eclipse_mask_auto(t, f, P); kr = keep_from(t, P, ecl, None)
        e0 = ev(t[k0], f[k0]); e1 = ev(t[kr], f[kr]); nf += len(e0); nn += len(e1)
        for e in e1:
            new = not any(abs(e["center"] - o["center"]) < 0.3 for o in e0)
            cut = 1 - k0[np.abs(t - e["center"]) < e["dur_h"] / 48].mean()
            ph = (((e["center"] % P) / P) - ph0) % 1.0
            print(f"  S{s}: BTJD {e['center']:.2f}  SNR {e['snr']:.1f}  depth {e['depth_ppm']:.0f} ppm  {e['dur_h']} h  binary phase {ph:.3f}  {'NEW (frozen mask removed ' + format(cut, '.0%') + ' of it)' if new else 'also found with the frozen mask'}")
    print(f"  events in all sectors: frozen mask {nf}, repeat rule {nn}")
