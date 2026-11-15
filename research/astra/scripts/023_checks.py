"""Small falsifiable checks for the interacting final-stage rules and access guard."""
import importlib
import inspect
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
S = importlib.import_module('023_score')


def tier(row):
    return '2' if row.get('gap_dump') or row.get('dominated') else '1B'


def main():
    guard = S.H.Guard()
    guard.start()
    event = dict(tic=1, sector=1, center=0., dur_h=6., depth_ppm=1000., snr=10.,
                 gap_dump=True, flags='momentum dump', lift_pre=.1, lift_post=-.2)
    count = 0

    def check(row, rivals, intervals, cap, expected):
        nonlocal count
        actual = S.decision(row, 0, rivals, intervals, cap, tier)
        assert actual == expected, (actual, expected)
        count += 1

    check(event, {0: event}, {}, 2000., [False, False, True, True])
    check(event, {0: event}, {}, 500., [False, False, True, False])
    check(dict(event, gap_dump=False, flags=''), {0: event}, {}, 1000., [True] * 4)
    check(dict(event, gap_dump=False, flags=''), {0: event}, {}, None, [True] * 4)
    check(event, {0: event}, {1: [(-.1, .1)]}, 2000., [False] * 4)
    check(dict(event, flags='gap edge; momentum dump'), {0: event}, {}, 2000., [False] * 4)
    check(dict(event, lift_pre=None), {0: event}, {}, 2000., [False] * 4)
    check(dict(event, lift_post=.251), {0: event}, {}, 2000., [False] * 4)
    rival = dict(event, center=2., gap_dump=False, flags='', repeater=True)
    check(event, {0: event, 1: rival}, {}, 2000., [False, False, True, True])
    check(event, {0: event, 1: dict(rival, repeater=False)}, {}, 2000., [False] * 4)
    # Mutating the cap and the dump-shape boundary must reverse these outcomes.
    assert S.decision(event, 0, {0: event}, {}, 2000., tier) != [False] * 4
    assert S.decision(event, 0, {0: event}, {}, 500., tier)[3] is False
    assert S.decision(dict(event, lift_pre=.251), 0, {0: event}, {}, 2000., tier)[2] is False
    namespace = dict(S.__dict__)
    broken = inspect.getsource(S.decision).replace('abs(v) > .25', 'abs(v) > .05')
    exec(broken, namespace)
    try:
        assert namespace['decision'](event, 0, {0: event}, {}, 2000., tier) == [False, False, True, True]
    except AssertionError:
        count += 1
    else:
        raise AssertionError('Deliberately broken dump-shape rule escaped the check')
    for forbidden in (S.H.ROOT / 'probe.txt', S.H.DATA / 'g1/probe.fits'):
        try:
            guard.check_write(forbidden)
        except PermissionError:
            count += 1
        else:
            raise AssertionError('Write guard accepted a forbidden location')
    print(count, 'rule and access checks, deliberate dump-shape mutation rejected')


if __name__ == '__main__':
    main()
