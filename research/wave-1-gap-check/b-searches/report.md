# Wave 1b report: every published circumbinary-planet search, and what each one missed

*Written 2026-10-19 by Claude (Opus 5.5), wave 1b of Second Sun. Research only; nothing built.*
*Every fact below has a row in `claims.md` (B-numbers) with its source and a confidence label. Sources are listed in `sources.md`.*

---

## 1. Plain-words summary (read this first)

**The short version:** only a handful of teams have ever searched TESS data systematically for planets around two stars. Almost all of it was published in the last 7 months, and the biggest search of all is running now and is not published yet.

What has been done, in order of importance to us:

1. **Warwick, April 2026 (Davies et al.)**: the first proper "computer does the searching" hunt in TESS. It covered **512 binaries**, all of them bright stars that NASA had already watched at 2-minute speed in TESS's first two years, and only binaries whose stars orbit each other in **more than 7 days**. Data up to **Sector 79 (June 2024)**. Result: **one weak candidate**, not confirmed. Their code (**mono-cbp**) is free on GitHub.
2. **New Mexico + Tufts, 15 Oct 2026, four days ago (Oddo et al.)**: a search of **1,291 binaries made of two small red stars (M dwarfs)**, Sectors 1-83. **One single-transit candidate.** It is the first measurement of "how common are these planets" from TESS. The answer so far: no more than about **a third** of such binaries host one; for small planets the answer is "we can't tell yet".
3. **Tufts University (David Martin's group, PI Tess Kleanthous)**: the big one. They have had NASA TESS Guest Investigator programmes for this **every year since Cycle 6**, and the current one (Cycle 9) says they are searching **10,000 eclipsing binaries** near the TESS "continuous viewing zone" with their **STANLEY** pipeline. They expect **~25 new planets**. **No results published yet.** STANLEY's code is public (MIT licence) and on PyPI.
4. **NASA Goddard (Veselin Kostov's group)**: found TESS's second circumbinary planet (TIC 172900988 b, 2021) **by eye**, and had Guest Investigator programmes in Cycles 2-4. Their systematic search result was promised as "Kruse et al., in prep" in 2021. **I could not find it published.**
5. **UNSW (Thornton et al., Dec 2025)**: 27 "candidates" found a different way: not from dips, but from the binary's orbit slowly twisting (apsidal precession). A follow-up paper (Aug 2026) already knocked out 2 of the 27. These are **candidates**, not planets.
6. **Kepler era (2012-2021)**: the 12 Kepler circumbinary planets were found **by eye** by the Kepler team (Orosz, Welsh, Doyle and others), plus volunteers for one (Planet Hunters). Automated tools came later (Armstrong 2014, Windemuth 2019, STANLEY 2021). None of the automated Kepler searches found a new confirmed planet, and the full blind STANLEY run on all Kepler binaries (its "Paper II") **has never appeared**.

**Where the gaps are (raw material for the gap list):**

- **Most TESS binaries have never been searched in any published work.** Published searches used 512 bright binaries and 1,291 red-dwarf binaries. NASA Goddard's machine-learning catalogue lists **10,001 checked binaries** and **~900,000 unchecked candidates** from TESS full-frame images. Tufts (10,000 near the CVZ) and Oddo (the 10,001 list, per a Dec 2025 talk title) are working on parts of it, but not on everything.
- **Data after mid-2025 is untouched by any published search.** The last published cut-off is Sector 83. TESS is now at Sector 109 (wave 1c), and Sectors 99-107 were special "rolled" sectors built for long-period planets.
- **Shorter-period binaries (under 7 days) of normal stars** were cut out by the Warwick search. No transiting circumbinary planet is known there, which may be real physics or a blind spot.
- **Single transits from small planets, long shallow transits, and transits of the second (fainter) star** are where every pipeline is weakest by its own admission.
- **Binaries that don't eclipse.** A 2014 paper said planets probably transit them too (if tilted). **I found no search of them, in Kepler or TESS.**
- **Tilted or polar planets.** All transit searches assume the planet's orbit is lined up with the binary's. A 2025 radial-velocity paper reports strong evidence for a polar one.

**What this means for us (my reading, not a finding):** our edge cannot be "the first automated TESS circumbinary search". Warwick and Tufts already own that, and Tufts has the bigger sample and a head start. Realistic angles are: (a) **newer sectors** (84+), (b) **binary samples nobody has claimed** (FFI-only, fainter, non-CVZ, non-M-dwarf, short-period), (c) **signals the pipelines are weak on** (secondary-star transits, two-transits-in-one-conjunction, long shallow events), and (d) **non-eclipsing binaries**. The merge session should weigh these against waves 1a and 1c.

---

## 2. The searches, one table

Abbreviations: EB = eclipsing binary; Re = Earth radii; P_bin = binary period; FFI = full-frame image; SPOC = NASA's 2-min pipeline; TEBC = Prša+2022 TESS EB catalogue (4,584 EBs, 2-min, Sectors 1-26).

### 2a. TESS (2018-2026)

| Search | Paper | Method | Sample | Data / cutoff | Detection limits (own numbers) | Result | Label |
|---|---|---|---|---|---|---|---|
| Davies, Brown, Gill, French (Warwick) | arXiv:2604.09435 (MNRAS 2026) | Automated single-transit search **mono-cbp** (3 points < 3×MAD), wotan detrending, eclipses masked, automated + visual vetting; no ML | 512 detached EBs from TEBC; morph < 0.5; **P_bin > 7 d**; median Tmag ~10.2 | TESS-SPOC FFI LCs binned to 30 min, **≤ Sector 79 (2024-06-18)**; 3,808 LCs | 49,000 injections; efficiency 0.33 at 0.22% depth, 0.47 at 0.46% depth; >50% for Jupiter-size; long shallow transits lost to detrending | 1 candidate event (TIC 319011894, S7), unconfirmed; recovered TOI-1338 b | VERIFIED (B1-B5) |
| Oddo, Dragomir, Martin, Tubthong, Han (UNM/Tufts/MIT) | arXiv:2610.22625 (2026-10-15) | Own single-transit search (SNR ≥ 10, 2-10 h boxes), multi-step wotan detrending, eclipses masked, LEO-vetter, no visual or ML | **1,291 M+M EBs** (their M&M catalogue), T < 15 | **TGLC** FFI LCs, **Sectors 1-83**; 7,422 LCs | >1 M injections (2-16 Re, 10-600 d); sensitivity ≤ ~60%; partial transits (<60% coverage) missed; polar planets missed | 1 planet candidate (TIC 5012780.01, ~15 Re, single transit S22), 4 stellar tertiaries; occurrence < 33% (95%, coplanar, 2-16 Re, 10-600 d); <6 Re unconstrained | VERIFIED (B8-B11) |
| Kostov et al. (NASA GSFC) | TOI-1338: arXiv:2004.07783 | **Visual** inspection of PHT-Talk "#eclipsingbinary" targets (W. Cukier) | Not stated | S1-12 (30-min), S4-12 (2-min) | none stated | TOI-1338 b (95.2 d, ~6.9 Re) | VERIFIED (B39) |
| Kostov et al. (NASA GSFC) | TIC 172900988: arXiv:2105.08614 | **Visual** examination of baselines of EBs from GSFC's neural-network EB catalogue (eleanor FFI LCs) | Not stated | Found in S21 | none stated | TIC 172900988 b; search results promised as "Kruse et al., in prep" (not found) | VERIFIED (B40) |
| Kostov et al. | arXiv:2008.02756 (AJ 160, 174) | **Method paper** (multiple transits in one conjunction → period estimate); proposes visual inspection | Tested on Kepler-16, -34, -35, -1647 | n/a | period estimate within 10-20% for low e; needs double-lined RVs; fails for eccentric (Kepler-34: 0.5-1.7×) | Predicted ~380 TESS CBPs in FFIs, 140 ± 110 with multi-transit conjunctions, 40 ± 32 in CVZs; **no TESS candidates named** | VERIFIED (B38) |
| Thornton, Montet+ (UNSW) | arXiv:2512.07934 (MNRAS 548, 2026) | **Apsidal precession** (eclipse timing), not transits | 1,590 EBs from Gaia DR3 EB candidates | TESS photometry (sectors not read) | mass/separation degenerate | 27 CBP candidates + 6 higher-mass; 2 of them (CH Ind, SW CMa) disputed by Jiang 2026 (arXiv:2608.13269) | LIKELY (B12-B13) |
| Esmer & Daylan | arXiv:2503.20900 | **Eclipse timing variations** | 152 detached EBs | TESS | 0.1% recovery for Jupiter-like planets, 5% for brown dwarfs; min. 1.6 MJup at 1,860 d | 1 substellar candidate (TIC 142979644) | LIKELY (B14) |
| Planet Hunters TESS (Eisner et al.) | arXiv:2011.13944 | Volunteers (>22,000) by eye, all star types | First 26 sectors, 2-min | S1-26 | 85% of TOIs > 4 Re recovered | Not a CBP search, but its EB tags fed TOI-1338 b | LIKELY (B43) |

**Unpublished, in progress (overlap risk):**

| Who | What | Evidence | Label |
|---|---|---|---|
| Tufts: D. Martin (PI Cycles 6-7), T. Kleanthous (PI Cycles 8-9) | STANLEY run on ~10,000 EBs near the TESS CVZ + 204 well-characterised EBs; expects ~25 new CBPs; 2-min targets observed in Sectors 97-108 (30-90 per sector) | GI G06010, G07004, G08058, G09079 (official pages) | VERIFIED that it is funded and planned; results unknown (B26, B27, B54) |
| NASA GSFC: V. Kostov (PI Cycles 2-4) | "Discovering Circumbinary Planets With TESS" via multi-transit conjunctions; search of GSFC EB catalogue | GI G022229, G03195, G04058; "Kruse et al. in prep" (2021) | VERIFIED programme; results not found (B26, B40) |
| UNM: D. Oddo / D. Dragomir | Talk title (Dec 2025): "searching the TESS 10k sample for transiting CBPs" | ESA workshop programme | VERIFIED title; content LIKELY (B42) |
| PLATO (Deeg, Klagyivik) | CBP detection challenge: "Two Stars, One Planet, No Pipeline" | ESA workshop programme | VERIFIED title (B42) |

### 2b. Kepler / K2 / CoRoT / ground

| Search | Paper | Method | Sample | Data | Detection limits | Result | Label |
|---|---|---|---|---|---|---|---|
| Kepler team (Doyle, Welsh, Orosz +) | Kepler-16, 34/35, 47, 38, 413, 453, 1647, 1661, 47 d (2011-2020) | **By eye** | Kepler EB catalogue (~2,900 EBs) | Kepler Q1-17 | not quantified | the 12 Kepler transiting CBPs (PH1 b first spotted by Planet Hunters volunteers, see next row) | LIKELY: "by eye" stated in Windemuth+2019 abstract and in the Tufts GI proposals (B18, B26) |
| Planet Hunters (Schwamb+ 2013) | arXiv:1210.3612 | Volunteers by eye | Kepler Q1-6 | | | PH1 b / Kepler-64 b | LIKELY |
| Kostov+ 2013 | arXiv:1210.3850 | "simple and semi-automated procedure for identifying individual transits" | Kepler EBs | | | independent discovery of KIC 4862625 b (= PH1 b) and Kepler-47 b,c | LIKELY |
| Armstrong+ 2014 | arXiv:1404.5617 | Automated: eclipses removed by phase-fold-subtract, single-event box search, then period folding with TTV-width boxes; 2 human vetters | **1,735** Kepler EBs (morph < 0.7) | Q1-16 long cadence | recovery ~55% (10 Re at 10.2 P_bin) to ~10% (4 Re at 300 d); **P ≤ 320 d, Rp ≥ 4 Re**, coplanar only | Recovered 6 known; missed Kepler-47; candidates KIC 6504534, 5473556, 9632895; occurrence 10.0 (+18/−6.5)% (Rp > 6 Re, P < 300 d, coplanar) | VERIFIED (B21, B37) |
| Windemuth+ 2019 | arXiv:1909.07443 (MNRAS 490, 1313) | Automated: subtract EB model, Δχ² transit statistic, correct TTVs/TDVs with Keplerian model, then **QATS** | method tested only on simulations + Kepler-35, -64 (728 modelled EBs available) | Kepler SAP long cadence | **needs ≥ 3 transits**; circular, edge-on planet; ~5 min per LC; no injection-recovery | No new candidates; thesis (2020) gives occurrence 18 (+7/−5)% for 4-10 Re to ~480 d from 728 EBs (secondary) | VERIFIED (B35); thesis LIKELY (B19) |
| Martin & Fabrycky 2021 (STANLEY I) | arXiv:2101.03186 (AJ 162, 84) | Automated: eclipses cut, cosine + biweight detrending, **N-body (REBOUND) brute-force grid**, stack variable-duration transits | **only the 10 known Kepler CBP systems** | Kepler SAP long cadence, all quarters | coplanar/edge-on, **primary-star transits only**, e ≤ 0.2, **P ≤ 2 yr, ≥ 3 transits**; ~hundreds of CPU hours per target; < 3 Re detectable in half the systems | Recovered all; no new planets; Paper II (blind search) never published | VERIFIED (B20, B36, B53) |
| Klagyivik+ 2017 | arXiv:1610.08471 (A&A 602, A117) | Custom code removes EB light, searches quasi-periodic dips; mainly visual review | **all >2,000 CoRoT EBs** | CoRoT 2007-2012 | lower precision, short baselines | 3 single-pass candidates; no multi-orbit candidates; short-period giant CBPs rarer than around single stars | LIKELY (B23) |
| Ofir 2008; Ofir, Deeg & Lacy 2009 | arXiv:0805.1116; arXiv:0905.3400 | **CB-BLS** algorithm | CoRoT blind tests; TrES ground survey EBs | | noise ≥ 1% OK | method + first real-data runs | LIKELY (B24) |
| CM Draconis ground campaigns (Deeg 2000; Doyle 2000; Jenkins 1996) | refs in Oddo+2026 | matched filter / eclipse minima timing | 1 system | ground | | limits only | ref-level only |
| **K2** | none found | | | | | | LIKELY absence (B52) |

### 2c. Occurrence-rate and bias papers (no new data searched, but they define the limits)

| Paper | Key point | Label |
|---|---|---|
| Martin & Triaud 2014 (arXiv:1404.5360) | Searches only target EBs; tilted CBPs can transit **non-eclipsing** binaries; min. occurrence ~9% | LIKELY (B22) |
| Martin 2017 (arXiv:1611.00526) | Most Kepler CBPs transit < 50% of the time; Kepler EBs likely host **~17-30 more CBPs** that will transit someday (possibly in TESS/PLATO) | LIKELY (B45) |
| Li, Holman & Tao 2016 (arXiv:1608.01768) | Pile-up near stability limit and coplanarity are real, not bias; ETVs better for misaligned / short-binary planets | LIKELY (B46) |
| Mogan & Zanazzi 2024 (arXiv:2412.01616) | None of 14 transiting CBPs orbit P_bin < 7 d; tidal shrinkage could hide them | LIKELY (B47) |
| Baycroft+ 2025 (arXiv:2504.12209) | RV evidence for a **polar** CBP around an eclipsing brown-dwarf pair | LIKELY (B48) |

---

## 3. Algorithms and code (feeds wave 3)

"Plausible on Windows + Python 3.12" is my **judgement from declared dependencies only**. Nothing was installed or run (as instructed). Wave 3 must test.

| Algorithm | Paper | Public code | Language / licence | Last activity | Windows + Py 3.12? | Label |
|---|---|---|---|---|---|---|
| **STANLEY** (N-body grid + variable-duration stacking) | Martin & Fabrycky 2021 | **github.com/TKleanthousT/stanley_cbp**; PyPI `stanley_cbp` 0.2.8 (44 releases) | Python (notebooks); **MIT** | push 2026-10-04; PyPI upload 2026-10-04 | **Plausible, with risk.** `requires-python >= 3.9`; their conda env pins Python 3.9. Depends on `rebound`, `batman-package` (C extensions), `wotan<2`, `lightkurve`, `ldtk`, `PyAstronomy`. Paper says ~hundreds of CPU hours per target and recommends a cluster. | VERIFIED repo facts (B31); Windows = UNVERIFIED |
| **mono-cbp** (single-transit search + vetting) | Davies+2026 | **github.com/bdrdavies/mono-cbp**; PyPI `mono-cbp` 0.1.9 | Python; **GPL-3.0** | push 2026-08-31; PyPI 2026-06-12 | **Plausible, with risk.** `requires-python >= 3.8`, classifiers stop at 3.11; pins **`scipy < 1.13`** (wheels for 3.12 should exist for scipy 1.12, unverified); needs `batman-package` | VERIFIED repo facts (B30); Windows = UNVERIFIED |
| **QATS** (quasi-periodic transit search) | Carter & Agol 2013 | faculty.washington.edu/agol/QATS/ (C++ + IDL, files dated 2016-03-17); used by Windemuth+2019 | C++ (needs `make`); **no licence file seen** | 2016 | **Not directly.** Needs a C++ compiler on Windows (or WSL); no Python wrapper in that folder | VERIFIED listing (B33) |
| **Windemuth+2019 TTV-corrected QATS** | Windemuth+2019 | **none found** (only her EB-modelling code `savvytruffle/keblat`, MIT, last push 2020-05-26, needs GSL) | | | | LIKELY absence (B34) |
| **CB-BLS** | Ofir 2008/2009 | **none found** | | | | LIKELY absence (B34) |
| Armstrong+2014 search | | **none found** | | | | LIKELY absence |
| Klagyivik+2017 CoRoT code ("can be used for … TESS and PLATO") | | **none found** | | | | LIKELY absence (B49) |
| Kostov multi-transit-per-conjunction | Kostov+2020 | analytic formula in paper; no code | | | trivial to reimplement | VERIFIED (paper) |
| Supporting: **LEO-vetter** (used by Oddo+2026) | Kunimoto | github.com/mkunimoto/LEO-Vetter | Jupyter/Python; GPL-3.0 | push 2026-07-29 | likely (pure Python, unverified) | VERIFIED repo facts |
| Supporting: wotan, lightkurve, TGLC, REBOUND, batman | various | public | | | wave 3 matrix | not checked here |

**Machine learning:** I found **no published neural-network detector for circumbinary transits** (B51). ML in this field is used to *find the binaries* (GSFC neural-network EB catalogue; TESS Ten Thousand), not the planets. That is a possible method gap, but an untested one. No training set of real TESS CBP transits exists (only 2 planets).

**Licence note for us:** STANLEY is MIT (fits our MIT plan). mono-cbp is **GPL-3.0**: if we copy its code into our repo, our combined code would have to be GPL. Using it as an installed tool is fine. Flag for wave 3.

---

## 4. Limits summary: what each search could NOT have found (by its own stated limits)

| Search | Sectors after cutoff | Fainter stars | Binaries missing | Single transits | Long periods | Eccentric / misaligned |
|---|---|---|---|---|---|---|
| **Davies+2026** | **S80+** unsearched | No explicit cut, but sample = 2-min primary-mission targets (median T ~10.2) | All FFI-only EBs; **P_bin < 7 d**; morph ≥ 0.5; EBs first seen after S26 | Searched (it *is* a single-transit search) but weak for long shallow transits, and <0.2% deep | Fine for any period (single events), but period then unknown | Masked-eclipse method is geometry-agnostic, but the injection grid is depth/duration only (no period dependence reported) |
| **Oddo+2026** | **S84+** unsearched | T < 15 (good depth) | **Everything except M+M binaries**; parent catalogue built only to S55, so M+M EBs first seen later are missing; biased to short P_bin (median 3.4 d) | Single transits only; partial transits (< 60% covered) missed | Injection range 10-600 d | Polar planets "largely missed" |
| **Tufts STANLEY (unpublished)** | unknown | unknown | Stated: ~10,000 EBs **near the CVZ** + 204 well-characterised (packaged table = 534 EBLM-type F/G+M binaries) → **non-CVZ EBs are outside their stated scope** | Requires ≥ 3 transits (paper I; Kepler-1647 needed relaxing to 2) | P ≤ 2 yr | Coplanar, primary-star only, e ≤ 0.2 |
| **GSFC / Kostov visual (unpublished)** | unknown | eleanor FFI LCs | unknown | by eye: any | any | any (by eye), but human-limited |
| **Kostov+2020 method** | n/a | n/a | only double-lined (SB2) EBs give a period | needs ≥ 2 transits in one conjunction | aimed at long periods | fails for eccentric orbits |
| **Thornton+2025 (apsidal)** | unknown | Gaia DR3 EB sample | only 1,590 EBs; only eccentric binaries show apsidal motion | n/a (not transits) | sensitive to massive / wide companions | **covers misaligned** (that is its point), but stellar-tide systematics |
| **Esmer & Daylan 2025 (ETV)** | unknown | | 152 EBs | n/a | ≥ ~1,000 d | covers misaligned; insensitive to planet masses (0.1% for Jupiters) |
| **Armstrong+2014 (Kepler)** | n/a | no cut | morph ≥ 0.7; active stars under-represented | needs repeated transits (periodicity fold) | **P ≤ 320 d** | coplanar only |
| **Windemuth+2019 (Kepler)** | n/a | | never run blind (method only) | **needs ≥ 3 transits** | P ≤ baseline/3 | circular, edge-on |
| **STANLEY I (Kepler)** | n/a | | **only the 10 known CBP hosts** | ≥ 3 transits | ≤ 2 yr | coplanar, e ≤ 0.2, primary only |
| **Klagyivik+2017 (CoRoT)** | n/a | CoRoT precision | | found 3 single-pass candidates | short CoRoT runs | coplanar limits |
| **All transit searches** | | | **non-eclipsing binaries never searched** (B50) | | | **all assume near-coplanar** |

---

## 5. Raw gap list (for the merge session to rank)

Ranked by my confidence that the slice is genuinely unsearched in *published* work. "Unclaimed" means no published search and no announced programme I found that covers it.

1. **Sectors 84-109+ (Sept 2024 onward).** No published search covers them. Includes the rolled Sectors 99-107 designed for long periods (wave 1c). *Caveat:* Tufts has 2-min data on dozens of EBs in Sectors 97-108 and will search them. **Partly claimed.**
2. **FFI-only EBs that are not M+M and not near the CVZ** (the bulk of TESS Ten Thousand's 10,001 and the ~900,000 unvetted list). *Caveat:* Oddo's Dec 2025 talk title says they are searching "the TESS 10k sample". **Partly claimed; the ~900k unvetted list looks unclaimed.**
3. **Non-eclipsing binaries** (e.g. Gaia DR3 spectroscopic/astrometric binaries). Martin & Triaud 2014 say such planets probably exist; **no search found at all**. Harder (no eclipses to anchor timing; needs known binary orbits). **Unclaimed.**
4. **Transits of the secondary star and two-transits-in-one-conjunction events, searched systematically.** Kostov proposed it (2020, GI Cycles 2-4); no survey result published; STANLEY searches the primary only. **Unclaimed in print.**
5. **Normal-star EBs with P_bin < 7 d.** Cut by Davies; the known population is empty there (the "desert"). A null result is still science (tests Mogan & Zanazzi 2024). **Unclaimed** for non-M-dwarfs.
6. **Small planets (< 6 Re) and long shallow transits.** Every pipeline says it is weak here. This is a sensitivity gap, not a sample gap: beating it needs better detrending, not just more stars.
7. **TESS re-observations of the Kepler EBs**, looking for the ~17-30 extra CBPs Martin 2017 predicts will precess into transit. No search found. Depends on TESS coverage of the Kepler field (wave 1c). **Unclaimed in print.**
8. **ML-based CBP transit detection.** No published attempt. Low priority: no real training set.

---

## 6. Citation trail (who cites the key search papers)

Semantic Scholar citations pulled for Windemuth+2019, Kostov+2020, Martin & Fabrycky 2021, Davies+2026, Kostov+2021, Kostov+2020 (TOI-1338), Klagyivik+2017. Filtered to titles about binaries or circumbinary planets. **Coverage was thin** (e.g. only 2 citers for Kostov+2020; 0 for Davies+2026), so I treat it as partial. Search-relevant citing papers 2022-2026: Esmer & Daylan 2025; Oddo+2025 (M&M catalogue); Kostov+2025 (TESS Ten Thousand; 52 quadruples); Mogan & Zanazzi 2024; Marcadon & Prša 2024 (FFI eclipse timing); Sairam+2023 (RV planet in TIC 172900988); Baycroft+2025 (polar CBP); Gordon+2024 (exomoons of CBPs). The reference lists of Davies+2026 and Oddo+2026 (both read) cite **no other TESS CBP transit search** beyond the ones in this report. That is the strongest evidence I have that this list is complete for published work.

---

## 7. What I did not do, and the confidence limits

- **ADS was not used** (as instructed). ADS would catch AAS conference abstracts and theses that arXiv misses (e.g. a Tufts AAS poster with early STANLEY-TESS results). This is the main way the "unpublished" labels could be wrong.
- Absence claims ("no search found") rest on arXiv abstract searches, GitHub searches and two full reference lists. They are **LIKELY**, not proven.
- Thornton+2025, Esmer & Daylan 2025, Klagyivik+2017, the Ofir papers and the bias papers were read at **abstract level only**.
- The STANLEY paper's last ~60k characters (injection results) and the TOI-1338 / TIC 172900988 papers' later sections were not read.
- No code was installed; "plausible on Windows" is from declared dependencies only.
