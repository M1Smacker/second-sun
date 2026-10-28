"""Compare two Stage 3 runs event by event. PRINTS AGGREGATES ONLY (no TIC, no time), safe to paste into research notes.
An event of the new run is UNCHANGED if the old run has an event in the same star-sector, product and kind with the same box length, the same signal-to-noise
and a centre within 0.02 d. Otherwise it is NEW (box length 20 h, or a shorter one that appears or moves because a longer box took over a dip). Old events with
no unchanged partner are DROPPED (absorbed into a 20 h event or moved). Tiers are compared as counts; the flags of unchanged events must not change.
Usage: python compare_versions.py <old_hash12> <new_hash12>"""
import sys, glob, json, collections
import pandas as pd

ROOT = r"D:\second-sun\data\stage3"


def load(h):
    rows = []
    for p in glob.glob(rf"{ROOT}\{h}\groups\*.json"):
        g = json.load(open(p))
        rows += [dict(e, key=(g["tic"], g["sector"], e["product"], e["kind"])) for e in g["events"]]
    return pd.DataFrame(rows)


def match(a, b):
    """Boolean per row of `a`: has an unchanged partner in `b`."""
    idx = collections.defaultdict(list)
    for r in b.itertuples():
        idx[r.key].append((r.center, r.dur_h, r.snr))
    return a.apply(lambda r: any(abs(c - r.center) < 0.02 and d == r.dur_h and abs(s - r.snr) < 1e-6 for c, d, s in idx.get(r.key, [])), axis=1)


if __name__ == "__main__":
    old, new = load(sys.argv[1]), load(sys.argv[2])
    new["same"], old["same"] = match(new, old), match(old, new)
    print(f"old {sys.argv[1]}: {len(old)} events | new {sys.argv[2]}: {len(new)} events")
    for kind in ("real", "flip"):
        o, n = old[old.kind == kind], new[new.kind == kind]
        n20 = n[n.dur_h == 20]
        print(f"  {kind:5s}: old {len(o):5d} | new {len(n):5d} | unchanged {int(n.same.sum()):5d} | new 20 h {len(n20):4d} | new shorter-box events {int((~n.same & (n.dur_h != 20)).sum()):4d} | old dropped {int((~o.same).sum()):4d}")
    for kind in ("real", "flip"):
        for lab, d in (("old", old), ("new", new)):
            t = d[d.kind == kind].tier.value_counts().reindex(["1A", "1L", "1B", "2", "3"]).fillna(0).astype(int)
            print(f"  tiers {kind:5s} {lab}: " + "  ".join(f"{k} {v}" for k, v in t.items()))
    t1 = new[new.tier.isin(["1A", "1L", "1B"])]
    print("  new run tier-1 events by box length (real | upside-down): " + ", ".join(
        f"{d:g} h {int(((t1.dur_h == d) & (t1.kind == 'real')).sum())}|{int(((t1.dur_h == d) & (t1.kind == 'flip')).sum())}" for d in sorted(new.dur_h.unique())))
    both = new[new.same].merge(old[old.same], on=["key", "center", "dur_h"], suffixes=("_n", "_o"))
    for f in ("c5", "ecl_overlap", "step", "ramp", "repeater", "gap_dump"):
        if f + "_n" in both and f + "_o" in both:
            print(f"  flag {f:12s} differs on unchanged events: {int((both[f + '_n'] != both[f + '_o']).sum())} of {len(both)}")
