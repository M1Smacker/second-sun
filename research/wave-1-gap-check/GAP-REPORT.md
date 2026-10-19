# Wave 1 gap report: where the unclaimed sky is

*Merged 2026-10-19 by the main Second Sun session from waves 1a (census), 1b (searches) and 1c (catalogues).*
*Claim numbers point to the wave files: **A** = `a-census/claims.md`, **B** = `b-searches/claims.md`, **C** = `c-catalogues/claims.md`.*

**Spot-check:** the main session re-fetched the four most important new papers from the arXiv API, and the IDs, titles, first authors and dates all matched: arXiv:2610.22625 (Oddo+ 2026), 2604.09435 (Davies+ 2026), 2506.05631 (Kostov+ 2025, TESS Ten Thousand), 2512.07934 (Thornton+ 2025). It also checked the STANLEY repo (MIT licence, pushed 2026-10-04) and the mono-cbp repo (GPL-3.0, pushed 2026-08-31) through the GitHub API.

---

## 1. In plain words

**The prize is real.** In 7½ years TESS has found only **two** planets that cross in front of two suns (TOI-1338 b in 2020, TIC 172900988 b in 2021). A 2026 paper still says "to date, TESS has detected two". A **third** would be a "first/record"-type result, and that is exactly the kind of hook NASA press releases are made of. *(A: census; B39-B40)*

**The race has started, but it's small.** Until this year almost nobody searched TESS binaries systematically. Then in 2026:
- **Warwick** searched 512 bright binaries, data up to mid-2024, and found 1 weak candidate.
- **New Mexico + Tufts** searched 1,291 red-dwarf pairs (published four days ago) and found 1 candidate.
- **Tufts University** is running the biggest search now: about 10,000 binaries near the patch of sky TESS watches longest. It's funded by NASA every year since 2023 and **not published yet**. They expect ~25 planets.

So "the first automated TESS search" is already taken. **Our edge has to be the parts of the sky and the data nobody has claimed.** *(B1-B11, B26-B27)*

**The big unclaimed thing is time.** TESS is alive and still collecting: it is shooting Sector 109 right now. But the newest binary-star list stops at **Sector 82 (Sept 2024)**, and no published planet search goes past **Sector 83**. That leaves **26 sectors (about 2 years of data) that no binary list and no published search has touched.** About **8 in 10** of the known binaries have new data in that window. NASA even designed nine of the newest sectors (99-107) specifically to catch long-period planets. *(C1-C8, C27, C37-C40)*

**The other unclaimed thing is faintness.** Most of the binaries found recently are fainter than the brightness limit (magnitude 13.5) where ready-made light curves stop. For those stars in newer sectors, **nobody has even made light curves yet**. Whoever wants them must build them from the raw full-frame images. That barrier is also protection: fewer people will do it. *(C32-C36, C41)*

**Physics tells us how to search.** These planets' dips come at irregular times, last different lengths and sometimes stop for years. In one ~27-day TESS sector you usually see **one dip or none**. So we hunt **single dips**, prefer stars watched for many sectors, and **re-check old stars in new sectors**, because a planet that wasn't crossing before may be crossing now. *(A: physics primer)*

**Precedent for you:** ordinary people have co-discovered two-sun planets twice, PH1 b (2012) and TOI-1338 b (2020). Both times they were co-authors, and NASA covered it, **always through a professional team's paper**. *(A: precedents)*

---

## 2. The gaps, ranked

Ranking weighs four things: **evidence** that it's unsearched, **competition** (who might be on it), **feasibility** for us (beginner + one PC + zero budget), and **payoff**.

