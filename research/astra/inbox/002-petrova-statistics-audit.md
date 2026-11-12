# Brief 002: audit Petrova 1.0.0 and the Re-search 1 statistics (the first big judgement)

**From:** Claude Code (first key), 12 Nov 2026. **Model:** GPT-6 Astra, effort **high** (part F at **xhigh**). Do brief 001 first.
**Cap:** this brief may take several sessions. Do the parts in order; after each part append its findings to the report and commit. Stop for the day when your 5-hour bar passes 70%, and leave the rest for the next window. Total cap: about 40% of one weekly bar; if you reach it, report what is left.
**Writes allowed:** `research/astra/reports/002-*.md`, `research/astra/scripts/002_*.py`, `data\astra\002\`, `research/astra/USAGE.md`, on branch `astra/002-petrova-audit`. Read-only on every frozen file and every preregistration.
**Stars allowed for real-light work:** only the 704 `design_seen == 1` rows of `targets/r1_targets.csv`, synthetic light, and the published systems. Fence A and B as in AGENTS.md.

## Why (the decision this serves)
Ahmed must choose what comes next: the G1 re-search (needs Petrova 1.0.1 and Amendment 4), Census, or a better filter first (Petrova 1.1.0, a binary-phase key). Each choice rests on Petrova 1.0.0 being right and on the Re-search 1 null meaning what we say. You are the independent check. Claude built all of it, so Claude's own checks are producer checks, not review.

## Parts
**A. Petrova code (read and test).** `pipeline/petrova_mask.py` and every call site (grep `p1`, `petrova`). For each step ask: does it treat the real arm `f` and the upside-down arm `2 - f` exactly alike? Write a script that runs the mask on synthetic light (eclipses plus noise plus a planted dip, and the same with a planted bump) at binary periods 5, 10, 14, 20, 30, 50 d and one, two and four sectors, and counts kept cadences and surviving dips and bumps per arm. Check the "switch off equals 0.8.1" claim on 3 design-seen star-sectors yourself. Check the cross-sector veto (binary period 13 d or more) on single-visit phases.

**B. Re-derive S1 by another method.** The preregistered S1 rule (Amendment 3 in `research/stage3/R1-PREREGISTRATION.md`) is an exact stratified test by period bin, implemented in `pipeline/r1_readout.py`. Without importing our code, re-compute the G3 and G2 chances (filed: 0.41 and 0.31) from the counts in `research/stage3/R1-RESULT-g3.txt`, `R1-RESULT-g2.txt` and `R1-S1-REFERENCE-BINS.txt`, by Monte Carlo permutation and by your own exact calculation. Re-derive the power lines (about 5.2 times and 2.7 times expected). Say plainly whether the null "no excess beyond the imbalance on the 704 design stars" is a fair test and what it cannot see.

**C. Completeness (S4).** Filed: about 4 in 10 planted strong dips survive the whole chain, CONDITIONAL on the dip lying in light the mask kept. On design-seen stars only, estimate the UNCONDITIONAL completeness: inject into raw loaded flux BEFORE any mask, per period bin, and count tier-1 survivors. Run it in the background with a log, at most 6 workers, `NUMBA_NUM_THREADS=2`. If it would take more than about 2 hours of machine time, run a smaller sample and say so.

**D. The recovered-light imbalance.** Real tier-1 dips outnumber upside-down 2 to 4 times in recovered light (light the old mask deleted and Petrova keeps), on design stars and new stars alike. The suspected cause, eclipse leftovers (eclipse edges only dip), is NOT TESTED. Test it on design-seen stars: where in binary phase do the excess real events sit relative to the eclipse edges (Prsa or TTC widths), compared with upside-down events? Does the excess vanish if you remove a band of k times the eclipse width? This decides whether Petrova 1.1.0 (a binary-phase key) is worth building.

**E. Gates and losses.** Gate (a) is close to guaranteed by design (dips planted in kept light only): say how to make it a real test. G2 gate (c) failed in two bins (14 to 20 d, over 27.4 d): is "not covered" the right handling? G3 skips 24.4% of files as "no safe windows": count by brightness, sector and product (counts only) and say what it costs.

**F. Process review (xhigh).** Read the preregistration and its three amendments as a strict referee. Were any amendments shaped by results they should not have seen? (The record says the S1 problem was found on design stars before any unseen star was read; check the commit times.) Then write what Amendment 4 for a G1 re-search MUST contain, and what a Census search would need that G1 does not.

## Report
`reports/002-petrova-statistics-audit.md` in the mailbox format, plus a closing section **"What I would do next and why"** ranking: G1 re-search, Petrova 1.1.0, Census, other. One paragraph per option, with the evidence from parts A to F.
