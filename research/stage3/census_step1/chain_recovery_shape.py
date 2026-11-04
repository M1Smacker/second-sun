"""FIX 28 (found 29 Oct; run overnight 4 Nov 2026): completeness for injected dips of other SHAPES than the symmetric 20%-ramp trapezoid, through the unchanged frozen chain.
A wrapper outside the hashed files: it imports pipeline/chain_recovery.py unchanged and replaces only its signal() function (also in the worker processes, because the patch runs at import).
Shapes (fractions of the total width spent in ingress and egress): sym = 0.2/0.2 (baseline, must reproduce rows_g3), skew = 0.1/0.5 (fast ingress, slow egress), stretch = 0.4/0.4 (V-like, long ramps), box = 0.05/0.05.
Usage (env as in g3_go.ps1): SS_SET=g3 VESPER_OPTS=c6 SS_RUN=g3_e7886a71a61f SHAPE=skew python chain_recovery_shape.py run 300 8 shape_skew"""
import os, sys
sys.path.insert(0, r"D:\second-sun\pipeline"); os.chdir(r"D:\second-sun\pipeline")
import numpy as np
import chain_recovery as cr
SHAPES = {"sym": (0.2, 0.2), "skew": (0.1, 0.5), "stretch": (0.4, 0.4), "box": (0.05, 0.05)}
A, B = SHAPES[os.environ.get("SHAPE", "sym")]
def signal(t, tc, dur_h, depth_ppm, sign):
    x = (t - tc) * 24.0
    prof = np.clip((x + dur_h / 2) / (A * dur_h), 0, 1) * np.clip((dur_h / 2 - x) / (B * dur_h), 0, 1)
    return -sign * depth_ppm * 1e-6 * prof
cr.signal = signal
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "run":
        cr.run(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], False)
