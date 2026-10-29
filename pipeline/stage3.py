"""Stage 3 wrapper (Phase E1). WRAPS stage2_search.py WITHOUT EDITING IT: the search code, thresholds and detector are the ones Stage 2 ran (checked identical to
detect_v2.find_events). What changes: the output folder is named by the hash of the frozen settings (never data\\stage2), and every event gets C5, the
second-product state, the QLP-only label and a tier. Real events stay in D:\\second-sun\\data (git-ignored); publish aggregates only.
NOTHING SEARCHES UNTIL YOU CALL `dry` (5 known hosts) OR `run` (all stars, only after `freeze`, which needs Ahmed's go: "start the search").
Usage: python stage3.py settings | stars | dry [n] | sapdry [n] | pdcdry [n] | freeze | run [n]"""
import sys, json, shutil, subprocess, pathlib, datetime, multiprocessing as mp
import numpy as np
import pandas as pd
import stage2_search as S2
import detect_v2 as D
import stage3_core as C
import sap_twin as T
import dataset as DS

PREP = DS.PREP                          # dataset.py: G1 by default (data/stage3_prep, data/stage3), G2 when SS_SET=g2
DRY = C.ROOT / "data" / "stage3_dry"
RUN = DS.RUNS
FROZEN = C.ROOT / "research" / "stage3" / "SETTINGS_FROZEN.json"
STARS_ALL = PREP / "stage3_stars_LOCAL.csv"
BASE = "f366d3682843"                  # v7 = this frozen v6 run (the v5 search plus the SAP twin pass), both folders copied unchanged; v7 adds two flags and one measurement, no new search
V7 = dict(common_d=C.COMMON_D, common_n=C.COMMON_N, pdc_min=C.PDC_MIN)
S3 = {}


def git(*a):
    return subprocess.run(["git", "-C", str(C.ROOT), *a], capture_output=True, text=True).stdout.strip()


def current_settings(stars_csv):
    code = {f: C.sha(C.ROOT / "pipeline" / f) for f in ("stage2_search.py", "detect_v2.py", "audit_all.py", "audit_paths.py", "common_time.py",
                                                       "stage3_core.py", "stage3.py", "sap_twin.py", "stage3_report.py", "dataset.py")}
    return dict(base_run=BASE, v7=dict(V7, common_moment="a dip is flagged if 3 or more OTHER stars have a primary event of EITHER kind within 0.1 d at the same sector and camera (stage3_core.common_moment_n); "
                                                          "it replaces the Stage 2 burst flag in the tiers, which counted only upside-down events",
                                       pdc_check="a SAP-only dip whose PDCSAP flux (same file, same box length, nothing filled from SAP: sap_twin.load_pdc) shows SNR under pdc_min is tier 3; not measurable (PDC dropped those cadences) means no judgement (stage3.pdc_pass writes pdc_snr into groups_sap)"),
                sap_twin="v6: the SAP flux (crowding fixed, hard quality mask, nothing filled) of every SPOC and TESS-SPOC file in star-sectors whose best product is one of them, "
                                        "searched with the v5 settings; a dip PDCSAP also found keeps its v5 version, a SAP-only dip is added (merge in stage3_report.load)",
                snr_threshold=7.0, durs_h=list(C.GRID_V5), bin_d=getattr(D, "BIN_D", None), burst_d=S2.BURST_D, flip_burst_min=S2.FLIP_BURST_MIN,
                c5_ph_d=C.PH_D, ecl_mtot=C.ECL_MTOT, ecl_rfac=C.ECL_RFAC, ecl_max_frac=C.ECL_MAX_FRAC, repeat_n=C.REPEAT_N, step_lift=C.STEP_LIFT, ramp_d=C.RAMP_D, dominance="strongest other-kind event in the same light curve >= this event", eb_widths=(C.sha(C.EBS) if C.EBS.exists() else None), step_cover=C.STEP_COVER, burst_min=C.BURST_MIN, c8_strict=C.C8_STRICT, c8_lenient=C.C8_LENIENT,
                injection="12 x 8 h noise, clipped to 1500..40000 ppm, 8 h wide, middle of the longest segment (stage2_search.do_group)",
                stars=C.sha(stars_csv), manifest=C.sha(C.MANIFEST), targets=C.sha(C.TARGETS), best_product=C.sha(C.BEST), code=code)


