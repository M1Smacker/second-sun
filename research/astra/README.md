# research/astra: where Claude Code and Codex work together

Started 12 Nov 2026. Ahmed bought (or will buy) ChatGPT Plus for one month to give Second Sun a second AI: **Codex**, mostly on GPT-6 Astra for big judgements and smaller models for normal work.

**Roles.** Claude Code is the first key (decides, builds, merges, publishes). Ahmed is the second key (says yes or no). Codex is the helper and reviewer: it audits, re-derives, tests, researches and drafts on its own branch. Rules for Codex: `AGENTS.md` at the repo root.

**How work moves (Ahmed never copies anything):**
1. Claude writes a brief: `inbox/NNN-<name>.md`, commits it on main.
2. Ahmed tells Codex "go" (Codex reads `AGENTS.md`, finds the newest brief without a report).
3. Codex works in its own folder `D:\second-sun-astra` (a git worktree: same repo, separate checkout, branch `astra/NNN-<name>`), writes `reports/NNN-<name>.md`, commits on its branch. It never pushes.
4. Ahmed tells Claude "Codex finished NNN". Claude runs `tools/fence_check.py`, reads the report and the diff, tests, merges what is right, files queue items, and answers in the next brief.

**Files here**
- `inbox/`, `reports/`: the mailbox.
- `scripts/`: Codex's scripts.
- `tools/sync_kit.py`: Claude copies its private memory and skills into the kit (`claude-memory/`, `.agents/skills/`). Rerun after memory changes; `--check` says if the copy is stale.
- `tools/fence_check.py` (+ `test_fence_check.py`): proves Codex did not touch the blind stars (G1, and the 803 hold-out stars), the frozen filter files, or `data\` outside `data\astra\`. Counts only.
- `claude-memory/`: Claude's memory, copied (rules Ahmed gave, decisions, lessons). Local only: it lives in the Codex worktree, is gitignored, and must never be committed (the repo is public).
- `USAGE.md`: Codex's usage rows. Claude's own ledger stays `research/usage-ledger.md`.
- `SETUP-FOR-AHMED.md`: the one-time steps after buying.
- `WHAT-TRANSFERS.md`: what of Claude's tools and habits Codex can use, and what it cannot.
