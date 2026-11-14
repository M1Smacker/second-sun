"""Offline checks of the novelty verdict rule (T127): python test_novelty_check.py (prints ok). No network: the sources are replaced by stubs."""
import novelty_check as N

no = lambda tic: dict(hit=False, evidence=[])
yes = lambda tic: dict(hit=True, evidence=["TOI 1.01 (PC)"])
def boom(tic):
    raise TimeoutError("archive down")
arx = lambda tic, names=(): dict(hit=False, evidence=[], searched=[f"TIC {tic}", *names])

r = N.check(5, dict(a=no, b=no, arxiv=arx))
assert r["verdict"] == "NO HIT" and r["failed"] == [] and "Not asked" in r["sentence"], r
r = N.check(5, dict(a=no, b=boom, arxiv=arx))
assert r["verdict"] == "INCOMPLETE" and r["failed"] == ["b"] and "not counted as no hit" in r["sentence"], r   # a failure is never "novel"
r = N.check(5, dict(a=yes, b=boom, arxiv=arx))
assert r["verdict"] == "KNOWN" and r["hits"] == ["a"], r                                                        # a hit wins even if another source failed
assert r["sources"]["arxiv"]["searched"] == ["TIC 5", "TOI-1"], r["sources"]["arxiv"]                          # names found earlier are searched on arXiv
assert set(N.names_from({"x": dict(evidence=["TOI-1338 b (cb_flag 1, TESS 2020)", "TOI-1338 otype SB* refs 77", "TOI 1338.01"])})) == {"TOI-1338"}
assert set(N.names_from({"x": dict(evidence=["Kepler-16 b (cb_flag 1, Kepler 2011)", "V* V1234 Cyg otype EB* refs 9", "TIC 5 otype * refs 1"])})) == {"Kepler-16", "V* V1234 Cyg"}
print("test_novelty_check ok")
