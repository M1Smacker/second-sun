# Bible Overhaul: plan

*Written 2026-10-20 11:35 UTC by Claude (Sonnet 5.5). Named by Ahmed: "an overhaul of the Bible".*

**Status: COMPLETE, 2026-10-20 (batches 1 to 6, commits cff5111 to the batch 6 commit).** Built as planned, with one deliberate change: the L2 to L6 lessons are one learning-track page (each level: what to read, which lab, a 3-question level check) instead of five separate pages, because the chapters and labs now carry the lesson content and separate pages would have duplicated them. The overhaul's labs caught three errors in our own records (noise number F-027, STANLEY peak period, G1 morph = -1 hole); all logged in research/mistakes.md.

## Why (Ahmed's words, 2026-10-20)
"I gotta catch up on the learning. I can't let an AI do all the work while I just sit and say yes or no." He wants (1) the core material the book does not have yet, (2) lessons on finding stars and reading data himself, the way Claude does, and (3) the rule that **every day's work is saved into the book, in teaching format, straight away.** For this overhaul the usual "core first, grow later" order is deliberately set aside: the book is the project's main product today.

## What the book has and lacks (Compass check, read-only; VERIFIED by reading the files)
| Have | Lack |
|---|---|
| Ch 1 to 6 (about 9,300 words), each in the 7-step form, with claim chips and quizzes | A plain-order **story so far**; a **reading order** |
| Learning-track design L0 to L6 with exercises (`research/burn-3-book/learning-track.md`); only L1 is a real page | **Hands-on labs**: no page shows how to go from a star's name to its data |
| Glossary: 19 terms | Names and catalogues (KIC, TIC, TOI, Gaia), missions (Kepler, TESS), SPOC/QLP/MAST, N-body, red noise, centroid, STANLEY: not defined |
| STANLEY mentioned 5 times, never explained | A **STANLEY chapter** |
| Blueprint page types (Start here, Records, Journal, What changed) | Not built yet |
No duplication: the labs become the exercise boxes of levels L0 to L6, and the new pages use the adopted blueprint (`research/SITE-BLUEPRINT.md`) templates.

## The new shape (Parts; renumbering is cheap now, costly later, so I do it once)
**Start here:** The story so far · How to read this book · Lab 0 Your workbench
**Part 1 The sky and the data:** 1 Stars, names and missions *(new)* · 2 Light curves *(old 2)* · 3 Where our data comes from *(old 6, expanded)* · Labs 1 to 3
**Part 2 Two suns:** 4 Binary stars and their planets *(old 1)* · 5 Why transits wander *(old 3)* · 6 Orbits and the three-body problem *(new)*
**Part 3 Finding dips:** 7 Noise and statistics *(new)* · 8 Our detector *(old 4, trimmed)* · 9 Fake planets: injection and recovery *(new, from old 4 plus the 33-transit test)* · Labs 4 to 6
**Part 4 Is it real?:** 10 Vetting *(old 5)* · 11 Pixels and neighbours *(new; includes the Compass finding on expected centroid shifts)* · Lab 7
**Part 5 The professionals' tool:** 12 STANLEY *(new: who made it, stacked search, stage 1 and 2, N-body, what it found on TOI-1338, its bugs)* · Lab 8
**Part 6 How the project runs:** 13 Your workshop *(tour of the folders and scripts)* · 14 Credit and publishing *(existing)* · 15 Our mistakes, as lessons *(the register retold)* · Lab 9 Your own star
**Field notes:** dated teaching pages (the same-day rule below). **Reference:** glossary grown to about 50 terms, reading list with plain summaries, claims.

## The labs (you run them; I check what you paste back)
Every lab is: goal · what you will see · copy-paste commands · "what you should see" · "what can go wrong" · **Your turn**. All use the project's own `.venv` (lightkurve 2.6.0 confirmed installed), keep downloads on **D:** (C: is nearly full), and start from data already on the PC where possible.
- **0 Workbench:** open a terminal, activate the environment, point the cache at D:.
- **1 Name to number:** from a star's name to its TIC/KIC number, position, brightness, and which TESS sectors saw it.
- **2 Get the data:** search, choose SPOC vs QLP, download one sector, open the file, read its columns and quality flags.
- **3 Plot and read:** raw vs cleaned flux, gaps, thruster-firing marks.
- **4 Find a dip:** by eye on TOI-1338, then with our box filter.
- **5 Two suns up close:** fold at the binary's period, see both eclipses, mask them.
- **6 Fake planets:** inject a planet, see what survives detrending and what the search finds.
- **7 Is it that star?:** the pixels, difference image, neighbours.
- **8 Read STANLEY's output** (re-running stage 2 takes about 33 minutes; optional).
- **9 Your own star:** pick one from the G1 list we have not touched and run the whole route. This is the "second key" practice.
Labs are tied to levels L0 to L6 so the quiet progress line still works. You report "L2 done" and I set the date; no points or badges.

