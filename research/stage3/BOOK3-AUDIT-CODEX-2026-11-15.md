# Independent Second Sun Book audit

## Summary

13 issues found. One is critical, six are major and six are minor. All entries below have a browser reproduction. Probable mechanisms have their own confidence where needed. No fixes were applied.

The mobile menu failure affects the Tree, Twinlight home and all six live lessons. Daylight makes the shared header nearly unreadable. New notes can be discarded silently. The fixed Next element reported by the owner is the first-visit tour card. It stays at the same screen position while the page scrolls, by design. Skip normally dismisses it. CX-04 records a separate dismissal race.

## Scope and evidence

- Checkout under audit is d16a8318. The pre-redesign comparison is 6f08b4e4, the parent of c56e08a1. Regression evidence uses website-file history. Earlier audit reports, project resumes, queues and planning documents were excluded.
- The requested interpreter has no mkdocs module. Python 3.14 and Python 3.12 also lack MkDocs. The strict build stopped before building. No dependency was installed. build-strict.log records the failure. The source was protected by build_guard.py, which rejects writes outside the two permitted output locations.
- Current-page runtime testing used the permitted live site. Archive testing used the tracked built archive through the provided local static server. This is a fallback for the missing build dependency. A current local build, generated redirects and current local Eyes/Rehearsal runtime remain unverified.
- Eleven live CSS/JavaScript assets were downloaded as evidence and compared with the checkout. They match after CRLF/LF normalization. Their raw bytes differ due to line endings. This establishes source correspondence for those assets, with semantic correctness assessed separately by probes. See http-and-assets.json.
- The current sweep rendered 45 source-backed pages at all seven requested viewports in both schemes, 630 page/size/theme combinations. It checked document overflow, initially visible small controls, broken loaded images, sidebar visibility and runtime errors. It also sampled heading/header contrast on all 45 daylight pages at 390x844. This is automated coverage, with representative screenshots inspected manually.
- Current HTML parsing checked 3002 internal link occurrences and archive parsing checked 8818. All resolved file destinations and ordinary HTML fragment anchors in those inputs existed. This is a static link check. It excludes external-link availability, PDF contents, JavaScript-only navigation correctness and generated redirects unavailable without a build. See static-links.json and archive-static-links.json.
- Local browser profiles, scripts, downloaded HTML evidence, screenshots and logs are under codex-out. Browsers used CDP with touch emulation on phone sizes. Live Eyes/Rehearsal document navigation was blocked. Cloud endpoints were blocked in current and archive probes. No cards were answered.

## Bug register

### CX-01 Mobile menu opens an empty overlay on the Tree and Twinlight

**P1 critical. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Home, Twinlight home and all six lessons. Header drawer. |
| Viewport | 390x844 touch reproduction. Hidden drawer also recorded at every sweep size. |
| Theme | Slate reproduced. Both schemes render the same hidden sidebar. |
| Exact steps | Open the Tree on a phone-sized viewport. Tap the top-left hamburger. Repeat in lesson 1.1. Compare with the Shelf. |
| Expected | The navigation drawer appears with usable links. |
| Actual | The drawer checkbox becomes checked and the scrim appears, while the sidebar remains hidden and display none. The Shelf drawer opens successfully. Eight current pages carry the hidden sidebar. |
| File and line | book/docs/index.md:2, book/docs/learn/index.md:2 and the six lesson frontmatter blocks at line 2. |
| Probable root cause and proposed correction | The navigation entry in hide removes the Material navigation sidebar even on mobile. The header still offers the drawer control. Preserve the mobile drawer when removing desktop navigation. |
| Saved evidence | targeted.json, diagnostics.json, matrix.json, home-drawer-failed.png, shelf-drawer.png |
| Confidence | High |

### CX-02 Daylight header text and navigation icons almost disappear

