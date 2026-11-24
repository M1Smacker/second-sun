"""T139 Census stage 2, part 1: one row per binary from the public EB lists on disk (Claude, 24 Nov 2026).

WHO comes from the lists; WHEN (epoch, width) is kept with its source and convention, never guessed (spec note rule 3).
Sources: Prsa 2022 (data/xmatch/ebs.csv), TTC tables 3 and 4 (data/g3/catalog_ttc), CALNet (data/calnet_2026-11-07,
TIC only, Gaia DR3 period for 1,596). Output: data/census_union/eb_union.csv and sources.csv (data/ is git-ignored).
Gaia DR4 (2 Dec 2026) joins later through the same function with source='gaia_dr4'.
"""
import json
import pathlib
import numpy as np
import pandas as pd
from astropy.io import ascii

D = pathlib.Path(r"D:\second-sun\data")
OUT = D / "census_union"
OUT.mkdir(exist_ok=True)
COLS = ["tic", "source", "p_bin_d", "p_err_d", "t0_btjd", "t0_err_d", "w_prim_d", "w_sec_d", "phase_sec", "width_conv", "tmag", "morph"]


def prsa():
    p = pd.read_csv(D / "xmatch/ebs.csv")
    per = p["Per"]
    return pd.DataFrame(dict(
        tic=p.TIC, source="prsa2022", p_bin_d=per, p_err_d=p.e_Per, t0_btjd=p.BJD0, t0_err_d=p.e_BJD0,
        w_prim_d=p["Wp-pf"] * per, w_sec_d=p["Ws-pf"] * per, phase_sec=(p["Phis-pf"] - p["Phip-pf"]) % 1,
        width_conv="prsa polyfit width (phase x P)", tmag=p.Tmag, morph=p.Morph))


def ttc():
    t3 = ascii.read(D / "g3/catalog_ttc/table3_new_ebs.txt", format="mrt").to_pandas()
    t4 = ascii.read(D / "g3/catalog_ttc/table4_known_ebs.txt", format="mrt").to_pandas()
    a = pd.DataFrame(dict(
        tic=t3.TIC, source="ttc_t3", p_bin_d=t3.Per, p_err_d=np.nan, t0_btjd=t3["T0-pri"], t0_err_d=np.nan,
        w_prim_d=t3["Dur-pri"] / 24, w_sec_d=t3["Dur-sec"] / 24, phase_sec=t3.Phase,
        width_conv="TTC median eclipse duration (hours / 24)", tmag=t3.Tmag, morph=np.nan))
    b = pd.DataFrame(dict(
        tic=t4.TIC, source="ttc_t4", p_bin_d=t4["Per-TESS"], p_err_d=np.nan, t0_btjd=t4["T0-TESS"], t0_err_d=np.nan,
        w_prim_d=np.nan, w_sec_d=np.nan, phase_sec=np.nan, width_conv="none", tmag=np.nan, morph=np.nan))
    return pd.concat([a, b])


def calnet():
    d = json.load(open(D / "calnet_2026-11-07/parsed.json"))
    c = pd.DataFrame(dict(tic=pd.to_numeric(d["tic"], errors="coerce"), gaia=d["gaia"]))
    g = pd.read_csv(D / "calnet_2026-11-07/gaia_dr3_vari_eb_for_calnet.csv", dtype={"source_id": str})
    g["p"] = 1 / g.frequency
    c = c.merge(g[["source_id", "p", "derived_primary_ecl_duration"]], left_on="gaia", right_on="source_id", how="left")
    return pd.DataFrame(dict(
        tic=c.tic, source="calnet+gaia_dr3", p_bin_d=c.p, p_err_d=np.nan, t0_btjd=np.nan, t0_err_d=np.nan,
        w_prim_d=c.derived_primary_ecl_duration * c.p, w_sec_d=np.nan, phase_sec=np.nan,
        width_conv="Gaia DR3 derived duration (phase x P), about 1.38x Prsa", tmag=np.nan, morph=np.nan))


def main():
    rows = pd.concat([prsa(), ttc(), calnet()], ignore_index=True)[COLS]
    rows = rows[rows.tic.notna()].copy()
    rows["tic"] = rows.tic.astype("int64")
    rows.to_csv(OUT / "sources.csv", index=False)

    # Check that can fail: our reading of the G2 rule must reproduce the saved G2 list (895 stars).
    g1 = set(pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").tic.astype("int64"))
    g2 = set(pd.read_csv(r"D:\second-sun\targets\g2_targets.csv", comment="#").tic.astype("int64"))
    g3 = set(pd.read_csv(r"D:\second-sun\targets\g3_targets.csv", comment="#").tic.astype("int64"))
    pr = rows[rows.source == "prsa2022"]
    rule = pr[(pr.morph >= 0) & (pr.morph < 0.5) & (pr.p_bin_d > 5) & (pr.tmag <= 13.5) & ~pr.tic.isin(g1)]
    print("G2 rule check: rule", rule.tic.nunique(), "saved", len(g2), "overlap", len(set(rule.tic) & g2))

    # Period agreement between sources for the same star (ratio near 1, 2 or 0.5).
    piv = rows.dropna(subset=["p_bin_d"]).groupby(["tic", "source"]).p_bin_d.first().unstack()
    pairs = [("prsa2022", "ttc_t4"), ("prsa2022", "calnet+gaia_dr3"), ("ttc_t3", "calnet+gaia_dr3"), ("ttc_t4", "calnet+gaia_dr3")]
    agree = {}
    for a, b in pairs:
        if a in piv and b in piv:
            r = (piv[a] / piv[b]).dropna()
            agree[f"{a} vs {b}"] = dict(n=int(len(r)), same=int((abs(r - 1) < 0.01).sum()),
                                       half_or_double=int(((abs(r - 2) < 0.02) | (abs(r - 0.5) < 0.01)).sum()))
    print(json.dumps(agree, indent=1))

    # One row per star: best ephemeris by order TTC t3 > TTC t4 > Prsa > Gaia (newest TESS fits first); all sources listed.
    order = {"ttc_t3": 0, "ttc_t4": 1, "prsa2022": 2, "calnet+gaia_dr3": 3}
    rows["rank"] = rows.source.map(order) + rows.t0_btjd.isna() * 0.5
    best = rows.sort_values(["tic", "rank"]).groupby("tic").first().reset_index()
    best["sources"] = rows.groupby("tic").source.apply(lambda s: "+".join(sorted(set(s)))).reindex(best.tic).values
    best["has_ephemeris"] = best.p_bin_d.notna() & best.t0_btjd.notna()
    best["has_width"] = best.w_prim_d.notna()
    best["searched"] = np.select([best.tic.isin(g1), best.tic.isin(g2), best.tic.isin(g3)], ["G1", "G2", "G3"], "")
    best.drop(columns="rank").to_csv(OUT / "eb_union.csv", index=False)
    s = dict(stars=len(best), with_ephemeris=int(best.has_ephemeris.sum()), with_width=int(best.has_width.sum()),
             p_over_5=int((best.p_bin_d > 5).sum()), p_over_5_ephem_width=int(((best.p_bin_d > 5) & best.has_ephemeris & best.has_width).sum()),
             searched=int((best.searched != "").sum()), by_best_source=best.source.value_counts().to_dict())
    print(json.dumps(s, indent=1))
    json.dump(dict(summary=s, agreement=agree), open(OUT / "summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
