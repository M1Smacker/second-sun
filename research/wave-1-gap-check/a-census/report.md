# Wave 1a report: census, citizen-science precedents, physics, NASA path

*Second Sun research, wave 1a. Written 2026-10-19 by Claude (Claude Code, Opus 5.5). Research only. Every number here is in `claims.md` with its source and label; the bibliography is `sources.md`.*

---

## Part 1: Plain words (read this first)

**How many "two-sun" planets are known?** It depends on what you count, and that is the first lesson.

- **The solid core is small: 14 planets that we have actually seen crossing in front of their two stars.** 12 came from NASA's old Kepler telescope (2011 to 2020 papers) and only **2 from TESS**: TOI-1338 b (announced 2020) and TIC 172900988 b (2021). A paper posted in April 2026 still says "to date, TESS has detected two." I found no third one, in NASA's archive or in the news.
- Add a few more found by the "wobble" method (radial velocity), which measures the stars being tugged: TOI-1338 c (2023), BEBOP-3 b (2025), and Kepler-16 b measured again. One found by eclipse timing around a normal binary (Kepler-1660 AB b, 2023).
- NASA's archive flags **53** planets as circumbinary, but that list also includes giant planets imaged hundreds of times farther out, a few microlensing events, and about a dozen "planets" inferred from timing wobbles in dead-star binaries. **Many of those timing planets are doubtful**: when one team re-checked seven of these systems, 30-plus planet models failed to predict the next eclipses within a year.

**Who found them?** Mostly two professional groups: the Kepler circumbinary team (Doyle, Welsh, Orosz and colleagues) and Veselin Kostov's group (now at NASA Goddard). Then the BEBOP team (Triaud, Standing, Baycroft) with the wobble method.

**Have ordinary people found one? Yes, twice.**
- **PH1 b (2012)**: two volunteers on the Planet Hunters website, Kian Jek and Robert Gagliano, spotted it by eye in public Kepler data. Both are **co-authors** on the discovery paper, and **NASA's JPL put out a press release the same day** as Yale.
- **TOI-1338 b (2020)**: an Italian volunteer, Giuseppe Pappa, flagged the star as an eclipsing binary on Planet Hunters TESS; then **Wolf Cukier, a 17-year-old summer intern at NASA Goddard**, noticed an extra dip "at the wrong time". Cukier and six volunteers are co-authors, NASA Goddard issued the press release, and NASA even has a profile page for Pappa.

**Why are these planets hard to find?** Around one star, a planet's dips come like a metronome, so computers just stack them. Around two stars, the stars are themselves moving, so each dip comes **early or late by up to days**, lasts a different time (one of TOI-1338 b's dips lasted twice as long as another), and can have a different depth (it may cross either star). Worse, the planet's orbit slowly **wobbles like a spinning top**, so for years at a time it simply stops crossing the stars. TOI-1338 b crosses only about 30% of the time.

**Where do these planets live?** Almost all of them sit **just outside the danger zone** close to the two stars, where orbits get thrown out. That edge is about 2.5 to 3.5 times the stars' separation; the planets we know sit just beyond it, with years about 5 to 7 times the stars' own orbit. None is known around binaries that orbit each other faster than ~7 days, even though those binaries are common. Nobody is sure why.

**What does this mean for TESS?** TESS stares at each patch of sky for about a month. A two-sun planet's "year" is usually 50 to 300 days, so in one month you usually see **one dip, or none**. Sometimes you get lucky and see two dips a few days apart (one on each star), as with TIC 172900988 b. So our search must look for **single dips**, not repeating ones, and stars watched for many sectors are the best hunting ground.

**How does NASA "announce" a discovery?** In every case I checked (PH1 b, Kepler-90i, TOI-1338 b, TOI-700 d), NASA's press office wrote about it only once a **professional-led paper had been written and submitted to a journal**, usually timed with a big American Astronomical Society meeting, and always involving NASA data and a NASA-linked scientist. Citizen finds do get NASA coverage, but **as part of a team paper**. Realistic route for Ahmed: find → submit a community candidate → a professional team follows it up → joint refereed paper with Ahmed as co-author → NASA coverage if it's notable. A "first" (for example the third TESS two-sun planet ever) is the kind of thing that gets a NASA headline.

