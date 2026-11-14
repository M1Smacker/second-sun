"""FIX 96 radius check (Claude, 15 Nov 2026). Is the depth cap only holding events because the catalogue makes the host too big?

RULE, written before any radius is fetched:
  For every background event under adopted B that has a host radius, take the MOST GENEROUS radius we can find (the smallest of:
  the TIC radius in our light-curve headers, the TIC 8.2 catalogue radius at MAST, Gaia DR3 GSP-Phot, Gaia DR3 FLAME) and recompute
  the cap. If at least 80% of the events the cap held stay held, the radius risk is small and FIX 96 goes to Fable as tested. If
  fewer stay held, the cap needs a radius floor or margin and Fable chooses it. Also count hosts whose smallest independent radius is
  under half the header radius (a factor-2 overestimate). Same counts for real and upside-down; no threshold is tuned on them.
Stars: only the design-seen hosts of Codex 014 part 3's background events (no fence A or B star; checked below and refused).
Downloads (tiny tables): MAST TIC 8.2 rows and Gaia DR3 astrophysical parameters, into data/fix96_radii_2026-11-15/.
Run: .venv/Scripts/python.exe -B research/stage3/fix96/fix96_radius_check.py"""
import csv, json, math, pathlib, sys
import pandas as pd

ROOT = pathlib.Path(r"D:\second-sun")
A = pathlib.Path(r"D:\second-sun-astra\data\astra\014")
OUT = ROOT / "data" / "fix96_radii_2026-11-15"
HERE = pathlib.Path(__file__).resolve().parent
RJ = 69911 / 695700
sys.path.insert(0, str(ROOT / "research" / "astra" / "tools"))
import fence_check as F


def cap(R):
    return 1e6 * min(1.0, (2 * RJ / R) ** 2)


bg = [r for c in ("g2", "g3") for r in json.loads((A / f"deep-{c}.json").read_text(encoding="utf-8"))["background"] if r["options"][1]]
hdr = {}
with open(ROOT / "targets" / "host_radii_g2_g3.csv", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        try:
            v = float(r["radius_rsun"])
        except ValueError:
            continue
        if v > 0 and math.isfinite(v):
            hdr[(r["set"], int(r["tic"]))] = v
tics = sorted({int(r["tic"]) for r in bg})
fa, fb, _ = F.fences()
bad = set(tics) & (fa | fb)
if bad:
    sys.exit(f"REFUSED: {len(bad)} fenced stars in the list")
print(f"{len(bg)} background events on {len(tics)} stars; fenced: 0", flush=True)

OUT.mkdir(parents=True, exist_ok=True)
tic_csv, gaia_csv = OUT / "tic82.csv", OUT / "gaia_dr3.csv"
if not tic_csv.exists():
    from astroquery.mast import Catalogs
    t = Catalogs.query_criteria(catalog="Tic", ID=tics).to_pandas()
    t[["ID", "rad", "e_rad", "logg", "Teff", "lumclass", "GAIA", "d", "Tmag"]].to_csv(tic_csv, index=False)
tic = pd.read_csv(tic_csv)
tic["ID"] = tic["ID"].astype("int64")
print(f"TIC rows {len(tic)}", flush=True)
if not gaia_csv.exists():
    from astroquery.gaia import Gaia
    ids = ",".join(str(int(x)) for x in tic["GAIA"].dropna())
    q = ("select n.dr2_source_id, n.dr3_source_id, n.angular_distance, n.magnitude_difference, ap.radius_gspphot, ap.radius_flame, "
         "ap.logg_gspphot, g.ruwe from gaiadr3.dr2_neighbourhood as n join gaiadr3.astrophysical_parameters as ap on ap.source_id = "
         f"n.dr3_source_id join gaiadr3.gaia_source as g on g.source_id = n.dr3_source_id where n.dr2_source_id in ({ids})")
    Gaia.launch_job(q).get_results().to_pandas().to_csv(gaia_csv, index=False)
gaia = pd.read_csv(gaia_csv)
gaia = gaia.assign(_k=gaia.angular_distance.fillna(99) + gaia.magnitude_difference.abs().fillna(99)).sort_values("_k")
gaia = gaia.drop_duplicates("dr2_source_id")                              # closest, most similar match per DR2 source
print(f"Gaia rows {len(gaia)}", flush=True)
g_by = gaia.set_index("dr2_source_id")
t_by = tic.set_index("ID")

rows, out = [], {"rule": "held fraction under the most generous radius must be >= 0.80", "arms": {}}
for r in bg:
    key = (r["campaign"], int(r["tic"]))
    h = hdr.get(key)
    if h is None:
        continue
    cand = {"header": h}
    if int(r["tic"]) in t_by.index:
        tr = t_by.loc[int(r["tic"])]
        if pd.notna(tr["rad"]) and tr["rad"] > 0:
            cand["tic82"] = float(tr["rad"])
        if pd.notna(tr["GAIA"]) and int(tr["GAIA"]) in g_by.index:
            gr = g_by.loc[int(tr["GAIA"])]
            for c in ("radius_gspphot", "radius_flame"):
                if pd.notna(gr[c]) and gr[c] > 0:
                    cand[c] = float(gr[c])
    Rmin = min(cand.values())
    rows.append(dict(tic=int(r["tic"]), kind=r["kind"], depth=r["depth_ppm"], held_header=r["depth_ppm"] > cap(h),
                     held_generous=r["depth_ppm"] > cap(Rmin), smallest=Rmin, n_sources=len(cand), **cand))
df = pd.DataFrame(rows)
df.to_csv(HERE / "radius_rows.csv", index=False)
for k in ("real", "flip"):
    d = df[df.kind == k]
    held = d[d.held_header]
    out["arms"][k] = {"events_with_radius": len(d), "held_header": int(held.shape[0]),
                      "still_held_generous": int(held.held_generous.sum()),
                      "kept_fraction": round(float(held.held_generous.mean()), 3) if len(held) else None,
                      "held_events_with_any_gaia_radius": int(held[["radius_gspphot", "radius_flame"]].notna().any(axis=1).sum())
                      if {"radius_gspphot", "radius_flame"} <= set(df.columns) else 0}
hosts = df.drop_duplicates("tic")
out["hosts"] = len(hosts)
out["hosts_smallest_under_half_header"] = int((hosts.smallest < hosts.header / 2).sum())
out["hosts_with_gaia_radius"] = int(hosts[[c for c in ("radius_gspphot", "radius_flame") if c in hosts]].notna().any(axis=1).sum())
kept = [v["kept_fraction"] for v in out["arms"].values() if v["kept_fraction"] is not None]
out["verdict"] = "PASS: radius risk small" if kept and min(kept) >= 0.80 else "FAIL: cap needs a radius floor or margin"
(HERE / "radius_check.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
print("sizes:", tic_csv.stat().st_size, gaia_csv.stat().st_size)
