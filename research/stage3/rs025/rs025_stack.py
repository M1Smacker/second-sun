"""RS-025 Q3 (Claude, 14 Nov 2026): for never-found planets classed weak or near miss, the IDEAL stacked SNR (sum of the detector's
crossing SNRs over sqrt(number of crossings), the planet's true times known) = an upper bound on what multi-transit combination can add.
Counts only to rs025/stack.json."""
import json, math
from pathlib import Path
import pandas as pd, numpy as np
ROOT = Path(r"D:\second-sun")
M = pd.read_csv(ROOT / "data/rs025/missed.csv"); M = M[(~M.found) & M.cause.isin(["4 near_miss", "5 weak"])]
out = []
for r in M.itertuples():
    for j in (ROOT / "data/astra/006").glob(f"planet-*-*-*-{r.campaign}/results.jsonl"):
        for line in j.read_text(encoding="utf-8").splitlines():
            x = json.loads(line)
            if x["trial"] != r.trial or x["star"] != r.star: continue
            sc = json.loads((j.parent / f"trial-{r.trial}" / "scores.json").read_text(encoding="utf-8")).get("1", [])
            best = {}
            for sector, arm, t, c, bc, snr in sc:
                if arm == 1 and t == r.trial and snr == snr and any(abs(c - cc) < 1e-6 for cc, d in x["observed"]):
                    best[round(c, 6)] = max(best.get(round(c, 6), -99), snr)
            v = np.array(list(best.values()))
            out.append(dict(cause=r.cause, bin=r.bin, n=len(v), stk=(v.sum() / math.sqrt(len(v)) if len(v) else np.nan), med=(np.median(v) if len(v) else np.nan)))
D = pd.DataFrame(out)
res = {}
for c, g in D.groupby("cause"):
    res[c] = dict(n=int(len(g)), median_crossing_snr=round(float(g.med.median()), 2), median_ideal_stack=round(float(g.stk.median()), 2),
                  ideal_stack_7plus=int((g.stk >= 7).sum()), ideal_stack_5_to_7=int(((g.stk >= 5) & (g.stk < 7)).sum()))
res["ideal_stack_7plus_by_bin"] = {int(b): int((g.stk >= 7).sum()) for b, g in D.groupby("bin")}
(ROOT / "research/stage3/rs025/stack.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
