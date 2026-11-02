# Research brief: Vigil, Witness, Horizon and the parked ideas (written 2 Nov 2026)

**Status: QUESTIONS ONLY. No research has been done for this brief.** Written at Ahmed's request ("every single new idea should be researched exhaustively"). He verifies this file first. After the weekly reset (Tue 3 Nov 2026, 01:00 Kuwait) he says go, and nothing else is touched or built before this research is finished. Queue entry: T122 in `BUILD-QUEUE.md`. Concepts: T119 Horizon, T120 Vigil, T121 Witness (all approved as concepts, none to be built yet).

Method: `research/RESEARCH-BLUEPRINT.md` in full. Questions tied to decisions, our own data first, primary pages opened (arXiv abstract and HTML, official docs, never a PDF or data file in the browser pane), exact sentences pulled, labels CONFIRMED / LIKELY / UNCERTAIN / NOT TESTED, every finding turned into a plan change and filed. At least 10 minutes on every P1 question. No sub-agents. Evidence ladder from `learning-and-checking-literature-2026-11-02.md`: a claim that "we are right" needs a ground-truth or a control that could have failed; my own reasoning is the weakest evidence.

**Priority tags.** P1 = a gate: the answer can kill or reshape the system, answer first. P2 = shapes the design. P3 = a detail that still bites later.

## 0. Facts already checked today (own house, 2 Nov 2026)

- CONFIRMED: the `second-sun` repository on GitHub is **PUBLIC** (`M1Smacker/second-sun`). Anything a cloud job prints or commits there is public. `data/` is git-ignored (`.gitignore` line 7).
- CONFIRMED: the search code never reads SAP_BKG, POS_CORR, MOM_CENTR or PSF_CENTR (case-insensitive grep over `pipeline/*.py`; the one hit for "centroid|background" is `leads_export.py`). One local SPOC file (Sector 6) carries all four plus QUALITY.
- CONFIRMED: `scorecard_plus.py` bounds the excess of tier-1 real over the upside-down control in star counts; book chapter 08 line 137 and `burn-1-science/open-questions.md` item 6 both say a real sensitivity map is missing.
- CONFIRMED (from the summary of the earlier session): item 70, QLP neighbour windows depend on the manifest; QLP changes method from Sector 94 and may reprocess all data (UNCERTAIN until its release notes are opened).
- From memory, UNCERTAIN, to be verified: every GitHub, MAST, TESS and statistics figure written below as "(memory)".

## 1. Constraints that shape every answer

1. **Ahmed's computer will not be on all day.** Vigil must not depend on it. A third-party scheduler is acceptable (he named n8n or an "AI automation site"), free, and it should tell him when something is found.
2. **Claude cannot create accounts or type passwords.** Any service that needs a new account is a step for Ahmed himself. Prefer what he already has (GitHub).
3. **The repository is public.** Leads, star IDs, event times and candidate claims must never reach a public log, commit or issue (standing rule: named leads stay private until two keys and his yes). Counts only in public.
4. Frozen version per Vigil line; sealed sets; no tuning on results; no outward action (email, CTOI, post) without his yes; book publishing stays mine.
5. Phone-first: he reads from an iPhone, so alerts must reach it.
6. Weekly cap: new-week default stop at 25% and wait for his word. This research is estimated at about 10 points (range 6 to 14) over 3 to 4 sessions (ledger calibration: the Loom first pass cost about 0.9 point against a 2.0 estimate; this brief is about three times wider and goes to primary pages everywhere).
7. Model: the blueprint (section 8) says deep research runs on the strongest model Ahmed picks. **Ask him which model before session 1, and tell him at each switch.**

## 2. Vigil (the main one): questions

Idea in one line: every new TESS sector for our star lists is searched within days by the frozen Vesper, under a protocol sealed in advance; time is the seal; a prediction ledger makes the sky the referee; the monthly run must not need his PC.

### V-A. Does the sky actually supply the data, and how fast? (nothing here has been searched)

