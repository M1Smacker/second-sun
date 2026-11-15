# 015 Eyes flow fixes (Codex, runtime model and effort unverified, 2026-11-15 03:56 +0300)

**Path slip** The local browser probes invoked `C:/Program Files/Google/Chrome/Application/chrome.exe`, outside the executable paths listed in AGENTS.md section 4.12. The brief requested local browser checks, but said AGENTS.md wins. I should have treated that executable as a path stop. Probe profiles and generated files were confined to `data/astra/015/`.

The brief specifies no model or effort. The related Book 3 plan requests Sol medium. This headless runner exposes neither the active model name nor the usage panel.

**Plain verdict** Flow changes implemented. All six required Node suites pass, totaling 115 checks. The flow regression passes 41 simulated DOM checks. Contrast passes. A strict build and real-browser layout verification remain pending.

**Branch** `astra/015-eyes-flow`, the supplied branch. Worktree changes are ready for the runner.

## Findings and root causes

1. **CONFIRMED, Tree node 4.4.** In the original `book/docs/assets/demos.js:447`, `showFinish()` appended detailed result sections before its action row. The action row at original line 453 could therefore appear far below the score. Replacing the stage did not scroll or focus the new result. Current `demos.js` places the action row immediately after the score and schedules result-heading focus and a header-offset scroll. Evidence from `015-flow-regression.mjs` includes standard, hard and practice finishes, action order and focus/scroll calls. Actual viewport fit is NOT TESTED.

2. **CONFIRMED, Tree node 4.4.** Original `demos.js:294` rebuilt the menu without recording its departure position. Original `demos.js:491` also routed history Back to that menu, even when entered from a finish screen. Review return at original line 408 rebuilt the finish without restoring a position. `book/docs/assets/book.js:252` delegates the header Back button to `history.back()`, with no widget-specific restoration. These code paths explain the missing explicit return point. The precise browser cause of Ahmed landing at the bottom or explanation is UNCERTAIN because his phone behavior was not reproduced.

3. **CONFIRMED in simulation, Tree node 4.4.** `eyes-flow.js` saves pixel coordinates and focus separately. Home, question look-back, finish review and My results have explicit return destinations. For Material instant navigation, idle widgets retain their DOM and closures in memory, and return with the recorded scroll position. The correct saved-round store is reattached to the existing cloud API on resume. Other-tab storage changes invalidate this cache. Active unfinished rounds use the existing loader path. Tests cover these routes, rehearsal finish and return, store binding with a stub, and reduced motion.

4. **CONFIRMED by source comparison, Tree node 4.4.** Both How it works sections are closed native details elements with short guidance. Existing detailed wording is retained verbatim in a nested fold. `data/astra/015/guidance-check.log` records the comparison against HEAD.

5. **CONFIRMED by source and simulated motion calls, Tree node 4.4.** Card changes and result entry use a 200 ms fade with a 6 px slide. The help fold uses a 200 ms fade/slide on opening. Reduced-motion settings suppress these animations. Scroll moves are immediate so they cannot outlive a subsequent screen change. Actual animation appearance is NOT TESTED.

Scroll anchoring is the browser's adjustment when content changes height. Explicit coordinates, disabled widget anchoring and focus with `preventScroll` give the widget a defined return point. Real-browser testing is still needed to verify its interaction with Material's own restoration.

## Files changed

- `book/docs/assets/eyes-flow.js`, shared scroll, focus, motion and instant-navigation helpers.
- `book/docs/assets/demos.js`, the actual Eyes UI entry points, finish controls and return destinations.
- `book/docs/assets/rehearsal.js`, session finish and return flow.
- `book/docs/assets/shape.css`, help motion, summary sizing, action spacing and anchoring.
- `book/docs/eyes.md` and `book/docs/rehearsal.md`, folded guidance.
- `book/mkdocs.yml`, loads the flow helper before its callers.
- `research/astra/scripts/015-flow-regression.mjs`, reproducible simulated DOM regression, baseline and mutation checks.
- `research/astra/scripts/015-flow-check.mjs`, local browser-check wrapper. It confines scratch profiles to `data/astra/015/` and adapts the legacy history-return navigation step to the new finish-return flow. It requires a built site.
- `research/astra/scripts/015-fold-help.py`, idempotent content transformation used for the folds.
- `research/astra/USAGE.md` and this report.

