"""Stage 2 report. PUBLISHABLE OUTPUT = AGGREGATES ONLY (research/stage2-2026-10-23/aggregate.txt): no TIC, no event time.
Per-event details go to D:\\second-sun\\data\\stage2\\survivors_LOCAL.csv (git-ignored). Usage: python stage2_report.py"""
import json, glob, re, io, contextlib, pathlib
import numpy as np, pandas as pd

D = pathlib.Path(r"D:\second-sun\data\stage2")
PUB = pathlib.Path(r"D:\second-sun\research\stage2-2026-10-23"); PUB.mkdir(exist_ok=True)
st = pd.read_csv(r"D:\second-sun\targets\stage2_stars.csv")
best = pd.read_csv(r"D:\second-sun\research\audit-2026-10-23\best_per_star_sector.csv")[["tic", "sector", "product"]].rename(columns={"product": "best"})
ev, inj, meta, errs = [], [], [], 0
for p in glob.glob(str(D / "groups" / "*.json")):
    g = json.load(open(p)); ev += g["events"]; inj += g["inj"]; meta += [dict(m, tic=g["tic"], sector=g["sector"]) for m in g["meta"]]
ev, inj, meta = pd.DataFrame(ev), pd.DataFrame(inj), pd.DataFrame(meta)
buf = io.StringIO()


def P(*a):
    print(*a); print(*a, file=buf)


tbin = lambda T: pd.cut(T, [0, 11, 12, 14], right=False, labels=["bright<11", "mid11-12", "faint12+"])
ev = ev.merge(st[["tic", "stratum", "tmag", "name"]], on="tic").merge(best, on=["tic", "sector"], how="left")
ev["tb"] = tbin(ev.tmag); ev["primary"] = ev["product"] == ev["best"]
ev["gap_dump"] = ev["flags"].fillna("").str.contains("gap edge|momentum dump")
ev["flipmatch"] = ev["flags"].fillna("").str.contains("flipped")
ev["burst"] = ev.burst_n >= 3
ev["c8_has"] = ev.c8_n > 0
tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#")
PH_D = 0.35                                                # rule C5: flag events within 0.35 d of a catalogue primary eclipse or of phase 0.5


def eclipse_phase_dist(r):
    """Days from the event to the nearest catalogue primary eclipse or phase-0.5 (circular secondary), over all catalogue periods of the star
    (Kepler-era ephemeris, so this works even where the automatic mask found no eclipse)."""
    best = np.inf
    for q in tg[tg.tic == r.tic].itertuples():
        ph = ((r.center - (q.bjd0 - 57000.0)) / q.p_bin_d) % 1.0
        best = min(best, min(ph, 1 - ph) * q.p_bin_d, abs(ph - 0.5) * q.p_bin_d)
    return best


ev["ph_d"] = ev.apply(eclipse_phase_dist, axis=1)
ev["c5"] = ev.ph_d < PH_D
meta = meta.merge(best, on=["tic", "sector"], how="left")
ok = meta[meta.status == "ok"]
P(f"STAGE 2 aggregate report (no star IDs, no event times). Groups searched: {len(glob.glob(str(D / 'groups' / '*.json')))}")
P(f"files: {len(meta)}; searched ok: {len(ok)} ({ok['product'].value_counts().to_dict()}); other status: {meta[meta.status != 'ok'].status.value_counts().to_dict()}")
pr_ss = ok[ok["product"] == ok["best"]].drop_duplicates(["tic", "sector"])
P(f"star-sectors searched with their best product: {len(pr_ss)}; with a second product available for rule C8: "
  f"{int(ev[ev.primary].drop_duplicates(['tic', 'sector']).shape[0] and (ok.groupby(['tic', 'sector']).size() >= 2).sum())} of {ok.drop_duplicates(['tic', 'sector']).shape[0]}")
pr_ss = pr_ss.merge(st[["tic", "tmag", "stratum"]], on="tic"); pr_ss["tb"] = tbin(pr_ss.tmag)
nss = pr_ss.groupby("tb", observed=True).size()
E = ev[ev.primary]
R, F = E[E.kind == "real"], E[E.kind == "flip"]

