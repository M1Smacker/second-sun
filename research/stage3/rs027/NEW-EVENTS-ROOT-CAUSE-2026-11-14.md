# RS-027: what are the new real-light events that the narrower mask lets through? (Claude, 14 Nov 2026, 19:04 Kuwait, Opus 5.5 medium)

**Why (root cause first, unasked):** Codex 011 (both mask variants re-scored with OAE) failed the preregistered rule: P 49.61% (V1) and 49.66% (V2) against 50%, and upside-down background +3 and +6. Its new real-light events (45 V1, 38 V2) sat "far from eclipses" by the catalogue geometry, origin UNCERTAIN. The FIX 94 decision rule (written before 011) said: events far from eclipses, research before any fix. Cap written first: 1 weekly point. Data: Codex's private rows `D:\second-sun-astra\data\astra\011\new-events.csv` (star ids now allowed, Ahmed 14 Nov).

## Findings
- **About half the new real events are deep eclipses, not planets or noise (CONFIRMED on the rows):** 18 of 38 (V2) and 21 of 45 (V1) are 8,000 ppm deep or more or SNR 50 or more, on 10 stars; depths up to 175,000 ppm (17%), SNR up to 1,410. No planet in our bench is that deep.
- **Their catalogue geometry is wrong, so the proxy could not see them as eclipses (CONFIRMED on one star, LIKELY for the rest):** TIC 140760434 has 7 new events of identical shape (10,000 ppm, 10 h, SNR 85 to 115) spaced exactly 1, 4, 2, 2, 24 and 1 cycles of **31.81 d** over 1,082 days (spacing residuals under 0.01 d). Its catalogue period is 30.98 d. A 0.84 d period error grows by a whole eclipse width every few cycles; that is exactly what the timing padding was covering. Another star (TIC 394728064) shows 73,000 to 89,000 ppm events at catalogue phase 0.48 to 0.50 while its catalogue secondary sits elsewhere: a misplaced secondary.
- **The rest (about 20 per variant) are shallower (about 1,000 to 6,000 ppm) and UNCERTAIN:** one star (TIC 306263608) has 4 events of 1,000 to 1,400 ppm at a steady catalogue phase (0.73 to 0.82), which looks like a shallow eclipse; the others are one or two per star.
- **Upside-down side (V2, 6 events):** two sit at the same moment in sector 4 (BTJD 1413.12 and 1413.19) on two different stars: a spacecraft-wide feature, not the mask (LIKELY; the common-moment flag should have caught it, worth a check). Three others sit at catalogue phase 0.04 to 0.12, near primary eclipses (LIKELY detrending overshoot beside an unmasked eclipse, NOT TESTED).

## What it means (plan change)
- Codex 011's verdict stands: neither V1 nor V2 is adoptable. **Root cause: the timing padding was doing its job: it hid eclipses whose catalogue period or secondary position is wrong.** Narrowing it without knowing where the eclipses really are lets those eclipses through as "real events" and adds a few upside-down artefacts beside them.
- **So the full FIX 94 design is needed (case 2 of the decision rule in RS-026, not case 3):** measure our own TESS eclipse times, and fit the PERIOD as well as the epoch (step 2 must not keep the catalogue period: TIC 140760434 is off by 0.84 d), primary and secondary separately; centre windows on the fit. Test: those 18 to 21 deep events must disappear, and the planet gain must survive.
- Add a cheap guard to the design: any new real event deeper than the star's own catalogue eclipse depth or deeper than 30,000 ppm is an eclipse candidate, never a planet (NOT TESTED as a rule).
- Feeds Fable's task 1 on Monday.


## Follow-up: price of a "too deep to be a planet" guard (Claude, 14 Nov 2026, 19:22)
Counts from Codex 011's background and new-event rows (tier 1, untouched design light, g2 plus g3), and the 006 planet journals:
| Depth over | V0+OAE background real / upside-down (176 / 83) | V2 new real / upside-down (38 / 6) |
|---|---|---|
| 10,000 ppm | 75 / 35 | 17 / 1 |
| 20,000 ppm | 56 / 19 | 9 / 0 |
| 30,000 ppm | 51 / 16 | 7 / 0 |
| 50,000 ppm | 39 / 7 | 6 / 0 |
- **CONFIRMED:** 51 of the 176 tier-1 real background events and 16 of the 83 upside-down ones are deeper than 30,000 ppm (3%). The planet bench cannot price the guard: its deepest planted planet is 5,990 ppm, so any guard above that costs zero planets there BY CONSTRUCTION (a blind spot, not evidence of safety).
- **The guard is not a substitute for FIX 94:** at 30,000 ppm it removes only 7 of the 38 new V2 real events; the 10,000 ppm eclipse of TIC 140760434 passes it.
- **Design idea (NOT TESTED, filed as FIX 96):** a per-star physical ceiling instead of a fixed number: the deepest transit a planet of 1.5 Jupiter radii could make across the primary (TIC radius), diluted by the companion's light; events deeper than that are labelled eclipse-like, both arms the same. A fixed 3% would wrongly cut a Jupiter crossing a small M dwarf (about 4% before dilution, UNCERTAIN, rough arithmetic); the known transiting circumbinary planets are far shallower (TOI-1338 b about 2,000 to 3,000 ppm, T109).

## FIX 95 pricing: a data-driven "sector-wide moment" flag (Claude, 14 Nov 2026, 19:39; `rs027_moments.py`, `moments.json`, rule written before the run)
Moment = events on at least K other stars of the same sector, ANY camera, within 0.1 d (pool: all SNR 7+ dev events, g2 plus g3).
| K | Tier-1 background at a moment, real / upside-down (of 176 / 83) | Planted crossings at a moment (of 5,308) |
|---|---|---|
| 3 | 22 / 15 | 1,291 (24%) |
| 5 | 10 / 7 | 787 (15%) |
| 8 | 6 / 4 | 459 (9%) |
- **CONFIRMED: not viable.** Ordinary events on hundreds of stars make "moments" everywhere, so this flag would put a quarter of planet crossings at risk to remove 15 upside-down events. (The planet window is wider, half the duration plus 0.1 d, so its share is an upper bound; even a fraction of it is too costly.)
- **Plan change:** FIX 95's fix must be a short list of KNOWN spacecraft events with exact times from the TESS data release notes (like the sector 4 pointing shift at TJD 1413.26), not a statistical moment finder. Building that list is a research task (one entry per sector from the notes), filed under FIX 95.

