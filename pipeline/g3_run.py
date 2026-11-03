"""The ONE way to search the 612 G3 stars (research/stage3/G3-PREREGISTRATION.md and its Amendment 1, 3 Nov 2026). A wrapper that lives OUTSIDE the hashed file list, modelled on sealed_run.py.
Vesper 0.8.1 = Vesper 0.8.0 (0.7.1 + c6) with the G3 data paths added in dataset.py, audit_all.py and stage3_core.py, and the dormant 0.9 study switches (dg, nd, fl; off under c6) that were added to
stage3.py, stage3_core.py and vopts.py on 2 Nov; no rule changed (proofs: research/stage3/zero-diff-0.8.1.txt on G1 and zero-diff-0.8.1-g2-sealed-c6.txt on the stored sealed G2 run).
It refuses to do anything unless: SS_SET=g3, VESPER_OPTS is exactly c6, and the rules-and-code hash of the code on disk equals the frozen v8.1 hash in research/stage3/SETTINGS_FROZEN_V81.json.
Modes:  python g3_run.py freeze           once: write SETTINGS_FROZEN_V81.json after proving the settings equal the frozen v8 settings except the code of five files and both zero-difference proofs read 300 of 300; needs a committed tree
        python g3_run.py check            guard + prerequisites (download complete, audit tables cover every file, hashed union windows table, ephemeris); changes nothing, reads no light curve
        python g3_run.py run N            the one G3 search with N workers; ALSO needs research/stage3/G3-GO.txt (Ahmed's explicit go, written only after he says it)
Resumable: a group already written is skipped (stage2_search.do_group), so a crashed run continues with the same hash. A fixed version has a different hash and a different folder; both are then reported.
Set OMP_NUM_THREADS, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS, NUMBA_NUM_THREADS to 1 and run at BelowNormal priority (or Normal while Ahmed is away), as for every heavy job."""
import os, sys, json, pathlib, datetime
import pandas as pd

if os.environ.get("SS_SET") != "g3":
    sys.exit("SS_SET must be g3")
import dataset as DS, vopts as V, stage3 as S3, stage3_core as C, stage2_search as S2

STAGE3 = C.ROOT / "research" / "stage3"
FROZEN8, FROZEN81, GO = STAGE3 / "SETTINGS_FROZEN_V8.json", STAGE3 / "SETTINGS_FROZEN_V81.json", STAGE3 / "G3-GO.txt"
G3_STARS = DS.PREP / "g3_stars_LOCAL.csv"
UNION_REC = STAGE3 / "g3-union-windows.json"
DROP = ("stars", "manifest", "targets", "best_product", "base_run")        # data-dependent keys, left out of the version hash exactly as in `stage3.py freeze8`
DATA_PATH_FILES = {"dataset.py", "audit_all.py", "stage3_core.py"}         # changed by the 0.8.1 patch (G3 data paths, ephemeris and eclipse widths)
DORMANT_STUDY_FILES = {"stage3.py", "vopts.py", "stage3_core.py"}          # changed on 2 Nov by the 0.9 study: switches dg, nd, fl, OFF unless VESPER_OPTS names them (nothing writes their keys otherwise)
PROOFS = ("zero-diff-0.8.1.txt", "zero-diff-0.8.1-c6.txt", "zero-diff-0.8.1-g2-sealed-c6.txt")      # G1 chain with options off and with c6 against the stored v7 run (as the 0.8.0 regression of 30 Oct); G2 sealed chain with c6 against the stored 0.8.0 sealed run
norm = lambda x: json.loads(json.dumps(x, default=str))


def settings():
    if V.ON != frozenset({"c6"}):
        sys.exit(f"VESPER_OPTS must be exactly c6, not {sorted(V.ON)}")
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic")
    if len(tg) != 612 or set(tg["slice"]) != {"g3"}:
        sys.exit(f"the G3 table must have 612 stars of slice g3, found {len(tg)}")
    DS.PREP.mkdir(parents=True, exist_ok=True); tg[["tic", "kic", "tmag", "morph"]].to_csv(G3_STARS, index=False)
    real_sha = C.sha                                                       # the data-dependent keys (dropped below) may not exist yet when the version is frozen, before the audit tables are made
    C.sha = lambda p: real_sha(p) if pathlib.Path(p).exists() else "missing"
    try:
        s = {k: v for k, v in S3.current_settings(G3_STARS).items() if k not in DROP}
    finally:
        C.sha = real_sha
    return s, C.settings_hash(s)


def freeze():
    if FROZEN81.exists():
        sys.exit(f"already frozen: {FROZEN81}")
    s, h = settings(); pv = S3.provenance()
    if pv["pipeline_dirty"]:
        sys.exit("pipeline or targets have uncommitted changes: commit first, then freeze")
    f8 = json.load(open(FROZEN8)); a, b = norm(s), f8["settings"]
    other = sorted(k for k in set(a) | set(b) if k != "code" and a.get(k) != b.get(k))
    changed = sorted(k for k in set(a["code"]) | set(b["code"]) if a["code"].get(k) != b["code"].get(k))
    if other or set(changed) != DATA_PATH_FILES | DORMANT_STUDY_FILES:
        sys.exit(f"0.8.1 must equal 0.8.0 except the code of {sorted(DATA_PATH_FILES | DORMANT_STUDY_FILES)}: other settings differ {other}; code files that differ {changed}")
    for name in PROOFS:
        t = (STAGE3 / name).read_text(encoding="utf-8") if (STAGE3 / name).exists() else ""
        if not ("equal to the frozen group files: 300 of 300" in t and "stage3_report.load of the frozen run: 300 of 300" in t and "Errors: 0. Star-sectors that differ: 0." in t):
            sys.exit(f"proof missing or not 300 of 300 with no difference: {name}")
    FROZEN81.write_text(json.dumps(dict(version="Vesper 0.8.1", based_on="Vesper 0.8.0", based_on_hash=f8["hash"], hash=h, code_files_changed_from_0_8_0=changed, data_path_files=sorted(DATA_PATH_FILES), dormant_study_files=sorted(DORMANT_STUDY_FILES), proofs=list(PROOFS),
                                        every_other_setting_equal_to_0_8_0=True, settings=s, provenance=pv), indent=1), encoding="utf-8")
    print("FROZEN v8.1", h, "| differs from 0.8.0 only in:", changed)


