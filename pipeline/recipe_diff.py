"""Loom phase 0 (research/stage3/loom-literature-2026-11-03.md, plan change 5): the RECIPE DIFF GATE. Before two runs are compared, print exactly what differs between their recorded settings (code files,
options, star list, manifest, targets, best-product table, every rule constant) and refuse a verdict unless only the options differ. Built from the 2 Nov 2026 incident: a baseline run made before the
manifest grew was about to be compared with a new one (FIX-QUEUE item 70). What the settings do NOT record is printed as a warning, because those inputs can still make two runs different.
Usage: python recipe_diff.py RUN_A RUN_B      (run folder names such as dev_428c5fb454cd; searched in data\\stage3_g2 and data\\stage3). Exit code 0 = like for like except options, 1 = not."""
import json, pathlib, sys

ROOT = pathlib.Path(r"D:\second-sun")
NOT_RECORDED = ["spoc_windows.pkl of the set's audit folder (decides QLP-only groups; overwritten at each prep)", "per-file sha256, DATA_REL and PROCVER (see manifest_fingerprint.py, data\\<set>\\manifest_fp.csv)",
                "library versions (astropy, lightkurve, numpy, numba, wotan, python)", "random seeds of the planted-dip runs"]


def load(name):
    for base in ("stage3_g2", "stage3"):
        f = ROOT / "data" / base / name / "settings.json"
        if f.exists():
            return json.load(open(f, encoding="utf-8"))
    sys.exit(f"no settings.json for run {name}")


def flat(d, p=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(flat(v, p + k + "."))
        else:
            out[p + k] = v
    return out


def diff(a, b):
    fa, fb = flat(a["settings"]), flat(b["settings"])
    return {k: (fa.get(k), fb.get(k)) for k in sorted(set(fa) | set(fb)) if fa.get(k) != fb.get(k)}


def main(na, nb):
    A, B = load(na), load(nb)
    d = diff(A, B)
    only_options = {k: v for k, v in d.items() if k == "options"}
    others = {k: v for k, v in d.items() if k != "options"}
    short = lambda v: (str(v)[:14] + "...") if isinstance(v, str) and len(v) > 24 else str(v)
    print(f"RECIPE DIFF {na} (made {A['provenance']['when'][:16]}, commit {A['provenance']['git_commit'][:8]}) against {nb} (made {B['provenance']['when'][:16]}, commit {B['provenance']['git_commit'][:8]})")
    print("  options:", sorted(A["settings"].get("options") or []), "against", sorted(B["settings"].get("options") or []))
    if others:
        print("  DIFFERENCES OTHER THAN OPTIONS:")
        for k, (x, y) in others.items():
            print(f"    {k}: {short(x)} | {short(y)}")
    print("  not recorded in the settings (can still differ):")
    for w in NOT_RECORDED:
        print("    -", w)
    if others:
        print("VERDICT: NOT LIKE FOR LIKE. Do not read any score from a comparison of these two runs; rerun the baseline under the same recipe.")
        return 1
    print("VERDICT: like for like in everything the settings record; the options above are the only intended difference (check the unrecorded inputs above before trusting a small effect).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
