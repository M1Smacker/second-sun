"""Stage 3 preparation, pure parts (Phase E1; Compass review 2026-10-27: research/compass-reviews/2026-10-27-phase-e1-plan.md).
No search runs here, no heavy imports. Rule C5 (distance from the catalogue eclipse phases), the second-product state, the QLP-only label and the
tier of an event; plus the settings hash used to freeze a run. Real events never leave D:\\second-sun\\data (git-ignored)."""
import json, hashlib, pathlib
import numpy as np, pandas as pd
import dataset as DS
import vopts as V

ROOT = pathlib.Path(r"D:\second-sun")
TARGETS = DS.TARGETS                # dataset.py: G1 by default, G2 when SS_SET=g2 (the same code reads either)
MANIFEST = DS.MANIFEST
BEST = DS.BEST
PH_D = 0.35                         # rule C5: same value as stage2_report.py (flag, never delete)
BURST_MIN = 3                       # same-moment events on other stars that make a burst (stage2_report.py)
C8_STRICT, C8_LENIENT = 4.0, 3.0    # second-product SNR: confirmed / weakly confirmed
# v2 (28 Oct, after the first real search): two flags set from physics, never tuned on the events they remove (flag, never delete)
ECL_MTOT, ECL_RFAC = 2.0, 2.0       # eclipse length: total mass 2 Msun (Kepler 3rd law), R1+R2 taken as 2 x the TIC radius; true length known to about 2x
ECL_MAX_FRAC = 0.4                  # an eclipse is never taken as longer than 0.4 of the orbit
STEP_LIFT, STEP_COVER = 0.5, 0.5    # v3 flat-baseline test: a transit is a box, so the flux just before and after must sit at baseline: a side lifted
                                    # or dropped by more than 0.5 of the dip depth, or a side with under half its data, flags the event
REPEAT_N = 3                        # a binary-orbiting planet has P >= about 15 d (binary > 5 d, stability), so at most 2 transits fit in a 27 d sector
TBINS, TLABELS = [0, 11, 12, 14], ["bright<11", "mid11-12", "faint12+"]


class Ephem:
    """Catalogue eclipse ephemeris per star (Villanova: bjd0 in BJD-2400000, period p_bin_d)."""
    def __init__(self, tg, widths=None):
        self.widths = widths or {}
        self.by = {}
        for q in tg.itertuples():
            self.by.setdefault(int(q.tic), []).append((float(q.bjd0) - 57000.0, float(q.p_bin_d), float(q.tic_radius_rsun)))

    def dist(self, tic, center):
        """Days from `center` to the nearest catalogue primary eclipse or phase 0.5 (circular secondary); inf if the star has no ephemeris."""
        best = np.inf
        for t0, P, _ in self.by.get(int(tic), []):
            ph = ((center - t0) / P) % 1.0
            best = min(best, min(ph, 1 - ph) * P, abs(ph - 0.5) * P)
        return best

    def overlap(self, tic, center, dur_h):
        """True if the event (its middle +- half its length) touches an eclipse. The eclipse length is the catalogue's measured width where the star has one
        (v4), else physics: T = P/pi x (R1+R2)/a with a from Kepler's third law. Stars with neither are never flagged by this rule (the 0.35 d rule still
        applies to them)."""
        w = self.widths.get(int(tic))
        for t0, P, R in self.by.get(int(tic), []):
            if w is not None:
                Tp, Ts = w[0] * P, w[1] * P
            elif np.isfinite(R):
                Tp = Ts = min(P / np.pi * ECL_RFAC * R / (215.03 * (ECL_MTOT * (P / 365.25) ** 2) ** (1 / 3)), ECL_MAX_FRAC * P)
            else:
                continue
            ph = ((center - t0) / P) % 1.0
            if min(ph, 1 - ph) * P <= Tp / 2 + dur_h / 48 or abs(ph - 0.5) * P <= Ts / 2 + dur_h / 48:
                return True
        return False


def qlp_only_tics(manifest=MANIFEST):
    m = pd.read_csv(manifest).drop_duplicates("file")
    a = m.groupby("tic").author.agg(lambda s: set(s))
    return {int(t) for t, s in a.items() if s == {"QLP"}}


