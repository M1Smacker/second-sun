# Vetting page for Second Sun: research brief for Claude Code

*Written 2026-10-23 by Claude (research session with web access). Tags: `[READ]` = primary or official source opened in this session; `[READ-2]` = read only through a secondary page (press release, Wikipedia, summary); `[MEMORY]` = from training, not opened now; `[INFERRED]` = my own reasoning or recommendation. Every "do this" line not tied to a source is my recommendation and is marked `[INFERRED]`.*

---

## 0. The ten decisions that matter most

1. **Both reviewers classify blind and independently, then reveal.** The AI's label, score and reasoning, the pipeline SNR, the star's name or TIC, and any known-planet status stay hidden until both labels are locked. Incorrect AI suggestions cut correct BI-RADS assignments by inexperienced radiologists from nearly 80% to under 20%, and by very experienced ones from 82% to 45.5% `[READ-2: RSNA press release on Dratsch et al. 2023, Radiology]`. Planet Hunters TESS hides TIC IDs until after classification "in order to reduce biases" `[READ: Eisner et al. 2021 §2]`.
2. **Hidden controls with known answers, mixed in at a falling rate, with immediate feedback.** Planet Hunters TESS showed simulated transits in 30% of a volunteer's first 10 subjects, falling to 1% by 100, and always told the volunteer afterwards `[READ: Eisner et al. 2021 §2.1]`. Space Warps started at about 2 in 5 and never let the rate fall below 10% "to keep volunteers alert" `[READ: Marshall et al. 2016 §2.2.2]`. Use controls for every class, not just planets (section 5).
3. **Fix the y-axis to the noise, never auto-scale each zoom.** Auto-scaling stretches pure noise to fill the panel, so every wiggle looks like a dip `[INFERRED]`. Set the range from the star's out-of-event scatter and show a ±1σ band (section 2).
4. **Show raw points faint and binned points bold, as the Kepler DV reports do.** DV plots use small raw points with "cyan-filled blue circles" for phase-binned averages and a red model line `[READ: Kepler DV one-page companion]`. On a phone, 2-minute raw points are just a grey cloud; the binned points carry the judgement `[INFERRED]`.
5. **No transit model on screen during the blind pass.** A planet-shaped model drawn over the data is itself a suggestion `[INFERRED, by analogy with automation bias, 1]`. Show model fits only after both labels are locked.
6. **Make "unclear" a full, equal option.** The TESS team's own vetting tool includes "U (undecided, ambiguously transit-like)", and vetters are "trained to be generous", so any PC or U goes on to group review `[READ: Guerrero et al. 2021 §7.1]`. "Unclear" should be the same size and weight as the other five buttons `[INFERRED]`.
7. **Counter the rarity of real planets.** In visual search, error rates were about 7% at 50% target prevalence, 16% at 10% and 30% below 1% `[READ-2: Wikipedia "Prevalence effect", citing Wolfe, Horowitz and Kenner 2005, Nature 435, 439]`. Real circumbinary transits will be extremely rare in your queue, so hidden planet-like controls also serve to keep the prevalence the reviewer experiences above zero `[INFERRED]`.
8. **Add a "lineup" test for marginal events.** Put the real event window among a few null windows (same star, same scale, other times or flipped data) and ask which one has a dip. This is the lineup protocol of Buja et al. 2009, where plots act as test statistics and human eyes as the test; their "Rorschach" protocol (looking at nulls first) helps people "acclimatize to random variability" `[READ: Wickham's summary page of Buja et al. 2009, Phil Trans R Soc A 367, 4361]`. If Ahmed cannot pick the real one, it is not a convincing dip `[INFERRED]`.
9. **Score each reviewer separately for "sees dips" and "says yes"** (signal detection: d′ and criterion c), plus a per-class confusion matrix and Cohen's κ between reviewers (section 5) `[MEMORY: standard methods]`.
10. **Portrait, linear time axis, panels stacked and x-aligned, big buttons in the thumb zone.** On phones, linear layouts were faster than radial ones, and the study ran in portrait only `[READ: Brehmer et al. 2019, IEEE TVCG]`. Touch targets at least 24 × 24 CSS px by WCAG 2.2 AA `[READ: W3C Understanding 2.5.8]`; I recommend 48 px tall `[INFERRED]`.

