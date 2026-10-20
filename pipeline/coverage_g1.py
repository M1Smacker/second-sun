"""Which TESS light curves exist for each G1 target, and for how many sectors (metadata only, no downloads).

MAST Observations queries in chunks: SPOC 2-min/20-s light curves (obs_collection TESS, provenance SPOC)
and the full-frame-image products QLP and TESS-SPOC (obs_collection HLSP). target_name = TIC number.
Output: targets/g1_coverage.csv (tic, n_spoc, n_qlp, n_tess_spoc, sectors per product).
"""
import csv, pathlib, collections
from astroquery.mast import Observations

ROOT = pathlib.Path(r"D:\second-sun")
T = ROOT / "targets" / "g1_targets.csv"
OUT = ROOT / "targets" / "g1_coverage.csv"
rows = [r for r in csv.DictReader(l for l in open(T, encoding="utf-8") if not l.startswith("#"))]
tics = sorted({r["tic"] for r in rows})
cov = collections.defaultdict(lambda: collections.defaultdict(set))


def add(tab, key):
    for o in tab:
        tic = str(o["target_name"]).lstrip("0")
        sec = o["sequence_number"]
        if tic in cov or tic in tics:
            cov[tic][key].add(int(sec))


for i in range(0, len(tics), 100):
    chunk = tics[i:i + 100]
    spoc = Observations.query_criteria(obs_collection="TESS", dataproduct_type="timeseries", target_name=chunk)
    add(spoc[[str(p).upper() == "SPOC" for p in spoc["provenance_name"]]], "spoc")
    hl = Observations.query_criteria(obs_collection="HLSP", target_name=chunk, provenance_name=["QLP", "TESS-SPOC"])
    add(hl[[str(p) == "QLP" for p in hl["provenance_name"]]], "qlp")
    add(hl[[str(p) == "TESS-SPOC" for p in hl["provenance_name"]]], "tess_spoc")
    print(f"{min(i + 100, len(tics))}/{len(tics)} queried", flush=True)

with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["tic", "n_spoc", "n_qlp", "n_tess_spoc", "spoc_sectors", "qlp_sectors", "tess_spoc_sectors"])
    for t in tics:
        c = cov.get(t, {})
        g = lambda k: sorted(c.get(k, ()))
        w.writerow([t, len(g("spoc")), len(g("qlp")), len(g("tess_spoc")),
                    " ".join(map(str, g("spoc"))), " ".join(map(str, g("qlp"))), " ".join(map(str, g("tess_spoc")))])

n = len(tics)
has = lambda k: sum(1 for t in tics if cov.get(t, {}).get(k))
anyp = sum(1 for t in tics if any(cov.get(t, {}).get(k) for k in ("spoc", "qlp", "tess_spoc")))
print(f"stars {n}: SPOC 2-min {has('spoc')}, QLP {has('qlp')}, TESS-SPOC {has('tess_spoc')}, any product {anyp}")
