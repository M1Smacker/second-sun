"""The ONE way to run Re-search 1 with Petrova 1.0.0 (research/stage3/R1-PREREGISTRATION.md). A wrapper that lives OUTSIDE the hashed file list, modelled on g3_run.py.
Petrova 1.0.0 = Vesper 0.8.1 (0.8.0 = 0.7.1 + c6) plus the study switch p1 (pipeline/petrova_mask.py: catalogue windows, within-sector repeat lane, event-stage cross-sector veto; recovered light recorded
per event). The switch is dormant unless VESPER_OPTS names it, and the p1-off proofs (zero-diff-P1-off*.txt) show that the other code is unchanged.
It refuses to do anything unless: SS_SET is g2 or g3 (G1 follows by a later amendment), VESPER_OPTS is exactly c6,p1, and (except in `dev`) the rules-and-code hash of the code on disk equals the frozen hash in
research/stage3/SETTINGS_FROZEN_P100.json.
Strata (column design_seen of targets/r1_targets.csv): `seen` = stars in a mask-design sample (the dry run, bug fixes only); `unseen` = never looked at (the sealed run, ONE shot).
Modes:  python r1_run.py check <stratum>      guard + prerequisites; changes nothing, reads no light curve
        python r1_run.py dev <stratum> N      DEVELOPMENT run before the freeze (seen stars only): no freeze, no go file; folder r1dev_<stratum>_<hash12>; used for the gates
        python r1_run.py freeze               once: write SETTINGS_FROZEN_P100.json after the settings check, the p1-off proofs (300 of 300) and the gate results; needs a committed tree
        python r1_run.py run <stratum> N      the frozen run with N workers; ALSO needs research/stage3/R1-GO-<stratum>.txt (written only after the go)
Set OMP_NUM_THREADS, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS, NUMBA_NUM_THREADS to 1; Normal priority (Ahmed, 11 Nov 2026: the hunt may always use 70 percent of the CPU)."""
import os, sys, json, pathlib, datetime
import pandas as pd

if os.environ.get("SS_SET") not in ("g2", "g3"):
    sys.exit("SS_SET must be g2 or g3 (G1 follows by a later amendment)")
import dataset as DS, vopts as V, stage3 as S3, stage3_core as C, stage2_search as S2

STAGE3 = C.ROOT / "research" / "stage3"
FROZEN81, FROZENP, R1LIST = STAGE3 / "SETTINGS_FROZEN_V81.json", STAGE3 / "SETTINGS_FROZEN_P100.json", C.ROOT / "targets" / "r1_targets.csv"
R1_LIST_SHA = "01d6d71a5b709cb68360acc409cfb5c04259fee3e680070b1662934941a0e0de"        # fixed in R1-PREREGISTRATION.md section 2
DROP = ("stars", "manifest", "targets", "best_product", "base_run")        # data-dependent keys, left out of the version hash exactly as in g3_run.py
CHANGED_FILES = {"stage2_search.py", "stage3_core.py", "stage3_report.py", "stage3.py", "vopts.py", "petrova_mask.py"}     # code that differs from 0.8.1; every change is dormant unless p1 is on
PROOFS = ("zero-diff-P1-off.txt", "zero-diff-P1-off-c6.txt", "zero-diff-P1-off-g2-sealed-c6.txt")     # the p1-off proofs: G1 chain with options off and with c6, the stored sealed G2 chain with c6
GATES = ("R1-GATE-RESULT-g2.txt", "R1-GATE-RESULT-g3.txt")                   # written by r1_gate.py summary; each must contain "(a) PASS" and "(b) PASS"
norm = lambda x: json.loads(json.dumps(x, default=str))


def stars_file(stratum):
    """Write the star list of this set and stratum in the format stage3.search expects (tic, kic, tmag, morph) and return its path."""
    if stratum not in ("seen", "unseen"):
        sys.exit("stratum must be seen or unseen")
    if C.sha(R1LIST) != R1_LIST_SHA:
        sys.exit("REFUSED: targets/r1_targets.csv does not hash to the value fixed in the preregistration")
    r1 = pd.read_csv(R1LIST, comment="#")
    r1 = r1[(r1["list"] == DS.NAME) & (r1["design_seen"] == (1 if stratum == "seen" else 0))].drop_duplicates("tic")
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic")
    st = tg[tg.tic.isin(r1.tic)][["tic", "kic", "tmag", "morph"]]
    if len(st) != len(r1):
        sys.exit(f"the star list and the chain targets disagree: {len(r1)} stars in the list, {len(st)} found in {C.TARGETS.name}")
    DS.PREP.mkdir(parents=True, exist_ok=True)
    p = DS.PREP / f"r1_{DS.NAME}_{stratum}_stars_LOCAL.csv"; st.to_csv(p, index=False)
    return p


