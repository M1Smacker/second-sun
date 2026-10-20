# Burn 3 DONE (2026-10-19 ~22:10 UTC; time limit lifted by Ahmed for this session)

Nothing committed or pushed. SITE-BLUEPRINT.md not edited. Build output, the stress copy and the test browser profiles were deleted.

## Done, and how each was verified

| Item | Verified how |
|---|---|
| Prototype aligned to the blueprint: §4 tokens and type scale, **one amber accent**, callouts with a 3 px rule, confidence chips by **shape** (solid/dashed/dotted), quiet "Level n of 6", `progress/` (no XP/ranks/badges/streaks), noindex meta, no robots.txt | `contrast_check.py` exit 0 (26 pairs + header); grep finds no XP/badge words; noindex present in built HTML; screenshots in `screens/` checked by eye (dark + light, 390 + 1280) |
| **3-cache service worker** (§6): batched precache that skips failures, capped runtime image cache, quiet "Updated. Reload" line, tap-only takeover, loop guards | `site_check fail404` (30/32 and 632/634 cached, activated), `images` (cache = cap), `update` (line once, exactly 1 reload, lands on B) |
| **Transitions** (theme, links/focus, quiz open/close, page change, update line, demo slider; 150-250 ms ease-out) + off under reduced motion | computed styles: 0.15-0.2 s normally, all 0 s / none under `prefers-reduced-motion` |
| **Stress tests:** strict build + time; 300 pages + 50 × 200 KB images; precache < 25 MB; install survives a 404; layout at 390/1280 dark/light; overflow; tap targets; contrast; console errors; loops; update flow; offline (pages, search, demo); JS off | `test-results.jsonl` (final run: 7/7 modes pass) + the report's "Stress tests" table |
| **No logic loops:** no worker reload loop (first install 0 reloads; update exactly 1), no infinite redirect (1 hop online/offline), no re-entrant hook (`mkdocs serve`: 1 + 1 builds, then none), no theme flicker (1 click = 1 change) | navigation counts, redirect counts, serve log, MutationObserver |
| **11 bugs found and fixed** (list in report.md) | each re-tested; the double theme-icon bug now has a regression assertion |
| Budget guard: precache over 25 MB fails the build | 26 MB test file → "40.1 MB, over the 25 MB budget", exit 1 |
| Learning track: no XP; L0 warm-up + L1-L6 in the blueprint lesson template; written to Ahmed on TOI-1338 and his G1 binaries | read-through; L1 page built and tested (quiz, demo, no-JS fallback) |
| Wave 5 leftovers: ExoFOP candidate fields/evidence/account (publish-first since 2026-08-19), MNRAS AI + unaffiliated authors + fees, A&A AI + charges | sources fetched (ExoFOP and OUP: VERIFIED; A&A: LIKELY, site returns 403) |
| report.md: plain words first, design rule, Stress tests, Bugs, what the blueprint still replaces, **Blueprint conflicts (13)**; claims B1-B28; sources; open questions; friction | files written |
| Test tools kept for re-use: `tools/site_check.mjs`, `tools/serve.mjs`, `tools/make_stress.py` | used for every result above |

## Not done
- [ ] **iPhone** offline test (blueprint §6 checklist): needs a deploy and Ahmed's phone. Only headless Chrome on Windows is verified.
- [ ] Move `hooks.py` logic to `tools/build_book.py` + `make_sw.py` + `check_site.py` (blueprint §5): listed as a later step.
- [ ] Demos loaded only on their own page (blueprint §8): untested whether instant navigation runs in-content scripts; still loaded globally (1.5 KB).
- [ ] `public: false` switch, merged all-wave `claims.csv`, candidate/log/recap templates, sky map: blueprint build phases, not started.
- [ ] Zero console errors in the **Claude Browser pane**: impossible there, because the pane refuses service workers (1 logged error per load); 0 errors in headless Chrome.
- [ ] Published Candidate Upload Request form fields (needs an ExoFOP login); A&A pages first-hand.
- [ ] Lessons L0, L2-L6 as pages (outlined only).

## Decision needed (Ahmed)
- The ExoFOP publish-first rule breaks "two keys, then CTOI" (C11) and changes the blueprint's candidate statuses and scoop-switch timing (open-questions #1, report conflict 4).
