# Learning Space: audit and design proposal (3 Nov 2026, evening)

Answer to the pasted prompt "Build a dedicated Learning Space, deep audit and design proposal first". NO EDITS to the book, no mockups, nothing built, nothing published. The Compass pass is `research/compass-reviews/2026-11-03-learning-space-prompt.md` (verdict REVISE). Factual and educational corrections are listed separately in `research/stage3/LEARNING-SPACE-CORRECTIONS-2026-11-03.md`. Waits for Ahmed's explicit approval. Labels: CONFIRMED (read or counted), LIKELY, UNCERTAIN, NOT TESTED.

Files read: `book/mkdocs.yml`, `book/data/path.yml`, `book/shape.py`, `book/hooks.py`, `book/docs/learn/index.md`, `learn/l1-dip-depth.md`, `book/docs/book/` (headings of Chapters 2, 10, 11; word counts of all 15; Chapters 6, 7, 9, 12 passages), `assets/extra.css` and `observatory.css` (tokens and the equation block), `assets/book.js` (progress, glossary popups, read aloud), `assets/demos.js` (demo registry), `progress/levels.yml`, `hooks.py precache_list`, `overrides/main.html`, the manifest. NOT read in full: `shape.css`, `sw-template.js` (cache versioning), the 5 demos' internals. Private events and the live Eyes page were not touched.

## A. Assessment of the existing learning experience
What works (CONFIRMED): the reading order is a real pedagogical choice and is written down once (`path.yml track:`); every level has Read, Do (optional PC labs) and Next; chapters share one seven-part shape; 40 knowledge checks exist with answers; glossary popups, a resume card, "opened" marks and a read-aloud bar exist; the book works offline.

What fails the way Ahmed uses it:
1. The track lives inside the documentation chrome (tabs, a sidebar of about 80 pages, search). There is no course frame. LIKELY the main reason it feels "disconnected".
2. Previous/Next is chapter-based (`shape.py _seq`), so it skips the L1 and L2 pages; the L1 page has no pager (LIKELY). CONFIRMED for `_seq`.
3. Three chapters are split across levels (2: L0 and L2; 10: L5 and L6; 11: L2 and L6) but `path.yml` and the progress store know only whole chapters. The section ranges exist only as prose in `learn/index.md`. CONFIRMED.
4. The 40 checks sit on one separate page (`learn/index.md`), away from the lessons, with no feedback beyond a revealed answer, no retry record, no memory of results. CONFIRMED. Counts: L0 3, L1 3, L2 3, L3 6, L4 3, L5 7, L6 9, After 6.
5. 125 evidence chips in 15 chapters sit in the reading text (about 8 per 1000 words in Chapters 1 to 3). CONFIRMED. He wants them out of the way.
6. No Back control and the app is standalone (`manifest.webmanifest`). CONFIRMED setup, LIKELY cause.
7. Three different progress ideas share one vocabulary (reading, level sign-off in `levels.yml` "Level N of 6", mission readiness in `mission.yml`). CONFIRMED.
8. Equations are plain text in the reading font (14 blocks, no renderer) and the read-aloud voice is the device default (`u.voice` never set). CONFIRMED setup; how they look and sound UNCERTAIN.
9. Whether the explanations answer a newcomer's questions: NOT TESTED. Ahmed reported "many questions left unanswered" and offered a list that has not arrived. Nothing below changes teaching content until it does.