def settings(stars):
    if V.ON != frozenset({"c6", "p1"}):
        sys.exit(f"VESPER_OPTS must be exactly c6,p1, not {sorted(V.ON)}")
    real_sha = C.sha
    C.sha = lambda p: real_sha(p) if pathlib.Path(p).exists() else "missing"
    try:
        s = {k: v for k, v in S3.current_settings(stars).items() if k not in DROP}
    finally:
        C.sha = real_sha
    return s, C.settings_hash(s)


def freeze():
    if FROZENP.exists():
        sys.exit(f"already frozen: {FROZENP}")
    st = stars_file("seen"); s, h = settings(st); pv = S3.provenance()
    if pv["pipeline_dirty"]:
        sys.exit("pipeline or targets have uncommitted changes: commit first, then freeze")
    f81 = json.load(open(FROZEN81)); a, b = norm(s), f81["settings"]
    other = sorted(k for k in set(a) | set(b) if k not in ("code", "options") and a.get(k) != b.get(k))
    changed = sorted(k for k in set(a["code"]) | set(b["code"]) if a["code"].get(k) != b["code"].get(k))
    if other or set(changed) != CHANGED_FILES or a["options"] != ["c6", "p1"]:
        sys.exit(f"Petrova 1.0.0 must equal Vesper 0.8.1 except options c6,p1 and the code of {sorted(CHANGED_FILES)}: other settings differ {other}; code files that differ {changed}; options {a['options']}")
    for name in PROOFS:
        t = (STAGE3 / name).read_text(encoding="utf-8") if (STAGE3 / name).exists() else ""
        if not ("equal to the frozen group files: 300 of 300" in t and "stage3_report.load of the frozen run: 300 of 300" in t and "Errors: 0. Star-sectors that differ: 0." in t):
            sys.exit(f"p1-off proof missing or not 300 of 300 with no difference: {name}")
    for name in GATES:
        t = (STAGE3 / name).read_text(encoding="utf-8") if (STAGE3 / name).exists() else ""
        if not ("(a) PASS" in t and "(b) PASS" in t):
            sys.exit(f"gate result missing or not passing (a) and (b): {name}")
    FROZENP.write_text(json.dumps(dict(version="Petrova 1.0.0", based_on="Vesper 0.8.1", based_on_hash=f81["hash"], hash=h, options=["c6", "p1"], code_files_changed_from_0_8_1=changed, p1_off_proofs=list(PROOFS), gates=list(GATES),
                                        every_other_setting_equal_to_0_8_1=True, r1_list_sha256=R1_LIST_SHA, settings=s, provenance=pv), indent=1), encoding="utf-8")
    print("FROZEN Petrova 1.0.0", h, "| differs from Vesper 0.8.1 only in:", changed)


def guard(stratum, dev=False):
    st = stars_file(stratum); s, h = settings(st)
    if dev:
        if stratum != "seen":
            sys.exit("the development run is for the seen stars only")
        print(f"dev guard ok: {DS.NAME} {stratum}, settings hash {h[:12]} (NOT frozen)", flush=True)
        return st, s, h
    if not FROZENP.exists():
        sys.exit("not frozen: run `r1_run.py freeze` first")
    fz = json.load(open(FROZENP))
    if h != fz["hash"]:
        sys.exit(f"REFUSED: the code and settings on disk hash to {h[:12]}, the frozen Petrova 1.0.0 hash is {fz['hash'][:12]}")
    print(f"guard ok: Petrova 1.0.0, hash {h[:12]} equals the frozen hash; {DS.NAME} {stratum} stars: {len(pd.read_csv(st))}", flush=True)
    return st, s, h


