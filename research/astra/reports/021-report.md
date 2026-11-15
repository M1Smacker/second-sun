7 confirmed issues, 2 major and 5 smaller. M-16, M-19 and M-29 remain partly broken. Both release gates pass.

# 021 independent Book 3.4 audit

Codex, runtime model and effort unverified. The brief specifies neither. Completed 2026-11-15 15:02 +0300 Kuwait.

Branch `astra/021-audit-book-3-4`, audited HEAD `5ff39bb4`, which includes the 020 merge. Tree node 4.1 applies to every finding below. The report is the only new repository deliverable. The pre-existing `.codex_run.lock` was preserved. Git's final read-only diff showed no tracked source changes.

## Execution slip

A broad source search printed an embedded public web API key from `research/burn-3-book/tools/site_check.mjs`. Its value is omitted here. Subsequent reads excluded that section. No cloud test or outward write was performed.

## Bug register

Severity follows the earlier audit. P2 means major, P3 minor, P4 improvement. Every issue below is CONFIRMED in the stated environment. Evidence files live under `data/astra/021/`.

| ID | Severity | Page and reproduction | Expected | Actual and evidence | Label |
| --- | --- | --- | --- | --- | --- |
| CX2-01 | P2 | Open the Tree online, let its offline worker finish, visit `/v2/`, then lose the connection and return to Book 3. Reproduced in Chrome and WebKit, including publication-equivalent assembly. | Previously saved Book 3 pages remain available. | Activating the archive deletes Book 3's 279-entry shell cache. Returning offline fails. Both workers share the `ss-shell-`, `ss-images-` and `ss-meta` names, and activation deletes other `ss-` caches. Evidence `publication-cross.json`, `offline-server-stopped.json`, `worker-isolation.json`. Source `book/sw-template.js` lines 15 to 17 and 54, and the archive's worker. | CONFIRMED |
| CX2-02 | P2 | At 1280 by 800, open node 1.1 from its row. At 1440 by 1000, open node 4.1 after scrolling to its row. Chrome and WebKit. | The panel's visible scroll area and Close control fit below the header. | The first panel spans about y=551 to 1235 on an 800 px screen. On the lower node, the panel rises to y=12, putting Close behind the header's Search field. A native hit test reaches Search at Close's centre. Playwright's automatic scrolling can recover a click, so this is a placement failure. Evidence `edgecases.json`, `panel-click.json`, `chromium-panel-bounds-1280-1.1.png`, `chromium-panel-bounds-1440-4.1.png`. Source `tree.css` lines 158 and 269. M-19 is back on these paths. | CONFIRMED |
| CX2-03 | P3 | Open Tree details, Eyes, rehearsal or Search window and inspect the rendered heading sequence. Both engines and themes. | Subsections follow a continuous heading hierarchy. | Tree details jump from h2 to h4. Eyes jumps from h1 to h4, rehearsal and Search window from h1 to h3. The ordinary static pages passed this scan. Evidence `edgecases.json` and `independent.json`, fields `headings` and `skips`. Source `tree.js` lines 218 to 224. M-29 remains partly broken in generated content. | CONFIRMED |
| CX2-04 | P3 | Disable JavaScript and open `/watch/`. Both engines. | A static status or an explanation that the live panel requires JavaScript. | The panel remains at `Loading...` indefinitely. The explanatory notes still read. Eyes and rehearsal have readable static explanations. Evidence `independent.json`, `nojs` entries for `watch/`. Source `book/docs/watch.md` line 3. | CONFIRMED |
| CX2-05 | P3 | On a 390 or 320 px phone, open `#n=4.1`, then close the sheet. Both engines and themes. | The underlying branch selection follows the linked node. | The correct node opens, while branch 1 remains selected. Closing reveals branch 1's rows. Restoring a link leaves the `chosen` branch unchanged. Evidence `independent.json`, Tree entries with `deep` ending in 4.1 and `chosen` equal to 1. Source `tree.js` lines 72 and 227. | CONFIRMED |
| CX2-06 | P3 | On a phone, open a sheet at scrollTop zero and drag its grab handle down 200 px. Native Chrome touch events. | The previously supported downward swipe dismisses the sheet. | It stays open. The design-A code retains the handle and removes the old touch listeners. The pre-020 first parent of merge `2b5d70a0` closes after a drag over 110 px. Evidence `edgecases.json`, `sheet-swipe-down`. Chrome emulation confirms the lost gesture. Physical iPhone behaviour was not tested. | CONFIRMED |
| CX2-07 | P4 | Open a visible confidence chip on `/claims/` at 390 px and hit-test above and below its centre. Both engines. | The requested 44 px tap height. | The visual chip is 16 px high and its expanded pseudo-element is 42 px high. Hits 22 px from the centre miss. The expansion substantially improves the target, but falls 2 px short of the stated mark. Evidence `chip-hit.json`. Source `book3.css` line 69. M-16 is partly fixed. | CONFIRMED |

