# Rehearsal in the real layout, version 1 (Eyes ladder rung 3; asked by Ahmed 2 Nov 2026)

**STATUS at the moment work was parked (2 Nov 2026, about 04:00): BUILT AND UNIT-TESTED, NOT YET BROWSER-TESTED, NOT COMMITTED TO THE BOOK, NOT PUBLISHED.** Nothing here is live.

## What it is
Step 3 of the ladder written in `research/decisions.md`: a rehearsal in the layout the real candidates will use, with hidden fake planets, before any real lead is shown. Pass line (fixed before the page existed): 8 sessions of 20 items on at least 4 different days; at least 80% of the clearly visible fake planets called planet-like; at most 15% of everything else called planet-like; d-prime at least 2. Claude decides whether the numbers are enough; the page does the arithmetic.

## What was built (all in the working tree, uncommitted except the generator and this note)
- `pipeline/make_rehearsal_deck.py`: makes `book/docs/assets/rehearsal-deck.json` (8 sessions x 20 items, 1.02 MB) from REAL development-slice TESS light (SPOC/TESS-SPOC PDCSAP). Per session: 3 clear and 3 near-limit fake planets (planted trapezoids, strength 13 to 24 and 6.5 to 9.5 on the hunt's box scale), 3 real eclipses of the binary, 3 instrument effects (ramp after a gap, dip ending at a gap), 2 flares, 2 steps, 4 "nothing hidden" items (the best wiggle the hunt's own box search finds in another part of the sector). The deck holds no TIC, sector or time. Leak audit: `rehearsal-deck-audit.txt` (no simple feature separates planets except the gap fraction, AUC 0.33, which is realistic: instrument effects sit next to gaps and the hunt never keeps events there).
- `book/docs/assets/rehearsal.js`: three panels as in the vetting brief (P1 whole sector with eclipses shaded and the event marked, P2 event zoom on a fixed scale with 6 minute and 30 minute lines and the event bracket, P3 binary phase strip), six answer buttons (Planet-like, Eclipse, Flare, Instrumental, Step, Unclear), optional confidence, lock then truth, keyboard 1 to 6 and Enter, own store (`ss-rehearsal-v1`), cloud upload through the existing uploader as mode `practice`, source `rehearsal-v1` (the published Firestore rules only allow practice, test, real), pass line.
- `book/docs/rehearsal.md`, styles in `shape.css`, nav entry and script in `mkdocs.yml`.
- `book/tools/test_rehearsal.mjs`: 38 checks pass (statistics, pass line, order, store, locked answers, cloud document shape, panels cannot leak the truth, deck integrity, a mutation). It already caught one real defect (neighbouring items from one star) which is fixed.
- `research/burn-3-book/tools/site_check.mjs`: new browser mode `rehearsal` (three screen sizes, six answers, targets 44 px or more, lock then truth, saved at once, keyboard, abandoned session, a whole session of 20). Written, syntax-checked, NOT RUN yet.

## What is left before it can go live
1. Build the book locally (strict), run `site_check.mjs rehearsal` and the layout, offline and JavaScript-off modes against it; fix what they find.
2. Add `test_rehearsal.mjs` and the `rehearsal` browser mode to `publish_book.ps1`.
3. `pipeline/eyes_scores.py`: read rounds with source `rehearsal-v1` separately (today they would be mixed into the practice stats) and print the rung 3 line. Its test must cover it.
4. Book 2.7.0 (a page added): versions row, footer, a field note, a learning-track mention.
5. Commit, then the autonomous publish, then a live check.

## Limits (said now)
Only panels 1 to 3; the second product, background and centroid panels are for a later version. Fake planets are trapezoids in real light, so passing is necessary, not sufficient. After the eighth session the same 160 items return. The deck uses development-slice stars only; no candidate and no hunt event appears in it.
