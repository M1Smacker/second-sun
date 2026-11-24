# 035 implementation checkpoint, node 2.1

This is a draft with a failing synthetic precision test. It is not ready for the
150-star validation or Census use. No validation flux has been examined.

Selection was fixed before reading any light. Use source exactly prsa2022 or
ttc_t3, finite period 1 through 30 days and magnitude at most 13.5. Exclude the
union of G1 IDs in both target lists and every design_seen=0 G2/G3 row in r1.
Sort IDs before NumPy default_rng seed 2026112501. Draw 50 per band:
[1,5), [5,10), [10,30]. If a band lacks 50, redistribute its shortfall round
robin across remaining bands. No shortfall occurred. Do not replace unavailable
or failed stars. The private sample includes input hashes and judging metadata.

The estimator receives arrays and sectors only, no catalogue answer. It compiles
seven unchanged pure functions from 032 after AST comparison against 032b. It
does not import the old harness, pipeline modules, or old absolute paths.
Preprocessing retains the inherited 30-minute bins and median trend. Sector
box searches provide seeds, the inherited primary function searches their half,
same and double bands, and an odd/even-depth wrapper can supply a doubled seed.
All supplied sectors enter refinement. Three supported cycles are mandatory.
Output quality is candidate, never a validated orbital-period claim. Equal-depth
twins can remain intrinsically ambiguous; this draft does not resolve that issue.

Box search was chosen to detect repeated dimming without a sinusoidal shape
assumption. API reference consulted:
https://docs.astropy.org/en/stable/timeseries/bls.html
The installed implementation was exercised by the synthetic tests; web version
identity with the installed package was not asserted.

The brief's real-data gates remain unchanged: at least 85% within 0.1% of the
catalogue among stars with at least three eclipses; less than 5% half/double
errors; every single-eclipse star flagged and no period for it. All are to be
reported per band. A validation runner still needs a truth-side eclipse coverage
definition independent of finder success. Dropping failed fits from its denominator
would falsely improve the recovery rate. No denominator or alias-error tolerance
has been adopted based on validation outcomes.

Remaining implementation includes guarded FITS loading, missing-light MAST
acquisition, a checkpointed at-most-two-worker supervisor with source hashes and
progress.json, truth-side coverage judging, a real-sample alias mutation and an
independent recount. Download destinations must stay in data/astra/035/lc;
temporary files and network caches must also remain under 035. File inventory
is metadata only and chooses the first sorted accepted file per sector. It is
not yet a final provenance/cadence/time-system audit for the loader.

Run the saved synthetic test with:

```powershell
& D:/second-sun/.venv/Scripts/python.exe -I -B research/astra/scripts/035_test.py
```

It currently exits nonzero intentionally: the test stays strict rather than
relaxing the required period accuracy. Private synthetic and diagnostic outputs
can be overwritten by these scripts; the selected sample cannot change silently.
