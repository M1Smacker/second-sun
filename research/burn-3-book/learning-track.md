# Learning track: a course written for Ahmed (wave 8 design)

*Second Sun, burn 3. Written 2026-10-19 by Claude (Opus 5.5). Follows `research/SITE-BLUEPRINT.md` (adopted 2026-10-19 21:14 UTC): the lesson template in section 3, no XP, ranks, badges or streaks. Level L1 exists as a working page in `site-proto/docs/learn/l1-dip-depth.md`.*

---

## In plain words

Ahmed, this course is written for you only. It takes you from "what is a light curve" to being the **second key**: you check a candidate like SS-0001 yourself and decide whether you agree with me, before anything goes to the professionals. That's your road to a NASA-recognised discovery, with your own judgement in it.

- **Seven levels:** L0 is a short warm-up; L1 to L6 are the course.
- **One weeknight sitting each** (15-30 minutes): a short lesson, one exercise on your project's own data, and three quiz questions you mark yourself.
- **Your data:** TOI-1338, the circumbinary planet we use as our test case, and Kepler-16, a star from your G1 campaign of Kepler-field binaries. Both are already downloaded on the D: drive. I write the code; you run it and read what it shows.
- **Gentle maths,** only what we use: percentages, squares and square roots, magnitudes (a log scale) and orbits. No calculus.

You can do the levels while the hunt runs. L0-L2 are worth finishing before the first G1 batch, and L6 before you turn the second key on SS-0001.

## How progress is tracked

- One quiet line in the book: **"Level 2 of 6 · Next: L3"**, plus a checklist with the date each level was finished, and a separate milestones page for project events. Nothing else: no points, ranks, badges or streaks.
- When you finish a level, you tell me the done line ("L2 done, 3/3"). I set that level's `done:` date in `progress/levels.yml` in the next commit.
- **Coming back after a break:** if 14+ days pass with no session, the two-minute recap links you to the three quiz questions from the last level you finished, as a refresher.

## The lesson template (every level uses it)

1. **Header strip:** level, time, maths it rebuilds.
2. **In plain words** (2-4 sentences).
3. **Lesson:** one idea per section; every technical term links to the glossary the first time it appears.
4. **Demo,** only if it helps (works with JavaScript off: a static figure shows instead).
5. **Exercise box:** the file, the command I prepared (`learn/ex-L#.py`), the one thing to write in your journal.
6. **Quiz:** 3 questions, answers in tap-to-open boxes (`details`/`summary`), self-marked.
7. **Done line:** "When you're done, tell Claude: L# done, n/3."
8. **Next level** link.

Below, each level is written in that order, as the outline Claude turns into a 600-1,200-word page.

---

## L0 Warm-up: what a light curve is

**Level L0 (warm-up) · 15 min · Maths: none, just reading a graph**

**In plain words:** TESS photographs the same patch of sky every few minutes for about 27 days. Measure one star's brightness in every picture, plot it against time, and you have a light curve. A dip means something blocked the light, or the star changed.