## Verification actually performed

These are producer checks. No independent review was performed.

- Runtime Node suites, 115 checks total. Each command exited 0.
- Contrast arithmetic with the allowed `D:\second-sun\.venv\Scripts\python.exe`, exit 0.
- Simulated DOM regression through the real `eyesEngine` and rehearsal `mount`, 41 checks, exit 0. The mock does not calculate browser layout.
- Baseline regression using `git show HEAD:book/docs/assets/demos.js`, exit 1 at the missing finish focus assertion.
- Deliberate mutation disabling `flow.move`, exit 1 at the same assertion.
- `node --check` on all three changed UI JavaScript files and the browser wrapper, exit 0.
- `git diff --check`, exit 0. Git emitted LF/CRLF conversion warnings.
- Original detailed guidance comparison against HEAD, pass for both pages.

### Required test outputs

#### node book/tools/test_eyes.mjs

```text
pass: the official test has exactly 10 clear dips, 4 faint, 8 quiet and 8 odd, and differs between shuffles
pass: practice rounds have the length asked for and always include a quiet curve
pass: the banner always says what it truly was: A DIP or NOT A DIP, with the reason, whatever the answer
pass: scoring: right, wrong, partly right (not a dip but the wrong kind) and not sure
pass: every answer is saved at once: a fresh store on the same storage sees it
pass: an answer can never be changed, repeated, skipped or added after the round ends
pass: looking back counts the look but never touches the answer
pass: a round left half done is kept as abandoned, an empty one is dropped
pass: unreadable saved data is never silently overwritten
pass: when the device refuses to save, the screen is told and the round still works in memory
pass: listeners hear about saves (the cloud upload will use this) and cannot break saving
pass: summary counts: clear and faint dips, false alarms, odd things, looks
pass: Wilson range behaves: 17 of 20 is about 64% to 95%, 0 of 0 is the whole range
pass: pass line: needs 2 rounds, 60 curves and 2 days before it says anything
pass: pass line: below the line when clear dips are missed or quiet curves are called dips; faint dips do not count
pass: pass line ignores practice rounds and unfinished test rounds
pass: export round-trips and holds every round with its answers
pass: a round marked as synced leaves the unsent list; a round still open can never be marked
pass: the cloud document has exactly the keys the published rules allow, with the right types
pass: encoding: integers, decimals, text, booleans, nulls, lists and maps survive a round trip
all 20 Eyes core checks passed
```

#### node book/tools/test_eyes_cloud.mjs

```text
pass: a finished round is sent once, in the shape the rules accept, and marked as synced
pass: a round still open is never sent; sending starts the moment it finishes
pass: offline: the round waits, nothing is lost, and it goes out when the internet returns
pass: network errors back off 5 s, 15 s, 60 s, 5 min and then recover without losing the round
pass: no duplicates: if the cloud stored a round but the answer was lost, the resend gets 409 and counts as stored
pass: a refused round (403) stays queued, does not block the others, and is retried slowly
pass: busy or down server (429, 503) is treated like being offline
pass: calling flush many times at once sends each round once
pass: several rounds waiting go out oldest first, and abandoned rounds are sent too
pass: syncing does not trigger more sending (no loop), and the status listener hears every change
pass: a paused uploader (a test copy of the book) never sends anything, whatever happens
pass: a visitor can play but nothing is ever sent, and the line says so
pass: who is an owner: a device with rounds before the rule, or the #owner link; a visitor stays a visitor even after playing
pass: the status line is honest before any round exists
all 14 Eyes cloud checks passed
```