**Big caution:** recent teams (2025 to 2026) are actively searching TESS binaries with new tools: one found 27 *candidates* through binary wobble (not confirmed), others ran single-dip searches and found one candidate each. The field is busier than it was in 2021. Sessions 1b and 1c cover exactly what they searched.

---

## Part 2: Census (technical)

### 2.1 Transiting circumbinary planets (14, the secure core)

Columns as requested. Binary/planet values from the discovery abstracts (and Davies et al. 2026 Table 2 for binary periods); planet radius/mass from the NASA Exoplanet Archive composite table unless noted. "≤" marks values that the discovery paper gives as an upper limit even though the archive shows them as a mass.

| Planet | Host binary: P_bin, stars | Planet P (d) | R (R_E) / M (M_E) | Method | Data | Discovery paper | Found by | Year | Citizen scientists? |
|---|---|---|---|---|---|---|---|---|---|
| Kepler-16 b | 41.08 d; 0.69 + 0.20 M_sun (low-mass pair) | 228.8 | 8.45 / 106 | Transit | Kepler | arXiv:1109.3432 (Doyle+ 2011, Science) | Kepler team | 2011 | No |
| Kepler-34 b | 27.80 d; two Sun-like stars | 288.8 | 8.56 / 70 | Transit | Kepler | arXiv:1204.3955 (Welsh+ 2012, Nature) | Kepler CBP team | 2011 (pub. 2012) | No |
| Kepler-35 b | 20.73 d; 0.89 + 0.81 M_sun | 131.5 | 8.16 / 40 | Transit | Kepler | arXiv:1204.3955 | Kepler CBP team | 2011 (pub. 2012) | No |
| Kepler-38 b | 18.80 d; evolved 0.95 + 0.25 M_sun, e=0.10 | 105.6 | 4.30 / ≤122 | Transit | Kepler | arXiv:1208.3712 (Orosz+ 2012) | Kepler CBP team | 2012 | No |
| Kepler-47 b | 7.45 d; Sun-like + ~1/3-size companion | 49.5 | 3.05 / 2.1 | Transit | Kepler | arXiv:1208.5489 (Orosz+ 2012, Science) | Kepler CBP team (also found independently by Kostov+ 2013) | 2012 | No |
| Kepler-47 c | same | 303.2 | 4.65 / 3.2 | Transit | Kepler | arXiv:1208.5489 | same | 2012 | No |
| Kepler-47 d | same | 187.4 | 7.04 / 19 | Transit | Kepler | arXiv:1904.07255 (Orosz+ 2019) | Kepler CBP team | 2019 | No |
| PH1 b (Kepler-64 b) | 20.0 d; F dwarf 1.53 + M dwarf 0.41 M_sun; quadruple system | 138.3 | 6.18 / ≤169 | Transit | Kepler | arXiv:1210.3612 (Schwamb+ 2013) | **Planet Hunters volunteers** (Jek, Gagliano); independently Kostov+ (arXiv:1210.3850) | 2012 | **Yes** (2 volunteer co-authors) |
| Kepler-413 b | 10.12 d; K 0.82 + M 0.54 M_sun | 66.3 | 4.35 / 67 | Transit | Kepler | arXiv:1401.7275 (Kostov+ 2014) | Kostov et al. | 2014 | No |
| Kepler-453 b (KIC 9632895 b) | 27.32 d; 0.93 + 0.19 M_sun | 240.5 | 6.20 / ≤16 (1σ) | Transit | Kepler | arXiv:1409.1605 (Welsh+ 2015) | Kepler CBP team | 2014 (pub. 2015) | No |
| Kepler-1647 b | 11.26 d; two ~solar-mass stars, e=0.16 | 1107.6 | 11.87 / 483 (1.52 M_J) | Transit (+ eclipse timing for mass) | Kepler | arXiv:1512.00189 (Kostov+ 2016) | Kostov, Orosz, Welsh et al. | 2016 | No |
| Kepler-1661 b | 28.16 d; 0.84 + 0.26 M_sun, grazing EB | 175.1 | 3.87 / 17 | Transit | Kepler | arXiv:2001.02840 (Socia+ 2020) | Kepler CBP team (SDSU) | 2020 | No |
| TOI-1338 b | 14.61 d; F-type ~1.1 M_sun (Teff 6050 K) + M dwarf ~0.3 M_sun, e=0.16 | 95.2 | 6.85 (paper) / 7.66 (archive) ; 33±20 M_E (paper) / 11.3 (archive) | Transit | TESS (2-min, Sectors 6 and 10; FFI Sector 3) | arXiv:2004.07783 (Kostov+ 2020) | Goddard team; **flagged by PHT volunteer Pappa, spotted by intern Wolf Cukier** | 2020 | **Yes** (6 volunteer co-authors + high-school intern) |
| TIC 172900988 b | 19.70 d; 1.24 + 1.20 M_sun, e=0.45 | 188.8 to 204.1 (six solutions; archive 200.45) | 11.25 / 824 to 981 | Transit | TESS FFI, Sector 21 (one sector) | arXiv:2105.08614 (Kostov+ 2021) | Kostov group (visual search of GSFC TESS EB catalog) | 2021 | Amateur (AAVSO) observers did follow-up photometry and are co-authors; discovery itself by the professional team |

