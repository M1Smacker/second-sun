"""Stage 3 wrapper (Phase E1). WRAPS stage2_search.py WITHOUT EDITING IT: the search code, thresholds and detector are the ones Stage 2 ran (checked identical to
detect_v2.find_events). What changes: the output folder is named by the hash of the frozen settings (never data\\stage2), and every event gets C5, the
second-product state, the QLP-only label and a tier. Real events stay in D:\\second-sun\\data (git-ignored); publish aggregates only.
NOTHING SEARCHES UNTIL YOU CALL `dry` (5 known hosts) OR `run` (all stars, only after `freeze`, which needs Ahmed's go: "start the search").
Usage: python stage3.py settings | stars | dry [n] | freeze | run [n]"""
import sys, json, subprocess, pathlib, datetime, multiprocessing as mp
import pandas as pd
import stage2_search as S2
import detect_v2 as D
import stage3_core as C

PREP = C.ROOT / "data" / "stage3_prep"
DRY = C.ROOT / "data" / "stage3_dry"
RUN = C.ROOT / "data" / "stage3"
FROZEN = C.ROOT / "research" / "stage3" / "SETTINGS_FROZEN.json"
STARS_ALL = PREP / "stage3_stars_LOCAL.csv"
S3 = {}


def git(*a):
    return subprocess.run(["git", "-C", str(C.ROOT), *a], capture_output=True, text=True).stdout.strip()


def current_settings(stars_csv):
    code = {f: C.sha(C.ROOT / "pipeline" / f) for f in ("stage2_search.py", "detect_v2.py", "audit_all.py", "audit_paths.py", "common_time.py",
                                                       "stage3_core.py", "stage3.py")}
    return dict(snr_threshold=7.0, durs_h=list(D.DURS_H), bin_d=getattr(D, "BIN_D", None), burst_d=S2.BURST_D, flip_burst_min=S2.FLIP_BURST_MIN,
                c5_ph_d=C.PH_D, ecl_mtot=C.ECL_MTOT, ecl_rfac=C.ECL_RFAC, ecl_max_frac=C.ECL_MAX_FRAC, repeat_n=C.REPEAT_N, step_lift=C.STEP_LIFT, step_cover=C.STEP_COVER, burst_min=C.BURST_MIN, c8_strict=C.C8_STRICT, c8_lenient=C.C8_LENIENT,
                injection="12 x 8 h noise, clipped to 1500..40000 ppm, 8 h wide, middle of the longest segment (stage2_search.do_group)",
                stars=C.sha(stars_csv), manifest=C.sha(C.MANIFEST), targets=C.sha(C.TARGETS), best_product=C.sha(C.BEST), code=code)


def provenance():
    return dict(git_commit=git("rev-parse", "HEAD"), pipeline_dirty=bool(git("status", "--porcelain", "--", "pipeline", "targets")),
                when=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))


def _init3(groups_dir, tag):
    S2._init()
    S2.GROUPS = pathlib.Path(groups_dir)
    S3["tag"] = tag
    S3["ephem"] = C.Ephem(pd.read_csv(C.TARGETS, comment="#"))
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


def search(stars_csv, out_dir, tag, n):
    out_dir = pathlib.Path(out_dir); groups_dir = out_dir / "groups"; groups_dir.mkdir(parents=True, exist_ok=True)
    S2.STARS = pathlib.Path(stars_csv)
    gl = S2.groups()
    st = pd.read_csv(stars_csv)
    if "batch" in st.columns:                                    # main batch first, 'shape unknown' batch last
        order = {int(t): (0 if b == "main" else 1) for t, b in zip(st.tic, st.batch)}
        gl.sort(key=lambda g: (order.get(g[0], 0), g[0], g[1]))
    print(f"{len(gl)} star-sector groups -> {groups_dir}", flush=True)
    with mp.Pool(n, initializer=_init3, initargs=(str(groups_dir), tag)) as pool:
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
        search(DRY / "stars_dry.csv", DRY, "dry", n)
    elif mode == "dry50":                                        # all 50 Stage 2 stars into a separate folder: full regression against Stage 2
        search(S2.STARS, C.ROOT / "data" / "stage3_dry50", "dry50", n)
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
    elif mode == "run":
        fz = json.loads(FROZEN.read_text(encoding="utf-8")) if FROZEN.exists() else sys.exit("not frozen: Ahmed has not said start")
        h = C.settings_hash(current_settings(STARS_ALL))
        if h != fz["hash"]:
            sys.exit(f"settings or code changed since the freeze ({h[:12]} vs {fz['hash'][:12]}): refusing to run")
        search(STARS_ALL, RUN / h[:12], h[:12], n)
