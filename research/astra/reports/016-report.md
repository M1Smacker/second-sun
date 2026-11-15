# 016 Book 3 browser tests (Codex, 2026-11-15)

Runtime model and effort are unverified. The brief specifies neither. The related Book 3 plan names Sol medium.

**Inspection slip** An initial broad read of `research/burn-3-book/tools/site_check.mjs` printed an existing Firebase web API-key literal in tool output. Its value is omitted here. No credential file was opened. Narrower source reads followed.

**Plain verdict** 2 issues, both need a book fix. The migration is complete. Of 19 authorized local modes, 17 pass and 2 fail. The 13 publish modes have 11 passes and 2 failures.

**Branch** `astra/016-browser-tests`. No git-writing command was run. The runner handles the commit.

## Findings

1. **CONFIRMED, node 4.1. Small controls fail the existing 44 px target rule.** `layout` completed 60 page/width/theme measurements. At `/`, Mission measures 81 by 36 px, Journey 85 by 36 px, and the search input 290 by 21 px. Desktop zoom controls measure 40 by 40 px. The Tree breadcrumb link measures about 42 by 44 px on the listed Shelf pages. The full output below names every violation. `book/docs/assets/tree.css` lines 14, 17 and 32 set a 36 px button minimum and 40 px search/zoom dimensions. Those causes are confirmed. The breadcrumb's intrinsic width is its LIKELY cause. The publish gate correctly remains red.

2. **CONFIRMED, node 4.1. Tree phone text breaks the 14 px floor.** At 375 by 844 px, `/` has 5 visible headings at 13 px and 19 small labels at 12 px. The other 14 listed pages have no reported floor violations. `textfloor` records the measurements. `book/docs/assets/tree.css` lines 100 and 107 set `.sst-sec h2` and `.sst-item .t small` to those sizes. Claude owns the book correction.

3. **CONFIRMED, node 4.1. The requested Tree interactions work.** At 1440 by 900 px, 24 nodes draw. CDP mouse clicks open one card. Escape and the close button each remove it. Journey draws 5 phases and 18 days. Title-word search dims other branches and clearing it restores them. At 390 by 844 px, a CDP touch opens one sheet, browser history Back removes it and its scrim, and horizontal overflow measures 0 px both open and closed. All 13 assertions pass with no recorded page console errors. A disposable built-asset mutation removed the node class. The test rejected it with exit 1. Restoration returned exit 0. Evidence is `tree.log`, `mutation-tree.log`, `restored-tree.log` and `mutation.json` under `data/astra/016/`.

4. **CONFIRMED, node 4.1. The strict build and retained behavior checks ran locally.** The final build precaches 256 entries, about 5341 KB. Offline mode reads six current pages, runs Tree/Journey and search, and handles unknown pages, unvisited images and a slashless URL. No-JS mode reads 15 pages, exposes the static Tree and toggles native details. Theme changes once per click, both palettes match, and reduced-motion durations are 1 ms against 180 ms toolbar and 520 ms content motion normally. Header title, Eyes, mock cloud, rehearsal and watch timer checks pass. These are producer checks. Claude's independent review is pending.

## What changed and why

- `site_check.mjs` uses 15 current pages, including Tree, Learning, Shelf, Training, diary, reference and lab pages. Static verification confirms they exist without `ss-redirect` markers.
- Added `tree` to mode dispatch and publish step 4b. Kept `chapter` in that list because its 16 responsive overflow checks still apply. They visit the astronomer reference page and the latest diary across the original eight viewport sizes.
- Retired the chapter rail, margin-note sweep, strip, fixed columns and line-length template. The mode prints RETIRED with a reason. The former offline slider and no-JS lesson quiz/demo also print retirement explanations. Tree interaction, static Tree reading and native details replace those checks.
- Reduced-motion measurement uses the Tree toolbar. Book 3 deliberately uses 1 ms reduced durations, so the check accepts at most 1 ms. The previous zero-duration assertion was tied to Book 2.
- Repointed screenshots and header-title pages. Image mode uses the current lab page and eagerly loads its image. The stress fetch uses a root-qualified local asset.
- Eyes results Back now returns to the finished round after brief 015. The test asserts that return, presses Another sitting, then starts hard practice. Update dismissal waits for Book 3's 300 ms exit animation before judging removal.
- Profiles use `data/astra/016/profiles/`. CDP calls have a 20-second timeout and protocol failures propagate. Initialization failure closes the browser owned by the test.
- The update utility changes only the disposable built index and worker, restoring their bytes afterward. It exercises cache replacement without editing source pages.

