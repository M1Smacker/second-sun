# 4. Two suns: binary stars and the planets around them

<p class="ss-meta">Chapter 4 · about 20 min · Maths: ratios, powers (squares, cubes, square roots)</p>

!!! plain "In plain words"
    Ahmed, most stars you see aren't alone. Many come in pairs that circle each other. A planet can orbit **both stars at once**, in a wide loop around the pair. These are **circumbinary planets** ("circum" = around, "binary" = pair). Only 14 have ever been caught crossing in front of their stars, so every new one matters. This chapter explains what they are, where they can live, and why we hunt them.

**What this chapter answers:** what is a circumbinary planet, and where around a pair of stars can one survive?

## 4.1 The intuition

Picture two dancers spinning around each other in the middle of a room, holding hands. Now picture a child running in a big circle around both of them. If the child runs too close, the dancers' swinging arms knock them off course. If the child stays far enough out, the dancers just feel like one big blur in the middle, and the child can run in circles forever.

That's a circumbinary planet. The two dancers are the stars. The child is the planet. "Too close" is a real, measurable distance, and the known planets sit just outside it.

## 4.2 The scientific meaning

A **[binary star](../glossary.md#binary-star)** is two stars bound by gravity, each orbiting their shared centre of mass. Astronomers describe a binary with:

- its **period**: how long the stars take to go around each other once (days for the pairs we study);
- its **separation**: how far apart they are (written *a*<sub>bin</sub>);
- its **eccentricity** *e*: how stretched the orbit is (0 = a circle, closer to 1 = a long thin oval);
- its **mass ratio** μ: the smaller star's share of the total mass.

A planet can orbit in two ways:

| Type | Orbits | Example |
|---|---|---|
| **S-type** (circumstellar) | one of the two stars, with the other far away | many planets in wide binaries |
| **P-type** (circumbinary) | both stars together | Kepler-16 b, TOI-1338 b |

We hunt the P-type. The first one caught transiting was **Kepler-16 b** in 2011, a Saturn-like planet on a ~229-day orbit around a pair of stars that circle each other every 41 days {{claim:F-002}}. Since then, only **14 transiting circumbinary planets** are known: 12 from Kepler and 2 from TESS {{claim:F-001}}.

## 4.3 The technical explanation

### How close can a planet get?

Too close to the pair, the stars' changing pull throws the planet out. Holman and Wiegert ran thousands of simulated orbits and fitted a formula for the closest stable distance, *a*<sub>c</sub> {{claim:F-004}}:

<div class="ss-eq" data-eq="Eq. 4.1 · Holman and Wiegert" markdown="1">
*a*<sub>c</sub> / *a*<sub>bin</sub> = 1.60 + 5.10 *e* − 2.22 *e*² + 4.12 μ − 4.27 *e* μ − 5.09 μ² + 4.61 *e*² μ²
</div>

Every symbol, one by one:

- *a*<sub>c</sub>: the critical (closest stable) distance of the planet from the pair's centre.
- *a*<sub>bin</sub>: the separation of the two stars.
- *e*: the binary's eccentricity (0 to about 0.7 for this formula).
- μ = *m*<sub>2</sub> / (*m*<sub>1</sub> + *m*<sub>2</sub>): the mass ratio, the small star's mass *m*<sub>2</sub> divided by the total (0.1 to 0.5 for this formula).

You don't need to memorise it. The lesson is in the result: for the known systems, *a*<sub>c</sub> comes out at **2.5 to 3.5 times** the stars' separation {{claim:F-005}}.

### From distance to time: Kepler's third law

We measure **periods** (time), not distances. Kepler's third law links them: for orbits around the same mass, **period² ∝ distance³**. So the ratio of two periods is the ratio of two distances raised to the power 3/2:

<div class="ss-eq" data-eq="Eq. 4.2 · Kepler's third law" markdown="1">
*P*<sub>c</sub> / *P*<sub>bin</sub> ≈ (*a*<sub>c</sub> / *a*<sub>bin</sub>)<sup>3/2</sup>
</div>

"Raised to the power 3/2" means: cube it, then take the square root. For a distance ratio of 3: 3³ = 27, and √27 ≈ 5.2. So a planet at 3 times the separation takes about **5 times as long** as the binary to go round. Across the known systems the critical period is **4 to 7 times the binary period** {{claim:F-005}}.

### The pile-up

The innermost known planets sit just outside the danger zone, at only **1.3 to 1.6 times** the critical period {{claim:F-006}}. Nature seems to park them right at the edge. That's useful: when we see a pair of stars with a 15-day period, we know roughly where to expect a planet (around 60 to 120 days).

## 4.4 Our implementation

This chapter's ideas become a **search window** in the pipeline. For each G1 binary:

1. Read its period and eccentricity from the Kepler eclipsing-binary catalogue (wave 1c).
2. Compute the critical period from the formula above.
3. Treat planets from about 1 to 10 times that period as the most likely, without throwing away anything outside it.

The formula is coded in `pipeline/stability.py` (about 30 lines). Its function `critical(e, mu)` returns the critical distance ratio, the critical period ratio, and whether *e* and μ are inside the range the fit was made for; `search_window(p_bin, e, m1, m2)` turns that into a range of planet periods to search. Running `python stability.py` checks it against TOI-1338 (next section). Status: VERIFIED (self-check passes).

## 4.5 Worked example: TOI-1338

TOI-1338 is a pair of stars (about 1.1 and 0.3 times the Sun's mass) that orbit each other every **14.6 days** with eccentricity 0.16. Its planet, TOI-1338 b, goes around both every **95.2 days** and is about 6.9 times Earth's size {{claim:F-003}}.

- Critical period: about 4.9 × 14.6 days ≈ **72 days** (the 4.9 comes from the Holman-Wiegert formula with this star's *e* and μ; wave 1a, claim C2).
- Planet's period: 95.2 days.
- Ratio: 95.2 ÷ 72 ≈ **1.3**. Just outside the edge, exactly like the pile-up says {{claim:F-006}}.

This is the star our tools have practised on. In Chapter 8 you'll see our search find one of its crossings in December 2025.

## 4.6 What this lets us conclude, and what it doesn't

- **It lets us** predict where planets are most likely, and recognise that a "planet" closer than the critical period is suspicious.
- **It doesn't** tell us whether a planet exists. Most pairs may have none, and the formula is a fit to simulations with limits (*e* up to ~0.7, μ from 0.1 to 0.5).
- **Fourteen planets is a tiny sample.** Patterns like the pile-up could partly reflect how we search. Papers argue it's real (Martin 2018), but keep the doubt in mind.

## 4.7 Check your understanding

??? quiz "1. What's the difference between an S-type and a P-type planet?"
    S-type orbits **one** star of the pair. P-type (circumbinary) orbits **both**. We hunt P-type.

??? quiz "2. A binary has a period of 10 days. Roughly where would you expect its innermost stable planet?"
    The critical period is 4 to 7 times the binary period: **40 to 70 days**. Known planets pile up at 1.3 to 1.6 times that, so roughly **50 to 110 days**.

??? quiz "3. A planet sits at 4 times the stars' separation. About how many binary periods does it take to orbit once?"
    4<sup>3/2</sup> = √(4³) = √64 = **8** binary periods.

**Next:** [Chapter 5](05-wandering-transits.md): why a two-sun planet's dips don't arrive on a clock.

## Sources
Facts on this page are listed with their sources in the [claims register](../claims.md): F-001 to F-006. Background: Martin 2018, "Populations of planets in multiple star systems", [arXiv:1802.08693](https://arxiv.org/abs/1802.08693).
