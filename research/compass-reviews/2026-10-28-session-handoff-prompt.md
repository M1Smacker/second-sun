# Compass review: the session handoff prompt (28 Oct 2026)

Review only. No project file was changed by this pass; this file is the saved review. Labels: CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED.

## 1. Verdict: REVISE

The prompt is a good skeleton (rules, checklist A to F, 12 deliverables, a safe save rule). It would produce a usable handoff as written, but it would miss things that matter for starting "exactly where we left off", and three of its instructions would cause harm or loss. The fixed version is Prompt A below. A matching fresh-session opener is Prompt B.

## 2. What is correct (keep)

- Do not assume something is done because it was discussed (the rule that "unverified is not fixed"). CONFIRMED as a standing rule in the memory index.
- The label set, and "preserve failed experiments, rejected approaches and caveats". CONFIRMED: this is how `research/stage3/learnings-2026-10-27.md` is already written.
- "Never turn a lead into a candidate": the book's own ladder agrees (`book/docs/candidates.md`: a candidate is a dip that passed first checks and still needs two keys).
- The premises STANLEY, Stage 2 trials, inverted-light-curve controls, injection-recovery, two keys and publication-first all exist in the repo. CONFIRMED: `pipeline/stanley/`, `data/stanley`, `data/stanley_cbp`, `pipeline/stage2_search.py`, `research/stage3/asymmetry*.txt`, `research/stage3/faint_recovery_v5.txt`, `book/docs/book/10-vetting.md` (row C11 "two keys"; line 88: ExoFOP accepts candidates only after publication), `research/burn-3-book/open-questions.md`.
- Create the file only if the name is free, and report the exact path, git status and what could not be recovered. CONFIRMED safe: `SESSION_HANDOFF_2026-10-28.md` does not exist today (checked).
- Do not start the next research task. Keep.

## 3. What needs changing, and why it matters