## The same-day lesson rule (new standing rule; saved in memory, RESEARCH-PLAN.md, OVERNIGHT.md and decisions.md)
1. **Trigger:** any change to code, data, results, decisions or mistakes.
2. **Deadline:** the **Field Note is written in the same work block**, before the block is called finished and before any pause for usage. If a usage limit is close, the note comes first and more work second.
3. **Format:** plain-words first, then: what we did and why, the concept it uses (links to chapter and glossary), how you could do it yourself, what we found and did not find, one or two quiz questions, claim IDs.
4. If the work introduces a concept the book lacks, it gets a chapter section or glossary entry, not just a note.
5. **Publish and report:** `publish_book.ps1`, then the live link in the reply.
6. **Guard:** a small script `book/tools/teach_check.py` lists commits (to pipeline/, research/, targets/) made since the last Field Note and prints "Book is N commits behind". Run at the start and end of every block; `publish_book.ps1` warns; every wrap-up must say the number.
7. **Backfill first:** Field Notes for 19 and 20 October are the first two pages, because they are the two days you missed.

## Build batches (each ends with a strict build, a publish and a "read this next" message)
| # | Contents | Done when |
|---|---|---|
| 1 | Story so far · How to read · Lab 0, 1, 2 · Ch 1 Stars, names and missions · Field Notes 19 and 20 Oct · `teach_check.py` · Parts nav | You can go from a star name to its data yourself; the live site shows it |
| 2 | Ch 7 Noise and statistics · Lab 3, 4 · Ch 3 expansion · glossary to 50 | Labs run clean on this PC; you can read a light curve |
| 3 | Ch 12 STANLEY · Lab 8 · Ch 6 Orbits and the three-body problem · Lab 5 | You can say what STANLEY adds and why it needs a real orbit |
| 4 | Ch 9 Injection and recovery · Lab 6 · Ch 11 Pixels · Lab 7 | You can explain a fake-planet test and a centroid check |
| 5 | Ch 13 Workshop tour · Ch 15 Mistakes as lessons · Lab 9 · L2 to L6 lesson pages and quizzes · reading list · density rewrite of old chapters | You can run the route on a star alone |
| 6 | Stress test: strict build, every link, no dashes, 390 px and desktop, dark and light, offline cache, every code block re-run, nav and quiz and progress have no loops; fresh-clone publish | Zero errors; results listed |
Batches run one after another in this session. I check usage between batches and pause at a clean edge, never half-finished.

## Quality gates (from your earlier instruction: transitions, stress-tested, no logic loops)
- Every code block in a lab is **executed by me on this PC** before publishing; its output is pasted as "what you should see" (VERIFIED). Untested code does not ship.
- Every fact carries a claim ID with a label; no dashes in book text; pages end with Sources; the site stays noindex.
- No keys or tokens anywhere; downloads on D:, logged in `research/downloads.csv`; nothing outward-facing.
- Page budget: each chapter opens with "In plain words", stays about 1,800 words or less (a 15-minute read), and has a "Stuck? Start here" box.
- Phone: reading and quizzes work on the iPhone; labs need the PC (they say so at the top).

## Risks
- **I write it all and you just read** (your worry): mitigated by labs you run and "Your turn" boxes; I only mark a level done after your result.
- **Too dense:** you flag any page; flagged pages go to the top of the rewrite list.
- **Labs break** (Avast, wrong environment, network): each lab lists its common failures; I test on this PC first.
- **Scope:** about 7 new chapters, 10 labs, 2 start pages, glossary and Field Notes is a lot. Batches are ordered so the most useful parts for catching up come first; a batch not finished is not published.

## Decisions I made (say "change X" to override)
1. Renumber into Parts now.
2. Labs use the existing `.venv` and D: cache.
3. No helpers. If you want two helper sessions writing chapters in parallel, say "use helpers"; that would be asked each time anyway.
4. The first thing built is Batch 1, so you can start reading and running Lab 1 early.
