"""Aggregate the completed detection-only measurements and recovery ceilings."""
import json
from collections import Counter
from pathlib import Path
from statistics import median

OUT = Path(r'D:\second-sun-astra\data\astra\005')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def is_reference(row):
    return 3000 <= row['depth_ppm'] <= 6000 and 6 <= row['duration_h'] <= 12


def statistics(rows):
    qualified = [r for r in rows if r['dip']['stage'] >= 3]
    measured = [(r, p) for r in qualified for p in r['paths']]
    primary = [p for r, p in measured if p['product'] == r['product']]

    def metric(values):
        values = [x for x in values if x is not None]
        return [len(values), median(values) if values else None]

    results = Counter()
    for row in qualified:
        paths = row['paths']
        if not paths:
            results['no eligible measurements'] += 1
        elif any(p['matched'] for p in paths):
            results['matched'] += 1
        elif any(p['above'] for p in paths):
            results['above bar, no retained match'] += 1
        elif any(p['best_snr'] is not None for p in paths):
            results['below bar'] += 1
        else:
            results['no finite box'] += 1
    near = [p for p in primary if p['phase_width'] is not None and p['phase_width'] < 2]
    far = [p for p in primary if p['phase_width'] is not None and p['phase_width'] >= 2]
    return dict(n=len(rows), qualified=len(qualified), original_no_event=sum(r['dip']['stage']==3 for r in rows),
                measured_paths=len(measured), eligible_results=results, primary_n=len(primary),
                primary_depth_before=metric(p['before'][0] for p in primary),
                primary_depth_after=metric(p['after'][0] for p in primary),
                primary_depth_change=metric(p['after'][0]-p['before'][0] for p in primary
                                            if p['before'][0] is not None and p['after'][0] is not None),
                primary_scatter=metric(p['after'][1] for p in primary),
                primary_snr=metric(p['best_snr'] for p in primary),
                primary_shift=metric(p['shift_duration'] for p in primary if p['matched']),
                primary_near_scatter=metric(p['after'][1] for p in near),
                primary_far_scatter=metric(p['after'][1] for p in far))


def main():
    rows = [json.loads(line) for p in (OUT / 'blindspot').glob('*/diagnostic.jsonl')
            for line in p.read_text(encoding='utf-8').splitlines()]
    assert len(rows) == len({r['trial'] for r in rows}) == 800
    summary = {}
    for k in (0, 3):
        part = [r for r in rows if r['bin']==k]
        assert len(part) == 400
        summary[str(k)] = dict(all=statistics(part), reference=statistics([r for r in part if is_reference(r)]))
    assert [summary[str(k)]['reference']['original_no_event'] for k in (0, 3)] == [19, 5]
    base = read(OUT/'both-summary.json')
    den = [b['ref_n'] for b in base['bins']]
    window = Counter()
    for name in ('g2','g3'):
        window.update(read(OUT/f'window-{name}.json')['bybin'])
    def ceiling(counts):
        return sum(n/d for n,d in zip(counts,den))/5
    all_ref = [json.loads(line) for p in (OUT.with_name('003')/'workers').glob('*/results-*.jsonl')
               for line in p.read_text(encoding='utf-8').splitlines()]
    stage = Counter((r['bin'],r['dip']['stage']) for r in all_ref if is_reference(r) and not r['dip']['recovered'])
    summary['R_increment_ceilings'] = dict(
        short_detection=ceiling([stage[0,3],0,0,0,0]),
        all_detection=ceiling([stage[k,3] for k in range(5)]),
        mask_support=ceiling([stage[k,2] for k in range(5)]),
        usable_window=ceiling([sum(window[f'{k}: {label}'] for label in ('recorded outside safe windows','recorded, no safe windows')) for k in range(5)]),
        no_safe_window=ceiling([window[f'{k}: recorded, no safe windows'] for k in range(5)]))
    (OUT/'diagnostic-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