def provenance():
    return dict(git_commit=git("rev-parse", "HEAD"), pipeline_dirty=bool(git("status", "--porcelain", "--", "pipeline", "targets")),
                when=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))


def _init3(groups_dir, tag, grid, sap=False):
    S2._init()
    C.use_grid(S2, grid)                                         # v5: the box lengths are set here, not in the Stage 2 file
    T.install(S2)                                                # v6: paths ending in sap_twin.SUFFIX are read as SAP (no effect on any other path)
    S2.GROUPS = pathlib.Path(groups_dir)
    S3["tag"] = tag
    S3["ephem"] = C.Ephem(pd.read_csv(C.TARGETS, comment="#"), C.eb_widths())
    S3["qlp"] = C.qlp_only_tics()


def add_step(g, paths):
    """v3: measure the flux just before and after every event, in the same prepared flux the detector used (the search code is not touched)."""
    prods, cache = {}, {}
    for q in paths:
        try:
            d, _ = S2.prepare(q)
        except Exception:
            continue
        if d is not None:
            prods[d["meta"]["product"]] = d
    for e in g["events"]:
        d = prods.get(e["product"])
        if d is None:
            continue
        key = (e["product"], 1 if e["kind"] == "real" else -1)
        if key not in cache:
            cache[key] = S2.Prod(d["t"], d["f"], key[1])
        P = cache[key]
        e.update(C.step_stats(P.bt, P.bf, P.bd, P.med, e["center"], e["dur_h"], e["depth_ppm"]))
        ed = np.asarray(d["edges"], dtype=float); before = ed[ed <= e["center"]]              # latest data edge before the event = when data last resumed
        e["ramp_d"] = float(e["center"] - before.max()) if len(before) else None


def do_group3(args):
    p = S2.do_group(args)                                        # the unchanged Stage 2 search; writes its JSON into S2.GROUPS
    g = json.load(open(p))
    if g.get("stage3") != S3["tag"]:
        if g["events"]:
            add_step(g, args[2])
        g["events"] = C.enrich_group(g, S3["ephem"], S3["qlp"])
        g["stage3"] = S3["tag"]
        json.dump(g, open(p, "w"), default=lambda o: None if o != o else float(o))
    return str(p)


def safe3(a):
    try:
        return do_group3(a)
    except Exception as e:
        return f"ERROR {a[0]} {a[1]}: {type(e).__name__}: {str(e)[:100]}"


def sap_pass_groups(gl):
    """v6 second pass: which star-sector groups are searched again, and with which files (see sap_twin.twin_groups)."""
    best = pd.read_csv(C.BEST, usecols=["tic", "sector", "product"])
    man = pd.read_csv(C.MANIFEST).drop_duplicates("file")
    return T.twin_groups(gl, {(int(a), int(b)): c for a, b, c in zip(best.tic, best.sector, best["product"])}, dict(zip(man.file, man.author)))


def _init_pdc():
    S2._init(); C.use_grid(S2, C.GRID_V5); T.install(S2)


def add_pdc(a):
    """v7: for every event of the SAP twin of the best product, the SNR the PDCSAP flux of the SAME file shows at that time and box length (Prod.snr_near, the rule C8 measure), on the
    real curve for a real event and on the upside-down curve for an upside-down event. The PDCSAP curve is read with nothing filled from SAP (sap_twin.load_pdc). Written into the group JSON as
    `pdc_snr`; NaN where the PDCSAP curve has no score there (PDC dropped those cadences): then the check says nothing."""
    p, paths, best = a
    g = json.load(open(p))
    if g.get("pdc_check") == "v7u":
        return p
    prods = {}
    for q in paths:
        try:
            d, _ = S2.prepare(q + T.SUFFIX_PDC)
        except Exception:
            continue
        if d is not None:
            prods[d["meta"]["product"]] = d
    d = prods.get(best)
    if d is not None:
        P = {1: S2.Prod(d["t"], d["f"]), -1: S2.Prod(d["t"], d["f"], -1)}
        for e in g["events"]:
            if e["product"] == best + "-SAP":
                e["pdc_snr"] = P[1 if e["kind"] == "real" else -1].snr_near(e["center"], e["dur_h"])
    g["pdc_check"] = "v7u"
    json.dump(g, open(p, "w"), default=lambda o: None if o != o else float(o))
    return p


