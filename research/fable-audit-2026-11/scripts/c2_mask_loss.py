"""C2 sanity test and tuning (10 Nov 2026, Opus 5.5). C1f cadence mask (c1_mask with C1_PSLOW=1e9, Z 5) + the event veto of c2_event_veto.py.
Imports the Part A, C0 and C1 harness files; edits none of them. Rows (private) -> data\\fable_audit_mask\\rows_<set>_c2.pkl. Counts only.
  SS_SET=g2 python c2_mask_loss.py synth N_PER   tuning on planted material: synthetic recurring eclipse in every sector + one planted dip, slow stars only
  SS_SET=g2 python c2_mask_loss.py run N_PER 6   harness (planted dips/bumps with the veto applied; real-light counts before/after the veto)
  SS_SET=g2 python c2_mask_loss.py summary"""
import os, sys, pathlib, multiprocessing as mp
os.environ.setdefault("C1_PSLOW", "1e9"); os.environ.setdefault("C1_Z", "5")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
import c1_mask_loss as L
import c1_mask as C1
import c2_event_veto as V
M, H, C0 = L.M, L.M.H, L.M.C0
H.ROWS = H.OUT / f"rows_{H.SET}_c2.pkl"
SYNTH = None
CUR = dict(P=np.nan, T0=0.0, off=0.0, oth={1: [], -1: []}, dip_found=0, dip_vetoed=0)
_CACHE = {}


def star_geom(tic, t, f):
    c = C0.cat().get(tic)
    if c is not None and np.isfinite(c.get("wp", np.nan)):
        return c, c["P"], c["T0"], C1._offset(t, f, c)
    per = H.A.PER.get(tic, [])
    return None, (per[0] if per else np.nan), 0.0, 0.0


def others(tic, own_sector):
    """{arm: [(phase, dur_h, depth_ppm)]} from the star's other sectors (one product per sector, SPOC family first), C1f mask, no injection."""
    key = (tic, own_sector, SYNTH is not None)
    if key in _CACHE:
        return _CACHE[key]
    man = pd.read_csv(H.DS.MANIFEST).drop_duplicates("file"); m = man[man.tic == tic].copy()
    m = m.assign(sec=[V.sector_of(x) for x in m.file], pri=(m.author == "QLP").astype(int).values)
    m = m[m.sec.notna() & (m.sec != own_sector)].sort_values(["sec", "pri"]).groupby("sec").head(1)
    out = {1: [], -1: []}; per = H.A.PER.get(tic, [])
    for p, sec in zip(m.path, m.sec):
        try:
            tf, meta, st = H.load_windowed(p)
            if tf is None:
                continue
            t, f = tf
            if SYNTH is not None:
                f = f + SYNTH(t)
            c, P, T0, off = star_geom(tic, t, f)
            if not np.isfinite(P) or P < V.PSLOW:
                continue
            t2, f2, _ = C1.mask_runs(t, f, per, tic=tic)
            for arm in (1, -1):
                out[arm] += [(V.phase(e["center"], P, T0, off), e["dur_h"], e["depth_ppm"], int(sec)) for e in H.S2.Prod(t2, f2, arm).events()]
        except Exception:
            continue
    _CACHE[key] = out
    return out


def found_veto(t, f, arm, tc, dur):
    pr = H.S2.Prod(t, f, arm)
    near = [e for e in pr.events() if abs(e["center"] - tc) <= 0.5 * max(dur, e["dur_h"]) / 24 + 0.1]
    if not near:
        return False, pr
    kept, vet = V.veto(near, CUR["oth"][arm], CUR["P"], CUR["T0"], CUR["off"])
    if arm == 1:
        CUR["dip_found"] += 1; CUR["dip_vetoed"] += int(not kept)
    return bool(kept), pr


def init():
    M.init(); H.found = found_veto


def run_file(args):
    path, tic = args[0], args[1]
    extra = {}
    try:
        tf, meta, st = H.load_windowed(path)
        if tf is not None:
            t, f = tf; c, P, T0, off = star_geom(tic, t, f)
            CUR.update(P=P, T0=T0, off=off, oth=others(tic, V.sector_of(pathlib.Path(path).name)) if np.isfinite(P) and P >= V.PSLOW else {1: [], -1: []},
                       dip_found=0, dip_vetoed=0)
            t2, f2, _ = C1.mask_runs(t, f, H.A.PER.get(tic, []), tic=tic)
            for arm, lab in ((1, "real"), (-1, "inv")):
                ev = H.S2.Prod(t2, f2, arm).events(); kept, vet = V.veto(ev, CUR["oth"][arm], P, T0, off)
                extra.update({f"c2_{lab}": len(kept), f"vet_{lab}": len(vet), f"c1f_{lab}": len(ev)})
            extra["n_oth"] = len(CUR["oth"][1]) + len(CUR["oth"][-1])
    except Exception as e:
        extra["c2_err"] = type(e).__name__
    rows = M.run_file(args)
    extra.update(dip_found=CUR["dip_found"], dip_vetoed=CUR["dip_vetoed"])
    return [dict(r, **extra) for r in rows]


def run(n_per, procs):
    jobs, _ = H.sample(n_per); rows = []
    with mp.Pool(procs, initializer=init) as pool:
        for r in pool.imap_unordered(run_file, jobs):
            rows += r
    pd.DataFrame(rows).to_pickle(H.ROWS); print("DONE", len(rows), flush=True)


