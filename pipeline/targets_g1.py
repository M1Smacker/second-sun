"""Freeze the G1 target list with its provenance (overnight: "make the ~550 traceable").

Source chain (all logged in research/downloads.csv):
  1. Villanova Kepler EB Catalog, third revision (live site, last update 2019-08-08), 2,920 rows
     https://keplerebs.villanova.edu/?format=file_csv -> data/wave-1/villanova_kepler-ebs_live/keplerebs_live.csv
  2. KIC -> TIC match via the MAST TIC catalogue (query by KIC), done in wave 3:
     research/wave-3-pipeline/g1_tmag.csv (kic, tic, tmag, tic_rad, p_bin, morph, kmag)
Selection (G1, wave 3): detached (morphology < 0.5), binary period > 5 d, TESS magnitude <= 13.5.
Output: targets/g1_targets.csv with a provenance header (source checksums, selection, date).
"""
import csv, hashlib, pathlib, datetime

ROOT = pathlib.Path(r"D:\second-sun")
CAT = ROOT / "data" / "wave-1" / "villanova_kepler-ebs_live" / "keplerebs_live.csv"
MATCH = ROOT / "research" / "wave-3-pipeline" / "g1_tmag.csv"
OUT = ROOT / "targets" / "g1_targets.csv"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:16]

lines = [l for l in open(CAT, encoding="utf-8") if not l.startswith("##")]  # "##" = comment block, "#KIC,..." = header
# keyed by (KIC, period): 13 KICs appear twice with different periods (multi-signal systems)
cat = {(int(r["KIC"]), round(float(r["period"]), 6)): r for r in csv.DictReader([lines[0].lstrip("#")] + lines[1:]) if r["KIC"].strip().isdigit()}
rows = list(csv.DictReader(open(MATCH, encoding="utf-8")))
problems = {"no_tic": 0, "no_tmag": 0, "kic_not_in_catalogue": 0}
seen_tic, dup_tic = {}, []
sel = []
for r in rows:
    kic = int(r["kic"])
    key = (kic, round(float(r["p_bin"]), 6))
    if key not in cat:
        problems["kic_not_in_catalogue"] += 1; continue
    if not r["tic"] or r["tic"] in ("", "None", "nan"):
        problems["no_tic"] += 1; continue
    try:
        tmag = float(r["tmag"])
    except ValueError:
        problems["no_tmag"] += 1; continue
    if r["tic"] in seen_tic:
        dup_tic.append((r["tic"], seen_tic[r["tic"]], kic))
    seen_tic[r["tic"]] = kic
    if float(r["morph"]) < 0.5 and float(r["p_bin"]) > 5 and tmag <= 13.5:
        c = cat[key]
        sel.append(dict(kic=kic, tic=r["tic"], tmag=round(tmag, 3), p_bin_d=r["p_bin"], bjd0=c["bjd0"],
                        morph=r["morph"], tic_radius_rsun=r["tic_rad"]))
sel.sort(key=lambda x: x["tmag"])

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="") as f:
    f.write(f"# G1 targets, frozen {datetime.date.today().isoformat()} by pipeline/targets_g1.py\n")
    f.write(f"# source 1: {CAT.relative_to(ROOT)} sha256:{sha(CAT)} (Villanova Kepler EB Catalog rev 3, 2019-08-08)\n")
    f.write(f"# source 2: {MATCH.relative_to(ROOT)} sha256:{sha(MATCH)} (KIC->TIC via MAST TIC, wave 3)\n")
    f.write("# selection: morph < 0.5 and p_bin > 5 d and tmag <= 13.5; sorted by tmag\n")
    f.write(f"# rows: {len(sel)} = {len({x['kic'] for x in sel})} unique stars; a star with two binary periods has two rows\n")
    w = csv.DictWriter(f, fieldnames=list(sel[0].keys())); w.writeheader(); w.writerows(sel)

print(f"rows in match file {len(rows)}; catalogue {len(cat)}; problems {problems}; duplicate TICs {len(dup_tic)}")
print(f"selected {len(sel)} rows = {len({x['kic'] for x in sel})} unique stars -> {OUT}")
assert len(sel) == 552, "wave 3 (claim P6) counted 552; a different number means the inputs changed"
print("targets_g1 self-check passed (552, matches wave 3)")
if dup_tic:
    print("same star listed twice (two binary periods in the Kepler catalogue):", sorted({d[0] for d in dup_tic})[:13])
