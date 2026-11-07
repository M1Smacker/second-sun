# Second Sun: outside review and honest odds (7 Nov 2026)

*Written by Claude (claude.ai, Opus 5.5) from the public repo at commit c525918 (6 Nov 2026) plus web checks. Report only: nothing in the repo was changed. Labels follow the project rule: CONFIRMED (I ran it or read the primary source), LIKELY, UNCERTAIN, NOT TESTED. My scripts are listed at the end so Claude Code can re-run them.*

## 1. The verdict in plain words

The science discipline in this project is genuinely better than most amateur work and some professional work: frozen versions, upside-down noise controls, planted-dip completeness, preregistration, an outside audit that found real issues, and a mistakes log that is actually used. That part does not need changing.

Two things I found change the Census plan, and one changes the odds you have been told. The rest are smaller.

## 2. Findings, most important first

### F1. A public list of 10,531 eclipsing binaries from 2-minute data, sectors 1 to 88, already exists and was filed as "method only" (CONFIRMED)

The CALNet paper (arXiv:2504.15875) was read on 4 Nov as "a neural network for EBs, method" (`research/stage3/CENSUS-STEP2-RESEARCH-2026-11-04.md`, line 13). Its paper gives no table, but its GitHub repository does: `github.com/wangleon/CALNet`, MIT licence, file `outputs/newecl.dat`. I downloaded it (1.26 MB, into a scratch folder, not into the repo) and checked it:

| Check | Result |
|---|---|
| Rows | 10,531, all unique TIC IDs |
| Columns | TIC, coordinates, HIP, Tycho, 2MASS, **Gaia DR3 source ID**, V and G magnitudes. **No period.** |
| Brightness | median G 11.7; 8,277 brighter than G 13.5; 5,973 brighter than G 12 |
| Overlap with our hunts | G1 51, G2 0, G3 20. **10,460 have never been searched by us.** |

Why this matters: Census stage 2 currently plans to find eclipsing binaries in post-sector-26 data ourselves (460 to 910 GB, 23 to 46 hours of downloads, plus building and proving a finder). Part of that list now exists for free.

