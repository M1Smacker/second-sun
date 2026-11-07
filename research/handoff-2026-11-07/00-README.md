# Handoff to Claude Code from Claude (claude.ai), 7 Nov 2026

*From: an outside Claude session (Opus 5.5) that read the public repo at commit 1debc5c (6 Nov 2026), ran some of its tests on a clean Linux machine, and checked sources on the web. To: Claude Code working in `D:\second-sun`. Ahmed carries this folder across.*

## Read this first

1. **You are the project's own session; I am an outside reviewer.** Nothing here is an order. Every finding is a claim to verify against your own data and code before acting, under `CLAUDE.md` ("verify before concluding", labels, cheapest check first). Where I could not check something, I say so.
2. **Ahmed's rules still apply in full:** CLAUDE.md, RESUME.md, the two queues (bugs to FIX-QUEUE, builds to BUILD-QUEUE), frozen versions never edited, weekly cap set by him in chat, downloads logged and told, no en or em dashes, "Next:" line, questions in plain chat. He prefers to see a plan and say "go" before any multi-step build.
3. **What to do with this folder:**
   - Commit it unchanged to `research/handoff-2026-11-07/` (so it is on record as an outside input, like the Compass reviews).
   - Run a Compass-style review of it (VERIFIED / LIKELY / UNCERTAIN / NOT TESTED per item), using your data on D:, which I could not see.
   - File each accepted item in the right queue with its number from `01-WORK-ORDERS.md` (WO-n) in brackets.
   - Show Ahmed one short plan: what you accept, what you reject and why, the order, the cost in weekly points. Then wait for his go.
4. **Ahmed has an exam this week.** Do not ask him for decisions until he says the exam is done, unless he starts the conversation. Cheap verification work inside his cap is fine if he has set one.

## The files

| File | What it is | Who it is for |
|---|---|---|
| `00-README.md` | this page | Claude Code |
| `01-WORK-ORDERS.md` | 22 work orders (WO-21 The Annex and WO-22 Petrova dataset added on Ahmed's request), ranked, each with evidence, steps, acceptance test, cost guess and whether it needs Ahmed | Claude Code |
| `02-ENGINE-ROOM-BRIEF.md` | design brief for a new book Part that teaches the pipeline (Tier 2 of Ahmed's mastery plan) | Claude Code, then Ahmed |
| `03-REVIEW-AND-ODDS.md` | the review findings F1 to F7 with numbers, and honest odds for the coming months | both |
| `04-MASTERY-PLAN.md` | Ahmed's study plan: Checker, Engineer, Inventor tiers, every link checked on 7 Nov 2026 | Ahmed (Claude Code: use it for the Engine Room and for Keystone T134) |
| `05-SCRIPTS.md` | the two small scripts behind my numbers, to re-run | Claude Code |
| `06-OPTIONAL-CLAUDE-MD-NOTE.md` | a standing note on how to read Ahmed's "my thoughts" requests; add only if not saved already | Claude Code |

## The five things that matter most, in one paragraph each

**1. A free public list of 10,531 TESS eclipsing binaries (2-minute data, sectors 1 to 88) already exists** (CALNet, `github.com/wangleon/CALNet`, MIT licence, `outputs/newecl.dat`, TIC and Gaia IDs, no periods). The repo filed the CALNet paper as "method only" (`CENSUS-STEP2-RESEARCH-2026-11-04.md`, line 13). 10,460 of its stars were never searched by G1 to G3. Census stage 2 should start from the union of public lists, get periods from Gaia DR3 through the Gaia IDs, and point our own finder only at what all lists miss: slow binaries with one or two eclipses per sector. WO-2.

**2. Census-worth's "chance of at least one planet" counts the three finished null hunts as if they were still to come.** `census_worth2.py` line 15 uses `1 - exp(-(E_existing + E_census))`. Forward-looking, Census alone with the null update gives about 21% to 52% at 1,400 stars and 38% to 76% at 3,000 (two priors, three geometry cases), not 86% to 100%. The ceilings in the same table are fine. WO-1.

**3. The public repo cannot run outside Ahmed's PC, and its tests can report "pass" when they skipped.** 64 of 111 pipeline files hard-code `D:\`. On a clean Linux machine with the libraries installed, `test_hunt_prep`, `test_leads`, `test_scorecard_plus` (part 1) and `test_detect_v2_paths` ran and passed, but `test_detect_v2_paths` printed "pass" for B2 and B5 after printing "skip" (lines 36 and 50 return early, line 65 prints pass). `test_vopts` and `test_stage3_prep` fail on `D:` paths; `test_g3_prep` and `test_eyes_scores` hard-code `D:` too (not run). WO-9.

**4. Process cost is about equal to science cost.** 141 of 305 commits are book, RESUME, ledger, recap or field-note commits; 70 touch `pipeline/`. RESUME.md is about 16,000 words (roughly 20,000 tokens per cold start). BUILD-QUEUE holds around 100 tasks and at least eight named systems (Horizon, Vigil, Witness, Loom, OMS, Keystone, Learning Space, Search Window 2.0). Census is the priority Ahmed set; most of the rest should be parked with a one-line reason. WO-11 and WO-12.

**5. The detector loses depth on long dips, which are exactly the circumbinary kind.** `detect_v2.detrend` runs a 2-day biweight on the light with nothing masked. Your own measurement (FIX-QUEUE item 11) says it keeps 57% of a 20-hour dip's depth and 68% of a 15-hour one. A second pass that masks each candidate and detrends again (FIX-QUEUE item 14, idea from mono-cbp) is the highest-value Petrova upgrade for Census, provided it runs on both the real and upside-down arms. WO-4.

## My Take for Ahmed

Ahmed asked for my personal view of the project in "My take" form. It is in the chat, not in this folder, because it is for him.
