# Work orders WO-F09, F10, F13, F15, F16, F17p, F18, F22 and WO-BUGTEST. Commit read: c9b9aca.

Common rules as in `WO-F02-F04-F05-F06.md`. Stop sign for all: a change to `pipeline/`, a decision number moving by more than 10%, or anything outward goes to Ahmed first.

---
## WO-F09: where do the host radii come from, and does dilution cancel? (Opus needed, about 0.6, no yes)
**Goal.** Decide whether Horizon's main scenario (dilution 1.0) is right, optimistic or pessimistic.
**Location.** `pipeline/horizon_reach.py` lines 41 to 48 (radius source), 75 (depth), 112 (scenarios); `targets/host_radii_g2_g3.csv`.
**Steps.** 1. Tabulate the radius source per star (column in the csv or the script that made it; `git log --oneline -- targets/host_radii_g2_g3.csv`). 2. For 50 G2 stars with a published component radius (Prsa 2022 does not give radii; use stars in common with any SB2 catalogue on disk, else report NOT TESTED) compare. 3. Arithmetic: for a twin binary, a radius from total luminosity is 1.41 times one star's, depth falls by 2: equal to dilution 0.5. Write which stars get the cancellation and which do not. 4. Re-run `horizon_reach.py` into a scratch copy with the corrected per-star depth factor.
**Proof.** One paragraph for `HORIZON-R0-RULE.md` (proposed text only) stating the assumption, plus the change in E. **Trap.** Do not apply dilution 0.5 on top of blend-inflated radii (double count).

## WO-F10: re-derive the star values after the mask fix (Opus needed, about 1, no yes; after WO-F01 part A)
Re-derive by a new script, not `q2-pool-value`: faint value 0.21, bright Census value 0.45, per-1,000 E, the noise fit log10(noise8) = 0.26 + 0.211 Tmag (fit bright and faint halves separately; report the bright-end residual), each with m(period, K) from WO-F01 applied. Also reconcile, from files not from RESUME: G3 stars 612 or 611; G3 star-sectors 4,080 (groups) and 3,425 (scored); the 19,464 total; G1 5,082 or 5,064. Output: one table "number, ours, re-derived, source file, changes a decision?".

## WO-F13: Gaia DR4 pool (Sonnet, about 1, no yes; not before 2 Dec 2026)
1. Read the DR4 documentation pages for the eclipsing-binary and epoch-photometry products; pull exact sentences (the ESA release page on 10 Nov 2026 gave only the date, 2 December 2026, and "based on 66 months of data"). 2. Re-run `research/stage3/ffi_door/gaia_pixels.py` logic against DR4 tables (catalogue rows only, logged in `research/downloads.csv`). 3. Repeat the period check against Prsa (`gaia_vs_tess_catalogs.py`): share of periods right, overall and for slow binaries. 4. Report pool sizes at G under 12, 13, 13.5, 14 for period over 5 d and over 7 d. **Stop sign:** the G5 star-list rule is Ahmed's; deliver counts and options only.

## WO-F15 (RS-014) and WO-F16 (RS-013): two short research stints (Sonnet, cap 25 tool calls each, about 0.5 each, no yes)
- RS-014: "Published detections or occurrence limits for circumbinary planets around M-dwarf eclipsing binaries; giant-planet occurrence around single M dwarfs for comparison." Deliver the exact sentences and a one-line recommendation against F-15.
- RS-013: "Has a systematic transit search for circumbinary planets been published on K2 eclipsing binaries? Which K2 EB catalogues exist and how many have period over 5 d? PLATO launch date and first public data date; does LOPS2 overlap the TESS southern continuous viewing zone?" Follow `research/RESEARCH-BLUEPRINT.md`. Primary sources, abstract and HTML pages.

