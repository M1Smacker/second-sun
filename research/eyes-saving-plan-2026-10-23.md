# Eyes mode: saving system and test (PLAN, agreed with Ahmed 2026-10-23 night; NOT BUILT until he approves)

*Why: Eyes mode was built as a practice game with saving deliberately switched off ("Nothing here is saved"), so Ahmed's practice score cannot be recovered. He wants every round saved forever, synced automatically, readable by Claude on request, plus a read-only look-back and a clear truth statement after every answer. Weekly cap: 70%.*

## Decisions (Ahmed's answers)
- Cloud: a **new free Firebase project** just for Second Sun (Spark plan, no card). Ahmed does the console steps; Claude never sees his login.
- Timing: **every answer saved on the device at once**; a round uploads when finished, or when a half-done round is left; offline rounds wait and upload when the internet returns.
- Reading: **on request, plus a daily automatic pull** into the repo (scheduled task).
- Look-back: **whole round, read-only** (step back and forward through earlier questions of the same round; the answer can never be changed; each look is recorded).
- Pass line (**Standard**): at least 85% of the clear hidden dips and at most 1 in 10 quiet curves called a dip, over at least 60 curves across 2 or more rounds on different days. Faintest dips (about 1,500 ppm) tracked separately, not in the pass line.
- Feedback: **big truth banner, 4 buttons** (Dip / No dip / Odd / Not sure). After every answer the banner states what it truly was: A DIP, or NOT A DIP with the reason (eclipse, spike, jump, nothing), and whether he was right.
- Real-lead pass: results go to the **private Firebase** too. Claude's condition: star IDs and light curves never leave this computer; only opaque codes (L1, L2...) and his answers are uploaded; nothing about leads in the public repo.

