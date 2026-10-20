# Burn 1: science check on TOI-1338 b

*Second Sun, burn 1 (science). Run by a side session (Claude, Opus 5.5) on 2026-10-19, 20:52-21:10 UTC. Internal test of our tools. **Not a discovery**: TOI-1338 b has been a known planet since 2020.*

Picture for phones: `burn1_summary.png`.

---

## In plain words (read this first)

**What we were checking.** Earlier today our computer search found a small dip in a star's light on **16 December 2025**. The star is TOI-1338, a pair of stars (two suns) with a known planet, **TOI-1338 b**. When the planet passes in front of the bigger star, the star looks a tiny bit darker for a few hours. That is called a **transit**. Claude guessed (80% sure) that our dip was this known planet passing in front again.

**1. The guess was right.** A 2024 paper by Wang and Liu worked out where the planet will be in the future. It said the planet would cross on **16 December 2025 at 02:13 UTC** and that the crossing would last **6.3 hours**. Our dip is:
- on the **same night**;
- about **6.4 hours** long (the same, within the error);
- about **57 minutes later** than they said.

An hour late is a small miss for a two-sun planet. These planets wobble, so their crossings are not like clockwork. The paper's own error was ±23 minutes, so we are a little outside it. That is interesting, not alarming. It is NOT a new planet. It does show our tools found a real planet crossing that nobody has written about yet.

**2. But our search often misses this planet.** We ran the exact same search on the older crossings that scientists already measured (2018-2023). TESS has 6 of them in clean data. **Our search found 3 of the 6.** Why it missed the others:
- In **3**, the dip was there but too shallow for our strict "is it a dip?" rule.
- In **1**, our tool mistook the planet's dip for one of the two stars hiding the other, and cut it out.
- **3 more** couldn't be tested: NASA's cleaned light curve had no data at that moment (2 sectors), or there were only 30-minute snapshots (1 sector).

**3. Fake-planet test.** We hid pretend planets in the December 2025 data and asked the search to find them:

| Fake planet size | Found |
|---|---|
| 2-6 × Earth | **0 of 8** at each size |
| 7 × Earth | 7 of 8 |
| 8 × Earth | 8 of 8 |

TOI-1338 b is about 7-7.7 × Earth, **right at the edge** of what our search can see. That explains why we catch only half its crossings.

**What it means for the project.** The search can see Saturn-sized planets but not smaller ones yet. Earlier we estimated it could find planets down to 2-5 × Earth. That estimate assumed a better detection rule than the one we actually use. The fix is known (see "Next" at the bottom). Until it's done, "we found nothing" in a star means only "nothing bigger than about 7 × Earth".

**Words used:** *BTJD* = the TESS clock (days; 4025.6 = 16 Dec 2025). *Sector* = one 27-day TESS stare at a patch of sky. *ppm* = parts per million (2,500 ppm = 0.25% dimmer). *R⊕* = Earth's radius (planet size).

---

## 1. Task 1: published prediction vs our S98 event

### Sources
- **Kostov et al. 2020**, "TOI-1338: TESS' First Transiting Circumbinary Planet", arXiv:2004.07783 (ID and title verified via the arXiv API). Its own future-transit predictions were **not read** this session. Wang & Liu's Table 1 lists predicted mid-times "from ref. 29" (very likely Kostov+2020; not checked). Those differ from the observed S27-S68 times by 0.02-0.61 d. Example: S65 predicted 3084.8165, observed 3085.4243.
- **Wang & Liu 2024**, "Photo-dynamical Analysis of Circumbinary Multi-planet system TOI-1338: a Fully Coplanar Configuration with a Puffy Planet", **arXiv:2404.18415** (ID verified via the arXiv API; title and authors Mu-Tian Wang and Hui-Gen Liu, Nanjing, read from the HTML). This is a photodynamical fit (3-body + planet c) to TESS sectors 3-68 plus ESPRESSO radial velocities. **Table 3 lists future primary transits of b in BJD − 2,455,000.** I checked the 2025-12-16 row directly in the raw HTML (`6025.5927 ± 0.0159`, `2025-12-16 02:13:28.3`, `6.31 ± 0.15` h, b = `0.428 ± 0.050`).

Since an explicit dynamical prediction exists for Dec 2025, **the rebound 3-body model the brief allowed as a fallback was not needed and not built.**

### Predicted transits in our S97-S98 window (Wang & Liu Table 3; BTJD = their value − 2000)

