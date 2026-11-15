# 019 Tree, tour and Twinlight fixes

Codex, 15 Nov 2026, 11:29 am Kuwait. The brief specifies no model or effort. This headless runner exposes neither the runtime model identity nor the usage panel.

**Path slip.** The first build used the brief's relative `-d data/astra/019/site` argument. MkDocs resolved it under `book/`, creating `book/data/astra/019/site`. Moved that generated site to `data/astra/019/site`. Subsequent builds used an absolute output path. No pre-existing files were removed. Empty parent directories remain under `book/data/astra/019/`.

**Plain verdict.** 22 scoped issues fixed and reproduced in Chromium and WebKit. The five existing modes also pass. One additional icon-sizing issue is recorded below for Claude.

**Branch.** `astra/019-fix-tree-tour-twinlight`, unchanged throughout. No git-writing command was run. All findings belong to Tree node 4.1, FIX 99.

## Findings

Every row is CONFIRMED by runtime checks in `site_check.mjs repairs`. The before run loads the five saved, unmodified assets through browser request interception. Service workers are blocked in this mode so each navigation really exercises the selected asset set. Evidence files live under `data/astra/019/`. These are producer checks. Claude's independent review remains pending.

| Bug | Result | Before measurement | After measurement | Changed code and failing regression guard |
|---|---|---|---|---|
| M-03 | FIXED | Toolbar sticky. Landscape toolbar bottom stayed at 128 px after scrolling. | Relative flow. Landscape bottom moves to -293.5 px. | `tree.css:12`, `M-03/320`, `/390`, `/landscape`. |
| M-04 | FIXED | Non-modal tour, unlocked background, scroll reached 907 px while ring stayed behind. | Modal tour, fixed-body scroll lock, ring alignment error 0 px and background scroll 0. | `tour.js:18`, `tree.css:170`, `M-04`, `M-04/position`. |
| M-05 | FIXED | Negative-answer input used `decimal`. | Negative-answer input uses `text`, including the three negative problems. | `learn.js:159`, `M-05/320`, `/390`. Physical iPhone keyboard remains NOT TESTED. |
| M-06 | FIXED | Skip during the delayed ring left a ring after 900 ms. | Zero remaining rings. Pending timers are cancelled on step change and exit. | `tour.js:41`, `tour.js:62`, `M-06`. |
| M-07 | FIXED | New note count 0 after focus collapsed the selection. No highlight after reload. | Note text saved and highlight survives reload at both phone sizes. | `learn.js:234`, `M-07/320`, `/390`, reload guards. |
| M-08 | FIXED | `2500%` accepted for the 2500 ppm problem. | Rejected. Bare 2500 and `2,500 ppm` remain accepted. | `learn.js:127`, `M-08`, `units/grouped`, `units/wrong`. |
| M-09 | FIXED | `0,90` parsed as 90 and rejected for 0.90. | `0,90` and `0,900` accepted for 0.90. | `learn.js:127`, `M-09`, `decimals/zero`. |
| M-11 | FIXED | Shift+Tab escaped both sheet types. Tree background position was relative and unlocked. | Focus wraps within each sheet. Background is inert and scroll-locked. The saved lesson place survives an open sheet. | `tree.js:437`, `learn.js:24`, `M-11/tree/*`, `M-11/learn/*`, `M-11/place/*`. |
| M-12 | FIXED | Saved 1800 px, resumed at 2123 px on 320 and 2053 px on 390. Old fractional save missed by about 212 px. | Both resume at 1800 px. Old fractional saves restore within 0.3 px in both engines. | `learn.js:340`, `learn.js:354`, `learn.js:370`, `M-12/320`, `/390`, `/legacy`. |
| M-13 | FIXED | Forward reopened zero cards after Back. | Forward reopens the saved card at both phone sizes. | `tree.js:59`, `tree.js:468`, `tree.js:508`, `M-13/*`. |
| M-14 | FIXED | Phone sheet remained after widening. | Zero phone sheets and one corresponding PC card. | `tree.js:51`, `M-14/*`. |
| M-15 | FIXED | Resize registrations rose 5 to 9 over four Mission/Journey cycles. Resize changed scale 1.188 to 0.88 and reset the translation. | Registrations stay 5. Transform stays byte-for-byte identical across resize. | `tree.js:56`, `tree.js:136`, `tree.js:278`, `M-15/listeners`, `M-15/view`. |
| M-16 | FIXED within assigned files | Tree Close 36 by 36 px, lesson tools 40 px high, history hit target about 8.8 px. Expanded neighboring dot targets would overlap. | Close and tools at least 44 by 44. Latest-history target 50 by 50 at reset scale, 67.5 px at the tested zoom. No history-target overlap at 1024 or 1280. End links have a 44 px minimum. | `tree.css:57`, `tree.css:79`, `tree.js:232`, `learn.css:69`, `learn.css:183`, `M-16/*`. |
| M-17 | FIXED | Enter opened zero phone cards. Unmatched query had no message. | Enter opens one matching card. Unmatched query displays `No matches`. | `tree.js:91`, `tree.js:126`, `M-17/empty/*`, `M-17/enter/*`. |
| M-18 | FIXED | Four canvas labels exceeded their rectangles in this reproduction. | Zero overflowing canvas labels. | `tree.js:211`, `M-18`. |
| M-19 | FIXED | Mission card bottom 807.5 px, Journey bottom 838.2 px on an 800 px screen. | Both card bottoms 788 px. Cards scroll internally. WebKit gives the same bottom. | `tree.css:68`, `tree.js:484`, `M-19/mission`, `/journey`. |
| M-20 | FIXED | Clipped branches had no clipping cue. Whole-tree fit reduced shortest branches to about 29 px. | Explicit exploration cue. Reset keeps shortest branches 44 px at 1024 and 1280. | `tree.js:265`, `tree.js:344`, `tree.css:37`, `M-20`, `M-20/targets/*`. |
| M-21 | FIXED within assigned files | Light Tree ids 3.27 to 1, end-link labels 3.43, coming labels 1.98, unbuilt units 2.60. Dark coming labels 2.51 and unbuilt units 3.54. | Minimum 9.80 to 1 across the tested labels, both themes and both phone widths, in both engines. | `tree.css:182`, `learn.css:146`, `learn.css:185`, `M-21/*` and focused contrast guards. |
| M-22 | FIXED | `0.9 AU`, `2.62 hours` and Unicode-minus `-35.8` equivalent rejected. | All three accepted. Wrong unit remains rejected. | `learn.js:127`, `M-22/AU`, `/hours`, `/minus`, `units/wrong`. |
| M-23 | FIXED | Welcome text said Book 3.0. | Version-free welcome. Phone step four identifies the menu. Menu opens after Done. | `tour.js:12`, `M-23/version`, `/menu-copy`, `/menu`. Version guard fails before, menu guards also verify Claude's earlier M-01 fix. |
| M-30 | FIXED | A 500 px downward scroll followed by a 1 px step showed the header again. | Header remains hidden through the 1 px step. | `learn.js:354`, `M-30/320`, `/390`. |
| M-31 | FIXED | Unread timestamp advanced after 4.2 seconds with no acknowledgement. | Timestamp remains unchanged until the reader chooses `Mark updates read`. Button then clears the badge. | `tree.js:95`, `M-31/unread`, `/explicit`, `/read`. |

