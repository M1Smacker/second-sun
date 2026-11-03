# Open Vigil and Horizon items closed, RS-005 (3 Nov 2026, Sonnet 5.5 Extra, cap 5)

Closes the 28 open and 5 partly answered Vigil questions and the Horizon items left by RS-001 and RS-002. Evidence: new reads today (listed per item), our own files, and reasoning (marked). Labels as in `vigil-literature-2026-11-03.md`. Question IDs are those of `NEW-SYSTEMS-RESEARCH-BRIEF-2026-11-02.md`.

## Result in one line
Of the 33 Vigil items, 25 are now answered, 3 stay partial (V-A8, V-C7, V-F2) and 5 need Ahmed or his accounts (V-A4, V-C3, V-C11, V-D1, V-F9). Horizon: all 14 answered or partly (H-12 partial).

## A: supply
- **V-A4 stays OPEN (needs Ahmed's yes):** the per-sector 2-minute target lists are small text files on [tess.mit.edu](https://tess.mit.edu/observations/target-lists); fetching a few is a download. Without them the trend is already clear from MAST metadata (SPOC share of our stars fell to about 1.5% a sector).
- **V-A6 answered, CONFIRMED (G3 fingerprint run, 612 stars):** TESS-SPOC files carry `DATA_REL` and `PROCVER` (830 files, 68 distinct DATA_REL, 49 distinct PROCVER); **QLP files carry neither** (4,075 files, 0 and 0). Rule for the ledger: DATA_REL and PROCVER when present, sha256 of every file always (it is the only version pin for QLP). The fingerprint is `data\g3\manifest_fp.csv`.
- **V-A7 answered, LIKELY:** QLP cadence went from 30 minutes to 10 minutes and, from Sector 56, to 200 seconds ([MAST QLP page](https://archive.stsci.edu/hlsp/qlp), text read in RS-001); SPOC has 20 s and 120 s. Vesper bins every product to 10 minutes and uses per-sector windows, so a cadence change inside one star's record does not break the matched filter; it can change the noise, which the per-light-curve noise unit already absorbs.
- **V-A8 stays partial:** TESS-SPOC full-frame is a year late and excluded; no other product was surveyed.

## B: statistics
- **V-B3 answered (design, reasoning):** a lead is one tier-1A real event on a non-known host (LEADS-RULES stage 4). Two events of one star within 0.5 d are one lead. Two events in different sectors count as a two-event lead only if their spacing fits a period inside the stability band (ratio about 5.5 to 7 binary periods for most known planets, section V-B4) and a period estimate from the pair is stated before the next window is looked at. Multi-conjunction transits within one binary orbit (Kostov 2020) give a period good to 10 to 20%.
- **V-B6 answered, LIKELY (from the MAST backtest):** a star of our union has a file in only about 5% to 11% of sectors, so a predicted window lands inside an observed sector with about that chance. This is why the prediction ledger is for two-event leads only and is rarely used.
- **V-B7 answered as a bracket, UNCERTAIN (my arithmetic):** new star-sector products per year about 1,300 to 3,000. If the Kepler coplanar rate (10%, planets above 6 Earth radii, periods under 300 d, Armstrong 2014) held for our stars, a year of Vigil would add tens of planetary tier-1 events (for example 2,000 x 0.10 x 0.27 x 0.57, about 30). The sealed G2 run (6,373 star-sectors) already found no excess, so the same arithmetic would have predicted around 100 there. The real figure is therefore far below the top of the bracket; the first honest number comes from Horizon's map. The book must say "one in a century" is not excluded.

## C: where it runs
- **V-C2 answered, LIKELY:** the injected-dip harness ran 1,548 injections through the full chain in about 4 minutes of machine time (ledger); a monthly increment of 100 to 230 star-sectors is of the same size. Environment setup is the larger part.
- **V-C3 stays OPEN:** needs a real runner test (Ahmed's GitHub step).
- **V-C7 partly answered:** results do not change with the worker count (zero-difference test 300 of 300 at 8 workers, anchor file); cross-platform equality NOT TESTED.
- **V-C9 answered, CONFIRMED:** [GitHub's terms for additional products](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features) limit Actions on GitHub-hosted runners to activity related to producing, testing, deploying or publishing the repository's software project, and ban cryptomining and activity that burdens servers disproportionately. A monthly science search over archive data is borderline under that text (UNCERTAIN how GitHub would read it). So the cloud job stays small (count, stamp, alert); the search itself runs locally. This supports the local-run base design.
- **V-C10 answered, reasoning:** secrets are set by Ahmed in the repository settings, never in code or logs; Claude does not type passwords.
- **V-C11 stays OPEN (Ahmed):** always-on device? a card he would use for a free tier?

## D: protocol
- **V-D1 stays OPEN (Ahmed, Q2).**
- **V-D2 answered (design):** each list is a dated file with its hash (G1, G2, G3 already are). A new list is a new list epoch; statistics are reported per epoch and pooled only with the epoch named.
- **V-D3 answered (design, with evidence):** the window rule is frozen in the protocol as a hashed reference windows table. G3 final counts (`g3-window-feasibility-2026-11-02.txt`, rerun 3 Nov on all 612 stars): QLP groups with 2 or more neighbours **80% with the union pool (G3 + G2 + G1) against 1% with a G3-only pool**; 7% would have none and 13% one. This is evidence for Q1.
- **V-D5 answered:** public: counts, ceilings, the hash chain head, the protocol, the OpenTimestamps proofs. Never public: star IDs, event times, lead lists, predictions in clear (only their hashes).
- **V-D6 answered (reasoning):** an independent check beats my own review (evidence ladder). Concretely the outsider rebuild test (V-E3) and a planted-dip end-to-end run are the independent checks.

## E: ledger and trust
- **V-E2 answered (design):** each line = sha256 over the RFC 8785 canonical JSON of {previous hash, record}; a genesis line with the protocol hash; mistakes are fixed by appending a correction line that cites the old line, never by editing; NaN written as null.
- **V-E3 answered (design):** `verify_chain.py` rebuilds every hash from public files only; it is written and run on a toy chain before the first real line.
- **V-E4 answered, CONFIRMED in our Loom notes:** one record format: the plain JSON status file per run from Loom phase 4 (RO-Crate and OpenLineage vocabulary, no tool adopted); the ledger line wraps that record with the previous hash.
- **V-E5 answered, LIKELY:** blind analysis and preregistration are argued for in [MacCoun and Perlmutter 2015](https://www.nature.com/articles/526187a.pdf) (seen in the earlier learning note; not reopened today); no astronomy-community rule was found. Our value claim stays modest: it protects us from our own tuning.
- **V-E6 answered (text for the book):** "We watch new sectors about a month after they arrive. We publish counts and a hash chain, never star names. A result counts only when the rules were written before the data existed."
- **V-E7 answered:** git (public, counts and hashes), a second copy on D:, the OpenTimestamps proofs committed beside the hash chain.

## F: small things
- **V-F1 answered, CONFIRMED (header of a local SPOC file):** `TIMESYS = TDB`, `TIMEREF = SOLARSYSTEM`, `BJDREFI = 2457000`, so TESS BTJD is barycentric dynamical time minus 2,457,000 days. Predicted windows are written in BTJD with that note. The QLP barycentric timing error of Sectors 99 to 104 (RS-001) shows why the file hash and the QLP correction date go into the ledger.
- **V-F2 stays partial** (four-orbit Sectors 97 and 98; safe-mode gaps not surveyed).
- **V-F3 answered (design):** one primary product per star-sector (the existing "best product"); other products are checks; counts are per star-sector, never per file.
- **V-F4 answered, CONFIRMED (G3 manifest):** median file size QLP 0.23 MB (4,075 files, 1.63 GB), SPOC 2-minute 1.92 MB (126 files, 0.24 GB), TESS-SPOC 0.39 MB (830 files, 0.41 GB). A monthly increment of 100 to 230 star-sectors is about 25 to 460 MB (mostly QLP files, so near the low end).
- **V-F5 answered:** a missing or corrupt file is a visible "skipped" line with the reason; the fetcher uses the retry and heartbeat pattern of fix item 72.
- **V-F6 answered (plan figure):** about 0.3 weekly point a month for the human review.
- **V-F7 answered:** the environment baseline file exists (`ENVIRONMENT-BASELINE-2026-10-30.txt`); packages are pinned and a version change is tested by the zero-difference test before use.
- **V-F8 answered (design):** the replay test pretends the last three released sectors are new and must reproduce the known events; a planted dip in a new file must be recovered end to end.
- **V-F9 stays OPEN (Ahmed):** the name Vigil.

## Horizon items
- **H-3 answered, CONFIRMED text:** [Martin 2018, arXiv:1802.08693](https://arxiv.org/abs/1802.08693) (ar5iv text read): the transit probability of a circumbinary planet is higher than around a single star and falls more slowly with period; a misaligned planet often misses the transits and makes a sparse signal, so an abundance deduced from a coplanar sample is only a minimum; the paper cites Li et al. 2016 for transit probability (title not seen).
- **H-11 answered, LIKELY:** 1,548 full-chain injections took about 4 minutes of machine time in the earlier harness, about 0.15 s each; 20,000 injections would take about 50 minutes at that rate. R1 still begins by timing one star.
- **H-12 stays partial:** only Oddo and Armstrong were read as comparable maps.

## Not done
No runner test, no Cycle 9 list, no reading of the MAST terms of use, Li 2016 not located.