## CLARIFICATION BY AHMED (2026-10-23 night, after the plan): this replaces the real-lead rows above
- **Now:** Eyes mode is only practice and the official test. **Claude decides when he is ready** (his words: "once only you agree, like if you are satisfied with my results"); not before.
- **Later: a separate tab in the book for real data, connected to the hunt** (hunt output pumped into the book as the Eyes deck). He will look at the dips Claude tells him to, possibly all of them, and is happy to give 40 to 60 minutes a day once his practice is solid.
- **It may be PUBLIC. His explicit decision:** "I don't care if it's public, nobody even knows this... you can put the entire data, every candidate, everything on the book... We will figure this part out of people looking at our candidates when we actually get something big." This overrides the earlier local-only rule for now (the old rule stays on file; reversible, but git history keeps whatever was pushed).
- **Design consequence for Stage A:** ONE Eyes engine with a swappable deck source (practice generator now; the hunt's events later). Every saved round records `mode` (practice, test, real) and `source`, so Stage C is a new source and a new tab, not a rewrite. Stage C is therefore a normal book tab, not a local page, and its results can use the same cloud save.

## HARD RULE (Ahmed, 24 Oct small hours): he must NEVER have to copy, paste, export or send his results to Claude
His words: "I absolutely do not want this copy my results option... I hate it... Make a system that automatically updates either Firebase or GitHub, and you can check it yourself, and I don't have to give you any data on how I scored... simultaneously updated so you can access it whenever you want, as soon as I complete the round... in practice eye test, and in real using eye mode too." Consequences, binding on all stages:
- No copy, paste, export, share, download or email button anywhere in Eyes mode (a browser check fails the publish if one appears: `noCopyOption`). `exportJSON` stays an internal function only, used by the uploader.
- Every round of every mode (practice, test, real) reaches the cloud by itself the moment it ends (or is abandoned), and waits for the internet if offline. Claude reads it directly (reader script) whenever Ahmed says "look at my eye test scores"; he supplies nothing.
- Until Ahmed sets up Firebase, Claude CANNOT see his scores. He has accepted that and will do the setup later. The screen says so plainly ("Cloud backup: not set up yet, so Claude cannot see these rounds yet"). Claude must not ask him to send scores in the meantime.

## Real-data mode (Stage C) needs a richer record, so Stage B must not hard-wire the four practice answers
Ahmed expects more options and a more usable, more savable interface once he looks at real dips. Design now so it is a new source and not a rewrite: (1) each round stores its own answer vocabulary (`answers` list, version number) instead of the fixed Dip / No dip / Odd / Not sure; (2) `truth` may be null for real events (scored later against Claude's key-1 labels, the machine's flags and the Kepler-era data); (3) each answer may carry a confidence, a free-text note, which products or sectors he viewed, how long he looked, zoom and pan use; (4) candidate codes are shown as they are in the hunt (public tab, his decision), and the hidden fakes and known-false controls are mixed in without labels; (5) the same save-after-every-answer store, the same upload, the same reader. Stage B's cloud document shape therefore allows arbitrary maps inside `a` and `s`, and `mode` includes `real`. Before Stage C, `eyes-core.js` gets a per-round vocabulary and optional truth (tests first).

## What is built, in three stages
**Stage A (no Firebase needed; lets Ahmed start testing at once):**
1. Round record, saved on the device after EVERY answer (IndexedDB, with a localStorage fallback): schema version, round id, device label, mode (practice, test), planned and actual length, start and end time, and per question: curve kind (truth), his answer, right/wrong/unsure, time taken, looked-back flag, curve id and seed (so any curve can be re-drawn exactly). Round summary: right, wrong, unsure; dips found of hidden; clear and faint split; false alarms on quiet curves; odd things spotted.
2. Truth banner after every answer (all seven kinds: clear dip, faint dip, the real TOI-1338 b crossing, quiet, eclipse, spike, jump).
3. Look-back through the whole round, read-only (his answer stays; in test mode the truth stays hidden until the end).
4. "My results" page: history table and trend from the device, works offline. Shows "saved on this device", later "sent to the cloud" or "waiting for internet (n rounds)".
5. Test mode: two rounds of 30 curves (each: 10 clear dips, 4 faint dips, 8 quiet, 8 odd), no answers shown until the end, pass line computed on screen from all test rounds (with the minimum counts and a confidence range). (A "copy my results" fallback was built first and REMOVED the same night at Ahmed's order, see the hard rule below.)
6. Tests (all must pass before publishing): saving logic (per-answer save, crash mid-round, no duplicates, offline then online), look-back cannot change answers, banner text for every kind, phone layout, contrast, offline precache, the existing book gates.

**Stage B (after Ahmed creates the Firebase project, about 10 minutes of clicks, exact steps given):**
7. Upload: plain REST calls to Firestore (no heavy SDK, so offline caching stays small), one document per round with a deterministic id (device + round id) so retries can never duplicate; triggers: round end, leaving the page, the browser's online event, page open; retries with back-off.
8. Rules (written by Claude, published by Ahmed): create-only, fixed fields and size limits, no public reads. Honest limit: anyone could post valid-shaped junk until the free daily quota runs out; that cannot lose data (rounds stay on the device) and reading is admin-only.
9. Reader: `pipeline/eyes_scores.py` with a service-account key kept on D: outside the repo (never printed, never committed). Writes `research/eyes-scores/rounds.csv` (practice and test rounds only; fake data, public-safe), prints the summary and the pass-line verdict. A daily scheduled task runs it and commits the file.
10. End-to-end test: Ahmed does one 5-curve round; Claude reads it back and checks every number against what the screen showed.

**Stage C (only after Ahmed says he passed Stage A's test):**
11. The real-lead Eyes pass as a separate local page on his PC (the public site cannot host lead curves), same Eyes engine, blind: the 3 leads, the 2 known-host control events, and hidden fakes injected into other real stars' light curves, in random order, no labels. Local files in git-ignored `data/`; answers saved locally and uploaded to the private Firebase under opaque codes; Claude does not tell him which are leads until he finishes.

## Risks to keep in view
- iPhone Safari can erase site storage after about 7 days without use unless the book is added to the Home Screen; the cloud copy is what makes "saved forever" true, so the screen shows unsent rounds and Claude tells Ahmed to add it to the Home Screen.
- Sample size: 20 clear dips (two test rounds) can show he is not below the line, not prove he is above it; a third round narrows it. Claude reports the range, not only the pass/fail.
- Nothing from this system touches the hunt's candidate data except Stage C, and that stays local to the PC.

## STATUS (small hours, 24 Oct local): Stage A built and tested (see RESUME.md). Stage B waits for Ahmed's Firebase setup (research/firebase-setup-steps.md). Stage C waits for Claude's judgement of his test results.
