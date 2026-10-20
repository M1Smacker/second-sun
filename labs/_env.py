"""Shared setup for every lab: keep all caches and downloads on D: (C: is nearly full). Import this first."""
import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # D:\second-sun
CACHE = ROOT / ".cache"
for k, v in {"ASTROPY_CACHE_DIR": CACHE / "astropy", "ASTROPY_CONFIG_DIR": CACHE / "astropy-config",
             "XDG_CACHE_HOME": CACHE, "MPLCONFIGDIR": CACHE / "mpl"}.items():
    os.environ.setdefault(k, str(v)); pathlib.Path(v).mkdir(parents=True, exist_ok=True)
DATA = ROOT / "data" / "labs"; DATA.mkdir(parents=True, exist_ok=True)   # lab downloads (git-ignored)
OUT = ROOT / "labs" / "out"; OUT.mkdir(parents=True, exist_ok=True)      # lab pictures (git-ignored)
import warnings; warnings.filterwarnings("ignore")