def flags_of(e):
    fl = e.get("flags") or ""
    return dict(gap_dump=("gap edge" in fl) or ("momentum dump" in fl), flipmatch="flipped" in fl, burst=(e.get("burst_n") or 0) >= BURST_MIN)


RAMP_D = 1.0                        # v4: an event within 1 day after data resumes (orbit start, gap, sector start) sits in the thermal and scattered light ramp
EBS = ROOT / "data" / "xmatch" / "ebs.csv"
GRID_V4 = (3, 4, 5, 6.5, 8, 10, 12, 15)    # box lengths in hours, Stage 2 to v4 (equal to detect_v2.DURS_H)
GRID_V5 = GRID_V4 + (20,)           # v5: long circumbinary transits were never searched; a 2 d window is 2.4 x 20 h (it still absorbs part of such a dip, learnings section 13)


def use_grid(S2, grid):
    """Make the Stage 2 search code score the given box lengths. stage2_search.py is not edited: its module-level name DURS_H is rebound (Prod.events and
    Prod.snr_near_any read it at call time). Dry runs use GRID_V4 to reproduce Stage 2 exactly; the v5 run uses GRID_V5."""
    S2.DURS_H = tuple(grid)


def eb_widths():
    """{tic: (primary width, secondary width)} in phase units of the Kepler period, from the TESS eclipsing binary catalogue (Prsa et al. 2022; columns
    Wp-pf, Ws-pf) for stars whose TESS period equals the Kepler period within 2%. Empty if the table is not on this machine."""
    if not EBS.exists():
        return {}
    tg = pd.read_csv(TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    eb = pd.read_csv(EBS).drop_duplicates("TIC").set_index("TIC")
    out = {}
    for tic, r in eb.iterrows():
        if tic in tg.index and abs(r.Per / tg.p_bin_d[tic] - 1) < 0.02 and np.isfinite(r["Wp-pf"]) and r["Wp-pf"] > 0:
            out[int(tic)] = (float(r["Wp-pf"]), float(r["Ws-pf"]) if np.isfinite(r["Ws-pf"]) and r["Ws-pf"] > 0 else float(r["Wp-pf"]))
    return out


def window_lift(bt, bf, bd, med, lo, hi, depth_ppm):
    """(mean flux in [lo, hi) minus the median, in units of the dip depth; share of the window that has data). The dip itself is -1 in these units."""
    k = (bt >= lo) & (bt < hi) & np.isfinite(bf)
    return (float((np.mean(bf[k]) - med) / (depth_ppm * 1e-6)) if k.any() and depth_ppm else None), float(k.sum() * bd / (hi - lo))


def step_stats(bt, bf, bd, med, center, dur_h, depth_ppm):
    """Flux just before and after an event, in the same flattened, binned flux the detector scored. Window length = event length, at least 6 h."""
    half, w = dur_h / 48, max(dur_h, 6.0) / 24
    pre = window_lift(bt, bf, bd, med, center - half - w, center - half, depth_ppm)
    post = window_lift(bt, bf, bd, med, center + half, center + half + w, depth_ppm)
    return dict(lift_pre=pre[0], lift_post=post[0], cover_pre=pre[1], cover_post=post[1])


def step_flag(e):
    """True if the event is not a box on a flat baseline (step, ramp, overshoot) or has too little data on a side to tell. False if never measured.
    Study switch c2 (vopts.py): the data-cover rule is dropped and a side with no data is not judged (the gap rule owns gaps)."""
    if "lift_pre" not in e:
        return False
    if "lift2_pre" in e:                                          # switch c1b: the lifts measured on the re-smoothed curve (plus the trend jump across the event) replace the 2 d lifts
        l2 = (e["lift2_pre"], e["lift2_post"])
        if "c2" in V.ON:
            return any(l is not None and abs(l) > STEP_LIFT for l in l2)
        return min(e["cover_pre"], e["cover_post"]) < STEP_COVER or any(l is None or abs(l) > STEP_LIFT for l in l2)
    if "c2" in V.ON:
        return any(l is not None and abs(l) > STEP_LIFT for l in (e["lift_pre"], e["lift_post"]))
    if min(e["cover_pre"], e["cover_post"]) < STEP_COVER:
        return True
    return any(l is None or abs(l) > STEP_LIFT for l in (e["lift_pre"], e["lift_post"]))


C1B_MASK, C1B_WIN, C1B_MIN_D = 0.75, 3.0, 0.5       # study switch c1b: mask half-width and window as multiples of the box length; shortest window in days


def resmooth_stats(t, f, center, dur_h, bin_d):
    """Study switch c1b: the step measurements of one event on a curve smoothed WITHOUT the event. t, f = the prepared curve in the search's orientation (dips are down, so the upside-down copy is already
    flipped). The event (centre +- C1B_MASK x box) is left out of a biweight trend of window C1B_WIN x box (at least C1B_MIN_D days); the trend is interpolated across the gap; the curve is binned as the
    search bins it. Returns (step_stats dict measured on that curve with the depth measured there, depth_ppm) or None when too little data is left."""
    from wotan import flatten
    import detect_v2 as D
    half = C1B_MASK * dur_h / 24
    keep = np.abs(t - center) >= half
    if keep.sum() < 100 or (~keep).sum() < 3:
        return None
    w = max(C1B_WIN * dur_h / 24, C1B_MIN_D)
    _, tr = flatten(t[keep], f[keep], method="biweight", window_length=w, return_trend=True)
    ok = np.isfinite(tr)
    if ok.sum() < 100:
        return None
    trend = np.interp(t, t[keep][ok], tr[ok])
    flat = f / trend
    bt, bf = D.bin10(t, flat, bin_d)
    med = np.nanmedian(bf)
    inside = (np.abs(bt - center) <= dur_h / 48) & np.isfinite(bf)
    if inside.sum() < 2:
        return None
    depth = float((med - np.mean(bf[inside])) * 1e6)
    if not depth > 0:
        return None
    st = step_stats(bt, bf, bin_d, med, center, dur_h, depth)
    # the smoothing follows a real level step, so on the flattened curve both sides look flat; the step lives in the TREND: carry the difference of the trend at the two edges of the mask as an extra lift
    # on each side (half the jump, opposite signs, in units of the depth). A smoothing shoulder leaves the trend alone, so it adds nothing.
    t_pre, t_post = np.interp([center - half, center + half], t[keep][ok], tr[ok])
    if st["lift_post"] is not None:
        st["lift_post"] = float(st["lift_post"] + (t_post - t_pre) / (depth * 1e-6))     # pre side is the reference, as one side sits at the baseline in the original rule
    return st, depth


# v7 (FIX-QUEUE 17, 18, 19): the Stage 2 burst flag counts other stars' UPSIDE-DOWN events at the same moment, whatever the kind of the event it judges, so it removes more of the control than of the
# data when the common-mode events are dips (learnings section 16). The common-moment flag below asks every event, real or upside-down, the same question of the same pool.
COMMON_D, COMMON_N = 0.1, BURST_MIN  # days and number of other stars: the Stage 2 burst values, unchanged
PDC_MIN = C8_LENIENT                # v7: a SAP-only dip must still show at this SNR in the PDCSAP flux of the same file (the systematics-corrected version of the same pixels)


def common_moment_n(E):
    """E = DataFrame of the primary events of a run, BOTH kinds (columns sector, camera, center, tic). Returns an int array: for each row, the number of OTHER stars that have an event of EITHER kind
    within COMMON_D days at the same sector and camera. The pool is the same for an event and its upside-down mirror, so the flag treats data and control identically (a same-kind count would not:
    an episode of dips on many stars flags the control's mirrors but not the real dips, and an episode of bumps does the reverse)."""
    out = np.zeros(len(E), int)
    pos = {ix: n for n, ix in enumerate(E.index)}
    for _, g in E.groupby(["sector", "camera"]):
        c, t = g.center.values, g.tic.values
        for ix, ci, ti in zip(g.index, c, t):
            out[pos[ix]] = len(set(t[np.abs(c - ci) < COMMON_D]) - {ti})
    return out


def tier_of(e):
    """2 = flagged (kept, lower priority); 1A second product agrees at SNR >= 4; 1L agrees at 3 to 4; 1B no second product (cannot be confirmed
    by this check, includes every QLP-only star); 3 = a second product exists and disagrees (SNR < 3), kept and labelled. Stage 2's 'survivors'
    are exactly 1A + 1L + 1B. v7: if the event carries `common` (the common-moment flag) it replaces `burst`; if it carries `pdc_snr` (SAP-only dips) a value under PDC_MIN makes it tier 3."""
    c = e.get("common")
    bad_moment = e["burst"] if c is None or c != c else c
    if e["gap_dump"] or bad_moment or e["flipmatch"] or e["c5"] or e.get("ecl_overlap") or e.get("repeater") or e.get("step") or e.get("ramp") or e.get("dominated"):
        return "2"
    p = e.get("pdc_snr")
    if p is not None and p == p and p < PDC_MIN:
        return "3"
    if not (e.get("c8_n") or 0) > 0 or e.get("c8_best") is None:
        return "1B"
    b = e["c8_best"]
    return "1A" if b >= C8_STRICT else ("1L" if b >= C8_LENIENT else "3")


def enrich_event(e, ephem, qlp_only, n_same=0, extra=True, dominated=False):
    """The fields Stage 3 adds to every event the Stage 2 search writes. Idempotent. `n_same` = events of the same kind in the same product and
    sector; `extra=False` switches the two v2 flags off (used to reproduce Stage 2's published numbers)."""
    d = ephem.dist(e["tic"], e["center"])
    out = flags_of(e)
    out.update(ph_d=(float(d) if np.isfinite(d) else None), c5=bool(d < PH_D), second_product=(e.get("c8_n") or 0) > 0,
               qlp_only_star=int(e["tic"]) in qlp_only, repeat_n=int(n_same),
               ecl_overlap=bool(extra and ephem.overlap(e["tic"], e["center"], e.get("dur_h") or 0)), repeater=bool(extra and n_same >= REPEAT_N), step=bool(extra and step_flag(e)),
               ramp=bool(extra and e.get("ramp_d") is not None and e["ramp_d"] == e["ramp_d"] and e["ramp_d"] < RAMP_D), dominated=bool(extra and dominated))
    out["tier"] = tier_of({**e, **out})
    return out


def enrich_group(g, ephem, qlp_only, extra=True):
    """Enrich every event of one star-sector group JSON (needs the whole group to count repeats). Returns the list of enriched events."""
    from collections import Counter
    n = Counter((e["kind"], e["product"]) for e in g["events"])
    mx = {}
    for e in g["events"]:
        mx[(e["product"], e["kind"])] = max(mx.get((e["product"], e["kind"]), 0.0), e.get("snr") or 0.0)
    # v4 local false alarm calibration: an event is dominated if the strongest event of the OTHER kind (real vs upside-down) in the same light curve is at
    # least as strong. Symmetric, no setting: under noise alone real and upside-down dominate each other equally often.
    return [{**e, **enrich_event(e, ephem, qlp_only, n[(e["kind"], e["product"])], extra,
                                 e.get("snr") is not None and mx.get((e["product"], "flip" if e["kind"] == "real" else "real"), 0.0) >= e["snr"])} for e in g["events"]]


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def settings_hash(s):
    return hashlib.sha256(json.dumps(s, sort_keys=True, default=str).encode()).hexdigest()


def class_sizes():
    """Star-sectors per brightness class of the whole campaign, derived from the data (Stage 2's report hard-coded 801, 1067 and 3196)."""
    best = pd.read_csv(BEST, usecols=["tic", "sector"]).drop_duplicates()
    tg = pd.read_csv(TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    tb = pd.cut(best.tic.map(tg.tmag), TBINS, right=False, labels=TLABELS)
    return {k: int(v) for k, v in tb.value_counts().items()}, len(best), int(tb.isna().sum())


def c5_timeline_cover(tg=None):
    """Share of each star's orbit inside the C5 windows (0.35 d either side of the primary and of phase 0.5): min(1, 4 x 0.35 / P)."""
    tg = pd.read_csv(TARGETS, comment="#") if tg is None else tg
    return (4 * PH_D / tg.p_bin_d).clip(upper=1).groupby(tg.tic).max()
