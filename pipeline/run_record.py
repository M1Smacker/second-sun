"""Automatic run record (BUILD T142, absorbs T128; Claude, 14 Nov 2026). NOT in the frozen hash list: it reads, never changes, what a run uses.

Every search or bench run calls write(run_dir, inputs, frozen_hash=..., extra=...) once, before the first group is searched. It writes run_dir/run_record.json:
when (UTC), git HEAD and every tracked file that differs from it (a dirty tree is recorded, not refused: the runner's own guard decides), the frozen hash
the runner checked, Python and package versions, the switches in the environment (SS_SET, VESPER_OPTS, NUMBA_NUM_THREADS), the machine, and for every named
input file its size and sha256 (directories: file count, total size and a hash over names, sizes and contents, in sorted order).
verify(run_dir) re-hashes the same inputs later and returns the list of differences (empty = the inputs on disk are still the ones the run read).
The record lives in the run folder under data\\ (git-ignored), so input paths may name stars; nothing here is published.
Usage: python run_record.py write <run_dir> name=path [name=path ...]   |   python run_record.py verify <run_dir>"""
import datetime
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys

ROOT = pathlib.Path(r"D:\second-sun")
PACKAGES = ("numpy", "pandas", "scipy", "astropy", "lightkurve", "numba", "matplotlib")
ENV = ("SS_SET", "VESPER_OPTS", "NUMBA_NUM_THREADS")
NAME = "run_record.json"


def _sha_file(p, h=None):
    own = h is None
    h = h or hashlib.sha256()
    with open(p, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest() if own else None


def describe(path):
    """{kind, size, sha256 [, files]} of a file or a directory (directories hashed over sorted relative names, sizes and contents)."""
    p = pathlib.Path(path)
    if p.is_file():
        return dict(kind="file", size=p.stat().st_size, sha256=_sha_file(p))
    if p.is_dir():
        h = hashlib.sha256(); n = size = 0
        for f in sorted(x for x in p.rglob("*") if x.is_file()):
            rel = f.relative_to(p).as_posix(); s = f.stat().st_size
            h.update(f"{rel}\0{s}\0".encode()); _sha_file(f, h); n += 1; size += s
        return dict(kind="dir", files=n, size=size, sha256=h.hexdigest())
    return dict(kind="missing")


def _git(*args):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as exc:                               # a record without git is still a record; say why
        return f"unavailable: {type(exc).__name__}"


def _versions():
    out = {}
    for name in PACKAGES:
        try:
            from importlib.metadata import version
            out[name] = version(name)
        except Exception:
            out[name] = "not installed"
    return out


def build(inputs, frozen_hash=None, extra=None):
    return dict(written_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                git_head=_git("rev-parse", "HEAD"), git_dirty=[l for l in _git("status", "--porcelain", "--untracked-files=no").splitlines() if l],
                frozen_hash=frozen_hash, python=sys.version.split()[0], executable=sys.executable, packages=_versions(),
                env={k: os.environ.get(k) for k in ENV}, machine=dict(system=platform.system(), release=platform.release(), cpu_count=os.cpu_count()),
                inputs={k: dict(path=str(v), **describe(v)) for k, v in sorted(inputs.items())}, extra=extra or {})


def write(run_dir, inputs, frozen_hash=None, extra=None):
    """Write run_dir/run_record.json. Refuses to overwrite an existing record (a resumed run keeps its first record; verify() compares)."""
    d = pathlib.Path(run_dir); d.mkdir(parents=True, exist_ok=True)
    out = d / NAME
    if out.exists():
        raise FileExistsError(f"{out} exists: a run keeps its first record; call verify()")
    rec = build(inputs, frozen_hash, extra)
    missing = [k for k, v in rec["inputs"].items() if v["kind"] == "missing"]
    if missing:
        raise FileNotFoundError(f"inputs missing, no record written: {missing}")
    out.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    return rec


def verify(run_dir):
    """Differences between the recorded inputs and the files on disk now ([] = unchanged)."""
    rec = json.loads((pathlib.Path(run_dir) / NAME).read_text(encoding="utf-8"))
    diffs = []
    for k, v in rec["inputs"].items():
        now = describe(v["path"])
        for field in ("kind", "size", "sha256", "files"):
            if v.get(field) != now.get(field):
                diffs.append(f"{k}: {field} recorded {v.get(field)} now {now.get(field)}")
    return diffs


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "write":
        pairs = dict(a.split("=", 1) for a in sys.argv[3:])
        r = write(sys.argv[2], pairs)
        print(f"run record written: git {r['git_head'][:12]}, {len(r['inputs'])} inputs, dirty files {len(r['git_dirty'])}")
    elif len(sys.argv) == 3 and sys.argv[1] == "verify":
        d = verify(sys.argv[2])
        print("inputs unchanged" if not d else "INPUTS CHANGED:\n  " + "\n  ".join(d)); sys.exit(1 if d else 0)
    else:
        sys.exit(__doc__)