1. **"Nested agents" is the wrong premise for this session.** CONFIRMED: the transcript of this session (`C:\Users\hanzl\.claude\projects\C--CLaudeCode\a8dcae12-19ed-4849-9f4f-b33134757b00.jsonl`, 19 to 28 Oct 2026, about 150 MB, title "Unknown mysteries and problems to solve") contains 0 Agent tool calls and no `subagents` folder. It contains 3 SendMessage calls, all to one side session, `local_fe4a9c04-9158-4f97-8519-d7b75a1f3250`, about the book's look (professional and clean), the site blueprint (`research/SITE-BLUEPRINT.md`) and "extended orders" for a prototype. The handoff must say "no subagents" plainly, and instead cover that side session and any other linked session. Why it matters: the prompt as written invites the writer to hunt for agent findings that do not exist, or to invent them.
2. **"Do not commit or push" would strand the handoff.** A file left untracked is visible only in the same working tree. Ahmed reads from a phone and wants pushed links, and Second Sun is the one project where auto-push is allowed. Fix: after verification and a privacy scan, commit and push that one file and nothing else.
3. **Privacy: the repo is public.** The prompt asks which targets were processed and for "candidate leads". A careless handoff would list star IDs or event times of real tier-1 events, which breaks the aggregates-only rule, and would be pushed (see item 2). Fix: an explicit privacy block, plus a scan before commit. Known planet hosts and controls (TOI-1338, Kepler-16 and so on) are public and fine.
4. **Memory does not carry over.** CONFIRMED mechanism: memory is stored per start folder (`C:\Users\hanzl\.claude\projects\C--CLaudeCode\memory\`). A fresh session started in `D:\second-sun` will not load it. About 25 of its entries (I counted 24 index lines that match) bind Second Sun work (phone-first, no popups, tiny edits are mine, ask before helpers, never click the live Eyes page, no manual data copy, Compass, verify science, always say what is next, usage ledger and cap, no dashes). `D:\second-sun\CLAUDE.md` carries only some of them. Fix: the handoff lists the memory files that apply and copies the rules into a "working agreements" section, and the opener says which folder to start in. (Update 28 Oct, evening: Ahmed asked why `C:\CLaudeCode` is needed; the entries were then copied into a memory folder for `D:\second-sun`, so Prompt B now says to start there, without a worktree.)
5. **Label mismatch.** `research/COMPASS.md` (28 Oct) says CONFIRMED replaces VERIFIED in new notes. The prompt says VERIFIED. Fix: use CONFIRMED, and treat VERIFIED in older notes as a synonym.
6. **The prompt is science-only; the project is not.** Missing: the book and its publish state (gh-pages at `c07f73d`), Eyes mode and its scoring, the paused visual-identity Artifact (`D:\ss-artifact-work\RESUME-HERE.md`), the to-do list after the weekly reset (`research/TODO-after-weekly-reset-2026-10-26.md`), the side session, scheduled tasks, the usage ledger and cap, Remote Control, and Ahmed's pending decisions. Without them the new session will not start where we left off.
7. **Missing: the last stretch of conversation.** The most recent hours hold decisions that are in no file except `VESPER-BRIEFING.md`: the name Vesper (chosen over Penumbra), the "be straight with me" correction, the seven raw-light dips that nobody has looked at, and the three questions to Ahmed. Fix: a "where we left off" section, step by step.
8. **Duplication risk.** `VESPER-BRIEFING.md` (commit `1848a6b`, 19 sections, about 7,000 words) already holds the science state. A second full science write-up would drift from it. Fix: point to its sections and write only the delta.
9. **"Verify that the handoff accurately reflects the repository" is too vague to check.** Fix: a claim ledger (each number with its source path), a list of cheap read-only checks, and a short "not recovered" list.
10. **Hazards and do-not-repeat items are not named.** Fix: `pipeline/eyes_rules_test.py` writes to Ahmed's real Firestore; the live Eyes page uploads to his real cloud; `python - <<EOF` heredocs hang in this shell; the GPL tool `mono-cbp` stays in `D:\ss-external`; `data\` (6.0 GB) is not in git; frozen versions are never tuned on the 549 stars; and `stage3.py run` now refuses because the report code is inside the freeze hash (FIX-QUEUE 21b).
11. **Known soft spots I want the handoff to preserve, not smooth over.** UNCERTAIN or open: my chat wording that the 7 raw-light dips "look like camera effects" (nobody looked), the total of about 4,584 binaries in the Prsa catalogue (from memory), how many scripts assume the G1 layout, the extent of SAP-filled cadences in the v5 cleaned-light half, and mutation checks that lived in a scratch script.
12. **The "single highest-priority next task" should not be decided by the writer.** Ahmed has open decisions. Fix: list the options with their costs and mark the choice as Ahmed's.
13. **The final report is allowed to be long.** Ahmed reads on a phone. Fix: the file may be long; the final response must be a short digest ending with a "Next:" line.

## 4. The single best next step

Run Prompt A in this session (it holds the context and the transcript), review the file it produces, then start the fresh session with Prompt B. Estimated cost of Prompt A: about 1.5 to 2.5 weekly points (mostly reading and verifying; no experiments), no machine time beyond cheap tests. UNCERTAIN: the estimate is my guess from the ledger, where reading-heavy tasks have run close to the middle of my range.

## 5. What this review checked

CONFIRMED by looking: `research/COMPASS.md`; the memory entry for Compass; that `SESSION_HANDOFF*` does not exist; git is clean at `1848a6b` equal to origin/main; `RESUME.md` exists and is the file a fresh session is told to read first; the two-key and publication-first wording; the STANLEY folders; the session transcript counts (0 Agent, 3 SendMessage, one target); the transcript's date span; that no `subagents` folder exists for this session. NOT CHECKED: the state of the side session `local_fe4a9c04...` (the writer must look); the scheduled tasks (the writer must list them).

---

## 6. Prompt A: the revised handoff prompt (paste into this long session)

```text
SECOND SUN: SESSION HANDOFF (revised after a Compass pass, 28 Oct 2026)

You are preparing a handoff from this long-running Claude Code session to a completely fresh session in the same project. The goal: the fresh session starts exactly where we left off, without this conversation's history, and without repeating, undoing or overclaiming anything. The conversation is too long for /compact to help. You hold the context; the files hold the truth. Where they disagree, the files win, and you say so.

WHO AND WHAT
Ahmed is the owner. Second Sun is a search for circumbinary planets in TESS data, plus a public teaching book. The search is now called Vesper (Ahmed's choice on 28 Oct 2026; renaming inside the book and notes is still pending). Repo: D:\second-sun (public: github.com/M1Smacker/second-sun; book: m1smacker.github.io/second-sun). This session's memory folder: C:\Users\hanzl\.claude\projects\C--CLaudeCode\memory\ (read MEMORY.md and every entry that mentions Second Sun).

SEED FACTS (from this session's own summary; every one must be checked against files before it goes into the handoff as CONFIRMED; anything you cannot check keeps its label)
1. Branch main, HEAD 1848a6b ("Add VESPER-BRIEFING.md"), clean tree, equal to origin/main; before it 46e136a and f252ee6. The book was published to gh-pages on 28 Oct (c07f73d) and checked live.
2. Vesper v7, frozen hash fd788be04650, builds on v1 to v6 (hashes in research/stage3/SETTINGS_FROZEN*.json). Tier 1 in v7: 21 real and 32 upside-down. No candidate exists. Nobody (human or AI) has looked at any real event.
3. VESPER-BRIEFING.md is the science state document (19 sections). Read it fully. Do not rewrite it; point to its sections and record only what it lacks.
4. Open decisions that belong to Ahmed: (a) a blind, shuffled look at the 7 raw-light-only tier-1 dips; (b) start the briefing's plan steps 1 and 2 (measure the blind spot in planet size; build a second target list); (c) rename the pipeline to Vesper in the book and notes; (d) an outside review of the briefing may come back; it goes through Compass (research/COMPASS.md) before anything is built.
5. Usage: weekly about 33% and 5-hour about 75% at the last reading on 28 Oct; weekly resets 2 Nov 21:59 UTC; Ahmed's working cap is 10 weekly points per day; ledger in research/usage-ledger.md (last row: v7 plus bug hunt, 4 points against an estimate of 1.5 to 3.0). Re-read get_usage now and record it.
6. This session: title "Unknown mysteries and problems to solve", 19 to 28 Oct 2026, transcript C:\Users\hanzl\.claude\projects\C--CLaudeCode\a8dcae12-19ed-4849-9f4f-b33134757b00.jsonl. It made 0 Agent calls. It sent 3 messages to a side session, local_fe4a9c04-9158-4f97-8519-d7b75a1f3250 (the book's look, SITE-BLUEPRINT, a prototype). The state of that side session is NOT KNOWN to me: find it.
7. Other threads: the visual-identity Artifact is paused (D:\ss-artifact-work\RESUME-HERE.md); research/TODO-after-weekly-reset-2026-10-26.md; book redesign (research/redesign-f4-plan-2026-10-27.md, research/SITE-BLUEPRINT.md); Eyes mode and scoring (pipeline/eyes_scores.py, scheduled tasks); the GPL tool mono-cbp lives outside the repo in D:\ss-external.
8. Ahmed has not started the book's learning track, practises Eyes mode, wants plain words (he cannot yet say many terms aloud), reads on an iPhone, and told me to "be straight" when I implied a look that did not happen.

RULES
1. Allowed writes: create the one handoff file (name check below). After verification and the privacy scan, commit and push that one file and nothing else (Second Sun allows auto-push; push main only). Do not modify, reset, clean, stash, check out, overwrite or commit anything else. Do not edit source, configuration, the book, RESUME.md or memory.
2. Do not run searches or experiments, download data, publish the book, write to Firestore, click the live Eyes page, or run pipeline/eyes_rules_test.py. Do not open event files under data\ or any event plot; do not report per-event information. Cheap read-only checks are allowed (git, grep, file listings, existing result files, the unit tests with the repo venv at D:\second-sun\.venv\Scripts\python.exe, scheduled-task listing, get_usage).
3. Labels: CONFIRMED (backed by a file, a tool run or a primary source you inspected), LIKELY, UNCERTAIN, NOT TESTED. Older notes say VERIFIED; treat it as CONFIRMED. Never mark something CONFIRMED because it was discussed or assigned.
4. Subagents and side sessions: report exactly what exists. If this session made no Agent calls, say "none". Look for linked sessions (list_sessions with linked true), the side session in seed fact 6, and saved reports under research\ and the scratchpad. If a transcript is inaccessible, say so. Never invent findings.
5. Preserve failures: rejected approaches, withdrawn controls, wrong diagnoses, known bugs, scientific caveats, unresolved questions. They are information, not clutter.
6. PRIVACY (the repo is public): aggregates only. No TIC, KIC or other IDs and no event times for any event in the real search, no Eyes device IDs, no Firebase keys or config, no email, no tokens. Known planet hosts and controls (TOI-1338, Kepler-16, and so on) are public and fine. Run a scan for ID patterns and secrets before committing; if it finds any, remove them and say so.
7. Do not duplicate VESPER-BRIEFING.md. Link its sections. Keep the handoff itself under about 4,000 words plus a claim-ledger appendix.
8. No en dashes or em dashes anywhere (use commas, colons, "to"). Plain words.
9. If the repo and this conversation disagree, write both and mark the discrepancy.

CHECKLIST
A. Repository: path, branch, HEAD, last 8 commits, git status (modified, untracked, ignored-but-important), unpushed commits, stashes, worktrees. Anything uncommitted?
B. Mission and pipeline: the research question, target population (G1, 549 stars, cuts), intended contribution, then the chain from raw light curves to detection, flags, tiers, reports, with exact file names. Production code versus prototypes versus proposals. The meaning of detection, lead, candidate (SS-IDs, two keys), validated, confirmed (book/docs/candidates.md, book/docs/book/10-vetting.md; ExoFOP wants publication first).
C. Actual progress: which stars were searched (all 549, 5,082 groups), data coverage, versions v1 to v7 with hashes and results, TOI-1338 b validation, STANLEY runs and limits, Stage 2 trial, upside-down controls, injection-recovery tests, pair search, the mono-cbp yardstick. Exact numbers, each with a source path.
D. Sessions and agents: see rule 4. Include accepted, rejected and never-implemented recommendations, and any conflicting conclusions.
E. Scientific validity: false-positive mechanisms, the lopsided-noise problem and the missing fair null for the raw-light half, what independent validation has and has not happened (none by a human or outside team), and what the strongest next experiment is.
F. Decisions, constraints, rejected approaches, hazards: frozen versions never tuned; real events private; GPL; the list of things not to run (rule 2); known quirks (python heredocs hang, separate venvs, stage3.py run refuses because the report is inside the freeze hash, data\ not in git).
G. Non-science state: the book and publish procedure (push main, then research\burn-3-book\tools\publish_book.ps1), Eyes mode and scoring, the paused Artifact, TODO-after-reset, scheduled tasks (list them and their health), the usage ledger and cap, Remote Control. Do not fetch Ahmed's Eyes scores; he said it wastes tokens.
H. Working agreements and Ahmed: read the memory entries that apply to Second Sun and copy their rules into the handoff (phone-first replies; questions in plain chat text, never popups; tiny edits are mine, big decisions are Ahmed's; ask before using subagents; end finished-work replies with a "Next:" line giving step, why, cost and whether it needs Ahmed; narrate friction as it happens; the usage ledger; Compass for big proposals; verify science with sources; no manual data copying; never click the live Eyes page). Note that a fresh session started in D:\second-sun will NOT auto-load that memory folder.
I. Where we left off: the last 15 exchanges in order (Ahmed's request, what was done, what was promised, what is waiting), including the seven raw-light dips nobody has looked at, the "be straight" correction, the name Vesper, and the questions still unanswered.

DELIVERABLES (sections of the file)
1 Executive summary: where Second Sun actually stands (10 lines).
2 Verified repository and Git state.
3 Current pipeline and configurations (point to VESPER-BRIEFING.md sections 4 to 6).
4 Completed experiments and exact results (with source paths).
5 Sessions, agents and outstanding delegated work.
6 Known bugs, limitations and unresolved questions.
7 Decisions, constraints, rejected approaches and hazards.
8 Ahmed's open decisions, with options and costs. Do not choose for him. Name the single task you would recommend and why, clearly marked as a recommendation.
9 A numbered next-step plan with acceptance criteria, ordered, including what each step must not touch.
10 Files to read first, with paths, in order.
11 Commands and tests that verify the current state (each cheap and read-only).
12 Claims the next session must not assume are true.
13 Working agreements and how to talk to Ahmed.
14 Non-science threads (book, Eyes, Artifact, scheduled tasks, side session, usage).
15 Where we left off, step by step.
16 Memory carry-over: which memory files apply, their path, and the auto-load caveat.
17 Appendix: claim ledger (claim, value, source path, label) for every number in the file. Also a "NOT RECOVERED" list.

SAVE, VERIFY, REPORT
- File: SESSION_HANDOFF_2026-10-28.md in D:\second-sun (repository root), only if that exact name does not exist. If it exists, do not overwrite; use SESSION_HANDOFF_2026-10-28_b.md (then _c) and say so.
- Verify: re-run git status and HEAD; check every path in the file exists; check the hashes quoted equal those in SETTINGS_FROZEN files; run the cheap checks in section 11 yourself and record the outcome; run the privacy scan; confirm no dashes (en or em) in the file.
- Commit and push only the handoff file, then confirm local HEAD equals origin/main and git status is clean.
- Final response (phone-readable, under about 30 lines): exact path, GitHub link, git status, what you could not recover, a 10-line digest, and a "Next:" line. Do not begin the next research task.
```

---

## 7. Prompt B: the revised opener for the fresh session (paste after the handoff exists)

```text
We are continuing Second Sun from a previous, extremely long Claude Code session. You are taking over an existing scientific project, not starting a new one. Ahmed is the owner.

Where to run: start this session in D:\second-sun, with no worktree. Its memory folder (C:\Users\hanzl\.claude\projects\D--second-sun\memory\) was seeded on 28 Oct with a copy of the Second Sun entries, and D:\second-sun\CLAUDE.md loads. If that memory is not visible to you, read C:\Users\hanzl\.claude\projects\C--CLaudeCode\memory\MEMORY.md and every Second Sun entry there explicitly before anything else.

Read, in this order: D:\second-sun\CLAUDE.md, D:\second-sun\SESSION_HANDOFF_2026-10-28.md (if the previous session reported another filename, use that exact one), D:\second-sun\RESUME.md (top), D:\second-sun\VESPER-BRIEFING.md, D:\second-sun\research\COMPASS.md. The handoff is a starting point, not unquestionable truth.

Before any implementation or experiment:
1. Inspect the current branch, HEAD and working-tree status yourself (expected: main at or after 1848a6b, clean).
2. Verify the handoff's most important claims against the repository and result files (aggregate_v7.txt, SETTINGS_FROZEN.json, claims.csv). Report any discrepancy.
3. Preserve all existing changes. Never reset, clean, discard, overwrite or commit unrelated work.
4. Find the exact point where work stopped, and the most important unresolved scientific question.
5. List the scheduled tasks and any linked sessions and say what state they are in.

Then give a concise, phone-readable status report: what is confirmed to work; what remains incomplete; what is scientifically uncertain; what must not be repeated; Ahmed's open decisions; and the single highest-priority next action with acceptance criteria and a cost estimate from research/usage-ledger.md.

Standing rules: no implementation, experiment, download, publish or subagent until Ahmed approves your proposed next action. Ask questions in plain chat text, never in popups. Tiny edits (wording, claim rows, field notes, ledger rows) are yours; big decisions are Ahmed's. No real event is inspected without Ahmed's explicit yes. Real events stay private; aggregates only. Use CONFIRMED, LIKELY, UNCERTAIN and NOT TESTED. No en or em dashes. Plain words (Ahmed is still learning the terms). End every finished-work reply with a "Next:" line. Do not restart the investigation, redesign the architecture or build a new tool just because this is a fresh conversation.

Our objective remains a scientifically defensible, reproducible search for circumbinary planets. Interesting signals are not discoveries.
```