**P2 major. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Shared header, page title and inactive top-level tabs. Every current page. |
| Viewport | 390x844 sampled on 45 pages. 1280x800 screenshot. |
| Theme | Default daylight. |
| Exact steps | Switch to daylight on the Shelf. Inspect the site name, theme/search controls and inactive Tree/Learning tabs. Navigate to another page. |
| Expected | Header text and controls remain readable against their backgrounds. |
| Actual | Header foreground stays rgb(230,232,238) while its new background becomes nearly white. The title contrast estimate is 1.14 to 1. Inactive desktop tabs also become very faint. Body headings inspected in this sweep retain dark text. |
| File and line | book/docs/assets/book3.css:29, book/docs/assets/book3.css:30, book/docs/assets/book3.css:32 and book/docs/assets/extra.css:18. |
| Probable root cause and proposed correction | The redesign replaces the dark header/tab background with theme-dependent --ss-bg, while retaining the light --md-primary-bg-color foreground. Pair foreground and background changes for the daylight scheme. The ratio uses the solid page background approximation for the translucent header. |
| Saved evidence | contrast.json, extra-tests.json, shelf-light.png |
| Confidence | High |

### CX-03 Adding a new note silently discards it

**P2 major. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Twinlight lesson reader, selection toolbar and note editor. |
| Viewport | 390x844. |
| Theme | Slate. |
| Exact steps | Select a passage in lesson 1.1. Choose Add a note. Wait for the editor to take focus. Enter a note and press Save. |
| Expected | The selected passage and note appear in the lesson and in saved notes. |
| Actual | The editor closes, tw-hl remains absent, and there are zero highlight marks. Saving reports no failure. A plain Highlight action stores and restores successfully in the separate persistence test. |
| File and line | book/docs/assets/learn.js:189, book/docs/assets/learn.js:201, book/docs/assets/learn.js:207 and book/docs/assets/learn.js:210. |
| Probable root cause and proposed correction | Focusing the textarea triggers selectionchange. Its delayed handler clears pend when the page selection collapses. Save subsequently calls add with pend already null. Capture the selection record for the editor independently of the live browser selection. |
| Saved evidence | extra-tests.json, note-save-result.png, robust-interaction.json |
| Confidence | High |

### CX-04 Skipping the tour can leave a permanent dimming ring

**P2 major. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Tree first-visit tour. |
| Viewport | 390x844. |
| Theme | Slate, ordinary motion. |
| Exact steps | Start the tour. Press Next to reach Branches, then press Skip before its 700 ms ring timer fires. Wait one second. |
| Expected | All tour decoration disappears after dismissal. |
| Actual | The tour card disappears and storage says done, but one ss-tour__ring remains. Its 9999 px shadow keeps the page dimmed until navigation or refresh. |
| File and line | book/docs/assets/tour.js:21, book/docs/assets/tour.js:41 and book/docs/assets/tree.css:169. |
| Probable root cause and proposed correction | The end function removes the current ring but never cancels pending ring-creation timers. Store and cancel the timer, and guard delayed callbacks after dismissal or a step change. |
| Saved evidence | navigation-tests.json, tour-orphan-ring.png |
| Confidence | High |

### CX-05 Modal sheets allow keyboard focus to escape behind them

**P2 major. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Tree node sheet and Twinlight Contents/glossary sheets. |
| Viewport | 390x844. |
| Theme | Slate. |
| Exact steps | Open a Tree node card and press Tab through its controls. Repeat with Twinlight Contents. |
| Expected | Focus remains within the active modal until it closes, then returns to the invoking control. |
| Actual | Tab reaches BODY, the skip link, search and underlying page controls while the modal remains open. Tree escaped after its history controls. Contents escaped after its lesson links. |
| File and line | book/docs/assets/tree.js:404, book/docs/assets/tree.js:424 and book/docs/assets/learn.js:24. |
| Probable root cause and proposed correction | aria-modal declares a modal to assistive technology, while the code only moves initial focus. It provides neither a focus trap nor inert background content. Implement the complete modal focus lifecycle. |
| Saved evidence | targeted.json under treeFocus and lessonFocus, tree-sheet.png, twinlight-contents.png |
| Confidence | High |

### CX-06 The answer checker accepts a percent answer as ppm

**P2 major. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Twinlight lesson 1.2, percent-to-ppm problem. |
| Viewport | 390x844. |
| Theme | Slate. |
| Exact steps | Find the problem asking to convert 0.25 percent to ppm. Enter 2500% and press Check. |
| Expected | Reject the explicit percent suffix for a ppm response, or convert its units before comparing. |
| Actual | The app displays Right and marks the answer correct. It accepts an explicitly different unit value. |
| File and line | book/docs/assets/learn.js:107 and book/docs/assets/learn.js:110. Lesson data in book/docs/learn/u1/l2-percent-and-ppm.md. |
| Probable root cause and proposed correction | num strips a trailing percent sign unconditionally. The comparison never considers data-unit. Make numeric parsing aware of the expected unit. |
| Saved evidence | unit-tests.json, ppm-percent-wrongly-accepted.png |
| Confidence | High |