#### node book/tools/test_eyes_hard.mjs

```text
pass: the star's own noise is measured sensibly
pass: a card is rebuilt exactly from its seed, and different seeds give different cards
pass: hard-noise cards hold the best dip of a whole sector, far better looking than an ordinary stretch
pass: the event does not sit in the same place on every kind of card (position must not give the answer away)
pass: leak audit: where the event sits, how many holes the card has and how strong the rivals are do not tell a hard-noise card from a faint fake planet; width tells only a little
pass: a fake planet is as strong as it says it is, on the detector's scale
pass: the dip is really in the data, with sloping sides and a flat bottom
pass: the official hard test has exactly the agreed mix, and every strength is inside its band
pass: a dip at a gap really ends where the data stops, and a down-jump never recovers
pass: a gap alone is no giveaway: other cards have gaps too, never touching the event, and only the gap-dip card has a dip that ends at one
pass: an eclipse card is a real eclipse of this star, levelled, and deep
pass: twin drill: the same noise twice, the planet in one only, the planet curve stronger, rebuilt exactly from its seed
pass: hard scoring counts each tier, and Not sure is a miss on a clear fake planet but free on hard noise
pass: one fact, one place: the hard line block states the clear-planet and hard-noise numbers once, the round block still has its own (F4, 27 Oct 2026)
pass: results view: a false-alarm rate above the limit is said to be above the limit, never softened; clear dips above the target say so
pass: results view: near a target the wording follows the confidence interval, not the point estimate
pass: results view: the pill never calls a practice result a pass; the line and the hard line stay separate; nothing without test rounds
pass: results view: the weak spot is a pattern to check and only appears when it is at least 10% of at least 20 jumps and gaps; trend is per test, oldest first
pass: the hard line: not enough, then meets, then below; the numbers are the ones fixed in advance
pass: the old pass line and the hard line never see each other's rounds
pass: an answer to a hard card is saved with its tier, an answer to an old card is saved exactly as before, and the cloud shape is unchanged
pass: the banner for hard cards says what they truly were
all 22 Eyes hard-test checks passed
```

#### node book/tools/test_eyes_strength.mjs

```text
pass: the same numbers as the Python box_scores on every golden array and every hunt duration
pass: the hunt durations are whole numbers of ten-minute bins
pass: a deep dip is found where it is, strongest at about its own length, and a card scored with the sector's scale agrees with the array's own scale
pass: a noise-free dip of unit depth scores depth over the scale of the best box
pass: a short or gappy array is handled: no scale from fewer than 20 boxes, and a box missing 20 percent of its points is skipped
all 5 Eyes strength checks passed
```

#### node book/tools/test_eyes_feedback.mjs

```text
pass: every measurement is a finite number or a plain label, the same every time, and fast
pass: one strength everywhere: the feedback's strength is the card's own strength from the hunt's function
pass: every text is three lines of 36 to 44 words with no dashes, on every kind of card, every answer and both modes
pass: only measured numbers appear: every number in a text is one the card was measured to have (or a fixed line like 7)
pass: the lead lesson and the measurement line never look at the true label
pass: a false alarm is never called a miss: 'You said Dip' on noise, and 'missed' appears nowhere
pass: real mode gives measurements, not a verdict: no 'it was', 'right', 'hidden planet' or 'wrong' in any real-mode text
pass: artifact lessons fire on their own kind of card and almost never on ordinary ones
pass: a card that nearly matches an artifact is not called plain noise, and the near-miss lesson is rare on ordinary cards
pass: the sentences do not repeat: 60 hard-noise cards in one sitting give many different lines, with the numbers masked
pass: the pattern line speaks about Ahmed's own habit, at most once every six cards
pass: easy-sitting cards (real windows with box fakes) get valid texts too
pass: a faint brightening just under its test line is never called plain noise: it is 'close to' and not classified
pass: an answer is saved with the measured strength of its card (field f), and a card without one is saved exactly as before
pass: his own habit by strength: counts per band, d-prime and criterion from measured answers only, and an honest message when nothing is measured yet
pass: a miss comes back 3 to 5 cards later, only unseen cards move, and the round keeps exactly the same cards
all 16 Eyes feedback checks passed
```

