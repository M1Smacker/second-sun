# Book 3.0 build plan (Claude, 15 Nov 2026, 3:05 am; follows Ahmed's decisions in `REDESIGN-DECISIONS-2026-11-15.md`)

Read this first after any compaction. Tick phases in the log at the bottom. Morning target: the Tree and the learning app with the first lessons live and tested. Everything else is a bonus.

## Rules for the whole night
- Ahmed asleep from about 3:15 am. No questions to him; defaults are written here. Only true stops: a science-rule hit (fence A/B star, sealed-run data, a lead), or a publish that cannot pass its checks.
- Hunt and Petrova work paused. Nothing frozen is touched. The live Eyes page is never clicked; Eyes is tested on a local build only.
- Usage: weekly 26% now, hard cap 60% (Ahmed, 3:16 am; was 40%). Ledger row after every phase. 5-hour limit: when it nears the end, start `tools/wake_at.py` for 1 minute after the reset (next reset 6:30 am Kuwait) and stop cleanly; resume from this file.
- Context can grow to 500K; auto-compact at 600K. RESUME.md and this file carry the state.
- Every piece: build, then test it at once (fix while building), then a full audit at the end. A drop file for every finished piece.
- Sync between phone and PC is SCRAPPED (Ahmed, 3:02 am). Notes, highlights and progress stay on each device.

