# The Tree as the project's brain: plan (Ahmed's ask, 14 Nov 2026; written by Claude Opus 5.5)

**What Ahmed wants:** one place that holds the WHOLE project: the work we do, what we find, what we learn (from research or anything else), every change, every decision, every open question. Highly interactive: open anything, learn anything, technical depth allowed. PC view primary, mobile works. It is the main brain of Second Sun, and keeping it current must NOT become a burden.

**The core idea: nobody "updates the Tree". The Tree is generated.** Everything it shows comes from files and habits we already have, plus one short line per piece of work. A builder script reads them and produces the map. If a thing is in the project, it is in the Tree, automatically.

## 1. What goes in: one shape for everything, the "card"
Every piece of knowledge is a card with the same few fields:
- **type:** finding, change, decision, lesson, research, fix, build, question, run, version, rule
- **node** (where it lives on the map, e.g. 1.4), **date**, **status** (open, done, superseded), **label** (CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED)
- **one plain line** (what it is), **why it matters** (one line), **links** (files, commits, reports, book pages)
- **supersedes / superseded by** (so old beliefs stay visible but crossed out, with the correction beside them)
- **plain explanation** and **technical depth** (both optional; the page shows plain first, "go deeper" on click)

## 2. Where cards come from (zero or near-zero extra work)
| Source we already keep | What the builder takes from it | Extra work |
|---|---|---|
| Git commits (every change is a commit) | a change card per commit, with its files | one trailer line: `Tree: 1.4 change` (or `finding`, `decision`, `lesson`) |
| Research files (blueprint already demands labelled findings) | a finding card per `### ...` heading carrying CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED | none: the blueprint format IS the card |
| FIX-QUEUE, BUILD-QUEUE | fix and build cards, open or done, with their node heading | none |
| research-sessions.md, Codex inbox and reports | research and run cards, cap and usage | none |
| RESUME LATEST blocks | the timeline ("what happened today"), Ahmed's instructions as decision cards | none |
| versions.md, FREEZE files, usage ledger | version and cost cards | none |
| Memory feedback files (rules Ahmed set) | rule cards ("how we work"), private memory never published, only a sanitised one-liner | none |
| Fable and auditor skills | lesson cards | none |
**Only truly new habit:** the one-line `Tree:` trailer on commits, and a node tag on findings (`node 1.4`). tree_check enforces both, so forgetting is caught the same day.

