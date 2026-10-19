"""Summarise coverage_sample_*.csv. Counts 'new' sectors as 83-108 (S108 = newest with FFIs complete enough
for TESScut); S109 (partial early release) and S1751 (7-day 3I/ATLAS comet pointing) reported separately.
Run: py -3.12 -I coverage_summary.py"""
import csv, glob, math, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CUT = {'TTT vetted EBs (table3+4)': 82, 'TTT unvetted NN candidates (table2)': 82, 'Prsa 2022 TESS-EBs': 26}


def pct(k, n):
    p = k / n
    return f'{100*p:.0f}% (+/-{100*math.sqrt(p*(1-p)/n):.0f})'


def window(s, lo, hi):
    return [x for x in s if lo <= x <= hi]


def demo():
    assert window([1, 82, 83, 99, 108, 109, 1751], 83, 108) == [83, 99, 108]
    assert pct(50, 100) == '50% (+/-5)'


demo()
by = {}
for f in sorted(glob.glob(os.path.join(HERE, 'coverage_sample_*.csv'))):
    for r in csv.DictReader(open(f, encoding='utf-8')):
        if r['sectors'] != 'ERROR':
            by.setdefault(r['set'], []).append([int(x) for x in r['sectors'].split()])

for name, rows in by.items():
    n, cut = len(rows), CUT[name]
    print(f'## {name}  (n = {n}, catalogue cutoff S{cut})')
    for lo in sorted({cut + 1, 83}):
        new = [window(s, lo, 108) for s in rows]
        k = [len(x) for x in new]
        print(f'- sectors S{lo}-S108: >=1 new sector: {pct(sum(1 for x in k if x), n)}; '
              f'>=5: {pct(sum(1 for x in k if x >= 5), n)}; mean {sum(k)/n:.2f} per star; max {max(k)}')
    roll = [len(window(s, 97, 107)) for s in rows]
    print(f'- EM3 long-stare block S97-107: >=1: {pct(sum(1 for x in roll if x), n)}; '
          f'>=6 of these 11 sectors: {pct(sum(1 for x in roll if x >= 6), n)}; max {max(roll)}')
    print(f'- also in partial S109: {sum(1 for s in rows if 109 in s)}; in comet S1751: {sum(1 for s in rows if 1751 in s)}; '
          f'never observed by TESS: {sum(1 for s in rows if not s)}; mean total sectors (S1-108): '
          f'{sum(len(window(s, 1, 108)) for s in rows)/n:.1f}')
    print()
