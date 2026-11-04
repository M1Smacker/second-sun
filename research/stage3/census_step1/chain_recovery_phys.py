"""FIX 28 follow-up (night of 4 Nov 2026): completeness for a PHYSICAL transit shape, through the unchanged frozen chain.
Same wrapper idea as chain_recovery_shape.py (imports pipeline/chain_recovery.py unchanged, replaces only signal()), but the profile is a planet of radius ratio K_R crossing a quadratic-limb-darkened star at impact parameter B_IMP along a straight chord.
The harness's "dur" is the total width (first to fourth contact); the profile is normalised so its maximum (the deepest point) equals the plateau depth K, the same convention as the trapezoid variants.
Shapes: SHAPE=phys03 -> radius ratio 0.08, b 0.3 (short ramps, curved bottom); SHAPE=phys08 -> radius ratio 0.08, b 0.8 (long ramps, strongly curved bottom). Limb darkening u1=0.40, u2=0.25 (typical for a Sun-like star in the TESS band; ASSUMPTION, not looked up).
Usage (env as in run_shapes.ps1): SS_SET=g3 VESPER_OPTS=c6 SS_RUN=g3_e7886a71a61f SHAPE=phys03 python chain_recovery_phys.py run 300 8 shape_phys03"""
import os, sys
sys.path.insert(0, r"D:\second-sun\pipeline"); os.chdir(r"D:\second-sun\pipeline")
import numpy as np
import chain_recovery as cr
PARS = {"phys03": (0.08, 0.3), "phys08": (0.08, 0.8)}
KR, BIMP = PARS[os.environ.get("SHAPE", "phys03")]
U1, U2 = 0.40, 0.25

def _profile_table(n=401, g=41):
    """Blocked fraction of the star's light vs position along the chord, u in [-0.5, 0.5] of the total width, normalised to max 1."""
    L = np.sqrt((1 + KR) ** 2 - BIMP ** 2)
    gx = (np.arange(g) + 0.5) / g * 2 - 1
    px, py = np.meshgrid(gx, gx); m = px ** 2 + py ** 2 <= 1
    px, py = KR * px[m], KR * py[m]; dA = (2 * KR / g) ** 2
    def inten(r2):
        mu = np.sqrt(np.clip(1 - r2, 0, None)); I = 1 - U1 * (1 - mu) - U2 * (1 - mu) ** 2
        return np.where(r2 < 1, I, 0.0)
    # total stellar flux by a fine radial integral
    r = np.linspace(0, 1, 4001); tot = np.trapz(inten(r ** 2) * 2 * np.pi * r, r)
    us = np.linspace(-0.5, 0.5, n); out = np.zeros(n)
    for i, u in enumerate(us):
        s = 2 * L * u
        out[i] = (inten((s + px) ** 2 + (BIMP + py) ** 2) * dA).sum() / tot
    return us, out / out.max()
_U, _P = _profile_table()

def signal(t, tc, dur_h, depth_ppm, sign):
    x = (t - tc) * 24.0 / dur_h
    prof = np.interp(x, _U, _P, left=0.0, right=0.0)
    return -sign * depth_ppm * 1e-6 * prof
cr.signal = signal

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "run":
        cr.run(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], False)
    elif mode == "show":
        for u in (-0.5, -0.45, -0.4, -0.3, -0.2, -0.1, 0.0):
            print(f"u {u:+.2f}  profile {np.interp(u, _U, _P):.3f}")
        full = _P >= 0.99 * _P.max(); print(f"share of the width within 1% of the maximum: {full.mean():.2f}")
        half = _P >= 0.5; print(f"width at half maximum / total width: {half.mean():.2f}")