### CX-07 The claims cards widen the 320 px page

**P2 major. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Claims register, mobile table-to-card transformation. |
| Viewport | 320x568. Other requested sizes had no document overflow in the current-page sweep. |
| Theme | Both slate and default. |
| Exact steps | Open the Claims register at 320x568. Scroll its claim cards and try horizontal scrolling. |
| Expected | The document fits the viewport. Table content wraps or scrolls inside a bounded table region. |
| Actual | The document is 362 px wide for a 320 px client width, adding 42 px of horizontal overflow. The table wrapper measures 360.61 px. Removing the card class in a diagnostic browser session reduces overflow to zero. |
| File and line | book/docs/assets/book3.css:89, book/docs/assets/book3.css:90, book/docs/assets/book3.css:94 and book/docs/assets/book3.js:65. |
| Probable root cause and proposed correction | Visible overflow on the table wrappers combines with an auto minimum in the card grid second column. The wrapper expands to its min-content width. A diagnostic minmax(0,1fr) column with wrapping restores zero overflow. That diagnostic was applied only in the browser. |
| Saved evidence | matrix.json, layout-followup.json, diagnostics.json, claims-320-overflow.png |
| Confidence | High |

### CX-08 Browser Forward does not restore the card just closed by Back

**P3 minor. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Tree card history. Twinlight uses a similar close-only popstate pattern. |
| Viewport | 390x844. |
| Theme | Slate. |
| Exact steps | Open a Tree node. Use browser Back to close it. Use browser Forward. |
| Expected | Forward restores the selected node card and its history state. |
| Actual | Back closes the card. Forward restores a history entry containing sst but leaves the card closed. |
| File and line | book/docs/assets/tree.js:55 and book/docs/assets/tree.js:410. |
| Probable root cause and proposed correction | The state contains only a flag, without the selected node/leaf key. The popstate handler only closes an existing card. Store the selection and handle restoration. Twinlight restoration is a code-only extension of this finding. |
| Saved evidence | targeted.json under treeBack and treeForward |
| Confidence | High for Tree reproduction |

### CX-09 Switching Tree views retains an extra resize listener each time

**P3 minor. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Desktop Tree Mission/Journey switching. |
| Viewport | 1280x800. |
| Theme | Slate. |
| Exact steps | Count window resize listeners with CDP DOMDebugger.getEventListeners. Switch to Journey and back to Mission 20 times. Count again. |
| Expected | A bounded set of listeners serves the current canvas. |
| Actual | The count grows from 6 to 26. Each new canvas installs another closure for a detached stage. |
| File and line | book/docs/assets/tree.js:112 and book/docs/assets/tree.js:240. |
| Probable root cause and proposed correction | render replaces the view markup, while canvas installs a window resize callback with no teardown. Remove the previous callback when disposing the canvas, or share one callback. The audit measured retained listeners. It did not quantify heap growth or long-session performance. |
| Saved evidence | extra-tests.json under resizeBefore and resizeAfter |
| Confidence | High |

### CX-10 A phone sheet survives switching to the desktop canvas

**P3 minor. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Tree card layout during resize or orientation changes across 900 px. |
| Viewport | 390x844 resized to 1280x800. |
| Theme | Slate. |
| Exact steps | Open a Tree node on the phone layout. Widen the viewport beyond 900 px. |
| Expected | The active card follows the new layout or closes cleanly as that view is rebuilt. |
| Actual | A new desktop canvas appears underneath the existing full-width phone sheet and scrim. The phone presentation persists until manually closed. |
| File and line | book/docs/assets/tree.js:52, book/docs/assets/tree.js:112 and book/docs/assets/tree.js:401. |
| Probable root cause and proposed correction | The breakpoint handler rebuilds only .sst-view. Mobile sheets and scrims were appended to body and remain in openState. Reconcile or close the open card during a layout-mode change. |
| Saved evidence | extra-tests.json under orientation, sheet-after-desktop-resize.png |
| Confidence | High |

### CX-11 Several controls fall below the requested 44 px target

