# Review: Part 3, Finding dips

<p class="ss-meta">Check yourself · about 5 minutes · no scores, nothing is saved</p>

!!! plain "In plain words"
    Try each question before you tap it. The answer opens underneath. If one surprises you, the chapter is one tap away.

## Chapter 7: Noise and statistics

[Read the chapter](../../book/07-noise-and-statistics.md)

??? quiz "1. One point wobbles by 1,000 ppm. With white noise, what does a 4-hour average (120 points) wobble by?"
    1,000 / √120 ≈ **91 ppm**.

??? quiz "2. You measure 400 ppm for that 4-hour average instead. What does that tell you?"
    The noise is **red**: slow drifts that don't average away. A dip must be judged against 400 ppm, not 91.

??? quiz "3. Why does running the search on upside-down data help?"
    It makes the same number of tries on data with no real dips. Whatever it finds shows how often noise alone crosses the bar: the look-elsewhere effect, measured.

??? quiz "4. Why not just flatten with a 3-hour window to get rid of red noise?"
    It would also flatten the planet: a 6-to-15-hour two-star transit would be partly removed.

## Chapter 8: Our detector

[Read the chapter](../../book/08-our-detector.md)

??? quiz "1. Why did v1's 1-day flattening window hurt us?"
    A 6-hour dip is a quarter of a day. A 1-day moving fit partly follows the dip down and "flattens" it away, making it shallower than it really is.

??? quiz "2. Why do we search flipped (upside-down) data?"
    Real dips become bumps, so anything found there is noise or spacecraft effects. It **measures** our false-alarm rate instead of guessing it.

??? quiz "3. The search finds nothing in a star. What can you say?"
    Only that no transit stronger than our bar happened in that data: roughly nothing bigger than ~6 Earth radii for a TOI-1338-like star. Smaller planets, or planets not crossing during that sector, could still be there.

## Chapter 9: Fake planets

[Read the chapter](../../book/09-fake-planets.md)

??? quiz "1. Why must fakes go in before cleaning, not after?"
    Cleaning can flatten part of a real dip. Injecting after cleaning would skip that damage, so the test would look better than reality.

??? quiz "2. 3 of 4 fakes found. What's the uncertainty?"
    √(0.75 × 0.25 / 4) ≈ 0.22: **75% ± 22%**. Four trials are far too few.

??? quiz "3. Why count fakes inside the eclipse mask separately?"
    They show a loss no detector improvement can fix. Mixing them into "missed" would blame the detector for what the mask did.

??? quiz "4. A dip's centre is deeper than (radius ratio)². Why?"
    **Limb darkening:** the star's edge is dimmer, so a planet over the bright middle blocks more light than the average.

---

[Try it yourself: Part 3](labs.md) · [Back to the chapters](../../start/index.md)
