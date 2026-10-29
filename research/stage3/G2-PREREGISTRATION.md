# G2 preregistration (PROPOSED 29 Oct 2026)

**Status: PROPOSED.** It becomes binding when Ahmed says "lock it" and the commit id of that moment is written at the bottom. Until then the development slice may be downloaded and used; the sealed slice may not be downloaded, searched or looked at. After locking, a change needs a new dated amendment at the bottom, never an edit of the rules above it.

## 1. Purpose
G1 (549 Kepler field stars) was used to build and tune Vesper v1 to v7, so it cannot be the final test. G2 is a second set of stars, defined before it is searched, so that a frozen version is tested once on stars it never saw. Win condition (Ahmed, 29 Oct 2026): a clean measured null, that is, how small a planet the chain could have found plus an honest count of what was found. A candidate would be welcome but is not the target. Interesting signals are not discoveries.

## 2. The star list (fixed by these hashes)
- Source: TESS eclipsing binary catalogue (Prsa et al. 2022, https://arxiv.org/abs/2110.13382) as saved in `data/xmatch/ebs.csv` (sha256 933e635c0370ee436fafbca250869e13067ddad22b13aecfd1d9e44f1e5d4087). The saved copy lists sectors up to 39; whether its periods and morphology were redone with the later sectors is UNCERTAIN.
- Rule: one row per TIC; morphology from 0 up to but not including 0.5 (detached); binary period over 5 days; Tmag 13.5 or brighter; TIC not in `targets/g1_targets.csv` (sha256 38ad01b2d1ceca7abb6e30bbf984f5debe1cdff10fcbc5910e341269b8ce87c9). This is the G1 rule applied to a different catalogue. It gives **895 stars**.
- The list is `targets/g2_targets.csv` (sha256 809212e5ef3ac1ecd77de99989aab89ba935cc97cebbb62d3fe6e651641f8bb6). It contains no light curve, no event and no search result.
- Known circumbinary hosts and TOIs inside the list are labelled, never removed. About 2 known hosts are expected (one very likely TOI-1338); their recovery is reported.

## 3. The split
- **Development slice (301 stars):** the integer value of sha256(str(TIC)) modulo 3 is 0. It may be downloaded, searched any number of times and used to tune and choose Vesper v8.
- **Sealed slice (594 stars):** modulo 3 is 1 or 2. Not downloaded, not searched and not looked at until all of: this file is locked; v8 (or v7) settings and code are frozen under a hash with the Stage 2 and G1 regression re-proved; Ahmed says go.
- The sealed slice is searched **once** with that one frozen version. If a bug is found afterwards, the fixed version is run again and BOTH results are reported with the reason; no setting changes in between.

## 4. The pipeline on G2
The same chain as the frozen version (search, flags, second-product check, SAP twin, PDCSAP check, union, tiers, common moment flag), with the data paths switched to `data/g2` and the target list to `targets/g2_targets.csv`. The switch must not change any rule; a zero-difference test on G1 (the same events and tiers as before) must pass before G2 is read.

## 5. What counts as an excess (decided before any G2 result exists)
On the sealed slice, per flux half and per SNR bar (7, 8, 10, 12): the real tier 1 count against the noise-expected count, where the noise-expected count is the upside-down tier 1 count divided by the real-to-upside-down ratio measured by `asymmetry_test.py` on the same slice, nothing else chosen. An **excess** needs the chance of at least the observed real count from noise (Poisson) to be 0.01 or less at the SNR 7 bar, with the real count above the noise-expected count at the other bars as well. Anything less is reported as **no excess**. A raw-light half without a fair control (as in G1) is reported on its own line and is never evidence. An excess is not a discovery: it only opens the two-key vetting (Claude's analysis and Ahmed's own check), pixel and centroid tests, and a human look only after the Eyes ladder allows it.

## 6. Completeness (reported with every result)
`chain_recovery.py` (unchanged logic) on the development slice, and on 300 random star-sectors of the sealed slice AFTER the sealed search. Reported as depth in ppm and duration first, tier 1 recovery, the 50% depth, and planet size only as a labelled range. A null is stated together with this table.

## 7. Reporting rules
Aggregates only. No real event is opened or plotted without Ahmed's explicit yes. Labels CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED. Anything searched in G2 before locking is development use and is reported as such.

## 8. Known limits of this design
G2 stars have many more sectors than G1 stars (median 7 against 15 for Kepler field stars, 28 GB in all, UNCERTAIN how much is 20 second data); the professionals (Davies and colleagues) already searched some of these stars with a different tool and we do not hold their list; the catalogue's periods may be updated; 895 stars give limited power for a rare event.

## Lock record
Not locked. (When locked: date, Ahmed's words, commit id.)
