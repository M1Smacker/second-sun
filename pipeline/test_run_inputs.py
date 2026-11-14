"""Tests for run_inputs.py (BUILD T52). Run: python test_run_inputs.py (from pipeline/). Each case runs in a fresh interpreter so the
environment and imports start clean."""
import json, os, subprocess, sys, tempfile, pathlib

HERE = pathlib.Path(__file__).resolve().parent
PY = sys.executable


def run(code, env_extra=None):
    env = {k: v for k, v in os.environ.items() if k not in ("SS_SET", "VESPER_OPTS")}
    env.update(env_extra or {})
    r = subprocess.run([PY, "-B", "-c", code], cwd=HERE, env=env, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


tmp = pathlib.Path(tempfile.mkdtemp())
good = tmp / "s.json"; good.write_text(json.dumps({"set": "g2", "opts": ["p1", "c6"]}))
bad = tmp / "b.json"; bad.write_text(json.dumps({"set": "g9", "opts": []}))
A = f"import run_inputs as RI; RI.apply(r'{good}'); import dataset as DS, vopts as V; print(DS.NAME, sorted(V.ON))"

c, o = run(A); assert c == 0 and o.endswith("g2 ['c6', 'p1']"), o                                     # settings come from the file
c, o = run(A, {"SS_SET": "g3"}); assert c != 0 and "REFUSED" in o and "SS_SET" in o, o              # stale shell value refused
c, o = run(A, {"VESPER_OPTS": "p1+c6"}); assert c == 0, o                                            # same options, other spelling: fine
c, o = run(f"import run_inputs as RI; RI.apply(r'{bad}')"); assert c != 0 and "must be one of" in o, o
c, o = run(f"import run_inputs as RI; RI.apply(r'{tmp / 'none.json'}')"); assert c != 0 and "not found" in o, o

R = f"import run_inputs as RI; RI.apply(r'{good}'); import dataset as DS; "
c, o = run(R + "import pandas as pd; r=pd.read_csv('../targets/r1_targets.csv', comment='#'); t=r[(r['list']=='g2')&(r.design_seen==1)].tic.head(3); print(RI.require(DS, t))")
assert c == 0 and "'stars_without_files': 0" in o, o                                                 # real G2 inputs pass
c, o = run(R + "print(RI.require(DS, [999999999999]))"); assert c != 0 and "no light-curve file" in o, o   # star without files refused
c, o = run(R + "import pathlib; DS.BEST = pathlib.Path('D:/nowhere/best.csv'); RI.require(DS)"); assert c != 0 and "missing inputs" in o, o
print("test_run_inputs: 8 cases passed")
