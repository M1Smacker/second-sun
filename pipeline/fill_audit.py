"""Step 0 of VESPER plan step 1 (29 Oct 2026; FIX-QUEUE 21a; Compass 2026-10-28-outside-ai-vesper-review.md change 1): how much of the v7 run's 'PDCSAP' light is not PDCSAP, and which
failures the run swallowed. Read only: no search is repeated, no rule changes, nothing frozen is edited.
A. Fill: detect_v2.load fills every cadence PDC dropped from locally scaled SAP (and reads SAP alone when the whole PDCSAP column is empty). For EVERY SPOC and TESS-SPOC file of G1 count the
   filled cadences (same hard quality mask, same rule as load()).
B. Events: how many primary events of the PDCSAP half (v7 merged table) have a filled cadence inside their box. COUNTS ONLY, no star number and no time is printed.
C. Swallowed failures in the group files: prepare statuses other than ok, events without step measurements (stage3.add_step swallows a failed prepare), SAP-twin events without a PDCSAP check
   (stage3.add_pdc swallows a failed prepare) and the error lines the run logs hold.
Usage: python fill_audit.py [procs]   (writes research\\stage3\\fill_audit_v7.txt; the per-file table stays in data\\chain_recovery)"""
import sys, glob, json, pathlib, multiprocessing as mp
import numpy as np, pandas as pd
import lightkurve as lk
import stage3_core as C, stage3_report as R

RUN = C.ROOT / "data" / "stage3" / "fd788be04650"
PREP = C.ROOT / "data" / "chain_recovery"
LOGS = C.ROOT / "data" / "stage3"


def one(args):
    """(tic, sector, product, cadences kept, cadences filled from SAP, PDCSAP column empty, times of the filled cadences) for one SPOC-family file, by the rule of detect_v2.load."""
    tic, file, path, author = args
    lc = lk.read(path, quality_bitmask="hard")
    t = lc.time.value; sap = np.asarray(lc.sap_flux.value, float); pdc = np.asarray(lc.pdcsap_flux.value, float)
    ok = np.isfinite(t); t, pdc, sap = t[ok], pdc[ok], sap[ok]
    s = sap / np.nanmedian(sap)
    sec = int(lc.meta.get("SECTOR"))
    if not np.isfinite(pdc).any():
        return tic, sec, author, int(np.isfinite(s).sum()), 0, True, np.empty(0)
    f = pdc / np.nanmedian(pdc)
    fill = ~np.isfinite(f) & np.isfinite(s)
    return tic, sec, author, int((np.isfinite(f) | fill).sum()), int(fill.sum()), False, t[fill]


def safe(a):
    try:
        return one(a)
    except Exception as e:
        return ("ERROR", a[1], f"{type(e).__name__}: {str(e)[:80]}")


def share(x, lab):
    return f"{lab}: {int(x.sum())} of {len(x)} ({100 * x.mean():.1f}%)"


