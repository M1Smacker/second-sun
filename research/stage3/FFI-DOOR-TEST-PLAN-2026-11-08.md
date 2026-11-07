# The full-frame door: can bright binaries with no 2-minute data feed our search? Test plan (DRAFT, written 8 Nov 2026, waits for Ahmed's approval; no light curve has been read)

## Why (Ahmed, 8 Nov 2026)
"Sooner or later we are going to run out of things to search." The 2-minute lists are the easy fuel. Census (G4) uses most of the bright slow detached binaries that were ever 2-minute targets; G5 (5,000 to 10,000 stars to about G 14) needs more than that. The full-frame images (FFIs, 10 to 30 minute light curves from QLP and TESS-SPOC) are the other door.

## What we already know (CONFIRMED from our own files)
- G3 already went through this door for 611 stars of the TESS Ten Thousand Catalog (period over 7 d, Tmag 13.5 or brighter, not in G1, G2 or Prsa): 4,075 QLP files, 830 TESS-SPOC full-frame files and only 126 SPOC 2-minute files; 4,080 star-sectors searched; 784 of 5,634 product reads (13.9%) had no safe windows. So reading FFI light with unchanged Vesper works (`G3-PREREGISTRATION.md`, `G4-GATHER-2026-11-04.md`).
- The loader reads QLP and TESS-SPOC (`detect_v2.load`); other products (TGLC, eleanor) are NOT supported (NOT TESTED).
- So the open question is not "can we read FFI light" but: (1) how many NEW bright slow binaries does the full-frame door hold that no list of ours has, (2) do usable FFI light curves exist for them, (3) are the Gaia periods and ephemerides good enough to mask their eclipses, (4) does a known circumbinary transit survive in FFI light.

## Sample (rule fixed before looking)
- Frame: Gaia DR3 `vari_eclipsing_binary`, period over 5 d (frequency under 0.2), joined to `gaia_source`, Gaia G under 14 (the G5 limit). Built by per-HEALPix-pixel queries (level 3, 768 pixels, in the background; the whole-sky join times out). The same run gives the exact bright slow pool for G5 (replaces my 1.6% north-cap sample).
- Remove: any star that was a 2-minute target in sectors 1 to 111 (position and Tmag match to the 111 lists in `data\census_targets_2m`, 3 arcsec), and any star in G1, G2, G3, Prsa 2022, TTC or CALNet.
- Draw 400, seed 20261108, stratified by Tmag (bins 8 to 10, 10 to 11, 11 to 12, 12 to 13, 13 to 14, equal quotas where the pool allows, rest filled from the next bin) and by Gaia period (5 to 10, 10 to 30, over 30 d). TIC ids from the MAST TIC catalogue by position.

## Metrics, written first (a star-sector counts as usable only if all of U2, U4 hold)
- U1 existence: at least one FFI light curve (QLP, TESS-SPOC, others listed) in at least 2 sectors.
- U2 quality: at least 70% good cadences; median 8-hour noise within 1.5 times the G3 fit at its Tmag (log10 noise8 = 0.26 + 0.211 x Tmag).
- U3 eclipses and ephemeris: at least one eclipse found at SNR 7 or more; observed eclipse times compared with the Gaia period and eclipse phase (does the Gaia ephemeris mask the eclipse within 0.25 d?). Reported separately: share of Gaia candidates that show no eclipse at all (Gaia false or blended).
- U4 pipeline-ready: loads with the unchanged frozen loader.
- U5 safe windows: share of star-sectors with safe windows under the current neighbour-window rule (G3: 86.1%).
- U6 second product: share of star-sectors with two independent products (tier 1A or 1L possible) against one (tier 1B).
- U7 dilution flag: TIC contamination ratio.
- Decision rule: door OPEN if U1 at least 80% of stars, U2 and U4 at least 70% of star-sectors, U3 at least 50% of stars, U5 at least 80%, U6 at least 50%. PARTIAL if all are at least half of those; CLOSED otherwise. Numbers are reported whatever the verdict. Nothing about Petrova is tuned.
- Positive control: TOI-1338 (TIC 260128333) in FFI-only sectors, QLP and TESS-SPOC full-frame light: is a known circumbinary transit still visible?

## Stages, cost in weekly points (UNCERTAIN; my rounds so far ran about 0.05 points each; range is the honest spread)
| Stage | What | Points |
|---|---|---|
| A | Research stint RS-012 (cap 0.6): primary sources on QLP, TESS-SPOC, TGLC, eleanor (coverage, Tmag limit per sector, cadence, systematics), Gaia EB period reliability (Mowlavi 2023); ASAS-SN and ZTF as extra period sources (count only); write this plan as the committed preregistration | 0.8 |
| B | Gaia pixel queries in the background, exclusions, seeded draw of 400, TIC ids | 0.5 |
| C | MAST existence census for the 400 (products by sector), counts only | 0.3 |
| CHECKPOINT 1 | Report U1, U6 and the pool size to Ahmed before any light-curve download | |
| D | Download about 2 sectors per star per product (about 1,600 files, a few GB, background, hours of wall-clock, MAST time-outs expected) into a new empty folder under `data\`, register on the Downloads job list, compute U2 to U7, positive control | 1.0 |
| E | Write-up, queue and plan changes, RESUME, ledger | 0.3 |
| Idea 3 | RS-013 (cap 0.4): K2 archive, has anyone searched it for circumbinary transits | 0.3 |
| Idea 1 | RS-014 (cap 0.4) plus the G5 plan note: 5,000 to 10,000 stars to about G 14, fainter only for M-dwarf hosts (research: Gaia counts of red-dwarf eclipsing binaries, literature on circumbinary planets around M dwarfs); reuses the pool of stage B | 0.5 |
| Overhead | RESUME, ledger, commits, queue filing | 0.2 |
Total about 3.9 (range 2.8 to 5). Order: A, B, C, checkpoint, idea 3, D, E, idea 1. If the budget runs out, idea 1 shrinks to a stub note.

## Not part of this test
Planting fakes in FFI light (completeness) is the next step if the door is OPEN; any search; any change to Petrova; idea 4 (Ahmed: no).

## Risks
Gaia slow-period solutions are unreliable (Mowlavi 2023: completeness 25% to 50% against OGLE, UNCERTAIN for P over 20 d); Gaia EBs include blends; MAST time-outs (G3 download took 21 hours); a 400-star sample gives shares good to about plus or minus 5 points.
