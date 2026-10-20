r"""Checks for the mission readiness score. Run:  .venv-docs\Scripts\python.exe book\tools\test_mission.py
The real rubric must validate, and every rule must fail loudly when broken. Prints 'all mission checks passed'."""
import copy, csv, datetime, pathlib, sys, tempfile
import yaml
BOOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK))
import mission

REPO = BOOK.parent
real = yaml.safe_load((BOOK / "progress" / "mission.yml").read_text(encoding="utf-8"))
claims = {r["id"] for r in csv.DictReader(open(BOOK / "data" / "claims.csv", encoding="utf-8", newline=""))}
TODAY = datetime.date(2030, 1, 1)


def must_fail(mutate, needle):
    m = copy.deepcopy(real); mutate(m)
    try:
        mission.score(m, REPO, claims, 0, TODAY)
    except ValueError as e:
        assert needle in str(e), f"wrong error for {needle!r}: {e}"
        return
    raise AssertionError(f"rule not enforced: {needle}")


# 1. the real file passes, and an independent sum agrees with the function
r = mission.score(real, REPO, claims, 0, TODAY)
indep = sum(i["weight"] * (i.get("credit", 0)) for s in real["stages"] for i in s["items"] if not i.get("auto"))
assert abs(r["typed"] - indep) < 1e-9 and abs(r["total"] - r["typed"]) < 1e-9, (r["typed"], indep)   # no search rows, no candidates yet
assert sum(s["weight"] for s in r["stages"]) == 100 and 0 <= r["total"] <= 100
assert abs(sum(c["delta"] for c in r["changes"]) - r["typed"]) < 0.011

# 2. every rule fails loudly
must_fail(lambda m: m["stages"][0].update(weight=11), "not 100")
must_fail(lambda m: m["stages"][0]["items"][0].update(weight=5), "add up to")
must_fail(lambda m: m["stages"][0]["items"][0].update(credit=1.5), "outside 0 to 1")
must_fail(lambda m: m["stages"][0]["items"][0].update(credit=-0.1), "outside 0 to 1")
must_fail(lambda m: m["stages"][0]["items"][0].pop("evidence"), "no proof, no points")
must_fail(lambda m: m["stages"][0]["items"][0].update(evidence=["claim:F-9999"]), "not in data/claims.csv")
must_fail(lambda m: m["stages"][0]["items"][0].update(evidence=["file:nope/missing.txt"]), "no such file")
must_fail(lambda m: m["stages"][0]["items"][0].update(evidence=["hunch"]), "must start with")
must_fail(lambda m: m["stages"][1]["items"][4].update(credit=0.5), "no proof, no points")       # a zero-credit item cannot get points without evidence
must_fail(lambda m: m["changes"][0].update(delta=30), "Log every change")                       # credit moved without a matching log line
must_fail(lambda m: m["changes"].append(dict(date=datetime.date(2029, 1, 1), delta=0, why="")), "numeric delta and a reason")
must_fail(lambda m: m["changes"].append(dict(date=datetime.date(2031, 1, 1), delta=0, why="future")), "not in the future")
must_fail(lambda m: m["stages"][4]["items"][0].update(auto={"mystery": 1}), "unknown auto rule")

# 3. a credit change WITH a matching log line and evidence is accepted, and the total moves by exactly that
m = copy.deepcopy(real)
item = m["stages"][1]["items"][4]; item.update(credit=0.2, evidence=["file:pipeline/detect_v2.py"])
m["changes"].append(dict(date=datetime.date(2026, 10, 22), delta=1.0, why="test"))
r2 = mission.score(m, REPO, claims, 0, TODAY)
assert abs(r2["total"] - r["total"] - 1.0) < 1e-9, (r2["total"], r["total"])

# 4. auto items: rows of a results file and the candidate count move the score without any typed change
with tempfile.TemporaryDirectory() as td:
    td = pathlib.Path(td); (td / "targets").mkdir()
    for p in ("pipeline", "research", "book", "targets"):
        (td / p).mkdir(exist_ok=True)
    for ev in {e.partition(":")[2] for s in real["stages"] for i in s["items"] for e in (i.get("evidence") or []) if e.startswith("file:")}:
        q = td / ev; q.parent.mkdir(parents=True, exist_ok=True); q.mkdir(exist_ok=True) if "." not in q.name else q.write_text("x")
    base = mission.score(real, td, claims, 0, TODAY)["total"]
    (td / "targets" / "g1_searched.csv").write_text("# comment\ntic,done\n" + "\n".join(f"{i},1" for i in range(549)) + "\n", encoding="utf-8")
    full = mission.score(real, td, claims, 0, TODAY)
    assert abs(full["total"] - base - 25) < 1e-9, (full["total"], base)                           # 549 of 549 searched = +25 points
    (td / "targets" / "g1_searched.csv").write_text("tic,done\n1,1\n2,1\n", encoding="utf-8")
    assert abs(mission.score(real, td, claims, 0, TODAY)["total"] - base - 25 * 2 / 549) < 1e-9   # 2 of 549
    assert abs(mission.score(real, td, claims, 1, TODAY)["total"] - mission.score(real, td, claims, 0, TODAY)["total"] - 2) < 1e-9   # SS-0001 exists = +2
    assert full["typed"] == r["typed"]                                                            # auto points never touch the typed total
print("all mission checks passed; current score", round(r["total"], 2))
