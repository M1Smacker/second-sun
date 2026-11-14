"""RS-025 Q2 (Claude, 14 Nov 2026): do false dips near momentum dumps differ in SHAPE from planted planets there?
Compares stored features (dur_h, depth, snr, lift_pre, lift_post, cover_pre, cover_post) of (a) untouched-light SNR 7+ events held only by
the dump rule, real and upside-down, against (b) the planted dips freed when the dump half is switched off. Exploratory: no rule is chosen
here; any rule found gets written down before it is tested. Counts only to rs025/dumpshape.json."""
import json
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[3]
tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic"); ok = set(tg.tic.astype(int))
F = ["dur_h", "depth_ppm", "snr", "lift_pre", "lift_post", "cover_pre", "cover_post"]
other = ("step", "ramp", "dominated", "c5", "ecl_overlap", "repeater", "flipmatch")
rows = []
for camp in ("g2", "g3"):
    for p in (ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0" / "groups").glob("*.json"):
        tic, sec = map(int, p.stem.split("_"))
        if tic not in ok: continue
        for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
            fl = str(e.get("flags") or "")
            if (e.get("snr") or 0) >= 7 and "momentum dump" in fl and "gap edge" not in fl and not any(e.get(o) for o in other):
                rows.append(dict(group=f"untouched {e['kind']}", **{k: e.get(k) for k in F}))
tr = pd.read_csv(ROOT / "data" / "rs024" / "rs025-gap-split-trials.csv")
gain = tr[(tr.edge_only_real_new == True) & (tr.base_real_new == False)]
for r in gain.itertuples():
    for j in (ROOT / "data" / "astra" / "006").glob(f"planet-*-*-*-{r.campaign}/results.jsonl"):
        for line in j.read_text(encoding="utf-8").splitlines():
            x = json.loads(line)
            if x["trial"] != r.trial or x["star"] != r.star: continue
            best = None
            for s in x["changed"]:
                p = j.parent / f"trial-{r.trial}" / "1" / "groups" / f"{r.star}_{s}.json"
                if not p.exists(): continue
                for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
                    if e["kind"] == "real" and (e.get("snr") or 0) >= 7 and "momentum dump" in str(e.get("flags") or "") and any(abs(e["center"] - c) <= d / 2 for c, d in x["observed"]):
                        if best is None or e["snr"] > best["snr"]: best = e
            if best: rows.append(dict(group="planted freed", **{k: best.get(k) for k in F}))
D = pd.DataFrame(rows)
for c in F: D[c] = pd.to_numeric(D[c], errors="coerce")
D["lift_max"] = np.maximum(D.lift_pre.abs(), D.lift_post.abs()); D["lift_diff"] = (D.lift_pre - D.lift_post).abs(); D["cover_min"] = np.minimum(D.cover_pre, D.cover_post)
out = {g: {c: [round(float(v), 3) for v in s[c].quantile([0.25, 0.5, 0.75])] for c in ["dur_h", "depth_ppm", "snr", "lift_max", "lift_diff", "cover_min"]} | {"n": int(len(s))} for g, s in D.groupby("group")}
(ROOT / "research/stage3/rs025/dumpshape.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for g, v in out.items(): print(g, v)
