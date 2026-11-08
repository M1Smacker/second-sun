"""FFI door test, stage B: Gaia DR3 slow eclipsing binaries (frequency < 0.2, period over 5 d), joined to gaia_source,
one HEALPix level-3 pixel at a time (768 pixels), because a whole-sky join times out.

Read-only public TAP queries (https://gea.esac.esa.int/tap-server/tap/sync). Restartable: one CSV per pixel, a pixel that
already has a file is skipped. Output folder (git-ignored, never public): D:\\second-sun\\data\\ffi_door_2026-11-08\\gaia_pixels
Usage:  python gaia_pixels.py [n_workers]
Preregistered in research/stage3/FFI-DOOR-TEST-PLAN-2026-11-08.md (frame: Gaia DR3 vari_eclipsing_binary, P over 5 d).
"""
import csv, io, os, sys, time, threading, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://gea.esac.esa.int/tap-server/tap/sync"
OUT = r"D:\second-sun\data\ffi_door_2026-11-08\gaia_pixels"
LOG = r"D:\second-sun\data\ffi_door_2026-11-08\gaia_pixels_log.txt"
DONE = r"D:\second-sun\data\ffi_door_2026-11-08\gaia_pixels_done.txt"
W = 2 ** 35 * 4 ** 9          # source_id span of one level-3 HEALPix pixel
NPIX = 768

E_COLS = ["source_id", "frequency", "frequency_error", "reference_time", "model_type", "num_model_parameters",
          "reduced_chi2", "global_ranking",
          "derived_primary_ecl_phase", "derived_primary_ecl_phase_error", "derived_primary_ecl_depth",
          "derived_primary_ecl_duration", "derived_secondary_ecl_phase", "derived_secondary_ecl_depth",
          "derived_secondary_ecl_duration", "geom_model_reference_level",
          "geom_model_gaussian1_phase", "geom_model_gaussian1_sigma", "geom_model_gaussian1_depth",
          "geom_model_gaussian2_phase", "geom_model_gaussian2_sigma", "geom_model_gaussian2_depth",
          "geom_model_cosine_half_period_amplitude"]
G_COLS = ["ra", "dec", "pmra", "pmdec", "parallax", "parallax_error", "ruwe", "phot_g_mean_mag", "phot_bp_mean_mag",
          "phot_rp_mean_mag", "non_single_star"]
SEL = ", ".join(["e." + c for c in E_COLS] + ["g." + c for c in G_COLS])
lock = threading.Lock()


def log(msg):
    with lock:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def one_pixel(p):
    fn = os.path.join(OUT, "pix_%03d.csv" % p)
    if os.path.exists(fn):
        return 0
    a, b = p * W, (p + 1) * W - 1
    sql = ("SELECT " + SEL + " FROM gaiadr3.vari_eclipsing_binary AS e JOIN gaiadr3.gaia_source AS g "
           "ON e.source_id = g.source_id WHERE e.source_id BETWEEN %d AND %d AND g.source_id BETWEEN %d AND %d "
           "AND e.frequency < 0.2" % (a, b, a, b))
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": sql}).encode()
    for attempt in range(6):
        t0 = time.time()
        try:
            txt = urllib.request.urlopen(urllib.request.Request(URL, data=data), timeout=170).read().decode()
            if not txt.startswith("source_id"):
                raise RuntimeError("unexpected reply: " + txt[:120].replace("\n", " "))
            n = txt.count("\n") - 1
            with open(fn + ".tmp", "w", encoding="utf-8", newline="") as fh:
                fh.write(txt)
            os.replace(fn + ".tmp", fn)
            log("pixel %d rows %d %.0fs" % (p, n, time.time() - t0))
            return n
        except Exception as e:
            log("pixel %d attempt %d failed after %.0fs: %r" % (p, attempt, time.time() - t0, e))
            time.sleep(10 * (attempt + 1))
    log("pixel %d GAVE UP" % p)
    return -1


def main():
    nw = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    os.makedirs(OUT, exist_ok=True)
    log("start, %d workers, %d pixels" % (nw, NPIX))
    # a pixel order that mixes the dense galactic plane with sparse areas is not needed; plain order is fine
    with ThreadPoolExecutor(max_workers=nw) as ex:
        res = list(ex.map(one_pixel, range(NPIX)))
    bad = [i for i, r in enumerate(res) if r < 0]
    log("finished; rows this run %d; gave up on %s" % (sum(r for r in res if r > 0), bad))
    with open(DONE, "w") as fh:
        fh.write("done; gave up on %s\n" % bad)


if __name__ == "__main__":
    main()
