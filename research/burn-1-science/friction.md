# Burn 1 friction

- Inline `python - <<'EOF'` heredocs in Git Bash mangled backslashes twice (`'second-sun\\'` and `"\\n"` in match strings). Worked around by writing small .py files.
- First `diagnose_misses.py` run: `sr.table.iterrows()` yields tuples (AttributeError). Switched to `sr.author` / `sr.exptime`.
- Second run: the S3 30-min FFI LC broke the 30-min binning (bins need ≥5 cadences → NaN MAD). S3 is now marked "method not applicable" instead of being analysed.
- `fit_event.py` free-impact-parameter `curve_fit` converged to a local minimum (T14 11.8 ± 6 h, χ² 820 > 770 for the constrained fit). Replaced by the χ² grid (`chi2_grid.py`).
- First `inject.py` run: a/R* formula bug (extra P/π factor → a/R* ≈ 3,300 → ~3-min injections) gave 0/56 recovered. Caught because the result was implausible. Fixed, and an `assert` on the injected duration added.
- astropy warns that `XDG_CONFIG_HOME` is not supported on Windows (ignored). `ASTROPY_CONFIG_DIR` is set, so nothing went to C:.
- lightkurve warns "tpfmodel submodule not available without oktopus". Harmless here.
- downloads.csv rows for burn-1 are stamped 20:59Z (when logged); the actual downloads ran ~20:54-20:58Z. Sizes were measured from the files on disk.
