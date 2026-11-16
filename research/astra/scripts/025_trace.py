"""Reconstruct 005's roster and trace first loss on the fixed design-only T156."""
import argparse
from collections import Counter, defaultdict
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
D = importlib.import_module('025_inputs')
H = D.H
HYPOTHESES = ['missing_file_or_manifest', 'product_choice', 'quality_bits', 'finite_flux',
              'time_system_or_sector', 'preparation_skips', 'cadence_product_era',
              'FIX101_drift', 'no_safe_windows']


def main(campaign, roster_only=False, injected=False):
    os.environ.update(SS_SET=campaign, VESPER_OPTS='c6,p1', NUMBA_NUM_THREADS='2')
    guard = H.Guard()
    guard.start()
    guard.allow_machine_inputs(campaign)
    import numpy as np
    import pandas as pd
    import lightkurve as lk
    from lightkurve.utils import TessQualityFlags
    from astropy.io import fits
    import stage2_search as S
    import audit_all as A
    import detect_v2 as V
    import petrova_mask as PM
    policy = importlib.import_module('025_loader')
    policy.ENABLED = False
    S._init()
    manifest = pd.read_csv(H.DATA / campaign / 'manifest.csv').drop_duplicates('file')
    manifest_names = set(manifest.file)
    raw, window_cache = {}, {}
    quality_mask = int(TessQualityFlags.HARD_BITMASK)

    def load_file(path):
        key = str(path)
        if key in raw:
            return raw[key]
        guard.allow_design_file(path)
        t, f, fills, info = S.load(str(path), info=True)
        with fits.open(path, memmap=False) as hdus:
            tab = hdus[1].data
            tt = np.asarray(tab['TIME'], float)
            finite = np.isfinite(np.asarray(tab[info['column']], float))
            if info['column'] == 'pdcsap_flux':
                finite |= np.isfinite(np.asarray(tab['SAP_FLUX'], float))
            q = np.asarray(tab['QUALITY'], np.int64)
            headers = dict(sector=hdus[0].header.get('SECTOR', hdus[1].header.get('SECTOR')),
                           bjdrefi=hdus[1].header.get('BJDREFI', hdus[0].header.get('BJDREFI')),
                           timesys=hdus[1].header.get('TIMESYS', hdus[0].header.get('TIMESYS')))
        cad = float(np.median(np.diff(t))) if len(t) > 1 else float('nan')
        item = dict(t=t, f=f, tt=tt, finite=finite, q=q, info=info, cad=cad,
                    headers=headers, fills=fills, path=str(path))
        raw[key] = item
        return item

    def support(times, center, cad):
        return bool(len(times) and np.isfinite(cad) and np.min(np.abs(times - center)) <= 1.5 * cad)

    def windows_for(path, item, meta, star):
        key = str(path)
        if key in window_cache:
            return window_cache[key]
        info = item['info']
        if not info['needs_windows']:
            result = (None, 'not required', 0, None)
        else:
            sector = int(info['sector'])
            windows, nn = A.neighbour_windows(sector, meta['camera'], meta['ccd'], star)
            own = next(path.parent.glob(f'tess*-s{sector:04d}-{star:016d}-*_lc.fits'), None)
            if own is not None:
                guard.allow_design_file(own)
                result = (S.good_windows(str(own)), 'own SPOC', nn, None)
            elif nn >= 2:
                lists = [w for tic, w in A.DB.get((sector, meta['camera'], meta['ccd']), {}).items()
                         if tic != star and w]
                result = (windows, 'neighbours', nn, V.intersect_windows(lists, trim_start_d=0))
            else:
                result = ([], 'no safe windows', nn, None)
        window_cache[key] = result
        return result

    rows = list(D.t156_rows(guard, campaign))
    if roster_only:
        rows = [(r, folder) for r, folder in rows if 3000 <= r['depth_ppm'] <= 6000
                and 6 <= r['duration_h'] <= 12 and r['dip']['stage'] < 2 and not r['dip']['recovered']]
    output, skip_counts, era_paths = [], Counter(), Counter()
    for trial, folder in rows:
        star, sec, center = trial['star'], trial['sector'], trial['time']
        path = folder / f'trial-{trial["trial"]}-1/groups/{star}_{sec}.json'
        group = json.loads(D.read(guard, path, '003'))
        selected = [m for m in group['meta'] if m.get('product') == trial['product']] or group['meta']
        files, alternatives = [], []
        for meta in (selected if roster_only else group['meta']):
            file = H.DATA / campaign / str(star) / meta['file']
            if not file.exists():
                files.append(dict(file=meta['file'], cause='missing file'))
                skip_counts['missing file'] += 1
                continue
            item = load_file(file)
            t, f, tt, cad = (item[k] for k in ('t', 'f', 'tt', 'cad'))
            finite_t = np.isfinite(tt)
            near = finite_t & (np.abs(tt - center) <= 1.5 * cad)
            wins, win_src, nn, untrimmed = windows_for(file, item, meta, star)
            cause = 'raw centre covered'
            if not support(tt[finite_t], center, cad):
                cause = 'no recorded cadence'
            elif not support(t, center, cad):
                cause = 'recorded but lost at quality/finite-flux load'
            elif win_src == 'no safe windows':
                cause = 'recorded, no safe windows'
            elif wins is not None and not support(t[S.in_windows(t, wins)], center, cad):
                cause = 'recorded outside safe windows'
            detail = 'own SPOC' if win_src == 'own SPOC' else 'too few neighbours' if win_src == 'no safe windows' else win_src
            if win_src == 'neighbours':
                detail = ('half-day start trim' if support(t[S.in_windows(t, untrimmed)], center, cad)
                          and not support(t[S.in_windows(t, wins)], center, cad) else 'neighbour intersection')
            near_finite = near & item['finite']
            effective_mask = quality_mask
            if item['info']['product'] == 'QLP':
                effective_mask |= 2 ** (30 if sec >= 56 else 12)
            rejected = near_finite & ((item['q'] & effective_mask) != 0)
            bits = {str(1 << b): int(np.count_nonzero(rejected & ((item['q'] & (1 << b)) != 0)))
                    for b in range(32) if np.any(rejected & ((item['q'] & (1 << b)) != 0))}
            row = dict(file=meta['file'], product=item['info']['product'], column=item['info']['column'],
                       cause=cause, window_detail=detail, neighbours=nn, original_status=meta.get('status'),
                       manifest=file.name in manifest_names, headers=item['headers'], cadence_min=item['info']['cadence_min'],
                       recorded_near=int(near.sum()), finite_near=int(near_finite.sum()),
                       quality_rejected_near=int(rejected.sum()), effective_quality_mask=effective_mask,
                       quality_words=dict(Counter(map(str, item['q'][near]))),
                       rejected_bits=bits, loaded_near=int(np.count_nonzero(np.abs(t - center) <= 1.5 * cad)),
                       quality_kept_nonzero=int(np.count_nonzero(item['q'][finite_t & ((item['q'] & effective_mask) == 0)])),
                       line=('detect_v2.py:47 quality_bitmask=hard' if rejected.any() else
                             'detect_v2.py:73 or 85 finite normalized flux' if cause.endswith('load') else
                             'stage2_search.py:170 no safe windows' if win_src == 'no safe windows' else
                             'stage2_search.py:164 own SPOC' if win_src == 'own SPOC' else
                             'stage2_search.py:166 neighbour intersection; detect_v2.py:112 start trim'))
            if not roster_only:
                kept = np.ones(len(t), bool) if wins is None else S.in_windows(t, wins)
                tw, fw = t[kept], f[kept]
                status = 'no safe windows' if win_src == 'no safe windows' else 'too little data' if len(tw) < 200 else 'ok'
                row['window_near'] = int(np.count_nonzero(np.abs(tw - center) <= 1.5 * cad))
                row['window_points'] = len(tw)
                cat = PM.cat().get(star)
                if cat is not None and np.isfinite(cat.get('wp', np.nan)) and len(tw):
                    full = PM.windows(tw, cat)[0]
                    no_drift = dict(cat, eP=0., eT0=0.)
                    base = PM.windows(tw, no_drift)[0]
                    row['catalogue_removed_fraction'] = float(full.mean())
                    row['drift_only_removed_fraction'] = float(np.mean(full & ~base))
                    row['FIX101_whole_sector'] = bool(full.all())
                    row['FIX101_near_centre'] = bool(np.any(full & ~base & (np.abs(tw - center) <= 1.5 * cad)))
                    row['FIX101_zero_drift_restores_200'] = bool(len(tw) >= 200 and (~full).sum() < 200 and (~base).sum() >= 200)
                if status == 'ok':
                    if injected:
                        duration = trial['duration_h'] / 24
                        shape = np.clip((duration / 2 - np.abs(tw - center)) / (.1 * duration), 0, 1)
                        planted = fw - trial['depth_ppm'] * 1e-6 * shape
                        tm = PM.mask_runs(tw, planted, A.PER.get(star, []), star)[0]
                    else:
                        # Untouched support is useful separately from injection-dependent masks.
                        if 'masked' not in item:
                            item['masked'] = PM.mask_runs(tw, fw, A.PER.get(star, []), star)
                        tm = item['masked'][0]
                    row['masked_near'] = int(np.count_nonzero(np.abs(tm - center) <= 1.5 * cad))
                    row['masked_points'] = len(tm)
                    if len(tm) < 200:
                        status = 'too little data after masking'
                    elif row['window_near'] and not row['masked_near']:
                        status = 'centre removed by mask'
                row['preparation_status'] = status
                skip_counts[status] += 1
            era = 'pre56' if sec < 56 else '56to93' if sec < 94 else '94plus'
            era_paths[f'{row["product"]}/{era}/{round(cad * 86400)}s'] += 1
            (files if meta in selected else alternatives).append(row)
        order = ['raw centre covered', 'recorded outside safe windows', 'recorded, no safe windows',
                 'recorded but lost at quality/finite-flux load', 'no recorded cadence', 'no cadence estimate']
        category = next((cause for cause in order if any(f['cause'] == cause for f in files)), 'missing input')
        output.append(dict(trial=trial['trial'], star=star, sector=sec, campaign=campaign, bin=trial['bin'],
                           time=center, depth_ppm=trial['depth_ppm'], duration_h=trial['duration_h'],
                           product=trial['product'], old_stage=trial['dip']['stage'], cause=category,
                           hypotheses=HYPOTHESES, files=files, alternatives=alternatives))
    result = dict(campaign=campaign, quality_mask=quality_mask, counts=dict(Counter(r['cause'] for r in output)),
                  preparation_paths=dict(skip_counts), era_paths=dict(era_paths), rows=output)
    prefix = 'roster' if roster_only else 'injected-trace' if injected else 'trace'
    destination = H.OUT / f'{prefix}-{campaign}.json'
    destination.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(campaign, 'roster' if roster_only else 'trace', len(output), result['counts'], flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign', choices=('g2', 'g3'))
    parser.add_argument('--roster-only', action='store_true')
    parser.add_argument('--injected', action='store_true')
    args = parser.parse_args()
    main(args.campaign, args.roster_only, args.injected)