## Implementation choices

- The tour is now a short modal interaction. Its background cannot move, its focus stays inside, and Skip, Done and Escape restore normal reading. The ring also follows viewport changes. Ordinary test modes explicitly seed the completed-tour mark. Production code runs the tour in automated browsers too.
- The toolbar scrolls with the phone page. This removes the overlap and leaves the reading area available in landscape.
- A branch shows one latest-history shortcut with a distinct large hit area and a count of older entries. Its card still contains the complete history. Six overlapping enlarged dot targets would have made neighboring events hard to select.
- Long canvas labels use measured ellipses. Their full titles remain in accessible names and opened cards.
- Reset restores a readable 44 px minimum branch size. The visible hint explains that branches extend outside the viewport and how to explore. The button is labelled `Reset tree view`. Manual zoom remains available.
- Unread work requires explicit acknowledgement after opening the new-work filter. Four elapsed seconds supplied no evidence that the reader had seen the updates.
- Saved places wait for plots, fonts, images and browser load restoration. New saves include pixel position and viewport width. Older saves and width changes retain fractional-position support.
- Comma input supports short decimal fractions and zero-leading fractions. Three-digit thousands groups such as `2,500` retain their existing meaning. Unit suffixes must match the requested unit or its listed spelling, such as `hour`, `hours` or `h`.

The common engineering issue was lifetime management. A timer, listener or history entry can outlive the interface that created it. These fixes give each transient interface a matching cleanup path for timers, focus, scrolling and its DOM elements.

## Checks performed

