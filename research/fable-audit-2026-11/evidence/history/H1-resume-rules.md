# H1: RESUME.md, CLAUDE.md and memory, read-only summary (10 Nov 2026)

Read in full: `D:\second-sun\CLAUDE.md`, `D:\second-sun\RESUME.md` (316 lines, 126,819 chars), all 62 `.md` files in `C:\Users\hanzl\.claude\projects\D--second-sun\memory\`. Nothing was run or re-computed except simple arithmetic on quoted numbers. "L" = RESUME.md line number.

## 1. Timeline of key decisions and reversals

| Date | Event |
|---|---|
| 19 Oct | Project locked in 13+ rounds. G1 (Kepler-field EBs seen again by TESS) approved as first campaign. "Everything goes in the book". |
| 20 Oct | Weekly cap 35%. Quality-mask experiment (one star): baseline reproduced; SAP finds 7 of 8 TOI-1338 b transits vs PDCSAP 4. Labels fixed as VERIFIED / LIKELY / UNVERIFIED. |
| 21 Oct | REVERSAL: hunt and all science follow-ups put on hold by Ahmed. |
| 23 Oct | Outside review finds bugs B1 to B5 in `detect_v2.py` (30-min data found nothing; QLP used spline column). Fixed. Odds 15% to 20% (5 to 45%). Hunt re-approved in stages. Stage 1 audit of 549 stars (8,100 files). Odds 18% (5 to 40%). Stage 2 trial on 50 stars: no excess, 3 leads kept local. |
| 24 Oct | Eyes saving plus Firebase; readiness ladder fixed (Step 1 still open). |
| 27 Oct | "Run the star search": G1 full search v1, v2. Daily cap 10 points, later 25% / 23%. |
| 28 Oct | G1 v5 (hash 5392f864e810): tier 1 real 14, upside-down 35, no excess. v6 SAP twin 33 vs 36, v7 fair check 21 vs 32. Name "Vesper" chosen. |
| 29 Oct | "Win = a clean measured null". Chain recovery: tier-1 ceiling 44 to 64%; "G1 null excludes giants only". G2 = 895 stars, split 301 dev / 594 sealed. Daily Eyes pull removed. |
| 30 Oct | Vesper 0.8.0 frozen (hash 5f73692944aa; only the orbit-locked flag c6 accepted). G2 sealed scored: S1 NO EXCESS, S2 FAIL 8.91 vs mark 8, TOI-1338 b 1 of 7. |
| 31 Oct | Post-sealed research; two queues (FIX, BUILD); book publish becomes autonomous. |
| 2 Nov | Horizon (T119), Vigil, Witness approved as concepts, research first (T122, 89 questions). |
| 3 Nov | "Three weeks finish and measure, no new system designs" (to 23 Nov). OMS deferred. Vesper 0.8.1 frozen (hash e7886a71a61f). Horizon R0 rule locked. Ahmed starts calling the filter Petrova (rename not done). |
| 4 Nov | G3 run 01:15 to 01:24 (612 TTC stars, one shot spent): S1 NO EXCESS, S2 FAIL 9.34, 0 leads. Ahmed: "change or quit". REVERSAL: G4 replaced by CENSUS (own EB list from post-sector-26 data); three-week rule lifted "for the Census list only". Night: Q1 finds Horizon lacks transit geometry (expected 13 to 22 planets, found 0). |
| 6 Nov | T138 YES: geometry factor g put into Horizon as R0 Amendment 4 (commit de2e951). Opus trial audit finds 9 issues, 2 change a conclusion. Census worth corrected. |
| 8 Nov | Outside handoff pack verified. WO-1: Census "87% to 100%" chance was wrong, now 21% to 52% at 1,400 stars (FIX 81). CALNet list checked. Private event backup. G5 sizing note. Ahmed rejects preregistering Census in January. FFI door: preregistered (28f8fc0), stages A, B, C done, stopped at 86% weekly; U6 reads CLOSED under the literal rule. |
| 10 Nov | Weekly reset, cap 14%. Fable audit planned (brief `research/fable-audit-2026-11/01-FABLE-BRIEF.md`), not started in RESUME. |

Gap: RESUME has no dated block for 1 to 3 Nov (Horizon build, T122 research, 0.8.1 freeze, G3 download stall). Those live only in memory files and the 4 Nov summary paragraph.

## 2. Decision-steering numbers

| Number | Value | Decision it steered | Source named |
|---|---|---|---|
| G1 / G2 / G3 stars | 549 / 895 (301 dev + 594 sealed) / 612 | Size of each null; total 2,056 stars, 19,464 star-sectors (L92) | `targets/g1_targets.csv`, `targets/g2_targets.csv`, `G3-RESULT-2026-11-04.md` |
| G1 v5 tier 1 | 14 real vs 35 upside-down | "No excess", G1 null | `aggregate_v5.txt` |
| Chain recovery v7 | tier-1 ceiling 44 to 64%; 50% at 11 x 8 h noise (about 8,000 ppm) | "G1 null excludes giants only"; led to G2 | `chain_recovery_v7.txt` |
| G2 dev tier 1 | 90 vs 25; 54 of 90 orbit-locked on 8 stars | Orbit-locked flag c6 (90 to 43, 25 to 23, cost 0.81% of fakes), freeze 0.8.0 | `g2-dev-results-2026-10-29.md`, `VESPER-VERSIONS.md` |
| S2 false-alarm mark | 8 per 1,000 | Pass or fail of every sealed run | `G2-SEALED-PLAN.md` |
| S2 G2 sealed / G3 / pooled | 8.91 / 9.34 (32 in 3,425; 6.39 to 13.19) / 8.57 (115 in 13,412; 7.08 to 10.29; p 0.24) | Open S2 decision A, B, C; "bar 8 gives about 6.8 at 19% to 30% completeness cost" | `benchmark-g2-sealed.txt`, `Q6-S2-EVIDENCE-2026-11-04.md` |
| G3 S1 | bar 7: 18 real, 31 upside-down, 23.5 expected, chance 0.896 | G3 null, "change or quit" | `G3-RESULT-2026-11-04.md` |
| G3 completeness | 33.8 / 43.7 / 40.0 / 24.6%; TOI-1338 b-size 6% | "Faint stars buy little"; Census by value | same |
| No safe windows | 784 of 5,634 reads (13.9%) = 655 of 4,080 star-sectors (16.1%) | T137 window table | `Q5-LOST-READS-2026-11-04.md`, `crosscheck_counts.py` |
| Horizon star-equivalents | G2 sealed 87 (ceiling 3.4%); G3 18 to 20 (15 to 17%) | Pool ranking; superseded by T138 | `G3-RESULT`, `horizon_reach.py` |
| Expected planets, no geometry | 13 to 22 (13.5 / 22.3) | Triggered T138 | `Q1-EXPECTED-PLANETS-2026-11-04.md` |
| Geometry g | min(1, (P_b/P_p)^(2/3)/f), f = 1.5, 1.8, 2.2; mean g 0.10 to 0.16 (G2, G3), 0.25 to 0.33 (G1) | R0 Amendment 4 | `HORIZON-R0-RULE.md`, `census_step1/t138_g_reach.py` |
| E with geometry, three hunts | 1.28 to 2.89; none 6% to 28%; ceiling 10.4% to 23.4% | "Nulls consistent with Kepler's 10%"; Census justified | `t138-g-reach.txt` |
| Armstrong rate | 10% (R over 6 R_earth, P under 300 d) | Prior for every E | Armstrong 2014 abstract |
| Census chance (old) | 87% to 100% at 1,400 stars | "Very likely finds one"; WRONG | `CENSUS-WORTH-2026-11-04.md`, `census_worth2.py` line 15 |
| Census chance (fixed) | 36% to 52% or 21% to 31% at 1,400; 59% to 76% or 37% to 52% at 3,000 | Census sizing | `census_worth3.py`, `census-worth3.txt` |
| Census E at 1,400 | 0.70 / 0.86 / 1.03 (adds 55%; 3,000 adds 118%) | Census target size | `census-worth2.txt` |
| New bright 2-min stars | 364,656 (258,858 at Tmag 13.5 or brighter); G2-type yield 0.4% | Census exists; scan 463 GB, 23 h | `CENSUS-STEP1-COUNTS-2026-11-04.md` |
| Finder answer key | 4,161 Prsa EBs seen again in S27+ (1,036 G2-type) | Stage 2 option 2 | `CENSUS-STAGE2-OPTIONS-2026-11-04.md` |
| CALNet | 10,531 TICs; Gaia period for 1,596 of 10,475 (15%); 80 with P 7 d or more | T139 amendment; "5% to 45% of the 1,400" | `census_step1/calnet_check.py`, `calnet_gaia.py` |
| Gaia slow EBs | 188,407 (P over 5 d); 137,637 (over 7 d) | G5 pool | Gaia TAP, `gaia_pixels.py` |
| Gaia bright slow, sampled | 5,500 / 11,600 / 20,800 (G under 13 / 14 / 15) | G5 "10,000 stars" answer | `G5-SIZING-2026-11-08.md` |
| Gaia bright slow, exact | 4,016 / 8,059 / 14,870; 7,505 after exclusions at G 14 | Corrects the above by 27% to 40% | `ffi_pool.py`, `ffi_exclude.py` |
| Gaia vs TESS | 4.2% (90 of 2,160) of TESS slow EBs in Gaia list; period right in 59% | Trust in a Gaia-fed pool | `gaia_vs_tess_catalogs.py` |
| FFI door U1 / U6 | 93.0% (372 of 400) / 22.7% (threshold 50%, half = 25%) | Door OPEN or CLOSED; literal rule says CLOSED | `existence_census.py`, `FFI-DOOR-TEST-PLAN-2026-11-08.md` |
| QLP / SPOC FFI coverage | 89.8% / 20.4% of sectors | Why U6 fails | same |
| G5 at 10,000 stars | ceiling 4.3% if empty; chance of one 60% to 85%; about 340 tier-1 dips to sort | G5 go or no | `G5-SIZING-2026-11-08.md` |
| Dip shape correction | minus 3 points on 30.5% kept (physical shapes 27.8%, 27.1%) | Quoted completeness | `FIX28-SHAPE-TEST-2026-11-04.md` |
| Kept share ceiling | about 53% of seen dips | Limits of the checks | `Q3-Q7-GAIA-AND-COMPLETENESS-2026-11-04.md` |
| 7-day period cut | no Kepler transiting CBP below 7 d | Target rule for all hunts | Hamers 2016 |
| Odds of a candidate | 15%, 20% (5 to 45%), 18% (5 to 40%) | Whether to hunt G1 | `yield_measured.py`, `research/predictions.md` |
| Eyes pass lines | 85% clear, at most 10% false; hard 80% / 20% | His readiness for real events | `eyes-core.js`, RESUME L188 to L193 |
| FIX 80 flake | about 2 failures in 80 runs | Left OPEN | `fix80-repro-2026-11-06.txt` |
| Weekly caps | 35, 50, 65, 70, 80, 85, 90, 97, 10 per day, 25/23, 30, 55, 70, 83, 14, 30, 60, 85, 87, 14 | Every stop | chat; `research/usage-ledger.md` |

## 3. Open, waiting or pending

Waiting for Ahmed:
- 10 Nov: go to launch the Fable audit; the reset plan.
- 8 Nov: view on the U6 = CLOSED reading and on the TOI-1338 control (same-sector FFI vs 2-minute); cap for RS-013 (K2, 0.3 points) and stage D (about 1 point); "continue" for stages D, E and the G5 note.
- 8 Nov list: answer on the three no-go items (blank); T139 go; WO-14; S2 decision A, B or C (open since 30 Oct); key name (WO-16); T143 RESUME slimming; Group B upgrades (WO-4, WO-5, WO-8); whether "outside check on decision numbers" is a standing rule; push of local commits (16f3f0a, edb7a21, 849139c, 0f8d46b and everything since, all "no push").
- 6 Nov: Petrova rename go (open since 3 Nov); book headline wording; Opus audit slices (probably overtaken by Fable, not stated).
- 4 Nov: Census stage 2 step; T137; fetcher tool; keep or strip G2 star details on the feed; Learning Space proposal; T135; T134 Keystone; he had not read Lessons 1 to 3 and the 7 files.
- 10 Nov: go for T133 stage 1; two more annoyances he will name.
- Old: Eyes ladder Step 1 (since 24 Oct), Step 3 not built; F4 redesign; visual identity Artifact paused 24 Oct; key-1 follow-up on the 3 Stage 2 leads (L216, 23 Oct, never closed); status-table tasks 7, 8, 9, 10 (20 to 21 Oct).

Pending on Claude's side:
- FIX 84 (QLP flag bit 31, effect NOT TESTED), T152, T153; ASAS-SN and Hipparcos counts NOT TESTED; Gaia DR4 date UNCERTAIN.
- FIX 80 OPEN; FIX 82, FIX 83; mission.yml reminder "not done" (L86).
- Thornton 2026, Li 2016 occurrence paper, Davies 2026 full read (dropped 6 Nov); Kepler-16 radii UNCERTAIN; claims B17 LIKELY, B4 UNVERIFIED.
- T60: Rabtsevich outcome after 26 Nov. U02 (TTC period fold check) and G3 scorecard_plus lines A to E (memory `project_g3_frozen_081_waits_for_go.md`). Horizon R1b fix.
- Private backup is on the same disk as the source.

## 4. Rules that conflict, duplicate, are stale or waste effort

Conflicts:
- Helpers. Memory index "Ask before helpers" (ask every time) vs `feedback_book_learn_first.md` rounds 9 to 11 ("standing permission for reading and checking only, replaces ask each time") vs RESUME L168 ("read-only helpers allowed") vs `feedback_research_freely.md` ("does NOT cover helpers").
- Labels. CLAUDE.md "CONFIRMED, LIKELY, UNCERTAIN or NOT TESTED" vs book register VERIFIED / LIKELY / UNVERIFIED (RESUME L273) vs Compass and the 8 Nov handoff order (VERIFIED / LIKELY / UNCERTAIN / NOT TESTED). Three vocabularies in live use.
- Teaching in chat. `feedback_book_learn_first.md` ("does NOT want concepts explained in chat") vs `project_census.md` ("teach each step before doing it") and Lessons 1 to 4 sent in chat. Also CLAUDE.md "phone-first, short replies" vs the same file's "chat reports detailed with numbers" and "as long as the topic needs".
- Privacy. `project_second_sun.md` "Everything goes in the book (candidates, batches); he rejected any private split" vs CLAUDE.md "real events stay in data\; named leads stay private".
- Downloads. `feedback_no_direct_file_links_in_browser.md` (ask first for any file) and `feedback_research_freely.md` (no big downloads) vs "Second Sun downloads need no yes". `project_second_sun.md` still says over 20 GB needs his OK.
- Publish and push. CLAUDE.md "I publish the book myself" and `project_second_sun.md` "auto-push book updates" vs RESUME since 8 Nov where every commit is "(no push)" and the push waits for him. `feedback_downloads_shown_automatically.md` and `feedback_work_fix_list_slowly.md` still say "tell him to publish".
- Stop or continue. `feedback_cpu_70_percent_when_away.md` second rule (stop after asking, wait for go) vs `feedback_dont_end_overnight_on_a_question.md` and `feedback_autocompact_600k_continue_alone.md` (keep working).
- Popups. "Ask in text chat, never popups" vs the 10 Nov ask-tool rounds (one-task override, RESUME L5). The memory was not annotated.
- "Three weeks: finish and measure" (no new designs to 23 Nov) vs Census, FFI door, G5 sizing, T150 Annex, T151 dataset, Engine Room and the Fable audit, all designed inside the window. Only the Census list was formally exempted.

Stale:
- CLAUDE.md "Weekly cap ... (25% and 23% on 27 Oct 2026)". Current cap 14% (10 Nov).
- CLAUDE.md "Until the page exists: a line in research/jobs.md": the Downloads page still does not exist, 11 days on.
- "Daily usage cap" (10 points per day): overridden about ten times.
- `project_horizon_reach_map.md` and its index line ("NOT started"): R0 is locked with four amendments.
- `project_g3_frozen_081_waits_for_go.md`: file name says waits; content says ran.
- `project_vesper_name.md`: "rename pending, batch with next publish"; no word of Petrova in the body.
- `project_three_weeks_finish_and_measure.md`: "14% is TODAY's cap (3 Nov)". Dangerous now that 14% is again the cap for a different reason.
- `feedback_autocompact_600k_continue_alone.md`: resume anchor `OVERNIGHT-2026-11-02.md`; the anchor is now RESUME.md.
- `project_second_sun.md`: caps 35 / 50 / 70%, "hunt paused", daily task `eyes-scores-daily` (removed 29 Oct).
- `project_todo_after_reset_2026_10_26.md`, `project_visual_identity_artifact_paused.md`, `reference_second_sun_memory_copy.md`: not in MEMORY.md (only in INDEX-ARCHIVE.md).
- "Default model = Sonnet 5.5 Extra": recent sessions ran Opus 5.5 and Fable 5.2.
- Dangling links to memories absent from this folder: `feedback_structured_choice_questions`, `feedback_dont_overpause_on_small_calls`, `feedback_autocompact_500k`, `feedback_bulk_push_and_cleanup`, `feedback_verify_pdf_output_dont_eyeball`.

Duplicated:
- Verify-with-sources: CLAUDE.md, `feedback_verify_science_with_sources.md`, `feedback_research_blueprint.md`, `feedback_research_freely.md`.
- No popups: `feedback_phone_first.md` and `feedback_ask_in_text_chat_not_popups.md`.
- "Never click the live Eyes page": twice in CLAUDE.md plus a memory.
- CPU: 68% (RESUME L164), 70% (`feedback_cpu_70_percent_when_away.md`), 75% (`feedback_cpu_target_numba_threads.md`), "at most 6 threads" (`feedback_no_direct_file_links_in_browser.md`).
- Queues: CLAUDE.md plus `feedback_file_obvious_followups.md`, `feedback_fix_list_bugs_only.md`, `feedback_work_fix_list_slowly.md`.

Looks wasteful:
- Per-task bookkeeping stack: "Update RESUME.md after every task" (detailed, never delete) + "Same-day lessons" (field note + publish) + "Learning track in sync" (chapter + quiz) + "Daily recap" (version bump + publish + confirm) + usage ledger before and after + mission.yml in the same commit + versions.md row. Evidence in RESUME: 8 book publishes in one night (2.9.6 to 2.9.13, 4 Nov); 67 of 385 commits touch only book/RESUME/ledger (L49); RESUME is 15,947 words, which defeats its cold-start purpose; T143 (slim it) is blocked because it "changes his 4 Nov rule".
- "At least about 10 minutes on a serious question" plus per-stint caps: RS-012 cost about 2 points against its 0.6 cap (L19).
- `feedback_hidden_pane_throttles_timers.md`, `feedback_narrate_friction_live.md`, `feedback_unverified_is_not_fixed.md` come from other projects; fine as habits, but they load in every session.

## 5. Internal inconsistencies in RESUME.md

1. G3 star count: 612 (L92, L144) vs 611 (L30 "611 TTC stars", L101 "16 of 611 stars").
2. Total "19,464 star-sectors" (L92) cannot be rebuilt from the file: G1 is 5,082 (L164) or 5,064 (L172); G3 is 4,080 (L101) or 3,425 (L142); pooled G2 + G3 is 13,412 (L109).
3. "3,425" appears as G2 dev groups (L164) and as G3 searched star-sectors (L142). G3 fits 4,080 minus 655. The match may be coincidence; worth one check, since the pooled S2 denominator depends on it.
4. Expected planets for the same hunts: 13 to 22 (L102), 1 to 4 (L106), 1.3 to 2.1 (L114), 1.5 to 4.1 for four hunts (L120), 1.28 to 2.89 and 1.46 to 3.26 (L75). Only L75 is current; older lines carry no "superseded" mark.
5. Horizon ceilings "3.4%" and "15 to 17%" (L142) stand in the same block that says "Do not quote Horizon ceilings as limits on planets until T138" (L102). With g of 0.10 to 0.16 they are several times too tight.
6. Census chance: "87% to 100%" (L114, L58) vs "86% to 100%" (L49); corrected 3,000-star low end "37%" (L49) vs "38%" (L58). L114 has no correction banner inside RESUME.
7. G5 pool: Ahmed's idea 1 is "5,000 or 10,000 stars down to about G 14" (L29) and L43 answers "10,000 yes if down to G 14 to 15", but the exact count at G under 14 is 8,059, 7,505 after exclusions (L14). 10,000 does not exist at G 14. L43 is not marked superseded.
8. Same frame, two counts: "under 14: 8,059" vs "Frame 8 at most G under 14 and period over 5 d: 7,999" (both L14).
9. "G4" was replaced by Census (L92), yet L43 says "12.3% after G4 alone".
10. Census target 1,400 G2-type stars vs supply "about 1,000 of the G2 type" among the bright new stars (L100); 0.4% of 258,858 is about 1,035. The 1,400 only works with all 364,656 stars.
11. CALNet: "10,531 TICs" vs "1,596 of 10,475 stars" (L49).
12. Label misuse: L8 "CONFIRMED from search summaries, pages not opened", against CLAUDE.md "a search-engine summary is a lead, not a source". L5 later says "Help pages read"; Fable counting toward weekly is still only LIKELY.
13. Book version: "Version 2.9.6 live" (L146) inside the block whose log reaches 2.9.13 (L135); 2.9.15 on 6 Nov (L86). "Book 2.6.0 is ready to publish" (L160) and "Book 2.5.0 once published (Ahmed says publish)" (L312) are stale.
14. Stale unchecked box: L229 "[ ] Stage 0 d + Stage 1 audit" under L227 "Full audit DONE".
15. Status table (L277 to L290): task 8 "QLP recipe automation: not started" vs L232 "QLP recipe automated" credited; task 9 "136 morph rows pending Ahmed" vs decided and measured (L178: 80 clear, 56 last). L64 calls this table "the single source of truth".
16. Stale instructions still imperative: "Weekly cap: 35%" (L266), "confirm under 35%" (L308), daily task `eyes-scores-daily` "about 07:42" (L202; removed 29 Oct, memory says 21:30).
17. Firebase key file: `firebase-second-sun.json` (L201, L203) vs "the one `*firebase-adminsdk*.json` file" (L202).
18. Unexplained meter jumps: 30% at stop on 4 Nov to 45% on 6 Nov ("cause unknown", L67); 53% at stop on 6 Nov (L87) to 80% on 8 Nov (L57) with no project work logged between.
19. 10 Nov week plan (L2): physics 15 + math 20 + website 10 + Cowork 20 to 30 = 65 to 75 points, plus Fable about 30, plus Claude's 14%: at or over 100.
20. Corrupted paths: "esearch/stage3/..." (L30, L36, L43, L49) and the broken `data\chain_recovery_g3` + newline + `ows_shape_<name>.pkl` (L123 to L124). A backslash-r was eaten.
21. Clock times in the 4 Nov log contradict each other: item 12 "started about 06:55", item 13 "launched 06:38, finished 06:44", item 15 "about 06:50", 30% at 07:03 (L123 to L136).
22. Structure: three LATEST blocks sit above the "# RESUME" title (L1 to L10); 13 blocks are tagged LATEST, NEWEST or "READ THIS FIRST"; L66 says "the 4 Nov block below is still the full state"; the "30 Oct night: sealed search done" block is at the very bottom (L311), below 20 Oct material.
23. "Done" vs tested: "FIX 79 DONE (... full script untested until next publish)" (L110) and "WO-1 FIXED" (L49), against the memory rule "Unverified is not fixed". FIX 79 was later exercised with no retry needed (L113), so the retry path itself is still unproven.
