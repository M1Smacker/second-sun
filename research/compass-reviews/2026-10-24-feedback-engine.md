# Compass review: "Second Sun feedback engine" (Claude AI report + working prototype, 2026-10-24)

*Review only: nothing in the book or the Eyes code was changed. The report and prototype are saved unchanged in `research/feedback-engine-2026-10-24/` (`report.md`, `prototype/`). My own checks are in `our_checks/` and can be re-run: `node research/feedback-engine-2026-10-24/our_checks/fe_on_our_decks.js` and `fe_lessons_ours.js`. The prototype was read in full before it was run (it only reads and writes its own files).*

Labels: **VERIFIED** (I ran it or read the primary text), **LIKELY** (secondary source or consistent with sources), **UNCERTAIN**, **NOT TESTED**.

## 1. Verdict: REVISE (accept about 80%; the approach is right, five things must be fixed before anything is wired in)

It is a good design: measure the card from the dots, write three lines from the measurements, keep length fixed, adapt to the learner's habits. It is deterministic, small and testable. But the report's thresholds come from its own simulator, and when I ran the engine on OUR real card generator and on Ahmed's own cards, several claims did not carry over.

## 2. What is correct

| Claim | Status |
|---|---|
| The prototype's own tests pass: 4,160 compositions (13 kinds x 40 cards x 4 answers x 2 modes), same input gives the same text, only computed numbers, 36 to 44 words, no dashes, no verdict words in real mode | **VERIFIED** (re-ran: 0 failures) |
| 60 hard-noise cards in one session: 46 distinct first lines, longest run of one lead 2 | **VERIFIED** (exact match, same seeds) |
| On OUR decks: 2,560 texts, all 36 to 44 words, zero dashes, zero verdict words in real mode | **VERIFIED** |
| Gap dips are caught: on our cards the pre-gap sag fires on 95% of gap dips and on 0% of 600 ordinary cards, including the 29% that carry decoy gaps | **VERIFIED** |
| Spikes 95%, eclipses 100% caught on our cards; steps 73% (ours are subtle, 1.2 to 3 sigma) | **VERIFIED** |
| On Ahmed's hard-practice cards, rebuilt from their seeds, the new text names the thing he missed: "In the 2 hours before the hole at 10.5 hours, light sags by 1,100 ppm. A sag ending at a hole is a thruster fake." (his gap dips: 4 of 4 missed) | **VERIFIED** |
| Petrov, Dosher and Lu 2006: feedback made little difference to learning rate or final accuracy, but mattered for decision bias (criterion) | **VERIFIED** (abstract and paper page) |
| Gravity Spy: machine-guided leveled training reached 90% accuracy against 54% for volunteers given all materials at once | **LIKELY** (Jackson et al. preprint, 386 participants, plus Zooniverse blog; a preprint, and it compares guided leveling against everything at once, not easy-first alone) |
| Elaborated, short, task-focused feedback; no praise or judgement of the person (Shute 2008; Kluger and DeNisi 1996; Hattie and Timperley 2007); immediate feedback for novices and hard tasks; interleaving similar classes; near-twin contrast (Kellman) | **LIKELY** (the report read Shute and Kellman in the primary; Kluger and Hattie through summaries; I did not re-check) |
| The prototype is MIT, about 33 KB, about 4 ms per card | **LIKELY** (header says MIT; timing not re-measured) |

## 3. What needs changing, and why it matters

### Fix 1 (important): our own decks have giveaways the engine would turn into lessons
The report's own audit rule says: if an irrelevant feature predicts the truth, Ahmed learns the quirk. I ran that audit on our hard-noise and limit-planet cards (**VERIFIED**, `fe_lessons_ours.js`):

| Median on our cards | hard noise | limit planets | clear planets |
|---|---|---|---|
| points inside the event | 15 | 37 | 37 |
| duration (hours) | 2 | 6 | 6 |
| flat-floor fit (shape) | 0.4 | 4.1 | 11.8 |
| strength | 6.0 | 6.2 | 11.7 |

