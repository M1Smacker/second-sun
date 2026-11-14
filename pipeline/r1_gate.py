"""Re-search 1 pre-run gates (R1-PREREGISTRATION.md section 5), measured through the WHOLE chain (search, second-product check, flags, SAP twin, PDCSAP check, union, common-moment, tiers, and the Petrova
cross-sector veto) on the seen stars. The earlier recovery tests (chain_recovery.py, recover_cbp.py, Lab 6) put the fake dip in AFTER the eclipse mask; here it goes into the RAW loaded flux, so it is
in the light when the mask is built, as a real planet is (audit F-01). Real events are never shown; counts only; rows are private (data\\chain_recovery_<set>).
Per star-sector: the same trapezoid at the same time and depth (K x the 8 h box noise) in EVERY product, durations 4, 8, 14, 20 h, K 12 and 25, sign +1 (dip, real arm) and -1 (bump, upside-down arm),
two modes: `before` (injected into the raw flux) and `after` (injected into the prepared flux, the old way). The recovery is tier 1 after the whole chain. m = tier-1 recovery before / after.
Environment: SS_SET (g2 or g3), SS_RUN = the folder name of a Petrova development run of the seen stars (r1dev_<set>_seen_<hash12>), VESPER_OPTS=c6,p1.
Usage:  python r1_gate.py run N PROCS     |     python r1_gate.py summary     (writes research/stage3/R1-GATE-RESULT-<set>.txt)"""
import os, sys, glob, random, json, pathlib, multiprocessing as mp
import numpy as np, pandas as pd

if os.environ.get("SS_SET") not in ("g2", "g3"):
    sys.exit("SS_SET must be g2 or g3")
import chain_recovery as X
import stage2_search as S2, stage3_core as C, stage3_report as R, dataset as DS, vopts as V
from audit_paths import noise

if V.ON != frozenset({"c6", "p1"}):
    sys.exit(f"VESPER_OPTS must be exactly c6,p1, not {sorted(V.ON)}")
KS, DURS = (12.0, 25.0), (4.0, 8.0, 14.0, 20.0)
BINS = [(5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e9)]
MODE = {"m": "before"}
TAG = os.environ.get("R1_TAG", "")      # R1_TAG=-sealed keeps the S4 completeness run on the sealed stars apart from the development gates (their files are frozen references)
ROWS = X.PREP / f"rows_r1_gate{TAG}.pkl"
OUT = C.ROOT / "research" / "stage3" / f"R1-GATE-RESULT-{DS.NAME}{TAG}.txt"


def install():
    """Inject into the raw loaded flux (mode before) or into the prepared flux (mode after). No cache: the mask depends on the injected light."""
    X.T.install(S2)
    base_load, base_prepare = S2.load, S2.prepare

    def load(path, info=False):
        r = base_load(path, info)
        if MODE["m"] != "before" or not X.INJ:
            return r
        return (r[0], r[1] + X.signal(r[0], **X.INJ)) + tuple(r[2:])

    def prepare(path):
        d, m = base_prepare(path)
        if MODE["m"] == "after" and d is not None and X.INJ:
            return {**d, "f": d["f"] + X.signal(d["t"], **X.INJ)}, m
        return d, m
    S2.load, S2.prepare = load, prepare


def init(raw_path):
    X.S3m._init3(str(X.TMP / "init"), "chain", C.GRID_V5)
    install()
    raw = pd.read_pickle(raw_path)
    X.W["raw"] = {k: g for k, g in raw.groupby(["sector", "camera"])}
    X.W["rawkey"] = {k: X.ev_key(g.to_dict("records")) for k, g in raw.groupby(["tic", "sector"])}
    best = pd.read_csv(C.BEST, usecols=["tic", "sector", "product"])
    X.W["best"] = {(int(a), int(b)): c for a, b, c in zip(best.tic, best.sector, best["product"])}
    man = pd.read_csv(C.MANIFEST).drop_duplicates("file")
    X.W["author"] = dict(zip(man.file, man.author))


def merged_star(evs, tic, sec, best):
    """As chain_recovery.merged, but apply_v7 also sees the star's STORED events in its other sectors: the Petrova veto and c6 are cross-sector rules and need their partners."""
    if not evs:
        return pd.DataFrame()
    new = pd.DataFrame(evs); new["best"] = best; new["primary"] = new["product"] == best
    new["c8_best"] = pd.to_numeric(new.c8_best, errors="coerce")
    base = X.W["raw"].get((sec, int(new.camera.iloc[0])))
    others = [d[d.tic == tic] for (s, c), d in X.W["raw"].items() if s != sec and (d.tic == tic).any()]
    sub = pd.concat(([] if base is None else [base[base.tic != tic]]) + [new] + others, ignore_index=True)
    ev = R.apply_v7(R.merge_sap(sub))
    return ev[(ev.tic == tic) & (ev.sector == sec)]


