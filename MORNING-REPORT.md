# Morning report: overnight run, 20 October 2026

*Written by Claude (Opus 5.5) in the main Second Sun session. Started ~00:58 UTC (03:58 Kuwait). This file is updated as work continues; the latest checkpoint is always in `OVERNIGHT.md`.*

## A. Executive summary (plain English)

Ahmed, three things happened overnight:

1. **I rebuilt our planet search and tested it honestly.** It's a little better than before. It now finds the known planet TOI-1338 b in 4 of the 8 sectors where it crossed, and it catches fake planets about **6 times Earth's size** or bigger. The important finding: **the limit is mostly the data, not our code.** In the sectors we missed, the planet's dip is barely above the noise, and the spacecraft makes fake bumps just as strong. The next step is to stack a planet's crossings together, the way the professionals' tool (STANLEY) does.
2. **Your study book has its first four real chapters.** They cover two suns, light curves, wandering transits and our detector. Each one goes: intuition, meaning, technical, our code, worked example, what it proves, quiz. They're built on our own data and figures, and every fact links to its source.
3. **The book now looks like a research observatory, not a template.** It has proper reading type, an instrument-style status panel, a "mission timeline" sidebar that marks the chapters you've opened, and numbered equations. I checked it at phone and PC sizes, in dark and light mode, with zero errors.

**No new planet. Nothing was submitted anywhere.** Everything is pushed to GitHub.

## B. Scientific progress

| What | Result | Label |
|---|---|---|
| Detector v2 written (`pipeline/detect_v2.py`): matched box filter 3-15 h, 2-day detrend, eclipse mask from the known binary period, SAP gap fill, red-noise-aware SNR | self-check passes (no event in pure noise; a 700 ppm, 6 h dip found at SNR 8.9) | CONFIRMED |
| Recovery of published TOI-1338 b transits (Wang & Liu 2024 times) | v2: 4 of 8 sectors with data (S10, S65, S68, S98); v1 also 4 of 8 but a different set | CONFIRMED |
| Why the misses happen | in missed sectors the planet's SNR is 3.7-6.5, below the bar of 7 | CONFIRMED |
| False alarms (search on flipped data) | 6 fake events in 10 sectors at SNR ≥ 7, peaks up to 12.6 | CONFIRMED |
| Injection test (S98) | 6 R⊕: 5 of 7 found; 7-8 R⊕: all; 5 R⊕ and below: none | CONFIRMED |
| S98 transit timing | +1.08 h vs Wang & Liu's prediction (burn 1 got +57 min); real error bar not measured yet | UNCERTAIN |
| G1 feasibility | the earlier "2-5 R⊕" estimate was too optimistic for single sectors; ~6 R⊕ at Tmag 11.5 measured | LIKELY (one star) |

This is reproduction of a known planet, **not a discovery**. Details: `research/overnight-science/report.md`.

## C. Study bible progress

New in `book/docs/book/`:

| Chapter | Covers | Depth reached |
|---|---|---|
| 1. Two suns | binaries, S- vs P-type planets, Holman-Wiegert stability limit, Kepler's third law, the pile-up; TOI-1338 worked example | every symbol explained; powers and ratios |
| 2. Light curves | transits, depth = (Rp/R★)², ppm, TESS sectors and cadences, SAP vs PDCSAP, noise, BTJD; TOI-1338's three dip types | squares and square roots |
| 3. Wandering transits | timing shifts, duration changes, precession switching transits on/off, why NASA's pipeline misses them, the G1 idea; TOI-1338 b timeline | conceptual + one worked timeline |
| 4. Our detector | matched filter, SNR, detrending, our code function by function, three honest tests with real figures | code-level |

Also: 18 new sourced facts (F-001 to F-018) in the claims register, 10 new glossary terms, 3 figures made from real TESS data.

**Read first:** Chapter 1, then Chapter 4's "In plain words" box. Chapter 1 gives you the picture; Chapter 4 tells you where we honestly stand.

## D. Website improvements

