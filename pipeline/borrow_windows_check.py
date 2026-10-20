"""Are SPOC good-time windows instrument-level? Compare TOI-1338's S98 windows with two neighbours on the same
camera/CCD, then run QLP TOI-1338 with BORROWED windows (the case for QLP-only G1 stars)."""
import csv, pathlib, datetime, numpy as np, lightkurve as lk
from astropy.io import fits
from detect_v2 import load, eclipse_mask, find_events, good_windows, in_windows
DL = pathlib.Path(r"D:\second-sun\data\overnight\lk")
OWN = r"D:\second-sun\data\wave-3\lk\mastDownload\TESS\tess2025312202959-s0098-0000000260128333-0298-s\tess2025312202959-s0098-0000000260128333-0298-s_lc.fits"
Q = r"D:\second-sun\data\wave-3\lk\mastDownload\HLSP\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc\hlsp_qlp_tess_ffi_s0098-0000000260128333_tess_v01_llc.fits"
own = good_windows(OWN)
print("TOI-1338 windows:", [(round(a, 2), round(b, 2)) for a, b in own])
borrowed = None
for tic in ("350861689", "260266504", "350933091", "150145337"):
    sr = lk.search_lightcurve(f"TIC {tic}", author="SPOC", exptime=120, sector=98)
    if not len(sr): continue
    lc = sr[0].download(download_dir=str(DL))
    path = lc.meta["FILENAME"]; size = pathlib.Path(path).stat().st_size
    with open(r"D:\second-sun\research\downloads.csv", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow():%Y-%m-%dT%H:%M:%SZ},TIC {tic} S98 SPOC 2-min LC,https://mast.stsci.edu,{size},{path},window-borrowing test (neighbour of TOI-1338),overnight\n")
    h = fits.getheader(path, 0)
    w = good_windows(path)
    diff = max(min(abs(a - a2) + abs(b - b2) for a2, b2 in own) for a, b in w) if len(w) == len(own) else None
    print(f"TIC {tic}: camera {h['CAMERA']} ccd {h['CCD']} windows {[(round(a, 2), round(b, 2)) for a, b in w]} max edge diff {diff if diff is None else round(diff * 24, 2)} h")
    if h["CAMERA"] == 4 and h["CCD"] == 1 and borrowed is None:
        borrowed = (tic, w)
if borrowed:
    t, f, _ = load(Q)
    keep, _ = eclipse_mask(t, f, 14.6084, 4.7, 6.1, 0.454)
    keep &= in_windows(t, borrowed[1])
    ev = find_events(t[keep], f[keep]); fl = find_events(t[keep], 2 - f[keep])
    print(f"QLP TOI-1338 with windows borrowed from TIC {borrowed[0]}: events", [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in ev],
          "| fakes", len(fl), "max", round(max([e["snr"] for e in fl], default=0), 1),
          "| planet found", any(abs(e["center"] - 4025.63) < 0.3 for e in ev))
