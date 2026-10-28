# The first real search

<p class="ss-meta">Start here · about 10 min · no maths</p>

!!! plain "In plain words"
    We searched all 549 two-star systems for planets. **Nothing in the results looks like a planet.** That is an honest result and not a failure: we now know how much junk the telescope's noise makes, how much of it our rules remove, and what a real planet would have to look like to get through. Our best guess is that there is still about a 1 in 10 chance that a findable planet is hiding in these 549 stars.

**What this page answers:** what we did, what we found, how our tool changed because of it, our chance of success, and what comes next.

## What we did

A computer slid a box, from 3 to 15 hours long, along the brightness record of each star and asked: is the light inside the box lower than usual by more than 7 times its normal wobble? If yes, that is a **dip**. We did this for 549 stars, month by month, which gave 5,082 star-months {{claim:F-060}}.

Noise also makes dips. To count how many, we ran the same search on the same data **turned upside-down**. A planet makes a dip, so an upside-down star has no planets in it. Every dip found there is a false alarm.

Before we looked at a single result, we **froze** the rules: every setting and a fingerprint of every file went into a sealed record. After that, no quiet tuning.

## What we found

| Step | Real stars | Upside-down stars |
|---|---|---|
| Dips found | 604 | 869 |
| After our first four checks | 186 | 174 |
| After all our rules (version 4) | 12 | 33 |

If planets were hiding in the real data, the **real** column would beat the **upside-down** column by a clear margin. At the very first step it was a little higher (186 against 174). Those extra real dips were mostly stars with repeating dips and the edges of eclipses, which our later rules removed, and from the second version on the real column was lower at every step {{claim:F-060}} {{claim:F-061}}. The 12 dips that are left sit on 10 stars. None of them is on a star that NASA already lists as a planet host, a TESS planet candidate or a known double star {{claim:F-069}}. Nobody has looked at them with their own eyes yet, and they look like noise.

## The twist: noise is lopsided

You would expect noise to push the light up and down equally. It does not. Stars flare upward, and telescope glitches jump upward more than downward. Turn the picture upside-down and those upward spikes become dips.

So the upside-down search finds **more** fakes than the real search would from noise alone. We measured it on 900 random star-months: at a low bar the upside-down side had 1.25 times as many dips, and at our bar of 7 it had 2.3 times as many {{claim:F-062}}. If planets were there, the real side would catch up. It fell further behind.

What this tells us: there is **no sign of a planet** at this strength, and our upside-down test is a harsh judge, so "real is below upside-down" proves nothing by itself. We found that out by measuring it, not by guessing.

## How our tool looks now, compared with before

**Before (until 24 October):** a detector. It smoothed the light, slid boxes along it and kept dips above 7. A few checks sat on top: is the same dip in a second data product, is there an upside-down dip at the same moment, do many stars dip at once. We had tested it on one known planet and on 50 stars.

**After:** **the detector itself did not change.** We proved it by running it four times: the same 2,642 dips came out every time. What changed is a layer around it that sorts every dip and keeps a record. Each change below came from something the search showed us.

| What we added | In simple words | Why |
|---|---|---|
| Frozen settings | Seal the rules in an envelope before reading any result | So we cannot tune the rules to the answer |
| Tiers | Bins from "best" to "probably junk" (1A, 1L, 1B, 2, 3) | Dips are sorted, never deleted |
| Eclipse overlap | A dip during the two stars' own eclipse is the stars, not a planet. We work out how long the eclipse lasts from the stars' size and orbit, and use measured widths for 40 stars | Our first search found the edges of eclipses and called them dips |
| Repeater flag | Three or more dips in one month cannot be one planet around two stars | A planet there needs at least about 15 days per lap, so only two fit in 27 days {{claim:F-068}} |
| Flat-baseline test | A planet's dip is a box: before and after it the light is normal. A ramp or a cliff is not a planet | Six of our eight strongest dips failed this test |
| Orbit-start ramp flag | Doubt any dip in the first day after TESS resumes recording | TESS is settling then. It costs 14% of the time {{claim:F-064}} |
| Dominated flag | If the strongest dip in a star's data is an upside-down one, the real ones lose | A fair contest with no setting to tune |
| Catalogue labels | Look every star up in NASA's lists of known objects | So nobody studies a known thing |
| Cost measurement | Hide 1,548 fake planets and count how many survive: 83 in 100 of the strong ones | We must know what our rules cost real planets {{claim:F-063}} |
| Aggregates only | Real events stay on your PC. The book shows totals | Nothing leaks before it is vetted |

We also corrected ourselves twice: an idea about "red noise" that the code had already handled, and a "scrambled control" that cannot remove single dips. Both are written down in [Chapter 15](../book/15-mistakes-as-lessons.md).

## Our chance of finding a planet, and how close we are

**Before the search**, our model said about an **18 in 100** chance to find at least one planet in these 549 stars, with a range of 5 to 40 {{claim:F-071}}.

**After the search**, nothing stands out. That does not prove there is no planet. Our rules keep about 7 in 10 of the strong fake planets we hid, so a planet could be in the 3 in 10 we would miss, or be too faint for us. Working it out roughly, there is **about a 1 in 10 chance that a findable planet is still hiding here**. That is my rough arithmetic on top of the model (it could be anywhere from 3 to 20 in 100), not a measured number.

**How close are we?** Think of six steps to a discovery:

1. Build the tools: **done**.
2. Search all the stars: **done**.
3. Get a clean list of candidates: **not yet**. The 12 left-overs look like noise.
4. A person looks at each one (this is what Eyes mode trains you for): **not yet**.
5. Two independent checks agree: **not yet**.
6. Publish, and tell NASA: **not yet**.

We are at step 2 of 6, and step 3 has not given us anything.

## What comes after the 549 stars

These are plans, not promises, and each needs your say first.

1. **Fix what the search taught us.** Search for dips up to 20 hours long (our limit now is 15, and long planets are missed), set a false-alarm level for each star the way NASA's Kepler team does, and test how well we find faint planets.
2. **Search more stars.** TESS itself found 4,584 two-star systems in its first 26 sectors. A professional team searched 512 of them, the well-separated ones with orbits longer than 7 days, and found one weak candidate {{claim:F-070}}. Only 30 of our 549 stars are in their starting list of 591 {{claim:F-072}}, so the two searches mostly cover different stars. The next step is to run both on the stars we share and compare.
3. **Search for pairs of dips.** We never built that.
4. **If a dip survives all of it:** people look at it, two independent checks, then publish.

## What to learn next

The new ideas from this week are in the book now, and in the [learning track](../learn/index.md), so you can catch up in order:

- [Chapter 7](../book/07-noise-and-statistics.md): lopsided noise, heavy tails, and why a scrambled control is the wrong control.
- [Chapter 8](../book/08-our-detector.md): flags, tiers and frozen settings.
- [Chapter 9](../book/09-fake-planets.md): completeness.
- [Chapter 10](../book/10-vetting.md): known objects (TOIs) and repeaters.
- [Chapter 15](../book/15-mistakes-as-lessons.md): two new lessons, "a check that cannot fail proves nothing" and "look it up before you believe it".
- The [glossary](../glossary.md) has every new word. The day-by-day details are in the [field note for 27 October](../field-notes/2026-10-27.md).