## B. Dashboard (kept at the existing address `/learn/`)
Reading order top to bottom, calm surfaces, no cards-in-cards, Atkinson for text, Plex Sans for labels:
1. Two-line welcome ("Seven levels, from what a light curve is to checking a candidate yourself.").
2. **Continue** block: level, lesson title, minutes, where he stopped ("Level 3 · Noise and statistics · stopped at 7.4"), one large button. If nothing was started: "Begin Level 0".
3. One thin line of overall progress by **words read** across the 21 reading units (so a long chapter weighs more than a short one), with the text "9 of 21 lessons · about 3 h left". Not a percent of levels.
4. **Level ladder**: seven rows L0 to L6, each with name, one-line description, lessons read x of y, total time, and a state shown by shape and word (not started, in progress, read), plus "needs L2" where a prerequisite matters. Tap a row to open its lessons (title, minutes, state, "Lab (optional, on your PC)").
5. **After Level 6: Running the project** as its own block below, labelled "not part of the seven levels".
6. **Labs** as a small separate list of the 10 optional PC labs, each tied to its level.
7. A quiet line: "Knowledge checks answered correctly on this device: 14 of 40" and a link "Project readiness is a different measure" to the Progress page. No XP, streaks, badges or leaderboards.

## C. Immersive lesson reader
Lesson pages are generated (part E) and carry `reader: true`, which removes the site header, tabs and sidebar.
**Desktop:** slim top bar (Back to Learning Space · "Level 3 · 3.2 Our detector" · thin progress for the course · Contents); left rail with the seven levels and their lessons (collapsible; current lesson marked with `aria-current`, finished ones ticked); centre column about 68 characters wide; the existing PC margin for side notes where it exists; fixed bottom bar with Previous and Next showing the titles of both neighbours.
**Mobile (375 px, iPhone standalone):** top bar with Back arrow, short title, and a menu button that opens a drawer holding the path and the page contents; fixed bottom bar with Previous / Next (titles shortened), respecting the iPhone safe-area inset; text 17 px as today.
Page order inside a lesson: title and minutes; "before you start" (prerequisites); "you will be able to" (learning objectives, already written as the `summary` lines in `path.yml`); the text; demo; worked example; "check yourself" (interactive, part I of the prompt); summary; at the very end, tiny: Sources and "Evidence" (collapsed, the claim chips' content). The evidence chips are not shown in the reading text.
**Back control:** if the previous page in history is inside Learning Space, `history.back()`; otherwise go to the dashboard. This is needed because an installed iPhone app has no browser Back (LIKELY). NOT TESTED on his phone.

## D. The course units and the special cases
A **unit** is the reading lesson, one generated page. Sources are sections of the chapter files (headings are numbered 2.1 to 2.7, so a section range is exact). Order below is the path as written in `learn/index.md`.

| Unit | Level | Source | Notes |
|---|---|---|---|
| L0.1 | L0 | Chapter 1 whole | |
| L0.2 | L0 | Chapter 2, 2.1 and 2.2 | split chapter |
| L0.3 | L0 | Chapter 3 whole | |
| L1.1 | L1 | `learn/l1-dip-depth.md` (dedicated lesson) | no chapter |
| L2.1 | L2 | Chapter 2, 2.3 | split chapter |
| L2.2 | L2 | Chapter 2, 2.5 | split chapter (2.4 is not in L2) |
| L2.3 | L2 | Chapter 11, 11.3 (dilution) | a look ahead; marked "read only this section now" |
| L3.1 | L3 | Chapter 7 whole | newest part "Noise is lopsided" |
| L3.2 | L3 | Chapter 8 whole (3,852 words; could be split in two) | newest part "Flags, tiers and frozen settings" |
| L3.3 | L3 | `start/first-search.md` | supporting story read |
| L4.1 to L4.3 | L4 | Chapters 4, 5, 6 | |
| L5.1 | L5 | Chapter 9 whole | newest part "Completeness" |
| L5.2 | L5 | Chapter 10, 10.1 and 10.2 | split chapter |
| L6.1 | L6 | Chapter 10, 10.3 to 10.7 | split chapter |
| L6.2 | L6 | Chapter 11 except 11.3 (already read in L2) | |
| L6.3 | L6 | Chapter 12 whole | |
| A.1 to A.3 | After | Chapters 13, 14, 15 | not in the seven levels |

That is 18 reading units for the seven levels and 3 after (21; the count is fixed when the units are written). Optional labs hang on units as `labs:`, listed separately from reading. Level checks are a separate "check" step at the end of each level, not a reading unit. Level 1 is a dedicated page (`kind: page`), Level 2 is three section units, and Chapter 2 appears in two levels; none of this needs a special case in code, only a `sections:` field on the unit.

## E. Architecture changes (exact paths)
1. `book/data/path.yml`: add `units:` (id, level, title, kind page or chapter-part, source file, `sections`, `labs`, `prereq`, `checks`). `track:` is then DERIVED from `units` in `shape.load()` (or deleted), so there is no second list of the order. The existing build check "learn/index.md links every chapter in its level" is rewritten against units.
2. `book/shape.py`: new `units()`, `unit_seq()` (replaces chapter-only `_seq` for the track), `unit_page()` (cuts the section range out of the chapter markdown, so the chapter file stays the single source of text), `dashboard()` and `reader_nav()`; validation that every section 2.1 to 2.7 etc. is covered as intended and every check id exists.
3. `book/hooks.py`: generate the unit pages (virtual files) with front matter `reader: true`; write `learn/units.json` (ids, urls, order, word counts) for the browser script; the chip function gets a reader mode (hidden, content moved to the page-end evidence list). `precache_list` already walks every built file, so new pages are cached automatically (CONFIRMED by reading it).
4. `book/docs/learn/index.md`: becomes the dashboard shell at the same URL; the intro text and the L5 check are corrected (corrections list); the 40 checks move to `book/data/checks.yml` and are rendered next to the lessons (levels' `#l0` to `#l6` and `#after` anchors are kept on the dashboard rows, so old deep links work).
5. New `book/data/checks.yml`: id, unit/level, type (choice, number with tolerance, pick the graph, interpret, reasoning with reveal), question, answer, feedback for each wrong choice. Free-text reasoning is revealed and self-assessed, never graded.
6. New `book/docs/assets/learn.js` and `learn.css`; added to `extra_javascript` and `extra_css` in `book/mkdocs.yml`: progress store, dashboard painting, drawer, bottom bar, Back control, check engine.
7. `book/overrides/main.html`: when `page.meta.reader` is set, override the Material header, tabs, sidebar and footer blocks (block names LIKELY from the Material theme; NOT TESTED against the installed version).
8. `book/docs/assets/book.js`: keep `get`/`put`; migrate the old `ss-read` and `ss-last` keys once into the new store; hide `.ss-chip` and the read-aloud bar becomes part of the reader top bar.
9. `book/mkdocs.yml`: nav entry "Learning Space"; unit pages kept out of the nav (`not_in_nav`); footer version bump (book 2.10.0, a new feature).
10. `book/sw-template.js`: cache name tied to the release so the icon app refreshes (NOT TESTED whether it already is).
11. URLs: no existing URL changes (`/learn/`, `/learn/l1-dip-depth/`, `/book/NN-.../`). New: `/learn/u/<id>/`. No redirects needed. Chapter pages stay for browsing and reference and gain a link "Open in Learning Space".
12. Tests: `book/tools/page_sweep.js` extended (every unit page, 375 and 1440 px); new `book/tools/test_learning_space.py` for the unit and section coverage rules.
Alternative considered: turn the existing chapter URLs into the reader by script. Rejected: it cannot show only 2.3 and 2.5 of Chapter 2, and it fails without JavaScript.

## F. Progress without a backend
One `localStorage` key `ss-learn` (version 1): last unit; per unit the section ids seen to the end and a read flag (also settable by the button "Mark as read" as an explicit override); per check the attempts, the last answer and whether it was ever correct. A section counts as seen when its heading has passed and the next heading, or the page end, has been reached (an IntersectionObserver), not merely opened. Course progress is words read over words in the path. Everything is wrapped in try/catch so private mode just shows nothing; the book works without it. `levels.yml` (Ahmed's sign-off, set by Claude when he reports a level) and `mission.yml` are never written by the page. Honest limits: per device, and the installed icon app and Safari keep separate storage on iOS (LIKELY, from memory of WebKit behaviour; not opened tonight), so progress made in one will not show in the other. Per his standing rule no export/copy step is asked of him.

## G. Reuse
Reuse: design tokens and fonts (`observatory.css`), `.ss-eq` (restyled after the formula test), `chapter_end()` markup as the base of the bottom bar, `.ss-resume` logic, `.ss-read-btn`, glossary popups, the read-aloud engine (with the better voice from FIX 75), `pymdownx.details` quiz markup as the no-JavaScript fallback for checks, the `DEMOS` registry in `demos.js` (depth, orbit, noise, explorer), `get`/`put`, `precache_list`, `page_sweep.js`. Not reused: the home mission bar data, the Eyes cloud code.

## H. Content to fix before the redesign
See the corrections list: the "three questions" sentence, the 82.7% description in L5 check 4 and the same flaw in Chapter 9's "7 in 10", the L6 check 5 arithmetic, "Level N of 6" against seven levels, one glossary cross-reference. Then: write the notation and units box for the 14 equations; wait for Ahmed's question list and add the explanations it shows are missing (NOT TESTED until it exists).

## I. Testing and acceptance
1. Unit rules test: every section covered as intended; each chapter's text appears in exactly the units the table says; build fails on a gap.
2. Strict build plus the existing publish gate (`publish_book.ps1 -Test`).
3. Page sweep at 375 and 1440 px on every unit page: no overflow, one h1, no script errors, focus visible, tap targets at least 44 px.
4. Navigation: Previous/Next from L0.3 goes to L1.1, from L2.3 to L3.1, from L6.3 to the After block; Back works with instant navigation; deep links `/learn/#l3` and `/learn/u/l3-1/` work.
5. No JavaScript: pages render, pager and checks (reveal fallback) work.
6. Progress store: unit test with a fake `localStorage`; private-mode fallback; migration of old keys; word-weighted progress.
7. Check engine: tolerance cases, retry, feedback text for every wrong option.
8. Reduced motion respected; keyboard walk through dashboard, drawer and bottom bar; screen reader landmark labels.
9. Offline: load, go offline, open three units (in the browser pane's service worker; NOT TESTED on iOS).
10. Acceptance by Ahmed on his iPhone icon app: Back button, drawer, bottom bar, no evidence chips in the text, tiny Evidence at the end, formulas and voice judged by him. I cannot run standalone iPhone; this step is his.
11. Mission readiness file unchanged after any reading (git diff of `book/progress/`).

## J. Usage estimate (LIKELY, from the ledger; UNCERTAIN where marked)
Calibration: the 27 Oct learning-spine build (data change, shape rules, pages, tests, publish) cost 2 points. Ranges in weekly points:
- Stage 1, units model + generated lesson pages + reader chrome + Back + hidden evidence + unit-aware Previous/Next + section progress: 3 to 4.5.
- Stage 2, dashboard: 1.5 to 2.
- Stage 3, check engine and moving the 40 checks with feedback: 2 to 3.
- Stage 4, formulas and voice (FIX 75 and 76): 1 to 2.
- Stage 5, new simulators (circumbinary transit, injection and recovery, matched filter, timing variation, centroid; one to one and a half each): 5 to 7 for five. UNCERTAIN.
- Stage 6, instructional rewrite (analogies, derivations, variable boxes, exercises): 6 to 15, driven by his question list. UNCERTAIN.
Stages 1 to 4 about 8 to 12; the full vision about 20 to 35 over many days. Recommended order: 1, the corrections he approves, 4 (samples first), 2, 3, then 5 and 6 one at a time.

## What I need from Ahmed
Approve (or change) stage 1 as the first build; say when, given his 3-week rule; send the question list; say yes to the corrections list item by item (scientific wording is never changed silently).
