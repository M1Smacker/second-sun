# The first real search

<p class="ss-meta">Start here · about 10 min · no maths</p>

!!! plain "In plain words"
    We searched all 549 two-star systems for planets, then improved the search step by step (seven versions by 28 October). **Nothing in the results looks like a planet.** That is an honest result and not a failure: we now know how much junk the telescope's noise makes, how much of it our rules remove, and how faint a dip has to be before we are blind to it. A faint planet could still be hiding, because the search is nearly blind to dips weaker than about 6 to 8 times the normal wobble.

**What this page answers:** what we did, what we found, how our tool changed because of it, our chance of success, and what comes next.

## What we did

A computer slid a box, from 3 to 20 hours long, along the brightness record of each star and asked: is the light inside the box lower than usual by more than 7 times its normal wobble? If yes, that is a **dip**. We did this for 549 stars, month by month, which gave 5,082 star-months {{claim:F-060}}. From version 6 on, about 3 star-months in 10 (1,420 of 5,064) were searched twice, once on NASA's cleaned light and once on the raw light of the same file, and a dip found by either version counts.

Noise also makes dips. To count how many, we ran the same search on the same data **turned upside-down**. A planet makes a dip, so an upside-down star has no planets in it. Every dip found there is a false alarm.

Before we looked at a single result, we **froze** the rules: every setting and a fingerprint of every file went into a sealed record. After that, no quiet tuning. Each new version was frozen the same way.

## What we found

| Step | Real stars | Upside-down stars |
|---|---|---|
| Dips found | 1,192 | 1,398 |
| After our first four checks | 284 | 234 |
| After all our rules (version 7) | 21 | 32 |

If planets were hiding in the real data, the **real** column would beat the **upside-down** column by a clear margin. After the first four checks the real column is a little higher (284 against 234). Those extra real dips are mostly stars with repeating dips and the edges of eclipses, which our later rules remove, and after all the rules the real column is lower (21 against 32) {{claim:F-085}}. The 21 that are left sit on 17 stars. None of them is on a TESS planet candidate, a known planet host or a known circumbinary host, and 3 are on stars in the TESS list of eclipsing binaries {{claim:F-085}}. Seven of the 21 are dips that only the raw light shows, and we think those are camera effects, not planets {{claim:F-082}}. Nobody has looked at any of them with their own eyes yet, and they look like noise.

## The twist: noise is lopsided

You would expect noise to push the light up and down equally. It does not. Stars flare upward, and telescope glitches jump upward more than downward. Turn the picture upside-down and those upward spikes become dips.

So the upside-down search finds **more** fakes than the real search would from noise alone. We measured it on 900 random star-months: at a low bar the upside-down side had 1.25 times as many dips, and at our bar of 7 it had 2.3 times as many {{claim:F-062}}. If planets were there, the real side would catch up. It fell further behind.

The raw light is lopsided in a different way. At our bar the two sides are about equal, at higher strength the upside-down side has more, and four of our checks (gap, same moment, repeater, flat baseline) remove a larger share of the upside-down dips than of the real ones {{claim:F-077}}. So for the raw-light half, "real against upside-down" is not a fair test, and we say so rather than quote a difference {{claim:F-082}}.

What this tells us: there is **no sign of a planet** at this strength, and our upside-down test is a harsh judge, so "real is below upside-down" proves nothing by itself. We found that out by measuring it, not by guessing.

## How our tool looks now, compared with before

**Before (until 24 October):** a detector. It smoothed the light, slid boxes along it and kept dips above 7. A few checks sat on top: is the same dip in a second data product, is there an upside-down dip at the same moment, do many stars dip at once. We had tested it on one known planet and on 50 stars.

**After:** **the core of the detector did not change.** Before each new version we proved that the old settings still reproduce the first search exactly (for example 298 events on 50 stars), and that the new rules fail when we break them on purpose. What changed is a layer around it that sorts every dip and keeps a record, and two additions to what it looks at: a longer box and the raw light. Each change below came from something the search showed us.

