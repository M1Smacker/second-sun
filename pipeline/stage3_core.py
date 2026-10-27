"""Stage 3 preparation, pure parts (Phase E1; Compass review 2026-10-27: research/compass-reviews/2026-10-27-phase-e1-plan.md).
No search runs here, no heavy imports. Rule C5 (distance from the catalogue eclipse phases), the second-product state, the QLP-only label and the
tier of an event; plus the settings hash used to freeze a run. Real events never leave D:\\second-sun\\data (git-ignored)."""
import json, hashlib, pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(r"D:\second-sun")
TARGETS = ROOT / "targets" / "g1_targets.csv"
MANIFEST = ROOT / "data" / "g1" / "manifest.csv"
BEST = ROOT / "research" / "audit-2026-10-23" / "best_per_star_sector.csv"
PH_D = 0.35                         # rule C5: same value as stage2_report.py (flag, never delete)
BURST_MIN = 3                       # same-moment events on other stars that make a burst (stage2_report.py)
C8_STRICT, C8_LENIENT = 4.0, 3.0    # second-product SNR: confirmed / weakly confirmed
# v2 (28 Oct, after the first real search): two flags set from physics, never tuned on the events they remove (flag, never delete)
ECL_MTOT, ECL_RFAC = 2.0, 2.0       # eclipse length: total mass 2 Msun (Kepler 3rd law), R1+R2 taken as 2 x the TIC radius; true length known to about 2x
ECL_MAX_FRAC = 0.4                  # an eclipse is never taken as longer than 0.4 of the orbit
REPEAT_N = 3                        # a binary-orbiting planet has P >= about 15 d (binary > 5 d, stability), so at most 2 transits fit in a 27 d sector
TBINS, TLABELS = [0, 11, 12, 14], ["bright<11", "mid11-12", "faint12+"]


class Ephem:
    """Catalogue eclipse ephemeris per star (Villanova: bjd0 in BJD-2400000, period p_bin_d)."""
    def __init__(self, tg):
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
        """True if the event (its middle +- half its length) touches an eclipse whose length comes from physics: T = P/pi * (R1+R2)/a, a from
        Kepler's third law. Stars without a TIC radius are never flagged by this rule (the 0.35 d rule still applies to them)."""
        for t0, P, R in self.by.get(int(tic), []):
            if not np.isfinite(R):
                continue
            T = min(P / np.pi * ECL_RFAC * R / (215.03 * (ECL_MTOT * (P / 365.25) ** 2) ** (1 / 3)), ECL_MAX_FRAC * P)
            ph = ((center - t0) / P) % 1.0
            if min(min(ph, 1 - ph) * P, abs(ph - 0.5) * P) <= T / 2 + dur_h / 48:
                return True
        return False


def qlp_only_tics(manifest=MANIFEST):
    m = pd.read_csv(manifest).drop_duplicates("file")
    a = m.groupby("tic").author.agg(lambda s: set(s))
    return {int(t) for t, s in a.items() if s == {"QLP"}}


def flags_of(e):
    fl = e.get("flags") or ""
    return dict(gap_dump=("gap edge" in fl) or ("momentum dump" in fl), flipmatch="flipped" in fl, burst=(e.get("burst_n") or 0) >= BURST_MIN)


def tier_of(e):
    """2 = flagged (kept, lower priority); 1A second product agrees at SNR >= 4; 1L agrees at 3 to 4; 1B no second product (cannot be confirmed
    by this check, includes every QLP-only star); 3 = a second product exists and disagrees (SNR < 3), kept and labelled. Stage 2's 'survivors'
    are exactly 1A + 1L + 1B."""
    if e["gap_dump"] or e["burst"] or e["flipmatch"] or e["c5"] or e.get("ecl_overlap") or e.get("repeater"):
        return "2"
    if not (e.get("c8_n") or 0) > 0 or e.get("c8_best") is None:
        return "1B"
    b = e["c8_best"]
    return "1A" if b >= C8_STRICT else ("1L" if b >= C8_LENIENT else "3")


def enrich_event(e, ephem, qlp_only, n_same=0, extra=True):
    """The fields Stage 3 adds to every event the Stage 2 search writes. Idempotent. `n_same` = events of the same kind in the same product and
    sector; `extra=False` switches the two v2 flags off (used to reproduce Stage 2's published numbers)."""
    d = ephem.dist(e["tic"], e["center"])
    out = flags_of(e)
    out.update(ph_d=(float(d) if np.isfinite(d) else None), c5=bool(d < PH_D), second_product=(e.get("c8_n") or 0) > 0,
               qlp_only_star=int(e["tic"]) in qlp_only, repeat_n=int(n_same),
               ecl_overlap=bool(extra and ephem.overlap(e["tic"], e["center"], e.get("dur_h") or 0)), repeater=bool(extra and n_same >= REPEAT_N))
    out["tier"] = tier_of({**e, **out})
    return out


def enrich_group(g, ephem, qlp_only, extra=True):
    """Enrich every event of one star-sector group JSON (needs the whole group to count repeats). Returns the list of enriched events."""
    from collections import Counter
    n = Counter((e["kind"], e["product"]) for e in g["events"])
    return [{**e, **enrich_event(e, ephem, qlp_only, n[(e["kind"], e["product"])], extra)} for e in g["events"]]


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