def extra(ev, kind, tc, dur):
    """veto and recovered-light state of the injected event (primary event nearest in time)."""
    out = dict(vetoed=False, recovered=np.nan)
    if not len(ev):
        return out
    near = ev[(ev.kind == kind) & ev.primary & (np.abs(ev.center - tc) <= 0.5 * np.maximum(dur, ev.dur_h) / 24 + 0.1)]
    if len(near):
        r = near.sort_values("snr", ascending=False).iloc[0]
        out.update(vetoed=bool(r.get("p1_veto", False)), recovered=(bool(r["recovered"]) if "recovered" in r and r["recovered"] == r["recovered"] else np.nan))
    return out


def baseline(tic, sec):
    X.CACHE.clear(); X.INJ.clear(); MODE["m"] = "before"
    paths = sorted(glob.glob(rf"{X.G1}\{tic}\*s{sec:04d}*.fits")); best = X.W["best"].get((tic, sec))
    if not paths or best is None:
        return paths, best, None, {}
    evs, _ = X.chain(tic, sec, paths, best); X.W["base_evs"] = evs
    prods = {}
    for p in paths:
        d, _ = S2.prepare(p)
        if d is not None:
            prods[d["meta"]["product"]] = d
    return paths, best, merged_star(evs, tic, sec, best), prods


def run_group(args):
    try:
        return _run_group(*args)
    except Exception as e:                                       # reported as a row and counted in the summary, never silent
        return [dict(tic=args[0], sector=args[1], error=f"{type(e).__name__}: {str(e)[:120]}")]


def _run_group(tic, sec, tmag):
    paths, best, base, prods = baseline(tic, sec)
    if not prods:
        return [dict(tic=tic, sector=sec, error="no prepared product")]
    a = max(prods.values(), key=lambda d: d["t"].max() - d["t"].min())
    n8 = noise(a["t"], a["f"], 8.0)
    if not np.isfinite(n8):
        return [dict(tic=tic, sector=sec, error="8 h noise not finite")]
    P = float((a["meta"].get("p1") or {}).get("P", np.nan))
    bc = base[["center", "dur_h"]].values if len(base) else np.empty((0, 2))
    rng = np.random.default_rng([20261111, tic, sec])
    out = [dict(tic=tic, sector=sec, P=P, base_ok=X.ev_key(X.W["base_evs"]) == X.W["rawkey"].get((tic, sec), []), n_base=len(X.W["base_evs"]))]
    for dur in DURS:
        tc = X.pick_tc(a["t"], bc, dur, rng)
        if tc is None:
            continue
        for sign in (1, -1):
            for K in KS:
                X.INJ.update(tc=tc, dur_h=dur, depth_ppm=K * n8, sign=sign)
                for mode in ("before", "after"):
                    MODE["m"] = mode
                    evs, _ = X.chain(tic, sec, paths, best); ev = merged_star(evs, tic, sec, best); kind = "real" if sign == 1 else "flip"
                    out.append({**X.row_of(ev, kind, tc, dur, tic=tic, sector=sec, tmag=tmag, best=best, n8=n8, K=K, sign=sign, mode=mode, P=P), **extra(ev, kind, tc, dur)})
    X.INJ.clear(); MODE["m"] = "before"
    return out


