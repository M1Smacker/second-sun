r"""Quality-mask experiment runner. Spec: SPEC.md in this folder (frozen before any arm ran).
  .\.venv\Scripts\python.exe experiments\quality_mask\qmask.py --check   inputs, hashes, constants; writes nothing
  .\.venv\Scripts\python.exe experiments\quality_mask\qmask.py --run     full run into a NEW results folder (never overwrites)
QMASK_SECTORS="65,98" restricts the sectors and names the folder smoke_*: a code test, not part of the experiment.
Imports only detect_v2 (read-only). Never imports accept_v2.py or diag_v2.py. No downloads."""
import os, sys, json, glob, hashlib, subprocess, pathlib, datetime, platform
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "labs")); sys.path.insert(0, str(ROOT / "pipeline"))
import _env                                   # keeps every cache on D: (labs/_env.py)
import lightkurve as lk, batman
from scipy.stats import chi2
from wotan import flatten
from detect_v2 import load, eclipse_mask, find_events

P, D1, D2, SEC = 14.6084, 4.7, 6.1, 0.454
PUB = {6: 1483.9048, 10: 1579.0423, 27: 2049.9515, 30: 2142.3991, 34: 2238.2258,
       37: 2331.0148, 62: 2989.6356, 65: 3085.4243, 68: 3178.2853, 98: 4025.5927}
HARD, DEFAULT = 24319, 17087
U = [2 * np.sqrt(0.17) * 0.478, np.sqrt(0.17) * (1 - 2 * 0.478)]
B, T14, PER = 0.4, 6.4 / 24, 95.4
ARS = np.sqrt(1.03 ** 2 - B ** 2) / np.sin(np.pi * T14 / PER)
TIMES_ALL = [3997.6376, 3999.9, 4014.2876, 4017.1, 4028.0876, 4029.3876, 4037.2876, 4040.8876]
SECTORS = [int(x) for x in os.environ.get("QMASK_SECTORS", "").split(",") if x] or list(PUB)
SMOKE = bool(os.environ.get("QMASK_SECTORS"))
BASELINE = ROOT / "pipeline" / "accept_v2_results.json"
assert lk.utils.TessQualityFlags.HARD_BITMASK == HARD and lk.utils.TessQualityFlags.DEFAULT_BITMASK == DEFAULT


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, check=True).stdout.strip()


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def fits_path(s):
    hits = glob.glob(rf"D:\second-sun\data\*\lk\mastDownload\TESS\*-s{s:04d}-0000000260128333-*-s\*_lc.fits")
    assert hits, f"no cached SPOC 2-min file for sector {s}"
    return hits[0]


def manifest(paths):
    files = {**{f"S{s}": p for s, p in paths.items()}, "detect_v2.py": ROOT / "pipeline/detect_v2.py", "accept_v2.py": ROOT / "pipeline/accept_v2.py",
             "baseline_json": BASELINE, "SPEC.md": HERE / "SPEC.md", "qmask.py": HERE / "qmask.py"}
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), commit=git("rev-parse", "HEAD"),
                tracked_files_modified=[l for l in git("status", "--porcelain", "--untracked-files=no").splitlines() if l],
                python=platform.python_version(), numpy=np.__version__, lightkurve=lk.__version__, batman=batman.__version__,
                sectors=SECTORS, smoke=SMOKE, constants=dict(P=P, D1=D1, D2=D2, SEC=SEC, HARD=HARD, DEFAULT=DEFAULT, PUB=PUB),
                inputs={k: dict(path=str(v), sha256=sha256(v)) for k, v in files.items()})


class Out:
    """All writes go through here: inside one new folder, never overwriting."""
    def __init__(self):
        name = f"{'smoke_' if SMOKE else ''}{datetime.datetime.now(datetime.timezone.utc):%Y%m%dT%H%M%SZ}_{git('rev-parse', '--short', 'HEAD')}"
        self.d = (HERE / "results" / name).resolve(); self.d.mkdir(parents=True, exist_ok=False)

    def write(self, name, text):
        p = (self.d / name).resolve(); assert p.parent == self.d and not p.exists(); p.write_text(text, encoding="utf-8"); return p


def same(a, b, tol=1e-6, path=""):
    bad = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            bad += same(a[k], b[k], tol, f"{path}/{k}") if (k in a and k in b) else [f"{path}/{k}: missing on one side"]
    elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        bad += [f"{path}: length {len(a)} vs {len(b)}"] if len(a) != len(b) else [m for i, (x, y) in enumerate(zip(a, b)) for m in same(x, y, tol, f"{path}[{i}]")]
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        bad += [] if abs(a - b) <= tol else [f"{path}: {a} vs {b}"]
    elif a != b:
        bad.append(f"{path}: {a!r} vs {b!r}")
    return bad


