# RS-028: known spacecraft events list for FIX 95 (Claude, 14 Nov 2026, 19:43 Kuwait, Opus 5.5 high)

**Question (decision it feeds):** can a short list of known spacecraft events (pointing shifts, lost fine pointing, tests, heater recoveries) remove false alarms like the sector 4 ones cheaply, where a data-driven moment flag could not (RS-027 follow-up: it would risk 1,291 of 5,308 planted crossings)? Cap 2 weekly points, written first.

**Source:** the HEASARC TESS sector summary pages 1 to 105 (https://heasarc.gsfc.nasa.gov/docs/tess/sectorN_summary.html), downloaded 14 Nov 2026 into `data/heasarc_sector_notes_2026-11-14/` (105 pages, 2.3 MB). The "Sector Notes" table of each page was read; 19 intervals with TESS times (TJD = BTJD) went into `known_events.csv` with the sentence each came from. Sector 22's watchdog resets (two missing cadences each) and pure data gaps were left out: gaps are already handled by the gap-edge flag. CONFIRMED that the times are the pages' own; UNCERTAIN whether the pages list every event (later sectors' notes are shorter; the full data release notes may hold more).

## Findings (`rs028_known.py`, `known.json`; event box overlapping the interval plus or minus 0.1 d)
| What | Total | Touching a known event |
|---|---|---|
| All SNR 7+ dev events, real | 13,290 | 745 (mostly heater recoveries after resets: 558) |
| All SNR 7+ dev events, upside-down | 7,810 | 552 (thermal 470) |
| Tier-1 background (Codex 011 V0+OAE), real | 176 | 2 |
| Tier-1 background, upside-down | 83 | 4 |
| Planted crossings of the 1,098 planets | 5,308 | 33 (0.6%) |
- **CONFIRMED:** the existing flags already hold almost all of these events (1,297 touch a known event, only 6 reach tier 1). A known-events flag would remove 2 real and 4 upside-down tier-1 background events for at most 33 crossings (0.6%; the planet-level cost is smaller or equal, NOT TESTED).
- **Verdict:** worth adding at the next fix round as a switch, priced on the planet bench and T156 with the usual rule (no more upside-down alarms, P not down). Small gain, low risk. The list stays a hashed table that a run reads, never edited after a freeze.
- **Plan change:** FIX 95 fix = this list as a flag treated like a momentum dump, both arms the same; filed for the fix round and noted for Fable's task 2.
