"""Wave 3 / G1 feasibility: how bright are the Kepler eclipsing binaries in TESS, and how small a
circumbinary planet could one TESS transit reveal at each brightness?

1. Read the Villanova Kepler EB catalogue (wave 1c download).
2. Cross-match KIC -> TIC (Tmag) via MAST Catalogs (TIC has a KIC column).
3. Summarise the Tmag distribution (all EBs, and the detached P_bin > 5 d subset that matters for CBPs).
4. For ~6 detached EBs spanning the Tmag range, download ONE FFI light curve (QLP / TESS-SPOC / TGLC),
   mask eclipses from the Kepler ephemeris, and measure 1-hr CDPP.
5. Convert to the smallest planet detectable from a single 6-hour transit at SNR 7 (our rule C1).

Outputs: g1_tmag.csv, g1_noise.csv, printed summary. Every download is appended to research/downloads.csv.
"""
import csv, datetime, math, pathlib, time
import numpy as np
import lightkurve as lk
from astroquery.mast import Catalogs

ROOT = pathlib.Path(r"D:\second-sun")
W = ROOT / "research" / "wave-3-pipeline"
CAT = ROOT / "data" / "wave-1" / "villanova_kepler-ebs_live" / "keplerebs_live.csv"
DL = ROOT / "data" / "wave-3" / "lk"

# --- 1. catalogue -------------------------------------------------------------
rows = []
with open(CAT) as f:
    lines = [l for l in f if not l.startswith("##")]
for r in csv.DictReader([lines[0].lstrip("#")] + lines[1:]):
    try:
        rows.append(dict(kic=int(r["KIC"]), p=float(r["period"]), t0=float(r["bjd0"]), morph=float(r["morph"]), kmag=float(r["kmag"])))
    except (ValueError, KeyError):
        pass
print(f"catalogue rows: {len(rows)}")

# --- 2. KIC -> TIC ------------------------------------------------------------
tic = {}
kics = [r["kic"] for r in rows]
for i in range(0, len(kics), 400):
    chunk = kics[i:i + 400]
    for attempt in range(3):
        try:
            t = Catalogs.query_criteria(catalog="Tic", KIC=[str(k) for k in chunk])
            for row in t:
                if row["KIC"] and str(row["KIC"]).strip() not in ("", "--"):
                    tic[int(row["KIC"])] = (int(row["ID"]), float(row["Tmag"]), float(row["rad"]) if row["rad"] else float("nan"))
            break
        except Exception as e:
            print("retry", i, type(e).__name__, str(e)[:120]); time.sleep(5)
print(f"matched to TIC: {len(tic)} / {len(rows)}")

with open(W / "g1_tmag.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["kic", "tic", "tmag", "tic_rad", "p_bin", "morph", "kmag"])
    for r in rows:
        t = tic.get(r["kic"], (None, float("nan"), float("nan")))
        w.writerow([r["kic"], t[0], t[1], t[2], r["p"], r["morph"], r["kmag"]])

def summarise(label, sel):
    tm = np.array([tic[r["kic"]][1] for r in sel if r["kic"] in tic])
    tm = tm[np.isfinite(tm)]
    edges = [0, 10, 11, 12, 13, 13.5, 14, 15, 16, 99]
    counts = np.histogram(tm, bins=edges)[0]
    print(f"\n{label}: n={len(tm)}  median Tmag={np.median(tm):.2f}  <=13.5: {np.sum(tm <= 13.5)} ({100*np.mean(tm <= 13.5):.0f}%)")
    print("  Tmag bins:", ", ".join(f"{edges[i]}-{edges[i+1]}: {c}" for i, c in enumerate(counts)))

summarise("ALL Kepler EBs", rows)
det = [r for r in rows if r["morph"] < 0.5 and r["p"] > 5]
summarise("DETACHED (morph<0.5) & P_bin>5 d", det)

# --- 4. noise at several magnitudes -------------------------------------------
targets = []
for lo, hi in [(9.5, 10.5), (10.5, 11.5), (11.5, 12.5), (12.5, 13.5), (13.5, 14.5), (14.5, 15.5)]:
    cand = [r for r in det if r["kic"] in tic and lo <= tic[r["kic"]][1] < hi]
    if cand:
        targets.append(sorted(cand, key=lambda r: abs(tic[r["kic"]][1] - (lo + hi) / 2))[0])

noise_rows = []
for r in targets:
    ticid, tmag, rad = tic[r["kic"]]
    rec = dict(kic=r["kic"], tic=ticid, tmag=round(tmag, 2), tic_rad=rad, p_bin=r["p"], product="", sector="", cdpp_1h_ppm="", min_rp_re_sunlike="", note="")
    try:
        sr = lk.search_lightcurve(f"TIC {ticid}")
        sr = sr[[a in ("QLP", "TESS-SPOC", "TGLC", "SPOC") for a in sr.author]]
        if len(sr) == 0:
            rec["note"] = "no LC product"; noise_rows.append(rec); print(rec); continue
        pref = {"SPOC": 0, "TESS-SPOC": 1, "QLP": 2, "TGLC": 3}
        idx = sorted(range(len(sr)), key=lambda i: (pref.get(sr.author[i], 9), -int(sr.mission[i].split()[-1])))[0]
        lc = sr[idx].download(download_dir=str(DL))
        rec["product"] = sr.author[idx]; rec["sector"] = sr.mission[idx]
        lc = lc.remove_nans().normalize()
        # mask primary + secondary eclipses (Kepler BJD0 = BJD-2400000 style 54953/55000 -> BTJD = BJD-2457000)
        t0_btjd = r["t0"] + 2400000 - 2457000
        ph = ((lc.time.value - t0_btjd) / r["p"]) % 1.0
        half_w = min(0.05, 0.25 / r["p"] + 0.01)  # crude eclipse half-width in phase
        mask = (ph < half_w) | (ph > 1 - half_w) | (np.abs(ph - 0.5) < half_w)
        lc = lc[~mask]
        dt = np.nanmedian(np.diff(lc.time.value)) * 24 * 60
        flat = lc.flatten(window_length=int(round(12 * 60 / dt)) | 1).remove_outliers(sigma_lower=4, sigma_upper=4)
        cdpp = float(np.asarray(flat.estimate_cdpp(transit_duration=max(1, int(round(60 / dt)))).value))
        depth_min = 7 * cdpp / math.sqrt(6) * 1e-6             # SNR 7 for a 6-hour single transit
        rp_re = math.sqrt(depth_min) * 109.1                  # around a 1 R_sun star, in Earth radii
        rec.update(cdpp_1h_ppm=round(cdpp), min_rp_re_sunlike=round(rp_re, 1), note=f"cadence {dt:.1f} min, n={len(flat)}")
        p = pathlib.Path(lc.meta.get("FILENAME", "")) if lc.meta.get("FILENAME") else None
    except Exception as e:
        rec["note"] = f"ERROR {type(e).__name__}: {str(e)[:120]}"
    noise_rows.append(rec); print(rec)

with open(W / "g1_noise.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(noise_rows[0])); w.writeheader(); w.writerows(noise_rows)

total = sum(p.stat().st_size for p in DL.rglob("*.fits"))
with open(ROOT / "research" / "downloads.csv", "a", newline="") as f:
    csv.writer(f).writerow([datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%MZ"),
                            f"G1 noise sample: {len(noise_rows)} FFI light curves (one sector each)", "MAST via lightkurve",
                            total, "data/wave-3/lk", "G1 feasibility: noise vs Tmag", "3"])
print(f"\ndownloaded {total/1e6:.1f} MB")
