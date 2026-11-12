"""Fence check: did Codex touch what it must not touch? (12 Nov 2026, Claude Opus 5.5)

Claude runs this before merging any Codex branch, and Ahmed can run it any time. It prints COUNTS ONLY (never a star id).

What it checks
  1. Codex's own session logs (C:\\Users\\hanzl\\.codex\\sessions\\**\\*.jsonl, newer than --since):
       a. any FENCE A star id (G1, 552 rows: never searched with Petrova, kept blind for the G1 re-search)
       b. any FENCE B star id (the 803 G2 and G3 rows unseen at the Petrova design; spent by Re-search 1 on 11 Nov 2026,
          kept as a hold-out for the next filter version)
       c. commands that run a real-light search or open events (search scripts, SS_SET=g1, look_event, stage2_look)
  2. Every local branch named astra/* against main: added lines that carry a fenced id or any id of our star lists,
     and any change to the 12 frozen (hashed) Petrova 1.0.0 code files.
  3. Files under D:\\second-sun\\data changed since --since OUTSIDE data\\astra (Codex may write only there).

Verdict: CLEAN, or NEEDS A LOOK (Claude opens the hits privately; nothing is merged until it is explained).
A hit is not proof of harm: a star id can appear because a catalogue file was printed. That is still a rule break
(counts only), so it is reported.

Usage: D:\\second-sun\\.venv\\Scripts\\python.exe research\\astra\\tools\\fence_check.py [--since 2026-11-12] [--sessions DIR]
       [--extra CSV_WITH_tic_COLUMN ...] [--no-data-scan]
"""
import argparse
import collections
import datetime
import json
import os
import re
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
FROZEN = ["stage2_search.py", "detect_v2.py", "audit_all.py", "audit_paths.py", "common_time.py", "stage3_core.py",
          "stage3.py", "sap_twin.py", "stage3_report.py", "dataset.py", "vopts.py", "petrova_mask.py"]
SEARCH_CMD = re.compile(r"(stage2_search|stage3_core|stage3\.py|sealed_run|r1_run\.py\s+run|r1_gate\.py\s+run|g3_run|"
                        r"look_event|stage2_look|SS_SET\s*=\s*['\"]?g1)", re.I)
NUM = re.compile(r"(?<![\d.])(\d{6,10})(?![\d.])")
ALLOW = {260128333, 172900988, 299096355, 158316612, 170348142, 164457525, 170344769}   # published systems (as push_star_check.py)


def fences(extra=()):
    d = pd.read_csv(ROOT / "targets" / "r1_targets.csv", comment="#")
    d["tic"] = d["tic"].astype("int64")
    a = set(d.loc[d["list"] == "g1", "tic"])
    b = set(d.loc[(d["list"].isin(["g2", "g3"])) & (d["design_seen"] == 0), "tic"]) - a
    for p in extra:
        x = pd.read_csv(p, comment="#")
        col = [c for c in x.columns if str(c).lower() in ("tic", "tic_id", "ticid")]
        if not col:
            raise SystemExit(f"--extra {p}: no tic column")
        a |= set(pd.to_numeric(x[col[0]], errors="coerce").dropna().astype("int64"))
    every = set()
    for p in (ROOT / "targets").glob("*.csv"):
        try:
            x = pd.read_csv(p, comment="#", low_memory=False)
        except Exception as e:
            print("skip list", p.name, type(e).__name__)
            continue
        for c in x.columns:
            if str(c).lower() in ("tic", "tic_id", "ticid"):
                every |= set(pd.to_numeric(x[c], errors="coerce").dropna().astype("int64"))
    return a - ALLOW, b - ALLOW, {i for i in every if i > 99999} - ALLOW


def scan_sessions(sdir, since, fa, fb):
    out = collections.Counter()
    files = [p for p in Path(sdir).rglob("*.jsonl") if datetime.datetime.fromtimestamp(p.stat().st_mtime) >= since] if Path(sdir).exists() else []
    out["session files scanned"] = len(files)
    if not Path(sdir).exists():
        print("NOTE: no Codex session folder at", sdir, "(nothing to scan; this is not a pass)")
    for p in files:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                ids = {int(m.group(1)) for m in NUM.finditer(line)}
                out["lines with a FENCE A id"] += bool(ids & fa)
                out["lines with a FENCE B id"] += bool(ids & fb)
                out["lines with a search or event-opening command"] += bool(SEARCH_CMD.search(line))
    return out


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def scan_branches(fa, fb, every):
    res = {}
    for br in [b.strip().lstrip("* ").strip() for b in git("branch", "--list", "astra/*").splitlines() if b.strip()]:
        c = collections.Counter()
        names = git("diff", "--name-only", f"main...{br}").split()
        c["frozen files changed"] = sum(Path(n).name in FROZEN and n.startswith("pipeline/") for n in names)
        c["files changed"] = len(names)
        for line in git("diff", "-U0", "--no-color", f"main...{br}").splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue
            ids = {int(m.group(1)) for m in NUM.finditer(line)}
            c["added lines with a FENCE A id"] += bool(ids & fa)
            c["added lines with a FENCE B id"] += bool(ids & fb)
            c["added lines with any list star id"] += bool(ids & every)
        msgs = git("log", "--format=%B", f"main..{br}")
        c["commit messages with any list star id"] = sum(int(m.group(1)) in every for m in NUM.finditer(msgs))
        res[br] = c
    return res


def scan_data(since):
    base = ROOT / "data"
    t0 = since.timestamp()
    c = collections.Counter()
    for dp, dn, fn in os.walk(base):
        rel = Path(dp).relative_to(base)
        if rel.parts[:1] == ("astra",):
            dn[:] = []
            continue
        for f in fn:
            try:
                if os.stat(os.path.join(dp, f)).st_mtime >= t0:
                    c[rel.parts[0] if rel.parts else "(data root)"] += 1
            except OSError:
                c["(unreadable)"] += 1
    return c


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=(datetime.date.today() - datetime.timedelta(days=7)).isoformat())
    ap.add_argument("--sessions", default=str(Path.home() / ".codex" / "sessions"))
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--no-data-scan", action="store_true")
    ap.add_argument("--no-branches", action="store_true")
    a = ap.parse_args(argv)
    since = datetime.datetime.fromisoformat(a.since)
    fa, fb, every = fences(a.extra)
    print(f"fence A ids: {len(fa)}; fence B ids: {len(fb)}; all list ids: {len(every)}; since {since:%Y-%m-%d %H:%M}")
    bad = 0
    s = scan_sessions(a.sessions, since, fa, fb)
    for k, v in s.items():
        print(f"  sessions: {k}: {v}")
    bad += s["lines with a FENCE A id"] + s["lines with a FENCE B id"] + s["lines with a search or event-opening command"]
    if not a.no_branches:
        br = scan_branches(fa, fb, every)
        print(f"  astra branches: {len(br)}")
        for name, c in br.items():
            print(f"  branch {name}: " + "; ".join(f"{k} {v}" for k, v in c.items()))
            bad += sum(v for k, v in c.items() if k != "files changed")
    if not a.no_data_scan:
        d = scan_data(since)
        print(f"  data files changed outside data\\astra: {sum(d.values())} " + (str(dict(d.most_common(8))) if d else ""))
        print("  (Claude's own runs also change data\\: compare with research/jobs.md before calling it a Codex write)")
    verdict = "CLEAN" if bad == 0 else "NEEDS A LOOK"
    print("VERDICT:", verdict)
    return verdict


if __name__ == "__main__":
    main()
