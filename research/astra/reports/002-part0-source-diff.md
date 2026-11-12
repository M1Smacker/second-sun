# Part 0 source diff

Compared with the Git blobs in the harness provenance manifest, with LF normalization and identifiers masked in the removed lines.

```diff
--- pipeline/audit_all.py
+++ harness/audit_all.py
@@ -18,2 +18,2 @@
-OUT = DS.AUDIT
-WIN_DB = OUT / "spoc_windows.pkl"
+OUT = DS.ROOT / "data" / "astra" / "002" / "audit"
+WIN_DB = DS.AUDIT / "spoc_windows.pkl"
@@ -30 +30 @@
-    for r in csv.DictReader(l for l in open(r"D:\second-sun\targets\g1_targets.csv") if not l.startswith("#")):
+    for r in csv.DictReader(l for l in open(r"D:\second-sun-astra\targets\g1_targets.csv") if not l.startswith("#")):
@@ -33 +33 @@
-    for r in csv.DictReader(open(r"D:\second-sun\research\wave-3-pipeline\g1_tmag.csv")):     # ALL catalogue periods (B3)
+    for r in csv.DictReader(open(r"D:\second-sun-astra\research\wave-3-pipeline\g1_tmag.csv")):     # ALL catalogue periods (B3)
@@ -94 +94 @@
-    pickle.dump(db, open(WIN_DB, "wb"))
+    pickle.dump(db, open(OUT / "spoc_windows.pkl", "wb"))
--- pipeline/audit_paths.py
+++ harness/audit_paths.py
@@ -17 +17 @@
-for r in csv.DictReader(l for l in open(r"D:\second-sun\targets\g1_targets.csv") if not l.startswith("#")):
+for r in csv.DictReader(l for l in open(r"D:\second-sun-astra\targets\g1_targets.csv") if not l.startswith("#")):
@@ -30 +30 @@
-    for p in pathlib.Path(r"D:\second-sun\data").rglob(f"tess*-s{sector:04d}-{tic:016d}-*-s_lc.fits"):
+    for p in pathlib.Path(r"D:\second-sun-astra\data").rglob(f"tess*-s{sector:04d}-{tic:016d}-*-s_lc.fits"):
--- pipeline/dataset.py
+++ harness/dataset.py
@@ -5 +5 @@
-ROOT = pathlib.Path(r"D:\second-sun")
+ROOT = pathlib.Path(r"D:\second-sun-astra")
@@ -12 +12 @@
-    PREP = ROOT / "data" / "stage3_prep"
+    PREP = ROOT / "data" / "astra" / "002" / "prep"
@@ -19 +19 @@
-    PREP = ROOT / "data" / "stage3_g2_prep"
+    PREP = ROOT / "data" / "astra" / "002" / "prep"
@@ -26 +26 @@
-    PREP = ROOT / "data" / "stage3_g3_prep"
+    PREP = ROOT / "data" / "astra" / "002" / "prep"
--- pipeline/detect_v2.py
+++ harness/detect_v2.py
@@ -101 +101 @@
-    gaps (seen on TIC [redacted]) simply doesn't narrow the result."""
+    gaps simply doesn't narrow the result."""
--- pipeline/petrova_mask.py
+++ harness/petrova_mask.py
@@ -19 +19 @@
-ROOT = pathlib.Path(r"D:\second-sun")
+ROOT = pathlib.Path(r"D:\second-sun-astra")
--- pipeline/stage2_search.py
+++ harness/stage2_search.py
@@ -19 +19 @@
-OUT = pathlib.Path(r"D:\second-sun\data\stage2")
+OUT = DS.ROOT / "data" / "astra" / "002" / "stage2"
@@ -21,2 +21,2 @@
-STARS = pathlib.Path(r"D:\second-sun\targets\stage2_stars.csv")
-CONTROLS = {"Kepler-16": [redacted], "Kepler-38": [redacted], "Kepler-64": [redacted], "Kepler-453": [redacted], "Kepler-1647": [redacted]}
+STARS = OUT / "stage2_stars.csv"
+CONTROLS = {}  # Legacy G1 selection is outside this audit harness.
@@ -27,3 +27,3 @@
-    per = pd.read_csv(r"D:\second-sun\research\audit-2026-10-23\per_star.csv")
-    tg = pd.read_csv(r"D:\second-sun\targets\g1_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
-    man = pd.read_csv(r"D:\second-sun\data\g1\manifest.csv").drop_duplicates("file")
+    per = pd.read_csv(r"D:\second-sun-astra\research\audit-2026-10-23\per_star.csv")
+    tg = pd.read_csv(r"D:\second-sun-astra\targets\g1_targets.csv", comment="#").drop_duplicates("tic").set_index("tic")
+    man = pd.read_csv(r"D:\second-sun-astra\data\g1\manifest.csv").drop_duplicates("file")
--- pipeline/stage3.py
+++ harness/stage3.py
@@ -17,3 +17,3 @@
-DRY = C.ROOT / "data" / "stage3_dry"
-RUN = DS.RUNS
-FROZEN = C.ROOT / "research" / "stage3" / "SETTINGS_FROZEN.json"
+DRY = PREP / "stage3_dry"
+RUN = PREP / "runs"
+FROZEN = PREP / "SETTINGS_FROZEN.json"
@@ -223 +223 @@
-        search(S2.STARS, C.ROOT / "data" / "stage3_dry50", "dry50", n, C.GRID_V4)
+        search(S2.STARS, PREP / "stage3_dry50", "dry50", n, C.GRID_V4)
--- pipeline/stage3_core.py
+++ harness/stage3_core.py
@@ -9 +9 @@
-ROOT = pathlib.Path(r"D:\second-sun")
+ROOT = pathlib.Path(r"D:\second-sun-astra")
--- pipeline/stage3_report.py
+++ harness/stage3_report.py
@@ -258 +258 @@
-        d = C.ROOT / "research" / "stage3"; d.mkdir(exist_ok=True)
+        d = C.ROOT / "data" / "astra" / "002"; d.mkdir(parents=True, exist_ok=True)
```
