"""Independent count-only S1 audit; no pipeline imports. Python -I -B."""
from pathlib import Path
from math import comb, sqrt
from functools import lru_cache
import itertools
import json
import re
import numpy as np

ROOT = Path(r"D:\second-sun-astra")
OUT = ROOT / "data/astra/002/statistics.json"
BARS = (7, 8, 10, 12)

@lru_cache(maxsize=100000)
def exact(tables):
    # Enumerate joint integer weights over small reference-sample counts.
    # Count reference real events <= observed, equivalent to sealed >= observed.
    distributions, denominator, observed = [], 1, 0
    for rs, fs, rr, fr in tables:
        total, real, draw = rs + fs + rr + fr, rs + rr, rr + fr
        denominator *= comb(total, draw)
        observed += rr
        distributions.append([(x, comb(real, x) * comb(total-real, draw-x))
                              for x in range(max(0, draw-(total-real)), min(draw, real)+1)])
    weights = {0: 1}
    for distribution in distributions:
        new = {}
        for a, wa in weights.items():
            for b, wb in distribution:
                if a+b <= observed:
                    new[a+b] = new.get(a+b, 0) + wa*wb
        weights = new
    return sum(weights.values()) / denominator

def expected(tables):
    return sum((rs+fs)*rr/(rr+fr) if rr+fr else 0 for rs, fs, rr, fr in tables)

def main():
    rng = np.random.default_rng(20261113)
    base = ROOT / 'research/stage3'
    ref = {}
    for name, bar, bin_, r, f in re.findall(r'REFBIN (g[23]) recovered bar (\d+) bin (\d+) real (\d+) flip (\d+)', (base/'R1-S1-REFERENCE-BINS.txt').read_text(encoding='utf-8')):
        ref[name, int(bar), int(bin_)] = (int(r), int(f))
    report = {}
    for name in ('g3', 'g2'):
        source = (base/f'R1-RESULT-{name}.txt').read_text(encoding='utf-8')
        tables, checks = {}, []
        for bar, filed, pairs in re.findall(r'bar\s+(\d+): sealed real.*?chance ([0-9.]+)\s+per bin sealed real/upside-down: ([0-9/ ]+)', source):
            bar = int(bar)
            tables[bar] = tuple((int(r), int(f), *ref[name, bar, k]) for k, (r,f) in enumerate(re.findall(r'(\d+)/(\d+)', pairs)))
            sampled = np.zeros(100000, dtype=int)
            for rs, fs, rr, fr in tables[bar]:
                sampled += rng.hypergeometric(rs+rr, fs+fr, rs+fs, size=len(sampled))
            p = exact(tables[bar])
            mc = float(np.mean(sampled >= sum(t[0] for t in tables[bar])))
            assert abs(p-float(filed)) <= 0.000051
            assert abs(mc-p) < 5*sqrt(p*(1-p)/len(sampled))
            checks.append(dict(bar=bar, filed=float(filed), exact=p, permutation=mc, expected=expected(tables[bar])))
        weights = np.array([r+f for r,f,_,_ in tables[7]], dtype=float)
        weights /= weights.sum()
        curve = []
        for dose in range(0, 201, 5):
            hits = 0
            for added in rng.multinomial(dose, weights, size=500):
                planted = {bar: tuple((r+int(n),f,rr,fr) for (r,f,rr,fr),n in zip(tables[bar],added)) for bar in BARS}
                hits += exact(planted[7]) <= 0.005 and all(sum(t[0] for t in planted[b]) > expected(planted[b]) for b in BARS[1:])
            curve.append(dict(added=dose, probability=hits/500))
        crossings = {}
        for probability in (0.5, 0.9):
            first = next((x for x in curve if x['probability'] >= probability), None)
            crossings[str(probability)] = None if first is None else dict(**first, total_real=sum(t[0] for t in tables[7])+first['added'], multiple=(sum(t[0] for t in tables[7])+first['added'])/expected(tables[7]))
        report[name] = dict(checks=checks, crossings=crossings, curve=curve)
        print(json.dumps(dict(campaign=name, checks=checks, crossings=crossings)), flush=True)
    OUT.write_text(json.dumps(report, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