| UTC | BTJD | Duration | Observed by us? |
|---|---|---|---|
| 2025-09-14 05:34 | 3932.7322 ± 0.0183 | 10.00 ± 0.19 h | **No.** Our S97 2-min light curve (hard quality mask) starts at BTJD 3936.42, 3.7 d later. |
| **2025-12-16 02:13** | **4025.5927 ± 0.0159** | **6.31 ± 0.15 h** | **Yes: our event** |

### Our measurement (fit_event.py, chi2_grid.py)
SPOC PDCSAP 2-min data, hard mask, window BTJD 4025.10-4026.20 (after the primary-eclipse mask). Model: batman single transit + linear baseline. Limb darkening from the paper (q1 0.17, q2 0.478). Impact parameter fixed at the predicted 0.428. I mapped χ² over mid-time × duration, fitting only planet size and baseline at each grid point. Flux errors were scaled ×0.95 so the best fit has reduced χ² = 1.

| | Predicted (Wang & Liu 2024) | Observed (ours) |
|---|---|---|
| Mid-time (BTJD) | 4025.5927 ± 0.0159 | **4025.632 ± 0.002** (white noise only) |
| Duration | 6.31 ± 0.15 h | **6.4-6.5 h** (Δχ²<1 range) |
| Depth | (R_b = 7.66 R⊕ on 1.313 R☉ → rp² ≈ 2,860 ppm) | ~2,450-3,100 ppm (fit-dependent) |
| Δt | | **+57 min**, 2.4σ using the combined error |

- Transit vs no-transit: Δχ² ≈ 230 over 792 points. The dip is a strong signal in 2-min data; the 30-min SNR ≈ 8 quoted in wave 3 was conservative.
- Fixing the predicted mid-time and duration costs Δχ² ≈ 65 against the best fit. So the ~1 h offset is real at the level of *our* white-noise error. The ±0.002 d error ignores red noise and the detrending choice, so the real error is probably several times larger. **Honest summary: same transit, ~1 h late, at ~2-2.5σ given the prediction's own uncertainty.**
- **Friction:** my first direct `curve_fit` with free impact parameter landed in a local minimum (T14 = 11.8 ± 6 h, χ² 820, worse than the constrained fit). I replaced it with the grid. The free-b result is not used.

**Outcome logged in `research/predictions.md`: RIGHT** (the ~80% call that the S98 event is a TOI-1338 b transit).

## 2. Task 2: recovering the published transits (recovery.py, diagnose_misses.py, mask_check.py)

