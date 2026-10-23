"""Tests Ahmed's published Firestore rules from the outside (a good write must work; reads, changes, deletes and junk must be refused),
then proves the admin reader sees the good document and cleans up after itself. Test documents have source 'e2e-rules-test' and are deleted at the end.
Usage: python eyes_rules_test.py"""
import copy, time
import requests
import eyes_firestore as F

RUN = f"rt{int(time.time())}"
GOOD = dict(v=1, id="", mode="practice", source="e2e-rules-test", n=2, t0=1761000000000, t1=1761000060000, status="done",
            device={"id": "testdev", "label": ""}, a=[dict(i=0, kind="quiet", truth="none", ans="none", ok=True, bin=True, ms=1000, lb=0, m=None),
                                                       dict(i=1, kind="dip2500", truth="dip", ans="dip", ok=True, bin=True, ms=1500, lb=0, m=dict(w=5, a=40, d=30, depth=2500))],
            s=dict(n=2, right=2, wrong=0, unsure=0))
made, results = [], []


def doc(i, **change):
    d = copy.deepcopy(GOOD); d["id"] = f"{RUN}-{i}"; d.update(change); return d


def create(i, **change):
    d = doc(i, **change); r = F.public_create(d["id"], d);
    if r.status_code == 200: made.append(d["id"])
    return r


def check(name, ok, detail=""):
    results.append(ok); print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


r = create(1)
check("a good round is accepted", r.status_code == 200, r.status_code)
r2 = F.public_create(f"{RUN}-1", doc(1))
check("the same round sent twice does not overwrite (second attempt is refused)", r2.status_code in (403, 409), f"status {r2.status_code}: {r2.json().get('error', {}).get('status')}")
dup_status = r2.status_code
check("junk: an extra field is refused", create(2, extra="x").status_code == 403)
check("junk: an unknown mode is refused", create(3, mode="bogus").status_code == 403)
check("junk: an id that does not match the document id is refused", F.public_create(f"{RUN}-4", doc(4, id="other")).status_code == 403)
check("junk: n above 200 is refused", create(5, n=300).status_code == 403)
check("junk: answers that are not a list are refused", create(6, a="text").status_code == 403)
check("junk: version 2 is refused", create(7, v=2).status_code == 403)
check("junk: more than 200 answers is refused", create(8, n=2, a=[GOOD["a"][0]] * 201).status_code == 403)
url = f"{F.BASE}/{F.COLLECTION}/{RUN}-1"
check("nobody can read a round with the public key", requests.get(url, params={"key": F.API_KEY}, timeout=30).status_code == 403)
check("nobody can list the rounds with the public key", requests.get(f"{F.BASE}/{F.COLLECTION}", params={"key": F.API_KEY}, timeout=30).status_code == 403)
check("nobody can change a round with the public key", requests.patch(url, params={"key": F.API_KEY}, json=F.doc_body(doc(1, n=3)), timeout=30).status_code == 403)
check("nobody can delete a round with the public key", requests.delete(url, params={"key": F.API_KEY}, timeout=30).status_code == 403)
check("a collection other than eyes_rounds is closed", requests.post(f"{F.BASE}/other", params={"documentId": "x", "key": F.API_KEY}, json=F.doc_body(doc(9)), timeout=30).status_code == 403)
rounds = [x for x in F.list_rounds() if x["id"].startswith(RUN)]
check("the admin reader sees exactly the one good round, unchanged", len(rounds) == 1 and rounds[0] == doc(1), f"{len(rounds)} found")
for i in made:
    F.admin_delete(i)
left = [x for x in F.list_rounds() if x["id"].startswith(RUN)]
check("test rounds were cleaned up", not left)
print(f"duplicate-send status was {dup_status}")
print("ALL RULES CHECKS PASSED" if all(results) else f"{results.count(False)} CHECK(S) FAILED")
raise SystemExit(0 if all(results) else 1)
