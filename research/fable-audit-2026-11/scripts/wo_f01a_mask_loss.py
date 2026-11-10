"""WO-F01 Part A (10 Nov 2026, Sonnet 5.5 Extra): how much of a real dip does the frozen 0.8.1 chain delete in eclipse_mask_auto, per binary-period bin, depth, duration and product family,
for G2 and G3. NOTHING in pipeline/ is edited: prepare() is copied here with an inject hook between the windows and the mask (the frozen order is windows -> mask_runs).
For each sampled FILE (one product of one star-sector): pick a time in light the baseline mask KEEPS (>= 1.5 d from the ends, 20 h window >= 90% covered, no baseline event within 1 d on either arm),
inject a trapezoid (20% ingress/egress, as chain_recovery.signal) of K x the 8 h noise (noise measured AFTER the baseline mask, as audit_paths.noise) either
 (before) into the windowed raw light, then mask_runs (what a real planet does), or
 (after)  into the already masked light (what every earlier recovery test did).
'found' = a Prod.events() event (SNR >= 7, v5 box grid) within 0.5*max(dur, event dur)/24 + 0.1 d of the injection, on the real arm for a dip and on the upside-down arm for a bump.
m = found_before / found_after. Bumps are the proof test: m must be ~1 in every bin.
Usage (SS_SET must be set in the environment, g2 or g3):
  python wo_f01a_mask_loss.py check            zero-injection identity vs the stored sealed / G3 group JSON (20 star-sectors)
  python wo_f01a_mask_loss.py run N_PER PROCS  sample N_PER files per (period bin, product family), resume-safe; rows -> data\\fable_audit_mask\\rows_<set>.pkl (private)
  python wo_f01a_mask_loss.py summary          counts table -> stdout (the caller saves it under evidence/)"""
import os
os.environ.setdefault("NUMBA_NUM_THREADS", "1"); os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("PYTHONUTF8", "1")
import sys, json, glob, pathlib, time, warnings, multiprocessing as mp
sys.path.insert(0, r"D:\second-sun\pipeline")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import dataset as DS
import stage2_search as S2
import stage3_core as C
import audit_all as A
from audit_paths import noise

SET = DS.NAME
assert SET in ("g2", "g3"), "set SS_SET=g2 or g3"
RUNDIR = {"g2": DS.RUNS / "sealed_5f73692944aa", "g3": DS.RUNS / "g3_e7886a71a61f"}[SET]
OUT = pathlib.Path(r"D:\second-sun\data\fable_audit_mask"); OUT.mkdir(parents=True, exist_ok=True)
ROWS = OUT / f"rows_{SET}.pkl"
BINS = ((5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e4))
DURS = (4.0, 8.0, 14.0, 20.0)
KS = (8.0, 12.0, 18.0, 25.0)
BUMPS = ((8.0, 12.0), (8.0, 25.0))          # (dur, K) of the bump proof test


def signal(t, tc, dur_h, depth_ppm, sign):
    """Same trapezoid as chain_recovery.signal. sign +1 = dip in the flux, -1 = bump (a dip in the upside-down copy)."""
    return -sign * depth_ppm * 1e-6 * np.clip((dur_h / 2 - np.abs(t - tc) * 24) / (0.2 * dur_h), 0, 1)


def init():
    S2._init(); C.use_grid(S2, C.GRID_V5)


def load_windowed(path):
    """Copy of stage2_search.prepare lines 144 to 161 (load, QLP windows, minimum length). Returns ((t, f) or None, meta, status)."""
    path = pathlib.Path(path); tic = A.tic_of(path.name)
    t, f, nfill, info = S2.load(str(path), info=True)
    sec, cam, ccd = A.head(path)
    meta = dict(tic=tic, file=path.name, product=info["product"], sector=sec)
    if info["needs_windows"]:
        nbw, nn = A.neighbour_windows(sec, cam, ccd, tic)
        own = next((p for p in path.parent.glob(f"tess*-s{sec:04d}-{tic:016d}-*_lc.fits")), None)
        if own is not None:
            k = S2.in_windows(t, S2.good_windows(str(own)))
        elif nn >= 2:
            k = S2.in_windows(t, nbw)
        else:
            return None, meta, "no safe windows"
        t, f = t[k], f[k]
    if len(t) < 200:
        return None, meta, "too little data"
    return (t, f), meta, "ok"


def prepare_copy(path, inject=None):
    """Same result as stage2_search.prepare, with an optional inject(t, f) -> f between the windows and the mask. Returns (status, n_searched)."""
    tf, meta, st = load_windowed(path)
    if tf is None:
        return st, None
    t, f = tf
    if inject is not None:
        f = inject(t, f)
    t2, f2, _ = S2.mask_runs(t, f, A.PER.get(meta["tic"], []))
    if len(t2) < 200:
        return "too little data after masking", None
    return "ok", len(t2)


