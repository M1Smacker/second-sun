"""Tests for gate_judge (FIX 87). Run: python pipeline/test_gate_judge.py"""
import math, sys
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0] if ("/" in __file__ or "\\" in __file__) else ".")
from gate_judge import judge

B = ["5-10", "10-14", "14-20", "20-27.4", "over 27.4"]
ok = lambda *ms: dict(zip(B, ms))
assert judge(ok(1, 1, 0.97, 0.99, 1.2))[0] == "PASS"
assert judge(ok(1, 1, 0.94, 0.99, 1.2))[0] == "FAIL"
# the FIX 87 case: sealed G3, the two slow bins had no injections
s, line = judge(ok(1, 1, 1, None, None))
assert s == "PASS ON TESTED BINS" and "3 of 5" in line and "20-27.4" in line and "over 27.4" in line, line
assert judge(ok(1, 1, 1, None, None), require_all=True)[0] == "INCOMPLETE"
# undefined ratio is not a pass
s, line = judge(ok(1, 1, 1, 1, math.nan))
assert s == "PASS ON TESTED BINS" and "not judged" in line
# a failure wins over missing coverage
assert judge(ok(0.5, None, None, None, None))[0] == "FAIL"
# nothing tested at all is never PASS
assert judge(ok(None, None, None, None, None))[0] == "PASS ON TESTED BINS"
assert judge(ok(None, None, None, None, None), require_all=True)[0] == "INCOMPLETE"
print("test_gate_judge: all passed")