A useful engineering concept is asynchronous state. An animated close can leave its element in the document briefly. The test checks eventual removal within a bound while still requiring removal to happen.

## Build and execution decisions

The book hook normally regenerates `book/docs/assets/data/tree.json`. To honor the source-edit boundary, `016-build.ps1` supplies `sitecustomize.py` under `data/astra/016/bootstrap/`. It redirects that generated asset to `data/astra/016/generated-tree.json`, and redirects only that asset's reads and copy operation so the build uses fresh data. Static verification confirms the built Tree is byte-identical to the isolated generated asset. That proves identity. Runtime behavior has separate browser evidence.

The harness runs the authorized MkDocs executable from this worktree's `book/` with `build --strict -d <data/astra/016/site>`, then copies `book/archive-v2` into built `/v2/`. All 180 copied archive files match their source bytes. Python bytecode generation is disabled and the process-local cache is under `data/astra/016/`.

Chrome's GPU subprocess failed with access denied in the Windows runner. GPU-disabled and in-process-GPU probes also failed. Successful local runs explicitly opt into `--chrome-no-sandbox=1`, adding `--no-sandbox --disable-gpu` for disposable Chrome profiles. The publish script keeps its normal browser launch. Hardware rendering and normally sandboxed Chrome remain unverified here.

Automatic command-policy review rejected the initial PowerShell `Start-Process` server launch. The Node harness subsequently started and stopped its own local server on port 8494.

## Reproduction

