# Post-hoc diagnostics (EXPLORATORY: not part of the frozen SPEC)

Run on 2026-10-20 after the official run (results folder `20261020T215121Z_e40982b`), to explain one surprise: SAP + HARD (A1) recovered four published transits (S6, S27, S34, S37) that PDCSAP + HARD (A0, our baseline) missed, on the very same cadences.

- `depth_by_flux.py` / `.txt`: the matched events' timing and depth, and a simple line-fit depth at each published time in SAP vs PDCSAP.
- `noise_by_flux.py` / `.txt`: the detector's own noise estimate (sigma_D, the robust spread of all box means of one length) and the box depth and SNR at the published time, in each flux.

Reading: the depths agree between the two fluxes; sigma_D does not (S6: 599 ppm PDCSAP vs 204 SAP). So the A0/A1 difference is the red-noise estimate, not an attenuated transit. The cause of PDCSAP's higher red noise in those sectors is not known.
Both scripts read the results folder by a fixed path and write nothing except to stdout.
