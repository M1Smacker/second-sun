"""Scorecard plus lines A to D for a G3 run (G3-PREREGISTRATION.md section 5: "the scorecard-plus lines A to E of SCORECARD-AMENDMENTS.md are printed with them, in stars and not only in events, as pre-specified reporting").
A wrapper around scorecard_plus.py with its own set of planted rows: the run's rows (data/chain_recovery_<set>/rows_<label>.pkl) take the place of the "sealed" columns and the G2 development rows stay the "dev" columns. Line E (TOI-1338 b) does not apply.
Test of the wrapper: run it with SS_SET=g2 on the stored sealed G2 run (label sealed): lines A to D must equal research/stage3/scorecard-plus-sealed.txt.
Usage: SS_SET=g3 VESPER_OPTS=c6 python scorecard_plus_g3.py RUN_FOLDER LABEL NSTARS ROWS_LABEL     (e.g. g3_e7886a71a61f g3 611 g3)"""
import os, sys
import pandas as pd
import scorecard_plus as SP
import stage3_core as C


def planted(name):
    folder = C.ROOT / "data" / ("chain_recovery_g2" if name == "g2dev" else f"chain_recovery_{C.DS.NAME}")
    r = pd.read_pickle(folder / f"rows_{name}.pkl")
    return r[r.K.notna() & r.error.isna()].copy()


def main(run, label, nstars, rows_label):
    SP.planted = lambda n: planted(rows_label if n == "sealed" else n)
    out = []
    P = lambda s="": (out.append(s), print(s, flush=True))
    P(f"VESPER SCORECARD PLUS on {run} ({label}), set {C.DS.NAME}, options {sorted(C.V.ON)}. In the lines below the column called 'sealed' is THIS run; 'dev' is the G2 development slice. Line E does not apply.")
    E, meta = SP.load_events(run)
    SP.print_star_table(SP.star_table(E, nstars), label, P)
    pl = pd.concat([SP.planted("sealed").assign(sl="sealed"), SP.planted("g2dev").assign(sl="dev")])
    SP.print_price_table(SP.price_table(E, pl), P)
    ss = meta[meta.status == "ok"].drop_duplicates(["tic", "sector"]).groupby("tic").size()
    SP.print_efficiency(SP.efficiency(pl, float(ss.mean()), nstars), nstars, P)
    SP.print_wording(E, meta, SP.planted("sealed"), SP.planted("g2dev"), P)
    (C.ROOT / "research" / "stage3" / f"scorecard-plus-{label}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
