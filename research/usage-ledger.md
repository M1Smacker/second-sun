# Usage ledger: what each kind of task really costs (Second Sun)

Why this exists: Ahmed rations weekly usage by the day, so my estimates must get better. Before 27 Oct night I guessed 5.5 to 6.5 points for ten steps; they cost 2. This file is the record I read before I quote a number, and update after every task.

## Protocol (every task, no exceptions)
1. **Before:** call `get_usage`. Write down weekly %, 5-hour %, and `tokensUsed` of the context.
2. **Estimate:** write my range in this file's table before starting, using the calibration section below and the task type. Say "uncalibrated" if the type has no row yet.
3. **After:** call `get_usage` again. Fill the actual columns the same day.
4. **Read the weekly meter with care:** it moves in whole points, so one task has about plus or minus 1 point of error. For small tasks use the 5-hour meter as the finer ruler: about 8 five-hour points equal 1 weekly point (see calibration). Bundle several small tasks into one row when each is under 1 point.
5. **Update the calibration** (ratios and per-type costs) when a row is added. Keep sample sizes honest.

What moves the meter: tokens I write, tool output I read into context, and the number of turns (each turn re-reads the whole context, so long sessions cost more per step). Screenshots and big file reads are expensive. Waiting idle costs nothing, so a long machine job is cheap if I do not poll it. Ahmed's own chats on the same account also count.

## Ledger
Times are UTC. "Mid" is the middle of my estimate range.

