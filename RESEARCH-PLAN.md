# Second Sun: Research Plan

*Written 2026-10-19 by Claude (Claude Code, Opus 5.5) with Ahmed Hanzala, after 25 question rounds.*
*Status: **DRAFT, waiting for Ahmed's OK.** No research starts until he says go.*

This is the plan for **researching** the bible. It is not the bible. When research is done, its findings get written into the bible (a book website), and this plan becomes one of the book's pages, so the method is on record.

---

## 0. Plain-words glossary (no jargon walls)

| Word | What it means |
|---|---|
| **TESS** | NASA's planet-hunting space telescope. It stares at patches of sky and records how bright stars are over time. All its data is free. |
| **Sector** | One ~27-day stare at one patch of sky. TESS has done many sectors since 2018; some stars were watched in dozens of them. |
| **Light curve** | A graph of a star's brightness over time. A planet passing in front of its star makes a small dip. |
| **Transit** | That dip: a planet crossing in front of its star. |
| **Eclipsing binary (EB)** | Two stars orbiting each other, taking turns blocking each other's light. Makes big, regular dips. |
| **Circumbinary planet (CBP)** | A planet orbiting *both* stars of a binary. Our main quest. Its dips come at irregular times, which is why NASA's normal search misses them. |
| **TOI / CTOI** | TESS Object of Interest: an official planet candidate. CTOI = a Community TOI, submitted by people like us. |
| **ExoFOP** | The official website where candidates are listed and where CTOIs are submitted. |
| **Vetting** | Checking whether a dip is a real planet or a fake (binary star, spacecraft glitch, neighbouring star). |
| **Pipeline** | Our chain of programs: download → clean → search → vet. |
| **Injection-recovery** | Plant fake planets in real data, see if our pipeline finds them. Tells us what we *can* find. |
| **Claim register** | A list of every fact in the bible, with its source, its confidence level and the date it was checked. |

---

## 1. Where we stand (measured, 2026-10-19)

| Thing | Value | Consequence |
|---|---|---|
| CPU | Intel i7-8700K, 6 cores / 12 threads | Fine for batch searches; parallel jobs over ~10 cores |
| RAM | 16 GB | Fine for light curves; limits giant in-memory datasets |
| GPU | AMD Radeon RX 6800 XT | No CUDA → machine learning runs on CPU (OK at our scale; research checks alternatives) |
| C: drive | **14.3 GB free (97% full), and it dropped ~4 GB in an hour** | Nothing for Second Sun goes on C:, *including hidden caches* (pip, astropy, lightkurve default to C:) |
| D: drive | 506 GB free | Project + all data live in `D:\second-sun` |
| Python | 3.14 is default; **3.12 installed at `C:\Python312`** | Project uses 3.12 (3.14 too new for some science packages) |
| uv / conda | Not installed | Plain `venv` from 3.12, unless research finds a must-have reason |
| WSL (Linux) | Not installed | Only installed if research proves a must-have tool is Linux-only; Ahmed runs the install |
| git / gh | Installed; GitHub account **M1Smacker** logged in; no global git name set | Repo-level identity: M1Smacker + GitHub no-reply email |
| Claude plan | **Pro.** Weekly limit 52% used, resets ~01:00 Kuwait on 2026-10-20 | Burn the leftover tonight (parallel OK), then one session at a time over weeks |

---

## 2. Every decision so far (seeds the book's dated decision log)

All decided 2026-10-19 by Ahmed. **Superseded** answers are marked so nobody re-litigates them.

**You and the goal**
- Starting level: **total beginner**; maths **rusty** (rebuild gently); coding goal: **read and understand** (Claude writes the code).
- Works in **bursts**, usually **weeknight evenings** (Kuwait time), from **PC and phone equally**.
- Why: **love of space (most important)**, leave a mark, prove an ordinary person + AI can do frontier science. Lifelong space fan.
- Dream ending: all four (NASA announces it, name on a big paper, recognised citizen scientist, new path), and **NASA announcing it** is the top one.
- Horizon: **as long as it's fun**, so fun is a design requirement, not decoration.
- People: **just Ahmed and Claude.** Open to formal collaboration with a university or research group if it goes big ("yes, gladly"). Telescope: maybe later.
- Identity: **Ahmed Hanzala, Pakistani, living in Kuwait as an expat.** Credit line: *"Ahmed Hanzala, independent citizen scientist (Pakistan), based in Kuwait"*. AI use disclosed plainly; Ahmed is the discoverer.
- Success: **the ladder**: clean CTOIs → a paper with your name → the headline circumbinary find. Side rungs: new variable stars to AAVSO VSX; a possible method paper ("an amateur + AI searched X stars").

