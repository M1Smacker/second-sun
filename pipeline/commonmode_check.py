"""POST-HOC diagnostic on a frozen run (v6 learnings section 16). NOT part of the frozen search or its tiers; nothing here changes an event.
The Stage 2 burst flag asks: do other stars show UPSIDE-DOWN events at this moment? For a real dip that is not the natural question (a common instrument dip shows up as dips on
other stars, not as bumps), so the flag removes more upside-down events than real ones. The symmetric version asks: do other stars show an event OF THE SAME KIND (real with real,
upside-down with upside-down) within 0.1 d at the same sector and camera? It treats the control exactly like the data. This script counts, per half of the v6 union (PDCSAP = the v5 run,
SAP only = what the SAP twin added), how many tier-1 events survive when 3 or more other stars show a same-kind event at that moment. Aggregates only (no TIC, no time).
Usage: python commonmode_check.py [hash12]   (writes research\\stage3\\commonmode_<hash12>.txt)"""
import sys, pathlib
import numpy as np, pandas as pd
import stage3_report as R, stage3_core as C

ROOT = r"D:\second-sun\data\stage3"
WINDOW_D, MIN_STARS = 0.1, C.BURST_MIN


def same_kind_stars(E):
    """For every row of E (primary events of a union run): the number of OTHER stars with a primary event of the same kind within WINDOW_D at the same sector and camera."""
    by = {k: (g.center.values, g.tic.values) for k, g in E.groupby(["kind", "sector", "camera"])}
    return np.array([len(set(by[(r.kind, r.sector, r.camera)][1][np.abs(by[(r.kind, r.sector, r.camera)][0] - r.center) < WINDOW_D]) - {r.tic}) for r in E.itertuples()])


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else "f366d3682843"
    ev, _ = R.load(rf"{ROOT}\{h}\groups")
    E = ev[ev.primary].copy()
    E["cm"] = same_kind_stars(E)
    E["t1"] = E.tier.isin(["1A", "1L", "1B"])
    E["half"] = np.where(E.seen_by == "SAP only", "SAP only", "PDCSAP (v5, with the dips SAP also found)")
    out = [f"POST-HOC common-mode check on frozen run {h} (diagnostic, not part of any tier). Same-kind event of at least {MIN_STARS} other stars within {WINDOW_D} d, same sector and camera.",
           "Tier-1 events (real | upside-down): as frozen -> after removing those with a same-kind common moment"]
    for half, g in E.groupby("half"):
        r, f = g[g.kind == "real"], g[g.kind == "flip"]
        a = (int(r.t1.sum()), int(f.t1.sum())); b = (int((r.t1 & (r.cm < MIN_STARS)).sum()), int((f.t1 & (f.cm < MIN_STARS)).sum()))
        out.append(f"  {half:44s}: {a[0]:3d} | {a[1]:3d} -> {b[0]:3d} | {b[1]:3d}   (all events with a common moment: real {int((r.cm >= MIN_STARS).sum())} of {len(r)}, upside-down {int((f.cm >= MIN_STARS).sum())} of {len(f)})")
    r, f = E[E.kind == "real"], E[E.kind == "flip"]
    out.append(f"  {'whole union':44s}: {int(r.t1.sum()):3d} | {int(f.t1.sum()):3d} -> {int((r.t1 & (r.cm < MIN_STARS)).sum()):3d} | {int((f.t1 & (f.cm < MIN_STARS)).sum()):3d}")
    txt = "\n".join(out)
    leaked = [str(t) for t in ev.tic.unique() if str(t) in txt]
    assert not leaked, f"star IDs leaked: {leaked[:3]}"
    print(txt)
    (pathlib.Path(r"D:\second-sun\research\stage3") / f"commonmode_{h}.txt").write_text(txt, encoding="utf-8")