- **Type:** Source Serif 4 for reading, IBM Plex Sans for headings, IBM Plex Mono for labels and data. All self-hosted (free OFL licences included), so they work offline on your iPhone.
- **Sidebar:** a "mission timeline". One track line, a station per chapter, amber for where you are, filled for chapters you've opened on that device.
- **Home:** a mission status panel (phase, campaign, detector, test result, candidates, next milestone) and a numbered chapter index.
- **Equations** get their own numbered block ("Eq. 1.1 · Holman and Wiegert"). **Figures** are framed with numbered captions.
- Still one amber accent, no game elements, transitions off under reduced motion.
- Files: `book/docs/assets/observatory.css` (new), `book/docs/assets/book.js` (read marks), `book/docs/index.md`, `book/mkdocs.yml`, `book/docs/assets/fonts/`.
- **Verified in a browser:** 13 pages at 390 px with 0 horizontal overflow; dark and light; 1280 px desktop; 0 console errors; all fonts load; `mkdocs build --strict` passes.
- **Preview locally:** `cd D:\second-sun\book`, run `..\.venv-docs\Scripts\mkdocs.exe build`, then `node tools\serve.mjs --dir=site --port=8471` and open http://localhost:8471.
- **Not done:** the site is **not deployed** to GitHub Pages yet (needs you to switch Pages on in the repo settings, see I). The iPhone offline test is still untested.

## E. Code and testing

| File | What |
|---|---|
| `pipeline/detect_v2.py` | detector v2 + self-check |
| `pipeline/accept_v2.py` → `accept_v2_results.json`, `accept_v2_log.txt` | recovery, flipped-data false alarms, injection |
| `pipeline/diag_v2.py` → `diag_v2_results.json` | SNR at each published transit vs strongest fake bump |
| `pipeline/book_figures.py` | the three chapter 4 figures |
| `book/` | the book (moved in from the burn-3 prototype) |
| `book/tools/serve.mjs` | local Pages-like server (now serves fonts) |

Commands run: `python detect_v2.py` (pass), `python accept_v2.py` (ran), `python diag_v2.py` (ran), `mkdocs build --strict` (pass, ~0.6-2.5 s). Bugs found and fixed: wrong self-check depth (my maths), a header misalignment, sidebar dots on the wrong level, a status-panel indent. Friction: a bad import guard (reverted before use), a backslash path mangled by sed (fixed), a hung heredoc earlier in the night (stopped).

## F. Evidence and confidence

- CONFIRMED: everything in the B table marked so (ran, results saved).
- LIKELY: "most known two-sun planets are Saturn-sized or larger" (from memory of the sample, not yet re-checked).
- UNCERTAIN: the meaning of the +1 h timing offset; the two extra events in S27 and S98 (not inspected).
- NOT TESTED: iPhone offline; the Holman-Wiegert calculator (not coded yet).
- BLOCKED: GitHub Pages deploy (needs your repo setting).

## G. Usage and session status

- Weekly limit: **2%** at the start (00:51 UTC), **4%** at 01:16 UTC. Ceiling you set: 30%; I stop new work at 25%.
- 5-hour window: 22% at 01:16 UTC, resets 05:50 UTC (08:50 Kuwait).
- One session (this one), no helpers. A one-time timer, "Second Sun: resume overnight run", fires at 08:55 Kuwait to continue from `OVERNIGHT.md`. **It may pause on permission prompts**, because the app wouldn't save Auto mode for a task created from a phone message.

## H. Next-session task queue (ranked)

1. **Systematics veto**: drop events near data gaps, momentum dumps and flagged cadences, and events that also appear in flipped data. Re-measure false alarms. *Why:* without it, 550 stars would flood us with fakes.
2. **STANLEY trial on TOI-1338** (all sectors together). *Why:* stacking crossings is the real test of whether G1 can reach small planets.
3. **Timing error bar** for the S98 transit (red-noise method). *Why:* decides whether the +1 h offset means anything.
4. **Book chapter 5: vetting** (how a dip becomes a candidate), plus the Holman-Wiegert calculator in `pipeline/`.
5. **Deploy the book** once you switch on Pages, then run the iPhone offline checklist.

## I. What you should do next

1. **Read** the book's Chapter 1 (20 min), then the "In plain words" box of Chapter 4.
2. **One setting, 2 minutes, at your PC:** in the Claude app, open **Scheduled → "Second Sun: resume overnight run" → set it to Auto**, so timed runs don't freeze.
3. **Decision waiting for you:** NASA's candidate site now requires **publishing first, then uploading** (we confirmed it at the source). That changes our path from "CTOI first" to "write-up first". Nothing is needed until we have a candidate, but think about it.
4. **Optional:** to put the book online (still hidden from Google), switch on GitHub Pages for the repo. I'll walk you through it.
