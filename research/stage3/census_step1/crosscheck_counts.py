"""Independent re-check (plain csv/json, no pandas) of numbers quoted tonight: (1) target-list star counts; (2) G3 lost reads from the RUN output (groups json) instead of the audit table."""
import csv, glob, json, os, re
base = r"D:\second-sun\data\census_targets_2m"
old, new, newT = set(), set(), {}
for f in glob.glob(base + r"\all_targets_S*_v*.csv"):
    s = int(re.search(r"_S(\d+)_", f).group(1))
    if s > 109: continue
    for line in open(f, encoding="utf-8"):
        if line.startswith("#") or line.startswith("TICID"): continue
        p = line.strip().split(",")
        if len(p) < 4: continue
        tic = int(p[0]); T = float(p[3])
        if s <= 26: old.add(tic)
        else:
            new.add(tic); newT[tic] = min(T, newT.get(tic, 99))
only = new - old
print(f"S1-26 unique {len(old):,}; S27-109 unique {len(new):,}; new only {len(only):,}; new only Tmag<=13.5 {sum(1 for t in only if newT[t] <= 13.5):,}")
d = r"D:\second-sun\data\stage3_g3\g3_e7886a71a61f"
ns = no = 0; lost_groups = 0; groups = 0; stars = set(); stars_ok = set()
for sub in ("groups", "groups_sap"):
    for f in glob.glob(os.path.join(d, sub, "*.json")):
        j = json.load(open(f)); 
        if sub == "groups": groups += 1
        st = [m.get("status") for m in j["meta"]]
        no += st.count("no safe windows"); ns += len(st)
        if sub == "groups":
            stars.add(j["tic"])
            if any(s == "ok" for s in st): stars_ok.add(j["tic"])
            else: lost_groups += 1
print(f"G3 run output: {groups} star-sector groups; product reads in main groups {ns - 0}; 'no safe windows' reads {no}; groups with no ok product {lost_groups}; stars {len(stars)}; stars with at least one ok group {len(stars_ok)}")
