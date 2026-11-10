# Fable's take on Second Sun, and three ideas (10 Nov 2026)

For Ahmed, and for Sonnet 5.5 or Opus 5.5 picking this up cold. Plain words. Evidence is in `REPORT.md`, `findings-*.md` and `evidence/` in this folder. Labels are written in words.

## What we found
The frozen filter (Vesper 0.8.1, Petrova) deletes planet dips in slow binaries before it searches. The eclipse mask (`pipeline/detect_v2.py`, `eclipse_mask_auto`) calls any low spot in one sector an eclipse. In a slow binary each orbit phase is seen once, so a planet's dip is "an eclipse" and is cut. Confirmed on real G2 light: a strong 8 hour dip planted the way a real planet arrives (before the mask) is found 0 times in 25 for binaries slower than 20 days, 3 in 25 at 14 to 20 days, 7 in 25 at 10 to 14 days. Planted after the mask, which is how every one of our recovery tests did it, all are found. That is why three hunts and many reviews never saw it.

The clue was on the page for weeks: upside-down events outnumbered real ones, more at higher strength, logged as "cause not studied". Binned by binary period it is 0.95 to 1 under 10 days and about 3 to 1 over 20 days.

## What it means for the past
The three empty hunts were not three fair tries. For binaries slower than about 14 days (38% of G2 sealed star-sectors, 16% of G3) the search was close to blind to deep transits. Eight of the twelve known transiting circumbinary planets orbit binaries slower than 18 days. The sealed verdicts stand as filed; what changes is how much they exclude. Completeness, the Horizon reach map and the Census odds are all too optimistic about reach for slow binaries, and the nulls pull the believed planet rate down less than we wrote. How much: uncertain until measured through the whole chain (work order WO-F01 part A).

## What is wasted and what is not
Wasted, honestly: the claim strength of the three nulls for slow binaries; some weeks spent hunting causes of the S2 false-alarm excess inside a design whose two arms were not equal; points spent on reading and on bookkeeping (a 16,000 word RESUME, eight book publishes in one night); about 10 weekly points on 10 Nov when Fable started four expensive helpers to read history.

Not wasted: every star list and every downloaded light curve; the control arm (it is what exposed the fault); the sealed-run and preregistration habit; the recovery harness (it only needs its planting point moved); the Horizon and Census arithmetic (rechecked by another method, it matched to the percent; only its inputs need the mask correction); the lessons, now in the private skill `second-sun-auditor`.

## Is the direction right, and can it find a planet?
The direction was right in spirit and wrong in one place. Yes, it can find a planet, and the chance is better than our notes say for slow binaries, because that light is on disk and nobody has looked at it. It is still more likely than not that the next hunt is empty: the reach is giant planets, a few thousand stars, single transits. Rough, uncertain estimate: fixing the mask before Census is worth about 10 to 16 points of "at least one planet", like adding 600 to 900 stars, for no download.

Where Fable disagrees with the drift of the plan: do not add stars (Census, G5) before Petrova 1.0 exists and has re-searched the slow binaries already held. A bigger list through a blind filter buys nothing.

## How to fix it (order of work for Sonnet or Opus)
1. Measure the loss through the whole chain: `work-orders/WO-F01.md` part A. No approval needed, changes nothing.
2. Finish the new mask: `design/PETROVA-1.0-MASK-DESIGN.md`. The "repeat rule" (an eclipse is a dip that comes back) is tested as a prototype: planted dips come back at 0.8 to 1.0 in every period bin. Still to add and measure: the catalogue window for eclipses seen once, and the single-visit lane. Never edit the frozen files; this is a new version with a new freeze.
3. Make the two arms equal (mirror rule) and move every recovery test to plant into raw light. Tests in `work-orders/WO-F02-F04-F05-F06.md`.
4. Re-search the slow binaries on disk as a new preregistered hunt: `design/SLOW-BINARY-RESEARCH-PREREG-DRAFT.md`. Do not look at any real event in the recovered light before it is filed.
5. Only then Census, ranked by coverage, and G5 after Gaia DR4 (2 December 2026).
Research before building: `work-orders/RESEARCH-ORDERS.md`, RS-016 first (how the professionals mask eclipses).
Ahmed's decisions of 10 Nov are in `03-AHMED-ANSWERS-ROUNDS.md`.

## Three ideas
**1. The leap of faith: binaries that do not eclipse.** Every circumbinary transit search looks only at eclipsing binaries. A planet can cross one star even when the two stars never cross each other, if the system is near edge-on (Martin and Triaud 2015 argued this; from memory, not re-read). Gaia lists a very large number of spectroscopic binaries with periods. They are bright, and they have no eclipses, so the mask problem does not exist for them. To Fable's knowledge no transiting planet is known around a non-eclipsing binary and no TESS search has targeted them (not verified). Rough arithmetic from memory: each star worth perhaps a half to a third of an eclipsing one, the pool perhaps ten times larger. The catch: no eclipse means no proof the system is edge-on, so a single dip is harder to trust; a second key is needed (Gaia radial velocities, the duration key, a second transit). It may be already done or may die on the numbers. Test first: RS-021 in the research orders, about half a point. Dead if the per-star value is under a fifth of the eclipsing value.

**2. The single-visit lane.** In very slow binaries a dip seen once cannot be told from a second eclipse by repetition. The old mask deleted all of them. Keep them, label them, and sort them by whether the dip's length fits the binary's phase (a circumbinary transit is long when the star moves with the planet and short when it moves against it; work order WO-F22). This is how the Kepler planets were recognised by eye; doing it by rule on TESS light is new for us and cheap.

**3. Coverage first.** A star with a year of continuous light (the continuous viewing zones, 8 or more sectors) is worth several 3-sector stars, because a slow planet must cross while we are watching. Sort Census by sectors of light times brightness over binary period, not by brightness alone.

Withdrawn idea, so nobody repeats it: looking for a planet tilting the binary's own eclipses over the years. A planet is too light to move the binary; it is the planet's orbit that precesses.
