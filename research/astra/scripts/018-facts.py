"""Independent FITS and arithmetic audit. No project science imports.

Run with D:/second-sun/.venv/Scripts/python.exe research/astra/scripts/018-facts.py
Expected scales: noise hundreds of ppm, eclipse spacing tens of days,
Earth crossing half a day, orbital speeds tens of km/s.
All event measurements are written only to private output.
"""
import json
import re
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy.ndimage import median_filter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/astra/018'
brief = (ROOT / 'research/astra/inbox/018-twinlight-check-2.md').read_text(encoding='utf-8')
source = ROOT / re.search(r'`(data/known/[^`]+/)`', brief).group(1)
lesson = (ROOT / 'book/docs/learn/u1/l4-what-a-dip-looks-like.md').read_text(encoding='utf-8')
centers = [float(x) for x in re.search(r'dips at day ([\d.]+) and ([\d.]+)', lesson).groups()]
OUT.mkdir(parents=True, exist_ok=True)
print('Input: brief-authorized published-system light. Output:', OUT)


def load(file, column):
    with fits.open(file, memmap=False) as hdus:
        d = hdus[1].data
        mask = (d['QUALITY'] == 0) & np.isfinite(d['TIME']) & np.isfinite(d[column])
        return np.array(d['TIME'][mask], dtype=float), np.array(d[column][mask], dtype=float)


def bins(t, f, minutes):
    # Independent dictionary grouping of fixed time cells, including sparse edges.
    cells = {}
    for ti, fi in zip(t, f):
        key = int(np.floor((ti - t[0]) * 1440 / minutes))
        cells.setdefault(key, []).append((ti, fi))
    pairs = [np.mean(v, axis=0) for v in cells.values() if len(v) >= 3]
    return np.array(pairs).T


t, flux = load(next(source.glob('hlsp_qlp_*s0021*.fits')), 'SAP_FLUX')
dips = []
for center in centers:
    region = np.abs(t - center) < 1
    tt, ff = t[region], flux[region] / np.median(flux[region])
    outside = np.abs(tt - center) > .35
    # Reimplement the documented local continuum, independently of plot code.
    continuum = np.interp(tt, tt[outside], median_filter(ff[outside], size=25, mode='nearest'))
    corrected = ff / continuum
    corrected /= np.median(corrected)
    inside = np.abs(tt - center) < .15
    sigma = np.std(corrected[outside]) * 1e6
    depth = (1 - np.mean(corrected[inside])) * 1e6
    low = (np.abs(tt - center) < .35) & (corrected < 1 - .0012)
    indices = np.flatnonzero(low)
    chunks = np.split(indices, np.flatnonzero(np.diff(indices) > 1) + 1)
    chunks = [c for c in chunks if len(c)]
    # Distinguish first-to-last threshold span from full contact duration.
    longest = max(chunks, key=len)
    linear = np.polyfit(tt[outside] - center, ff[outside], 1)
    alternate = ff / np.polyval(linear, tt - center)
    alternate /= np.median(alternate)
    dips.append(dict(center=center, points=int(inside.sum()), noise_ppm=float(sigma),
                     depth_ppm=float(depth), snr=float(depth * np.sqrt(inside.sum()) / sigma),
                     snr_using_305=float(depth * np.sqrt(inside.sum()) / 305),
                     single_point_snr=float(depth / sigma),
                     below_threshold_points=int(low.sum()),
                     threshold_span_hours=float(np.ptp(tt[low]) * 24),
                     longest_threshold_span_hours=float(np.ptp(tt[longest]) * 24),
                     cadence_minutes=float(np.median(np.diff(tt)) * 1440),
                     linear_continuum_depth_ppm=float((1 - np.mean(alternate[inside])) * 1e6)))

