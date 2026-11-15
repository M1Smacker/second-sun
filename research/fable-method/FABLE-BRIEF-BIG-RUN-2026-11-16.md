# Fable brief, big run (Claude, 15 Nov 2026; for Monday 16 Nov evening; replaces FABLE-BRIEF-2026-11-16.md, which stays as background)

**Who you work for.** Ahmed runs Second Sun: a search for planets around two suns (circumbinary planets) in TESS light, with our own filter, Petrova. Claude (Opus) does most of the work; Codex (GPT-6-Astra) is the second key. Your access ends at the weekly reset, **Tue 17 Nov 01:00 Kuwait**: finish by about **23:30 Monday**.

**What Ahmed wants from you (his words, 15 Nov):** "a real groundbreaking breakthrough": a bug that lets us find more planets, or a change that raises our chance of finding one a lot. "If we don't get one, it's fine." And: learn HOW you and Astra work, and keep it as one method skill for every Claude and Codex model.

## Budget and meters (hard rules; last time helpers and a resume wasted 14 points)
- **No helpers or subagents. No reading of chat history or old transcripts.** Read files directly, as named below.
- Read `get_usage` before and after each task; write each in `research/usage-ledger.md` and in `research/fable-method/FABLE-LEDGER-2026-11-16.md`.
- **Stop all work when the weekly all-models bar reaches 92%**, save, and write the report. Claude needs the rest to report to Ahmed.
- Machine time is free: long scripts in the background, never poll.

## Read first (about 50 KB)
1. `CLAUDE.md`, `research/TREE.md` top part to "Triage", `research/RESEARCH-BLUEPRINT.md`, `.agents/skills/second-sun-auditor/SKILL.md` (lessons from your own 10 Nov audit).
2. `research/fable-method/BIG-RUN-PLAN-2026-11-16.md` (this run's plan and our numbers).
3. Astra's reports and work logs from this weekend, in `D:\second-sun-astra` on branches `astra/023-candidate-matrix`, `astra/024-short-binary-subtraction`, `astra/025-load-losses` (`research/astra/reports/02[345]-*.md`; Claude merges them into main before you start if they passed review; Claude's review notes are in `research/fable-method/ASTRA-REVIEW-2026-11-16.md`).
4. Per task, only the files you need for a script you plan to write.

## Rules (CLAUDE.md wins)
Never edit frozen `pipeline/` files; never touch fence A or fence B stars; no G1, sealed or one-shot data; never push or publish; nothing outward. Label findings CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED. Tree rule 1: a Petrova change counts only if the bench shows more planets without more upside-down alarms (fairness amendment allowed). Plain English, no en or em dashes, explain every id.

## The work log (half of the product)
For each task keep `research/fable-method/WORK-LOG-F<n>.md` WHILE you work: what you looked at first and why; what you deliberately did not read or do; the check that could have proven you wrong, and whether you ran it; when you stopped reading and started testing; each decision (options, evidence, choice); where you changed your mind and why. Steps, choices and evidence only.

## F1 (judgement and design): decide Petrova 1.1
From Astra's 023 matrix (eight combinations of the adopted set B with the FIX 96 depth cap, the dump-shape rule DS, and the two FIX 94 mask-timing variants), 024 (short-binary light subtraction) and 025 (load losses), plus the older evidence (RS-024 to RS-030, Codex 009 to 014; paths in the old brief):
- Which combination to freeze as Petrova 1.1, or why none yet. Where Astra's numbers are borderline, say which extra measurement would settle it, and run it yourself on the bench copies if it fits the meter.
- The FIX 94 mask-timing design that survives its controls (RS-027: half the new real events are deep eclipses at wrong catalogue times; our own eclipse times failed controls twice, Codex 012 and 014 part 2).
- The one combined test that must pass before the freeze, written as a pass rule.
**Target:** a frozen set with planet-level P at least 0.50 and its lower bound at least 0.40 (the G1 GO bar), at no more upside-down alarms. If the evidence says it cannot be reached yet, say so and name the biggest remaining lever.

## F2 (the bug hunt): the second "F-01"
On 10 Nov your audit found the bug that mattered most: the eclipse mask deleted planet dips in slow binaries, and every earlier test missed it because planets were injected after the mask. Do the same kind of hunt on today's adopted set, aimed at the pools nobody has opened: **"not found" (41 of 222 Saturn-like test planets on T156)** and **"outside the searched windows" (45 + 7)**, using 025's load-loss findings as a start. Inject into RAW light, follow planets step by step, and look for any step that loses planets for a reason that is not physics. **Deliver:** ranked silent losses, each with a measured ceiling (planets) and, for the top one, a prototype fix on a bench copy with its failing-first test and its bench numbers.

## F3: the method skill, from both models
Write `research/fable-method/second-sun-method/SKILL.md` from your logs (F1, F2) AND Astra's logs (`023-worklog.md`, `024-worklog.md`, `025-worklog.md`): an ordered procedure for a hard Second Sun task; decision rules ("if X, do Y before Z"); stop signs; two or three worked examples quoted from the logs; a short section on where you and Astra worked differently and which way served better, with evidence. Frontmatter like the auditor skill (name, a description saying when to load it). It must work for any Claude model and for Codex models. Do not repeat the auditor skill; point to it. Do NOT open `research/fable-method/HELD-OUT-TASK.md` (Claude uses it to test the skill afterwards).

## Done means
F1 verdict file `research/fable-method/F1-PETROVA-1.1-VERDICT.md`; F2 file `research/fable-method/F2-SILENT-LOSSES.md` (plus any prototype under `data\fable\`); the skill; the work logs; the ledger rows; `research/fable-method/FABLE-REPORT-BIG-RUN.md` (what was done, what is unfinished, the single most important thing for Ahmed). Commit on main; do not push (Claude pushes after reading).