---

## 1. What the professional and citizen-science tools show

| Tool | Panels (in their order) | What to borrow |
|---|---|---|
| **Kepler DV one-page summary** `[READ]` | A: full light curve with quarter boundaries and triangles under each predicted transit (red if coincident with rolling-band artefacts); B: full-orbit fold with binned points and red model; C: secondary-eclipse fold, with depth, phase and MES in the header (MES coloured red if above 7.1); D: transit-only fold, x in **hours**; E: whitened fold with residuals offset below; F: odd/even side by side with the joint depth line and its error; G: centroid offsets in arcsec, target at (0,0), 3σ circle; H: parameter and diagnostic table | Hours on the x-axis of zooms; raw plus binned points; markers under the axis for event times and for artefact coincidences; diagnostics as numbers in a header, not prose |
| **TESS TOI vetting (TEV)** `[READ: Guerrero et al. 2021 §5, §7]` | SPOC DV one-page summary, full report and mini-report; QLP report pages for multi-aperture depth, centroids and difference images; vetters also use odd-even plots, finder charts and estimated radius | Five dispositions: PC, EB, V (variability), IS (instrumental/systematic), U (undecided); 3 to 5 independent vetters, then group vetting with at least 3; any PC or U goes forward; ties among non-planet labels default to EB |
| **LATTE** `[READ: Eisner, Lintott and Aigrain 2020, JOSS 5, 2101]` | momentum dumps; target properties; background flux; x and y centroids; two-aperture light curves; average in-transit, out-of-transit and difference images; nearby stars brighter than T 17 on DSS with Gaia positions; five nearest 2-minute neighbours' light curves; per-pixel light curves; two-step BLS | Every panel is aligned to the event time. For a single circumbinary event, background, centroid, apertures, neighbours and pixels are the panels that catch impostors |
| **DAVE / Triple-9** `[READ: Magliano et al. 2023, arXiv:2303.00624]` | DAVE centroid difference images; "Modelshift" fold with trapezoid model, secondary and odd/even panels; transit-masked periodogram; background in a 4-day window around each transit; LATTE-style pixel light curves; eleanor and QLP compared on one portal | At least 3 vetters including one core-team member; each vetter weighted by a precision score against an earlier catalogue (0.67 to 0.97); short comment codes such as CO (centroid offset), OED (odd-even difference), LowSNR |
| **Planet Hunters TESS** `[READ: Eisner et al. 2021 §2, §3]` | One question, "Do you see a transit?"; volunteers draw a column over each event, as many as they like; early sectors in ~7-day chunks, later one full light curve with x-axis zoom; subject info panel | Simulated transits only above SNR 7 (UI1) or 4 (UI2); feedback after every simulation; volunteer weights capped 0.05 to 3; aggregation by clustering marks (DBSCAN, 1-day ε, at least 4 marks); TIC hidden until after classifying |

**What vetting removed in practice.** In Planet Hunters TESS, discards were mostly momentum dumps and background events, and among LATTE-stage discards about 40% were eclipsing binaries and 25% systematics `[READ: Eisner et al. 2021 §5]`. For TESS TOIs overall, about 25% of prime-mission TOIs later proved false positives despite human vetting `[READ: Guerrero et al. 2021 §7.3]`. For the TOI-1338 b discovery, fake dips were traced to pointing jitter just before momentum dumps `[READ: your register F-022, from Kostov et al. 2020]`.

---

## 2. Panels, zoom levels, axes, markers and colours

### 2.1 The panel stack (top to bottom, all time panels sharing one x-axis where they show the same window)