## Codex: how it is run tonight
- Runner `research/astra/tools/codex_run.py` (built in phase 0): takes an inbox brief, starts `codex.exe exec` in `D:\second-sun-astra` on a new branch `astra/0NN-*`, NEW chat each job, model GPT-6.1 Sol at medium effort (exact model id read from Codex's own config or model cache; a test call proves it), sandbox `workspace-write` (it can write only in its own folder), output to `data/astra/0NN/exec.log`.
- The runner exits when Codex finishes, so it wakes me. If the output says the usage limit is reached, the runner reads the reset time if given (else retries every 30 minutes) and starts the same job again after the reset, then wakes me.
- One Codex job at a time. Codex never pushes. I review every job: fence_check, read the diff, run the tests, then merge or reject. Codex builds small pieces that fit into my big pieces; it never edits the same files I am editing at that moment.
- Planned Codex jobs (in order): 015 drop-builder scenario tests; 016 phone table cards and redirect map; 017 Eyes logic bug list (read-only review of eyes-*.js, I fix); 018 lesson problems drafts; 019 lesson fact-check; 020 full bug hunt on the built site (local server, both sizes).

## Phase 0. Setup (about 0.6 point)
1. `HUNT-PAUSED.md` at the root: exact state of G1, Petrova fixes (adopted set B, held DS, FIX 94/96/70 and others), Codex queue (014a waiting), open decisions for Ahmed, how to resume step by step.
2. Backup of the current book: build main now and keep the output as a frozen copy served at `/v2/` (static files, kept out of search and the menu); tag `book-2-final`.
3. `codex_run.py` and `tools/wake_at.py`; a test call proving the model and the sandbox.
4. Audit of the book's machinery: theme, overrides, service worker and offline cache, `book.js`, publish checks (`site_check.mjs` tests that name pages we will delete must be updated, not deleted).

## Phase 1. The look: Book 3.0 design system (about 2)
Night observatory kept and improved. Deep blue base, cool accent (teal/cyan family), never orange or yellow. Serif for reading, sans for labels. One motion library (CSS plus small JS): page enter and leave, card slides, fades, vine growth, reduced-motion respected. Opening animation with the Second Sun logo (full on the first open of the day, quick fade otherwise, tap to skip). Starfield refined and quieter behind text. Main menu: Tree, Learning; the folded Shelf holds the rest. Phone tables become stacked cards (Codex 016), PC tables stay. Old pages deleted with redirects (Quests, Progress, the Story-so-far set). Version 3.0.0 in the footer and versions page.

## Phase 2. The Drop box and the builder (about 1.5; Codex 015 in parallel)
`research/tree/brain_build.py` reads every file in `drops/` plus `research/TREE.md` and writes generated data only (`book/docs/assets/data/tree.json`, the diary timeline). It REFUSES, never fixes: a missing or unknown field, an unknown node, a bad date, an id with no plain words, a fence A/B star id, sealed-run wording, a lead not marked 'not checked yet', a broken `supersedes` chain, a duplicate. Handles: empty folder, CRLF and BOM, hundreds of drops, renamed nodes (alias table), superseded drops shown as history. A `--check` mode for the publish gate; the publish runs the builder first, so the Tree updates itself every publish. Tests: my unit tests plus Codex's scenario suite (015), each with a mutation that must go red. Fan-out to field notes, versions and RESUME stays by hand for now (later, once the Tree is proven).

## Phase 3. The Tree page (about 2.5)
Built from the decisions plus the three Tree rounds (see REDESIGN-DECISIONS: two views with a toggle, mission tree and journey trunk through time; grows on open; changed branches pulse; a quiet 'N new' badge; search; smooth high-quality zoom and pan, researched first (how the best map and canvas apps do inertia, pinch and zoom-to-point); thickness = importance weight in TREE.md; small status icons; calm card anchored where the branch is on PC (side panel only if that works better), slide-up on phone; leaf cards with a quiet link to the full report; project leaves link to their lesson; no sound). Data from `tree.json` only (no hand-written statuses). Blue glowing vine, active path brighter, side panel on PC, slide-up card on phone, thin vine down the left on phone. Card: plain status, full history, what's next, lesson link; ids small and grey. Diary timeline. Keyboard and screen-reader usable, 44 px taps.

## Phase 4. Research stint RS-035: how to teach this (about 2, a real stint, not rushed)
Questions tied to decisions: how should a lesson be built (worked examples, retrieval practice, cognitive load), what order do the best courses use for this physics, how do good interactive texts mix plots and text, how to write margin notes and problems. Sources: learning-science reviews (for example Dunlosky et al. 2013, Sweller on worked examples), astronomy education research, well-regarded open texts (OpenStax Astronomy 2e), transit and binary star references (Winn 2010; Kepler and TESS mission documentation), the best interactive explainers. Primary pages read, exact sentences pulled, labels, then a lesson template and the full unit outline (data first). Written to `research/stage3/rs035/`, filed in research-sessions.

## Phase 5. The learning app (about 3.5)
Own full-screen space. Home: Continue (exact spot), unit map (done / not done), My notes, Problems due. Reader: full screen on phone (menu hides; tap the top edge), thin progress bar, side contents (swipe in on phone), minimal next and previous. Margin notes; glossary words open a sheet over the page, so the place is never lost; the back gesture also returns to the exact spot. Highlights and notes saved on the device. Typed problems checked instantly, worked solution after. Formulas rendered with KaTeX (served from our own assets). Read-aloud: voice picker (remembered), speed, follow-along sentence highlight with scrolling, tap a paragraph to start there, sleep timer, formulas read in words. Real TESS plots from design stars only (generator refuses fenced and sealed stars).

## Phase 6. Lessons (about 3; Codex 018, 019)
Units and lessons from the RS-035 outline, data first, conversational, full maths built up, worked examples on our real stars, margin notes, end-of-lesson problems. Facts checked against sources while writing; Codex fact-checks each lesson and drafts problems; I check every one. As many as fit; the outline shows the rest as coming.

## Phase 7. Eyes and the update diary (about 0.6; Codex 017 review)
"How it works" folded behind a small label. After an easy or hard test: Try again and Back in view at once; returning restores the exact place, never the bottom or "how it works". Transitions. The update diary pop-up: verified, transition, improved. Tested on a local build only.

## Phase 8. Audit and publish (about 1.5)
Every page at 375 px and 1440 px; every button, transition, return-to-place, offline open, reduced motion, formulas, read-aloud controls; the builder's refusals; redirects; the /v2/ backup. Codex 020 independent bug hunt; I fix. `publish_book.ps1 -Test` (all checks), live page confirmed (not Eyes). Morning report: plain, short, links.

## Scenarios planned for
- Codex limit reached: runner waits for the reset and wakes me; I keep building meanwhile.
- My 5-hour limit: wake script, then resume from this file.
- A Codex job fails or is wrong: rejected, noted in its report and the ledger; I do the piece myself if needed.
- A publish check fails: fix forward (Ahmed's choice); the old book stays at /v2/.
- Compaction mid-phase: RESUME LATEST block names the phase and the next step.
- A drop with bad data: the builder refuses with a plain message; nothing broken reaches the site.
- Weekly near 58%: stop new building, finish testing and publish what is done.

## Safeguards: expect the worst (added 3:13 am, before the go)

### Nothing may hang unseen
- Every background process I start has a hard time limit and exits by itself; none runs open-ended. Each one writes a heartbeat line, and its exit is what wakes me.
- **Codex runner watchdog:** per job a wall-clock limit (2 h default, set per brief) and an idle limit (no new log output and no new file change in its folder for 25 min). On either: it stops ONLY the process tree it started (by its own process id), writes STALL or TIMEOUT with the last log lines, and exits so I wake. I then read the log and either restart once with a narrower brief or do the piece myself.
- Codex runs with approvals off (non-interactive, `approval_policy=never`) so it can never sit waiting for a click; sandbox `workspace-write` so it cannot write outside its folder.
- Before each start: no other Codex process is using `D:\second-sun-astra` (lock file plus a process check); the worktree is clean and on the expected branch. After each job: branch, commits and `git status` checked; uncommitted leftovers reported, never silently kept.
- The Codex executable path is looked up fresh at every start (`Get-AppxPackage *Codex*`), because the app can update itself overnight and move the path.
- **Codex usage limit:** detected from its output. If a reset time is given, the runner waits until 1 minute after it, then restarts the job (at most twice); if no time is given, it retries every 30 min up to 3 h, then gives up and wakes me. While Codex waits, I keep building my own parts.
- A first test call proves the model id (GPT-6.1 Sol, medium), the sandbox and a commit on a scratch branch before any real job. If the model id is refused, fall back to Codex's default model and say so in the morning.

### My own limits
- A wake script runs from the start for 1 minute after each 5-hour reset (next: 6:31 am Kuwait). If my limit cuts a turn, its exit restarts me; I resume from the plan log and RESUME.
- Commit and push small and often (every finished piece), so a cut-off loses minutes, not hours.
- Weekly: stop new building at 58%, finish tests and publish what works. Ahmed's other Claude use shares the meter; outside jumps are noted, not blamed on me.
- Keep-awake requested from the app so Windows does not sleep. If the PC still sleeps or restarts, nothing can resume: the morning report says so plainly.
- Network down: Codex and downloads wait and retry; offline work (code, tests, writing) continues.

### Checkpoint publishes (so the morning shows real progress even if the night breaks)
- Publish after each big phase that passes every check: (1) the look plus the Shelf and redirects, (2) the Tree, (3) the learning app with the first lessons, (4) the final audit. Each publish is the full `publish_book.ps1 -Test`; a failed check stops the push and I fix forward.

### Book edge cases
- **Deleted pages:** every link to Quests, Progress and the Story-so-far set is found and repointed; old addresses get small static redirect pages (no new plugin install); the strict build must pass.
- **Old cached book on his phone:** the offline cache version is bumped; the update path from 2.x to 3.0 is tested with the existing update test (`run_update_test.ps1`) on a local copy, so his home-screen app updates cleanly and never mixes old and new files.
- **Eyes stays safe:** its answers and cloud saving (`eyes-cloud.js`) are not changed in behaviour; only layout, folding, scroll and transitions. Tested only on a local server; the live Eyes page is never clicked.
- **Publish tests** that name deleted pages are updated to the new pages, never just removed; new tests cover the Tree, the reader and the redirects.
- **iPhone Safari and the home-screen app:** no browser Back button there, so an in-app Back everywhere; voices load late, so the voice picker waits for them; viewport height and safe areas handled; reduced motion respected; slow phones get lighter motion.
- **Tree:** the builder never crashes the publish on a bad drop or a malformed TREE.md line: it refuses with a plain message and the publish stops before anything broken goes live. Tested with 1,000 fake drops for speed on a phone.
- **Plots:** the plot generator refuses any fence A/B or sealed-run star; only design stars.
- **Formulas:** KaTeX files served from our own assets (download logged); pages still readable if they fail to load.
- **Backup:** the 2.x book kept at /v2/ and tagged; size checked against the site limit before it goes live.
- **Lessons:** every fact checked against a source while writing; anything not verified is marked in the draft and never published as fact; Codex fact-checks each lesson.

### Morning
- The report is short and plain, opens like a friend saying welcome back (Ahmed asked for a real change, not a rule), says what is live with links, what is not done, what broke and was fixed, Codex jobs and their outcome, and usage.

## Log
- 3:05 am plan written.
- 3:11 am Tree rounds added.
- 3:13 am safeguards added.
- 3:19 am rounds 18 to 20 answered; GO given; weekly cap 60%. Build started.
- 3:20 to 3:33 am PHASE 0 DONE: codex_run.py (headless Codex, new chat, watchdog proven: stall stops its own tree in 1.5 min test; runner commits for Codex because the Windows sandbox blocks git's files; limit wait parsed and tested, test_codex_run.py 8 checks); wake_at.py running for 6:31 am (task bf0pokmo6); HUNT-PAUSED.md; frozen Book 2 in book/archive-v2 (tag book-2-final, byte-exact, publish step 3d copies it to /v2/ BEFORE the link check).
- 3:35 to 3:49 am PHASE 1 DONE (c56e08a): palette deep blue + ice-cyan accent (contrast test passes), Literata serif (font test passes; coverage rebuilt with brotli from scratchpad), logo.svg + icons, splash (CSS-run, skips webdriver), starfield, view transitions, phone table cards, calm chips (14 px for the text floor), update line; menu Tree / Learning / Shelf; shelf.md, training.md; book3_migrate.py removed 47 pages (redirect stubs with ss-redirect meta, 90 links to /v2/), path.yml retired (test_shape says RETIRED), check_site exempts redirects.
- 3:49 to 3:58 am PHASE 2 DONE (a2465b9): research/tree/brain_build.py + node-plain.yml + phases.yml + weights in TREE.md; runs in hooks on every build; test_brain_build.py 21 checks (mutation red); publish step 2b2 now runs it.
- 3:58 am Codex 015 (Eyes flow) DONE, fence-checked (benign flags: quoted RESUME text, own Chrome stops; slip: read C:/Users/hanzl/.agents/skills/transitions-dev, and ran Chrome outside its allowlist: tell Ahmed), merged (459d5cd; conflicts in mkdocs.yml and eyes.md resolved).
- 4:04 am PHASE 3 Tree page DONE in a first version (a46ec2d): tree.js/tree.css; checked in the browser at 1440 and 375: canvas, anchored card, history expand, journey, phone list, sheet, Back closes. Pointer-capture click bug and noon-time 'new' bug fixed.
- NEXT (in order): (a) migrate the publish browser tests (research/burn-3-book/tools/site_check.mjs: PAGES list line 14 and modes layout/chapter/offline/jsoff/headertitle/textfloor still name Book 2 pages; chapter mode -> a field note or later a lesson) and run all 12 modes; (b) checkpoint publish 1 (publish_book.ps1 -Test), confirm live (not Eyes); (c) Phase 4 research stint RS-035; (d) Phase 5 learning app; (e) lessons; (f) Eyes check in browser; (g) audit + Codex bug hunt; (h) morning report. Local test server: node research/burn-3-book/tools/serve.mjs --dir=D:/second-sun/scratch-build --port=8493 (background task bz4f2wig7). In the browser pane, finish animations with document.getAnimations().forEach(a=>a.finish()) before screenshots (the pane freezes animation time).