## Checks completed

### Build and provenance

The strict build passed in 3.91 seconds. A data-only Python wrapper ran the MkDocs module with the specified docs interpreter and arguments. Its write guard rejected any attempted Python file write outside this audit's data folder. Bytecode writing was disabled. This allowed the normal build hooks to validate the current source while enforcing the read-only audit.

The brief's archive-copy recipe omits a publication assembly step. `publish_book.ps1` lines 96 to 99 add a generated `/v2/404.html`, which is absent from the byte-exact archive. The initial audit build therefore lacks that file. I reproduced this exact assembly step in a separate `publication-site/` copy, then tested its offline behaviour. This copy adds the publisher's generated file to machine output. Source files were unchanged. The publication-equivalent cross-archive test still reproduces CX2-01.

The static link scan covered 181 HTML files, including the archive. It found zero missing local link targets and zero missing static anchors after normalising the production `/second-sun/` prefix. It also inspected 299 lab-link occurrences. This proves target resolution in the assembled files. It does not prove the meaning of their contents. Evidence `build.log`, `links.json`, `assemble_publication.py`.

### Browser coverage

- Both release scripts ran unchanged against the initial build. Chrome checked 35 sitemap pages at 320, 390, 768 and 1280 px in both themes, plus first-visit tour and splash paths. WebKit checked the same 35 pages using its iPhone 13 profile in both themes. Both returned zero gate failures. Evidence `release.json`, `webkit.json`, `progress.json`.
- The retained repairs suite passed 68 checks in Chrome and 68 in WebKit. These are producer regression checks, supplemented here by fresh tests. They are not independent validation of their own assertions. Evidence `repairs-chromium.log`, `repairs-webkit.log`.
- Fresh measurements covered 152 page/theme/engine loads, including load-only checks of Eyes and rehearsal. There were zero captured sweep exceptions, horizontal overflows, measured low-contrast text items or failed theme switches. Script inspection confirmed the eight Eyes/rehearsal scripts are confined to those pages, and `watch.js` is confined to Search window. Evidence `independent.json`.
- The Tree matrix covered 1440 by 1000, 1280 by 800, 1024 by 768 touch, 390 by 844 touch and 320 by 568 touch, in both themes and both engines, 20 cells. Text boxes had zero measured horizontal overflow. Back and Forward worked in every cell. Phone sheets trapped keyboard focus and locked the body. Desktop regions are non-modal, so they correctly permit focus outside the panel.
- An additional 152 node openings covered every one of the 19 child nodes in both engines at four widths. All opened with the requested node identity. After repeated opening, closing and resizing, all 32 measured vine endpoints met card edges within 0.04 CSS px. Journey dates stayed in one descending column, with its line outside the text. Evidence `tree-extra.json`, `independent.json`.
- Chrome's native wheel moved the desktop panel internally while page position stayed constant. The retained WebKit check exercised its manual wheel fallback through a DOM wheel event. That WebKit check supplies handler evidence. Native Safari wheel behaviour remains untested.
- The tour covered four steps at four sizes in both engines, 32 step captures. Its targets stayed aligned, the page remained locked, Skip removed the delayed ring and Done persisted. Search Enter, No matches, resize and explicit update acknowledgement passed. The update badge survived 4.3 seconds and disappeared after Mark updates read and reload. Evidence `independent.json`, `tree-extra.json`, repairs logs.
- Dark-mode starfield counters advanced 11 and 8 frames during the measured interval in Chrome and WebKit. Both advanced zero frames in light mode. Theme changes persisted through navigation and reload. Journey and open-detail contrast scans also returned zero low-contrast items in both themes and engines. Evidence `tree-extra.json`, `edgecases.json`, `state-contrast.json`.
- All ten old lab addresses reached their matching `/v2/labs/` destination in both engines, 20 browser checks. Each destination loaded successfully at 390 px without horizontal overflow. Lab code was not executed. Evidence `independent.json`, `labs`.

