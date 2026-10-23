# Compass review: "Vetting page for Second Sun" (outside research brief, Claude AI, 2026-10-23)

*Reviewed 2026-10-24. Review only: no code or page was changed. The brief is saved unchanged at `research/vetting-page-research-2026-10-23/brief.md`; our own checks are in `research/vetting-page-research-2026-10-23/our_checks.py` (re-run them any time).*

Labels: **VERIFIED** (I read the primary text or ran it), **LIKELY** (secondary source, abstract only, or memory consistent with sources), **UNCERTAIN**, **NOT TESTED**.

## 1. Verdict: REVISE (accept about 85%; five corrections, one of them important)

The brief is the best design input we have had for the real-candidate page. It does not need to be rejected or rebuilt. But five of its points are wrong or incomplete for our case, and two things in OUR OWN current Eyes mode that it exposes matter more than anything in the brief.

## 2. What is correct (and which parts we already had)

| Claim in the brief | Status | Note |
|---|---|---|
| Hide the star's name/TIC until after classifying; PHT does it "to reduce biases" | **VERIFIED** (Eisner et al. 2021 full text, ar5iv) | We already hide everything in Eyes mode. |
| PHT simulated-transit rate: 30% for the first 10 classifications, falling to 1% by 100 | **VERIFIED** (same paper) | Note: PHT goes down to 1%, the brief's "never below 10%" comes from Space Warps. |
| Space Warps: minimum training rate 10% "to ensure that the inspectors remained alert" | **VERIFIED** (Marshall et al. 2016 full text) | Their schedule was about 30%, 20%, then 10% in 20-image steps. |
| TESS vetting has an "undecided" (U) option; any PC or U goes to group vetting; vetters "trained to be generous"; 3 to 5 vetters | **VERIFIED** (Guerrero et al. 2021 full text) | Our "Not sure" button is already equal size to the others (read in `demos.js`). |
| Wilson ranges: 16/20 = 0.58 to 0.92, 18/20 = 0.70 to 0.97, 45/50 = 0.79 to 0.96, 90/100 = 0.83 to 0.94 | **VERIFIED** (I re-computed; exact match) | |
| d-prime and criterion examples (2.12 / 0.22 and 1.81 / -0.38) | **VERIFIED** (re-computed; exact match) | See correction 5 for the zero-count problem. |
| Dratsch et al. 2023: wrong AI suggestions cut inexperienced readers' accuracy from about 80% to under 20% (19.8%) and very experienced readers' from 82% to 45.5% | **LIKELY** (press and trade coverage agree; I did not read the paper) | Small study: 27 readers, 50 mammograms, 12 of 40 suggestions deliberately wrong. Radiology, not astronomy; the brief says so. |
| Rare targets are missed more: about 7% error at 50% prevalence, about 30% at 1% | **LIKELY** (Wolfe et al. 2005 quoted via an NPR interview; the brief's "16% at 10%" I could not confirm) | |
| Lineup of 20 panels (Buja et al.) | **LIKELY** (Roy Chowdhury et al. use m = 20 lineups; I did not open Buja's paper) | The brief marked this `[MEMORY]`; it is right. |
| Okabe-Ito colour codes | **LIKELY** (match my memory and the brief) | See correction 4 for how they fit our dark canvas. |
| Design ideas: fixed y-range, raw faint plus binned bold, no model drawn before both answers are in, "unclear" as an equal button, momentum-dump ticks, a binary-phase strip, hidden controls for every class, d-prime and criterion scoring, per-class confusion matrix, blind lock-then-reveal, log who switches after the reveal | **LIKELY** good practice; **NOT TESTED** on Ahmed | Several already match the two-key method (`research/two-key-method-2026-10-24.md`) and the current Eyes build (no model drawn on the data; answers locked; four equal buttons). |
| Our own facts quoted (F-016: flipped data still gives "dips" up to SNR 12.6; F-022: TOI-1338 pre-dump jitter) | **VERIFIED** (`book/data/claims.csv`) | |

## 3. What needs changing, and why it matters

### Correction 1 (important): the lineup test needs nulls chosen the same way as the event
The brief says to put the real event among "null windows (same star, same scale, other times or flipped data)". Other random times would make every noise peak look convincing.
**Why: the event was picked because it is the biggest dip the search found in the whole sector. A random stretch of noise is not.**
- **VERIFIED by simulation** (`our_checks.py` section 4): with white noise only, no planet at all, an ideal observer picks the "event" window out of 5 in **84%** of lineups when the other four are random stretches (chance is 20%). When the other four are each the best event found by the same search on an independent null series, the ideal observer is at **20%**, exactly chance, which is what an honest lineup must give.
- So: build lineup nulls by running the SAME detector on upside-down copies (we already do this for false alarms), on other stars at the same noise, or on other sectors, and show each run's top event. Never random windows.
- **UNCERTAIN:** upside-down flares become fast-fall, slow-rise dips, which an eye can learn to spot, making flipped nulls easier to reject than real noise. Prefer other-star and other-sector nulls first; use flipped ones only after checking the shapes.

### Correction 2 (important, about our current Eyes mode, not the brief): "quiet" is not quiet in real life
The practice and the official test draw their "quiet" curves as random stretches (`window_("quiet")` in `demos.js` picks any clear start). But everything Ahmed will meet on real data is the machine's biggest-dip event of a whole sector. The simulation in correction 1 is exactly this effect.
**So his false-alarm rate on random quiet curves under-estimates his false-alarm rate on real, pre-selected noise.** The pass line (at most 1 in 10 quiet called a dip) is measured on the easy kind.
Fix: add a "noise at its best" card kind built from the detector's top event on upside-down or null data, in practice, in the test version 2 and in the rehearsal. **VERIFIED** (logic read in the code, effect shown in simulation); **NOT TESTED** on Ahmed.

### Correction 3 (important): the pass line does not carry over to the real layout
Our Eyes test shows a plain 36-hour cutout of one star (TOI-1338, sector 98) with nothing else. The brief's layout (whole-sector strip, zoom, eclipse phase strip, second product) is a different task, and the brief itself says "any change to panels or scaling starts a new accuracy baseline". Passing the current test shows he can spot a dip in a clean cutout, not that he can vet. Also, one star only means one noise level, while our measured noise factor across the 549 stars ranges from about 1.7 to 4 (quartiles).
So the **rehearsal (fake candidates with known answers, in the real layout, on many stars) is no longer optional**: it is the actual readiness test. Current Eyes practice stays useful for learning shapes.
Side notes **VERIFIED in code:** the y-range is a fixed minimum of plus or minus 6,000 ppm that grows only for big events, so spike and eclipse cards have a different axis range from dip and quiet cards (a small leak); and the single real TOI-1338 b card repeats every round, so he may begin to recognise it.

### Correction 4: small fit changes for our book
- Our Eyes canvas is dark in both themes. Computed contrast on the canvas background (#070b14): the brief's blue #0072B2 is **3.8:1** (passes the 3:1 rule for marks, fails our 7:1 rule if used for text), sky blue #56B4E9 is **8.5:1**, orange #E69F00 8.7:1, vermillion #D55E00 5.1:1. Use sky blue for the binned points on our canvas; all text stays at our 7:1 rule (the brief says 4.5:1; our stricter book rule wins).
- Per-star fixed range from noise: fine, but derive it from the star's out-of-event scatter only. The brief's "1.5 times the event depth" lets the axis hint at the depth; clip deep eclipses instead (the brief's own P1 advice).
- Every panel array must be small (about 2,000 points); a deck of 100 items is a few MB. Keep it out of the offline precache or the 50 MB publish limit and the offline size will bite. **NOT TESTED.**

### Correction 5: scoring details the brief leaves out
- d-prime is infinite when hits are perfect or false alarms are zero (**VERIFIED**: H = 1 or F = 0 gives infinity). Use the standard log-linear fix (add 0.5 to each count, 1 to each total): for 17/20 hits and 0/16 false alarms the corrected d-prime is 2.86.
- Our pass line is a point-estimate gate. **VERIFIED by simulation** (`our_checks.py` section 3), the chance to "meet the line" in the first two rounds:

| True skill (hit / false alarm) | Chance to meet the line after 2 rounds | If checked after every round up to 6 |
|---|---|---|
| 95% / 5% | 80% | n/a |
| 90% / 8% | 55% | n/a |
| 80% / 12% | 17% | n/a |
| 75% / 12% | 9% | 12% |
| 70% / 20% | 2% | 2% |

So the line is not lax (a weak reader rarely passes), but it is noisy: a skilled reader fails it 45% of the time on the first try and a middling one passes about one time in six. That is why Claude judges and does not just read the line. Keep the numbers (agreed with Ahmed), add the 95% ranges (already shown), add d-prime and the criterion c next to hit rate and false alarm rate, and have Claude require the lower end of the hit range to be reasonably high before calling him ready.
- Prevalence: the official test has **14 of 30 dips (47%)**; a real queue has a handful of planets among hundreds of events. High-prevalence practice can train a trigger-happy criterion. The criterion c in the record page will show it.
- The brief's falling control rate (30% to 10%) was designed for volunteers who see thousands of items. Ahmed will see tens to hundreds. Recommendation **UNCERTAIN**: keep controls near 25 to 30% for the whole first real pass (fewer items, and we need enough controls to measure him), then lower it only if the queue grows large. To quote a per-class number we need about 50 controls of that class: at 30% planet-like that is roughly 170 items, about 8 sessions of 20.

## 4. Gaps and risks the brief does not address (our situation)

1. **Who is the "AI reviewer"?** The brief assumes an AI that labels from the panels alone, in a fresh context. I am a session that has already seen the machine's scores and the lead list. A fair second key means: render the same panels to images, and have a fresh session (or helper) that sees only the images label them, write the file and hash it BEFORE Ahmed answers. That costs usage and needs Ahmed's yes for any helper (standing rule). **UNCERTAIN:** my reading of a noisy picture by eye is weaker than my numeric checks; I have not measured it. Fix: score my labels on the same hidden controls, so both keys' error rates are measured, not assumed.
2. **The answer key must not ship in the page.** Ahmed said the real page may be public. If the page's data says which items are fakes, the controls are readable by anyone. Keep the key out of the page: the page holds item codes only; the key is a hashed file kept by Claude, joined by the reader after the pass (the same idea as the fingerprinted lead list).
3. **`eyes-core.js` is hard-wired to four answers.** `recordAnswer` refuses any answer not in `NAME`, and `verdict` assumes truth is dip, none or odd. Real mode needs a per-round vocabulary and an optional truth (**tests first**, as already planned). **VERIFIED by reading the code.**
4. **Cloud rules need no change.** The published rules allow any list of up to 200 entries in `a` and any map in `s` (**VERIFIED**, rules text); nested maps already round-tripped in the real end-to-end test. A richer answer (confidence, reason chip, evidence opened, time) fits. **NOT TESTED** with those exact fields; I would add one real round-trip test when the vocabulary is built.
5. **The machine must emit the panel data.** Stage 3 should save, for every event, the binned arrays for the sector strip, the zoom, the second product, dump times, gap edges and the eclipse phase, plus the matching null events. Cheaper to do while the search runs than to re-read the files later.
6. **Time per item:** class, confidence, optional reason, lock is 3 to 4 taps per item. At about 1 minute per item his 40 to 60 minutes a day covers 40 to 60 items. Fine. Keep the reason chip optional.
7. **Button count:** the brief uses six labels (Planet-like, Eclipse, Flare, Step, Instrument, Unclear). My earlier plan had seven. Use the brief's six (two rows of three in the thumb zone); "other variable star" becomes a reason chip.

## 5. Recommended order (greatest value first)
1. **Training record page, with d-prime and criterion.** Small, and it is the instrument that reads the next steps. (Ahmed's go needed.)
2. **"Noise at its best" cards** in practice and in a test version 2, so the false-alarm number means something. Small. (Ahmed's go needed: it changes the test, so the pass line is restarted on the new test.)
3. **Rehearsal deck, then the locked real-candidate page** in the brief's layout, built on many stars with injected fakes and nulls chosen like the events.
4. **Stage 3 emits panel data** when the full search is approved.
5. Only then the real leads, blind, with fakes mixed in.

## 6. The single best next step
Ahmed practises on his phone now (the current Eyes still teaches him the shapes), and I read his first scores with `eyes_scores.py` when he says so. Nothing else is built until he approves the new order above. Weekly usage is about 75% of the 80% cap, so the larger builds wait for the weekly reset in any case. The usage readout says it resets 2026-10-26 at 21:59 UTC (about 01:00 on Tuesday 27 October in Kuwait). I had said "Sunday" in an earlier message; that was wrong.
