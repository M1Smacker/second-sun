"""Second Sun single-transit detector, version 2.

Why v2: burn 1 (research/burn-1-science) showed v1 (3 consecutive 30-min bins below 3 MAD, 1-day
biweight) found only planets >= ~7 R_earth and 3 of 6 testable TOI-1338 b transits. Three causes:
  1. a 1-day detrending window eats into 6-hour dips;
  2. a "3 bins below 3 MAD" rule throws away most of a long, shallow dip's signal;
  3. per-sector BLS sometimes mistook a planet transit or the secondary eclipse for the primary.

v2, step by step:
  1. Flux: PDCSAP, with gaps filled from SAP flux scaled to match locally (PDCSAP is sometimes NaN
     where SAP is fine).
  2. Eclipses: masked from a KNOWN binary period. Each sector only re-finds the primary's phase
     (deepest point of the folded light curve), so a planet dip can't be mistaken for an eclipse.
  3. Detrend: wotan biweight with a 2-day window (>= 3x the longest duration we search, 15 h).
  4. Matched filter: bin to 10 min, slide boxes of 3-15 h, and score each box by
     SNR = (median - box mean) / (robust scatter of ALL box means of that length).
     Measuring the scatter from the box means themselves includes correlated ("red") noise,
     which a white-noise formula would ignore.
  5. Events: peaks above the threshold, merged across durations (keep the highest SNR).

The threshold is not assumed: run the same search on the flipped light curve (1 - flux) to count
false alarms (see accept_v2.py).
"""
import numpy as np
import lightkurve as lk
from wotan import flatten

BIN_D = 10 / 1440
DURS_H = (3, 4, 5, 6.5, 8, 10, 12, 15)


def load(path):
    """Quality-masked, normalized time and flux.
    SPOC: PDCSAP, with gaps filled from locally scaled SAP. QLP / other FFI products (no PDCSAP column):
    QLP's sys_rm_flux (keeps long-transit depth; det_flux lost ~70% of a 6 h dip), to be paired with good_windows() from a SPOC file. Raw QLP SAP was tried first and is dominated by
    scattered light (fake bumps up to SNR 38.7 on TOI-1338 S98), see research/overnight-science/report.md §9."""
    lc = lk.read(path, quality_bitmask="hard")
    t = lc.time.value
    cols = {c.lower() for c in lc.columns}
    sap = np.asarray(lc.sap_flux.value, float)
    pdc = np.asarray(lc.pdcsap_flux.value, float) if "pdcsap_flux" in cols else np.full_like(sap, np.nan)
    ok_t = np.isfinite(t)
    t, pdc, sap = t[ok_t], pdc[ok_t], sap[ok_t]
    s = sap / np.nanmedian(sap)
    if not np.isfinite(pdc).any():           # QLP-style file: its detrended flux (lightkurve's lc.flux = raw SAP here)
        col = next((c for c in ("sys_rm_flux", "det_flux", "kspsap_flux") if c in cols), "flux")  # sys_rm keeps long-dip depth; pair with good_windows()
        q = np.asarray(lc[col].value, float)[ok_t]
        q = q / np.nanmedian(q)
        good = np.isfinite(q)
        return t[good], q[good], 0
    f = pdc / np.nanmedian(pdc)
    fill = ~np.isfinite(f) & np.isfinite(s)
    for i in np.where(fill)[0]:
        near = np.isfinite(f) & (np.abs(t - t[i]) < 1.0)
        f[i] = s[i] * (np.median(f[near] / s[near]) if near.sum() > 20 else 1.0)
    good = np.isfinite(f)
    return t[good], f[good], int(fill.sum())


def good_windows(spoc_path, min_gap_d=0.25):
    """Time windows a SPOC 2-min file keeps after the HARD quality mask, as [(start, end), ...].
    QLP keeps stretches that SPOC drops (scattered light recurring each TESS orbit). On TOI-1338 S98,
    restricting QLP to these windows removed every strong fake and recovered the planet at SNR 10.1
    (research/overnight-science/report.md §9c). The windows are instrument-level, so for a QLP-only star
    they should come from a SPOC star on the same sector/camera/CCD (NOT TESTED yet)."""
    ts = lk.read(spoc_path, quality_bitmask="hard").time.value
    ts = ts[np.isfinite(ts)]
    gi = np.where(np.diff(ts) > min_gap_d)[0]
    return list(zip(np.r_[ts[0], ts[gi + 1]], np.r_[ts[gi], ts[-1]]))


def in_windows(t, windows):
    m = np.zeros_like(t, bool)
    for a, b in windows:
        m |= (t >= a) & (t <= b)
    return m


