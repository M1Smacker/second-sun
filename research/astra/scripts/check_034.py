"""Independent first-pass lesson arithmetic. No pipeline imports or light reads.
Run with the project's approved Python interpreter. Outputs only data/astra/034.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data' / 'astra' / '034'
print('ROOT:', ROOT, 'OUTPUT:', OUT)
OUT.mkdir(parents=True, exist_ok=True)
e, period = 0.4479, 19.658173
a = ((1.2384 + 1.2019) * (period / 365.25)**2)**(1/3)
# Independent areal-law integration, not the producer's anomaly conversion.
def separation_phase(omega, eccentricity=e):
    f0 = math.pi / 2 - omega
    return quad(lambda f: (1-eccentricity**2)**1.5 /
                (1+eccentricity*math.cos(f))**2,
                f0, f0+math.pi, epsabs=1e-12)[0] / (2*math.pi)

target = 11.879 / period  # Lesson input, NOT remeasured from light.
w = brentq(lambda x: separation_phase(x)-target, 0, math.pi/2)
other_e = brentq(lambda x: separation_phase(0, x)-target, 0.01, 0.5)
mean_r = quad(lambda E: a*(1-e*math.cos(E))**2,
              0, 2*math.pi)[0]/(2*math.pi)
perimeter = quad(lambda E: a*math.sqrt(1-e*e*math.cos(E)**2),
                 0, 2*math.pi)[0]
scale = 149597870.7 / (period*86400)
v1 = 2*1.384*696000/(0.4*86400)
v2 = 2*1.312*696000/(0.27*86400)
vp = 2*math.pi*0.901*149600000/(200*86400)
result = {
    'scope': 'Algebra and ideal two-body geometry only; supplied lesson inputs.',
    'doppler_shift_15kms_nm': 656.28*15/299792,
    'doppler_worked_kms': -0.010/500*299792,
    'doppler_turn_ms': .0015/500*299792458,
    'jupiter_sun_ms': 13100/1048,
    'earth_sun_ms': 29780/333000,
    'doppler_55_5ms_nm': 656.28*55.5/299792458,
    'minimum_mass_mj': 55.5*(4.2308*86400/(2*math.pi*6.67430e-11))**(1/3)*(1.07*1.98847e30)**(2/3)/1.89813e27,
    'full_secondary_percent': 100*1.99/4.30,
    'eighty_percent_primary_depth': 100*.8*2.31/4.30,
    'temperature_fourth_power': (6050/5983)**4,
    'secondary_phase_from_quoted_separation': target,
    'first_order_ecosw': (target-.5)*math.pi/2,
    'omega_degrees_assuming_published_e': math.degrees(w),
    'ecosw_assuming_published_e': e*math.cos(w),
    'same_phase_different_e_at_omega_zero': other_e,
    'a_AU': a,
    'time_mean_distance_AU': mean_r,
    'mean_distance_ratio': mean_r/a,
    'circular_speed_scale_kms': 2*math.pi*a*scale,
    'actual_time_mean_speed_kms': perimeter*scale,
    'periastron_AU': a*(1-e), 'apastron_AU': a*(1+e),
    'a1_AU_rounded_inputs': .192*1.2019/2.4403,
    'a2_AU_rounded_inputs': .192*1.2384/2.4403,
    'speed_ratio_rounded_inputs': .278/.106,
    'apastron_speed_rounded_inputs': 172*.106/.278,
    'planet_speed_kms': vp,
    'central_point_planet_relative_speed1_kms': v1,
    'central_point_planet_relative_speed2_kms': v2,
    'star1_signed_speed_if_planet_overtakes_kms': vp-v1,
    'star2_signed_speed_if_planet_overtakes_kms': vp-v2,
    'star1_other_signed_branch_kms': vp+v1,
    'diluted_depth_ppm': (.103/1.384)**2*.537*1e6,
    'dip_spacing_binary_fraction': 4.9/19.66,
}
# Sanity checks on independent formula implementation, not producer verification.
assert abs(separation_phase(0, 0)-.5) < 1e-12
assert abs(mean_r/a-(1+e*e/2)) < 1e-12
assert abs(separation_phase(w)-target) < 1e-10
assert abs(separation_phase(0, other_e)-target) < 1e-10
assert result['star1_signed_speed_if_planet_overtakes_kms'] < 0
lessons = ['u3/l4-doppler.md', 'u4/l1-eclipsing-binaries.md',
           'u4/l2-how-two-stars-orbit.md', 'u4/l4-planets-around-two-suns.md']
result['dash_scan'] = {}
result['finding_lines'] = {}
phrases = ['average distance', 'average relative speed', 'almost with it',
           'for this pair the exact answer', 'v_{\\text{planet}}',
           'Sideways motion', 'would need a spectrograph']
for lesson in lessons:
    lines = (ROOT/'book/docs/learn'/lesson).read_text(encoding='utf-8').splitlines()
    result['dash_scan'][lesson] = [i for i,s in enumerate(lines,1) if '\u2013' in s or '\u2014' in s]
    result['finding_lines'][lesson] = {p:[i for i,s in enumerate(lines,1) if p in s] for p in phrases}
(OUT/'arithmetic.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