**Quests**
- **Main quest: circumbinary planets.** "Circumbinary regardless (mainly)" + find the gaps inside it.
- **Training quest:** hidden siblings around known planet hosts.
- **Side quest:** anomalies (exocomets, disintegrating planets, the next Tabby's Star). **Opportunistic:** habitable-zone rocky planets, white-dwarf planets.
- **Archives in bounds: all** (TESS, Kepler/K2, Gaia, ground surveys), built into "one smart system".

**Rules of evidence and judgment**
- **Every claim sourced**, with a confidence label, in a claim register. Claude's memory is a *lead*, never a source.
- Core papers read **in full**; the rest by abstract. Conflicting sources: **show both, pick one, say why.**
- Hands-on proof: **mixed**. Prove key claims with small tests.
- Contact astronomers **only when it saves months**: Claude drafts, Ahmed sends. Their private messages and contact details never go in the book.
- Submitting a candidate needs **two keys** (Claude's analysis passes AND Ahmed agrees; either can veto) and a **very strict** bar.
- **Scheduled reviews** after each phase or ~2 months of active work.
- Claude keeps a **prediction scoreboard** (confidence vs outcome) and a **mistakes register**.
- Bad news: **straight, with the why.** Hard no's: **jargon walls, silent gaps, hype, busywork for Ahmed.**
- Hitting a wall: **work around + log it**; ask only if it changes direction or needs Ahmed's action.

**The book (the bible)**
- **MkDocs Material** website on **GitHub Pages**, built from markdown files in `D:\second-sun` (markdown is the master copy).
- ~~Private repo~~ / ~~private work split~~ → **superseded: one public repo; EVERYTHING goes in the book** (phases, batches, candidates, where we left off). Only Ahmed reads it until we publish. Search engines blocked (noindex). Claude flags scooping risk **once**, when the first real candidate appears.
- "A whole book": **chapters + index**, **medium-length chapters**, **English**, tone = **friendly mentor with some bro-to-bro seasoning**, **night-observatory** look, **diagrams + a few interactive demos**, **full gamification** (levels, XP, achievements, sky-coverage map, cool-finds gallery).
- **Offline-capable on iPhone**, added to the home screen.
- **Living book**: updated every session; comeback kit = **2-minute recap + what-changed log + refresher quiz**; **every decision logged with a date**; **journey/story thread**; **fully portable** (any future AI or person can continue from the book + repo alone).
- Learning track **built into the book**, learned **side by side** with the hunt.
- Licenses: **MIT** (code) + **CC BY** (text). Later: a guide others can follow (maybe Urdu).

**Operations**
- Project and data on **D:** (`D:\second-sun`). **Keep raw data.** Downloads over **20 GB** need Ahmed's OK; every download is logged with its size.
- Internet: fast, but **no unnecessary downloads or uploads**.
- **Zero budget.** Accounts: Ahmed creates **all of them** when Claude says so, with the reason and a walkthrough.
- PC can run **overnight often**; jobs must be **resumable**.
- **Phone push alerts** (free service): big finds, batch finished, problems, decisions waiting.
- Git: **auto-push book updates for this repo only** (overrides the usual ask-before-push rule). Commit identity: **M1Smacker** + GitHub no-reply email.
- Usage: **burn the leftover weekly allowance tonight** (parallel sessions allowed), then **one session at a time**. Models **split by task** (cheaper model for routine, strongest for science). Second Sun ranks **below other projects** when usage is tight.
- **Scheduled Claude sessions** allowed, but they **only spend leftover weekly usage near the reset** (never usage Ahmed would use himself).
- Research reports: **short + link** after each wave; Ahmed reads summaries + **3-5 key sources** per wave.
- Candidates get IDs **SS-0001…** plus a nickname once they survive vetting.
- Go public (social, press): **at TOI promotion**, with **full visibility** (name, face, interviews).
- Research **stop rule**: once the chapters needed for Phase 0 and the main-quest gap analysis are solid, hunting starts; other chapters grow alongside.

---

## 3. Research principles (how I research, every wave)

1. **My memory is a lead, not a source.** My training ends June 2026; it is now October 2026. Anything that could have changed (mission status, catalogue versions, tool maintenance, submission rules, fees) gets a live check.
2. **Every citation verified.** A paper only enters the bible after I've fetched it and checked that its ID (arXiv number or DOI) resolves and that the title and authors match. AI tools invent citations; this rule exists to stop me doing it.
3. **Confidence labels** on every claim:
   - **VERIFIED**: read in a primary source (the paper itself, official docs), or proven hands-on.
   - **LIKELY**: secondary source, or primary source read only at abstract level.
   - **UNVERIFIED**: my memory or a single weak source. Never used to make a decision.
4. **Source hierarchy:** official mission/archive docs and refereed papers > arXiv preprints > official tool docs/repos > community forums > blogs/news > my memory.
5. **Measure, don't eyeball** (from your client playbook): data sizes, download times, run speeds, tool compatibility get measured with a script, not estimated.
6. **Narrate friction:** every failed command, workaround or surprise gets one line in the wave report and the log.
7. **No hype words:** "candidate" until promoted; "planet" only after confirmation.
8. **Checkpoint constantly:** findings are written to files as they happen, so a usage limit or crash never loses work.

---

## 4. Where I'll look (source map)

**Literature**
- **arXiv** (free API, no account): preprints of nearly every astronomy paper.
- **NASA ADS** (the astronomy paper search engine): web search now; the API needs **your free account + token** (wave 1 works without it, it just gets better with it).
- **Semantic Scholar** (free API): citation trails ("who cited this search paper?").
- Journals: AJ, ApJ, ApJS, MNRAS, A&A, RNAAS (most are open access now; to verify).

**Data archives and catalogues**
- **MAST** (TESS, Kepler, K2 data), TESS Science Support Center, per-sector data release notes, TESS on AWS open data.
- **ExoFOP-TESS** (TOI + CTOI lists, submission rules), **NASA Exoplanet Archive** (confirmed planets, TOI table).
- **TESS eclipsing binary catalogues** (Prša et al. 2022 and anything newer), Kepler EB catalogue (Villanova).
- **Gaia** archive (DR3 now; DR4 timing to verify), TIC (TESS Input Catalog), SIMBAD, VizieR.
- Ground surveys: **ZTF** (IRSA), **ASAS-SN Sky Patrol**, ATLAS.
- **AAVSO VSX** (variable star index; our side-win route).

**Tools (docs + GitHub repos + release history)**
- lightkurve, astroquery, astropy, wotan, transitleastsquares, astropy BLS, TESScut, eleanor, TGLC, QLP / TESS-SPOC light curves, LATTE, TRICERATOPS, exovetter (to verify), batman, ellc, PHOEBE 2, REBOUND, photodynamical codes, plus any **circumbinary-specific search codes** wave 1 turns up.

**Community and policy**
- Planet Hunters TESS (Zooniverse Talk + its papers), TFOP (TESS Follow-up Observing Program), AAS journal + MNRAS + arXiv **AI-use policies**, arXiv **endorsement** rules, IAU naming rules, ORCID, NASA press-release practice.

**Book tech**
- MkDocs Material (status/successor), offline/PWA options for iPhone, GitHub Pages + Actions, ntfy (or similar free push service), static-site gamification and quiz approaches, interactive plotting in a static site.

---

## 5. The research waves

Each wave = **goal → questions → sources → hands-on proofs → outputs (which book chapters it feeds) → done-when**. Waves 1-4 are the **core** (needed before Phase 0). Waves 5-9 grow alongside the hunt.

### Wave 1: Main-quest gap check *(tonight)*
**Goal:** know exactly who has searched for circumbinary planets, how, where, and what they left untouched.

Questions:
1. **Census:** every known circumbinary planet (transit, radial-velocity, eclipse-timing). For each: host binary, periods, discovery data and method, who found it, year. Which were found by **citizen scientists**?
2. **Every published circumbinary search** in TESS and Kepler: team, method (by-eye, automated, eclipse timing, machine learning), star sample, sectors covered, brightness limit, **detection limits** (what they could and couldn't find), year. Includes Goddard (Kostov et al.), Planet Hunters TESS, BEBOP (Triaud, Martin, Standing), the Kepler CBP team (Orosz, Welsh), Windemuth et al., and **anything from 2024-2026**.
3. **The binary-star supply:** which EB catalogues exist for TESS, which sectors they cover, how many EBs, and how many sectors have arrived **since** the last catalogue and the last search.
4. **Physics we need for the search:** why the transits are irregular, how often they happen given TESS's ~27-day sectors, the stability limit (planets cluster near it), typical periods, transit probability, eclipse-timing detection.
5. **Gap list:** concrete slices with evidence that they're under-searched (e.g. newest sectors, fainter EBs, EBs missing from catalogues, single-transit CBPs, unusual binaries).
6. **Ground-truth set:** known CBPs with TESS data, to test whether our pipeline would have found them (TOI-1338 b, TIC 172900988 b, any Kepler CBPs re-observed by TESS).
7. **Path to "NASA announces it":** how NASA discovery announcements actually happen (who issues them, what it takes), and what that means for us.

Hands-on: none heavy. Maybe one ExoFOP/archive table query to confirm access from Kuwait works.
Outputs: **Main Quest** chapter draft notes, gap list (ranked), ground-truth set, ~20-40 verified claims, key-reads list for Ahmed.
Done when: we can name **at least one specific under-searched slice, with evidence**, or show honestly that there isn't one and what the next-best angle is.

### Wave 2: Data and archives *(core)*
**Goal:** know every data product we'll use, how to get it, and what it costs in disk and time.

Questions:
1. **TESS mission status in 2026** (still operating? extended mission? any budget threat?) and the current sector count.
2. Cameras, pixel size (and why big pixels cause blended-star fakes), cadences over the years (30 → 10 → ~3.3 min full-frame images; 2-min; 20-s), continuous viewing zones.
3. Every light-curve product (SPOC 2-min, TESS-SPOC full-frame, QLP, TGLC, eleanor, CDIPS, others): who makes it, which stars, quality, gaps.
4. Systematics and gotchas: quality flags, momentum dumps, scattered light, sector edges.
5. Access: lightkurve, astroquery, bulk scripts, TESScut, **AWS public bucket** (free?), rate limits.
6. Kepler/K2 overlap and value; **Gaia** (DR3 fields useful to us; **DR4 release timing and what it adds**); ZTF/ASAS-SN for long-term checks.
7. **Data budget:** GB per 1,000 stars per product, for each quest.

Hands-on: download one light curve, one pixel file and one cutout to `D:`; **measure** sizes and times; confirm all caches land on D:, not C:.
Outputs: **Data** chapter notes, data-budget table, download strategy, download ledger started.
Done when: we can say "searching N binaries costs X GB and Y hours", measured, not guessed.

### Wave 3: Methods and tools *(core)*
**Goal:** design the pipeline from proven parts.

Questions:
1. Cleaning light curves (detrending): which methods, and their tradeoffs.
2. **Removing a binary's own eclipses** to expose planet transits: masking vs modelling (ellc, PHOEBE 2, phenomenological).
3. **Circumbinary-specific search algorithms** from the literature (and whether code exists).
4. Standard planet search (BLS, TLS) for the training quest; single-transit search methods.
5. Statistical validation (TRICERATOPS), vetting tools (LATTE, others), centroid analysis, eclipse-timing analysis, photodynamical modelling (for later).
6. Anomaly-detection methods suitable for a 16 GB RAM CPU (for the side quest).
7. **Compatibility matrix:** each tool × Windows × Python 3.12 × last release date × licence × maintained or abandoned.
8. **WSL verdict:** do we need Linux, yes or no, with the reason.

Hands-on (all on D:, Python 3.12 venv): install the core set; **recover a known planet** (e.g. TOI-700 or TOI-1338) end to end; time it per star (→ batch sizes); one **injection-recovery** smoke test.
Outputs: **Pipeline** chapter notes, compatibility matrix, WSL verdict, first proof scripts.
Done when: a known planet is recovered on this PC, and every tool in the design has a verified compatibility row.

### Wave 4: Vetting and false positives *(core)*
**Goal:** know every way a fake looks like a planet, and the test that catches each.

Questions:
1. Catalogue of fakes: eclipsing binaries, blended background binaries, triple stars, stellar variability, spacecraft events, scattered light, and the extra ones specific to circumbinary searches.
2. The tests and thresholds the professionals use (signal-to-noise cut-offs, odd/even, secondary eclipse, centroid shift, Gaia neighbours, false-positive probability).
3. **Our "very strict" bar, in numbers.**
4. Design of the **phone-friendly vetting sheet**.

Outputs: **Vetting** chapter notes, vetting-sheet spec, the numeric submission bar.
Done when: every fake type has a named test and a threshold, each sourced.

> **Stop rule check after wave 4:** if waves 1-4 are solid → build the core bible chapters → Phase 0 starts. Waves 5-9 continue alongside.

### Wave 5: Credit, submission and publishing
Questions:
1. **ExoFOP:** account, CTOI format and fields, requirements, review process, CTOI → TOI promotion, etiquette.
2. **AAVSO VSX:** account and rules for submitting new variable stars; how credit appears.
3. **Publishing:** RNAAS, AJ, MNRAS; **fees** (we have zero budget: are there waivers for independent researchers?); **arXiv endorsement** for first-time and independent authors; **ORCID**.
4. **AI-use policies** of AAS journals, MNRAS and arXiv: exact wording.
5. **Citizen-scientist precedents:** Planet Hunters' first circumbinary planet (PH1 b, 2012, to verify), Wolf Cukier / TOI-1338 b, PHT co-authorship norms.
6. Naming rules (IAU, NameExoWorlds); going public safely at TOI promotion.
7. **Account schedule:** which account, when, why, with a walkthrough.

Outputs: **Credit & Publishing** chapter notes, account schedule.

### Wave 6: Training quest + opportunistic targets
Questions: prior searches for extra planets in known TESS systems (what SPOC's multi-sector search already covers); habitable-zone definitions and which stars have enough TESS coverage; white-dwarf planet searches in TESS (methods, cadence needs, catalogues); ground-truth sets for each.
Outputs: chapters for each quest.

### Wave 7: Side quest, anomalies
Questions: prior anomaly searches in TESS/Kepler; exocomet and disintegrating-planet searches; "dipper" and Tabby's-Star-like objects; which methods suit our hardware; how to triage weirdness into the cool-finds gallery and VSX submissions.
Outputs: **Anomalies** chapter notes.

### Wave 8: Learning track design
Questions: every concept each phase needs (taken from waves 1-4), the order to learn them, a gentle rusty-maths rebuild path, how to read our Python, the best **free** outside resources (checked to exist and be free), quiz bank design, and the demo list (transit-size slider, binary light curve, circumbinary timing animation, phase folding, how a search works).
Outputs: learning-track outline with chapter list.

### Wave 9: Book and infrastructure tech
Questions:
1. **MkDocs Material status** (I have an unverified memory of maintenance mode / a successor project) → pick the engine.
2. Offline + home-screen install on **iPhone** (service worker options; iOS storage rules).
3. Night-observatory theme; interactive demos in a static site; **gamification** (XP, levels, achievements, sky map) on a static site; quizzes.
4. GitHub Pages deploy via Actions; noindex; licence files; repo layout; a repo `CLAUDE.md` so every session loads the rules.
5. **Phone alerts** (ntfy or alternative: free, iPhone support, no account).
6. **Scheduled sessions** mechanics + Windows Task Scheduler for scripts; resumable batch runner; logs; disk monitor.

Hands-on: a tiny local MkDocs build to confirm the engine and theme work on this PC.
Outputs: **How this project runs** chapter notes, infrastructure design.

---

## 6. Schedule and usage

| When | What | Mode |
|---|---|---|
| **Tonight** (now → ~01:00 Kuwait, before the weekly reset) | **Wave 1**, split into 3 parallel sessions: **(a)** census + precedents + NASA-announcement path, **(b)** every published CBP search and its coverage/limits, **(c)** EB catalogues + sector coverage since the last searches. Then I merge them into one gap report. If usage remains: wave 9 Q1 (MkDocs status, a cheap check). | Strongest model; parallel |
| Next weeknight evenings | Waves 2 → 3 → 4 (core), one session at a time | Strongest model for science; cheaper model for formatting/logs |
| After core | **Build the core bible chapters** → Phase 0 starts | |
| Alongside the hunt | Waves 5 → 9, as usage allows; scheduled sessions use leftover usage near each weekly reset | Split by task |

Usage rules: check usage at the start of every wave; checkpoint to files constantly; stop cleanly before a 5-hour limit hits; log what each wave cost (so later estimates are measured, not guessed).

---

## 7. Files the research produces

Created when research starts (after your OK), in `D:\second-sun`:

```
D:\second-sun\
  RESEARCH-PLAN.md          this file
  research\
    wave-1-gap-check\       notes + extracts per sub-topic
    wave-2-data\ ... wave-9-tech\
    claims.md               claim register (claim | source | label | date checked)
    sources.md              bibliography (verified IDs, read depth: full/abstract)
    decisions.md            dated decision log (seeded from section 2)
    mistakes.md             mistakes register (what, cost, rule)
    predictions.md          Claude's prediction scoreboard
    usage-log.md            what each wave cost
    downloads.csv           download ledger (what, size, when, why)
    key-reads.md            3-5 sources per wave for Ahmed
  proofs\                   hands-on test scripts + results
  data\                     downloaded data (never pushed to GitHub)
```

The git repo (public, MIT + CC BY, auto-push) gets created at the start of wave 1. `data\` is git-ignored. **No tokens or keys ever go in the repo** (e.g. your ADS token lives in an environment variable you set yourself).

---

## 8. Accounts (you create; I explain why, when it's time)

| Account | When | Why |
|---|---|---|
| NASA ADS | Wave 1-2 (helpful, not required) | Proper paper search + citation tracking |
| ORCID | Wave 5 | Your permanent researcher ID for papers and submissions |
| ExoFOP | Before the first CTOI | Submitting candidates under your name |
| AAVSO | Before the first VSX submission | New variable stars as side wins |
| Zooniverse (PHT) | Wave 6-7 | Community + checking what volunteers already flagged |
| Push-alert app on iPhone | Wave 9 | Batch and find alerts |
| arXiv | At publishing time | Posting papers (may need an endorsement) |

---

## 9. Leads from my memory that MUST be verified (not facts yet)

- TOI-1338 b: first TESS circumbinary planet, found by 17-year-old intern Wolf Cukier, announced Jan 2020.
- TIC 172900988 b: second TESS circumbinary planet (Kostov et al., ~2021).
- TOI-1338 c / BEBOP-1 c: found by radial velocity (~2023).
- Kepler-16 b: first transiting circumbinary planet (2011).
- PH1 b (Kepler-64 b): first circumbinary planet found by Planet Hunters volunteers (2012).
- Prša et al. 2022: TESS EB catalogue, first two years of TESS, ~4,500 EBs.
- Holman & Wiegert 1999: stability limit for circumbinary orbits.
- A large newer TESS EB catalogue from full-frame images (~2025?): **very unsure.**
- Material for MkDocs entering maintenance mode / a successor ("Zensical"?): **unsure.**
- Gaia DR4 release ~Dec 2026: **unsure.**
- TESS operating status and funding in 2026: **unsure.**
- AAS journals' publication fees and waivers; arXiv endorsement rules: **unsure of current details.**
- iOS home-screen web-app offline storage behaviour; ntfy iPhone support: **unsure.**

---

## 10. Risks to the research, and what we do about them

| Risk | Guard |
|---|---|
| Stale knowledge (my cutoff is June 2026) | Live checks on anything that changes; section 9 list |
| Invented citations | Every citation fetched and matched before it enters the bible |
| Paywalls | arXiv versions; zero budget means no paid access |
| Sites blocking automated access | Workaround + log; ask you only if it needs your account |
| Usage limits mid-wave | Constant checkpoint files; waves sized to fit a window |
| Over-researching (kills the fun) | Stop rule after wave 4; the hunt starts on core chapters |
| Windows-incompatible tools | Compatibility matrix in wave 3; WSL only if proven necessary |
| C: filling up | All caches redirected to D:; disk check in every batch |
| Scooping (public book) | Flag once at the first real candidate; your call then |
| Hype | Label rules; "candidate" until promoted |

---

## 11. What I need from you now

1. **Read this plan** (or skim sections 2, 5 and 6) and tell me if anything is wrong or missing.
2. **Say go**, and I'll start wave 1 tonight as three parallel sessions, then report back short + link.

Nothing else is needed from you until the first account (NASA ADS), and that's optional for wave 1.