| # | Panel | Window | Why | Source |
|---|---|---|---|---|
| P1 | **Context strip**: whole sector | full sector | Shows gaps, orbit starts, eclipses, momentum dumps and where the event sits; catches "it's at a gap edge" | DV panel A; LATTE dumps `[READ]` |
| P2 | **Event zoom**: raw (faint) + binned (bold), ±1σ band, baseline line | event ± max(1 d, 3 × duration) | The main judgement: shape, ingress and egress, local trend | DV panel D (hours axis) `[READ]` |
| P3 | **Binary-phase strip**: one row showing where the event falls relative to primary and secondary eclipse phases | 0 to 1 in binary phase | The single most circumbinary-specific check: events stacked at eclipse phases are eclipse leakage | your rule C5 `[READ: wave-4 report]`; `[INFERRED]` |
| P4 | **Same window, second product** (QLP or SAP vs PDCSAP) | as P2 | Real dips appear in independent extractions | Triple-9 eleanor vs QLP; TOI-1338 used eleanor and SPOC `[READ]` |
| P5 | **Background flux** | as P2 | Rules out scattered light and asteroids | LATTE, Triple-9 `[READ]` |
| P6 | **Centroid x and y** | as P2 | Blends | LATTE, DV panel G `[READ]` |
| P7 | **Detrending robustness**: the event under 3 to 5 windows, overlaid thin | as P2 | A dip carved by detrending changes shape across windows | Davies et al. keep events found in ≥18 of 21 windows (your wave-4 V5) `[READ via your register]` |
| P8 | **Pixels / difference image** | event vs out-of-event | Second stage only (heavy on a phone) | LATTE, DAVE `[READ]` |

On a phone, show P1 to P3 by default and P4 to P7 behind a single "more evidence" toggle that opens them all at once, so both reviewers always see the same evidence set before deciding `[INFERRED]`. P8 belongs to a later vetting step, not first-pass classification `[INFERRED]`.

### 2.2 Axes
- **x-axis in hours from the event centre** on zoom panels, as DV panel D does `[READ]`; time in days (BTJD) only on the context strip `[INFERRED]`.
- **y-axis in ppm (parts per million) relative to the local baseline**, not raw counts or "normalised flux 0.998" `[INFERRED]`.
- **Fixed y-range per star**, from the out-of-event robust scatter σ: range = baseline ± max(6σ_binned, 1.5 × event depth). The same range on P2, P4 and P7. Never autoscale per window `[INFERRED]`.
- **Clip the binary's eclipses** on P1 (draw them as shaded bands reaching off the bottom of the panel with a small "eclipse, 6%" label), otherwise a 6% eclipse squashes a 0.2% dip to nothing `[INFERRED]`.
- **Aspect ratio.** Banking to 45° chooses the aspect ratio so the average line slope is near 45°, to maximise "the discriminability of the orientations of the line segments" `[READ: Heer and Agrawala 2006]`. For dips that means giving P2 enough height that ingress and egress are visibly sloped: about 0.55 to 0.6 of its width on a phone `[INFERRED]`.

### 2.3 Markers
- Binned points: filled circles, about 5 px; raw points: 1.5 px at 25% opacity `[INFERRED, following DV's raw plus binned convention]`.
- Event window: a light shaded column in P1 and a thin bracket above the data in P2, not a box drawn over the data `[INFERRED]`.
- **Momentum dumps:** small ticks along the bottom of every time panel (DV and LATTE both mark artefact times along the axis `[READ]`). Mark the 0.5 days before each dump with a faint hatch, matching your rule C7 `[INFERRED]`.
- Data gaps: draw as visible breaks, not lines joining across `[INFERRED]`.
- Quality-flagged cadences that were dropped: hollow ticks on the context strip, so "nothing here" is distinguishable from "data removed here" `[INFERRED]`.

