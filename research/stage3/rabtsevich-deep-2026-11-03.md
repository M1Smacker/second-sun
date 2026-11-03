# Rabtsevich, deep pass (RS-007, 3 Nov 2026, Ahmed's request; G3 stays paused)

Method: `research/RESEARCH-BLUEPRINT.md`. Second pass on top of `rabtsevich-literature-2026-10-30.md` (that pass did not open his Note, his data and code record, his preregistration or his later papers). Pages opened in the browser pane (HTML only); his PDFs and ZIP were fetched with Python into `data/rabtsevich_zenodo/` (all logged in `research/downloads.csv`, about 7.7 MB in total, text extracted with pdftotext). Cap 3 weekly points, written before the start; the 5-hour meter was the tighter limit (82% at the start).

## Questions and the decision each feeds
1. What exactly did he do, step by step? Decides which of his steps we lack.
2. What tips and workflow did he give openly? Decides how we use the AI agents ourselves.
3. What is different from Vesper and our lead rules? Decides what goes in the build queue.
4. How firm is the candidate, and where does it stand? Decides how we describe it to Ahmed and in the book.
5. Which of his tests can we run on our own data now? Decides whether anything is cheap enough to do before G3.

## Our own house first (files read, 3 Nov)
- `research/stage3/LEADS-RULES.md`: verdict sentences are chosen by rule from the numbers (no free text); a control column shows real against upside-down; "seen in another sector" is a count only; the pixel check is "NOT BUILT"; the known-host test uses only `toi.csv` and `cbp.csv`. CONFIRMED (file read).
- `research/stage3/BUILD-QUEUE.md`: T46 (by-eye record) and T47 (crowding note from headers, real pixel check later) exist; no task for a follow-up protocol, a second independent implementation, a number audit or a wider novelty check. CONFIRMED (grep for pixel, TRICERATOPS, novelty, DDT).
- A grep of `pipeline/` for package-version recording (pip freeze, `__version__`, requirements) found nothing; `requirements.txt` exists at the top level. So I found no place where a frozen run records the library versions. LIKELY (grep only; not every file was read).

