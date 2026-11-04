# Census step 1: how many stars have 2-minute TESS data after sector 26 (4 Nov 2026, night, counts only)

Ahmed's go: the night plan of 4 Nov (downloads allowed, told every time). Method: the 111 public 2-minute target lists of the TESS Science Office (https://tess.mit.edu/public/target_lists/, file `2m/all_targets_S###_v1.csv`; CONFIRMED to exist for sectors 1 to 111). Nothing but the lists was read: no light curve, no search, no list design. Script `research/stage3/census_step1/count_targets.py`, output `step1-counts.txt`, downloads logged in `research/downloads.csv` and `research/jobs.md` (111 files, 65.2 MB, `data\census_targets_2m`).

## Plain verdict
**There is a lot of fuel the published lists do not name.** 476,784 different stars were 2-minute targets in sectors 27 to 109; **364,656 of them (258,858 with Tmag 13.5 or brighter) were never a 2-minute target in sectors 1 to 26**, where the Prsa 2022 eclipsing-binary list comes from. Nobody has published an eclipsing-binary list for them (MAST TESS-EBs is v1.0, sectors 1 to 26; CONFIRMED earlier). How many of them are eclipsing binaries is NOT measured here.

## Numbers (CONFIRMED: counted from the files)
- Target-sectors: sectors 1 to 26 507,898; sectors 27 to 109 1,250,090. The sector 110 and 111 files are plans (23,752 rows), not data yet (110 runs to 26 Nov).
- Unique stars: 232,764 (S1 to 26); 476,784 (S27 to 109).
- S27 to 109 stars by brightness (Tmag): up to 10: 149,970; 10 to 11: 77,438; 11 to 12: 85,668; 12 to 13: 36,975; 13 to 13.5: 12,723; fainter 114,010. About half are in 2 or more sectors; 4 or more sectors: 39,646 (up to 10), 9,216, 8,512, 6,293, 2,637 for the bright bins.
- Sectors 27 to 55 list 20,000 targets each; from sector 56 on 9,687 to 13,000 each (the lists shrink).
- Prsa 2022 EBs: 4,578 distinct stars in the saved table (4,584 rows in the paper); 4,161 are also 2-minute targets again in S27 to 109 (those already have a published list entry).
- Our searches: G1 549 stars (211 in S27+), G2 895 (854 in S27+), G3 612 (22 in S27+). TTC new EBs 7,936 (126 in S27+), known 2,065 (95).

## A rough size of the prize (LIKELY at best; NOT measured; my arithmetic, wide error)
- Prsa found EBs in 1.97% of the 232,764 stars of S1 to 26 (4,578 / 232,764); the same share holds for Tmag 13.5 or brighter (1.98%).
- If the new bright stars were like those: 258,858 x 1.97% = about **5,100 eclipsing binaries** among them, all periods. 946 of 4,584 Prsa EBs (20.6%) fit the G2 rule (long period, detached, bright; CONFIRMED in G4-GATHER), so **about 1,000 G2-type targets** (long-period detached bright). Error at least a factor of 2 either way, for three reasons: many 2-minute targets after sector 26 were chosen by guest-observer programs, not from the same population; Prsa's detection depends on the coverage (1 or 2 sectors) and a long-period EB with 1 eclipse in the data is missed; the true share of long-period detached EBs among them is unknown. Even at half, the size is over 500 stars.
- Meaning for Census: a target list of well over 1,000 bright stars with 2-minute data looks reachable from this pool alone, before FFI data or Gaia. Finding them is the real work (step 2): a detection step run on those 258,858 light curves, which is a download of order terabytes if done naively; the cheap route is a first pass on the QLP/FFI-free summary or on a few sectors. NOT planned yet, Ahmed decides.

## What this does NOT say
- It does not say a single star is an eclipsing binary. It says nothing about orbital periods, depths or planets.
- It does not choose a list or a rule. No star IDs are published; the lists are public TESS target files.
- The 2-minute lists only cover pre-selected targets; the Full-Frame Image data (30, 10, 3.3 min) hold many more stars (TTC used FFIs). That part is not counted here.

## Cost record
Prediction 1 point; actual in the ledger row.
