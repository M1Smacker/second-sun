"""v6: the SAP twin of a SPOC or TESS-SPOC file (FIX-QUEUE item 15; learnings sections 15 and 16). The v5 search reads PDCSAP flux (gaps filled from SAP). On the known planet
TOI-1338 b that input found 4 of 8 testable transits and plain SAP flux found 7 of 8, because the two fail in different sectors. v6 therefore ALSO searches the SAP flux of the
best product's file and keeps the union. This module is the small, pure-ish part: the SAP loader, the hook that lets the unchanged Stage 2 search read it, and the choice of
which star-sectors get a second pass. stage2_search.py and detect_v2.py are NOT edited: S2.load and S2.prepare are rebound in the worker process, the way C.use_grid rebinds the box lengths.
A path ending in SUFFIX means "this file, read as SAP"; v7 adds SUFFIX_PDC, "this file, read as PDCSAP with nothing filled". Only SPOC and TESS-SPOC files have a twin (QLP flux is already SAP-based before sector 56)."""
import pathlib
import numpy as np
import lightkurve as lk

SUFFIX = "::sap"
SUFFIX_PDC = "::pdc"                # v7: this file, read as PDCSAP exactly as PDC delivered it (nothing filled from SAP)
FAMILY = ("SPOC", "TESS-SPOC")
MODE = {"sap": False, "pdc": False}


def crowd_fix(sap, crowdsap=None):
    """SAP flux with the crowding (contaminating light) removed the way PDCSAP does, then divided by its median. After the normalisation the dip depth is the real one
    (a dip of fraction d in the target shows as d x CROWDSAP in raw SAP). A missing or absurd CROWDSAP counts as 1 (no correction)."""
    sap = np.asarray(sap, float)
    cr = float(crowdsap) if crowdsap is not None and np.isfinite(crowdsap) and crowdsap > 0.05 else 1.0
    f = sap - (1.0 - cr) * np.nanmedian(sap)
    return f / np.nanmedian(f)


def load_sap(path, info=False):
    """Same call signature and return as detect_v2.load: (time, flux, n_filled[, meta]). Hard quality mask, finite SAP cadences only, nothing filled."""
    lc = lk.read(path, quality_bitmask="hard")
    t = lc.time.value
    sap = np.asarray(lc.sap_flux.value, float)
    ok = np.isfinite(t) & np.isfinite(sap)
    t, sap = t[ok], sap[ok]
    f = crowd_fix(sap, lc.meta.get("CROWDSAP"))
    if not info:
        return t, f, 0
    return t, f, 0, dict(product=("TESS-SPOC" if "tess-spoc" in str(path).lower() else "SPOC") + "-SAP", sector=lc.meta.get("SECTOR"), needs_windows=False,
                         cadence_min=round(float(np.median(np.diff(t))) * 1440, 2) if len(t) > 1 else None, column="sap_flux")


def load_pdc(path, info=False):
    """Same call signature and return as detect_v2.load. PDCSAP flux as PDC delivered it: hard quality mask, finite PDCSAP cadences only, nothing filled. detect_v2.load fills the cadences PDC dropped
    from locally scaled SAP, which puts the SAP systematics back into the very curve the v7 check judges SAP-only dips by; this loader leaves those cadences out, so a dip there is 'not measurable'."""
    lc = lk.read(path, quality_bitmask="hard")
    t = lc.time.value
    pdc = np.asarray(lc.pdcsap_flux.value, float)
    ok = np.isfinite(t) & np.isfinite(pdc)
    t, pdc = t[ok], pdc[ok]
    f = pdc / np.nanmedian(pdc)
    if not info:
        return t, f, 0
    return t, f, 0, dict(product=("TESS-SPOC" if "tess-spoc" in str(path).lower() else "SPOC"), sector=lc.meta.get("SECTOR"), needs_windows=False,
                         cadence_min=round(float(np.median(np.diff(t))) * 1440, 2) if len(t) > 1 else None, column="pdcsap_flux")


def install(S2):
    """Make S2.prepare understand paths that end in SUFFIX. Safe to call twice in one process."""
    if getattr(S2, "_sap_twin", False):
        return
    prepare0, load0 = S2.prepare, S2.load

    def load(path, info=False):
        return load_sap(path, info) if MODE["sap"] else load_pdc(path, info) if MODE["pdc"] else load0(path, info)

    def prepare(path):
        p = str(path)
        for suffix, key in ((SUFFIX, "sap"), (SUFFIX_PDC, "pdc")):
            if p.endswith(suffix):
                MODE[key] = True
                try:
                    return prepare0(p[:-len(suffix)])
                finally:
                    MODE[key] = False
        return prepare0(path)

    S2.load, S2.prepare, S2._sap_twin = load, prepare, True


def twin_groups(groups, best_product, family):
    """The second pass. groups = [(tic, sector, [paths])] as S2.groups() returns; best_product = {(tic, sector): product of the best file}; family = {file name: product}.
    A star-sector gets a pass only if its best product is SPOC or TESS-SPOC; inside it every SPOC or TESS-SPOC file is read as SAP (QLP files are left out), so the SAP twins
    can confirm each other the way the PDCSAP products do (rule C8). The paths carry SUFFIX."""
    out = []
    for tic, sec, paths in groups:
        if best_product.get((int(tic), int(sec))) not in FAMILY:
            continue
        tw = [p + SUFFIX for p in paths if family.get(pathlib.Path(p).name) in FAMILY]
        if tw:
            out.append((tic, sec, tw))
    return out
