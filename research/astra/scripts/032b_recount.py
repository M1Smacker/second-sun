"""Closed-form timing arithmetic and gate recount without importing the fitter."""
import argparse
from collections import Counter, defaultdict
import importlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
H = importlib.import_module('032b_harness')
DIAGNOSTICS = Counter()


def regression(events, epoch, center, extra=0., keep=None):
    if keep is None:
        keep = np.ones(len(events),dtype=bool)
    x = np.array([e['cycle']-center for e in events],dtype=float)
    y = np.array([e['time']-epoch for e in events])
    errors = np.array([e['error'] for e in events])
    weights = 1/(errors[keep]**2+extra**2)
    xx, yy = x[keep], y[keep]
    sw = sum(weights)
    mx, my = sum(weights*xx)/sw, sum(weights*yy)/sw
    ss = sum(weights*(xx-mx)**2)
    slope = sum(weights*(xx-mx)*(yy-my))/ss
    intercept = my-slope*mx
    residual = y-intercept-slope*x
    cov = np.array([[1/sw+mx*mx/ss,-mx/ss],[-mx/ss,1/ss]])
    chi = sum(weights*residual[keep]**2)/(sum(keep)-2)
    return intercept+epoch, slope, residual, cov, chi


def check_fit(events, fit, epoch, width):
    if not fit:
        assert len(events) < 3 or len({e['cycle'] for e in events}) < 2
        return False
    sig = np.array([e['error'] for e in events])
    cycles = np.array([e['cycle'] for e in events])
    center = int(np.rint(sum(cycles/sig**2)/sum(1/sig**2)))
    assert center == fit['epoch_cycle']
    _, _, initial, _, initial_chi = regression(events,epoch,center)
    delta = abs(initial-np.median(initial))
    mad = 1.4826*np.median(delta)
    candidates = np.flatnonzero(delta > 5*mad)
    ordered = candidates[np.argsort(-delta[candidates],kind='stable')]
    dropped = ordered[:min(len(events)//10,len(events)-3)].tolist()
    assert dropped == fit['dropped_indices']
    keep = np.ones(len(events),dtype=bool); keep[dropped] = False
    t0, p, residual, cov, chi = regression(events,epoch,center,fit['extra_scatter'],keep)
    assert math.isclose(t0,fit['epoch'],rel_tol=0,abs_tol=1e-8)
    assert math.isclose(p,fit['period'],rel_tol=1e-9,abs_tol=1e-9)
    assert np.allclose([cov[0,0],cov[1,1],cov[0,1]],
                       [fit['epoch_error']**2,fit['period_error']**2,fit['covariance']],rtol=1e-7,atol=1e-14)
    assert np.allclose(residual,fit['residuals'],rtol=1e-6,atol=1e-8)
    assert math.isclose(chi,fit['reduced_chi2'],rel_tol=2e-5,abs_tol=2e-5)
    if not math.isclose(initial_chi,fit['initial_reduced_chi2'],rel_tol=2e-5,abs_tol=2e-5):
        # Some preserved 014 secondary timing errors are smaller than one
        # floating-point spacing of their measured times. Initial chi-square
        # then amplifies arithmetic roundoff. Do not claim that diagnostic was
        # verified; retain strict checks of clipping, final fit and all gates.
        assert min(sig) < np.spacing(max(abs(e['time']) for e in events))
        DIAGNOSTICS['initial_chi2_below_time_precision_not_verified'] += 1
    assert fit['extra_scatter'] >= 0
    assert abs(chi-1) < 2e-5 if fit['extra_scatter'] > 0 else chi <= 1+2e-5
    scatter = 1.4826*np.median(abs(residual[keep]-np.median(residual[keep])))
    assert math.isclose(scatter,fit['robust_scatter'],rel_tol=1e-6,abs_tol=1e-8)
    sectors = len({e['sector'] for e,k in zip(events,keep) if k})
    assert fit['n'] == sum(keep) and fit['n_input'] == len(events)
    assert fit['n_sectors'] == sectors and fit['n_dropped'] == len(dropped)
    usable = bool(sum(keep) >= 3 and sectors >= 2 and scatter <= .1*width)
    assert usable == fit['usable']
    return usable


def check_record(r):
    events = r['events']
    all_usable = check_fit(events,r['all_fit'],r['epoch_seed'],r['width'])
    assert all_usable == r['all_usable']
    sectors = {e['sector'] for e in events}
    eligible = len(sectors) >= 3
    assert eligible == r['eligible'] and len(events) == r['n_measured']
    usable = predicted = False
    if eligible:
        last = max(sectors)
        train = [e for e in events if e['sector'] != last]
        held = [e for e in events if e['sector'] == last]
        assert r['held_sector'] == last and r['n_train'] == len(train) and r['n_held'] == len(held)
        usable = check_fit(train,r['train'],r['epoch_seed'],r['width'])
        if r['train']:
            fit = r['train']
            t0,p,_,_,_ = regression(train,r['epoch_seed'],fit['epoch_cycle'],fit['extra_scatter'],
                                    np.array([i not in fit['dropped_indices'] for i in range(len(train))]))
            offsets = [(e['time']-t0-(e['cycle']-fit['epoch_cycle'])*p)/r['width'] for e in held]
            assert np.allclose(offsets,r['offsets_widths'],atol=1e-7,rtol=1e-7)
            predicted = bool(usable and np.median(abs(np.array(offsets))) <= .25 and max(map(abs,offsets)) <= .5)
    assert usable == r['usable'] and predicted == r['predicts']
    agree, sigma = False, None
    if all_usable and r['type'] == 'primary':
        fit,cat = r['all_fit'],r['catalogue']
        offsets = []
        for t in r['catalogue_midpoints']:
            tc = cat['T0']+round((t-cat['T0'])/cat['P'])*cat['P']
            tf = fit['epoch']+round((tc-fit['epoch'])/fit['period'])*fit['period']
            offsets.append(abs(tc-tf))
        agree = bool(offsets and max(offsets) <= .25*cat['wp'])
        if math.isfinite(cat['eP']):
            sigma = abs(fit['period']-cat['P']) <= 3*math.sqrt(fit['period_error']**2+cat['eP']**2)
    assert agree == r['catalogue_agrees'] and sigma == r['period_3sigma']
    return dict(eligible=eligible,usable=usable,predicts=predicted,measured=len(events),all_usable=all_usable,
                catalogue_agrees=agree,train_dropped=r['train']['n_dropped'] if r['train'] else 0,
                all_dropped=r['all_fit']['n_dropped'] if r['all_fit'] else 0,
                period_3sigma_available=sigma is not None,period_3sigma=sigma is True)


def main(cached_only=False):
    guard = H.Guard(); guard.start()
    summary = json.loads((H.OUT/('cached-summary.json' if cached_only else 'summary.json')).read_text(encoding='utf-8'))
    samples = json.loads((H.OUT/'samples.json').read_text(encoding='utf-8'))
    verified, fits = {}, 0
    mutation_done = False
    for label, expected in summary['sets'].items():
        rows = json.loads((H.OUT/f'judged-{label}.json').read_text(encoding='utf-8'))
        sample = samples['sets'][label]
        assert len(rows) == 2*len(sample['selected'])
        assert {(r['star'],r['type']) for r in rows} == {(s,k) for s in sample['selected'] for k in ('primary','secondary')}
        counts, bins = Counter(), defaultdict(Counter)
        for r in rows:
            values = check_record(r)
            fits += int(bool(r['train']))+int(bool(r['all_fit']))
            b = sum(sample['periods'][str(r['star'])] >= edge for edge in [10,14,20,27.4])
            assert b == r['period_bin'] and str(r['star']) in guard.seen[sample['campaign']]
            if r['type'] == 'primary':
                counts['selected'] += 1; bins[str(b)]['selected'] += 1
            for k,v in values.items():
                counts[f"{r['type']}:{k}"] += int(v)
                bins[str(b)][f"{r['type']}:{k}"] += int(v)
            if not mutation_done and r['predicts']:
                broken = dict(r,predicts=False)
                try:
                    check_record(broken)
                except AssertionError:
                    mutation_done = True
                else:
                    raise AssertionError('Changed prediction verdict escaped recount')
        assert dict(counts) == expected['counts']
        assert dict(bins) == expected['bins']
        n,u,p = [counts['primary:'+k] for k in ('eligible','usable','predicts')]
        rules = dict(H1=bool(n and 100*u >= 80*n),H2=bool(u and 100*p >= 90*u),H3=summary['trap_pass']==30)
        rules['passed'] = all(rules.values())
        assert rules == expected['rules']
        verified[label] = dict(eligible=n,usable=u,predicts=p,rules=rules)
    assert mutation_done
    if not cached_only:
        assert summary['passed'] == all(verified[k]['rules']['passed'] for k in ('affected','g3'))
    result = dict(status='passed',sets=verified,closed_form_fits_checked=fits,mutated_verdict_rejected=True,
                  numerical_exclusions=dict(DIAGNOSTICS),
                  scope='Producer arithmetic verification, not independent review.')
    (H.OUT/('cached-recount.json' if cached_only else 'recount.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Closed-form fits verified:',fits,'; count and bin recount matched; verdict mutation rejected.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--cached-only',action='store_true')
    main(p.parse_args().cached_only)
