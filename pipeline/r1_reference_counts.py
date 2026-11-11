"""Re-search 1, Amendment 2: the reference counts of the SEEN stars (counts only, no star id, no event time).
For one list (SS_SET = g2 or g3) and its development run on the seen stars (SS_RUN, e.g. r1dev_g3_seen_bcd29c7aabb0): the number of real and upside-down tier-1 events (PDCSAP half, as benchmark_g2.s1 counts them) in
RECOVERED light at the SNR bars 7, 8, 10 and 12, plus the same counts in the light both masks keep (the control). Printed as plain lines and appended to research/stage3/R1-S1-REFERENCE-COUNTS.txt only with --write.
The sealed readout (r1_readout.py) reads the lines of that file, never the seen run again, so the reference cannot drift after the freeze.
Usage: SS_SET=g3 SS_RUN=r1dev_g3_seen_bcd29c7aabb0 VESPER_OPTS=c6,p1 python r1_reference_counts.py [--write]"""
import os, sys
import stage3_core as C, stage3_report as R

T1 = ["1A", "1L", "1B"]
BARS = (7, 8, 10, 12)


def counts(E):
    t1 = E[E.tier.isin(T1)]
    r1, f1 = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
    return {b: (int((r1.snr >= b).sum()), int((f1.snr >= b).sum())) for b in BARS}


BINS = [(5, 10), (10, 14), (14, 20), (20, 27.4), (27.4, 1e9)]      # binary-period bins of the preregistration (Amendment 3 stratifies S1 by them)


def bin_lines(name, run):
    """REFBIN lines (Amendment 3): the same tier-1, PDCSAP-half, recovered-light counts as above, split by the binary period of the event's own binary (column p1_P), per SNR bar."""
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    E = ev[ev.primary].copy()
    E["rec"] = E.recovered.fillna(False).astype(bool)
    t1 = E[E.rec & E.tier.isin(T1)]
    r, f = R.pdc_half(t1[t1.kind == "real"]), R.pdc_half(t1[t1.kind == "flip"])
    out = [f"# {name} seen run {run}: tier-1 events in recovered light without a binary period (dropped from the bins): real {int(r.p1_P.isna().sum())}, flip {int(f.p1_P.isna().sum())}"]
    for b in BARS:
        for k, (lo, hi) in enumerate(BINS):
            nr = int(((r.snr >= b) & (r.p1_P >= lo) & (r.p1_P < hi)).sum()); nf = int(((f.snr >= b) & (f.p1_P >= lo) & (f.p1_P < hi)).sum())
            out.append(f"REFBIN {name} recovered bar {b} bin {k} real {nr} flip {nf}")
    return out


def lines(name, run):
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    E = ev[ev.primary].copy()
    E["rec"] = E.recovered.fillna(False).astype(bool)
    out = []
    for light, sub in (("recovered", E[E.rec]), ("kept", E[~E.rec])):
        for b, (r, f) in counts(sub).items():
            out.append(f"REF {name} {light} bar {b} real {r} flip {f}")
    return out


if __name__ == "__main__":
    name, run = C.DS.NAME, os.environ["SS_RUN"]
    if "--bins" in sys.argv:                                     # Amendment 3: per-bin reference counts go to their own file (the Amendment 2 file stays as it was, with its hash)
        out = bin_lines(name, run)
        print("\n".join(out))
        if "--write" in sys.argv:
            f = C.ROOT / "research" / "stage3" / "R1-S1-REFERENCE-BINS.txt"
            head = "" if f.exists() else ("Re-search 1, Amendment 3: reference counts of the SEEN stars by binary-period bin (tier-1, PDCSAP half, recovered light, development runs, counts only). Written 11 Nov 2026 BEFORE the freeze.\n"
                                          "Lines: REFBIN <list> recovered bar <SNR bar> bin <0..4: 5-10, 10-14, 14-20, 20-27.4, over 27.4 d> real <n> flip <n>. Made by pipeline/r1_reference_counts.py --bins.\n")
            with open(f, "a", encoding="utf-8", newline="\n") as h:
                h.write(head + "\n".join(out) + "\n")
        sys.exit(0)
    out = lines(name, run)
    print("\n".join(out))
    if "--write" in sys.argv:
        f = C.ROOT / "research" / "stage3" / "R1-S1-REFERENCE-COUNTS.txt"
        head = "" if f.exists() else ("Re-search 1, Amendment 2: reference counts of the SEEN stars (tier-1, PDCSAP half, development runs, counts only). Written 11 Nov 2026 BEFORE the freeze and before any unseen star was read.\n"
                                      "Lines: REF <list> <recovered|kept> bar <SNR bar> real <n> flip <n>. Made by pipeline/r1_reference_counts.py.\n")
        with open(f, "a", encoding="utf-8") as h:
            h.write(head + f"# {name} seen run {run}\n" + "\n".join(out) + "\n")
