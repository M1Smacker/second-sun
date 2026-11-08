"""FFI door stage B, step 3: the preregistered seeded draw of 400 stars (rule in FFI-DOOR-TEST-PLAN-2026-11-08.md, written and committed before this script ran).

Rule (summary; the plan file is the authority):
  cells = Gaia G bin (8-10, 10-11, 11-12, 12-13, 13-14) x Gaia period class (5-10, 10-30, >30 d); quota 80 per G bin = 27, 27, 26.
  shortfall of a cell: other period classes of the same G bin (lower period class first), then the next fainter G bin.
  within a cell: survivors sorted by source_id ascending; order = numpy.random.default_rng(20261108 + cell_index).permutation,
  cell_index = 3 * g_bin_index + period_class_index; first quota = sample, rest = ordered reserve.
  TIC id from the MAST TIC (v8.2) by position (J2000 epoch, 3 arcsec, sanity -0.3 <= G - Tmag <= 1.8; prefer GAIA id equal to the DR3 source_id, else brightest passing).
  A candidate is skipped (replaced by the next in its cell order) when it has no TIC match, or its TIC id is in a 2-minute list (sectors 1-111), G1/G2/G3 targets, Prsa 2022, TTC or CALNet.
Output (star ids ONLY under data\\ffi_door_2026-11-08, git-ignored): sample_400.csv, sample_400.sha256 ; counts: research/stage3/ffi_door/draw-counts.txt
"""
import glob, hashlib, json, os, re, sys, time, urllib.parse, urllib.request
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

ROOT = r"D:\second-sun"
D = os.path.join(ROOT, "data", "ffi_door_2026-11-08")
SEED = 20261108
GBINS = [8, 10, 11, 12, 13, 14]
PCLASS = [5, 10, 30, 1e9]
QUOTA = [27, 27, 26]

s = pd.read_csv(os.path.join(D, "pool_survivors.csv"))
s["gbin"] = pd.cut(s["phot_g_mean_mag"], GBINS, right=False, labels=False)
s["pcls"] = pd.cut(s["P"], PCLASS, right=True, labels=False)
s = s.dropna(subset=["gbin", "pcls"]).copy()
s["gbin"] = s["gbin"].astype(int); s["pcls"] = s["pcls"].astype(int)

out = []
def say(x=""):
    print(x); out.append(x)

# ---------- quota plan with shortfall rule ----------
avail = np.zeros((5, 3), int)
for (g, p), grp in s.groupby(["gbin", "pcls"]):
    avail[g, p] = len(grp)
plan = np.zeros((5, 3), int)
carry = 0
for g in range(5):
    want = np.array(QUOTA) + 0
    got = np.minimum(want, avail[g])
    short = int(want.sum() - got.sum()) + carry
    # other period classes of the same bin absorb first, lower period class first
    for p in range(3):
        room = int(avail[g, p] - got[p])
        take = min(room, short)
        got[p] += take; short -= take
    plan[g] = got
    carry = short          # to the next fainter G bin (added to its wanted total through `short`)
    # the carried shortfall is absorbed in the next bin by the same loop above (it starts from `carry`)
say("FFI door draw: quota plan per cell (rows G bins 8-10,10-11,11-12,12-13,13-14; columns P 5-10,10-30,>30 d)")
say(str(plan))
say("availability (survivors) per cell:")
say(str(avail))
say("planned total %d; unplaced shortfall %d" % (plan.sum(), 400 - plan.sum()))

# ---------- exclusion sets by TIC id ----------
excl_tic = set()
src_counts = {}
frames = []
for fn in sorted(glob.glob(os.path.join(ROOT, "data", "census_targets_2m", "all_targets_S*_v1.csv"))):
    frames.append(pd.read_csv(fn, comment="#", usecols=["TICID"]))
t2m = set(pd.concat(frames)["TICID"].astype(int)); src_counts["2min"] = len(t2m)
g1 = set(pd.read_csv(os.path.join(ROOT, "targets", "g1_targets.csv"), comment="#")["tic"].astype(int))
g2 = set(pd.read_csv(os.path.join(ROOT, "targets", "g2_targets.csv"), comment="#")["tic"].astype(int))
g3 = set(pd.read_csv(os.path.join(ROOT, "targets", "g3_targets.csv"), comment="#")["tic"].astype(int))
pr = set(pd.read_csv(os.path.join(ROOT, "data", "xmatch", "ebs.csv"))["TIC"].astype(int))
ttc = set()
for fn in ("table3_new_ebs.txt", "table4_known_ebs.txt"):
    for ln in open(os.path.join(ROOT, "data", "g3", "catalog_ttc", fn), encoding="utf-8", errors="replace"):
        m = re.match(r"^\s*(\d{3,10})\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
        if m and len(ln) > 40:
            ttc.add(int(m.group(1)))
lines = open(os.path.join(ROOT, "data", "calnet_2026-11-07", "newecl.dat"), encoding="utf-8", errors="replace").read().splitlines()
spans = [(m.start(), m.end()) for m in re.finditer(r"-+", lines[1])]
names = [lines[0][a:b].strip() for a, b in spans]
cal = set(int(l[spans[names.index("TIC")][0]:spans[names.index("TIC")][1]]) for l in lines[2:] if l.strip())
lists = {"2min_S1-111": t2m, "G1": g1, "G2": g2, "G3": g3, "Prsa2022": pr, "TTC": ttc, "CALNet": cal}
for k, v in lists.items():
    excl_tic |= v
say("TIC-id exclusion lists: " + ", ".join("%s %d" % (k, len(v)) for k, v in lists.items()) + "; union %d" % len(excl_tic))

# ---------- MAST TIC lookup ----------
API = "https://mast.stsci.edu/api/v0/invoke"
def tic_lookup(row):
    ra0, de0 = row["ra0"], row["dec0"]
    req = {"service": "Mast.Catalogs.Tic.Cone", "params": {"ra": float(ra0), "dec": float(de0), "radius": 3.0 / 3600.0},
           "format": "json", "pagesize": 50, "page": 1}
    body = urllib.parse.urlencode({"request": json.dumps(req)}).encode()
    for attempt in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request(API, data=body, headers={"User-Agent": "SecondSunResearch/1.0"}), timeout=60)
            js = json.loads(r.read().decode())
            return js.get("data", [])
        except Exception as e:
            time.sleep(3 * (attempt + 1))
    return None