## WO-F17p: remove star ids from the public `watch-data` history (Sonnet prepares, about 0.5; the push NEEDS AHMED'S YES)
**Evidence.** `git -C D:\ss-watch-data log --format=%h | Select -Last 60` then `git -C D:\ss-watch-data show <hash>:watch.json | Select-String '"tic"'` returns rows for old commits (label "SEALED RUN ... 594 sealed G2 stars"). `gh repo view M1Smacker/second-sun --json visibility` says PUBLIC.
**Steps.** 1. Count commits whose `watch.json` contains `"tic"` (expected: most of the 87). 2. Prepare, in a scratch clone, an orphan branch holding only the current counts-only `watch.json`. 3. STOP. Show Ahmed: what is exposed, that a force push of `watch-data` replaces the history, that GitHub may keep unreachable commits for a while and forks or caches may exist. 4. Only on his yes: force push the orphan branch to `watch-data`; confirm the Search window page still loads. 5. In a separate normal commit (needs a book or tool change, so file it in the queue): make `counts_only` the default in `pipeline/watch_export.py` `build` and never write `tic` in cards or ticker.
**Trap.** Never click the live Eyes page while checking. Do not rewrite `main`.

## WO-F18: tidy rules and queues (Sonnet, about 0.8; NEEDS AHMED'S YES, it edits his rules and queues)
Apply the lists in `findings-R.md` F-18 and F-19 exactly: mark stale memory entries "superseded" with the date (do not delete), close or restate the listed FIX items, tick the done T items, merge the duplicates, move FIX 27 to the build queue, put the Petrova 1.0 mask at the top. Verify each status in code or in a result file before changing it (H2 marked several only LIKELY). Then shorten RESUME to one current block of at most 400 words and move the rest, unchanged, to `RESUME-ARCHIVE.md`, marking superseded numbers listed in `evidence/history/H1-resume-rules.md` section 5.

## WO-F22: binary-phase duration key, prototype (Opus needed, about 1.5, no yes for the prototype; using it in Petrova is a yes)
**Idea.** For a dip at time t in a binary with known ephemeris, the crossed star's sky-plane velocity at that phase is known up to the mass ratio; the planet's velocity is bounded by stability (period at least about 5.6 binary periods). So the transit duration must lie in a computable range. Dips outside it are not circumbinary transits.
**Steps.** 1. Open the Kepler-16 discovery paper (Doyle et al. 2011) and one multi-transit analysis (Kostov et al. 2020, TOI-1338) and pull the sentences on duration against binary phase. 2. Write `duration_range(P_bin, phase, q in [0.3, 1], M_tot = 2, R_star, P_planet in [5.6 P_bin, 500 d])` on circular orbits. 3. Test: published transits of TOI-1338 b and TIC 172900988 b must fall inside; then the share of stored G2 and G3 upside-down events (counts only) that fall outside is the key's rejection power.
**Proof.** Known transits inside; upside-down rejection share reported with an interval. **Stop sign:** eccentric binaries widen the range; if the range is so wide that under 20% of upside-down events fail, report "weak key" and stop.

---
## WO-BUGTEST: does the auditor skill help? (Sonnet 5.5 Extra, two fresh sessions, about 0.5 each, no yes)
**Material.** `D:\second-sun\data\fable_audit_bugtest\` holds scratch copies of `detect_v2.py`, `stage2_search.py`, `stage3_core.py`, `audit_all.py` with 4 planted bugs. The key is `D:\second-sun\data\fable_audit_private\BUGTEST-KEY.md`: the tested sessions must NOT open that folder, `make_bugtest.py`, the real `pipeline/`, git history, or `research/fable-audit-2026-11/`.
**Run 1 (without the skill).** Temporarily move `C:\Users\hanzl\.claude\skills\second-sun-auditor` aside (Ahmed or the starting session does this, then restores it). Prompt: "Four files in D:\second-sun\data\fable_audit_bugtest are copies of a transit-search pipeline with an unknown number of planted bugs. Find them by reading and by small scripts on synthetic data only. Do not look anywhere else on D:. Cap 40 tool calls. Report each bug as file, line, what is wrong, what it does to the search."
**Run 2 (with the skill).** Same prompt in a new session with the skill installed, plus "Use the second-sun-auditor skill."
**Score** (a third session or Ahmed, with the key): 1 point per planted bug found with the right effect; minus 1 for each false report beyond 2. Record both scores and tool calls in `research/fable-audit-2026-11/evidence/bugtest-result.md`.
**Trap.** Note that example 4 in the skill's `examples.md` describes a bug of the same family as planted bug 1. That is deliberate (the skill should transfer), but say so next to the score.
