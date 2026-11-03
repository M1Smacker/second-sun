"""Vesper 0.8.1 self-checks (the G3 data-path patch; research/stage3/G3-PREREGISTRATION.md). Each check proves one claim the patch rests on. No G3 flux is read.
Run: .venv\\Scripts\\python.exe pipeline\\test_g3_prep.py   (from D:\\second-sun; needs git and the tables named below)
The patch edits dataset.py, audit_all.py and stage3_core.py. It must change nothing for SS_SET unset (g1) or g2, so the first check runs the OLD code (commit 85e14c1, the last before the patch)
and the NEW code side by side and compares paths, widths and tables."""
import json, os, pathlib, pickle, subprocess, sys, tempfile, hashlib

ROOT = pathlib.Path(r"D:\second-sun")
OLD = "85e14c1"
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
DIGEST = """
import json, hashlib, dataset as DS, stage3_core as C, audit_all as A
def h(x): return hashlib.sha256(json.dumps(x, sort_keys=True, default=str).encode()).hexdigest()
w = C.eb_widths(); rad, per = A.g1_tables() if DS.NAME == "g1" else A.g2_tables()
print(json.dumps(dict(name=DS.NAME, paths=[str(p) for p in (DS.DATA, DS.TARGETS, DS.AUDIT, DS.RUNS, DS.PREP, DS.TIC_LIST, DS.MANIFEST, DS.BEST)],
                      widths=[len(w), h(sorted(w.items()))], rad=[len(rad), h(sorted((k, str(v)) for k, v in rad.items()))], per=[len(per), h(sorted(per.items()))])))
"""


def digest(tree, ss):
    env = {k: v for k, v in os.environ.items() if k not in ("SS_SET", "VESPER_OPTS")}
    if ss:
        env["SS_SET"] = ss
    r = subprocess.run([PY, "-W", "ignore", "-c", DIGEST], cwd=tree, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-600:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_g1_and_g2_unchanged_by_the_patch():
    with tempfile.TemporaryDirectory() as tmp:
        tar = subprocess.run(["git", "-C", str(ROOT), "archive", OLD, "pipeline"], capture_output=True)
        assert tar.returncode == 0
        subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
        for ss in ("", "g1", "g2"):
            old, new = digest(pathlib.Path(tmp) / "pipeline", ss), digest(ROOT / "pipeline", ss)
            assert old == new, f"SS_SET={ss!r}: old {old} new {new}"
            assert old["widths"][0] > 20 and old["per"][0] > 100, old


def test_g3_paths_and_unknown_set():
    env = {**os.environ, "SS_SET": "g3"}
    r = subprocess.run([PY, "-W", "ignore", "-c", "import dataset as DS; print(DS.DATA, DS.TARGETS.name, DS.AUDIT, DS.RUNS, DS.PREP, DS.TIC_LIST.name)"], cwd=ROOT / "pipeline", env=env, capture_output=True, text=True)
    assert r.stdout.split() == [r"D:\second-sun\data\g3", "g3_chain_targets.csv", r"D:\second-sun\data\g3\audit", r"D:\second-sun\data\stage3_g3", r"D:\second-sun\data\stage3_g3_prep", "g3_targets.csv"], r.stdout
    r = subprocess.run([PY, "-W", "ignore", "-c", "import dataset"], cwd=ROOT / "pipeline", env={**os.environ, "SS_SET": "g4"}, capture_output=True, text=True)
    assert r.returncode != 0 and "g1, g2 or g3" in r.stderr, r.stderr[-300:]


def test_g3_tables_and_widths():
    code = """
import dataset as DS, stage3_core as C, audit_all as A, pandas as pd, numpy as np
tg = pd.read_csv(C.TARGETS, comment="#"); w = C.eb_widths(); rad, per = A.g3_tables()
assert len(tg) == 612 and tg.tic.is_unique and set(tg["slice"]) == {"g3"} and len(per) == 612 and len(rad) == 612
r = tg.iloc[0]; wp, ws = w[int(r.tic)]
assert abs(wp - r.dur_pri_h / 24 / r.p_bin_d) < 1e-12 and abs(ws - (r.dur_sec_h if r.dur_sec_h == r.dur_sec_h else r.dur_pri_h) / 24 / r.p_bin_d) < 1e-12
nosec = tg[tg.dur_sec_h.isna()].iloc[0]; assert w[int(nosec.tic)][1] == w[int(nosec.tic)][0]          # no secondary duration: the primary one
assert per[int(r.tic)] == [round(r.p_bin_d, 6)] and all(p[0] > 7 for p in per.values())
assert sum(v == v for v in rad.values()) == int((tg.tic_radius_rsun > 0).sum()) == 562                  # the headers' -1 is "no radius", never a radius
E = C.Ephem(tg, w); t0 = r.bjd0 - 57000.0
assert E.dist(int(r.tic), t0) == 0 and E.overlap(int(r.tic), t0, 6.5) and not E.overlap(int(r.tic), t0 + 1.3, 6.5)
print("ok")
"""
    r = subprocess.run([PY, "-W", "ignore", "-c", code], cwd=ROOT / "pipeline", env={**os.environ, "SS_SET": "g3"}, capture_output=True, text=True)
    assert r.stdout.strip().endswith("ok"), r.stderr[-800:]


def test_union_windows_table():
    rec = json.loads((ROOT / "data" / "g3" / "audit" / "spoc_windows_union.json").read_text())
    pk = ROOT / "data" / "g3" / "audit" / "spoc_windows.pkl"
    assert hashlib.sha256(pk.read_bytes()).hexdigest() == rec["union"]["sha256"], "the union table on disk is not the recorded one"
    assert json.loads((ROOT / "research" / "stage3" / "g3-union-windows.json").read_text())["union"]["sha256"] == rec["union"]["sha256"]
    u = pickle.load(open(pk, "rb")); g3 = pickle.load(open(ROOT / "data" / "g3" / "audit" / "spoc_windows_g3only.pkl", "rb"))
    g2 = pickle.load(open(ROOT / "data" / "g2" / "audit" / "spoc_windows.pkl", "rb")); g1 = pickle.load(open(ROOT / "research" / "audit-2026-10-23" / "spoc_windows.pkl", "rb"))
    assert sum(len(v) for v in u.values()) == sum(len(v) for p in (g1, g2, g3) for v in p.values()), "star-sector windows were lost or doubled"
    for p in (g1, g2, g3):
        for k, d in p.items():
            assert all(t in u[k] and u[k][t] is not None for t in d)
    assert list(u) == sorted(u), "keys not sorted: the bytes would differ between builds"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("pass:", name)
