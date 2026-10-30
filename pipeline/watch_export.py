"""Search window: turns a Stage 3 run folder into one small JSON of AGGREGATES for the book page `watch.md`. It reads the group files the search is writing (groups, groups_sap) and never plots or lists a
real event. With --blind (the sealed run) real and upside-down events are POOLED everywhere, so nobody sees the real-versus-control result before the preregistered analysis; the ticker shows a star-sector
only as finished with a pooled event count. Without --blind (development runs) the split is shown.
Usage: python watch_export.py RUN_FOLDER [--blind] [--label TEXT] [--out PATH] [--loop SECONDS] [--push]
       python watch_export.py --note "what is happening now"      (adds a dated line to the page's activity log; works without a run)
--push publishes the JSON to the data branch `watch-data` (a separate branch of the repository, never main) through a scratch clone in D:\\ss-watch-data; the book page reads it from GitHub, so the page
updates by itself, with no new book publish. RUN_FOLDER is e.g. ..\\data\\stage3_g2\\dev_73f62615e365. Totals come from the star list (S2.groups), cached in watch_plan.json."""
import sys, os, json, glob, time, pathlib, subprocess, datetime, argparse, shutil
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "book" / "docs" / "assets" / "data" / "watch.json"
NOTES = ROOT / "data" / "watch_notes.json"
SCRATCH = pathlib.Path(r"D:\ss-watch-data")
REPO = "https://github.com/M1Smacker/second-sun.git"
FLAGS = [("gap_dump", "Near a data gap or a spacecraft momentum dump"), ("flipmatch", "The upside-down copy has the same wiggle"), ("c5", "Sits at a catalogue eclipse phase"),
         ("ecl_overlap", "Overlaps a predicted eclipse"), ("repeater", "Many similar dips in the same light curve"), ("step", "The baseline jumps across the dip"),
         ("ramp", "Sits on a slow ramp after data resumes"), ("dominated", "A stronger event of the other kind in the same curve")]
BANDS = [(7, 8, "7 to 8"), (8, 10, "8 to 10"), (10, 12, "10 to 12"), (12, 1e9, "12 and up")]
CACHE = {}


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def summarise(path):
    g = json.load(open(path))
    ev = g["events"]; first = Counter(); tiers = Counter(); kinds = Counter(); boxes = Counter(); bands = Counter()
    for e in ev:
        kinds[e["kind"]] += 1; tiers[e.get("tier", "?")] += 1; boxes[str(e["dur_h"])] += 1
        bands[next(l for lo, hi, l in BANDS if lo <= e["snr"] < hi)] += 1
        first[next((k for k, _ in FLAGS if e.get(k)), "clean")] += 1
    inj = g.get("inj") or []
    meta = g["meta"]
    evs = [dict(kind=e["kind"], product=e["product"], center=e["center"], dur_h=e["dur_h"], snr=e["snr"], depth_ppm=e["depth_ppm"], tier=e.get("tier", "?"),
                flags=[k for k, _ in FLAGS if e.get(k)]) for e in ev]
    return dict(tic=g["tic"], sector=g["sector"], mtime=os.path.getmtime(path), n=len(ev), evs=evs, files={m["product"]: m["file"] for m in meta if m["status"] == "ok"}, kinds=dict(kinds), first=dict(first), tiers=dict(tiers), boxes=dict(boxes), bands=dict(bands),
                files_ok=sum(m["status"] == "ok" for m in meta), files_bad=Counter(m["status"] for m in meta if m["status"] != "ok"),
                products=sorted({m["product"] for m in meta if m["status"] == "ok"}),
                inj_n=len(inj), inj_second=sum(1 for i in inj if (i.get("snr_B") or 0) >= 4), pdc=g.get("pdc_check") == "v7u")


