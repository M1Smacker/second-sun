# Burn 2: reading (rivals, NASA's search coverage, exocomets)

*Second Sun research, burn 2. Run 2026-10-19, 20:52-21:05 UTC, by a side session (Claude, Opus 5.5). Reading only, no commits. Claims R… in `claims.md`, sources in `sources.md`.*
*Tools: NASA ADS API via `ads_watch.py` (this folder), arXiv PDFs read with `pdftotext`, MAST and NASA NTRS pages, GitHub API. Raw ADS outputs: `ads_run_2025-01-01.txt`, `ads_adhoc_1..5.txt`.*

---

## In plain words (read this first)

**1. Has anyone already done our first campaign (G1)?** G1 means: take the binary stars that the old Kepler telescope found, look at them again in the newer TESS data, and hunt for planets that have only now started crossing their stars.
- **Nobody has published this.** Not in papers, not in conference talks, not in the NASA grant records we searched.
- **But one team is close.** In 2024, David Martin's group (Tufts University, makers of the STANLEY software) got NASA money for a two-year search. They planned to run it on two sets of stars:
  - the same ~3,000 Kepler binaries, but using **Kepler's own old data**, not TESS data;
  - "over 10,000 TESS binaries", using TESS data.

  Nothing from that project has been published yet. If their 10,000 TESS binaries include the Kepler patch of sky, they could overlap with us. That is the biggest risk to G1 and we can't resolve it from public records. (R1, R2)
- **Other near misses:**
  - A NASA team (Mullally et al., 2025) ran an ordinary planet search on the Kepler patch of sky using TESS data. They used the known binaries only as test cases; they did not hunt for planets around them. (R9)
  - A student (Zhang, 2025) searched all Kepler binaries with AI, but in Kepler data, not TESS. (R6)

**2. Who else is racing, and what's new since wave 1?**
- Three new searches turned up that only appear as conference abstracts or grant records (that is why we needed ADS):
  - a Goddard-linked team looked by eye at **over 11,000 TESS binaries** and found 1 candidate (R5);
  - a 2026 survey timed the eclipses of **most TESS binaries in all sectors so far** (R7);
  - a 2022 NASA grant planned to hunt "two dips in one pass", our G4 method, on **300,000 TESS binaries** (R8). No results from that grant appear in ADS.
- **No new two-sun planet was announced in 2026** in any peer-reviewed paper we could find. TESS still has only two. The 2026 news is *candidates*, not planets:
  - 27 candidates from a "wobbling orbit" method (Thornton et al.);
  - 1 candidate around red-dwarf pairs (Oddo et al.). (R10, R11)

**3. Does NASA's own planet search already cover the training quest (hidden siblings around known TOI stars)?**
- NASA's pipeline (SPOC) only flags a planet if it sees **at least two dips** and the signal clears a strength score of **7.1**. (R12, R13)
- Its long, multi-sector searches only cover stars that got the special **2-minute "VIP" pixels**: about 27,000 stars in the northern run. (R14)
- The newest combined searches stop at **Sector 96 (south) and Sector 86 (north)**. Single sectors are searched up to Sector 107. (R15)
- **So there's room for us in four places:**
  - planets that showed only **one** dip;
  - stars that **never got 2-minute data**;
  - **combinations of the newest sectors** that nobody has stacked together yet;
  - **weak signals just under NASA's cut-off**.

**4. The exocomet paper (Norazman et al. 2025), in one paragraph.**
- **What they searched:** comet-shaped dips (a sudden drop, then a slow recovery) in **15.5 million light curves** from TESS's first two years (sectors 1-26), for stars brighter than magnitude 13.
- **What they found:** after many filters, **6 candidates**, one of which is the famous comet star β Pictoris.
- **Their conclusion:** exocomet dips are very rare.
- **Their code is public on GitHub, but it has no licence.** We can read it to learn, but we must not copy it into our MIT-licensed project.
- **The same authors point at our gap themselves:** sectors 27-82 hold about **2.6 million more "star-years"** of data that haven't been searched this way. (R16-R22)