sectors = []
eclipses = []
for file in sorted(source.glob('tess2021*-s004[4-7]-*_lc.fits')):
    st, sf = load(file, 'PDCSAP_FLUX')
    sf /= np.median(sf)
    indices = np.flatnonzero(sf < .9)
    splits = np.flatnonzero((np.diff(indices) > 1) | (np.diff(st[indices]) > .05)) + 1
    for group in np.split(indices, splits):
        if len(group) < 5:
            continue
        eclipses.append(dict(middle=float((st[group[0]] + st[group[-1]]) / 2),
                             minimum_time=float(st[group[np.argmin(sf[group])]]),
                             depth=float(1 - min(sf[group])), points=len(group)))
    gaps = [(float(st[i]), float(st[i+1]), float(st[i+1]-st[i]))
            for i in np.flatnonzero(np.diff(st) > .1)]
    bt, bf = bins(st, sf, 60)
    sectors.append(dict(start=float(st[0]), end=float(st[-1]), gaps=gaps,
                        binned_depth_percent=float((1 - min(bf)) * 100)))
    if len(sectors) == 1:
        bt, bf = bins(st, sf, 30)
        center = bt[np.argmin(bf)]
        region = np.abs(st - center) < .6
        et, ef = bins(st[region], sf[region], 10)
        bottom_points = int(np.count_nonzero(ef <= min(ef) + .01))
        eclipse = dict(bottom_points_within_one_percentage_point=bottom_points,
                       bottom_depth_percent=float((1 - min(ef)) * 100))
primary = sorted(e['middle'] for e in eclipses if e['depth'] > .4)
secondary = sorted(e['middle'] for e in eclipses if e['depth'] <= .4)
cycles = np.rint((np.array(primary) - primary[0]) / 19.658)
slope, intercept = np.polyfit(cycles, primary, 1)
missing = []
for family in [primary, secondary]:
    for left, right in zip(family, family[1:]):
        if right - left > 1.5 * slope:
            predicted = left + slope
            covering = [g for s in sectors for g in s['gaps'] if g[0] < predicted < g[1]]
            missing.append(dict(predicted=predicted, covering_gaps=covering))

au_km, sun_km = 149597870.7, 695700
mass = 1.238 + 1.202
binary_a = (mass * (19.658 / 365.25)**2)**(1/3)
planet_a = (mass * (200 / 365.25)**2)**(1/3)


def duration(period, radius, orbit):
    return period / np.pi * radius / (orbit * 215) * 24


orbit_lesson = (ROOT / 'book/docs/learn/u2/l1-orbits-and-periods.md').read_text(encoding='utf-8')
last_primary = float(re.search(r'The last primary eclipse in the plot is at day ([\d.]+)', orbit_lesson).group(1))
arithmetic = dict(
    snr_second=2655 * np.sqrt(12) / 305, snr_first=1900 * np.sqrt(14) / 305,
    noise_12=305 / np.sqrt(12), noise_14=305 / np.sqrt(14),
    single_point_snr_using_lesson=2655 / 305,
    snr_problem=2000 * np.sqrt(16) / 400, six_hour_points=6 * 60 / 30,
    planet_earth_widths=np.sqrt(2500 / 1e6) * 1.3 * 109.08, threshold_ppm=7 * 100,
    radius_only_depth_ppm=(11.25 / (1.3827 * 109.08))**2 * 1e6,
    primary_period_endpoint=(primary[-1] - primary[0]) / 5,
    binary_a_AU=binary_a, binary_a_solar_radii=binary_a * au_km / sun_km,
    binary_a_solar_diameters=binary_a * au_km / (2 * sun_km),
    planet_a_AU=planet_a, separation_ratio=planet_a / binary_a,
    orbit_problem_days=(160 - 100) / 3, next_eclipse=last_primary + 19.658,
    four_AU_years=np.sqrt(4**3), jupiter_years=np.sqrt(5.2**3),
    kepler16_AU=(.89 * (229 / 365.25)**2)**(1/3), mass_factor=np.sqrt(8),
    AU_solar_radii=au_km/sun_km, earth_hours=duration(365.25, 1, 1),
    hot_jupiter_hours=duration(3, 1, .0407), ten_day_hours=duration(10, 1, .09),
    target_hours=duration(200, 1.38, .90), jupiter_hours=duration(365.25*np.sqrt(5.2**3), 1, 5.2),
    star_km_s=2*np.pi*(binary_a/2)*au_km/(19.658*86400),
    planet_km_s=2*np.pi*.9*au_km/(200*86400),
    two_minute_points=6*60/2, claimed_cadence_gain=np.sqrt(180/12),
    photon_noise_per_2min_over_30min=np.sqrt(30/2),
    photon_noise_total_gain=np.sqrt(180/12)/np.sqrt(30/2),
    radius_duration_factor=2, radius_depth_factor=1/2**2,
    hot_jupiter_finite_size_factor=1+.1,
    jupiter_full_hours=duration(365.25*np.sqrt(5.2**3), 1+11.21/109.08, 5.2),
    secondary_static_hours=duration(200, 1.3124, .90),
    radius_ratio_binary=1.3124/1.3827,
    uniform_binary_flat_fraction=(1-1.3124/1.3827)/(1+1.3124/1.3827),
    stationary_offset_for_six_of_eleven=np.sqrt(1-(6/11)**2),
    doubled_radius_relative_depth=.25,
    binary_periastron_AU=binary_a*(1-.45), binary_apastron_AU=binary_a*(1+.45),
    relative_speed_opposed=49+53, relative_speed_aligned=abs(49-53),
)
result = dict(dips=dips, eclipse=eclipse, sectors=sectors, primary=primary, secondary=secondary,
              period_fit=float(slope), residuals_minutes=((np.array(primary)-(intercept+slope*cycles))*1440).tolist(),
              missing_eclipses=missing, arithmetic=arithmetic)
