# Brief 018: fact-check Twinlight lessons 1.4, 2.1 and 2.2 (Claude, 15 Nov 2026, early morning; Ahmed asleep, Claude reviews)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why
Your brief 017 audit caught real errors in lessons 1.1 to 1.3 (medians against a mean rule, too-strong claims); all were fixed (commit b7e9bdbb). Three new lessons need the same independent check before Ahmed reads them: `book/docs/learn/u1/l4-what-a-dip-looks-like.md`, `book/docs/learn/u2/l1-orbits-and-periods.md`, `book/docs/learn/u2/l2-how-long-a-dip-lasts.md`. Also, the answer checker in `book/docs/assets/learn.js` was changed (an absolute tolerance alone no longer gets a 2% relative one).

## Do
1. **Fact-check the three lessons independently**, exactly as in brief 017: recompute every measured number from the FITS files in `data/known/172900988/` with your OWN script (do not import `book/tools/lesson_plots.py`): lesson 1.4 uses the sector 21 QLP file (`hlsp_qlp_tess_ffi_s0021-...`), dips near days 1883.39 and 1888.31, noise 305 ppm, 12 and 14 points within 0.15 d, depths 2,655 and about 1,900 ppm, SNR 30 and 23.3, the eclipse "2 points within 1 percentage point" claim; lesson 2.1 uses sectors 44 to 47 (eclipse middles, period 19.658 d, the two missing eclipses in data gaps, Kepler's-law numbers 0.192 AU, 41 Sun radii, 0.90 AU, Kepler-16 0.70 AU); lesson 2.2 (durations 13.0 h, 2.62 h, 3.95 h, about 11 h for the planet, the 6-hour reading, star and planet speeds near 50 km/s). Every worked example, every problem answer and hint: recompute. Primary sources: open the arXiv abstract pages (Kostov et al. 2021 2105.08614; Doyle et al. 2011 1109.3432; Winn 2010 1001.2010) and quote the supporting or contradicting sentence. Label each CONFIRMED, LIKELY, UNCERTAIN or WRONG with its line; flag true-but-misleading sentences for a beginner. Say plainly if a physics explanation is wrong or oversimplified in a way that would mislead (for example the moving-star explanation of the short dip in 2.2, or V against U shapes in 1.4).
2. **Make the `learn` mode cover every live lesson automatically**: read `assets/data/learn.json` from the built site and test every lesson that has a `url` (not a fixed list), with the same checks as now, plus: for every numeric problem, a value 20% off its answer must be judged wrong.
3. Build and run as in brief 017 (port 8496, profile in `data/astra/018/`): run `learn`, `layout`, `textfloor`.
4. Do NOT edit book pages, CSS, `learn.js`, `hooks.py` or lessons; report defects with page, measurement and likely cause. Claude fixes the book.

## Report
`research/astra/reports/018-report.md`: the fact-check table, each mode's output, every defect, DONE / PARTIAL / BLOCKED. No git commits (the runner commits). Never push. Never open the live site.
