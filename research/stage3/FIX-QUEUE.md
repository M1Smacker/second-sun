# Stage 3 fix queue (filed 27 Oct 2026; Claude schedules these, Ahmed does not need to ask)

Rule from Ahmed: obvious follow-ups are filed and done by Claude when it judges best, inside the weekly cap (stop line 23% while the cap is 25%). Only item 10 needs him. Every fix is a flag or a labelled measurement unless noted; each new version is tested, mutation-checked, frozen under a new hash and judged by real minus control per tier, never by list length. Source of each item: `learnings-2026-10-27.md` sections 5 and 7.

## Do first (no re-search needed, small); v3 step test DONE 27 Oct (hash 23a74c021d8a); item 1 DONE (report section 5)
1. **Report line: real minus upside-down per tier and per SNR threshold,** written into every aggregate. (Item 5 of the review prompt too.)
2. DONE 28 Oct (report section 6; 0 of 15 tier-1 events on any catalogue star). **Auto-labels on existing events:** star is a TOI, a known planet host, a known circumbinary host or in the TESS eclipsing binary catalogue (tables in `data\xmatch`).
3. DONE 28 Oct (depth scatter only; the period test was dropped as vacuous). **Repeater labels:** for repeater stars, depth scatter and odd/even depths: "periodic blend" if uniform and regular, "variability" if scattered. Label, never discard.
4. DONE 28 Oct (86.4% completeness ceiling on deep injections; Kepler-1660 gives no tier-1 events; faint-dip recovery still NOT TESTED). **Sixth control and recovery:** use Kepler-1660 as a control; measure recovery of known planets and of trapezoid-shaped injected dips under the frozen version (extend `step_retention.py`).

## v4 DONE 28 Oct (hash d5767e66c4d2: flags only). v5 (next; about 0.6 point; add: faint-dip recovery test, which is the biggest open measurement): everything that changes the search (about 40 to 60 minutes of machine time, about 0.5 to 0.8 point)
5. DONE as a local calibration (v4 dominated flag; the original "red-noise SNR" idea was wrong, see learnings section 11: the SNR already uses the measured scatter of the box statistic). Still open: a per-star bootstrap false-alarm level in the style of Kepler (Twicken et al., arXiv:1501.03586), judged against a scrambled control.
6. WITHDRAWN 28 Oct: a scrambled control keeps single dips, so it is not a null for our search (learnings section 12). Replaced by the asymmetry test, DONE (`asymmetry.txt`): the upside-down control overstates dip false alarms by about 1.3 to 2.5 times. Still to do: report real against upside-down divided by this ratio in every aggregate.
7. DONE in v4 (flag; price 14.2% of the data timeline). **Orbit-start ramp flag:** flag events within about 1 day after each orbit start and gap.
8. DONE in v4 (40 stars). **Measured eclipse width** from the TESS eclipsing binary catalogue (53 stars) instead of the formula where available; the formula over-flags by a median 2.7x.
9. v5 (kept out of v4 so the search stayed identical and the flags are attributable; use 20 h at most, since a 2 d detrending window is 2.4 x 20 h and Wotan says at least 2.2). **Duration grid beyond 15 h** (events pile at 3 h and 15 h; long circumbinary transits are not searched). Changes the search, so Stage 2 regression is re-proved first.

## Needs Ahmed once
10. **Pair search** (two dips close together) was never built. Default if he does not answer: not built, stated plainly in every report.

## Not now
- Pixel and centroid blend tests: only for survivors, later (needs target pixel files).
- Human review of any event: stays gated behind his own Eyes practice and the real-candidate page.
