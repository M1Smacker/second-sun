"""Vesper study phase D1: link tier-1 dips of one star across sectors and count the links of real against upside-down events (the control).
Pool: primary events of one kind, tiers 1A/1L/1B (the frozen chain's own flags), SNR >= 5 (run with VESPER_BAR=5). A link = a seed event plus, from every OTHER sector, the strongest event whose box length is within a factor 1.6 of the seed's
and whose depth is within a factor 2 of the seed's (centred on the seed, not mutual: a ceiling for the null, so it errs towards more false links). Combined SNR = sqrt(sum of squares). Per star and kind the best link counts once.
"New" link = every member below SNR 7 (a link with a member at 7 or more is already a single-dip candidate). Aggregates only: counts of stars per kind.
Usage: SS_SET=g1|g2 python stack_links.py <run folder under data\\stage3 or data\\stage3_g2>   (appends to research\\stage3\\stack-links.txt)"""
import sys
import numpy as np, pandas as pd
import stage3_core as C, stage3_report as R

T1 = ["1A", "1L", "1B"]; BARS = (7, 8, 9, 10, 11, 12)


def best_link(g):
    """g: tier-1 events of one star and one kind. Returns (combined SNR, members, strongest member SNR) of the best link, or None."""
    best = None
    for s in g.itertuples():
        m = g[(g.sector != s.sector) & (g.dur_h / s.dur_h).between(1 / 1.6, 1.6) & (g.depth_ppm / s.depth_ppm).between(0.5, 2.0)]
        if m.empty:
            continue
        m = m.sort_values("snr", ascending=False).drop_duplicates("sector")
        snrs = np.r_[s.snr, m.snr.values]
        comb = float(np.sqrt((snrs ** 2).sum()))
        if best is None or comb > best[0]:
            best = (comb, len(snrs), float(snrs.max()))
    return best


def count(ev, kind, lo=5.0):
    E = ev[ev.primary & (ev.kind == kind) & ev.tier.isin(T1) & (ev.snr >= lo)]
    out = []
    for _, g in E.groupby("tic"):
        b = best_link(g)
        if b:
            out.append(b)
    return out


if __name__ == "__main__":
    run = sys.argv[1]
    ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
    n = len(meta[(meta.status == "ok") & (meta["product"] == meta["best"])].drop_duplicates(["tic", "sector"]))
    lines = [f"{C.DS.NAME} run {run}: {n} star-sectors; pool = tier-1 primary events with SNR >= 5 ({int(((ev.primary) & ev.tier.isin(T1) & (ev.kind == 'real') & (ev.snr >= 5)).sum())} real, "
             f"{int(((ev.primary) & ev.tier.isin(T1) & (ev.kind == 'flip') & (ev.snr >= 5)).sum())} upside-down; of those below SNR 7: "
             f"{int(((ev.primary) & ev.tier.isin(T1) & (ev.kind == 'real') & (ev.snr >= 5) & (ev.snr < 7)).sum())} real, {int(((ev.primary) & ev.tier.isin(T1) & (ev.kind == 'flip') & (ev.snr >= 5) & (ev.snr < 7)).sum())} upside-down)"]
    for kind in ("real", "flip"):
        L = count(ev, kind)
        for label, sel in (("new links (all members below SNR 7)", lambda b: b[2] < 7), ("all links", lambda b: True)):
            row = " / ".join(f"{B}: {sum(1 for b in L if sel(b) and b[0] >= B)}" for B in BARS)
            lines.append(f"   {'real' if kind == 'real' else 'upside-down':11s} {label}, stars with a best link at combined SNR >= bar: {row}")
    txt = "\n".join(lines); print(txt)
    with open(C.ROOT / "research" / "stage3" / "stack-links.txt", "a", encoding="utf-8") as fh:
        fh.write(txt + "\n")
