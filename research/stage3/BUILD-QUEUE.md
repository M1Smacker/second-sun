# Build queue (filed 30 Oct 2026): things to BUILD, not bugs

Rule from Ahmed (30 Oct 2026): `research/stage3/FIX-QUEUE.md` holds bugs only. Everything that is a new build, a study, a feature or a change to how we count lives here, one task per entry, never combined. Task numbers T31 to T60 are the old fix list numbers 31 to 60, kept so the notes that cite them still read right.

**Gate:** nothing here starts until the research (`research/RESEARCH-QUESTIONS-2026-10-30.md`, 14 questions, waiting for Ahmed's approval and a new weekly cap) is done and Ahmed says go. Then slowly: one task at a time, each in a fresh session, each logged in `research/usage-ledger.md` with the estimate written first. The research may change, merge or drop a task; that is decided task by task, not in advance.

**Legend:** V changes the search (a new Vesper version, a re-freeze, a new sealed-style test). S scorecard or statistics (a dated written amendment first; changes no old result). H harness, tool or page (no re-freeze). B book, learning or the other tracks. Cost is a guess in weekly points of my usage in a fresh session; machine time is free. Needs = the research question (Q) or task (T) that must be done first. Who = Claude, or Ahmed is needed. Every task starts as `[ ]` not started.

**Guess for all of it: about 33 to 40 points of my usage, before any research.** Each entry below is its own task.

## A. The filter (V). Each is a separate switch for a later Vesper version

- [ ] **T31. Depth sanity guard.** A dip deeper than about 30% of the flux, or a flux that reaches zero or below, cannot be a planet transit: tier 2 with its own flag name. Evidence: upside-down tier-1 max depth 1.0e7 ppm, 23 of 59 deeper than 1%; real max 265,216 ppm. Needs: Q8. Cost: about 0.3. Who: Claude.
- [ ] **T32. Near-zero noise guard for the SNR.** One sealed star-sector scored 3.5e26 (TIC 392536805, sector 76, QLP). Refuse or cap an SNR when the scatter estimate is below a floor. Needs: Q8. Cost: about 0.2. Who: Claude.
- [ ] **T33. Flare-shape check (ingress against egress).** 44 of 59 upside-down tier-1 events are 3 h boxes, short and deep, flare-like (LIKELY, NOT TESTED). Needs: Q3. Cost: about 1. Who: Claude.
- [ ] **T34. Review the step check.** It fires on 82% to 90% of all raw events and on 51% of the strong planted dips that were lost (found 98% at K 14, kept 48%); the biggest single completeness cost. Each option trades about 1 point of recovery for 1 false alarm per 1,000, so test a better baseline estimate, not a looser threshold. Needs: Q5. Cost: about 1. Who: Claude.
- [ ] **T35. Decide the 3 h box.** It holds 62% of real and 75% of upside-down tier-1 events; circumbinary transits are longer. First a report-only split line (no search change), then decide. Needs: Q11. Cost: about 0.3. Who: Claude.
- [ ] **T36. Cross-sector orbit-lock harness.** The 0.51% cost of c6 is an offline estimate because the harness cannot see other sectors. Either build a multi-sector plant test or keep the label "estimate". Related: Q6. Cost: about 1. Who: Claude.
- [ ] **T37. Run the Vesper 0.9 study.** Only after T31 to T36 each exist as their own switch (like c1 to c6 before): judge each switch on the same two numbers (kept real dips and false alarms), then freeze once. Machine time about 2 hours. Needs: T31 to T36 decided. Cost: about 2. Who: Claude.
- [ ] **T37b. Fresh-set sealed-style test of Vesper 0.9.** The 591 sealed stars are spent, so this needs a new star list, a preregistration written before any result, the download (shown on the Downloads page job list, needs Ahmed's yes), the search and the scoring. Needs: T37. Cost: about 3 (guess). Who: Claude, Ahmed for the download yes.

## B. The scorecard and the statistics (S)

- [ ] **T38. Star-level S1.** Count stars with at least one tier-1 real event against stars with at least one upside-down event, with a cluster bootstrap over stars, beside the event count. Evidence: development 78 events on 21 stars, up to 14 on one star. Needs: Q4. Cost: about 0.5. Who: Claude.
- [ ] **T39. Asymmetry ratio from the whole run, per bar, with an interval.** The 1,500-sample, all-products estimate gave 1.41 where the full run gives 1.18 (sealed) and 0.98 against 0.92 (development); the ratio rises from 1.09 to 1.78 across bars 4.5 to 10. Needs: Q4. Cost: about 0.5. Who: Claude.
- [ ] **T40. S2 wording.** Both slices straddle the mark (development 4.97 to 11.34, sealed 6.80 to 11.47). Write down how a borderline reading is to be stated, and state a pooled 895-star rate once the development slice has been re-run with 0.8.0. Needs: T43. Cost: about 0.2. Who: Claude.
- [ ] **T41. "DID NOT GENERALISE" fires in both directions** (the 20 h box was better in the sealed slice). Say "better" or "worse". Cost: about 0.1. Who: Claude.
- [ ] **T42. S4 gets a "found at all" column beside "kept".** The cost of the filter should be visible in every scorecard. Cost: about 0.2. Who: Claude.
- [ ] **T43. Census run.** Re-run Vesper 0.8.0 over the 301 development stars so all 895 stars have one version and one lead list (about 25 minutes of machine time, registered on the job list). Development tuning makes it unfit for a test, fine for a census. Cost: about 0.3. Who: Claude.
- [ ] **T44. TOI-1338 b second line.** Add a labelled post-hoc line with an updated ephemeris; keep the preregistered line unchanged. Needs: Q1. Cost: about 0.2. Who: Claude.
- [ ] **T45. Dated amendments for every scorecard change.** Each change is written as a dated amendment with the reason before the next sealed-style run (as was done for the leads rules). A process rule applied by T38 to T42, no cost of its own.

## C. Leads and vetting (H)

- [ ] **T46. By-eye record per lead.** Store Ahmed's verdict on each lead. Needs: T59d (the real-candidate Eyes page). Cost: about 1.5. Who: Claude, Ahmed for the looking.
- [ ] **T47. Crowding and neighbour note on every lead card** from the light-curve headers if the keys are there, then a real pixel check later (target pixel files). Needs: Q12. Cost: about 1. Who: Claude.
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

## Where the old lines went

The four lines under "After the sealed search" in the fix list: TOI-1338 b ephemeris drift is Q1 and T44; the chapter and learning-track check is T57a to T57d; the near-zero noise guard is T32; lead checks 5 and 6 (by-eye record, pixel check) are T46 and T47.