def scan(folder):
    out = {}
    for p in glob.glob(str(folder / "*.json")):
        m = os.path.getmtime(p)
        c = CACHE.get(p)
        if c is None or c["mtime"] < m:
            try:
                c = CACHE[p] = summarise(p)
            except Exception:       # a file being written right now: try again next round
                continue
        out[p] = c
    return out


def totals(run):
    f = run / "watch_plan.json"
    if f.exists():
        return json.load(open(f))
    sys.path.insert(0, str(HERE))
    import stage3 as S3, stage2_search as S2
    S2.STARS = S3.PREP / "g2_dev_stars_LOCAL.csv" if (S3.PREP / "g2_dev_stars_LOCAL.csv").exists() else S3.STARS_ALL
    gl = S2.groups()
    plan = dict(groups=len(gl), sap=len(S3.sap_pass_groups(gl)), stars=len({g[0] for g in gl}))
    json.dump(plan, open(f, "w"))
    return plan


def machine():
    """Python workers of the Second Sun scripts and the whole-machine CPU load (Windows; None if it cannot be read)."""
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "$p=@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match 'stage3|stage2|sealed_run|spawn_main|paired_recovery|chain_recovery|audit_all' -and $_.CommandLine -notmatch 'watch_export' }).Count;"
                            "$c=(Get-CimInstance Win32_Processor | Measure-Object LoadPercentage -Average).Average; \"$p $c\""], capture_output=True, text=True, timeout=40)
        w, c = r.stdout.split()[:2]
        return dict(workers=int(w), cpu=int(float(c)))
    except Exception:
        return dict(workers=None, cpu=None)


def run_info(run):
    info = dict(folder=run.name, version="Vesper 0.7.1 (development use)")
    s = {}
    if (run / "settings.json").exists():
        j = json.load(open(run / "settings.json")); s = j.get("settings", {}); info["hash"] = j.get("hash")
        info["git_commit"] = (j.get("provenance") or {}).get("git_commit", "")[:7]
        if s.get("options") == ["c6"]:
            info["version"] = "Vesper 0.8.0 (frozen)"
    info["settings"] = dict(snr_bar=s.get("snr_threshold"), boxes_h=s.get("durs_h"), bin_days=s.get("bin_d"), options=s.get("options"),
                            flags=dict(common_stars=s.get("v7", {}).get("common_n"), step_lift=s.get("step_lift"), ramp_days=s.get("ramp_d"), repeat_n=s.get("repeat_n")))
    return info


def history(run, done, nev, per_min):
    f = run / "watch_history.json"
    h = json.load(open(f)) if f.exists() else []
    t = time.time()
    if not h or t - h[-1]["t"] >= 50:
        h.append(dict(t=round(t), done=done, events=nev, per_min=per_min)); h = h[-400:]
        json.dump(h, open(f, "w"))
    return h


def notes():
    return json.load(open(NOTES)) if NOTES.exists() else []


def add_note(text):
    n = notes(); n.append(dict(at=now_iso(), text=text)); NOTES.parent.mkdir(exist_ok=True); json.dump(n[-30:], open(NOTES, "w"), indent=1)


WHAT = {"gap_dump": "Right next to a data gap or a momentum dump. The dashed lines mark gaps. The instrument is settling there, so the dip is probably not the star.",
        "flipmatch": "The upside-down copy of this star has a matching wiggle at the same time, so this is not a one-way dip.",
        "c5": "It falls where one of the binary's own eclipses should be.",
        "ecl_overlap": "It overlaps an eclipse of the binary.",
        "repeater": "This light curve has many similar dips, so it is probably another eclipsing pair in the same pixels.",
        "step": "The brightness level is different before and after, so it is a step, not a dip that comes back.",
        "ramp": "Slow ramp just after data resumes, a known instrument effect.",
        "dominated": "A stronger event of the opposite kind sits in the same light curve.",
        "clean": "No safety check fired here."}
GAL = {}