## Q1. What he did (CONFIRMED unless marked)
Source: his Research Note, text extracted from https://zenodo.org/records/22967456 (116 KB PDF), and his reproducibility README, https://zenodo.org/records/22999133 (v1.0.1; v1.0.0 is https://zenodo.org/records/22967099).
- **Search:** Sector 98 QLP light curves of 126,246 stars (T up to 11.5), box least squares, then the LEO-Vetter flux tests. The two signals passed every flux test but their multiple-event statistics (10.6 and 11.0) were **below the shortlist threshold of 15**, so he examined them "post hoc". He says so in the Note. The search itself is not deposited (only a recount and a LEO-Vetter re-run for this star).
- **Cross-sector test:** the Sector 98 period alone (rule written into the script before it ran) was used to look for the signal in Sectors 6 and 32. The fixed-epoch version found nothing because the predicted timing was off by 18 to 25 hours, far more than the 1.87 h transit. So he searched epoch and period inside the 3 sigma prediction ellipse, and built the null with 20,000 fake periods through **identical machinery with the true transits removed**. Observed signal never exceeded by the null (0 of 20,000).
- **He then refused to trust 0 of 20,000:** neighbouring fake periods are correlated, so the bound is (k+1)/(N_eff+1) with N_eff the number of independent trials. His own heuristic gave N_eff 164 (Sector 6); a review pass measured it (autocorrelation time and declustered exceedances) as 77 to 140; the printed claim was widened from "<0.7% per sector, <0.03% jointly" to "about 1% per sector, about 0.1% jointly". The README also says this is not the false-alarm rate of the original 126,246-star search, which was "not re-assessed". Source: `data/rabtsevich_zenodo/v1.0.0/part1/03_archival_test_A/README.md`.
- **Timing and shape:** 23 per-transit times with injection-calibrated errors, 19 used in the ephemeris fit; odd/even and phase 0.5 depths; V-shape test; emcee fit. P = 3.182785 +/- 0.000006 d, depth about 500 ppm, 1.4 +/- 0.1 Earth radii if on the target.
- **Where the dip comes from:** difference images fitted with the TESS pixel response function, offset (+5, 0) +/- 3 arcseconds; all Gaia stars able to make the depth are more than 43 arcseconds away; Gaia RUWE 1.21 and radial-velocity scatter elevated but under the thresholds; an overluminosity test limits an unresolved companion to below about 0.38 solar masses; TRICERATOPS FPP 0.03 to 0.04 (above the 0.015 validation line), "so I claim no validation". Sector 6 difference images were unusable because **the transits lie 0.4 to 3.5 hours from momentum dumps**.
- **Novelty:** "As of 2026 September 25 (UTC), I found no prior report in ExoFOP, TCE tables, the NASA Exoplanet Archive, candidate catalogs, SIMBAD, VizieR, ADS, or arXiv." A dated sentence with a list of places.
- **Package:** 1,888 files, 41.7 MB, `SHA256SUMS` for every file; an input list with MAST product, retrieval time, bytes and sha256 per file; a table `FINAL_FACTS.csv` plus `NOTE_NUMBER_MAP.csv` that maps **every number printed in the Note to a file and a key**, with an automatic coverage check; a `SUPERSEDED.md` listing old values and why they were replaced; the three Python environments frozen.
- **Preregistration for the new data** (https://zenodo.org/records/23175179, deposited 6 Oct 2026, before Sector 110 began): period, 9 and 3 predicted transit times known to about 4 minutes, expected depths (442 +/- 52 and 586 +/- 137 ppm), the processing, and **four outcomes**: recovered, inconsistent, excluded, insufficient. "Excluded" needs the mean depth below threshold, below the allowed range **and sensitivity of at least 95%**; "insufficient" is never evidence against. The noise is measured in the same light curve by placing the same windows at fake times; the threshold is the 99.9th percentile. The first valid run that writes an output file defines the result and is posted before the variants run. Frozen code refuses to start in another environment. The whole thing was reproduced from a fresh copy with freshly downloaded files before deposit. The README states plainly that the false-detection rate was about 0.47% and 0.49% in archival tests, not the nominal 0.1%.
- **His later papers (CONFIRMED, PDFs read):** an 18.15-day candidate around L 279-94 (20 Oct) found by looking for stars that dip once in each of two sectors, with a cross-star shuffle null ("almost as many pairs appeared as in the real data"), a funnel (163 kept, 40 looked at by eye, 8 clean, 7 removed by image checks), two transits predicted before looking, and a note that Planet Hunters volunteers had marked both 2020 dips (found after his search); and a 252-day Kepler candidate KOI-5005.01 (30 Oct) where he reports that in 16 of 34 upside-down copies dips are as strong as the real ones, so "not established". His upside-down control is the same idea as ours.

## Q2. Tips and workflow
- **Not read:** his X thread (logged-out view shows only the first post, 1.2M views) and his r/ClaudeAI post (Reddit is blocked in our browser pane for safety). I did not work around either. His own account is therefore read from what he deposited and signed: the AI disclosures.
- **CONFIRMED (his disclosures):** he chose the target and the questions, "requiring re-checks with separate code and explicit caveats"; Claude wrote and ran most code; **OpenAI Codex wrote and ran separate analyses of the same data**; one recalculation found a script error; review passes found a missed transit and a TRICERATOPS error; "Agreement between AI tools was not treated as confirmation"; he personally inspected every light curve shown. Sources: https://zenodo.org/records/22967456 (Note), `data/rabtsevich_zenodo/later/` (two papers).
- **LIKELY (secondary):** two weeks, 74 analyses, more than 1,000 scripts, 36 catalogues, 340,505 TESS alerts checked for prior detection; restarted from zero (new code, re-downloaded data, 364 values recomputed one by one) with the same result; blind prediction of each of three years from the other two (journaldugeek, 11 Oct; explainx, 9 Oct; a third-party gist). The count of 74 and the list of the tests are his figures; I did not find an itemised list (UNCERTAIN).
- **NOT TESTED:** whether the v1.0.0 step reports hold his workflow remarks (he removed "tool-workflow remarks" in v1.0.1); I counted keyword hits in 10 files and read none of them.

## Q3. What differs from us (gap table)
| Practice | He | We | Verdict |
|---|---|---|---|
| Search discipline | candidate chosen post hoc below a shortlist threshold, then tested on new data | frozen settings, sealed slice, one-shot | we are stronger at the search; he is stronger after it |
| Future-data test | public, hashed preregistration; on-demand new data through a TESS DDT | Vigil designed, not built (T120) | same idea; Vigil is our version |
| Follow-up outcomes | four outcomes, "excluded" needs sensitivity of at least 95%, first valid run counts, fixed sentences | fixed verdict sentences for a run only | **we lack the follow-up protocol** |
| Cross-sector test | epoch search plus identical-machinery null plus measured N_eff | "seen in another sector" is a count | **we lack the null** |
| Second implementation | separate code by a different model, agreement not counted as proof | zero-difference tests (same code line), review passes | **we lack independent code** |
| Number audit | every printed number mapped to a file and key, automatic coverage check | claim labels in `claims.csv` | **we lack the map** (today's F-028 error is the kind it catches) |
| Novelty check | ExoFOP, TCE, Archive, SIMBAD, VizieR, ADS, arXiv, Planet Hunters, dated UTC | TOI and known-circumbinary lists only | **we lack the wider check** |
| Pixel localisation | difference images with the pixel response function | not built (T47 note only) | known gap, queued |
| Run environment | frozen, refuses another environment, hashes for every file | code and data fingerprints | **library versions not recorded** (LIKELY) |
| Control with upside-down copies | yes, reports counts | yes | same |
| Honest status | "what I cannot say" section, "no validation claimed" | labels | same |

## Q4. How firm is it (labels)
- **CONFIRMED:** a candidate, not validated (Note); TRICERATOPS FPP 0.03 to 0.04 is above the 0.015 line; found post hoc below the shortlist; Sector 6 transits sit near momentum dumps; TESS DDT program 100 (PI Rabtsevich) is on the official list https://tess.mit.edu/science/ddt/ and Sector 110 runs 31 Oct to 26 Nov 2026; no result exists before 26 Nov (a search on 3 Nov found none).
- **LIKELY (30 Oct note, Scientific American quoting a TESS-team member):** professional filters had already flagged it; so "nobody knew" is too strong.
- So "very strong candidate" says more than the sources do. It is a plausible candidate, and its strength will rest on the November data.
- The DDT list also holds programs 101 (L 198-93 and TYC 9078-80-1) and 102 (TIC 458191673) for planet candidates by other people, and a preregistration of a TOI-913 candidate by another author (Zenodo 23290795). Whether those used AI is NOT CHECKED. What is clear (CONFIRMED) is that the practice is spreading.
- **DDT route, CONFIRMED from the official page:** proposals can be sent at any time, about six weeks before the sector starts (two weeks in special cases), by email with a template; up to 500 two-minute targets per sector; reviewed by the TESS PI, an expert and operations; no proprietary period; renewed every year.

## Q5. Own data
Nothing of his can be run on our data before G3 without a lead to run it on. The one thing we can check now is the N_eff issue: whether our scorecard treats clustered upside-down and real events as independent when it quotes a null. NOT TESTED; queued as T129.

## What changes (queue, not built; the three-week rule holds)
- **T125 Lead follow-up protocol:** a template extending `LEADS-RULES.md`: four outcomes, a power rule for "excluded", first valid run counts, fixed sentences, a public hashed deposit before the new data. Written before any lead exists. Cost about 0.5.
- **T126 Second independent implementation:** for any lead that reaches Candidate, a different model writes separate code for the final checks; agreement is not counted as confirmation. Cost per lead.
- **T127 Wider novelty check:** extend lead stage 4 beyond TOI and circumbinary lists (ExoFOP CTOI, TCE tables, Exoplanet Archive, SIMBAD, VizieR, ADS, arXiv, Planet Hunters), with a dated UTC sentence. Cost about 0.3.
- **T128 Run environment record:** write the library versions and hashes into every frozen run's settings (and a refusal when they differ). For G3 the cheapest form is `pip freeze` saved into the run folder at the start; that touches only `g3_go.ps1`, not the 11 fingerprinted files, but G3 is frozen, so it needs Ahmed's yes. Cost about 0.2.
- **T129 N_eff check of our null counts** (small audit) and **T130 number-to-file audit** for published results with an automatic coverage check. Cost about 0.3 and about 1.5.
- Not new: pixel localisation stays T47; Vigil stays T120 and is the same idea as his Sector 110 test.
- A DDT request is available only for a lead with two keys, and needs about six weeks of lead time; recorded in `LEADS-RULES.md` follow-up (T125).

## Open (said plainly)
Reddit post and X thread unread; the list of his 74 analyses not found; whether v1.0.0 step reports hold workflow remarks not read; Sector 110 result due after 26 Nov (T60 stays); whether DDT 101 and 102 or the TOI-913 author used AI not checked; the grep for library-version recording is a grep only.