From the worktree root, run these commands in order. The browser harness runs sequentially, records individual logs and a completion file, and stops its server. Its final version returns a nonzero suite exit for a failing mode. The mutation run exercised that failure path.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File research/astra/scripts/016-build.ps1
node research/astra/scripts/016-run.mjs
D:/second-sun/.venv/Scripts/python.exe research/astra/scripts/016-verify.py
node research/astra/scripts/016-mutation.mjs
```

`016-migrate.py` records the initial one-shot transformation and refuses reapplication after migration. Final review-driven edits are in the tool files.

## Checks and limitations

Node syntax checks ran for `site_check.mjs`, `016-run.mjs` and `016-mutation.mjs`. PowerShell parsing reported 0 errors for the publish script and build harness. `git diff --check` reported no whitespace errors. Read-only git checks confirmed the branch. `git diff --numstat -- book pipeline` produced no changes. These static checks exclude semantic validation of unexecuted publication code.

## What I did NOT check

- `eyesreal` is NOT TESTED. It enables writes to the real Firebase service, prohibited by AGENTS.md sections 4.4 and 4.5. Both cloud modes exercised above use local mocks.
- Live publication, the live Eyes page, real cloud scores, Safari/iPhone hardware and normally sandboxed/GPU-backed Chrome are NOT TESTED.
- Full accessibility, every interaction state, archive navigation semantics and scientific content are NOT TESTED by this migration. Phone Mission and desktop Journey screenshots were visually inspected. Screenshot generation alone supplies no layout verdict.
- Image mode caches one content image within the 150-image bound. Eviction beyond 150 entries remains NOT TESTED.
- Update testing covers browser cache lifecycle through built-output mutations. A multi-build publication transaction is NOT TESTED.
- The headless runner exposes no usage meter. Actual five-hour and weekly usage are unavailable.

## STOP SIGNS hit

The real-cloud mode is excluded under the existing Firebase prohibition. All 19 local modes ran. The two book defects are handed back to Claude under the brief's source-edit boundary.

## QUEUE PROPOSALS

- FIX, node 4.1. Bring Tree toolbar, search, zoom controls and the Tree breadcrumb to the existing 44 px target rule. The evidence is the failing `layout` output.
- FIX, node 4.1. Bring Tree phone section headings and small labels to the existing 14 px floor. The evidence is the failing `textfloor` output.

## IDEAS

None.

## Disagreements with Claude

None. The brief's expectation that Eyes already passed was superseded by the results-return behavior from 015. The migrated test follows that behavior and passes.

## Questions for Ahmed

None.

## Usage

Predicted 25 five-hour points and 5 weekly points, logged before implementation. Actual unavailable. The lesson is to diagnose browser startup from stderr and wait for animated dismissal before judging removal. The completion row is in `research/astra/USAGE.md`.

## Recorded outputs

### Static verification

```text
Book 3 canonical pages exist without redirect markers: 15
Publish list includes Tree and retained responsive chapter checks
Built Tree is byte-identical to this build's isolated generated asset
Archive copy has matching bytes for 180 files
These static checks establish routing and byte identity. Browser behavior is recorded separately.
```

### layout FAIL, exit 1

```text
{"mode":"layout","checks":60,"overflow":[],"small":["390 slate /: button. 81x36 'Mission'","390 slate /: button. 85x36 'Journey'","390 slate /: input. 290x21 'Search the Tree'","390 slate shelf/: a.md-path__link 42x44 'Tree'","390 slate training/: a.md-path__link 42x44 'Tree'","390 slate candidates/: a.md-path__link 42x44 'Tree'","390 slate eyes/: a.md-path__link 42x44 'Tree'","390 slate rehearsal/: a.md-path__link 42x44 'Tree'","390 slate glossary/: a.md-path__link 42x44 'Tree'","390 slate claims/: a.md-path__link 42x44 'Tree'","390 slate field-notes/: a.md-path__link 42x44 'Tree'","390 slate field-notes/2026-11-14/: a.md-path__link 42x44 'Tree'","390 slate watch/: a.md-path__link 42x44 'Tree'","390 slate versions/: a.md-path__link 42x44 'Tree'","390 slate reference/for-astronomers/: a.md-path__link 42x44 'Tree'","1280 slate /: button. 81x36 'Mission'","1280 slate /: button. 85x36 'Journey'","1280 slate /: input. 290x21 'Search the Tree'","1280 slate /: button. 40x40 '+'","1280 slate /: button. 40x40 '−'","1280 slate /: button. 40x40 '⌖'","1280 slate shelf/: a.md-path__link 42x44 'Tree'","1280 slate training/: a.md-path__link 42x44 'Tree'","1280 slate candidates/: a.md-path__link 42x44 'Tree'","1280 slate eyes/: a.md-path__link 42x44 'Tree'","1280 slate rehearsal/: a.md-path__link 42x44 'Tree'","1280 slate glossary/: a.md-path__link 42x44 'Tree'","1280 slate claims/: a.md-path__link 42x44 'Tree'","1280 slate field-notes/: a.md-path__link 42x44 'Tree'","1280 slate field-notes/2026-11-14/: a.md-path__link 42x44 'Tree'","1280 slate watch/: a.md-path__link 42x44 'Tree'","1280 slate versions/: a.md-path__link 42x44 'Tree'","1280 slate reference/for-astronomers/: a.md-path__link 42x44 'Tree'","390 default /: button. 81x36 'Mission'","390 default /: button. 85x36 'Journey'","390 default /: input. 290x21 'Search the Tree'","390 default shelf/: a.md-path__link 42x44 'Tree'","390 default training/: a.md-path__link 42x44 'Tree'","390 default candidates/: a.md-path__link 42x44 'Tree'","390 default eyes/: a.md-path__link 42x44 'Tree'","390 default rehearsal/: a.md-path__link 42x44 'Tree'","390 default glossary/: a.md-path__link 42x44 'Tree'","390 default claims/: a.md-path__link 42x44 'Tree'","390 default field-notes/: a.md-path__link 42x44 'Tree'","390 default field-notes/2026-11-14/: a.md-path__link 42x44 'Tree'","390 default watch/: a.md-path__link 42x44 'Tree'","390 default versions/: a.md-path__link 42x44 'Tree'","390 default reference/for-astronomers/: a.md-path__link 42x44 'Tree'","1280 default /: button. 81x36 'Mission'","1280 default /: button. 85x36 'Journey'","1280 default /: input. 290x21 'Search the Tree'","1280 default /: button. 40x40 '+'","1280 default /: button. 40x40 '−'","1280 default /: button. 40x40 '⌖'","1280 default shelf/: a.md-path__link 42x44 'Tree'","1280 default training/: a.md-path__link 42x44 'Tree'","1280 default candidates/: a.md-path__link 42x44 'Tree'","1280 default eyes/: a.md-path__link 42x44 'Tree'","1280 default rehearsal/: a.md-path__link 42x44 'Tree'","1280 default glossary/: a.md-path__link 42x44 'Tree'","1280 default claims/: a.md-path__link 42x44 'Tree'","1280 default field-notes/: a.md-path__link 42x44 'Tree'","1280 default field-notes/2026-11-14/: a.md-path__link 42x44 'Tree'","1280 default watch/: a.md-path__link 42x44 'Tree'","1280 default versions/: a.md-path__link 42x44 'Tree'","1280 default reference/for-astronomers/: a.md-path__link 42x44 'Tree'"],"schemeMismatch":[],"inlineExempt":["a","ss3-shelf__item ss-reveal is-in","ss3-deck__card ss-reveal is-in","ss-chip ss-chip--verified","ss-chip ss-chip--likely","ss-chip ss-chip--unverified"],"toggle":{"before":"default","after":"slate","changes":1,"ready":true,"bodyTransition":"0.2s, 0.2s, 0.2s"},"reducedMotion":{"body":"0.001s","content":"none","contentDuration":"0.001s","toolbar":"0.001s"},"normalMotion":{"content":"ss3-enter 0.52s","toolbar":"0.18s","link":"0.18s, 0.18s"},"hiddenShown":0,"paletteToggles":1,"errors":[],"pass":false}
```

### tree PASS, exit 0

```text
{"mode":"tree","checks":13,"fails":[],"nodes":24,"journey":{"phases":5,"days":18},"search":{"word":"How","id":"1"},"phoneOverflowOpen":0,"phoneOverflowClosed":0,"errors":[],"pass":true}
```

### chapter PASS, exit 0

```text
RETIRED chapter template: Book 3 removed the chapter rail, margin-note sweep, chapter strip and fixed chapter-column template, including its line-length and column-width rules.
{"mode":"chapter","retired":"Book 3 removed the chapter rail, margin-note sweep, chapter strip and fixed chapter-column template, including its line-length and column-width rules.","checks":16,"fails":[],"errors":[],"pass":true}
```

### eyeslayout PASS, exit 0

```text
{"mode":"eyeslayout","checks":120,"fails":[],"sizes":[{"tag":"390x844","cvh":178,"cvw":324,"rowH":60,"bannerB":697,"nextB":757},{"tag":"683x325","cvh":278,"cvw":506,"rowH":60,"bannerB":730,"nextB":317},{"tag":"1024x768","cvh":278,"cvw":506,"rowH":60,"bannerB":734,"nextB":760},{"tag":"1366x650","cvh":293,"cvw":532,"rowH":60,"bannerB":482,"nextB":542},{"tag":"1440x900","cvh":293,"cvw":532,"rowH":60,"bannerB":581,"nextB":641}],"errors":[],"pass":true}
```

### offline PASS, exit 0

```text
RETIRED offline slider: the Book 2 dip-depth demo has no Book 3 page. Offline Tree interaction is checked instead.
{"mode":"offline","precached":true,"shell":"256 / 256","firstVisitNavigations":1,"pages":{"/":{"title":"Second Sun - Second Sun","css":1572,"controlled":true,"text":1077},"candidates/":{"title":"Candidates - Second Sun","css":1448,"controlled":true,"text":516},"glossary/":{"title":"Glossary - Second Sun","css":1448,"controlled":true,"text":11277},"claims/":{"title":"Facts (claims register) - Second Sun","css":1448,"controlled":true,"text":37339},"shelf/":{"title":"The Shelf - Second Sun","css":1448,"controlled":true,"text":542},"training/":{"title":"Training deck - Second Sun","css":1448,"controlled":true,"text":714}},"treeReady":true,"treeOffline":true,"search":10,"unknownPage":true,"unvisitedImage":true,"noSlashOffline":{"url":"http://127.0.0.1:8494/learn/","title":"Learning - Second Sun"},"errors":[],"pass":true}
```

### jsoff PASS, exit 0

```text
RETIRED jsoff lesson quiz/demo: Book 2 lesson removed. Book 3 static Tree, native details and reading/navigation are checked instead.
{"mode":"jsoff","pages":{"/":{"noJS":true,"text":3374,"links":1,"redirect":false},"learn/":{"noJS":true,"text":82,"links":2,"redirect":false},"shelf/":{"noJS":true,"text":542,"links":12,"redirect":false},"training/":{"noJS":true,"text":714,"links":14,"redirect":false},"candidates/":{"noJS":true,"text":516,"links":2,"redirect":false},"eyes/":{"noJS":true,"text":1136,"links":5,"redirect":false},"rehearsal/":{"noJS":true,"text":1317,"links":2,"redirect":false},"glossary/":{"noJS":true,"text":11277,"links":116,"redirect":false},"claims/":{"noJS":true,"text":37339,"links":218,"redirect":false},"field-notes/":{"noJS":true,"text":2820,"links":17,"redirect":false},"field-notes/2026-11-14/":{"noJS":true,"text":2534,"links":3,"redirect":false},"watch/":{"noJS":true,"text":2891,"links":6,"redirect":false},"versions/":{"noJS":true,"text":13163,"links":6,"redirect":false},"labs/lab3-plot-and-read/":{"noJS":true,"text":3612,"links":11,"redirect":false},"reference/for-astronomers/":{"noJS":true,"text":2716,"links":15,"redirect":false}},"checks":15,"fails":[],"staticTree":true,"details":{"exists":true,"before":false,"after":true,"text":327},"errors":[],"pass":true}
```

### eyes PASS, exit 0

```text
{"mode":"eyes","phone":[{"over":0,"small":0},{"over":0,"small":0},{"over":0,"small":0}],"errors":[],"checks":{"started":true,"noOldPromise":true,"answered0":true,"next0":true,"answered1":true,"next1":true,"backButtonShown":true,"lookBackReadOnly":true,"cannotGoBeforeFirst":true,"returnedToLive":true,"answersUnchangedByLooking":true,"answered2":true,"next2":true,"answered3":true,"next3":true,"answered4":true,"next4":true,"easyFeedbackLines":true,"bannerSaysTruth":true,"lookBackShowsTruthAndAnswer":true,"measuredStrengthSaved":true,"practiceSaved":true,"lookBacksRecorded":true,"finishScreen":true,"noUploadFromTestCopy":true,"scoreLineFirst":true,"reviewOpens":true,"reviewCloses":true,"testHidesTruth":true,"testFinish":true,"testFinishDetails":true,"testScoreLine":true,"testSaved":true,"habitTable":true,"resultsAfterReload":true,"abandonedKept":true,"resultsTable":true,"noCopyOption":true,"exportApiForTheUpload":true,"hardButtons":true,"hardTestHidesTruth":true,"hardFinish":true,"hardFinishDetails":true,"hardReviewShowsNumbers":true,"hardTestSaved":true,"hardInResults":true,"resultsDetailsClosed":true,"resultsReturnToFinish":true,"hardPracticeStarts":true,"hardPracticeShowsTruth":true,"plotBarExplained":true,"hardPracticeFeedback":true,"twinButton":true,"twinDrillRuns":true,"twinDrillSavesNothing":true,"phoneLayout":true,"noConsoleErrors":true},"failed":[],"pass":true}
```

### eyescloud PASS, exit 0

```text
{"mode":"eyescloud","mock":{"calls":5,"docs":4},"errors":[],"checks":{"visitorStatus":true,"visitorSendsNothing":true,"ownerLinkWorks":true,"statusAtStart":true,"roundSentAtOnce":true,"shapeAcceptedByRules":true,"statusSaysSafe":true,"noCopyOrSendStep":true,"sentMatchesScreen":true,"offlineWaits":true,"sentWhenInternetReturns":true,"statusAfterReturn":true,"serverBusyThenRetried":true,"abandonedRoundSentAfterReload":true,"everyRoundExactlyOnce":true,"noLoopOrResend":true,"noConsoleErrors":true},"failed":[],"pass":true}
```

### rehearsal PASS, exit 0

```text
{"mode":"rehearsal","checks":73,"fails":[],"sizes":[{"tag":"390x844","p1":94,"p2":216,"p3":43},{"tag":"768x1024","p1":192,"p2":439,"p3":88},{"tag":"1440x900","p1":183,"p2":419,"p3":84}],"errors":[],"pass":true}
```

### rehearsalcloud PASS, exit 0

```text
{"mode":"rehearsalcloud","checks":12,"fails":[],"errors":[],"pass":true}
```

### watchtimers PASS, exit 0

```text
{"mode":"watchtimers","checks":7,"fails":[],"requests":{"onPageIn16s":3,"awayIn12s":0},"errors":[],"pass":true}
```

### headertitle PASS, exit 0

```text
{"mode":"headertitle","checks":3,"fails":[],"pages":{"shelf/":{"top":{"n":2,"first":true,"second":false,"text":"SECOND SUN"},"down":{"n":2,"first":true,"second":false,"text":"SECOND SUN"}},"reference/for-astronomers/":{"top":{"n":2,"first":true,"second":false,"text":"SECOND SUN"},"down":{"n":2,"first":true,"second":false,"text":"SECOND SUN"}},"field-notes/2026-11-14/":{"top":{"n":2,"first":true,"second":false,"text":"SECOND SUN"},"down":{"n":2,"first":true,"second":false,"text":"SECOND SUN"}}},"errors":[],"pass":true}
```

### textfloor FAIL, exit 1

```text
{"mode":"textfloor","checks":15,"fails":[": h2 13px x5; small 12px x19"],"pages":{"":{"h2":{"n":5,"px":13},"small":{"n":19,"px":12}}},"errors":[],"pass":false}
```

### redirect PASS, exit 0

```text
{"mode":"redirect","online":{"url":"http://127.0.0.1:8494/learn/","redirects":1},"offline":{"url":"http://127.0.0.1:8494/glossary/","redirects":1,"title":"Glossary - Second Sun"},"pass":true}
```

### update PASS, exit 0

```text
{"mode":"update","aReady":true,"versionA":"ss-shell-6839794d062b","freshB":true,"lineShown":true,"linesAfter2s":1,"barDismissible":true,"navigationsForB":1,"cachesWithB":["ss-shell-626f6f6b332d746573742d42","ss-shell-6839794d062b"],"freshC":true,"prunedB":true,"cachesWithC":["ss-shell-626f6f6b332d746573742d43","ss-shell-6839794d062b"],"reloadsAfterClick":1,"onC":true,"cachesAfter":["ss-shell-626f6f6b332d746573742d43"],"lineAfterReload":0,"offlineAfter":{"title":"Glossary - Second Sun","css":1448,"controlled":true,"text":11277},"errors":[],"pass":true}
```

### fail404 PASS, exit 0

```text
{"mode":"fail404","failing":"training/","precached":true,"installMs":2585,"shell":"254 cached, 254 expected (shell 256 minus the forced 404s)","state":"activated","otherPageOffline":{"title":"Glossary - Second Sun","css":1448,"controlled":true,"text":11277},"failedPageOffline":"404 page shown","pass":true}
```

### images PASS, exit 0

```text
{"mode":"images","cap":150,"imagesOnPage":3,"imageCache":1,"pass":true}
```

### shots PASS, exit 0

```text
{"mode":"shots","files":["D:\\second-sun-astra\\data\\astra\\016\\shots/home-390-dark.png","D:\\second-sun-astra\\data\\astra\\016\\shots/home-390-light.png","D:\\second-sun-astra\\data\\astra\\016\\shots/training-390-dark.png","D:\\second-sun-astra\\data\\astra\\016\\shots/eyes-details-390-dark.png","D:\\second-sun-astra\\data\\astra\\016\\shots/search-open-390-dark.png","D:\\second-sun-astra\\data\\astra\\016\\shots/shelf-1280-dark.png","D:\\second-sun-astra\\data\\astra\\016\\shots/shelf-1280-light.png","D:\\second-sun-astra\\data\\astra\\016\\shots/search-1280-light.png","D:\\second-sun-astra\\data\\astra\\016\\shots/claims-390-light.png","D:\\second-sun-astra\\data\\astra\\016\\shots/journey-1280-dark.png"],"errors":[],"pass":true}
```

### hammer PASS, exit 0

```text
{"mode":"hammer","loaded":true,"controlled":false,"where":"http://127.0.0.1:8494/shelf/ | The Shelf - Second Sun","result":{"requests":120,"ok":120,"fail":0,"timeout":0,"errs":{},"slowOver1s":0,"totalMs":402},"pass":true}
```

### eyesreal BLOCKED by the Firebase prohibition

No runtime output. This mode was excluded before invocation.

### Mutation verification

```json
{
  "brokenAssetExit": 1,
  "restoredAssetExit": 0,
  "rejectedMissingNodes": true,
  "restoredPass": true
}
```

Next, Claude reviews this report before publication because two UI gates remain red. Review usage is unmeasured and needs Claude.

DONE, browser-test migration and authorized local verification are complete, with two book defects reported for Claude.