def card(tic, sec, e, blind, mtime):
    """One picture: the star's own binned light 36 h either side of the event, in ppm from its median. An upside-down event is drawn from the flipped curve, so every picture shows a dip."""
    import numpy as np
    import dataset as DS, stage2_search as S2
    if "init" not in GAL:
        S2._init(); GAL["init"] = 1
    f = DS.DATA / str(tic) / GAL["files"][(tic, sec)][e["product"]]
    d, _ = S2.prepare(f)
    if d is None:
        return None
    P = S2.Prod(d["t"], d["f"], 1 if e["kind"] == "real" else -1)
    x = (P.bt - e["center"]) * 24; k = np.abs(x) <= 36
    if k.sum() < 20:
        return None
    y = (P.bf[k] / P.med - 1) * 1e6; ok = np.isfinite(y)
    gaps = [round(float((g - e["center"]) * 24), 1) for g in d["edges"] if abs(g - e["center"]) * 24 <= 36]
    first = next((f_ for f_ in e["flags"]), "clean")
    c = dict(tic=tic, sector=sec, product=e["product"], tier=e["tier"], snr=round(e["snr"], 1), depth=round(e["depth_ppm"]), dur=e["dur_h"], flags=e["flags"], first=first, what=WHAT[first],
             at=datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc).strftime("%H:%M"), x=[round(float(v), 1) for v in x[k][ok]], y=[int(round(v)) for v in y[ok]], gaps=gaps)
    if not blind:
        c["kind"] = e["kind"]
    return c


def gallery(run, A, blind, per_loop=3):
    """Keeps the last 8 kept (tier 1) and the last 8 stopped events as pictures; new ones come from the groups finished since the last call. Persisted in the run folder."""
    f = run / "watch_gallery.json"
    st = json.load(open(f)) if f.exists() else dict(last=0, kept=[], stopped=[])
    new = sorted([r for r in A.values() if r["mtime"] > st["last"]], key=lambda r: -r["mtime"])[:30]
    if new:
        st["last"] = max(r["mtime"] for r in new)
        GAL["files"] = {(r["tic"], r["sector"]): r["files"] for r in A.values()}
        pool = [(r, e) for r in new for e in r["evs"] if "SAP" not in e["product"]]
        kept = [x for x in pool if x[1]["tier"] in ("1A", "1L", "1B")][:per_loop]
        stopped = sorted([x for x in pool if x not in kept], key=lambda x: -x[1]["snr"])[:per_loop]
        for key, picks in (("kept", kept), ("stopped", stopped)):
            for r, e in picks:
                try:
                    c = card(r["tic"], r["sector"], e, blind, r["mtime"])
                except Exception as ex:
                    print("gallery skip", r["tic"], r["sector"], type(ex).__name__, str(ex)[:80], flush=True); c = None
                if c:
                    st[key] = ([c] + st[key])[:8]
        json.dump(st, open(f, "w"))
    return dict(kept=st["kept"], stopped=st["stopped"])


