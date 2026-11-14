# RS-031: what TESS momentum dumps do to the light, and how others guard against them (started 14 Nov 2026, 10:29 pm Kuwait, Opus 5.5 medium)

**Why:** Codex 013 found the dump-shape rule (DS) frees 30 real vs 4 upside-down untouched events, 23 of 30 before a dump: likely dump artefacts our upside-down meter cannot see. Fable designs a safe version on Monday; this stint gives a physics-based window written BEFORE Codex 014's dump map reports, so no window is tuned on our own events.

**Cap, written before the start:** 2 weekly points, about 25 tool calls. No helpers.

## Questions
| # | Question | Decision it feeds |
|---|---|---|
| Q1 | What happens to the pointing and the photometry before, during and after a TESS momentum dump (duration, size, which quality bits mark it), by era? | the window of a dump guard |
| Q2 | Is the dump systematic one-sided (dips more than bumps)? Why? | whether the upside-down control can ever see it |
| Q3 | How do other TESS searches (single transits, circumbinary planets, vetting tools) treat dumps? | whether a distance rule, a shape rule or a model is the field's practice |
| Q4 | Our own rule C7 (flag 0.5 d before to 0.25 d after) came from one Kepler-16 dry-run event: does any source support those numbers? | keep, narrow or widen C7 |

## Findings
Pages read 14 Nov 2026 night as arXiv HTML (saved in data/rs031_arxiv_pages_2026-11-14/, 1.3 MB, logged); sentences pulled by script, quoted exactly.

### Q1. What a dump does, and for how long. CONFIRMED (three independent papers plus the TOI catalogue)
- **Before the dump, for about a day:** Vanderburg et al. 2019 (HR 858, [arXiv 1905.05193](https://arxiv.org/abs/1905.05193)): systematics on long "(~day) timescales (which come from steady increases in the pointing scatter ahead of reaction wheel momentum dump events)"; the light curve shows "slow trends ... with jumps each time the spacecraft resets the reaction wheel speeds". They model it with spline breaks at each dump.
- **After the dump, hours to half a day:** Eisner et al. 2019 (Planet Hunters TESS I, [arXiv 1909.09094](https://arxiv.org/abs/1909.09094)): "the satellite pointing remains affected for several hours after each dump, and can result in spurious flux variations due to aperture losses or inter-/intra-pixel sensitivity variations"; dumps "occur every 2 to 2.5 days and typically last around half an hour" (sectors of their study). Wong et al. 2020 (WASP-19b, [arXiv 1912.06773](https://arxiv.org/abs/1912.06773)): "clear short-term flux ramps and/or increased scatter within the ~0.5 days of photometry immediately following a momentum dump".
- **The dump itself:** Guerrero et al. 2021 (TOI catalogue, [arXiv 2103.12538](https://arxiv.org/abs/2103.12538)): "Momentum dumps briefly affect the spacecraft pointing for 1-2 frames"; 3 to 4 dumps per orbit early in year 1, 1 to 2 per orbit in year 2.
### Q2. One-sided? LIKELY dips, mostly before the dump
Growing pointing scatter smears the star's light outside its aperture ("aperture losses", Eisner), which lowers the flux; the dump resets the pointing and the flux jumps back (Vanderburg's "jumps"). So the window just before a dump ends in a dip-like drop that the upside-down copy never shows as a bump. Intra-pixel effects can go either way (Eisner), so the after-dump side is less one-sided. This matches Codex 013: 23 of the 30 real events DS freed sit before the dump, against 4 upside-down events in all. The mechanism is from the papers (CONFIRMED); that it explains our 30 is LIKELY (not shown event by event).
### Q3. Field practice. CONFIRMED
"Spacecraft momentum dumps may create signals that mimic transit-like events in depth and duration" (Guerrero 2021); the TOI process flags TCEs "occurring at the same time as a spacecraft momentum dump"; early SPOC and QLP "were not able to distinguish transit-like events due to momentum dumps from actual transits". Eisner checks every transit against dump times, centroids and background. Vanderburg excludes the 2% of points with the widest PSF. So the field uses distance to dumps plus a jitter or PSF-width measure, not the dip's own shape; no source uses a shape rule like DS.
### Q4. Our rule C7 (hold events from 0.5 d before to 0.25 d after a dump). PARTLY SUPPORTED
Before: the day-scale growth of scatter supports holding before the dump (0.5 d is inside the contaminated span; UNCERTAIN whether it should be longer). After: Wong's ~0.5 d ramps and Eisner's "several hours" suggest 0.25 d may be short. Not changed (the filter is frozen; any change is a new rule priced on the bench).

## What it changes (for Fable's round, Mon 16 Nov)
1. **DS's blind spot has a known physical cause:** pre-dump pointing scatter makes one-sided dips. A safe DS must keep the dump hold, whatever the shape, for boxes before or containing a dump; shape relief, if any, belongs only after the dump, where the effect is less one-sided. This is a physics-based candidate written now, before Codex 014's dump map reports; Claude has seen Codex 013's 23-of-30 count, so it is not blind to our data (disclosed).
2. **A better meter than shape:** the field's tool is pointing jitter itself (PSF width, centroid scatter, or the spacecraft quaternions). A jitter-based dump test is a candidate build for Petrova 1.2 or Census, not for G1 (filed idea, node 1.6).
3. **C7 after-dump side (0.25 d)** may be short against 0.5 d ramps: filed as a question for the next version, NOT TESTED.

## Bench test of the physics-based variant DSp (rule written 10:31 pm, BEFORE the run and before Codex 014 part 1 reports)
- **B** = adopted set (repeater b + FIX 91 + OAE + K). **B+DS** = Codex 013's B+K+DS (identity: P 0.4998, background 204 / 83). **B+DSp** = DS shape relief only for an event whose whole box lies AFTER every dump in its flag window (box start at or after the dump time); boxes before or containing a dump keep the dump hold whatever their shape. Dump times: QUALITY bit 32 from design stars' SPOC or TESS-SPOC files, one per sector (as rs025_dumps.py).
- **Pass rule:** Tree rule 1 against B (P rises, upside-down background not higher, paired control passes in every bin). Reported beside it, not part of the rule: the real background change and the real : upside-down ratio of the untouched events DSp frees (DS: 30 : 4).
- Script `research/stage3/rs031/rs031_dsp_bench.py` (RS-024 harness, own output files).
