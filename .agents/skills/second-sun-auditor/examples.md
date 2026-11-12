# Worked examples (real bugs in Second Sun). Private.

## Example 1. The eclipse mask that ate the planets (Fable audit F-01, 10 Nov 2026)
**Code** (`pipeline/detect_v2.py`, `eclipse_mask_auto`): fold ONE sector at the binary period into 600 phase bins, mask every bin more than 4 sigma low.
```python
med = np.array([np.median(flat[ok & (k == i)]) ... for i in range(nbins)])
low = np.nan_to_num(med < m0 - nsig * sig)        # any low bin is "an eclipse"
```
**Why it is wrong.** With a 20 d binary and a 27 d sector, each phase bin is visited once. A planet dip is a low bin. It is masked. Found on real G2 light: an 8 h dip at 25 times the noise is found 0 times in 25 for binaries slower than 20 d, 1.00 if injected after the mask.
**Why nobody saw it for three hunts.** Every recovery test did this:
```python
d, _ = S2.prepare(path)            # loads AND masks
fi = d["f"].copy(); fi[in_transit] -= depth     # injected after the mask
```
**The test that catches it** (40 lines, `research/fable-audit-2026-11/scripts/p01c_real_light_premask_injection.py`):
```python
t, f, _ = D.load(path)
fa = f.copy(); fa[in_transit] -= depth          # BEFORE the mask
keep, _ = D.eclipse_mask_auto(t, fa, P)
found = any(abs(e["center"] - tc) < 0.3 for e in D.find_events(t[keep], fa[keep]))
```
**The second symptom that was already on the page.** Upside-down events outnumbered real ones, more at higher SNR ("cause not studied"). An unexplained asymmetry between the arms is never noise until a binned test says so: binned by binary period it was 0.95 under 10 d and about 3 over 20 d.
**Lessons.** Inject before every step. Bin by period. An asymmetry between arms is a bug report.

## Example 2. A flag that "leaked", settled by counting (FIX 84 / F-02)
**Claim in the queue:** "QLP's quality flag is bit 31 from Sector 56 and lightkurve's hard mask misses it; effect NOT TESTED" (open for days, blocking trust in G3).
**The count** (`scripts/p02_fix84_qlp_bits.py`, 2 minutes): 0 of 982,103 kept cadences in Sectors 56 to 93 carry any flag, because lightkurve 2.6.0's QLP reader adds bit 30 itself. But in Sectors 94 on, 11.9% of kept cadences carry bit 29.
**Lesson.** Do not reason about what a library masks. Count the bits on the cadences you keep, per era. The answer was different from both the fear and the hope.

## Example 3. Right arithmetic, wrong meaning (WO-1, 8 Nov 2026, and F-07)
```python
old = 1 - np.exp(-(E0 + Ec))     # "chance of at least one planet": 87% to 100%
```
`E0` is three finished hunts that found nothing. A forecast counts only what is still to come, and the nulls lower the believed rate: the right number was 21% to 52%. Two days later the corrected number was re-derived by Monte Carlo and matched to the percent, and was STILL too optimistic in meaning, because `E0` and `Ec` come from recovery tables measured after the mask (example 1).
**Lesson.** After the arithmetic checks out, ask what each input does not include.

## Example 4. The loader path nobody ran (23 Oct 2026)
```python
BIN_D = 10 / 1440
bt, bf = bin10(tt, ff)            # 30-min data fills 1 bin in 3
m[n < min_cover * w] = np.nan     # every box fails 80% coverage -> no events, no error
```
The self-check used only 2-minute data, so it passed. Fix: `bin_width()` uses the data's own cadence when slower. **Lesson.** One test file per product and cadence; "no events" must be distinguishable from "could not search" (print the count of boxes scored).

## Example 5. A label that described the intent (F-17)
```python
g("commit", "-q", "-m", "watch: counts only")     # 87 commits
ticker=[dict(tic=r["tic"], sector=r["sector"], ...)]   # in the same payload, for the sealed G2 run
```
The branch is public. **Lesson.** Before a push, search the payload itself for `tic`, `center`, `source_id`. Make the safe mode the default and the unsafe mode need a flag.
