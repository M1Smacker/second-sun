"""T130 check of the Eyes numbers on the 27 Oct field note (14 Nov 2026). Reads research/eyes-scores/rounds.jsonl (Ahmed's own saved rounds,
read from the cloud earlier; counts only, nothing new is fetched). Prints: finished rounds and curves at round 25; deep (4,000 ppm) dips
answered "odd" in the first five finished rounds and after; first standard sitting test scores; accuracy by third of a round over the
first 25 finished rounds; the Wilson 95% upper bound for 0 false alarms on 32 and 35 quiet curves."""
import json
from pathlib import Path
R = [json.loads(l) for l in open(Path(r"D:\second-sun\research\eyes-scores\rounds.jsonl"), encoding="utf-8")]
D = sorted([r for r in R if r["status"] == "done"], key=lambda r: r["t0"])
print("finished rounds at 25:", 25, "curves", sum(len(r["a"]) for r in D[:25]))
odd = lambda r: sum(1 for a in r["a"] if a["truth"] == "dip" and a["ans"] == "odd" and a["kind"] == "dip4000")
print("deep dips called odd: first five rounds", sum(odd(r) for r in D[:5]), "| rounds 6 to 25", sum(odd(r) for r in D[5:25]))
S = [r for r in D[:12] if r["mode"] == "test"]
pct = lambda rs: round(100 * sum(a["ok"] for r in rs for a in r["a"]) / sum(len(r["a"]) for r in rs), 1)
print("first sitting tests:", len(S), "first two", pct(S[:2]), "| from the fourth on", [round(100 * sum(a["ok"] for a in r["a"]) / len(r["a"])) for r in S[3:]])
t = [[0, 0], [0, 0], [0, 0]]
for r in D[:25]:
    n = len(r["a"])
    for a in r["a"]:
        k = min(2, a["i"] * 3 // n); t[k][0] += a["ok"]; t[k][1] += 1
print("thirds of a round, first 25 rounds (first, middle, last):", [round(100 * a / b, 1) for a, b in t])
z2 = 1.959964 ** 2
for n in (32, 35):
    print(f"Wilson 95% upper bound, 0 of {n}: {100 * z2 / (n + z2):.1f}%")
