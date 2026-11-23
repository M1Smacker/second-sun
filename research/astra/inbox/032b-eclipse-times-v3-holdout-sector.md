# 032b: eclipse times v3 judged by predicting a held-out sector, then the V3 mask bench

Written by Claude, 23 Nov 2026, 11:28 am Kuwait. GO: Ahmed 22 Nov 9:30 pm and 23 Nov 10:43 am. Preregistration, committed before any 032b number exists. Background: your 032 (merged 98842e2c): Part A FAIL by one star (47 of 53 fresh controls agree with the catalogue, 48 needed). Claude's RS-045 (`research/stage3/rs045/RS-045-RESULT-2026-11-23.md`): for all 6 disagreeing tracks the eclipses MEASURED in the light are 0.3 to 35 widths from the catalogue while the v3 fit follows them within 0.04 width; the catalogue, not the method, failed. 032's verdict stays FAIL in the record; this is a new judge on new stars.

## Method: v3 exactly as in 032, no change
Measurement, alias resolution, error model, usable rule: the 032 code and settings unchanged (`032_*` scripts on main). Nothing may be retuned.

## Judging stars (not used to design or judge v3)
(a) the 112 affected G2 stars (014/010 list): v3 was designed on controls, never judged on these; (b) 60 G3 design-seen stars drawn with seed **2026112318**, stratified by the 5 period bins as before, needing 3 or more TESS sectors; state the counts before fitting. (The G2 control pool is exhausted: 165 eligible, 160 used.)

## Judge: the held-out sector
For each primary track with eclipse times in 3 or more sectors: fit v3 on all sectors except the LAST one with measured eclipses; predict every primary eclipse centre in that last sector; compare with the eclipse times measured there (the same measurement code). A track PREDICTS if the median |measured minus predicted| in the held-out sector is at most 0.25 x the eclipse width AND every one is at most 0.5 x the width.

## Pass rules (each set separately)
(H1) usable: at least 80% of primary tracks with 3 or more sectors are usable on the fit sectors; (H2) at least 90% of usable tracks PREDICT; in set (a) and in set (b) separately; (H3) the 30-case trap stays 30/30. Also report, not judged: catalogue agreement as in 032 (set (a) is expected to disagree often: that is why they are "affected"), the same held-out judge on 032's 53 fresh controls (labelled seen), secondary tracks.

## Part B (only if H1 to H3 pass in both sets)
Exactly Part B of brief 032 (V3 mask: usable v3 tracks set the window centres and a padding of 3 x the v3 predicted-centre error, catalogue windows elsewhere, same mask both arms; NEW fresh bench seed 2026112301, NEW T156 seed 2026112302, F1 rules (a) to (g), identity at both ends, untouched background, TOI-1338 b; exploratory: P on the 112 affected stars, RS-027 deep events removed). The V3 ephemerides used in Part B are fitted on ALL sectors (the held-out split is only the judge).

## Rules
Never edit frozen files; design stars and planted light only; counts only; 2 workers x NUMBA_NUM_THREADS=2 (the 031 bench is still running); checkpoints; data in `data/astra/032b/`; branch `astra/032b-v3-holdout`. Start long parts detached and hand back with a progress file; if Part A passes, launch Part B detached in the same job. Meter before and after, logged in `research/astra/USAGE.md`. Claude recounts independently before any merge.
