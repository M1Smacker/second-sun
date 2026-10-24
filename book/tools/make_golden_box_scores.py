"""Writes book/tools/golden_box_scores.json: the hunt's own box_scores() (taken straight from pipeline/detect_v2.py, not copied) run on fixed test arrays.
The JavaScript port (docs/assets/eyes-strength.js) must reproduce these numbers (book/tools/test_eyes_strength.mjs).
Run: .venv\\Scripts\\python.exe book\\tools\\make_golden_box_scores.py"""
import ast, json, pathlib
import numpy as np

root = pathlib.Path(__file__).resolve().parents[2]
src = (root / "pipeline" / "detect_v2.py").read_text(encoding="utf-8")
tree = ast.parse(src)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "box_scores")
ns = {"np": np, "BIN_D": 10 / 1440}
exec(compile(ast.Module([fn], []), "detect_v2.box_scores", "exec"), ns)
box_scores = ns["box_scores"]

rng = np.random.default_rng(1338)
cases = []
def add(name, bf, durs=(3, 4, 5, 6.5, 8, 10, 12, 15)):
    bf = np.asarray(bf, float)
    bt = np.arange(len(bf)) * (10 / 1440)
    out = []
    for d in durs:
        c, snr, m = box_scores(bt, bf, d)
        out.append({"dur_h": d, "snr": [None if not np.isfinite(v) else float(v) for v in snr], "m": [None if not np.isfinite(v) else float(v) for v in m]})
    cases.append({"name": name, "bf": [None if not np.isfinite(v) else float(v) for v in bf], "out": out})

noise = rng.normal(0, 1000, 700)
add("white noise", noise)
dip = noise.copy(); dip[300:340] -= 2500
add("noise with a dip", dip)
gap = dip.copy(); gap[100:160] = np.nan; gap[500:505] = np.nan
add("dip and two gaps", gap)
red = np.convolve(rng.normal(0, 1000, 760), np.ones(12) / 3.5, mode="valid")[:700]
add("lumpy noise", red)
heavy = noise.copy(); heavy[::17] = np.nan; heavy[200:420] = np.where(np.arange(220) % 3 == 0, np.nan, heavy[200:420])
add("many missing points (coverage rule)", heavy)
add("too short for the scale (under 20 boxes)", rng.normal(0, 1000, 100), durs=(15,))

(root / "book" / "tools" / "golden_box_scores.json").write_text(json.dumps(cases), encoding="utf-8")
print("wrote", len(cases), "cases")
