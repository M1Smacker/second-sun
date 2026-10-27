# Stage 3 fix queue (filed 27 Oct 2026; Claude schedules these, Ahmed does not need to ask)

Rule from Ahmed: obvious follow-ups are filed and done by Claude when it judges best, inside the weekly cap (stop line 23% while the cap is 25%). Only item 10 needs him. Every fix is a flag or a labelled measurement unless noted; each new version is tested, mutation-checked, frozen under a new hash and judged by real minus control per tier, never by list length. Source of each item: `learnings-2026-10-27.md` sections 5 and 7.

## Do first (no re-search needed, small); v3 step test DONE 27 Oct (hash 23a74c021d8a); item 1 DONE (report section 5)
1. **Report line: real minus upside-down per tier and per SNR threshold,** written into every aggregate. (Item 5 of the review prompt too.)
2. **Auto-labels on existing events:** star is a TOI, a known planet host, a known circumbinary host or in the TESS eclipsing binary catalogue (tables in `data\xmatch`).
3. **Repeater labels:** for repeater stars, depth scatter and odd/even depths: "periodic blend" if uniform and regular, "variability" if scattered. Label, never discard.
4. **Sixth control and recovery:** use Kepler-1660 as a control; measure recovery of known planets and of trapezoid-shaped injected dips under the frozen version (extend `step_retention.py`).

## v4: one frozen re-search for everything that changes the search or needs it (about 40 minutes of machine time, about 0.5 point)
5. **Red-noise-corrected SNR** (our control finds 869 events where Gaussian noise would find about 0). Biggest expected gain. Check first how `box_scores` computes noise. Model: Kepler's per-target bootstrap that sets the false alarm rate for each star (Twicken et al., arXiv:1501.03586, CONFIRMED in the text); our scrambled and upside-down curves can play the bootstrap's role.
6. **Scrambled control** next to the upside-down one (Kepler's two controls differed by 2x), both reported.
7. **Orbit-start ramp flag:** flag events within about 1 day after each orbit start and gap.
8. **Measured eclipse width** from the TESS eclipsing binary catalogue (53 stars) instead of the formula where available; the formula over-flags by a median 2.7x.
9. **Duration grid beyond 15 h** (events pile at 3 h and 15 h; long circumbinary transits are not searched). Changes the search, so Stage 2 regression is re-proved first.

## Needs Ahmed once
10. **Pair search** (two dips close together) was never built. Default if he does not answer: not built, stated plainly in every report.

## Not now
- Pixel and centroid blend tests: only for survivors, later (needs target pixel files).
- Human review of any event: stays gated behind his own Eyes practice and the real-candidate page.