### Offline and JavaScript-disabled paths

With a fresh Book 3 cache and its local server physically stopped, the Tree, Eyes, rehearsal and Search window all reached their ready states in Chrome and WebKit. The lesson's HTML also loaded offline. Eyes and rehearsal were mounted without answering a card. On the separate publication-equivalent assembly, an unknown archive address displayed `Page not found` with two recovery links in both engines. The ordinary Book 3 404 page has four recovery links. Evidence `publication-offline.json`, `offline-server-stopped.json`.

After an archive visit, both browsers lost Book 3's cache and failed to reopen its home offline, including with the publisher-generated archive 404 present. These positive controls distinguish CX2-01 from general failure to support offline pages. Evidence `publication-cross.json`.

With JavaScript disabled, the Tree's generated static list remained visible. Eyes, rehearsal, archive home and 404 text remained readable. Search window has CX2-04. Twelve engine/page fallback cases were inspected. Evidence `independent.json`, `nojs`.

## M-01 through M-32 regression

There are 27 still-fixed entries on the tested paths, three partial or returning defects, and two intentional retained behaviours. The evidence names below refer to this audit's files.

| Original | Outcome | Retest and evidence |
| --- | --- | --- |
| M-01 | Still fixed | Menu opens after scrolling on the sitemap sweep, including Tree and all lessons. Both release JSON files. |
| M-02 | Still fixed | Light headers and icons pass the measured contrast thresholds. Both release JSON files. |
| M-03 | Still fixed | Tree toolbar scrolls away, including phone landscape. Both repairs logs. |
| M-04 | Still fixed | Modal tour locks scrolling and keeps its ring aligned. Both repairs logs and 32 tour captures. |
| M-05 | Still fixed in emulation | Negative-answer inputs use text mode. Both repairs logs. Real iPhone keypad remains untested. |
| M-06 | Still fixed | Skip during the ring delay leaves no ring. Both repairs logs. |
| M-07 | Still fixed | Saved notes and their highlights survive reload. Both repairs logs. |
| M-08 | Still fixed | A ppm answer with an incorrect percent suffix is rejected. Both repairs logs. |
| M-09 | Still fixed | Decimal comma and leading-zero decimal cases are accepted correctly. Both repairs logs. |
| M-10 | Still fixed | Claims fits 320 px. Chrome release gate. |
| M-11 | Still fixed | Tree and lesson sheets trap focus. Tree body locks, saved lesson place stays stable while its sheet is open. Both repairs logs. |
| M-12 | Still fixed | Continue returns within 5 px of the saved position, including the old fractional save format. Both repairs logs. |
| M-13 | Still fixed | Back closes and Forward reopens in all 20 Tree matrix cells. `independent.json`. |
| M-14 | Still fixed | Widening a phone replaces the sheet with a desktop panel. Both repairs logs. |
| M-15 | Still fixed | Four Mission/Journey round trips add no resize listeners. Both repairs logs. |
| M-16 | Partial | Tree and Twinlight controls meet 44 px. Confidence-chip hit areas measure 42 px. CX2-07, `chip-hit.json`. |
| M-17 | Still fixed | Enter opens a matching node and an unmatched query shows No matches. Both repairs logs. |
| M-18 | Still fixed | HTML labels fit across 20 Tree cells and the node-opening sweep. `independent.json`, `tree-extra.json`. |
| M-19 | Back on PC placement | A panel extends below the viewport or puts Close behind the header. CX2-02, `edgecases.json`, `panel-click.json`. |
| M-20 | Still fixed by new layout | All branches are reachable by normal page scrolling. The old clipped canvas is gone. Phone first-screen density is discussed below. |
| M-21 | Still fixed on measured states | All-page text scan, Tree IDs, coming units, lesson links, Journey and details pass both themes. Release JSON files, repairs logs, `state-contrast.json`. |
| M-22 | Still fixed | Valid unit suffixes and Unicode minus work. Incorrect units fail. Both repairs logs. |
| M-23 | Still fixed | Tour copy has no stale Book 3.0 introduction and its final menu path works. Both repairs logs. |
| M-24 | Still fixed on measured states | Sky animation advances in dark mode and pauses in light mode. `tree-extra.json`. Battery consumption was not measured. |
| M-25 | Still fixed in publication assembly | The publisher adds the missing archive 404. Its offline fallback works in both engines. The brief's simpler local recipe omits that step. `publication-offline.json`. |
| M-26 | Retained by design | Old addresses still redirect to the chosen current pages or archive. Static targets resolve, all ten lab redirects were followed. `links.json`, `independent.json`. |
| M-27 | Retained by design | Three frozen-archive GitHub links still return HTTP 404. `archive-links.json`, sources below. |
| M-28 | Still fixed | Current 404 contains four recovery links. No-JavaScript browser checks and static target resolution. `independent.json`, `links.json`. |
| M-29 | Partial | Static pages pass. Tree details and the three generated tool pages still skip heading levels. CX2-03. |
| M-30 | Still fixed | A 1 px downward step after a longer scroll keeps the lesson header hidden. Both repairs logs. |
| M-31 | Still fixed | N new persists until explicit acknowledgement, then stays cleared after reload. `tree-extra.json`. |
| M-32 | Still fixed | The source daily recap appears in the Tree's Now line. `research/TREE.md`, `independent.json` and screenshots. |

