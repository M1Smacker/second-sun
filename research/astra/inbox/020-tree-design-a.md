# Brief 020: build Tree design A into the book (Claude, 15 Nov 2026, about 12:10 pm; Ahmed away, Claude reviews)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why
Ahmed rejected the current Tree (canvas with zoom and pan, phone vine on the left, a Journey that alternates sides with a line through the text). He also rejected a second design of Claude's. His words: "Go back to the design which ChatGPT's mockup created. Exactly that design. Follow that design." That is mockup A ("A Real Tree").

Claude rebuilt mockup A as a working prototype from the real Tree data. It is in `research/tree/design-a/`:
- `prototype.src.html`: the page source. `build_prototype.py` inlines `tree-data-sample.json` to make a runnable copy.
- `prototype-*.png`: the prototype's screenshots (PC, phone, phone sheet).
- `Second-Sun-A-Real-Tree-0*.png`: the mockup itself. **The mockup is the judge when the two differ.**

Your job: replace the Tree page's views with this design inside the real book. It must keep the page's working features and pass every gate. Tree node 4.1, FIX 100 (new; Claude files it on the Tree).

## Hard design rules from Ahmed (each one is a test)
1. **Layout, PC (900 px and wider).**
   - Title "The Tree", with "Field notes ›" and "Search window ›" at the right.
   - The Goal card, and beside it the Petrova scoreboard card (rate, a range bar, "Range a to b%", "Fix first").
   - Path chips: the ACTIVE item, a dashed link, then the NEXT item.
   - Below: branch 1 and branch 4 cards on the left, branch 2 and branch 3 cards on the right.
   - A thin golden vine up the middle, from the roots to the Goal card, with a golden branch to each card, small outline leaves and roots.
   - A node detail panel on the right, sticky. It shows a breadcrumb, the title, a status chip with the short note, What it is, Why it matters (only when real), the loss bar where there is one, Work under this node, and Read more and Learn this links.
   - Proportions as in `prototype.src.html` (`.pc-cols`, `.pc-head`, `.pc-tree`).
2. **Layout, phone.**
   - Title, Goal card, scoreboard card, and the two path chips side by side.
   - The vine with the four branch cards alternating left and right and overlapping in height, as in mockup 01 (`placePhone()` in the prototype).
   - Below: the list card for the chosen branch, with its rows.
   - Tapping a row opens the bottom sheet (mockup 02).
3. **The trunk and vine are golden.** No gold and blue switch. No colour or brightness that depends on a node's weight or importance. Every node looks alike except for its status word.
4. **Text always fits its box.** Boxes grow with their text. Nothing is drawn on a canvas with fixed-size labels. No ellipsis on titles. Work rows may clamp to two lines, because the full text opens on tap.
5. **No zoom and no pan.** The page scrolls like any page, so the tree can never be "lost".
6. **M-33 (new bug, Ahmed):** with a card or panel open on PC, the mouse wheel over it scrolls the card, never the tree. The panel scrolls inside itself (`max-height`, `overflow-y: auto`, `overscroll-behavior: contain`).
7. **Journey view.** One column only: a single vine down the left, newest first, each day's entries to the right of it. Nothing alternates sides and no line crosses any text.
8. **Keep the starfield background** (book3.js). Ahmed likes it. Both themes must work: the prototype has light tokens. Use the book's `--ss-*` tokens and add a gold token pair, legible in daylight (contrast 4.5:1 or better for any gold text).

## Keep what works (do not lose these features)
- Search with Enter and "No matches" (M-17).
- "N new" with "Mark updates read" (M-31).
- The "Now:" line, which is Ahmed's daily recap and must show on the Tree. Put it as one small line under the title.
- The Mission/Journey switch (one small control near the title, not sticky).
- Deep links `#n=1.1`, and Back and Forward reopening the card (M-13).
- On the sheet: the focus trap and the scroll lock (M-11).
- Tap targets of 44 px (M-16). Widening a phone to PC moves an open sheet to the panel (M-14).
- The no-JavaScript static list (`ss:tree-static`).
- Update `tour.js` steps so every step points at an element that exists in the new design (the ring must sit on it, M-04 and M-06 behaviour kept).

## Data (no hand-typed numbers in the page)
Extend `research/tree/brain_build.py` and its tests `research/tree/test_brain_build.py` so `tree.json` carries:
- `sub` per node, a short subtitle: add a `sub:` key to `research/tree/node-plain.yml` for branches 1 to 4 and any node whose title needs one. Use the prototype's SUB words and its 2.1, 2.2 and 3.3 subtitles.
- `loss` per node: parse "Loss: N of 222" from the node's line in `research/TREE.md` (for "45 + 7 of 222", sum it to 52). Null when there is none.
- `bench`: rate, lower and upper bound, and label, parsed from the "**Bench so far:** Petrova 1.0.0 R 27.5% [20.7, 33.7]" sentence in TREE.md. Round for display only.
- `path`: the ACTIVE item and the first NEXT item, each with an id when it names one. The chips use these.

Each new field needs a test that fails when the field is wrong. Builds must still refuse fence stars, as now. Run `research/tree/tree_check.py`; it must pass.

## Files you may change
- `book/docs/assets/tree.js`, `tree.css`, `tour.js`, `book/docs/index.md` (only the Tree block).
- `research/tree/brain_build.py`, `test_brain_build.py`, `node-plain.yml`.
- `book/docs/assets/data/tree.json` (regenerated only, by brain_build).
- `research/burn-3-book/tools/site_check.mjs` (update the `tree` and `repairs` modes to the new design; add checks for rules 3 to 7).
- Your report.

Do NOT change book3.css, book3.js, extra.css, mkdocs.yml, versions.md, hooks.py, learn.*, other pages, `research/TREE.md`, the release gate scripts, pipeline/, data/ (except data/astra/020), or any star data. No version bump.

## How
1. Build with `D:\second-sun\.venv-docs\Scripts\mkdocs.exe build --strict -f book\mkdocs.yml -d D:\second-sun-astra\data\astra\020\site` (absolute output path; a relative one lands under book/, as you found in 019). Serve with `node research\burn-3-book\tools\serve.mjs --dir=data\astra\020\site --port=8497`.
2. Compare your page against the mockup PNGs at 1440 by 1000 (PC) and 390 by 844 (phone). Save screenshots of yours beside them in data/astra/020. Say in the report where yours still differs and why.
3. Run Claude's release gates. Both must pass with exit 0 (they check overflow against the set width, text and header contrast in both themes, sticky see-through bars, JS errors, the menu tap, and the tour):
   - `node research\burn-3-book\tools\release_gates.mjs http://127.0.0.1:8497/ --pages=all`
   - `node research\burn-3-book\tools\webkit_gates.mjs http://127.0.0.1:8497/ --pages=all`

   For WebKit, set `PLAYWRIGHT_BROWSERS_PATH=D:\second-sun\data\tools\ms-playwright`.
4. Run the existing site_check modes at the end: `layout`, `tree`, `learn`, `textfloor`, `chapter`, `repairs`.
5. Show each new check fails on main before your change.
6. Never open the live Eyes page. Never run eyesreal, eyescloud or rehearsalcloud. Never print key values.

## Report
`research/astra/reports/020-report.md`:
- one row per rule above: DONE, PARTLY or NOT DONE, with the measurement;
- the gate results;
- where your page differs from the mockup;
- what you did not check;
- new bugs as a list (do not fix outside your files).

No git commits (the runner commits). Never push.
