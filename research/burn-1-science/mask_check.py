"""Burn 1: are the S30 / S62 published transits removed by our HARD quality mask, or absent from PDCSAP entirely?"""
import numpy as np, lightkurve as lk, pathlib
DL = pathlib.Path(r"D:\second-sun\data\burn-1\lk")
for s, tp in ((30, 2142.3991), (62, 2989.6356)):
    r = lk.search_lightcurve("TIC 260128333", author="SPOC", exptime=120, sector=s)[0]
    for bm in ("hard", "default", "none"):
        lc = r.download(download_dir=str(DL), quality_bitmask=bm)
        t = lc.time.value; w = np.abs(t - tp) < 0.2
        fin = np.isfinite(lc.flux.value)
        print(f"S{s} {bm:8s}: cadences within 0.2 d of {tp}: {w.sum()}, with finite PDCSAP: {(w & fin).sum()}, "
              f"finite SAP: {(w & np.isfinite(lc.sap_flux.value)).sum()}; sector span {np.nanmin(t):.2f}-{np.nanmax(t):.2f}")
