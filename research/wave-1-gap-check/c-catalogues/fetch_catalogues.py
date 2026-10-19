"""Download the small EB catalogue tables (each < 100 MB) to D:\\second-sun\\data\\wave-1\\<dir>\\
and append one row per file to D:\\second-sun\\research\\downloads.csv with the MEASURED size.
Skips files already on disk. Run: py -3.12 -I fetch_catalogues.py"""
import csv, datetime, os, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
DATA = r'D:\second-sun\data\wave-1'
LOG = r'D:\second-sun\research\downloads.csv'
CDS = 'https://cdsarc.cds.unistra.fr/ftp/'
LIMIT = 100 * 1024 * 1024

# (dest dir, url, what, why)
FILES = []
def cds(d, cat, names, what, why):
    for n in names:
        FILES.append((d, CDS + cat + '/' + n, f'{what}: {n}', why))

cds('prsa2022_tess-ebs', 'J/ApJS/258/16', ['ReadMe', 'tess-ebs.dat.gz'],
    'Prsa+2022 TESS EB catalogue S1-26 (VizieR J/ApJS/258/16)', 'baseline TESS EB list, 2-min LCs')
cds('kostov2025_ttt', 'J/ApJS/279/50', ['ReadMe', 'table2.dat.gz', 'table3.dat.gz', 'table4.dat'],
    'Kostov+2025 TESS Ten Thousand S1-82 FFI (VizieR J/ApJS/279/50)', 'newest big TESS FFI EB catalogue + 872,720 unvetted NN candidates')
cds('ijspeert2021_oba', 'J/A+A/652/A120', ['ReadMe', 'eb-cat.dat.gz'],
    'IJspeert+2021 OBA EB candidates (VizieR J/A+A/652/A120)', 'hot-star TESS EB list')
cds('ijspeert2024_obaf', 'J/A+A/691/A242', ['ReadMe', 'obaf-eb1.dat.gz'],
    'IJspeert+2024 TESS OBAF EB catalogue (VizieR J/A+A/691/A242)', 'largest O-F TESS EB list')
cds('tang2025_eccentric', 'J/AJ/170/356', ['ReadMe', 't1mrt.dat'],
    'Tang+2025 TESS eccentric EBs (VizieR J/AJ/170/356)', 'eccentric EB list')
cds('shi2022_ea', 'J/ApJS/259/50', ['ReadMe', 'table1.dat'],
    'Shi+2022 TESS EA-type EBs (VizieR J/ApJS/259/50)', 'detached EB list')
cds('justesen2021_south', 'J/ApJ/912/123', ['ReadMe', 'table2.dat', 'table3.dat'],
    'Justesen & Albrecht 2021 southern TESS EBs (VizieR J/ApJ/912/123)', 'southern TESS EB list with parameters')
cds('kirk2016_kepler-ebs', 'J/AJ/151/68', ['ReadMe', 'catalog.dat.gz'],
    'Kirk+2016 Kepler EB catalogue 3rd rev, 2016 snapshot (VizieR J/AJ/151/68)', 'Kepler EB list (paper version)')
cds('conroy2014_k2-eng', 'J/PASP/126/914', ['ReadMe', 'table2.dat'],
    'Conroy+2014 K2 engineering EBs (VizieR J/PASP/126/914)', 'K2 EB list')
cds('lacourse2015_k2-c0', 'J/MNRAS/452/3561', ['ReadMe', 'table1.dat', 'table2.dat'],
    'LaCourse+2015 K2 C0 EBs (VizieR J/MNRAS/452/3561)', 'K2 EB list')
FILES.append(('villanova_kepler-ebs_live', 'https://keplerebs.villanova.edu/?format=file_csv',
              'Villanova Kepler EB catalogue live CSV (3rd revision, updated 2019-08-08)', 'current Kepler EB list (2920 rows on site)'))

new = not os.path.exists(LOG) or os.path.getsize(LOG) == 0
with open(LOG, 'a', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    for d, url, what, why in FILES:
        name = 'keplerebs_live.csv' if 'villanova' in url else url.rsplit('/', 1)[-1]
        dest = os.path.join(DATA, d, name)
        if os.path.exists(dest):
            print('skip (exists)', dest); continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        req = urllib.request.Request(url, headers={'User-Agent': 'second-sun-research/0.1 python-urllib'})
        with urllib.request.urlopen(req, timeout=300) as r:
            size = int(r.headers.get('Content-Length') or 0)
            if size > LIMIT:
                print('SKIP >100MB', url, size); continue
            body = r.read()
        if len(body) > LIMIT:
            print('SKIP >100MB', url, len(body)); continue
        if b'not a bot' in body[:4000]:  # CDS Anubis challenge page, not data
            print('BLOCKED (bot challenge)', url); continue
        open(dest, 'wb').write(body)
        n = os.path.getsize(dest)
        w.writerow([datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    what, url, n, dest, why, '1c'])
        f.flush()
        print(f'{n:>12,}  {dest}')