def main(procs, reuse=False):
    if reuse and (PREP / "fill_files.pkl").exists():             # the file table of the first run (3,019 files read, 0 unreadable): only the event counts below changed
        df, bad = pd.read_pickle(PREP / "fill_files.pkl"), []
    else:
        man = pd.read_csv(C.MANIFEST).drop_duplicates("file"); man = man[man.author.isin(("SPOC", "TESS-SPOC"))]
        with mp.Pool(procs) as pool:
            res = pool.map(safe, [(int(r.tic), r.file, r.path, r.author) for r in man.itertuples()], chunksize=20)
        bad = [r for r in res if r[0] == "ERROR"]
        df = pd.DataFrame([r for r in res if r[0] != "ERROR"], columns=["tic", "sector", "product", "kept", "filled", "pdc_empty", "fill_t"])
        PREP.mkdir(parents=True, exist_ok=True); df.to_pickle(PREP / "fill_files.pkl")
    df["frac"] = df.filled / df.kept
    t = ["Step 0 audit of the v7 run (hash fd788be04650): cadences filled from SAP in the 'PDCSAP' half, and failures the run swallowed. Counts only; nothing was searched again.", "",
         f"A. FILL, every SPOC and TESS-SPOC file of G1 ({len(df)} read, {len(bad)} could not be read" + (": " + "; ".join(f"{b[1][:30]} {b[2]}" for b in bad[:5]) if bad else "") + ")",
         f"  cadences kept {int(df.kept.sum())}, filled from SAP {int(df.filled.sum())} ({100 * df.filled.sum() / df.kept.sum():.2f}% of all cadences)",
         "  " + share(df.filled > 0, "files with at least one filled cadence"), "  " + share(df.frac > 0.01, "files with more than 1% filled"), "  " + share(df.frac > 0.05, "files with more than 5% filled"),
         "  " + share(df.frac > 0.20, "files with more than 20% filled"), "  " + share(df.pdc_empty, "files whose whole PDCSAP column is empty (read as SAP alone)"),
         "  by product: " + ", ".join(f"{p} {100 * g.filled.sum() / g.kept.sum():.2f}% filled, {int((g.filled > 0).sum())} of {len(g)} files touched" for p, g in df.groupby("product")), ""]
    ev, meta = R.load(str(RUN / "groups"))
    fm = {(int(r.tic), int(r.sector), r.product): (r.fill_t, bool(r.pdc_empty)) for r in df.itertuples()}
    pe = ev[ev.primary & ev["product"].isin(("SPOC", "TESS-SPOC")) & ev.seen_by.isin(("PDCSAP only", "both"))].copy()
    inbox, empty = [], []
    for r in pe.itertuples():
        ft, pe_empty = fm.get((int(r.tic), int(r.sector), r.product), (np.empty(0), False))
        inbox.append(bool(np.any(np.abs(ft - r.center) <= r.dur_h / 48))); empty.append(pe_empty)
    pe["fill_in_box"], pe["pdc_empty"] = inbox, empty
    pe["t1"] = pe.tier.isin(("1A", "1L", "1B"))
    t.append(f"B. PRIMARY EVENTS OF THE PDCSAP HALF ({len(pe)}: SPOC or TESS-SPOC best product, seen by PDCSAP or both) WITH A FILLED CADENCE INSIDE THE BOX")
    for lab, g in (("all tiers", pe), ("tier 1 (1A, 1L, 1B)", pe[pe.t1])):
        for kind in ("real", "flip"):
            h = g[g.kind == kind]
            t.append(f"  {lab}, {kind}: {int(h.fill_in_box.sum())} of {len(h)} have at least one filled cadence in the box; {int(h.pdc_empty.sum())} come from a file whose PDCSAP column is empty")
    h = pe[pe.t1]
    t.append(f"  tier 1 real minus upside-down: {int((h.kind == 'real').sum())} vs {int((h.kind == 'flip').sum())} in the PDCSAP half; with filled cadences in the box {int(h[h.kind == 'real'].fill_in_box.sum())} vs {int(h[h.kind == 'flip'].fill_in_box.sum())}")
    p1 = ev[ev.primary & ev.tier.isin(("1A", "1L", "1B"))].assign(src=lambda x: np.where(x.seen_by == "SAP only", "SAP only", x["product"]))
    t.append("  tier 1 primary events by where they come from (all products, counts): " + "; ".join(f"{s}: {int((g.kind == 'real').sum())} real, {int((g.kind == 'flip').sum())} upside-down" for s, g in sorted(p1.groupby("src"))))
    p1 = p1.assign(flux=lambda x: np.where(x["product"] == "QLP", "QLP " + x["column"].astype(str), np.where(x["product"].str.endswith("-SAP"), "SPOC family raw SAP (twin)", "SPOC family PDC flux")))
    t.append("  tier 1 primary events by FLUX COLUMN (counts; QLP before sector 56 has no cleaned column, our loader reads its raw sap_flux): " + "; ".join(f"{s}: {int((g.kind == 'real').sum())} real, {int((g.kind == 'flip').sum())} upside-down" for s, g in sorted(p1.groupby("flux"))))
    t.append("")
    # C. swallowed failures in the group files
    bp = pd.read_csv(C.BEST, usecols=["tic", "sector", "product"]); best = {(int(a), int(b)): c for a, b, c in zip(bp.tic, bp.sector, bp["product"])}
    stat, noshift, nopdc, nanpdc, nsap = {}, {}, 0, 0, 0
    for d in ("groups", "groups_sap"):
        for p in glob.glob(str(RUN / d / "*.json")):
            g = json.load(open(p))
            for m in g["meta"]:
                s = str(m.get("status", "?")); s = "ERROR" if s.startswith("ERROR") else s
                stat[(d, s)] = stat.get((d, s), 0) + 1
            for e in g["events"]:
                if "lift_pre" not in e:
                    noshift[(d, e["product"])] = noshift.get((d, e["product"]), 0) + 1
                if d == "groups_sap" and e["product"] == best.get((g["tic"], g["sector"]), "?") + "-SAP":       # only the SAP twin of the best product is checked against PDCSAP (stage3.add_pdc)
                    nsap += 1
                    if "pdc_snr" not in e:
                        nopdc += 1
                    elif e["pdc_snr"] is None or e["pdc_snr"] != e["pdc_snr"]:
                        nanpdc += 1
    t.append("C. SWALLOWED OR SILENT FAILURES")
    t.append("  prepare status of every file in every group, by folder (status other than ok is a file that gave no data to that search):")
    for (d, s), n in sorted(stat.items()):
        t.append(f"    {d:11s} {s:34s} {n}")
    t.append("  events with no step measurement (stage3.add_step swallowed a failed prepare, or the product was missing): " + (", ".join(f"{d} {p}: {n}" for (d, p), n in sorted(noshift.items())) if noshift else "none"))
    t.append(f"  SAP-twin events of the best product: {nsap}; with no PDCSAP check at all (stage3.add_pdc swallowed a failed prepare): {nopdc}; with an empty check (NaN, 'not measurable', PDC dropped those cadences): {nanpdc}")
    logs = {p.name: sum("ERROR" in line for line in open(p, errors="replace")) for p in sorted(LOGS.glob("run_log*.txt"))}
    t.append("  ERROR lines in the run logs (what the run itself printed): " + ", ".join(f"{k} {v}" for k, v in logs.items()))
    print("\n".join(t))
    (C.ROOT / "research" / "stage3" / "fill_audit_v7.txt").write_text("\n".join(t), encoding="utf-8")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5, len(sys.argv) > 2 and sys.argv[2] == "reuse")
