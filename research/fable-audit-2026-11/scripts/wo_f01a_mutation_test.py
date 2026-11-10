"""WO-F01 Part A mutation test (10 Nov 2026): do the Part A checks go RED when the harness is deliberately broken?
Part A's proof tests (zero-injection identity, bump control) were only shown to pass. This builds copies of wo_f01a_mask_loss.py with one deliberate bug each,
runs each on the same small sample of G2 (6 files per period bin and product family, 60 files, 6 workers, about 30 s each), and applies three explicit checks to every variant.
Nothing in pipeline/ or the real Part A rows is touched (mutants write their rows to a temp folder).
Checks (on dips at K 25 and bumps at K 25, 8 h bump, pooled over files per period bin):
  T1 mask loss visible : in the two longest period bins (20-27.4 d and over 27.4 d) the share found BEFORE the mask is at least 0.3 below the share found AFTER.
  T2 injection works   : the share found AFTER is at least 0.9 in every bin (a clean injection at 25 times the noise is found).
  T3 bump control      : bumps found before and after agree within 0.1 in every bin.
Expected: the unmodified copy passes T1, T2, T3. Mutant A (before-case injected after the mask) must fail T1. Mutant B (injection sign flipped) must fail T2. Mutant C (bump injected as a dip in the before case) must fail T3.
Usage: SS_SET is set here (g2). python wo_f01a_mutation_test.py"""
import os, sys, subprocess, tempfile, pathlib
import pandas as pd

SRC = pathlib.Path(r"D:\second-sun\research\fable-audit-2026-11\scripts\wo_f01a_mask_loss.py")
PY = r"D:\second-sun\.venv\Scripts\python.exe"
text = SRC.read_text(encoding="utf-8")
OUT_LINE = 'OUT = pathlib.Path(r"D:\\second-sun\\data\\fable_audit_mask"); OUT.mkdir(parents=True, exist_ok=True)'
assert text.count(OUT_LINE) == 1
MUTANTS = {
    "control (unmodified)": [],
    "A before-case injected AFTER the mask": [("fnd_b, _ = found(ta, fa2, arm, tc, dur) if len(ta) > 200 else (False, None)", "fnd_b, _ = found(t0, fb, arm, tc, dur)")],
    "B injection sign flipped": [("return -sign * depth_ppm", "return sign * depth_ppm")],
    "C bump injected as a dip in the before case": [("fa = f + signal(t, tc, dur, depth, sign)", "fa = f + signal(t, tc, dur, depth, 1)")],
}
BINS = (5, 10, 14, 20, 27.4)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="wo_f01a_mut_"))
env = dict(os.environ, SS_SET="g2", PYTHONUTF8="1", NUMBA_NUM_THREADS="1")
report = []
for name, edits in MUTANTS.items():
    d = tmp / name.split()[0]; d.mkdir()
    t = text.replace(OUT_LINE, f'OUT = pathlib.Path(r"{d}"); OUT.mkdir(parents=True, exist_ok=True)')
    for a, b in edits:
        assert t.count(a) == 1, (name, a)
        t = t.replace(a, b)
    (d / "variant.py").write_text(t, encoding="utf-8")
    r = subprocess.run([PY, str(d / "variant.py"), "run", "6", "6"], env=env, capture_output=True, text=True, cwd=str(d))
    if r.returncode != 0:
        report.append(f"{name}: RUN FAILED {r.stderr[-300:]}"); continue
    df = pd.read_pickle(d / "rows_g2.pkl")
    df = df[df.K.notna()]
    dips = df[(df.sign == 1) & (df.K == 25.0)]; bumps = df[(df.sign == -1) & (df.K == 25.0)]
    def cells(x):
        return [(x[x.bin_lo == lo].found_before.mean(), x[x.bin_lo == lo].found_after.mean(), x[x.bin_lo == lo].file.nunique()) for lo in BINS]
    cd, cb = cells(dips), cells(bumps)
    t1 = all(b <= a - 0.3 for b, a, _ in cd[3:])
    t2 = all(a >= 0.9 for _, a, _ in cd)
    t3 = all(abs(b - a) <= 0.1 for b, a, _ in cb)
    report.append(f"\n{name}: files with injections {df.file.nunique()}")
    report.append("  dips K 25 before/after by bin (5-10, 10-14, 14-20, 20-27.4, >27.4): " + " | ".join(f"{b:.2f}/{a:.2f}" for b, a, _ in cd))
    report.append("  bumps K 25 before/after by bin:                                  " + " | ".join(f"{b:.2f}/{a:.2f}" for b, a, _ in cb))
    report.append(f"  T1 mask loss visible: {'PASS' if t1 else 'FAIL'}   T2 injection works: {'PASS' if t2 else 'FAIL'}   T3 bump control: {'PASS' if t3 else 'FAIL'}")
print("\n".join(report))
