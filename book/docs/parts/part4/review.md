# Review: Part 4, Is it real?

<p class="ss-meta">Check yourself · about 5 minutes · no scores, nothing is saved</p>

!!! plain "In plain words"
    Try each question before you tap it. The answer opens underneath. If one surprises you, the chapter is one tap away.

## Chapter 10: Vetting

[Read the chapter](../../book/10-vetting.md)

??? quiz "1. Why does a centroid shift during a dip worry us?"
    It means the dimming light isn't centred on our star. The dip probably comes from a **different star** in the same big TESS pixel, often a background eclipsing binary.

??? quiz "2. A dip looks perfect but sits 3 hours before a momentum dump. What do we do?"
    Flag it, don't trust it yet. Check the pixels: spacecraft jitter before dumps faked transits during TOI-1338 b's confirmation. Only if the pixel-level check clears it can it pass C7.

??? quiz "3. What's the circumbinary smoking gun?"
    Transit **durations** that change with the binary's phase (shorter near primary eclipse) plus irregular timing that a three-body model predicts. Fakes don't do that.

## Chapter 11: Pixels and neighbours

[Read the chapter](../../book/11-pixels-and-neighbours.md)

??? quiz "1. A neighbour gives 2% of the light and eclipses by 10%. How deep is the dip in our light curve?"
    0.02 × 0.10 = **0.2%** (2,000 ppm): planet-like.

??? quiz "2. Why is a small centroid shift not automatically a problem?"
    Even a dip on the target moves the centre a little, away from the target (Eq. 11.3). The shift must be compared with what's expected and with the chance spread.

??? quiz "3. Why not just divide the centroid scatter by √N for the error?"
    That assumes white noise. Pointing drifts are red noise, so the real error is bigger. Measuring the spread of shifts in same-length quiet windows includes it.

??? quiz "4. CROWDSAP is 0.8. A planet's dip in raw SAP data is 800 ppm. What's the true depth?"
    800 / 0.8 = **1,000 ppm**.

---

[Try it yourself: Part 4](labs.md) · [Back to the chapters](../../start/index.md)
