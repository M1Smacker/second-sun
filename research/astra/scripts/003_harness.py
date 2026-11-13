"""Guarded entry point for the copied Petrova modules. Run with Python -I -B."""

import csv
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(r"D:\second-sun-astra")
DATA = ROOT / "data"
OUT = DATA / "astra" / "003"
COPIES = Path(__file__).resolve().with_name("harness") / "sprint003"
TARGETS = ROOT / "targets" / "r1_targets.csv"
CATALOGUES = (
    DATA / "xmatch" / "ebs.csv",
    DATA / "g3" / "catalog_ttc" / "table3_new_ebs.txt",
)
DEVELOPMENT_HASH = "bcd29c7aabb0"


class Guard:
    def __init__(self):
        for path in (COPIES, TARGETS, *CATALOGUES):
            print(f"READ {path}", flush=True)
        print(f"WRITE {OUT}", flush=True)
        self.data = DATA.resolve(strict=True)
        self.out = OUT.resolve()
        if self.out != self.data / "astra" / "003":
            raise PermissionError("Output root resolves outside its expected directory")
        self.reads = set()
        for path in CATALOGUES:
            resolved = path.resolve()
            if resolved != self.data / path.relative_to(DATA):
                raise PermissionError("Catalogue path escapes its expected location")
            self.reads.add(resolved)
        with TARGETS.open(encoding="utf-8-sig", newline="") as source:
            rows = csv.DictReader(line for line in source if not line.startswith("#"))
            self.seen = {name: set() for name in ("g2", "g3")}
            for row in rows:
                if row["list"] in self.seen and row["design_seen"] == "1":
                    self.seen[row["list"]].add(row["tic"])

    def allow_design_file(self, path):
        """Register a design-seen FITS or stored development group before opening it."""
        path = Path(path)
        relative = path.relative_to(DATA)
        directory, group, name = relative.parts if len(relative.parts) == 3 else ("", "", "")
        valid = directory in self.seen and group in self.seen[directory] and name.endswith(".fits")
        if len(relative.parts) == 4:
            directory, run, group, name = relative.parts
            campaign = directory.removeprefix("stage3_")
            star, sep, sector = Path(name).stem.partition("_")
            valid = (
                campaign in self.seen
                and directory == f"stage3_{campaign}"
                and run == f"r1dev_{campaign}_seen_{DEVELOPMENT_HASH}"
                and group in {"groups", "groups_sap"}
                and name.endswith(".json")
                and sep and sector.isdecimal()
                and star in self.seen[campaign]
            )
        if not valid or path.resolve() != self.data / relative:
            raise PermissionError("Input is outside the design-seen file policy")
        self.reads.add(path.resolve())
        return path

    def check_write(self, path):
        path = Path(os.fsdecode(path))
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.is_relative_to(OUT) or not path.resolve().is_relative_to(self.out):
            raise PermissionError("Write outside data/astra/003")

    def allow_machine_inputs(self, campaign):
        """Exact shared inputs authorized by AGENTS rule 2, read only."""
        if campaign not in self.seen:
            raise PermissionError("Unsupported campaign")
        base = DATA / campaign
        paths = [base / "manifest.csv"]
        paths += [base / "audit" / name for name in
                  ("audit_all.csv", "spoc_windows.pkl", "best_per_star_sector.csv")]
        for path in paths:
            if path.resolve() != self.data / path.relative_to(DATA):
                raise PermissionError("Machine input path escape")
            self.reads.add(path.resolve())
            print(f"MACHINE READ {path}", flush=True)
        references, used = {}, set()
        with paths[0].open(encoding="utf-8-sig", newline="") as source:
            for row in csv.DictReader(source):
                if row["file"] in used:
                    continue
                used.add(row["file"])
                if row["author"] == "SPOC":
                    sector = int(row["file"].split("-s")[1][:4])
                    old = Path(row["path"])
                    relative = old.relative_to(Path(r"D:\second-sun") / "data")
                    reference = DATA / relative
                    if reference.resolve() != self.data / relative:
                        raise PermissionError("Reference path escape")
                    references.setdefault(sector, reference)
        self.reads.update(path.resolve() for path in references.values())
        print("MACHINE READ reference SPOC files selected by frozen manifest rule (momentum dumps only)", flush=True)
        return references

    def audit(self, event, args):
        if event == "open":
            path, _, flags = args
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                self.check_write(path)
            elif not isinstance(path, int):
                local = Path(os.path.abspath(os.fsdecode(path)))
                resolved = local.resolve()
                if local.is_relative_to(DATA) or resolved.is_relative_to(self.data):
                    if not local.is_relative_to(DATA):
                        raise PermissionError("Read through the helper data junction")
                    if resolved not in self.reads and not resolved.is_relative_to(self.out):
                        raise PermissionError("Data input is not on the harness allowlist")
        elif event in {"os.mkdir", "os.remove", "os.rmdir", "os.chmod", "os.utime"}:
            if event == "os.mkdir" and Path(os.fsdecode(args[0])) == OUT.parent:
                if OUT.parent.resolve() != self.out.parent:
                    raise PermissionError("Unsafe output parent")
            else:
                self.check_write(args[0])
        elif event == "os.rename":
            self.check_write(args[0])
            self.check_write(args[1])
        elif event in {"os.link", "os.symlink", "subprocess.Popen", "os.system"}:
            raise PermissionError("Operation disabled in the audit harness")

    def start(self):
        if not sys.flags.isolated or not sys.dont_write_bytecode:
            raise RuntimeError("Run with Python -I -B")
        sys.addaudithook(self.audit)
        OUT.mkdir(parents=True, exist_ok=True)
        temporary = OUT / "tmp"
        temporary.mkdir(exist_ok=True)
        os.environ["TMP"] = str(temporary)
        os.environ["TEMP"] = str(temporary)
        tempfile.tempdir = str(temporary)
        cache = OUT / "numba-cache"
        cache.mkdir(exist_ok=True)
        os.environ["NUMBA_CACHE_DIR"] = str(cache)
        provenance = json.loads((COPIES / "provenance.json").read_text(encoding="utf-8"))
        for name, row in provenance.items():
            content = (COPIES / name).read_bytes().replace(b"\r\n", b"\n")
            if hashlib.sha256(content).hexdigest() != row["copy_sha256_lf"]:
                raise RuntimeError(f"Copied module hash mismatch: {name}")
        sys.path.insert(0, str(COPIES))
        return provenance


def smoke():
    guard = Guard()
    provenance = guard.start()
    forbidden = (
        (ROOT / "AGENTS.md", os.O_WRONLY),
        (DATA / "g1" / "probe.fits", os.O_RDONLY),
        (DATA / "g2" / "audit" / "audit_all.csv", os.O_RDONLY),
    )
    for path, flags in forbidden:
        try:
            sys.audit("open", str(path), None, flags)
        except PermissionError:
            continue
        raise RuntimeError("Forbidden path passed the audit hook")
    probe = OUT / "part0-probe.txt"
    probe.write_text("guard smoke check\n", encoding="utf-8")
    assert probe.read_text(encoding="utf-8") == "guard smoke check\n"
    mask = importlib.import_module("petrova_mask")
    assert Path(mask.__file__).parent == COPIES
    mask.selftest()
    print(f"Verified {len(provenance)} copied source hashes, {len(forbidden)} rejected access events and one allowed write.")


if __name__ == "__main__":
    try:
        smoke()
    except PermissionError:
        sys.exit("Harness refused a path or operation under its access policy.")