**P3 minor. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Tree history dots and sheet close button, Twinlight floating tools, archived home map links. |
| Viewport | 390x844 and 1280x800. The sweep also records lesson tools at other sizes. |
| Theme | Slate and default tools measured in the sweep. |
| Exact steps | Open a Tree card and inspect Close. Open a lesson and inspect Contents, Listen and Home. Inspect desktop Tree history dots at fitted zoom. |
| Expected | The requested touch-target size is at least 44 by 44 CSS pixels. |
| Actual | Tree Close is 36 by 36. Twinlight tools are 40 px high. History dots are radius 5 in the SVG and get smaller when the canvas zooms out. Opening measurements were roughly 5 to 8 px across. The archived home map has 20 by 20 px SVG link targets, with duplicate text navigation available. |
| File and line | book/docs/assets/tree.css:74, book/docs/assets/tree.js:201, book/docs/assets/learn.css:69 and book/archive-v2/index.html:2562. |
| Probable root cause and proposed correction | The new controls use explicit sizes below the requested target, and the dots scale with the canvas. Use larger hit areas independent of the visible artwork. This is evaluated against the brief's 44 px target. |
| Saved evidence | matrix.json under small, targeted.json under treeDesktop, source-lines.txt |
| Confidence | High |

### CX-12 Continue restores a different reading position after plots settle

**P3 minor. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Twinlight saved place and Continue. |
| Viewport | 390x844. |
| Theme | Slate. |
| Exact steps | Load lesson 1.1, wait for both plots and fonts, scroll to y=1800 and wait for saving. Open Twinlight home and choose Continue. Wait for both plots and fonts again. |
| Expected | Continue returns to the saved reading position in the unchanged lesson and viewport. |
| Actual | Before navigation y is 1800 with a 7724 px scroll range. After Continue, y is 1579 with the same final scroll range. The reader is 221 px earlier. |
| File and line | book/docs/assets/learn.js:313 and book/docs/assets/learn.js:332. |
| Probable root cause and proposed correction | Probable cause is restoring on the first animation frame while asynchronous plots still change page geometry. The stored fraction is applied to an intermediate height. The mechanism remains LIKELY. The visible displacement was reproduced. Restore after layout-affecting lesson content is ready. |
| Saved evidence | robust-interaction.json under savedBefore and savedAfter |
| Confidence | Medium |

### CX-13 The archive has no offline 404 fallback file

**P3 minor. CONFIRMED. VERIFIED in Chromium.**

| Field | Evidence |
| --- | --- |
| Page and component | Book 2 archive, offline unknown routes. |
| Viewport | 390x844 local archive. |
| Theme | Slate. |
| Exact steps | Serve book/archive-v2 locally. Let its service worker activate, then emulate offline mode and navigate to an unknown route. |
| Expected | The cached archive shows an understandable 404 page, keeping site navigation available. |
| Actual | Known cached pages render offline. The unknown route has no article, no stylesheets and an empty title in the probe. The archive omits 404.html although its worker attempts to precache and use that file. |
| File and line | book/archive-v2/sw.js:14 and book/archive-v2/sw.js:83. book/archive-v2/404.html is absent. |
| Probable root cause and proposed correction | The archive packaging omitted the fallback page that its frozen worker requires. Include the matching built 404 file in the archive. Initial offline probes bypassed service workers and were discarded. The final probe explicitly enabled worker handling. |
| Saved evidence | archive-offline.json, archive-offline-final.log, archive-offline-final.mjs and filesystem existence check |
| Confidence | High for missing file and local offline failure |

## Regression attribution

Git history attributes source introduction. A full pre-redesign runtime rebuild was unavailable. Browser testing of the checked-in archive supplies an earlier-version comparison. The archive itself was introduced at the chosen baseline, so CX-13 is already present there.

