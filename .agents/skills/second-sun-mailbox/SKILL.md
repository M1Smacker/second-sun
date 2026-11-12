---
name: second-sun-mailbox
description: Use in Second Sun whenever you pick up a brief from research/astra/inbox, start or finish a task for Claude or Ahmed, write a report, make a branch, or hand work back. The exact protocol for passing work between Codex and Claude Code without Ahmed copying anything.
---

# The Second Sun mailbox (Codex and Claude Code, written 12 Nov 2026)

Ahmed never copies text between us. We talk through files in git. Ahmed only says "go" to each of us.

## Folders
- `research/astra/inbox/NNN-<name>.md`: briefs FROM Claude (or from Ahmed, written down by Claude). Numbered 001, 002, ...
- `research/astra/reports/NNN-<name>.md`: your answer to brief NNN (same number). One report per brief. A report for work Ahmed asked for in chat without a brief gets the next free number and the name `NNN-chat-<topic>.md`.
- `research/astra/scripts/`: your scripts (one command each; print counts, never star ids).
- `research/astra/USAGE.md`: your usage rows.
- `data\astra\`: your machine outputs (private, not in git).

## Your worktree and branch
You work in your own checkout `D:\second-sun-astra` (a git worktree of the same repo, so Claude's working copy at `D:\second-sun` is never disturbed). Its `data` folder is a link to the real `D:\second-sun\data` (read anything allowed by the fence; write only under `data\astra\`).
1. Start: create your branch from the local main: `git switch -c astra/NNN-<name> main`. If the branch exists, `git switch astra/NNN-<name>` and `git merge main`. (Main is checked out in Claude's folder, so git will not let you switch to main in yours; you never need to.) The newest briefs are on main, so read them with `git show main:research/astra/inbox/NNN-<name>.md` if your branch is older.
2. Commit small and often on that branch, messages that say what the payload IS ("counts only" only if it is true). Never commit star ids, event times or lead details.
3. Never push, never merge into main, never rebase main. Claude merges after review.

## Picking up a brief
1. Read the brief top to bottom. Note its MODEL and EFFORT line; if you are on another model, say so first in the report.
2. Write your PREDICTED usage row in `research/astra/USAGE.md` before starting.
3. If the brief needs a hard rule broken (AGENTS.md section 4), do not start that part: write it under STOP SIGNS.
4. Ask Ahmed in chat only for a real fork that blocks the work. Otherwise choose the safe default, say which, and continue.

## Report format (`research/astra/reports/NNN-<name>.md`)
```
# NNN <title> (Codex, <model> <effort>, <date and Kuwait time>)
**Plain verdict:** <one line: found nothing / N issues, M need a fix / done>
**Branch:** astra/NNN-<name> (<k> commits) or "no file changes"

## Findings
1. <finding>. LABEL (CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED). Evidence: <script + its printed numbers, or file:line, or link + exact sentence>. Why it matters: <decision it changes>.

## What I did NOT check
## STOP SIGNS hit
## QUEUE PROPOSALS (Claude files them: FIX for bugs, BUILD for builds and studies)
## IDEAS (cost, and what decision each serves)
## Disagreements with Claude (each with the script or source that shows it)
## Questions for Ahmed (plain words, at most 3)
## Usage: predicted <x>, actual <y>, lesson <z>
```
No en or em dashes. Counts only. Keep it as short as the findings allow; put long tables in a second file next to it.

## Handing back
Tell Ahmed in chat, in one or two plain lines: what the verdict is and that report NNN is ready for Claude. Claude then reads the branch, runs `research/astra/tools/fence_check.py`, tests, and merges or answers in a new brief (which may reply to your disagreements). A brief that answers you quotes your report number.
