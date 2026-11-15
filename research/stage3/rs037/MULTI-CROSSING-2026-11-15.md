# RS-037 findings: can adding up crossings carry P to 0.75? (Claude, Opus 5.5 medium, 15 Nov 2026, 6:40 to 7:00 pm Kuwait)

**Verdict: No, not alone. Adding up crossings is worth about 2 to 4 points of P. The road to 0.75 is mostly elsewhere: about 12 points are planets we DETECT and then hold below tier 1, and about 14 points are planets whose crossings are in the data but never scored. 0.75 sits at or just above the realistic ceiling of everything combined, so it needs nearly every fixable pool closed.** (LIKELY; numbers from Astra 006 captures on the older chain, joined to 023's adopted set B.)

## Correction of what I told Ahmed
I said a combined search was "never built" and that it was likely the road to 0.75. Both too strong. On 30 Oct a rule written first said skip stacking (known two-sun planets mostly have periods over 100 days, so few crossings per star; field note 2026-10-30), Astra ran STANLEY once on TOI-1338 (F-044, F-045: 28% of noise orbits scored above 5 sigma, so its scale needs calibration), and Astra 003 checked STANLEY and mono-cbp feasibility (`research/astra/reports/003-methods.md`). And today's measurement says stacking is a small lever.

## Q1: the ceiling, from our own bench (CONFIRMED as computed; LIKELY as a forecast)
Source: Astra 006 saved, for every planted crossing, the search score (SNR) at the planted time even when nothing was flagged (`scores.json`, sign 1 planted, sign 0 same times without a planet). 1,075 of the 1,098 reference planets joined to 023's config B result. Scripts: `data/rs037/ceiling.py`, `split.py`, `vetting.py`, `vouch.py`.

| Pool (points of P, equal weight per binary-period bin) | P points |
|---|---|
| Found by B today | 48.4 |
| Strongest crossing SNR 7 or more, but B missed (held below tier 1) | **11.6** |
| Crossings in the data but never scored (mask, windows, load) | **13.8** |
| No crossing reaches 7, but an equal-weight stack of all crossings reaches 7 | 3.9 |
| same, stack must reach 9 (safer bar for many orbit tries) | 1.7 |
| Scored, too faint even stacked | 22.4 |

- Null check: at the same times without a planet, the per-crossing score has a robust spread of 1.03 (good, calibrated in the core) but a heavy tail (99.9th percentile 24): systematics, not Gaussian noise. That tail is what any stack would add up too.
- Crossings per planet in the data: 0 scored for 145 planets, 1 for 263, 2 for 201, 3 or more for 466. STANLEY's standard rule needs three.
- Realistic ceiling: if the never-scored crossings behave like the scored ones (about 68% reach SNR 7), closing that pool adds about 9 to 10 points, not 14. Everything closed: about 48 + 12 + 9.5 + 2 to 4 = **about 71 to 74**. **0.75 is at the edge of what these planets and TESS data allow, under today's reference planets.** (UNCERTAIN: chain differences between 006 and B; never-scored crossings not measured.)

## What holds the 123 detected planets below tier 1 (006 chain)
Best matched event tier: 2 for 110 planets (13 reach tier 1 in 006 but not in B). Flags on those events: near momentum dump 55, step 49, data-gap edge 34, ramp 33, repeater 32, near dump text 28, c5 16, eclipse overlap 10, dominated 8. These are the false-alarm guards; relaxing them blindly adds upside-down alarms (as DS showed).

## A different use of multiple crossings: vouching (new idea, measured ceiling)
Instead of adding weak dips up, let a second crossing of the same planet vouch for a flagged dip: a tier-2 dip is promoted when another crossing at a time a circumbinary orbit allows shows a dip too. Ceiling: of the 11.6 points held below tier 1, **5.6 points** have a second crossing scoring 4 or more (4.5 at 6 or more). Null at the true times: 0.15% of planets (pairs 7 and 4 or more without a planet). A real search tries many orbits, so the true false-alarm rate is higher: must be measured with the upside-down arm.

## Extra check: does a cross-star time veto separate dump false alarms from planets? (CONFIRMED as computed, `data/rs037/coincide.py`)
No-planet events at SNR 7+ in 4,214 bench star-sectors, against planted dips flagged near a dump. Share with at least one other bench star dipping within the window:

| Window | Dump-flagged, real arm | Dump-flagged, upside-down arm | Not dump, real | Planted dump-flagged dips |
|---|---|---|---|---|
| 0.1 day | 0.73 | 0.74 | 0.28 | 0.50 |
| 0.03 day | 0.50 | 0.52 | 0.13 | 0.26 |

So dump false alarms coincide across stars about twice as often as planted dips do. That helps, but alone it is not clean: at 0.03 day a veto would keep about 74% of planted dump dips and also free about half the dump false alarms. LIKELY stronger with more stars per sector (our bench holds only a sample of each sector's stars; the full G1 list would add neighbours) and when combined with the dump shape rule (DS) and vouching. For F4 to measure, not to adopt.

## Q2: methods in the literature (primary pages read today)
- **STANLEY** (Martin and Fabrycky 2021, [arXiv 2101.03186](https://arxiv.org/html/2101.03186v1)): N-body orbits, stack variable crossings; standard rule "three transits on the primary star"; on two transits: "finding Earth-like circumbinary planets with only two transits would be nearly impossible". Also removes timestamps that are deep in many stars at once: "35 timestamps that correspond to a deep flux point in more than five of the 270 light curves" (a cross-star coincidence veto). CONFIRMED.
- **mono-cbp** (Davies and co-workers 2026, [arXiv 2604.09435](https://arxiv.org/html/2604.09435v1)): single-event TESS search like ours; "Our vetting metrics and model comparison do have the unintended effect of filtering out some injected transit signals"; for TESS, "individual transit detections serve primarily to identify promising CBP candidates". Recovery at least 50% per known planet, above 75% for 9 of 14. CONFIRMED. Our vetting-loss finding matches theirs.
- **QATS-EB** (Windemuth and co-workers 2019, [arXiv 1909.07443](https://ar5iv.arxiv.org/html/1909.07443)): corrects binary-driven timing shifts by realigning crossings using a full binary solution (masses, flux ratio, orbit), then QATS; one injection gave S/N 20 against 14 uncorrected ("about 1.4 times"). Needs full binary solutions, which most of our stars lack. Threshold and false-alarm calibration not found in the part read (UNCERTAIN).

## Q3 and Q4: false alarms and cost
- Any orbit search must be calibrated on the upside-down arm and on no-planet data; STANLEY on our PC had 28% of noise orbits above 5 sigma (F-045). Our heavy-tail null says single systematics will dominate stacks unless vetoed first.
- Cost: STANLEY reports hundreds of CPU hours for broad searches (Astra 003). A vouching search is cheaper: it only tests orbits through an already flagged dip (one anchor), so the grid shrinks by the number of crossings times the phase grid. NOT TESTED on our PC.

## Q5: the simpler road
A looser single bar (SNR 6, or 5) plus B: P 0.63 (6) and 0.67 (5) at perfect vetting, but false alarms rise steeply (null tail); only useful with vouching.

## What this changes (plan)
1. The biggest levers toward 0.75, in order: **vetting losses (11.6, mostly dump, step, gap edge, ramp, repeater flags)**, **never-scored crossings (13.8; Astra 025 load losses and Fable F2)**, then vouching (up to 5.6 of the 11.6), then stacking (2 to 4).
2. Fable gets F4 (below) instead of "design a stacked search".
3. Ahmed should know: 0.75 is a stretch goal at the edge of the ceiling; the honest forecast after all known levers is about 0.60 to 0.70 (UNCERTAIN).

## F4 for Fable (text for the brief)
**F4: the vetting-loss pool and orbit vouching (cap 4 points).** RS-037 (`research/stage3/rs037/MULTI-CROSSING-2026-11-15.md`) shows 11.6 points of P are planets detected at SNR 7+ and held at tier 2 by guard flags (dump 55, step 49, gap edge 34, ramp 33, repeater 32 of 123), and that a second crossing scoring 4+ exists for 5.6 points. Design, and if the meter allows prototype on a bench copy: (a) a cross-star coincidence veto (STANLEY's deep-timestamp list idea) to replace the blanket dump flag; (b) orbit vouching: promote a tier-2 dip when a circumbinary orbit through it predicts another crossing that scores 4+; with a preregistered pass rule under Tree rule 1 (upside-down alarms not above B), the zero-planet identity check, and the fresh-seed confirmation. Say which flag loses the most planets for the fewest prevented false alarms.
