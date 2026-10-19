# Second Sun book: site blueprint

*Planning only, no code. Written 2026-10-20 by Claude (Opus 5.5) for Ahmed Hanzala, for the Claude Code session that builds the site. Read with `D:\second-sun\RESEARCH-PLAN.md` (section 2), `research\wave-9-tech\report.md` and `research\burn-3-book\`. Nothing in `D:\second-sun` was edited.*

> **Status: ADOPTED 2026-10-19 21:14 UTC** by Ahmed as the plan for the book, with three additions (below). Building has NOT started; it waits for Ahmed's go.
>
> **Additions:**
> 1. **One claim-ID scheme.** The wave registers use per-wave prefixes (A, B, C, D, P, V, Q, R, A7-...). When content moves into the book, merge them into one `claims.csv` with one ID format and keep an old-ID to new-ID map.
> 2. **Two more pages:** *Side wins* (AAVSO VSX submissions, under The Hunt) and *Credit and AI use* (credit line "Ahmed Hanzala, independent citizen scientist (Pakistan), based in Kuwait", ORCID 0009-0009-1075-2365, exactly how Claude was used; under Reference).
> 3. **Scooping:** keep the existing rule (Claude flags the risk once, when the first real candidate appears). Build the switch from section 11 now: candidate data can stay local, off GitHub, until both keys pass, so that decision is a one-line flip.

Confidence labels below follow the project's rules: **VERIFIED** (read in a primary source or measured), **LIKELY** (secondary source or reasoned from documented behaviour), **UNVERIFIED** (memory; test before relying on it).

---

## 0. Assumptions I'm challenging first

1. **The learning track still has XP, ranks and badges** (`learning-track.md`, `game/xp.yml`, `hooks.py`). That contradicts the locked rule from 2026-10-19 20:59 UTC: no XP banners or badges. **Drop XP, ranks and badges entirely.** Keep levels L0 to L6, a milestones page and one quiet progress line. Rename `game/` to `progress/` so the word stops pulling the design back.
2. **"noindex" does not hide the project.** The repo is public on github.com, and GitHub pages for repos are indexable whatever the site says. Free GitHub Pages also needs a public repo (Pages from a private repo needs a paid plan: LIKELY). So with a zero budget, **everything you push is effectively public from day one.** noindex only keeps the *book site* out of search results. The scooping risk is the repo, not the site. Decide that knowingly now, not at the first candidate.
3. **robots.txt cannot work on a project site.** `m1smacker.github.io/second-sun/robots.txt` is ignored; only `m1smacker.github.io/robots.txt` counts (the prototype already noted this). The switch is the `<meta name="robots" content="noindex">` tag only. LIKELY.
4. **"Every claim carries a source and confidence label" will drift if labels are hand-typed in pages.** Make claims data: every claim lives once in `claims.csv` with an ID, and pages reference the ID. The build renders the label, the source and the date, so the label can never disagree with the register.
5. **The prototype has two accents** (blue links and amber). The brief says one. **Amber is the accent**; links use the accent plus an underline; blue goes.
6. **Mermaid diagrams and maths break offline by default.** Material loads Mermaid, and usually MathJax or KaTeX, from a CDN (LIKELY). On an iPhone in airplane mode those diagrams and formulas vanish. **Pre-render diagrams to SVG at build time, and self-host KaTeX**, or keep formulas as plain text (the learning track's maths is simple enough for that).
7. **The prototype's service worker caches every file at install.** That's fine at 2.7 MB but breaks as vetting-sheet images pile up, and `cache.addAll` is all-or-nothing: one failed file means no offline at all. See section 6.

---

## 1. Stack recommendation

**Decision: stay on Material for MkDocs 9.7.7 (pinned) now, but make the engine replaceable.** Move all custom logic out of `hooks.py` into plain Python scripts that run *before* and *after* the engine. The engine then only turns finished Markdown into HTML, so switching to Zensical, or to anything else, means changing one config file and one command.

Why:
- It works on your PC today: a 2 s build, measured in wave 9 (VERIFIED).
- Your pipeline is Python, so one language and one toolchain for Claude to maintain.
- Critical fixes continue until 2027-05-05, and it already blocks MkDocs 2.0 by itself (VERIFIED, wave 9 T1 to T3).
- **Zensical does not run `hooks.py`**: its compatibility docs say configuration for unsupported plugins is silently ignored, and migrators replace hooks with pre-build scripts ([Zensical plugin compatibility](https://zensical.org/docs/compatibility/mkdocs/plugins/), [example migration](https://github.com/sentenz/skills/pull/136), LIKELY). If the logic stays in a hook, migration later means a rewrite. Put it in scripts, and migration is a config change.

| Option | What you'd gain | What you'd lose |
|---|---|---|
| **Material 9.7.7 (recommended now)** | Proven here, offline search built in (lunr index is a file), light/dark toggle, admonitions, tabs, instant navigation, 2 s builds | It ends in May 2027; no new features |
| **Zensical now** | The successor; same config file | Pre-1.0 (0.0.71, releases every few days), no hooks, plugin gaps (VERIFIED/LIKELY above). Too early to bet the book on |
| **Astro Starlight** | Excellent docs framework, Pagefind search (works offline as static files), per-page islands for demos, strong right-to-left support for the future Urdu version | A second toolchain (Node) beside Python; Claude rewrites every template and component; lose Material's polish you already tuned |
| **Plain Astro or custom** | Total control | You build search, navigation, theming and accessibility from scratch. Busywork, with no gain for a book |

**Review gate:** in Feb 2027, or when Zensical reaches 1.0, whichever comes first. If Zensical has stalled, move to Starlight instead. Because the content is plain Markdown plus our own scripts, either move costs days, not weeks.

---

## 2. Information architecture

Top tabs on PC; on iPhone they fold into the drawer (Material does this).

| Tab | Pages |
|---|---|
| **Home** | (see below) |
| **Start here** | Where we left off (2-min recap) · How to read this book · About the project · About Ahmed |
| **Learn** | Track overview (levels L0 to L6, quiet progress) · one page per level · Refresher quizzes · Milestones |
| **The Hunt** | Quests (main, training, side) · Candidates (index + one page each) · Sky coverage · Batches · Cool finds |
| **Book** | Chapters (Science, Data, Pipeline, Vetting, Credit and publishing, Anomalies, How this project runs) |
| **Records** | Decision log · Mistakes register · Prediction scoreboard · What changed · Journal |
| **Reference** | Glossary · Claims register · Sources · Index · Licences and credits |

**Home page, in order** (it's a dashboard for you, not a marketing page):
1. **Where we left off**: three lines (last session, next step, anything waiting on Ahmed), with a link to the full recap.
2. **Next for you**: one action, sized to a weeknight burst (for example "L3, 25 min").
3. **Quiet progress line**: "Level 2 of 6 · 3 of 12 milestones · 41 stars searched".
4. **Since your last visit**: the latest 5 entries from What changed.
5. **Candidates**: the newest 3 cards, or "No candidates yet."
6. Links to the Glossary and the Journal.

Personal voice: every page is written to you ("Ahmed, this is where…"). When the book goes public, the About page explains that voice: it's a working notebook between you and Claude, kept in the open.

---

## 3. Page templates (top to bottom)

Every page starts with an **In plain words** box (2 to 4 sentences) and ends with **Sources** for its claims. Technical terms link to the glossary on first use (automatic, section 5).

**Chapter**
1. Title + one-line "what this chapter answers".
2. In plain words.
3. "You need first" (links to levels or chapters), only if needed.
4. Body in short sections, each with its claims inline as chips.
5. Figure(s) with numbered captions.
6. "What this means for our hunt" (the practical bit).
7. Open questions (what we don't know yet).
8. Sources (generated from the claim IDs used on the page) · Last reviewed date.

**Lesson + quiz** (one per level, 600 to 1,200 words, one burst)
1. Header strip: level, time (for example 20 min), maths it rebuilds.
2. In plain words.
3. Lesson.
4. One demo, if any (works with JavaScript off: a static figure shows instead).
5. Exercise box: the file, the command Claude prepared, the one thing to write down.
6. Quiz: 3 questions, answers in collapsible boxes, self-marked, no JavaScript.
7. Done line: "When you're done, tell Claude: L2 done, 3/3." Claude records it in `progress/levels.yml`.
8. Next level link.

**Candidate (SS-0001 "nickname")**
1. ID, nickname and a status chip (Under vetting / Passed both keys / CTOI submitted / TOI / Rejected).
2. Two keys: Claude's key (pass/fail + date), Ahmed's key (pass/fail + date).
3. In plain words: what we think it is and how sure we are.
4. **Vetting sheet image** at phone width (generated by the pipeline), with full alt text from the data.
5. Facts table: TIC, coordinates, magnitude, sectors, period or single-event times, depth, duration, SNR. Every number comes from `candidates.json`, never typed by hand.
6. Tests C1 to C11: a pass/fail table with the threshold for each.
7. Story: how we found it (prose, the journal link).
8. Fakes we ruled out and how.
9. Next step and who holds it.
10. Sources + history (status changes with dates).

**Log pages** (decisions, mistakes, predictions, what changed): one shared shape. Newest first; each entry has date, ID, a one-line summary and a details box. Filters are plain anchors (by quest, by phase), no JavaScript.
- Decision: what, why, alternatives, who decided, superseded-by link.
- Mistake: what happened, cost, rule we added, where the rule now lives.
- Prediction: what Claude predicted, confidence %, date, resolution date, outcome. The page header shows the calibration (Brier score, plus a "when I said 80%, I was right X% of the time" table), computed at build.

**Recap ("where we left off")**: written by Claude at the end of every session into `progress/recap.yml`. Two minutes of reading: last session in 3 bullets, what we learned, the next step, decisions waiting for you, blockers, plus a refresher quiz link if it's been 14 or more days.

**Journal**: dated entries, one file per entry, in the same light story voice. The index is generated (no blog plugin, because Zensical's blog support is uncertain: UNVERIFIED).

---

## 4. Design system

**Principles:** a textbook at night. Calm surfaces, strong reading type, one accent, nothing that glows or animates for decoration. Mobile first: design at 390 px wide, then let it breathe on PC.

**Type** (system fonts: nothing to download, instant, offline; the prototype already does this)
- Text: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. Mono for IDs and data: `ui-monospace, "Cascadia Mono", Consolas, monospace`, with tabular numbers.
- Scale (ratio 1.25), phone / PC: caption 13/14 · body 17/18 · h4 19/20 · h3 21/23 · h2 26/29 · h1 32/38. Line height 1.65 for body, 1.25 for headings. Measure 66 characters max.
- Arabic or Urdu later: add `"Noto Naskh Arabic"` self-hosted only when that version starts.

**Palette tokens (measured contrast, WCAG formula)**

| Token | Dark (default) | Light | Use |
|---|---|---|---|
| `--bg` | #0c1018 | #faf9f6 | page |
| `--surface` | #131a27 | #f1efe9 | callouts, cards, code |
| `--raised` | #1a2233 | #ffffff | demo panels, tables header |
| `--line` | #2a3448 | #d9d5cb | dividers only (1.3 to 1.5:1, decorative) |
| `--text` | #e6e8ee | #1a1e26 | body: 13.0 to 15.5:1 dark, 14.5 to 16.7:1 light |
| `--text-2` | #aab1c0 | #495160 | secondary text: 7.4 to 8.9:1 / 7.0 to 8.0:1 |
| `--text-3` | #7d8597 | #6a7282 | captions **on `--bg` only** (5.1:1 / 4.6:1); fails 4.5:1 on `--raised` (4.3 / 4.2), so never there |
| `--accent` | #e2b45f (starlight amber) | #8a5a12 | links (with underline), focus ring, progress line, the one highlight: 8.3 to 9.9:1 / 5.1 to 5.9:1 |
| `--on-accent` | #0c1018 | #ffffff | text on an accent fill (9.9:1 dark) |

Input and control borders use `--text-3`, not `--line`, to reach 3:1 for UI boundaries. Recheck every pair with `research/burn-3-book/contrast_check.py` after any change.

**Spacing:** 4 px base: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64. Sections 48 apart on phone, 64 on PC. Radius 6 px on callouts and figures only.

**Components**
- **Callouts** (Material admonitions, restyled): `plain` (In plain words), `note`, `warning`, `exercise`, `quiz`. A 3 px left rule plus a label; no coloured backgrounds except `--surface`.
- **Confidence label chip**: the text is always spelled out, and shape carries the meaning, not colour (no red, yellow or green): **VERIFIED** solid outline with a check mark · **LIKELY** dashed outline · **UNVERIFIED** dotted outline in `--text-3`. Hover or tap shows the source, the read depth and the checked date.
- **Source citation**: a numbered superscript linking to the page's Sources list. That list uses DOI or arXiv ID first and the URL second (IDs survive link rot).
- **Figure + caption**: "Figure 3.2", then one plain sentence saying what to look at, then the credit (for example "Data: NASA TESS via MAST").
- **Data table**: tabular numbers, right-aligned numerals, a sticky first column on phones, horizontal scroll inside its own box, never the page.
- **Progress indicator**: one thin line plus text ("Level 2 of 6"), `role="progressbar"` with values. No percentages shouting, no banners.
- **Candidate card**: mono ID, nickname, status chip, two key chips, one line of facts.
- **Status chips** (candidates): text + outline style, same rule as confidence (no traffic-light colours).

**Mobile-first rules:** 16 px side gutter; tap targets 44 px; tables and figures never widen the page; demo controls are full-width sliders; no hover-only information (every tooltip also works on tap); images `max-width: 100%` with `width` and `height` set.

---

## 5. Data flow

```
pipeline (D:\second-sun\pipeline, Python 3.12)
   writes  results\*.csv / *.json            (full, private-ish working data)
      │