def safe_pdc(a):
    try:
        return add_pdc(a)
    except Exception as e:
        return f"ERROR {a[0]}: {type(e).__name__}: {str(e)[:100]}"


def pdc_pass(run_dir, stars_csv, n):
    """v7 measurement pass over run_dir/groups_sap (the SAP search is not repeated): which groups, with which PDCSAP files, comes from sap_pass_groups."""
    S2.STARS = pathlib.Path(stars_csv)
    best = pd.read_csv(C.BEST, usecols=["tic", "sector", "product"]); bp = {(int(a), int(b)): c for a, b, c in zip(best.tic, best.sector, best["product"])}
    todo = []
    for tic, sec, tw in sap_pass_groups(S2.groups()):
        f = pathlib.Path(run_dir) / "groups_sap" / f"{tic}_{sec}.json"
        if f.exists():
            todo.append((str(f), [q[:-len(T.SUFFIX)] for q in tw], bp[(int(tic), int(sec))]))
    print(f"{len(todo)} SAP groups get a PDCSAP check", flush=True)
    with mp.Pool(n, initializer=_init_pdc) as pool:
        for i, r in enumerate(pool.imap_unordered(safe_pdc, todo), 1):
            if r.startswith("ERROR"):
                print(r, flush=True)
            if i % 100 == 0:
                print(f"{i}/{len(todo)}", flush=True)
    print("PDC CHECK DONE", flush=True)


def search(stars_csv, out_dir, tag, n, grid=C.GRID_V5, sap=False):
    out_dir = pathlib.Path(out_dir); groups_dir = out_dir / ("groups_sap" if sap else "groups"); groups_dir.mkdir(parents=True, exist_ok=True)
    S2.STARS = pathlib.Path(stars_csv)
    gl = S2.groups()
    if sap:
        gl = sap_pass_groups(gl)
    st = pd.read_csv(stars_csv)
    if "batch" in st.columns:                                    # main batch first, 'shape unknown' batch last
        order = {int(t): (0 if b == "main" else 1) for t, b in zip(st.tic, st.batch)}
        gl.sort(key=lambda g: (order.get(g[0], 0), g[0], g[1]))
    print(f"{len(gl)} star-sector groups -> {groups_dir}", flush=True)
    with mp.Pool(n, initializer=_init3, initargs=(str(groups_dir), tag, tuple(grid), sap)) as pool:
        for i, r in enumerate(pool.imap(safe3, gl), 1):
            if r.startswith("ERROR"):
                print(r, flush=True)
            if i % 100 == 0:
                print(f"{i}/{len(gl)}", flush=True)
    print("STAGE3 SEARCH DONE", flush=True)


def build_stars():
    """All 549 stars; batch = 'main' unless morph = -1 and the eclipse check (shape_check.py) found no eclipse."""
    tg = pd.read_csv(C.TARGETS, comment="#")
    st = tg.drop_duplicates("tic")[["tic", "kic", "tmag", "morph"]].copy()
    sc = PREP / "shape_class_LOCAL.csv"
    cls = pd.read_csv(sc).set_index("tic")["class"] if sc.exists() else pd.Series(dtype=str)
    unk = (st.tic.map(cls) != "clear") & st.tic.isin(tg[tg.morph == -1].tic)
    st["batch"] = unk.map({True: "unknown", False: "main"})
    st["qlp_only"] = st.tic.isin(C.qlp_only_tics())
    PREP.mkdir(parents=True, exist_ok=True); st.to_csv(STARS_ALL, index=False)
    print(st.batch.value_counts().to_dict(), "qlp-only:", int(st.qlp_only.sum()), "->", STARS_ALL)


