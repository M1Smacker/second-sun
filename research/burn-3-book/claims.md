# Burn 3 claims

| # | Claim | Source | Label | Checked |
|---|---|---|---|---|
| B1 | Final prototype passes `mkdocs build --strict` (Material 9.7.7, MkDocs 1.6.1): 0.50 s warm (1.1 s wall), 1.33 s first cold run; earlier versions 0.44-0.88 s | own test, `site-proto/` | VERIFIED | 2026-10-19 22:01 UTC |
| B2 | 3-cache service worker activates and precaches all 32 shell entries (559 KB); offline, 6 pages load styled and controlled, search finds 4 results, the demo works; unknown page and unvisited image show the 404 page | own test, `tools/site_check.mjs offline`, `test-results.jsonl` | VERIFIED | 2026-10-19 22:05 UTC |
| B3 | In the Claude desktop browser pane, SW registration fails ("unknown error when fetching the script") although `fetch('/sw.js')` returns 200, and the server never logs the request | own test (3 attempts) | VERIFIED (environment-specific) | 2026-10-19 |
| B4 | An iPhone home-screen web app keeps its offline cache; Safari tabs may lose storage after 7 days unused | memory (carried over from wave 9) | UNVERIFIED | |
| B5 | robots.txt rules "MUST be accessible in a file named /robots.txt ... in the top-level path of the service" | RFC 9309 §2.3, https://www.rfc-editor.org/rfc/rfc9309.html | VERIFIED | 2026-10-19 |
| B6 | noindex only works if the page is not blocked by robots.txt; otherwise "the crawler will never see the noindex rule" | Google Search Central, https://developers.google.com/search/docs/crawling-indexing/block-indexing | VERIFIED | 2026-10-19 |
| B7 | Latest action releases: checkout v7.0.1, setup-python v7.0.0, configure-pages v6.0.0, upload-pages-artifact v5.0.0, deploy-pages v5.0.1 | `gh api repos/actions/*/releases/latest` | VERIFIED | 2026-10-19 |
| B8 | All blueprint token pairs pass WCAG contrast (26 pairs + header; `--text-3` only on `--bg`, 4.59/5.14) | own script `contrast_check.py` | VERIFIED | 2026-10-19 22:01 UTC |
| B9 | ExoFOP: community candidates must be published in a peer-reviewed journal with online access before upload; RNAAS allowed only if the detection/vetting method was previously published (peer-reviewed) and is cited; paper URL required | ExoFOP help, "Guidelines for Submitting Community Planet Candidates", https://exofop.ipac.caltech.edu/tess/help.php | VERIFIED | 2026-10-19 |
| B10 | ExoFOP paused new candidate uploads 2026-03-31; reopened 2026-08-19 with publish-first + approval required | ExoFOP news, https://exofop.ipac.caltech.edu/tess/news.php | VERIFIED | 2026-10-19 |
| B11 | Candidate fields: TIC.nn (req), discovery source (req), name (opt), disposition PC/FP (opt), ≥ 2 of period/epoch BJD/depth ppm > 0 (req), all 4 incl. duration for cTOI consideration, tag (req), paper URL (req), initial note (req); supporting material expected | as B9 | VERIFIED | 2026-10-19 |
| B12 | Uploading any data needs an ExoFOP account and login | ExoFOP help, "Uploading Data to ExoFOP" | VERIFIED | 2026-10-19 |
| B13 | The Published Candidate Upload Request form is only visible when logged in | https://exofop.ipac.caltech.edu/tess/pub_candidate_upload_request.php | VERIFIED | 2026-10-19 |
| B14 | MNRAS: AI tools can't be authors; AI use (incl. writing code, processing data) disclosed in cover letter AND Methods/Acknowledgements | OUP MNRAS General instructions §3.2, https://academic.oup.com/mnras/pages/general_instructions | VERIFIED | 2026-10-19 |
| B15 | MNRAS: "no restrictions based on nationality, institutional affiliation, qualifications"; title page needs a full address for each author | as B14, §1, §2.3 | VERIFIED | 2026-10-19 |
| B16 | MNRAS APC £2,356 papers / £1,122 letters (20% off for RAS members); LMIC waiver/discount; discretionary waivers | as B14, §1.3 | VERIFIED | 2026-10-19 |
| B17 | A&A AI statement (18 Jun 2026): no AI authors; no disclosure needed for language, coding, info search under human oversight; other uses declared at submission | aanda.org news 3200 + masthead page 17, via search summary (direct fetch 403) | LIKELY | 2026-10-19 |
| B18 | A&A: sponsoring-country authors pay no page charges; non-sponsoring pay; > 30 pages surcharge since 2025 | aanda.org "Page charges before 2 April 2025" + ESO journal list, via search summary | LIKELY (amounts UNVERIFIED) | 2026-10-19 |
| B19 | Plotly-type libraries add multiple MB to the offline cache | memory | UNVERIFIED | |
| B20 | With no Mermaid/maths extension configured, the built prototype HTML makes no external script/style/font requests (only canonical links to its own site) | own grep of built HTML | VERIFIED | 2026-10-19 21:22 UTC |
| B21 | A reused browser profile keeps serving the previous cached version after a rebuild (cache-first) until the new worker takes over | own test (stale profile showed b2a43298b6fc while build was c745ab6dfcb5) | VERIFIED | 2026-10-19 21:24 UTC |
| B22 | GitHub's Pages starter workflow uses `cancel-in-progress: false` | memory | UNVERIFIED | |
| B23 | On this PC, headless Chrome left 5-21 of 120 sequential requests to Python's http.server (stock and threaded) hanging > 5 s; curl had 0/120; a Node http server had 0/120 (and 0/240 for `tools/serve.mjs`) | own test, `site_check hammer` | VERIFIED | 2026-10-19 |
| B24 | Stress copy (300 extra pages + 50 × 203,188-byte images): strict build 3.2-3.6 s; precache 634 entries / 14.1 MB; search index 4.1 MB; install with 2 forced-404 URLs caches 632/634 in 5.1 s and activates; a 26 MB extra file fails the build on the 25 MB budget | own test, `tools/make_stress.py` + `site_check` | VERIFIED | 2026-10-19 |
| B25 | Update flow: after a rebuild, the 'Updated. Reload' line appears once, the page stays on the old version until tapped, one tap = exactly one reload onto the new version; first install causes no reload | own test, `site_check update` / `offline` | VERIFIED | 2026-10-19 |
| B26 | Layout: 0 px overflow and 0 tap targets under 44 px (inline text links and chips exempt) on 9 pages at 390/1280 px in dark and light; one theme click = one scheme change; reduced motion sets every transition to 0 s | own test, `site_check layout` | VERIFIED | 2026-10-19 |
| B27 | Light-scheme `--text-3` (#6a7282) measures 4.84:1 on `--raised` (#ffffff) and 4.21:1 on `--surface` (#f1efe9) | own script | VERIFIED | 2026-10-19 |
| B28 | `mkdocs serve` with the hook: 1 build at start, 1 rebuild after one watched-file change, none after (no re-entrant loop) | own test | VERIFIED | 2026-10-19 |
