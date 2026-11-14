"""T54: the funnel of a finished run must equal the scorecard's counts (Claude, 14 Nov 2026). Usable on any finished run; the G1 readout runs it.
The funnel (leads_export.build, what the Search window shows) and an independent recount (pandas on stage3_report.load, best product, PDCSAP half,
the selection r1_readout.t1_counts uses) must give the same Dips / Kept / Confirmed numbers, real and upside-down. A difference means the page
and the verdict disagree (it happened once: LEADS-RULES Amendment 1, 129 against 26).
Usage (from pipeline/): SS_SET=g2 SS_RUN=r1dev_g2_seen_bcd29c7aabb0 VESPER_OPTS=c6,p1 python test_funnel_scorecard.py
Default run is the design-seen G2 development run (never a fenced or sealed folder by default)."""
import os, sys, pathlib
os.environ.setdefault("SS_SET", "g2"); os.environ.setdefault("SS_RUN", "r1dev_g2_seen_bcd29c7aabb0"); os.environ.setdefault("VESPER_OPTS", "c6,p1")
import dataset as DS
import leads_export as L
import stage3_report as R

KEPT, CONF = {"1A", "1L", "1B"}, {"1A"}


def recount(run):
    ev, _ = R.load(str(pathlib.Path(run) / "groups"))
    e = R.pdc_half(ev[ev.primary]).copy()
    e["key"] = list(zip(e.tic.astype(int), e.sector.astype(int), e["product"], e.center.astype(float).round(4)))
    out = {}
    for name, sel in (("Dips", e), ("Kept", e[e.tier.isin(KEPT)]), ("Conf", e[e.tier.isin(CONF)])):
        out[name] = (sel[sel.kind == "real"].key.nunique(), sel[sel.kind == "flip"].key.nunique())
    out["_rows_kept"] = (int(((e.kind == "real") & e.tier.isin(KEPT)).sum()), int(((e.kind == "flip") & e.tier.isin(KEPT)).sum()))
    return out


def funnel(run):
    out = L.build(run, {}, {}, True, False, None, {}, known=set(), rows=L.final_rows(run, {}))  # MAX_CARDS = 0 below: no card or picture is built
    return {s["label"][:4]: (s["real"], s["flip"]) for s in out["stages"]}


if __name__ == "__main__":
    run = DS.RUNS / os.environ["SS_RUN"]
    if os.environ["SS_RUN"].startswith(("r1_", "sealed_")) and os.environ.get("ALLOW_SEALED") != "1":
        sys.exit("refused: a sealed or unseen run needs ALLOW_SEALED=1 (counts only)")
    rc = recount(run)
    import leads_export
    leads_export.MAX_CARDS = 0                                 # no picture is built: counts only
    fn = funnel(run)
    print("recount:", {k: v for k, v in rc.items()}, "\nfunnel: ", fn)
    bad = [k for k in ("Dips", "Kept", "Conf") if fn.get(k) != rc[k]]
    if rc["_rows_kept"] != rc["Kept"]:
        print(f"note: {rc['_rows_kept']} kept rows against {rc['Kept']} distinct events (duplicate rows exist; both counts use distinct events)")
    if bad:
        sys.exit(f"FUNNEL AND SCORECARD DISAGREE at {bad}")
    print("funnel equals the scorecard counts")
