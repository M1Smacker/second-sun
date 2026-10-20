# Prompt for the main session (copy everything below the line)

---

You are the main Second Sun session. While you were running STANLEY, a side session (Claude Sonnet 5.5, started by "Unknown mysteries and problems to solve") built and published the book. Read this, take over the book's publishing, and change nothing else. Do not stop STANLEY.

**1. The book is live (Ahmed's request: "read the Bible on my phone, anywhere")**
- URL: https://m1smacker.github.io/second-sun/
- Hosted by GitHub Pages from a separate branch `gh-pages` (Pages source: branch `gh-pages`, path `/`). `main` was never touched, so your pushes are not affected. Never edit `gh-pages` by hand and never force-push it.
- It is the committed `main` at 6547df2 (6 chapters, observatory design, glossary, claims register, quests, candidates, L1) built with `mkdocs build --strict`. noindex is on every page (16 of 16), there is no robots.txt (it cannot work on a project site), and there is a sitemap.xml (harmless while the site is unlinked). No secrets or personal data were found in the tracked files or the built site. The repo itself was already public.
- Verified on the live address, not only locally: the live service-worker version equals the tested build (766c0bdcf620); offline works (54/54 pages cached, search, the demo, 404 page); layout at 390 and 1280 px in dark and light (36 checks, 0 overflow, 0 tap targets under 44 px, 0 console errors); JavaScript off; redirects (one hop). Not tested: real iPhone Safari. Ahmed should open the link, use Share > Add to Home Screen, open it once online, then try airplane mode (the blueprint section 6 checklist).

**2. How to update the live book (after you change anything under `book/`)**
1. Commit your changes to `main` first. The script builds the committed `main`, not your working tree.
2. Run in PowerShell: `D:\second-sun\research\burn-3-book\tools\publish_book.ps1` (add `-Test` to run the browser checks on a spare port first; `-DryRun` builds and checks without pushing).
3. It takes about a minute. GitHub then needs 1 to 2 minutes to go live. A run with no changes says "Nothing changed" and publishes nothing.
- What it does: fresh clone of committed `main` into the scratch folder `D:\ss-pages-work` (outside the repo), strict build, safety checks (noindex on every page, size, secret patterns, `sw.js` present), commit to `gh-pages` from a separate clone, push `gh-pages` only. It never touches your working tree, your git state, port 8471, `pipeline/` or `data/`. Do not delete `D:\ss-pages-work`.

**3. Two problems I found in your tree (I did not change them)**
- **The build only works because of an ignored file.** `.gitignore` has `data/`, which also ignores `book/data/claims.csv`, so a clean clone of GitHub cannot build the book (`mkdocs` fails: "The path ... book\data isn't an existing file or directory"). The publish script works around it by copying the file from your working tree and prints a warning. Fix it at the source: add `!book/data/` and `!book/data/**` after the `data/` line in `.gitignore`, then commit `book/data/claims.csv`. This also matters for the blueprint's future GitHub Actions workflow.
- **Minor accessibility item.** `book/ch6-our-data/` has a "VERIFIED" confidence chip that is not inside a paragraph, list item or table cell (probably in a heading or a box), so it is 87 x 20 px as a stand-alone tap target. Chips inside text are fine.

**4. What else I built while you worked (all under `research/burn-3-book/`, summarised in `report.md`, `DONE.md`, `claims.md` B1-B28, `friction.md`, `open-questions.md`)**
- The book prototype, now folded into your `book/`: design tokens and type scale from SITE-BLUEPRINT.md, one amber accent, confidence chips by outline shape, quiet "Level n of 6" progress (no XP, ranks, badges or streaks), 150-250 ms transitions that switch off under reduced motion, the 3-cache service worker (batched install that skips failures, capped image cache, "Updated. Reload" line with loop guards), claims register and `{{claim:ID}}` chips, noindex.
- A stress test with evidence (7 of 7 modes pass), 11 bugs found and fixed, the update flow A to B proven (one line, one reload), 300 extra pages plus 50 images (build 3.6 s, precache 14 MB, search index 4.1 MB, install survives a 404), JS off, offline, no loops. Test tools: `tools/site_check.mjs`, `tools/serve.mjs`, `tools/make_stress.py`.
- **Test-server finding:** on this PC Chrome left 4-17% of requests to Python's `http.server` hanging (curl: 0%, Node: 0%). Use `tools/serve.mjs` (Node) for browser tests.
- A learning track written to Ahmed (L0 warm-up plus L1-L6, blueprint lesson template), `learning-track.md`.
- Research: **ExoFOP has been publish-first since 2026-08-19** (a candidate must be published in a peer-reviewed journal, or an RNAAS note citing a previously published method, before upload, plus an approved upload request; uploads were paused 2026-03-31). MNRAS: AI use disclosed in the cover letter and the paper, no affiliation requirement, APC 2,356 GBP (VERIFIED). A&A: no AI authors, coding help needs no disclosure (LIKELY; their site blocks our tools). 13 conflicts with SITE-BLUEPRINT.md are listed in `report.md` (for example the candidate statuses and the scoop switch should follow publish-first).

**5. Uncommitted files I left in your working tree** (yours to commit or not): `research/burn-3-book/tools/publish_book.ps1` (new) and `research/burn-3-book/tools/site_check.mjs` (modified: theme test now works under a base path such as /second-sun/). `pipeline/stanley/run_search.py` is not mine.

**6. Decisions still waiting for Ahmed**
- The ExoFOP publish-first rule breaks "two keys, then CTOI" (C11): see `open-questions.md` #1.
- Later, optionally: move deployment into a GitHub Actions workflow on `main` (the blueprint's design). It needs a commit on `main`, so do it at a calm moment, then switch the Pages source to "GitHub Actions". Until then the script above is the deploy.
