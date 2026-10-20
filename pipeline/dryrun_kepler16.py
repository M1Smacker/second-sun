"""First G1 dry run: Kepler-16 (KIC 12644769, TIC 299096355), all SPOC 2-min sectors, catalogue period only.
Pipeline: load -> eclipse_mask_auto(P from targets/g1_targets.csv) -> find_events -> flipped false alarms
-> systematics flags. Kepler-16 b is a known circumbinary planet; whether it transits during TESS must be
checked against the literature before interpreting any event (not assumed here).
Downloads ~2 MB per sector to D:\\second-sun\\data\\overnight\\lk, each logged in research/downloads.csv."""
import csv, json, pathlib, datetime, numpy as np, lightkurve as lk
from detect_v2 import load, eclipse_mask_auto, find_events, systematics, veto

DL = pathlib.Path(r"D:\second-sun\data\overnight\lk")
LOG = pathlib.Path(r"D:\second-sun\research\downloads.csv")
TIC, P = "299096355", 41.0775867   # P_bin from targets/g1_targets.csv (Villanova)
sr = lk.search_lightcurve(f"TIC {TIC}", author="SPOC", exptime=120)
print(len(sr), "SPOC 2-min sectors", flush=True)
rows = []
for i in range(len(sr)):
    lc = sr[i].download(download_dir=str(DL))
    path = lc.meta["FILENAME"]; sec = int(lc.meta["SECTOR"])
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow():%Y-%m-%dT%H:%M:%SZ},Kepler-16 S{sec} SPOC 2-min LC,https://mast.stsci.edu,"
                f"{pathlib.Path(path).stat().st_size},{path},G1 dry run (known CBP host),overnight\n")
    t, f, _ = load(path)
    keep, runs = eclipse_mask_auto(t, f, P)
    ev = find_events(t[keep], f[keep]); fl = find_events(t[keep], 2 - f[keep])
    edges, dumps = systematics(path)
    kept, rej = veto(ev, edges, dumps, fl)
    rows.append(dict(sector=sec, n_eclipse_runs=len(runs), masked_pct=round(100 * (~keep).mean(), 1),
                     events=[(round(e["center"], 3), e["dur_h"], round(e["snr"], 1), round(e["depth_ppm"]), e["flags"]) for e in kept],
                     rejected=[(round(e["center"], 3), e["veto"]) for e in rej], fakes=len(fl)))
    print(rows[-1], flush=True)
tot = dict(sectors=len(rows), events=sum(len(r["events"]) for r in rows),
           unflagged=sum(1 for r in rows for e in r["events"] if not e[4]), fakes=sum(r["fakes"] for r in rows))
print("TOTALS", tot)
pathlib.Path(__file__).with_name("dryrun_kepler16_results.json").write_text(json.dumps(dict(rows=rows, totals=tot), indent=1, default=str))