tools\export_book_data.py   (copies the PUBLISHABLE subset, strips paths/keys)
      ▼
book\data\                  candidates.json  coverage.csv  predictions.csv
                            claims.csv  sources.csv  decisions.yml  mistakes.yml
                            progress\levels.yml  milestones.yml  recap.yml  changes.yml
      │
tools\build_book.py         1. validate every data file against schemas\ (fail = stop)
                            2. expand book\src\*.md into book\docs\ (git-ignored):
                               {{claim:C-0042}}        → confidence chip + footnote
                               {{table:predictions}}   → HTML table + calibration
                               {{candidate:SS-0001}}   → facts table, tests, keys
                               {{figure:coverage}}     → the generated SVG
                               glossary terms          → first-use link + tooltip
                            3. generate pages: candidate pages, log pages, journal index,
                               Sources per page, claims register, glossary, index
                            4. draw SVGs: sky-coverage map, scoreboard calibration chart
      ▼
mkdocs build --strict       (the engine sees only finished Markdown/HTML)
      ▼
tools\make_sw.py            writes sw.js with the precache list + version hash
      ▼
tools\check_site.py         dashes, noindex flag, size budget, broken images, no secrets
```

- **Why expand `src/` into `docs/`** instead of a hook or macros plugin: it works with any engine, it's testable on its own (`python tools/build_book.py --check`), and a bad CSV fails the build before anything deploys. `docs/` is git-ignored and every generated file starts with a "generated, edit book/src" comment, so nobody edits the wrong copy.
- **Sky-coverage map:** a static SVG drawn in Python (an equirectangular or Mollweide sky; one point per star coloured by status: searched / pending / candidate) plus a per-sector table. No mapping library. An optional tiny script adds tap-to-identify. Plotly (about 3.5 MB) is out.
- **Scoreboard:** `predictions.csv` → a table plus a Brier score and a calibration chart, computed at build, so the honesty is automatic.
- **Schemas:** JSON Schema files in `schemas/`, validated with the `jsonschema` package. Every schema is documented in `schemas/README.md`, which is what makes the project portable to another person or AI.

---

## 6. Offline on iPhone

**What WebKit documents:** the first-party domain of a home-screen web app is exempt from Safari's 7-day storage cap, and its data is kept separate from Safari ([WebKit Tracking Prevention](https://webkit.org/tracking-prevention/), VERIFIED as WebKit's own statement; still to be **tested on your phone**). Quotas are a share of disk, and data can still be evicted under storage pressure, least recently used first (secondary sources, LIKELY). Some 2026 guides claim a 50 MB cache cap and others deny it: UNVERIFIED, so design to stay well under it anyway.

**Strategy**
1. Install it as a home-screen app (Share → Add to Home Screen), and read it from there, not from a Safari tab.
2. `manifest.webmanifest` + icons + `display: standalone` + dark theme colour (prototype has these).
3. **Service worker, three caches:**
   - *Shell* (precached at install): CSS, JS, fonts if any, icons, the search index, the 404 page, and **every HTML page** (text is small: hundreds of pages are a few MB).
   - *Images* (runtime): cached the first time you view them (cache-first), capped at about 150 entries with oldest removed first. Vetting sheets you've opened stay offline.
   - *Install resilience*: precache in small batches and skip individual failures, so one bad file never kills offline mode (the prototype's single `addAll` does).
4. **Updates:** a new deploy changes the version hash. The new worker installs in the background, and the page shows a quiet "Updated. Reload" line. No forced reloads mid-read.
5. **Budget:** the whole precache stays under 25 MB. `check_site.py` fails the build over budget.
6. Material's `navigation.instant` fetches pages with JavaScript; the service worker serves those requests from cache too. Test both instant on and off on the phone before deciding.

**Limits to accept:** iOS updates the worker only when the app is opened online; no background sync or downloads; if iOS clears storage under pressure, the next online open re-caches everything. Nothing the site can do changes those.

**Test checklist (on Ahmed's iPhone, after the first deploy):** add to home screen → open 5 pages and 2 candidates → airplane mode → force-quit → reopen → all 5 pages, both sheets, search and one demo work → the 404 page shows for an unvisited image → turn data back on → deploy a change → reopen → "Updated" appears.

---

## 7. Build and deploy

**GitHub Actions** (`.github/workflows/book.yml`), on push to `main` touching `book/**`, `tools/**`, `schemas/**`:
1. Checkout; `actions/setup-python` with Python 3.12 and a pip cache.
2. `pip install -r requirements-docs.txt` (exact pins, with hashes).
3. `python tools/build_book.py` (validate + generate) → `mkdocs build --strict` → `python tools/make_sw.py` → `python tools/check_site.py`.
4. `actions/upload-pages-artifact` → `actions/deploy-pages`.
5. `concurrency: { group: pages, cancel-in-progress: true }`, so rapid auto-pushes don't queue up.
6. On failure, post to your ntfy topic (topic name stored as a repo secret).

**Build time:** about 1 minute in Actions (LIKELY: the local build is 2 s, measured; the rest is setup and install, with cache). Measure it on the first run and log it.

**Why auto-push stays safe:**
- A failing check stops the deploy, and **the last good site stays live**: Pages only switches when `deploy-pages` succeeds.
- Claude pushes through one script (`tools/publish.ps1`) that runs the same build locally first. It refuses to push if:
  - the build fails
  - a secret pattern is found (the ADS key format, `ntfy` topic, anything from `.env`)
  - a file over 5 MB is staged
  - anything under `data/` is staged
- Never `--force`. One commit per session or batch, not per file, to stay well inside Pages' soft build limits.
- Secret scanning is also turned on in the GitHub repo settings (free for public repos: LIKELY).

**The public switch:** one line in `book/config.yml`: `public: false`. While false, the build adds the noindex meta and leaves out the sitemap. Flipping it adds the sitemap, canonical URLs and social cards. Rehearse the flip once on a branch build before you need it.

---

## 8. Demos

- **Vanilla JavaScript + SVG or canvas.** No frameworks and no chart libraries. Each demo is at most 15 KB, lives in `book/src/assets/demos/<name>.js` and is loaded **only on its own page** (a `<script>` tag in that page's Markdown), so the rest of the site carries nothing.
- Progressive enhancement: the page includes a static SVG of the demo's key frame; the script replaces it with the live version. JavaScript off, or offline before the script was cached, still reads correctly.
- Keyboard-operable sliders (native `<input type="range">`), visible values, and `prefers-reduced-motion` respected (animations pause and show a Step button).
- Planned and worth it: **transit depth** (built, L1), **binning and noise** (L3), **circumbinary orbit and wandering transits** (L4, the one that explains the main quest), **phase folding** (later).
- Not worth it: 3D globes, live data fetched from MAST in the browser, anything that needs a server.

---

## 9. Accessibility and performance targets

**Accessibility (WCAG 2.2 AA):** contrast as measured above; visible focus ring (`--accent`, 2 px plus offset); one `h1` per page; real headings in order; every figure has alt text, and vetting sheets have a long description generated from the data; confidence and status never shown by colour alone; quizzes use `details`/`summary` (works with screen readers and with JavaScript off); demos labelled, keyboard-operable, and respect reduced motion; tap targets 44 px; zoom to 200% without horizontal scroll.

**Performance:**
- Any page: under 300 KB transferred on first visit, excluding its figures; HTML + CSS + JS for a normal page under 150 KB.
- Largest content shown in under 2.0 s on a mid iPhone over 4G; repeat visits instant from cache.
- Demo script ≤ 15 KB each; vetting sheet images ≤ 200 KB (WebP or optimised PNG at 1170 px wide, for 390 px at 3×).
- Precache total ≤ 25 MB (enforced by `check_site.py`).

---

## 10. Phased build plan

Each step ends with a check you can see.

| # | Step | Done when |
|---|---|---|
| 1 | Repo layout (`book/src`, `book/data`, `schemas`, `tools`), pinned requirements, LICENSE (MIT) + LICENSE-TEXT (CC BY 4.0), README "how to continue", repo `CLAUDE.md` | A fresh clone builds with one command |
| 2 | Actions deploy of a one-page site with the noindex switch | The live URL loads; view-source shows the noindex meta |
| 3 | Design tokens + typography + light/dark toggle | Contrast script passes; screenshots at 390 and 1280 px |
| 4 | `build_book.py`: validators + `src → docs` expansion + glossary auto-links + claim chips | `--check` fails on a bad CSV in a test; a page shows chips from `claims.csv` |
| 5 | Templates: chapter, lesson + quiz, log pages, recap, home | Each template filled with one real page from the research waves |
| 6 | Data pages: candidates (the SS-0000 practice card), scoreboard + calibration, decisions, mistakes, what changed | Editing a CSV changes the page; a schema error blocks the deploy |
| 7 | Sky-coverage SVG from `coverage.csv` | Matches a hand count of 10 stars |
| 8 | Offline: manifest + service worker + update line + budget check | The iPhone airplane-mode checklist (section 6) passes on your phone |
| 9 | Demos: binning (L3), circumbinary orbit (L4) | ≤ 15 KB each, keyboard test, no-JS fallback visible |
| 10 | Move the research waves' content into chapters; the claims register goes live | Every chapter has In plain words + Sources; zero unlabelled claims (the build checks this) |
| 11 | Public-switch rehearsal on a branch | The flipped build has a sitemap and no noindex; `main` unchanged |
| 12 | Engine review (Feb 2027 or Zensical 1.0) | A written yes/no, with a test build on the new engine |

**Do not build:** XP, ranks, badges or streaks; comments; accounts or logins; analytics; a database or server; automatic quiz scoring with stored state (self-marking is honest and offline); Plotly or other heavy chart libraries; a 3D sky; the Material blog plugin; translations (Urdu comes later, as its own phase); a PDF export; live archive queries in the browser; push notifications from the site (ntfy already does that).

---

## 11. Risks and how this ages over 2 to 3 years

| Risk | Likelihood | Guard |
|---|---|---|
| Material reaches end of maintenance (May 2027) | Certain | Engine-agnostic build (section 1); review gate Feb 2027 |
| Zensical stalls or changes direction | Possible | Starlight as the fallback; content is plain Markdown + data, so either move is days |
| iOS changes home-screen web app rules (Apple tried removing them in the EU in 2024, then reversed: UNVERIFIED memory) | Possible | Offline is a convenience, not the only copy; the book is readable online and from the repo |
| The public repo exposes candidates before submission (scooping) | Real, from day one | Decide now (section 0.2). If needed later: keep candidate *data* local until both keys turn, publish the page at CTOI time |
| Repo bloat from images | Likely by year 2 | Image budget per sheet; no raw data in git (already `.gitignore`d); review repo size every phase review |
| Claim register drifts from pages | Likely without tooling | Claims are IDs resolved at build; the build fails on unknown IDs and lists unlabelled numbers |
| Source links rot | Certain over years | Store DOI/arXiv IDs; URLs are second |
| GitHub free terms change (Pages, Actions minutes) | Low | Output is a plain static folder; any free static host (Cloudflare Pages, Netlify free) takes it unchanged |
| Python or package churn | Certain | Pin Python 3.12 and every package with hashes; a yearly bump on purpose, not by accident |
| A broken auto-push takes the site down | Low | Strict build + checks; failed builds never deploy; the last good site stays live |
| The personal voice reads as unserious to astronomers when public | Moderate | The About page explains the notebook format; science pages keep the plain-words-then-detail structure with sources on every claim, which is what credibility rests on |

---

## Open items I could not settle

- The real iOS cache limit for home-screen apps (sources conflict). **Test on the phone.**
- Whether Material 9.7.7 loads Mermaid and maths from a CDN in this exact setup. Check the built HTML once and self-host whatever it pulls in. LIKELY yes.
- Actions build time and Pages limits for this repo: measure on the first deploys.
- Whether Zensical will support build hooks before 1.0: the roadmap mentions replacements for popular plugins, nothing specific on hooks ([roadmap](https://zensical.org/roadmap/)).

Sources used today: [Zensical plugin compatibility](https://zensical.org/docs/compatibility/mkdocs/plugins/) · [Zensical roadmap](https://zensical.org/roadmap/) · [sentenz/skills PR #136 (hooks replaced by a pre-build script)](https://github.com/sentenz/skills/pull/136) · [Material blog: what MkDocs 2.0 means](https://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/) · [WebKit Tracking Prevention](https://webkit.org/tracking-prevention/) · [Synthetixis: PWAs on iPhone in 2026](https://synthetixis.com/writing/pwa-ios-2026) · wave 9 report (`D:\second-sun\research\wave-9-tech\report.md`).