#### node book/tools/test_rehearsal.mjs

```text
pass: six answers, each with a label
pass: d-prime for 80% hits and 10% false alarms is about 2.1 (got 2.06)
pass: equal rates give 0 and perfect scores stay finite
pass: no planets or no others: not measured
pass: Wilson interval for 8 of 10
pass: entries: right, planet-like call, tier and strength kept
pass: summary counts hits, false alarms and classes
pass: reveal: a planet call on nothing is a false alarm
pass: reveal: hit, miss, and near-limit wording
pass: eight good sessions on eight days meet the line (d-prime 2.38)
pass: seven sessions are not enough
pass: eight sessions on one day are not enough (needs four days)
pass: 6 false alarms in 14 others (43%) is below the line
pass: one clear fake in three found is below the line
pass: an abandoned session does not count
pass: the next session follows the number finished, cycling after eight
pass: 300 random orders: 20 items each, no two neighbours from one star
pass: a round is mode practice, source rehearsal-v1, version 1 (the published cloud rules accept it)
pass: skipping ahead is refused
pass: an unknown answer is refused
pass: the first answer is kept; a second answer to the same item is refused (answers cannot be changed)
pass: an open round is never offered to the cloud
pass: a finished round is offered once and cannot be finished twice
pass: the cloud document has only the allowed keys, an allowed mode, at most 200 answers
pass: the document encodes for Firestore with the source tag and every answer
pass: a synced round is not sent again
pass: a half-done session is kept as abandoned; an empty one is dropped
pass: the three panels draw identically whatever the hidden class (they cannot leak it)
pass: panel 2 is an svg with the data lines and the event bracket and no class words
pass: panel 1 marks the event and panel 3 marks the phase
pass: the deck has 8 sessions of 20 items
pass: every session: 3 clear and 3 near-limit fake planets, 3 eclipses, 3 instrument, 2 flares, 2 steps, 4 nothing-hidden
pass: no item carries a field outside the allowed list (no TIC, no sector, no time stamp)
pass: arrays have the length the window says; box lengths are the hunt's grid
pass: the deck holds 69 different star-sectors
pass: fake planets carry their depth; clear ones are strong (13 or more), near-limit ones are under 10
pass: the deck is 1.02 MB (limit 1.6)
pass: mutation: a line looking only at fake planets found would pass a player who calls everything a planet; the real line does not

all 38 rehearsal checks passed
```

#### Contrast

Command used `D:\second-sun\.venv\Scripts\python.exe -B book/tools/test_contrast.py`.

```text
contrast ok: text, secondary text and accent are at least 7:1 on every surface in both schemes
```

### Flow regression output

Command used `node research/astra/scripts/015-flow-regression.mjs`.

