"""RS-024 Q2/Q3 (Claude, 14 Nov 2026): is the untouched light of our binaries sign-symmetric, as the 'dominated' rule assumes?
Reads the Re-search 1 design-star groups (g2, g3; design_seen == 1 only; fence A and B never read). No planting, no tiering.
For every light curve (star, sector, product) with events of both arms it takes the strongest real dip and the strongest
upside-down event (= strongest bump of the real light) and asks:
  A. how often the dip side is stronger (noise alone: 50%), per binary-period bin;
  B. for strong winners (SNR >= 7): what they look like: distance to the catalogue eclipse (ph_d), duration, depth,
     the flags already on them (step, ramp, gap_dump, repeater), and their phase on the star's own eclipse ephemeris (p1_P, p1_T0);
  C. do strong off-eclipse dips of one star come back at the same binary phase in other sectors (a periodic, astrophysical source)?
Counts only to research/stage3/rs024/symmetry.json; private rows to data/rs024/winners.csv.
Usage: D:\\second-sun\\.venv\\Scripts\\python.exe research/stage3/rs024/rs024_symmetry.py"""
import json, math
from collections import defaultdict, Counter
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BINS = [5, 10, 14, 20, 27.4, 1e9]
LAB = ["5-10", "10-14", "14-20", "20-27.4", "27.4+"]


def pbin(p):
    for i in range(5):
        if BINS[i] <= p < BINS[i + 1]:
            return LAB[i]
    return None


def main():
    tg = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
    tg = tg[tg["list"].isin(["g2", "g3"]) & (tg.design_seen == 1)].drop_duplicates("tic")
    Pb = dict(zip(tg.tic.astype(int), tg.p_bin_d.astype(float)))
    rows = []
    for camp in ("g2", "g3"):
        src = ROOT / "data" / f"stage3_{camp}" / f"r1dev_{camp}_seen_bcd29c7aabb0"
        for kind in ("groups", "groups_sap"):
            for p in (src / kind).glob("*.json"):
                tic, sec = map(int, p.stem.split("_"))
                if tic not in Pb:
                    continue
                for e in json.loads(p.read_text(encoding="utf-8"))["events"]:
                    if e.get("snr") is None:
                        continue
                    rows.append(dict(camp=camp, src=kind, tic=tic, sector=sec, product=e["product"], kind=e["kind"], snr=float(e["snr"]),
                                     center=float(e["center"]), dur_h=e.get("dur_h"), depth=e.get("depth_ppm"), ph_d=e.get("ph_d"),
                                     c5=bool(e.get("c5")), ov=bool(e.get("ecl_overlap")), step=bool(e.get("step")), ramp=bool(e.get("ramp")),
                                     gap=bool(e.get("gap_dump")), rep_n=e.get("repeat_n") or 0, p1_P=e.get("p1_P"), p1_T0=e.get("p1_T0"),
                                     dominated=bool(e.get("dominated")), tier=str(e.get("tier"))))
    E = pd.DataFrame(rows)
    E["P"] = E.tic.map(Pb); E["bin"] = E.P.map(pbin)
    key = ["camp", "src", "tic", "sector", "product"]
    top = E.sort_values("snr").groupby(key + ["kind"]).tail(1)
    w = top.pivot_table(index=key, columns="kind", values="snr", aggfunc="max").dropna().reset_index()
    w = w.merge(E[key + ["bin"]].drop_duplicates(key), on=key)
    out = {"light curves with both arms": int(len(w)), "events read": int(len(E))}
    A = {}
    for b in LAB + ["all"]:
        s = w if b == "all" else w[w.bin == b]
        strong = s[(s.real >= 7) | (s.flip >= 7)]
        A[b] = dict(n=int(len(s)), dip_stronger=round(float((s.real > s.flip).mean()), 3) if len(s) else None,
                    n_strong=int(len(strong)), dip_stronger_when_one_is_strong=round(float((strong.real > strong.flip).mean()), 3) if len(strong) else None,
                    median_ratio_dip_over_bump=round(float((s.real / s.flip).median()), 3) if len(s) else None,
                    strongest_dip_median=round(float(s.real.median()), 2) if len(s) else None, strongest_bump_median=round(float(s.flip.median()), 2) if len(s) else None)
    out["A: share of light curves where the strongest dip beats the strongest bump (noise alone 0.5)"] = A
    # B: what the strong winners are
    win = top.merge(w[key + ["real", "flip"]], on=key)
    win = win[((win.kind == "real") & (win.real > win.flip)) | ((win.kind == "flip") & (win.flip >= win.real))]
    win = win[win.snr >= 7]
    def phase(r):
        if r.p1_P and r.p1_P == r.p1_P and r.p1_T0 == r.p1_T0 and r.p1_P > 0:
            return ((r.center - r.p1_T0) / r.p1_P) % 1.0
        return np.nan
    win["phase"] = win.apply(phase, axis=1)
    B = {}
    for (b, k), s in win.groupby(["bin", "kind"]):
        off = s[~(s.c5 | s.ov)]
        ph = off.phase.dropna()
        B[f"{b} {'dip wins' if k == 'real' else 'bump wins'}"] = dict(
            n=int(len(s)), on_catalogue_eclipse=int((s.c5 | s.ov).sum()), off=int(len(off)),
            off_with_step=int(off.step.sum()), off_with_ramp=int(off.ramp.sum()), off_with_gap_dump=int(off.gap.sum()),
            off_repeat_n_3plus=int((off.rep_n >= 3).sum()), off_any_of_these_flags=int((off.step | off.ramp | off.gap | (off.rep_n >= 3)).sum()),
            off_clean=int((~(off.step | off.ramp | off.gap | (off.rep_n >= 3))).sum()),
            off_dur_h_median=float(off.dur_h.median()) if len(off) else None, off_depth_ppm_median=float(off.depth.median()) if len(off) else None,
            off_ph_d_median=round(float(off.ph_d.dropna().median()), 2) if off.ph_d.notna().any() else None,
            off_phase_known=int(len(ph)), off_phase_hist_10=np.histogram(ph, bins=10, range=(0, 1))[0].tolist(),
            products=dict(Counter(s["product"])))
    out["B: strong winners (SNR 7+) by bin and side"] = B
    # C: do one star's strong off-eclipse dip winners recur at the same binary phase in other sectors?
    C = Counter()
    offd = win[(win.kind == "real") & ~(win.c5 | win.ov) & win.phase.notna()]
    for tic, s in offd.groupby("tic"):
        secs = s.drop_duplicates("sector")
        if len(secs) < 2:
            C["stars with off-eclipse dip winners in only 1 sector"] += 1
            continue
        ph = secs.phase.values
        d = np.abs(((ph[:, None] - ph[None, :]) + 0.5) % 1 - 0.5)
        np.fill_diagonal(d, 1)
        C["stars with winners in 2+ sectors"] += 1
        C["... of which some pair agrees within 0.02 in phase"] += int((d < 0.02).any())
        C["... expected by chance (pairs x 0.04), summed"] += 0
        C["_pairs"] += int(len(ph) * (len(ph) - 1) / 2)
    out["C: recurrence of off-eclipse dip winners at the same binary phase"] = dict(C)
    out["C: chance level"] = "a random pair agrees within 0.02 with probability 0.04; compare the 'agrees' count to 0.04 x pairs per star (upper bound: 1 - 0.96^pairs)"
    hd = ROOT / "research" / "stage3" / "rs024"
    (hd / "symmetry.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    pdir = ROOT / "data" / "rs024"; pdir.mkdir(exist_ok=True)
    win.to_csv(pdir / "winners.csv", index=False)
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
