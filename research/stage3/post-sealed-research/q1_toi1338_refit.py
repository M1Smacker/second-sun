# Q1 (31 Oct 2026): TOI-1338 b in the sealed run, re-scored against the later published times. POST HOC, exploratory; the preregistered S6 line (Kostov 2020 Table 6, 1 of 7 strong) is unchanged.
# Times: Wang and Liu 2024 (arXiv:2404.18415) Table 1 = observed mid-transit times (BJD-2457000 = BTJD) for sectors up to 68; Table 3 = photodynamical forecast (BJD-2455000, so BTJD = value - 2000) for sectors 89 to 98.
# The Table 3 forecast was published 29 Apr 2024, before sectors 89 to 98 were observed (2025): those four are an out-of-sample prediction.
import json, os, math
R = r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa"; TIC = 260128333
KOS = {27: 2049.69, 30: 2142.40, 34: 2237.92, 37: 2331.00, 62: 2989.35, 65: 3084.82, 68: 3177.98, 89: 3743.62, 93: 3836.04, 96: 3931.42, 98: 4024.62}
OBS = {27: (2049.9515, .0034), 34: (2238.2258, .0034), 37: (2331.0148, .0024), 62: (2989.6356, .0047), 65: (3085.4243, .0044), 68: (3178.2853, .0077)}
PRED = {89: (5744.4534 - 2000, .0104), 93: (5836.9195 - 2000, .0132), 96: (5932.7322 - 2000, .0183), 98: (6025.5927 - 2000, .0159)}
UPD = {**OBS, **PRED}
tier_rank = {"1A": 0, "1L": 1, "1B": 2, "2": 3, "3": 4}
rows, ps, hits = [], [], 0
print("sector | Kostov time | updated time (source) | shift d | events within 3 sigma + 0.1 d of updated time (kind product tier offset_h dur_h snr) | distinct events in sector (real, flip) | chance P(>=1 event in window)")
for sec in sorted(KOS):
    ev = []
    for sub in ("groups", "groups_sap"):
        p = os.path.join(R, sub, f"{TIC}_{sec}.json")
        if os.path.exists(p):
            ev += json.load(open(p))["events"]
    if sec not in UPD:
        near = [(e["kind"], e["product"], e["tier"], round(24 * (e["center"] - KOS[sec]), 1)) for e in ev if abs(e["center"] - KOS[sec]) < 1.5]
        print(f"{sec} | {KOS[sec]} | no updated time (Wang and Liu excluded S30: damaged egress) | events within 1.5 d of Kostov time: {near}"); continue
    t, s = UPD[sec]; w = 3 * s + 0.1
    inw = [e for e in ev if abs(e["center"] - t) <= w]
    cl = lambda k: len({round(e["center"] * 4) for e in ev if e["kind"] == k})
    n = len({round(e["center"] * 4) for e in ev}); p_ch = min(1.0, n * 2 * w / 27.4)
    src = "obs" if sec in OBS else "forecast"
    desc = "; ".join(f"{e['kind']} {e['product']} tier {e['tier']} {24*(e['center']-t):+.1f} h {e['dur_h']} h snr {e['snr']:.1f}" for e in sorted(inw, key=lambda e: (tier_rank.get(e['tier'], 9), e['product']))) or "none"
    best = min((tier_rank.get(e["tier"], 9) for e in inw if e["kind"] == "real"), default=None)
    rows.append((sec, bool(inw), best, src)); ps.append(p_ch); hits += bool(inw)
    print(f"{sec} | {KOS[sec]} | {t:.4f} ({src}, +-{s}) | {t-KOS[sec]:+.3f} | {desc} | {cl('real')}, {cl('flip')} | {p_ch:.3f}")
# exact Poisson-binomial tail P(hits >= observed) under chance
def tail(ps, k):
    dp = [1.0]
    for p in ps:
        dp = [(dp[i] * (1 - p) if i < len(dp) else 0) + (dp[i - 1] * p if i > 0 else 0) for i in range(len(dp) + 1)]
    return sum(dp[k:])
print(f"\nSectors with an updated time: {len(rows)}; with an event in the window: {hits}; chance probability of that many (Poisson-binomial, uniform events): {tail(ps, hits):.2e}")
oos = [(r, p) for r, p in zip(rows, ps) if r[3] == "forecast"]
print(f"Out-of-sample forecast sectors (89, 93, 96, 98): events in window {sum(r[1] for r,_ in oos)} of {len(oos)}; chance probability {tail([p for _,p in oos], sum(r[1] for r,_ in oos)):.2e}")
keep = sum(1 for r in rows if r[2] is not None and r[2] <= 2)
print(f"Real event in window at tier 1 (1A/1L/1B): {keep}; at tier 2 only: {sum(1 for r in rows if r[2]==3)}; none: {sum(1 for r in rows if r[2] is None)}")
