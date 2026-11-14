"""Twin-transit refinement of OAE (Claude, 14 Nov 2026, 19:21 Kuwait; RS-025 Q5 follow-up). Written BEFORE running.
Problem (RS-025 Q5): under OAE a planet's stronger transit (same sign, a few days away) counts as a rival and makes the weaker transit
'dominated' (TIC 172900988 b: two transits 4.95 d apart).
Option OAEt = OAE, except a SAME-KIND rival whose box length is within LOCK_BOX (1.6x) and depth within LOCK_DEPTH (2.0x) of the candidate's
does not count (it may be another transit of the same planet). Both numbers are the frozen stack-link matching values in stage3_core
(orbit_locked), not tuned here.
Pass rule (Tree rule 1 as amended; written now): OAEt replaces OAE only if (a) P does not fall, (b) the paired control still passes in
every bin, (c) the untouched-light upside-down background (tier 1) is not higher than OAE's. Anything else: OAE stays, OAEt filed.
Same harness, trials and matching as rs024_options.py (imported; only prep and dominated are extended). Output: rs024/twin.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rs024_options as O

LOCK_BOX, LOCK_DEPTH = 1.6, 2.0
_prep = O.prep


def prep(df):
    df, _ = _prep(df)
    groups = {k: (g.index.values, g.kind.values, g.snr.fillna(0).values.astype(float), g.center.values.astype(float), g._expl.values,
                  g.dur_h.fillna(0).values.astype(float), g.depth_ppm.fillna(0).values.astype(float))
              for k, g in df.groupby(["tic", "sector", "product"])}
    return df, groups


def dominated(row, idx, groups, opt):
    ix, kind, snr, t, ex, dur, dep = groups[(row.tic, row.sector, row["product"])]
    s = row.snr
    if s is None or s != s:
        return False
    dt = np.abs(t - row.center)
    m = (ix != idx) & (dt <= O.WIN_D) & (dt >= 1.5 * float(row.dur_h or 0) / 24) & ~ex
    if opt == "OAEt":
        d0, p0 = float(row.dur_h or 0), float(row.depth_ppm or 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            twin = (kind == row.kind) & (dur / d0 <= LOCK_BOX) & (d0 / dur <= LOCK_BOX) & (dep / p0 <= LOCK_DEPTH) & (p0 / dep <= LOCK_DEPTH)
        m = m & ~twin
    return bool(m.any() and snr[m].max() >= s)


O.prep, O.dominated, O.OPTS = prep, dominated, ("OAE", "OAEt")
_main_write = O.main
if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser(); a.add_argument("--limit", type=int); lim = a.parse_args().limit
    O.main(lim)
    src = Path(O.__file__).parent / (f"options-prefix{lim}.json" if lim else "options.json")
    dst = Path(__file__).parent / (f"twin-prefix{lim}.json" if lim else "twin.json")
    # O.main writes options*.json; move it so RS-024's own file is not overwritten
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
