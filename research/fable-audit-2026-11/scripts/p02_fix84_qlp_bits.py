"""P-02 (Fable audit, FIX 84): which QUALITY bits are set on the QLP cadences that Petrova's loader keeps (lk.read(path, quality_bitmask="hard"))?
Counts only. Random sample of G3 QLP files (seed 84), split by sector era (<56, 56-93, >=94).
For every file: cadences in the file, cadences kept by the loader, kept cadences with QUALITY != 0, and the bit histogram of those.
Usage: python p02_fix84_qlp_bits.py [n_files]"""
import sys, glob, warnings, collections
warnings.filterwarnings("ignore")
import numpy as np
from astropy.io import fits
import lightkurve as lk

n = int(sys.argv[1]) if len(sys.argv) > 1 else 240
files = sorted(glob.glob(r"D:\second-sun\data\g3\*\hlsp_qlp*.fits"))
rng = np.random.default_rng(84); pick = rng.choice(len(files), size=min(n, len(files)), replace=False)
era = lambda s: "<56" if s < 56 else ("56-93" if s < 94 else ">=94")
tot = collections.defaultdict(lambda: dict(files=0, cad=0, kept=0, kept_flagged=0, files_with=0, bits=collections.Counter(), cols=collections.Counter()))
for i in pick:
    p = files[i]
    with fits.open(p) as h:
        sec = h[0].header.get("SECTOR"); d = h[1].data; q = np.asarray(d["QUALITY"], dtype=np.int64); t = np.asarray(d["TIME"], float)
        cols = [c.lower() for c in d.columns.names]
    lc = lk.read(p, quality_bitmask="hard")
    kept_t = lc.time.value; kept_t = kept_t[np.isfinite(kept_t)]
    keep = np.isin(np.round(t, 6), np.round(kept_t, 6)) & np.isfinite(t)
    T = tot[era(sec)]; T["files"] += 1; T["cad"] += int(np.isfinite(t).sum()); T["kept"] += int(keep.sum())
    fl = keep & (q != 0); T["kept_flagged"] += int(fl.sum()); T["files_with"] += int(fl.any())
    T["cols"]["sys_rm_flux" if "sys_rm_flux" in cols else ("det_flux" if "det_flux" in cols else "kspsap_flux" if "kspsap_flux" in cols else "other:" + ",".join(cols[:12]))] += 1
    for b in range(40):
        c = int(((q[fl] >> b) & 1).sum())
        if c:
            T["bits"][b] += c
print(f"G3 QLP files on disk: {len(files)}; sampled {len(pick)} (seed 84); lightkurve {lk.__version__}")
for k in ("<56", "56-93", ">=94"):
    T = tot[k]
    if not T["files"]:
        print(f"sectors {k}: no files in the sample"); continue
    print(f"sectors {k}: files {T['files']}; cadences {T['cad']}; kept by the loader {T['kept']} ({100*T['kept']/T['cad']:.1f}%); kept WITH a flag set {T['kept_flagged']} "
          f"({100*T['kept_flagged']/max(T['kept'],1):.2f}% of kept); files with any {T['files_with']}; bits (bit: cadences) {dict(sorted(T['bits'].items()))}; flux columns {dict(T['cols'])}")
