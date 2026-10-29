"""Step 1 (29 Oct 2026): recovery of injected dips through the WHOLE frozen v7 chain (VESPER-BRIEFING plan step 1; Compass 2026-10-28-outside-ai-vesper-review.md; FIX-QUEUE 12, 13, 20).
Earlier recovery files (faint_recovery.py, sap_recovery.py) model only the 'found at SNR 7' step and some flags. Here the unchanged frozen code does everything: S2.prepare is wrapped so the
SAME fake dip (same time, same depth in ppm) is added to the prepared flux of EVERY file of a star-sector, then stage3.do_group3 (search, second-product check, flags), the v6 SAP twin pass,
the v7 PDCSAP check, stage3_report.merge_sap and apply_v7 (union, common-moment flag, tiers) run exactly as in the real run. The common-moment pool is the real run's events of the same sector and
camera. Nothing in the frozen hash is edited (this file is not in current_settings' code list); a zero-depth run reproduces the real run's events (chain_recovery_test.py).
Mirror-bump test: sign +1 puts a DIP in the flux (seen by the real path), sign -1 puts a BUMP (seen as a dip by the upside-down path). Same shape, same place, same chain: if the upside-down
control is fair for planet-like signals, tier-1 recovery is equal for the two.
Injection time: a random cadence of the longest product, not within the match window of an event the star-sector already has (so every hit is the fake). Depth: K x the 8 h box noise of that
light curve in ppm (the unit of faint_recovery_v5.txt), converted to ppm in the summary. Planet radius is NOT computed from a measured star: see summarize().
Usage: python chain_recovery.py run [n_groups] [procs] [label]   |   python chain_recovery.py summary [label]   (writes research\\stage3\\chain_recovery_<label>.txt; real events are not shown)"""
import sys, json, glob, random, shutil, uuid, pathlib, multiprocessing as mp
import numpy as np, pandas as pd
import stage2_search as S2, stage3 as S3m, stage3_core as C, stage3_report as R, sap_twin as T
from audit_paths import noise

