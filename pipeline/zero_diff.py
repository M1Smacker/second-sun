"""Zero-difference test for the dataset switch (G2 preregistration section 4; 29 Oct 2026). The data paths now come from dataset.py. With SS_SET unset (G1) the edited code must give EXACTLY the
events, flags and tiers of the frozen v7 run (data/stage3/fd788be04650). Re-runs the whole per-group chain (search, second-product check, flags, SAP twin pass, v7 PDCSAP check; chain_recovery.chain)
on a stratified random sample of G1 star-sectors and compares (1) every field of every event with the frozen group files, and (2) the tiers after the union and the v7 flags with stage3_report.load.
Also checks that the paths the code reads are the old literal ones, and runs a mutation (a changed flag setting must be caught).
Usage: python zero_diff.py [n_groups] [procs]    (default 300 groups, 6 processes; writes research\\stage3\\zero-diff-dataset-switch.txt; real events are not shown)"""
import sys, os, json, glob, pathlib, random, time, multiprocessing as mp
import numpy as np, pandas as pd
import chain_recovery as X, stage3_core as C, stage3_report as R, sap_twin as T, dataset as DS

KEEP = {"tic", "sector"}


def frozen_events(tic, sec):
    out = []
    for d in ("groups", "groups_sap"):
        f = X.RUN / d / f"{tic}_{sec}.json"
        if f.exists():
            out += json.load(open(f))["events"]
    return out


def same_events(a, b):
    """Every field equal (None for NaN in both); order of the lists may differ."""
    k = lambda e: (e["kind"], e["product"], e["center"], e["dur_h"])
    return len(a) == len(b) and all(x == y for x, y in zip(sorted(a, key=k), sorted(b, key=k)))


def key(ev):
    return sorted((r.kind, r.product, round(float(r.center), 3), round(float(r.snr), 2), str(r.tier), bool(r.primary), str(r.seen_by), bool(r.common)) for r in ev.itertuples())


def check(args):
    tic, sec, want_key = args
    try:
        X.CACHE.clear(); X.INJ.clear()
        paths = sorted(glob.glob(rf"{X.G1}\{tic}\*s{sec:04d}*.fits")); best = X.W["best"].get((tic, sec))
        evs, _ = X.chain(tic, sec, paths, best)
        ok_fields = same_events(evs, frozen_events(tic, sec))
        ok_tiers = key(X.merged(evs, tic, sec, best)) == want_key if len(evs) or want_key else True
        return (tic, sec, len(evs), ok_fields, ok_tiers, "")
    except Exception as e:
        return (tic, sec, -1, False, False, f"{type(e).__name__}: {str(e)[:100]}")


def sample(real, n):
    g = real.groupby(["tic", "sector"]).agg(best=("best", "first")).reset_index()
    allg = [tuple(int(x) for x in p.stem.split("_")) for p in sorted((X.RUN / "groups").glob("*.json"))]
    have = {(int(r.tic), int(r.sector)): r.best for r in g.itertuples()}
    best = pd.read_csv(C.BEST, usecols=["tic", "sector", "product"]); bp = {(int(a), int(b)): c for a, b, c in zip(best.tic, best.sector, best["product"])}
    rng = random.Random(20261029)
    cells = {(fam, ev): [] for fam in (True, False) for ev in (True, False)}
    for k in allg:
        cells[(bp.get(k) in T.FAMILY, k in have)].append(k)
    quota = {(True, True): n // 3, (True, False): n // 5, (False, True): n // 3, (False, False): n - n // 3 - n // 5 - n // 3}
    pick = []
    for c, q in quota.items():
        rng.shuffle(cells[c]); pick += cells[c][:q]
    return pick, {c: (len(cells[c]), min(quota[c], len(cells[c]))) for c in cells}


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    assert DS.NAME == "g1", "the zero-difference test runs on G1 (leave SS_SET unset)"
    t0 = time.time()
    lit = {"TARGETS": (C.TARGETS, r"D:\second-sun\targets\g1_targets.csv"), "MANIFEST": (C.MANIFEST, r"D:\second-sun\data\g1\manifest.csv"),
           "BEST": (C.BEST, r"D:\second-sun\research\audit-2026-10-23\best_per_star_sector.csv"), "DATA": (DS.DATA, r"D:\second-sun\data\g1"),
           "AUDIT": (DS.AUDIT, r"D:\second-sun\research\audit-2026-10-23"), "RUNS": (DS.RUNS, r"D:\second-sun\data\stage3"), "PREP": (DS.PREP, r"D:\second-sun\data\stage3_prep")}
    for k, (now, old) in lit.items():
        assert str(now) == old, f"{k}: {now} is not the old literal {old}"
    print("paths: all", len(lit), "equal the old literal G1 paths", flush=True)
    X.PREP.mkdir(parents=True, exist_ok=True); X.TMP.mkdir(parents=True, exist_ok=True)
    raw = X.PREP / f"raw_{X.RUN.name}.pkl"
    if not raw.exists():
        X.build_raw(raw)
    real, _ = R.load(str(X.RUN / "groups"))
    pick, cells = sample(real, n)
    jobs = [(t, s, key(real[(real.tic == t) & (real.sector == s)])) for t, s in pick]
    print(f"{len(jobs)} star-sectors sampled (cell: available, taken): {cells}", flush=True)
    res = []
    with mp.Pool(procs, initializer=X.init, initargs=(str(raw),)) as pool:
        for i, r in enumerate(pool.imap_unordered(check, jobs), 1):
            res.append(r)
            if i % 50 == 0:
                print(f"{i}/{len(jobs)}", flush=True)
    df = pd.DataFrame(res, columns=["tic", "sector", "n_events", "fields_equal", "tiers_equal", "error"])
    nev = int(df.n_events.clip(lower=0).sum())
    bad = df[~(df.fields_equal & df.tiers_equal)]
    # mutation: a changed flag setting (the flat-baseline lift, 0.5 -> 0.05) must be caught by the same comparison on the star-sectors that have events
    X.init(str(raw)); C.STEP_LIFT = 0.05
    withev = [j for j in jobs if j[2]][:15]
    caught = sum(1 for r in map(check, withev) if not (r[3] and r[4]))
    C.STEP_LIFT = 0.5
    txt = [f"Zero-difference test of the dataset switch, G1, 29 Oct 2026 (SS_SET unset, frozen run {X.RUN.name}).",
           f"Paths: all {len(lit)} paths read by the edited code equal the old literal G1 paths.",
           f"Sample: {len(df)} random star-sectors (seed 20261029), stratified (SPOC family best / QLP best x with events / without events), {nev} events re-made by the whole chain.",
           f"Every field of every event equal to the frozen group files: {int(df.fields_equal.sum())} of {len(df)} star-sectors.",
           f"Tiers, union and v7 flags equal to stage3_report.load of the frozen run: {int(df.tiers_equal.sum())} of {len(df)} star-sectors.",
           f"Errors: {int((df.error != '').sum())}. Star-sectors that differ: {len(bad)}.",
           f"Mutation (flat-baseline lift 0.5 changed to 0.05, {len(withev)} star-sectors with events): the comparison caught {caught} of {len(withev)}.",
           f"Not tested: the other {5082 - len(df)} star-sectors of the frozen run (the code paths are the same; only the sample was re-run). Time {time.time() - t0:.0f} s."]
    print("\n".join(txt))
    bad.to_csv(X.PREP / "zero_diff_bad_LOCAL.csv", index=False)
    (C.ROOT / "research" / "stage3" / "zero-diff-dataset-switch.txt").write_text("\n".join(txt), encoding="utf-8")