## 3. What Ahmed sees (PC first)
- **The map:** the five branches (How we see, Where we look, How we prove it, Tools and book, plus Goal), zoomable; each node shows its health at a glance: open fixes, last finding, progress, confidence colour.
- **Click any node:** a side panel with everything on it: plain summary, findings (newest first, superseded ones crossed out), changes, decisions, open questions, the files and commits, and "learn this": the book chapter and glossary words for it.
- **Timeline:** scroll the project day by day; filter by type (only findings, only decisions, only changes); "since you last looked" highlights what is new (kept in the browser).
- **Search everything:** one box over all cards, files and plain text.
- **Road to G1 and progress bars** on top, always current (from the Tree's own road section).
- **Follow a thread:** click a finding and see the chain: question, research, finding, decision, change, test, result (cards link to each other).
- **Mobile:** the same data as a drill-down list (branch, node, cards), the map hidden; readable on the phone.

## 4. How it stays cheap
- **Generated at every book publish** (`publish_book.ps1` already runs on every change): the builder reads the sources, writes one JSON file, the page renders it. No hand-edited page.
- **A git hook** reminds (does not block) when a commit lacks the `Tree:` line; tree_check fails on research findings without a node.
- **Codex follows the same convention** in its reports, so its work lands on the Tree with no translation.
- **Old material is backfilled once** by the builder from the existing files (research-sessions, queues, RESUME, reports), labelled "backfilled".

## 5. Safety (REVISED 14 Nov 2026, 16:15: Ahmed lifted the star-data privacy rule; star ids, star data and event details go on the Tree plainly. What still blocks a drop: unblinding a sealed run, fence A or B stars or private memory text; a named lead before two keys is allowed if marked 'not checked yet'. The old lines below are superseded where they say otherwise.)
- The builder never copies star ids, event times or lead details: it reads only counts-and-text files and runs the same privacy scan as publishing (block on `tic`, centres, `source_id`).
- Private memory content is never published; only rule titles Ahmed approves.
- The Tree shows only what is already in the repo; `data\` is never read.

## 6. Phases
- **Phase 0, now (small, before G1):** adopt the two habits (commit `Tree:` trailer, node tag on findings) so the material is already structured when we build; tree_check warns on missing tags. About 0.3 weekly points.
- **Phase 1, first build after G1 is locked (T160):** the builder script and the JSON; design rounds with Ahmed (map style, colours, what a node panel shows first) in question rounds; then the PC page; then the mobile list.
- **Phase 2:** "follow a thread" links, "since you last looked", search, and the Codex convention.
- **Phase 3:** the control room and learning track read from the same JSON (one brain, many views).

## 7. Open design questions for Ahmed (Phase 1 rounds, not now)
Map style (tree, mind map, metro map); how much technical text a panel shows by default; whether lessons from mistakes are public; colours with the planned colour change.

## 8. Ahmed's refinement (14 Nov 2026, 14:20): a neural knowledge graph
"Like a neural network... a neural knowledge graph... hold everything about the project in one visualization, which could be opened into more detailed, and I could basically learn anything from there."

**So the Tree is a graph, not a list:**
- **Dots (nodes):** every card (finding, change, decision, lesson, research, fix, run, rule, question, version), plus concept dots for the ideas themselves (eclipse mask, upside-down arm, momentum dump, TOI-1338 b, P bar, Petrova) and the five branches as big hubs.
- **Lines (edges), each with a meaning:** led to, tested by, found in, fixed by, supersedes, depends on, part of, learned from, measured on, contradicts. A line is drawn brighter when the evidence is CONFIRMED, faint when UNCERTAIN.
- **Edges are mostly found automatically**, so no burden: a card that names another card's id (FIX 94, RS-025, T160, Codex 010, node 1.4, a file path, a commit) links to it; two cards touching the same file link weakly; the research blueprint's "decision it feeds" column becomes a "led to" edge; "superseded by" lines come from the corrections we already write.
- **Semantic zoom (one picture, opened into detail):** far out you see the five hubs and their health; zoom in and hubs open into their nodes; further in, each node's cards; click a card for its plain explanation, then its technical depth, then the actual files and numbers. The neighbourhood of whatever you click lights up, like a neuron firing: everything connected to it, one or two steps away.
- **Learning paths:** pick any concept dot ("why do slow binaries lose planets?") and the graph shows the chain of cards that explains it, in order, with the book chapters attached.
- **Time slider:** drag back to any date and see the brain as it was then; watch findings appear and old beliefs get crossed out.
- **PC:** a full-screen graph view (WebGL force layout so thousands of dots stay smooth) with a side panel; **mobile:** the same graph simplified to the neighbourhood of one dot at a time, plus the tap-through list.
- **Same JSON feeds it:** the builder of section 4 writes nodes and edges; nothing is drawn by hand.

## 9. Ahmed's idea (14 Nov 2026, 16:05): the Drop box and the auto-builder
"We make changes, we go around our day... then we just give it to the Python scripts. They do the sorting and the code writing, and we just put it into our website."

**Shape:** a folder `drops/` in main (not a branch: branches get forgotten; git history is the backup). At the moment a piece of work ends, the worker (Claude or Codex) writes ONE small file there in the card shape of section 1 (type, node, date, label, one plain line, why it matters, plain explanation, technical depth, links, supersedes). Python never writes the words; it sorts, checks and formats them.
**One drop fans out to every place we now hand-edit:** the Tree JSON (dots and lines), the book field note, the learning-track chapter hook, the home "Two-minute recap", the versions row, the RESUME LATEST block, the ledger row. Today each finished task means about six hand edits; with the Drop it is one file.
**The builder `tools/brain_build.py`:** reads drops plus the auto-sources of section 2; refuses (does not fix) a drop with a missing field, an unknown node, an unexplained id, or a science-rule hit (sealed-run unblinding, fence A or B stars, a lead not marked 'not checked yet'); star ids are allowed (Ahmed, 14 Nov 2026), so the publish privacy scan must be loosened to match; writes generated files only; then `publish_book.ps1 -Test` pushes gh-pages as it already does (GitHub Pages, no Netlify needed). Preview locally first; any failed check stops the push.
**When:** drops are written the moment work ends (memory and context fade); building and publishing can be batched (end of day, or at once after a big task).
**Phasing:** the drop habit replaces the commit trailer of Phase 0 and can start before G1; the builder is part of T160 after G1.
