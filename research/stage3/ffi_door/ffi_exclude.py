"""FFI door stage B, step 2: apply the preregistered position/Gaia-id exclusions to the frame and print COUNTS ONLY.

Frame (preregistration, FFI-DOOR-TEST-PLAN-2026-11-08.md): P > 5 d, 8 <= G < 14 (Gaia DR3 vari_eclipsing_binary joined to gaia_source).
Exclusions applied here (by position and Gaia id; lists that carry only TIC ids, namely G1/G2/G3, are applied after the TIC lookup in draw_sample.py):
  (a) 2-minute targets of sectors 1..111 (data\\census_targets_2m, TIC J2000 coordinates)
  (b) Prsa 2022 (data\\xmatch\\ebs.csv), TTC tables 3 and 4 (data\\g3\\catalog_ttc), CALNet newecl.dat (Gaia id and position)
Match: Gaia position moved from 2016.0 to J2000 with pmra, pmdec; 3 arcsec; magnitude sanity -0.3 <= G - Tmag <= 1.8 where the list has Tmag, else the match must be within 1 arcsec.
Output (git-ignored): data\\ffi_door_2026-11-08\\pool_survivors.csv ; counts: research/stage3/ffi_door/exclusion-counts.txt
"""
import glob, os, re
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

D = r"D:\second-sun\data\ffi_door_2026-11-08"
ROOT = r"D:\second-sun"
pool = pd.read_csv(os.path.join(D, "gaia_pool_p5.csv"))
G = pool["phot_g_mean_mag"]
fr = pool[(pool["P"] > 5) & (G >= 8) & (G < 14)].copy().reset_index(drop=True)

# Gaia position at J2000 (move back 16 years); pm in mas/yr, pmra already includes cos(dec)
dec = fr["dec"].values
cosd = np.cos(np.radians(dec))
dra = np.where(fr["pmra"].notna(), -fr["pmra"].fillna(0).values * 16.0 / (3.6e6 * cosd), 0.0)
ddec = np.where(fr["pmdec"].notna(), -fr["pmdec"].fillna(0).values * 16.0 / 3.6e6, 0.0)
fr["ra0"] = fr["ra"].values + dra
fr["dec0"] = fr["dec"].values + ddec

def xyz(ra, de):
    r, d = np.radians(ra), np.radians(de)
    return np.column_stack([np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)])

ASEC = np.radians(1.0 / 3600.0)
pool_xyz = xyz(fr["ra0"].values, fr["dec0"].values)
Gv = fr["phot_g_mean_mag"].values

def match(ref_ra, ref_de, ref_tmag):
    """boolean array over fr: matched to any reference object under the rule."""
    tree = cKDTree(xyz(ref_ra, ref_de))
    hit = np.zeros(len(fr), bool)
    cand = tree.query_ball_point(pool_xyz, r=3 * ASEC)
    for i, c in enumerate(cand):
        if not c:
            continue
        for j in c:
            sep = np.linalg.norm(pool_xyz[i] - tree.data[j]) / ASEC
            if ref_tmag is None or not np.isfinite(ref_tmag[j]):
                if sep <= 1.0:
                    hit[i] = True; break
            else:
                d = Gv[i] - ref_tmag[j]
                if -0.3 <= d <= 1.8:
                    hit[i] = True; break
                if sep <= 1.0:
                    hit[i] = True; break
    return hit

out = []
def say(s=""):
    print(s); out.append(s)

say("FFI door stage B exclusions (COUNTS ONLY). Frame: P>5 d and 8<=G<14: %d stars" % len(fr))

# (a) 2-minute lists
frames = []
for fn in sorted(glob.glob(os.path.join(ROOT, "data", "census_targets_2m", "all_targets_S*_v1.csv"))):
    sec = int(re.search(r"S(\d+)", os.path.basename(fn)).group(1))
    t = pd.read_csv(fn, comment="#")
    t["sector"] = sec
    frames.append(t[["TICID", "Tmag", "RA", "Dec", "sector"]])
tm = pd.concat(frames, ignore_index=True)
nlists = len(frames)
tm1 = tm.sort_values("sector").drop_duplicates("TICID")
say("2-minute lists read: %d files, %d rows, %d unique TIC ids" % (nlists, len(tm), len(tm1)))
h_2m = match(tm1["RA"].values, tm1["Dec"].values, tm1["Tmag"].values)
say("  frame stars matched to a 2-minute target of sectors 1..111: %d" % h_2m.sum())
# the 2-minute exclusion by sector range, for the record (S1-26 lists vs later)
h_2m_early = match(tm1[tm1["sector"] <= 26]["RA"].values, tm1[tm1["sector"] <= 26]["Dec"].values, tm1[tm1["sector"] <= 26]["Tmag"].values)
say("    of which already matched in sectors 1..26 lists (first-seen sector <= 26): %d" % h_2m_early.sum())