def summary():
    out = M.summary()
    df = pd.read_pickle(H.ROWS); f = df.drop_duplicates("file"); f = f[f["skip"].isna()] if "skip" in f else f
    out += ["", "G. C2 = C1f + event veto (slow binaries, P >= 13 d). Real light, nothing planted: real/upside-down events before -> after the veto; events vetoed real/upside-down"]
    for lo, hi in H.BINS:
        g = f[f.bin_lo == lo]
        if not len(g):
            continue
        s = lambda c: int(g[c].sum())
        out.append(f"  {lo:>4g} d n{len(g):3d} | C1f {s('c1f_real')}/{s('c1f_inv')} -> C2 {s('c2_real')}/{s('c2_inv')} = {s('c2_real') / max(s('c2_inv'), 1):.2f} | vetoed {s('vet_real')}/{s('vet_inv')} | "
                   f"planted dips found {s('dip_found')}, vetoed by chance match {s('dip_vetoed')}")
    return out


def synth_one(args):
    """One slow-star file: synthetic recurring eclipse in every sector + one planted dip here; events at the synthetic eclipse and at the dip, vetoed or not, per TOL."""
    global SYNTH
    path, tic, P0, fam, lo, i = args
    try:
        tf, meta, st = H.load_windowed(path)
        if tf is None:
            return []
        t, f = tf; c, P, T0, off = star_geom(tic, t, f)
        if not np.isfinite(P) or P < V.PSLOW:
            return []
        C0.CURRENT_TIC = tic; t2, f2, _ = C1.mask_runs(t, f, H.A.PER.get(tic, []), tic=tic); n8 = H.noise(t2, f2, 8.0)
        rng = np.random.default_rng([tic, i, 99]); Ke = (6.0, 15.0, 40.0)[i % 3]; ws = rng.uniform(3, 8); phs = rng.uniform(0.15, 0.35) if i % 2 else rng.uniform(0.6, 0.85)
        def syn(tt):
            dt = ((tt - T0 - phs * P + P / 2) % P) - P / 2
            return H.signal(dt, 0.0, ws, Ke * n8, 1)
        SYNTH = syn
        oth = others(tic, V.sector_of(pathlib.Path(path).name))
        fs = f + syn(t); dt = ((t - T0 - phs * P + P / 2) % P) - P / 2
        ok = (np.abs(dt) > 1.0) & (t - t.min() > 1.5) & (t.max() - t > 1.5)
        if ok.sum() < 10:
            return []
        tp = float(rng.choice(t[ok])); fsp = fs + H.signal(t, tp, 8.0, 12 * n8, 1)
        t3, f3, _ = C1.mask_runs(t, fsp, H.A.PER.get(tic, []), tic=tic)
        ev = H.S2.Prod(t3, f3, 1).events(); evu = H.S2.Prod(t3, f3, -1).events()
        cens = T0 + off + (np.round((t - T0 - off) / P - phs) + phs) * P
        at_syn = [e for e in ev if np.min(np.abs(np.unique(np.round(cens, 3)) - e["center"])) < ws / 48 + 0.1]
        at_dip = [e for e in ev if abs(e["center"] - tp) <= 0.5 * max(8, e["dur_h"]) / 24 + 0.1]
        rows = []
        for tol in (1.0, 2.0, 4.0):
            rows.append(dict(bin_lo=lo, Ke=Ke, tol=tol, n_oth=len(oth[1]), syn_ev=len(at_syn), syn_vet=len(V.veto(at_syn, oth[1], P, T0, off, tol)[1]),
                             dip_ev=int(bool(at_dip)), dip_vet=int(bool(at_dip) and not V.veto(at_dip, oth[1], P, T0, off, tol)[0]),
                             other_real=len(ev) - len(at_syn) - len(at_dip), other_real_vet=len(V.veto([e for e in ev if e not in at_syn and e not in at_dip], oth[1], P, T0, off, tol)[1]),
                             inv=len(evu), inv_vet=len(V.veto(evu, oth[-1], P, T0, off, tol)[1])))
        return rows
    except Exception as e:
        return [dict(err=f"{type(e).__name__}: {str(e)[:60]}")]


def synth(n_per):
    jobs, _ = H.sample(n_per); jobs = [j for j in jobs if j[2] >= V.PSLOW]
    with mp.Pool(6, initializer=init) as pool:
        df = pd.DataFrame([r for rr in pool.map(synth_one, jobs) for r in rr])
    if "err" in df:
        print("errors:", int(df.err.notna().sum()), df.err.dropna().unique()[:3]); df = df[df.err.isna()]
    print(f"C2 synthetic test, set {H.SET}: {len(df) // 3} slow-star files (P >= 13 d); synthetic eclipse in every sector + one planted 8 h K 12 dip in the sampled sector")
    for tol, g in df.groupby("tol"):
        print(f"  TOL {tol:g} h | synthetic-eclipse events vetoed {int(g.syn_vet.sum())} of {int(g.syn_ev.sum())} | planted dip found {int(g.dip_ev.sum())}, vetoed by chance {int(g.dip_vet.sum())} | "
              f"other real-arm events vetoed {int(g.other_real_vet.sum())} of {int(g.other_real.sum())} | upside-down events vetoed {int(g.inv_vet.sum())} of {int(g.inv.sum())} | files with no other-sector events {int((g.n_oth == 0).sum())}")
    for (tol, ke), g in df.groupby(["tol", "Ke"]):
        print(f"    TOL {tol:g} Ke {ke:g}: synthetic vetoed {int(g.syn_vet.sum())}/{int(g.syn_ev.sum())}, dip vetoed {int(g.dip_vet.sum())}/{int(g.dip_ev.sum())}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "synth":
        synth(int(sys.argv[2]))
    elif mode == "run":
        run(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("\n".join(summary()))
