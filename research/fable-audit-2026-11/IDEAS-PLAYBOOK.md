# Ideas playbook: the four ideas in detail, for Sonnet 5.5, Opus 5.5 and Ahmed (Fable, 10 Nov 2026)

How to read this: each idea has what it is, why Fable believes it, how to attack it, what to check so it does not fool us, how it can die, and the cost. You have your own judgement; these are the lines Fable would not cross and the traps Fable expects. Evidence files are in this folder. Skill to load first: `second-sun-auditor`.

## Fable's ranking
1. **Idea A, re-search the light we threw away.** Best. Do first. Evidence in hand, zero download.
2. **Idea B, the single-visit lane with the duration key.** Do with A; it is A's vetting half.
3. **Idea C, coverage first.** Cheap, almost no risk; it is a sort order, not a project. Apply to Census.
4. **Idea D, binaries that do not eclipse.** The leap. Half a point of research decides if it lives. Do not build anything before RS-021.
**Scrap:** a planet tilting the binary's eclipses (physics kills it); a separate M-dwarf hunt (46 stars); raising the SNR bar to pass S2 (pays 20% to 30% of reach to fix a number that was within noise); any bigger star list before Petrova 1.0.

One rule above all four: **plant before you look.** No idea below is tested by looking at real events first. Each is tested by planting fake dips into raw light and by counting the upside-down arm. Real events are opened only after the rules are frozen and written down.

---
## Idea A: re-search the slow binaries already on disk
**What.** The frozen mask deleted most strong dips in binaries slower than about 10 days. With the new mask, the G1 to G3 stars with period 10 d or more become a new hunt.
**Why believe it.** `evidence/p01c_real_light.txt` (planted dips: 0 of 25 found over 20 d), `evidence/p01b_real_vs_flip.txt` (real against upside-down 0.95 under 10 d, about 1 to 3 over 20 d), `evidence/d01_mask_v1_prototype.txt` (new rule recovers 0.8 to 1.0). `evidence/k01_known_planets.txt`: on TOI-1338 the new rule returns 5 dips the frozen mask had removed.
**How to attack.**
1. Finish the mask (design note, with Amendment A if the d02 result and question K1 call for it). Module outside the frozen list, new version.
2. Build the completeness table by planting into raw light: period bin x strength x duration x product.
3. Prove the arms are equal on light 0.8.1 already judged and on synthetic light.
4. File the preregistration (`design/SLOW-BINARY-RESEARCH-PREREG-DRAFT.md`), then run once.
**What to check so it does not fool us.**
- Period drift: pooling 7 years at the catalogue period smears a narrow eclipse. TOI-1338 may already show this (question K1 in STATE.md). Measure the primary's phase per sector; if it walks by more than a bin, refit the period or count repeats per cycle with a tolerance.
- Eclipses seen once will flood the real arm in the slowest binaries (d01: 0.65 real against 0.44 upside-down at 20 to 27 d). They must go to the lane or the catalogue window, and the count of what is left must match the upside-down arm.
- Second eclipses of eccentric binaries are not at phase 0.5. Use the catalogue's own secondary phase (Prsa columns `Phis-pf`, `Ws-pf`) and check the convention on 10 stars by eye-number before trusting it.
- Never open a real event in recovered light before filing. Counts only.
**How it dies.** If, after the lane and the window, real over upside-down stays above about 1.25 in slow bins with nothing planted, the mask still leaks eclipses and the hunt cannot be scored. Then fix the mask again, do not loosen the score.
**Cost.** Mask and tests 3 to 5 points, preregistration and run 2 to 3. Sonnet builds, Opus reviews the statistics.

