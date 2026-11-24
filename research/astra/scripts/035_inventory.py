"""Inventory selected stars' existing SPOC 120-second files, counts only stdout.

No light arrays are read. FITS headers are opened only after sample/fence and
resolved-path checks. The private manifest carries file paths for continuation.
"""
import importlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('035_select')
from astropy.io import fits


def main():
    sample = json.loads((S.OUT/'sample.json').read_text(encoding='utf-8'))
    r1 = S.rows(S.ROOT/'targets/r1_targets.csv')
    forbidden = {int(r['tic']) for r in r1 if r['list'] == 'g1' or
                 (r['list'] in ('g2', 'g3') and r['design_seen'] == '0')}
    forbidden.update(int(r['tic']) for r in S.rows(S.ROOT/'targets/g1_targets.csv'))
    data = S.ROOT/'data'
    manifest, counts = [], [dict(stars=0, with_local=0, files=0, bytes=0) for _ in range(3)]
    rejected = dict(identity=0, cadence=0, product=0, unreadable=0)
    for row in sample['selected']:
        star = int(row['tic'])
        if star in forbidden:
            raise PermissionError('Selected star crosses fence')
        selected = {}
        for campaign in ('g2', 'g3'):
            folder = data/campaign/str(star)
            if folder.resolve() != data.resolve()/campaign/str(star):
                raise PermissionError('Input folder path escape')
            for path in sorted(folder.glob('*.fits')):
                if path.resolve().parent != folder.resolve():
                    raise PermissionError('FITS path escape')
                # SPOC target light curve names, exclude QLP and FFI products.
                if not path.name.startswith('tess') or not path.name.endswith('_lc.fits'):
                    rejected['product'] += 1
                    continue
                try:
                    with fits.open(path, memmap=False, lazy_load_hdus=True) as h:
                        head, ext = h[0].header, h[1].header
                        if int(head.get('TICID', -1)) != star:
                            rejected['identity'] += 1
                            continue
                        dt = float(ext.get('TIMEDEL', head.get('TIMEDEL', 0)))*86400
                        if abs(dt-120) > 1:
                            rejected['cadence'] += 1
                            continue
                        sector = int(head['SECTOR'])
                        item = dict(path=str(path.relative_to(S.ROOT)), sector=sector,
                                    bytes=path.stat().st_size)
                        # Deterministic one-file-per-sector selection, no flux ranking.
                        selected.setdefault(sector, item)
                except (OSError, ValueError, KeyError):
                    rejected['unreadable'] += 1
        files = [selected[k] for k in sorted(selected)]
        b = int(row['band'])
        counts[b]['stars'] += 1
        counts[b]['with_local'] += bool(files)
        counts[b]['files'] += len(files)
        counts[b]['bytes'] += sum(x['bytes'] for x in files)
        manifest.append(dict(tic=star, band=b, files=files))
    result = dict(counts=counts, rejected=rejected, manifest=manifest,
                  downloaded_files=0, downloaded_bytes=0)
    (S.OUT/'inventory.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(dict(counts=counts, rejected=rejected, downloaded_files=0)))


if __name__ == '__main__':
    main()
