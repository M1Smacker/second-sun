# The real redesign (F4): build plan, written 27 October 2026. Plan only, nothing built.

Status: waiting for Ahmed's go. His picks so far: Atkinson Hyperlegible Next (A) for text and headings; the rest left to me (listed below). The approved picture is the Design canvas, version 12: https://claude.ai/artifact/D5a9xdG1NFnDVHrCJUXyTQ. Measurements behind it: `research/redesign-type-tests/REPORT.md`.

## What the book is built from today (VERIFIED by reading the repo)
Material for MkDocs with `overrides/main.html`; three CSS files (`extra.css` 14 KB, `observatory.css` 11 KB, `shape.css` 16 KB); `book.js` and `demos.js` (44 KB, the Eyes interface) plus the Eyes logic files; fonts declared in `observatory.css` (Inter normal and italic, IBM Plex Mono 400 and 500) with files in `docs/assets/fonts`; text lines capped at `66ch` in `extra.css`; offline reading through a service worker built from `sw-template.js`. Tests: `test_contrast.py`, `test_shape.py`, `test_mission.py`, `check_site.py`, and seven `test_eyes*.mjs` files; the publish gate is `research/burn-3-book/tools/publish_book.ps1 -Test`.

## Decisions (all reversible, all on the plan page)
- Reading face A: Atkinson Hyperlegible Next for text and headings; interface IBM Plex Sans; code IBM Plex Mono; labels and plot notes IBM Plex Sans with tabular figures.
- Symbols: `ss-symbols.woff2` (1.9 KB) and `ss-cross.woff2` (0.9 KB), already cut and verified, with their licence file.
- Scale: body 17 px on a phone and 18 px from 640 px up; titles 30 and 38; reading column 540 px (about 70 characters in Atkinson, measured).
- PC chapter: three zones from 1100 px (rail 232, text 540, margin 260), page never wider than 1400 px; the margin opens only the note for what is on screen; under 1100 px and at zoom the notes sit inline.
- Eyes: curve height 40% of the window (220 to 400 px, up to 1000 px wide), four answers in a row, feedback as body text, Next pinned after answering, natural scrolling.

## Steps, files, proof
1. **Type, symbols, offline.** Files: `observatory.css` (font faces, variables), `extra.css` (scale, column), `assets/fonts/*`, `sw-template.js` precache list. New test `tools/test_fonts.py`: every non-ASCII character used in `docs/` must be drawn by a font the book serves or by the symbol files (fontTools, read from the served files). This makes today's finding permanent. Proof: that test, `test_contrast.py`, the existing browser tests with the network off, and a local look at phone and PC widths. Calibrated 0.8 to 1.8 points (original gut 2 to 3).
2. **Chapter page and notes on PC.** Files: `overrides/main.html` (rail with the track and the 15 chapters as two labelled lists, from `data/path.yml`), `shape.css`, `book.js` (move evidence notes and glossary meanings into the margin, open the one in view, inline fallback). Notes stay in document order so a keyboard and a screen reader read them where they belong. Proof: `test_shape.py`, `check_site.py`, and a new browser layout test at 390, 683, 1100, 1366 and 1500 px (no sideways scroll, column width 540, 60 to 72 characters a line, margin shown only from 1100 px). Calibrated 1 to 2.5 points (gut 2 to 4).
3. **Eyes on PC and zoom.** Files: `demos.js` (layout only), `shape.css`. The scoring, saving and cloud logic stay untouched; all `test_eyes*.mjs` must pass unchanged. Proof: those tests plus browser checks at 1366 by 650, 683 wide (200% zoom) and 390, that the pinned Next never covers feedback text, and that answers stay reachable. Calibrated 0.5 to 1.5 points (gut 1 to 2).
4. **Quieter look, full gate, publish.** Four callout styles only; colours unchanged; the Cygnus home map untouched. Run the publish gate with `-Test`, write the same-day field note, publish. Ahmed reloads once on his iPhone. Calibrated 0.7 to 2 points (gut 1.5 to 3).

Total calibrated 3 to 8 points (the first estimate on the canvas was 6.5 to 12; my gut has run about 2.5 times high on design work, see `research/usage-ledger.md`). Uncalibrated for a large CSS change that needs browser tests, so I would quote 3 to 8 and report the real number after each step.