**Note on TIC 172900988 b:** a 2023 radial-velocity paper (Sairam et al., arXiv:2310.07527) detects a circumbinary planet in this system with a **150-day** period, "different than previously proposed". I did not read further than the abstract; this conflict is unresolved here (open question).

**Note on TOI-1338 b numbers:** the archive's composite row uses a later solution (7.66 R_E, 11.3 M_E) than the discovery paper (6.85 R_E, 33±20 M_E). A 2024 photodynamical paper calls it "a puffy planet" (arXiv:2404.18415, title only). Show both, prefer the newer once read.

### 2.2 Radial-velocity and main-sequence eclipse-timing detections

| Planet | Host binary | Planet P (d) | Mass | Method | Data | Discovery paper | Found by | Year | Citizen? |
|---|---|---|---|---|---|---|---|---|---|
| TOI-1338 c (BEBOP-1 c) | as TOI-1338 | 215.5 | 65.2 M_E (paper); 75.4 (archive) | RV (first CBP by RV alone) | HARPS + ESPRESSO (ground) | arXiv:2301.10794 (Standing+ 2023, Nat. Astron.) | BEBOP | 2023 | No |
| BEBOP-3 b | eclipsing binary (period not read) | 550 (archive 547) | 0.56 M_J (m sin i) | RV (first RV detection of a previously unknown CB system) | SOPHIE (ground) | arXiv:2506.14615 (Baycroft+ 2025) | BEBOP | 2025 | No |
| BEBOP-4 (AB) b | 72 d; 1.51 + 0.46 M_sun, e=0.27 | ~1800 | m sin i 20.9 M_J, < 26.3 M_J | RV | SOPHIE | arXiv:2510.25329 (Triaud+ 2025) | BEBOP | 2025 | No; **the authors call it a brown dwarf**, the archive lists it as a planet |
| Kepler-1660 AB b | 18.6 d | 239.5 | 4.87 M_J | Eclipse timing + depth variations + RV | Kepler + ground RV | arXiv:2308.09255 (Goldberg+ 2023) confirming an ETV signal first reported by Borkovits+ 2016 (not read) | Goldberg, Fabrycky, Martin et al. | 2023 | No |
| Kepler-16 b (re-detection) | as above | 228.8 | mass measured by RV | RV | SOPHIE | arXiv:2112.06584 (Triaud+ 2022) | BEBOP | 2022 | No |

### 2.3 Eclipse-timing "planets" around evolved / post-common-envelope binaries (disputed class)

From the archive (`cb_flag=1`, method "Eclipse Timing Variations"): DP Leo b (2009), NN Ser c, d (2010), UZ For b, c (2011), HU Aqr b, c (2011), NY Vir b (2011), c (2019), RR Cae b (2012), Kepler-451 b (= 2MASS J19383260+4603591 b, 2015), c, d (2022), MXB 1658-298 b (X-ray binary, 2017), DE CVn b (2018), NSVS 14256825 b (2019). Plus PSR B1620-26 b (pulsar timing, 2003).

Status: treat as **contested**. Pulley et al. 2022 (arXiv:2206.06919): of 30+ planetary models for seven such systems, all but the latest NY Vir model failed within a year. Martin 2018: ~90% of these binaries show timing variations, unlikely to all be planets. Kepler-451's configuration was re-analysed again in 2025 (arXiv:2606.26817: one planet at 3.4 AU supported, others uncertain). The archive does **not** list HW Vir's proposed planets at all.

