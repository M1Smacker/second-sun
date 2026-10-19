"""Coverage-gap estimate: random samples of catalogued EBs -> TESScut sector list -> how many sectors
each star got AFTER its catalogue's cutoff. Writes coverage_sample.csv and prints a summary.
Run: py -3.12 -I coverage_sample.py [N per set] [set index 0-2]   (seeded, so reruns give the same sample)
ponytail: random sample + binomial error, not the full 10k/870k sets; full run = same loop, ~1 s/star."""
import csv, gzip, json, math, os, random, sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
D = r'D:\second-sun\data\wave-1'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'coverage_sample{}.csv')
UA = {'User-Agent': 'second-sun-research/0.1 python-urllib'}
N = int(sys.argv[1]) if len(sys.argv) > 1 else 250
ONLY = int(sys.argv[2]) if len(sys.argv) > 2 else None


def ws(path, opener=open):  # TIC RA Dec as the first three whitespace fields
    with opener(path, 'rt') as f:
        return [(int(p[0]), float(p[1]), float(p[2])) for p in (l.split() for l in f) if len(p) >= 3]


def prsa():
    with gzip.open(os.path.join(D, 'prsa2022_tess-ebs', 'tess-ebs.dat.gz'), 'rt') as f:
        rows = {int(p[0]): (float(p[5]), float(p[6])) for p in (l.split('|') for l in f)}
    return [(t, ra, de) for t, (ra, de) in rows.items()]


SETS = {  # name: (stars, cutoff sector)
    'TTT vetted EBs (table3+4)': (ws(os.path.join(D, 'kostov2025_ttt', 'table3.dat.gz'), gzip.open)
                                  + ws(os.path.join(D, 'kostov2025_ttt', 'table4.dat')), 82),
    'TTT unvetted NN candidates (table2)': (ws(os.path.join(D, 'kostov2025_ttt', 'table2.dat.gz'), gzip.open), 82),
    'Prsa 2022 TESS-EBs': (prsa(), 26),
}


def sectors(ra, dec):
    url = f'https://mast.stsci.edu/tesscut/api/v0.1/sector?ra={ra}&dec={dec}&radius=0m'
    for attempt in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
            return sorted({int(x['sector']) for x in r['results']})
        except Exception as e:  # transient MAST errors: back off and retry
            print('retry', attempt, e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    return None


def summary(name, cut, lists):
    ok = [s for s in lists if s is not None]
    n = len(ok)
    after = [[x for x in s if x > cut] for s in ok]
    frac = sum(1 for a in after if a) / n
    err = math.sqrt(frac * (1 - frac) / n)
    mean_new = sum(len(a) for a in after) / n
    print(f'{name}: n={n}, cutoff S{cut}: {100*frac:.1f}% +/- {100*err:.1f}% have >=1 sector after S{cut}; '
          f'mean {mean_new:.2f} new sectors/star (median {sorted(len(a) for a in after)[n//2]}); '
          f'mean total sectors {sum(len(s) for s in ok)/n:.2f}; never observed: {sum(1 for s in ok if not s)}')
    if cut < 82:
        a82 = [[x for x in s if x > 82] for s in ok]
        f82 = sum(1 for a in a82 if a) / n
        print(f'   ... and after S82: {100*f82:.1f}% have >=1 sector; mean {sum(map(len, a82))/n:.2f} sectors/star')


if __name__ == '__main__':
    with open(OUT.format('' if ONLY is None else f'_{ONLY}'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['set', 'tic', 'ra', 'dec', 'sectors'])
        for i, (name, (stars, cut)) in enumerate(SETS.items()):
            if ONLY is not None and i != ONLY:
                continue
            random.seed(20261019 + i)
            print(f'{name}: {len(stars)} stars in file', file=sys.stderr)
            got = []
            for tic, ra, dec in random.sample(stars, N):
                s = sectors(ra, dec)
                got.append(s)
                w.writerow([name, tic, ra, dec, ' '.join(map(str, s)) if s is not None else 'ERROR'])
                f.flush()
                time.sleep(0.3)
            summary(name, cut, got)
            sys.stdout.flush()
