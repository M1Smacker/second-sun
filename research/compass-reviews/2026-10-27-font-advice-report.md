# Compass review: font advice report (27 Oct 2026)

**Verdict: APPROVE WITH ADDENDUM.** Review only: nothing in the book was changed.

## What was reviewed
Another AI's answer to `research/font-advice-prompt-2026-10-26.md` (its links carry chatgpt.com tags, so probably ChatGPT; LIKELY). Its advice:
- First choice: Literata for reading and titles, IBM Plex Sans for interface and tables, Plex Mono only for plot and instrument labels.
- Control: Atkinson Hyperlegible Next with Plex Mono.
- Third: the IBM Plex family (Serif, Sans, Mono).
- Softer text colour, a "Reading font: serif or sans" switch, and test before committing.

## What is correct
- Test first, do not switch on faith. Right plan.
- All seven families named are OFL-1.1: VERIFIED (Fontsource metadata, 27 Oct).
- Literata has Latin, Greek and Cyrillic, is variable (weights 200 to 900) and has italic: VERIFIED. Source Serif 4 and Plex Sans have Greek: VERIFIED.
- Softer text colour #DCE1EB gives 14.5:1 on the dark background; the current #f2f4f9 gives 17.3:1. Both pass 7:1: VERIFIED by calculation.
- Keep Plex Mono for labels only. Agreed (judgment). It is already hosted (2 files, 29 KB).
- Its estimates were labelled as estimates; I found no invented claims.

## What needs changing (the addendum)
1. **Glyph coverage was the question we asked, and the report did not answer it.** Measured on the files the book serves today: Inter (2 files) and Plex Mono (2 files) all lack σ μ λ Δ θ ≈ ≥ ≤ →. VERIFIED (character maps read). The book uses σ 38 times, ≈ 28, μ 11, ≥ 3, Δ 2, ≤ 1, → 1 (counts in the book's source). So today those characters come from the phone's system font. This may be part of why the type feels off (UNCERTAIN). ⊕ and ☉ appear 0 times, so ignore them.
2. **Two of its three pairings lack Greek.** Atkinson Next ships Latin and Latin Extended only in the Google Fonts build; Plex Serif and Plex Mono also have no Greek: VERIFIED (metadata; upstream sources may differ, UNCERTAIN). Fix if needed: a tiny Greek and math subset (σ μ λ Δ θ ≈ ≤ ≥ →, a few KB), NOT TESTED.
3. **The CSS is a sketch, not drop-in.** The book's hooks are `.md-typeset` and three variables, `--ss-read`, `--ss-ui`, `--ss-data` (`observatory.css` lines 12 to 25). A font swap is a few lines there plus new `@font-face` rules. The snippet's selectors do not match them.
4. **Remove `"cv11", "ss03"`** (`observatory.css` line 20) on any swap. Those tags are Inter's own; in another font they could switch on unrelated letter alternates. Line exists: VERIFIED. Effect on other fonts: UNCERTAIN.
5. **Old-style figures in body text suit this book badly.** Prose is full of measurements ("7.2 σ", "95.2 d"). Use lining figures in prose and tabular figures in tables (judgment, LIKELY). Whether Literata supports each figure style: NOT TESTED.
6. **Literata has an optical size axis (7 to 72): VERIFIED.** The report's `@font-face` ignores it. Keep the axis in the file and leave `font-optical-sizing` on auto.
7. **Size budget.** Today's set is 130 KB (Inter 48 + 52, Plex Mono 15 + 15). The report's 100 to 200 KB for Literata roman and italic plus Plex Sans is UNCERTAIN; variable files with an optical axis are larger. Measure before deciding.
8. **The test must include controls.** Put Inter and Source Serif 4 in the same test, because you set aside both within four days. Also separate font from other causes (glare of bright text on dark, density, the PC layout). The unhappy feeling may not be only the font (UNCERTAIN).
9. **Offline.** No font file names appear in the book's JS (VERIFIED), so how the service worker caches fonts is NOT TESTED. Our offline browser gate will catch a miss. A "Reading font" switch does not exist yet (VERIFIED, not in the repo).

## Single best next step
A font test page, outside the book. Use a private Artifact (Google Fonts are allowed inside an Artifact only), so nothing is downloaded and nothing in the repo changes. It shows your real paragraph, a number table, "σ" labels, dark and light, at 17 px and line height 1.7, with a switcher: Inter, Source Serif 4, Literata, Plex Sans, Plex Serif, Atkinson. Read it on your iPhone at night. Estimated 0.5 to 1 point. The real change then belongs to to-do item 10 (visual identity).
