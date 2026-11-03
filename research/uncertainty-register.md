# Uncertainty register (RS-006, started 3 Nov 2026; Ahmed's go; cap 2 weekly points, written before the start)

Method: `research/RESEARCH-BLUEPRINT.md` with the evidence ladder in this order for each item: (1) own data, a script that can contradict me; (2) one primary source, the page opened and the sentence pulled out; (3) if neither can settle it now, label it **NOT TESTABLE UNTIL <condition>** with the check that would settle it. A fourth outcome is **WRONG**: every sentence that used it is fixed. Raw extraction: 306 lines with UNCERTAIN, NOT TESTED or Not tested in 84 files (research/ and book/docs). Of these, 27 are label definitions, about 195 sit in dated records from 23 to 31 Oct (reports, Compass reviews, old learnings; each was true on its day and is kept, not re-edited) and 29 are in the book. The rest, plus the facts page, are audited here.

Sample check of the 195 old lines (22 read): about 4 in 5 are dated records or label definitions; about 1 in 5 is a real open item that is already tracked in the BUILD-QUEUE or FIX-QUEUE (example: the reason for NASA's 7.1 sigma bar, which the book already says it dropped). NOT audited line by line: the other ~170 old lines (said plainly).

## Group G: feeds the G3 search inputs (still cheap to change until the search runs)
| ID | Item | Plan | Status |
|---|---|---|---|
| U01 | Is the TTC eclipse "duration" (Dur-pri, Dur-sec) the full width or a narrower one? Feeds the eclipse-overlap flag via `dur_pri_h` in `g3_chain_targets.csv`. | own data: ratio of TTC duration to the physics duration (P/pi x (R1+R2)/a, the frozen rule's constants) for G3 stars with a TIC radius, against the same ratio for Prsa full widths on G1; plus the paper's reference for the fit | open |
| U02 | TTC ephemeris and period accuracy (integer-ratio periods, shallow few-eclipse targets; the paper's own caveat). | NOT TESTABLE before the search by design (needs the light itself); checked after, by the fold check as for G2 (FIX-QUEUE 24) | label |
| U03 | TTC sector range stated two ways (1 to 82 and 1 through 26); FIX-QUEUE 25 weird sector numbers in TESS-SPOC headers. | own data: sector range of the 5,031 G3 files | open |
| U04 | g3-source guesses (table size 1 to 2 MB; 100 to 500 stars). | closed by the download: table 3 is 2.0 MB, the rule gave 612 stars. The guess of the count was WRONG (612, not 100 to 500) | to close |

## Group P: published on the facts page (`book/data/claims.csv`: 98 claims, 75 VERIFIED, 22 LIKELY, 1 UNVERIFIED)
Plan: own data where we hold the number, else the primary page. Result column filled as each is settled (VERIFIED / kept LIKELY with reason / WRONG and fixed). Claims: B4 (UNVERIFIED, iPhone home-screen cache: only Ahmed's iPhone can test it), B17, F-002, F-009, F-017, F-018, F-024, F-028, F-030, F-031, F-032, F-033, F-034, F-042, F-044, F-047, F-051, F-059, F-068, F-071, F-074, F-077, F-082.

## Group H: Horizon numbers (not yet published on any page)
| ID | Item | Plan | Status |
|---|---|---|---|
| H1 | Window function W = min(1, covered days / P) and independent epochs per star-sector. | own data: fold the real good-time windows of a sample of star-sectors at the cell periods, compare | open |
| H2 | What Armstrong 2014's 10% covers (per binary? which binaries? coplanar?) and Li 2016 transit probability. | primary source | open |
| H3 | S = 0 below K = 6 (understates reach). | NOT TESTED; a planting run at K 3 to 5 on the dev split would settle it (about 0.3) | label |
| H4 | Depth uses the TIC radius, no dilution (generous). | sensitivity scenario already printed (dilution 0.5); the true light share is unknown for these binaries | NOT TESTABLE until light ratios exist; keep the scenario |
| H5 | TOI-1338 b reality check rests on one planet. | NOT TESTABLE UNTIL T109 (larger known-planet test, needs a download) | label |

## Group D: deferred with a reason (nothing to settle now)
Vigil items V-C3, V-C7, V-C11, V-F9, V-A3 (mission funding), V-B7 yield bracket (partly answered by Horizon): UNTIL Vigil design starts (three-week rule). Loom: Sculley 2015 not opened, no external speed figures: UNTIL Loom phase 0 is picked up. Learning builds T113 to T118: the primary papers behind the LIKELY effects are opened when T113 or T114 starts. OMS thresholds: judgement, not a measurement (labelled so). FIX-QUEUE 69 preview loop: workaround exists. Browsers/devices never tested (Safari on a real iPhone, touch, print): only Ahmed's iPhone can test them.

## Results (3 Nov 2026; weekly usage 10% before, 11% after, inside the cap of 2 points)

### Group G (G3 inputs)
| ID | Result | Label |
|---|---|---|
| U01 | Own data (`research/uncertainty-checks/u01_ttc_duration_ratio.py`): TTC duration / physics duration (P/pi x (R1+R2)/a, the frozen rule's constants), 562 G3 stars with a TIC radius: median 0.50, IQR 0.37 to 0.64. Prsa full widths on G1 (P above 7 d, radius known, n = 26): median 0.38, IQR 0.30 to 0.49. By period bin the G3 medians (0.52, 0.48, 0.46) sit at or above the G1 ones (0.33, 0.50, 0.34). The TTC durations are not narrower than full widths; if anything they are wider. The TTC paper's own definition of its duration column was not opened. | **LIKELY** full-width-like. Effect if wrong: one flag (eclipse overlap), small. |
| U02 | TTC period and epoch accuracy cannot be tested without the light itself. Settled by design after the search, with the fold check (FIX-QUEUE 24). | **NOT TESTABLE UNTIL** the G3 run is done |
| U03 | The 5,031 G3 files cover sector numbers 1 to 1751 (105 distinct); 3 files of 3 stars carry 1751 in the file name and in the header (7.2 days, BTJD 4055.8 to 4063.0, 1,835 cadences). Filed as a dated note in FIX-QUEUE item 25. What 1751 stands for is not in the files. | number CONFIRMED in the header; meaning **UNCERTAIN**; effect LIKELY harmless (under 0.1% of files) |
| U04 | The earlier guesses were WRONG on the star count (100 to 500 guessed, 612 real) and close on the table size (1 to 2 MB guessed, 2.0 MB real). Nothing downstream used the guesses after the download. | closed |

### Group P (facts page, `book/data/claims.csv`: 98 claims)
Before: 75 VERIFIED, 22 LIKELY, 1 UNVERIFIED. After: **85 VERIFIED, 12 LIKELY, 1 UNVERIFIED.**
- **Moved to VERIFIED (10), each by opening the primary abstract or by an own-data script:** F-009 (Welsh 2015), F-018 (Martin 2017), F-031 (Ricker 2015), F-032 (Stassun 2019), F-033 (Guerrero 2021), F-034 (Gaia DR3, Vallenari 2023), F-047 (Kostov 2020), F-068 (Holman and Wiegert 1999 eq. 3 plus our table of 21 known planets: period ratios 5.57 to 98), F-074 (our own recorded script output, re-read), F-028 (own data, below).
- **WRONG and fixed (1): F-028.** The book said momentum dumps come "every 2 to 6 days". Our own count (`research/uncertainty-checks/f028_dump_intervals_cameras.py`) of quality-bit-32 events in one file of each of 108 sectors (396 intervals): 5th to 95th percentile 2.5 to 7.5 days, median 6.3, per-sector medians 2.5 to 13.9 days (some later sectors about once per orbit). Sector 82 (Kepler-16, Lab 3): 6.1 to 6.7 days, so "about every 6 days" in Lab 3 stays true. Fixed in `claims.csv` and in chapter 3 ("every 2 to 8 days in most sectors (6 days in Sector 82)"). Lab 2's bit table reads the same claim and needs no edit.
- **Kept LIKELY, source note extended (7):** F-002 (numbers match the abstract, "first" is not in it), F-024 (4 cameras and all 16 camera/CCD pairs confirmed in our files; field size, pixel size and 21 arcseconds not re-opened), F-042, F-059, F-071, F-077 (489 against 480 and 150 against 255 re-read in `asymmetry_v6sap.txt`), F-082 (67/41, 14/2, 14/0 re-read in `sap_fairness_fd788be04650.txt`). The conclusions of F-077 and F-082 are arguments from those numbers.
- **NOT settled this pass, stay as they were, said plainly (5):** F-017 (the 7.1 sigma bar, tracked in the queues), F-030 (Kepler field and star counts, abstracts checked on ADS on 20 Oct, not re-opened today), F-044 (STANLEY, abstract read on ADS on 20 Oct), F-051 (titles checked; content from the Compass reading), B17 (A&A policy from a search summary; the site blocks our tools; needs a copy a browser can read). B4 (iPhone offline cache) can only be tested on Ahmed's iPhone.

### Group H (Horizon)
| ID | Result | Label |
|---|---|---|
| H1 | Own-data fold test on 80 development stars, 1,179 star-sectors (`research/stage3/horizon_window_fold_test.py`, output `horizon-window-fold-test.txt`). Per star-sector W = min(1, covered/P) is within 2% of the folded value from 43 days up and 10% high at 13 days. The independent-epochs step is the weak one: a star's true joint coverage is 0.93 / 0.84 / 0.69 / 0.48 / 0.38 at 43 / 78 / 139 / 250 / 448 days against 0.985 / 0.91 / 0.77 / 0.60 / 0.44 for 1 - product(1 - W): too high by 6 / 8 / 12 / 24 / 15%. Published ceilings are therefore optimistic by roughly 5 to 25% at long periods; recorded as R0 Amendment 3; the exact fix is queued (BUILD-QUEUE, Horizon R1b). | per-sector W **CONFIRMED** (sample of 80); independence **WRONG by a measured margin**, not yet fixed in the calculator |
| H2 | Armstrong et al. 2014 (arXiv 1404.5617, abstract read): 10.0 (+18, -6.5)% at 95% limits for R_p above 6 Earth radii and P_p below 300 d if planets are preferentially coplanar; at least 47% if isotropic; from the seven systems then known. The abstract does not say per what sample. Our matching region ceiling (G2 sealed, final run): 2.1% (1.7 to 2.8% across the scenarios), 3.3% with the known planet counted. The H1 bias moves 2.1% to about 2.2 to 2.4% (estimate, not rerun). So the gap to 10% is not an artifact of the windows. Whether the 10% applies to our TESS binaries is **UNCERTAIN**, and one known planet is a weak reality check. Li 2016 not opened. | CONFIRMED (what the abstract says); the comparison **UNCERTAIN** |
| H3 | Unchanged: S = 0 below K = 6 understates reach. | NOT TESTED (a planting run at K 3 to 5 on the development split, about 0.3 points) |
| H4 | Unchanged: no dilution is generous; the half-light scenario is printed beside it (2.8% against 2.1%). | NOT TESTABLE UNTIL light ratios of these binaries exist |
| H5 | Unchanged: one known planet (TOI-1338 b). | NOT TESTABLE UNTIL T109 (a larger known-planet test, needs a download) |

### Group D (deferred) and the old lines
No change; the reasons stay as written above. The other ~170 old dated lines were not audited line by line (said at the top).

### What changes for the plan
1. G3 inputs: nothing blocks the go; U01 is LIKELY and cheap if wrong, U02 waits for the run.
2. Horizon page (R3): must carry the optimism sentence (R0 Amendment 3) and the "UNCERTAIN how the 10% maps" label; R1b is queued, not done.
3. Book: F-028 corrected (claims page and chapter 3).