### 2.4 Imaged and microlensing circumbinary planets (different regime, listed for completeness)

Imaging (wide, tens to thousands of AU; young systems): Ross 458 c, SR 12 AB c, ROXs 42 B b, 2MASS J0103 AB b (Delorme 1 AB b), VHS 1256 b, HD 284149 AB b, 2MASS J0249 c, HIP 79098 AB b, b Cen AB b, WISPIT 1 b, c (2025), HD 143811 AB b (2025, 6.1 M_J at ~60 AU, arXiv:2509.06009). Microlensing: OGLE-2007-BLG-349L AB c, OGLE-2016-BLG-0613L AB b, OGLE-2018-BLG-1700L b, OGLE-2019-BLG-1470L AB c, OGLE-2023-BLG-0836L b, KMT-2016-BLG-1337L b (2026). None of these is reachable by our TESS method.

### 2.5 Notable candidates (not planets)

| Candidate | What | Source | Status |
|---|---|---|---|
| 2M1510 (AB) b | polar-orbit planet around eclipsing brown-dwarf pair, inferred from retrograde apsidal precession (RV) | arXiv:2504.12209 (Sci. Adv. 2025) | "strong evidence"; not in archive |
| BEBOP-3 c | ~1400-d outer signal | arXiv:2506.14615 | candidate |
| 27 TESS apsidal-precession candidates (+6 higher-mass) | excess precession in 1,590 Gaia DR3 EBs with TESS data | arXiv:2512.07934 (Thornton+ 2025; MNRAS per 2026 press) | candidates; mass/separation degenerate |
| TIC 142979644 | ETV companion, ~11 to 19 M_J (brown-dwarf range) | arXiv:2503.20900 (Esmer & Daylan 2025) | candidate |
| TIC 319011894 | single ~0.2%-deep transit-like event in Sector 7 | arXiv:2604.09435 (Davies+ 2026) | candidate event; stellar scenarios not excluded |
| (unnamed in abstract) | one planet-sized single-transit candidate around an M+M TESS EB | arXiv:2610.22625 (Oddo+ 2026, 4 days old) | candidate |
| HW Vir planets | ETV planets in a post-common-envelope binary | arXiv:2309.05716 (title) | disputed; absent from archive |

### 2.6 Why the counts disagree

16 known CBPs (Baycroft 2025, transit + RV), 14 transiting (Mogan & Zanazzi 2024; Davies 2026), 31 circumbinary systems (Thebault & Bonanni 2025), "60 confirmed or candidate systems" incl. brown dwarfs (Esmer & Daylan 2025), 53 flagged planets (archive). Recommendation for the book: **lead with 14 transiting + 3 RV/ETV planets around normal binaries (TOI-1338 c, Kepler-1660 AB b, BEBOP-3 b) = 17 secure planets**, then list the rest with labels. Reason: those are the ones whose detection we could reproduce and the ones every recent paper counts. Cross-check: Baycroft et al. (April 2025, before BEBOP-3 b) count 16, which is exactly 14 + TOI-1338 c + Kepler-1660 AB b.

---

## Part 3: Citizen-science precedents

| Case | Who did what | Credit given | Announcement |
|---|---|---|---|
| **PH1 b** (Kepler, 2012) | Volunteers Kian Jek (San Francisco) and Robert Gagliano (Cottonwood, AZ) spotted transits by eye on Planet Hunters; Yale's Meg Schwamb led confirmation with Keck | Both volunteers **co-authors** (20-author paper); planet informally "dubbed PH1"; named in Yale's release | Yale + **NASA JPL** releases 2012-10-15; paper submitted to ApJ; AAS DPS meeting, Reno |
| **TOI-1338 b** (TESS, 2020) | PHT volunteer "Pappa" (Giuseppe Pappa, Catania) flagged the EB; Goddard team inspected PHT-tagged EBs; 2019 summer intern Wolf Cukier (Scarsdale High School) saw the off-time dip | Cukier 5th author; **6 PHT volunteers co-authors**; Cukier named in NASA release; NASA citizen-scientist profile page for Pappa | **NASA Goddard** release 2020-01-07, AAS 235 Honolulu panel; paper "submitted" |
| TIC 172900988 b (TESS, 2021) | Professional visual search; AAVSO amateurs did ground follow-up | Amateur observers co-authors | (No NASA release found in this wave) |
| Non-circumbinary comparisons | HD 152843 (PHT, 2021), TOI-2180 b (Visual Survey Group, Tom Jacobs, 2022), TOI-4633 c (15 PHT volunteers, 2024) | Volunteers co-authors (HD 152843: Cesar Rubio and >12 others); VSG has co-authored >68 papers | NASA Goddard feature; AAS press event; NASA "Discovery Alert" |

