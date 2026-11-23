"""Independent synthetic checks; no real judging sample is opened."""
import ast
import importlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
M = importlib.import_module('032_error_model')
ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/032'


def events(n=40, scale=.02, error=.001):
    rng = np.random.default_rng(32)
    x = np.arange(n)
    return [dict(cycle=int(i), time=float(t), error=error, sector=int(i//10), width=1.)
            for i, t in zip(x, 2000+7*x+rng.normal(0, scale, n))]


def independent(rows, fit):
    good = [e for i, e in enumerate(rows) if i not in fit['dropped_indices']]
    x = np.array([e['cycle']-fit['epoch_cycle'] for e in good])
    y = np.array([e['time']-2000 for e in good])
    w = 1/np.array([e['error']**2+fit['extra_scatter']**2 for e in good])
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    slope = np.sum(w*(x-mx)*(y-my))/np.sum(w*(x-mx)**2)
    intercept = my-slope*mx
    v_slope = 1/np.sum(w*(x-mx)**2)
    v_intercept = 1/w.sum()+mx*mx*v_slope
    assert np.isclose(fit['period'], slope, rtol=0, atol=1e-10)
    assert np.isclose(fit['epoch'], intercept+2000, rtol=0, atol=1e-10)
    assert np.isclose(fit['period_error']**2, v_slope, rtol=1e-10)
    assert np.isclose(fit['epoch_error']**2, v_intercept, rtol=1e-10)
    residual = y-intercept-slope*x
    chi = np.sum(w*residual**2)/(len(good)-2)
    assert np.isclose(chi, fit['reduced_chi2'], atol=1e-8)
    if fit['extra_scatter']:
        assert abs(chi-1) < 1e-7


def main():
    checks = []
    rows = events()
    fit = M.fit_track(rows, 7, 2000, 1)
    independent(rows, fit)
    assert fit['extra_scatter'] > .005 and fit['usable']
    checks.append('independent slope, epoch, covariance and positive-scatter root')
    # A broad grid independently brackets the root of the minimized weighted sum.
    grid = np.linspace(fit['extra_scatter']*.99, fit['extra_scatter']*1.01, 101)
    chis = []
    good = [e for i,e in enumerate(rows) if i not in fit['dropped_indices']]
    for s in grid:
        x = np.array([e['cycle'] for e in good], float)
        y = np.array([e['time'] for e in good])
        w = 1/np.array([e['error']**2+s*s for e in good])
        mx, my = np.average(x, weights=w), np.average(y, weights=w)
        b = np.sum(w*(x-mx)*(y-my))/np.sum(w*(x-mx)**2)
        chis.append(np.sum(w*(y-my-b*(x-mx))**2)/(len(x)-2))
    assert chis[0] > 1 > chis[-1] and np.all(np.diff(chis) < 0)
    checks.append('independent scatter grid')
    small = events(scale=.00001, error=.01)
    low = M.fit_track(small, 7, 2000, 1)
    assert low['extra_scatter'] == 0 and low['reduced_chi2'] < 1
    independent(small, low)
    checks.append('zero extra scatter')
    outliers = events(n=100)
    for i in range(0,100,6):
        outliers[i]['time'] += 2
    clipped = M.fit_track(outliers, 7, 2000, 1)
    assert clipped['n_dropped'] == 10
    independent(outliers, clipped)
    checks.append('one-pass ten-percent clipping cap')
    one = [dict(e, sector=1) for e in rows]
    assert not M.fit_track(one, 7, 2000, 1)['usable']
    assert not M.fit_track(rows, 7, 2000, .0001)['usable']
    assert M.fit_track(rows[:2], 7, 2000, 1) is None
    checks.append('sector, width and time-count guards')
    cat = dict(P=7., T0=2000., wp=1.)
    assert M.sector_agreement(dict(period=7.,epoch=2000.25), cat, [2000.,2070.])[0]
    assert not M.sector_agreement(dict(period=7.,epoch=2000.2501), cat, [2000.,2070.])[0]
    assert not M.sector_agreement(dict(period=7.1,epoch=2000.), cat, [2000.,2070.])[0]
    checks.append('all-sector agreement and exact boundary')
    assert M.rules(50,40,36,30)['passed']
    assert not M.rules(50,39,39,30)['passed']
    assert not M.rules(50,40,35,30)['passed']
    assert not M.rules(50,40,36,29)['passed']
    assert not M.rules(0,0,0,30)['passed']
    checks.append('pass-rule boundaries and empty denominators')
    broken = dict(fit, extra_scatter=0)
    try:
        independent(rows, broken)
    except AssertionError:
        pass
    else:
        raise AssertionError('Deliberate missing-scatter mutation escaped')
    checks.append('deliberate omitted-scatter mutation rejected')
    for module, functions in [('eclipse_fit', None), ('eclipse_calibrate', ['trap']),
                              ('eclipse_select', ['stratified', 'midpoint'])]:
        source = subprocess.check_output(['git','show',f'astra/014-dumps-ephemerides:research/astra/scripts/014_{module}.py'], cwd=ROOT).decode('utf-8')
        before = ast.parse(source)
        after = ast.parse((Path(__file__).parent/f'032_{module}.py').read_text(encoding='utf-8'))
        originals = {n.name: ast.dump(n) for n in before.body if isinstance(n, ast.FunctionDef)}
        current = {n.name: ast.dump(n) for n in after.body if isinstance(n, ast.FunctionDef)}
        for name in functions or originals:
            assert originals[name] == current[name], name
    checks.append('014 timing, alias, trap and selection function AST identity')
    (OUT/'tests.json').write_text(json.dumps(dict(passed=checks), indent=2), encoding='utf-8')
    print('Runtime checks passed:', len(checks), '; mutation rejected; timing and alias functions unchanged.')


if __name__ == '__main__':
    main()
