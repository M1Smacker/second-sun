"""Pair search: link single dips of one star across different sectors (a long-period planet may show one dip per sector it was caught in).
Works on the events of a FROZEN Stage 3 run; changes nothing in the detector. PRINTS AGGREGATES ONLY (no TIC, no time), safe to paste into notes.
Rules fixed before any result was looked at: two dips pair if they are in different sectors of the same star, their depths are within a factor DEPTH_RATIO and
their durations within DUR_RATIO. The same dip seen in several products of one sector counts once (the strongest). The same rules run on the upside-down
copies: real pairs are only interesting if they beat what the upside-down pairs predict (scaled by dips squared). The unit of the noise line is STARS WITH A PAIR, not pairs:
k similar dips on one star make k(k-1)/2 pairs that are not independent. Two things were changed after the first print, and both are logged in learnings section 14: the first print
counted any product's version of a dip (24 clean real dips, 10 real pairs against 2 upside-down), but the aggregate report judges each dip by its BEST product (14 clean real dips); and it counted pairs, not stars.
NOT done here (needs the observed time stamps): a check that the shorter-period aliases (gap/n) fall in data gaps.
Usage: python pair_search.py [hash12]"""
import sys, collections
import stage3_report as R

ROOT = r"D:\second-sun\data\stage3"
DEPTH_RATIO = 1.5
DUR_RATIO = 1.5
CLUSTER_D = 0.5
HARD = ("gap_dump", "burst", "flipmatch", "c5", "ecl_overlap")
CLASSES = {
    "clean (tier 1A, 1L, 1B)": lambda e: e["tier"] in ("1A", "1L", "1B"),
    "soft (tier 1 or 2 with no data-quality or eclipse flag)": lambda e: e["tier"] in ("1A", "1L", "1B", "2") and not any(e.get(k) for k in HARD),
}


def one_per_dip(events):
    """Collapse the same dip found in several products of one sector to the strongest one."""
    out = []
    for e in sorted(events, key=lambda e: -e["snr"]):
        if not any(o["sector"] == e["sector"] and abs(o["center"] - e["center"]) < CLUSTER_D for o in out):
            out.append(e)
    return out


def ratio_ok(a, b, lim):
    return a > 0 and b > 0 and max(a, b) / min(a, b) <= lim


def pairs_of(events):
    """Days between the two dips of every pair among the events of ONE star and kind."""
    ev = one_per_dip(events)
    return [abs(a["center"] - b["center"]) for i, a in enumerate(ev) for b in ev[i + 1:]
            if a["sector"] != b["sector"] and ratio_ok(a["depth_ppm"], b["depth_ppm"], DEPTH_RATIO) and ratio_ok(a["dur_h"], b["dur_h"], DUR_RATIO)]


def collect(h):
    """Best-product events only, the same unit the aggregate report counts."""
    ev, _ = R.load(rf"{ROOT}\{h}\groups")
    by = collections.defaultdict(list)
    for e in ev[ev.primary].to_dict("records"):
        by[(e["kind"], e["tic"])].append(e)
    return by


def summarize(by, pred, kind):
    stars = {k[1]: [e for e in v if pred(e)] for k, v in by.items() if k[0] == kind}
    n_ev = sum(len(one_per_dip(v)) for v in stars.values())
    dts = [dt for v in stars.values() for dt in pairs_of(v)]
    n_star = sum(1 for v in stars.values() if pairs_of(v))
    bins = (sum(d < 60 for d in dts), sum(60 <= d < 365 for d in dts), sum(d >= 365 for d in dts))
    return dict(events=n_ev, stars_with_events=sum(1 for v in stars.values() if v), pairs=len(dts), stars_with_pair=n_star, bins=bins)


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else "5392f864e810"
    by = collect(h)
    print(f"PAIR SEARCH on frozen run {h}. Rules: different sectors, depths within x{DEPTH_RATIO}, durations within x{DUR_RATIO}, one count per dip. Aggregates only.")
    for name, pred in CLASSES.items():
        r, f = summarize(by, pred, "real"), summarize(by, pred, "flip")
        print(f"\n{name}")
        for lab, s in (("real", r), ("upside-down", f)):
            print(f"  {lab:12s}: {s['events']:4d} dips on {s['stars_with_events']:3d} stars | pairs {s['pairs']:3d} on {s['stars_with_pair']:3d} stars | gap between the two dips: under 60 d {s['bins'][0]}, 60 to 365 d {s['bins'][1]}, over 365 d {s['bins'][2]}")
        if r["events"] and f["events"]:
            lam, chance = R.noise_expected(r["stars_with_pair"], f["stars_with_pair"], (f["events"] / r["events"]) ** 2)
            print(f"  noise-expected real stars with a pair (upside-down stars with a pair x (real dips / upside-down dips) squared): {lam:.2f}; real {r['stars_with_pair']}; chance of at least that many from noise {chance:.2f}")
