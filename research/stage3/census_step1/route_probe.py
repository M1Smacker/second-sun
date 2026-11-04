"""Census step 2 research (4 Nov 2026 night): how fast and how big is it to fetch TESS 2-minute light curves in bulk? Probe: 20 files by the AWS open-data bucket and 6 by MAST, sector 27 (random draw). Folder data/census_probe (new, empty)."""
import os, random, re, time, urllib.request, subprocess
random.seed(27)
OUT = r"D:\second-sun\data\census_probe"
txt = urllib.request.urlopen("https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_27_lc.sh", timeout=60).read().decode()
names = re.findall(r"-o (\S+_lc\.fits)", txt)
print("files in the sector 27 script:", len(names))
pick = random.sample(names, 26)
def s3(n):
    m = re.search(r"-(\d{16})-", n); t = m.group(1); sec = re.search(r"-s(\d{4})-", n).group(1)
    return f"https://stpubdata.s3.amazonaws.com/tess/public/tid/s{sec}/{t[0:4]}/{t[4:8]}/{t[8:12]}/{t[12:16]}/{n}"
def mast(n): return f"https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:TESS/product/{n}"
def fetch(u, dest):
    t0 = time.time(); d = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "second-sun-census/1.0"}), timeout=120).read()
    open(dest, "wb").write(d); return len(d), time.time() - t0
for name, route, group in (("AWS S3", s3, pick[:20]), ("MAST", mast, pick[20:])):
    tot = 0; tt = 0; fails = 0
    t0 = time.time()
    for n in group:
        try:
            b, dt = fetch(route(n), os.path.join(OUT, ("s3_" if name == "AWS S3" else "mast_") + n)); tot += b; tt += dt
        except Exception as e:
            fails += 1
    wall = time.time() - t0
    print(f"{name}: {len(group)-fails}/{len(group)} files, {tot/1e6:.1f} MB, mean {tot/max(1,len(group)-fails)/1e6:.2f} MB per file, {wall:.1f} s wall = {len(group)/wall:.2f} files/s, {tot/wall/1e6:.2f} MB/s, {fails} failures")
