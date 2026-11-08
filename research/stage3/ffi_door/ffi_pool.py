"""FFI door stage B, step 1: merge the 768 Gaia pixel files into one pool file and print COUNTS ONLY.

Input : D:\\second-sun\\data\\ffi_door_2026-11-08\\gaia_pixels\\pix_###.csv   (Gaia DR3 vari_eclipsing_binary, frequency < 0.2, joined to gaia_source)
Output: D:\\second-sun\\data\\ffi_door_2026-11-08\\gaia_pool_p5.csv  (git-ignored; star ids stay in data\\)
        research/stage3/ffi_door/pool-counts.txt (counts only, no ids)
Run with the project interpreter:  .venv\\Scripts\\python.exe -I research\\stage3\\ffi_door\\ffi_pool.py
"""
import glob, os, sys
import numpy as np
import pandas as pd

D = r"D:\second-sun\data\ffi_door_2026-11-08"
frames = []
for fn in sorted(glob.glob(os.path.join(D, "gaia_pixels", "pix_*.csv"))):
    frames.append(pd.read_csv(fn))
pool = pd.concat(frames, ignore_index=True)
n_files = len(frames)
pool = pool.drop_duplicates("source_id").reset_index(drop=True)
pool["P"] = 1.0 / pool["frequency"]
pool["bp_rp"] = pool["phot_bp_mean_mag"] - pool["phot_rp_mean_mag"]
pool["M_G"] = pool["phot_g_mean_mag"] + 5 * np.log10(pool["parallax"].clip(lower=1e-3) / 100.0)  # only meaningful for parallax_over_error > 5
pool.to_csv(os.path.join(D, "gaia_pool_p5.csv"), index=False)

out = []
def say(s=""):
    print(s); out.append(s)

say("FFI door stage B: Gaia DR3 slow eclipsing binary pool (COUNTS ONLY). Source: gaiadr3.vari_eclipsing_binary with frequency < 0.2, joined to gaia_source, per HEALPix level-3 pixel.")
say("pixel files merged: %d of 768; rows (unique source_id): %d" % (n_files, len(pool)))
say("expected total with frequency < 0.2 (parent's count, 8 Nov 2026): 188,407")
G = pool["phot_g_mean_mag"]
say("rows with a G magnitude: %d; without: %d" % (G.notna().sum(), G.isna().sum()))
say("")
say("== exact all-sky pools (cumulative, G brighter than) ==")
say("%-8s %9s %9s %9s %9s %9s" % ("", "G<11", "G<12", "G<13", "G<13.5", "G<14"))
for lo in (5, 7, 10, 20, 30):
    row = [int(((pool["P"] > lo) & (G < g)).sum()) for g in (11, 12, 13, 13.5, 14)]
    say("P>%-5d %9d %9d %9d %9d %9d" % ((lo,) + tuple(row)))
for g in (15, 16, 17, 18):
    say("P>5 d, G<%d: %d   P>7 d: %d" % (g, int(((pool["P"] > 5) & (G < g)).sum()), int(((pool["P"] > 7) & (G < g)).sum())))
say("")
say("== model type, P>5 d and G<14 (G5 frame) ==")
fr = pool[(pool["P"] > 5) & (G < 14)]
say("total %d" % len(fr))
for k, v in fr["model_type"].value_counts().items():
    say("  %-45s %6d  (%.1f%%)" % (k, v, 100 * v / len(fr)))
say("== model type, P>7 d and G<13.5 ==")
fr2 = pool[(pool["P"] > 7) & (G < 13.5)]
say("total %d; TWOGAUSSIANS %d" % (len(fr2), int((fr2["model_type"] == "TWOGAUSSIANS").sum())))
say("")
say("== 8 <= G < 14, P>5 d: counts per sample cell (G bin x period class) ==")
fr = pool[(pool["P"] > 5) & (G >= 8) & (G < 14)]
gb = pd.cut(fr["phot_g_mean_mag"], [8, 10, 11, 12, 13, 14], right=False)
pc = pd.cut(fr["P"], [5, 10, 30, 1e9], right=True)
tab = pd.crosstab(gb, pc)
say(tab.to_string())
say("")
say("== Gaia alias peaks (Mowlavi 2023): share of P>5 d, 8<=G<14 within 1% of the period ==")
for pk in (34.1, 53.7, 107.2):
    n = int((np.abs(fr["P"] / pk - 1) < 0.01).sum())
    say("  within 1%% of %.1f d: %d of %d (%.2f%%)" % (pk, n, len(fr), 100 * n / len(fr)))
say("")
say("== period distribution of the 8<=G<14, P>5 d pool ==")
for lo, hi in ((5, 7), (7, 10), (10, 20), (20, 30), (30, 60), (60, 120), (120, 1e9)):
    say("  P %5s to %5s d: %d" % (lo, hi if hi < 1e8 else "inf", int(((fr["P"] > lo) & (fr["P"] <= hi)).sum())))
say("")
say("== red-dwarf stratum (counts only): P>5 d, 14<=G<17 ==")
rd = pool[(pool["P"] > 5) & (G >= 14) & (G < 17)]
say("14<=G<17, P>5 d: %d" % len(rd))
red = rd[rd["bp_rp"] > 2.0]
say("  BP-RP > 2.0: %d" % len(red))
poe = rd["parallax"] / rd["parallax_error"]
good = rd[(poe > 5) & (rd["parallax"] > 0)]
say("  parallax_over_error > 5: %d" % len(good))
m = good[(good["bp_rp"] > 2.0) & (good["M_G"] > 8.0)]
say("  parallax_over_error > 5 and BP-RP > 2.0 and M_G > 8 (small-radius proxy, roughly M dwarf main sequence): %d" % len(m))
say("  of which TWOGAUSSIANS: %d" % int((m["model_type"] == "TWOGAUSSIANS").sum()))
say("")
say("== U8 pool-level: Gaia ephemeris error at the TESS epoch (catalogue only) ==")
# reference_time is BJD(TCB) - 2455197.5; TESS Sector 1 start is BJD 2458325 -> reference-relative days
t_tess = np.array([2458325.0 - 2455197.5, 2460000.0 - 2455197.5, 2461000.0 - 2455197.5])
fe = pool["frequency_error"].astype(float)
ph_err = pool["derived_primary_ecl_phase_error"].astype(float)
for lab, t in (("TESS Sector 1 (2018 Jul)", t_tess[0]), ("BJD 2460000 (2023 Feb)", t_tess[1]), ("BJD 2461000 (2025 Oct)", t_tess[2])):
    dt = t - pool["reference_time"].astype(float)
    # phase drift (cycles) = frequency_error * dt ; in days = drift / frequency ; plus the phase-location error (cycles) times P
    err_d = np.sqrt((fe * dt.abs() / pool["frequency"]) ** 2 + (ph_err.fillna(0) * pool["P"]) ** 2)
    sel = (pool["P"] > 5) & (G >= 8) & (G < 14)
    e = err_d[sel]
    say("  %-26s median reference_time offset %.0f d; error median %.2f d; share <= 0.25 d: %.1f%%; <= 1 d: %.1f%%; of %d stars" % (
        lab, float(dt[sel].median()), float(e.median()), 100 * float((e <= 0.25).mean()), 100 * float((e <= 1.0).mean()), int(sel.sum())))
say("  (frequency_error median %.3g /d; share with frequency_error > 1e-4 /d: %.1f%%)" % (float(fe[sel].median()), 100 * float((fe[sel] > 1e-4).mean())))
open(r"D:\second-sun\research\stage3\ffi_door\pool-counts.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
