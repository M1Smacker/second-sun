# Area R findings (process, project health, privacy). Read at commit c9b9aca.

## F-17. Privacy: G2 sealed star IDs are public in the history of the `watch-data` branch, under commit messages that say "counts only". CONFIRMED. Fable used: yes (small).
- The repository is PUBLIC (`gh repo view`: PUBLIC) and has a public branch `watch-data` (87 commits, all titled "watch: counts only").
- The current file is clean: counts only, 0 ticker rows, no star id.
- Older commits are not: three old commits I opened carry a `ticker` with `tic` and `sector` rows under the label "SEALED RUN: Vesper 0.8.0 on the 594 sealed G2 stars (blind)". `pipeline/watch_export.py` lines 146 and 228 write `tic` and `sector` into every picture card and ticker row unless `counts_only` is set, and line 254's own comment admits "earlier commits all said counts only; the older feeds did carry star pictures".
- What leaked: which G2 sealed stars had events in which sectors, with product, tier, SNR, depth and duration. Not the event time itself (pictures are in hours from the event centre), but star plus sector plus depth is enough for anyone to find the dip in public light. No lead exists in G2, so no candidate is exposed; the rule "star IDs never public" is broken.
- This is the open 4 Nov item "keep or strip G2 star details on the feed". Removing it means rewriting a public branch (an outward action): Ahmed's yes needed. Work order WO-F17p.
- Going forward: make `counts_only` the default in `watch_export.build` and require an explicit flag for cards, with `tic` never written (use a salted hash label). Sonnet ok.

## F-18. Rules and memory: nine live conflicts, a stale core, and a bookkeeping stack that eats points. LIKELY (from H1, `evidence/history/H1-resume-rules.md` section 4; I did not re-read the memory files). Fable used: judgement only.
Proposals for the originals (report only; nothing edited):
1. Mark as overridden or delete: "Ask before helpers" (three later rules disagree), "Daily usage cap", "25% and 23%" in CLAUDE.md, "Horizon NOT started", "G3 waits for go", "three weeks, no new designs".
2. One label vocabulary everywhere: CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED (the book still uses VERIFIED / UNVERIFIED).
3. The per-task stack (RESUME block + field note + chapter and quiz + daily recap publish + ledger + versions row) produced 8 book publishes in one night and a 16,000 word RESUME. Proposal: RESUME keeps ONE current block of at most 400 words plus a pointer to `RESUME-ARCHIVE.md`; recap and field note once per day, not per task.
4. New standing rule proposed: "every recovery or completeness test injects into the raw light, before any step of the search" (from F-01).
5. New standing rule proposed: "the two arms must be exchangeable: any step that looks at the sign of the flux (mask, flags) is applied in mirror to the upside-down arm".
Merged into the skill (section "Merged rules"): verify before concluding; cheapest check first; unverified is not fixed; read the clock; never click the live Eyes page; downloads logged; no dashes; phone-first; "Next:" line; outside check on decision numbers; size caps by tool calls.

## F-19. Queues: dead and duplicate items. LIKELY (from H2 section 3 and 4; statuses not re-checked in code). Fable used: no (routine; Sonnet can apply after Ahmed's yes).
- FIX-QUEUE, stale or closed in fact: FIX 30 (c6 was built and frozen), FIX 70 (hashed union table exists for G3; G1 and G2 still exposed: restate), FIX 12, 13, 20 (superseded by chain recovery and Horizon), FIX 72 (dead unless the script is reused), FIX 79 (close: six publishes since), FIX 84 (settled by F-02: restate as "bit 29 from Sector 94"). FIX 27 is a build, not a bug. FIX 26 duplicates T137.
- BUILD-QUEUE, done but unticked: T104, T111, T112, T122. Dead or parked: T37b, T121, T123, T131, T132, T56, T118, T124. Duplicates: T106 = T141; T128 = T142; T55 = FIX 69; T50 = T43; T101 conflicts with FIX 6.
- Re-rank after this audit: the new top item is the Petrova 1.0 mask (WO-F01), above T136/T139 (Census), T137, T34.
- FIX 11 and FIX 14 (detrending window, mask before detrend) should be done in the same Petrova 1.0 pass as the mask.

## F-20. Tests and reproducibility: top 5 problems. LIKELY. Fable used: judgement only.
1. No test injects before the mask (F-01). The whole completeness chain tested the wrong path, the same family as the 23 Oct loader bug.
2. Tests can print "pass" after "skip" (FIX 83) and nothing runs them automatically.
3. 65 of 111 pipeline files have hard D: paths (FIX 82): a stranger cannot rerun G3 from the repo. Also the data are git-ignored with no manifest of hashes published, so even with paths fixed a rerun cannot be checked against ours.
4. The zero-difference proofs show a version equals the previous one. They cannot show either is right; they froze F-01 into every version.
5. The private backup of G1 to G3 events sits on the same disk as the source (H1). One disk failure loses the sealed results.

## F-21. Cost per result (half page). LIKELY. Fable used: judgement only.
- The ledger explains under half of the 3 Nov week (about 47 of 86 points have no row). Without attribution, cost per result cannot be managed. Cheapest fix: one meter reading at session start and end, written by a hook or by habit, even when no task row is written.
- What paid: scripts that can contradict us on our own data. The first real search cost about 0.4 points; G3 itself about 1; this audit's main finding (F-01) cost about 1 bar point of Fable, most of it three small scripts.
- What did not pay: reading (one pasted review, 1 point; four Fable helpers reading history, about 10 bar points for two summaries), long contexts (0.05 or more per tool call beyond 600K), publish cycles.
- Rule of thumb for this project: before any reading over about 20 KB, ask "which script would this reading let me write?" If none, do not read it.

## Pending 8 Nov decisions: one recommendation each
- **S2:** option A (accept and restate as 8.6 per 1,000, interval 7.1 to 10.3, no pass/fail), which Q6 already argued and my re-derivation supports. Add: do not raise the bar (B) and do not spend on a cause hunt in 0.8.1; the arms are not exchangeable (F-01), so S2 in its present form is not a clean false-alarm measure. Define a new S2 for Petrova 1.0 after the mask fix.
- **Second key name:** no view from the audit; pick one name and use it everywhere (T147). Fable not needed.
- **RESUME shortening:** yes (F-18 item 3).
- **Push of local commits (16f3f0a onward):** yes for main after one check that no file under `research/` names a star (Sonnet, grep for 6 to 10 digit ids next to "TIC"). The history rewrite of `watch-data` is a separate yes (F-17).
- **Outside check on every decision number:** yes, as a standing rule, but done by a script that re-derives by another method (as `n01_census_odds_and_s2.py`), not by a reading review. Cost about 0.2 to 0.5 points each.

## Not audited (budget, Amendment 1)
The book, the learning track, Eyes correctness and the flaky test FIX 80.
