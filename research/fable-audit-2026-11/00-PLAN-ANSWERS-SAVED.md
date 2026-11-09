# Fable audit: Ahmed's answers, saved (10 Nov 2026, about 01:30 to 02:30 Kuwait). Status: PLAN ONLY, NOT STARTED

This file records Ahmed's answers from 16 rounds of questions, asked by Opus 5.5 medium in session 0aeb43a8. The Fable brief (`01-FABLE-BRIEF.md`) is NOT written yet. Ahmed stopped in round 16 to settle how the Fable reset and the weekly meter interact. Do not start Fable or the audit until he says so.

## Facts about the offer (Pro plan), from the Anthropic help pages, read 10 Nov 2026
Source: support.claude.com articles 17506494 (Fable 5.2 launch offers) and 11647753 (usage limits). CONFIRMED by reading the pages.
- Fable is included from 9 Nov to **16 Nov 2026, 11:59 pm PT** (17 Nov about 10:59 Kuwait), "up to 50% of your weekly usage limits".
- Pro gets **one** Fable limit reset, which expires at the same time. Once used, it cannot be undone.
- On the weekly limit, a reset gives back only the usage spent on Fable; other models' usage stays.
- A reset refills the whole 5-hour window and does not raise any limit.
- Help page: "Weekly limits apply across all models, and some plans also have a separate weekly limit for Fable." So Fable use LIKELY counts on "Weekly · all models" too. The app shows a separate "Weekly · Fable" meter (0% on 10 Nov, 01:3x). Whether one Fable step moves both meters is NOT TESTED.
- Normal weekly reset: 17 Nov 2026, 01:00 Kuwait (2026-11-16T22:00Z), before the offer ends at 10:59 Kuwait.

## Answers
**Run shape (rounds 1, 13, 16)**
- Run 1 (Fable): audits everything, finds where research is needed, writes a research plan by the research blueprint, does the research, then reports what it learnt and what we lack.
  - Smaller models (Opus, Sonnet) must be able to check and continue its work.
- Ahmed presses the reset after run 1's report.
- Run 2 = discuss (ask-tool rounds with Ahmed), then the fixes he approves, only after every doubt is settled.
- After Fable: Sonnet 5.5 Extra by default.
- Start: right after the brief (10 Nov). He has since paused the start until the meter question is settled.

**Effort, helpers, pacing (rounds 1, 15, 16)**
- Effort: medium; high for statistics.
- Read-only helper agents are allowed.
- At the Fable cap: finish the report first, keeping about 10% of the meter for writing it.
- Use the full Fable meter in run 1.
- Watch the Fable meter only. Ahmed then asked to re-plan this, see "Open".
- First test whether Fable use moves "Weekly · all models". If it does, stop run 1 at **40%** on that meter.

