"""Vesper study switches (VESPER-STUDY-PLAN.md phase C). Set VESPER_OPTS in the environment, e.g. VESPER_OPTS=c1b,c2 (comma or plus separated). EVERY switch defaults OFF: with VESPER_OPTS unset the code is
exactly Vesper 0.7.1 (proved by zero_diff.py). The set is read at import, so worker processes inherit it. Switches:
  c1b  step test measured on a curve re-smoothed around each event: event masked (centre +- 0.75 x box), biweight window 3 x box (at least 0.5 d), trend interpolated across the mask; depth re-measured on it
  c1a  search each box length on its own curve: biweight window 3 x the box (at least 0.5 d) instead of one 2 d window for all boxes (wotan guidance, H7); the step test keeps the 2 d curve
  c1c  only the long boxes (those whose 5 x box exceeds 2 d: 10, 12, 15, 20 h) get their own curve: biweight window 5 x box; boxes up to 8 h keep the 2 d curve unchanged (window length set from a synthetic depth-kept curve, plan section 7)
  c2   step test without its data-cover rule (that duplicates the gap rule; phase A showed every 8 h step flag came from it); a side with no data is not judged
"""
import os

ON = frozenset(x for x in os.environ.get("VESPER_OPTS", "").replace("+", ",").split(",") if x)
KNOWN = {"c1a", "c1b", "c1c", "c2"}
assert ON <= KNOWN, f"unknown VESPER_OPTS switch: {sorted(ON - KNOWN)}"
