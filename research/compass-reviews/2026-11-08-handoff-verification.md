# Verification of the outside handoff pack of 7 Nov 2026 (Claude Code, 8 Nov 2026)

Pack: `research/handoff-2026-11-07/` (filed unchanged, commit ee286c1). Author: an outside Claude session (claude.ai, Opus 5.5) that read the public repo at 1debc5c. This note is the Compass-style review Ahmed asked for. Labels: VERIFIED (I ran it or read the file myself), LIKELY, UNCERTAIN, NOT TESTED. Nothing here changes a frozen version, a search setting or the book. No build-side work was started.

## Plain verdict
The pack is good. Its two decision-changing findings are right: WO-1 is a real error in my own Census arithmetic (fixed today), and WO-2 is a real, free public list that changes how Census stage 2 should be sized, with one correction from our data: Gaia gives periods for only 15% of that list, so it is a cheap first slice, not a replacement for the Census list. Nothing was rejected outright. Four statements are narrowed or corrected below.

## The two checks Ahmed asked for first

### WO-1 Census odds: VERIFIED, FIXED
- `census_step1/census_worth2.py` line 15 prints `1 - exp(-tot)` with `tot = E0 + Census E`, and E0 is G2 development + G2 sealed + G3, which are finished and found nothing. `CENSUS-WORTH-2026-11-04.md` said "very likely finds one" (86% to 100%). VERIFIED by reading both.
- I re-derived the method independently (new script `census_step1/census_worth3.py`, output `census-worth3.txt`) and got the reviewer's numbers: Census alone, rate updated by the three nulls, completeness trimmed 10% (FIX 28 confirms about 3 points, so c = 0.9 is right):

| Census size (3 sectors each) | Kepler-like prior (median 10%) | Broad prior (1% to 20%) | Old table |
|---|---|---|---|
| 1,400 G2-type stars | 36% to 52% | 21% to 31% | 86% to 99% |
| 3,000 G2-type stars | 59% to 76% | 37% to 52% | 94% to 100% |

- The believed rate itself drops to about 5% to 7% (Kepler-like prior) or 2% to 3% (broad prior). Adding G1 (about E 0.3) lowers each number by 1 to 2 points. The 95% ceilings are unchanged and correct.
- Small corrections to the pack: its text says E0 is "G1, G2 and G3"; our E0 is G2 development, G2 sealed and G3 (G1 left out as before). The numbers still match because it used our E values. The two priors are a choice, not data (UNCERTAIN), and all of this is the main scenario only (F = 5.6, no dilution); the floor-3 scenario would update the rate much harder (NOT TESTED).
- Done today: correction banner on `CENSUS-WORTH-2026-11-04.md`, correction 2 on Lesson 2, a note under item 6 of the 4 Nov morning report, a row in `research/mistakes.md`. No book page quotes the old chance (grep). FIX-QUEUE item 81.