## Requirement added 27 Oct (Ahmed, morning): results must be clear, not crowded. "Smarter lines, not fewer lines."
Ahmed said the book is hard to read for his stats, that it feels messy, and that Claude should present results in the clearest way. Cause found by reading the code (VERIFIED): `eyes-core.js` `hardLine()` line 184 appends the same sentences `hardLines()` already printed (`demos.js` lines 418 and 419 show both after a hard test), so on the finish screen and in My results the same facts appear two or three times (clear fake planets, near-limit bands, hard noise), each as a full sentence, with the pass line, the 95% range and the verdict mixed in the same list. The pass line block repeats the standard numbers the same way.

Rules for the F4 Eyes results (they are part of step 3, not extra scope):
1. **One fact, one place.** No number appears twice on a screen. A test enforces it: print the results page text and fail if two lines state the same count.
2. **Verdict first.** The top shows one plain sentence, then at most four numbers: dips you caught, quiet curves you called a dip, glitches you took for a dip, and the pass line status. Each number has a label, a bar with the pass line marked on it, and the count behind it ("93%, 102 of 110").
3. **Trend as a picture.** One small chart of accuracy per round, so "am I getting better" needs no sentence.
4. **Detail on request.** The band-by-band lines (near-limit strengths, hard noise, odd things by type) sit behind one "Details" control. The 95% range is shown as the shaded part of the bar, with one line explaining it once.
5. **Words say what to do.** "Weakest spot: jumps called a dip (8 of 50)" with the one-line habit to fix it, instead of a list of counts.
Proof: the no-repeat test above, a screenshot read at 390 px, and Ahmed's answer to "can you find your pass-line status in three seconds". Cost is inside step 3 (0.5 to 1.5 points) plus about 0.2 for the repeat test; not a new step.

## Risks and how each is covered
- Material's own styles override mine: build on the existing override files and test at every width listed.
- The service worker keeps old fonts: bump the cache version through the existing template and test with the network off.
- A flash of fallback text while fonts load: `font-display: swap` plus size-matched fallback metrics.
- Noto Sans Math has one weight: a bold heading with a sigma shows it regular; accepted and stated in the report.
- Eyes behaviour must not change: logic files untouched, all seven Eyes tests run unchanged.

## Pacing and rollback
Day 1 steps 1 and 2 (publish once they pass); day 2 steps 3 and 4. Each step ends with tests, a commit and a ledger row. Rollback is a git revert plus republishing the previous commit through the same gate.

## What I need before starting
Ahmed says "start F4". Nothing else is blocking: the typeface, the label face, the margin, the pinned Next and the symbol files are settled.

## Status, 27 Oct evening (Ahmed said "start F4"; weekly cap raised to 20%)
- **Step 1 done and live** (gh-pages 3ea879f). Atkinson Hyperlegible Next for text and headings, Plex Sans for the interface and labels (400 and 600 files; a 500 request renders at 600), Plex Mono for code, the two symbol files with their unicode-range. Inter removed. `tools/test_fonts.py` (31 non-ASCII characters in the sources and the built pages, all drawn; it reads `tools/font_coverage.json`, made by `tools/make_font_coverage.py` because the gate's Python has no brotli) is in the gate as step 3c. The service worker needed no list change: `hooks.py` precaches every built file.
- **Step 2 done and live.** Rail (232), reading column (540), margin (260) from 1120 px (not the 1100 drawn: the three zones plus gaps need 1086 px), strip hidden beside the rail, notes inline below that. `site_check.mjs chapter` (14 checks at 7 widths on 2 chapters, plus a scroll check at 1366 by 650) is in the gate. It was shown to fail by widening the column in a scratch copy. Chapter-number buttons are a 4 column grid (5 columns gave 40 px wide targets and the existing layout test refused them).
- **Step 3 partly done.** The hard line no longer prints the clear-planet and hard-noise sentences a second time (`hardLines(h, true)`), with a test. NOT built: the Eyes PC layout, and the verdict-first results screen, which waits for Ahmed's decisions 1 to 3 on the Results board of the design Artifact (v13).
- **Step 4 not done:** four callout styles and the look pass. The gate and a field note item for steps 1 and 2 are done.
- **Not verified:** nothing has been seen on Ahmed's iPhone or PC; the layout was measured by script and looked at in one window. Actual cost so far about 2.0 weekly points (estimate for what was done 3 to 6.5).
- Process: push main before running the gate, because it builds the pushed main.
