"""Run every pipeline test once and say plainly what passed, what was SKIPPED and what failed (FIX 83 step 1; Claude, 15 Nov 2026).
Each test_*.py runs in its own interpreter from pipeline/ with the venv's python and a time limit. A test counts as SKIPPED if its output
contains a 'SKIP' or 'skip ' line, even when it exits 0, so a skip can never be read as a pass. Writes test-run.txt beside this file.
Usage: python run_tests.py [--timeout 900] [name ...]"""
import argparse, pathlib, re, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
SKIP = re.compile(r"^\s*(SKIP\b|skip\s)", re.M)


def main():
    a = argparse.ArgumentParser(); a.add_argument("--timeout", type=int, default=900); a.add_argument("names", nargs="*")
    o = a.parse_args()
    tests = sorted(p for p in HERE.glob("test_*.py") if not o.names or any(n in p.name for n in o.names))
    lines, res = [], {"PASS": [], "SKIPPED": [], "FAIL": [], "TIMEOUT": []}
    for p in tests:
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, "-B", p.name], cwd=HERE, capture_output=True, text=True, timeout=o.timeout,
                               encoding="utf-8", errors="replace")
            out = (r.stdout + r.stderr).strip()
            kind = "FAIL" if r.returncode else ("SKIPPED" if SKIP.search(out) else "PASS")
        except subprocess.TimeoutExpired:
            out, kind = f"no result within {o.timeout} s", "TIMEOUT"
        res[kind].append(p.name)
        last = out.splitlines()[-1] if out else ""
        lines.append(f"{kind:8} {p.name:32} {time.time() - t0:6.0f} s  {last[:140]}")
        print(lines[-1], flush=True)
    summary = "RESULT: " + ", ".join(f"{len(v)} {k}" for k, v in res.items()) + (f"; not passing: {res['SKIPPED'] + res['FAIL'] + res['TIMEOUT']}" if len(res["PASS"]) < len(tests) else "")
    print(summary)
    if not o.names:                                   # only a full run is the record
        (HERE / "test-run.txt").write_text("\n".join(lines + [summary]) + "\n", encoding="utf-8")
    sys.exit(0 if len(res["PASS"]) == len(tests) else 1)


if __name__ == "__main__":
    main()
