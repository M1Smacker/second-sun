"""Run STANLEY's planet search (stage 2) with two compatibility shims, without editing the package:
numpy 2 removed np.product (STANLEY 0.2.8 still calls it) -> alias to np.prod; lightkurve cache forced to D:.
Usage (STANLEY venv python): python run_search.py <same CLI args as Stanley_PlanetSearch_InterpN_DebugPadding>"""
import sys, runpy, numpy as np
import lightkurve as lk
if not hasattr(np, "product"):
    np.product = np.prod
lk.conf.cache_dir = r"D:\second-sun\.cache\lightkurve"
sys.argv = ["Stanley_PlanetSearch_InterpN_DebugPadding"] + sys.argv[1:]
runpy.run_module("stanley_cbp.Stanley_PlanetSearch_InterpN_DebugPadding", run_name="__main__")
