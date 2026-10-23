"""Data-path self-checks for detect_v2 (deep review 2026-10-23, bugs B1, B2, B5).
Each check hides a known dip or reads a real file through the REAL code path and fails loudly if the path is blind.
Run: .venv\\Scripts\\python.exe pipeline\\test_detect_v2_paths.py   (the B2/B5 checks skip if the local files are missing)."""
import glob, pathlib
import numpy as np
from detect_v2 import find_events, load

DATA = pathlib.Path(r"D:\second-sun\data")
SCRATCH = pathlib.Path(r"D:\second-sun\.cache\tests")      # never C:


def dip_found(cad_min, rng):
    """8 h, 1,500 ppm dip, same noise per unit time at every cadence: SNR about 23 at any spacing."""
    t = np.arange(0, 27, cad_min / 1440)
    f = 1 + rng.normal(0, 1000e-6 * np.sqrt(2 / cad_min), t.size)
    f[np.abs(t - 13.3) < 4 / 24] -= 1500e-6
    ev = find_events(t, f)
    return bool(ev) and abs(ev[0]["center"] - 13.3) < 0.15 and ev[0]["snr"] > 12, ev[:1]


def test_cadences():
    """B1: 30-minute TESS FFIs (S1-26) and 29.4-minute Kepler long cadence used to give NO events."""
    rng = np.random.default_rng(1)
    for cad in (2, 200 / 60, 10, 29.4, 30):
        ok, ev = dip_found(cad, rng)
        assert ok, f"{cad} min cadence: dip not recovered {ev}"
    t = np.arange(0, 27, 30 / 1440)
    f = 1 + np.random.default_rng(2).normal(0, 1000e-6 * np.sqrt(2 / 30), t.size)
    assert find_events(t, f) == [], "30-min white noise should give no event at SNR 7"


def test_qlp_pre56_column():
    """B2: before sector 56 QLP has no sys_rm_flux; the detrended kspsap_flux eats long dips, so use sap_flux."""
    p = glob.glob(str(DATA / "**" / "hlsp_qlp*s0054*.fits"), recursive=True)
    if not p:
        print("  skip B2: no pre-56 QLP file on disk"); return
    t, f, _, info = load(p[0], info=True)
    assert info["column"] == "sap_flux" and info["product"] == "QLP" and info["sector"] == 54, info
    assert info["needs_windows"], info
    post = glob.glob(str(DATA / "**" / "hlsp_qlp*s0098*.fits"), recursive=True)
    if post:
        assert load(post[0], info=True)[3]["column"] == "sys_rm_flux"


def test_spoc_all_nan_pdcsap():
    """B5: a SPOC file whose PDCSAP is entirely NaN used to return zero cadences; now it falls back to SAP."""
    from astropy.io import fits
    src = glob.glob(str(DATA / "overnight" / "**" / "*s0082-0000000299096355*_lc.fits"), recursive=True)
    if not src:
        print("  skip B5: Kepler-16 S82 SPOC file not on disk"); return
    SCRATCH.mkdir(parents=True, exist_ok=True)
    dst = SCRATCH / "pdcsap_all_nan.fits"
    with fits.open(src[0]) as h:
        h[1].data["PDCSAP_FLUX"][:] = np.nan
        h.writeto(dst, overwrite=True)
    t, f, _, info = load(dst, info=True)
    assert len(t) > 1000 and info["column"] == "sap_flux" and info["product"] == "SPOC", (len(t), info)
    t0, f0, _ = load(src[0])
    assert info["column"] != load(src[0], info=True)[3]["column"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("pass:", name)
