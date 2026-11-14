"""Gate verdict with explicit coverage (FIX 87, Claude, 14 Nov 2026). Before this, r1_gate.py kept PASS for a period bin with no
injections and for a bin whose ratio was undefined (nothing found even after the mask), so a gate could say PASS having tested only
3 of 5 bins (sealed G3, 20 to 27.4 d and over 27.4 d). Filed verdicts are not changed; this is for every later run (G1 on).
judge(per_bin, mark, require_all) takes {bin label: m} where m is a number (tested), None (no injections) or NaN (injected, nothing
found even after the mask, ratio undefined) and returns (status, line):
  FAIL                         any tested bin has m below the mark
  PASS                         every bin tested and every m at or above the mark
  PASS ON TESTED BINS          some bins untested or undefined, every tested m at or above the mark (require_all False)
  INCOMPLETE                   the same, when require_all is True (a gate that must cover every bin)
The line always names the untested and undefined bins, so coverage is never silent."""
import math


def judge(per_bin, mark=0.95, require_all=False):
    tested = {b: m for b, m in per_bin.items() if m is not None and not (isinstance(m, float) and math.isnan(m))}
    none = [b for b, m in per_bin.items() if m is None]
    undef = [b for b, m in per_bin.items() if m is not None and b not in tested]
    failed = [b for b, m in tested.items() if m < mark]
    if failed:
        status = "FAIL"
    elif none or undef or not tested:
        status = "INCOMPLETE" if require_all else "PASS ON TESTED BINS"
    else:
        status = "PASS"
    cov = f"{len(tested)} of {len(per_bin)} bins tested"
    if none:
        cov += "; no injections: " + ", ".join(none)
    if undef:
        cov += "; nothing found even after the mask (not judged): " + ", ".join(undef)
    if failed:
        cov += "; below the mark: " + ", ".join(failed)
    return status, f"{status} ({cov})"
