"""Phase E1(d): cheap eclipse check of the G1 rows with morph = -1 (eclipse shape not measured in the Villanova catalogue; 136 stars).
Uses the SAME automatic eclipse mask the search already uses (stage2_search.prepare -> eclipse_mask_auto at the catalogue period), on up to 3 light curves
per star (SPOC first, then TESS-SPOC, then QLP; one per sector). 'clear' = the mask found an eclipse run in at least one tested curve and joins the main
run; 'unknown' = tested, no run found, searched in the last batch; 'untested' = no curve could be prepared. Ahmed's recorded default (decisions.md 2026-10-20).
LOCAL output: data\\stage3_prep\\shape_class_LOCAL.csv. Prints counts only. Usage: python shape_check.py [n_procs]"""
import sys, multiprocessing as mp
import pandas as pd
import stage2_search as S2
import stage3_core as C

PREP = C.ROOT / "data" / "stage3_prep"
PRIO = {"SPOC": 0, "TESS-SPOC": 1, "QLP": 2}
MAN = pd.read_csv(C.MANIFEST).drop_duplicates("file")


def check_star(tic, max_files=3):
    m = MAN[MAN.tic == tic].copy()
    m["pr"] = m.author.map(PRIO).fillna(3); m["sec"] = m.file.str.extract(r"s(\d{4})-")[0]
    rows, seen = [], set()
    for r in m.sort_values(["pr", "sec"]).itertuples():
        if r.sec in seen:
            continue
        seen.add(r.sec)
        if len(rows) >= max_files:
            break
        try:
            d, meta = S2.prepare(r.path)
            rows.append(dict(tic=tic, file=r.file, author=r.author, status=meta["status"], n_runs=(sum(len(x) for _, x in d["runs"]) if d else 0)))
        except Exception as e:
            rows.append(dict(tic=tic, file=r.file, author=r.author, status=f"ERROR {type(e).__name__}", n_runs=0))
    return rows


def classify(rows):
    ok = [r for r in rows if r["status"] == "ok"]
    return "untested" if not ok else ("clear" if any(r["n_runs"] > 0 for r in ok) else "unknown")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    tg = pd.read_csv(C.TARGETS, comment="#")
    tics = sorted(int(t) for t in tg[tg.morph == -1].tic.unique())
    with mp.Pool(n, initializer=S2._init) as pool:
        res = pool.map(check_star, tics)
    files = pd.DataFrame([r for rows in res for r in rows])
    cls = pd.DataFrame(dict(tic=tics, **{"class": [classify(r) for r in res]}, n_tested=[sum(x["status"] == "ok" for x in r) for r in res]))
    PREP.mkdir(parents=True, exist_ok=True)
    cls.to_csv(PREP / "shape_class_LOCAL.csv", index=False); files.to_csv(PREP / "shape_files_LOCAL.csv", index=False)
    print(f"{len(tics)} stars with morph = -1;", cls["class"].value_counts().to_dict(), f"; curves tested {len(files)}; status {files.status.value_counts().to_dict()}")
