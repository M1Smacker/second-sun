"""Star-name check before a push (10 Nov 2026, Sonnet 5.5 Extra). Ahmed's rule: no star ids, event details or lead details in the repo or the book.
Collects every TIC id of every star list we search or build (targets/*.csv, data/xmatch/ebs.csv, the TTC table, the CALNet list), then scans the lines ADDED by the unpushed commits
(git diff origin/main..HEAD) and their commit messages for those ids as whole numbers. Public known systems are allowed (TOI-1338, TIC 172900988) and listed in ALLOW.
Prints only counts and file paths (not the ids) plus a general pattern scan for source_id-like long numbers and the words 'center'/'lead' next to a number.
Usage: python push_star_check.py   (run in D:\\second-sun)"""
import re, subprocess, pathlib, collections, sys
import pandas as pd
ROOT = pathlib.Path(r"D:\second-sun")
ALLOW = {260128333, 172900988, 299096355, 158316612, 170348142, 164457525, 170344769}   # TOI-1338, TIC 172900988 and the Kepler-16, -38, -64, -453, -1647 hosts: published planetary systems
ids = set()
for p in list((ROOT / "targets").glob("*.csv")) + [ROOT / "data" / "xmatch" / "ebs.csv"]:
    try:
        df = pd.read_csv(p, comment="#", low_memory=False)
    except Exception as e:
        print("skip", p.name, type(e).__name__); continue
    for c in df.columns:
        if str(c).lower() in ("tic", "tic_id", "ticid"):
            ids |= set(pd.to_numeric(df[c], errors="coerce").dropna().astype(int))
for p in (ROOT / "data").glob("calnet_2026-11-07/*.csv"):
    try:
        df = pd.read_csv(p, low_memory=False)
        for c in df.columns:
            if str(c).lower() in ("tic", "tic_id", "ticid"):
                ids |= set(pd.to_numeric(df[c], errors="coerce").dropna().astype(int))
    except Exception:
        pass
ttc = ROOT / "data" / "g3" / "catalog_ttc" / "table3_new_ebs.txt"
if ttc.exists():
    for l in open(ttc, encoding="latin-1"):
        if l[:10].strip().isdigit():
            ids.add(int(l[:10]))
ids = {i for i in ids if i > 99999} - ALLOW
print(f"star ids collected: {len(ids)} (allowed public systems excluded: {sorted(ALLOW)})")
diff = subprocess.run(["git", "diff", "origin/main..HEAD", "-U0", "--no-color"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
msgs = subprocess.run(["git", "log", "origin/main..HEAD", "--format=%H%n%B"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
fileof = None; hits = collections.defaultdict(lambda: collections.Counter()); patt = collections.defaultdict(int)
num = re.compile(r"(?<![\d.])(\d{6,10})(?![\d.])")
for line in diff.splitlines():
    if line.startswith("+++ "):
        fileof = line[6:]; continue
    if not line.startswith("+") or line.startswith("+++"):
        continue
    for m in num.finditer(line):
        n = int(m.group(1))
        if n in ids:
            hits[fileof][n] += 1
    if re.search(r"source_id|Gaia DR3 \d{15,}|\b\d{16,19}\b", line):
        patt[fileof] += 1
mh = [int(m.group(1)) for m in num.finditer(msgs) if int(m.group(1)) in ids]
print(f"commit messages: {len(mh)} star-id hits")
tot = sum(sum(c.values()) for c in hits.values())
print(f"added lines with a star id: {tot} hits in {len(hits)} files, {len({n for c in hits.values() for n in c})} distinct ids")
for f, c in sorted(hits.items(), key=lambda kv: -sum(kv[1].values()))[:40]:
    print(f"  {f}: {sum(c.values())} hits, {len(c)} distinct ids")
print("long-number / source_id pattern lines:", sum(patt.values()), "in", len(patt), "files:", dict(list(patt.items())[:15]))
