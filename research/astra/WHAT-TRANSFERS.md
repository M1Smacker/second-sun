# What of Claude's toolkit transfers to Codex, and what it improves (12 Nov 2026, Claude Opus 5.5)

Method: I listed everything Claude Code uses on Second Sun (instructions, memory, skills, scripts, habits, app tools), checked each against what the Codex app on Ahmed's PC has (`C:\Users\hanzl\.codex`: app version 26.1106, plugins browser, computer use, documents, pdf, spreadsheets; models and effort levels low to max from `models_cache.json`), and decided: COPIED, POINTED (Codex reads the original), REPLACED (Codex has its own), or NOT TRANSFERRED (and why).

## Transferred
| What Claude uses | How Codex gets it | Status |
|---|---|---|
| `CLAUDE.md` standing rules | merged into `AGENTS.md` (Codex reads it every session), plus Codex may read `CLAUDE.md` itself | COPIED |
| Claude's private memory (70 files: Ahmed's rules, decisions, lessons) | `research/astra/claude-memory/` in the Codex worktree only (gitignored, never committed) via `tools/sync_kit.py` | COPIED (Claude reruns the sync after changes; `--check` catches drift) |
| `second-sun-auditor` skill (Fable audit lessons, stop signs, worked bugs) | `.agents/skills/second-sun-auditor/` with a Codex reading note on top | COPIED |
| `my-take` skill (the opinion format Ahmed approved) | `.agents/skills/my-take/` | COPIED |
| Research blueprint, research-session numbering | `.agents/skills/second-sun-research/` (points to `research/RESEARCH-BLUEPRINT.md`), stints AS-NNN | POINTED |
| Usage prediction and calibration habit | `research/astra/USAGE.md` (predict first, actual after, lesson) | REPLACED (Codex's usage panel instead of `get_usage`; whether Codex can read its own panel is UNCERTAIN, so ACTUAL may lag) |
| RESUME.md as the cold-start state | Codex reads it first every session; its own memory is the map in report 001 | POINTED (Codex never edits RESUME) |
| Star-id privacy and the push check | rule 3 in `AGENTS.md`; `fence_check.py` adds the blind-star fence, the frozen-file check and the data-write check | COPIED and extended |
| Frozen-filter discipline, preregistration, no tuning on results | `AGENTS.md` rules 1, 2, 6 | COPIED |
| Watchdog for long runs | Codex may run `research/fable-audit-2026-11/scripts/watchdog.py CONFIG.json` for its own jobs | POINTED |
| Pipeline scripts (gates, readouts, zero-diff, compare) | usable on design-seen stars and synthetic light only | POINTED (fenced) |
| Browser checks of the book at phone width | Codex browser plugin, local `mkdocs serve` only | REPLACED |
| Writing style for Ahmed (no dashes, phone-first, plain verdict, Next line, clock) | `AGENTS.md` section 6 | COPIED |

## Not transferred, on purpose
- **Publishing the book, pushing to GitHub, merging into main, freezing versions, writing preregistrations and amendments**: first-key work, stays with Claude. A second writer to main would break the record of who decided what.
- **Shared ledgers and queues** (`usage-ledger.md`, `research-sessions.md`, `FIX-QUEUE.md`, `BUILD-QUEUE.md`, `mission.yml`): Codex proposes lines in its report; Claude files them. Two writers on one file in two checkouts make merge conflicts, and the queues contain NUL bytes that a text write corrupts.
- **The live Eyes page and Firebase**: never, for either of us.
- **Claude-only app tools** (Artifacts, session management, the Claude browser pane, scheduled Claude tasks, Remote Control): no Codex equivalent needed.
- **gstack and design skills** (review, qa, cso, design): general tools, not Second Sun knowledge; Codex has its own plugins.
- **Secrets** (ADS key, Firebase key, `D:\second-sun-secrets`): never.

## Where Codex can make the project BETTER (not just copy Claude)
1. **A different brain as reviewer.** Every Claude check so far is a producer check: the same model that built the code checked it. The Fable audit (10 Nov) found the eclipse mask bug that three Claude-built hunts missed. A second model family is the cheapest way to get that kind of outside eye regularly.
2. **The "outside re-derivation for every decision number" rule** (auditor skill, section 8, recommended by Fable, never made routine because it cost Claude's meter twice) becomes affordable: Codex re-derives, Claude builds.
3. **Compass reviews** (`research/COMPASS.md`) of big proposals by a model that did not write the proposal.
4. **Long reading on a cheap model**: scanning the 780 research files, indexing papers, checking the book's links and claims (Luna), instead of spending Claude's weekly meter.
5. **Machine experiments in parallel**: Codex can run design-seen experiments (part C and D of brief 002) while Claude builds something else, within the shared CPU limit.
6. **Book drafts**: field-note drafts, learning-track checks, glossary entries, the units foundation (T133) drafted by Codex and reviewed by Claude, which keeps the learning track in sync with findings (a standing rule that often lags).
7. **Science strength**: on independent tests Astra leads Opus 5.5 on science tasks (Vals Science Index 65 against 59, Terminal-Bench-Science 63 against 47), while Opus leads on most coding (CONFIRMED on vals.ai, read 12 Nov 2026). That fits the split: Codex judges the science, Claude writes the code.

## Risks and how the kit handles them
| Risk | Guard |
|---|---|
| Codex looks at blind stars and spoils the G1 or a Census sealed search | Fence A/B in `AGENTS.md`; `fence_check.py` scans its session logs, branches and data writes before every merge (tested: it fails on a planted fenced id) |
| Codex edits the frozen filter | rule 1; `fence_check.py` counts frozen-file changes on every astra branch; `r1_run.py` refuses a frozen run if hashes differ |
| Two agents trample each other's files | Codex works in `D:\second-sun-astra` (a git worktree on its own branch); Claude's checkout is untouched |
| Codex's copy of Claude's rules goes stale | `sync_kit.py --check`; RESUME.md wins over memory |
| Star data used for OpenAI training | privacy switches in `SETUP-FOR-AHMED.md`; no thumbs ratings |
| Scarce Astra spent on chores | model table in `AGENTS.md` section 7; every brief names model and effort |
| Codex and Claude disagree and Ahmed is stuck in the middle | disagreements must come with a script or source; Ahmed decides as second key; Claude answers in a brief |
