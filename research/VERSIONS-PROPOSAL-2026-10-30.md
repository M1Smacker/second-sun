# What needs a version number, a baseline and a history (proposal, 30 Oct 2026; Ahmed: "find every single thing")

Status: **TRIMMED AND DECIDED 30 Oct 2026 (Ahmed: "be mindful ... not every single thing needs it"; F4 gets no version number; older level marks get their track version; Versions page next to the field notes).** Only six things keep a version: Vesper, the G2 test, the book, the learning track, Eyes mode, and the software baseline; the rest of the table below is dropped. The live version is `book/docs/versions.md`. CORRECTION to section 1: each Eyes round already carries a data-format number `v`, the deck name and a date, so its test version can be read from the date; no code change is needed. (Original status: PROPOSED by Claude, nothing renamed, tagged or published.) Evidence comes from `git log` (227 commits, 19 to 30 Oct), the field notes, `VESPER-VERSIONS.md`, `decisions.md` and the files named. Numbers marked "estimate" are retroactive reconstructions, labelled so on the page when published.

## 1. What actually existed, said plainly
- **Vesper had an internal version table since 29 Oct** (`research/stage3/VESPER-VERSIONS.md`: 0.0.0 to 0.8.0, settings hashes, a named baseline 0.7.1). So the history was not missing, but you are right about three things: it lives only in a research file and **not in the book**; the old names (v1 to v7, "Stage 3", "Penumbra") and the new numbers are mixed; and there was **no rule for what a baseline is or when to make one**.
- **Nothing else has a version.** Not the book, not the learning track, not Eyes mode, not the star lists or the data, not the preregistration, not the scorecard, not the software. The one automatic version is the offline-app hash the book already prints (the "Updated. Reload" banner).
- **A cost of that gap is already visible:** Eyes mode saves your answers with a storage key `ss-eyes-v1` only; no round records which test, deck or feedback version you took, so scores from different versions of the test cannot be told apart later. And I added learning-track checks today (L5 6 and 7, L6 7, 8 and 9), which silently changes what "L5 done" means.

## 2. The scheme (one rule for everything)
**MAJOR.MINOR.PATCH.** MAJOR: the thing's rules or its whole look or structure change, so old results or old progress are not directly comparable. MINOR: something is added (a page, a chapter, a check, a flag). PATCH: a fix or wording change that changes no result.
- **Baseline** = a frozen reference we compare later versions against. For each item: a name, a date, a git tag, and where relevant a hash. A baseline is made when (a) a version is frozen for a test, (b) before a redesign starts, (c) when a result is published.
- **History** = a short changelog per item (date, version, what changed, why, commit), kept in git and shown on one public **Versions** page in the book.
- **Git tags** (annotated) mark baselines: `vesper-0.7.1`, `vesper-0.8.0`, `book-2.4.0`, and so on. Tags are cheap and never rewritten.

