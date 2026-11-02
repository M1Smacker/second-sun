# Build queue (filed 30 Oct 2026): things to BUILD, not bugs

Rule from Ahmed (30 Oct 2026): `research/stage3/FIX-QUEUE.md` holds bugs only. Everything that is a new build, a study, a feature or a change to how we count lives here, one task per entry, never combined. Task numbers T31 to T60 are the old fix list numbers 31 to 60, kept so the notes that cite them still read right.

**Gate:** nothing here starts until the research (`research/RESEARCH-QUESTIONS-2026-10-30.md`, 14 questions, waiting for Ahmed's approval and a new weekly cap) is done and Ahmed says go. Then slowly: one task at a time, each in a fresh session, each logged in `research/usage-ledger.md` with the estimate written first. The research may change, merge or drop a task; that is decided task by task, not in advance.

**Legend:** V changes the search (a new Vesper version, a re-freeze, a new sealed-style test). S scorecard or statistics (a dated written amendment first; changes no old result). H harness, tool or page (no re-freeze). B book, learning or the other tracks. Cost is a guess in weekly points of my usage in a fresh session; machine time is free. Needs = the research question (Q) or task (T) that must be done first. Who = Claude, or Ahmed is needed. Every task starts as `[ ]` not started.

**Guess for all of it: about 33 to 40 points of my usage, before any research.** Each entry below is its own task.

## A. The filter (V). Each is a separate switch for a later Vesper version

- [ ] **T31. Depth sanity guard.** A dip deeper than about 30% of the flux, or a flux that reaches zero or below, cannot be a planet transit: tier 2 with its own flag name. Evidence: upside-down tier-1 max depth 1.0e7 ppm, 23 of 59 deeper than 1%; real max 265,216 ppm. Needs: Q8. Cost: about 0.3. Who: Claude. *Research 31 Oct:* (Q8) sealed: 147 of 12,261 events deeper than 10% (119 are QLP), 25 at 100% or more, 6 of the 85 tier-1 events deeper than 10%. **BUILT 2 Nov 2026 as switch `dg` (default off; tests in `pipeline/test_vopts.py`; zero-difference with switches off 300 of 300); judged in the 0.9 study (`V9-STUDY-PLAN.md`).**
- [ ] **T32. Near-zero noise guard for the SNR.** One sealed star-sector scored 3.5e26 (TIC 392536805, sector 76, QLP). Refuse or cap an SNR when the scatter estimate is below a floor. Needs: Q8. Cost: about 0.2. Who: Claude. *Research 31 Oct:* (Q8) sealed: 129 events with SNR above 100, 13 above 1,000. **RE-SCOPED and BUILT 2 Nov 2026 as switch `nd`: the 3.5e26 event is not near-zero scatter (scatter is about 1,000 ppm) but a baseline near zero (depth 3.7e29 ppm); its absurd SNR marks every real event of that light curve as dominated. `nd` leaves unphysical events out of the dominance comparison; judged in the 0.9 study.**
- [ ] **T33. Flare-shape check (ingress against egress).** 44 of 59 upside-down tier-1 events are 3 h boxes, short and deep, flare-like (LIKELY, NOT TESTED). Needs: Q3. Cost: about 1. Who: Claude. *Research 31 Oct:* (Q3) shape CONFIRMED. Concrete switch: flag when the late third of the box is shallower than the early third by more than 1.0 of the box depth; on the sealed run it flags about 18 of 42 measured tier-1 upside-down events and 1 of 26 real. Its price on planted box dips is NOT TESTED. See `post-sealed-literature-2026-10-31.md`. **BUILT 2 Nov 2026 as switch `fl` (asymmetry stored for every event, flag above the threshold, candidates 0.5, 1.0, 1.5 judged on development only); price on planted dips measured in the 0.9 study (`V9-STUDY-PLAN.md`).**
- [ ] **T34. Review the step check.** It fires on 82% to 90% of all raw events and on 51% of the strong planted dips that were lost (found 98% at K 14, kept 48%); the biggest single completeness cost. Each option trades about 1 point of recovery for 1 false alarm per 1,000, so test a better baseline estimate, not a looser threshold. Needs: Q5. Cost: about 1. Who: Claude. *Research 31 Oct:* (Q5) split into two switches, the coverage rule and the lift rule, priced separately. The step check alone: +9.8 planted points for +68 upside-down events (6.8 per point); gap-dump, ramp and dominated cost 1.4 to 2.0 per point.
- [ ] **T35. Decide the 3 h box.** It holds 62% of real and 75% of upside-down tier-1 events; circumbinary transits are longer. First a report-only split line (no search change), then decide. Needs: Q11. Cost: about 0.3. Who: Claude. *Research 31 Oct:* (Q11) tier-1 events by box (real, upside-down): 3 h (16, 44), 4 to 6.5 h (6, 3), 8 to 12 h (2, 8), 15 to 20 h (2, 4); predicted TOI-1338 b durations are 4.7 to 13.5 h.
- [ ] **T36. Cross-sector orbit-lock harness.** The 0.51% cost of c6 is an offline estimate because the harness cannot see other sectors. Either build a multi-sector plant test or keep the label "estimate". Related: Q6. Cost: about 1. Who: Claude.
- [ ] **T37. Run the Vesper 0.9 study.** Only after T31 to T36 each exist as their own switch (like c1 to c6 before): judge each switch on the same two numbers (kept real dips and false alarms), then freeze once. Machine time about 2 hours. Needs: T31 to T36 decided. Cost: about 2. Who: Claude.
- [ ] **T37b. Fresh-set sealed-style test of Vesper 0.9.** The 591 sealed stars are spent, so this needs a new star list, a preregistration written before any result, the download (shown on the Downloads page job list, needs Ahmed's yes), the search and the scoring. Needs: T37. Cost: about 3 (guess). Who: Claude, Ahmed for the download yes.

## B. The scorecard and the statistics (S)

- [x] **T38. Star-level S1.** Count stars with at least one tier-1 real event against stars with at least one upside-down event, with a cluster bootstrap over stars, beside the event count. Evidence: development 78 events on 21 stars, up to 14 on one star. Needs: Q4. Cost: about 0.5. Who: Claude. *Research 31 Oct:* (Q4) design effect 1.9 to 2.6 (sealed), 2.2 to 5.0 (development under 0.7.1). **DONE 2 Nov 2026:** built as section A of `pipeline/scorecard_plus.py`, Amendment 2 (`SCORECARD-AMENDMENTS.md`).
- [x] **T39. Asymmetry ratio from the whole run, per bar, with an interval.** The 1,500-sample, all-products estimate gave 1.41 where the full run gives 1.18 (sealed) and 0.98 against 0.92 (development); the ratio rises from 1.09 to 1.78 across bars 4.5 to 10. Needs: Q4. Cost: about 0.5. Who: Claude. *Research 31 Oct:* (Q4) ratio by bar, sealed: 1.18, 1.28, 1.39, 1.54 with star-bootstrap intervals; the two slices overlap at bar 7; dropping the 25 heaviest stars gives 1.36 and 1.33. Print both the limit and the detectable excess (sealed 33, 27, 17, 13 kept dips at bars 7, 8, 10, 12). **DONE 2 Nov 2026:** built as section A, with the detectable excess printed beside the limit.
- [x] **T40. S2 wording.** Both slices straddle the mark (development 4.97 to 11.34, sealed 6.80 to 11.47). Write down how a borderline reading is to be stated, and state a pooled 895-star rate once the development slice has been re-run with 0.8.0. Needs: T43. Cost: about 0.2. Who: Claude. **DONE 2 Nov 2026:** partly: the borderline wording rule is built (section D); the pooled 895-star rate waits for T43.
- [x] **T41. "DID NOT GENERALISE" fires in both directions** (the 20 h box was better in the sealed slice). Say "better" or "worse". Cost: about 0.1. Who: Claude. **DONE 2 Nov 2026:** built as section D (better, worse or no clear difference).
- [x] **T42. S4 gets a "found at all" column beside "kept".** The cost of the filter should be visible in every scorecard. Cost: about 0.2. Who: Claude. **DONE 2 Nov 2026:** built as section D (found at all beside kept).
- [x] **T43. Census run.** Re-run Vesper 0.8.0 over the 301 development stars so all 895 stars have one version and one lead list (about 25 minutes of machine time, registered on the job list). Development tuning makes it unfit for a test, fine for a census. Cost: about 0.3. Who: Claude. **DONE 2 Nov 2026 as a by-product of the 0.9 study:** the fresh 0.8.0 development run (`dev_428c5fb454cd`, options c6, under the post-download manifest) gives all 895 stars one version (0.8.0) and one manifest context; no extra census run is needed.
- [x] **T44. TOI-1338 b second line.** Add a labelled post-hoc line with an updated ephemeris; keep the preregistered line unchanged. Needs: Q1. Cost: about 0.2. Who: Claude. *Research 31 Oct:* (Q1) content ready: 7 of 10 sectors with an updated time hold a real event within 1.7 h, 4 of 4 forecast sectors, tier 1 in 4. Add it to the sealed scorecard file as a labelled post hoc section from Wang and Liu 2024 Tables 1 and 3; the preregistered line stays unchanged. **DONE 2 Nov 2026:** built as section E of `scorecard_plus.py` (Wang and Liu 2024 times, labelled post hoc).
- [x] **T45. Dated amendments for every scorecard change.** Each change is written as a dated amendment with the reason before the next sealed-style run (as was done for the leads rules). A process rule applied by T38 to T42, no cost of its own. **DONE 2 Nov 2026:** applied: `SCORECARD-AMENDMENTS.md`, Amendment 2.

## C. Leads and vetting (H)

- [ ] **T46. By-eye record per lead.** Store Ahmed's verdict on each lead. Needs: T59d (the real-candidate Eyes page). Cost: about 1.5. Who: Claude, Ahmed for the looking.
- [ ] **T47. Crowding and neighbour note on every lead card** from the light-curve headers if the keys are there, then a real pixel check later (target pixel files). Needs: Q12. Cost: about 1. Who: Claude. *Research 31 Oct:* (Q12) TESS-SPOC headers carry CROWDSAP and FLFRCSAP (QLP headers do not); 2 of 6 sealed leads have CROWDSAP below 0.8. Buildable from headers now.
- [ ] **T48. "Too deep for a planet" tag** on the card, automatically. Needs: T31. Cost: about 0.2. Who: Claude.
- [ ] **T49. Raw-light twin picture beside the cleaned one,** and the other sectors of the star at the same phase. Needs: Q12. Cost: about 0.5. Who: Claude.
- [ ] **T50. A census page** for all 895 stars (leads from both slices, one place). Needs: T43. Cost: about 1. Who: Claude.

## D. Harness, tools and process (H)

- [ ] **T51. Data branch commit message** says "counts only" even when it carries lead cards; say "counts and leads". Cost: 0.05. Who: Claude.
- [ ] **T52. Read the data set and the study options from each run's own settings** instead of the environment variables SS_SET and VESPER_OPTS, and fail loudly when the data folder is missing (the development example showed G1 paths with no files). Cost: about 0.3. Who: Claude.
- [ ] **T53. Finished marker.** `sealed_run.py` writes a small DONE file; the page uses it instead of inferring completion from file counts; plus an "exporter alive" light separate from "search alive". Cost: about 0.3. Who: Claude.
- [ ] **T54. Regression test:** the funnel of a finished run must equal the scorecard (sealed 26 and 59). Add to `pipeline/test_leads.py`. Cost: about 0.2. Who: Claude.
- [ ] **T55. Write the book preview recipe** into RESUME (static test page or `--no-livereload`; the pane's service-worker reload loop). Cost: 0.05. Who: Claude.
- [ ] **T56. Plan long jobs in a fresh context.** About 0.3 point per step after a compaction against about 1 point at 500K tokens (usage ledger). A working rule, applied to this whole queue by the gate above, no cost of its own.

## E. Book, learning and the other tracks (B)

The same-day rule for the learning track (finding goes into its chapter and a `learn/index.md` quiz check) is overdue for the sealed result; Ahmed set the order on 30 Oct, so these wait for the gate. One task each:

- [ ] **T57a. Chapter and quiz check: the sealed result** (what it showed, the clean null). Cost: about 0.25. Who: Claude.
- [ ] **T57b. Chapter and quiz check: events cluster on stars.** Cost: about 0.25. Who: Claude.
- [ ] **T57c. Chapter and quiz check: what a null means.** Needs: Q2 (so the wording is right). Cost: about 0.25. Who: Claude.
- [ ] **T57d. Chapter and quiz check: the leads section on the Search window.** Cost: about 0.25. Who: Claude.
- [ ] **T58a. Teaching note: "events cluster on stars",** in plain words with the development against sealed picture. Cost: about 0.25. Who: Claude.
- [ ] **T58b. Teaching note: "a control that is not a mirror".** Cost: about 0.25. Who: Claude.

The old "open build items" line was eight different builds; each is its own task:

- [ ] **T59a. Downloads page** (job list with what, from where, why, expected size, and the progress bar). Plan in `research/live-updates-literature-2026-10-30.md`. Until it exists, jobs go in `research/jobs.md`. Cost: about 1.5. Who: Claude.
- [ ] **T59b. Real-time channel (Firebase).** Needs Ahmed's console steps in `research/firebase-setup-steps.md`. Needs: T59a. Cost: about 2. Who: Ahmed first, then Claude.
- [ ] **T59c. F4 redesign** with rounded bars and the big colour change (unblocked now that the sealed search is done; Ahmed says when the colours change). Cost: about 8 to 15 (guess, the biggest task). Who: Claude, Ahmed for the colour decisions.
- [ ] **T59d. Real-candidate Eyes page** (unbuilt). T46 waits on it. Cost: about 1.5. Who: Claude.
- [ ] **T59e. Eye-training record page** (unbuilt). Cost: about 1. Who: Claude.
- [ ] **T59f. Real-layout rehearsal page** (unbuilt). Cost: about 1. Who: Claude.
- [ ] **T59g. Eyes sittings still needed.** Ahmed's own time on the Eyes pages. Cost: none of mine. Who: Ahmed.
- [ ] **T59h. Mission readiness cells** (44 work commits behind). Cost: about 0.5. Who: Claude.
- [ ] **T60. Rabtsevich / TIC 4206066:** report the TESS follow-up outcome honestly after 26 Nov 2026 (memory: reference_rabtsevich_tic4206066). Cost: about 0.2. Who: Claude. Date-driven, not research-driven.

## F. New tasks from the 31 Oct 2026 research (each its own task; details in `research/stage3/post-sealed-literature-2026-10-31.md`)

- [ ] **T101. Second control: scrambled light curves** beside the upside-down one, judged on the pooled union, as in Kepler DR25 (Q4). Needs: T38, T39. Cost: about 1. Who: Claude. Kind: S/V.
- [x] **T102. Loss ledger per known-planet transit:** which check cost which transit and in which product (Q1: S27 ramp, S96 gap-dump + step + dominated, S98 dominated). Cost: about 0.3. Who: Claude. Kind: H. **DONE 2 Nov 2026:** built as section E (flags that fired on every event near each transit).
- [x] **T103. Price table of every safety check** (planted points gained against upside-down events added when it is dropped alone) printed in every scorecard (Q5). Cost: about 0.3. Who: Claude. Kind: S. **DONE 2 Nov 2026:** built as section B.
- [ ] **T104. Store cover and lift in the planted-dip rows,** so the step check can be studied on planted dips (Q5 gap). Cost: about 0.3. Who: Claude. Kind: H. **BUILT 2 Nov 2026: `chain_recovery.py` rows now carry ev_depth_ppm, cover_pre, cover_post, lift_pre, lift_post, asym and the new flags; the rows themselves are produced by the 0.9 study run.**
- [x] **T105. Efficiency table beside every null:** expected tier-1 detections per planet-bearing star by depth and period (Q2). Cost: about 0.3. Who: Claude. Kind: S. **DONE 2 Nov 2026:** built as section C (host radius still 1 solar radius until T107).
- [ ] **T106. Cross-sector linker for single events:** rule written before running, tolerance near 1.6% on spacings, positive control TOI-1338 b (events in 4 of 4 forecast sectors) (Q6). Needs: Q6 follow-up. Cost: about 1.5. Who: Claude. Kind: V.
- [ ] **T107. Host radius and dilution in the efficiency table** (TIC radii from the headers for all 895 stars; two leads have none) so a limit can be set against Armstrong 2014 (Q2). Needs: T105. Cost: about 0.3. Who: Claude. Kind: S.
- [ ] **T108. Go-professional playbook page** (private draft): ExoFOP takes only published candidates, so the route is a collaborator or a refereed paper first; what leaves the public book at that moment (Q14). Cost: about 0.5. Who: Claude, Ahmed decides. Kind: B.
- [ ] **T109. Larger known-planet test:** add Kepler-field circumbinary hosts with TESS light curves (Q7); needs a download, so Ahmed's yes first. Cost: about 2. Who: Claude, Ahmed for the download. Kind: S.
- [ ] **T110. Compare the Eyes pass line with our own sittings** (Q13): both papers are read (PHT II has no single-volunteer accuracy; Davenport confirms the flare template). What is left is to set the clear-hit and false-alarm lines from our own Eyes data and keep feedback in training. Cost: about 0.3. Who: Claude, needs Ahmed's sittings. Kind: B.

## G. The next star list (31 Oct 2026; opinion in `research/stage3/NEXT-HUNT-OPINION-2026-10-31.md`)

- [ ] **T111. Find the new star list:** pull a post-sector-26 eclipsing-binary catalogue (Villanova live portal or Gaia DR3 candidates; a small file, Ahmed's yes first), count the detached, P over 7 d, Tmag 13 or brighter stars and their sectors, with no light curve touched. Needs: Ahmed's yes. Cost: about 0.7. Who: Claude. Kind: B. **PROGRESS 2 Nov 2026 (Ahmed said yes, tables only):** TESS Ten Thousand Catalog tables 3 and 4 downloaded (`data/g3/catalog_ttc`, 2.0 MB and 0.3 MB); counts in `g3-pool-counts-2026-11-02.txt`: table 3 has 7,936 EBs, none in G1, G2 or the Prsa table; P over 7 d and Tmag 13.5 or brighter = 612 stars (451 with RUWE 1.4 or less). Rule and list hash still to write (T112).
- [ ] **T112. Write the G3 rule, count and split before any download:** star rule, number of stars, ranking by sectors, preregistration committed with its hash (as G2 was). Needs: T111, T37. Cost: about 0.5. Who: Claude. Kind: S.

## Where the old lines went

The four lines under "After the sealed search" in the fix list: TOI-1338 b ephemeris drift is Q1 and T44; the chapter and learning-track check is T57a to T57d; the near-zero noise guard is T32; lead checks 5 and 6 (by-eye record, pixel check) are T46 and T47.
