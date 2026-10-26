# L1 How big is the dip?

<p class="ss-meta">Level 1 of 6 · 20 min · Maths: fractions, percentages, ppm, squares</p>

!!! plain "In plain words"
    When a planet passes in front of its star, it blocks a small circle of light. How much light it blocks tells you how big the planet is compared with the star. By the end of this level, Ahmed, you'll be able to look at a dip and say "that's planet-sized" or "that's a whole star".

## Why this matters for you
Most dips in your G1 binaries are the two stars eclipsing each other. The first thing you'll do with any new dip, for the rest of the project, is ask: is it deep enough to be a star? This level gives you that test.

## The one idea
The fraction of light blocked is the **[depth](../glossary.md#depth)**:

**depth = (planet radius ÷ star radius)²**

[Radius](../glossary.md#radius) means centre to edge. It's squared because what's blocked is an *area*, and area grows with the square of the size. Double the planet's size and the dip gets four times deeper.

## Try it

<div class="ss-demo" data-demo="depth" markdown>
<label>Planet radius (Earths) <input type="range" min="0.5" max="22" step="0.5" value="1" name="rp"> <output name="rp_out">1</output></label>
<label>Star radius (Suns) <input type="range" min="0.1" max="3" step="0.05" value="1" name="rs"> <output name="rs_out">1</output></label>
<p class="ss-demo__result" aria-live="polite">Depth: 0.0084% (84 ppm)</p>
<div class="ss-demo__lc" aria-hidden="true"><span></span></div>
</div>

<figure class="ss-fallback">
<svg viewBox="0 0 320 120" role="img" aria-label="A flat light curve with one shallow box-shaped dip in the middle">
<polyline class="ss-svg-line" fill="none" stroke-width="2" points="10,30 120,30 128,70 192,70 200,30 310,30"/>
<text class="ss-svg-text" x="10" y="100">Earth and Sun: 84 ppm · Jupiter and Sun: about 1.05%</text>
</svg>
<figcaption>Figure 4.1. A transit is a box-shaped dip. The slider version works when JavaScript is on.</figcaption>
</figure>

## Your exercise (on real data)

!!! exercise "Exercise"
    - **File:** TOI-1338, [sector](../glossary.md#sector) 97, 2-minute [light curve](../glossary.md#light-curve) (`data/wave-3/lk/`).
    - **Command:** `py -3.12 learn/ex-L1.py` (I prepare it; it marks one deep dip and prints its depth).
    - **Write in your journal:** is that dip planet-sized or star-sized, and why?

## Quiz

??? quiz "1. A planet half as wide as its star. What depth?"
    (1/2)² = 1/4 = **25%**. That's far too big for a planet; it's the size of a star. When a dip is that deep, think "[eclipsing binary](../glossary.md#eclipsing-binary)", not "planet".

??? quiz "2. You double the planet's size. What happens to the depth?"
    It goes up **4×** (2² = 4).

??? quiz "3. Why do small red stars help us find small planets?"
    The star is smaller, so the same planet blocks a bigger fraction: the dip is deeper and easier to see.

**Summary:** depth = (planet ÷ star)². Tiny dips (ppm) can be planets; huge dips (tens of %) are stars.

**When you're done, tell Claude: "L1 done, n/3".** Next: [Level 2](index.md#l2) turns a depth back into a size. Back to the [learning track](index.md#l1).
