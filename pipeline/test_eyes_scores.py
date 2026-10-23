"""Tests the reader's saving and the report (no cloud, no key needed): test rounds are ignored, the file is deterministic, the numbers in the report are right.
Usage: python test_eyes_scores.py"""
import json, pathlib, subprocess, sys, tempfile
import eyes_scores as S

D = pathlib.Path(r"D:\second-sun\.cache\t_eyes_scores"); D.mkdir(parents=True, exist_ok=True)


def entry(i, kind, truth, ans, ok, bin_):
    return dict(i=i, kind=kind, truth=truth, ans=ans, ok=ok, bin=bin_, ms=1000, lb=0, m=None)


def rnd(rid, t0, mode, entries, status="done", source="practice-toi1338-s98", label="iPhone"):
    return dict(v=1, id=rid, mode=mode, source=source, n=len(entries), t0=t0, t1=t0 + 60000, status=status, device=dict(id="d1", label=label), a=entries, s=None)


A = [entry(0, "quiet", "none", "none", True, True), entry(1, "dip2500", "dip", "dip", True, True), entry(2, "dip1500", "dip", "none", False, False)]
rounds = [rnd("b", 1761500000000, "practice", A), rnd("a", 1761400000000, "practice", A[:1]), rnd("c", 1761600000000, "practice", A, source="e2e-x"), rnd("d", 1761700000000, "practice", A, label="E2E-test")]
assert [S.is_test(r) for r in rounds] == [False, False, True, True], "end-to-end test rounds must be ignored"
keep = [r for r in rounds if not S.is_test(r)]
f = D / "rounds.jsonl"
assert S.save(f, keep) is True, "first save writes the file"
assert S.save(f, list(reversed(keep))) is False, "same rounds in any order give an identical file (no spurious changes)"
lines = f.read_text(encoding="utf-8").splitlines()
assert [json.loads(l)["id"] for l in lines] == ["a", "b"], "sorted by time"
out = subprocess.run(["node", r"D:\second-sun\book\tools\eyes_report.mjs", str(f)], capture_output=True, text=True, encoding="utf-8").stdout
for want in ["2 practice, 0 test, 0 real", "PRACTICE: 2 round(s), 4 curves: 3 right, 1 wrong, 0 not sure (75% right)", "clear dips found 1/1 (100%)",
             "faint dips found 0/1 (0%)", "quiet curves called a dip 0/2 (0%)", "Not enough yet"]:
    assert want in out, f"report is missing: {want!r}\n{out}"
assert S.save(f, keep + [rnd("e", 1761800000000, "practice", A)]) is True, "a new round changes the file"
nothing = D / "nothing.jsonl"
assert S.save(nothing, []) is False and not nothing.exists(), "no rounds must not create an empty file"
empty = subprocess.run(["node", r"D:\second-sun\book\tools\eyes_report.mjs", str(D / "none.jsonl")], capture_output=True, text=True).stdout
assert "No Eyes rounds in the cloud yet" in empty
print("eyes_scores checks passed: test rounds ignored, deterministic file, report numbers right, empty case handled")
