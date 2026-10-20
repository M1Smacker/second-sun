# Morning report: overnight run, 20 October 2026

*Written by Claude (Opus 5.5) in the main Second Sun session. Started ~00:58 UTC (03:58 Kuwait). This file is updated as work continues; the latest checkpoint is always in `OVERNIGHT.md`.*

## A. Executive summary (plain English)

Ahmed, three things happened overnight:

1. **I rebuilt our planet search and tested it honestly.** It's a little better than before. It now finds the known planet TOI-1338 b in 4 of the 8 sectors where it crossed, and it catches fake planets about **6 times Earth's size** or bigger. The important finding: **the limit is mostly the data, not our code.** In the sectors we missed, the planet's dip is barely above the noise, and the spacecraft makes fake bumps just as strong. The next step is to stack a planet's crossings together, the way the professionals' tool (STANLEY) does.
2. **Your study book has its first four real chapters.** They cover two suns, light curves, wandering transits and our detector. Each one goes: intuition, meaning, technical, our code, worked example, what it proves, quiz. They're built on our own data and figures, and every fact links to its source.
3. **The book now looks like a research observatory, not a template.** It has proper reading type, an instrument-style status panel, a "mission timeline" sidebar that marks the chapters you've opened, and numbered equations. I checked it at phone and PC sizes, in dark and light mode, with zero errors.

