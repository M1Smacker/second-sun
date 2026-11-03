# Compass review: "Build a dedicated Learning Space" prompt (3 Nov 2026, evening)

Review only. The prompt came from ChatGPT via Ahmed (pasted in chat). Checked against the real files; nothing was edited in the book. Labels: CONFIRMED (read in a file or counted by script), LIKELY, UNCERTAIN, NOT TESTED.

## 1. Verdict: REVISE (approve the vision, change six points before any build)

## 2. What is correct
- Seven levels plus a last step: CONFIRMED (`book/data/path.yml` `track:` L0 to L6 and AFTER).
- The order is deliberately not the chapter order (Chapters 7 and 8 before 4, 5, 6): CONFIRMED.
- Level 1 has its own page (`book/docs/learn/l1-dip-depth.md`) and Level 2 borrows Chapter 2 sections 2.3 and 2.5 and Chapter 11 section 11.3: CONFIRMED (`learn/index.md` lines 31 to 48).
- Progress is on the device only and the book works offline: CONFIRMED (`book/docs/assets/book.js` uses `localStorage` keys `ss-opened`, `ss-read`, `ss-last`; `hooks.py precache_list` caches every built file).
- The chapter has the seven-part shape (intuition, meaning, technical, ours, worked example, conclusions, check) plus Sources: CONFIRMED (headings 2.1 to 2.7 in Chapters 2, 10, 11).
- The two content issues the prompt names are real: the "three questions" sentence is wrong and the 82.7% is mis-described (details in the corrections list).

## 3. What needs changing, and why it matters
1. **Three levels split chapters, not two.** The prompt names only Levels 1 and 2 as special. In fact Chapter 2 is split between L0 (2.1 to 2.2) and L2 (2.3, 2.5), Chapter 10 between L5 (10.1 to 10.2) and L6 (10.3 to 10.6), and Chapter 11 between L2 (11.3) and L6. `path.yml` lists each chapter once and holds none of the section ranges; they exist only as prose in `learn/index.md`. CONFIRMED. So a "unit" model with section ranges is required, and the lesson pages must be built from sections.
2. **Previous/Next skips whole lessons today.** `book/shape.py` `_seq()` is chapters only, so from Chapter 7 "Previous" goes to Chapter 3, skipping the L1 and L2 pages; the L1 page has no generated pager (hooks wrap chapters only). CONFIRMED from the code; the L1 pager LIKELY (page ends with a Quiz section and no Next line).
3. **"Native back button stays functional" does not help Ahmed.** He opens the book from the home-screen icon, and the manifest is `"display": "standalone"`, which has no browser Back. LIKELY (his answer plus the manifest; not tested on his phone). The reader needs its own Back control.
4. **Chapter-level progress cannot represent partial-chapter lessons.** The existing store marks whole chapters read (`ss-read` holds chapter numbers). Reading 2.1 and 2.2 of Chapter 2 cannot be recorded. CONFIRMED. The new store needs section-level state.
5. **Three or four different measures must stay apart, and one of them is hand-kept.** (a) reading progress (device), (b) check results (device), (c) Ahmed's level sign-off in `book/progress/levels.yml` ("L2 done 3/3", set by Claude on his report, and it counts "Level N of 6" while the page says seven levels), (d) mission readiness `book/progress/mission.yml`. The prompt is right that (d) must not move; (c) cannot be updated by a page and must stay manual. CONFIRMED.
6. **Too many projects in one prompt.** It bundles a reader, a dashboard, a check engine, five or more new simulators, a rewrite of the teaching style of 15 chapters and a content audit. Stage it. The five existing demos (depth, orbit, noise, explorer, eyes in `demos.js`) probably cover three of the eight simulators named (LIKELY, judged from their names; the demos were not opened); the rest are new builds of their own.
Also missing from the prompt, from Ahmed's answers tonight: evidence labels hidden by default and nearly invisible (tiny entry at the very end of the page), a natural read-aloud voice, and formula typesetting. They belong inside the reader.

## 4. Duplicates found (reuse, do not rebuild)
Pager and "Mark as read" (`shape.py chapter_end`), resume card, sidebar "opened" marks, glossary popups, read-aloud bar, collapsible quiz blocks (`pymdownx.details`), the `get`/`put` storage helpers, the demo registry, design tokens in `observatory.css`, the page sweep test (`book/tools/page_sweep.js`).

## 5. Risks
- Scope and cost (see proposal part J). Ahmed's own 3-week rule (no new system designs before T122 verdicts and the G3 result) applies to the dashboard and simulators; his instruction tonight is a design request, not a build go.
- Duplicated content: generated lesson pages repeat chapter text at a second URL; fine for a noindex book, but each text change must flow from one source (the chapter markdown), never be copied.
- iOS stores the home-screen app's data separately from Safari's (LIKELY, from memory of WebKit behaviour, not opened tonight), so progress made in Safari will not appear in the icon app.
- The service worker must refresh on release or the icon app keeps old pages (NOT TESTED: whether `sw-template.js` versions the cache by build).

## 6. The single best next step
Approve the proposal's stage 1 only (units in `path.yml`, generated lesson pages, reader chrome with Back and hidden evidence, unit-aware Previous/Next, section-level progress). It fixes everything he hit last night and every later stage sits on it. The proposal is `research/stage3/LEARNING-SPACE-PROPOSAL-2026-11-03.md`.