| Finding | Commit evidence and classification |
| --- | --- |
| CX-01 | Introduced during the redesign. a46ec2dd for the Tree frontmatter, e8342b16 for Twinlight. Both are redesign additions. |
| CX-02 | Introduced during the redesign. c56e08a1 introduced book3.css and its header/background rules. The archived dark header supplies the earlier design. |
| CX-03 | Introduced during the redesign. e8342b16 added this selection/editor implementation. |
| CX-04 | Introduced during the redesign. 297e5d5b introduced tour.js. |
| CX-05 | Introduced during the redesign. a46ec2dd introduced Tree sheets. e8342b16 introduced Twinlight sheets. |
| CX-06 | Introduced during the redesign. e8342b16 introduced the parser and comparison. The later tolerance patch retains percent stripping. |
| CX-07 | Introduced during the redesign. c56e08a1 introduced the card CSS/JavaScript. The archived page sweep provides the comparison. |
| CX-08 | Introduced during the redesign. a46ec2dd introduced these history handlers. |
| CX-09 | Introduced during the redesign. a46ec2dd introduced the render/canvas lifecycle. |
| CX-10 | Introduced during the redesign. a46ec2dd introduced both the breakpoint renderer and body-mounted sheet. |
| CX-11 | Mixed. The archived 20 px map targets are pre-existing. The current Tree/Twinlight variants were introduced during the redesign. a46ec2dd introduced Tree targets. e8342b16 introduced Twinlight tools. |
| CX-12 | Introduced during the redesign. e8342b16 introduced asynchronous plot setup and early saved-place restoration. |
| CX-13 | Present at the 6f08b4e4 comparison baseline. Unknown whether the original deployed Book 2 had the issue. The archived worker was added in 6f08b4e4 immediately before the first redesign commit. Attribution is archive packaging during the redesign, without a pre-packaging runtime comparison. |

Source introduction dates support these classifications. They do not establish that every interaction in the older book was correct. No unrelated historical issue is classified as fixed or safe.

## Useful engineering concept

A UI component needs a teardown lifecycle. Timers, history entries, global event listeners and modal focus can outlive the DOM that created them. CX-04, CX-05, CX-08, CX-09 and CX-10 are different consequences of leaving that lifecycle incomplete.

## Coverage matrix

Each viewport has one column per scheme. S means slate and D means daylight. PASS means the saved initial-render snapshot had no document overflow, broken loaded image, measured small control or hidden mobile drawer in the checked set. FAIL means at least one of those checks failed. At 390x844 daylight, the shared-header contrast check is included. A PASS cell covers these snapshot checks only. Delayed controls, off-screen content and interactive flows have narrower coverage below. Search-overlay labels were excluded as scan artifacts from the archive status. The raw measurements remain in the JSON files.

The matrices are automated browser measurements. Source-wide inference about a common style does not turn an untested interaction into a PASS.

### Current pages

630 snapshots across 45 pages. No observed scheme mismatches.

| Page | 320 S | 320 D | 375 S | 375 D | 390 S | 390 D | 430 S | 430 D | 768 S | 768 D | 1280 S | 1280 D | 1920 S | 1920 D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| / | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| candidates/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| claims/ | FAIL | FAIL | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-19/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-20/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-21/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-23/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-24/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-27/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-28/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-29/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-30/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-10-31/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-11-02/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-11-03/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-11-04/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-11-10/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-11-11/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| field-notes/2026-11-14/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| glossary/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab0-workbench/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab1-name-to-number/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab2-get-the-data/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab3-plot-and-read/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab4-find-a-dip/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab5-two-suns/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab6-fake-planets/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab7-pixels/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab8-read-stanley/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| labs/lab9-your-star/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| learn/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| learn/u1/l1-a-light-curve/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS |
| learn/u1/l2-percent-and-ppm/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | PASS |
| learn/u1/l3-noise/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| learn/u1/l4-what-a-dip-looks-like/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| learn/u2/l1-orbits-and-periods/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL |
| learn/u2/l2-how-long-a-dip-lasts/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| reference/for-astronomers/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| reference/prior-work/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| reference/reading-list/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| shelf/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| training/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| versions/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| watch/ | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

### Archive pages

1204 snapshots across 86 archived pages. No observed scheme mismatches. No document overflow or broken loaded images were recorded. Some older map links remain below the requested target size, as the raw archive-matrix.json records. Their duplicate text navigation was preserved in the archive. CX-11 covers those older map targets alongside the new Tree/Twinlight targets. Search-overlay labels remain excluded as scan artifacts.

