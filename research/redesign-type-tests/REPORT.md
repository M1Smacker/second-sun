# Redesign v2: type and symbol tests (27 October 2026, overnight run)

Nothing in `book/` was touched. These are research notes and the scripts that produced the numbers, so the real redesign (F4) can start from measured facts.

## Why this exists
Ahmed did not approve the first redesign canvas. He asked for: Atkinson Hyperlegible Next against Literata for reading text and headings, IBM Plex Sans for the interface, Plex Mono kept as a candidate for scientific labels; a quieter contextual right margin; the 15 chapters kept apart from the 7 level track; an Eyes layout that scrolls naturally; and a tested symbol font. The canvas is now version 2 at https://claude.ai/artifact/D5a9xdG1NFnDVHrCJUXyTQ (seven boards: Main, Type-Compare, Symbols, Phone, PC-Chapter, PC-Eyes, Zoomed).

## Characters the book needs
`scan_glyphs.py` found 31 characters beyond ASCII in `book/docs`, `book/data`, `book/progress` and `book/overrides` (see `glyphs_used.txt`): Greek (sigma 44 uses, mu 15, delta, Delta, Sigma, pi, lambda, theta), maths (approx 32, square root 27, minus 23, times 35, divide, plus-minus, superscripts, primes, greater-or-equal, less-or-equal, proportional-to, right arrow, combining macron), and marks (black star 9, check mark, ballot x, left and right triangles). Four astronomy candidates were added for the test (circled dot, circled plus, sun, Jupiter); the book does not use them yet.

## Coverage, read from the font files (`analyze.py`, `proof.py`)
| Font (Fontsource 5.3.0 files) | draws of 31 used | of 4 astronomy |
|---|---|---|
| Atkinson Hyperlegible Next | 10 | 0 |
| Literata | 20 | 0 |
| IBM Plex Sans | 20 | 0 |
| IBM Plex Mono | 12 (no Greek) | 0 |
| Inter | 20 | 0 |
| Noto Sans Math (full) | 28 | 3 |

Inter, the earlier assumption, has Greek and primes but not the maths signs or marks (approx, root, greater-or-equal, less-or-equal, proportional-to, arrow, black star, check mark, ballot x, triangles).

## Symbol files cut for the redesign
- `ss-symbols.woff2`: Noto Sans Math cut to 23 characters (Greek, maths signs, primes, black star, check mark, triangles, and three astronomy symbols), **1,876 bytes**. Re-opened and verified: all 23 present.
- `ss-cross.woff2`: Noto Sans Symbols 2 cut to U+2717 only, **876 bytes**. Noto Sans Math lacks the ballot x.
- Jupiter (U+2643) is in no cut file. Noto Sans Symbols has it (about 1.2 KB if ever needed); the book does not use it.
- Full Noto Sans Math is 264 KB, so the cut saves 99%.
- Licence: SIL Open Font Licence (`OFL-noto-sans-math.txt`); keep it with the files when they are hosted.
- Noto Sans Math has one weight, so a sigma in a bold heading is drawn regular, not faux bold (`font-weight:100 900` on the `@font-face` stops synthesis).
- Not tested: STIX Two Math, Latin Modern Math, DejaVu Sans, Libertinus Math; Greek in IBM's own Plex Mono release (the Google and Fontsource build has none).

## Weight of each option (Latin, one chapter page with Greek)
Today (Inter normal and italic, Plex Mono 400 and 500) 126.9 KB; option A (Atkinson normal and italic, Plex Sans 400 and 600, Plex Mono 400, symbol files) 132.8 KB; option B (Literata normal, italic and Greek, Plex Sans 400 and 600, Plex Mono 400, symbol files) 185.3 KB.

## Measured in a browser on a local plain-HTML copy of the boards
- No horizontal overflow on any board at 390, 1100, 1366 and 1500 px.
- 540 px reading column at 18 px: about 70 characters a line in A, 65 in B. In the PC chapter board 64 to 69 characters in A. (A 600 px column gave 72 to 75, so the redesign column is 540 px.)
- All fonts loaded; the face toggle and the Normal and Large buttons switch correctly (17 px to 19.55 px).
- 106 glyph outlines drawn and 104 marked "none" (35 characters in 6 fonts); every outline inside its box.
- Contrast by script, night and day, on all three surfaces: text 14.5 or better, secondary 9.6, accent 7.1 (rule 7). The lighter grey is used only for lines and "none" marks (6.3 or better).

## Not verified
The boards inside the Artifact viewer itself and on an iPhone; day mode on a device; the Eyes boards are drawings of a proposed layout, not tested pages; Google serves the fonts in the canvas and the numbers above come from Fontsource files that should match.

## Reproduce
`python download_fonts.py`, `python scan_glyphs.py D:/second-sun`, `python analyze.py`, `python proof.py`, then `python build.py` (needs fontTools and brotli). Real feedback text and the example Eyes card come from `fb_sample.cjs`, which calls the book's own `eyes-feedback.js` and `eyes-hard.js`.
