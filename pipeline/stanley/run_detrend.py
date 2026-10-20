r"""Run STANLEY's detrending (stage 1) with every download forced onto D: (STANLEY itself calls
download_all() with no folder, which lightkurve sends to C:\Users\...\.cache\lightkurve).
Usage: python run_detrend.py "TIC 260128333" ss_toi1338   (run with the STANLEY venv's python)"""
import sys, pathlib
import lightkurve as lk
CACHE = pathlib.Path(r"D:\second-sun\.cache\lightkurve")
CACHE.mkdir(parents=True, exist_ok=True)
lk.conf.cache_dir = str(CACHE)
assert str(lk.config.get_cache_dir()).lower().startswith("d:"), lk.config.get_cache_dir()
print("lightkurve cache:", lk.config.get_cache_dir(), flush=True)
if len(sys.argv) > 1:
    from stanley_cbp import Stanley_Detrending as D
    D.runDetrendingModule(SystemName=sys.argv[1], DetrendingName=sys.argv[2], UseSavedData=0)