| Page | 320 S | 320 D | 375 S | 375 D | 390 S | 390 D | 430 S | 430 D | 768 S | 768 D | 1280 S | 1280 D | 1920 S | 1920 D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /v2/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/book/01-stars-names-missions/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/02-light-curves/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/03-our-data/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/04-two-suns/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/05-wandering-transits/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/06-orbits-three-body/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/07-noise-and-statistics/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/08-our-detector/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/09-fake-planets/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/10-vetting/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/11-pixels-and-neighbours/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/12-stanley/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/13-your-workshop/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/14-credit-and-publishing/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/book/15-mistakes-as-lessons/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/candidates/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/claims/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/eyes/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-19/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-20/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-21/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-23/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-24/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-27/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-28/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-29/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-30/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-10-31/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-11-02/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-11-03/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-11-04/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-11-10/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-11-11/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/field-notes/2026-11-14/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/glossary/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab0-workbench/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab1-name-to-number/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab2-get-the-data/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab3-plot-and-read/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab4-find-a-dip/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab5-two-suns/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab6-fake-planets/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab7-pixels/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab8-read-stanley/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/labs/lab9-your-star/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/learn/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/learn/l1-dip-depth/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part1/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part1/cheat/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part1/labs/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/parts/part1/review/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part2/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part2/cheat/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part2/labs/ | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/parts/part2/review/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part3/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part3/cheat/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part3/labs/ | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/parts/part3/review/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part4/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part4/cheat/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part4/labs/ | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/parts/part4/review/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part5/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part5/cheat/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part5/labs/ | PASS | PASS | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/parts/part5/review/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part6/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part6/cheat/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/parts/part6/labs/ | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| /v2/parts/part6/review/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/progress/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/quests/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/reference/for-astronomers/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/reference/prior-work/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/reference/reading-list/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/rehearsal/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/start/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/start/first-search/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/start/how-to-read/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/start/journey/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/start/story-so-far/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/versions/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| /v2/watch/ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

### Functional checks

| Feature | Viewport and theme actually exercised | Result |
| --- | --- | --- |
| Tree drawer touch tap | 390x844 slate | FAIL, CX-01 |
| Shelf drawer touch tap | 390x844 slate | PASS |
| Tree fixed Next tour card | 390x844 slate | PASS for fixed positioning and normal Skip. FAIL for dismissal race, CX-04 |
| Tree phone nodes and history expansion | 390x844 slate | PASS for 19 node openings and 55 expansions |
| Tree desktop node openings | 1280x800 slate | PASS for 24 nodes |
| Tree pan and two-touch pinch | 1280x800 slate, touch emulation explicitly enabled | PASS for transform changes |
| Tree search and Journey | 1280x800 slate | PASS for dimming matches, five phases and 18 days |
| Tree direct node fragment | 390x844 slate | PASS after initialization |
| Tree Back/Forward | 390x844 slate | FAIL, CX-08 |
| Modal keyboard traversal | 390x844 slate | FAIL, CX-05 |
| Tree breakpoint with an open sheet | 390x844 to 1280x800 slate | FAIL, CX-10 |
| Tree listener lifetime | 1280x800 slate | FAIL, CX-09 |
| Six lessons, plots and answer forms | 390x844 slate | PASS for rendering and configured-answer smoke checks. FAIL for explicit wrong-unit input, CX-06 |
| Plot touch point readout | 390x844 slate | PASS |
| Highlight and reload | 390x844 slate | PASS |
| New note and Save | 390x844 slate | FAIL, CX-03 |
| Saved place and Continue | 390x844 slate | FAIL, CX-12 |
| Glossary sheet and Back | 390x844 slate | PASS for opening, definition and unchanged scroll position |
| Listen panel | 390x844 slate | PASS for controls and voice enumeration. NOT TESTED for audio and timed behavior |
| Search query and returned results | 390x844 slate | PASS for the transit query |
| Theme toggle and persistence | 390x844 daylight | PASS across subsequent navigation |
| Reduced motion | 390x844 | PASS for sampled animation duration and omitted starfield |
| Unknown current route | 390x844 slate | PASS for rendered 404 text |
| Ten lab pages | 390x844 slate | PASS for loading. No web range sliders or demo canvases were present on these lab pages. Executing their local Python exercises was excluded |
| Archive Eyes and Rehearsal | All seven sizes, both schemes | PASS for initial rendering and document geometry. NOT TESTED for answering, cloud or score persistence |
| Archive offline known pages | 390x844 slate | PASS for home, learning and glossary |
| Archive offline unknown route | 390x844 slate | FAIL, CX-13 |
| Current local build and generated redirects | All viewports and themes | NOT TESTED, missing MkDocs |
| Current Eyes and Rehearsal runtime | All viewports and themes | NOT TESTED, missing current local build and live-document exclusion |
| Other combinations for the interactions above | Viewport/theme combinations outside the stated cells | NOT TESTED |