def prereq(stars_csv):
    ok = True
    stars = pd.read_csv(stars_csv).tic.astype(int).tolist()
    missing = [t for t in stars if not (DS.DATA / str(t) / "_done").exists()]
    parts = list(DS.DATA.rglob("*.part"))
    print(f"download: {len(stars) - len(missing)} of {len(stars)} stars finished; {len(parts)} unfinished .part files", flush=True); ok &= not missing and not parts
    fits = {p.name: int(p.parent.name) for t in stars for p in (DS.DATA / str(t)).glob("*.fits")}
    print(f"files on disk: {len(fits)}", flush=True)
    audit = pd.read_csv(DS.AUDIT / "audit_all.csv")
    got = audit[audit.file.isin(fits)]; bad = got[got.status.astype(str).str.startswith("ERROR")]
    print(f"audit rows: {len(got)} of {len(fits)} ({len(bad)} errors)", flush=True); ok &= len(got) == len(fits) and len(bad) == 0
    nb = pd.read_csv(DS.BEST); nb = nb[nb.tic.isin(stars)]
    print(f"best-product table: {len(nb)} star-sectors from {nb.tic.nunique()} stars", flush=True); ok &= len(nb) > 0
    import petrova_mask as PM
    cat = PM.cat(); inn = [t for t in stars if t in cat and pd.notna(cat[t]["wp"])]
    print(f"catalogue: {len(inn)} of {len(stars)} stars have an ephemeris and an eclipse width for the Petrova mask; the others use the repeat lane alone", flush=True)
    return ok


def run_search(stars, dst, n, h, s, pv, extra):
    dst.mkdir(parents=True, exist_ok=True)
    hashes = dict(r1_targets=C.sha(R1LIST), stars=C.sha(stars), targets=C.sha(C.TARGETS), manifest=C.sha(DS.MANIFEST), best_product=C.sha(DS.BEST), audit=C.sha(DS.AUDIT / "audit_all.csv"))
    (dst / "settings.json").write_text(json.dumps(dict(hash=h, settings=s, provenance=pv, data_hashes=hashes, **extra), indent=1), encoding="utf-8")
    with open(dst / "starts.log", "a") as f:
        f.write(datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds") + f" start, {n} workers, git {pv['git_commit'][:7]}\n")
    S2.STARS = stars
    gl = S2.groups(); (dst / "watch_plan.json").write_text(json.dumps(dict(groups=len(gl), sap=len(S3.sap_pass_groups(gl)), stars=len({g[0] for g in gl}))))
    print("SEARCH", h[:12], "->", dst, flush=True)
    S3.search(stars, dst, DS.NAME, n, C.GRID_V5)                          # PDCSAP / QLP products, second-product check, flags
    S3.search(stars, dst, DS.NAME + "sap", n, C.GRID_V5, sap=True)        # the SAP twins of the best product
    (dst / "v7.json").write_text(json.dumps(S3.V7), encoding="utf-8")
    S3.pdc_pass(dst, stars, n)                                            # the PDCSAP check
    print("SEARCH DONE", flush=True)


def main():
    mode = sys.argv[1]
    if mode == "freeze":
        return freeze()
    stratum = sys.argv[2]
    if mode == "check":
        st, s, h = guard(stratum, dev=not FROZENP.exists() and stratum == "seen")
        sys.exit(0 if prereq(st) else "prerequisites NOT met")
    n = int(sys.argv[3])
    pv = S3.provenance()
    if mode == "dev":
        st, s, h = guard(stratum, dev=True)
        if not prereq(st):
            sys.exit("prerequisites NOT met")
        return run_search(st, DS.RUNS / f"r1dev_{DS.NAME}_{stratum}_{h[:12]}", n, h, s, pv, dict(mode="development, before the freeze"))
    st, s, h = guard(stratum)
    go = STAGE3 / f"R1-GO-{stratum}.txt"
    if not go.exists():
        sys.exit(f"REFUSED: {go} does not exist. This run needs the explicit go; the file is written only after it is given.")
    if not prereq(st):
        sys.exit("prerequisites NOT met: the search does not start")
    if pv["pipeline_dirty"]:
        sys.exit("pipeline or targets have uncommitted changes: commit first")
    dst = DS.RUNS / f"r1_{DS.NAME}_{stratum}_{h[:12]}"
    if stratum == "unseen" and dst.exists() and any(dst.glob("groups/*.json")):
        print("note: the sealed run folder already has groups; a crashed run resumes with the same hash, a finished one is never repeated", flush=True)
    run_search(st, dst, n, h, s, pv, dict(frozen=str(FROZENP), go=go.read_text(encoding="utf-8"), stratum=stratum))


if __name__ == "__main__":
    main()