What I did **not** find: any planet officially named after a citizen discoverer, or any case where a lone amateur was the lead author of a circumbinary discovery paper. Every precedent went through a professional team.

---

## Part 4: Physics primer for designing the search

### 4.1 Plain words

1. **Wobbly timing.** The two stars circle each other. The planet crosses whichever star is in the way, wherever that star happens to be. So the dips are irregular: TOI-1338 b's gaps were 93 then 95 days, and theory says the drift "may be on the order of days". Normal planet-search software assumes a perfect beat and fails.
2. **Wobbly length and depth.** If the star is moving the same way as the planet, the crossing is long; if opposite, short (TOI-1338 b: 0.3 vs 0.6 days). Crossing the smaller star gives a shallower or deeper dip than crossing the big one.
3. **On-off seasons.** The planet's orbit tilts back and forth over decades (precession). For years it crosses the stars, then for years it misses: Kepler-453 b crosses only ~8% of the time, Kepler-1661 b ~7%, TOI-1338 b ~30%. Upside: given enough time, a two-sun planet is *more* likely to cross its stars than a one-sun planet at the same distance.
4. **The danger line.** Too close to two stars and the planet gets flung out. The safe edge is ~2.5 to 3.5 times the stars' separation (Holman & Wiegert 1999). Real planets crowd right next to it, at 1.3 to 1.6 times the edge's orbital period. So **planet year ≈ 5 to 7 × the stars' orbit** for the innermost planet (Kepler-47 b: 49.5 d around 7.45 d; TOI-1338 b: 95 d around 14.6 d).
5. **The tight-binary desert.** None known around binaries faster than ~7 days. Ideas: a third star squeezed those binaries tight and wrecked their planets on the way; or the planets exist but are tilted or far out, so they don't cross.
6. **Timing the eclipses (ETV).** A planet tugs the pair around, so eclipses come a bit early or late. For planets near the stars this is tiny (TOI-1338 c: ~0.05 s by light-delay alone). TESS alone mostly catches brown dwarfs this way.
7. **TESS's month.** One sector ≈ one month, planet years ≈ 50 to 1100 days → usually 0 or 1 dip per sector, occasionally 2 a few days apart at one "conjunction". Stars watched for many sectors are the gold.

### 4.2 Technical

- **Stability limit (VERIFIED, HW99 Eq. 3):** a_c/a_b = 1.60 + 5.10e − 2.22e² + 4.12μ − 4.27eμ − 5.09μ² + 4.61e²μ², μ = m2/(m1+m2), test particles, 10⁴ binary periods, 0 ≤ e ≤ 0.7, 0.1 ≤ μ ≤ 0.5. Unstable islands at n:1 resonances (3:1 to 9:1) just outside a_c.
- **Pile-up (derived from HW99 + discovery parameters; script below):**

  | System | μ | a_c/a_b | P_c/P_b | P_p/P_b | P_p/P_c |
  |---|---|---|---|---|---|
  | Kepler-38 | 0.208 | 2.65 | 4.31 | 5.62 | 1.30 |
  | Kepler-413 | 0.398 | 2.56 | 4.09 | 6.55 | 1.60 |
  | Kepler-1661 | 0.236 | 2.72 | 4.48 | 6.22 | 1.39 |
  | TOI-1338 b | 0.214 | 2.87 | 4.86 | 6.52 | 1.34 |
  | TOI-1338 c | 0.214 | 2.87 | 4.86 | 14.75 | 3.04 |
  | Kepler-1647 | ~0.5 | 2.83 | 4.77 | 98.4 | 20.6 |
  | TIC 172900988 | 0.493 | 3.52 | 6.60 | 9.58 | 1.45 |

  Caveats: HW99 is a test-particle fit; Kepler-1647 masses approximated as equal; TIC 172900988 uses its shortest allowed period. Literature: the pile-up is physical, not a selection bias (Martin & Triaud 2014; Li, Holman & Tao 2016, "eight of the nine").