**Lesson:**
- What a [sector](glossary#sector) is, and why each one has a gap in the middle (the satellite sends its data down to Earth).
- "Flux" just means brightness.
- Flat means nothing is happening; a dip means something happened.
- Things other than planets that make dips: the two stars of a binary eclipsing each other, starspots, the spacecraft itself.

**Exercise:** run `learn/ex-L0.py`. It plots TOI-1338 (TIC 260128333), sector 97, 2-minute data (`data/wave-3/lk/`). *Write in your journal:* how many deep dips you see and roughly how many days apart they are.

**Quiz:**
1. What's on each axis? → time across, brightness up.
2. Why is there a gap mid-sector? → data download to Earth.
3. Name one thing other than a planet that makes a dip. → e.g. the two stars eclipsing each other.

**Done line:** "When you're done, tell Claude: L0 done, n/3." · Next: L1.

## L1 How big is the dip? *(built as a page)*

**Level 1 of 6 · 20 min · Maths: fractions, percentages, ppm, squares**

**In plain words:** a planet in front of its star blocks a small circle of light. How much it blocks tells you how big the planet is compared with the star. After this level, Ahmed, you can look at a dip and say "planet-sized" or "that's a whole star".

**Lesson:**
- **Why it matters for you:** most dips in your G1 binaries are the two stars eclipsing each other, and this is the test that tells them apart from planets.
- The one idea: [depth](glossary#depth) = (planet radius ÷ star radius)².
- It's squared because area grows with the square of size.
- Earth crossing the Sun blocks 84 ppm; Jupiter crossing the Sun blocks about 1.05%.

**Demo:** depth slider (built; text fallback without JavaScript).

**Exercise:** `learn/ex-L1.py` marks one deep dip in TOI-1338 sector 97 and prints its depth. *Write:* planet-sized or star-sized, and why?

**Quiz:**
1. A planet half as wide as its star? → 25%: a star, not a planet.
2. Double the size? → 4× the depth.
3. Why do small red stars help? → the same planet blocks a bigger fraction.

**Done line:** "tell Claude: L1 done, n/3." · Next: L2.

## L2 From depth back to size

**Level 2 of 6 · 20 min · Maths: square roots**

**In plain words:** a square root undoes a square. So if you know a dip's depth and the star's size, you can work out the planet's size. That number is the first thing anyone at NASA will ask about a candidate.

**Lesson:**
- Planet radius = star radius × √depth.
- Our three rulers: the Earth radius, Jupiter's radius (about 11.2 Earths) and the Sun's radius (about 109 Earths).
- The star's size comes from the TESS Input Catalog; if it's wrong, the planet's size is wrong too.
- Why anything bigger than 2 Jupiters is not our planet (the wave 4 checklist).

**Exercise:** `learn/ex-L2.py` reads the known circumbinary planets from `data/wave-1/nea_pscomppars_cbflag1.csv`. It shows TOI-1338 b's catalogue radius and its star's radius. You predict the depth with the L1 formula; the script then measures it. *Write:* your predicted depth and the measured one, in ppm.

**Quiz:**
1. √0.01? → 0.1.
2. Depth 1%, star = 1 Sun: planet size? → 0.1 × 109 ≈ 11 Earths, Jupiter-sized.
3. Why does a wrong star radius matter? → the planet's size scales with it.

**Done line:** "tell Claude: L2 done, n/3." · Next: L3.

## L3 Bright stars, faint stars, and noise

**Level 3 of 6 · 25 min · Maths: logs and magnitudes; noise falls like 1/√N**

**In plain words:** astronomers measure brightness in "magnitudes", a backwards scale where bigger means fainter. Faint stars give noisier light curves, and noise hides small dips. Many of your G1 stars are faint, so this is why some dips are clear and others vanish.

**Lesson:**
- +5 magnitudes = 100× fainter; +1 magnitude ≈ 2.5× fainter.
- Noise, and binning (averaging neighbouring points): average N points and the noise shrinks by √N, so averaging helps, but slowly.
- 20-second vs 2-minute vs full-frame data.

**Demo (planned):** binning slider.

**Exercise:** `learn/ex-L3.py` compares Kepler-16 (TIC 299096355), sector 82, in two products: SPOC 2-minute vs QLP full-frame (`data/wave-2/lk/`). Then it bins the 2-minute data by 15. *Write:* the scatter (ppm) of each version, and whether binning by 15 cut it by about √15 ≈ 3.9.

**Quiz:**
1. 5 mag fainter = how many times fainter? → 100.
2. Average 100 points: noise shrinks how much? → 10×.
3. Why do faint stars hide small planets? → their noise is bigger than the dip.

**Done line:** "tell Claude: L3 done, n/3." · Next: L4.

## L4 Orbits, and why your dips wander

**Level 4 of 6 · 30 min · Maths: Kepler's third law, P² = a³ (years, AU, a Sun-mass star); speed = distance ÷ time**

**In plain words:** a normal planet crosses its star like a clock. A planet around *two* stars crosses them while they're moving, so its dips come at different times and with different lengths. This is the heart of your main quest, and why NASA's clock-based search misses these planets.

**Lesson:**
- Orbits and periods, in friendly units.
- Transit duration from speed.
- The [circumbinary](glossary#circumbinary-planet) geometry; eclipse timing.
- The stability limit: a planet can't orbit too close to the two stars.

**Demo (planned):** circumbinary orbit with wandering transits. This is the demo worth building, because it shows *why* the dips wander.

**Exercise:** `learn/ex-L4.py` plots planet period against binary period for the known circumbinary planets (from the archive file), so you see them bunch just outside the stability limit. Then it marks the predicted window for a TOI-1338 b transit in sectors 97/98. (If no transit falls there, I fetch a sector that has one: a few MB.) *Write:* is the transit visible, and how does its length compare with the stars' eclipses?

**Quiz:**
1. P = 8 years, Sun-mass star: how far out? → 4 AU.
2. Why don't circumbinary transits repeat like a clock? → the stars move between transits.
3. A "planet" inside the stability limit? → probably not a planet.

**Done line:** "tell Claude: L4 done, n/3." · Next: L5.

## L5 The fakes

**Level 5 of 6 · 30 min · Maths: signal-to-noise; what "3 sigma" and "7 sigma" mean**

**In plain words:** most signals we'll find are fakes: the spacecraft, scattered sunlight, a nearby star's eclipse leaking into ours. Catching them is what makes our real candidates believable.

**Lesson:**
- SNR = depth ÷ noise × √(points in the dip), with coin-flip intuition for sigma.
- The catalogue of fakes (wave 4): blended eclipsing binaries, thruster firings ("momentum dumps"), scattered light, starspots, cosmic rays.
- Odd/even depth differences.
- Centroid shift: if the centre of the light moves during the dip, the dip came from another star.

**Exercise:** `learn/ex-L5.py` shows a deck of 10 real signals from our own downloaded data and pipeline runs: eclipses, systematics and the real TOI-1338 b transit. For each one you choose fake or real and give a reason; the script then shows the answer and the evidence. *Write:* your score and the one that fooled you.

**Quiz:**
1. SNR 4: believe it? → no, too weak.
2. The centroid moves during the dip? → the dip comes from a different star.
3. Two fakes that hit many stars at the same time? → thruster firings, scattered light.

**Done line:** "tell Claude: L5 done, n/3." · Next: L6.

## L6 Two-key vetting

**Level 6 of 6 · 30 min · Maths: nothing new; L1-L5 together**

**In plain words:** before any candidate leaves the house, two keys must turn: my analysis, and your own check. After this level, Ahmed, you're the second key on SS-0001.

**Lesson:**
- Our strict bar, C1-C11 (wave 4, section 4), in plain words.
- The phone vetting sheet.
- What my key covers and what yours means. You answer the ten yes/no questions *before* reading my verdict, because agreeing without looking isn't a key.
- What happens next: an SS number and a nickname, then a write-up. ExoFOP now accepts only published candidates (see `report.md` §3.1), so it goes RNAAS or paper first, then ExoFOP, then the TESS team decides on a TOI.

**Exercise:** vet the SS-0000 practice card, built from the real TOI-1338 b transit (a known planet, so we know the right answer). Fill in the ten questions on your phone. *Write:* your verdict, and the one question you were least sure about.

**Quiz:**
1. What two things must both be true before a candidate gets an SS number? → it passes my automated tests and your independent check.
2. A single event: what extra condition applies? → C11: every check passes with margin.
3. Who must agree before anything is sent anywhere? → both of us.

**Done line:** "tell Claude: L6 done, n/3." · Then: the real hunt.

---

## Writing rules for each lesson page
- Follow the template above and the book design rule: a calm, professional textbook look; no XP, ranks, badges or streaks.
- 600-1,200 words of reading, plus one figure or demo.
- Written to Ahmed by name where natural, with a little warmth ("that dip is 25% deep: that's not a planet, that's a whole star walking past").
- Every number either comes from the claims register or is computed from our own data file in the exercise. Nothing from memory.
- Demos: plain JavaScript, at most 15 KB, loaded only on their own page, with a static figure when JavaScript is off (blueprint section 8).

## Open design questions
- **"Level 2 of 6" with seven levels:** I made L0 an uncounted warm-up. The alternative is "Level 3 of 7".
- **Urdu later:** short, plain sentences, partly so the pages translate well.
