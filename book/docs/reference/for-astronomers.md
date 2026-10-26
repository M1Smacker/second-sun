# For astronomers

<p class="ss-meta">Reference · about 3 min · written 27 Oct 2026</p>

!!! plain "In plain words"
    Second Sun is a small citizen-science project that looks for planets orbiting two stars in public TESS data. It has found no planet and claims none. This page says what is solid, what is not yet, and where to check each statement.

## Who writes this

The book is by Ahmed Hanzala, an independent citizen scientist who is learning astronomy as the project goes, with Claude, an AI model made by Anthropic. Claude writes most of the code and the diary-style text and runs the checks. Ahmed decides what to test, reads the results, and is the human second key on any candidate: both keys must turn before anything leaves the project. Because the book is a diary written to Ahmed, it speaks to "you".

## What has been done

Every line below has a label and a source on the [facts page](../claims.md); the claim number is in brackets.

- **Known planets.** 14 transiting two-star planets are known: 12 from Kepler and 2 from TESS (F-001).
- **The detector.** It flattens each light curve, bins it to 10 minutes and scans boxes 3 to 15 hours long ([Chapter 8](../book/08-our-detector.md)). It re-found the known planet TOI-1338 b in 4 of the 8 sectors with data at the transit; the missed transits had a signal strength of 3.7 to 6.5 (F-014).
- **Honest false alarms.** The same search runs on upside-down copies of the data to count how often noise alone crosses the bar ([Chapter 9](../book/09-fake-planets.md)).
- **How faint is too faint.** We hid six fake two-star planets (33 crossings) in 40 sectors of TOI-1338. The search found 0 of 10 at 4 Earth radii, 8 of 10 at 6 and 10 of 10 at 8 (F-029).
- **The professionals' tool.** We ran STANLEY (Martin and Fabrycky 2021) on TOI-1338. Its best score was 18.4 sigma at 96.11 days, but 28% of all orbits it tried scored above 5 sigma, so its sigma scale is not calibrated (F-045). We say so wherever we mention that number ([Chapter 12](../book/12-stanley.md)).

## What we do not claim

- No planet and no candidate. The hunt on the real target list is on hold, as of 27 Oct 2026.
- No new method. The methods are published; our contribution so far is an open, labelled record of using them, mistakes included ([Chapter 15](../book/15-mistakes-as-lessons.md)).
- Nothing below those limits. In our injection test, no planet of 4 Earth radii was found.
- NASA's ExoFOP takes candidates only after a paper, so we would publish first ([Chapter 14](../book/14-credit-and-publishing.md)).

## How to check us

- Every number on the [facts page](../claims.md) carries a label (VERIFIED, LIKELY, UNCERTAIN or NOT TESTED) and a source. If you find one that is wrong, we want to know.
- The code, the data tables and the tests are public: [github.com/M1Smacker/second-sun](https://github.com/M1Smacker/second-sun) (MIT licence). Open an issue there.
- The [prior work page](prior-work.md) says how this project relates to the published searches.
- The [reading list](reading-list.md) shows how deeply we have read each paper.