- **Transit timing/duration:** TTV amplitude ~ (T_p T_bin²)^(1/3)/(2π) (Martin 2018 citing Agol+ 2005), days, ≫ transit duration (hours) → no phase folding; all Kepler CBPs found by eye. Automated alternatives: STANLEY (Martin & Fabrycky 2021, N-body-guided stacking; recovered all Kepler CBPs), mono-cbp (Davies+ 2026, single-event search with eclipse removal, ≥50% recovery per known planet), Oddo+ 2026 single-transit algorithm. (Session 1b covers these in depth.)
- **Transit probability:** probability of "transitability" (orbits overlap on sky at some time) is always ≥ the single-star value and weakly dependent on P_p; e.g. a 1 AU planet around a 0.3 AU EB eventually transits with certainty if mutual inclination > 0.6° (Martin & Triaud 2015). But the *instantaneous* fraction is set by precession: Kepler-453 b ~8% (precession ~103 yr), Kepler-1661 b ~7% (35 yr), TOI-1338 b 29.7% (nodal 21.4 yr; two ~1000-d windows per cycle), Kepler-413 b long gaps (precession ~11 yr).
- **Mutual inclination bias:** all known transiting CBPs have mutual inclination < 4.5° (Goldberg+ 2023); "it is not a selection bias that the planetary and stellar orbits are nearly coplanar (≲3°)" (Li+ 2016).
- **Occurrence:** ~10% for R > 6 R_E, P < 300 d if coplanar (Armstrong+ 2014), comparable to single stars; minimum ~9% (Martin & Triaud 2014); first TESS limit: < 33% (95%) for 2 to 16 R_E, P < 600 d around M+M EBs (Oddo+ 2026).
- **Tight-binary desert:** no transiting CBP around P_bin < 7 d, Kepler EB median 2.8 d; ≥2× more planets expected otherwise (Martin & Triaud 2014; Armstrong+ 2014). Explanations: Kozai-Lidov + tidal friction from a tertiary (Martin, Mazeh & Fabrycky 2015; Muñoz & Lai 2015); tidal shrinkage (Mogan & Zanazzi 2024); resonance-advection instability in multi-planet systems (Liu & Lai 2026).
- **Eclipse timing:** light-travel-time half-amplitude = a_p · m_p/(M_bin + m_p) · sin i / c. Derived values: TOI-1338 c 0.055 s; 1 M_J at 1 yr around 1.5 M_sun 0.36 s; 5 M_J at 10 yr 8.4 s. Dynamical (non-Keplerian) ETVs dominate for close-in massive planets (Kepler-1660 AB b). TESS-only ETV sensitivity: 0.1% recovery for Jupiters, 5% for brown dwarfs, minimum 1.6 M_J at 1860 d (Esmer & Daylan 2025). PCEB ETV "planets" unreliable (Pulley+ 2022). Apsidal precession is the newer route (Baycroft+ 2023; Thornton+ 2025), with tidal systematics (Jiang 2026).
- **TESS implication:** a sector is ~27 days (e.g. Sector 21 = 2020-01-21 to 02-18). With P_p ≥ 49 d (known minimum) and typically 5 to 7 P_bin, a single sector holds ≤ 1 conjunction; at a conjunction, 2+ transits within days are common and give P_p to within 10 to 20% for low-e orbits (Kostov+ 2020b), which predicted "hundreds" of such TESS candidates. Reality check: TESS still has 2 transiting CBPs (Davies+ 2026, April 2026). Precession means a system that showed no transits in early sectors can show them in new sectors (and vice versa): TOI-1338 b's transit probability falls to ≲30% after 2025-09-12 per the discovery paper, while NASA's release simplified this to "cease after November 2023 and resume eight years later".

### 4.3 Script used for the derived numbers

`hw99.py` (run with `py -3.12 -I`, stdlib only; kept in the session scratchpad, reproduced here so the numbers are checkable):