expected_answers = {
    'learn/u1/l4-what-a-dip-looks-like.md': [arithmetic['snr_first'], 20, 12, arithmetic['planet_earth_widths'], 700, 'ingress'],
    'learn/u2/l1-orbits-and-periods.md': [planet_a, 20, arithmetic['next_eclipse'], 8, arithmetic['kepler16_AU'], np.sqrt(8)],
    'learn/u2/l2-how-long-a-dip-lasts.md': [arithmetic['hot_jupiter_hours'], arithmetic['ten_day_hours'], 2, 12, 'longer'],
}
checks = []
for relative, calculated in expected_answers.items():
    content = (ROOT / 'book/docs' / relative).read_text(encoding='utf-8')
    problems = re.findall(r'<div class="tw-prob"([^>]+)>', content)
    assert len(problems) == len(calculated), 'Problem inventory changed'
    for index, (attributes, answer) in enumerate(zip(problems, calculated), 1):
        declared = re.search(r'data-answer="([^"]+)"', attributes).group(1).split('|')
        if isinstance(answer, str):
            matches = answer in declared
        else:
            tolerance = re.search(r'data-tol="([^"]+)"', attributes)
            absolute = re.search(r'data-abs="([^"]+)"', attributes)
            tol = float(tolerance.group(1)) if tolerance else (0 if absolute else .02)
            abs_tol = float(absolute.group(1)) if absolute else 0
            matches = any(abs(float(a)-answer) <= max(abs_tol, abs(float(a))*tol) for a in declared)
        checks.append(dict(page=relative, problem=index, computed=answer, declared=declared, matches=matches))
result['problem_checks'] = checks
result['worked_intermediates'] = dict(
    noise_second_root=np.sqrt(12), noise_first_root=np.sqrt(14),
    binary_years=19.658/365.25, binary_squared=(19.658/365.25)**2,
    binary_cubed=mass*(19.658/365.25)**2,
    planet_years=200/365.25, planet_squared=(200/365.25)**2,
    planet_cubed=mass*(200/365.25)**2,
    earth_radius_ratio=1/215, earth_period_over_pi=365.25/np.pi,
    earth_days=duration(365.25,1,1)/24,
    hot_jupiter_a_solar=.0407*215, hot_jupiter_ratio=1/(.0407*215),
    hot_jupiter_days=duration(3,1,.0407)/24,
    ten_day_a_solar=.09*215, ten_day_ratio=1/(.09*215),
    target_a_solar=.9*215, target_ratio=1.38/(.9*215), target_days=duration(200,1.38,.9)/24,
    kepler16_years=229/365.25, kepler16_squared=(229/365.25)**2,
    kepler16_cubed=.89*(229/365.25)**2,
    half_period_hint=last_primary+19.658/2,
)
(OUT / 'facts.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('Wrote independent FITS measurements and', len(arithmetic), 'arithmetic checks to facts.json')
print('Eclipses counted:', len(primary), 'primary,', len(secondary), 'secondary. Missing in gaps:', len(missing))
print('Source answer comparisons:', sum(c['matches'] for c in checks), '/', len(checks))
assert all(c['matches'] for c in checks), 'A source answer disagrees with independent arithmetic'
