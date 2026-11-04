"""Second probe: 8 parallel threads from the AWS open-data bucket, 40 sector-27 files (other random draw). Folder data/census_probe."""
import os, random, re, time, urllib.request, concurrent.futures as cf
random.seed(1027)
OUT = r"D:\second-sun\data\census_probe"
txt = urllib.request.urlopen("https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_27_lc.sh", timeout=60).read().decode()
names = random.sample(re.findall(r"-o (\S+_lc\.fits)", txt), 40)
def s3(n):
    t = re.search(r"-(\d{16})-", n).group(1)
    return f"https://stpubdata.s3.amazonaws.com/tess/public/tid/s0027/{t[0:4]}/{t[4:8]}/{t[8:12]}/{t[12:16]}/{n}"
def get(n):
    d = urllib.request.urlopen(urllib.request.Request(s3(n), headers={"User-Agent": "second-sun-census/1.0"}), timeout=120).read()
    open(os.path.join(OUT, "par_" + n), "wb").write(d); return len(d)
t0 = time.time()
with cf.ThreadPoolExecutor(8) as ex: sizes = list(ex.map(get, names))
w = time.time() - t0
print(f"8 threads: {len(sizes)} files, {sum(sizes)/1e6:.1f} MB in {w:.1f} s = {len(sizes)/w:.2f} files/s, {sum(sizes)/w/1e6:.2f} MB/s")
