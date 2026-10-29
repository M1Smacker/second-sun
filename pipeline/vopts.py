"""Vesper study switches (VESPER-STUDY-PLAN.md phase C). Set VESPER_OPTS in the environment, e.g. VESPER_OPTS=c1b,c2 (comma or plus separated). EVERY switch defaults OFF: with VESPER_OPTS unset the code is
exactly Vesper 0.7.1 (proved by zero_diff.py). The set is read at import, so worker processes inherit it. Switches:
  c1b  step test measured on a curve re-smoothed around each event: event masked (centre +- 0.75 x box), biweight window 3 x box (at least 0.5 d), trend interpolated across the mask; depth re-measured on it
  c2   step test without its data-cover rule (that duplicates the gap rule; phase A showed every 8 h step flag came from it); a side with no data is not judged
"""
import os

ON = frozenset(x for x in os.environ.get("VESPER_OPTS", "").replace("+", ",").split(",") if x)
KNOWN = {"c1b", "c2"}
assert ON <= KNOWN, f"unknown VESPER_OPTS switch: {sorted(ON - KNOWN)}"
