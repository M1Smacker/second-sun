"""RS-010 Q3 (night of 4 Nov 2026): Gaia DR3 eclipsing-binary candidates (Mowlavi et al. 2023, gaiadr3.vari_eclipsing_binary) that are bright and long-period.
Counts only through the public Gaia archive TAP service (read-only ADQL; the join is restricted to the long-period subset first). Output: a small table. Second attempt: the first (join over all 2.2 million rows) timed out."""
import urllib.request, urllib.parse, csv, io, time
URL = "https://gea.esac.esa.int/tap-server/tap/sync"
def run(adql, t=170):
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": adql}).encode()
    t0 = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL, data=data, headers={"User-Agent": "second-sun-census/1.0"}), timeout=t).read().decode()
        return list(csv.reader(io.StringIO(r)))[1:], round(time.time() - t0, 1)
    except Exception as e:
        return "ERR " + str(e)[:90], round(time.time() - t0, 1)
print("Gaia DR3 EB candidates, total:", run("SELECT COUNT(*) FROM gaiadr3.vari_eclipsing_binary")[0], flush=True)
for nm, lo_f in (("P > 7 d", 1/7), ("P > 10 d", 1/10), ("P > 20 d", 1/20), ("P > 40 d", 1/40)):
    n, _ = run(f"SELECT COUNT(*) FROM gaiadr3.vari_eclipsing_binary WHERE frequency < {lo_f:.6f}")
    rows, dt = run(f"SELECT FLOOR(g.phot_g_mean_mag) AS gb, COUNT(*) AS n FROM (SELECT source_id FROM gaiadr3.vari_eclipsing_binary WHERE frequency < {lo_f:.6f}) AS v JOIN gaiadr3.gaia_source AS g ON g.source_id = v.source_id GROUP BY gb ORDER BY gb")
    print(f"{nm}: all magnitudes {n}; query {dt}s;", flush=True)
    if isinstance(rows, list):
        d = {int(float(a)): int(b) for a, b in rows if a not in ("", None)}
        cum = 0; parts = []
        for G in range(0, 20):
            cum += d.get(G, 0); parts.append(f"G<{G+1}: {cum}")
        print("   cumulative: " + "; ".join(parts[8:16]), flush=True)
    else:
        print("   ", rows, flush=True)
