# Brief 021: independent read-only audit of Book 3.4 with the new Tree (Claude, 15 Nov 2026; launch only after Codex 020 is merged; Ahmed away, Claude reviews)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why
This morning's audit of Book 3.2.1 found 32 bugs. Your independent pass found 8 that Claude missed. All 32 were fixed in 3.3.0 (live). Codex 020 then rebuilt the Tree to ChatGPT mockup A.

A brand-new page is where new bugs hide. Ahmed opens the book on an iPhone first, and last time he hit three bugs within a minute. This audit is the second pair of eyes before or right after 3.4.0 goes live.

## Mission: find everything, fix nothing
- Do not edit any source file and do not commit (the runner commits your report only).
- Never push, never publish, never open the live Eyes page, never run eyesreal, eyescloud or rehearsalcloud, never print key values.

## What to audit
Build the current main with `D:\second-sun\.venv-docs\Scripts\mkdocs.exe build --strict -f book\mkdocs.yml -d D:\second-sun-astra\data\astra\021\site` (absolute path). Copy `book\archive-v2` to `site\v2`. Serve with `node research\burn-3-book\tools\serve.mjs --dir=data\astra\021\site --port=8497`.

1. **The new Tree, first and hardest.** Compare it to the mockups in `research/tree/design-a/` (Second-Sun-A-Real-Tree-01, -02, -03) at 1440 by 1000, 1280 by 800, 1024 by 768 touch, 390 by 844 and 320 by 568 touch, in both themes. Check:
   - text inside every box;
   - the vine drawn to every card, including after resize and after opening and closing cards;
   - the wheel over the open panel scrolls the panel (M-33);
   - the sheet's focus trap and scroll lock;
   - Back and Forward;
   - deep links `#n=1.1`;
   - search, Enter and "No matches";
   - "N new" and "Mark updates read";
   - the Now line;
   - Journey in one column, with no line through text;
   - the tour ring on every step;
   - the no-JavaScript list;
   - light-mode contrast of the gold.
2. **Regression of the 32 fixed bugs.** For each M-01 to M-32 in `research/stage3/BOOK3-AUDIT-2026-11-15.md` (status section at the end), retest the steps and say still fixed or back.
3. **Everything else a reader touches.** Every page in `sitemap.xml` except eyes/ and rehearsal/ beyond loading, in Chrome and in WebKit (Playwright WebKit with iPhone 13; set `PLAYWRIGHT_BROWSERS_PATH=D:\second-sun\data\tools\ms-playwright`, Playwright at `D:\second-sun\data\tools\playwright\node_modules\playwright`). Check:
   - overflow against the set width (clientWidth, never innerWidth);
   - small text and contrast;
   - tap targets of 44 px;
   - the menu after scrolling;
   - the theme switch;
   - offline (service worker);
   - the 404 page and /v2/.
4. **Three more changes in 3.4.0 (Claude, 15 Nov 2026 afternoon).**
   - **Light mode is now a soft sky blue with white cards** (extra.css tokens). Check readability in both themes on every page, with special care for the Tree's gold and any element that hard-coded white or the old near-white.
   - **The Eyes, rehearsal and Search window scripts now load only on their own pages** (overrides/main.html, T161). Check those three pages still work locally, offline and with JavaScript off, and that no other page lost a feature. Never use the cloud modes.
   - **The ten Book 2 labs left Book 3.** Their links and old addresses now go to /v2/labs/. Check every lab link and redirect lands on the right v2 lab.
5. **Claude's release gates.** Run `release_gates.mjs` and `webkit_gates.mjs` (research/burn-3-book/tools) on your build. Then ask what they CANNOT see: name at least three reader problems they would miss and show whether any exists now.

## Report
`research/astra/reports/021-report.md`:
- the plain verdict line first;
- a bug register (id CX2-01 on, severity P0 to P4, page, steps, expected, actual, evidence file, CONFIRMED or HYPOTHESIS);
- the regression table for M-01 to M-32;
- the mockup comparison (where the Tree differs from mockup A);
- the gate blind spots;
- what you did NOT check.

Evidence goes under data/astra/021. No fixes. Never push.
