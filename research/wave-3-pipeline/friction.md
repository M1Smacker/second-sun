# Wave 3 friction log

- ~17:22 UTC: all 6 main-venv installs failed with RecursionError, caused by Claude's own wave 2 truststore sitecustomize hook running inside pip, which injects its own truststore. The hook now skips pip. Re-run: 6/6 PASS.
- ~17:25: triceratops silently downgraded numpy, scipy and astropy (P3).
- ~17:28: g1_feasibility noise step crashed: `MaskedNDArray` has no `__round__` under astropy 7.2. Wrapped in `float(np.asarray(...))`; re-ran (cached downloads).
- ~17:30: mono-cbp install failed (no C compiler for its forced scipy source build).
- ~17:33: wrote the licence column from memory first, then verified it from package metadata (all matched).
- Deviation from WAVE-QUEUE.md: used the main `.venv` instead of `.venv-w3`, because no parallel runners were active, so no install collision was possible.
