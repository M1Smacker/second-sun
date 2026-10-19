"""Ground-truth set: for each transiting circumbinary-planet host, which TESS sectors and cadences exist.
Reads hosts (name, TIC, RA, Dec) from 1a's NASA Exoplanet Archive pull; no light curves downloaded.
 - TESScut sector endpoint -> sectors whose FFIs cover the position (FFI cadence by era: 30 min S1-26,
   10 min S27-55, 200 s S56+)
 - MAST CAOM (Mast.Caom.Filtered, target_name = TIC) -> 2-min / 20-s SPOC data and HLSP light curves
Run: py -3.12 -I ground_truth.py > ground_truth_out.md"""
import csv, json, re, sys, time, urllib.parse, urllib.request
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
UA = {'User-Agent': 'second-sun-research/0.1 python-urllib'}
NEA = r'D:\second-sun\data\wave-1\nea_pscomppars_cbflag1.csv'


def get(url, data=None, key=None):
    for attempt in range(4):
        req = urllib.request.Request(url, data=data, headers=UA)
        r = json.loads(urllib.request.urlopen(req, timeout=120).read())
        if key is None or key in r:
            return r
        print(f'<!-- retry {attempt}: {str(r)[:200]} -->', file=sys.stderr)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'MAST gave no {key!r}: {str(r)[:300]}')


def tesscut_sectors(ra, dec):
    r = get(f'https://mast.stsci.edu/tesscut/api/v0.1/sector?ra={ra}&dec={dec}&radius=0m')
    return sorted({int(x['sector']) for x in r['results']})


def caom(tic):
    req = {'service': 'Mast.Caom.Filtered', 'format': 'json', 'pagesize': 5000, 'page': 1,
           'params': {'columns': 'obs_collection,provenance_name,sequence_number,t_exptime,dataproduct_type,obs_id',
                      'filters': [{'paramName': 'target_name', 'values': [str(tic)]},
                                  {'paramName': 'obs_collection', 'values': ['TESS', 'HLSP']}]}}
    body = urllib.parse.urlencode({'request': json.dumps(req)}).encode()
    return get('https://mast.stsci.edu/api/v0/invoke', body, 'data')['data']


def ffi_cadence(s):
    return '30m' if s <= 26 else '10m' if s <= 55 else '200s'


def demo():  # tiny self-check of the cadence-era logic
    assert [ffi_cadence(s) for s in (1, 26, 27, 55, 56, 107)] == ['30m', '30m', '10m', '10m', '200s', '200s']


if __name__ == '__main__':
    demo()
    hosts = {}
    for r in csv.DictReader(open(NEA, encoding='utf-8')):
        if r['discoverymethod'] == 'Transit':
            hosts[r['hostname']] = (r['tic_id'].replace('TIC ', ''), r['ra'], r['dec'])
    # Davies+ 2026 single-event candidate (not in the archive): TIC id only, coords resolved via CAOM below
    extra = {'TIC 319011894 (Davies+2026 candidate)': '319011894'}
    print('| Host | TIC | FFI sectors (TESScut) | 2-min SPOC sectors | 20-s sectors | HLSP light curves (sectors) |')
    print('|---|---|---|---|---|---|')
    for name, (tic, ra, dec) in list(hosts.items()) + [(k, (v, None, None)) for k, v in extra.items()]:
        rows = caom(tic)
        spoc = defaultdict(set)
        for x in rows:
            if x['dataproduct_type'] != 'timeseries' or x['sequence_number'] is None:
                continue
            # SPOC single-sector LC ids look like tess2019198215352-s0014-0000000272369124-0150-s;
            # multi-sector search products (s0014-s0086) are skipped
            if x['obs_collection'] == 'TESS' and not re.search(r'-s\d{4}-\d{16}-\d{4}-[a-z](_fast)?$', x['obs_id'] or ''):
                continue
            exp = round(float(x['t_exptime'] or 0)) if x['obs_collection'] == 'TESS' else 0
            key = (x['obs_collection'], x['provenance_name'], exp)
            spoc[key].add(int(x['sequence_number']))
        two = sorted(set().union(*[v for k, v in spoc.items() if k[0] == 'TESS' and k[2] == 120] or [set()]))
        twenty = sorted(set().union(*[v for k, v in spoc.items() if k[0] == 'TESS' and k[2] == 20] or [set()]))
        hl = '; '.join(f"{k[1]}: {','.join(map(str, sorted(v)))}" for k, v in sorted(spoc.items()) if k[0] == 'HLSP')
        if ra is None:  # position for TESScut from the TIC via MAST
            q = {'service': 'Mast.Catalogs.Filtered.Tic', 'format': 'json', 'params': {
                'columns': 'ID,ra,dec', 'filters': [{'paramName': 'ID', 'values': [tic]}]}}
            t = get('https://mast.stsci.edu/api/v0/invoke',
                    urllib.parse.urlencode({'request': json.dumps(q)}).encode(), 'data')['data'][0]
            ra, dec = t['ra'], t['dec']
        ffi = tesscut_sectors(ra, dec)
        ffi_s = ', '.join(f'{s}' for s in ffi) or 'none'
        print(f"| {name} | {tic} | {ffi_s} | {', '.join(map(str, two)) or 'none'} | "
              f"{', '.join(map(str, twenty)) or 'none'} | {hl or 'none'} |")
        sys.stdout.flush()
        time.sleep(1)
