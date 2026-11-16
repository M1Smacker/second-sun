"""Design-only sector census and four-source fallback radius inventory."""
from collections import Counter, defaultdict
import csv
import importlib
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('026_harness')
D = importlib.import_module('026_inputs')
M = importlib.import_module('026_rules')


def main():
    os.environ.update(SS_SET='g2', VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    import petrova_mask as PM
    from astropy.io import fits
    summaries = {}
    for campaign in ('g2', 'g3'):
        catalogue = PM.load_catalogue(campaign, H.ROOT / f'targets/{campaign}_chain_targets.csv')
        old = set(map(int, json.loads(D.read(guard, H.DATA / f'astra/010/affected-{campaign}.json', '010'))))
        assert old <= {int(x) for x in guard.seen[campaign]}
        source = H.DATA / f'stage3_{campaign}' / f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        groups, times = {}, {}
        for kind in D.KINDS:
            for path in sorted((source / kind).glob('*.json')):
                star, sector = map(int, path.stem.split('_'))
                if str(star) not in guard.seen[campaign]:
                    continue
                guard.allow_design_file(path)
                row = json.loads(path.read_text(encoding='utf-8'))
                assert row['tic'] == star and row['sector'] == sector
                item = groups.setdefault((star, sector), dict(star=star, sector=sector, products=[]))
                item['products'].append(dict(kind=kind, path=str(path)))
                item['blanked'] = item.get('blanked', False) or any(m['status'] == 'too little data after masking' for m in row['meta'])
                if sector not in times:
                    for meta in row['meta']:
                        file = H.DATA / campaign / str(star) / Path(meta['file'].removesuffix('::sap')).name
                        guard.allow_design_file(file)
                        with fits.open(file, memmap=False, lazy_load_hdus=True) as hdus:
                            for hdu in hdus[:2]:
                                h = hdu.header
                                if 'TSTART' in h and 'TSTOP' in h:
                                    time = (float(h['TSTART']) + float(h['TSTOP'])) / 2 + float(h.get('BJDREFI', 2457000)) + float(h.get('BJDREFF', 0)) - 2457000
                                    if 1300 < time < 10000:
                                        times[sector] = time
                                        break
                        if sector in times:
                            break
        assert all(s in times for _, s in groups)
        sets = defaultdict(set)
        categories = Counter()
        for (star, sector), item in groups.items():
            c = catalogue.get(star)
            time = times[sector]
            cls = M.category(c, time)
            item.update(category=cls, time=time, historical_m2=star in old)
            categories[cls] += 1
            if item['blanked']:
                sets['blanked'].add(star)
            # The original 010 timing selection did not require a finite width.
            if c is not None and all(math.isfinite(c.get(k, math.nan)) for k in ('P', 'T0')):
                if M.drift(c, time) > .5:
                    sets['high'].add(star)
            if cls == 'unknown':
                continue
            padding = M.drift(c, time)
            if cls == 'B':
                sets['B'].add(star)
            ws = c['ws'] if math.isfinite(c['ws']) and math.isfinite(c['phs']) else c['wp']
            full = min(1., (1.5 * c['wp'] + 2 * padding) / c['P']) + min(1., (1.5 * ws + 2 * padding) / c['P'])
            if full > .25:
                sets['quarter_full'].add(star)
            if 4 * padding / c['P'] > .25:
                sets['quarter_drift'].add(star)
        selected = sets['high'] | sets['blanked']
        summaries[campaign] = dict(sectors=len(groups), categories=dict(categories), saved010=len(old),
            recomputed010=len(selected), roster_difference=len(old ^ selected), class_b_stars=len(sets['B']),
            new_class_b_stars=len(sets['B'] - old), quarter_full=len(sets['quarter_full']),
            quarter_drift=len(sets['quarter_drift']), old_only=len(old - sets['quarter_full']),
            quarter_only=len(sets['quarter_full'] - old), overlap=len(old & sets['quarter_full']),
            symmetric_difference=len(old ^ sets['quarter_full']))
        (H.OUT / f'inventory-{campaign}.json').write_text(json.dumps(list(groups.values())), encoding='utf-8')
    # Catalogue-only reads, restricted to permitted design hosts before use.
    all_seen = set.union(*[{int(s) for s in v} for v in guard.seen.values()])
    candidates = defaultdict(list)
    for file, id_column, columns in (
        (H.DATA / 'fix96_radii_2026-11-15/tic82.csv', 'ID', ('rad',)),
    ):
        guard.reads.add(file.resolve())
        with file.open(encoding='utf-8-sig') as f:
            ticrows = list(csv.DictReader(f))
        for row in ticrows:
            star = int(row[id_column])
            if star not in all_seen:
                continue
            for col in columns:
                try:
                    value = float(row[col])
                except (ValueError, TypeError):
                    continue
                if math.isfinite(value) and value > 0:
                    candidates[star].append(value)
    file = H.DATA / 'fix96_radii_2026-11-15/gaia_dr3.csv'
    guard.reads.add(file.resolve())
    with file.open(encoding='utf-8-sig') as f:
        gaiarows = list(csv.DictReader(f))
    def number(r, k, default=99.):
        try:
            v = float(r[k])
            return v if math.isfinite(v) else default
        except (ValueError, TypeError):
            return default
    gaiarows.sort(key=lambda r: number(r, 'angular_distance') + abs(number(r, 'magnitude_difference')))
    by_gaia = {}
    for row in gaiarows:
        by_gaia.setdefault(row['dr2_source_id'], row)
    for row in ticrows:
        star = int(row['ID'])
        if star not in all_seen:
            continue
        gaia = by_gaia.get(row.get('GAIA', ''))
        if gaia:
            for col in ('radius_gspphot', 'radius_flame'):
                value = number(gaia, col, math.nan)
                if math.isfinite(value) and value > 0:
                    candidates[star].append(value)
    radii = {}
    with (H.ROOT / 'targets/host_radii_g2_g3.csv').open(encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row['set'] not in guard.seen or row['tic'] not in guard.seen[row['set']]:
                continue
            radius = number(row, 'radius_rsun', math.nan)
            if math.isfinite(radius) and radius > 0:
                radii[row['set'], int(row['tic'])] = radius
    fallback, missing = {}, 0
    for campaign, seen in guard.seen.items():
        for star in map(int, seen):
            if (campaign, star) not in radii:
                missing += 1
                if candidates[star]:
                    fallback[f'{campaign}:{star}'] = min(candidates[star])
    (H.OUT / 'fallback-radii.json').write_text(json.dumps(fallback), encoding='utf-8')
    summaries['fallback'] = dict(missing_header_hosts=missing, supplied_hosts=len(fallback),
                                  still_missing=missing - len(fallback))
    (H.OUT / 'inventory-summary.json').write_text(json.dumps(summaries, indent=2), encoding='utf-8')
    print(json.dumps(summaries, indent=2))


if __name__ == '__main__':
    main()