**After that, I kept going** (budget allowed it):
4. **Automatic clean-up of fake dips doesn't work on its own.** Rejecting dips near data gaps or thruster firings removed fakes but also threw out half the real planet crossings, so those became warning flags for a human instead.
5. **The 16 December crossing really is about an hour late:** 56 ± 5 minutes after the 2024 prediction, which is 2.4 times the combined error. That's a mild, interesting tension, not proof of anything.
6. **Chapter 5 (vetting)** is written, a **stability calculator** is in the code, and the **learning track** now points each level to the chapter that teaches it.
7. **STANLEY** (the professionals' stacked circumbinary search) now runs on your PC after two fixes. Its first stage was still working at the time of writing (see B).
8. **The G1 list is frozen and traceable:** 552 rows = **549 different stars**, with the source files' fingerprints recorded. Every one has at least one TESS light curve; half have NASA's best (2-minute) data. All their ready-made light curves together are only **~6.3 GB**.
9. **QLP data, half-fixed:** half the G1 stars only have MIT's QLP light curves. At first our search failed on them: scattered light made fake dips up to 44 times the noise, and QLP's own cleaning ate most of a long dip. I found the cause: QLP keeps stretches of time that NASA's SPOC pipeline throws away. Keeping only SPOC's good stretches, the QLP data shows **just one event: the planet**, at the same time as in SPOC data. Then I tested the real G1 case, a star with **no** SPOC file of its own: borrowing the good stretches from 4 neighbouring stars on the same camera, the planet still comes out clearly (10.9 times the noise).
10. **First dry run on a real G1 star (Kepler-16, 17 sectors): nothing survives.** The pipeline flagged one dip; I vetted it like a real candidate, and it was the classic fake: the telescope wobbling just before a thruster firing. That's the very impostor our vetting rules were written for. It slipped past the code because the code didn't match the written rule; fixed. With all sectors folded together, every remaining event carries a warning flag.
11. **The pipeline can now handle a binary nobody hand-tuned:** an automatic eclipse finder locates both eclipses from the catalogue period alone, and on TOI-1338 leaves only the planet.
12. **Realistic fake planets now work** (morning, after Compass). STANLEY's fake-planet maker had a bug that threw away every crossing; found and worked around. With 33 crossings that move and change length like real ones: our cleaning keeps 90-100% of each dip, we find 6-Earth-size planets 8 times in 10 and 8-Earth-size every time, 4-Earth-size never, and about 1 crossing in 11 is lost inside the binary's eclipses. Book Chapter 4 has it as "a sixth test".

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
| Systematics veto (gap/dump/flipped) | strict version kept only 2 of 4 real crossings; loosened once: gap/dump = flags, flipped-match = reject; 4/4 kept, 4 of 6 fakes flagged | CONFIRMED |
| S98 timing with red-noise error | +56 ± 5 min vs prediction ± 23 min → 2.4σ; +34 min if the shape floats | CONFIRMED (numbers) / UNCERTAIN (meaning) |
| Stability calculator (`pipeline/stability.py`) | TOI-1338: critical period 71 d, planet at 1.34× (matches the literature) | CONFIRMED |
| G1 target list (`targets/g1_targets.csv`) | 552 rows = 549 stars; provenance + checksums; reproduces wave 3 | CONFIRMED |
| G1 data coverage (`targets/g1_coverage.csv`) | QLP 549/549 (median 9 sectors), SPOC 2-min 275, TESS-SPOC 312; ~6.3 GB total | CONFIRMED |
| Detector on QLP data | raw flux: fakes up to SNR 38.7; QLP-cleaned flux: ~70% of a 6 h dip lost; **fix: sys_rm_flux + SPOC good-time windows → only the planet (SNR 10.1), fakes max 9.7** | CONFIRMED (one sector); borrowing windows for QLP-only stars NOT TESTED |
| QLP for stars without SPOC (windows borrowed from 4 neighbours, intersected, starts trimmed) | planet SNR 10.9; 1 edge event; fakes max 8.2 | CONFIRMED (one star, one sector) |
| Automatic eclipse mask (`eclipse_mask_auto`) | both TOI-1338 eclipses found from the period alone; 96% agreement with hand mask; only the planet remains (SNR 8.5) | CONFIRMED (one star) |
| G1 dry run: Kepler-16, 17 SPOC sectors | 1 event (per-sector fold) = pre-dump pointing jitter, QLP flat: impostor (C7/C8). Global fold: 4.9% masked, 3 events all flagged, 0 unflagged, 4 fakes | CONFIRMED |
| Rivals: Spalding & Orosz 2024 | TESS + Kepler eclipse-timing modelling of Kepler-16/34/1647 (abstracts) | LIKELY |
| STANLEY stage 1 on TOI-1338 | runs after 2 fixes (setuptools for Py3.12; downloads forced to D:); 40 sectors downloaded (78 MB); slow eclipse fitting | NOT TESTED (result pending) |

This is reproduction of a known planet, **not a discovery**. Details: `research/overnight-science/report.md`.

## C. Study bible progress

New in `book/docs/book/`:

| Chapter | Covers | Depth reached |
|---|---|---|
| 1. Two suns | binaries, S- vs P-type planets, Holman-Wiegert stability limit, Kepler's third law, the pile-up; TOI-1338 worked example | every symbol explained; powers and ratios |
| 2. Light curves | transits, depth = (Rp/R★)², ppm, TESS sectors and cadences, SAP vs PDCSAP, noise, BTJD; TOI-1338's three dip types | squares and square roots |
| 3. Wandering transits | timing shifts, duration changes, precession switching transits on/off, why NASA's pipeline misses them, the G1 idea; TOI-1338 b timeline | conceptual + one worked timeline |
| 4. Our detector | matched filter, SNR, detrending, our code function by function, four honest tests with real figures | code-level |
| 5. Vetting | every impostor and its test, NASA's bar vs ours (C1-C11), the circumbinary smoking gun, ExoFOP publish-first | rules + one worked example |

Also: 23 new sourced facts (F-001 to F-023) in the claims register, 10 new glossary terms, 3 figures made from real TESS data.

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

- Weekly limit: **2%** at the start (00:51 UTC), **10%** at 02:40 UTC. Ceiling you set: 30%; I stop new work at 25%. Well inside.
- 5-hour window: 68% at 02:40 UTC; resets 05:50 UTC (08:50 Kuwait).
- One session (this one), no helpers. Model: Opus 5.5 (this session; its effort level is the session's own setting, not changed).
- At 02:40 UTC I stopped active polling to save window while STANLEY's search runs in the background; it wakes this session when it finishes. Backup: the timer "Second Sun: resume overnight run" at 08:55 Kuwait, which **may pause on permission prompts** unless you set it to Auto (see I).
- These figures come from the app's usage meter, read during the night.

## H. Next-session task queue (ranked)

*Updated after Compass (2026-10-20 morning); items 1, 3 and 4 below are done, 2 has run (uncalibrated).* Current order: (a) contextual quality flags + eclipse-phase check (C5) + odd-even on the binary; (b) pixel tool for survivors; then scale the injection test to ~200 planets.

0. **Automate the QLP recipe** for all QLP-only G1 stars (find SPOC neighbours on the same sector/camera/CCD automatically), then re-run injection on QLP. *Why:* half of G1 depends on it.
1. **Systematics veto**: drop events near data gaps, momentum dumps and flagged cadences, and events that also appear in flipped data. Re-measure false alarms. *Why:* without it, 550 stars would flood us with fakes.
2. **STANLEY trial on TOI-1338** (all sectors together). *Why:* stacking crossings is the real test of whether G1 can reach small planets.
3. **Timing error bar** for the S98 transit (red-noise method). *Why:* decides whether the +1 h offset means anything.
4. **Book chapter 5: vetting** (how a dip becomes a candidate), plus the Holman-Wiegert calculator in `pipeline/`.
5. **Deploy the book** once you switch on Pages, then run the iPhone offline checklist.

## I. What you should do next

1. **Read** the book's Chapter 1 (20 min), then the "In plain words" box of Chapter 4.
2. **One setting, 2 minutes, at your PC:** in the Claude app, open **Scheduled → "Second Sun: resume overnight run" → set it to Auto**, so timed runs don't freeze.
3. **Decision waiting for you:** NASA's candidate site now requires **publishing first, then uploading** (we confirmed it at the source). That changes our path from "CTOI first" to "write-up first". Nothing is needed until we have a candidate, but think about it.
4. The book is online (hidden from Google): https://m1smacker.github.io/second-sun/
