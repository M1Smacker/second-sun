# Compass review: "Second Sun, Visual Identity Redesign" (Phase 1: Artifact prototype), 24 Oct 2026

*Review only. Nothing was built, no Artifact was made, no site file was changed. I read the live book (home, a chapter, the field notes page), `book/mkdocs.yml`, the colour tokens in `book/docs/assets/extra.css`, `research/BOOK-REDESIGN-BRIEF.md` (Ahmed's approved brief of 23 Oct), the build log and the gate scripts.*

Labels: **VERIFIED** (I read or measured it), **LIKELY**, **UNCERTAIN**, **NOT TESTED**.

## 1. Verdict: REVISE (accept about 85%; run it after a short addendum and three answers from Ahmed)

It is a strong brief. The approval gate (Phase 1 prototype only, then STOP) matches our two-key rule. "Do not invent" and "preserve what works" are exactly right. One finished direction instead of three concepts is right. The problems are not in the taste of the brief but in facts it does not know about the book.

## 2. What is correct

| Claim in the brief | Status |
|---|---|
| The homepage's opening should be identity first, metrics later | **VERIFIED** as a real issue below the map: after the Cygnus map come four stat tiles (readiness 48/100, candidates 0), a "Where you are" box, a six-gauge readiness panel and a six-row status panel, all before the contents list |
| The existing Cygnus sky map is worth keeping as a signature | **VERIFIED**: it is built from real catalogues (Bright Star Catalogue, Villanova Kepler EB), shows 546 of our 549 Kepler stars at true places, and already carries the six Parts |
| The site is a documentation theme with a dark palette | **VERIFIED**: it is Material for MkDocs with custom CSS (`theme` in `mkdocs.yml`, night default `#0c1018`, day `#faf9f6`), a left sidebar, a right contents rail, and the same boxed callouts ("In plain words", "1-minute summary") on every chapter |
| Navigation can be regrouped without breaking URLs | **VERIFIED**: the menu is a `nav:` list in `mkdocs.yml`; URLs come from file paths, so regrouping and renaming labels changes no address |
| Field notes and the learning record deserve their own character | **VERIFIED** they exist: field notes 19, 20, 21, 23, 24 Oct 2026 (day 1 to day 6), and a Learning track with levels L0 to L6 (only the L1 lesson has its own page; the rest are check questions) |

## 3. What needs changing, and why it matters

### Fix 1 (CLOSED, 24 Oct night: Ahmed confirmed the book's spelling "Hanzala" is correct; ChatGPT has "Hanzla" from his Google account; no change to the brief needed beyond using the correct spelling): the surname is spelled differently in the brief and on the site
The brief says "Ahmed Hanzla". The book says **Hanzala** (home page byline and Chapter 15). **VERIFIED** (2 places in the book, 0 uses of "Hanzla" anywhere in the repo). I cannot tell which is right. A cover with the wrong spelling of the author's own name is the worst possible error on a cover. Ahmed confirms the spelling; until then the prototype uses the site's.

### Fix 2: the book is not a first-person notebook, and the design must not pretend it is
The brief pictures "one person's journal". The real record is a diary **written to Ahmed**: the home page says "Ahmed, this is your book", the byline is "Ahmed Hanzala with Claude", and the field notes use "you" for Ahmed and "I" for Claude (**VERIFIED**, 24 Oct note and home page). Ahmed's own voice appears as his decisions and questions, not as authored paragraphs. The brief's own honesty rule ("do not pretend every line was written by him") requires: a byline "Ahmed Hanzala with Claude"; each field note labelled as written by Claude from the day's work for Ahmed; and Ahmed's decisions shown as decisions (for example "Ahmed decided: ..."), quoted only where his words exist in the project files. No invented marginal handwriting.
**The honest margin that already exists:** the shape-coded evidence chips (VERIFIED solid, LIKELY dashed, UNVERIFIED dotted), claim numbers like F-059, glossary pop-ups, "Idea:" and "You could try:" lines, and the quiz questions. Make these the marginalia. They are real, they are the project's signature, and they need no invention.

### Fix 3: it reopens two decisions Ahmed made yesterday
`BOOK-REDESIGN-BRIEF.md`, approved 23 Oct after 19 rounds of questions: **dark night-sky look by default, light on request, high contrast**; font chosen: **Inter** (Literata and Source Serif 4 were the other candidates, and Source Serif 4 was the old font). This brief leans to ivory reading surfaces and a serif for titles. That may well be what he wants now, but it must be his decision on seeing it, not mine. So the prototype shows **one direction in two schemes** with a night/day switch, serif display plus Inter for interface, and says plainly which scheme is the default in the design. It is not two concepts; it is one identity with the two modes the book already has.

### Fix 4: constraints the brief does not know, which would block the build in Phase 2
All **VERIFIED** in the repo:
- **Contrast of 7:1 or better** for text, secondary text and accent on every surface in both schemes (`test_contrast.py` is a publish gate). Measured: a typical muted brass on ivory (`#b08d57` on `#faf7ef`) is **2.9:1**, another (`#a67c3d` on parchment) **3.2:1**, a typical grey secondary text (`#6b6f7a`) **4.7:1**. All fail. What passes: today's day accent `#6f4608` (7.8:1), amber on night `#eebf6a` (11.2:1), ink `#1b1f2a` on ivory (15.4:1). So brass can be an ornament (rules, ticks, the orbit line), never small text on ivory; text accents use the deep brass.
- **Fonts must be hosted in the book**, not loaded from a font service, because the book works offline on the iPhone (precache is 4.7 MB of a 25 MB budget, plenty of room; each font needs its licence file like the existing `OFL-inter.txt`). Source Serif 4, Literata and Inter are, as far as I know, under the SIL Open Font License (**LIKELY**; Inter's licence is in the repo, the others from memory). The Artifact itself may use Google Fonts, because that is what an Artifact allows.
- **Phone tests**: no sideways scroll at 375 px and tap targets of at least 44 px are checked by the browser tests before every publish.
- **Existing features that must survive** and are not in the brief: Eyes mode (canvas, banner, twin drill, results), the labs, the Listen button, glossary pop-ups, mark-as-read, search, instant navigation, the per-Part cheat sheets, the day/night toggle, reduced-motion.
- **No en or em dashes** in the book's visible text (standing rule). The prototype copy must follow it.

### Fix 5: do not invent an edition, and keep one honest status line
No volume, edition or publication date is supported. Supported and **VERIFIED**: the notes start on **19 October 2026** (day 1), the latest is 24 October (day 6). A cover line like "Field notes since 19 October 2026" is true. The current panels also carry the book's honesty ("Nothing here is a discovery yet", "readiness is not the chance of finding a planet"). Keep metrics off the cover, but keep one plain status line near the foot of the opening page and link to Progress, so the honesty is not lost to elegance.

### Fix 6: "learning record" is the Learning track
Use the real name and structure (levels L0 to L6, one lesson page so far). Levels without their own page are shown as "check questions only" and never dressed up as finished lessons.

### Fix 7: cost and timing
Weekly usage is 94% now, reset about 01:00 Tuesday 27 Oct Kuwait time. A polished five-view Artifact with real content is a big job: my estimate is **4 to 8 weekly points for the first round and 1 to 3 per revision (UNCERTAIN: no earlier Artifact of this size)**. Run it after the reset, in a fresh session with a short brief, and allow at most two self-revisions before showing it. Build order: homepage, chapter, field note, contents, then the phone pass.

## 4. Practical notes for building it (not problems)
- An Artifact cannot be assumed to read the live site, so real material is embedded: the home map SVG (from the built page), the chapter list from `mkdocs.yml`, Chapter 2 text (about 6 KB), the 24 Oct field note (7 KB), and a figure drawn from the real TOI-1338 sector 98 data (40 KB file, labelled as 10-minute averages). Expect well under 1 MB.
- I can check the phone layout at 375 px in my browser pane; I cannot see an actual iPhone.
- Everything stays private (an Artifact is private until you share it). Nothing goes near the repository or the live book in Phase 1.

## 5. Paste-ready addendum for the brief (about 10 lines)
> Project facts to follow. The site names the author "Ahmed Hanzala" (confirm spelling with Ahmed) and the byline is "Ahmed Hanzala with Claude". The book is a diary written to Ahmed by Claude from the day's work; field notes are second person ("you") and say who wrote them; Ahmed's own words appear only as decisions or quotes found in project files. The margin of the book is its evidence apparatus: chips VERIFIED, LIKELY, UNVERIFIED (solid, dashed, dotted outline), claim numbers, glossary terms, "Idea" and "You could try" lines. Keep the real structure: tabs Read, Hunt, Reference, Parts 1 to 6 with chapters 1 to 15, Eyes mode, Field notes (19 to 24 Oct 2026), Learning track L0 to L6. Show both a night and a day scheme (night is today's default, chosen by Ahmed on 23 Oct); text and accent colours must reach 7:1 contrast on every surface; brass is for ornaments, deep brass for any text. No en or em dashes in any visible text. No volume or edition number; "field notes since 19 October 2026" is true. Production fonts will be hosted in the book, so choose only fonts with an open licence. Phone first: check 375 px, tap targets at least 44 px, no sideways scroll, reduced motion respected. Do not remove or hide Eyes mode, labs, Listen, glossary pop-ups, search or progress.

## 6. The single best next step
Ahmed answers three things in chat: (1) the correct spelling of his surname; (2) which scheme the cover should lead with, night or day; (3) that the serif-plus-Inter pairing may be shown (it replaces yesterday's Inter-only pick for titles only if he likes it on seeing it). Then run Phase 1 after the weekly reset.