## 3. The things that need a version (ordered by how much results or your progress depend on them)
| # | Thing | Why it needs one (evidence) | Proposed current version | Baseline | History kept in |
|---|---|---|---|---|---|
| 1 | **Vesper search chain** | Results depend on its exact rules; 8 frozen versions already | **0.8.0** (frozen 30 Oct, hash 5f73692944aa) | **0.7.1** for the study; **0.8.0 on G2 sealed** becomes the benchmark baseline once the sealed run is scored | `VESPER-VERSIONS.md` plus a Vesper page in the book (missing today) |
| 2 | **Software environment** (Python 3.12.10, numpy 1.26.4, scipy 1.13.1, wotan 2.0, astropy 7.2.3, lightkurve 2.6.0, numba 0.68.0 ...) | The freeze records code hashes but NOT library versions; a library update could change results | `ENVIRONMENT-2026-10-30` | recorded today in `research/stage3/ENVIRONMENT-BASELINE-2026-10-30.txt` | that file, one per frozen Vesper version |
| 3 | **Star lists** G1 (549 stars) and G2 (895: 301 development, 594 sealed) | Hash-locked lists; G2 split rule fixed | G1 1.0, G2 1.0 (hashes in the preregistration) | list hashes 38ad01b2..., 809212e5... | preregistration |
| 4 | **Data snapshots** (which TESS files, downloaded when) | MAST adds sectors and re-processes; the same star can have different files next month | G1-data (Oct 2026), G2-dev-data (29 Oct), G2-sealed-data (30 Oct; manifest) | the manifest file and download date | `data/g2/manifest.csv`, job list |
| 5 | **External reference tables** (TESS eclipsing binary catalogue, NASA archive pulls, TOI list, circumbinary host list, the professionals' table) | The TOI count (95) and labels change as NASA updates; stated "measured 29 Oct" in places | snapshot dates | `data/xmatch/*` hashes, to be recorded with dates | a small snapshot table |
| 6 | **Preregistrations and plans** | Rules written before results; already amended | G2 prereg **1.0** (locked 29 Oct) and **1.1** (Amendment 1, 30 Oct); Study plan 1.0; Sealed plan 0.9 draft | git tags at the lock and amendment commits | the amendments section |
| 7 | **Benchmark scorecard** (`benchmark_g2.py`, lines S1 to S8) | Pass marks must not change after the sealed run; it is committed but NOT yet recorded by hash | **1.0** | tag plus file hash written into the sealed run settings | git |
| 8 | **Completeness harness and paired yardstick** (`chain_recovery.py`, `paired_recovery.py`) | Labels v5, v6, v7, g2dev already differ; recovery numbers are compared across them | 1.0 (harness as of 0.8.0) | the rows files with date | `VESPER-VERSIONS.md` columns |
| 9 | **The book** | Public, changes daily, F4 coming | **2.4.0** (estimate, see section 4) | `book-2.4.0` tag now, before F4 | Versions page, `book/VERSION` |
| 10 | **Learning track** (levels L0 to L6, checks) | Your "L2 done, 3/3" depends on its contents; I changed it today | **1.3** (estimate: 1.0 20 Oct; 1.1 27 Oct one spine; 1.2 28 Oct checks; 1.3 30 Oct) | track 1.3 | progress line should record the track version at each "done" |
| 11 | **Eyes mode** (engine, official test, HARD test, feedback texts, strength function, answer record) | Scores over time must say which test they came from | **1.3** (estimate: 1.0 stage A 23 Oct; 1.1 HARD test 24 Oct; 1.2 feedback engine 24 Oct; 1.3 layout and calibrated results 27 Oct) | 1.3 | each saved round should carry `eyesVersion` (needs a small code change) |
| 12 | **Mission readiness score rules** (`mission.yml`) | The number you see depends on its formula | 1.0 | rules as of 21 Oct, plus later edits | git |
| 13 | **Claims register** (F-001 to F-090, B-, etc.) | Identifiers are stable; history is in git | release number = highest claim | one per publish | git |
| 14 | **Live data formats** (`watch.json`, the coming live channel) | The page and sender must agree | `schema: 1` (to add) | schema field | code comment |
| 15 | **Ways of working** (research blueprint 1.0 of 29 Oct; Compass 1.0; project rules in CLAUDE.md; decision log) | Behaviour rules change; already dated entries | blueprint 1.0, Compass 1.0, rules 1.0 | dates exist | git (decision log is already a history) |
| 16 | **Offline app shell** (service worker) | Already versioned automatically (hash) | automatic | none needed | none needed |

## 4. The book's version, estimated from history
Reconstruction from the commits and the 31 gh-pages publishes (first publish 20 Oct):
| Version | Date | What a reader would notice | Commit (main) |
|---|---|---|---|
| **1.0.0** | 20 Oct | First complete book: 15 chapters, labs, learning track, glossary (Bible Overhaul batches 1 to 6) | 2f3ca9a |
| 1.1.0 | 21 Oct | Mission readiness bar, one label vocabulary | 8ce5e8e |
| **2.0.0** | 23 Oct | Navigation redesign: real-sky home map, tabs, chapter template, one diagram per chapter | f5a3a3f |
| 2.1.0 | 23 to 24 Oct | Eyes mode, cloud backup, HARD test, feedback engine | ca40167 to a632adb |
| 2.2.0 | 27 Oct | One learning path; F4 steps 1 and 2 (Atkinson and Plex type, symbol files, PC chapter rail) | 8deaa5c, 8dcdfe6 |
| 2.3.0 | 28 Oct | The first real search page, new sections in chapters 7 to 10 | a1f23ec |
| **2.4.0** | 30 Oct | Search window page with live counts and pictures, chapters 9, 10, 14 additions, learning checks | 07ecbf6 |
**Estimate: the book is now 2.4.x.** F4 (the complete redesign with the new colours and rounded bars) is the next change of look and structure for everything, so it should be **3.0.0**. A baseline tag `book-2.4.0` should be made BEFORE F4 starts, so the old book stays reproducible. The 23 Oct navigation redesign is counted as 2.0.0 because it changed how the whole book is navigated; if you prefer to keep "2.0" for F4, the numbers shift by one (1.x, then F4 as 2.0.0); that is your call.

## 5. What I would build after your yes (small, in this order)
1. Make the baseline tags (`vesper-0.7.1`, `vesper-0.8.0`, `book-2.4.0`, the preregistration tags) and push them.
2. A **Versions page** in the book: Vesper history, the book's own history, the track and Eyes histories, and what a baseline is, in plain words, with a link from the footer. (Uses the new rounded bar style where it shows anything.)
3. `book/VERSION` and a visible "Book 2.4.0" in the footer, set by the publish script so it cannot be forgotten.
4. Add `schema` to `watch.json`; add `eyesVersion` and the track version to what Eyes and the progress line save.
5. Record the scorecard hash and the environment file in the sealed run settings, and note them in the preregistration.
6. Put the external-table snapshot dates in one small table.

## 6. Questions only you can answer
(a) Is 2.4.0 now and 3.0.0 for F4 right, or do you want F4 to be 2.0.0? (b) The learning track gets a version recorded when you mark a level done: do you accept that older "done" marks are labelled "track 1.0 or 1.2"? (c) Should the Versions page be a Records page next to Field notes?
