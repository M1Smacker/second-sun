"""The 'What the search found' section of the Search window. Rules: research/stage3/LEADS-RULES.md (written before any sealed result was read).
Called by watch_export.build(); it only reads the finished group summaries, it never changes a search result."""
import csv, json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEPT = ("1A", "1L", "1B")
SCORECARD = ROOT / "research" / "stage3" / "benchmark-g2-sealed.txt"
MAX_CARDS = 12
CHECKS = [("Passed every safety check of the search", "done"), ("A second light curve of the star agrees", "done"), ("Not a known TOI or known planet host", "done")]


def known_hosts():
    ids = set()
    for f, col in (("toi.csv", "tid"), ("cbp.csv", "tic_id")):
        p = ROOT / "data" / "xmatch" / f
        if p.exists():
            for r in csv.DictReader(open(p, encoding="utf-8")):
                v = "".join(ch for ch in str(r.get(col, "")) if ch.isdigit())
                if v:
                    ids.add(int(v))
    return ids


def sealed_locked(run):
    """A sealed run stays blind until the scorecard is filed."""
    return pathlib.Path(run).name.startswith("sealed_") and not SCORECARD.exists()


def verdict(finished, blind, n, real_conf, flip_conf):
    if not finished:
        return "Not finished. No verdict yet."
    if blind:
        return "Finished. Counts only until the scoring is filed."
    if n == 0:
        return "Finished: no leads. Nothing survived every check, so this run adds to the null."
    s = "1 lead" if n == 1 else f"{n} leads"
    if real_conf > flip_conf:
        return f"Finished: {s} for 2 or 3 more checks."
    return f"Finished: {s}, but real dips do not outnumber the upside-down copies, so treat them as noise until a check says otherwise."


def final_rows(run, A):
    """The events the scorecard scores: the finished run after the union and the v7 flags, best product per star-sector, the PDCSAP half (the half with a fair control)."""
    st = json.load(open(pathlib.Path(run) / "settings.json")).get("settings", {})
    if st.get("options"):
        os.environ["VESPER_OPTS"] = ",".join(st["options"])
    import stage3_report as R
    ev, _ = R.load(str(pathlib.Path(run) / "groups"))
    rm = {(r["tic"], r["sector"]): r for r in A.values()}
    return [(rm.get((int(x.tic), int(x.sector)), dict(tic=int(x.tic), sector=int(x.sector), mtime=0)),
             dict(kind=x.kind, product=x.product, center=float(x.center), dur_h=float(x.dur_h), snr=float(x.snr), depth_ppm=float(x.depth_ppm), tier=x.tier, flags=list(x.flags)))
            for x in R.pdc_half(ev[ev.primary]).itertuples()]


def build(run, A, B, finished, blind, card, GAL, known=None, rows=None):
    blind = blind or sealed_locked(run)
    known = known_hosts() if known is None else known
    final = bool(finished)
    if rows is None:
        rows = final_rows(run, A) if final else [(r, e) for r in list(A.values()) + list(B.values()) for e in r["evs"]]

    def count(pred):
        """Finished run: events, exactly as the scorecard counts them. Running: star-sectors with at least one event of each kind (one dip seen in three products counts once)."""
        s = {"real": set(), "flip": set()}
        for r, e in rows:
            if pred(e):
                s[e["kind"]].add((r["tic"], r["sector"], e["product"], round(e["center"], 4)) if final else (r["tic"], r["sector"]))
        return {k: len(v) for k, v in s.items()}

    def pick(kind):
        """One lead per star: its strongest Confirmed event; n = how many distinct Confirmed dips (sector, day) the star has."""
        by = {}
        for r, e in rows:
            if e["kind"] == kind and e["tier"] == "1A":
                by.setdefault(r["tic"], []).append((r, e))
        out = [max(v, key=lambda x: x[1]["snr"]) + (len({(r["sector"], round(e["center"])) for r, e in v}),) for t, v in by.items() if t not in known]
        return sorted(out, key=lambda x: -x[1]["snr"]), sum(1 for t in by if t in known)

    leads, kn = pick("real"); flips, _ = pick("flip")
    ev, kept, conf = count(lambda e: True), count(lambda e: e["tier"] in KEPT), count(lambda e: e["tier"] == "1A")
    stages = []
    for label, c, lead_n in (("Dips found (signal-to-noise 7 or more)", ev, None), ("Kept: no safety check fired", kept, None),
                             ("Confirmed: a second light curve agrees", conf, None), ("Leads: stars with a confirmed real dip, no known planet", None, (len(leads), len(flips)))):
        real, flip = (c["real"], c["flip"]) if c else lead_n
        stages.append(dict(label=label, both=real + flip) if blind else dict(label=label, both=real + flip, real=real, flip=flip))
    out = dict(schema=1, blind=blind, final=final, verdict=verdict(finished, blind, len(leads), conf["real"], conf["flip"]), stages=stages, known=None if blind else kn, cards=[])
    if blind:
        return out
    if SCORECARD.exists() and pathlib.Path(run).name.startswith("sealed_"):
        out["scored"] = next((l.split("[rule")[0].replace("VERDICT S1:", "Scored result (S1):").strip() for l in open(SCORECARD, encoding="utf-8") if "VERDICT S1" in l), None)
    kept_sec = {}
    for r, e in rows:
        if e["kind"] == "real" and e["tier"] in KEPT:
            kept_sec.setdefault(r["tic"], set()).add(r["sector"])
    keys = [[r["tic"], r["sector"], round(e["center"], 3), e["product"]] for r, e, _ in leads[:MAX_CARDS]]
    cf = pathlib.Path(run) / "watch_leads.json"
    old = json.load(open(cf)) if cf.exists() else {}
    if old.get("keys") == keys:
        out["cards"] = old["cards"]
        return out
    GAL["files"] = {}
    for r in list(A.values()) + list(B.values()):
        GAL["files"].setdefault((r["tic"], r["sector"]), {}).update(r["files"])
    for i, (r, e, n) in enumerate(leads[:MAX_CARDS], 1):
        try:
            c = card(r["tic"], r["sector"], e, False, r["mtime"])
        except Exception as ex:
            print("lead picture skipped", r["tic"], r["sector"], type(ex).__name__, str(ex)[:80], flush=True); c = None
        c = c or dict(tic=r["tic"], sector=r["sector"], product=e["product"], tier=e["tier"], snr=round(e["snr"], 1), depth=round(e["depth_ppm"]), dur=e["dur_h"])
        others = sorted(kept_sec.get(r["tic"], set()) - {r["sector"]})
        c.update(id=f"L{i}", center=round(e["center"], 3), others=others, events=n,
                 checks=[dict(t=t, s=s) for t, s in CHECKS] + [dict(t=("Kept events in another sector of this star: " + ", ".join(map(str, others))) if others else "Seen in another sector: no, this star has no other kept sector in the run", s="info"),
                                                                dict(t="Looked at by eye (Ahmed)", s="pending"), dict(t="Pixel check: background and neighbouring stars (not built yet)", s="notbuilt")],
                 next="Look at the picture yourself and say what you see.")
        out["cards"].append(c)
    json.dump(dict(keys=keys, cards=out["cards"]), open(cf, "w"))
    return out