def keep_from_T1(t, T1, pad=1.5):
    """Same geometry as detect_v2.eclipse_mask, but with the primary epoch T1 given (held fixed from A0)."""
    d1 = np.abs(((t - T1 + P / 2) % P) - P / 2); d2 = np.abs(((t - (T1 + SEC * P) + P / 2) % P) - P / 2)
    return (d1 > pad * D1 / 24) & (d2 > pad * D2 / 24)


def load_sap(path, mask):
    """SAP flux with a given lightkurve mask ('hard' or 'default'). Normalised by the median over HARD-retained cadences, so both arms share a scale.
    Returns t, f, restored (kept now but dropped by HARD), background."""
    lc = lk.read(path, quality_bitmask=mask)
    t = np.asarray(lc.time.value, float); sap = np.asarray(lc.sap_flux.value, float)
    q = np.asarray(lc.quality.value, int); bkg = np.asarray(lc["sap_bkg"].value, float)
    ok = np.isfinite(t) & np.isfinite(sap); t, sap, q, bkg = t[ok], sap[ok], q[ok], bkg[ok]
    hard_ok = (q & HARD) == 0
    return t, sap / np.nanmedian(sap[hard_ok]), ~hard_ok, bkg


def inject_trials(t, f, sizes, times):
    out = []
    for re_ in sizes:
        pr = batman.TransitParams()
        pr.per, pr.rp, pr.a, pr.inc, pr.ecc, pr.w, pr.u, pr.limb_dark = PER, re_ / (1.313 * 109.08), ARS, np.degrees(np.arccos(B / ARS)), 0.0, 90.0, U, "quadratic"
        for t0 in times:
            pr.t0 = t0; model = batman.TransitModel(pr, t).light_curve(pr)
            ev = find_events(t, f * model); h = [e for e in ev if abs(e["center"] - t0) < 0.25]
            out.append(dict(size=re_, t0=t0, recovered=bool(h), snr=float(h[0]["snr"]) if h else None, depth_ppm=float(h[0]["depth_ppm"]) if h else None,
                            dt_h=float(h[0]["center"] * 24 - t0 * 24) if h else None, centre_depth_ppm=float((1 - model.min()) * 1e6), n_events=len(ev)))
    return out


def pois(k, days):
    lo = chi2.ppf(0.025, 2 * k) / 2 if k else 0.0; hi = chi2.ppf(0.975, 2 * k + 2) / 2
    return dict(events=k, exposure_days=round(days, 1), per100d=round(100 * k / days, 2) if days else None,
                lo95=round(100 * lo / days, 2) if days else None, hi95=round(100 * hi / days, 2) if days else None)


