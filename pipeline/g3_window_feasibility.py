"""G3 window feasibility (2 Nov 2026; Loom research finding 4, research/stage3/loom-literature-2026-11-03.md). Counts only, no light curve is analysed and no frozen file is touched.
A QLP star-sector borrows good-time windows from OTHER stars that have a SPOC 2-minute file on the same sector, camera and CCD (audit_all.neighbour_windows; own windows if the star itself has a SPOC
2-minute file). With 2 or more such neighbours the group is searched ("neighbours"), with 1 it is weak, with 0 it is "NONE (unsafe)" and not searched. This script counts, for the G3 star-sectors,
how many QLP groups would fall in each class if the neighbour pool were (A) the G3 files only (what a G3-only prep would build) or (B) the union of G3, G2 (data\\g2\\audit\\spoc_windows.pkl) and G1
(research\\audit-2026-10-23\\spoc_windows.pkl). Usage: python g3_window_feasibility.py   (writes research\\stage3\\g3-window-feasibility-2026-11-02.txt)"""
import glob, pickle, pathlib, collections, warnings
warnings.filterwarnings("ignore")
from astropy.io import fits

ROOT = pathlib.Path(r"D:\second-sun")
OUT = []
P = lambda s="": (OUT.append(s), print(s))
cell = lambda h0, h1: tuple(int(h0.get(k, h1.get(k))) for k in ("SECTOR", "CAMERA", "CCD"))
groups = collections.defaultdict(lambda: dict(fam=set(), cell=None))
for f in sorted(glob.glob(str(ROOT / "data" / "g3" / "*" / "*.fits"))):
    p = pathlib.Path(f); name = p.name
    fam = "QLP" if name.startswith("hlsp_qlp") else ("TESS-SPOC" if name.startswith("hlsp_tess-spoc") else ("SPOC2" if name.startswith("tess") and name.endswith("_lc.fits") else "other"))
    try:
        h0, h1 = fits.getheader(f, 0), fits.getheader(f, 1); c = cell(h0, h1)
    except Exception:
        continue
    g = groups[(int(p.parent.name), c[0])]; g["fam"].add(fam); g["cell"] = c
spoc3 = collections.defaultdict(set)
for (tic, sec), g in groups.items():
    if "SPOC2" in g["fam"]:
        spoc3[g["cell"]].add(tic)
db2 = pickle.load(open(ROOT / "data" / "g2" / "audit" / "spoc_windows.pkl", "rb"))
db1 = pickle.load(open(ROOT / "research" / "audit-2026-10-23" / "spoc_windows.pkl", "rb"))
pool = lambda db, c: {t for t, w in db.get(c, {}).items() if len(w)}
n_all = len(groups); n_qlp = sum("QLP" in g["fam"] for g in groups.values()); n_own = sum("SPOC2" in g["fam"] for g in groups.values())
qonly = [(k, g) for k, g in groups.items() if "QLP" in g["fam"] and "SPOC2" not in g["fam"]]
P(f"G3 files on disk now: {len(groups)} star-sector groups from {len({k[0] for k in groups})} stars; with a QLP file {n_qlp}; with their own SPOC 2-minute file {n_own}; QLP groups WITHOUT own windows (they must borrow): {len(qonly)}")
P(f"neighbour pools: G3 SPOC 2-minute star-sectors {sum(len(v) for v in spoc3.values())} in {len(spoc3)} cells; G2 pickle {sum(len(v) for v in db2.values())} star-sectors in {len(db2)} cells; G1 pickle {sum(len(v) for v in db1.values())} in {len(db1)} cells")
for label, fn in (("A: G3 files only", lambda c, t: len(spoc3.get(c, set()) - {t})), ("B: G3 + G2 + G1 union", lambda c, t: len((spoc3.get(c, set()) | pool(db2, c) | pool(db1, c)) - {t})), ("B2: G2 + G1 only (no G3 SPOC)", lambda c, t: len((pool(db2, c) | pool(db1, c)) - {t}))):
    cnt = collections.Counter("2 or more (searched)" if (nn := fn(g["cell"], k[0])) >= 2 else ("1 (weak)" if nn == 1 else "0 (NONE, not searched)") for k, g in qonly)
    P(f"  pool {label}: " + "; ".join(f"{k} {v} ({100 * v / max(len(qonly), 1):.0f}%)" for k, v in sorted(cnt.items())))
(ROOT / "research" / "stage3" / "g3-window-feasibility-2026-11-02.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
