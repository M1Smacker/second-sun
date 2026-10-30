# 10. Vetting: when does a dip deserve a name?

<p class="ss-meta">Chapter 10 · about 25 min · Maths: percentages, comparing two numbers with an error bar</p>

!!! plain "In plain words"
    Finding a dip is the easy part, because most dips are not planets. Vetting is the set of tests that tries to kill a dip, and only one that survives gets a name.

**What this chapter answers:** how do we tell a planet's dip from all the things that imitate one?

## 10.1 The intuition

A detective with a suspect doesn't ask "could they have done it?" They ask "what else could explain this?" and rule each explanation out. Vetting works the same way. For every dip we list the usual impostors and run a test that each one would fail.

## 10.2 The scientific meaning

**Vetting** means testing a signal against every known **false positive**: something that isn't a planet but makes a planet-like dip. The scale of the problem: of 2,241 TESS planet candidates from the first two years, **565 (about 25%)** were later flagged as false positives {{claim:F-019}}. And those had already passed NASA's own checks.

The usual impostors:

| Impostor | How it fakes a dip | The test that catches it |
|---|---|---|
| Our own binary's eclipses | leftover bits after masking | does the dip repeat at the same point in the binary's orbit? |
| **A different binary in the same pixels** | TESS pixels are huge (~21 arcseconds), so a faint eclipsing pair nearby blends in | does the light's centre shift during the dip? (centroid test) |
| The spacecraft | thruster firings (momentum dumps) make the pointing wobble | is the dip next to a dump or a flagged cadence? |
| Scattered light, asteroids | background changes or a rock crossing the pixels | per-pixel and background checks |
| The star itself | spots, pulsations, flares | does a transit shape beat a wave, a step or a line? |
| Our own software | bad detrending carves a dip | does it survive many different detrendings? |

## 10.3 The technical explanation

### NASA's bar and ours

NASA's SPOC pipeline flags a candidate at **MES > 7.1 with at least 2 transits**; QLP uses **SNR > 9**; a centroid shift of **1 pixel or more** points to a background binary {{claim:F-020}}. The Warwick circumbinary team kept an event only if it survived **at least 18 of 21** different detrendings and a transit model beat a sinusoid, a step and a straight line {{claim:F-021}}.

Our own bar is **stricter on purpose**. A clean record is how an independent citizen scientist earns trust. The rules for a single circumbinary dip (C1 to C11, from the wave 4 research):

| Rule | Test | Pass means |
|---|---|---|
| C1 | strength | SNR ≥ 7 (Chapter 8) |
| C2 | robustness | found in at least 18 of 21 detrendings |
| C3 | shape | a transit model beats sine, step and line |
| C4 | duration | under 1 day, and possible for an orbit outside the stability limit (Chapter 4) |
| C5 | not an eclipse | not at a binary phase shared by 3 or more events |
| C6 | not a neighbour | no centroid shift, no correlated dip in nearby pixels |
| C7 | not the spacecraft | no flagged data in the dip; not just before a momentum dump unless pixel checks clear it |
| C8 | independent data | seen in at least 2 different light-curve products |
| C9 | physical size | implied radius under 2 Jupiters whichever star it crosses |
| C10 | smoking gun | if 2+ dips: timing and duration fit a circumbinary orbit |
| C11 | two keys | Claude's analysis passes **and** you agree |

### The circumbinary smoking gun

One test is special to our quest. A real planet orbiting two stars crosses them while they move. Its transits are **shorter near the binary's primary-eclipse phase and longer near the other** {{claim:F-023}}, and they come at irregular times a three-body model can predict. No fake has that fingerprint. Two dips that fit it are worth more than ten that don't.

## 10.4 Our implementation

Today's pipeline covers C1 (`find_events` in `pipeline/detect_v2.py`), part of C5 (the eclipse mask), part of C7 (the warning flags from `veto`, Chapter 8) and C4's orbit range (`pipeline/stability.py`). The rest is research, not code yet:

- C2 (21 detrendings), C3 (model comparison), C6 (pixel checks), C8 (second product), C9 (size for both stars), C10 (orbit fit): not tested in code.
- The planned output is a one-page **vetting sheet** per event, readable on your phone, with every rule as a pass/fail line.