## Idea B: the single-visit lane and the binary-phase duration key
**What.** A dip seen once in a slow binary is either a second eclipse, a planet, or junk. Repetition cannot say which. Physics can: a circumbinary transit is long when the crossed star moves with the planet and short when it moves against it, so for a given binary phase only a range of durations is allowed. Eclipses and junk do not obey that relation.
**Why believe it.** It is how the Kepler circumbinary planets were recognised (Doyle et al. 2011, Welsh et al. 2012; from memory, RS-018 opens the papers). Our TOI-1338 list shows durations from 3 to 20 hours at different binary phases, which is what the key predicts for a real planet and a nuisance for any fixed-duration rule.
**How to attack.**
1. RS-018 first (15 calls): the formula and whether anyone automated it.
2. Write `duration_range(binary period, phase, mass ratio range, star radius, planet period range)` for circular orbits, then eccentric. Units in days throughout; test it on Kepler-16 numbers from the paper.
3. Validate on the published transits of TOI-1338 b and TIC 172900988 b (they must fall inside), then on stored upside-down events (the share falling outside is the key's power). Counts only.
4. Use it as a FLAG (a label on the lane), never as a delete.
**What to check.**
- We usually do not know which star is crossed or the mass ratio: compute the union of ranges and report how wide it is. If nearly every duration is allowed, the key is weak: say so.
- Our duration is a box length from a coarse grid (3 to 20 h) on detrended light; the 2 day detrending shortens long dips (FIX 11). Calibrate "measured box length against true duration" with planted trapezoids before comparing with physics.
- Phase zero must be the primary eclipse in the same time system (BTJD) as the event; check one eclipse by number.
**How it dies.** Under 20% of upside-down events rejected: weak key, keep only as a note on lead cards.
**Cost.** Research 0.3, prototype 1.5 (Opus).

## Idea C: coverage first
**What.** Rank stars by how long we watched them, not only by brightness. A planet with a 150 day orbit crosses once per 150 days; a star with 3 sectors (81 days) often misses it, a star with 13 sectors rarely does.
**Why believe it.** It is already in our own model: `horizon_reach.py` line 86, W = min(1, covered days / planet period). TOI-1338 sits in the southern continuous viewing zone and has 40 sectors.
**How to attack.**
1. From the Horizon outputs compute E per star as a function of sectors (3, 8, 13, 26) at fixed brightness and binary period. One script, no new data.
2. Census score = that E. Sort the candidate list by it; download in that order. The 5,193 stars with 8 or more sectors (option 3 of `CENSUS-STAGE2-OPTIONS`) come before the 1-sector scan.
3. Report how much of the total E sits in the top 10% of stars.
**What to check.** Sectors must be counted from files that load, not from the target lists (a past count was 25% off that way). Adjacent sectors are not independent chances; scattered sectors are. Long coverage also means more eclipses seen, so the repeat-rule mask works best exactly on these stars: a second reason to start there.
**How it dies.** It does not; at worst the gain is small. If the top 10% hold under 20% of E, drop the special ordering.
**Cost.** 0.5 points.

## Idea D (the leap): binaries that do not eclipse
**What.** Search bright spectroscopic binaries (two stars known from their radial velocities, period 5 to 50 d, NOT eclipsing) for circumbinary transits. If the binary is within a few degrees of edge-on, a planet can cross one star although the stars never cross each other.
**Why it could be big.** The pool is far larger and brighter than the eclipsing one, and with no eclipses there is nothing to mask and no eclipse leak. A find would be the first of its kind (to Fable's knowledge; not verified).
**Why it could be nothing.** Per star the chance is lower (most such binaries are not near edge-on), a lone dip on a bright star has many causes, and without eclipses there is no free proof of geometry. Someone may have done it.
**How to attack.**
1. RS-021 (about half a point): the Martin and Triaud 2015 numbers, any prior search, the Gaia counts, and the per-star arithmetic in a script. This decides everything. Dead if the per-star value is under a fifth of the eclipsing value.
2. If alive: a pilot of a few thousand stars from the Gaia non-single-star tables (DR4 after 2 Dec 2026), 2-minute light first. The filter is simpler than Petrova: no mask, both arms, same checks.
3. Second key before any lead: Gaia's own radial-velocity orbit gives the binary phase of the dip, so the duration key (idea B) applies; a second dip; and the star must not be a known single-star planet candidate (cross-match the TOI list).
**What to check.**
- Gaia spectroscopic periods have false solutions and aliases; test the period on TESS light where the star shows ellipsoidal or reflection variation, or accept only solutions with high significance. Never fold or flag on an unchecked period.
- Bright single-lined binaries are ordinary TESS targets: any dip found may already be a TOI or a known false positive. Check before excitement.
- The control arm matters more here, because there is no eclipse-phase logic to lean on. Arms must be equal on the pilot before anything is read.
- Do not let this delay idea A. It is a side bet.
**Cost.** Research 0.5; pilot design 1 to 2; pilot run 2 to 3. Opus for the research and arithmetic.

---
## How to search and test without making new bugs (all four)
- Write the test that could kill the idea before the code that supports it, and run it.
- Every count binned by binary period, brightness, product and era. Never trust a pooled number.
- One script per claim, saved with its output. A claim without a script is a guess.
- When a number surprises you, that is the finding. Stop and look at it before going on.
- If you catch yourself explaining an asymmetry between the real and the upside-down arm with a story, stop: bin it.
- Anything touching the frozen files, a sealed result, or a threshold chosen after seeing events: stop and ask Ahmed.
