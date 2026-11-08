"""FFI door stage C: existence census for the 400 preregistered stars. COUNTS ONLY in the repo; per-star table stays in data\\ffi_door_2026-11-08 (git-ignored).

For each star: (1) which sectors TESS pointed at its position (MAST TESSCut sector lookup, read-only; sectors <= 109 = completed),
(2) which sectors have a QLP, TESS-SPOC FFI, TGLC, GSFC-ELEANOR-LITE, CDIPS, T16 or TARS high-level product on MAST (CAOM, read-only queries by TIC id, obs_collection HLSP),
(3) whether it has mission-produced 2-minute light curves (obs_collection TESS, SPOC) -- must be none (the exclusion list covers sectors 1-111).
No light curve file is downloaded. Metrics from FFI-DOOR-TEST-PLAN-2026-11-08.md: U1 (loader-readable FFI light curve in at least 2 sectors), U6 (both QLP and TESS-SPOC in a star-sector).
"""
import collections, json, os, sys, time, urllib.parse, urllib.request
import numpy as np
import pandas as pd

ROOT = r"D:\second-sun"; D = os.path.join(ROOT, "data", "ffi_door_2026-11-08")
from concurrent.futures import ThreadPoolExecutor

s = pd.read_csv(os.path.join(D, "sample_400.csv"))
s["tic"] = s["tic"].astype(int)
LAST_DONE = 109   # sector 110 is in progress on 8 Nov 2026 (RESUME)
out = []
def say(x=""):
    print(x); out.append(x)

# ---- (1) pointing: MAST TESSCut sector lookup (no external code is run)
def sectors_of(row):
    url = "https://mast.stsci.edu/tesscut/api/v0.1/sector?" + urllib.parse.urlencode({"ra": row["ra0"], "dec": row["dec0"], "radius": "0d"})
    for attempt in range(6):
        try:
            js = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "SecondSunResearch/1.0"}), timeout=90).read().decode())
            return sorted({int(x["sector"]) for x in js.get("results", [])})
        except Exception:
            time.sleep(4 * (attempt + 1))
    return None
ids = s["tic"].values
rows_ = [r for _, r in s.iterrows()]
with ThreadPoolExecutor(max_workers=4) as ex:
    sl = list(ex.map(sectors_of, rows_))
failed = sum(1 for x in sl if x is None)
obs = collections.defaultdict(set)
for t_, lst in zip(s["tic"], sl):
    for x in (lst or []):
        if 1 <= x <= LAST_DONE:
            obs[int(t_)].add(int(x))
s["n_obs_sectors"] = [len(obs[t_]) for t_ in s["tic"]]
say("FFI door stage C (counts only). Sample: %d stars; sha256 of the sample file is in data\ffi_door_2026-11-08\sample_400.sha256 (e8d30070...)." % len(s))
say("TESSCut sector service: lookups failed for %d stars; sectors 1..%d that pointed at the star position: median %d, min %d, max %d; stars never on silicon: %d" % (
    failed, LAST_DONE, int(s["n_obs_sectors"].median()), int(s["n_obs_sectors"].min()), int(s["n_obs_sectors"].max()), int((s["n_obs_sectors"] == 0).sum())))

# ---- (2) CAOM
API = "https://mast.stsci.edu/api/v0/invoke"
def invoke(req):
    body = urllib.parse.urlencode({"request": json.dumps(req)}).encode()
    for attempt in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(API, data=body, headers={"User-Agent": "SecondSunResearch/1.0"}), timeout=180)
            return json.loads(r.read().decode())
        except Exception as e:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("MAST failed")
def caom(tics, collections_):
    rows = []
    for i in range(0, len(tics), 60):
        chunk = [str(int(t)) for t in tics[i:i + 60]]
        page = 1
        while True:
            js = invoke({"service": "Mast.Caom.Filtered", "format": "json", "pagesize": 5000, "page": page,
                         "params": {"columns": "obsid,obs_collection,provenance_name,target_name,sequence_number,t_min,t_max,dataproduct_type,project,obs_id",
                                    "filters": [{"paramName": "target_name", "values": chunk}, {"paramName": "obs_collection", "values": collections_}]}})
            rows += js.get("data", [])
            pg = js.get("paging", {})
            if page >= pg.get("pagesFiltered", 1):
                break
            page += 1
    return pd.DataFrame(rows)
hl = caom(list(ids), ["HLSP"])
two = caom(list(ids), ["TESS"])
say("MAST CAOM rows: HLSP %d; TESS collection %d" % (len(hl), len(two)))
hl["tic"] = hl["target_name"].astype(int)
hl["sector"] = hl["sequence_number"].astype(int)
def is_lc(row):
    o = str(row["obs_id"]).lower()
    p = row["provenance_name"]
    if p == "QLP": return o.endswith("_llc")
    if p == "TESS-SPOC": return o.endswith("_lc") or o.endswith("_tp")
    if p == "TGLC": return o.endswith("_llc") or "llc" in o
    if p == "GSFC-ELEANOR-LITE": return o.endswith("_lc")
    return True