P("\n1. EVENTS PER STAR-SECTOR (best product, SNR >= 7): real curve vs upside-down curve (false-alarm proxy)")
for thr in (7, 8, 9, 10, 12, 20):
    r, f = (R.snr >= thr).sum(), (F.snr >= thr).sum()
    P(f"  SNR >= {thr:>2}: real {r:4d} ({r / len(pr_ss):.3f} per star-sector) | upside-down {f:4d} ({f / len(pr_ss):.3f}) | real/upside-down = {r / max(f, 1):.2f}")
P("  by brightness (SNR >= 7): star-sectors, real per star-sector, upside-down per star-sector")
for b, n in nss.items():
    P(f"    {b:10s} n={n:4d} real {(R.tb == b).sum() / n:.3f} | upside-down {(F.tb == b).sum() / n:.3f}")

P("\n2. CUTS, applied one after another to the SNR >= 7 events of the best product (real | upside-down)")


def waterfall(X, label):
    a = X
    b = a[~a.gap_dump]
    c = b[~b.burst]
    d0 = c[~c.flipmatch]
    d = d0[~d0.c5]                                         # rule C5: not at a catalogue eclipse phase
    e3 = d[(d.c8_best.fillna(99) >= 3) | ~d.c8_has]       # lenient: events with no second product are kept
    e4 = d[(d.c8_best.fillna(99) >= 4) | ~d.c8_has]
    s4 = d[d.c8_has & (d.c8_best >= 4)]                    # strict: only events a second product confirms
    P(f"  {label:12s} start {len(a):4d} | no gap/dump flag {len(b):4d} | not in a same-moment burst {len(c):4d} | not matched upside-down {len(d0):4d} "
      f"| not at an eclipse phase {len(d):4d} | second product SNR>=3 (lenient) {len(e3):4d} | >=4 lenient {len(e4):4d} | >=4 strict {len(s4):4d}")
    return len(a), len(d), len(e4), len(s4)


wr, wf = waterfall(R, "real"), waterfall(F, "upside-down")
P(f"  share of real events with a second product to check: {R.c8_has.mean():.0%}; upside-down: {F.c8_has.mean():.0%}")

P("\n3. WHAT EACH CHECK COSTS IN REAL DIPS: dips injected in every product at the same time (about 12x the star's own 8 h noise), found in product A at SNR >= 7")
ij = inj[inj.snr_A >= 7]
if len(ij):
    P(f"  injected dips found in the product they were put in: {len(inj[inj.snr_A >= 7])} of {len(inj)} product-trials ({len(inj[inj.snr_A >= 7]) / len(inj):.0%})")
    for thr in (3, 4, 5):
        k = ij[ij.snr_B.fillna(-1) >= thr]
        P(f"  second product shows it at SNR >= {thr}: {len(k)} of {len(ij)} = {len(k) / len(ij):.0%} kept")
    P("  by product pair (A -> B), share kept at SNR >= 4:")
    for (a, b), g in ij.groupby(["A", "B"]):
        P(f"    {a:9s} -> {b:9s} n={len(g):4d}  {(g.snr_B.fillna(-1) >= 4).mean():.0%}")
    both = F[F.c8_has]
    P(f"  compare: upside-down false alarms confirmed by a second product at SNR >= 4: {(both.c8_best >= 4).sum()} of {len(both)} = {(both.c8_best >= 4).mean():.0%}")
    P(f"  so the second-product check removes {1 - (both.c8_best >= 4).mean():.0%} of false alarms and loses {1 - (ij.snr_B.fillna(-1) >= 4).mean():.0%} of real dips")

P("\n4. ECLIPSE LEAKAGE: distance of events from the masked eclipses, in eclipse widths (real vs upside-down; an excess of real events just outside the mask means leakage)")
bins = [(0, 2), (2, 3), (3, 5), (5, 10), (10, 1e9)]
for lo, hi in bins:
    r = ((R.ecl_w >= lo) & (R.ecl_w < hi)).sum(); f = ((F.ecl_w >= lo) & (F.ecl_w < hi)).sum()
    P(f"  {lo:>2} to {('end' if hi > 1e8 else hi):>3} widths: real {r:4d} ({r / max(len(R), 1):.0%}) | upside-down {f:4d} ({f / max(len(F), 1):.0%})")