def intersect_windows(window_lists, trim_start_d=0.5):
    """Most conservative good-time windows from several SPOC stars on the same sector/camera/CCD:
    keep only times inside a window for EVERY star, then drop the first trim_start_d of each window
    (scattered light and thermal settling are worst right after a gap). A star whose SPOC data has no
    gaps (seen on TIC 260266504) simply doesn't narrow the result."""
    out = [tuple(w) for w in window_lists[0]]
    for wl in window_lists[1:]:
        nxt = []
        for a, b in out:
            for c, d in wl:
                lo, hi = max(a, c), min(b, d)
                if hi > lo:
                    nxt.append((lo, hi))
        out = nxt
    return [(a + trim_start_d, b) for a, b in out if b - a > trim_start_d]


def eclipse_mask(t, f, P, dur1_h, dur2_h, sec_phase, pad=1.5):
    """True = keep (out of eclipse). Primary phase is re-found per sector at fixed period P."""
    grid = np.linspace(0, P, 2000, endpoint=False)
    w = dur1_h / 24 / 2
    ph = t % P
    score = [np.median(f[np.abs(((ph - g + P / 2) % P) - P / 2) < w]) if
             np.any(np.abs(((ph - g + P / 2) % P) - P / 2) < w) else 9 for g in grid]
    T1 = grid[int(np.argmin(score))]
    d1 = np.abs(((t - T1 + P / 2) % P) - P / 2)
    T2 = T1 + sec_phase * P
    d2 = np.abs(((t - T2 + P / 2) % P) - P / 2)
    keep = (d1 > pad * dur1_h / 24) & (d2 > pad * dur2_h / 24)
    return keep, T1


def eclipse_mask_auto(t, f, P, nbins=600, nsig=4.0, pad=1.5):
    """Eclipse mask for a binary with known period P but unknown eclipse widths (the G1 case).
    Fold at P, take the median flux in nbins phase bins, flag bins more than nsig robust sigmas
    below the median, grow each flagged run by `pad` times its own width on both sides, and mask
    those phases. Returns (keep, flagged_phase_runs). Self-check: compared with the hand-tuned
    TOI-1338 mask in auto_mask_check.py."""
    ph = (t % P) / P
    flat = flatten(t, f, method="biweight", window_length=2.0)   # remove slow drifts first (else they swamp shallow eclipses)
    ok = np.isfinite(flat)
    edges = np.linspace(0, 1, nbins + 1)
    k = np.clip(np.digitize(ph, edges) - 1, 0, nbins - 1)
    med = np.array([np.median(flat[ok & (k == i)]) if np.any(ok & (k == i)) else np.nan for i in range(nbins)])
    m0 = np.nanmedian(med)
    sig = 1.4826 * np.nanmedian(np.abs(med - m0))
    low = np.nan_to_num(med < m0 - nsig * sig)
    runs, i = [], 0
    while i < nbins:                       # contiguous low runs (phase wraps at 1)
        if low[i]:
            j = i
            while j + 1 < nbins and low[j + 1]:
                j += 1
            runs.append([edges[i], edges[j + 1]]); i = j + 1
        else:
            i += 1
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][1] == 1:   # merge a run split by the wrap
        runs[0][0] = runs[-1][0] - 1; runs.pop()
    keep = np.ones_like(t, bool)
    for a, b in runs:
        w = b - a
        lo, hi = a - pad * w, b + pad * w
        for sh in (-1, 0, 1):
            keep &= ~((ph >= lo + sh) & (ph <= hi + sh))
    return keep, runs


def detrend(t, f, window_d=2.0):
    flat = flatten(t, f, method="biweight", window_length=window_d)
    ok = np.isfinite(flat)
    return t[ok], flat[ok]


def bin10(t, f):
    edges = np.arange(t.min(), t.max() + BIN_D, BIN_D)
    k = np.digitize(t, edges) - 1
    n = np.bincount(k, minlength=len(edges))
    s = np.bincount(k, weights=f, minlength=len(edges))
    with np.errstate(invalid="ignore", divide="ignore"):
        bf = s / n
    bt = edges + BIN_D / 2
    cad = np.median(np.diff(t)) if len(t) > 1 else BIN_D
    good = n >= (2 if cad < 5 / 1440 else 1)   # 2-min/200-s data: >=2 points per bin; 10-/30-min FFI: >=1
    bf[~good] = np.nan
    return bt, bf