hl = hl[hl.apply(is_lc, axis=1)]
# SPOC FFI: CAOM lists the observation by its target pixel file; check the sibling light-curve file in the products table (listing only, nothing downloaded)
spoc = hl[hl["provenance_name"] == "TESS-SPOC"].copy()
lc_ok = set()
oids = [str(int(x)) for x in spoc["obsid"].unique()]
for i in range(0, len(oids), 80):
    js = invoke({"service": "Mast.Caom.Products", "format": "json", "pagesize": 20000, "page": 1, "params": {"obsid": ",".join(oids[i:i + 80])}})
    for d in js.get("data", []):
        fn = str(d.get("productFilename", "")).lower()
        if fn.endswith("_lc.fits"):
            lc_ok.add(str(d.get("parent_obsid", d.get("obsID", ""))))
spoc["lc_ok"] = spoc["obsid"].astype(str).isin(lc_ok)
say("TESS-SPOC FFI observations in the sample (target-pixel-file entries): %d; with a listed light-curve file: %d (%.1f%%)" % (len(spoc), int(spoc["lc_ok"].sum()), 100 * spoc["lc_ok"].mean() if len(spoc) else 0))
bad = set(spoc.loc[~spoc["lc_ok"], "obsid"].astype(str))
hl = hl[~((hl["provenance_name"] == "TESS-SPOC") & hl["obsid"].astype(str).isin(bad))]
# per product, sets of sectors per star
prods = ["QLP", "TESS-SPOC", "TGLC", "GSFC-ELEANOR-LITE", "TASOC", "CDIPS", "T16", "TARS"]
sec = {p: collections.defaultdict(set) for p in prods}
for _, r in hl.iterrows():
    if r["provenance_name"] in sec:
        sec[r["provenance_name"]][int(r["tic"])].add(int(r["sector"]))
for p in prods:
    s["n_" + p] = [len(sec[p][t]) for t in s["tic"]]
    s["n_" + p + "_obs"] = [len(sec[p][t] & obs[t]) for t in s["tic"]]
sp2 = two[(two.get("provenance_name") == "SPOC")] if len(two) else two
n2 = collections.Counter()
if len(sp2):
    for _, r in sp2.iterrows():
        n2[int(r["target_name"])] += 1
s["n_2min"] = [n2[t] for t in s["tic"]]

# ---- metrics
read = ["QLP", "TESS-SPOC"]
S = s.copy()
S["ffi_sectors"] = [len(sec["QLP"][t] | sec["TESS-SPOC"][t]) for t in S["tic"]]
S["both_sectors"] = [len(sec["QLP"][t] & sec["TESS-SPOC"][t]) for t in S["tic"]]
def pct(a, n): return "%d of %d (%.1f%%)" % (a, n, 100 * a / max(n, 1))
sets = {"all 400": S, "Tmag <= 13.5": S[S["tmag"] <= 13.5], "Tmag > 13.5": S[S["tmag"] > 13.5]}
say("")
say("== U1: loader-readable FFI light curve (QLP or TESS-SPOC FFI) in at least 2 sectors ==")
for k, X in sets.items():
    say("  %-14s U1 %s; at least 1 sector: %s; NOTHING in any sector: %s" % (k, pct(int((X["ffi_sectors"] >= 2).sum()), len(X)), pct(int((X["ffi_sectors"] >= 1).sum()), len(X)), pct(int((X["ffi_sectors"] == 0).sum()), len(X))))
say("== by product: stars with the product in >=1 / >=2 sectors ==")
for p in prods:
    say("  %-18s >=1 sector: %s; >=2 sectors: %s; median sectors per star (stars with any) %s" % (p, pct(int((S["n_" + p] >= 1).sum()), len(S)), pct(int((S["n_" + p] >= 2).sum()), len(S)),
        (str(int(S.loc[S["n_" + p] >= 1, "n_" + p].median())) if (S["n_" + p] >= 1).any() else "-")))
say("  mission 2-minute SPOC light curves on MAST for any sample star (should be 0): %d stars" % int((S["n_2min"] > 0).sum()))
say("")
say("== U6: star-sectors with BOTH QLP and TESS-SPOC FFI light curves vs only one ==")
tot_union = int(S["ffi_sectors"].sum()); tot_both = int(S["both_sectors"].sum())
q_only = sum(len(sec["QLP"][t] - sec["TESS-SPOC"][t]) for t in S["tic"]); sp_only = sum(len(sec["TESS-SPOC"][t] - sec["QLP"][t]) for t in S["tic"])
say("  star-sectors with at least one of the two: %d; both: %s; QLP only: %d; SPOC only: %d" % (tot_union, pct(tot_both, tot_union), q_only, sp_only))
say("  stars with at least 2 sectors where BOTH exist: %s; stars with at least 1: %s" % (pct(int((S["both_sectors"] >= 2).sum()), len(S)), pct(int((S["both_sectors"] >= 1).sum()), len(S))))
say("")
say("== coverage of the sectors TESS pointed at (sectors <= %d) ==" % LAST_DONE)
obs_tot = int(S["n_obs_sectors"].sum())
for p in read:
    have = int(S["n_" + p + "_obs"].sum())
    say("  star-sectors on silicon: %d; with %s light curve: %s" % (obs_tot, p, pct(have, obs_tot)))