Our hard-noise "best dips" are short (2 hours) while our fake planets last 4 to 12 hours, and fakes have cleaner shapes. The lesson "only 15 points sit inside the dip, so a few low points can make it" fires on 72% of hard noise and 15% of limit planets: true on our deck, but a quirk of how we built it, not of the sky. In the real hunt, noise events and planets overlap in length (the detector's smallest box is 3 hours). Fix the generator first: draw hard-noise events with the same length distribution as the fakes, make faint-fake shapes as ragged as noise at that strength, and keep this audit as a test (every irrelevant feature at AUC under about 0.6).

### Fix 2 (important): "strength" must be ONE function, and it should be the hunt's own
On our cards the engine's median strength agrees with ours (ratios 0.91 to 1.05), but card by card they differ by up to 40% (one of Ahmed's hard-noise cards: our banner number 7.3, the engine 10.2; another 8.0 against 10.1). Different box lengths (the engine goes down to 2 hours, the detector to 3), a different noise estimate (point differences times a red-noise factor, against the detector's spread of box means). If the banner says 7.3 and the feedback says 10.2, he loses trust in both. Port `detect_v2.box_scores` to JavaScript, golden-test it against the Python on shared arrays, and use that one function in the deck, the feedback and (later) the real vetting page. Then "strength 7 or more" means exactly what the hunt means.

### Fix 3: the report's separation claim for limit planets does not hold on our deck
The report: strength separates limit planets from hard noise at AUC 0.86. On our cards it is **0.53** (chance), and "how far it stands out from the next wiggle" is 0.55. Our hard noise is stronger (median 6.0, against 4.2 in the report's simulator). That is what I told Ahmed earlier from our own measurement: fakes at strength 5 to 6.5 cannot be told from ordinary hard noise. The engine has to say this plainly on those cards (its `shape_unclear` idea is right), and its lessons must be re-calibrated on our decks. On our cards: lesson "unique" (argues for planet) fires on 50% of hard noise and 53% of limit planets, so in real mode (no label to filter with) it would tell Ahmed that a lone hard-noise dip "is what a real crossing does". **VERIFIED**; lessons with no separating power on our deck must not be shown in real mode.

### Fix 4: the variety claim is overstated, and there is a wording bug
- Variety: across 60 hard-noise cards on OUR deck there were only **10 distinct first-line wordings and 20 distinct second-line sentences** once the numbers are masked, one lead appeared 3 times in a row, and "A month of pure noise often gives one dip this strong" led 19 of 60 cards. The numbers change, so it is far better than before, but Ahmed may still feel the sentences repeating. Counting "46 distinct first lines" includes the numbers. Add paraphrase pools per lesson, facts about where in the card (hours in), and a variety test measured with numbers masked (target 40 or more distinct second lines per 60 cards).
- Bug: wrong answers use "<Answer> missed:", so a false alarm reads "Dip missed: it was only noise." (10 of 60 on our deck; examples 11, 17, 20, 29, 32 in the report). Should be "You said Dip; it was only noise."

### Fix 5: practice picks lessons by looking at the label; real mode cannot
In practice the ranking adds +3 for lessons that argue for the true class and −4 against, and four "anchor" lessons (faint step, faint flare, faint gap, faint planet) fire because of the label even when the detectors saw nothing (7% of practice texts on our deck). Useful for teaching, but it is exactly "look up the label", and real mode gets none of it. Keep truth-aware choice for the closing "check next time" cue only, make the lead lesson label-blind, and log how often the two disagree.

## 4. Gaps and risks

- **Real mode can falsely reassure.** Faint steps, ramps and variables slip past the detectors (the report's own examples 39 to 41). The fallback says "a month of pure noise often gives one dip this strong". On our artifact cards that lead appears on 4% (24 of 640). Fix: in real mode never lead with "weak" when any artifact detector is near its threshold; say "not classified" instead.
- **The "feedback only fixes bias" finding is partly overstated.** Petrov et al. used mixed easy and hard trials; Liu, Lu and Dosher (2010, 2012) found that at low accuracy, learning did not happen without feedback (**VERIFIED** via the search summary). Ahmed's hard cards are low accuracy, so feedback matters for sight there too. It still fits his habit of calling weak noise a dip.
- **Easy-mode cards were not tested** (they use raw light-curve windows with box fakes). **NOT TESTED.**
- **Thresholds** (for example 6, 1.6, 3) were fitted on the report's simulator; every one needs re-calibration on our decks after Fix 1 and Fix 2.
- **No mutation tests** in the prototype. Our rule: each test family must be shown to fail when the code is broken.

## 5. How I would improve the engine further (beyond the report)

1. **His own threshold line.** Store the measured strength with every answer (the cloud rules already allow extra fields) and show him his own curve: "On cards scoring 3 to 5 you said Dip 8 times in 10; the hunt's line is 7." That teaches the criterion directly, which is his main habit.
2. **A machine opinion to compare with, shown only after he answers.** For each card the engine can state what a strength-only observer would have said, so he sees where his eye and the numbers differ. Track agreement over time. (Never before he answers in real mode, because of anchoring.)
3. **Near-twin pairs are cheap for us.** Our builder is seeded, so "the same noise with and without a planet" is a few lines. This is the best-supported format for his hardest confusion.
4. **Replace the banner numbers with the measured ones everywhere,** so the plot, the text and the cloud record carry the same measurements. Those records then become the evidence log for the real vetting page.
5. **One definition of "near a gap" in hours,** shared with the detector's gap-edge and momentum-dump flags (`veto()` in `detect_v2.py`), so the eye training and the machine search never disagree.
6. **Sequence the cards:** start with easy and clear cases, interleave hard noise with limit planets, bring a missed kind back within 3 to 5 cards.

## 6. How it would help us

- It aims straight at the two things the data shows: 9 of 10 hard-noise cards wrong (he says Dip or Odd, almost never No dip or Not sure) and 4 of 4 gap dips missed. The pre-gap sag line and the "N of your false alarms scored under 7" pattern line speak to exactly those.
- It should move him through Steps 2 and 3 of the ladder faster, which saves calendar days and my usage.
- The same measurements become the numbers behind every real label, so Claude's sealed verdict and his answer can be compared against measured facts, not just against each other.
- No hand-written text per card; deterministic and testable; no AI at run time.

## 7. Order and cost

1. **Phase 0, before any text changes:** leak audit and generator fix on our decks (Fix 1), JavaScript port of the hunt's strength function with golden tests (Fix 2). About 1 to 2 points of weekly usage.
2. **Phase 1:** import the engine, re-calibrate on our decks, fix the wording bug, add paraphrase pools and the variety test, make the lead label-blind (Fixes 3 to 5), wire it into the practice banner and the end-of-round review, mutation-test, browser-test, publish. About 2 to 3 points.
3. **Phase 2:** overlays, near-twin pairs, his threshold line, sequencing. About 2 to 3 points.
These are estimates. The weekly meter moved from 77% to 85% during this one planning session, so it is volatile; the main driver is this session's long history (about 400,000 tokens carried into every step). **A fresh session with a short brief would cost much less per step than building here.**

## 8. The single best next step
Do Phase 0 first: the leak audit on our decks and the shared strength function. Every later lesson depends on those two being right, and neither changes anything Ahmed sees. Start it in a fresh session after the weekly cap allows it.
