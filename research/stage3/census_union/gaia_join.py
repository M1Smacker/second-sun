"""Census: join a Gaia eclipsing-binary table to the union (Claude, 24 Nov 2026). Built for Gaia DR4 (2 Dec 2026), tested now on DR3.

Usage: python gaia_join.py <gaia csv> <release tag> <epoch year>
  DR3 test: data/ffi_door_2026-11-08/gaia_pool_p5.csv gaia_dr3 2016.0
  DR4 (2 Dec): the vari_eclipsing_binary rows joined to gaia_source positions; CHECK the release's reference epoch on the ESA page first
  (DR3 is J2016.0; DR4's is NOT checked here).
Conventions (C1, 23 Nov 2026, CONFIRMED on DR3 only): P = 1 / frequency; primary eclipse BTJD = reference_time - 1802.5 +
derived_primary_ecl_phase x P; widths = derived duration (phase) x P, about 1.38 x Prsa's. A DR4 change of convention must be retested
with C1 before these rows are used.
Outputs (data/census_union/): <tag>_matched.csv (union star, Gaia row, period class), <tag>_summary.json.
WHO not WHEN: a Gaia period is recorded, never adopted over a TESS one (C1-C2 result).
"""
import json, pathlib, sys
import numpy as np
import pandas as pd
from astropy.io import ascii
from scipy.spatial import cKDTree

D = pathlib.Path(r"D:\second-sun\data")
OUT = D / "census_union"


def xyz(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]


def union_positions():
    p = pd.read_csv(D / "xmatch/ebs.csv")[["TIC", "RAJ2000", "DEJ2000"]].set_axis(["tic", "ra", "dec"], axis=1)
    t3 = ascii.read(D / "g3/catalog_ttc/table3_new_ebs.txt", format="mrt").to_pandas()[["TIC", "RAdeg", "DEdeg"]].set_axis(["tic", "ra", "dec"], axis=1)
    t4 = ascii.read(D / "g3/catalog_ttc/table4_known_ebs.txt", format="mrt").to_pandas()[["TIC", "RAdeg", "DEdeg"]].set_axis(["tic", "ra", "dec"], axis=1)
    c = ascii.read(D / "calnet_2026-11-07/newecl.dat", format="fixed_width_two_line").to_pandas()[["TIC", "RAJ2000", "DEJ2000"]].set_axis(["tic", "ra", "dec"], axis=1)
    pos = pd.concat([t3, t4, p, c]).dropna()
    pos["tic"] = pos.tic.astype("int64")
    return pos.drop_duplicates("tic")


def main(path, tag, epoch):
    g = pd.read_csv(path, dtype={"source_id": str})
    dt = 2000.0 - epoch
    g["ra0"] = g.ra + np.nan_to_num(g.pmra) * dt / 3.6e6 / np.cos(np.radians(g.dec))
    g["dec0"] = g.dec + np.nan_to_num(g.pmdec) * dt / 3.6e6
    g["P"] = 1 / g.frequency
    g["t0_btjd"] = g.reference_time - 1802.5 + g.derived_primary_ecl_phase * g.P
    g["w_prim_d"] = g.derived_primary_ecl_duration * g.P
    g["phase_sec"] = (g.derived_secondary_ecl_phase - g.derived_primary_ecl_phase) % 1

    pos = union_positions()
    u = pd.read_csv(OUT / "eb_union.csv").merge(pos, on="tic", how="left")
    has = u.ra.notna()
    d, i = cKDTree(xyz(g.ra0, g.dec0)).query(xyz(u.ra[has], u.dec[has]), distance_upper_bound=np.radians(3 / 3600))
    ok = np.isfinite(d)
    m = u[has][ok].reset_index(drop=True)
    gi = g.iloc[i[ok]].reset_index(drop=True)
    r = gi.P / m.p_bin_d
    m["gaia_source_id"] = gi.source_id
    m["gaia_P"] = gi.P
    m["gaia_t0_btjd"] = gi.t0_btjd
    m["gaia_w_prim_d"] = gi.w_prim_d
    m["gaia_G"] = gi.phot_g_mean_mag
    m["period_class"] = np.select([m.p_bin_d.isna(), abs(r - 1) < 0.002, abs(r - 2) < 0.004, abs(r - 0.5) < 0.001],
                                  ["gaia_only", "same", "double", "half"], "other")
    m.to_csv(OUT / f"{tag}_matched.csv", index=False)

    matched_ids = set(gi.source_id)
    rest = g[~g.source_id.isin(matched_ids)]
    s = dict(gaia_rows=len(g), union_stars_with_position=int(has.sum()), matched=int(ok.sum()),
             period_class=m.period_class.value_counts().to_dict(),
             union_no_period_given_gaia_period=int((m.period_class == "gaia_only").sum()),
             gaia_not_in_union=len(rest), gaia_not_in_union_P5_G13_5=int(((rest.P > 5) & (rest.phot_g_mean_mag <= 13.5)).sum()),
             gaia_not_in_union_P10_G13_5=int(((rest.P > 10) & (rest.phot_g_mean_mag <= 13.5)).sum()))
    print(json.dumps(s, indent=1))
    json.dump(s, open(OUT / f"{tag}_summary.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