anyff = sum(len((sec["QLP"][t] | sec["TESS-SPOC"][t]) & obs[t]) for t in S["tic"])
say("  with QLP or TESS-SPOC: %s" % pct(anyff, obs_tot))
# by era
def era(sct): return "S1-26 (30 min)" if sct <= 26 else ("S27-55 (10 min)" if sct <= 55 else "S56+ (200 s)")
for e in ("S1-26 (30 min)", "S27-55 (10 min)", "S56+ (200 s)"):
    o_e = sum(1 for t in S["tic"] for x in obs[t] if era(x) == e)
    q_e = sum(1 for t in S["tic"] for x in (sec["QLP"][t] & obs[t]) if era(x) == e)
    s_e = sum(1 for t in S["tic"] for x in (sec["TESS-SPOC"][t] & obs[t]) if era(x) == e)
    b_e = sum(1 for t in S["tic"] for x in ((sec["QLP"][t] & sec["TESS-SPOC"][t]) & obs[t]) if era(x) == e)
    say("  %-16s star-sectors on silicon %d; QLP %s; SPOC %s; both %s" % (e, o_e, pct(q_e, o_e), pct(s_e, o_e), pct(b_e, o_e)))
say("")
say("== U1 by stratum (all 400) ==")
S["gb"] = pd.cut(S["G"], [8, 10, 11, 12, 13, 14], right=False).astype(str)
for g, X in S.groupby("gb"):
    say("  G %-10s n=%3d U1 %s; nothing %s" % (g, len(X), pct(int((X["ffi_sectors"] >= 2).sum()), len(X)), pct(int((X["ffi_sectors"] == 0).sum()), len(X))))
for pc, lab in ((0, "P 5-10 d"), (1, "P 10-30 d"), (2, "P >30 d")):
    X = S[S["pcls"] == pc]
    say("  %-10s n=%3d U1 %s; nothing %s" % (lab, len(X), pct(int((X["ffi_sectors"] >= 2).sum()), len(X)), pct(int((X["ffi_sectors"] == 0).sum()), len(X))))
lg = pd.to_numeric(S["logg"], errors="coerce")
for lab, X in (("TIC log g < 3.5 (giants)", S[lg < 3.5]), ("TIC log g >= 3.5", S[lg >= 3.5]), ("no TIC log g", S[lg.isna()])):
    if len(X):
        say("  %-26s n=%3d U1 %s; SPOC FFI in >=1 sector %s; QLP in >=1 %s" % (lab, len(X), pct(int((X["ffi_sectors"] >= 2).sum()), len(X)), pct(int((X["n_TESS-SPOC"] >= 1).sum()), len(X)), pct(int((X["n_QLP"] >= 1).sum()), len(X))))
for mt, X in S.groupby(S["model_type"] == "TWOGAUSSIANS"):
    say("  %-26s n=%3d U1 %s" % ("TWOGAUSSIANS" if mt else "other model types", len(X), pct(int((X["ffi_sectors"] >= 2).sum()), len(X))))
# Gaia ephemeris quality for the chosen epoch is stage D; here only the number of sectors per star
say("")
say("== sectors per star with a loader-readable FFI light curve: distribution ==")
say("  " + ", ".join("%s: %d" % (k, v) for k, v in sorted(collections.Counter(np.minimum(S["ffi_sectors"], 12)).items())) + "  (12 means 12 or more)")
say("  median %d; mean %.1f" % (S["ffi_sectors"].median(), S["ffi_sectors"].mean()))
# positive control: TOI-1338 (TIC 260128333)
pc_tic = 260128333
pc_hl = caom([pc_tic], ["HLSP"]); pc_two = caom([pc_tic], ["TESS"])
pc_hl["sector"] = pc_hl["sequence_number"].astype(int)
qs = set(pc_hl[(pc_hl.provenance_name == "QLP") & pc_hl.obs_id.str.endswith("_llc")]["sector"])
ss = set(pc_hl[(pc_hl.provenance_name == "TESS-SPOC") & (pc_hl.obs_id.str.endswith("_tp") | pc_hl.obs_id.str.endswith("_lc"))]["sector"])
twos = set()
if len(pc_two):
    t2 = pc_two[pc_two.provenance_name == "SPOC"]
    twos = set(t2["sequence_number"].astype(int))
say("")
say("== positive control TOI-1338 (TIC %d, a public planet host) ==" % pc_tic)
say("  QLP sectors: %s" % sorted(qs)); say("  TESS-SPOC FFI sectors: %s" % sorted(ss)); say("  mission 2-minute sectors: %s" % sorted(twos))
say("  FFI-only sectors (QLP or SPOC FFI present, no 2-minute): %s" % sorted((qs | ss) - twos))
S.drop(columns=["gb"]).to_csv(os.path.join(D, "existence_per_star.csv"), index=False)
hl.to_csv(os.path.join(D, "caom_hlsp_products.csv"), index=False)
open(os.path.join(ROOT, "research", "stage3", "ffi_door", "existence-counts.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
