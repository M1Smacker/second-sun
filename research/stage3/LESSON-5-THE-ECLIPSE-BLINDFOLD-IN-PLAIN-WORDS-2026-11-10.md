# Lesson 5: what happened on 10 Nov, in plain words

For Ahmed. No background needed. Read the 30-second version first.

## The 30-second version
- Our search looks at stars that are really TWO stars circling each other. Sometimes one passes in front of the other and the light dips. That is an **eclipse**.
- A planet around both stars would make a **different, smaller dip**. We want those. The eclipses are noise for us, so the search first **covers the eclipses with a blindfold** (the "mask").
- On 10 Nov an audit found our blindfold is **too eager**. For slow binaries it sometimes covers the planet's dip too. So planets we *could* have found were hidden from our own search.
- Our old tests did not notice, because they hid the fake planets **after** the blindfold went on. Hiding them before, like a real planet would be, shows we lose 4 to 6 out of every 10 strong planets.
- We have tried one fix (C0). It keeps the planets but lets real eclipses through as false alarms. A second fix (C1) should handle that. Then we wrap up.
- "We found nothing" still stands. It just proves less than we wrote.

## Words you asked about
- **Eclipsing binary:** two stars orbiting each other, seen edge on, so they take turns hiding each other. Our whole search is made of these.
- **Binary period:** the time for one full orbit of the two stars, for example 14 days. After 14 days the pattern repeats. A "slow" binary has a long period (over about 14 days).
- **Eclipse:** the dip when one star hides the other. Deep and repeating every period.
- **Planet dip (transit):** the small dip when a planet passes in front of one star. Shallower than an eclipse, and it does not repeat on the binary's timetable.
- **Eclipse mask (the blindfold):** we cut out the light around the eclipses so they do not look like planets.
- **Catalogue:** a published list of binaries with a **timetable** for each: the period, when the eclipse happens, how long it lasts. Two catalogues feed us: the **Prsa catalogue** (the TESS eclipsing binary list, used for G2) and the **TTC** (TESS Ten Thousand Catalog, used for G3). Think of them as bus timetables.
- **Planted dip (injection):** a fake planet we hide in real data to test the search. If the search finds it, good. If not, we learn what we would miss.
- **K:** how many times deeper a planted dip is than the normal wobble (noise) of that star. K 25 is a big, clear dip. K 12 is a medium one.
- **m:** the share of planted dips that survive the blindfold. m = 1.00 means none lost. m = 0.40 means six out of ten lost.
- **Real arm and upside-down arm:** our honesty check. We also turn the light upside down, so planet dips become bumps. A real planet dip shows only in the normal light. If both versions give the same number of finds, the finds are just noise. If the two numbers differ a lot, something in our search favours one side, and the check is no longer fair.
- **G1, G2, G3:** our three finished searches (549, 895 and 612 stars). All found no excess of real dips over noise.
- **C0, C1:** just names for two blindfold designs. C0 = use the catalogue timetable. C1 = timetable plus one more rule.

## What went wrong, with a picture
Imagine a guard who watches one month of a slow binary. The old blindfold has no timetable. It looks at the shape of that month, finds the part of the cycle that is low, and covers it, because "eclipses are low".
In a **fast** binary the same part of the cycle is seen several times in the month, so a one-off dip is not mistaken for an eclipse. In a **slow** binary each part of the cycle is seen only **once** a month. So any dip looks like an eclipse, **including a planet's dip**. The guard covers it.
Our old tests hid the fake planets after the guard had already gone home, so the guard never saw them. That is why nothing looked wrong.

## What we measured today
- With fake planets hidden **before** the blindfold (like a real planet), a strong dip was lost **40 to 60 times out of 100** in G2 and G3. For binaries slower than 20 days nearly all of them were lost.
- The same check on the real planet system TOI-1338: found 0.58 of the time before the blindfold against 0.95 after.
- A real planet, TIC 172900988 b: both its published dips are deleted by our blindfold in one data set.
- Tests that cannot fail are useless, so we also **broke our own test on purpose**. It went red each time, as it should.

## What the professionals do
The two closest published searches do not guess the eclipses from the light. They **read the timetable** from the catalogue and cover only those hours. That does not depend on the planet at all, so a planet can never be mistaken for an eclipse. That is C0.

## What C0 did when we ran it
- **Planets kept:** 98 to 100 out of 100 fake planets survive, in G2 and G3. Good.
- **A new problem:** on real data with nothing planted, the normal light shows about twice as many "dips" as the upside-down light (G3: 328 against 134). Some real eclipses are not in the timetable, for example a second eclipse that sits at an odd moment because the orbit is not round. Those leak through, and only the normal side sees them. So our honesty check is no longer fair.
- **A clue:** about half of those extra dips come back at the same point of the binary's cycle. Eclipses come back. Planets mostly do not.

## C1, the next step
Timetable **plus** one rule: "if a dip comes back at the same point of the cycle, treat it as an eclipse and cover it. A dip that appears only once stays visible." And the same rule is applied to the upside-down light, so both sides are treated alike. We test it the same way: fake planets must survive (at least 9 out of 10) and the two sides must come out about equal.

## What it means for the book and the nulls
- "We found no excess of real dips over noise" is still true.
- "Nothing bigger than about 6 Earth radii crossed" is **too strong** for slow binaries. We found 16 places in the book to fix. We fix them once, with the new blindfold beside the problem.
- Census (the big new search): it builds its own list of binaries, so it will also write down each binary's timetable. Then the new blindfold works for it from the start.

## Check yourself
1. Why can a planet's dip be covered by the old blindfold in a slow binary but not in a fast one? (Answer: in a slow binary each part of the cycle is seen once, so a one-off dip looks like an eclipse.)
2. Why did our old tests miss it? (They hid the fake planets after the blindfold.)
3. What is the upside-down light for? (A fair check: real planet dips should not show up there.)
4. Why is C0 alone not enough? (Eclipses missing from the timetable leak through as false alarms on the real side only.)
