# Review: Part 1, The sky and the data

<p class="ss-meta">Check yourself · about 5 minutes · no scores, nothing is saved</p>

!!! plain "In plain words"
    Try each question before you tap it. The answer opens underneath. If one surprises you, the chapter is one tap away.

## Chapter 1: Stars, names and missions

[Read the chapter](../../book/01-stars-names-missions.md)

??? quiz "1. Star A is magnitude 8, star B is magnitude 13. Which is brighter, and by how much?"
    **A**, by 5 magnitudes: **100 times** brighter.

??? quiz "2. Why does our G1 list need both the KIC and the TIC number?"
    The binary's period and eclipse times come from Kepler's catalogue (KIC); the TESS data is filed under the TIC number. We need both to connect the two.

??? quiz "3. A TESS pixel is 21″. A neighbour sits 30″ from our star. Could its light get into our star's pixels?"
    **Yes.** 30″ is less than 2 pixels, and a star's light spreads over a few pixels. That's why Chapter 11 checks where a dip really comes from.

??? quiz "4. What's the BTJD of BJD 2,460,295?"
    2,460,295 − 2,457,000 = **3,295**.

## Chapter 2: Light curves

[Read the chapter](../../book/02-light-curves.md)

??? quiz "1. A dip is 1% deep. Roughly how big is the planet compared with its star?"
    √0.01 = **0.1**, so about a tenth of the star's radius. Around a Sun-sized star, that's about Jupiter's size.

??? quiz "2. What's the difference between SAP and PDCSAP?"
    SAP is the raw summed light; PDCSAP has known spacecraft effects removed. We trust PDCSAP first and use SAP to fill its gaps.

??? quiz "3. TOI-1338's 5% dips repeat every 14.6 days. Planet or star?"
    **Star.** 5% means an object about √0.05 ≈ 0.22 of the big star's radius: the small companion star, eclipsing on the binary's 14.6-day orbit.

## Chapter 3: Our data

[Read the chapter](../../book/03-our-data.md)

??? quiz "1. Why do we need a dip in two different light-curve products?"
    Each pipeline cleans data differently. A dip in only one could be created by that pipeline's cleaning, not by the star.

??? quiz "2. A light curve is 2 MB. Roughly how much space do 550 stars × 10 sectors take?"
    550 × 10 × 2 MB = **11,000 MB ≈ 11 GB**. Easy for D:.

??? quiz "3. Why are TESS's big pixels a problem for planet hunters?"
    A faint eclipsing binary next to our star can sit in the same pixel and leak its dips into our light curve, faking a small planet.

---

[Try it yourself: Part 1](labs.md) · [Back to the chapters](../../start/index.md)
