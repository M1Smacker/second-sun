"""P-03 (Fable audit): the flip-match flag is one-sided. stage2_search.do_group line 190-191: a REAL event with an upside-down event within 0.3 d is flagged
("matched in flipped data") and goes to tier 2; an UPSIDE-DOWN event with a real event within 0.3 d is never flagged (veto(flip, ..., [], ...)).
Counts only: among stored first-tier upside-down events (tier field in groups/*.json, before the v7 and c6 passes of stage3_report), how many have a real event
of the same product within 0.3 d, i.e. would be tier 2 under the rule the real arm gets? Also the reverse count on the real arm (must be 0 by construction).
Usage: python p03_flipmatch_asymmetry.py"""
import json, glob, pathlib
ROOT = pathlib.Path(r"D:\second-sun")
RUNS = {"G3": ROOT / "data/stage3_g3/g3_e7886a71a61f", "G2 sealed": ROOT / "data/stage3_g2/sealed_5f73692944aa"}
T1 = {"1A", "1L", "1B"}
for name, run in RUNS.items():
    n = dict(groups=0, flip_t1=0, flip_t1_matched=0, real_t1=0, real_t1_matched=0, real_t2_only_flipmatch=0)
    for fn in glob.glob(str(run / "groups" / "*.json")):
        g = json.load(open(fn)); n["groups"] += 1; ev = g["events"]
        for e in ev:
            if str(e.get("tier")) in T1:
                other = "real" if e["kind"] == "flip" else "flip"
                m = any(o["kind"] == other and o["product"] == e["product"] and abs(o["center"] - e["center"]) < 0.3 for o in ev)
                k = "flip" if e["kind"] == "flip" else "real"
                n[k + "_t1"] += 1; n[k + "_t1_matched"] += int(m)
            elif e["kind"] == "real" and e.get("flipmatch") and not any(e.get(x) for x in ("gap_dump", "burst", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated")):
                n["real_t2_only_flipmatch"] += 1
    g = n["groups"]
    print(f"{name}: groups {g}; upside-down first-tier {n['flip_t1']} ({1000*n['flip_t1']/g:.2f} per 1000), of which {n['flip_t1_matched']} have a real event within 0.3 d "
          f"-> {n['flip_t1']-n['flip_t1_matched']} ({1000*(n['flip_t1']-n['flip_t1_matched'])/g:.2f} per 1000) under a two-sided rule; "
          f"real first-tier {n['real_t1']} (matched {n['real_t1_matched']}); real events in tier 2 ONLY because of the flip-match flag: {n['real_t2_only_flipmatch']}")
