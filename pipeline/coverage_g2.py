"""G2 candidate list and which TESS light curves exist for it (metadata only, NO downloads; Ahmed said yes to this query on 29 Oct 2026).
Candidate list = the G1 rule applied to the TESS eclipsing binary catalogue (Prsa et al. 2022, data/xmatch/ebs.csv): detached (morphology 0 to under 0.5), binary period over 5 d, Tmag 13.5 or brighter, not in G1.
This is a PROPOSAL (research/stage3/g2-counts-2026-10-29.md); nothing is fixed until the preregistration file is committed. Query pattern = coverage_g1.py.
Files: data/g2/g2_candidates_LOCAL.csv, data/g2/g2_coverage_LOCAL.csv (git-ignored). Prints aggregates only."""
import csv, pathlib, collections
import numpy as np, pandas as pd
from astroquery.mast import Observations

ROOT = pathlib.Path(r"D:\second-sun")
OUT = ROOT / "data" / "g2"; OUT.mkdir(parents=True, exist_ok=True)
e = pd.read_csv(ROOT / "data" / "xmatch" / "ebs.csv").drop_duplicates("TIC")
g1 = set(pd.read_csv(ROOT / "targets" / "g1_targets.csv", comment="#").tic)
cand = e[(e.Morph >= 0) & (e.Morph < 0.5) & (e.Per > 5) & (e.Tmag <= 13.5) & ~e.TIC.isin(g1)][["TIC", "Tmag", "Per", "Morph", "Sectors"]].sort_values("TIC")
cand.to_csv(OUT / "g2_candidates_LOCAL.csv", index=False)
tics = [str(int(t)) for t in cand.TIC]
print(f"candidates {len(tics)} (expected 895)", flush=True)
cov = collections.defaultdict(lambda: collections.defaultdict(set))


def add(tab, key):
    for o in tab:
        tic = str(o["target_name"]).lstrip("0")
        cov[tic][key].add(int(o["sequence_number"]))


for i in range(0, len(tics), 100):
    chunk = tics[i:i + 100]
    spoc = Observations.query_criteria(obs_collection="TESS", dataproduct_type="timeseries", target_name=chunk)
    add(spoc[[str(p).upper() == "SPOC" for p in spoc["provenance_name"]]], "spoc")
    hl = Observations.query_criteria(obs_collection="HLSP", target_name=chunk, provenance_name=["QLP", "TESS-SPOC"])
    add(hl[[str(p) == "QLP" for p in hl["provenance_name"]]], "qlp")
    add(hl[[str(p) == "TESS-SPOC" for p in hl["provenance_name"]]], "tess_spoc")
    print(f"{min(i + 100, len(tics))}/{len(tics)} queried", flush=True)

rows = []
for t in tics:
    c = cov.get(t, {})
    rows.append(dict(tic=int(t), n_spoc=len(c.get("spoc", ())), n_qlp=len(c.get("qlp", ())), n_tess_spoc=len(c.get("tess_spoc", ())),
                     spoc=" ".join(map(str, sorted(c.get("spoc", ())))), qlp=" ".join(map(str, sorted(c.get("qlp", ())))), tess_spoc=" ".join(map(str, sorted(c.get("tess_spoc", ()))))))
df = pd.DataFrame(rows).merge(cand.rename(columns={"TIC": "tic"})[["tic", "Tmag", "Per", "Sectors"]], on="tic")
df.to_csv(OUT / "g2_coverage_LOCAL.csv", index=False)

man = pd.read_csv(ROOT / "data" / "g1" / "manifest.csv").drop_duplicates("file")
mb = man.groupby("author").bytes.mean()          # mean bytes per file in G1 by product: the size guess
df["files"] = df.n_spoc + df.n_qlp + df.n_tess_spoc
est = df.n_spoc * mb.get("SPOC", np.nan) + df.n_qlp * mb.get("QLP", np.nan) + df.n_tess_spoc * mb.get("TESS-SPOC", np.nan)
df["any"] = df.files > 0
n = len(df)
print(f"\nG2 candidate coverage ({n} stars, metadata only):")
print(f"  with any product {int(df['any'].sum())}; SPOC 2-min family {int((df.n_spoc > 0).sum())}; TESS-SPOC {int((df.n_tess_spoc > 0).sum())}; QLP {int((df.n_qlp > 0).sum())}; QLP only {int(((df.n_qlp > 0) & (df.n_spoc == 0) & (df.n_tess_spoc == 0)).sum())}")
print(f"  files to fetch: SPOC {int(df.n_spoc.sum())}, TESS-SPOC {int(df.n_tess_spoc.sum())}, QLP {int(df.n_qlp.sum())}, total {int(df.files.sum())}")
print(f"  mean bytes per file in G1: " + ", ".join(f"{k} {v / 1e6:.2f} MB" for k, v in mb.items()))
print(f"  estimated download (G1 file sizes x G2 file counts): {est.sum() / 1e9:.1f} GB (G1 was {man.bytes.sum() / 1e9:.1f} GB for {len(man)} files)")
best = df[["n_spoc", "n_qlp", "n_tess_spoc"]].max(axis=1)
print("  sectors per star (largest of the three products), quantiles 10/50/90:", np.percentile(best, [10, 50, 90]).tolist(), "| stars with 1 sector only:", int((best == 1).sum()), "| zero:", int((best == 0).sum()))
h = (df.tic.astype(str).apply(lambda s: int(__import__("hashlib").sha256(s.encode()).hexdigest(), 16)) % 3)
print("  split by the last step of a hash of the TIC number (an example rule, NOT fixed): slice sizes", h.value_counts().sort_index().to_dict(), "| estimated GB per slice", (est.groupby(h).sum() / 1e9).round(2).to_dict())
