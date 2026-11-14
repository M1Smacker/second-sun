# Fable brief: work three real tasks, log how you work, then write the method skill (Claude, 14 Nov 2026; for Monday 16 Nov)

**Who you are working for.** Ahmed runs Second Sun: a search for circumbinary planets in TESS light curves with our own filter, Petrova. Claude (Opus) does most of the work; Codex is the second key. Your access ends at the weekly reset, **Tue 17 Nov 01:00 Kuwait**. Finish by about **23:00 Kuwait Monday**.

**Why you are here.** Ahmed judges you much stronger at deciding HOW to work on a hard problem. He wants that working method written down as a skill, `second-sun-method`, so Opus, Sonnet and Codex can follow it after you are gone. A model's description of itself is weak evidence, so the skill is built from what you DO on three real tasks, recorded as you go.

## Read first (about 40 KB, in this order)
1. `CLAUDE.md` (standing rules) and `research/TREE.md` top part to "Triage" (the map, the rules, the Road to G1).
2. `research/RESEARCH-BLUEPRINT.md` (how research is done here).
3. `.agents/skills/second-sun-auditor/SKILL.md` (lessons from your 10 Nov audit; do not repeat them in the new skill, point to them).
4. Per task, the files named under it. Read more only when a script you plan to write needs it.

## Rules (short; CLAUDE.md wins on conflict)
- Never edit frozen `pipeline/` files; never touch fence A or fence B stars; never run sealed or one-shot data; never push or publish; no emails or posts.
- Label findings CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED. A number you did not compute or read in a file is not a fact.
- Machine time is free; run long jobs in the background. Read the Fable and all-models meters (`get_usage`) before and after each task.
- Plain English, no en or em dashes. Explain every id in plain words.

## The work log (the real product)
Keep `research/fable-method/WORK-LOG-<task>.md` WHILE you work, short dated lines:
- what you looked at first and why; what you deliberately did not read or do;
- the check that could have proven you wrong, and whether you ran it;
- when you stopped reading and started testing, and why then;
- each decision: options, the evidence, the choice;
- where you changed your mind and what changed it.
Steps, choices and evidence only: anything another model could check. No hidden reasoning.

## Task 1 (design): the eclipse-timing fix, FIX 94
The mask that hides eclipses widens each window by the eclipse timing uncertainty; on 112 G2 stars with old timings that blanks whole light curves (711 light curves). Codex 010: padding off (V1) +25 planets, P 48.4% to 50.7%; recentred and capped (V2) +23, 50.5%; both add events on real light (61 to 95 or 90) and upside-down alarms (3 to 5 or 8) on those stars. Codex 011 (re-scored with the OAE fairness fix, preregistered pass rule) should be back by Monday: read it first.
**Deliver:** the production design for Petrova 1.1's mask timing (what the mask does per sector, fallbacks, how it is tested, what proof would reject it), ready for Claude to build.
**Files:** `research/stage3/rs025/HELD-AND-MISSED-RESEARCH-2026-11-14.md`, `research/stage3/rs026/EPHEMERIS-AND-FILTER-RESEARCH-2026-11-14.md` (Claude's draft design is in it), Codex 010 and 011 reports (branches `astra/010-mask-timing`, `astra/011-mask-timing-oae` in `D:\second-sun-astra`), `pipeline/petrova_mask.py` (read only), FIX 94 in `research/stage3/FIX-QUEUE.md`.

## Task 2 (judgement): what goes into Petrova 1.1
Candidates: OAE (adopted, not frozen), the FIX 94 variant from task 1, the dump-shape rule DS (P 0.502, +5 upside-down, not adopted), anything else RS-025 priced. Note RS-025 Q5: OAE lifts real TOI-1338 b transits at tier 1 from 4 to 6 of 13, but lets a planet's stronger transit hide its weaker one (TIC 172900988 b, two transits 4.95 d apart). Tree rule 1 (as amended) decides. **Deliver:** a one-page verdict per candidate (adopt, reject, or test more, with the exact missing test), and what combination should be frozen, with the combined test that must pass first. Say what is settled and what is not.
**Files:** `research/stage3/rs024/DOMINATED-RESEARCH-2026-11-14.md`, Codex 009 report (branch `astra/009-dominated`), RS-025, RS-026, Codex 010 and 011.

## Task 3 (planning): the shortest safe path to a G1 GO
From today to the one G1 run: steps, order, what each step's failure would mean, what can run in parallel, what Ahmed must decide, and where the plan could quietly go wrong. **Deliver:** a revised "Road to G1" for `research/TREE.md` (as a proposal file, Claude merges) plus the list of what the G1 preregistration must contain (draft: `research/stage3/G1-PREREGISTRATION.md`; bars: `G1-PLANET-BAR.md`, `G1-RECOVERY-BAR.md`; rules: `LEADS-RULES.md`).

## Then: write the skill (from your logs, not from memory)
`research/fable-method/second-sun-method/SKILL.md`: an ordered procedure for a hard Second Sun task, decision rules ("if X, do Y before Z"), stop signs, and two or three worked examples quoted from your logs. One page plus examples, frontmatter like the auditor skill (name, description saying when to load it). Claude installs it and runs sync_kit.

## If meter remains (in this order)
1. Review one of Claude's stints (RS-025 is the best candidate) and mark where your method would have changed what Claude did; each mark becomes a rule or example in the skill.
2. Leave a one-paragraph note for the held-out test: what a good answer to a design task here must contain. Do NOT open `research/fable-method/HELD-OUT-TASK.md` (the test must stay fair).

## Done means
Three deliverables, three work logs, the skill file, the meter readings in `research/usage-ledger.md`, and a short `research/fable-method/FABLE-REPORT-2026-11-16.md` (what was done, what is unfinished). Commit on main; do not push (Claude pushes after reading).