```python
def acrit(e, mu):  # Holman & Wiegert 1999, Eq. 3
    return 1.60 + 5.10*e - 2.22*e**2 + 4.12*mu - 4.27*e*mu - 5.09*mu**2 + 4.61*e**2*mu**2
# P_c/P_b = acrit**1.5 (Kepler III, same total mass); P_p/P_c = (P_p/P_b) / (P_c/P_b)
AU_s = 499.004784  # light travel time over 1 AU, s
def ltte(mp_msun, Mbin, P_days):  # edge-on half-amplitude, s
    a = ((Mbin+mp_msun)*(P_days/365.25)**2)**(1/3)
    return a*mp_msun/(Mbin+mp_msun)*AU_s
```

---

## Part 5: The NASA announcement path

| Discovery | Issued by | Date | Team | Stage at announcement |
|---|---|---|---|---|
| PH1 b | NASA JPL (plus Yale) | 2012-10-15 | Yale-led (Schwamb, Fischer) + volunteers | Paper submitted to ApJ; presented at AAS DPS meeting |
| Kepler-90i | NASA HQ release 17-098 (contacts HQ + Ames) | 2017-12-14 | Shallue (Google) + Vanderburg (NASA Sagan Fellow, UT Austin) | Paper **accepted** in AJ; statistically validated |
| TOI-1338 b | NASA Goddard | 2020-01-07 (AAS 235 panel 01-06) | Goddard-led (Kostov) + SDSU, U. Chicago, SETI, volunteers, intern | Paper **submitted**; transits confirmed with eleanor; archival RVs |
| TOI-700 d | NASA Goddard | 2020-01-07 (AAS 235) | Gilbert (U. Chicago) / Rodriguez (CfA) / TESS team; high-school student Alton Spencer found the star misclassification | **Three papers submitted**; Spitzer confirmation transit |

**What it realistically takes (synthesis; my inference from the four cases plus the citizen-science features):**
1. NASA mission data (Kepler, TESS, Spitzer). TESS qualifies.
2. A professional-led, refereed paper, at least submitted. No release I found was for an unpublished candidate.
3. A NASA-linked scientist on the team (Goddard, Ames, a NASA fellow) or a NASA-funded program; the release is written by a NASA center's communications office (Goddard for TESS).
4. A hook: "first" or "record" (first TESS circumbinary planet; first TESS habitable-zone Earth; record-tying 8 planets; first citizen-science circumbinary planet), often timed with an AAS meeting.
5. Credit for citizens comes as co-authorship and naming in the release text, plus NASA profile pages. Lighter coverage (Goddard features, "Discovery Alerts") exists for less headline-worthy citizen finds, again after a paper.

**For Second Sun:** a third TESS transiting circumbinary planet would clear the "first/record" bar (TESS has two as of April 2026). The route that worked twice: candidate found by a volunteer → handed to a professional team (Kostov's Goddard group and BEBOP are the active CBP teams) → follow-up (RV, more transits) → paper with the volunteer as co-author → NASA Goddard release if the team includes Goddard. Session 5 (credit/publishing) should check the CTOI → TOI route and whether a CBP single-transit candidate can even be submitted as a CTOI.

---

## Part 6: What this hands to the gap report (for the main session)

- TESS transiting CBP yield (2) is far below the 2020 prediction of "hundreds" of multi-transit candidates. Whether this is a search gap, a follow-up bottleneck, or a physics/occurrence effect is the key gap question (sessions 1b/1c).
- 2025 to 2026 searches exist and are recent: Davies+ 2026 (Prša 2022 catalogue, 512 detached EBs with P > 7 d, data through Sector 79), Oddo+ 2026 (M+M EBs), Thornton+ 2025 (1,590 Gaia DR3 EBs, apsidal), Esmer & Daylan 2025 (152 EBs, ETV). Their **samples** (2-min catalogue EBs; detached P > 7 d) suggest the FFI-only EBs and post-Sector-79 data are less searched; session 1c must confirm with numbers.
- Physics says: search per-event (single dips), prioritise long-baseline stars, expect P_p ≈ 5 to 7 P_bin for the innermost planet, and re-search old targets in new sectors because precession switches transits on.
- Ground-truth set candidates for wave 3: TOI-1338 b (Sectors 3, 6, 10), TIC 172900988 b (Sector 21); Kepler CBPs re-observed by TESS (not checked here).