What it does NOT give (so Census is still needed): periods, and almost certainly good coverage of slow binaries with one eclipse per sector, which are exactly the circumbinary hosts we want. CALNet classifies each sector separately from the light curve and a periodogram, so a long-period pair with one eclipse in a sector is the hardest case for it (LIKELY, from the paper's own example of a star classified differently in different sectors). The share of slow, detached binaries in the list is NOT TESTED.

What to do (Census stage 2, revised): (a) start from the union of public lists (Prsa 2022 for sectors 1 to 26, CALNet sectors 1 to 88, TESS Ten Thousand from FFIs to sector 82, Gao 2025 / arXiv:2412.06175); (b) get periods cheaply by matching CALNet's Gaia IDs to the Gaia DR3 eclipsing-binary table, which has periods (the project already counts that table but never cross-matched it); (c) point our own finder only at what those lists miss: slow binaries with one or two eclipses per sector; (d) use CALNet plus Prsa as a bigger answer key for testing the finder. This probably saves days of downloads and turns the finder into something more original, because it targets the gap the other lists leave.

### F2. The "chance of at least one planet" in Census-worth counts hunts that already found nothing (CONFIRMED by reading the code)

`research/stage3/census_step1/census_worth2.py`, line 15, computes `1 - exp(-tot)` where `tot` is the existing hunts' expectation plus Census's. But the existing hunts are finished and found zero. The chance that matters for the future is Census alone, and the existing null should also pull down the believed rate. The note `CENSUS-WORTH-2026-11-04.md` says Census at 1,400 stars "very likely finds one" (87% to 100%). That sentence is wrong as a forecast.

I re-ran it properly (script in section 5): Census only, the rate updated by the three null hunts, completeness trimmed 10% for real transit shapes (FIX 28):

| Census size (3 sectors each) | Prior: Kepler-like rate (median 10%) | Prior: broad (1% to 20%) | What the repo's table says |
|---|---|---|---|
| 1,400 G2-type stars | 36% to 52% | 21% to 31% | 86% to 99% |
| 3,000 G2-type stars | 59% to 76% | 38% to 52% | 94% to 100% |

Those are chances that a real planet is in the data AND passes the frozen search. They are not chances of a confirmed planet (section 3). The null hunts also pull the most believable rate down to about 5% to 7% (Kepler-like prior) or 2% to 3% (broad prior). The ceiling numbers in the same table ("95% ceiling if none") are computed correctly, because they use all hunts together, which is right for a ceiling.

Fix: one line in the script, a correction banner on the note and on Lesson 2, and the same wording check wherever the book quotes "chance of at least one".

### F3. The paperwork costs as much as the science (CONFIRMED counts; the judgement is mine)

141 of the 305 commits are book publishes, RESUME updates, ledgers, recaps or field notes; 70 touch the pipeline. RESUME.md is about 16,000 words, so every cold-start session reads roughly 20,000 tokens before doing anything. On 6 Nov an evening went partly to verifying claims that no conclusion depends on and to chasing a browser test that fails about once in 40 runs. It is very well documented, which is lovely, and expensive.

Suggestions: keep RESUME to one screen (state, open decisions, next step) and move history to an archive file; publish the book once a day at most, not after every task; verify claims only when a sentence or decision rests on them (that is already the rule in CLAUDE.md, it is just not being applied); park FIX 80 until it fails in a real publish.

### F4. The public repo cannot be run by anyone else (CONFIRMED)

64 of the 111 pipeline scripts contain hard-coded `D:\` paths, and there is no continuous testing (no `.github/workflows`). `pipeline/dataset.py` already centralises paths for some scripts. For a project whose whole pitch is "anyone can check us", and for the day a write-up is submitted, the core chain should run on any machine. Fix: route the core files through `dataset.py` (or an environment variable) and add one GitHub Actions workflow that runs the 9 existing test files on every push. Small job, large credibility gain.

### F5. The plan for the day a real candidate appears is filed but not written (CONFIRMED: BUILD-QUEUE T108 "Go-professional playbook page" and T125 "Lead follow-up protocol (template)" exist, neither is built)

The two-key rule and the private-leads rule are good. What is missing is the step after: for a single circumbinary transit, which future TESS sectors will see the star again (TESS-point), how to turn one dip into predicted windows, what evidence is needed before a write-up, where the write-up goes (NASA's candidate site now wants something published first, which the book already notes), and who could follow up. Writing this before any result is the same logic as preregistration: decisions made in advance are not bent by excitement.

### F6. Check the odds model against what professionals actually found (NOT TESTED; suggestion)

Davies et al. 2026 searched 512 detached eclipsing binaries and reported one weak candidate. Only a couple of transiting circumbinary planets have been discovered in TESS data and published (TOI-1338 b in 2020 and TIC 172900988 b in 2021; I did not do an exhaustive search, so UNCERTAIN). A cheap back-test: run Horizon's expected yield on the professional samples (the Prsa list and Davies's sample). If Horizon predicts several planets where the professionals found about one, Horizon is still generous and every Census forecast should be scaled down by the same factor.

### F7. Small things

The book calls Ahmed the "second key" (learning track, L6 check 3; `candidates.md`), while Ahmed calls himself the first key. Pick one. Second, the new study track should not be called "Workshop", because Chapter 13 is already "Your workshop". I use "Engine Room" in the mastery plan.

## 3. Honest odds for the next few months

"Finding a planet" is really four different events, so here they are separately. These are my estimates (UNCERTAIN), built from section 2 and the repo's own numbers.

| Event | By end of Feb 2027 | By end of 2027 |
|---|---|---|
| Census search actually run (list, ranking, Petrova upgrade, audit, preregistration, run) | 25% to 40% (your boards come first, and four big stages remain) | 75% to 90% |
| A real planet sits in the Census data and passes the frozen search (section 2, about 1,400 to 3,000 stars) | about 5% to 20% (needs the run to happen first) | 20% to 60% |
| A lead that survives both keys and is worth a public write-up | about 3% to 15% | 15% to 45% |
| A confirmed planet | under 1% | under 5% |

Why the last row is so low even if you find a perfect dip: one circumbinary transit is not a planet. Confirmation needs more transits or radial-velocity work by observatory teams, and that usually takes a year or more. The realistic best outcome of 2027 is "the first credible candidate from a citizen pipeline on a list nobody else searched, with predicted future transit windows". That would be a real, publishable result, and it is in reach.

The other honest result: if Census finds nothing, the two nulls together would set one of the tightest limits on how common big two-sun planets are around this kind of binary in TESS data. That is also publishable, and it needs no luck.

## 4. What I would do next, in order

1. Fix F2 (one line, one banner), so nobody plans on 90% odds. About 0.3 points.
2. Revise Census stage 2 with F1: download the four public lists, match Gaia periods, count slow detached binaries, and build the finder only for the gap. Lesson first, as agreed.
3. F4: paths and continuous testing, during a quiet week.
4. F5: build T125 and T108 (the "first candidate" playbook) before Census runs.
5. F3: slim RESUME and the publish rhythm, any time.

## 5. My scripts (re-runnable)

- CALNet check: downloaded `https://raw.githubusercontent.com/wangleon/CALNet/main/outputs/newecl.dat`, counted unique TICs and magnitudes, intersected with `targets/g1_targets.csv`, `g2_targets.csv`, `g3_targets.csv`.
- Odds: rate grid 0.1% to 40%; prior A lognormal, median 10%, factor-2 spread; prior B log-uniform 1% to 20%; likelihood of the null exp(-0.9 x E0 x r / 0.1); P(Census finds at least one) = posterior mean of 1 - exp(-0.9 x Ec x r / 0.1); E0 and Ec from `census-worth2.txt` (f 2.2 rule A, f 1.8 rule A, f 1.5 rule B). The 0.9 is the FIX 28 shape correction.

## Sources

- [CALNet paper, arXiv:2504.15875](https://arxiv.org/abs/2504.15875) and [CALNet repository](https://github.com/wangleon/CALNet)
- [TESS Ten Thousand Catalog, arXiv:2506.05631](https://arxiv.org/abs/2506.05631)
- [Prsa et al., TESS Eclipsing Binary Stars I, arXiv:2110.13382](https://arxiv.org/abs/2110.13382)
- [Thornton et al., arXiv:2512.07934](https://arxiv.org/abs/2512.07934)
- [Kostov et al., TOI-1338, arXiv:2004.07783](https://arxiv.org/abs/2004.07783)
- [TIC 172900988, arXiv:2105.08614](https://arxiv.org/abs/2105.08614)
- Repo files named in each finding.