def pick(row, cands):
    best = None
    for c in cands or []:
        tmag = c.get("Tmag")
        if tmag is None:
            continue
        d = row["phot_g_mean_mag"] - tmag
        if not (-0.3 <= d <= 1.8):
            continue
        if str(c.get("GAIA")) == str(int(row["source_id"])):
            return c
        if best is None or tmag < best["Tmag"]:
            best = c
    return best

# ---------- draw ----------
sample = []
reserve_used = 0
rejected = {"no_tic": 0, "excluded_tic": 0}
cell_idx_of = lambda g, p: 3 * g + p
for g in range(5):
    for p in range(3):
        q = int(plan[g, p])
        grp = s[(s["gbin"] == g) & (s["pcls"] == p)].sort_values("source_id").reset_index(drop=True)
        if len(grp) == 0 or q == 0:
            continue
        perm = np.random.default_rng(SEED + cell_idx_of(g, p)).permutation(len(grp))
        taken = 0
        pos = 0
        while taken < q and pos < len(grp):
            batch = perm[pos: pos + max(q - taken, 1) + 3]
            pos += len(batch)
            rows = [grp.iloc[i] for i in batch]
            with ThreadPoolExecutor(max_workers=4) as ex:
                res = list(ex.map(tic_lookup, rows))
            for row, cands in zip(rows, res):
                if taken >= q:
                    break
                c = pick(row, cands)
                if c is None:
                    rejected["no_tic"] += 1; continue
                tic = int(c["ID"])
                if tic in excl_tic:
                    rejected["excluded_tic"] += 1; continue
                sample.append({"source_id": int(row["source_id"]), "tic": tic, "tmag": c.get("Tmag"), "G": row["phot_g_mean_mag"],
                               "bp_rp": row["bp_rp"], "P_gaia": row["P"], "model_type": row["model_type"], "gbin": g, "pcls": p,
                               "order": int(pos), "ra": row["ra"], "dec": row["dec"], "ra0": row["ra0"], "dec0": row["dec0"],
                               "contratio": c.get("contratio"), "logg": c.get("logg"), "teff": c.get("Teff"), "gaia_dr2_in_tic": c.get("GAIA"),
                               "frequency": row["frequency"], "frequency_error": row["frequency_error"], "reference_time": row["reference_time"],
                               "primary_phase": row["derived_primary_ecl_phase"], "primary_phase_error": row["derived_primary_ecl_phase_error"],
                               "primary_depth": row["derived_primary_ecl_depth"], "primary_duration": row["derived_primary_ecl_duration"],
                               "secondary_phase": row["derived_secondary_ecl_phase"], "secondary_depth": row["derived_secondary_ecl_depth"],
                               "global_ranking": row["global_ranking"], "ruwe": row["ruwe"], "non_single_star": row["non_single_star"]})
                taken += 1
        say("cell G-bin %d period-class %d: quota %d taken %d (looked at %d of %d)" % (g, p, q, taken, pos, len(grp)))
        if taken < q:
            say("   WARNING cell short by %d" % (q - taken))
df = pd.DataFrame(sample)
fn = os.path.join(D, "sample_400.csv")
df.to_csv(fn, index=False)
h = hashlib.sha256(open(fn, "rb").read()).hexdigest()
open(os.path.join(D, "sample_400.sha256"), "w").write(h + "  sample_400.csv\n")
say("")
say("sample size %d; rejected during draw: %s; duplicates of TIC in sample: %d" % (len(df), rejected, len(df) - df["tic"].nunique()))
say("sha256 of sample_400.csv: " + h)
say("seed %d" % SEED)
if len(df):
    say("Tmag: min %.2f median %.2f max %.2f; share with Tmag > 13.5: %.1f%% (%d)" % (df["tmag"].min(), df["tmag"].median(), df["tmag"].max(), 100 * (df["tmag"] > 13.5).mean(), int((df["tmag"] > 13.5).sum())))
    say("TWOGAUSSIANS %d; others %d" % ((df["model_type"] == "TWOGAUSSIANS").sum(), (df["model_type"] != "TWOGAUSSIANS").sum()))
    say("P (Gaia, d): 5-10 %d, 10-30 %d, >30 %d; log g < 3.5 (TIC): %d of %d with logg" % ((df["pcls"] == 0).sum(), (df["pcls"] == 1).sum(), (df["pcls"] == 2).sum(), int((pd.to_numeric(df["logg"], errors="coerce") < 3.5).sum()), int(pd.to_numeric(df["logg"], errors="coerce").notna().sum())))
open(os.path.join(ROOT, "research", "stage3", "ffi_door", "draw-counts.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
