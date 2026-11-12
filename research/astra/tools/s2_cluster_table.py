"""Anonymous S2 frequency table for Codex brief 002 part B (Claude, 13 Nov 2026).

For each sealed Re-search 1 list, every star with recovered light gives one pair:
  (exposure = its star-sectors with recovered light, flips = its upside-down tier-1 events at SNR >= 7 in recovered light).
The output counts how many stars share each pair. No star id, time or depth leaves this script. It first reproduces the
filed S2 totals (G3 6 in 1152, G2 13 in 2381) with the same selection as pipeline/r1_readout.py main(), and refuses to
write if they differ.
Usage (one list per run): set SS_SET=g3 SS_RUN=r1_g3_unseen_bcd29c7aabb0 VESPER_OPTS=c6,p1, then
  D:\\second-sun\\.venv\\Scripts\\python.exe research\\astra\\tools\\s2_cluster_table.py
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
import stage3_core as C, stage3_report as R  # noqa: E402

FILED = {"g3": (6, 1152), "g2": (13, 2381)}
T1 = ["1A", "1L", "1B"]

name, run = C.DS.NAME, os.environ["SS_RUN"]
ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
E = ev[ev.primary].copy()
E["rec"] = E.recovered.fillna(False).astype(bool)
ok = meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"])
rec_ss = ok[ok["p1"].apply(lambda d: bool(isinstance(d, dict) and d.get("recovered")))]
rec = E[E.rec]
fl = rec[(rec.kind == "flip") & rec.tier.isin(T1) & (rec.snr >= 7)]
k, n = len(fl), len(rec_ss)
print(f"{name}: flips {k} in {n} star-sectors (filed {FILED[name]})")
if (k, n) != FILED[name]:
    raise SystemExit("totals differ from the filed S2 line: nothing written")
expo = rec_ss.groupby("tic").size()
cnt = fl.groupby("tic").size().reindex(expo.index, fill_value=0)
missing = set(fl.tic) - set(expo.index)
if missing:
    raise SystemExit(f"{len(missing)} stars have flips but no recovered star-sector: nothing written")
tab = (expo.to_frame("exposure").assign(flips=cnt.values).value_counts().rename("stars").reset_index()
       .sort_values(["exposure", "flips"]))
out = ROOT / "research" / "astra" / "inbox" / f"002-s2-cluster-table-{name}.csv"
with open(out, "w", newline="") as fh:
    fh.write(f"# S2 cluster input, list {name}, run {run}: stars with recovered light by (exposure, flips); no ids. "
             f"Totals: {len(expo)} stars, {n} star-sectors, {k} flips (filed S2 reproduced). Claude, 13 Nov 2026\n")
    tab.to_csv(fh, index=False)
print(f"wrote {out.name}: {len(expo)} stars, {len(tab)} rows")
