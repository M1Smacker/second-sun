# Job list (interim, until the Downloads page exists)
One line per download or long machine run: when, what, from where, why, expected size, state. Started automatically by Claude (Ahmed's rule, 30 Oct 2026).

| Started (30 Oct 2026) | What | From | Why | Size | State |
|---|---|---|---|---|---|
| 17:20 | G2 sealed slice light curves, 594 stars (SPOC 2 min, TESS-SPOC, QLP) | MAST (mast.stsci.edu) | the one-time sealed Vesper search, G2 preregistration Amendment 1 | about 16 to 17 GB (estimate) | DONE 18:3x: 594 of 594 stars, 17,383 light-curve files, about 14.6 GB; restarted 17:35 at normal priority with 16 threads |
| after the download | Sealed data preparation: audit windows, audit of every file, best-product table, TOI-1338 b expected transits, development-rows-unchanged check | local files | needed before the sealed search can start (not the search itself) | about 1 hour of machine time, 6 workers | running |
| 2 Nov, 03:28 Kuwait | Vesper 0.9 study: full development-slice search (301 stars) with switches c6,dg,nd,fl, then planted-dip recovery on 300 development star-sectors | local files (data\g2, development slice), no download | judge the new switches on development only; rules in research/stage3/V9-STUDY-PLAN.md | about 1 to 3 GB of run files | running: 5 processes at BelowNormal, expected 1 to 1.5 hours; status in research/stage3/v9-study-status.txt |
