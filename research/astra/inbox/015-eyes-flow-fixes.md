# Brief 015: Eyes mode flow fixes (Claude, 15 Nov 2026, overnight; Ahmed asleep, Claude reviews)

Part of Book 3.0 (`research/stage3/BOOK3-BUILD-PLAN-2026-11-15.md`, decisions in `research/stage3/REDESIGN-DECISIONS-2026-11-15.md`, section "Eyes mode"). You run headless; nobody can answer questions. If something is unclear, choose the safest reading, say so in the report, and go on.

## What Ahmed reported (his words, summarised)
1. After finishing an easy test or a hard test, the Try again / Back controls are far down the page; he has to scroll a lot to find them.
2. When he goes back, he does not return to where he was: sometimes the bottom of the page, sometimes a random place, sometimes the "How it works" explanation, instead of the part with the try-again option.
3. "How it works" must stay but be short and folded behind a small label (closed by default); he does not need to read it every time.
4. The page lacks transitions: things just appear. Add calm transitions (fade or slide, 150 to 300 ms) for the card changes, the result panel and the fold opening; respect `prefers-reduced-motion`.

## Where
`book/docs/eyes.md`, `book/docs/rehearsal.md`, `book/docs/assets/eyes-core.js`, `eyes-hard.js`, `eyes-feedback.js`, `eyes-strength.js`, `rehearsal.js`, `book.js` (navigation, instant loading, scroll), `observatory.css`, `shape.css`, `extra.css`. The book uses MkDocs Material with `navigation.instant` (pages load without a full reload; scroll restoration is involved).

## Hard rules
- **Never open or click the live site** (m1smacker.github.io). It uploads answers to Ahmed's real cloud. Test only on a local build.
- **Do not change behaviour that the tests guard:** scoring, saving after every answer, locked answers, the cloud uploader (`eyes-cloud.js` must not change), the hard test's card rules, the feedback text, the rehearsal statistics. Layout, folding, scroll position, focus and transitions only.
- All these must still pass after your change (run them with node from the repo root): `book/tools/test_eyes.mjs`, `test_eyes_cloud.mjs`, `test_eyes_hard.mjs`, `test_eyes_strength.mjs`, `test_eyes_feedback.mjs`, `test_rehearsal.mjs`. Also `book/tools/test_contrast.py` (colours stay at 7:1 or better) with `D:\second-sun\.venv-docs\Scripts\python.exe`.
- If you can, build the book (`D:\second-sun\.venv-docs\Scripts\mkdocs.exe build --strict -d <temp folder>` from `book/`) and run the browser checks `node research/burn-3-book/tools/site_check.mjs eyeslayout http://127.0.0.1:8491/ --site=<temp>` and `eyes` after starting `node research/burn-3-book/tools/serve.mjs --dir=<temp> --port=8491`. Stop the server you started when done. If the browser cannot start, say so; do not fake a pass.
- No git commits (the runner commits for you). Never push. AGENTS.md wins over this brief.

## Deliver
1. The root cause of points 1 and 2 with file and line (what the code does now, why he lands in the wrong place).
2. The fix on your branch: when a test ends, the result and its Try again / Back controls are in view at once (scroll to them, move focus to them); returning from any Eyes sub-view restores the exact place he left (store and restore a position, not the browser's guess), never the bottom or "How it works".
3. "How it works" folded (a `details` element or the book's own fold), with a short summary label.
4. Transitions as above.
5. Report `research/astra/reports/015-report.md`: causes, what changed (file list), test output pasted (every test above), what you could not test, any risk you see. End with DONE, PARTIAL or BLOCKED.