### WO-2 CALNet list: VERIFIED, with a new measured limit
- Downloaded (logged in `research/downloads.csv`, stored in `data\calnet_2026-11-07\`, git-ignored): `newecl.dat`, 1,263,960 bytes, 10,531 unique TICs, median G 11.68, 5,973 brighter than G 12, 8,277 brighter than 13.5, 46 rows with no Gaia ID or magnitude. Overlap with our lists: G1 51, G2 0, G3 20; 10,460 never searched. All VERIFIED, identical to the pack.
- New (not in the pack): the `Disp` column holds 1, 2 or 3 for most rows and about 120 rows carry SPLIT, DUPLICATE or ARTIFACT flags; the CALNet README does not explain them (UNCERTAIN what the numbers mean).
- Periods: 27 read-only queries to the Gaia DR3 `vari_eclipsing_binary` table by Gaia ID returned a period for only **1,596 of 10,475 stars (15%)**. By period: 860 under 1 d, 493 at 1 to 3 d, 120 at 3 to 5 d, 43 at 5 to 7 d, **80 at 7 d or more (69 brighter than G 13.5)**, of which 47 at 7 to 15 d, 26 at 15 to 40 d, 7 above 40 d. The other 85% have no period from this route.
- What it means for Census stage 2 (LIKELY, not yet planned): CALNet is a cheap first slice. Its 8,277 bright stars would cost roughly 10 to 21 GB of light curves (the 460 to 910 GB estimate for 364,656 stars scales to about 1.3 to 2.5 MB per star; UNCERTAIN) against 460 to 910 GB for a full scan. But it is not the whole Census. Only 80 stars are certain long-period (7 d or more); if the 85% with no Gaia period have the same mix as the 15% that do (7.7% at 5 d or more), the bright part could hold about 640 G2-type stars, but that assumption is UNCERTAIN (Gaia solutions may favour some stars). So CALNet may supply anywhere from about 5% to about 45% of the planned 1,400 G2-type stars. Periods for the rest must come from the TESS light curves, so the finder is still needed, and CALNet is weakest on slow binaries with one eclipse per sector (LIKELY from its own method, NOT TESTED). The zero overlap with G2 suggests CALNet lists only EBs new relative to its 4,225-star training set (LIKELY).
- I have NOT changed `CENSUS-PLAN-2026-11-04.md`. Proposed amendment filed as T139, waiting for Ahmed's word.

## All findings and work orders
Go = needs Ahmed's go. Cost in weekly points is the reviewer's guess unless I say otherwise (UNCERTAIN; my past tasks ran 1 to 2 times the guess).

| Item | Label | What I checked | Decision | Where | Go | Cost |
|---|---|---|---|---|---|---|
| F1 / WO-2 | VERIFIED + narrowed | above | accept, amended | BUILD T139 | yes | 1.5 |
| F2 / WO-1 | VERIFIED | above | accept, done | FIX 81 | no | 0.5 spent |
| F3 / WO-11 | VERIFIED in kind | RESUME is 15,947 words. Of 385 commits, 87 touch pipeline/, 67 touch only book/RESUME/ledger files, 260 touch at least one of them. The pack's 141 of 305 sits between my narrow and broad counts | accept as proposal; it changes his 4 Nov RESUME rule, so his call | BUILD T143 | yes | 0.5 |
| F4 / WO-8 | VERIFIED | 65 of 111 pipeline files contain a D: path (pack: 64); no `.github` folder | accept; touches frozen code, so only at the next freeze | FIX 82 | yes | 1.5 |
| F4 / WO-9 | VERIFIED by reading | `test_detect_v2_paths.py` prints "skip" and returns (lines 36 and 50), then its runner prints "pass" (line 65). Linux runs NOT TESTED by me | accept; step 1 (SKIP counted) no go, step 2 (CI) yes | FIX 83 | step 2 | 0.3 + 0.5 |
| F5 / WO-13 | VERIFIED | T108 and T125 exist, unbuilt | accept; tag both | BUILD T108, T125 | yes | 1 |
| F6 / WO-3 | LIKELY / NOT TESTED | Davies 2026 (mono-cbp, arXiv:2604.09435) is in our notes: 512 detached Prsa EBs, P over 7 d, to sector 79, 1 weak candidate. It is the same population as our G2, so the back-test needs Davies's own completeness, which I have not read. "Only a couple of TESS CBPs published" UNCERTAIN | accept as a study, park | BUILD T140 | before any quoted number changes | 1 |
| F7 / WO-16 | VERIFIED | "second key" appears on 4 book pages (field note 3 Nov, lab 9, learn index, for-astronomers) | accept; needs his one-line answer on the name | BUILD T147 | yes | 0.2 |
| WO-4 | VERIFIED | FIX 11 and FIX 14 hold the 57% / 68% (2 d) and 72% / 79% (3 d) figures | accept; already queued, tag them | FIX 11, 14 | yes (search change) | 2.5 |
| WO-5 | VERIFIED | FIX 70 and T137 exist | accept; tag | FIX 70, T137 | yes | 1.2 |
| WO-6 | VERIFIED arithmetic | 115 in 13,412 = 8.57 per 1,000, exact Poisson 95% 7.08 to 10.29, so the mark of 8 is inside. The decision is his; my lean stays A | remind in plan | decision | yes | 0.2 |
| WO-7 | LIKELY | STANLEY and Windemuth 2019 are in our literature note; novelty stays "possibly" until T127 | accept after WO-4, extends T106 | BUILD T141 | yes | 4 |
| WO-10 | LIKELY | T128 partly done for G3 | accept, small | BUILD T142 | no | 0.5 |
| WO-12 | VERIFIED | BUILD-QUEUE has 82 task lines (pack: about 100) | accept; triage list for him | BUILD T144 | yes | 0.5 |
| WO-14 | VERIFIED numbers, narrowed | FIX 30 holds 54 events, 8 stars, median 822 ppm, 5.5 to 20.6 d. The pack leaves out our own first hypothesis, shallow secondary eclipses of eccentric binaries (LIKELY, NOT tested directly) | accept as a study, with that hypothesis first | FIX 30, BUILD T145 | yes | 1 |
| WO-15 | VERIFIED sizes | the 11 core files are 1,958 lines, all of pipeline/ is 9,043 (pack: about 2,000 and 9,000) | accept for after the boards; map page and ER1 can come earlier | BUILD T146 | yes | 8+ in total |
| WO-17 | LIKELY | Keystone T134 spec has a case panel and a cold run, the Checker blind test is the same idea | accept; a spec edit | tag T134 | no (his instruction) | 0.3 |
| WO-18 | UNCERTAIN | LOPS2 paper exists (arXiv:2409.13039, over 1,000 bright EBs in LOPS2). It says launch in late 2026 (2024 paper); the pack says ESA gives April 2027. I did not open ESA | accept as a count only, low priority | BUILD T148 | yes | 0.3 |
| WO-19 | UNCERTAIN | `asymmetry*.txt` files exist; I did not re-derive the 1.3 to 2.5 times figure | accept as a T127-style check, low priority | BUILD T149 | yes | 0.5 |
| WO-20 | VERIFIED papers | Thornton et al. is arXiv:2512.07934 (27 candidates, 1,590 Gaia EBs, posted Dec 2025); arXiv:2608.13269 re-evaluates CH Ind and SW CMa from that sample | accept as a design question only | FIX 27 | no build | 0 |
| WO-21 Annex | VERIFIED code | `stage2_search.py` lines 190 and 191 use `flip_action="flag"`; `tier_of` puts flagged events in tier 2. Group JSONs are small and kept: `data\stage2\groups` (474 files) and one run folder per run under `data\stage3\<run>\groups` (5,082 files, 14 to 22 MB each). The pack's paths for G2 and G3 were loose. One disk only (data is git-ignored), LIKELY no backup | accept, after Census stage 2 is planned | BUILD T150 | yes | 1.3 |
| WO-22 Petrova dataset | LIKELY | depends on T150 | accept, after T150 | BUILD T151 | yes | 1 |
| 04 Mastery plan | LIKELY | 7 arXiv links opened, all match their stated titles; non-arXiv links NOT TESTED; hours are estimates | use for Engine Room and the Keystone merge; nothing goes to the book without his word | n/a | n/a | n/a |
| 06 CLAUDE.md note | VERIFIED gap | the `my-take` skill had the format but not how to read the phrase or what to say after a block | added a short version to CLAUDE.md | CLAUDE.md | no | 0 |

## Corrected or narrowed statements in the pack
1. "Saves days of downloads": true only for the CALNet slice (about 10 to 21 GB), not for the full Census list. LIKELY.
2. "Existing hunts E0 belongs to G1, G2 and G3": it is G2 development, G2 sealed and G3.
3. WO-14's cause list omits the eccentric-binary secondary eclipse, already our leading hypothesis.
4. The odds in `03` section 3 use the main scenario only and the commit and queue counts differ slightly from ours (385 commits, 82 task lines).

## Not done, on purpose
No change to `CENSUS-PLAN`, no stage 2 download of any EB list beyond the two small files above, no search, no frozen file touched, no book publish, nothing from `04-MASTERY-PLAN.md` published.
