"""Run settings from the run's own file, and loud failure on missing inputs (BUILD T52; Claude, 14 Nov 2026). NOT in the frozen hash list:
it reads and checks, never changes, what a run uses. For the G1 runner (and any later runner), imported BEFORE dataset / vopts.

Why: dataset.py and vopts.py read SS_SET and VESPER_OPTS from the environment at import. A stale shell variable silently points a run at
the wrong star set or options, and the R1 runner hashes an absent file as "missing" instead of stopping (the development example showed
G1 paths with no files).

    import run_inputs as RI
    cfg = RI.apply("research/stage3/G1-RUN-SETTINGS.json")   # sets SS_SET and VESPER_OPTS from the file; refuses a conflicting shell value
    import dataset as DS, vopts as V                          # only now
    RI.require(DS, stars=[...], targets=C.TARGETS)            # refuses missing folders, tables or stars without light curves

Settings file: {"set": "g1"|"g2"|"g3", "opts": ["c6", "p1"], "note": "..."}. Nothing else is read from it."""
import json, os, pathlib

SETS = ("g1", "g2", "g3")


class Refused(SystemExit):
    pass


def apply(path):
    p = pathlib.Path(path)
    if not p.is_file():
        raise Refused(f"REFUSED: run settings file not found: {p}")
    cfg = json.loads(p.read_text(encoding="utf-8"))
    st, opts = cfg.get("set"), cfg.get("opts")
    if st not in SETS:
        raise Refused(f"REFUSED: settings 'set' must be one of {SETS}, not {st!r}")
    if not isinstance(opts, list) or not all(isinstance(o, str) and o for o in opts):
        raise Refused("REFUSED: settings 'opts' must be a list of switch names")
    want = {"SS_SET": st, "VESPER_OPTS": ",".join(sorted(opts))}
    for k, v in want.items():
        have = os.environ.get(k)
        if have is not None and _norm(k, have) != _norm(k, v):
            raise Refused(f"REFUSED: the shell has {k}={have!r} but the run settings say {v!r}; unset it or fix the file")
        os.environ[k] = v
    return cfg


def _norm(k, v):
    return ",".join(sorted(x for x in v.replace("+", ",").split(",") if x)) if k == "VESPER_OPTS" else v


def require(DS, stars=(), targets=None):
    """Refuse when any input the chain reads is absent. Returns a dict of counts for the run record."""
    miss = [str(x) for x in (DS.DATA, DS.RUNS.parent) if not pathlib.Path(x).is_dir()]
    miss += [str(x) for x in (DS.MANIFEST, DS.BEST, targets or DS.TARGETS) if not pathlib.Path(x).is_file()]
    if miss:
        raise Refused("REFUSED: missing inputs:\n  " + "\n  ".join(miss))
    no_lc = [int(t) for t in stars if not any((pathlib.Path(DS.DATA) / str(int(t))).glob("*.fits"))]
    if no_lc:
        raise Refused(f"REFUSED: {len(no_lc)} of {len(stars)} stars have no light-curve file in {DS.DATA} (first: {no_lc[:5]})")
    return {"set": DS.NAME, "stars": len(stars), "stars_without_files": 0}
