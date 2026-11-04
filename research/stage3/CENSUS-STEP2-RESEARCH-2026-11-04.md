# Census stage 2 groundwork: do lists already exist, and how big and how slow is it to build our own? (night of 4 Nov 2026; research stint RS-011; report only, nothing built)

Two questions, both asked in the Census plan and neither answered by Step 1: (A) is any list of eclipsing binaries after sector 26 already public, so we should not build what exists; (B) what would it cost, in files, gigabytes and hours, to fetch the light we would need to find our own. Scripts and raw output in `research/stage3/census_step1/` (`route_probe.py`, `route_parallel.py`, `route-probe.txt`, `route-parallel.txt`, `route-scenarios.txt`).

## Plain verdict
**A: no complete list exists beyond sector 26, but there are partial ones that are biased against the long-period binaries we want. B: fetching the light is much cheaper than G3 made it look: 3 files a second with 8 threads from a public AWS bucket, 1.8 MB a file. A first pass over one sector of every new bright star is about a day and 460 GB; the long-coverage stars (5,200 stars with 8 or more sectors, all their sectors) are 6.7 hours and 135 GB.** Building our own list is a days-long job, not months, if the speed holds. The speed was measured on 66 files only (UNCERTAIN for a run of hundreds of thousands).

## A. Lists after sector 26 (abstracts read on arXiv; CONFIRMED unless marked)
- **Prsa et al. 2022, MAST TESS-EBs v1.0:** sectors 1 to 26, last updated 29 June 2022 (earlier note, page read). Still the only official one.
- **TESS Ten Thousand Catalog (Kostov et al. 2025, arXiv:2506.05631):** 10,001 EBs from full-frame images, machine learning plus citizen scientists; already used (G3).
- **Classification of Periodic Variable Stars from TESS (arXiv:2412.06175, Dec 2024):** 2-minute data of the first 67 sectors, 72,505 periodic variables, about 1,600 newly classified eclipsing binaries (3,938 detached among the labelled and predicted). Method: Lomb-Scargle on each light curve with the search limited to 13 days for one-sector stars and 13 x N days for N sectors (full text read), so slow, detached binaries with one eclipse per sector are exactly what it cannot see well. A partial list, biased short (LIKELY).
- **The Phenomenological Classification of TESS Eclipsing Binaries (arXiv:2604.26398, Apr 2026):** a classifier applied to 20,196 TESS eclipsing binaries "collected from multiple star catalogs", ASAS-SN based: a classification of known ones, not a new search.
- **Others read:** a catalogue of 1,292 short-period M-dwarf pairs (arXiv:2508.13941; the sample Oddo used), a neural network for EBs trained on 4,225 samples (arXiv:2504.15875, method), quadruple candidates (arXiv:2309.14200) and 370 new EB candidates from sectors 1 to 26 (arXiv:2205.14184).
- **Not found, NOT TESTED beyond arXiv titles and abstracts:** any EB list from the 2-minute data of sectors 27 and later that targets long periods. The ADS and a title search outside arXiv were not done; the `mono-cbp` catalogue choice of Davies et al. 2026 (arXiv:2604.09435) is another sign that the old list is still the standard.

## B. What it costs to fetch the light (CONFIRMED by measurement on 66 files of sector 27; extrapolation UNCERTAIN)
- **Routes:** MAST publishes a cURL script per sector listing every 2-minute light curve (sector 27 has 19,997 files; scripts exist up to sector 109 in the FFI list). The same files sit in the public AWS bucket at `stpubdata.s3.amazonaws.com/tess/public/tid/s####/xxxx/xxxx/xxxx/xxxx/<file>`, which worked and returned the same size as MAST.
- **File size:** 1.79 MB per sector-27 light curve (every probed file the same size, 1,785,600 bytes).
- **Speed:** 1 thread from the bucket 0.49 files/s (0.87 MB/s); MAST 0.35 files/s; **8 threads from the bucket 3.1 files/s (5.6 MB/s)**. G3 took 21 hours for 5,031 files because of MAST time-outs and restarts (0.07 files/s); the bucket route did not time out in 66 files.
- **Disk:** D: has 464 GB free. Streaming (fetch, reduce to a few hundred bytes of features, delete the file) removes the disk limit.

