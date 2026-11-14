"""RS-024 Q2 chance level for rs024_phase.py: shift each sector's events of a star by one random binary phase (keeps within-sector
structure, breaks any phase link between sectors), 200 times; report observed against mean shuffled recurrence, and distinct stars.
Also counts how many recurring clean dips carry orbit_lock or a tier-1 label. Counts only to rs024/phase-null.json."""
import json
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[3]
LAB = ["5-10", "10-14", "14-20", "20-27.4", "27.4+"]; BINS = [5, 10, 14, 20, 27.4, 1e9]
tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic")
Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
rows = []
for camp in ("g2", "g3"):
    for p in (ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0" / "groups").glob("*.json"):
        tic, sec = map(int, p.stem.split("_"))
        if tic not in Pb: continue
        for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
            if (e.get("snr") or 0) >= 7:
                rows.append(dict(tic=tic, sector=sec, kind=e["kind"], t=float(e["center"]), off=not (e.get("c5") or e.get("ecl_overlap")),
                                 flagged=bool(e.get("step") or e.get("gap_dump") or e.get("ramp")), lock=bool(e.get("orbit_lock")), tier=str(e.get("tier"))))
E = pd.DataFrame(rows).drop_duplicates(["tic", "sector", "kind", "t"]); E["P"] = E.tic.map(Pb); E["bin"] = pd.cut(E.P, BINS, labels=LAB, right=False).astype(str)
rng = np.random.default_rng(7); TOL = 0.01

def rec(s, shift=None):
    ph = (s.t.values / s.P.values) % 1
    if shift is not None:
        ph = (ph + s.sector.map(shift).values) % 1
    d = np.abs((ph[:, None] - ph[None, :] + 0.5) % 1 - 0.5)
    return ((d < TOL) & (s.sector.values[:, None] != s.sector.values[None, :])).sum(1) >= 1

out = {}
for kind in ("real", "flip"):
    S = E[E.kind == kind]
    obs = pd.Series(False, index=S.index); null = pd.Series(0.0, index=S.index)
    for tic, s in S.groupby("tic"):
        obs[s.index] = rec(s)
        secs = s.sector.unique(); acc = np.zeros(len(s))
        for _ in range(200):
            acc += rec(s, dict(zip(secs, rng.random(len(secs)))))
        null[s.index] = acc / 200
    S = S.assign(obs=obs, null=null)
    for b in LAB:
        for f in (False, True):
            x = S[(S.bin == b) & S.off & (S.flagged == f)]
            out[f"{kind} {b} {'flagged' if f else 'clean'}"] = dict(n=int(len(x)), stars=int(x.tic.nunique()), recur=int(x.obs.sum()), chance=round(float(x.null.sum()), 1),
                                                                   recur_stars=int(x[x.obs].tic.nunique()), recur_with_orbit_lock=int((x.obs & x.lock).sum()),
                                                                   recur_tier1=int((x.obs & x.tier.isin(["1A", "1B", "1L"])).sum()))
(ROOT / "research/stage3/rs024/phase-null.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for k, v in out.items(): print(k, v)