- **V-A1 [P1]** How many stars on our lists (G1, G2, G3) got at least one new light-curve file in sectors released after each list was frozen, and how soon after the sector ended? Decides: whether Vigil has anything to watch. Own data: a free MAST query backtest, no download (like `g3_window_feasibility.py`). Plan change if: fewer than about 1 in 5 stars get any new file a year, Vigil shrinks to a quarterly check.
- **V-A2 [P1]** Release lag per product: SPOC 2-minute, TESS-SPOC full-frame, QLP full-frame (days from sector end to MAST). Open: TESS data release notes per sector, MAST HLSP pages for QLP and TESS-SPOC, Huang 2020 and Kunimoto 2022 (QLP), Caldwell 2020 (TESS-SPOC). Decides: how quick "within days" really is.
- **V-A3 [P1]** TESS pointing plan for the cycles ahead and mission end date: where do our stars fall, how many future looks per star, is there a funding or safe-mode risk? Open: TESS mission pages, the TESS pointing and sector plan, the NASA Senior Review outcome (UNCERTAIN what it says). Also check the observing tool for our stars (tess-point).
- **V-A4 [P2]** Does a star stay on 2-minute cadence? 2-minute targets are chosen per cycle (guest investigator and TESS science team lists). How many of our stars are on the approved target lists for the coming cycle (public CSV lists on the TESS site; open the page, do not click files in the pane)?
- **V-A5 [P1]** QLP in detail: what changes at Sector 94, whether old sectors are reprocessed, whether new and old QLP light curves are comparable. Open: QLP HLSP release notes. Decides: whether QLP stars can sit in a Vigil line at all (item 70 showed comparability can break silently).
- **V-A6 [P2]** Reprocessing of SPOC data (past reprocessings of early sectors): how often, announced how? Our ledger must record DATA_REL and PROCVER per file (SPOC and TESS-SPOC carry them; QLP has none: filename token and sha256 only).
- **V-A7 [P3]** Cadence changes (20 s, 120 s, 200 s, 10 min, 30 min full-frame history): does a cadence change inside one star's record break the matched filter or the windows table?
- **V-A8 [P2]** Are there other free sources worth adding for new data (TESS-SPOC faint-star products, DIAMANTE, eleanor-lite)? Open each product page; check whether it covers our stars and how fast.

### V-B. The statistics of looking every month