We ran C6 by hand once, on the TOI-1338 dip of 16 December 2025: the dimming came from the target's own pixels and the light's centre didn't move (0.0 to 0.2σ). That is a manual check, recorded in `research/wave-3-pipeline/`.

## 10.5 Worked example: how TOI-1338 b fooled people for a moment

When TOI-1338 b was being confirmed, some dips in sector 3 looked like transits. They were traced to **pointing jitter just before momentum dumps**, a spacecraft effect, not the planet {{claim:F-022}}. The team found this with pixel-level (PSF) analysis.

That's exactly why rule C7 exists, and why our own veto test (Chapter 8) found fakes clustered near gaps and dumps. The lesson: even professionals meet fakes, and the way out is a **specific test for each impostor**, not a gut feeling.

### Worked example 2: the same impostor in our own data

On 20 October 2026 our pipeline ran on Kepler-16 (a real G1 binary) and flagged one dip in sector 54: about 0.2% deep, 15 hours, SNR 7.8. Treated like a real candidate:

- **C5 (not an eclipse):** the real primary eclipse was at BTJD 2771.73, 13% deep, exactly where the catalogue said; the dip was 4 days later. Pass.
- **C7 (not the spacecraft):** a momentum dump at BTJD 2776.07, **0.41 days after** the dip, with quality flags set around it. **Fail.** This is pointing jitter before a dump, the same impostor as in the TOI-1338 b story.
- **C8 (second product):** QLP shows nothing there. **Fail.**

Verdict: impostor. The lesson for us: the rule was right, but our code checked "within 0.25 days either side" instead of the rule's "up to 0.5 days **before**". The code now follows the rule. Writing the rule down first, then checking the code against it, is how this got caught.

### Known objects and repeats

Before anyone studies a dip, look the star up in NASA's lists: **TOIs** (TESS Objects of Interest, dips that TESS itself flagged; the code KP means "known planet"), the known circumbinary hosts, and the TESS eclipsing binary catalogue. Six of our 549 stars are TOIs, six are known hosts and 53 are in the eclipsing binary catalogue {{claim:F-069}}. None of the dips that survived our rules sits on one of them {{claim:F-061}}. A star with many repeated dips of similar depth is probably a second eclipsing pair hiding in the same pixels, not a planet.

### Leftover eclipses that keep the binary's clock

Some dips survive every flag and still are not planets: they are faint leftover eclipses of the binary itself, for example a shallow second eclipse of a pair on an oval orbit. Their tell is timing. The binary's eclipses repeat on the binary's own clock; a planet orbits more slowly on its own clock, so its crossings land on a whole number of binary orbits only by chance. Vesper v8 adds the **orbit-locked flag**: a dip moves to tier 2 if another first-tier dip on the same star, in a different sector, sits a whole number of binary periods away with a similar length (within 1.6 times) and depth (within 2 times). On the 301 development stars of our second list it moved 49 dips on 7 stars, and the real dips' excess over the upside-down control fell from +65 to +20. Its price is about 0.8% of planted fake planets, flagged by bad luck.

## 10.6 What this lets us conclude, and what it doesn't

- **Passing vetting does not make a planet.** It makes a **candidate**: a dip with no known innocent explanation. Confirmation needs more data, usually from other telescopes.
- **Failing one test doesn't always kill a dip.** Some rules are flags for a closer look (C7 near a dump, for example). Others are hard stops (C9: a "planet" bigger than 2 Jupiters is a star).
- **The path after vetting changed in 2026.** NASA's community candidate site (ExoFOP) now accepts candidates **only after they're published**, in a peer-reviewed journal or a research note citing a published method {{claim:B9}}. So our order is: vetting, two keys, write-up, then upload. That decision is still yours (it's in the decision log).

## 10.7 Check your understanding

The questions for this chapter are on the [Part 4 review page](../parts/part4/review.md).

## Sources
In the [claims register](../claims.md): F-019 to F-023, B9. Full research: `research/wave-4-vetting/report.md`.
