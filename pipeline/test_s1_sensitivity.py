"""FIX 86 acceptance (Claude, 14 Nov 2026): (1) strat_exact on the filed tables reproduces the 8 filed chances; (2) the sensitivity
crossings reproduce Codex 002 part B (G3: 50% at 55 added, 90% at 60; G2: 60 and 70) within one grid step (Monte Carlo error at 500
placements is up to 2.2 points; we use 2,000 here); (3) mutation: an unstratified expectation must move the crossings.
Reads only the filed count files (no sealed light). Run from pipeline/: SS_SET=g3 python test_s1_sensitivity.py"""
import os, re, sys
from pathlib import Path
os.environ.setdefault("SS_SET", "g3"); os.environ.setdefault("VESPER_OPTS", "c6,p1"); os.environ.setdefault("SS_RUN", "x")
ROOT = Path(__file__).resolve().parents[1]
import s1_sensitivity as S
from r1_readout import strat_exact

ref = {(n, int(b), int(k)): (int(r), int(f)) for n, b, k, r, f in re.findall(r"REFBIN (g[23]) recovered bar (\d+) bin (\d+) real (\d+) flip (\d+)", (ROOT / "research/stage3/R1-S1-REFERENCE-BINS.txt").read_text(encoding="utf-8"))}
codex = {"g3": (55, 60), "g2": (60, 70)}
for name in ("g3", "g2"):
    src = (ROOT / f"research/stage3/R1-RESULT-{name}.txt").read_text(encoding="utf-8")
    tables = {}
    for bar, filed, pairs in re.findall(r"bar\s+(\d+): sealed real.*?chance ([0-9.]+)\s+per bin sealed real/upside-down: ([0-9/ ]+)", src):
        bar = int(bar)
        tables[bar] = [(int(r), int(f), *ref[name, bar, k]) for k, (r, f) in enumerate(re.findall(r"(\d+)/(\d+)", pairs))]
        assert abs(strat_exact(tables[bar]) - float(filed)) <= 0.000051, (name, bar)
    assert set(tables) == set(S.BARS)
    res, e7 = S.crossings(tables, strat_exact, n=2000)
    got = (res[0.5]["added"], res[0.9]["added"])
    assert all(abs(g - c) <= 5 for g, c in zip(got, codex[name])), (name, got, codex[name])
    print(name, "filed chances reproduced; crossings", got, "Codex", codex[name], f"expectation {e7:.2f}")
    print("  ", S.note(tables, strat_exact))
print("test_s1_sensitivity: all passed")