def run(n, procs):
    X.PREP.mkdir(parents=True, exist_ok=True); X.TMP.mkdir(parents=True, exist_ok=True)
    raw = X.PREP / f"raw_{X.RUN.name}.pkl"
    if not raw.exists():
        X.build_raw(raw)
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    gl = [tuple(int(x) for x in p.stem.split("_")) for p in sorted((X.RUN / "groups").glob("*.json"))]
    meta = {}
    for p in (X.RUN / "groups").glob("*.json"):                  # period of each group, to stratify (30 per bin when n = 150)
        m = json.load(open(p, encoding="utf-8"))["meta"]; q = next((x.get("p1") for x in m if x.get("p1")), None)
        meta[tuple(int(x) for x in p.stem.split("_"))] = (q or {}).get("P", np.nan)
    random.Random(20261111).shuffle(gl)
    jobs = []
    for lo, hi in BINS:
        sel = [g for g in gl if lo <= (meta.get(g) or 0) < hi][: n // len(BINS)]
        jobs += [(t, s, float(tg.tmag[t])) for t, s in sel]
    print(f"{len(jobs)} star-sectors ({n // len(BINS)} per period bin)", flush=True)
    rows = []
    with mp.Pool(procs, initializer=init, initargs=(str(raw),)) as pool:
        for i, r in enumerate(pool.imap_unordered(run_group, jobs), 1):
            rows += r
            if i % 10 == 0:
                print(f"{i}/{len(jobs)} groups, {len(rows)} rows", flush=True); pd.DataFrame(rows).to_pickle(ROWS)
    pd.DataFrame(rows).to_pickle(ROWS)
    print("R1 GATE RUN DONE", len(rows), flush=True)


def binlab(p):
    for lo, hi in BINS:
        if lo <= p < hi:
            return f"{lo:g}-{hi:g}" if hi < 1e8 else f"over {lo:g}"
    return "n/a"


def summary():
    df = pd.read_pickle(ROWS)
    err = df[df.get("error").notna()] if "error" in df else df.iloc[:0]
    g0 = df[df.get("base_ok").notna()] if "base_ok" in df else df.iloc[:0]
    inj = df[df.get("mode").notna()] if "mode" in df else df.iloc[:0]
    out = [f"R1 gates, set {DS.NAME}, run {X.RUN.name}, VESPER_OPTS {sorted(V.ON)}. Counts only.",
           f"Star-sectors: {len(g0)}; zero-injection identity with the stored run: {int(g0.base_ok.sum())} of {len(g0)}; errors: {len(err)} {err['error'].value_counts().head(3).to_dict() if len(err) else ''}"]
    inj = inj.assign(bin=[binlab(p) for p in inj.P])
    order = [binlab(lo) if False else (f"{lo:g}-{hi:g}" if hi < 1e8 else f"over {lo:g}") for lo, hi in BINS]
    ok = {1: True, -1: True}
    from gate_judge import judge                 # FIX 87 (14 Nov 2026): a bin with no injections or an undefined ratio is reported, never a silent PASS
    for sign, gate, lab in ((1, "(a)", "dips (real arm)"), (-1, "(b)", "bumps (upside-down arm)")):
        out.append(f"{gate} {lab}: tier-1 recovery, injected before the mask / after the mask = m (mark: at least 0.95 per bin); counts are injections")
        per_bin = {}
        for b in order:
            g = inj[(inj.sign == sign) & (inj.bin == b)]
            bf, af = g[g["mode"] == "before"], g[g["mode"] == "after"]
            if not len(af):
                per_bin[b] = None
                out.append(f"   {b:>9} d: no injections"); continue
            rb, ra = bf.tier1.mean(), af.tier1.mean()
            m = rb / ra if ra > 0 else np.nan
            byK = "; ".join(f"K{k:g} {bf[bf.K == k].tier1.mean() / max(af[af.K == k].tier1.mean(), 1e-9):.2f}" for k in KS)
            out.append(f"   {b:>9} d: before {100 * rb:3.0f}% ({int(bf.tier1.sum())}/{len(bf)}), after {100 * ra:3.0f}% ({int(af.tier1.sum())}/{len(af)}), m = {('%.2f' % m) if m == m else 'n/a (nothing found even after the mask, not judged)'} ({byK}); lost to the veto: {int(bf.vetoed.sum())} of {len(bf)}")
            per_bin[b] = float(m)
        status, line = judge(per_bin, 0.95)
        ok[sign] = status != "FAIL"
        out.append(f"{gate} {line}")
    out += exchange()
    OUT.write_text("\n".join(out), encoding="utf-8"); print("\n".join(out))


def exchange():
    """Gates (c) and (d) on the stored development run of the seen stars (nothing planted): tier-1 real / upside-down primary events per period bin, and events vetoed. Counts only."""
    ev, _ = R.load(str(X.RUN / "groups"))
    ev = ev[ev.primary & ev["p1_P"].notna()].copy()
    ev["bin"] = [binlab(p) for p in ev.p1_P]
    t1 = ev[ev.tier.isin(X.TIER1)]
    out = ["(c) exchangeability, nothing planted: tier-1 real / upside-down primary events per binary-period bin (mark 0.67 to 1.5 where a bin has 20 or more events; bins with fewer are not judged; "
           "G3 over 27.4 d is a KNOWN LIMIT, reported apart)"]
    c_ok = True
    for lo, hi in BINS:
        b = f"{lo:g}-{hi:g}" if hi < 1e8 else f"over {lo:g}"
        g = t1[t1.bin == b]; r, f = int((g.kind == "real").sum()), int((g.kind == "flip").sum()); ratio = r / max(f, 1)
        judged = r + f >= 20; known = DS.NAME == "g3" and hi > 1e8
        verdict = "not judged (under 20 events)" if not judged else ("known limit" if known else ("inside" if 0.67 <= ratio <= 1.5 else "OUTSIDE"))
        c_ok &= (not judged) or known or 0.67 <= ratio <= 1.5
        out.append(f"   {b:>9} d: real {r}, upside-down {f}, ratio {ratio:.2f}: {verdict}")
    out.append(f"(c) {'PASS' if c_ok else 'FAIL (a failed bin is labelled not covered; the search still runs)'}")
    v = ev[ev.get("p1_veto", False) == True]
    out.append(f"(d) events vetoed (flagged to tier 2) among primary events: real {int((v.kind == 'real').sum())}, upside-down {int((v.kind == 'flip').sum())}; "
               f"tier-1 events in recovered light: real {int(((t1.kind == 'real') & (t1.recovered == True)).sum())}, upside-down {int(((t1.kind == 'flip') & (t1.recovered == True)).sum())}")
    return out


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(int(sys.argv[2]), int(sys.argv[3]))
    else:
        summary()