- **V-B1 [P1]** Repeated looks: how is the false-alarm budget paid when we test every new sector? Candidates: group-sequential alpha spending (Pocock, O'Brien-Fleming, Lan-DeMets), online false discovery control (alpha-investing, LORD, SAFFRON), or the empirical null we already own (the upside-down control recomputed every sector). Which is valid when the noise is red and not stationary? Open: Foster and Stine 2008; Javanmard and Montanari; Ramdas et al. Decides: the sentence in the protocol that defines a lead. Must be written before sector one.
- **V-B2 [P1]** Is the upside-down control still a fair null in a rolling setting (stars, sectors and months are not exchangeable)? Own data: compute control versus real ratios per sector within G2 and G3 once available and see how much they wobble from sector to sector. Plan change if: wobble is large, the protocol uses pooled windows and says so.
- **V-B3 [P2]** What does "lead" mean when evidence accumulates over sectors: one tier-1 event, or two weak events consistent with one orbit? Open: how Kepler CBP searches linked events (Kostov 2013 and 2016, Armstrong 2014, Windemuth 2019; exact titles to be found, not recalled).
- **V-B4 [P1]** Stacking was ruled out for generic periods in the 0.9 plan. Is it rescued by a physical prior (circumbinary planets pile up just outside the stability limit)? Open: Welsh 2012, Martin and Fabrycky 2021, Li 2016, Quarles 2018 (memory, titles unverified). Own data: compute planet to binary period ratios for all known CBPs from the NASA Exoplanet Archive. Decides: whether a linker unit exists in Vigil. Honest expectation: the gain in reach is modest (two events of SNR 5 give about 7); the question is whether the trials factor collapses enough to make it real.
- **V-B5 [P1]** Predicting repeat windows from one transit: given the binary ephemeris and one observed event, how wide are the windows in days (transit timing variations of a circumbinary planet can be days)? If the windows are months wide, the prediction ledger has no power. Open: Kostov 2020 (TOI-1338), Doyle 2011 (Kepler-16), Welsh 2012, Martin 2017 and Borkovits on timing; tools REBOUND, ellc, photodynam. Own data: compute from TOI-1338 b's published ephemeris.
- **V-B6 [P2]** What fraction of the future windows land inside already planned sectors? Needs V-A3.
- **V-B7 [P2]** Expected yield: with a Kepler-like occurrence and our coverage, how many detections per year of Vigil? Shares with Horizon H-4 and H-9. If the answer is "one in a century", say so in the book.

### V-C. Where it runs without his PC (the question he raised)

First, the question under the question:

- **V-C0 [P1]** How much does latency matter? The archive keeps the data, so a run that happens a week late finds the same files. What is time-critical is only that predictions are stamped before the data they predict is released. If a monthly catch-up run (Windows Task Scheduler with "run as soon as possible after a missed start") is enough, then the PC-off problem is smaller than it looks and a cloud runner becomes a convenience for alerts. Decide this before spending on cloud research.

Then, if cloud is wanted:

- **V-C1 [P1]** Options and their real limits, each checked on the official page: GitHub Actions (public repo: minutes, per-job time limit (6 h, memory), runner size, disk, cron delay and cron disabling after long inactivity (memory: 60 days, UNCERTAIN); private repo: free minutes (memory: 2,000 a month, UNCERTAIN)); n8n (self-hosted needs a server; n8n Cloud pricing and execution limits, UNCERTAIN); Oracle Cloud Always Free (needs a card; idle reclaim rules); Kaggle scheduled notebooks; Google Colab (no free scheduling, memory); PythonAnywhere free tier (internet whitelist: is MAST on it?); Hugging Face Spaces; Anthropic scheduled cloud agents (uses plan points, cannot hold large data); an always-on home device if he owns one (a Raspberry Pi uses a few watts; ask him).
- **V-C2 [P1]** Can any of them run Vesper? Own data first: time one star end to end locally (compile time, search time, memory). Then compare to the runner limits: a monthly run over about 1,500 stars; chunk into matrix jobs if the 6 h job limit bites.
- **V-C3 [P1]** MAST access from cloud runner IPs: rate limits, blocking, throttling (we already saw 12 concurrent lightkurve searches throttled; 8 worked). Open: MAST API usage policy and the data-access guidance.
- **V-C4 [P1]** Privacy on a public repo: how to keep leads out. Options: a private second repository (Actions logs of private repos are private, UNCERTAIN to confirm), an encrypted output file (age or GPG) with the key only on his machine, or publish counts only and keep the lead list local until he is online. Which one breaks fewest rules? Open: GitHub docs on log visibility and secrets.
- **V-C5 [P2]** Where does state live between runs (last processed sector, ledger, caches)? Options: repository files (counts only), GitHub cache and artifacts (retention limits), release assets, free object storage tiers (UNCERTAIN: Cloudflare R2, Backblaze B2 free sizes). The ledger must survive: what is the recovery plan if a runner loses state?
- **V-C6 [P1]** Alert to his iPhone with no new account if possible: GitHub mobile notifications for a private issue, an email from the workflow, ntfy.sh push (free, no account, but topic names are public-guessable), Telegram or Discord bot, healthchecks.io for "the job did not run" (dead-man switch). What may the message contain? Default: "sector N searched, K leads waiting, details private", never a star ID.
- **V-C7 [P2]** Does the cloud result equal the local result? Same code on x86 and ARM, different numba, numpy and BLAS versions can move events marginally. Test: run 20 stars locally and in the cloud, compare event lists to a stated tolerance. Pin the environment (lockfile or container).
- **V-C8 [P2]** Is an "AI agent" needed in the loop? The monthly run is deterministic Python. LLM nodes in n8n need a model API key, which costs money per use (memory, UNCERTAIN). Likely answer: no AI inside the run; AI (me) only reads the summary. Verify, then say so plainly.
- **V-C9 [P3]** Terms of service: automated scheduled downloads from MAST, scheduled compute on GitHub (cron on a public repo is allowed; abuse rules). Read the pages.
- **V-C10 [P3]** Secrets handling: tokens in the repository settings, no keys in code; Claude cannot type passwords, so Ahmed sets the secrets himself.
- **V-C11 [P2]** What does he have already (GitHub account, any always-on device, a card for a free-tier signup he is willing to use)? Ask him; do not guess.

### V-D. The protocol itself (written once, before sector one)

- **V-D1 [P1]** Which Vesper runs: 0.8.0, or 0.9 once frozen with the five rejected switches retired? A Vigil line never mixes versions. What event forces a new line (Witness, a bug fix)?
- **V-D2 [P2]** Which star lists, and what happens to new stars (new EB catalogs, Gaia DR3 eclipsing binaries)? A growing list needs "list epochs" so the statistics stay clean.
- **V-D3 [P2]** Window rules in a rolling setting: the QLP neighbour-window issue (item 70). Freeze the pool rule in the protocol.
- **V-D4 [P1]** What happens to a lead? Two keys (machine and Ahmed's eye), the rehearsal pass line first, the Eyes pictures, pixel checks (T46, T47), then ExoFOP or CTOI only with his yes. Which of these exist today and which are missing?
- **V-D5 [P2]** What is public: counts, ceilings, the hash chain, the protocol. What is never public: leads. Write the exact list.
- **V-D6 [P3]** Do we need a second, independent implementation or a reviewer for the protocol? (Evidence ladder: my review is the weakest check.)

### V-E. The ledger and trust

- **V-E1 [P1]** Is a GitHub commit time a real timestamp? A commit's author date can be set to anything locally; the push time is not stored in the commit. Candidates: OpenTimestamps (anchored to Bitcoin, free), an RFC 3161 timestamp authority, GitHub's events API for push times. Open the official docs. This decides whether the prediction ledger has evidential value.
- **V-E2 [P2]** Hash chain design: SHA-256 over canonical JSON (key order, float formatting, newline rules), what is hashed (inputs, outputs, code hash, data hashes), genesis record, how a mistake is corrected (append a correction, never edit).
- **V-E3 [P2]** Can an outsider rebuild the chain from public inputs? Write that test before building.
- **V-E4 [P2]** How do the ledger and the Loom status JSON (phase 4) relate? One record format, or two? Open the RO-Crate and OpenLineage notes in `loom-literature-2026-11-03.md`.
- **V-E5 [P3]** Does a preregistered prediction convince anyone? How do registered reports and the astronomy community treat preregistration and blind analysis (MacCoun and Perlmutter 2015 is the start)?
- **V-E6 [P3]** Credit and honesty text for the book page: what we claim, what we do not.
- **V-E7 [P3]** Backups of the ledger and caches (the memory-copy rule: two independent copies).

### V-F. Small things that bite later

- **V-F1 [P2]** Time systems: TESS BTJD versus UTC, barycentric correction (TIMECORR), leap seconds, so predicted windows are stated in one system with the offset written down.
- **V-F2 [P2]** TESS gaps in future sectors: orbit gaps, momentum dumps, safe-mode events (some sectors were cut short; check), scattered light, stars near camera edges or chip gaps.
- **V-F3 [P3]** A star observed by two cameras or two products in one sector: which is used, how not to count twice.
- **V-F4 [P2]** Disk and bandwidth per sector for about 1,500 stars; clean-up rules; `research/jobs.md` and `downloads.csv` updates.
- **V-F5 [P3]** What if MAST is down, a sector is missing, or a file is corrupt: retry rules and a visible "skipped" record.
- **V-F6 [P3]** Cost of the monthly human review in points; what Ahmed sees each month on the book (one status line).
- **V-F7 [P3]** Who can break it: package updates, Python versions, Windows updates; pin and test before upgrade.
- **V-F8 [P2]** What is Vigil's own test: a dry run on already-released sectors that replays "as if new" (the backtest) and a planted dip injected into a new sector's input that must be recovered end to end.
- **V-F9 [P3]** Name check: "Vigil" fine? (Ahmed's call.)

## 3. Witness (runner-up): questions

Idea: use the spacecraft's own housekeeping channels to testify against false alarms, in the manner of LIGO's Hveto.

- **W1 [P1]** Own data first, before any web: how many tier-1 upside-down control events survive the flags in the G2 dev runs? If there are fewer than about 30, the coincidence statistics are too weak and the idea stops here. Cost of the check: small.
- **W2 [P1]** Novelty check: is this just standard decorrelation? Astronomy already regresses flux on pointing and centroid motion (K2SFF, EVEREST, pixel-level decorrelation, the Kepler cotrending basis vectors) and TESS data validation reports run centroid tests. What does a veto add that regression does not? Open: Vanderburg and Johnson 2014, Luger 2016, Deming 2015, Twicken 2018, Li 2019 (titles to be verified).
- **W3 [P1]** Open Hveto itself: Smith et al. 2011, Classical and Quantum Gravity 28, 235005, arXiv:1107.2948. Pull the exact steps, the statistic, the thresholds, the window, the safety test, the efficiency and deadtime definitions. Check the later software documentation.
- **W4 [P2]** Which channels exist in each product we use? Own data: scan headers in `data/g2`, `data/g3` for SPOC 2-min, TESS-SPOC and QLP; list columns and the fraction that are all NaN (PSF_CENTR often is, memory, check).
- **W5 [P2]** What each channel measures (TESS archive manual and data release notes): SAP_BKG, POS_CORR1 and 2, MOM_CENTR, PSF_CENTR, QUALITY bits.
- **W6 [P1]** Safety: do true transits move the channels? Planted dips are added to flux only and so are safe by construction (a trap). Real transits are the honest test (TOI-1338 b and known TOIs). Centroids shift when a blended target dims (Bryson 2013 on centroid offsets). Which channels are safe: background and pointing probably; centroid not for blends.
- **W7 [P2]** Which surviving false alarms are they, physically? Own data: look at a sample of control events with the channels beside them. If the cause is stellar variability, no housekeeping channel will see it.
- **W8 [P2]** Trials: channels times thresholds times windows. Pay for them (V-B1 applies). Train on G2 dev only; the out-of-sample test is Vigil's future sectors, which is free.
- **W9 [P2]** Deadtime: fraction of observing time vetoed, charged to Horizon's reach and to window coverage.
- **W10 [P1]** Kill rule written first: coincidence excess below p 0.01 after the trials correction, or any loss of planted or real recoveries above a stated limit, kills it. Set the numbers before running.
- **W11 [P3]** It is a new switch: the 0.9 rules apply, it forces a new Vigil line, and it must be frozen before G3 or run only as an analysis.
- **W12 [P3]** Cost of reading the channels per event (cache in the Loom).

## 4. Horizon: questions

- **H-1 [P1]** Find and open Oddo et al. 2026 (said to be arXiv:2610.22625, UNCERTAIN, entry not found on 29 Oct). How did they compute reach and the occurrence ceiling, which grid, which assumptions?
- **H-2 [P1]** Stability limit: verify Holman and Wiegert 1999 (critical semi-major axis formula, mass-ratio and eccentricity dependence) and the observed ratio P_planet to P_binary for every known transiting CBP (NASA Exoplanet Archive query; own data once downloaded as a small table with Ahmed's yes). Fills the two UNCERTAIN lines in `HORIZON-DESIGN.md`.
- **H-3 [P1]** Transit probability of a circumbinary planet given the mutual inclination distribution (Martin and Fabrycky 2015 on transit probabilities, titles to be verified), and what Kepler says about coplanarity.
- **H-4 [P1]** Kepler CBP occurrence rates (Armstrong 2014, Welsh 2012, Martin and Fabrycky 2021, Li 2016 as starting points) and what they predict for our searches. Needed for V-B7 too. Label which numbers are measured and which assumed.
- **H-5 [P2]** Depth to radius in a blended pair: are the radii and light ratios in the TESS Ten Thousand Catalog tables we hold (`data/g3/catalog_ttc`)? Own data first: list columns. Otherwise Gaia DR3 sources, or an explicit assumption.
- **H-6 [P2]** Window coverage to detection chance: read the reference windows table (Loom phase 0) and the preview `g3-window-feasibility-2026-11-02.txt`; write the exact formula for P(at least one event) per period.
- **H-7 [P1]** Injection realism: real circumbinary transits shift in time, change duration, and can sit on eclipses (`ecl_overlap`). What do our planting tools do now (the book names STANLEY; read the code and the chapter)? Own data: the fraction of random transit times that land inside eclipses for G2 binaries.
- **H-8 [P2]** Noise model for recovery: bin by measured noise per star, not only by Tmag.
- **H-9 [P1]** Ceiling statistics with a background: zero found versus k found with a measured control background. Feldman and Cousins 1998, Gehrels 1986, Poisson one-sided; which is right for an excess over a bootstrapped control? Compare against how our `scorecard_plus.py` does it today.
- **H-10 [P2]** How many injections per cell for a stated precision (binomial error): compute before launching.
- **H-11 [P2]** Compute: time one star, then budget the overnight job.
- **H-12 [P2]** What do published sensitivity maps and ceilings for Kepler and TESS binaries look like, so ours is comparable?
- **H-13 [P3]** Planet radius range and the name (Ahmed's two answers).
- **H-14 [P2]** Rules check: planting only in G2 dev; confirm from `G2` split files that nothing sealed is touched; write the G3 preregistration addendum text.

## 5. Parked ideas from the first brainstorm (short; a fourth block)

Twin Test (does Ahmed's eye add information beyond Vesper's flags?)
- **T-1 [P2]** Map the rehearsal's six answers onto Vesper's flags. Own data: which flags correspond to Flare, Step, Instrumental, Eclipse?
- **T-2 [P2]** Which agreement statistic (kappa, d-prime, McNemar) and how many items are needed. Compute the sample size first.
- **T-3 [P3]** Independence of the two keys: if he learns from Vesper's flags, he stops being independent. How to keep the test clean.

Numbers Desk (book numbers pulled from result files)
- **N-1 [P2]** Count the measured numbers typed by hand in the book today (the status cells I refreshed by hand on 2 Nov are the first example).
- **N-2 [P2]** Can MkDocs macros or a build hook resolve tokens and fail on stale sources without false alarms?
- **N-3 [P3]** Overlap with Loom phase 4 (one JSON status per run).

State pack generator (rebuilds the resume file from jobs, ledger, queues and git)
- **S-1 [P3]** Is it worth the points compared with the anchor file I write by hand? The 2 Nov clock slips (times from estimates) are the evidence for it.

## 6. Cross-cutting questions

- **X-1 [P1]** Dependency order: Loom phase 0 and 1, then Horizon, then Vigil; Witness feeds the version decision; G3 prep and search. Draw it, with what blocks what.
- **X-2 [P1]** For each system, write the kill criteria before researching further: what finding means "do not build".
- **X-3 [P2]** How does each system change what the book may claim? Honest-limits text per system.
- **X-4 [P2]** Monthly upkeep in points for Vigil with and without cloud.
- **X-5 [P2]** For each key claim, name the check that could have failed (evidence ladder). Flag any claim that rests on my reasoning alone.
- **X-6 [P1]** What Ahmed has to provide or decide, in one list at the end: accounts he must create, devices, secrets, the model for the research, the two Horizon answers.
- **X-7 [P3]** Stop lines: the research stops at the weekly line he sets; what is unfinished is filed, not rushed.

## 7. Order and time boxes

1. **Session 1, Vigil gates (about 5 points, 2.5 hours):** V-C0, V-A1 to V-A3, V-A5, V-C1 to V-C4, V-C6, V-E1, V-B1, V-B2, V-B4, V-B5. Gates: (a) cloud cannot run Vesper within limits or cannot keep leads private: Vigil becomes a local monthly run with catch-up; (b) too few stars get new data or the lag is too long: Vigil shrinks; (c) prediction windows too wide: the ledger loses its power and Vigil becomes a monthly null meter.
2. **Session 2, Horizon (about 3 points, 1.5 hours):** H-1 to H-4, H-7, H-9, then the rest.
3. **Session 3, Witness (about 1.5 points, 1 hour):** W1 first (own data), then W2, W3, W6, W10.
4. **Session 4, rest (about 1 point):** remaining V, T, N, S, X questions.
Output: one findings file per system (`vigil-literature-<date>.md` and so on), each question with its answer, label, link and plan change; a plain verdict per system (go, no-go, changed); queue entries updated; ledger rows; commit and push the same session.

## 8. Count

89 questions in all: Vigil 49 (A8, B7, C12 including C0, D6, E7, F9), Witness 12, Horizon 14, parked ideas 7, cross-cutting 7, plus the model and account questions for Ahmed.