| When | Task | Type | Size | My estimate | Weekly before to after | 5-hour before to after | Context tokens added | Actual points | Actual / mid |
|---|---|---|---|---|---|---|---|---|---|
| 27 Oct Day 1 | Eight mixed items: backup copy to D, score line, visitor guard, two expert pages, font test Artifact, spine review, field note | Mixed code, pages, Artifact, publish | 8 items, 1 publish | 4.1 to 7.1 | 0 to 5 | not recorded | not recorded | 5 | 0.9 |
| 27 Oct Day 2 | Learning spine: data change, shape rules, pages, tests, publish | Book code plus full publish gate | 1 item, 1 publish | 2.5 to 6.5 | 5 to 7 | not recorded | not recorded | 2 | 0.44 |
| 27 Oct Day 3 | Redesign plan canvas v1 (4 boards), field note item, book republish | Design Artifact plus publish | 4 boards, 1 publish | 4 to 7 (as scoped then) | 7 to 8 | not recorded | not recorded | 1 | 0.18 |
| 27 Oct night, part 1 | Font and glyph research: scan book, download 10 font packages, coverage, cut and proof scripts, plan reply | Research with scripts | about 8 script runs, 3.5 MB downloaded | none given | 8 to 9 | 52 to 60 | +129K | 1 | n/a |
| 27 Oct night, part 2 | The ten step run: generator, 7 boards, font upload, local browser checks, 12 publishes, notes, commits | Design Artifact build plus verification | 7 boards (about 70 KB source), 12 publishes, about 30 browser calls, 3 commits | 5.5 to 6.5 | 9 to 11 | 60 to 76 | +196K | 2 | 0.33 |
| 27 Oct, 02:05 to 02:20 UTC | Phase E1 prep: Compass review, 5 pipeline files (about 700 lines) with 7 self-checks, dry run of the 5 known hosts (45 s machine time), eclipse shape check of 136 stars (25 s), commit | Pipeline code with tests plus a Compass review | 5 code files, 1 review, 2 short machine runs, 1 commit | 1.5 to 3 (uncalibrated) | 11 to 12 | 78 to 83 | +71K | about 0.6 (5-hour ruler; the weekly meter rounded to 1) | 0.27 |
| 27 Oct, 02:20 UTC | Option 4: written plan for the real redesign (F4), one repo survey | Plan document | 1 document (about 60 lines), 1 survey command | 0.3 to 0.7 | 12 to 12 | 83 to 84 | +9K | about 0.15 | 0.3 |
| 27 Oct, 02:25 UTC | Same-day field note (5 edits), ledger and notes, commit, full book publish gate (all tests, 5 browser tests, gh-pages push) | Mixed book work with a publish gate | 5 edits, 1 gate run, 2 commits | 0.2 to 0.5 | 12 to 12 | 84 to 85 | +15K | about 0.15 | 0.43 |
| 27 Oct, afternoon Kuwait (F4, Ahmed's go; weekly cap now 20%) | F4 steps 1 and 2 built and published (fonts, symbol files, font test, PC rail and margin notes, chapter layout test), Results design board and Artifact v13, repeat lines removed from the hard line, field note, 2 gate runs (the first stopped on a real tap-size flaw) | Large CSS, JS and Python change with browser tests, plus a design Artifact, plus 2 gates | about 12 files, 1 new browser test, 1 new unit test, 2 gates, 1 Artifact publish, 4 commits | 3 to 6.5 for what was done (the plan said 3.7 to 8.9 in all; the Eyes PC layout and the look pass are not built) | 14 to 15 | 8 to 22 | +229K | about 2.0 (5-hour ruler 1.75, context ruler 2.2) | 0.42 |

Breakdown of part 2, derived from the 5-hour meter divided by 8 (approximate):

| Step | 5-hour points | About weekly points |
|---|---|---|
| Generator, 7 boards, font upload | 5 | 0.6 |
| Local browser checks, fixes, first publish | 4 | 0.5 |
| Notes, memory, commit, push | 2 | 0.25 |
| Visual checks, fixes, publish v8 | 2 | 0.25 |
| Final fixes, publishes v9 to v12, commit | 3 | 0.4 |

## Calibration (current, n = 8 estimated rows)
- **Bias:** actual divided by the middle of my estimate: 0.9, 0.44, 0.18, 0.33, 0.27, 0.3, 0.43, 0.42. Median 0.38. Large CSS, JS and Python work with browser tests and two gates (F4 steps 1 and 2) also landed at 0.42, so the 0.4 to 0.9 band for book work with a gate holds; quote the low end of it.
- **F4 lessons (27 Oct):** about a third of the cost was reading: roughly 60K tokens of CSS, Python and JS were read before the first edit. Read only the regions the plan names. The gate clones the pushed main, so push before running it (the first run tested stale code). A tool that fails on a real flaw (the 40 px tap target) is cheaper than finding it by eye. My gut runs about 3 times too high on almost everything except a mixed day of many small book items (0.9, n = 1).
- **Rule for now:** quote 0.25 to 0.6 times my gut for design and document work, for plan documents, and (first data point) for pipeline code with tests. Quote 0.4 to 0.9 times my gut for mixed book work with a publish gate (0.43 for a small note plus one gate run, 0.44 for a spine build). For long unattended runs and Compass reviews alone there is still no clean data: say "uncalibrated" and widen the range.
- **Rulers:** about 8 five-hour points per weekly point (16 to 2, 24 to 3, 32 to 4: n = 3, steady). About 100K to 110K added context tokens per weekly point (n = 3).
- **Per unit costs seen so far:** one Artifact publish about 0.15 to 0.25 point. A pass of about 25 browser calls with a few screenshots about 0.5 to 0.7 point. Notes, commit and push about 0.1 to 0.25 point. A research script batch with downloads about 1 point. A written plan document about 0.15 point. A machine job that I do not poll (45 s and 25 s runs) costs almost nothing beyond reading its output.
- **Estimating habit that helps:** write the estimate before the work, do the work in the order of the plan, read `get_usage` at each step boundary. A lower number is not a better estimate: the aim is for actual divided by mid to sit near 1.
- **Whole stretch, 27 Oct about 02:05 to 02:30 UTC:** E1 prep, F4 plan, field note, full publish gate, notes: weekly 11 to 12, 5-hour 78 to 85, +95K context tokens, so about 0.9 weekly points for what I had estimated at 2.0 to 4.2.
- **To learn next:** a full book publish gate, a CSS change that needs browser tests, a long machine run that I monitor.

Lapse noted 27 Oct morning: no estimate was written before the Eyes review task (row in the bundled table below). Rule restated: the estimate goes into the ledger before the first tool call, even for a "quick look".

## Small tasks, bundled (each under 1 point)
| When | Task | Context tokens added | 5-hour | Weekly | Note |
|---|---|---|---|---|---|
| 27 Oct, 01:58 UTC | Read Ahmed's message, two greps of this file's source data, write the ledger | +12K | 76 to 77 | 11 to 11 | about 0.1 point |
| 27 Oct, 02:00 UTC | Memory entry, record Ahmed's picks, commit and push (research only) | +9.5K | 77 to 77 | 11 to 11 | under 0.1 point; lower end of the notes-and-commit unit cost (0.25) |
| 27 Oct, 02:40 UTC | Full regression: dry50 mode, 75 s machine run of all 474 Stage 2 groups, one test fix (NaN equality), commit and push | +6K | 85 to 87 | 12 to 12 | about 0.25 by the 5-hour ruler; a 75 s machine run itself cost nothing |

| 27 Oct, morning | Ahmed's Eyes review: cloud pull (26 rounds), 2 analysis scripts, 3 code files read, F4 plan section, field note item 10, commit, full publish gate | +39K | 2 to 4 | 13 to 13 | about 0.3 point (5-hour ruler 0.25, context ruler 0.37); no estimate written beforehand, my gut would have said 0.5 to 1, so about 0.4 of gut |

## Open rows (fill in as they happen)
| When | Task | Estimate | Weekly before | 5-hour before | Context tokens before | After | Actual |
|---|---|---|---|---|---|---|---|
