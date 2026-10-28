# B-lite: mono-cbp run as a yardstick (28 Oct 2026)

Ahmed said "go ahead" to B-lite in chat. mono-cbp is GPL-3.0, so it lives OUTSIDE this repository (`D:\ss-external`: a clone of github.com/bdrdavies/mono-cbp at commit 8d373b4, version 0.1.9, and its own Python 3.12 environment). Nothing of its code is copied here. Only its output files are read, by `pipeline/compare_monocbp.py`, and only aggregates are published. The three small run scripts are not in this repository either (they import the package); the steps are written below so anyone can repeat them.

## What was run (all VERIFIED: our own runs)
- Install: Python 3.12, `numpy<2`, `scipy==1.12.0`, `setuptools<81`, then the repository with `pip install -e`. It took three attempts. The first two tried to build scipy 1.11 from source (no Python 3.12 wheel); the fix was a constraints file pinning numpy and scipy. Python 3.12 also needs setuptools for `distutils`. Resulting versions: mono_cbp 0.1.9, scipy 1.12.0, numpy 1.26.4, lightkurve 2.6.0, wotan 2.0, batman 2.5.3, lmfit 1.3.4, astropy 7.2.3.
- Data: our local TESS-SPOC files for the 30 stars both searches share (224 star-sectors), converted with mono-cbp's own `lc_to_txt` (SAP flux, hard quality mask, crowding and flux-fraction fix, 30 minute bins). Eclipse table: the authors' own TEBC catalogue rows for those 30 stars. Default configuration, vetting on.
- Control: the same 224 files with the flux turned upside down (flux to 2 minus flux), same eclipse masks.
- Speed: real run 459 s, upside-down run 430 s, one core, 224 star-sectors (about 2 s each, vetting included).

## Result 1: the two searches mostly do not see the same events (`research/stage3/monocbp_compare_30stars.txt`)
| | real | upside-down |
|---|---|---|
| mono-cbp, all events | 437 (195 per 100 star-sectors) | 209 (93) |
| mono-cbp, SNR 7 or more (their scale) | 144 on 18 stars | 27 on 10 stars |
| mono-cbp, class T or AT | 209 | 34 |
| mono-cbp, SNR 7 or more, robust, T or AT, not flagged | 114 on 14 stars | 6 on 3 stars |
| Second Sun v5, all tiers (SNR 7 or more) | 41 (18 per 100) | 46 (20) |
| Second Sun v5, tier 1 | 0 | 1 |

- Agreement (same star-sector, centres within 0.5 d): 3 of our 41 real events were also found by mono-cbp; 0 of their 144 events at SNR 7 or more were found by us. 134 of those 144 sit in star-sectors where we have no event at all.
- Their SNR 7 or more events are deep and short: median depth about 10,000 ppm (1%), median duration 4.5 h, 47% on just 3 stars, 36 of them above SNR 30. That pattern fits leftover eclipses of the binaries better than planets (LIKELY; NOT TESTED: I looked at no individual event, by rule). The upside-down copy has far fewer such events, which says the real curves hold real structure, not that it is a planet.
- So "real above upside-down" means something different for mono-cbp: its real events include real stellar signals. Our design (eclipse-aware search, flags, then compare with upside-down) is stricter. The count difference is NOT evidence that either tool is better. Their SNR is not our SNR.

## Result 2: the known planet TOI-1338 b (published mid-times, Wang and Liu 2024, arXiv:2404.18415)
Sectors with cached SPOC 2 minute data. "SAP" means the same file read as SAP flux with the same hard quality mask. Our SNR is the box SNR of the frozen detector (bar 7).
| Sector | Data near the transit | Ours, PDCSAP (our normal input) | Ours, SAP | mono-cbp (SAP, 30 min) |
|---|---|---|---|---|
| 6 | yes | missed | 12.5 | found, SNR 5.2, class Sin |
| 10 | yes | 11.5 | 10.8 | found, SNR 4.9, class Sin |
| 27 | yes | missed | 7.2 | found, SNR 3.7, class Sin |
| 30 | none (gap) | n/a | n/a | n/a |
| 34 | yes | missed | 10.7 | found, SNR 4.8, class Sin |
| 37 | yes | missed | 7.4 | found, SNR 3.2, class A |
| 62 | none (gap) | n/a | n/a | n/a |
| 65 | yes | 9.0 | 12.5 | found, SNR 5.3, class Sin |
| 68 | yes | 7.5 | missed | missed |
| 98 | yes | 9.0 | 10.1 | found, SNR 2.8, class Sin |
- Our PDCSAP input finds 4 of 8 testable transits; SAP finds 7 of 8; either one finds 8 of 8. They fail on different sectors.
- mono-cbp detects 7 of 8, but its model comparison calls 6 of those 7 a sinusoid and 1 ambiguous: none is T or AT, the classes the paper keeps as candidates. UNCERTAIN why: I used the default configuration and 2 minute SPOC data binned to 30 minutes, not the FFI TESS-SPOC product their paper used. NOT TESTED with the paper's own settings.
- This also explains the earlier open puzzle in `research/mistakes.md` (SAP gave a 2 to 3 times smaller noise estimate than PDCSAP in sectors 6, 34 and 37): on this star it is a real loss of sensitivity from our input choice.

## Result 3: SAP against PDCSAP across the 224 shared star-sectors (a measurement on mono-cbp's data, our own script)
Noise = 8 h box scatter after a 2 day biweight, SAP with the same crowding fix. SAP over PDCSAP: quantiles 10, 25, 50, 75, 90 = 0.45, 0.83, 1.01, 1.13, 1.30. SAP noise below 0.8 times PDCSAP in 23% of star-sectors (below 0.5 times in 12%), above 1.25 times in 13%. The median is equal, so neither flux is better everywhere; each is better in a quarter of sectors (LIKELY, 30 stars only). Cause NOT KNOWN.

## What this means (LIKELY, labelled)
1. B-lite worked as a yardstick: installable, fast, and it exposed an input-choice weakness of ours that nothing else had measured. That is a v6 candidate (FIX-QUEUE item 15): search both SAP and PDCSAP and take the union, flagging which product saw the event. It changes the search, so it needs Ahmed's go and a regression re-proof first.
2. mono-cbp is not a drop-in better detector for our job: on the 30 shared stars it floods with eclipse-like events and its vetting rejects the known planet's transits as sinusoids with default settings.
3. Not done (NOT TESTED): same injected dips in both tools (the fair recovery comparison), a repeat run to prove mono-cbp reproduces itself, the paper's own data product, and a longer list of known planets (only TOI-1338 had cached data; Kepler-1647 is the other shared known host).