## Checks and exclusions

- All 19 phone node buttons opened. Their saved history entries supported 55 expansion actions. All 24 desktop nodes, including the root and branch levels, opened. See navigation-tests.json.
- Direct #n=1.1 navigation opened the expected card once the asynchronous Tree initialization completed. Earlier short waits were insufficient and are excluded from the verdict. Search dimmed 17 nodes and left seven bright for an eclipse query. Desktop pan changed the canvas transform, and a two-touch pinch changed scale from 0.88 to 1.32. See navigation-tests.json and robust-interaction.json.
- All six live lessons rendered their nine plots and 34 answer forms. A deliberately incorrect string was rejected and the configured accepted answer was accepted for every form. These are producer-style checks against configured answers. They do not independently validate the astronomy, worked mathematics or all numeric tolerance boundaries. CX-06 is a separate adversarial unit-input check.
- A touch on a visible plot changed its point readout. A plain highlight survived reload. The glossary opened with a definition and Back closed it while preserving y=700. Contents and Listen controls appeared, and 22 speech voices were available. Audible speech, pause/resume timing, sleep timers and real iPhone speech behavior were NOT TESTED.
- Search entered through CDP Input.insertText returned ten rendered results and reported 26 matching documents for transit. An earlier synthetic input-only event did not trigger the complete search path and is excluded. Theme toggle and subsequent navigation preserved daylight. Reduced-motion rendering used a 0.001 s content animation and omitted the star canvas.
- A separate console pass loaded all 45 current and 86 archived pages at 390x844 and recorded zero console.error calls, runtime exceptions or error-level browser log entries. It used the initially selected scheme and one viewport, with cloud and worker exclusions. See console.json.
- All top-level current asset JavaScript files were syntax-checked with node --check. This is static parsing. It supplies no behavioral guarantee. See js-syntax.json.
- The current sweep recorded no Runtime.exceptionThrown events, no failed network requests and no broken loaded images. Its scope excluded blocked cloud requests, service-worker handling and the two forbidden live documents. It did not force every lazy resource to load.
- The archive sweep recorded zero runtime exceptions and 23 aborted requests. Their source causes were not isolated, so they are not filed as bugs. The archive worker controlled the local page and cached 216 shell entries. Home, learning and glossary rendered offline with styles. Unknown-route fallback failed as CX-13 records. A requested training route is absent from the old archive and is excluded as a functional page test. Current-worker installation/update behavior and skipped-precache recovery were NOT TESTED.
- Real iPhone Safari/WebKit, VoiceOver, installed-PWA mode, physical device gestures, safe-area hardware, audio output and operating-system text scaling were NOT TESTED. Chromium emulation supplies different browser-engine behavior.
- External reference destinations, PDFs, scientific claims, private data and the live cloud/scoring flows were excluded. Current local Eyes/Rehearsal tests were blocked by the missing current build. The archive versions were opened locally and rendered in the archive sweep, with scoring and answering excluded.
- Initial contrast sampling covers headings and the header. Full contrast checking of all body/link/icon/active-state combinations, opacity compositing and every scroll position was NOT TESTED. The source-wide daylight header issue is CX-02.
- Keyboard focus was tested in the sheets and exposed CX-05. Complete keyboard-only operation of every lab and every plot, screen-reader output, and visual inspection of every scroll position were NOT TESTED. Touch-target scanning covered initially visible controls plus targeted Tree/lesson controls, with ordinary inline text links excluded from the 44 px scan.
- Measured listener retention is CX-09. Heap snapshots, garbage-collection measurements and hours-long memory soak tests were NOT TESTED.

## Read-only result and remaining limitation

Final git diff --exit-code returned zero and git status --porcelain=v1 was empty. These are tracked-workspace checks. The audit made no source changes, commits, pushes, installations or configuration edits. The strict-build and current-local-app gaps require an environment with the existing project MkDocs dependencies available. Usage-panel percentages were unavailable in this audit environment.

## Next action

Claude reviews this report and its saved reproductions to choose the fixes. Review needs Claude and incurs no additional model usage until a new review or implementation task starts.
