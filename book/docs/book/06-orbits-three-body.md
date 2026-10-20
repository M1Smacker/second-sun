# 6. Orbits and the three-body problem

<p class="ss-meta">Chapter 6 · about 20 min · Maths: squares, cubes, cube roots, speeds</p>

!!! plain "In plain words"
    Two stars circle their shared balance point; a planet circles both. Because the stars keep moving, the planet finds them in a different place each time it comes round, so its crossings arrive early or late and last longer or shorter. Three bodies pulling on each other have no simple formula, so we let a computer move them step by step: an **N-body simulation**. That's what STANLEY does, and why it can predict crossings that look random.

**What this chapter answers:** how do orbits work, why can't we just write down when a two-star planet will cross, and how far from the stars can a planet survive?

## 6.1 The intuition

Two dancers hold hands and spin. They turn around a point between them, closer to the heavier dancer. A third dancer jogs in a big circle around both. Each time the jogger passes the front of the room, one of the spinners is somewhere different: sometimes in front, sometimes behind, sometimes moving the same way as the jogger, sometimes the opposite way.

If you were timing "jogger passes spinner A", your times would jump around, and how long the jogger stays in front of A would change too. That's a two-star planet's transit.

## 6.2 The scientific meaning

- **The balance point (barycentre).** Two stars orbit their common centre of mass. The heavy star makes a small circle, the light star a big one.
- **Kepler's third law.** The farther out an orbit, the longer it takes, in a fixed way that depends on the mass inside it (Eq. 6.1). Johannes Kepler found it in 1619; Newton explained it with gravity.
- **Eccentricity (e).** How stretched an orbit is: 0 is a circle; TOI-1338's stars have e ≈ 0.16 {{claim:F-047}}. In a stretched orbit the two eclipses are **not** half an orbit apart. In Lab 5 they're 0.453 apart {{claim:F-046}}.
- **The three-body problem.** Two bodies: a neat formula (an ellipse) for all time. Three: no general formula exists. You calculate the forces, move everything a tiny step, and repeat. That's an **N-body simulation**.
- **Stability.** Too close to the two stars, a planet gets thrown out or swallowed. Holman and Wiegert (1999) measured the closest safe distance with thousands of simulations {{claim:F-004}}. For known two-star planets it's 2.5 to 3.5 times the stars' separation {{claim:F-005}}, and many known planets sit just outside it {{claim:F-006}}.
- **Precession.** The planet's orbit slowly wobbles like a spinning top, so its crossings switch on and off over years ({{claim:F-009}}, Chapter 5).

## 6.3 The technical explanation

### Kepler's third law

<div class="ss-eq" data-eq="Eq. 6.1 · Kepler's third law" markdown="1">
*P*² = *a*³ / *M*
</div>

- *P*: orbital period in **years**; *a*: orbit size in **AU** (the Earth-Sun distance); *M*: total mass inside, in **Suns**.
- **TOI-1338's stars:** *P* = 14.6 d = 0.0400 yr, *M* = 1.4 Suns. *a*³ = 1.4 × 0.0400² = 0.00224, so *a* = **0.131 AU**.
- **Its planet:** *P* = 95.2 d = 0.261 yr. *a*³ = 1.4 × 0.261² = 0.0951, so *a* = **0.457 AU**: 3.5 times the stars' separation.

### The closest stable orbit

Holman and Wiegert give the critical distance *a*<sub>c</sub> as a formula in *e* and the mass ratio μ = *m*<sub>B</sub> / (*m*<sub>A</sub> + *m*<sub>B</sub>). Converting it to a period with Kepler's law:

<div class="ss-eq" data-eq="Eq. 6.2 · critical period" markdown="1">
*P*<sub>c</sub> / *P*<sub>bin</sub> = (*a*<sub>c</sub> / *a*<sub>bin</sub>)<sup>1.5</sup>
</div>

- For TOI-1338 (*e* = 0.16, μ = 0.21): *a*<sub>c</sub> / *a*<sub>bin</sub> = 2.87, so *P*<sub>c</sub> = 2.87<sup>1.5</sup> × 14.6 d = **71 days**.
- The planet's 95.2 days is **1.34 times** that {{claim:F-006}}: close to the edge, like most known two-star planets.
- **For G1 this sets where to look:** planets shorter than *P*<sub>c</sub> can't exist, so the search starts there.

### Why crossing times and lengths change