| # | Gap | Evidence it's open | Competition | Feasibility for us | Payoff |
|---|---|---|---|---|---|
| **G1** | **Kepler-field binaries re-observed by TESS: "switched-on" planets.** A 2017 paper predicts ~17-30 more circumbinary planets among Kepler's binaries will start crossing their stars at some point (orbit precession). TESS re-observed the Kepler field in Sectors 14-83. | No search found (B45, gap #7: "unclaimed in print", LIKELY); all 10 Kepler CBP hosts have TESS data to S83 (C28-C31, VERIFIED) | None published. The best-placed team (Tufts) states a CVZ-focused sample. | **High**: ~2,900 known binaries with precise Kepler timings (C25), ready-made TESS light curves, and 10 known planets *inside the sample* to prove the pipeline. **Unknown:** how faint/noisy these stars are in TESS (measure in waves 2-3). | "TESS finds the planet Kepler missed". A strong story with a theory prediction behind it. |
| **G2** | **Newest sectors (84-108+) for known binaries outside the CVZ and not red-dwarf pairs.** | ~80% of TESS Ten Thousand binaries have ≥1 new sector; no published search past S83 (C37-C40, B) | **Partly claimed**: Tufts (near-CVZ), and an Oddo/Dragomir talk titled "searching the TESS 10k sample" (scope unknown, B42) | Medium: bright ones (≤13.5) have QLP light curves to S107 and TESS-SPOC to S96 (C33-C35); faint ones need DIY | Biggest sample; highest overlap risk |
| **G3** | **Faint binaries (mag 13.5-15) in sectors after 65.** No ready-made light curves exist. | 63% of TTT's new binaries are this faint (C41); no MAST product covers them after S65 (C32-C36) | Low: the DIY barrier | **Hard**: own photometry from TESScut cutouts; only big planets (Saturn/Jupiter-size) are detectable this faint | Large unclaimed slice; also feeds side wins |
| **G4** | **Method gap: transits of the second (fainter) star, two dips in one conjunction, partial dips**, searched systematically | Proposed by Kostov 2020, never published as a survey; STANLEY searches the primary star only (B38, B20) | Unclaimed in print | Medium: it's a design choice in our pipeline, applied to G1/G2 | Finds what other pipelines are blind to |
| **G5** | **Non-eclipsing binaries** (binaries known from Gaia or spectra that don't eclipse) | A 2014 paper says tilted planets can still cross them; **no search found at all** (B22, B50; LIKELY, needs an ADS check) | Unclaimed | **Hardest**: no eclipses to anchor the timing | Truly novel; a stretch goal |
| **G6** | **The "tight-binary desert"**: normal-star binaries orbiting in under 7 days, where no such planet is known | Warwick cut these out (B1); a 2024 paper says tides could hide planets there (B47) | Unclaimed for non-red-dwarf pairs | Medium | Even a **null result is publishable**: a rung for the "method paper" fallback |
| **G7** | **TESS Ten Thousand's ~873,000 unchecked binary candidates.** Cross-match with Gaia's eclipsing-binary list to confirm new binaries | No vetting effort found (C open question 10) | Unclaimed as far as found | High for small batches | **New variable stars → AAVSO VSX side wins**, plus fresh samples for G2/G3 |

**Not worth our time now:** machine-learning planet detection (no training set: there are only 2 TESS examples; B51). Eclipse-timing-only searches (TESS alone catches 0.1% of Jupiter-mass planets this way; A, B14).

---

## 3. Recommendation

**First campaign: G1, the Kepler field "switched-on" hunt**, with **G4 built into the pipeline from day one** and **G7 as the side-wins stream**. Reasons:
- **Best evidence of an open gap** with a published theory prediction behind it (a reason to expect planets, not just hope).
- **Small, well-defined sample** (~2,900 binaries) that fits one PC and a beginner's learning curve.
- **Built-in proof:** the 10 known Kepler planets are in the sample, so our search proves itself on real targets before we trust any new find.
- **Low overlap risk** right now.
- **Biggest unknown:** whether TESS's precision on these mostly faint stars is good enough. **Wave 2/3 measure this first.** If it isn't good enough, we switch the first campaign to **G2 (bright end)** and keep G1 for the bright subset.

**Second campaign:** G2 (non-CVZ, non-red-dwarf, newest sectors), then G3 as our photometry skills grow. **G5/G6 are stretch goals.**

**Warm-up targets (training quest, before the main campaign):**
1. **TOI-1338 b in Sectors 97-98 (Sept 2025 to Jan 2026).** Its chance of crossing after Sept 2025 was ≲30% per pass. Was one caught? Nobody has published on it. A perfect first hands-on exercise (C open question 8; A).
2. **TIC 319011894** (the Warwick single-dip candidate), re-observed in **Sector 87**, which nobody has published on (C open question 9).
3. **The 10 Kepler hosts + TIC 172900988**: recover their known transits in TESS data (C28-C31).

**Code to start from (to test in wave 3):** STANLEY (Tufts, **MIT** licence, maintained) and mono-cbp (Warwick, **GPL-3.0**, so use it as an installed tool and never copy its code into our MIT repo). Neither is proven on Windows + Python 3.12 yet (B30-B31).

---

## 4. The NASA path, applied to us

Every NASA announcement found came **after a professional-led paper was at least submitted**, with a NASA-linked scientist on the team and a "first/record" hook (A: NASA path). For Second Sun that means:

**find a candidate → submit it as a CTOI → hand it to an active circumbinary team** (Goddard/Kostov, BEBOP, or Tufts/Martin) **→ follow-up observations → joint paper with Ahmed as co-author → NASA coverage if a NASA team is on it.**

A third TESS transiting circumbinary planet clears the "first/record" bar. Open (wave 5): **can a single-dip circumbinary candidate even be submitted as a CTOI**, when the form expects a period?

---

## 5. What we still don't know (and how to find out)

| Unknown | Why it matters | How to resolve |
|---|---|---|
| What exactly Tufts' STANLEY TESS search covers, and when it publishes | Overlap with G2 (and maybe G1) | **ADS** conference-abstract search (needs your free ADS account); possibly a polite email later (Claude drafts, you send) |
| Scope of Oddo/Dragomir's "TESS 10k sample" search | Could shrink G2 | Same as above |
| Goddard's promised "Kruse et al., in prep" (2021) | Possible hidden overlap | ADS |
| Is there really no search of non-eclipsing binaries? | G5's novelty | ADS full-text search |
| TESS precision on Kepler-field binaries | Whether G1 is feasible | Waves 2-3, measured |
| TESS's funding for 2027 | Data flow (old data stays public regardless) | Re-check periodically |
| TIC 172900988 b's period (189-204 d by transits vs a 150-d planet by radial velocity) | Ground-truth accuracy | Wave 3 reading |
| CTOI rules for single-transit circumbinary candidates | Our submission route | Wave 5 |

**This is the reason to create your NASA ADS account soon:** three of these unknowns (Tufts, Oddo, Goddard) probably show up only as conference abstracts, which ADS indexes and arXiv doesn't.

---

## 6. Key reads for Ahmed (wave 1)

1. **NASA Goddard, "NASA's TESS Mission Uncovers Its 1st World With Two Stars"** (2020): the TOI-1338 b story, with the 17-year-old intern and the volunteers. <https://www.nasa.gov/universe/nasas-tess-mission-uncovers-its-1st-world-with-two-stars/>
2. **NASA JPL, "Citizens Discover Four-Star Planet with NASA's Kepler"** (2012): how two volunteers became co-discoverers of PH1 b. <https://jpl.nasa.gov/news/news.php?release=2012-324>
3. **Martin (2018), "Populations of planets in multiple star systems"**, read the introduction only: the best overview of why two-sun planets behave the way they do. <https://arxiv.org/abs/1802.08693>
4. **Davies et al. (2026)**, read the introduction: the current state of the race, from the team that just did it. <https://arxiv.org/abs/2604.09435>
