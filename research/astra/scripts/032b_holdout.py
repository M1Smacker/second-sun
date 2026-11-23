"""Fixed 032b judge. Only training times enter the unchanged 032 v3 fit."""
import copy
import importlib
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
M = importlib.import_module('032_error_model')


def calibrated(track, scales):
    events = copy.deepcopy(track.get('events', []))
    for e in events:
        e['error'] = e.get('uncalibrated_error', e['error'])*scales.get(e['product'].removesuffix('-SAP'), 1.)
    return events


def predicts(offset_widths):
    return bool(len(offset_widths) and np.median(np.abs(offset_widths)) <= .25
                and np.max(np.abs(offset_widths)) <= .5)


def judge(track, seed_period, scales):
    ev = calibrated(track, scales)
    sectors = sorted({e['sector'] for e in ev})
    result = dict(eligible=len(sectors) >= 3, n_measured=len(ev), sectors=len(sectors),
                  usable=False, predicts=False, offsets_widths=[], train=None, all_fit=None)
    if len(ev) >= 3:
        result['all_fit'] = M.fit_track(ev, seed_period, track['epoch_seed'], track['width'])
    if not result['eligible']:
        return result
    last = sectors[-1]
    train = [e for e in ev if e['sector'] != last]
    held = [e for e in ev if e['sector'] == last]
    fit = M.fit_track(train, seed_period, track['epoch_seed'], track['width'])
    result.update(held_sector=last, n_train=len(train), n_held=len(held), train=fit,
                  usable=bool(fit and fit['usable']))
    if fit:
        # Preserve measured cycle labels. Nearest-centre wrapping could hide
        # a wrong whole-cycle prediction and is not used for this judge.
        offset = [(e['time']-(fit['epoch']+(e['cycle']-fit['epoch_cycle'])*fit['period']))/track['width'] for e in held]
        result.update(offsets_widths=offset, median_abs_widths=float(np.median(np.abs(offset))),
                      max_abs_widths=float(np.max(np.abs(offset))),
                      predicts=bool(result['usable'] and predicts(offset)))
    return result


def rules(eligible, usable, predicted, trap):
    h1 = eligible > 0 and usable*5 >= eligible*4
    h2 = usable > 0 and predicted*10 >= usable*9
    h3 = trap == 30
    return dict(H1=h1, H2=h2, H3=h3, passed=h1 and h2 and h3)
