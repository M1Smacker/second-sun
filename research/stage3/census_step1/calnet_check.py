import re, csv, pathlib, urllib.request, hashlib, json
url = "https://raw.githubusercontent.com/wangleon/CALNet/main/outputs/newecl.dat"
out = pathlib.Path(r"D:\second-sun\data\calnet_2026-11-07"); out.mkdir(parents=True, exist_ok=True)
f = out / "newecl.dat"
if not f.exists():
    urllib.request.urlretrieve(url, f)
b = f.read_bytes()
print("bytes", len(b), "sha256", hashlib.sha256(b).hexdigest()[:16])
lines = b.decode("utf-8", "replace").splitlines()
print("header lines:"); [print("  ", l[:200]) for l in lines[:3]]
hdr, dash = lines[0], lines[1]
spans = [(m.start(), m.end()) for m in re.finditer(r"-+", dash)]
names = [hdr[a:b].strip() for a, b in spans]
rows = [[l[a:b].strip() for a, b in spans] for l in lines[2:] if l.strip()]
class T(dict): pass
t = T({n: [r[i] for r in rows] for i, n in enumerate(names)})
print("rows", len(rows), "cols", names)
tic = list(t["TIC"])
print("unique TIC", len(set(tic)))
g = t["Gmag"]
import statistics, math
gm = [float(x) if x not in ("", "--") else float("nan") for x in g]
ok = [x for x in gm if not math.isnan(x)]
print("median G", statistics.median(ok), "G<12", sum(x < 12 for x in ok), "G<13.5", sum(x < 13.5 for x in ok), "G missing", len(gm) - len(ok))
gaia = [str(x).strip() for x in t["Gaia"]]
print("Gaia id non-empty", sum(1 for x in gaia if x not in ("", "--", "0")), "sample", gaia[:3])
print("Disp column values:", sorted(set(str(x) for x in t["Disp"]))[:10], "m_TIC:", sorted(set(str(x) for x in t["m_TIC"]))[:6])
seen = set(); tics = set(tic)
for name in ("g1_targets.csv", "g2_targets.csv", "g3_targets.csv"):
    rs = list(csv.DictReader(l for l in open(rf"D:\second-sun\targets\{name}", encoding="utf-8") if not l.startswith("#")))
    s = {r["tic"].strip() for r in rs}; seen |= s
    print(name, "stars", len(s), "in CALNet", len(s & tics))
print("CALNet stars never searched by G1 to G3:", len(tics - seen))
json.dump({"gaia": gaia, "tic": tic, "g": [None if math.isnan(x) else x for x in gm]}, open(out / "parsed.json", "w"))