P(f"  events on stars with no detected eclipse run: real {R.ecl_w.isna().sum()}, upside-down {F.ecl_w.isna().sum()}")
P(f"  rule C5 (within {PH_D} d of a catalogue primary or phase-0.5 eclipse): real {int(R.c5.sum())} of {len(R)} ({R.c5.mean():.0%}), upside-down {int(F.c5.sum())} of {len(F)} ({F.c5.mean():.0%})")
P(f"    of the real events at an eclipse phase, the automatic mask had found NO eclipse in that product-sector for {int((R.c5 & R.ecl_w.isna()).sum())} of {int(R.c5.sum())}")

P("\n5. KNOWN HOSTS (negative controls: none should show a real crossing in TESS)")
for name in st[st.stratum == "control"].name:
    t = ev[ev.name == name]; tr, tf = t[(t.kind == "real") & t.primary], t[(t.kind == "flip") & t.primary]
    surv = tr[(tr.snr >= 7) & ~tr.gap_dump & ~tr.burst & ~tr.flipmatch]
    P(f"  {name:12s} real events {len(tr):3d} | upside-down {len(tf):3d} | real events that pass the flag cuts {len(surv):3d}")

P("\n6. PROJECTION TO THE FULL CAMPAIGN (5,064 star-sectors; rates per brightness class applied to the campaign's own class sizes)")
camp = {"bright<11": 801, "mid11-12": 1067, "faint12+": 1838 + 1358}
for label, fn in (("all events SNR >= 7 (real curve)", lambda X: X),
                  ("after the flag cuts", lambda X: X[~X.gap_dump & ~X.burst & ~X.flipmatch]),
                  ("... and not at an eclipse phase (C5)", lambda X: X[~X.gap_dump & ~X.burst & ~X.flipmatch & ~X.c5]),
                  ("... and second product SNR >= 4 (lenient)", lambda X: X[~X.gap_dump & ~X.burst & ~X.flipmatch & ~X.c5 & ((X.c8_best.fillna(99) >= 4) | ~X.c8_has)])):
    for kind, X in (("real", R), ("upside-down", F)):
        x = fn(X); tot = sum(((x.tb == b).sum() / nss[b]) * camp[b] for b in camp)
        P(f"  {label:44s} {kind:11s}: about {tot:6.0f} events for a person across the campaign")

P("\n7. SURVIVORS: real, non-control, best product, SNR >= 7, no gap/dump flag, not in a burst, not matched upside-down, not at an eclipse phase, second product SNR >= 3 where one exists")
S = R[(R.stratum != "control") & ~R.gap_dump & ~R.burst & ~R.flipmatch & ~R.c5 & ((R.c8_best.fillna(99) >= 3) | ~R.c8_has)]
P(f"  {len(S)} events on {S.tic.nunique()} stars ({S.groupby('tb', observed=True).size().to_dict()}); strongest SNR {S.snr.max() if len(S) else 'n/a'}; "
  f"{int((S.snr >= 10).sum())} at SNR >= 10; {int((S.c8_has & (S.c8_best >= 4)).sum())} confirmed in a second product at SNR >= 4")
S.sort_values("snr", ascending=False).drop(columns=["tb", "primary"]).to_csv(D / "survivors_LOCAL.csv", index=False)
R.to_csv(D / "events_real_LOCAL.csv", index=False); F.to_csv(D / "events_flip_LOCAL.csv", index=False)
P("  (per-event details are in data\\stage2\\survivors_LOCAL.csv, git-ignored)")

txt = buf.getvalue()
bad = [str(t) for t in st.tic if str(t) in txt]
assert not bad, f"star IDs leaked into the published text: {bad[:3]}"
(PUB / "aggregate.txt").write_text(txt, encoding="utf-8")