| What we added | In simple words | Why |
|---|---|---|
| Frozen settings | Seal the rules in an envelope before reading any result | So we cannot tune the rules to the answer |
| Tiers | Bins from "best" to "probably junk" (1A, 1L, 1B, 2, 3) | Dips are sorted, never deleted |
| Eclipse overlap | A dip during the two stars' own eclipse is the stars, not a planet. We work out how long the eclipse lasts from the stars' size and orbit, and use measured widths for 40 stars | Our first search found the edges of eclipses and called them dips |
| Repeater flag | Three or more dips in one month cannot be one planet around two stars | A planet there needs at least about 15 days per lap, so only two fit in 27 days {{claim:F-068}} |
| Flat-baseline test | A planet's dip is a box: before and after it the light is normal. A ramp or a cliff is not a planet | Six of our eight strongest dips failed this test |
| Orbit-start ramp flag | Doubt any dip in the first day after TESS resumes recording | TESS is settling then. It costs 14% of the time {{claim:F-064}} |
| Dominated flag | If the strongest dip in a star's data is an upside-down one, the real ones lose | A fair contest with no setting to tune |
| 20 hour box (version 5) | Also slide a box up to 20 hours long | Long transits around two stars last many hours, and the box stopped at 15 |
| Raw light twin (version 6) | Also search the raw light of the same file and keep a dip either version finds | The cleaned light found 4 of 8 transits of a known planet, the raw light 7 of 8, together 8 of 8 {{claim:F-073}} |
| Common moment (version 7) | Doubt a dip if three or more other stars on the same camera have an event of either kind at the same moment | The old same-moment check only counted upside-down events, so it treated the control differently from the data. The new one treats both alike {{claim:F-079}} |
| Cleaned-light check (version 7) | A dip that only the raw light shows must also show, at strength 3 or more, in the cleaned light of the same file | Camera drift shows in the raw light and the cleaning removes it. Fake dips pass this check 87 times in 100 {{claim:F-080}} |
| Catalogue labels | Look every star up in NASA's lists of known objects | So nobody studies a known thing |
| Cost measurement | Hide 1,548 fake planets and count how many survive: 83 in 100 of the strong ones | We must know what our rules cost real planets {{claim:F-063}} |
| Aggregates only | Real events stay on your PC. The book shows totals | Nothing leaks before it is vetted |

We also corrected ourselves several times: an idea about "red noise" that the code had already handled, a "scrambled control" that cannot remove single dips, and a line in our own report that mixed the two kinds of light and made 33 real dips look unlikely from noise. It now covers the cleaned-light half only: 14 real dips against 15.6 expected {{claim:F-083}}. They are written down in [Chapter 15](../book/15-mistakes-as-lessons.md) and the [field notes](../field-notes/2026-10-28.md).

## Our chance of finding a planet, and how close we are

**Before the search**, our model said about an **18 in 100** chance to find at least one planet in these 549 stars, with a range of 5 to 40 {{claim:F-071}}.

**After the search**, nothing stands out. That does not prove there is no planet. We hid fake dips of graded depth in 240 random star-months to measure what we can see. An 8 hour dip is found 61 times in 100 when it is 10 times the normal wobble of 8 hour averages, 22 times in 100 at 8 times, and 2 times in 100 at 6 times {{claim:F-084}}. Our rules then remove about a fifth of the ones found. So a faint planet could easily be hiding here. Our earlier rough figure of "1 in 10 that a findable planet is still hiding" was worked out from strong fake planets and is too hopeful for faint ones. We have no honest replacement yet. It needs the next test: every check included, converted to planet size.

**How close are we?** Think of six steps to a discovery:

1. Build the tools: **done**.
2. Search all the stars: **done**.
3. Get a clean list of candidates: **not yet**. The 21 left-overs look like noise or camera effects.
4. A person looks at each one (this is what Eyes mode trains you for): **not yet**.
5. Two independent checks agree: **not yet**.
6. Publish, and tell NASA: **not yet**.

We are at step 2 of 6, and step 3 has not given us anything.

## What comes after the 549 stars

These are plans, not promises, and each needs your say first.

1. **Fix what the search taught us.** Done so far: dips up to 20 hours long, the faint-dip test, the raw light, and a fairer same-moment check. Still to do: a longer smoothing window for long dips (the current 2 day window keeps only about 57% of a 20 hour dip's depth), the faint-dip test with every check included and converted to planet size, and a fair control for the raw-light half. The per-star false-alarm level of NASA's Kepler team is not built: both controls we have fail for single dips, so there is no honest comparison for it.
2. **Compare with the professionals.** A professional team searched 512 two-star systems of the well-separated kind and found one weak candidate {{claim:F-070}}. Only 30 of our 549 stars are in their starting list of 591 {{claim:F-072}}. We ran their tool on its own on those stars. On the known planet TOI-1338 b it picks up 7 of the 8 transits, but its own vetting step calls 6 of them sinusoids {{claim:F-075}}. The two tools count different things, so a bigger number is not a better tool.
3. **Search for pairs of dips.** A first version exists: it links dips of one star from different sectors. It finds no pair among the 21 first-tier dips. It can only get interesting with weaker dips, which needs a new frozen search.
4. **If a dip survives all of it:** people look at it, two independent checks, then publish.

## What to learn next

The new ideas from this week are in the book now, and in the [learning track](../learn/index.md), so you can catch up in order:

- [Chapter 7](../book/07-noise-and-statistics.md): lopsided noise, heavy tails, and why a scrambled control is the wrong control.
- [Chapter 8](../book/08-our-detector.md): flags, tiers and frozen settings.
- [Chapter 9](../book/09-fake-planets.md): completeness.
- [Chapter 10](../book/10-vetting.md): known objects (TOIs) and repeaters.
- [Chapter 15](../book/15-mistakes-as-lessons.md): two new lessons, "a check that cannot fail proves nothing" and "look it up before you believe it".
- The [glossary](../glossary.md) has every new word. The day-by-day details are in the field notes for [27 October](../field-notes/2026-10-27.md) and [28 October](../field-notes/2026-10-28.md).