def run_a0(paths):
    """Reproduce pipeline/accept_v2.py exactly (same code path, no file written), plus per-trial injection detail."""
    res = dict(recovery=[], false_alarms=[], injection=[]); T1s = {}; times = None; trials = []
    for s in SECTORS:
        t, f, nfill = load(paths[s]); keep, T1 = eclipse_mask(t, f, P, D1, D2, SEC); T1s[s] = T1; tpub = PUB[s]
        in_data = int(np.sum(np.abs(t - tpub) < 3 / 24)); in_kept = int(np.sum(keep & (np.abs(t - tpub) < 3 / 24)))
        ev = find_events(t[keep], f[keep]); hit = [e for e in ev if abs(e["center"] - tpub) < 0.3]
        res["recovery"].append(dict(sector=s, pub=tpub, sap_filled=nfill, cad_near_transit=in_data, kept_near_transit=in_kept, recovered=bool(hit),
            dt_h=hit[0]["center"] * 24 - tpub * 24 if hit else None, dur_h=hit[0]["dur_h"] if hit else None, snr=hit[0]["snr"] if hit else None,
            depth_ppm=hit[0]["depth_ppm"] if hit else None, other_events=[(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in ev if e not in hit]))
        fa = find_events(t[keep], 2 - f[keep])
        res["false_alarms"].append(dict(sector=s, n=len(fa), events=[(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in fa]))
        print("A0 sector", s, "done", flush=True)
    if 98 in SECTORS:
        t, f, _ = load(paths[98]); keep, _ = eclipse_mask(t, f, P, D1, D2, SEC); keep &= ~((t > 4025.30) & (t < 4025.95)); t, f = t[keep], f[keep]
        times = [x for x in TIMES_ALL if np.sum(np.abs(t - x) < T14 / 2) >= 0.9 * T14 / (2 / 1440)]
        res["injection_base_events"] = [(round(e["center"], 3), e["dur_h"], round(e["snr"], 1)) for e in find_events(t, f)]
        trials = inject_trials(t, f, (2, 3, 4, 5, 6, 7, 8), times)
        for re_ in (2, 3, 4, 5, 6, 7, 8):
            tr = [x for x in trials if x["size"] == re_]
            res["injection"].append(dict(R_earth=re_, depth_ppm=round((re_ / (1.313 * 109.08)) ** 2 * 1e6), recovered=sum(x["recovered"] for x in tr), n=len(times),
                                         snr=[round(x["snr"], 1) if x["recovered"] else None for x in tr]))
        print("A0 injection done", flush=True)
    return res, T1s, times, trials


def box_diag(e, t, rest, bkg, keep):
    box = keep & (np.abs(t - e["center"]) < e["dur_h"] / 48)
    ref = np.nanmedian(bkg[keep & ~rest])
    return dict(center=round(e["center"], 3), dur_h=e["dur_h"], snr=round(e["snr"], 2), depth_ppm=round(e["depth_ppm"]),
                restored_frac=round(float(rest[box].mean()), 3) if box.any() else None, bkg_ratio=round(float(np.nanmedian(bkg[box]) / ref), 2) if box.any() else None)


def run_arm(name, mask, paths, T1s, times):
    arm = dict(name=name, mask=mask, sectors=[], injection=[], restored_injection=[])
    for s in SECTORS:
        t, f, rest, bkg = load_sap(paths[s], mask); keep = keep_from_T1(t, T1s[s]); tpub = PUB[s]
        cad = float(np.median(np.diff(t))); win = np.abs(t - tpub) < 3 / 24
        ev = find_events(t[keep], f[keep]); flip = find_events(t[keep], 2 - f[keep])
        hit = [e for e in ev if abs(e["center"] - tpub) < 0.3]
        fl = flatten(t[keep], f[keep], method="biweight", window_length=2.0); ok = np.isfinite(fl); r_k = rest[keep]
        rob = lambda x: float(1.4826 * np.median(np.abs(x - np.median(x)))) if len(x) > 20 else None
        arm["sectors"].append(dict(
            sector=s, cadences=int(len(t)), kept=int(keep.sum()), restored_kept=int((keep & rest).sum()),
            window_all=int(win.sum()), window_kept=int((win & keep).sum()), window_restored=int((win & keep & rest).sum()),
            recovered=bool(hit), hit=box_diag(hit[0], t, rest, bkg, keep) if hit else None,
            other_events=[box_diag(e, t, rest, bkg, keep) for e in ev if e not in hit],
            flipped=[box_diag(e, t, rest, bkg, keep) for e in flip],
            exposure_retained_days=float((keep & ~rest).sum() * cad), exposure_restored_days=float((keep & rest).sum() * cad),
            scatter_ppm_retained=(rob(fl[ok & ~r_k]) or 0) * 1e6, scatter_ppm_restored=(rob(fl[ok & r_k]) or 0) * 1e6 if (ok & r_k).any() else None,
            bkg_restored_over_retained=float(np.nanmedian(bkg[keep & rest]) / np.nanmedian(bkg[keep & ~rest])) if (keep & rest).any() else None))
        print(name, "sector", s, "done", flush=True)
    if 98 in SECTORS and times:
        t, f, rest, bkg = load_sap(paths[98], mask)
        k = keep_from_T1(t, T1s[98]) & ~((t > 4025.30) & (t < 4025.95))
        arm["injection"] = inject_trials(t[k], f[k], (5, 6, 7), times)
        # exploratory: centres of restored stretches (>= 0.6 d, clear of eclipses), searched only if >= 90% of the transit window has data
        full_t, full_f, full_rest, _ = load_sap(paths[98], "default"); fk = keep_from_T1(full_t, T1s[98]) & ~((full_t > 4025.30) & (full_t < 4025.95))
        idx = np.where(full_rest)[0]; cuts = np.where(np.diff(full_t[idx]) > 0.1)[0]
        stretches = [(full_t[g[0]], full_t[g[-1]]) for g in np.split(idx, cuts + 1) if len(g) and full_t[g[-1]] - full_t[g[0]] >= 0.6]
        centres = [round(float((a + b) / 2), 4) for a, b in stretches]
        usable = [c for c in centres if np.sum(fk & (np.abs(full_t - c) < T14 / 2)) >= 0.9 * T14 / (2 / 1440)][:6]
        tk, fk_f = t[k], f[k]
        for c in usable:
            cov = int(np.sum(np.abs(tk - c) < T14 / 2)); need = 0.9 * T14 / (2 / 1440)
            arm["restored_injection"].append(dict(t0=c, coverage_cadences=cov, searched=bool(cov >= need), trials=inject_trials(tk, fk_f, (6, 8), [c]) if cov >= need else []))
        print(name, "injections done", flush=True)
    return arm


def summarise(res_a0, a1, a2, trials_a0, times):
    L = ["# Quality-mask experiment: results summary", "", "*Generated by qmask.py. Read SPEC.md for what each number can and cannot mean.*", ""]
    a0r = {r["sector"]: r for r in res_a0["recovery"]}
    L += ["## 1. Known transits (event within +-0.3 d of the published time, SNR bar 7)", "",
          "| Sector | cadences within +-3 h: A0 kept / A1 kept / A2 kept (A2 restored) | A0 | A1 | A2 |", "|---|---|---|---|---|"]
    for i, s in enumerate(SECTORS):
        x1, x2 = a1["sectors"][i], a2["sectors"][i]; r0 = a0r[s]
        fmt = lambda x: f"yes, SNR {x['hit']['snr']}, restored share {x['hit']['restored_frac']}" if x["recovered"] else "no"
        L.append(f"| {s}{' (prediction)' if s == 30 else ''} | {r0['kept_near_transit']} / {x1['window_kept']} / {x2['window_kept']} ({x2['window_restored']}) | "
                 f"{'yes, SNR %.2f' % r0['snr'] if r0['recovered'] else 'no'} | {fmt(x1)} | {fmt(x2)} |")
    if trials_a0:
        L += ["", "## 2. Injections in S98 (baseline's retained times; paired per trial)", "",
              "| size R_earth | time | A0 rec/SNR | A1 rec/SNR | A2 rec/SNR | A0 depth ratio | A1 | A2 |", "|---|---|---|---|---|---|---|---|"]
        g = lambda arm, sz, t0: next((x for x in arm["injection"] if x["size"] == sz and x["t0"] == t0), None)
        def c(x): return "n/a" if x is None else (f"yes {x['snr']:.1f}" if x["recovered"] else "no")
        def d(x): return "" if x is None or not x["recovered"] else f"{x['depth_ppm'] / x['centre_depth_ppm']:.2f}"
        for sz in (5, 6, 7):
            for t0 in times:
                x0 = next(x for x in trials_a0 if x["size"] == sz and x["t0"] == t0); x1, x2 = g(a1, sz, t0), g(a2, sz, t0)
                L.append(f"| {sz} | {t0} | {c(x0)} | {c(x1)} | {c(x2)} | {d(x0)} | {d(x1)} | {d(x2)} |")
        both = [(g(a1, sz, t0), g(a2, sz, t0)) for sz in (5, 6, 7) for t0 in times if g(a1, sz, t0) and g(a2, sz, t0) and g(a1, sz, t0)["recovered"] and g(a2, sz, t0)["recovered"]]
        if both:
            dd = [y["snr"] - x["snr"] for x, y in both]; L.append(f"\nTrials recovered in both A1 and A2: {len(both)}. SNR change A1 to A2: median {np.median(dd):+.2f}, range {min(dd):+.2f} to {max(dd):+.2f}.")
        disc = [(sz, t0) for sz in (5, 6, 7) for t0 in times if g(a1, sz, t0) and g(a2, sz, t0) and g(a1, sz, t0)["recovered"] != g(a2, sz, t0)["recovered"]]
        L.append(f"Discordant trials (recovered in only one of A1, A2): {disc if disc else 'none'}.")
        L += ["", "### Exploratory: injections inside restored stretches of S98", "", "| arm | centre | window cadences | searched | 6 R_earth | 8 R_earth |", "|---|---|---|---|---|---|"]
        for arm in (a1, a2):
            for r in arm["restored_injection"]:
                cell = lambda sz: next((f"yes {x['snr']:.1f}, depth ratio {x['depth_ppm'] / x['centre_depth_ppm']:.2f}" if x["recovered"] else "no" for x in r["trials"] if x["size"] == sz), "-")
                L.append(f"| {arm['name']} | {r['t0']} | {r['coverage_cadences']} | {r['searched']} | {cell(6)} | {cell(8)} |")
    L += ["", "## 3. Flipped-data events (SNR >= 7), all sectors", "", "| arm | events | retained exposure (d) | rate per 100 d (95% interval) |", "|---|---|---|---|"]
    fa0 = sum(r["n"] for r in res_a0["false_alarms"])
    L.append(f"| A0 (baseline, reproduced) | {fa0} | n/a | n/a |")
    for arm in (a1, a2):
        ev = [e for s in arm["sectors"] for e in s["flipped"]]; dr = sum(s["exposure_retained_days"] for s in arm["sectors"]); dx = sum(s["exposure_restored_days"] for s in arm["sectors"])
        p_all = pois(len(ev), dr + dx); L.append(f"| {arm['name']} all | {p_all['events']} | {p_all['exposure_days']} | {p_all['per100d']} ({p_all['lo95']} to {p_all['hi95']}) |")
        if dx:
            w = [e for e in ev if e["restored_frac"]]; wo = [e for e in ev if not e["restored_frac"]]
            pw, po = pois(len(w), dx), pois(len(wo), dr)
            L.append(f"| {arm['name']} events containing restored cadences (per 100 d of restored exposure) | {pw['events']} | {pw['exposure_days']} | {pw['per100d']} ({pw['lo95']} to {pw['hi95']}) |")
            L.append(f"| {arm['name']} events without restored cadences (per 100 d of retained exposure) | {po['events']} | {po['exposure_days']} | {po['per100d']} ({po['lo95']} to {po['hi95']}) |")
            adverse = pw["per100d"] is not None and po["per100d"] is not None and pw["per100d"] > po["per100d"] and pw["lo95"] > po["hi95"]
            L.append(f"\nPre-registered adverse rule (restored rate above retained rate with non-overlapping 95% intervals): **{'ADVERSE' if adverse else 'not triggered; inconclusive at this sample size'}**.")
    L += ["", "## 4. Restored cadences (A2)", "", "| sector | restored kept | retained kept | scatter ppm retained / restored (2-min, flattened) | background restored / retained |", "|---|---|---|---|---|"]
    for s in a2["sectors"]:
        L.append(f"| {s['sector']} | {s['restored_kept']} | {s['kept'] - s['restored_kept']} | {s['scatter_ppm_retained']:.0f} / " +
                 (f"{s['scatter_ppm_restored']:.0f}" if s["scatter_ppm_restored"] else "-") + f" | {s['bkg_restored_over_retained']:.2f} |" if s["bkg_restored_over_retained"] else f"| {s['sector']} | 0 | {s['kept']} | - | - |")
    z = [(x1["hit"]["snr"], x2["hit"]["snr"], s) for s, x1, x2 in zip(SECTORS, a1["sectors"], a2["sectors"]) if x1["recovered"] and x2["recovered"] and not x2["hit"]["restored_frac"]]
    if z:
        L += ["", "Known transits recovered in A1 and A2 whose box has no restored cadences (pure effect of added data elsewhere): " + "; ".join(f"S{s}: {a:.2f} to {b:.2f}" for a, b, s in z)]
    return "\n".join(L) + "\n"


def main():
    paths = {s: fits_path(s) for s in SECTORS}
    man = manifest(paths)
    if "--check" in sys.argv:
        print(json.dumps({k: v for k, v in man.items() if k != "inputs"}, indent=1, default=str)); print(len(man["inputs"]), "input files hashed"); return
    assert "--run" in sys.argv, "use --check or --run"
    out = Out(); out.write("manifest.json", json.dumps(man, indent=1, default=str)); print("results folder:", out.d, flush=True)
    res0, T1s, times, trials0 = run_a0(paths)
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    mine = json.loads(json.dumps(res0, default=float))
    expect = dict(recovery=[r for r in base["recovery"] if r["sector"] in SECTORS], false_alarms=[r for r in base["false_alarms"] if r["sector"] in SECTORS])
    got = dict(recovery=mine["recovery"], false_alarms=mine["false_alarms"])
    if 98 in SECTORS:
        expect.update(injection=base["injection"], injection_base_events=base["injection_base_events"]); got.update(injection=mine["injection"], injection_base_events=mine["injection_base_events"])
    bad = same(got, expect)
    out.write("a0_reproduction.json", json.dumps(dict(match=not bad, mismatches=bad, a0=mine), indent=1, default=float))
    if bad:
        print("REPRODUCTION GATE FAILED:", len(bad), "mismatches; first:", bad[:5]); sys.exit(2)
    print("A0 reproduces the frozen baseline: all fields match", flush=True)
    a1 = run_arm("A1 SAP+HARD", "hard", paths, T1s, times); a2 = run_arm("A2 SAP+DEFAULT", "default", paths, T1s, times)
    out.write("arms.json", json.dumps(dict(T1=T1s, injection_times=times, a0_trials=trials0, A1=a1, A2=a2), indent=1, default=float))
    out.write("summary.md", summarise(res0, a1, a2, trials0, times)); print("done:", out.d)


if __name__ == "__main__":
    main()
