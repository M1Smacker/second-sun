# Burn 3: the book prototype, the learning track, and submission rules

*Second Sun, burn 3. Claude (Opus 5.5), 2026-10-19, 20:52-22:10 UTC (Ahmed lifted the time limit for this session). Claims B1… are in `claims.md`; raw test output is in `test-results.jsonl`; screenshots are in `screens/`. Follows Ahmed's design rule and the adopted `research/SITE-BLUEPRINT.md`; the blueprint wins wherever this prototype differs.*

---

## In plain words (read this first)

**1. The book prototype now matches the blueprint, and it has been stress-tested.** (`site-proto/`)
- **Look:** a calm textbook at night, using the blueprint's exact colours and type sizes, with **one amber accent**. Facts carry small **confidence labels** whose meaning comes from the outline shape (solid / dashed / dotted), never from colour. Every colour pair passes the readability check (B8).
- **Quiet progress, no game:** one line, "Level 0 of 6 · Next: L0 What a light curve is", plus dated checklists, a quests page and plain candidate cards. No XP, ranks, badges or streaks.
- **Gentle motion where it helps:** the theme switch, link hover and focus, quiz answers opening, page changes, the update notice and the demo slider all ease in over 150-250 ms. Turn on "reduce motion" on your phone and all of it switches off (measured).
- **Offline, the blueprint way (three caches):**
  - every page is saved in small batches, and a file that fails is skipped instead of breaking offline mode;
  - images are saved when you first view them, with a cap;
  - a new version waits until you tap **"Updated. Reload"**: one tap, one reload, and it never forces a reload mid-read.

**2. What the stress tests showed** (details under "Stress tests"):
- Everything passes: build, phone and PC widths, dark and light, offline (pages, search, demo), JavaScript off, the update flow, and 300 extra pages with 50 big images.
- **No loops:** the page reloads at most once on an update, never on first install. A theme click changes the theme exactly once. Redirects happen once. The build never re-triggers itself.
- **I found and fixed 11 real bugs** (list below). The worst was that my own tap-size rule made both theme icons show at once.
- **A useful side finding for all your projects:** on this PC, Chrome leaves 4-17% of requests to Python's built-in web server hanging, and 0% with a tiny Node server. It explains the random "connection reset" errors seen tonight. Tests now use the Node server.

**3. The learning track is a course written for you** (`learning-track.md`): an L0 warm-up plus levels 1-6, each in the blueprint's lesson template, on TOI-1338 and your G1 Kepler binaries. No XP.

**4. Submitting candidates changed this year** ⚠️: since 19 August 2026, ExoFOP only accepts candidates **after** they're published (B9, B10). "Find it, two keys, CTOI" becomes "find it, two keys, publish, then ExoFOP". This needs your decision (open-questions.md #1).

**5. Journals:** MNRAS wants AI use disclosed in the cover letter and the paper, accepts authors without an institution, and charges £2,356 (VERIFIED). A&A: no AI authors; coding help needs no disclosure (LIKELY, because their site blocks our tools). RNAAS (free) stays the first venue.

---

## Book design rule (Ahmed, 2026-10-19; applies to every page)

Ahmed's words: "make sure the bible still look professional and cleaner. dont make it a full gamey look. It should explain everything very cleanly and it should be personalized to me."

1. **Look:** a calm, professional reference book. Restrained night-sky palette with **one accent (amber)**; no neon, glow, game fonts, badges or trophies.
2. **Progress stays, but quiet:** one line ("Level 2 of 6"), checklists, milestones, plain candidate cards. **No XP, ranks, badges, streaks or level-up banners.**
3. **Explaining:** "In plain words" first, then detail; one idea per section; glossary links for technical terms.
4. **Personalised:** written to Ahmed by name, on his data and project (TOI-1338, G1 Kepler-field binaries, SS-0001…), his goal, his pace and his level.
5. **Motion (Ahmed, this session):** subtle and purposeful, 150-250 ms, ease-out, no bounce or glow, and off under `prefers-reduced-motion`.

---

## Stress tests (all run 2026-10-19; evidence = tool output, not eyeballing)

