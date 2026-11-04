"""Census step 1: download TESS 2-minute target lists (sectors 27+) from tess.mit.edu.
Public lists. Output: data/census_targets_2m/ (new folder). Prints one summary line."""
import os, re, sys, time, urllib.request
base = "https://tess.mit.edu/public/target_lists/"
out = r"D:\second-sun\data\census_targets_2m"
MINSEC = int(sys.argv[1]) if len(sys.argv) > 1 else 27
links = [l.strip() for l in open(os.path.join(out, "_links.txt")) if l.strip()]
tot = 0; ok = 0; bad = []
for l in links:
    m = re.search(r"_S(\d+)_", l); sec = int(m.group(1))
    if sec < MINSEC: continue
    dest = os.path.join(out, os.path.basename(l))
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        tot += os.path.getsize(dest); ok += 1; continue
    try:
        data = urllib.request.urlopen(urllib.request.Request(base + l, headers={"User-Agent": "second-sun-census/1.0"}), timeout=60).read()
        if data[:15].lower().startswith(b"<!doctype") or b"<html" in data[:200].lower():
            bad.append((sec, "html")); continue
        open(dest, "wb").write(data); tot += len(data); ok += 1
    except Exception as e:
        bad.append((sec, str(e)[:60]))
    time.sleep(0.3)
print(f"files ok {ok}, bytes {tot/1e6:.1f} MB, bad {bad}")