### 2.4 Colours (colour-blind safe)
Use the Okabe and Ito palette `[READ: palette codes from a reference page; the palette is Okabe and Ito 2008, popularised by Wong 2011, Nature Methods 8, 441, cited by the R factoextra docs]`: orange `#E69F00`, sky blue `#56B4E9`, bluish green `#009E73`, yellow `#F0E442`, blue `#0072B2`, vermillion `#D55E00`, reddish purple `#CC79A7`, black `#000000`.

| Element | Colour `[INFERRED]` |
|---|---|
| Raw points | text colour at 25% opacity |
| Binned points | blue `#0072B2` (sky blue `#56B4E9` in dark mode) |
| ±1σ band | grey at 12% |
| Event window shading | orange `#E69F00` at 15% |
| Eclipse bands | neutral grey hatch |
| Momentum dumps | vermillion `#D55E00` |
| Second product (P4) | bluish green `#009E73` |
| Models (after reveal only) | reddish purple `#CC79A7` |

Never encode a class judgement in colour (no green "planet", red "fake") before the reveal `[INFERRED]`. Keep text contrast at least 4.5:1 `[MEMORY: WCAG 1.4.3]`.

---

## 3. What causes human mistakes, and the countermeasure for each

| Error | Evidence | Countermeasure |
|---|---|---|
| **Anchoring on another reviewer's or the AI's label** | Dratsch et al. 2023 (1) `[READ-2]`; automation bias is "the tendency to over-rely on automation", made worse by workload, task complexity, time pressure and trust, and reduced by training, accountability, showing confidence and "providing information rather than a recommendation" `[READ: Goddard, Roudsari and Wyatt 2012, JAMIA 19, 121]`; anchoring in general `[MEMORY: Tversky and Kahneman 1974, Science 185, 1124]` | Blind protocol (section 4). After reveal, show the AI's evidence and confidence, not just its label |
| **Rare-target misses (prevalence effect)** | Error 7% at 50% prevalence, 30% below 1% `[READ-2]`; high-prevalence training with feedback reduced later misses, but the same page warns feedback can also magnify prevalence effects `[READ-2]` | Planet-like hidden controls at 20 to 30% early, never below about 10% `[INFERRED, following Space Warps' 10% floor READ]` |
| **Over-reading noise (seeing dips that aren't there)** | Space Warps false positives where "volunteers clicked many different features" `[READ]`; your own flipped-data test finds SNR 7 to 12.6 "dips" in pure systematics `[READ: your F-016]` | Fixed y-range; ±1σ band; null controls (flipped and random windows); the lineup test (0.8) |
| **Seeing only part of a pattern** | PHT volunteers often marked only some transits in short-period systems `[READ: Eisner et al. 2021]` | For a circumbinary pair, ask "any other dip within ±2 binary periods?" as a separate question after the class `[INFERRED]` |
| **Detrending or instrumental artefacts look real** | PHT discards mostly dumps and background; TOI-1338 pre-dump jitter `[READ]` | Dump ticks and pre-dump hatch on every panel; background panel (P5) |
| **Inconsistency between and within reviewers** | Kepler's human vetters "do not always agree with each other" and dispositions can depend on "external factors", which is why the team moved to the automated Robovetter for uniformity `[READ: Coughlin et al. 2016 §3]` | Written decision rules per class, shown in a field-guide drawer; periodic re-showing of already-classified items (unannounced) to measure self-consistency `[INFERRED]` |
| **Practice effects** | PHT recovery of TCEs rose across sectors, suggesting volunteers improve with practice `[READ]`; Space Warps skill rose with number of classifications `[READ]` | Track accuracy over time; don't trust early classifications without controls `[INFERRED]` |
| **Fatigue and order effects** | `[MEMORY: general vigilance literature]` | Sessions of about 20 items; randomise order; never show events from the same star consecutively `[INFERRED]` |
| **Reference pictures as anchors** | `[INFERRED]` | Field guide with one example per class in a drawer that is closed by default, not on the decision screen |

---

## 4. Protecting the second reviewer (blind protocol)

The literature I found supports blinding in principle (1, 3) but I did not find a study measuring blinded against informed second reading directly. The UK CO-OPS cohort reports that 12 of 33 screening centres used workflow systems built to hide the first reader's decision, and notes that readers who could see the first decision would make the second reader's added value look smaller `[READ: Taylor-Phillips et al. 2018, Radiology 287(3), per the RSNA journal page]`. Protocol `[INFERRED]`:

1. **Each item is shown to both reviewers with identical panels and no identifying metadata.** No TIC, no Tmag, no SNR, no pipeline score, no "known planet" badge, no previous labels.
2. **The AI classifies first, writes its label, confidence (0 to 100) and a two-line reason to storage, and the page never displays them until Ahmed has locked his own.** Running the AI in a fresh context per item, without Ahmed's history, keeps it independent too.
3. **Ahmed classifies, gives a confidence (three steps is enough on a phone: low, medium, high), optionally taps one reason chip** (shape, timing, gap or dump, eclipse phase, other product, background), **then locks.** A locked label cannot be edited; a later change is stored as a new "revised" record with a timestamp.
4. **Reveal both labels side by side**, then the evidence the AI used, then (if the item was a control) the truth, with feedback.
5. **Disagreements go to a third, independent look**: a fresh AI session with no access to either label, or a later re-showing to Ahmed in a different week. Store all three.
6. **Record who switched after the reveal.** If Ahmed switches to the AI's label far more often than the AI's label is right on controls, that is measured automation bias.
7. **Order and timing:** randomise item order separately for each reviewer; don't show the next item from the same star; store time-on-item.
8. **The "two keys" rule stays:** a candidate needs both locked labels to be planet-like before discussion, or one planet-like plus a confirmed agreement after the third look.

---

## 5. Measuring reviewer accuracy with hidden controls

### 5.1 Control types (all built from your own data so they look exactly like real items)

| True class | How to make a control | Notes |
|---|---|---|
| Planet-like | Inject realistic circumbinary transits (your STANLEY N-body timing and batman shapes) into real G1 windows at SNR 6 to 15 | PHT showed simulations only above SNR 7 (later 4) `[READ]`; include some near your threshold, since that is where judgement matters |
| Planet-like (real) | Known TOI-1338 b transits | Use only if hidden by removing all identifying information |
| Eclipse | Windows containing a real eclipse with the mask turned off, scaled into the same y-range, or a secondary eclipse of a G1 binary | Tests whether eclipse leakage is recognised |
| Instrumental | Known impostors: your Kepler-16 S54 pre-dump dip; events from the flipped-data runs flipped back; scattered-light ramps at orbit starts | |
| Flare | Real flares found in G1 or TOI-1338 data, or injected fast-rise exponential-decay shapes | |
| Step | Windows containing a real flux discontinuity, or an injected step | |
| Noise / unclear | Random event-free windows, and flipped data | Pure noise should be labelled unclear (or not planet-like) |

### 5.2 Mixing rate and feedback
Start at about 30% controls for the first 20 to 30 items, fall to about 10 to 15%, never below 10% `[INFERRED, following PHT READ and Space Warps READ]`. Give feedback right after each control (both projects did `[READ]`), but log that the item was a control so later stats can separate "before feedback" from "after feedback" `[INFERRED]`.

### 5.3 Metrics `[MEMORY: standard statistics; numbers RAN in my sandbox]`
- **Per-class confusion matrix** on controls, and per-class recall (how many true eclipses were called eclipse, etc.).
- **Planet-like versus not, as signal detection:** hit rate H on planet-like controls, false-alarm rate F on all non-planet controls; sensitivity d′ = z(H) − z(F) and criterion c = −(z(H) + z(F))/2, where z is the inverse normal. Example: H = 0.8, F = 0.1 gives d′ = 2.12, c = 0.22; H = 0.9, F = 0.3 gives d′ = 1.81, c = −0.38, a reviewer who sees slightly less but says "planet" more freely `[RAN]`. This separates "can't see it" from "too keen".
- **Agreement between Ahmed and the AI on real items:** Cohen's κ, which corrects raw agreement for chance.
- **Calibration:** for each confidence level, the fraction of controls labelled correctly (should rise with confidence); Brier score if using 0 to 100 confidence.
- **Self-consistency:** agreement with oneself on repeated items.
- **Persuasion index:** switches after reveal, split by whether the other reviewer was right.

### 5.4 How many controls you need
Accuracy from few controls is very uncertain. 95% Wilson intervals: 16 of 20 correct is 0.58 to 0.92; 18 of 20 is 0.70 to 0.97; 45 of 50 is 0.79 to 0.96; 90 of 100 is 0.83 to 0.94 `[RAN]`. So: about 50 controls before quoting any accuracy number, and at least 20 per class before quoting per-class recall `[INFERRED]`. Space Warps needed about 10 classifications per subject from a crowd to reach a decision `[READ]`; you have two reviewers, so every disagreement matters more and the third look (4.5) is essential `[INFERRED]`.

### 5.5 Weighting (later)
Once you have enough controls, weight each reviewer by their measured confusion matrix, as Space Warps did with a 2 × 2 matrix per volunteer updated from training images `[READ]` and as Triple-9 did with a precision score per vetter `[READ]`. With two reviewers this is mainly a diagnostic, not an aggregation rule `[INFERRED]`.

---

## 6. Phone layout (portrait, 390 × 844 CSS px class of screen)

All sizes `[INFERRED]` unless tagged.

```
┌──────────────────────────────── 390 px ┐
│ Item 7 of 20 · session timer · (no star name)  │  44 px header
├────────────────────────────────────────────────┤
│ P1 Context strip: full sector, eclipses clipped │  96 px
│    dump ticks, gaps, event column (orange)      │
├────────────────────────────────────────────────┤
│ P2 Event zoom (hours from centre, ppm)          │  220 px
│    raw faint · binned bold · ±1σ band · dumps   │
├────────────────────────────────────────────────┤
│ P3 Binary phase strip: 0 ─ prim ─ sec ─ 1  ●    │  44 px
├────────────────────────────────────────────────┤
│ [ More evidence ▾ ] opens P4 to P7 (scroll)     │  44 px
├────────────────────────────────────────────────┤
│ Planet-like │ Eclipse │ Flare                    │  2 rows of
│ Step        │ Instrum.│ Unclear                  │  3 buttons, 52 px each
├────────────────────────────────────────────────┤
│ Confidence: Low · Med · High   [ Lock ]         │  52 px
└────────────────────────────────────────────────┘
```

- **Side gutter 16 px, panels full width (358 px).** P2 at about 220 px tall gives an aspect ratio near 0.6 (2.2).
- **Buttons:** six equal buttons, at least 48 px tall (WCAG minimum is 24 × 24 CSS px with spacing exceptions `[READ: W3C 2.5.8]`), in the bottom third where thumbs reach. No button is pre-selected or highlighted. "Unclear" is identical in size and style.
- **Interactions:** pinch or drag to zoom the x-axis of P2 only (PHT added x-zoom in its second interface `[READ]`); y never zooms; double-tap resets. Tapping P1 recentres P2. "More evidence" opens all secondary panels together so the evidence seen is logged (store `evidence_opened: true/false`).
- **Lock flow:** class, then confidence, then Lock. After Lock, the reveal card slides up: AI label and confidence, AI's two-line reason, truth and feedback if it was a control, and "Discuss" for disagreements.
- **Landscape:** allow rotating P2 alone to full-screen landscape for a closer look; the classification controls stay on the portrait screen `[INFERRED]`.
- **Dark mode:** swap binned blue to sky blue `#56B4E9`; keep the grey band visible (raise to 18%).
- **Performance:** pre-bin on the server; send at most about 2,000 points per panel; draw on canvas `[INFERRED]`.

---

## 7. What to log per classification `[INFERRED]`

`item_id, star_id (hidden from UI), sector, window, is_control, control_truth, reviewer (ahmed|ai|ai_third), label, confidence, reason_chip, evidence_opened, time_on_item_s, locked_at, revealed_at, revised_label, revised_at, order_index, session_id, ui_version, y_range_ppm, binning_min, detrend_window_d, product`. Version the UI: any change to panels or scaling starts a new accuracy baseline.

---

## 8. What I could not verify

The original Wolfe et al. 2005 Nature paper (numbers taken from Wikipedia's summary); Dratsch et al. 2023 itself (numbers from the RSNA press release); the Okabe and Ito source page (hex codes from a secondary reference page, and they match what I remember); the full Buja et al. 2009 paper (I read only the abstract page, so I cannot confirm their recommended lineup size of 20, which I remember but have marked as memory); and any published study of anchoring specifically in exoplanet vetting (I found none). I also did not find a published blinded-versus-informed double-reading comparison in astronomy; the radiology evidence is indirect.

---

## Sources
- [Eisner et al. 2021, Planet Hunters TESS II, MNRAS 501, 4669 (Oxford repository PDF)](https://ora.ox.ac.uk/objects/uuid:b2e7db4a-dd3a-4996-aeab-bc050616947d/files/rbn999706m)
- [Eisner, Lintott and Aigrain 2020, LATTE, JOSS 5, 2101](https://joss.theoj.org/papers/10.21105/joss.02101.pdf)
- [Description of the Kepler DV one-page summary reports (DR25)](https://exoplanetarchive.ipac.caltech.edu/docs/DVOnePageSummaryPageCompanion-dr25-V7.html)
- [Guerrero et al. 2021, TESS Objects of Interest catalogue, arXiv:2103.12538](https://arxiv.org/pdf/2103.12538)
- [Magliano et al. 2023, TESS Triple-9 Catalog II, arXiv:2303.00624](https://arxiv.org/pdf/2303.00624)
- [Kostov et al. 2019, DAVE, arXiv:1901.07459](https://arxiv.org/pdf/1901.07459) (found, not opened in detail)
- [Marshall et al. 2016, Space Warps I, arXiv:1504.06148](https://arxiv.org/pdf/1504.06148)
- [Coughlin et al. 2016, Kepler DR24 catalogue and Robovetter, arXiv:1512.06149](https://www.arxiv.org/pdf/1512.06149)
- [Goddard, Roudsari and Wyatt 2012, Automation bias review, JAMIA 19, 121](https://academic.oup.com/jamia/article/19/1/121/732254)
- [RSNA press release on Dratsch et al. 2023, Radiology](https://www.rsna.org/media/press/i/2432)
- [Taylor-Phillips et al. 2018, Double reading in the CO-OPS trial, Radiology](https://pubs.rsna.org/doi/full/10.1148/radiol.2018171010)
- [Wikipedia, Prevalence effect (summary of Wolfe et al. 2005)](https://en.wikipedia.org/wiki/Prevalence_effect)
- [Buja et al. 2009, Statistical inference for exploratory data analysis (abstract page)](https://vita.had.co.nz/papers/inference.html) · [Roy Chowdhury et al., lineups, arXiv:1408.1889](https://arxiv.org/pdf/1408.1889)
- [Brehmer et al. 2019, Visualizing ranges over time on mobile phones, IEEE TVCG](https://terpconnect.umd.edu/~choe/download/TVCG-2019-Brehmer-Mobile.pdf)
- [Heer and Agrawala 2006, Multi-scale banking to 45 degrees](https://idl.uw.edu/papers/banking)
- [W3C, Understanding WCAG 2.2 SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [Okabe-Ito hex reference](https://conceptviz.app/blog/okabe-ito-palette-hex-codes-complete-reference) · [factoextra docs citing Okabe and Ito 2008 and Wong 2011](https://rdrr.io/cran/factoextra/man/factoextra_palette.html)
