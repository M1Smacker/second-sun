"""Transcription test (11 Nov 2026): petrova_mask.veto_events must flag exactly the events the tested C2 veto (c2_event_veto.veto, TOL 1 h, NMIN 2) removes, on random synthetic stars. Synthetic data only."""
import os, sys, pathlib
os.environ.update(C2_TOL_H="1", C2_NMIN="2")
sys.path.insert(0, str(pathlib.Path(__file__).parent)); sys.path.insert(0, r"D:\second-sun\pipeline")
import numpy as np, pandas as pd
import c2_event_veto as V, petrova_mask as PM
rng = np.random.default_rng(11); agree = total = nveto = 0
for trial in range(400):
    P = float(rng.choice([8.0, 13.0, 17.3, 24.0, 40.0])); T0 = float(rng.uniform(0, 5)); nsec = int(rng.integers(2, 8)); base = rng.uniform(0, 1, 3)
    rows = []
    for s in range(nsec):
        off = float(rng.uniform(-0.05, 0.05))
        for _ in range(int(rng.integers(0, 4))):
            ph = float(rng.choice(base)) + float(rng.normal(0, 0.003)) if rng.random() < 0.6 else float(rng.uniform(0, 1))
            rows.append(dict(tic=1, kind="real", sector=s, center=T0 + off + (ph % 1.0) * P + P * int(rng.integers(0, 3)), dur_h=float(rng.choice([3, 4, 5, 6.5, 8, 10])), depth_ppm=float(rng.uniform(800, 9000)), p1_P=P, p1_T0=T0, p1_off=off))
    if not rows:
        continue
    ev = pd.DataFrame(rows); got = PM.veto_events(ev)
    for i, r in ev.iterrows():
        others = [(V.phase(q.center, P, T0, q.p1_off), q.dur_h, q.depth_ppm, int(q.sector)) for q in ev.itertuples() if q.sector != r.sector]
        kept, vet = V.veto([dict(center=r.center, dur_h=r.dur_h, depth_ppm=r.depth_ppm)], others, P, T0, r.p1_off)
        agree += int(bool(vet) == bool(got[i])); total += 1; nveto += int(bool(vet))
print(f"random synthetic events {total} (P 8 to 40 d): same decision as the tested C2 veto {agree} of {total}; events vetoed {nveto}")