def guard():
    if not FROZEN81.exists():
        sys.exit("not frozen: run `g3_run.py freeze` first")
    s, h = settings(); fz = json.load(open(FROZEN81))
    if h != fz["hash"]:
        sys.exit(f"REFUSED: the code and settings on disk hash to {h[:12]}, the frozen v8.1 hash is {fz['hash'][:12]}")
    print(f"guard ok: Vesper 0.8.1, hash {h[:12]} equals the frozen v8.1 hash; 612 G3 stars", flush=True)
    return s, h


def prereq():
    ok = True
    stars = pd.read_csv(G3_STARS).tic.astype(int).tolist()
    missing = [t for t in stars if not (DS.DATA / str(t) / "_done").exists()]
    parts = list(DS.DATA.rglob("*.part"))
    print(f"download: {len(stars) - len(missing)} of {len(stars)} stars finished; {len(parts)} unfinished .part files", flush=True); ok &= not missing and not parts
    fits = {p.name: int(p.parent.name) for t in stars for p in (DS.DATA / str(t)).glob("*.fits")}
    print(f"files on disk: {len(fits)}", flush=True)
    audit = pd.read_csv(DS.AUDIT / "audit_all.csv")
    got = audit[audit.file.isin(fits)]; bad = got[got.status.astype(str).str.startswith("ERROR")]
    print(f"audit rows: {len(got)} of {len(fits)} ({len(bad)} errors; status {got.status.value_counts().head(4).to_dict()})", flush=True); ok &= len(got) == len(fits) and len(bad) == 0
    nb = pd.read_csv(DS.BEST); nb = nb[nb.tic.isin(stars)]
    print(f"best-product table: {len(nb)} star-sectors from {nb.tic.nunique()} stars", flush=True); ok &= len(nb) > 0
    rec = json.load(open(UNION_REC)); on_disk = C.sha(DS.AUDIT / "spoc_windows.pkl")
    print(f"reference windows table: sha256 {on_disk[:16]} equals the recorded union table {rec['union']['sha256'][:16]}: {on_disk == rec['union']['sha256']}", flush=True); ok &= on_disk == rec["union"]["sha256"]
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic")
    print(f"ephemeris: {int(tg.bjd0.notna().sum())} of {len(tg)} stars have a catalogue BJD0; eclipse widths for {len(C.eb_widths())}; radius for {int((tg.tic_radius_rsun > 0).sum())}", flush=True)
    return ok


def main():
    mode = sys.argv[1]
    if mode == "freeze":
        return freeze()
    s, h = guard()
    if mode == "check":
        sys.exit(0 if prereq() else "prerequisites NOT met")
    n = int(sys.argv[2])
    if not GO.exists():
        sys.exit(f"REFUSED: {GO} does not exist. The G3 search needs Ahmed's explicit go; the file is written only after he says it.")
    if not prereq():
        sys.exit("prerequisites NOT met: the G3 search does not start")
    pv = S3.provenance()
    if pv["pipeline_dirty"]:
        sys.exit("pipeline or targets have uncommitted changes: commit first")
    dst = DS.RUNS / f"g3_{h[:12]}"; dst.mkdir(parents=True, exist_ok=True)
    hashes = dict(union_windows=C.sha(DS.AUDIT / "spoc_windows.pkl"), g3_targets=C.sha(C.TARGETS), g3_list=C.sha(DS.TIC_LIST), manifest=C.sha(DS.MANIFEST),
                  manifest_fingerprint=C.sha(DS.DATA / "manifest_fp.csv"), best_product=C.sha(DS.BEST), audit=C.sha(DS.AUDIT / "audit_all.csv"))
    (dst / "settings.json").write_text(json.dumps(dict(hash=h, settings=s, provenance=pv, frozen_v81=str(FROZEN81), data_hashes=hashes, go=GO.read_text(encoding="utf-8")), indent=1), encoding="utf-8")
    with open(dst / "starts.log", "a") as f:
        f.write(datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds") + f" start, {n} workers, git {pv['git_commit'][:7]}\n")
    S2.STARS = G3_STARS
    gl = S2.groups(); (dst / "watch_plan.json").write_text(json.dumps(dict(groups=len(gl), sap=len(S3.sap_pass_groups(gl)), stars=len({g[0] for g in gl}))))
    print("G3 SEARCH", h[:12], "->", dst, flush=True)
    S3.search(G3_STARS, dst, "g3", n, C.GRID_V5)                          # the v5 half: PDCSAP / QLP products, second-product check, flags
    S3.search(G3_STARS, dst, "g3sap", n, C.GRID_V5, sap=True)             # the v6 half: SAP twins of the best product
    (dst / "v7.json").write_text(json.dumps(S3.V7), encoding="utf-8")
    S3.pdc_pass(dst, G3_STARS, n)                                         # the v7 PDCSAP check
    print("G3 SEARCH DONE", flush=True)


if __name__ == "__main__":
    main()
