"""RS-002 H-2 (own arithmetic on a CONFIRMED formula): Holman and Wiegert 1999 eq. 3, outer critical orbit a_c / a_binary for a circumbinary planet (arXiv:astro-ph/9809315, ar5iv page read 3 Nov 2026):
a_c = 1.60 + 5.10 e - 2.22 e^2 + 4.12 mu - 4.27 e mu - 5.09 mu^2 + 4.61 e^2 mu^2   (valid 0 <= e <= 0.7, 0.1 <= mu <= 0.9; good to 3% typically, 6% worst case).
Critical period ratio P_c / P_binary = a_c^1.5 (Kepler's third law, planet mass negligible, mu = M2 / (M1 + M2)). Compared with the observed ratios of the transiting circumbinary planets (v_b4_period_ratios.py)."""
import numpy as np
f = lambda e, mu: 1.60 + 5.10*e - 2.22*e**2 + 4.12*mu - 4.27*e*mu - 5.09*mu**2 + 4.61*e**2*mu**2
print("critical period ratio P_c/P_bin = a_c^1.5   (rows: binary eccentricity e; columns: mass ratio mu = M2/(M1+M2))")
mus = [0.1, 0.2, 0.3, 0.4, 0.5]
print("   e  | " + " | ".join(f"mu {m:.1f}" for m in mus))
for e in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
    print(f"  {e:.1f} | " + " | ".join(f"{f(e, m)**1.5:6.2f}" for m in mus))
print("\nrange over e 0 to 0.3 and mu 0.1 to 0.5: %.2f to %.2f" % (min(f(e, m)**1.5 for e in np.linspace(0, .3, 7) for m in np.linspace(.1, .5, 9)), max(f(e, m)**1.5 for e in np.linspace(0, .3, 7) for m in np.linspace(.1, .5, 9))))
print("Observed planet/binary period ratios, shortest ten: 5.57 5.62 6.34 6.53 6.55 6.64 6.92 8.80 10.39 12.87")
print("Kepler-16 check with its published e = 0.159 and mu = 0.226 (values from memory, UNCERTAIN): P_c/P_bin = %.2f" % (f(0.159, 0.226)**1.5))
