"""Kepler-16 dry run, v2 of the mask: eclipses found from ALL sectors folded together (period 41 d > one sector),
then the search runs per sector with that global mask. Uses files already downloaded (no new downloads)."""
import glob, json, pathlib, numpy as np
from detect_v2 import load, eclipse_mask_auto, find_events, systematics, veto
P = 41.0775867
files = sorted(glob.glob(r"D:\second-sun\data\overnight\lk\mastDownload\TESS\*-0000000299096355-*-s\*_lc.fits"))
data = [load(p)[:2] for p in files]
T = np.concatenate([d[0] for d in data]); F = np.concatenate([d[1] for d in data])
keepG, runs = eclipse_mask_auto(T, F, P)
print(f"{len(files)} sectors; global eclipse runs (phase): {[(round(a, 4), round(b, 4)) for a, b in runs]}; masked {100*(~keepG).mean():.1f}%")
rows, i0 = [], 0
for p, (t, f) in zip(files, data):
    keep = keepG[i0:i0 + len(t)]; i0 += len(t)
    ev = find_events(t[keep], f[keep]); fl = find_events(t[keep], 2 - f[keep])
    e, d = systematics(p); kept, rej = veto(ev, e, d, fl)
    rows.append(dict(file=pathlib.Path(p).name[:30], events=[(round(x["center"], 3), x["dur_h"], round(x["snr"], 1), x["flags"]) for x in kept],
                     rejected=[(round(x["center"], 3), x["veto"]) for x in rej], fakes=len(fl)))
    if kept or rej: print(rows[-1])
tot = dict(events=sum(len(r["events"]) for r in rows), unflagged=sum(1 for r in rows for x in r["events"] if not x[3]), fakes=sum(r["fakes"] for r in rows))
print("TOTALS", tot)
pathlib.Path(__file__).with_name("dryrun_kepler16_global_results.json").write_text(json.dumps(dict(runs=runs, rows=rows, totals=tot), indent=1, default=str))
