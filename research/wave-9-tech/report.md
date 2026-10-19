# Wave 9: book and infrastructure tech (PARTIAL)

*Second Sun research, wave 9. Run inline by the main session (Claude, Opus 5.5) on 2026-10-19 from 17:34 UTC. Claims T1… in `claims.md`.*

---

## In plain words (read this first)

**The book engine works on your PC.** We built a tiny test version of the book with **Material for MkDocs 9.7.7**: dark "slate" theme, search, notes boxes. It took 60 seconds to install and 2 seconds to build (T4).

**But that engine is being retired, slowly.**
- Its makers put it into maintenance mode in **Nov 2025**.
- It **won't work with the coming MkDocs 2.0**, though it already blocks 2.0 automatically, so nothing breaks by surprise.
- They'll keep fixing critical problems **until 5 May 2027**.
- Its successor, **Zensical**, reads the same settings file, but is still a young version 0.0.71 (T1-T3).

**Plan: build on Material now, and move to Zensical before May 2027**, ideally once it hits version 1.0. Moving should be cheap because our content is plain markdown.

**Phone alerts: ntfy.** There's a free iPhone app, no account, and messages arrive through the free ntfy.sh server. Topic names are public, so we use a long random topic name. That's fine because our alerts are things like "batch 4 done" (T5).

**Offline reading on iPhone** needs a small hand-written "service worker" file. No ready-made plugin exists on PyPI under the obvious names (T6). It's a normal, well-understood web technique; we'll build and test it with the book.

---

## 1. Engine decision (T1-T4)

| Option | Status (2026-10-19) | Verdict |
|---|---|---|
| **Material for MkDocs 9.7.7** + MkDocs 1.6.1 | maintenance mode since 2025-11-05; last release 2026-07-17; incompatible with MkDocs 2.0 (auto-pinned `mkdocs<2` since 9.7.5); critical maintenance **until 2027-05-05** | **Use now, with pinned versions** |
| **Zensical** 0.0.71 | released 2026-10-16; 71 releases since 2024-11-25 (every few days); "drop-in replacement for MkDocs 1.x", "not fully there yet" (plugins) | **Migrate later**: schedule a review by Feb 2027 |
| MkDocs 2.0 | pre-release (2.0.dev6, 2026-09-15) | avoid |

Pins for `requirements-docs.txt`: `mkdocs>=1.6,<2` and `mkdocs-material==9.7.7`.

## 2. Hands-on test (T4)
`D:\second-sun\.venv-docs`; test site in `research\wave-9-tech\site-test\`.
- Theme `material`, palette `slate` (dark), `navigation.instant`, `search`, and the built-in `offline` plugin.
- The `offline` plugin is for opening the site from files on disk; it is **not** an iPhone app cache.
- Build: 2 s, output 2.6 MB. It works.

## 3. iPhone offline / home screen (T6, design)
- Needs: `manifest.webmanifest` (name, icons, `display: standalone`, dark colours) plus a `sw.js` service worker that caches the site's pages and assets, registered from `extra_javascript`, with the manifest link added through a theme override (`overrides/main.html`).
- No PyPI plugin found under `mkdocs-pwa`, `mkdocs-material-pwa` or `mkdocs-offline-pwa`.
- `navigation.instant` (single-page navigation) needs care with service-worker caching; test both.
- iOS behaviour (UNVERIFIED, from memory): home-screen web apps keep their storage, while Safari tabs may lose it after 7 days of non-use. **Test on Ahmed's iPhone** after the first deploy.

## 4. Phone alerts (T5)
- **ntfy:** free iPhone app; publish with a plain HTTP POST to `https://ntfy.sh/<topic>`. iPhone pushes go through the ntfy.sh relay.
- Free tier: rate-limited; messages cached ~12 h.
- **Topic names are public**: use a long random topic, never anything personal.
- Self-hosting can't push to iPhone on its own (the Apple certificate belongs to the ntfy.sh project; LIKELY, secondary sources).
- Plan: the batch runner posts "big find / batch done / problem / decision waiting" messages, as agreed in round 24.

## Not done (carry over)
- Gamification on a static site (XP, levels, achievements, sky map, quizzes): design only. Material has no built-in quiz plugin; plan small JS + JSON files.
- Interactive demos (Plotly vs plain JS) in MkDocs.
- The "night observatory" theme design (custom CSS on top of slate).
- noindex / robots (`<meta name="robots" content="noindex">` via override + a robots.txt that disallows everything).
- The GitHub Pages deploy via Actions (official `actions/deploy-pages`).
- Windows Task Scheduler + a resumable batch-runner design.
- **Lesson from tonight:** Claude Code scheduled tasks start in default permission mode and freeze on prompts unless Ahmed sets Auto in the desktop app.
