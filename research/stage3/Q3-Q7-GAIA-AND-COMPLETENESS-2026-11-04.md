# RS-010 Q3 (Gaia counts) and Q7 (what limits completeness) (night of 4 Nov 2026; research stint RS-011; report only, nothing changed)

Scripts and raw outputs in `research/stage3/census_step1/`: `q3_gaia_counts.py` and `q3-gaia-counts.txt`; `q7_completeness.py` and `q7-completeness.txt`.

## Q3: how many Gaia DR3 eclipsing-binary candidates are bright and slow?
Source: the public Gaia archive TAP service, read-only ADQL counts on `gaiadr3.vari_eclipsing_binary` joined to `gaiadr3.gaia_source` (Mowlavi et al. 2023 sample; no rows downloaded, only counts; nothing stored but the counts). The first attempt, a join over all 2.2 million rows, timed out; the second restricted the join to the long-period subset first and answered in seconds.

**Plain verdict: a few thousand bright long-period candidates, a real but modest extra pool; the Gaia period for a long-period binary is the weak part.**

| period | all magnitudes | Gaia G < 13 | G < 14 | G < 15 |
|---|---|---|---|---|
| over 7 d | 137,637 | 2,709 | 5,503 | 10,206 |
| over 10 d | 96,591 | 1,831 | 3,767 | 7,016 |
| over 20 d | 41,319 | 777 | 1,528 | 2,889 |
| over 40 d | 10,726 | 311 | 550 | 1,063 |

- CONFIRMED (archive counts): total candidates 2,184,477, as in the paper's abstract.
- Gaia G 14 is about TESS magnitude 13.5 for a Sun-like star (the colour term is not applied here, LIKELY). So **about 5,500 Gaia candidates with P over 7 days and in our brightness range**, against the 2,056 stars we have searched in all three hunts. Not cross-matched with TESS coverage or with our searched lists (NOT TESTED; most of the sky has been observed in at least one sector, but how many have 2-minute data or usable FFI light curves is open).
- NOT TESTED / UNCERTAIN: how many are detached (the model type was not queried), how many are real EBs rather than other variables (Mowlavi report a completeness of 25 to 50% against OGLE and contamination from the candidates' classification; abstract read), and how right the Gaia periods are for long-period systems (the Gaia sampling is sparse; for periods of tens of days an eclipse is seen only a few times).
- Use for Census: Gaia is a list of places to look first, not a list of confirmed binaries. A cheap first filter (period and brightness from Gaia, then a short check with TESS light) would turn it into a ranked list. The 5,500 would add to the post-sector-26 pool of Step 1 (about 1,000 G2-type stars, estimated), and the two overlap by an unknown amount.

## Q7: why is the TOI-1338 b-size dip found so rarely, and what would raise it?
Own data: the planted dips of the G3 completeness run (6,024 positive dips on 251 star-sectors with a prepared product, `data/chain_recovery_g3/rows_g3.pkl`). K is the planted depth divided by the 8 h box noise of that star-sector.

**Plain verdict: the lever is brightness (noise), with a second ceiling from our own checks that no brightness can lift.**

| K (depth over noise) | seen | kept in tier 1 | kept given seen |
|---|---|---|---|
| 6 to 8 | 8% | 4% | 47% |
| 8 to 10 | 28% | 14% | 51% |
| 10 to 12 | 62% | 32% | 52% |
| 12 to 14 | 85% | 45% | 53% |
| 14 to 18 | 95% | 51% | 54% |
| over 18 | 99% | 53% | 54% |

- **CONFIRMED (our data):** the kept share rises with K and then flattens at about 53%. Roughly **half of every dip that the search sees is thrown out by the safety checks, whatever its depth** (kept given seen 47% to 54% at every K). Among seen-but-lost planted dips with K 8 to 14, the checks that fired were: step 53%, gap-dump 28%, ramp 21%, dominated 21%, orbit check c5 14%, eclipse overlap 12%, repeater 7% (a dip can carry several). This agrees with fix and build items T34 (step check) and T35.
- **TOI-1338 b-size (2,300 ppm as seen)** against G3's median 8 h noise of about 570 ppm gives K = 4, below the planted range (6 and up), hence the roughly 6% reported. To reach K = 12 to 14 (kept 45%) the noise would have to be about 180 ppm, three times lower: with the slope fitted on G3 (log10 noise grows 0.211 per magnitude, Q2) that is **about 2.3 magnitudes brighter**, Tmag near 10.5 instead of about 13. In the Tmag-binned table in `q7-completeness.txt` the brightest dips reach 41% kept, the faintest 8%, but that binned table mixes brightness with depth (planted depth is K times noise), so use the K table above, not the bins.
- **Product:** at K 8 to 14 the kept share is 29% for QLP and 42% to 44% for SPOC and TESS-SPOC (n 2,640 against 372). So bright stars with 2-minute light would keep a dip more often than QLP light of the same noise (LIKELY: the QLP products lose more to the step, ramp and gap checks; cause NOT tested).
- **Box length:** the 8 h and 14 h boxes keep the most (38% and 36% at K 8 to 14), the 20 h box the least (21%).

**What would raise completeness (options, for Ahmed; nothing done):**
1. Brighter stars (Census already ranks by value, now with the measured lever: every magnitude brighter is worth about 0.2 in log noise).
2. Review the checks that cost half of every seen dip (T34 step check first, then ramp and dominated). A planted dip is easier than a wandering real one, so some of the cost is probably deserved; the price is not yet separated from the benefit for real data (the false-alarm line S2 is already over its mark, so loosening needs care).
3. Prefer 2-minute SPOC light over QLP where both exist.
4. None of these touches the sensitivity ceiling set by transit geometry (Q1 update).

## Labels
CONFIRMED: Gaia counts, K table, flag shares (our data). LIKELY: Gaia G 14 about TESS 13.5; SPOC versus QLP difference caused by checks. UNCERTAIN: how many Gaia candidates are real detached EBs. NOT TESTED: cross-match of Gaia with TESS products and with our searched lists; effect of loosening any check on false alarms.
