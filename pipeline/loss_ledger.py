"""Vesper study phase A (VESPER-STUDY-PLAN.md): the per-flag loss ledger. No search runs. For each flag: the share of injected planet-shaped dips it costs (from chain_recovery rows: data/chain_recovery/rows_v7.pkl
for G1, data/chain_recovery_g2/rows_g2dev.pkl for G2 dev) against the upside-down and real events it removes (from the run's events through stage3_report.load). "Sole" = the event carries only this flag, so
dropping the flag alone would free it. Also: the long-dip split (seen vs kept by flags, per box length) and the transits a circumbinary planet could give per star (sizes the stacking idea).
Usage: python loss_ledger.py   (reads both sets; writes research\\stage3\\loss-ledger-0.7.1.txt; aggregates only)"""
import os, sys, subprocess, json, pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(r"D:\second-sun")
FLAGS = ("gap_dump", "common", "flipmatch", "c5", "ecl_overlap", "repeater", "step", "ramp", "dominated")
T1 = ("1A", "1L", "1B")


def inj_part(rows, name):
    r = rows[rows.get("error").isna()] if "error" in rows else rows
    d = r[(r.sign == 1) & (r.K >= 10)].copy()
    for f in FLAGS:
        d[f] = d[f].fillna(False).astype(bool)
    prim = d[d.found_primary.fillna(False).astype(bool)]
    n = len(d); out = [f"{name}: injected dips at 10 x noise or more: {n}; primary {len(prim)}; tier 1 {int(prim.tier.isin(T1).sum())} ({100 * prim.tier.isin(T1).sum() / n:.0f}%); tier 2 {int((prim.tier == '2').sum())} ({100 * (prim.tier == '2').sum() / n:.0f}%)"]
    t2 = prim[prim.tier == "2"]
    nflags = t2[list(FLAGS)].sum(axis=1)
    out.append(f"  flags per lost (tier-2) fake: 1 flag {int((nflags == 1).sum())}, 2 flags {int((nflags == 2).sum())}, 3 or more {int((nflags >= 3).sum())}")
    out.append("  flag        | on lost fakes | SOLE flag on lost fakes (dropping it alone frees them) | share of ALL fakes it alone loses")
    for f in FLAGS:
        on, sole = int(t2[f].sum()), int((t2[f] & (nflags == 1)).sum())
        out.append(f"  {f:11s} | {on:5d} ({100 * on / max(len(t2), 1):3.0f}%) | {sole:5d} ({100 * sole / max(len(t2), 1):3.0f}%) | {100 * sole / n:4.1f}%")
    out.append("  long-dip split (all K 10 or more): box h | seen at SNR 7 anywhere | primary | tier 1 | step on primary | gap_dump on primary | ramp on primary")
    for dur, g in d.groupby("dur"):
        p = g[g.found_primary.fillna(False).astype(bool)]
        out.append(f"    {dur:4.0f} | {100 * g.found_any.mean():3.0f}% | {100 * len(p) / len(g):3.0f}% | {100 * p.tier.isin(T1).sum() / len(g):3.0f}% | {100 * p.step.mean():3.0f}% | {100 * p.gap_dump.mean():3.0f}% | {100 * p.ramp.mean():3.0f}%")
    return out


def events_part(set_name, run):
    code = ("import os,sys,json; sys.path.insert(0, r'D:\\second-sun\\pipeline'); import stage3_report as R; "
            f"ev,_=R.load(r'{run}'); E=ev[ev.primary]; E[['kind','tier','snr'] + [c for c in {list(FLAGS)!r} if c in E]].to_pickle(r'{ROOT}\\data\\loss_ledger_{set_name}.pkl')")
    env = dict(os.environ, SS_SET=set_name)
    subprocess.run([sys.executable, "-c", code], env=env, check=True, capture_output=True)
    E = pd.read_pickle(ROOT / "data" / f"loss_ledger_{set_name}.pkl")
    for f in FLAGS:
        E[f] = E[f].fillna(False).astype(bool) if f in E else False
    E = E[E.snr >= 7]
    nfl = E[list(FLAGS)].sum(axis=1)
    out = [f"{set_name} run events (best product, SNR 7 or more): real {int((E.kind == 'real').sum())}, upside-down {int((E.kind == 'flip').sum())}; tier 1 real {int(((E.kind == 'real') & E.tier.isin(T1)).sum())}, upside-down {int(((E.kind == 'flip') & E.tier.isin(T1)).sum())}"]
    out.append("  flag        | removes real (sole) | removes upside-down (sole) | sole upside-down per 1,000 events = false alarms it alone prevents")
    for f in FLAGS:
        r, u = E[E.kind == "real"], E[E.kind == "flip"]
        rs, us = int((r[f] & (nfl[r.index] == 1)).sum()), int((u[f] & (nfl[u.index] == 1)).sum())
        out.append(f"  {f:11s} | {int(r[f].sum()):5d} ({rs:4d}) | {int(u[f].sum()):5d} ({us:4d}) | {1000 * us / max(len(u), 1):5.0f}")
    return out


def transits_part():
    b = pd.read_csv(ROOT / "data" / "g2" / "audit" / "best_per_star_sector.csv", usecols=["tic", "sector"])
    n = b.groupby("tic").sector.nunique()
    out = [f"G2 dev: sectors per star with a usable product: min {n.min()}, quartiles {n.quantile([.25, .5, .75]).tolist()}, max {n.max()}"]
    days = n * 25.0                                            # about 25 usable days per sector (27 d minus the orbit gaps), an assumption
    for Pp in (50, 100, 200, 400):
        k = days / Pp
        out.append(f"  planet period {Pp:3d} d: expected transits seen per star (about 25 usable days per sector): median {k.median():.1f}; stars with 4 or more {int((k >= 4).sum())} of {len(k)}; with 16 or more {int((k >= 16).sum())}")
    return out


if __name__ == "__main__":
    txt = ["Vesper 0.7.1 loss ledger (study phase A, 29 Oct 2026). Aggregates only. Injections: K = depth in units of the 8 h box noise; 'lost' = primary but tier 2.", ""]
    txt += inj_part(pd.read_pickle(ROOT / "data" / "chain_recovery" / "rows_v7.pkl"), "G1 (rows_v7)") + [""]
    txt += inj_part(pd.read_pickle(ROOT / "data" / "chain_recovery_g2" / "rows_g2dev.pkl"), "G2 dev (rows_g2dev)") + [""]
    txt += events_part("g1", str(ROOT / "data" / "stage3" / "fd788be04650" / "groups")) + [""]
    txt += events_part("g2", str(ROOT / "data" / "stage3_g2" / "dev_73f62615e365" / "groups")) + [""]
    txt += transits_part()
    print("\n".join(txt))
    (ROOT / "research" / "stage3" / "loss-ledger-0.7.1.txt").write_text("\n".join(txt), encoding="utf-8")