def check(n=20):
    init()
    man = pd.read_csv(DS.MANIFEST).drop_duplicates("file"); pth = dict(zip(man.file, man.path))
    gs = sorted((RUNDIR / "groups").glob("*.json")); rng = np.random.default_rng(7)
    bad = tot = 0; stats = {}
    for p in rng.choice(gs, n, replace=False):
        for m in json.load(open(p))["meta"]:
            fn = m["file"]
            if fn not in pth:
                continue
            st, ns = prepare_copy(pth[fn])
            exp_st, exp_n = m["status"], m.get("n_searched")
            same = (st == exp_st) and (ns == exp_n)
            tot += 1; bad += (not same); stats[exp_st] = stats.get(exp_st, 0) + 1
            if not same:
                print("MISMATCH", pathlib.Path(p).name, fn[:40], "copy:", st, ns, "stored:", exp_st, exp_n)
    print(f"IDENTITY CHECK {SET}: {tot - bad} of {tot} files give the same status and n_searched as the stored group JSON; stored statuses: {stats}")


def found(t, f, arm, tc, dur):
    pr = S2.Prod(t, f, arm)
    return any(abs(e["center"] - tc) <= 0.5 * max(dur, e["dur_h"]) / 24 + 0.1 for e in pr.events()), pr


def run_file(args):
    path, tic, P, fam, lo, seed = args
    base = dict(file=pathlib.Path(path).name, tic=tic, P=P, fam=fam, bin_lo=lo)
    try:
        tf, meta, st = load_windowed(path)
        if tf is None:
            return [dict(base, skip=st)]
        t, f = tf
        periods = A.PER.get(tic, [])
        t0, f0, _ = S2.mask_runs(t, f, periods)
        if len(t0) < 200:
            return [dict(base, skip="too little data after masking")]
        n8 = noise(t0, f0, 8.0)
        if not np.isfinite(n8):
            return [dict(base, skip="8 h noise not finite")]
        cad = float(np.median(np.diff(t0)))
        ev0 = S2.Prod(t0, f0).events() + S2.Prod(t0, f0, -1).events()
        c0 = np.array([e["center"] for e in ev0])
        rng = np.random.default_rng([20261110, tic, seed])
        tc = None
        for x in rng.choice(t0, 300):
            if x - t0.min() > 1.5 and t0.max() - x > 1.5 and np.sum(np.abs(t0 - x) < 10 / 24) >= 0.9 * (20 / 24) / cad and (not len(c0) or np.all(np.abs(c0 - x) > 1.0)):
                tc = float(x); break
        if tc is None:
            return [dict(base, skip="no clean slot")]
        rows = []
        jobs = [(d, K, 1) for d in DURS for K in KS] + [(d, K, -1) for d, K in BUMPS]
        for dur, K, sign in jobs:
            depth = K * n8; arm = 1 if sign == 1 else -1
            fa = f + signal(t, tc, dur, depth, sign)
            ta, fa2, _ = S2.mask_runs(t, fa, periods)
            intr_all = np.sum(np.abs(t - tc) < dur / 48); intr_kept = np.sum(np.abs(ta - tc) < dur / 48)
            fb = f0 + signal(t0, tc, dur, depth, sign)
            fnd_b, _ = found(ta, fa2, arm, tc, dur) if len(ta) > 200 else (False, None)
            fnd_a, _ = found(t0, fb, arm, tc, dur)
            rows.append(dict(base, dur=dur, K=K, sign=sign, n8=n8, found_before=bool(fnd_b), found_after=bool(fnd_a), cut=1 - intr_kept / max(intr_all, 1)))
        return rows
    except Exception as e:
        return [dict(base, skip=f"ERROR {type(e).__name__}: {str(e)[:80]}")]


def sample(n_per):
    tg = pd.read_csv(DS.TARGETS, comment="#").drop_duplicates("tic"); P = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    man = pd.read_csv(DS.MANIFEST).drop_duplicates("file"); man = man[man.tic.isin(P)].copy()
    man["P"] = man.tic.map(P); man["fam"] = np.where(man.author == "QLP", "QLP", "SPOCfam")
    jobs = []
    for lo, hi in BINS:
        for fam in ("SPOCfam", "QLP"):
            sub = man[(man.P >= lo) & (man.P < hi) & (man.fam == fam)]
            pick = sub.sample(n=min(n_per, len(sub)), random_state=1)
            jobs += [(r.path, int(r.tic), float(r.P), fam, lo, i) for i, r in enumerate(pick.itertuples())]
    return jobs, man