- Strict MkDocs build, exit 0. Log `data/astra/019/build-after.log`.
- Chromium repairs, 74 checks passed. `data/astra/019/repairs-after.json`.
- WebKit repairs, 74 checks passed. `data/astra/019/repairs-webkit.json`.
- Original-asset reproduction, 73 checks, 62 failures expected. Each of the 22 assigned issues has a failing guard. `data/astra/019/repairs-before.json`.
- Focused contrast reproduction, 12 of 16 checks failed on the original assets. All 16 passed in Chromium and WebKit after the fixes. This calculation composites CSS colours and opacity in sRGB before computing relative luminance. Logs `contrast-before.json`, `contrast-after.json` and `contrast-webkit.json` under `data/astra/019/`.
- Viewports cover touch-emulated 320 by 568 and 390 by 844, phone landscape 844 by 390, desktop 1280 by 800 and tablet-width 1024 by 800. Colour checks cover both themes. WebKit uses the same explicit mobile and touch settings. Chromium checks background wheel scrolling. Mobile WebKit lacks Playwright wheel support, so its tour scroll-lock check uses a scripted scroll attempt.
- Browser page-error collectors reported zero errors in both repair runs.
- Existing modes passed both runs with 60 layout, 13 Tree, 498 learning, 15 text-floor and 16 chapter checks. Final results are the five correspondingly named JSON files under `data/astra/019/`.
- `node --check` on all three changed application scripts and the test script, plus `git diff --check`, passed. Git prints its existing CRLF conversion warning for the test file.
- Visually inspected the generated 390 px light Tree, 320 px dark sheet, 390 px light Twinlight home, 1280 px light canvas, 1024 px dark WebKit canvas, phone WebKit tour and PC mission card.
- A further Chromium reader-path probe confirms that the PC card bottom is actually painted and selectable, and that choosing Learning from the phone menu after Done opens Twinlight. Both booleans are true in `reader-path-final.json`.
- All five built assets match their final source bytes. Baseline snapshots match HEAD after CRLF normalization. This establishes which versions were exercised. It supplies no independent semantic review. Evidence `asset-verification.json`.
- `verification-summary.json` records all gate outcomes and verifies that none of the 22 assigned issues is missing a failing before check.
- The task's local server was stopped through its own execution session after testing.

Reproduction commands run from the worktree root. The output directory must be absolute for MkDocs.

```powershell
& 'D:\second-sun\.venv-docs\Scripts\mkdocs.exe' build --strict -f book\mkdocs.yml -d D:\second-sun-astra\data\astra\019\site
node research/burn-3-book/tools/serve.mjs --dir=data/astra/019/site --port=8497
node research/burn-3-book/tools/site_check.mjs repairs http://127.0.0.1:8497/ --output=data/astra/019
node research/burn-3-book/tools/site_check.mjs repairs http://127.0.0.1:8497/ --engine=webkit --output=data/astra/019
node research/burn-3-book/tools/site_check.mjs repairs http://127.0.0.1:8497/ --baseline=data/astra/019/before-assets --output=data/astra/019
node research/burn-3-book/tools/site_check.mjs repairs http://127.0.0.1:8497/ --contrast-only=1
```

For each existing mode, use `--site=data/astra/019/site --profiles=data/astra/019/profiles --chrome-no-sandbox=1`. The five modes are `layout`, `tree`, `learn`, `textfloor` and `chapter`.

## What I did NOT check

- Physical iPhone Safari, its on-screen keyboard, screen-reader operation, or an external independent review.
- Scientific lesson contents or planet-search behaviour. Lesson text, lesson numbers and pipeline files were outside this brief.
- Other owners' portions of M-16 and M-21, the live site and cloud-writing modes. No publish or version bump was performed.
- Pre-upgrade Tree history entries store no card identity. Newly created history entries support reopening. Ignoring the old boolean marker has a static type guard, with no separate browser migration test.
- Continue across an edited lesson or a changed browser font setting. Old saves use the settled page fraction when their viewport width is unavailable.

## STOP SIGNS hit

No blocking stop sign. The corrected build-path slip is recorded at the top. Browser tooling was already installed. No package installation was needed.

## QUEUE PROPOSALS

Node 4.1, FIX 99. Claude can close these 22 scoped items after review. The remaining audit items retain their existing owners.

Proposed additional FIX under node 4.1, scope canvas SVG sizing to the canvas element. The additional observation below gives its evidence.

## Additional observation

CONFIRMED, recorded for Claude. A PC card's status icon declares 14 by 14 px and renders at 52.64 by 52.64 px. The existing `.sst-stage svg` sizing rule also applies to SVG icons inside the card. Evidence `data/astra/019/extra-observation.json` and `mission-card-final.png`. The declaration is unchanged in this patch. This additional issue is left in the requested new-bug list.

## IDEAS

None outside the brief.

## Disagreements with Claude

None.

## Questions for Ahmed

None.

## Usage

| Date and brief | Model and effort | Predicted before implementation | Actual | Lesson |
|---|---|---|---|---|
| 15 Nov 2026, 019 | Runtime identity unavailable, brief specifies neither | Approximately 3 weekly points and 30 five-hour points, unmeasured estimates | NOT TESTED, headless runner has no usage panel | Browser service workers must be blocked when comparing intercepted old assets against current assets. |

The brief permits research writes only to the test file and this report, so the usage row is here. No USAGE.md or RESUME.md change.

Next action is Claude's review of the worktree and report before merging, a small review task requiring Claude's first-key authority.
