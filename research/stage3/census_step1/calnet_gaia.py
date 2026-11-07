import json, csv, io, urllib.request, urllib.parse, time, collections, statistics, math, pathlib
out = pathlib.Path(r"D:\second-sun\data\calnet_2026-11-07")
d = json.load(open(out / "parsed.json"))
# Disp categories
lines = (out / "newecl.dat").read_text(encoding="utf-8", errors="replace").splitlines()
hdr, dash = lines[0], lines[1]
import re
spans = [(m.start(), m.end()) for m in re.finditer(r"-+", dash)]
names = [hdr[a:b].strip() for a, b in spans]
rows = [{n: l[a:b].strip() for n, (a, b) in zip(names, spans)} for l in lines[2:] if l.strip()]
print("Disp counts:", collections.Counter(r["Disp"] for r in rows))
print("m_TIC non-empty:", sum(1 for r in rows if r["m_TIC"]))
ids = [r["Gaia"] for r in rows if r["Gaia"] not in ("", "0")]
ids = sorted(set(ids))
print("distinct Gaia ids", len(ids))
URL = "https://gea.esac.esa.int/tap-server/tap/sync"
cols = "source_id, frequency, model_type, derived_primary_ecl_depth, derived_primary_ecl_duration"
res = []
t0 = time.time()
for i in range(0, len(ids), 400):
    chunk = ids[i:i + 400]
    q = f"SELECT {cols} FROM gaiadr3.vari_eclipsing_binary WHERE source_id IN ({','.join(chunk)})"
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": q}).encode()
    for attempt in range(3):
        try:
            txt = urllib.request.urlopen(urllib.request.Request(URL, data=data), timeout=120).read().decode()
            break
        except Exception as e:
            print("retry", i, repr(e)[:150]); time.sleep(5); txt = None
    if txt is None:
        print("FAILED chunk", i); continue
    if i == 0 and not txt.startswith("source_id"):
        print("unexpected reply:", txt[:300]); break
    rd = list(csv.DictReader(io.StringIO(txt)))
    res += rd
    print("chunk", i // 400, "rows", len(rd), f"{time.time()-t0:.0f}s")
with open(out / "gaia_dr3_vari_eb_for_calnet.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["source_id", "frequency", "model_type", "derived_primary_ecl_depth", "derived_primary_ecl_duration"]); w.writeheader(); w.writerows(res)
print("Gaia DR3 vari_eclipsing_binary matches", len(res), "of", len(ids))
by = {r["source_id"]: r for r in res}
gm = {r["Gaia"]: (float(r["Gmag"]) if r["Gmag"] not in ("", "--") else None) for r in rows}
P = []
for sid, r in by.items():
    try:
        fr = float(r["frequency"]); P.append((1 / fr, sid))
    except (ValueError, ZeroDivisionError): pass
print("with a period", len(P))
for lo, hi in ((0, 1), (1, 3), (3, 5), (5, 7), (7, 15), (15, 40), (40, 1e9)):
    n = sum(1 for p, s in P if lo <= p < hi); nb = sum(1 for p, s in P if lo <= p < hi and gm.get(s) is not None and gm[s] < 13.5)
    print(f"  P {lo}-{hi} d: {n} (G<13.5: {nb})")
long7 = [s for p, s in P if p >= 7]
print("P>=7 d:", len(long7), " and G<13.5:", sum(1 for s in long7 if gm.get(s) is not None and gm[s] < 13.5))
print("model types among P>=7:", collections.Counter(by[s]["model_type"] for s in long7).most_common(6))
