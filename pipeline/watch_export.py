"""Search window: turns a Stage 3 run folder into one small JSON of AGGREGATES for the book page `watch.md`. It reads the group files the search is writing (groups, groups_sap) and never plots or lists a
real event. With --blind (the sealed run) real and upside-down events are POOLED everywhere, so nobody sees the real-versus-control result before the preregistered analysis; the ticker shows a star-sector
only as finished with a pooled event count. Without --blind (development runs) the split is shown.
Usage: python watch_export.py RUN_FOLDER [--blind] [--label TEXT] [--out PATH] [--loop SECONDS] [--push]
RUN_FOLDER is e.g. ..\\data\\stage3_g2\\dev_73f62615e365. Totals come from the star list in the run's settings (S2.groups); cached after the first call."""
import sys, os, json, glob, time, pathlib, subprocess, datetime, argparse
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "book" / "docs" / "assets" / "data" / "watch.json"
FLAGS = [("gap_dump", "Near a data gap or a spacecraft momentum dump"), ("flipmatch", "The upside-down copy has the same wiggle"), ("c5", "Sits at a catalogue eclipse phase"),
         ("ecl_overlap", "Overlaps a predicted eclipse"), ("repeater", "Many similar dips in the same light curve"), ("step", "The baseline jumps across the dip"),
         ("ramp", "Sits on a slow ramp after data resumes"), ("dominated", "A stronger event of the other kind in the same curve")]
CACHE = {}


def summarise(path):
    g = json.load(open(path))
    ev = g["events"]; first = Counter(); tiers = Counter(); kinds = Counter()
    for e in ev:
        kinds[e["kind"]] += 1; tiers[e.get("tier", "?")] += 1
        f = next((k for k, _ in FLAGS if e.get(k)), None)
        first[f or "clean"] += 1
    inj = g.get("inj") or []
    meta = g["meta"]
    return dict(tic=g["tic"], sector=g["sector"], mtime=os.path.getmtime(path), n=len(ev), kinds=dict(kinds), first=dict(first), tiers=dict(tiers),
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
    import pandas as pd
    S2.STARS = S3.PREP / "g2_dev_stars_LOCAL.csv" if (S3.PREP / "g2_dev_stars_LOCAL.csv").exists() else S3.STARS_ALL
    gl = S2.groups()
    plan = dict(groups=len(gl), sap=len(S3.sap_pass_groups(gl)), stars=len({g[0] for g in gl}))
    json.dump(plan, open(f, "w"))
    return plan


def build(run, blind, label):
    run = pathlib.Path(run)
    plan = totals(run)
    A = scan(run / "groups"); B = scan(run / "groups_sap")
    now = time.time(); rows = sorted(A.values(), key=lambda r: r["mtime"])
    last10 = [r for r in rows if now - r["mtime"] < 600]
    rate = len(last10) / 10.0 if last10 else 0.0
    done, total = len(A), plan["groups"]
    pdc_done = sum(1 for r in B.values() if r["pdc"])
    ph = "search" if done < total else ("sap" if len(B) < plan["sap"] else ("pdc" if pdc_done < plan["sap"] else "finished"))
    first, tiers, kinds = Counter(), Counter(), Counter(); files_ok = 0; bad = Counter(); inj_n = inj_s = 0; prods = Counter()
    for r in list(A.values()) + list(B.values()):
        first.update(r["first"]); tiers.update(r["tiers"]); kinds.update(r["kinds"]); files_ok += r["files_ok"]; bad.update(r["files_bad"]); inj_n += r["inj_n"]; inj_s += r["inj_second"]
        for p in r["products"]:
            prods[p] += 1
    nev = sum(kinds.values())
    d = dict(label=label, blind=blind, phase=ph, updated=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
             progress=dict(search=[done, total], sap=[len(B), plan["sap"]], pdc=[pdc_done, plan["sap"]], stars=plan["stars"], per_min=round(rate, 1),
                           eta_min=round((total - done) / rate) if rate and done < total else None),
             files=dict(read_ok=files_ok, skipped=dict(bad), products=dict(prods)),
             events=dict(found=nev, stopped_by=[dict(flag=k, text=t, n=first.get(k, 0)) for k, t in FLAGS] + [dict(flag="clean", text="No flag fired", n=first.get("clean", 0))],
                         tiers=dict(tiers)),
             selftest=dict(fakes=inj_n, second_product_sees=inj_s),
             ticker=[dict(tic=r["tic"], sector=r["sector"], events=r["n"], files=r["files_ok"], at=datetime.datetime.fromtimestamp(r["mtime"], datetime.timezone.utc).strftime("%H:%M:%S"))
                     for r in rows[-12:][::-1]])
    if not blind:
        d["events"]["by_kind"] = dict(kinds)
    return d


def write(d, out):
    out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp"); tmp.write_text(json.dumps(d, indent=1), encoding="utf-8"); tmp.replace(out)


def push():
    g = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    g("add", str(OUT)); g("commit", "-q", "-m", "watch: search window update (aggregates only)", "-m", "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"); g("push", "-q")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--blind", action="store_true"); ap.add_argument("--label", default="")
    ap.add_argument("--out", default=str(OUT)); ap.add_argument("--loop", type=int, default=0); ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    while True:
        d = build(a.run, a.blind, a.label); write(d, a.out)
        print(d["phase"], d["progress"]["search"], d["progress"]["sap"], d["progress"]["pdc"], flush=True)
        if a.push:
            push()
        if not a.loop or d["phase"] == "finished":
            break
        time.sleep(a.loop)