Tools: `tools/site_check.mjs` drives headless Chrome over the DevTools Protocol (no npm packages); `tools/serve.mjs` is a static server that behaves like GitHub Pages (directory index, one 301 for a missing slash, 404 page, `--fail` to force a 404); `tools/make_stress.py` makes the dummy pages and images. The final full run (all modes on the final build) is in `test-results.jsonl`: **7/7 modes pass**.

| Test | Result | How it was measured |
|---|---|---|
| `mkdocs build --strict` | **passes**; build 0.50 s warm (1.1 s wall), 1.33 s first cold run (2.8 s wall); precache **32 entries, 559 KB** | three timed runs; the hook logs the precache size |
| 300 dummy pages + 50 dummy images (203,188 bytes each, 9.7 MB) | strict build **passes in 3.2-3.6 s** (3.8-4.1 s wall); precache **634 entries, 14.1 MB (< 25 MB)**; images correctly left out of the precache (9.8 MB, runtime cache); search index 4.1 MB; one page 33 KB | temporary copy built twice, then deleted |
| Service worker install when a precache file 404s | **installs and activates**: normal site 30/32 cached (2 forced 404 URLs); stress site **632/634 cached in 5.1 s**; the missing page shows the 404 page offline | `serve.mjs --fail=…`, `site_check fail404` |
| Image cache cap | 50 images viewed, cache holds **exactly 10** with the cap set to 10 for the test (real cap 150) | `site_check images` on the stress copy |
| 25 MB budget | adding a 26 MB file makes the build **fail**: "offline precache is 40.1 MB, over the 25 MB budget", exit 1 | stress copy |
| Layout at 390 and 1280 px, dark and light, 9 pages (36 checks) | **0 px horizontal overflow** in all 36; correct theme in all 36 | `scrollWidth − clientWidth` per page |
| Tap targets ≥ 44 px | **0 under 44 px** after fixes (5 kinds were too small before, see Bugs) | bounding box of every visible link, button, input, summary and label. Inline text links and confidence chips are exempt (WCAG 2.5.8 inline exception); chips also get a 44 px tall hit area via `::after` |
| Contrast | **all pass**: 26 token pairs + header (lowest text pair 4.59, light `--text-3` on `--bg`; captions only) | `contrast_check.py` (exit 0) |
| Console errors | **0** in every headless test mode. In the Claude Browser pane: exactly **1 per page load**, the pane's browser refusing service workers ("unknown error when fetching the script"; the code catches it), and 0 connection resets with the Node server | CDP `Log`/`Runtime` events; pane console counted before/after one reload |
| Theme toggle | one click → **exactly one** scheme change in 1.5 s (no flicker loop); colour transitions are 0.2 s and only switch on after the first paint (`html.ss-ready`) | MutationObserver on `data-md-color-scheme` |
| Reduced motion | all transitions **0 s**, page animation **none**, slider **0 s** | emulated `prefers-reduced-motion: reduce` |
| Normal motion | page fade 0.2 s, demo bar 0.15 s, links 0.15 s, permalinks 0.15 s, quiz chevron 0.2 s | computed styles |
| No reload loop on first install | first visit = **1 navigation** (no reload) | `Page.frameNavigated` count |
| Update flow A → B | A loads → B built → reopen: the "Updated. Reload" line appears **once** (still 1 after 2 s) while the page stays on A → tap → **exactly 1 reload** → page shows B, cache is B's version only, line gone, 0 errors | `site_check update` |
| No infinite redirect | `/learn` → `/learn/` with **1 redirect online and 1 offline** (the worker redirects to the cached pretty URL; the target ends in "/" so it can't loop) | `Network.requestWillBeSent` redirect count |
| No re-entrant build hook | `mkdocs serve`: **1 build at start, 1 after one touch** of a watched file, **0 more** in the next 8 s | serve log |
| Offline after a first visit | **32/32** precached; 6 pages (visited and unvisited) load offline with full CSS, controlled by the worker; the **demo** works offline (11 Earths → 1.02%); **search** finds 4 results offline; an unknown page and an unvisited image show the 404 page | network emulated offline |
| JavaScript off | `no-js` class; 3 quiz answers start closed and **open natively**; the demo is hidden and its **static SVG fallback** shows; 1,846 characters of lesson text; 23 nav links; candidate cards render | scripts disabled via CDP |
| Test server | Chrome → `serve.mjs`: **240/240 OK, 0 hangs** | `site_check hammer` |

**Not covered (honest list):**
- **Real iPhone Safari:** the blueprint §6 checklist needs the phone after a deploy.
- **Theme switching on top of a running page transition:** only the reduced-motion and normal states were measured, not every combination.
- **Light-theme screenshots:** checked by eye for 3 pages only (chapter, claims, search).

---

## Bugs found and fixed

| # | Bug | Found by | Fix | Re-tested |
|---|---|---|---|---|
| 1 | **Both theme icons showed at once:** my `display:inline-flex` on header buttons overrode Material's `hidden` attribute | screenshot (the measuring script skipped `[hidden]`) | `[hidden]{display:none!important}` | layout now asserts 1 visible toggle and 0 rendered `[hidden]` elements: pass |
| 2 | Tap targets under 44 px: search icon 24 px, clear-search button 18 px, top tabs 31-42 px wide, "Table of contents" label 18 px tall | layout test | sized to 44 px; search box 44 px tall with icon/button aligned | 0 small; search screenshots at 390 and 1280 px checked by eye |
| 3 | Permalink (¶) fade was 125 ms, under the 150 ms floor | computed style | 150 ms ease-out | measured 0.15 s |
| 4 | Offline, `/learn` (no slash) would have shown the 404 page | review | worker redirects once to the cached `/learn/` | 1 redirect online and offline |
| 5 | An unvisited image opened offline gave a network error, not the 404 page (blueprint §6 checklist) | review against blueprint | 404 page for image navigations | offline test asserts it: pass |
| 6 | Old worker: one failed file in `cache.addAll` = no offline at all | blueprint §0.7 | batched `Promise.allSettled`, failures skipped and fetched later | forced-404 tests on the normal and 634-file sites |
| 7 | Old worker cached images in the precache (it would outgrow the budget as vetting sheets pile up) | blueprint §6 | runtime image cache, capped, oldest out | cap test |
| 8 | Precache could store a stale HTTP-cached copy after a deploy (GitHub Pages caches for minutes) | review (risk, not observed) | precache requests use `cache: "no-cache"` | update test lands on B's content |
| 9 | Material's coloured admonitions (cyan, green) broke the one-accent rule; its border rule beat mine | screenshot | unified callouts with a 3 px left rule, `!important` borders | screenshots |
| 10 | Prototype still had XP, ranks, badges, two accents | blueprint §0 | removed; `progress/`; amber only | grep: no XP/badge words in the prototype |
| 11 | Test server (Python `http.server`) hung 4-17% of Chrome requests, causing false failures and the "connection resets" | `hammer` comparison | tests use `tools/serve.mjs` (Node) | 240/240 OK |

Test-harness mistakes (mine, not the site's), each caught and fixed:
- a fixed 4 s wait for the worker was too short;
- the demo was checked on the wrong page;
- Git Bash rewrote `--asset=/assets/...` into a Windows path (`MSYS_NO_PATHCONV=1` fixes it, but then `/d/...` paths and `curl -o /dev/null` break, so both had to change);
- rebuilding under a running server stranded it;
- a reused browser profile served the old build.

---

## What the blueprint still replaces later

| Prototype now | Blueprint target | Status |
|---|---|---|
| `hooks.py` (validate data, expand `<!-- ss:… -->` and `{{claim:ID}}`, write `sw.js`, budget check) | `tools/build_book.py` + `tools/make_sw.py` + `tools/check_site.py`, JSON Schemas | **later step** (logic is small and self-checked; moving it is mechanical) |
| `data/claims.csv` (8 real claims) + claims register page + chips | one merged `claims.csv` for all waves, with an old-ID → new-ID map (blueprint addition 1) | chip and register mechanics done; the merge is later |
| `sw-template.js`: 3 caches, batched install, image cap, tap-to-update | same (§6) | **done** in the prototype |
| `overrides/main.html`: noindex meta | `public: false` switch in `book/config.yml` that also drops the sitemap | noindex done; switch later |
| `deploy-book.yml` | `book.yml` with the extra check scripts, ntfy on failure, `publish.ps1` | later |
| `demos.js` loaded on every page (1.5 KB) | loaded only on its own page | **not done**; see conflict 10 |

---

## Blueprint conflicts (my research vs SITE-BLUEPRINT.md; blueprint not edited)

1. **robots.txt (§0.3, marked LIKELY):** **VERIFIED** (RFC 9309 §2.3 + Google's noindex docs; B5, B6).
2. **Build time (§1, §7, "2 s"):** measured **0.50 s** (1.1 s wall) now, and **3.2-3.6 s at 300 extra pages**.
3. **Precache size (§0.7, "2.7 MB"):** now **0.56 MB / 32 entries**; at 300 long pages **14.1 MB**. The **search index is the big item** (4.1 MB at 300 pages), so the 25 MB budget could be reached at roughly 500+ long pages. Watch the search index size, not just images.
4. **Candidate statuses (§3), scoop switch "at CTOI time" (§11, addition 3):** ExoFOP has been **publish-first since 2026-08-19** (B9, B10). Statuses should be *Under vetting → Passed both keys → Write-up submitted → Published → On ExoFOP → TOI / Rejected*, and the scoop switch should flip at write-up submission.
5. **Mermaid/maths from a CDN (§0.6):** measured. With neither extension configured, the built HTML makes **no external requests** (B20).
6. **Deploy concurrency (§7.5, `cancel-in-progress: true`):** GitHub's Pages starter uses `false` so a started deployment finishes (UNVERIFIED, B22).
7. **Action versions (§7):** checkout v7, setup-python v7, configure-pages v6, upload-pages-artifact v5, deploy-pages v5 (B7).
8. **"Level 2 of 6" vs seven levels L0-L6:** resolved as an uncounted L0 warm-up ("Level n of 6").
9. **Contrast table (§4), light `--text-3`:** the blueprint says it fails on `--raised` (4.2). Measured: light `--text-3` is **4.84 on `--raised` (#fff)** but **4.21 on `--surface`**. The light-scheme surface and raised values look swapped in that note. Same rule either way: `--text-3` only for captions on `--bg`.
10. **Demos loaded per page (§8):** not done. Material's instant navigation may not run scripts placed in page content (UNVERIFIED). Test that before moving the 1.5 KB demo script off the global list.
11. **Testing (§10 step 8):** the Claude Browser pane **can't register service workers**, and Python's dev server is unreliable with Chrome on this PC (bug 11). Offline and update tests need headless Chrome + `serve.mjs` (`tools/site_check.mjs`), plus the phone.
12. **Version hash (§5, `make_sw.py`):** hash the shell files, not `sw.js`. A logic-only change to the worker still triggers an update, because browsers compare `sw.js` bytes. Tested: the update flow works with an unchanged shell version.
13. **Multi-tab updates (§6, not covered):** if Ahmed taps Reload in one tab, other open tabs get the "Updated. Reload" line instead of a forced reload. That's implemented and part of the no-loop guard (but only single-tab was tested).

---

## 1. Prototype reference (`site-proto/`)

| File | Job |
|---|---|
| `mkdocs.yml` | Material 9.7.7, `custom_dir: overrides`, `font: false`, slate default + light toggle, `hooks: [hooks.py]`, `watch:` for data folders, `navigation.instant` |
| `docs/assets/extra.css` | blueprint tokens + type scale, callouts, confidence chips, quiet progress, cards, tables in their own scroll box, demo + fallback, update line, 44 px tap targets, transitions, reduced-motion switch-off |
| `docs/assets/book.js` | sets `ss-ready` after first paint; registers the worker; shows "Updated. Reload"; loop guards |
| `sw-template.js` | 3-cache worker (shell batches, capped image cache, tap-to-update, one-redirect pretty URLs, 404 fallbacks) |
| `hooks.py` | validates `progress/*.yml` and `data/claims.csv` (bad data fails the build), expands placeholders and `{{claim:ID}}` chips (unknown ID fails the build), writes `sw.js`, enforces the 25 MB budget; `python hooks.py` = self-check |
| `progress/levels.yml`, `milestones.yml`, `quests.yml`, `candidates.yml` | Ahmed's progress (real events only; SS-0000 is a flagged layout example) |
| `data/claims.csv` | 8 real claims from this burn, labelled |
| `docs/claims.md`, `docs/book/credit-and-publishing.md`, `docs/glossary.md` | claims register, a sample chapter in the blueprint's chapter template, glossary |
| `docs/learn/l1-dip-depth.md` | lesson in the blueprint's lesson template, with the demo and its no-JS figure |
| `overrides/main.html` | noindex meta, manifest, icons, the `book.js` tag |
| `.github/workflows/deploy-book.yml` | Pages deploy (written, **not enabled**) |

Offline on iPhone: **UNVERIFIED** until the blueprint §6 checklist is run on Ahmed's phone after a deploy (B4).

## 2. Learning track
See `learning-track.md`.

## 3. Submission and journal rules

### 3.1 ExoFOP candidate upload (B9-B13, VERIFIED, ExoFOP help and news pages, fetched 2026-10-19)
- **Timeline:** on 2026-03-31, new candidate uploads were "temporarily paused". On 2026-08-19 they reopened: "candidates must first be published in a peer-reviewed journal with online access before being uploaded", and "approval to upload candidates is required".
- **Who can submit:** a logged-in ExoFOP user with an approved **Published Candidate Upload Request** (that form needs a login, so its fields are unknown). "You must have an account and be logged in to enter or update data."
- **RNAAS route:** allowed "if the methodology to detect and vet the candidate has been previously published in a peer-reviewed journal" and is cited.
- **Fields:**

| Field | Required? |
|---|---|
| TIC.nn name (next in sequence) | required |
| Discovery source (TESS default) | required |
| Candidate name (no 'b'/'c' until confirmed) | optional |
| Disposition PC/FP | optional |
| Period (d), transit midpoint (BJD), depth (ppm), with errors | ≥ 2 of 3, > 0 |
| + duration, for cTOI consideration by the TOI working group | all 4 > 0 |
| Data tag | required |
| Paper URL | required |
| Initial note | required |

- **Evidence:** supporting material (e.g. the light curve with the fitted transit) uploaded with the same tag, or "candidates may be removed". Cross-check against candidates, TOIs and confirmed planets first; a period that's an integer multiple of a known one goes in as an extra parameter set; duplicates risk account suspension. Contact: exofop-support@ipac.caltech.edu (Ahmed's call).
- **Single-dip circumbinary candidates:** epoch + depth can create a candidate; a cTOI needs all four values.
- **Updates wave 5 claim K1:** the 2021 route predates these rules.

### 3.2 MNRAS (B14-B16, VERIFIED, OUP "General instructions")
- AI tools "do not qualify as authors". Use (content or images, **code, data processing**, translation) is "disclosed both in cover letters to Editors and in the Methods or Acknowledgements section"; authors stay fully responsible.
- "No restrictions based on nationality, institutional affiliation, qualifications"; each author gives a full address.
- APC **£2,356** (papers), **£1,122** (letters), 20% off for RAS members. Low/middle-income country waivers; discretionary waivers requested separately from review. Kuwait is high-income, so the country waiver likely doesn't apply (LIKELY).

### 3.3 A&A (B17-B18, LIKELY: aanda.org returns 403 to our tools)
- AI statement of 18 June 2026: no AI authors or citations; language, **coding** and search help under human oversight needs **no disclosure**; other uses are declared at submission.
- Subscribe-to-Open. Sponsoring-country authors pay no page charges; others do; pages beyond 30 cost extra since 2025. Amounts and the country list are unconfirmed (Kuwait probably non-sponsoring, UNVERIFIED). Independent-author rules: not found.

### 3.4 Disclosure line
The wave 5 template line ("Pipeline code, data retrieval and preliminary analysis were developed with Claude Code … under the direction of the author") satisfies AAS and MNRAS (cover letter **and** Methods/Acknowledgements) and goes beyond A&A. Use it on the blueprint's *Credit and AI use* page.