**Absolute rule for the audit (round 8, Ahmed's words, summarised)**
- In the audit Fable changes NOTHING. It may read, check and review everything, including the frozen Petrova code, and it may research.
- It does not file bugs or queue entries and edits no existing file.
- Its output is the audit markdown, plus a chat report of the important points.
- Fixing starts only after Ahmed is in the loop, all doubts are settled and Fable's questions are answered with the ask tool.
- Round 5's "report plus queue entries" is overridden by this.

**Allowed writes in the audit (rounds 5, 9)**
- Only its own files in `research/fable-audit-2026-11/`, committed locally once at the end. Never pushed.
- New scratch data folders `data\fable_audit_*`.
- Downloads: any Second Sun data, logged in `research/downloads.csv`. This is the only edit outside its folder.
- Its own STATE.md and usage log. RESUME and `usage-ledger.md` are updated by Sonnet afterwards.

**Scope and order (rounds 2, 3)**
- Order: Petrova (P), then numbers (N), then stars and data (S), then process (R), then book and tools (B, at most about 10% of the meter).
- Main goal: a higher real chance of finding a circumbinary planet.

**Petrova (rounds 3, 10, 14)**
- It may propose anything, even a rewrite or a new method.
- Read-only re-runs on G1 to G3 are allowed (injections, re-runs into new scratch folders).
- It may look at all real and upside-down G1 to G3 events. Report counts only; star IDs stay private (same rules as now).
- Filter goals: smaller planets; the cause of the S2 failures; recovering lost light; single and long-period transits.
- Question everything, including whether transits are the right method.
- Test Petrova on the known circumbinary planets: TESS ones on real light, Kepler ones by injection with their real parameters.
- Settle first: FIX 84 (QLP flag bit 31 and its effect on G3), completeness and Horizon (c 0.9, faint value 0.21, noise extrapolation), S2 and WO-14 (eccentric secondary first), and FIX 70/T137 (QLP neighbour windows).

**Numbers (rounds 6, 8, 10)**
- Re-derive every decision-steering number by an independent method.
- Trust no important conclusion without a recheck.
- Bad news is said blunt and plain.

**Stars and data (rounds 4, 11)**
- Sources: the FFI door (QLP, TESS-SPOC, TGLC, eleanor), Gaia DR3/DR4, other missions (K2, Kepler, CHEOPS, PLATO, ASAS-SN, ZTF, WASP, KELT), and public EB lists.
- It may redesign the FFI-door test (a new preregistration) rather than run stage D.
- Size the true bright pool, rank sources by value per point, draft G4/G5 star-list rules (Ahmed decides), and check Census stage 2 (T139).
- M-dwarf hosts: a full study. Gaia DR4: find the release date and plan around it.
- A 2027 roadmap tied to the study calendar.
- Outside-the-box ideas: bold, but the top 5 reported in depth.

**Research (round 6)**
- About 15% of the meter.
- Questions: what the professionals do that we don't; where planets are most likely; unsearched data; other detection methods (eclipse timing, apsidal motion, single-transit stacking).
- Normal RS numbers (RS-015 onward, marked Fable).
- Benchmark groups: Fable decides.

**Process, book, tools (rounds 2, 12)**
- Process: rules and memory, queues, tests and reproducibility, cost per result.
- Book: a full audit of wrong science, learning track design, structure and clutter, and the publish pipeline.
- Tools: results correctness, privacy leaks, breakage and flaky tests.
- Fable recommends on each pending 8 Nov decision: S2 A/B/C, the key name, RESUME shortening, the push, and the outside-check rule.

**Report (rounds 7, 8, 9, 13, 14)**
- A ranked findings list. Each finding has its effect on planet chance, cost in points per model, risk if ignored, and who can do it (Sonnet ok / Opus needed / Fable only).
- Full report in chat. Urgent finds are flagged at the top of the report, without stopping.
- One short note per area.
- Decisions are asked in ask-tool rounds at the end.
- Work orders per finding, a live STATE.md, saved evidence and difficulty tags.
- Write STATE.md before compaction, then continue.
- Read the full history first (RESUME, compass reviews, mistakes.md, git log).
- Include a glossary, a repo map, the mistakes history, and Ahmed's goal in his own words: his dream of finding a planet; "think outside the box while staying in it".

## Open (Ahmed, round 16)
Ahmed's other needs this week (10 Nov, after round 16): physics notes chats until his exam 13 Nov; 13 and 14 Nov off; from 15 Nov his math study (exam 28 Nov), so he needs about 20 weekly points for the math plan (Opus in Cowork scanning a 1 GB folder), about 10 for his father's website, and 20 to 30 for Cowork questions. Ahmed leans to Plan B (run 1 audit now, reset after its report, run 2 later), not decided. Opus's proposal: run 2 gets only what is left after his needs, with a stop line; Fable work orders can go to Sonnet next week.
Update 10 Nov (Ahmed): physics chats get 15 weekly points; Cowork 20 to 30 points are THIS week; the math plan may move to 13 or 14 Nov. Because run 2 may get little room, every finding must come with a work order so complete that Sonnet 5.5 Extra or Opus can do it cold: exact files and lines, the evidence and how to reproduce it, step-by-step method, the test that proves it worked, traps, and what not to touch. Fable explains what it saw that a smaller model would miss. Opus proposal: the approved "Fable only" fixes are done BEFORE the reset is pressed (14 Nov), so their cost is refunded too; run 2 after the reset is optional, with a stop at 92% on the weekly bar.
His goal: at the end of the Fable audit and fix, the normal weekly meter is back to where it was before Fable started. The way to do this (single reset, normal weekly reset on 17 Nov 01:00 Kuwait) is to be agreed with him before the brief is written.

## Rounds 17 to 21 (lessons for smaller models, ledger), 10 Nov
Fable keeps its own fable-ledger.md (task and area, both meters before and after, predicted vs actual, findings count). Lessons go into a private user skill C:\Users\hanzl\.claude\skills\second-sun-auditor, installed during run 1 (exception), budget Fable's judgement, written during run 1 before the reset. Topics: scanning for bugs, fixing without new bugs, checking numbers, research and planning, usage; a blunt 'mistakes Claude keeps making here' section; one set for all models; stop signs only for Petrova and stats; 3 to 6 worked examples; anything allowed (private). Proof: blind bug test prepared by Fable, run by Sonnet next week with and without the skill. Upkeep: any model adds lessons; core rules not weakened. Fable starts as a nested session from Ahmed's main chat. Useful rules from CLAUDE.md, memory and my-take are merged into the skill, originals untouched. Full brief: 01-FABLE-BRIEF.md.
