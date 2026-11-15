"""Independent Twinlight arithmetic and published-system FITS checks.

Run with D:/second-sun/.venv/Scripts/python.exe research/astra/scripts/017-facts.py
Expected scale before measurement: eclipses tens of percent, quiet scatter 1e-3,
30-minute scatter a few 1e-4. No project pipeline or plotting imports.
"""
import json
import re
from pathlib import Path

import numpy as np
from astropy.io import fits

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/astra/017'
brief = (ROOT / 'research/astra/inbox/017-twinlight-check.md').read_text(encoding='utf-8')
SOURCE = ROOT / re.search(r'`(data/known/[^`]+\.fits)`', brief).group(1)
OUT.mkdir(parents=True, exist_ok=True)
print('Input: explicitly authorized published-system FITS. Output:', OUT)
with fits.open(SOURCE, memmap=False) as hdus:
    data = hdus[1].data
    mask = (data['QUALITY'] == 0) & np.isfinite(data['TIME']) & np.isfinite(data['PDCSAP_FLUX'])
    t = np.array(data['TIME'][mask], dtype=float)
    f = np.array(data['PDCSAP_FLUX'][mask], dtype=float)
    headers = {k: hdus[1].header.get(k) for k in ['TUNIT1', 'TUNIT8', 'BJDREFI', 'TIMEDEL']}
normal = float(np.median(f))
lesson = (ROOT / 'book/docs/learn/u1/l1-a-light-curve.md').read_text(encoding='utf-8')
quoted = re.search(r'bottoms of the two eclipses are at day (\d+\.\d+) and day (\d+\.\d+)', lesson)
quoted_times = [float(v) for v in quoted.groups()]
# Locate the two broad, separated eclipse troughs directly in the time series.
troughs = []
available = np.ones(len(t), dtype=bool)
for _ in range(2):
    i = np.flatnonzero(available)[np.argmin(f[available])]
    troughs.append({'time': float(t[i]), 'flux': float(f[i]), 'depth_percent': float(100 * (1 - f[i] / normal))})
    available &= np.abs(t - t[i]) > 2
troughs.sort(key=lambda x: x['time'])
# Independent candidate enumeration, excluding a full day around measured troughs.
quiet_start = None
for tick in range(int(np.ceil(t[0]) * 4), int((t[-1] - 1) * 4)):
    start = tick / 4
    if any(start - 1 <= e['time'] <= start + 2 for e in troughs):
        continue
    keep = (t >= start) & (t < start + 1)
    if keep.sum() >= 700:
        quiet_start = start
        break
if quiet_start is None:
    raise RuntimeError('No quiet-day candidate meets the predeclared coverage rule')
qt, qf = t[keep], f[keep] / normal
if len(qt) % 15:
    raise RuntimeError('Quiet-day point count does not allow equal fifteen-point groups')
# Consecutive groups provide an independent cross-check of time-defined bins.
groups = np.array_split(np.arange(len(qt)), len(qt) // 15)
means = np.array([qf[g].mean() for g in groups])
medians = np.array([np.median(qf[g]) for g in groups])
centered_t = qt - qt.mean()
slope = np.dot(centered_t, qf - qf.mean()) / np.dot(centered_t, centered_t)
flat = qf - slope * centered_t
flat_means = np.array([flat[g].mean() for g in groups])
flat_medians = np.array([np.median(flat[g]) for g in groups])
hour_means = np.array([qf[g].mean() for g in np.array_split(np.arange(len(qt)), len(qt) // 30)])
quiet_normal = np.median(qf)
result = {
    'points': len(t), 'span_days': float(np.ptp(t)), 'normal_electrons_per_second': normal,
    'median_cadence_minutes': float(np.median(np.diff(t)) * 1440), 'headers': headers,
    'troughs': troughs, 'quiet_start': quiet_start, 'quiet_points': len(qt),
    'quiet_std_ppm_global_normal': float(np.std(qf) * 1e6),
    'quiet_std_ppm_local_normal': float(np.std(qf / quiet_normal) * 1e6),
    'mean_30_std_ppm': float(np.std(means / quiet_normal) * 1e6),
    'median_30_std_ppm': float(np.std(medians / quiet_normal) * 1e6),
    'detrended_mean_30_std_ppm': float(np.std(flat_means / quiet_normal) * 1e6),
    'detrended_median_30_std_ppm': float(np.std(flat_medians / quiet_normal) * 1e6),
    'detrended_white_prediction_ppm': float(np.std(flat / quiet_normal) * 1e6 / np.sqrt(15)),
    'drift_ppm_per_day': float(slope / quiet_normal * 1e6),
    'actual_hour_mean_ppm': float(np.std(hour_means / quiet_normal) * 1e6),
    'retained_days_at_nominal_cadence': len(t) / 720,
    'large_gaps_days': [float(x) for x in np.diff(t) if x > .05],
    'quiet_range_ppm': [float(x) for x in (qf / quiet_normal - 1)[[np.argmin(qf), np.argmax(qf)]] * 1e6],
    'arithmetic': {
        'eclipse_example_percent': (12316 / 22437 - 1) * 100,
        'second_percent': (0.642 - 1) * 100, 'gap_days': quoted_times[1] - quoted_times[0],
        'earth_ppm': (1 / 109.08)**2 * 1e6,
        'planet_ppm': (11.25 / 109.08 / 1.3827)**2 * 1e6,
        'jupiter_ppm': (11.21 / 109.08)**2 * 1e6,
        'small_star_ppm': (1 / 54.54)**2 * 1e6,
        'five_point_std_ppm': float(np.std([1.001, .999, 1.0005, .9995, 1]) * 1e6),
        'four_point_population_std_ppm': float(np.std([.998, 1.002, 1, 1]) * 1e6),
        'four_point_sample_std_ppm': float(np.std([.998, 1.002, 1, 1], ddof=1) * 1e6),
        'half_hour_white_ppm': 930 / np.sqrt(15), 'hour_white_ppm': 930 / np.sqrt(30),
        'day_points': 24 * 60 / 2, 'percent_problem': (19800 / 20000 - 1) * 100,
        'ratio_problem': (.97 - 1) * 100, 'quarter_percent_ppm': .25 * 10000,
        'three_hundred_ppm_percent': 300 / 10000, 'flux_deficit_ppm': (1 - .9988) * 1e6,
        'tenth_radius_ppm': .1**2 * 1e6, 'average_25_ppm': 1000 / np.sqrt(25),
        'needed_points': (1200 / 300)**2,
    },
}
(OUT / 'facts.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
