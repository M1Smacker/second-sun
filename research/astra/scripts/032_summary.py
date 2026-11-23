"""Apply fixed errors and v3 fits, score fresh controls once, save private evidence."""
from collections import Counter, defaultdict
import copy
import csv
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('032_eclipse_select')
M = importlib.import_module('032_error_model')
CAL = importlib.import_module('032_eclipse_calibrate')
H, O = S.H, S.O


def write_csv(path, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    guard = H.Guard()
    guard.start()
    samples = json.loads((H.OUT/'fresh-controls.json').read_text(encoding='utf-8'))
    calibration = json.loads(S.saved(guard, H.OUT.with_name('014')/'timing-calibration.json', '014'))
    old_rows = []
    for i in range(3):
        old_rows += json.loads(S.saved(guard, H.OUT.with_name('014')/f'eclipse-calibrate-{i}.json', '014'))['rows']
    assert all(str(r['star']) in guard.seen['g2'] for r in old_rows)
    trap = CAL.trap(old_rows)
    rows = [json.loads((H.OUT/'tracks'/f'{s}.json').read_text(encoding='utf-8')) for s in samples['selected']]
    assert len(rows) == len({r['star'] for r in rows}) == len(samples['selected'])
    assert all(str(r['star']) in guard.seen['g2'] for r in rows)
    ephemerides, events, offsets = [], [], []
    counts = Counter()
    bins = defaultdict(Counter)
    for row in rows:
        star, cat = row['star'], row['catalogue']
        p = samples['periods'][str(star)]
        period_bin = next((i for i, edge in enumerate([10,14,20,27.4]) if p < edge), 4)
        counts['selected'] += 1
        bins[period_bin]['selected'] += 1
        for kind in ('primary', 'secondary'):
            track = copy.deepcopy(row['fit'].get(kind, {}))
            ev = track.get('events', [])
            for e in ev:
                e['uncalibrated_error'] = e['error']
                e['error'] *= calibration['scales'].get(CAL.family(e['product']), 1)
            fit = M.fit_track(ev, row['fit']['search_period'], track['epoch_seed'], track['width']) if len(ev) >= 3 else None
            usable = bool(fit and fit['usable'])
            agree = sigma_ok = False
            if usable:
                midpoints = [samples['sector_midpoints'][str(sec)] for sec in samples['sectors'][str(star)]]
                if kind == 'primary':
                    agree, delta = M.sector_agreement(fit, cat, midpoints)
                    for sec, d in zip(samples['sectors'][str(star)], delta):
                        offsets.append(dict(star=star, sector=sec, offset_days=d, offset_widths=d/cat['wp']))
                    sigma_ok = abs(fit['period']-cat['P']) <= 3*math.hypot(fit['period_error'], cat['eP'])
            reason = ('usable' if usable else 'fewer than three times' if len(ev)<3 else
                      'singular cycles' if not fit else 'fewer than two sectors' if fit['n_sectors']<2 else 'scatter exceeds one tenth width')
            record = dict(star=star, sample='fresh', type=kind, period_bin=period_bin,
                          n_measured=len(ev), usable=usable, agrees=agree, period_3sigma=sigma_ok,
                          status=reason, width=track.get('width'), catalogue_period=cat.get('P') if cat else None,
                          catalogue_period_error=cat.get('eP') if cat else None,
                          alias=row['fit'].get('alias'), alias_reason=row['fit'].get('alias_reason'))
            if fit:
                record.update({k: v for k,v in fit.items() if k not in ('residuals','dropped_indices','usable')})
                for i, e in enumerate(ev):
                    e['retained'] = i not in fit['dropped_indices']
                    e['residual_v3'] = fit['residuals'][i]
                    e['inflated_error'] = math.hypot(e['error'], fit['extra_scatter'])
            ephemerides.append(record)
            events.extend(dict(star=star, type=kind, **e) for e in ev)
            counts[f'{kind}:times'] += len(ev)
            counts[f'{kind}:dropped'] += fit['n_dropped'] if fit else 0
            counts[f'{kind}:tracks_with_drops'] += bool(fit and fit['n_dropped'])
            counts[f'{kind}:usable'] += usable
            counts[f'{kind}:status:{reason}'] += 1
            if kind == 'primary':
                for key, value in [('three_times', len(ev)>=3), ('usable',usable), ('agrees',agree), ('period_3sigma',sigma_ok)]:
                    counts[key] += int(value)
                    bins[period_bin][key] += int(value)
    verdict = M.rules(counts['three_times'], counts['usable'], counts['agrees'], trap)
    write_csv(H.OUT/'ephemerides-v3.csv', ephemerides)
    write_csv(H.OUT/'eclipse-times-v3.csv', events)
    write_csv(H.OUT/'sector-offsets-v3.csv', offsets)
    result = dict(seed=samples['seed'], counts=dict(counts), period_bins=dict(bins), trap_pass=trap,
                  trap_n=30, rules=verdict, error_scales=calibration['scales'],
                  scope='Fresh controls only. The trap reuses the exact 014 design-noise library.')
    O.write_json(H.OUT/'summary.json', result, indent=2)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
    # The supervisor marks Part A complete only after the independent arithmetic
    # recount succeeds as well. This is still producer verification.
    importlib.import_module('032_recount').main()
