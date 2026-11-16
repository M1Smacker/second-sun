# X3: is Codex 025's stray-light candidate safe to combine with the 1.1 set? (Fable, 16 Nov 2026)

**Verdict in one line: not yet, and probably not as it stands. The candidate lets the loader keep cadences flagged "scattered light" (quality bit 4096). My own measurement on the same change says that light throws strong events about 8 times as often as the light we search today, on both arms. Unless the tier flags absorb more than nine in ten of those, it breaks Tree rule 1. One number settles it: the tier-1 upside-down count of the untouched background with the candidate on.**

Basis: Codex 025's work log and the top of its report, read in the Codex worktree (branch astra/025-load-losses; it had not landed on main when this was written, and Claude's review notes for it were not there yet), and my F2 prototype (`F2-SILENT-LOSSES.md` section 4), which makes the same loader change for SPOC and TESS-SPOC files.

## What 025 established (CONFIRMED there)
- 21 of 222 Saturn-like T156 dips are lost at load; 15 of them carry bit 4096; "Fifteen archived 4096 cases fail under the original loader, pass with the prototype, and fail when the policy is reverted as a mutation." Loader support is proven. Tier-1 recovery and the background were still pending when the job was cut.

## What F2 adds (CONFIRMED as computed, detector level)
- The loss is bigger than T156 shows and the planet bench cannot see it at all: 404 planted crossings are removed at load (269 by bit 4096) and 175 more QLP crossings are removed because a QLP star takes its safe windows from its own SPOC file's hard mask.
- With the bit admitted, 610 of 754 SPOC crossing-and-file pairs get a score and 215 are clean detections (SNR 7 or more with nothing there before planting). Expected gain 1.0 to 3.1 points of P for the whole family.
- Cost: on 679 SPOC and TESS-SPOC files, strong events on untouched light go from 232 real / 189 upside-down to 747 / 672. In the newly admitted light the rate is 16.9 / 15.5 per 100 days against 1.9 / 1.6. In 82 of 754 pairs an SNR 7 "dip" was already at the planted time before any planet was added.

## Why that matters for combining
- The X10 proposal already sits at 172 real / 66 upside-down against limits of 174 / 79. It has room for 13 more upside-down alarms and 2 more real ones.
- The candidate adds about 480 upside-down strong events at detector level on the files with planted crossings alone. Even if step, ramp and common-moment flags hold 95% of them, about 24 reach tier 1: over the room.
- The two arms rise together (510 real, 468 upside-down in new time), so this is instrument dirt the upside-down meter does see. The meter will catch it; the candidate will most likely fail on it.

## The one measurement that settles it
Untouched background, all design star-sectors, adopted set B with the depth cap, loader candidate on: tier-1 real and upside-down counts, split into "event in newly admitted time" and "elsewhere". Pass line for combining with X10: upside-down added at most 13, real added minus 2.3 x upside-down added at most 5. This is the bench Claude is finishing for 025; read that line first, before any planet number.

Two cautions for reading its planet numbers:
1. Do not use P as defined today: a planet whose crossings were all wiped at load is not in the 1,098, so the gain shows as a change of denominator, not of P (F2 section 1). Use T156 or a raw-observable denominator.
2. T156's 15 cases are one per star-sector; the planet-level gain is smaller than "15 of 222" suggests because many planets have other crossings.

## If it fails as it stands (LIKELY)
Test a guarded form (NOT TESTED): admit a flagged stretch only when the star's own detrended scatter inside it is at most 1.5 times its scatter in the unflagged light of the same sector, same rule on both arms. The 215 clean detections say a real part of the flagged light is usable; the 8-times event rate says most of it is not.

## Label
LIKELY for the verdict (detector-level evidence, tier level not measured by me). CONFIRMED for the event rates and counts.