```text
pass: Take the official test (30 curves), look-back restores question position
pass: Take the official test (30 curves), finish heading focused
pass: Take the official test (30 curves), finish controls immediately after score
pass: Take the official test (30 curves), finish scrolled below header
pass: Take the official test (30 curves), review restores exact finish position
pass: Take the official test (30 curves), review restores its launch control focus
pass: Take the official test (30 curves), results returns to finish
pass: Take the official test (30 curves), results restores its launch control focus
pass: Take the official test (30 curves), home position and launcher focus restored
pass: Take the HARD test (30 curves), look-back restores question position
pass: Take the HARD test (30 curves), finish heading focused
pass: Take the HARD test (30 curves), finish controls immediately after score
pass: Take the HARD test (30 curves), finish scrolled below header
pass: Take the HARD test (30 curves), review restores exact finish position
pass: Take the HARD test (30 curves), review restores its launch control focus
pass: Take the HARD test (30 curves), results returns to finish
pass: Take the HARD test (30 curves), results restores its launch control focus
pass: Take the HARD test (30 curves), home position and launcher focus restored
pass: 5, look-back restores question position
pass: 5, finish heading focused
pass: 5, finish controls immediately after score
pass: 5, finish scrolled below header
pass: 5, review restores exact finish position
pass: 5, review restores its launch control focus
pass: 5, results returns to finish
pass: 5, results restores its launch control focus
pass: 5, home position and launcher focus restored
pass: home results returns to original launcher position
pass: instant navigation reuses idle widget
pass: instant navigation restores saved pixels and focus
pass: resumed Eyes widget reconnects its own saved-round store
pass: unfinished round retains existing re-entry behavior
pass: reduced motion suppresses reveal
pass: normal motion reveals
pass: new asset precedes widget scripts
pass: rehearsal finish controls follow its score
pass: rehearsal finish focuses heading and scrolls
pass: rehearsal returns to saved position and next launcher
pass: idle rehearsal can resume
pass: resumed rehearsal reconnects its own store
pass: other-tab saves invalidate cached widgets
41 flow regression checks passed (DOM simulation, no browser geometry).
```

### Negative controls

```text
baseline expected-failure exit=1
AssertionError [ERR_ASSERTION]: Take the official test (30 curves), finish heading focused
mutation expected-failure exit=1
AssertionError [ERR_ASSERTION]: Take the official test (30 curves), finish heading focused
fixed flow exit=0
```

## What I did NOT check

- A strict MkDocs build, rendered Markdown, real viewport geometry, actual fold animation, or iPhone/Safari behavior.
- The official `site_check.mjs eyeslayout` and `eyes` modes against a built book. The wrapper's prerequisite check exits 1 because a local build is unavailable.
- Full-document reload restoration. The new idle-widget cache supports instant-navigation swaps within the current document. A full reload uses the existing saved-round loader.
- Real cloud uploads or real star light. Cloud routing in the new regression uses a stub.

## STOP SIGNS hit

- AGENTS.md section 4.12 allows running the project `.venv` interpreter. The separate `.venv-docs` executables requested in the brief fall outside that path table. The allowed interpreter reported `mkdocs_available False`. This prevented the strict build. No dependency installation was attempted.
- The synthetic local browser probe failed before CDP could complete its first command. WebSocket probes reported `CDP connection closed 1006` and Node reported `Detected unsettled top-level await`. A pipe probe also failed. These attempts produced no browser-layout pass. Scratch files are under `data/astra/015/`.
- Process-command-line inspection returned Access denied. A subsequent process-metadata check found zero Chrome processes started during this task. Server handles created by the probe were stopped in its `finally` blocks.
- The usage panel is inaccessible in this headless runner. Actual usage is unmeasured.

## Risks and assumptions

- My results Back returns to its launching screen. A finish-origin visit returns to the finish, while a menu-origin visit returns to the menu. This implements the brief's exact-return requirement.
- The instant-navigation cache retains only idle or completed UI state. Its interaction with the full Material build remains NOT TESTED in a browser.
- Full guidance is kept in a second fold so the first opening stays short.
- The existing published button wording, including Another sitting, is retained.
- The optional browser wrapper changes one navigation step in its private harness copy because the legacy test assumes history always returns home. It preserves the grading assertions. The wrapper has been syntax checked, but its browser suites have not run successfully here.

## QUEUE PROPOSALS

None. This work belongs to the existing brief under Tree node 4.4.

## IDEAS

None.

## Disagreements with Claude

None.

## Questions for Ahmed

None.

## Usage

Predicted before implementation, 25 five-hour points and 5 weekly points. Actual usage is unavailable. Lesson, simulated focus and routing checks need separate real-browser layout verification.

Next: Claude validates the patch in a permitted local book build before merge, estimated 1 weekly point for review and tests.

PARTIAL, the implementation and runnable logic checks are complete, while the strict build and real-browser layout checks remain unverified.
