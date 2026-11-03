"""G3 reference windows table (FIX-QUEUE item 70; Ahmed, 3 Nov 2026: "do what you think is right"). QLP-only star-sectors borrow good-time windows from other stars with SPOC 2-minute files on the same
sector, camera and CCD. With only the 612 G3 stars as the pool, 93% of the QLP groups would have no neighbour; with the union of the G3, G2 and G1 stars as the pool, 80% have two or more
(research/stage3/g3-window-feasibility-2026-11-02.txt). This script builds that pool ONCE, writes it as data/g3/audit/spoc_windows.pkl (the file audit_all.py reads for SS_SET=g3) and records its sha256, so the
rule is a fixed, hashed table and not "whatever the run's manifest holds". Windows are time stamps and quality flags only; no flux is searched.
Order: SS_SET=g3 python audit_all.py windows   (writes the G3-only pickle)  then  python g3_union_windows.py   (moves it to spoc_windows_g3only.pkl, writes the union, the sha256 file and prints counts).
Refuses to run twice (the union is never rebuilt silently)."""
import hashlib, pickle, pathlib, sys, json

ROOT = pathlib.Path(r"D:\second-sun")
OUT = ROOT / "data" / "g3" / "audit"
SRC = {"g1": ROOT / "research" / "audit-2026-10-23" / "spoc_windows.pkl", "g2": ROOT / "data" / "g2" / "audit" / "spoc_windows.pkl"}
G3_ONLY, UNION, REC = OUT / "spoc_windows_g3only.pkl", OUT / "spoc_windows.pkl", OUT / "spoc_windows_union.json"
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

if REC.exists():
    sys.exit(f"already built: {REC} (the union table is fixed; delete the record only with Ahmed's yes)")
if not G3_ONLY.exists():
    UNION.rename(G3_ONLY)                                   # the file audit_all.py windows just wrote (G3 SPOC files only)
pools = {"g3": pickle.load(open(G3_ONLY, "rb")), **{k: pickle.load(open(p, "rb")) for k, p in SRC.items()}}
union, seen = {}, {}
for name in ("g3", "g2", "g1"):
    for key, d in pools[name].items():
        for tic, w in d.items():
            assert tic not in seen or seen[tic] == name, f"TIC {tic} is in two pools ({seen[tic]} and {name})"
            seen[tic] = name
            union.setdefault(key, {})[tic] = w
union = {k: {t: union[k][t] for t in sorted(union[k])} for k in sorted(union)}   # sorted: the same bytes on every build
pickle.dump(union, open(UNION, "wb"), protocol=4)
rec = dict(built="3 Nov 2026", pools={k: dict(file=str(p if k != "g3" else G3_ONLY), sha256=sha(p if k != "g3" else G3_ONLY), groups=len(pools[k]), star_sector_windows=sum(len(v) for v in pools[k].values())) for k, p in {**SRC, "g3": G3_ONLY}.items()},
           union=dict(file=str(UNION), sha256=sha(UNION), groups=len(union), distinct_tics=len(seen), star_sector_windows=sum(len(v) for v in union.values()), groups_with_2_or_more=sum(len(v) >= 2 for v in union.values())))
REC.write_text(json.dumps(rec, indent=1), encoding="utf-8")
print(json.dumps(rec, indent=1))