# (b1) Prsa 2022
pr = pd.read_csv(os.path.join(ROOT, "data", "xmatch", "ebs.csv"))
h_pr = match(pr["RAJ2000"].values, pr["DEJ2000"].values, pr["Tmag"].values)
say("Prsa 2022 (%d rows): frame stars matched: %d" % (len(pr), h_pr.sum()))

# (b2) TTC tables
def read_ttc(fn, with_tmag):
    rows = []
    for ln in open(fn, encoding="utf-8", errors="replace"):
        m = re.match(r"^\s*(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)?", ln)
        if m and len(ln) > 40 and ln[11:12] != "-":
            tm_ = float(ln[37:43]) if with_tmag and ln[37:43].strip() else np.nan
            rows.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), tm_))
    return pd.DataFrame(rows, columns=["tic", "ra", "dec", "tmag"])
t3 = read_ttc(os.path.join(ROOT, "data", "g3", "catalog_ttc", "table3_new_ebs.txt"), True)
t4 = read_ttc(os.path.join(ROOT, "data", "g3", "catalog_ttc", "table4_known_ebs.txt"), False)
ttc = pd.concat([t3, t4], ignore_index=True).drop_duplicates("tic")
say("TTC tables parsed: table3 %d rows, table4 %d rows, %d unique TIC (expected about 10,001 in total)" % (len(t3), len(t4), len(ttc)))
h_ttc = match(ttc["ra"].values, ttc["dec"].values, ttc["tmag"].values)
say("  frame stars matched to TTC: %d" % h_ttc.sum())

# (b3) CALNet by Gaia id and by position
lines = open(os.path.join(ROOT, "data", "calnet_2026-11-07", "newecl.dat"), encoding="utf-8", errors="replace").read().splitlines()
hdr, dash = lines[0], lines[1]
spans = [(m.start(), m.end()) for m in re.finditer(r"-+", dash)]
names = [hdr[a:b].strip() for a, b in spans]
cal = pd.DataFrame([{n: l[a:b].strip() for n, (a, b) in zip(names, spans)} for l in lines[2:] if l.strip()])
cal["ra"] = cal["RAJ2000"].astype(float); cal["dec"] = cal["DEJ2000"].astype(float)
cal["gmag"] = pd.to_numeric(cal["Gmag"], errors="coerce")
cg = set(cal.loc[cal["Gaia"].isin(["", "0"]) == False, "Gaia"].astype(str))
h_calid = fr["source_id"].astype(str).isin(cg).values
h_calpos = match(cal["ra"].values, cal["dec"].values, None)
say("CALNet (%d rows): frame stars matched by Gaia id: %d; by position: %d; either: %d" % (len(cal), h_calid.sum(), h_calpos.sum(), (h_calid | h_calpos).sum()))
h_cal = h_calid | h_calpos

excl = h_2m | h_pr | h_ttc | h_cal
say("")
say("== union ==")
say("excluded by any of the lists above: %d of %d (%.1f%%)" % (excl.sum(), len(fr), 100 * excl.mean()))
say("  only 2-minute: %d; only Prsa: %d; only TTC: %d; only CALNet: %d" % (
    (h_2m & ~h_pr & ~h_ttc & ~h_cal).sum(), (h_pr & ~h_2m & ~h_ttc & ~h_cal).sum(), (h_ttc & ~h_2m & ~h_pr & ~h_cal).sum(), (h_cal & ~h_2m & ~h_pr & ~h_ttc).sum()))
say("survivors (frame minus position/Gaia-id exclusions): %d" % (~excl).sum())
fr["ex_2m"] = h_2m; fr["ex_prsa"] = h_pr; fr["ex_ttc"] = h_ttc; fr["ex_calnet"] = h_cal
fr["excluded"] = excl
fr.to_csv(os.path.join(D, "pool_frame_flags.csv"), index=False)
s = fr[~fr["excluded"]]
s.to_csv(os.path.join(D, "pool_survivors.csv"), index=False)
say("")
say("== survivors per sample cell (G bin x period class) ==")
gb = pd.cut(s["phot_g_mean_mag"], [8, 10, 11, 12, 13, 14], right=False)
pc = pd.cut(s["P"], [5, 10, 30, 1e9], right=True)
say(pd.crosstab(gb, pc).to_string())
say("survivors: TWOGAUSSIANS %d of %d" % ((s["model_type"] == "TWOGAUSSIANS").sum(), len(s)))
say("G<13 survivors: %d; G<13.5: %d; P>7 d: %d (all within the frame 8<=G<14)" % ((s["phot_g_mean_mag"] < 13).sum(), (s["phot_g_mean_mag"] < 13.5).sum(), (s["P"] > 7).sum()))
open(os.path.join(ROOT, "research", "stage3", "ffi_door", "exclusion-counts.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