For M-27, read-only HEAD requests returned 404 for all three retained targets. The web fetch tool returned cache-miss errors, so the network status evidence comes from the separate Python probe. [Old data chapter](https://github.com/M1Smacker/second-sun/blob/main/book/docs/book/03-our-data.md), [old pixels chapter](https://github.com/M1Smacker/second-sun/blob/main/book/docs/book/11-pixels-and-neighbours.md), [old publishing chapter](https://github.com/M1Smacker/second-sun/blob/main/book/docs/book/14-credit-and-publishing.md).

## Mockup A comparison

I viewed all three supplied mockups, all five Chrome sizes in both themes, and selected WebKit phone, panel, Journey and tour captures. Automated geometry checks covered the full two-engine matrix.

- The alternating phone branch cards, central gold vine, desktop branch arrangement and phone bottom sheet follow mockup A. The new page scrolls normally. At 1024 px the two branch columns become narrow and long, while text continues to fit.
- The real page adds the current book header, two destination links, the Now paragraph, search and Mission/Journey controls. The mockup goes much more directly from the title to Goal. The first phone branch begins around y=839 at 390 px and y=909 at 320 px, beyond the initial viewport. This is the largest visible composition difference. Evidence `chromium-tree-390-slate.png`, `chromium-tree-320-slate.png` and `tree-extra.json`.
- Current titles, statuses and work history differ from the older example data. The scoreboard displays frozen Petrova 1.0.0, rounded to 28%, with range 21 to 34%. The mockup displays 27%. This reports the existing rounding and source content, without re-auditing the scientific estimate.
- Goal and scoreboard have no mockup chevrons, and Goal omits its mockup status line. The node 1.1 sheet omits the mockup's separate Why it matters section. The implementation renders that section only when a node supplies `why`.
- Light mode uses the new sky-blue background and pale-blue Tree cards. Selected controls and raised sheets use the lighter raised surface. Gold text passed the contrast screens. The mockup references are dark-only. Desktop panel placement differs materially through CX2-02.

## What the release gates miss

| Reader problem | Why the gates miss it | Current result |
| --- | --- | --- |
| Losing saved pages after visiting Book 2 | They never test the root-to-archive offline transition. | Exists, CX2-01. |
| A detail panel or Close control outside usable screen space | The repairs suite checks sticky/overflow CSS properties. It does not require the whole panel and control to remain below the header and inside the viewport. | Exists, CX2-02. Both retained suites still report M-19 passing. |
| Heading structure produced by JavaScript | Neither release gate checks heading order after opening details or mounting tool UI. | Exists, CX2-03. |
| A permanent loading message without JavaScript | Their normal page sweep enables JavaScript. | Exists, CX2-04. |
| A deep link leaving an unrelated branch selected | They check that a card opens, Back closes it and Forward reopens it. | Exists, CX2-05. |
| Loss of swipe dismissal and slightly undersized expanded targets | No grab-handle gesture or pseudo-element hit-area measurement is present. | Exists, CX2-06 and CX2-07. |

A cache name is shared across an entire origin, including separate service-worker scopes. That is the engineering reason two independently working offline books can damage each other's saved data. Similarly, a correct CSS property does not establish where a reader can actually see or hit a control.

## What I did NOT check

- Physical iPhone Safari, VoiceOver, real on-screen keyboards, installed-app update behaviour, native WebKit wheel input, audio playback and sleep timers.
- Every possible saved-state history, hours-long use or performance/battery consumption. The starfield check measures drawing activity only.
- Scientific correctness of lesson content, searches or detection results. No search, injection or lab program was run. No live Eyes page, cloud mode or answer submission was used.
- The deployed site's byte identity with this branch. This is a local audit of the merged source and its publication assembly. Apart from the three M-27 targets, external destinations were not re-audited.
- A separate independent review of these new audit scripts, or Claude's fence checker. The source-change check was a read-only Git diff and status comparison.

## Execution adaptations and exclusions

The first full Journey screenshot exceeded the browser's 32767 px image dimension limit. Its catch path left the test browser open. WMI process inspection was denied. I stopped my own failed command with Ctrl+C and reran with viewport-only Journey captures, a shorter absent-selector timeout and explicit failure exit. The rerun completed with zero sweep exceptions. The initial JSON and log are retained as `independent-initial.*`.

The first offline probe used a blanket request route and `setOffline`. It produced misleading online responses in Chrome and internal errors in WebKit. It is excluded from the offline verdict. Later probes stopped dedicated servers owned by the audit, verified the server was unreachable, and waited for the asynchronous widgets to become ready. Those results are in `offline-server-stopped.json`, `publication-offline.json` and `publication-cross.json`.

The local 404 template uses production-prefixed assets and destinations. Static checking normalised that prefix. The publication-equivalent archive fallback was tested separately. Temporary additional audit servers used ports 8507 to 8509 and were stopped by their owning scripts.

## STOP SIGNS hit

The key-output slip is recorded above. No scientific stop sign was encountered. The read-only brief takes precedence over the mailbox's usual commit, branch, USAGE and RESUME edits. Usage is recorded here. Git-writing commands were not run.

## QUEUE PROPOSALS

All seven are FIX proposals on Tree node 4.1. Claude files them.

- CX2-01, isolate the two books' offline cache lifecycles.
- CX2-02, keep the desktop detail panel and Close control inside usable viewport space, including lower rows.
- CX2-03, repair heading levels in generated Tree and tool content.
- CX2-04, replace the JavaScript-disabled Search window loading placeholder with a static explanation or status.
- CX2-05, restore the linked node's parent selection on phone deep links.
- CX2-06, restore the sheet's downward dismissal gesture.
- CX2-07, complete the confidence chips' 44 px hit area.

## IDEAS

None beyond the requested audit findings.

## Disagreements with Claude

The statement that all 32 earlier defects are fixed is too broad for the tested build. M-16 is partial, M-19 returns on actual panel placement, and M-29 remains in generated content. The table above gives the contradicting runtime evidence. M-26 and M-27 are documented retained behaviours. Technical direction remains Claude's decision.

## Questions for Ahmed

None.

## Usage

Predicted before execution, 35 five-hour points and 7 weekly points, with a 100-tool-call cap. Runtime model and effort are unverified. Actual bars are unavailable in this headless runner. No percentage is inferred. This report holds the usage row because the brief permits only the report and machine evidence.

Lesson learned, wait for asynchronous offline readiness and test a real loss of the server. Compare measured hit areas and panel coordinates with the reader's screen, even when the existing gate passes.

Next, Claude reviews the seven findings, starting with the offline cache and panel placement. Estimated review cost is small and unmetered here. Claude owns that review.