Ground truth: Wang & Liu 2024, Table 1 (TESS mid-times; S30 has no fitted time because of a damaged egress, so I used the paper's predicted 2142.3991). Method: the wave-3 search, unchanged, run per sector (`method.py`). A transit counts as recovered if an event is centred within 0.5 d of the published time.

| Sector | Published mid (BTJD) | Dur (h) | Cadences at transit (after eclipse mask) | Depth in window after 1-d detrend | Result (1-d window, as in wave 3) | Why |
|---|---|---|---|---|---|---|
| 3 | 1391.2516 | 8.6 | n/a | n/a | **not testable** | No SPOC 2-min LC on MAST; only 30-min FFI (eleanor-lite, TASOC, TARS). The method needs ≥5 cadences per 30-min bin |
| 6 | 1483.9048 | 6.0 | 179/179 | 2,093 ppm | **recovered**, centre −0.49 h, SNR 8.5 | |
| 10 | 1579.0423 | 11.6 | 0/339 | n/a | **missed** | Per-sector BLS locked onto the *secondary* eclipse (0.37%) as "primary". The fixed-period second pass then found the planet transit (T = 1579.068, 9.7 h) and **masked it as a "secondary eclipse"** |
| 27 | 2049.9515 | 7.2 | 215/215 | 1,524 ppm | **missed** (recovered with a 3-d window) | Below the "≥3 consecutive 30-min bins < 3 MAD" rule |
| 30 | (2142.3991 pred.) | n/a | 0 | n/a | **not testable** | PDCSAP is NaN there even with the default mask; SAP has 263 cadences |
| 34 | 2238.2258 | 9.6 | 288/288 | 1,486 ppm | **missed** (all windows) | Below threshold; a long transit is suppressed by the 1-d biweight |
| 37 | 2331.0148 | 5.9 | 176/176 | 1,813 ppm | **missed** (all windows) | Below threshold (~2.7 MAD per bin; the rule needs 3) |
| 62 | 2989.6356 | 7.7 | 0 (hard) | n/a | **not testable** | PDCSAP NaN at the transit (8 hard-mask cadences only from 2989.82); SAP has 288 cadences |
| 65 | 3085.4243 | 10.2 | 308/308 | 1,532 ppm | **recovered**, centre +0.48 h, SNR 7.9 | |
| 68 | 3178.2853 | 6.2 | 143/186 | 1,887 ppm | **recovered**, centre −1.65 h, SNR 6.7 (lost at 2-d window) | |
| *98 (ours)* | *4025.5927 (pred.)* | *6.3* | | | *recovered* | |

**Score:** 3 of 6 testable published transits (50%). Counting the S98 event: 4 of 7. False events in these sectors at the 1-d window: S6 (1471.56, 3,754 ppm) and S65 (3090.20, 4,200 ppm); both are deep and not investigated (open question). "Centre" is the middle of the flagged bins, not a timing fit; those offsets are not timing measurements.

**Failure modes found (all fixable):**
1. **Eclipse masking from per-sector BLS is unsafe.** It can take a planet transit for an eclipse (S10). Use the published binary ephemeris (P_B = 14.6085659 d) or a joint all-sector fit, and check that the masked "secondary" falls at the known phase (0.454).
2. **The consecutive-bins rule is much weaker than a matched filter.** S37 sits at ~2.7 MAD per bin for 12 bins, a matched-filter SNR of ~9, and is still missed.
3. **1-d biweight eats long transits** (S27, S34: 7-10 h). Use a window ≳3 × the longest expected duration, or a transit-masked / iterative detrend.
4. **PDCSAP gaps:** at S30 and S62, SPOC blanked PDCSAP where SAP exists. Wang & Liu still measured S62, so a SAP fallback would make these testable.

## 3. Task 3: injection-recovery smoke test (inject.py)

S98 PDCSAP, hard mask, eclipses masked once from the real data, real event (4025.30-4025.95) removed. 8 random out-of-eclipse mid-times (seed 42; ≥90% in-transit coverage). batman transits with b = 0.4, duration 6.4 h (a/R* = 108; an `assert` checks the injected duration), TOI-1338 A limb darkening, R* = 1.313 R☉. Recovered = event centred within 0.25 d. 30-min MAD = 566 ppm. **No events in the un-injected data** (0 false alarms in S98 with the real event removed).

| R (R⊕) | Depth (ppm, rp²) | Recovered |
|---|---|---|
| 2 | 195 | 0/8 |
| 3 | 439 | 0/8 |
| 4 | 780 | 0/8 |
| 5 | 1,219 | 0/8 |
| 6 | 1,755 | 0/8 |
| 7 | 2,389 | 7/8 |
| 8 | 3,120 | 8/8 |

The method's real single-transit threshold on this star is a **depth of ~2,000-2,400 ppm (≈4 × the 30-min MAD)**. That is ~7 R⊕ on a 1.31 R☉ star. **This is much less sensitive than the wave-3 feasibility table**, which assumed SNR-7 matched filtering: 2-5 R⊕ at Tmag 10-13. That table describes what the *data* allow, not what our *current rule* achieves.

**Friction:** the first injection run returned 0/56 even at 8 R⊕. The cause was a bug in my a/R* formula (a stray P/π factor gave a/R* ≈ 3,300, i.e. ~3-minute injections). I found it because 0% at 5.5 × MAD was not believable. It's fixed, and the script now asserts the injected duration.

## Next (recommended)
1. Swap the event rule for a matched-filter single-transit search (box/transit template SNR over durations of 3-15 h). Then re-run this recovery + injection test as the acceptance check.
2. Mask eclipses from a global binary ephemeris and check the eclipse identity (depth and phase) per sector.
3. Detrend with a window ≳3× the longest duration, or mask the transit and iterate.
4. Fall back to SAP flux where PDCSAP is NaN.
5. Optional science follow-up: the S98 mid-time (+57 min vs Wang & Liu) is a new, unpublished timing point for TOI-1338 b. It is worth a careful red-noise error estimate (e.g. residual permutation / time-correlated noise) before anyone treats the offset as meaningful.

## Files
`method.py` (wave-3 method as functions) · `fit_event.py` → `fit_event_results.json`, `fit_event_data.npz` · `chi2_grid.py` → `chi2_grid_results.json`, `chi2_grid.npz` · `recovery.py` → `recovery_results.json`, `recovery_log.txt` · `diagnose_misses.py` → `diagnose_results.json` · `mask_check.py` · `inject.py` → `inject_results.json`, `inject_log.txt` · `summary_png.py` → `burn1_summary.png` · `log_downloads.py`.
