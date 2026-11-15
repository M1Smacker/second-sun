"""Bench-only quality policy, admitting bit 4096 and preserving every other bit."""
import numpy as np

ENABLED = True
RELAX_BIT = 4096
HARD = 24319


def flags_mask(quality, qlp, sector, enabled=True):
    mask = HARD | (2 ** (30 if sector >= 56 else 12) if qlp else 0)
    if enabled:
        mask &= ~RELAX_BIT
    return (np.asarray(quality, dtype=np.int64) & mask) == 0


def read(lk, path):
    if not ENABLED:
        return lk.read(path, quality_bitmask='hard')
    lc = lk.read(path, quality_bitmask='none')
    qlp = bool(set(lc.columns) & {'sys_rm_flux', 'det_flux', 'kspsap_flux'})
    sector = int(lc.meta.get('SECTOR', 0))
    q = np.asarray(lc.quality.value, dtype=np.int64)
    old = flags_mask(q, qlp, sector, False)
    new = flags_mask(q, qlp, sector, True)
    if np.array_equal(old, new):
        return lk.read(path, quality_bitmask='hard')
    return lc[new]


def checks():
    q = np.array([0, 4096, 8192, 12288, 128, 16384, 2 ** 29, 2 ** 30, 2 ** 30 + 4096])
    expected = np.array([True, True, True, True, False, False, True, True, True])
    assert np.array_equal(flags_mask(q, False, 1), expected)
    assert np.array_equal(flags_mask(q, True, 26), expected)
    late = expected.copy()
    late[-2:] = False
    assert np.array_equal(flags_mask(q, True, 56), late)
    baseline = expected.copy()
    baseline[1] = baseline[3] = baseline[-1] = False
    assert np.array_equal(flags_mask(q, False, 1, False), baseline)
    # Mutation removes the relaxation, so the required 4096-only cadence is lost.
    assert not flags_mask([4096], False, 1, False)[0]
    assert flags_mask([4096], False, 1, True)[0]
    return dict(policy_checks=4, mutation_rejected=True, bit=RELAX_BIT)
