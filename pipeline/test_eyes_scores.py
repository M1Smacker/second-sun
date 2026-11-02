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

# ---- rehearsal (rung 3): kept apart from the practice stats, and its pass line is read with the page's own code ----
def rh_entry(i, cls, tier, ans):
    return dict(i=i, cls=cls, tier=tier, ans=ans, ok=ans == cls, pc=ans == "planet", conf="medium", ms=1000, st=None, bx=6)


def rh_round(rid, day, status="done", planet_miss=0):
    es = [rh_entry(i, "planet", "clear", "planet") for i in range(3)] + [rh_entry(3 + i, "planet", "near", "planet" if i >= planet_miss else "noise") for i in range(3)]
    es += [rh_entry(6 + i, "eclipse", None, "eclipse") for i in range(14)]
    t0 = 1762000000000 + day * 86400000
    return rnd(rid, t0, "practice", es, status=status, source="rehearsal-v1")


rh = [rh_round(f"r{d}", d) for d in range(8)]
assert [S.is_rehearsal(r) for r in rh + keep] == [True] * 8 + [False] * 2, "only source rehearsal-v1 counts as a rehearsal round"
rf = D / "rehearsal.jsonl"
S.save(rf, rh + [rh_round("open", 9, status="open")])
rout = subprocess.run(["node", r"D:\second-sun\book\tools\rehearsal_report.mjs", str(rf)], capture_output=True, text=True, encoding="utf-8").stdout
for want in ["9 round(s) read, 1 not finished", "Sessions 8 of 8", "Clearly visible fake planets found: 24 of 24", "Not-planets called planet-like: 0 of 112"]:
    assert want in rout, f"rehearsal report is missing: {want!r}\n{rout}"
assert "On the numbers you meet the line" in rout, f"eight good sessions on eight days must meet the line\n{rout}"
worse = D / "rehearsal_bad.jsonl"
S.save(worse, [rh_round(f"b{d}", d) for d in range(7)] + [rh_round("b7", 7, planet_miss=0)])
bad_entries = [json.loads(l) for l in worse.read_text(encoding="utf-8").splitlines()]
for r in bad_entries[:7]:                                       # calling everything else a planet must turn the verdict to "below"
    for e in r["a"][6:]:
        e["ans"], e["ok"], e["pc"] = "planet", False, True
worse.write_text("".join(json.dumps(r) + "\n" for r in bad_entries), encoding="utf-8")
bout = subprocess.run(["node", r"D:\second-sun\book\tools\rehearsal_report.mjs", str(worse)], capture_output=True, text=True, encoding="utf-8").stdout
assert "Below the line" in bout, f"false alarms must show below the line\n{bout}"
none = subprocess.run(["node", r"D:\second-sun\book\tools\rehearsal_report.mjs", str(D / "nope.jsonl")], capture_output=True, text=True, encoding="utf-8").stdout
assert "no rehearsal rounds in the cloud yet" in none
print("eyes_scores checks passed: test rounds ignored, deterministic file, report numbers right, empty case handled, rehearsal rounds kept apart with the page's own pass line")