if __name__ == "__main__":
    mode = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    if mode == "settings":
        stars = STARS_ALL if STARS_ALL.exists() else S2.STARS
        s = current_settings(stars); print(json.dumps(s, indent=1)); print("HASH", C.settings_hash(s)); print(json.dumps(provenance()))
    elif mode == "stars":
        build_stars()
    elif mode == "dry":                                          # the 5 known hosts only, into a separate folder; regression check vs Stage 2
        DRY.mkdir(parents=True, exist_ok=True)
        st = pd.read_csv(S2.STARS); st[st.stratum == "control"].to_csv(DRY / "stars_dry.csv", index=False)
        search(DRY / "stars_dry.csv", DRY, "dry", n, C.GRID_V4)  # regression runs use the Stage 2 box lengths (v5 adds 20 h only in `run`)
    elif mode == "sapdry":                                       # v6 second pass on the 5 known hosts only, into the dry folder
        DRY.mkdir(parents=True, exist_ok=True)
        st = pd.read_csv(S2.STARS); st[st.stratum == "control"].to_csv(DRY / "stars_dry.csv", index=False)
        search(DRY / "stars_dry.csv", DRY, "sapdry", n, C.GRID_V5, sap=True)
    elif mode == "pdcdry":                                       # v7 measurement on the dry folder's groups_sap (run `sapdry` first)
        pdc_pass(DRY, DRY / "stars_dry.csv", n)
    elif mode == "dry50":                                        # all 50 Stage 2 stars into a separate folder: full regression against Stage 2
        search(S2.STARS, C.ROOT / "data" / "stage3_dry50", "dry50", n, C.GRID_V4)
    elif mode == "freeze":
        if FROZEN.exists():
            sys.exit(f"already frozen: {FROZEN}")
        if not STARS_ALL.exists():
            sys.exit("run `python stage3.py stars` first")
        s = current_settings(STARS_ALL); pv = provenance()
        if pv["pipeline_dirty"]:
            sys.exit("pipeline or targets have uncommitted changes: commit first, then freeze")
        FROZEN.parent.mkdir(exist_ok=True)
        FROZEN.write_text(json.dumps(dict(hash=C.settings_hash(s), settings=s, provenance=pv), indent=1), encoding="utf-8")
        print("FROZEN", C.settings_hash(s))
    elif mode == "devrun":                                       # G2 preregistration sections 3 and 4: the whole chain on the 301 DEVELOPMENT stars only (development use, any number of times)
        if DS.NAME != "g2":
            sys.exit("devrun needs SS_SET=g2")
        tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic")
        st = tg[tg["slice"] == "dev"][["tic", "kic", "tmag", "morph"]]
        assert len(st) == 301, f"the development slice must have 301 stars, not {len(st)}"
        PREP.mkdir(parents=True, exist_ok=True); dev_stars = PREP / "g2_dev_stars_LOCAL.csv"; st.to_csv(dev_stars, index=False)
        s = current_settings(dev_stars); s["base_run"] = None    # nothing is copied from a G1 run: both searches are made here
        h = C.settings_hash(s)[:12]; dst = RUN / f"dev_{h}"; dst.mkdir(parents=True, exist_ok=True)
        (dst / "settings.json").write_text(json.dumps(dict(hash=h, settings=s, provenance=provenance()), indent=1), encoding="utf-8")
        print("G2 DEVELOPMENT RUN", h, "->", dst, flush=True)
        search(dev_stars, dst, "dev", n, C.GRID_V5)              # the v5 half: PDCSAP / QLP products, second-product check, flags
        search(dev_stars, dst, "devsap", n, C.GRID_V5, sap=True) # the v6 half: SAP twins of the best product
        (dst / "v7.json").write_text(json.dumps(V7), encoding="utf-8")
        pdc_pass(dst, dev_stars, n)                              # the v7 PDCSAP check
    elif mode == "run":
        fz = json.loads(FROZEN.read_text(encoding="utf-8")) if FROZEN.exists() else sys.exit("not frozen: Ahmed has not said start")
        h = C.settings_hash(current_settings(STARS_ALL))
        if h != fz["hash"]:
            sys.exit(f"settings or code changed since the freeze ({h[:12]} vs {fz['hash'][:12]}): refusing to run")
        dst = RUN / h[:12]
        for sub in ("groups", "groups_sap"):                     # v7: the PDCSAP half (v5) and the SAP half (v6) ARE the frozen v6 run, copied byte for byte (not searched again)
            if not (dst / sub).exists():
                shutil.copytree(RUN / BASE / sub, dst / sub); print(f"copied {len(list((dst / sub).glob('*.json')))} {sub} files from {BASE}", flush=True)
        (dst / "v7.json").write_text(json.dumps(V7), encoding="utf-8")   # marks the folder: stage3_report.load applies the v7 flags
        pdc_pass(dst, STARS_ALL, n)