RUN = C.ROOT / "data" / "stage3" / "fd788be04650"
PREP = C.ROOT / "data" / "chain_recovery"
TMP = PREP / "tmp"
G1 = C.ROOT / "data" / "g1"
KS = (6.0, 8.0, 10.0, 12.0, 14.0, 18.0)                      # injected depth in units of the 8 h box noise
DURS = (4.0, 8.0, 14.0, 20.0)
TIER1 = ("1A", "1L", "1B")
FLAGS = ("gap_dump", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated", "common")
R_EARTH_PER_RSUN = 109.076
INJ, CACHE, W = {}, {}, {}


def signal(t, tc, dur_h, depth_ppm, sign):
    """Fractional flux change of the injected trapezoid (20 percent ingress and egress, the shape of faint_recovery.py). sign +1 = dip in the flux, -1 = bump (a dip in the upside-down copy)."""
    return -sign * depth_ppm * 1e-6 * np.clip((dur_h / 2 - np.abs(t - tc) * 24) / (0.2 * dur_h), 0, 1)


def install():
    """Wrap S2.prepare: cache the prepared (masked, windowed) file once per star-sector and add the active injection to a COPY of its flux."""
    T.install(S2)
    base = S2.prepare

    def prepare(path):
        key = str(path)
        if key not in CACHE:
            CACHE[key] = base(path)
        d, m = CACHE[key]
        if d is None or not INJ:
            return d, m
        return {**d, "f": d["f"] + signal(d["t"], **INJ)}, m
    S2.prepare = prepare


def build_raw(path):
    """Every event of the real v7 run (both folders), unmerged, with the columns stage3_report.load adds before merge_sap."""
    ev = []
    for d in ("groups", "groups_sap"):
        for p in glob.glob(str(RUN / d / "*.json")):
            ev += json.load(open(p))["events"]
    ev = pd.DataFrame(ev).merge(pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"}), on=["tic", "sector"], how="left")
    ev["primary"] = ev["product"] == ev["best"]
    ev["c8_best"] = pd.to_numeric(ev.c8_best, errors="coerce")
    ev.to_pickle(path)


def ev_key(evs):
    """Identity key of a list of group events: what the search and the Stage 3 enrichment wrote (kind, product, centre, SNR, tier before the union)."""
    return sorted((e["kind"], e["product"], round(float(e["center"]), 3), round(float(e["snr"]), 2), str(e["tier"])) for e in evs)


def init(raw_path):
    S3m._init3(str(TMP / "init"), "chain", C.GRID_V5)         # Stage 2 init, v5 box lengths, SAP hook, ephemeris, QLP-only list: the frozen worker set-up
    install()
    raw = pd.read_pickle(raw_path)
    W["raw"] = {k: g for k, g in raw.groupby(["sector", "camera"])}
    W["rawkey"] = {k: ev_key(g.to_dict("records")) for k, g in raw.groupby(["tic", "sector"])}
    best = pd.read_csv(C.BEST, usecols=["tic", "sector", "product"])
    W["best"] = {(int(a), int(b)): c for a, b, c in zip(best.tic, best.sector, best["product"])}
    man = pd.read_csv(C.MANIFEST).drop_duplicates("file")
    W["author"] = dict(zip(man.file, man.author))


def chain(tic, sec, paths, best):
    """The frozen per-group chain on the (possibly injected) flux: PDCSAP search + enrichment, then the SAP twin pass + v7 PDCSAP check. Returns (events, meta)."""
    tmp = TMP / uuid.uuid4().hex[:12]
    try:
        S2.GROUPS = tmp / "groups"; S2.GROUPS.mkdir(parents=True)
        g = json.load(open(S3m.do_group3((tic, sec, paths))))
        evs, meta = list(g["events"]), list(g["meta"])
        tw = [p + T.SUFFIX for p in paths if W["author"].get(pathlib.Path(p).name) in T.FAMILY] if best in T.FAMILY else []
        if tw:
            S2.GROUPS = tmp / "groups_sap"; S2.GROUPS.mkdir()
            p2 = S3m.do_group3((tic, sec, tw)); S3m.add_pdc((p2, [q[:-len(T.SUFFIX)] for q in tw], best))
            evs += json.load(open(p2))["events"]
        return evs, meta
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def merged(evs, tic, sec, best):
    """The star-sector's events after the v6 union and the v7 flags, judged against the real run's events of the same sector and camera (what stage3_report.load does for the whole run)."""
    if not evs:
        return pd.DataFrame()
    new = pd.DataFrame(evs); new["best"] = best; new["primary"] = new["product"] == best
    new["c8_best"] = pd.to_numeric(new.c8_best, errors="coerce")
    base = W["raw"].get((sec, int(new.camera.iloc[0])))
    sub = new if base is None else pd.concat([base[base.tic != tic], new], ignore_index=True)
    ev = R.apply_v7(R.merge_sap(sub))
    return ev[(ev.tic == tic) & (ev.sector == sec)]


def b(x):
    return bool(x) if x == x and x is not None else False


def row_of(ev, kind, tc, dur, **meta):
    """What happened to one injected dip: seen in any product, seen as a primary event, its tier and the flags on it."""
    near = ev[ev.kind == kind] if len(ev) else ev
    if len(near):
        near = near[np.abs(near.center - tc) <= 0.5 * np.maximum(dur, near.dur_h) / 24 + 0.1]
    prim = near[near.primary] if len(near) else near
    row = dict(meta, dur=dur, tc=tc, found_any=len(near) > 0, found_primary=len(prim) > 0, tier="", seen_by="", snr=np.nan, **{f: False for f in FLAGS})
    if len(prim):
        r = prim.sort_values("snr", ascending=False).iloc[0]
        row.update(tier=r["tier"], seen_by=r["seen_by"], snr=float(r["snr"]), **{f: b(r.get(f)) for f in FLAGS})
    row["tier1"] = row["tier"] in TIER1
    return row


def pick_tc(t, bc, dur, rng):
    for _ in range(200):
        tc = float(rng.choice(t))
        if not len(bc) or np.all(np.abs(bc[:, 0] - tc) > 0.5 * np.maximum(dur, bc[:, 1]) / 24 + 0.15):
            return tc
    return None


def baseline(tic, sec):
    """(paths, best product, chain events with the v6 union and v7 flags, prepared products) of a star-sector with nothing injected."""
    CACHE.clear(); INJ.clear()
    paths = sorted(glob.glob(rf"{G1}\{tic}\*s{sec:04d}*.fits")); best = W["best"].get((tic, sec))
    if not paths or best is None:
        return paths, best, None, {}
    evs, _ = chain(tic, sec, paths, best); W["base_evs"] = evs
    prods = {}
    for p in paths:
        d, _ = S2.prepare(p)
        if d is not None:
            prods[d["meta"]["product"]] = d
    return paths, best, merged(evs, tic, sec, best), prods


def run_group(args):
    try:
        return _run_group(*args)
    except Exception as e:                                       # reported as a row and counted in the summary, never silent
        return [dict(tic=args[0], sector=args[1], error=f"{type(e).__name__}: {str(e)[:120]}")]


def _run_group(tic, sec, tmag, rtic):
    paths, best, base, prods = baseline(tic, sec)
    if not prods:
        return [dict(tic=tic, sector=sec, error="no prepared product")]
    a = max(prods.values(), key=lambda d: d["t"].max() - d["t"].min())
    n8 = noise(a["t"], a["f"], 8.0)
    if not np.isfinite(n8):
        return [dict(tic=tic, sector=sec, error="8 h noise not finite")]
    bc = base[["center", "dur_h"]].values if len(base) else np.empty((0, 2))
    rng = np.random.default_rng([20261029, tic, sec])
    out = [dict(tic=tic, sector=sec, base_ok=ev_key(W["base_evs"]) == W["rawkey"].get((tic, sec), []), n_base=len(W["base_evs"]))]   # zero-injection identity with the real run, every sampled star-sector
    for dur in DURS:
        tc = pick_tc(a["t"], bc, dur, rng)
        if tc is None:
            continue
        for sign in (1, -1):
            for K in KS:
                INJ.update(tc=tc, dur_h=dur, depth_ppm=K * n8, sign=sign)
                evs, _ = chain(tic, sec, paths, best)
                out.append(row_of(merged(evs, tic, sec, best), "real" if sign == 1 else "flip", tc, dur,
                                  tic=tic, sector=sec, tmag=tmag, rtic=rtic, best=best, n8=n8, K=K, depth_ppm=K * n8, sign=sign))
    INJ.clear()
    return out


def run(n, procs, label, resume=False):
    PREP.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)
    raw = PREP / f"raw_{RUN.name}.pkl"
    if not raw.exists():
        build_raw(raw)
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    gl = [tuple(int(x) for x in p.stem.split("_")) for p in sorted((RUN / "groups").glob("*.json"))]
    random.Random(20261029).shuffle(gl)
    jobs = [(t, s, float(tg.tmag[t]), float(tg.tic_radius_rsun[t])) for t, s in gl[:n]]
    rows = []
    if resume and (PREP / f"rows_{label}.pkl").exists():         # a stopped run continues with the star-sectors that have no row yet (a star-sector is written whole, so none is half done)
        rows = pd.read_pickle(PREP / f"rows_{label}.pkl").to_dict("records"); done = {(int(r["tic"]), int(r["sector"])) for r in rows}
        jobs = [j for j in jobs if (j[0], j[1]) not in done]; print(f"resuming: {len(done)} star-sectors done, {len(jobs)} to go", flush=True)
    with mp.Pool(procs, initializer=init, initargs=(str(raw),)) as pool:
        for i, r in enumerate(pool.imap_unordered(run_group, jobs), 1):
            rows += r
            if i % 10 == 0:
                print(f"{i}/{len(jobs)} groups, {len(rows)} rows", flush=True)
                pd.DataFrame(rows).to_pickle(PREP / f"rows_{label}.pkl")
    pd.DataFrame(rows).to_pickle(PREP / f"rows_{label}.pkl")
    print("CHAIN RECOVERY DONE", len(rows), flush=True)


def rate(g, col="tier1"):
    return f"{100 * g[col].mean():3.0f}%" if len(g) else "  n/a"


def k_at(g, level):
    """K (units of the 8 h box noise) at which the tier-1 recovery rate first reaches `level`, by linear interpolation between the injected levels."""
    r = g.groupby("K").tier1.mean().reindex(KS)
    if r.isna().all():
        return "n/a"
    if r.iloc[0] >= level:
        return f"<{KS[0]:g}"
    for (k0, r0), (k1, r1) in zip(r.items(), list(r.items())[1:]):
        if r0 < level <= r1:
            return f"{k0 + (k1 - k0) * (level - r0) / (r1 - r0):.1f}"
    return f">{KS[-1]:g}"


def summarize(df, label):
    from scipy.stats import binomtest
    err = df[df.error.notna()] if "error" in df else df.iloc[0:0]
    bo = df[df.base_ok.notna()] if "base_ok" in df else df.iloc[0:0]
    df = df[df.K.notna()].copy()
    for c in ("found_any", "found_primary", "tier1") + FLAGS:
        df[c] = df[c].astype(bool)                               # rows of different kinds were concatenated, so these columns arrive as object
    df = df.assign(cls=pd.cut(df.tmag, C.TBINS, right=False, labels=C.TLABELS).astype(str), fam=df.best.isin(T.FAMILY))
    ng = df.groupby(["tic", "sector"]).ngroups
    t = [f"Full-chain recovery of injected dips through the frozen v7 chain (hash fd788be04650), {ng} random star-sectors, {len(df)} injections, label {label}. {len(err)} star-sectors failed (listed below).",
         "Each injection is a trapezoid (20% ingress and egress) added at the same time and ppm depth to EVERY file of the star-sector, then the unchanged search, flags, second-product check, SAP twin, PDCSAP check, union and tiers run.",
         "'Recovered' = the dip is a primary event in tier 1 (1A, 1L or 1B). Depth K is in units of the 8 h box noise of that light curve (the unit of faint_recovery_v5.txt). Time = a random cadence, so gap edges, orbit starts,",
         "eclipse overlap and the common-moment flag cost what they really cost. Planet size is NOT measured: G1 has no light ratio or radius ratio (see the last section).",
         f"Zero-injection check: {int(bo.base_ok.astype(bool).sum())} of {len(bo)} sampled star-sectors reproduce the real run's events exactly (kind, product, centre, SNR, tier) when nothing is injected.", ""]
    if len(err):
        t += ["FAILED star-sectors (reported, not hidden):"] + [f"  {r.error}" for r in err.itertuples()][:10] + [""]
    d = df[df.sign == 1]
    t.append("1. DIPS (sign +1, real path). Tier-1 recovery by duration and depth; cell = share recovered (share seen at SNR 7 in some product)")
    for lab, g0 in (("all", d),) + tuple((c, d[d.cls == c]) for c in C.TLABELS):
        t.append(f"  {lab} ({g0.groupby(['tic', 'sector']).ngroups} star-sectors)")
        t.append("    box h | " + " | ".join(f"{k:g} x noise" for k in KS))
        for dur in DURS:
            t.append(f"    {dur:5.0f} | " + " | ".join(f"{rate(h)} ({rate(h, 'found_any')[:-1]})" for k in KS for h in [g0[(g0.dur == dur) & (g0.K == k)]]))
    t += ["", "2. WHERE IT FAILS (dips, K 10 or more): share of injections lost at each step"]
    g = d[d.K >= 10]
    t.append(f"  n = {len(g)}; not seen at SNR 7 in any product {100 * (~g.found_any).mean():.0f}%; seen but not a primary event {100 * (g.found_any & ~g.found_primary).mean():.0f}%; primary but tier 2 {100 * (g.found_primary & (g.tier == '2')).mean():.0f}%; tier 3 {100 * (g.found_primary & (g.tier == '3')).mean():.0f}%; tier 1 {100 * g.tier1.mean():.0f}%")
    p2 = g[g.found_primary & (g.tier == "2")]
    t.append("  flags on the tier-2 dips (a dip can carry several): " + ", ".join(f"{f} {100 * p2[f].mean():.0f}%" for f in FLAGS) if len(p2) else "  no tier-2 dips")
    t.append("  which product found the tier-1 dips: " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in g[g.tier1].seen_by.value_counts(normalize=True).items()))
    t += ["", "3. MIRROR-BUMP TEST (same place, same shape, same chain): dip in the real path vs bump in the upside-down path. Tier-1 recovery; paired by star-sector, duration and depth"]
    pv = df.pivot_table(index=["tic", "sector", "dur", "K"], columns="sign", values="tier1", aggfunc="first").dropna()
    pf = df.pivot_table(index=["tic", "sector", "dur", "K"], columns="sign", values="found_any", aggfunc="first").dropna()
    t.append("    K x noise | pairs | dip recovered | bump recovered | only dip | only bump | exact p      | dip seen | bump seen")
    for k in KS:
        x, y = pv.xs(k, level="K"), pf.xs(k, level="K")
        a, c = int((x[1] & ~x[-1]).sum()), int((~x[1] & x[-1]).sum())
        p = binomtest(a, a + c, 0.5).pvalue if a + c else float("nan")
        t.append(f"    {k:9g} | {len(x):5d} | {100 * x[1].mean():12.0f}% | {100 * x[-1].mean():13.0f}% | {a:8d} | {c:9d} | {p:12.3f} | {100 * y[1].mean():7.0f}% | {100 * y[-1].mean():8.0f}%")
    x = pv[pv.index.get_level_values("K").isin((8, 10, 12))]
    a, c = int((x[1] & ~x[-1]).sum()), int((~x[1] & x[-1]).sum())
    t.append(f"  K 8, 10 and 12 pooled: {len(x)} pairs, only dip {a}, only bump {c}, exact p = {binomtest(a, a + c, 0.5).pvalue if a + c else float('nan'):.3f}; dip {100 * x[1].mean():.0f}% vs bump {100 * x[-1].mean():.0f}%")
    t += ["", "4. DEPTH THAT IS RECOVERED, in ppm, with planet radius only as a labelled illustration",
          "  K50 and K90 = the depth (units of the 8 h box noise) at which tier-1 recovery first reaches 50% and 90%. Depth in ppm = K x the class's median 8 h noise. The radius columns are an ILLUSTRATION, not a measurement:",
          "  they assume the crossed star has the TIC radius (a blended-point radius) and give the planet radius for it carrying all the light (smallest planet) and half the light (the crossed star is one of two equal stars, planet x 1.41).",
          "  The crossed star's own radius and light share are NOT in the G1 table; treat the radius as a range with at least that spread plus the unknown radius ratio.",
          "    class        box h | K50 | K90 | median 8 h noise ppm | depth50 ppm | depth90 ppm | median TIC R (Rsun) | R_planet at 50% (Rearth, share 1 to 0.5) | at 90%"]
    for lab, g0 in tuple((c, d[d.cls == c]) for c in C.TLABELS) + (("all", d),):
        n8m, rr = g0.drop_duplicates(["tic", "sector"]).n8.median(), g0.drop_duplicates("tic").rtic.median()
        for dur in DURS:
            h = g0[g0.dur == dur]
            if not len(h):
                continue
            k5, k9 = k_at(h, 0.5), k_at(h, 0.9)
            cells = []
            for kk in (k5, k9):
                try:
                    dp = float(kk) * n8m; lo = R_EARTH_PER_RSUN * rr * np.sqrt(dp * 1e-6); cells.append((f"{dp:6.0f}", f"{lo:4.1f} to {lo * np.sqrt(2):4.1f}"))
                except ValueError:
                    cells.append(("   n/a", "n/a"))
            t.append(f"    {lab:11s} {dur:5.0f} | {k5:>4s} | {k9:>4s} | {n8m:19.0f} | {cells[0][0]} | {cells[1][0]} | {rr:19.2f} | {cells[0][1]:40s} | {cells[1][1]}")
    t += ["", "5. BY PRODUCT FAMILY (dips, K 10 or more): best product with a SAP twin (SPOC, TESS-SPOC) vs QLP", "  " + ", ".join(f"{'SPOC family' if f else 'QLP'}: {rate(h)} of {len(h)}" for f, h in g.groupby("fam"))]
    return t


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "run":
        run(int(sys.argv[2]) if len(sys.argv) > 2 else 100, int(sys.argv[3]) if len(sys.argv) > 3 else 8, sys.argv[4] if len(sys.argv) > 4 else "v7", "resume" in sys.argv[5:])
    else:
        label = sys.argv[2] if len(sys.argv) > 2 else "v7"
        txt = summarize(pd.read_pickle(PREP / f"rows_{label}.pkl"), label)
        print("\n".join(txt))
        (C.ROOT / "research" / "stage3" / f"chain_recovery_{label}.txt").write_text("\n".join(txt), encoding="utf-8")