A crossing lasts about **(star's width) ÷ (planet's speed relative to the star)**. Both bodies are moving:

- Star A's speed around the balance point: its orbit radius is 0.131 AU × (0.3 / 1.4) = 0.028 AU = 4.2 million km, covered in 14.6 days: about **21 km/s**.
- The planet's speed: 2π × 0.457 AU in 95.2 days: about **52 km/s**.
- Moving the same way: 52 − 21 = 31 km/s (a slow, **long** crossing). Opposite ways: 52 + 21 = 73 km/s (a fast, **short** one).

So one planet's crossings can differ in length by a factor of about 2. TOI-1338 b's first crossings lasted between about 0.3 and 0.6 days {{claim:F-008}}. And because star A is somewhere different on its little circle each time, the crossing **time** shifts by hours to days {{claim:F-007}}.

### An N-body simulation, step by step

1. Put the three bodies at their starting positions with their speeds.
2. Work out the gravity force on each from the other two (Newton: force ∝ mass × mass ÷ distance²).
3. Move every body a tiny time step, update speeds, repeat millions of times.
4. Whenever the planet passes in front of a star along our line of sight, record the time and the length of the crossing.

Real codes like **REBOUND** (Rein and Liu 2012) use clever stepping rules that stay accurate over years. STANLEY uses REBOUND.

## 6.4 Our implementation

| Where | What |
|---|---|
| `pipeline/stability.py` | `critical(e, mu)`: the Holman-Wiegert formula. `search_window(...)`: the planet periods worth searching for a binary. Self-check: TOI-1338 gives 71 days |
| STANLEY's `TransitTiming_nbody_lite` | the N-body crossing finder (REBOUND, step by step) |
| `pipeline/stanley/inject_cbp.py` | uses that crossing finder to make realistic fake planets (Chapter 9) |

## 6.5 Worked example: TOI-1338's numbers

| | Value | From |
|---|---|---|
| Stars' orbit | 14.6 d, *e* 0.16, 0.131 AU apart | Kostov et al. 2020 {{claim:F-047}}; Eq. 6.1 |
| Eclipses | 0.453 of an orbit apart (not 0.5: eccentric) | your Lab 5 {{claim:F-046}} |
| Closest safe planet | 71 days | Eq. 6.2, `stability.py` |
| Planet | 95.2 d, 0.457 AU, 1.34 × the limit | Kostov et al. 2020; Eq. 6.1 |
| Crossing lengths | about 0.3 to 0.6 days | {{claim:F-008}}; speeds above explain a factor of about 2 |
| Orbits aligned | within about 1° | {{claim:F-047}} |

## 6.6 What this lets us conclude, and what it doesn't

- **We can:** say where a two-star planet can live, and why its crossings wander and change length.
- **We can't:** predict an **unknown** planet's crossings without guessing its whole orbit. That's why STANLEY tries thousands of orbits (Chapter 12).
- **Simplification we use:** our fake planets are flat (same plane as the stars) and never cross the smaller star (Chapter 9). Real ones can be slightly tilted.

## 6.7 Check your understanding

??? quiz "1. A planet orbits a pair of 1-Sun-total stars at 1 AU. How long is its year?"
    *P*² = 1³ / 1 = 1, so **1 year**. Same as Earth around the Sun: Kepler's law only cares about the total mass inside.

??? quiz "2. Why are TOI-1338's two eclipses 0.453 of an orbit apart, not 0.5?"
    The stars' orbit is **eccentric** (stretched). The stars move faster when close together, so the time from one eclipse to the next is shorter one way round.

??? quiz "3. A binary has a critical period of 50 days. Should we search for planets with 30-day orbits?"
    **No.** Planets that close would be unstable and wouldn't survive. Start at 50 days.

??? quiz "4. Why might one crossing last 6 hours and the next 12?"
    The star moves too. When it moves the same way as the planet, they pass each other slowly (long crossing); in opposite directions, quickly (short crossing).

**Next:** [Lab 5: two suns up close](../labs/lab5-two-suns.md), then Part 3, starting with [Chapter 7](07-noise-and-statistics.md).

## Sources
In the [claims register](../claims.md): F-004 to F-009, F-046, F-047. Background: Holman and Wiegert 1999 (AJ 117, 621); Rein and Liu 2012 (REBOUND, A&A 537, A128); Kostov et al. 2020 (AJ 159, 253); all checked on ADS.