**5. Short notes:**
- β Pictoris: the first comet dips TESS ever saw (2019): three dips, 0.05-0.2% deep, lasting up to 2 days. (R23)
- "Dipper" stars: young stars with dusty discs that blink by 10-50%. These are well studied in TESS (293 dippers catalogued in 2022). That's crowded ground, so it's not a good side quest for us. (R24, R25)

---

## 1. Rivals watch (task 1)

### 1.1 Table: who is searching TESS for circumbinary planets

| Who | Method | Sample | Sectors covered | Status (as of 2026-10-19) | Link | Label |
|---|---|---|---|---|---|---|
| **Davies+ 2026** (Warwick; mono-cbp) | Semi-automated single-transit search | 512 bright EBs (wave 1, B1) | Data to mid-2024 (wave 1) | Published, MNRAS 548 (Jun 2026); 1 weak candidate (wave 1) | [ADS 2026MNRAS.548ag743D](https://ui.adsabs.harvard.edu/abs/2026MNRAS.548ag743D) / arXiv:2604.09435 | VERIFIED (ADS record); sample per wave 1 |
| **Oddo+ 2026** (UNM / Dragomir; with Kostov) | Transit search on M+M EBs; occurrence rate | 1,291 M-dwarf EBs (wave 1) | To S83 (wave 1) | arXiv eprint Oct 2026; earlier AAS 243 abstract (2024) "Towards Transiting Tatooines"; funded by Dragomir FINESST 2022 | [arXiv:2610.22625](https://ui.adsabs.harvard.edu/abs/2026arXiv261022625O), [2024AAS...24344504O](https://ui.adsabs.harvard.edu/abs/2024AAS...24344504O), [2022fine.prop..258D](https://ui.adsabs.harvard.edu/abs/2022fine.prop..258D) | VERIFIED (ADS) |
| **Tufts / Martin (STANLEY)** | STANLEY photodynamical-style search for small CBPs | "almost 3,000 Kepler binaries" (**Kepler data**) + "over 10,000 TESS binaries" | TESS "as of Cycle 7 … ~6-7 years" | NASA XRP 2024, two-year project; **no results paper or abstract found in ADS** (queries on STANLEY, aff:Tufts, author:Martin) | [2024xrp..prop..113M](https://ui.adsabs.harvard.edu/abs/2024xrp..prop..113M) | LIKELY (proposal abstract) |
| **Dunning+ 2025** (EB-catalog team; likely Goddard TESS Ten Thousand) | Visual inspection for CBP transits | ">11,000 surveyed systems", EBs with P > 6 d | Not stated | AAS 245 abstract (Jan 2025); 1 new CBP candidate | [2025AAS...24516010D](https://ui.adsabs.harvard.edu/abs/2025AAS...24516010D) | LIKELY (abstract); team link UNVERIFIED |
| **Goddard / Kostov** | EB / triple / quadruple catalogs | TESS Ten Thousand (VizieR 2026), 52 quadruples (AJ 2026) | FFIs | No new CBP transit paper by Kostov in 2025-2026 (author query, 30 records) | [ADS author query, see ads_adhoc_1.txt] | VERIFIED (query run) |
| **Thornton+ 2025/2026** | Apsidal precession (not transits) | Gaia DR3 EBs with TESS photometry | Not stated in abstract | Published MNRAS 548 (May 2026): 27 CBP candidates; plus Cool Stars talk 2026 (extending to Gaia DR4, RVs) | [2026MNRAS.548ag515T](https://ui.adsabs.harvard.edu/abs/2026MNRAS.548ag515T), [2026csss.confE..77T](https://ui.adsabs.harvard.edu/abs/2026csss.confE..77T) | VERIFIED (ADS) |
| **Esmer+ 2026** (new to us) | Eclipse-timing (ETV) survey for CBPs and brown dwarfs | "a majority of the TESS eclipsing binaries" | "all TESS sectors released to date" | AAS 247 abstract (Jan 2026): >2,000 targets with significant ETV periods | [2026AAS...24713506E](https://ui.adsabs.harvard.edu/abs/2026AAS...24713506E) | LIKELY (abstract) |
| **Haghighipour 2022** (new to us) | **Multiple transits in one conjunction** (= our G4 idea) | "300,000 TESS EBs" | Not stated | NASA XRP 2022 proposal; **no CBP-search results found** in ADS 2023-2026 (his recent papers are dynamics theory) | [2022xrp..prop..190H](https://ui.adsabs.harvard.edu/abs/2022xrp..prop..190H) | LIKELY (proposal) |
| **Zhang 2025** (new to us) | BLS + CNN ("BLSiNet") | Entire Kepler EB catalog (**Kepler data**) | n/a (Kepler) | AAS 246 abstract: 2 strong candidates | [2025AAS...24614414Z](https://ui.adsabs.harvard.edu/abs/2025AAS...24614414Z) | LIKELY (abstract) |
| **Mullally+ 2025** (NASA; new to us) | Plain transit search, cloud (TGLC light curves) | Stars observed by Kepler (Mathur+ 2017) | TESS FFIs | AAS 246 abstract; uses known EBs/KOIs as ground truth, **not a CBP search** | [2025AAS...24633707M](https://ui.adsabs.harvard.edu/abs/2025AAS...24633707M) | LIKELY (abstract) |
| **Grziwa+ 2025** (SINGLETRANS) | Wavelet single-transit search | CoRoT, Kepler, K2, TESS archives | n/a | EPSC 2025 abstract; says it also finds "quasi periodic (… circumbinary planets)" transits | [2025epsc.conf.1460G](https://ui.adsabs.harvard.edu/abs/2025epsc.conf.1460G) | LIKELY (abstract) |

### 1.2 Has anyone searched Kepler-field EBs in TESS data for CBPs (our G1)?

- **No publication or abstract found.**
- **Queries run:**
  - `abs:"Kepler" abs:"eclipsing binar*" abs:"TESS" abs:(circumbinary OR tertiar* OR "third body") year:2023-2026` (0 hits);
  - `abs:("Kepler eclipsing binaries" OR "Kepler field" OR "Kepler binaries") abs:"TESS" abs:"circumbinary"` (25 hits, none a CBP transit search of Kepler EBs in TESS);
  - `abs:"circumbinary" abs:("precession" OR "switch on" OR "transits begin" OR "transitability") abs:"TESS"` (22 hits, none).

  Label: **VERIFIED as "nothing found in ADS"**. That is not proof that nobody is working on it.
- **Closest overlap risk:** the Tufts/Martin XRP 2024 project. Its Kepler part uses Kepler data. Its TESS part is "over 10,000 TESS binaries", which matches the TESS Ten Thousand catalog size. Wave 1 recorded Tufts' TESS sample as CVZ-focused (B). **Whether it includes the Kepler field is unknown.**
- **Related precedent:** KIC 8610483 b (C. Martin+ 2025, AAS 245 abstract). It's a *non-transiting* CBP found by eclipse timing, combining Kepler, TESS and ground data for one Kepler EB. This shows TESS data of Kepler EBs is already used for timing work, one system at a time. (R27, LIKELY)

### 1.3 Circumbinary planet discoveries announced in 2026

- **None found.** I searched refereed 2026 records with "circumbinary planet" plus discovery words in the abstract, and titles containing "circumbinary planet(s)/exoplanet" in 2026. The hits were all theory, candidates or other topics.
- **The 2026 additions are candidates only:**
  - Thornton+ 2026: 27 apsidal-precession candidates;
  - Oddo+ 2026: 1 transit candidate;
  - Esmer+ 2026: ETV periodicities (not claims of planets).
- **Late 2025, for context:**
  - BEBOP-3b, an RV discovery (Baycroft+ 2025, MNRAS 541; ADS record);
  - a circumbinary **brown dwarf** (BEBOP VIII, Triaud+ 2025; ADS record).
- Label: **LIKELY**. ADS indexing lags arXiv by days to weeks, and I did not run an arXiv-only sweep.

### 1.4 `ads_watch.py`

- **What it does:** runs 11 saved queries (rivals' names, circumbinary+TESS, STANLEY, exocomets, Norazman, Kepler-field+TESS), restricted to ADS's astronomy collection, and prints records ADS **added** since a date. It filters on `entdate`, so re-running with the last run date shows only new papers.
- **Usage:**
  ```bash
  python ads_watch.py --since 2026-10-19
  ```
  Options:
  - `--q '<ADS query>'` for ad-hoc queries;
  - `--abstracts` to print abstracts;
  - `--selftest` to run the offline check (passes).
- **Key:** read from the `ADS_DEV_KEY` environment variable only, never printed. In Git Bash, load it with:
  ```bash
  export ADS_DEV_KEY=$(powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('ADS_DEV_KEY','User')" | tr -d '\r\n')
  ```
- **Known weak spots:**
  - `abs:"circumbinary"` also matches circumbinary *discs* (noisy);
  - `entdate` catches re-indexed old records too (some 2019-2022 items appeared), so the broad `abs:"circumbinary" abs:"TESS"` query hits the 50-row cap even for a 3-week window (raise `--rows` or skim);
  - PowerShell 5.1 strips the inner double quotes from `--q` arguments, so run it from Bash (see friction.md).

---

## 2. What NASA's SPOC (and QLP) searches already cover (task 2)

**Source 1: Guerrero+ 2021** (arXiv:2103.12538), sections 5.1-5.2 and 10.6, read in full text (pdftotext).
- **SPOC/TPS:** a TCE needs MES > 7.1, a pass on the transit consistency tests, and **at least two transits**. Kepler's pipeline needed three. (R12)
- **SPOC multi-sector runs** in the prime mission covered S1-2, 1-3, 1-6, 1-9, 1-13 and S14-16, 14-19, 14-23, 14-26.
  - A target enters a later run only if it has sectors not included in an earlier run. (R13)
  - DV can find up to six TCEs per star, by masking each found signal and searching again.
- **QLP** (MIT) stitches **all available sectors** of FFI light curves.
  - It runs BLS from 0.1 d to half the longest baseline.
  - A TCE needs SNR > 9 and BLS peak significance > 9.
  - It re-searches after masking until no peaks are left. (R26)
- **Both pipelines need ≥ 2 transits.** Single transits get into the TOI list only by accident. (R13b)

**Source 2: SPOC Data Release Notes DR113** (multi-sector S14-78; Twicken, Caldwell+; NASA NTRS 20250008654), read in full text. (R14)
- **Input:** **2-minute cadence targets only**. For S14-26 that means DR73 reprocessed 2-min data; for S40-78, the 2-min cotrended light curves.
- **Size:** 27,374 targets searched, 6,631 with TCEs, 12,595 TCEs. The longest period allowed is the 1,769-day baseline, "while requiring at least two transit events".
- **Binning:** the search runs on 10-minute binned "super-cadences".

**Source 3: MAST TCE bulk-download page** (raw HTML grep, 2026-10-19). (R15)
- **Multi-sector ranges published:**
  - S1-2, 1-3, 1-6, 1-9, 1-13, 1-36, 1-39, 1-46, 1-65, 1-69, 1-92, **1-96**;
  - S2-72;
  - S14-16, 14-19, 14-23, 14-26, 14-41, 14-50, 14-55, 14-60, 14-78, **14-86**;
  - S42-43, 42-46.
- **Single-sector TCEs:** up to **S107**.

**Where room is left for the training quest (hidden siblings around TOI hosts):**
1. **Single-transit siblings.** Neither SPOC nor QLP makes TCEs from one transit. A long-period sibling that transited once is exactly what both pipelines skip. *Best fit for us; the same tools serve the circumbinary single-dip hunt.*
2. **Hosts without 2-min data.** SPOC's multi-sector search only sees 2-min targets. Many TOI hosts were found in FFIs (QLP, TESS-SPOC FFI) and are covered only by QLP's stricter SNR > 9 cut.
   - Open question: whether SPOC also runs TPS on TESS-SPOC FFI light curves. I did not verify this (see open-questions).
3. **Newest sectors stacked.** No combined SPOC search covers south S97+ or north S87+. A target observed in S90 and S100 has not had those sectors searched *together* by SPOC.
4. **Sub-threshold signals.** Siblings with MES around 5-7.1 (SPOC) or SNR around 6-9 (QLP), only recoverable by phase-folding with a known host and a targeted search, as for TOI-700 e (wave 6, Q6).
5. **Strong-TTV siblings.** Box-search pipelines lose planets whose transit times wander. (Physics argument, UNVERIFIED for specific systems.)

**Not a gap:** periodic siblings with at least two transits in 2-min data up to S96/S86. NASA has already searched those.

---

## 3. Norazman+ 2025, "A Search for Transiting Exocomets in TESS Sectors 1-26" (task 3)

*arXiv:2508.04673; MNRAS 542, 1486 (2025); Warwick, SETI Institute, NASA Goddard (Kruse). Read in full.*

**Data**
- eleanor-lite 30-min FFI light curves (all stars T < 16) for S1-26, using the PCA flux.
- TESS-SPOC PDCSAP for saturated stars (T < 6.8).
- Sample: **T < 13**, giving **15,477,322 light curves (9,224,280 unique TIC)**.
- Why T < 13: to match Kepler's ~600,000 star-years, and because injection-recovery drops past T = 13.

**Method** (built on Kennedy+ 2019, Kepler)
1. Drop flagged cadences. Make an extra **MAD flag**: per sector and camera, cadences more than 3σ from the median MAD across 2-min targets are cut. This removes scattered-light ramps.
2. Detrend with a **2.5-day sliding median** (wotan). Lomb-Scargle pre-whitening failed on 30-min data: it erased β Pic's comet dip.
3. Find events with the **T-statistic** (moving average over 0.1-2.5 d windows). Keep only the **single most significant dip per light curve**. SNR = −T / σ_T.
4. Fit a **Gaussian and a skewed Gaussian**. Asymmetry ratio α = χ²(sym)/χ²(skew). The skewness sign gives the direction (positive means comet-like).

**Cuts (Table 1 funnel)**

| Step | Remaining |
|---|---|
| Start | 15,477,322 |
| Events that could be fitted | 6,424,883 |
| SNR > 5 | 553,294 |
| Duration > 0.4 d; known TOIs/EBs removed | 184,828 |
| Depth < 1% | 123,819 |
| "Common-time" artefact cut (bins > 10× MAD across 100 bins per sector) | 8,358 |
| Skewness > 0 | 3,515 |
| α > 1.02, skewness < 8, skew error < 50% | 272 |
| Visual vetting (background, centroids, raw flux, other sectors, dilution) | 12 |
| Final | **6** |

**Injection-recovery**
- 20,000 injections per magnitude bin, T = 3 to 15, depths 0.01-1%.
- Real recovery falls sharply below 0.3% depth. At 0.1% depth it drops from about 20% (T = 13) to 10% (T = 14).

**Results**
- β Pic recovered (S6 event, only in TESS-SPOC because of saturation). Its two shallower S5 events were missed: one failed the 0.4-d duration and skewness < 8 cuts, the other failed SNR > 5.
- New candidates:
  - TIC 280832588 (F, T = 12.1, 0.27%, S1);
  - TIC 73149665 (possibly G, T = 11.7, 0.3%, S12);
  - TIC 143152957 (G?, T = 12.86, 0.55%, S7);
  - giant TIC 229790952 (0.25%, S15; 42 sectors, CVZ);
  - probable supergiant TIC 110969638 (0.39%, S7).
- Occurrence rate: 2.64 × 10⁻⁴ per star per year, versus Kepler's 6.7 × 10⁻⁶. Both rest on tiny numbers.
- **Dippers were deliberately excluded** by the < 1% depth cut.

**Code**
- "The code for this project is available on https://github.com/azibn/automated_exocomet_hunt" (paper's Data Availability).
- GitHub API check: repo exists, Jupyter/Python, last push 2026-06-25, **no licence file** (`license: null`). Legally that means read-only for us: no copying into the MIT repo. (R21)

**What a repeat on sectors 27+ would need** (authors' own outlook plus my reading)
- **Data.**
  - eleanor-lite covers the **primary mission only**. The authors had to use QLP and TESS-SPOC for extended sectors.
  - A repeat needs a uniform FFI product for S27+: QLP (T ≲ 13.5) or TESS-SPOC FFI (≤ 160k targets per sector, so not magnitude-complete). Alternatively, build our own (TGLC, eleanor, TESScut).
  - The authors estimate **~2.6 million more star-years in S27-82 to T = 13 on the QLP target list**. (R20)
  - S83-107 is beyond even that.
- **Cadence.** Extended-mission FFIs are 10-min (S27-55) and 200-s (S56+). That means more points per dip, so frequency-based detrending might work again. It also means larger files.
- **Compute and storage.** 15.5 M light curves for 26 sectors already ran at survey scale. Sectors 27-107 is roughly 3× the sectors. A full repeat is not a one-PC job. A **subset is**: for example, only the binaries and TOI hosts we already download for the main quest, or a magnitude/age-selected subset (young A/F stars, debris-disc hosts).
- **Method upgrades they flag:**
  - keep more than one event per light curve (they kept only the strongest, which is why they missed β Pic's smaller dips);
  - a better "common-time" artefact filter (theirs throws away real events);
  - ML/CNN (they are "currently exploring CNNs", so expect a follow-up);
  - Dobrycheva+ 2025 already did a random-forest pass (ADS 2025KosNT..31f..80D).
- **Competition:** the same Warwick, SETI and Goddard group (and Cody's 2020 XRP "hidden occulters" project) is the obvious team to do S27+. An overlap risk exists. (R22, LIKELY)

---

## 4. Short notes (task 4)

**β Pictoris exocomets in TESS: Zieba+ 2019** (A&A 625, L13; arXiv:1903.11071; ADS abstract). (R23, LIKELY)
- They pre-whitened 54 δ Scuti modes over 105 days (S4-7 era, Oct 2018 to Feb 2019).
- They found **three asymmetric dips, 0.5-2 mmag deep, the longest lasting ~2 days**, matching an evaporating comet with a tail. This was the first broadband exocomet detection at β Pic.
- Data: reduced light curve at CDS (J/A+A/625/L13). Notebooks on GitHub (`sebastian-zieba/betaPic_comet`, MIT licence).
- **Lesson:** at β Pic, the comet dips only appear *after* removing the star's pulsations with 2-min data. Norazman's 30-min search missed the two shallower ones.

**Dipper searches in TESS** (ADS abstracts)
- Tajiri+ 2020 (ApJS 251, 18): CNN on year-1 FFIs found **35 dippers**, including old dippers older than 10 Myr. (R25)
- Capistrant+ 2022 (ApJS 263, 14): visual survey of millions of TESS light curves found **293 dippers (234 new)**, mostly younger than 5 Myr, with IR excess. (R24)
- Gaidos+ 2022 (PAST II): an M-dwarf dipper aged 40-60 Myr.
- Cody+ 2025: TESS variability of Herbig Ae/Be stars.
- 2026: "Evidence for a giant companion orbiting Tabby's star" (Madurga-Favieres+ 2026), and "No deep dimming events in Boyajian's star from TESS 2-min, 2019-2022" (Yang+ 2026, RNAAS).
- **Takeaway:** dippers are a mature, well-catalogued TESS topic. A Second Sun dipper side quest would add little. Exocomet-style **shallow** asymmetric dips (< 1%) in S27+ remain the better anomaly gap.

---

## 5. Implications for Second Sun (recommendations, not decisions)

1. **G1 still looks open, with one named risk (Tufts XRP 2024).**
   - Keep G1.
   - Run `ads_watch.py --since <last run>` weekly.
   - The polite question to Tufts (wave 1 idea) is now specific: "does your TESS sample include the Kepler-field EBs?"
2. **G4 (two dips per conjunction) was proposed to NASA in 2022 (Haghighipour)**, with no output found. It's still unclaimed in print, but cite that proposal if we write a method paper.
3. **Training quest:**
   - aim at **single-transit siblings** and **FFI-only TOI hosts**;
   - **do not** spend effort re-folding 2-min TOI hosts for ≥ 2-transit periodic siblings up to S96/S86. NASA has done that.
4. **Anomaly side quest:**
   - an exocomet search on S27+ restricted to stars we already download;
   - keep several events per light curve;
   - borrow Norazman's *ideas* (T-statistic, skew-Gaussian, MAD and common-time cuts), **not their code** (no licence).
