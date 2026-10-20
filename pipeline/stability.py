"""Closest stable circumbinary orbit (Holman & Wiegert 1999, Eq. 3; book chapter 1, Eq. 1.1).

a_c / a_bin = 1.60 + 5.10 e - 2.22 e^2 + 4.12 mu - 4.27 e mu - 5.09 mu^2 + 4.61 e^2 mu^2
mu = m2 / (m1 + m2). Fitted for 0 <= e <= 0.7 and 0.1 <= mu <= 0.5; outside that we still compute
but say so. Period ratio from Kepler's third law (planet mass neglected): P_c / P_bin = (a_c / a_bin)^1.5.
"""


def critical(e, mu):
    """Returns (a_c/a_bin, P_c/P_bin, in_fit_range)."""
    a = (1.60 + 5.10 * e - 2.22 * e**2 + 4.12 * mu - 4.27 * e * mu
         - 5.09 * mu**2 + 4.61 * e**2 * mu**2)
    return a, a ** 1.5, (0 <= e <= 0.7) and (0.1 <= mu <= 0.5)


def search_window(p_bin, e, m1, m2, lo=1.0, hi=10.0):
    """Planet periods (days) most worth searching: lo to hi times the critical period."""
    _, ratio, ok = critical(e, m2 / (m1 + m2))
    return lo * ratio * p_bin, hi * ratio * p_bin, ok


if __name__ == "__main__":
    # TOI-1338: P_bin 14.6 d, e 0.16, ~1.1 + 0.3 M_sun (Kostov+ 2020); expected critical ~4.9 P_bin (wave 1a C2)
    a, r, ok = critical(0.16, 0.3 / 1.4)
    assert ok and abs(r - 4.9) < 0.15, r
    lo, hi, _ = search_window(14.6, 0.16, 1.1, 0.3)
    assert 95.2 > lo, "TOI-1338 b (95.2 d) must lie outside the unstable zone"
    print(f"stability self-check passed: TOI-1338 a_c/a_bin = {a:.2f}, P_c = {r:.2f} P_bin = {r*14.6:.0f} d; "
          f"TOI-1338 b at {95.2/(r*14.6):.2f} x critical; search window {lo:.0f}-{hi:.0f} d")
