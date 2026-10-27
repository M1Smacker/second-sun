"""Stage 3 report, PUBLISHABLE OUTPUT = AGGREGATES ONLY (no TIC, no event time). Works on any folder of group JSONs, including Stage 2's (events are enriched on
the fly), so it can be checked against Stage 2's published numbers. Differences from stage2_report.py: tiers (1A, 1L, 1B, 2, 3), the QLP-only share, the
share of the timeline C5 covers, class sizes derived from data, and the planning number is the REAL-curve tier-1 count (upside-down is only an upper bound).
Usage: python stage3_report.py <groups_dir> [label]   (writes research\\stage3\\aggregate_<label>.txt)"""
import sys, glob, json, pathlib
import numpy as np, pandas as pd
import stage3_core as C


def load(groups_dir, extra=True):
    ephem, qlp = C.Ephem(pd.read_csv(C.TARGETS, comment="#")), C.qlp_only_tics()
    ev, meta = [], []
    for p in glob.glob(str(pathlib.Path(groups_dir) / "*.json")):
        g = json.load(open(p))
        ev += g["events"] if all("tier" in e for e in g["events"]) else C.enrich_group(g, ephem, qlp, extra)
        meta += [dict(m, tic=g["tic"], sector=g["sector"]) for m in g["meta"]]
    best = pd.read_csv(C.BEST)[["tic", "sector", "product"]].rename(columns={"product": "best"})
    ev = pd.DataFrame(ev).merge(best, on=["tic", "sector"], how="left")
    ev["primary"] = ev["product"] == ev["best"]
    ev["c8_best"] = pd.to_numeric(ev.c8_best, errors="coerce")
    return ev, pd.DataFrame(meta).merge(best, on=["tic", "sector"], how="left")


def waterfall(X):
    """Same order and rules as stage2_report.waterfall: start, no gap/dump, no burst, not matched upside-down, not at an eclipse phase (C5),
    second product >= 3 (lenient), >= 4 (lenient), >= 4 (strict)."""
    b = X[~X.gap_dump]; c = b[~b.burst]; d0 = c[~c.flipmatch]; d = d0[~d0.c5]
    has = d.second_product
    return (len(X), len(b), len(c), len(d0), len(d), len(d[(d.c8_best.fillna(99) >= 3) | ~has]), len(d[(d.c8_best.fillna(99) >= 4) | ~has]),
            len(d[has & (d.c8_best >= 4)]))


def report(groups_dir):
    ev, meta = load(groups_dir)
    tg = pd.read_csv(C.TARGETS, comment="#").drop_duplicates("tic").set_index("tic")
    ok = meta[meta.status == "ok"]; pr = ok[ok["product"] == ok["best"]].drop_duplicates(["tic", "sector"])
    pr = pr.assign(tb=pd.cut(pr.tic.map(tg.tmag), C.TBINS, right=False, labels=C.TLABELS)); nss = pr.groupby("tb", observed=True).size()
    E = ev[ev.primary].assign(tb=lambda x: pd.cut(x.tic.map(tg.tmag), C.TBINS, right=False, labels=C.TLABELS))
    R, F = E[E.kind == "real"], E[E.kind == "flip"]
    out = []
    P = out.append
    P(f"STAGE 3 aggregate report (no star IDs, no event times). Groups: {len(glob.glob(str(pathlib.Path(groups_dir) / '*.json')))}; star-sectors with a best product searched: {len(pr)}")
    P("\n1. CUTS in order (real | upside-down): start, no gap/dump, no burst, not matched upside-down, not at an eclipse phase (C5), second product >=3 lenient, >=4 lenient, >=4 strict")
    for lab, X in (("real", R), ("upside-down", F)):
        P(f"  {lab:12s} " + " | ".join(str(v) for v in waterfall(X)))
    P("\n2. TIERS of the best-product events (1A second product agrees >=4; 1L 3 to 4; 1B no second product; 2 flagged; 3 second product disagrees)")
    for lab, X in (("real", R), ("upside-down", F)):
        t = X.tier.value_counts().reindex(["1A", "1L", "1B", "2", "3"]).fillna(0).astype(int)
        P(f"  {lab:12s} " + "  ".join(f"{k} {v}" for k, v in t.items()))
    t1 = R[R.tier.isin(["1A", "1L", "1B"])]
    P(f"  real tier-1 events on QLP-only stars: {int(t1.qlp_only_star.sum())} of {len(t1)} (no second product is possible there)")
    P("\n3. HOW MUCH TIMELINE C5 COVERS (windows of 0.35 d around the primary and phase 0.5): stars with at least 5% / 10% / 20% / 30% of the timeline")
    cov = C.c5_timeline_cover()
    P("  " + " | ".join(f">= {int(q * 100)}%: {int((cov >= q).sum())} of {len(cov)}" for q in (0.05, 0.1, 0.2, 0.3)))
    P("\n4. PROJECTION TO THE CAMPAIGN (class sizes derived from data; rates per brightness class from this sample; REAL-curve tier-1 is the planning number, upside-down is an upper bound)")
    camp, nsec, nan = C.class_sizes()
    P(f"  campaign star-sectors by class: {camp} (total {nsec}, without a magnitude class {nan})")
    for lab, X in (("real tier-1", R[R.tier.isin(['1A', '1L', '1B'])]), ("real tier-1 + tier 2 (all real)", R), ("upside-down tier-1 (upper bound)", F[F.tier.isin(['1A', '1L', '1B'])])):
        tot = sum((X.tb == b).sum() / nss[b] * camp[b] for b in camp if b in nss.index)
        P(f"  {lab:34s}: about {tot:6.0f} events across the campaign")
    txt = "\n".join(out)
    leaked = [str(t) for t in ev.tic.unique() if str(t) in txt]
    assert not leaked, f"star IDs leaked into the published text: {leaked[:3]}"
    return txt


if __name__ == "__main__":
    txt = report(sys.argv[1]); print(txt)
    if len(sys.argv) > 2:
        d = C.ROOT / "research" / "stage3"; d.mkdir(exist_ok=True)
        (d / f"aggregate_{sys.argv[2]}.txt").write_text(txt, encoding="utf-8")