def run(n_per, procs):
    jobs, _ = sample(n_per); rows = []
    if ROWS.exists():
        rows = pd.read_pickle(ROWS).to_dict("records"); done = {r["file"] for r in rows}
        jobs = [j for j in jobs if pathlib.Path(j[0]).name not in done]; print(f"resuming: {len(done)} files done, {len(jobs)} to go", flush=True)
    t0 = time.time()
    with mp.Pool(procs, initializer=init) as pool:
        for i, r in enumerate(pool.imap_unordered(run_file, jobs), 1):
            rows += r
            if i % 20 == 0:
                pd.DataFrame(rows).to_pickle(ROWS); print(f"{i}/{len(jobs)} files, {len(rows)} rows, {time.time() - t0:.0f} s", flush=True)
    pd.DataFrame(rows).to_pickle(ROWS); print("DONE", len(rows), f"{time.time() - t0:.0f} s", flush=True)


def summary():
    df = pd.read_pickle(ROWS)
    if "skip" not in df:
        df["skip"] = None
    sk = df[df.skip.notna()]
    ok = df[df.K.notna()].copy()
    _, man = sample(1)
    cnt = man.groupby([pd.cut(man.P, [b[0] for b in BINS] + [1e9], right=False, labels=[b[0] for b in BINS]), "fam"], observed=True).size()
    out = [f"WO-F01 Part A, set {SET}. Files sampled {df.file.nunique()}; with injections {ok.file.nunique()}; skipped {sk.file.nunique()} ({'; '.join(f'{k}: {v}' for k, v in sk.skip.str.slice(0, 40).value_counts().items())}).",
           "m = found when injected BEFORE the mask (what a real planet does) / found when injected AFTER the mask (what every earlier recovery test did). Cells: before/after, n files. Standard error of one cell about 0.05 at n = 100.",
           "Period bins (d): " + " | ".join(f"{lo:g}-{hi:g}" if hi < 1e3 else f">{lo:g}" for lo, hi in BINS)]
    def line(h):
        cells = []
        for lo, _hi in BINS:
            c = h[h.bin_lo == lo]
            cells.append("      n/a    " if len(c) == 0 else f"{c.found_before.mean():.2f}/{c.found_after.mean():.2f} n{c.file.nunique():3d}")
        return " | ".join(cells)
    d = ok[ok.sign == 1]
    out += ["", "A. DIPS, all four durations pooled, by K and product family"]
    for K in sorted(d.K.unique()):
        for fam in ("SPOCfam", "QLP"):
            out.append(f"  K {K:4g} {fam:8s} | " + line(d[(d.K == K) & (d.fam == fam)]))
    out += ["", "B. DIPS by duration (both families pooled)"]
    for K in (12.0, 25.0):
        for dur in DURS:
            out.append(f"  K {K:4g} dur {dur:4g} h  | " + line(d[(d.K == K) & (d.dur == dur)]))
    out += ["", "C. share of the dip's cadences the mask removed (before case, mean, K 12 and 25, all durations)"]
    for fam in ("SPOCfam", "QLP"):
        cells = [f"{d[(d.bin_lo == lo) & (d.fam == fam) & d.K.isin((12.0, 25.0))].cut.mean():.2f}" for lo, _ in BINS]
        out.append(f"  {fam:8s} | " + " | ".join(cells))
    out += ["", "D. BUMPS on the upside-down arm (proof test: before/after must agree, m about 1)"]
    b = ok[ok.sign == -1]
    for K in sorted(b.K.unique()):
        out.append(f"  K {K:4g} dur 8 h | " + line(b[b.K == K]))
    # hunt-level m: cells weighted by the number of files of that cell in the hunt's manifest times the share of sampled files that were usable
    out += ["", f"E. ONE NUMBER FOR THE HUNT {SET}: m = sum(w * before) / sum(w * after), w = files of the cell in the {SET} manifest x usable share of the sample (a file with no safe windows was never searched)"]
    use = df.groupby(["bin_lo", "fam"]).apply(lambda g: g[g.skip.isna()].file.nunique() / max(g.file.nunique(), 1))
    for K in sorted(d.K.unique()):
        for lab, sel in (("dur 8 h", d.dur == 8.0), ("all durations", d.dur > 0)):
            num = den = 0.0
            for (lo, fam), g in d[(d.K == K) & sel].groupby(["bin_lo", "fam"]):
                w = float(cnt.get((lo, fam), 0)) * float(use.get((lo, fam), 0))
                num += w * g.found_before.mean(); den += w * g.found_after.mean()
            out.append(f"  K {K:4g} {lab:14s} | m = {num / den:.2f} (dips lost to the mask: {100 * (1 - num / den):.0f}%)" if den else f"  K {K:4g} {lab}: n/a")
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "check":
        check()
    elif mode == "run":
        run(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("\n".join(summary()))
