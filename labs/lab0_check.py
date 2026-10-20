r"""Lab 0: is your workbench ready? Run:  .\.venv\Scripts\python.exe labs\lab0_check.py"""
import _env, sys, shutil, urllib.request
print("Python", sys.version.split()[0], "at", sys.executable)
for name in ("numpy", "astropy", "lightkurve", "astroquery", "matplotlib", "wotan", "batman"):
    try:
        print(f"  {name:11s}", getattr(__import__(name), "__version__", "installed"))
    except Exception as e:
        print(f"  {name:11s} MISSING ({e.__class__.__name__})")
for drive in ("C:\\", "D:\\"):
    u = shutil.disk_usage(drive)
    print(f"Drive {drive} free: {u.free / 1e9:.0f} GB of {u.total / 1e9:.0f} GB")
print("Caches go to:", _env.CACHE)
print("Lab downloads go to:", _env.DATA)
try:
    urllib.request.urlopen("https://mast.stsci.edu/api/v0/", timeout=15)
    print("NASA's archive (MAST): reachable")
except Exception as e:
    print("NASA's archive (MAST): NOT reachable:", e)
