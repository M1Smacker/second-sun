# Fable brief, big run (Claude, 15 Nov 2026; audited and corrected 16 Nov 2026, 9:45 am; replaces FABLE-BRIEF-2026-11-16.md, which stays as background)

**Starts Monday 16 Nov late morning. Ahmed is travelling (family emergency) and cannot answer: make every decision yourself, write the reason in the work log, and go on.**

**Who you work for.** Ahmed runs Second Sun: a search for planets around two suns (circumbinary planets) in TESS light, with our own filter, Petrova. Claude (Opus) does most of the work; Codex is the second key (jobs 023 to 025 ran on GPT-6.1-Sol at high effort, not GPT-6-Astra: a runner default Claude missed; say so in F3 when comparing models). Your access ends at the weekly reset, **Tue 17 Nov 01:00 Kuwait**: finish by about **00:15 Tuesday** at the latest.

**What Ahmed wants from you (his words, 15 Nov):** "a real groundbreaking breakthrough": a bug that lets us find more planets, or a change that raises our chance of finding one a lot. "If we don't get one, it's fine." And: turn the steps that worked on this project (yours and Codex's, from the written work logs) into one reusable procedure file for Second Sun tasks.

## Budget and meters (hard rules; last time helpers and a resume wasted 14 points)
- **No helpers or subagents. No reading of chat history or old transcripts.** Read files directly, as named below.
- Read `get_usage` before and after each task; write each in `research/usage-ledger.md` and in `research/fable-method/FABLE-LEDGER-2026-11-16.md`.
- **Stop all work when the weekly all-models bar reaches 95%** (Ahmed, 16 Nov 9:51 am; Claude finishes up to 98% and Ahmed keeps the last 2 points), save, and write the report. If the 5-hour bar fills, stop cleanly with state saved in your work log; Claude restarts you after the reset. The bar was 70% at 9:30 am.
- Machine time is free: long scripts in the background, never poll. You have the CPU: up to 6 workers with NUMBA_NUM_THREADS=2 (Codex is idle during your run; 025's finishing bench may use 4 workers until about midday).

## Read first (about 50 KB)
1. `CLAUDE.md`, `research/TREE.md` top part to "Triage", `research/RESEARCH-BLUEPRINT.md`, `.agents/skills/second-sun-auditor/SKILL.md` (lessons from your own 10 Nov audit).
2. `research/fable-method/BIG-RUN-PLAN-2026-11-16.md` (this run's plan and our numbers).
3. Codex's reports and work logs from this weekend, merged into main: `research/astra/reports/023-*.md` and `024-*.md` (025 lands later today on main when Claude has merged it; read it then). Claude's review notes: `research/fable-method/ASTRA-REVIEW-2026-11-16.md`. Also Claude's research of 15 Nov: `research/stage3/rs037/MULTI-CROSSING-2026-11-15.md` and `research/stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md`, and the new bar `research/stage3/G1-PLANET-BAR-75-2026-11-15.md`.
4. Per task, only the files you need for a script you plan to write.

## Rules (CLAUDE.md wins)
Never edit frozen `pipeline/` files; never touch fence A or fence B stars; no G1, sealed or one-shot data; never push or publish; nothing outward. Label findings CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED. Tree rule 1: a Petrova change counts only if the bench shows more planets without more upside-down alarms (fairness amendment allowed). Plain English, no en or em dashes, explain every id.

## The work log (a lab notebook)
For each task keep `research/fable-method/WORK-LOG-F<n>.md` as you go, like a lab notebook: files read, scripts written and run, their results, the falsification check you ran (or chose not to run, and why), and each decision with the evidence for it, plus any decision you later reversed and the result that reversed it. Record actions, results and decisions only.

## F0 (10 minutes, before F1): pre-mortem
Write `research/fable-method/F0-PREMORTEM.md`: the three most likely ways this run could produce a FALSE breakthrough (a P that looks better than it is, against the 0.75 bar below or against the old 0.50 mark), and the check that would catch each. Known one to start from: **picking the best of eight combinations on the same planet bench that scores them inflates its P (winner's curse)**; with P near 0.50 and an interval of about plus or minus 0.04, that bias can decide GO.

## Per-task meter caps (weekly bar points; stop the task at its cap and write what is left)
F0 and F1 together 8; F2 7; F4 4; F3 3; reserve 1.5 for your report (total about 23.5 of the 23 points from 72% to 95%; trim F2 by 0.5 if needed). Order: F0, F1, F2, F4, F3. Never start a task with less than its cap left before 95%; if one runs short, cut its depth, not F3.

## Where the benches are
Astra's harness copies, scripts and data are under `D:\second-sun-astra\data\astra\0NN\` and named in each report's reproduce section (006 planet bench, 013 and 014 background and deep bench, 023 matrix). Run them as they are, or copy them under `data\fable\`; never edit `pipeline/`. Read the report's reproduce lines before writing new code.

## New bar (15 Nov, Ahmed)
G1 GO now needs P at least 0.75 with lower bound at least 0.65 (`research/stage3/G1-PLANET-BAR-75-2026-11-15.md`). Judge F1 against it and say how far each candidate is from it. RS-037 puts the realistic ceiling of all known levers at about 0.71 to 0.74 (LIKELY), so say plainly if 0.75 is out of reach and what would change that.

## F1 (judgement and design): decide Petrova 1.1
From Astra's 023 matrix (eight combinations of the adopted set B with the FIX 96 depth cap, the dump-shape rule DS, and the two FIX 94 mask-timing variants), 024 (short-binary light subtraction) and 025 (load losses), plus the older evidence (RS-024 to RS-030, Codex 009 to 014; paths in the old brief):
- Which combination to freeze as Petrova 1.1, or why none yet. Where Astra's numbers are borderline, say which extra measurement would settle it, and run it yourself on the bench copies if it fits the meter.
- The FIX 94 mask-timing design that survives its controls (RS-027: half the new real events are deep eclipses at wrong catalogue times; our own eclipse times failed controls twice, Codex 012 and 014 part 2).
- The one combined test that must pass before the freeze, written as a pass rule. **It must include a confirmation on a FRESH planet bench (new random seed, new planets, same rules) that was not used to choose the combination**; a combination is a GO candidate only if it passes there too. If the meter allows, run that confirmation yourself; otherwise write it as Claude's first job on Tuesday.
- You propose; you do not freeze. The freeze needs Ahmed and two keys.
**Target:** the G1 GO bar is now **P at least 0.75 with lower bound at least 0.65** (see 'New bar' below; the old 0.50 bar stays on record). Propose the best set and say how far it is from 0.75, at no more upside-down alarms. If the evidence says 0.75 cannot be reached yet, say so and name the biggest remaining lever.

## F2 (the bug hunt): the second "F-01"
On 10 Nov your audit found the bug that mattered most: the eclipse mask deleted planet dips in slow binaries, and every earlier test missed it because planets were injected after the mask. Do the same kind of hunt on today's adopted set, aimed at the pools nobody has opened: **"not found" (41 of 222 Saturn-like test planets on T156)** and **"outside the searched windows" (45 + 7)**, using 025's load-loss findings as a start. Inject into RAW light, follow planets step by step, and look for any step that loses planets for a reason that is not physics. **Deliver:** ranked silent losses, each with a measured ceiling (planets) and, for the top one, a prototype fix on a bench copy with its failing-first test and its bench numbers.

**F2 context, FIX 101 (found 15 Nov, 8:40 pm, RS-038 trace; NOT yours to build: Codex 026 prototypes it after your run, brief `research/astra/inbox/026-fix101-mask-drift.md`; read the brief and, if you see a flaw in its variants or controls, write it in F2 and Claude fixes the brief before launch):** the Petrova eclipse mask's catalogue drift term (`pipeline/petrova_mask.py` `windows()`, 3 x sqrt(eT0^2 + (n x eP)^2)) grows each year on bad catalogue period errors until windows cover the whole orbit: 18% of catalogue binaries over half the orbit by BTJD 3500; on the bench 100 planets on such stars get 31% of crossings scored (79% elsewhere), recovery 0.32 vs 0.50; realistic gain about 1.7 P points, up to 6.4, more in new sectors. Also: the trace shows about a quarter of the 'never scored' pool is a bench capture gap (best-product table), not a search loss.

**Your F2 target, from RS-038 task B (start here):** of 1,271 planted crossings never scored (Astra 006), 887 had good data in a prepared sector and were removed inside the chain; about 220 of them sit at eclipse times (mask), so about **600 crossings with good data, away from eclipses, are lost for a reason nobody has named**: safe windows, the single scored product, or gap trimming. Another 308 sit in sectors that failed to prepare ('no safe windows' 165, 'too little data after masking' 143). Start there; scripts `data/rs037/neverscored.py`, `phase.py`, `replay.py`, `replay_mask.py` and their outputs `data/rs037/replay-*.txt`. Codex 025 found that 14 of the 21 T156 load losses are the stray-light quality bit 4096 alone and none are FIX 101 cases; its stray-light candidate bench was cut by a PC restart and Claude is finishing it this morning (review notes will land in `research/fable-method/ASTRA-REVIEW-2026-11-16.md`).

## F4 (after F2)
**F4: the vetting-loss pool and orbit vouching (cap 4 points).** RS-037 (`research/stage3/rs037/MULTI-CROSSING-2026-11-15.md`) shows 11.6 points of P are planets detected at SNR 7+ and held at tier 2 by guard flags (dump 55, step 49, gap edge 34, ramp 33, repeater 32 of 123), and that a second crossing scoring 4+ exists for 5.6 points. Design, and if the meter allows prototype on a bench copy: (a) a cross-star coincidence veto (STANLEY's deep-timestamp list idea) to replace the blanket dump flag; (b) orbit vouching: promote a tier-2 dip when a circumbinary orbit through it predicts another crossing that scores 4+; with a preregistered pass rule under Tree rule 1 (upside-down alarms not above B), the zero-planet identity check, and the fresh-seed confirmation. Say which flag loses the most planets for the fewest prevented false alarms.

**F4 evidence from RS-038 (read `research/stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md` first):** our dump hold covers about 20% of Year 1 to 2 data and 7.5% later; mono-cbp's cross-star check costs only a few per cent of planted transits; the TOI-1338 b team separated jitter fakes with per-pixel tests; all 443 checked SPOC and TESS-SPOC files carry star-position columns. Test first: replace the blanket dump hold with our existing cross-star flag plus a centroid-excursion jitter test (a planted dip is lost only if the real data at that time shows jitter), on both arms; second, a narrower pre-dump window if the TESS release notes support it. Also check whether stray-light or other quality bits remove planted crossings (part of the never-scored pool).

## F3: the procedure file, from both sets of logs
Write `research/fable-method/second-sun-method/SKILL.md` from the written work logs (yours for F1 and F2, and Codex's `023-worklog.md`, `024-worklog.md`, `025-worklog.md`): an ordered procedure for a hard Second Sun task; project rules ("if X, do Y before Z"); stop signs; two or three worked examples quoted from the logs; a short section comparing the steps the two logs record and which order of steps gave better results, with evidence. Frontmatter like the auditor skill (name, a description saying when to load it). It must work for any Claude model and for Codex models. Do not repeat the auditor skill; point to it. Do NOT open `research/fable-method/HELD-OUT-TASK.md` (Claude uses it to test the skill afterwards).

## Done means
F4 file `research/fable-method/F4-VETTING-VOUCHING.md`; F1 verdict file `research/fable-method/F1-PETROVA-1.1-VERDICT.md`; F2 file `research/fable-method/F2-SILENT-LOSSES.md` (plus any prototype under `data\fable\`); the skill; the work logs; the ledger rows; `research/fable-method/FABLE-REPORT-BIG-RUN.md` (what was done, what is unfinished, the single most important thing for Ahmed). Commit on main with explicit paths only (`git add <your files>`, never `git add -A` or `.`: Claude works in the same folder and commits its own files the same way); do not push (Claude pushes after reading). Do not edit `RESUME.md`, `research/TREE.md` or the book: Claude keeps those.
