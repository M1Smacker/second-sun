# Search window blueprint: how to prepare, start and close the live card for ANY search (written 11 Nov 2026 at Ahmed's request)

Follow this top to bottom. It replaces re-planning the page each time. Every step is a command or a check; nothing needs a decision except the go word. Worked example: Re-search 1 (11 Nov 2026), files named in each step. Counts only, always: no star id, no event time, no picture of a real event in a blind run.

## 0. What the card is
The Search window page (`book/docs/watch.md`, script `book/docs/assets/watch.js`) reads ONE small JSON of aggregates. The JSON is made by `pipeline/watch_export.py`, pushed to the data branch `watch-data` (never main) and read by the page from GitHub, so the card updates by itself with no book publish. States: `ready` (prepared, not started, ring with no fill), `search` / `sap` / `pdc` (running), `finished`. Blind mode pools real and upside-down; counts-only mode also removes pictures and the star list.

## 1. Before anything: preconditions (all must be true)
- The version is frozen: its settings file exists (Vesper: `research/stage3/SETTINGS_FROZEN_V81.json`; Petrova: `SETTINGS_FROZEN_P100.json`). If not frozen, the card may still be prepared but its label must say "NOT FROZEN YET" (the exporter does this by itself: `run.version`).
- The star list is fixed by a hash in the preregistration.
- The go rule: the run script refuses without its go file (`R1-GO-<stratum>.txt`, `G3-GO.txt`). The go file is written only after Ahmed's words; quote them in it.

## 2. Archive the previous campaign (2 minutes)
1. `copy book\docs\assets\data\watch.json book\docs\assets\data\watch-<previous>.json`
2. Check it holds no star id: open the JSON with Python and confirm `counts_only` is true and `ticker` is empty (a sealed run before G3 kept pictures by Ahmed's 30 Oct yes; do not copy those into a new file).
3. Add a link to it in the campaigns note of `book/docs/watch.md` (format `[open the finished X run](?src=../assets/data/watch-<previous>.json)`).

## 3. Prepare the card ("prepared, not started")
1. New campaign: copy `ready_r1()` in `pipeline/watch_export.py` to `ready_<name>()` and change four things: the list file, the sets (`g2`, `g3`, ...), the version file, the counts it reports. Add a `--ready-<name>` flag next to `--ready-r1` (3 lines).
2. Run: `python -W ignore watch_export.py --ready-<name> --push --label "<NAME>: <version> on the N stars ... (blind, counts only)"` (venv python, from `pipeline\`). It writes `book/docs/assets/data/watch.json` and pushes it to `watch-data`.
3. Update the campaigns note in `watch.md` (what it searches, blind, counts only, what waits). The wording of the "prepared" line in `watch.js` follows the version state by itself.
4. Check the JSON: `phase` is `ready`, `run.version` is right, `progress.stars` and `list_stars` match the list, `counts_only` true.

## 4. Publish the book (when the page text changed)
1. Version: book third number up for fixes, second number up for a new tool or page (`book/docs/versions.md` row and `book/mkdocs.yml` footer).
2. `git add` the changed files and commit.
3. Star check: `python research\fable-audit-2026-11\scripts\push_star_check.py` (counts and file names only). A hit on a list that is already on `main` (g1, g2, g3 target lists) is allowed; a hit on an event, a lead or a new id is not.
4. `git push origin main`, then `research\burn-3-book\tools\publish_book.ps1 -Test` (background; log in `data\`). A failed check stops it before anything is published.
5. Confirm the live page 1 to 2 minutes later (`curl` the page and look for the new label text). Tell Ahmed in one line. Never click the live Eyes page.

## 5. Start the run (only after the go)
1. Write the go file with his words and the time (`R1-GO-<stratum>.txt`). The dry run on seen stars needs `R1-GO-seen.txt` only if the frozen hash differs from the development hash.
2. Start the go script detached: `pipeline\r1_go.ps1 [workers]` (template; copy and edit label, sets and star counts). It saves the library versions, starts the exporter (`--blind --counts-only --wait --loop 60 --push --label "<quoted label>"`) and then the run. 70 percent CPU: 6 workers on his 12 cores, numba threads capped (the script sets them).
3. One minute after launch check: the exporter process is alive, the label in the JSON is the full quoted text (an unquoted label is cut at the first space), `watch_plan.json` exists in the run folder, the data branch has a new commit. Register the job in `research/jobs.md`.
4. Then do not watch it. A background waiter on a line in the log (`SEARCH DONE`, `ALL SEARCH STEPS DONE`) is enough; read the log tail every 30 to 60 minutes at most.

## 6. After the run
1. The feed ends by itself at `finished`. Add one note line: `python watch_export.py --note "..."`.
2. Counts first, plain verdict first (found something, found nothing, N leads under check), then the numbers. Leads stay private until two keys and Ahmed's yes.
3. Campaign note in `watch.md` gets the result line; book publish as in step 4; same-day field note.

## 7. Pitfalls already met
- An unquoted `--label` was cut at the first space. Quote it inside the argument list.
- The Browser pane is hidden overnight and its timers crawl: judge the card by its JSON, not by watching it.
- A run folder name is built from the settings hash; a changed hashed file means a new folder and a new version.
- `S2.groups()` takes about two minutes per list: the exporter caches it in `watch_plan*.json`.
- The data branch is a scratch clone in `D:\ss-watch-data`; never write the feed to `main` by hand.

## 8. Not automated yet (filed in BUILD-QUEUE)
One config file per campaign (`research/stage3/campaigns/<name>.json`: label, sets, list, version file, parts) so steps 3 and 5 need no code copy. Until then, the copy in step 3.1 is the only code edit.