| scenario (stars never 2-minute targets in S1 to 26; sectors 27 to 109) | stars | files | GB | hours at 8 threads |
|---|---|---|---|---|
| Tmag up to 13.5, all sectors | 258,858 | 510,446 | 914 | 45.6 |
| Tmag up to 13.5, one sector each (first pass) | 258,858 | 258,858 | 463 | 23.1 |
| Tmag up to 12, one sector each | 218,225 | 218,225 | 391 | 19.5 |
| Tmag up to 10, one sector each | 82,976 | 82,976 | 149 | 7.4 |
| Tmag up to 11, 4 or more sectors, all their sectors | 17,279 | 108,078 | 193 | 9.7 |
| Tmag up to 10, 4 or more sectors, all their sectors | 12,703 | 71,999 | 129 | 6.4 |
| Tmag up to 12, 6 or more sectors, all their sectors | 8,075 | 84,308 | 151 | 7.5 |
| Tmag up to 13.5, 8 or more sectors, all their sectors | 5,193 | 75,151 | 135 | 6.7 |

(All files are taken at the sector-27 size; later sectors should be similar, NOT checked. The machine time to find eclipses in 250,000 light curves is not measured: G2's full search ran 0.73 s per star-sector on 6 to 8 workers; a plain eclipse finder is cheaper, so hours, not days, LIKELY.)

## What this changes
1. The "months" we feared for the list are mostly not the download. The hard parts are the detection step (an eclipse finder that does not mistake pulsators, rotators and flares for binaries), the vetting (secondary eclipse, odd-even, neighbours), and the star-by-star ranking.
2. **The long-coverage stars are the natural first step:** 5,193 stars with Tmag up to 13.5 and 8 or more sectors need only 135 GB and under 7 hours, they are where a long-period eclipse is caught several times, and they are the stars where orbit linking (idea 4) and the planet geometry (Q1) pay best (Q2 showed value per star rises with sectors). Candidate for the pilot of Census stage 2.
3. Disk and speed are not blockers; polite use is: the bucket is public and free, but stay at 8 threads and add a back-off.
4. Not decided and not started: which light curves, which finder, which pilot size. Those are Ahmed's calls, taught step by step.

## Labels
CONFIRMED: sector-27 script size, file size, measured speeds, scenario arithmetic, abstract and full-text statements quoted above. LIKELY: that later sectors have the same size; that a plain finder costs less than the G2 search. UNCERTAIN: sustained speed over hours, bucket behaviour under heavy load, the finder's false-alarm and completeness rates. NOT TESTED: ADS and non-arXiv sources for a post-26 list; reading any light curve; the AWS bucket terms of use (public open-data registry, not opened).

## UPDATE (same night): what each pool would yield (own data, `census_step1/eb_share_by_coverage.py`, output `eb-share-by-coverage.txt`)
The Prsa 2022 EB share among 2-minute stars of sectors 1 to 26, by brightness and number of sectors, is flat at about 1.2% to 4.0% (EB) and 0.3% to 1.0% (G2 type: period over 5 d, detached). It does not climb with coverage. So the number of G2-type stars we could find is set by how many stars we scan, not by how many sectors each has. Applied to the pools of the scenario table (the stars new to 2-minute data in sectors 27 to 109):
| pool | stars | expected EBs | expected G2-type | download |
|---|---|---|---|---|
| Tmag up to 13.5, all new | 258,858 | about 5,800 | about 1,400 | 914 GB, 46 h (all sectors) or 463 GB, 23 h (one sector each) |
| Tmag up to 11, 4 or more sectors | 17,279 | about 370 | about 110 | 193 GB, 9.7 h |
| Tmag up to 10, 4 or more sectors | 12,703 | about 250 | about 84 | 129 GB, 6.4 h |
| Tmag up to 12, 6 or more sectors | 8,075 | about 170 | about 50 | 151 GB, 7.5 h |
| Tmag up to 13.5, 8 or more sectors | 5,193 | about 85 | about 27 | 135 GB, 6.7 h |
**Correction to the verdict above:** the 5,193 long-coverage stars (6.7 hours) are a good PILOT for testing the eclipse finder and the fetch, but they hold only about 27 G2-type stars. A Census of over 1,000 such stars needs most of the 258,858 new bright stars, which is the 23 to 46 hour and 460 to 910 GB job. That is still days, not months, if streamed (fetch, reduce, delete). All the yields are LIKELY at best (the S1 to 26 shares may not transfer: UNCERTAIN, factor 2). Free ground truth for the finder: 4,161 Prsa EBs were 2-minute targets again in sectors 27 to 109 (Step 1), including 854 of the G2 stars; a finder run on their later sectors can be scored for recall without any new labels. NOT done; Ahmed's call.
