"""The ONE way to search the 594 sealed G2 stars (preregistration section 3 and Amendment 1, 30 Oct 2026). A wrapper that lives OUTSIDE the hashed file list, so the frozen code is untouched.
It refuses to do anything unless: SS_SET=g2, VESPER_OPTS is exactly c6 (Vesper 0.8.0 = 0.7.1 + c6), and the rules-and-code hash of the code on disk equals the frozen v8 hash in
research/stage3/SETTINGS_FROZEN_V8.json (5f73692944aa...). It then runs exactly what `stage3.py devrun` runs on the development slice: the search, the SAP twin pass, the v7 marker and the PDCSAP check.
Modes:  python sealed_run.py check            guard + prerequisites (download complete, audit tables cover the sealed files, ephemeris present); changes nothing, reads no light curve
        python sealed_run.py run N [--watch]  the one sealed search with N workers; --watch also starts the BLIND Search window exporter (watch_export.py --blind --loop 60 --push)
Resumable: a group already written is skipped (stage2_search.do_group), so a crashed run continues with the same hash. A fixed version has a different hash and a different folder; both are then reported.
Set OMP_NUM_THREADS, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS, NUMBA_NUM_THREADS to 1 and run at BelowNormal priority, as for every heavy job."""
import os, sys, json, csv, pathlib, subprocess, datetime
import pandas as pd

if os.environ.get("SS_SET") != "g2":
    sys.exit("SS_SET must be g2")
import dataset as DS, vopts as V, stage3 as S3, stage3_core as C, stage2_search as S2

FROZEN8 = C.ROOT / "research" / "stage3" / "SETTINGS_FROZEN_V8.json"
SEALED_STARS = DS.PREP / "g2_sealed_stars_LOCAL.csv"
DROP = ("stars", "manifest", "targets", "best_product", "base_run")        # data-dependent keys, left out of the version hash exactly as in `stage3.py freeze8`


def guard():
    if V.ON != frozenset({"c6"}):
        sys.exit(f"VESPER_OPTS must be exactly c6 for v8, not {sorted(V.ON)}")
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic")
    st = tg[tg["slice"] == "sealed"][["tic", "kic", "tmag", "morph"]]
    if len(st) != 594:
        sys.exit(f"the sealed slice must have 594 stars, found {len(st)}")
    DS.PREP.mkdir(parents=True, exist_ok=True); st.to_csv(SEALED_STARS, index=False)
    s = {k: v for k, v in S3.current_settings(SEALED_STARS).items() if k not in DROP}
    h = C.settings_hash(s); fz = json.load(open(FROZEN8))
    if h != fz["hash"]:
        sys.exit(f"REFUSED: the code and settings on disk hash to {h[:12]}, the frozen v8 hash is {fz['hash'][:12]}")
    print(f"guard ok: Vesper 0.8.0, hash {h[:12]} equals the frozen v8 hash; 594 sealed stars", flush=True)
    return st, s, h


def prereq():
    ok = True
    stars = pd.read_csv(SEALED_STARS).tic.astype(int).tolist()
    missing = [t for t in stars if not (DS.DATA / str(t) / "_done").exists()]
    parts = list(DS.DATA.rglob("*.part"))
    print(f"download: {len(stars) - len(missing)} of {len(stars)} sealed stars finished; {len(parts)} unfinished .part files", flush=True); ok &= not missing and not parts
    fits = {p.name: int(p.parent.name) for t in stars for p in (DS.DATA / str(t)).glob("*.fits")}
    print(f"files on disk for the sealed stars: {len(fits)}", flush=True)
    audit = pd.read_csv(DS.AUDIT / "audit_all.csv")
    got = audit[audit.file.isin(fits)]
    bad = got[got.status.astype(str).str.startswith("ERROR")]
    print(f"audit rows for sealed files: {len(got)} of {len(fits)} ({len(bad)} errors; status {got.status.value_counts().head(4).to_dict()})", flush=True); ok &= len(got) == len(fits) and len(bad) == 0
    best = pd.read_csv(DS.BEST)
    nb = best[best.tic.isin(stars)]
    print(f"best-product table: {len(nb)} sealed star-sectors from {nb.tic.nunique()} stars", flush=True); ok &= len(nb) > 0
    pkl = DS.AUDIT / "spoc_windows.pkl"; newest = max((p.stat().st_mtime for t in stars for p in (DS.DATA / str(t)).glob("*.fits")), default=0)
    fresh = pkl.exists() and pkl.stat().st_mtime > newest
    print(f"spoc_windows.pkl newer than the newest sealed file: {fresh}", flush=True); ok &= fresh
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic"); tg = tg[tg.tic.isin(stars)]
    print(f"ephemeris: {int(tg.bjd0.notna().sum())} of {len(tg)} sealed stars have a catalogue BJD0", flush=True)
    return ok


def main():
    mode = sys.argv[1]
    st, s, h = guard()
    if mode == "check":
        sys.exit(0 if prereq() else "prerequisites NOT met")
    n = int(sys.argv[2])
    if not prereq():
        sys.exit("prerequisites NOT met: the sealed search does not start")
    dst = DS.RUNS / f"sealed_{h[:12]}"; dst.mkdir(parents=True, exist_ok=True)
    pv = S3.provenance()
    if pv["pipeline_dirty"]:
        sys.exit("pipeline or targets have uncommitted changes: commit first")
    (dst / "settings.json").write_text(json.dumps(dict(hash=h, settings=s, provenance=pv, frozen_v8=str(FROZEN8), preregistration_amendment="Amendment 1, 30 Oct 2026"), indent=1), encoding="utf-8")
    with open(dst / "starts.log", "a") as f:
        f.write(datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds") + f" start, {n} workers, git {pv['git_commit'][:7]}\n")
    S2.STARS = SEALED_STARS
    gl = S2.groups(); (dst / "watch_plan.json").write_text(json.dumps(dict(groups=len(gl), sap=len(S3.sap_pass_groups(gl)), stars=len({g[0] for g in gl}))))
    watcher = None
    if "--watch" in sys.argv:
        watcher = subprocess.Popen([sys.executable, str(pathlib.Path(__file__).with_name("watch_export.py")), str(dst), "--blind", "--loop", "60", "--push",
                                    "--label", "SEALED RUN: Vesper 0.8.0 on the 594 sealed G2 stars (blind)"])
    print("SEALED G2 SEARCH", h[:12], "->", dst, flush=True)
    S3.search(SEALED_STARS, dst, "sealed", n, C.GRID_V5)                  # the v5 half: PDCSAP / QLP products, second-product check, flags
    S3.search(SEALED_STARS, dst, "sealedsap", n, C.GRID_V5, sap=True)     # the v6 half: SAP twins of the best product
    (dst / "v7.json").write_text(json.dumps(S3.V7), encoding="utf-8")
    S3.pdc_pass(dst, SEALED_STARS, n)                                     # the v7 PDCSAP check
    print("SEALED SEARCH DONE", flush=True)
    if watcher:
        try: watcher.wait(timeout=300)
        except subprocess.TimeoutExpired: watcher.terminate(); print("page exporter did not stop by itself: stopped by sealed_run", flush=True)


if __name__ == "__main__":
    main()