def build(run, blind, label, loop=0):
    run = pathlib.Path(run)
    plan = totals(run)
    A = scan(run / "groups"); B = scan(run / "groups_sap")
    now = time.time(); rows = sorted(A.values(), key=lambda r: r["mtime"])
    last10 = [r for r in rows if now - r["mtime"] < 600]
    rate = len(last10) / 10.0 if last10 else 0.0
    done, total = len(A), plan["groups"]
    pdc_done = sum(1 for r in B.values() if r["pdc"])
    ph = "search" if done < total else ("sap" if len(B) < plan["sap"] else ("pdc" if pdc_done < plan["sap"] else "finished"))
    first, tiers, kinds, boxes, bands = Counter(), Counter(), Counter(), Counter(), Counter(); files_ok = 0; bad = Counter(); inj_n = inj_s = 0; prods = Counter()
    for r in list(A.values()) + list(B.values()):
        first.update(r["first"]); tiers.update(r["tiers"]); kinds.update(r["kinds"]); boxes.update(r["boxes"]); bands.update(r["bands"]); files_ok += r["files_ok"]; bad.update(r["files_bad"])
        inj_n += r["inj_n"]; inj_s += r["inj_second"]
        for p in r["products"]:
            prods[p] += 1
    nev = sum(kinds.values())
    all_m = [r["mtime"] for r in list(A.values()) + list(B.values())]
    d = dict(label=label, blind=blind, phase=ph, updated=now_iso(), loop_s=loop, run=run_info(run), machine=machine(),
             started=datetime.datetime.fromtimestamp(min(all_m), datetime.timezone.utc).isoformat(timespec="seconds") if all_m else None,
             progress=dict(search=[done, total], sap=[len(B), plan["sap"]], pdc=[pdc_done, plan["sap"]], stars=plan["stars"], per_min=round(rate, 1),
                           eta_min=round((total - done) / rate) if rate and done < total else None),
             files=dict(read_ok=files_ok, skipped=dict(bad), products=dict(prods)),
             events=dict(found=nev, stopped_by=[dict(flag=k, text=t, n=first.get(k, 0)) for k, t in FLAGS] + [dict(flag="clean", text="No flag fired", n=first.get("clean", 0))],
                         tiers=dict(tiers), boxes={k: boxes[k] for k in sorted(boxes, key=float)}, bands={l: bands.get(l, 0) for _, _, l in BANDS}),
             selftest=dict(fakes=inj_n, second_product_sees=inj_s),
             history=history(run, done, nev, round(rate, 1)), notes=notes()[-8:][::-1], gallery=gallery(run, A, blind),
             ticker=[dict(tic=r["tic"], sector=r["sector"], events=r["n"], files=r["files_ok"], at=datetime.datetime.fromtimestamp(r["mtime"], datetime.timezone.utc).strftime("%H:%M:%S"))
                     for r in rows[-12:][::-1]])
    if not blind:
        d["events"]["by_kind"] = dict(kinds)
    return d


def write(d, out):
    out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp"); tmp.write_text(json.dumps(d, indent=1), encoding="utf-8"); tmp.replace(out)


def push_data(out):
    """Publish the JSON on the data branch `watch-data` (separate branch, normal fast-forward pushes, never main)."""
    g = lambda *a: subprocess.run(["git", "-C", str(SCRATCH), *a], capture_output=True, text=True)
    if not (SCRATCH / ".git").exists():
        SCRATCH.mkdir(parents=True, exist_ok=True); g("init", "-q"); g("remote", "add", "origin", REPO)
        g("fetch", "-q", "origin", "watch-data")
        if g("rev-parse", "--verify", "-q", "origin/watch-data").returncode == 0:
            g("checkout", "-q", "-B", "watch-data", "origin/watch-data")
        else:
            g("checkout", "-q", "--orphan", "watch-data")
    shutil.copy(out, SCRATCH / "watch.json")
    g("add", "watch.json"); g("commit", "-q", "-m", "watch: counts only", "-m", "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
    r = g("push", "-q", "origin", "HEAD:refs/heads/watch-data")
    if r.returncode:
        print("push failed:", r.stderr[:200], flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("run", nargs="?"); ap.add_argument("--blind", action="store_true"); ap.add_argument("--label", default="")
    ap.add_argument("--out", default=str(OUT)); ap.add_argument("--loop", type=int, default=0); ap.add_argument("--push", action="store_true"); ap.add_argument("--note")
    a = ap.parse_args()
    if a.note:
        add_note(a.note)
        if not a.run:
            sys.exit(0)
    while True:
        d = build(a.run, a.blind, a.label, a.loop); write(d, a.out)
        print(d["phase"], d["progress"]["search"], d["progress"]["sap"], d["progress"]["pdc"], d["machine"], flush=True)
        if a.push:
            push_data(a.out)
        if not a.loop or d["phase"] == "finished":
            break
        time.sleep(a.loop)
