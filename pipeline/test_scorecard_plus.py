"""Checks for scorecard_plus.py (Amendment 2, 2 Nov 2026). Part 1 needs no data. Part 2 reproduces, from the sealed run on this PC, the numbers written in
research/stage3/post-sealed-literature-2026-10-31.md on 31 Oct (they came from one-off scripts); a failure means the port changed a number. Part 3 is a mutation: swapped labels must give the inverse ratio.
Usage: SS_SET=g2 VESPER_OPTS=c6 python test_scorecard_plus.py"""
import os
os.environ["SS_SET"] = "g2"; os.environ["VESPER_OPTS"] = "c6"
import numpy as np, pandas as pd
import scorecard_plus as S, stage3_core as C

ok = lambda cond, msg: (print(("pass: " if cond else "FAIL: ") + msg), cond)[1]
res = []

# part 1: wording rules and small helpers, no data
res.append(ok("below the mark" in S.s2_reading(2, 1000), "S2 with 2 in 1,000 star-sectors is below the mark of 8"))
res.append(ok("above the mark" in S.s2_reading(30, 1000), "S2 with 30 in 1,000 is above the mark"))
res.append(ok("BORDERLINE" in S.s2_reading(8, 1000), "S2 with 8 in 1,000 is borderline (interval includes 8)"))
res.append(ok("BORDERLINE" in S.s2_reading(59, 6734) and "8.76" in S.s2_reading(59, 6734), "the sealed S2 reading (59 in 6,734) is borderline at 8.76 per 1,000"))
res.append(ok(S.compare_word(30, 40, 10, 20) == "better in this slice" and S.compare_word(10, 20, 30, 40) == "worse in this slice" and S.compare_word(10, 30, 20, 40) == "no clear difference",
              "better, worse and no clear difference are told apart by non-overlapping intervals"))
res.append(ok(abs(S.tail([0.5, 0.5], 1) - 0.75) < 1e-12 and abs(S.tail([0.2], 1) - 0.2) < 1e-12 and abs(S.tail([0.3, 0.3], 0) - 1.0) < 1e-12 and abs(S.tail([0.3, 0.3], 2) - 0.09) < 1e-12, "Poisson-binomial tail is exact on small cases"))
lo, hi = S.wilson(0, 10)
res.append(ok(lo == 0 and 20 < hi < 35, "Wilson interval for 0 of 10 starts at 0"))

# part 2: reproduce the 31 Oct numbers on the sealed run (skipped when the data are not on this machine)
run = "sealed_5f73692944aa"
if (C.DS.RUNS / run / "groups").exists():
    E, meta = S.load_events(run)
    rows = {r["bar"]: r for r in S.star_table(E, 594)}
    res.append(ok(abs(rows[7]["ratio"] - 1.18) < 0.005 and abs(rows[12]["ratio"] - 1.54) < 0.005, f"ratio per bar 1.18 ... 1.54 (got {rows[7]['ratio']:.3f}, {rows[12]['ratio']:.3f})"))
    res.append(ok([round(rows[b]["detectable"]) for b in S.BARS] == [33, 27, 17, 13], "detectable excess 33, 27, 17, 13 kept dips at bars 7, 8, 10, 12"))
    res.append(ok((rows[7]["real"], rows[7]["real_stars"], rows[7]["flip"], rows[7]["flip_stars"]) == (26, 17, 59, 36), "bar 7: 26 real on 17 stars, 59 upside-down on 36 stars"))
    res.append(ok(abs(rows[7]["trims"][25][0] - 1.36) < 0.005, "ratio after dropping the 25 heaviest stars is 1.36"))
    pl = pd.concat([S.planted("sealed").assign(sl="sealed"), S.planted("g2dev").assign(sl="dev")])
    price = {r["check"]: r for r in S.price_table(E, pl)}
    res.append(ok(price["step"]["add_flip"] == 68 and price["step"]["add_real"] == 94 and abs(price["step"]["gain_sealed"] - 9.8) < 0.1, "step check: +9.8 planted points for +68 upside-down (+94 real) events"))
    res.append(ok(price["flipmatch"]["add_flip"] == 0 and price["c5"]["add_flip"] == 0, "dropping flipmatch or c5 lets no upside-down event in"))
    ss = meta[meta.status == "ok"].drop_duplicates(["tic", "sector"]).groupby("tic").size()
    eff = S.efficiency(pl, float(ss.mean()), 594)
    r13 = [r for r in eff["rows"] if r["depth"] == 2300][0]
    res.append(ok(abs(r13["det"][1] - 0.62) < 0.01 and abs(100 * r13["lim95"][0] - 2.2) < 0.1, f"TOI-1338 b-like planet at P = 95 d: 0.62 detections per planet-bearing star, limit 2.2% (got {r13['det'][1]:.2f}, {100 * r13['lim95'][0]:.1f}%)"))
    t = S.toi1338(C.DS.RUNS / run)
    res.append(ok(sum(r["hit"] for r in t) == 7 and len(t) == 10 and sum(r["hit"] for r in t if r["src"] == "forecast") == 4 and sum(1 for r in t if r["best"] is not None and r["best"] <= 2) == 4,
                  "TOI-1338 b: 7 of 10 sectors hold a real event, 4 of 4 forecast sectors, 4 at tier 1"))
    res.append(ok(any("step" in e["flags"] for r in t for e in r["events"]) and any("gap_dump" in e["flags"] for r in t for e in r["events"]), "the loss ledger names the flags that cost transits (step and gap_dump seen)"))
    # part 3: mutation. Swap the kinds: the ratio must invert and the real count must become the old upside-down count
    M = E.copy(); M["kind"] = M.kind.map({"real": "flip", "flip": "real"})
    m7 = {r["bar"]: r for r in S.star_table(M, 594)}[7]
    res.append(ok(abs(m7["ratio"] - 1 / rows[7]["ratio"]) < 0.005 and m7["real"] == rows[7]["flip"], "mutation: swapped kinds invert the ratio and swap the counts (the test can fail)"))
else:
    print("skipped part 2 and 3: the sealed run is not on this machine")

print(f"\n{sum(res)} of {len(res)} checks passed")
raise SystemExit(0 if all(res) else 1)