def box_scores(bt, bf, dur_h, min_cover=0.8):
    """Box mean and SNR at every bin centre for one duration; NaN where coverage < min_cover."""
    w = max(int(round(dur_h * 60 / 10)), 1)
    v = np.isfinite(bf)
    c_n = np.concatenate([[0], np.cumsum(v)])
    c_f = np.concatenate([[0], np.cumsum(np.where(v, bf, 0.0))])
    n = c_n[w:] - c_n[:-w]
    m = (c_f[w:] - c_f[:-w]) / np.maximum(n, 1)
    m[n < min_cover * w] = np.nan
    centre = bt[: len(m)] + (w - 1) * BIN_D / 2
    med = np.nanmedian(bf)
    good = np.isfinite(m)
    if good.sum() < 20:
        return centre, np.full_like(m, np.nan), m
    sig = 1.4826 * np.nanmedian(np.abs(m[good] - np.nanmedian(m[good])))
    return centre, (med - m) / sig, m


def find_events(t, f, thr=7.0, durs_h=DURS_H, window_d=2.0):
    """t, f = out-of-eclipse data. Returns events sorted by SNR (highest first)."""
    tt, ff = detrend(t, f, window_d)
    bt, bf = bin10(tt, ff)
    med = np.nanmedian(bf)
    cands = []
    for d in durs_h:
        c, snr, m = box_scores(bt, bf, d)
        for i in np.where(np.nan_to_num(snr) >= thr)[0]:
            cands.append((snr[i], c[i], d, (med - m[i]) * 1e6))
    cands.sort(reverse=True)
    events = []
    for snr, c, d, depth in cands:  # greedy merge: one event per dip
        if all(abs(c - e["center"]) > 0.5 * max(d, e["dur_h"]) / 24 + 0.1 for e in events):
            events.append(dict(center=c, dur_h=d, snr=snr, depth_ppm=depth))
    return events


# ---------------------------------------------------------------------------------------------
# Systematics veto (overnight task 8, loosened once after testing; see research/overnight-science/report.md §6).
# On TOI-1338, gap-edge and momentum-dump distances did NOT separate real transits from fakes (real ones sat
# 0.09 d from a gap and 0.17 d from a dump; fakes 0.06-0.35 d and 0.16-0.24 d). So:
#   - AUTO-REJECT only events matched within FLIP_D by an event in the flipped light curve (symmetric wiggles);
#   - FLAG (for the human vetting sheet, never auto-reject) events within GAP_D of a data-gap edge or within
#     DUMP_D of a momentum dump (TESS quality bit 32, "Desat").
GAP_D, DUMP_D, FLIP_D = 0.5, 0.25, 0.3
PRE_DUMP_D = 0.5   # rule C7: flag events up to 0.5 d BEFORE a dump (Kepler-16 S54 dry-run event sat 0.41 d before one)


def systematics(path):
    """Gap edges and momentum-dump times for one SPOC light-curve file."""
    lc = lk.read(path, quality_bitmask="none")
    t = lc.time.value
    q = np.asarray(lc.quality.value, int)
    good = lk.read(path, quality_bitmask="hard").time.value
    good = good[np.isfinite(good)]
    dt = np.diff(good)
    edges = np.concatenate([good[:-1][dt > 0.25], good[1:][dt > 0.25], [good.min(), good.max()]])
    dumps = t[(q & 32) > 0]
    return edges, dumps[np.isfinite(dumps)]


def veto(events, edges, dumps, flipped_events):
    """Returns (kept, rejected). Kept events carry a 'flags' list for the vetting sheet."""
    kept, rejected = [], []
    for e in events:
        c = e["center"]
        if any(abs(fe["center"] - c) < FLIP_D for fe in flipped_events):
            rejected.append({**e, "veto": "matched in flipped data"}); continue
        flags = []
        if edges.size and np.min(np.abs(edges - c)) < GAP_D:
            flags.append("near data-gap edge")
        if dumps.size and np.any((dumps - c > -DUMP_D) & (dumps - c < PRE_DUMP_D)):
            flags.append("near momentum dump (C7: pointing jitter before dumps fakes transits)")
        kept.append({**e, "flags": flags})
    return kept, rejected

def _selfcheck():
    rng = np.random.default_rng(1)
    t = np.arange(0, 27, 2 / 1440)
    f = 1 + rng.normal(0, 1000e-6, t.size)
    assert find_events(t, f) == [], "pure white noise should give no event at SNR 7"
    f2 = f.copy()
    f2[np.abs(t - 13.3) < 3 / 24] -= 700e-6  # 6 h, 700 ppm: box noise = 1000/sqrt(5*36) = 75 ppm, SNR ~ 9
    ev = find_events(t, f2)
    assert ev and abs(ev[0]["center"] - 13.3) < 0.1 and 4 <= ev[0]["dur_h"] <= 8, ev[:2]
    print("detect_v2 self-check passed:", {k: round(v, 2) for k, v in ev[0].items()})


if __name__ == "__main__":
    _selfcheck()
