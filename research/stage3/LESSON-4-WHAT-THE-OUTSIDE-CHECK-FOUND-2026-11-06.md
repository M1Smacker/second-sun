## Lesson 4: what the outside check found, and what it changed

Ahmed, this lesson is about the evening a second model read my work and found two things I had gotten wrong. I want you to see them in plain words, because they show how a project like ours can be wrong in a way that no test of the code would ever catch. The code ran fine both times. It was the idea behind the code that was off.

Remember what the reach map is for: it says how many planets our searches could have seen if planets like Kepler's were out there. It had no factor for the chance that a planet actually crosses in front of a star, even when the pair of stars eclipses each other. On 4 Nov I added a factor with a probe, and I told you our nulls were "consistent with Kepler in most cases, not in the most optimistic corner". The second model, Opus 5.5, was given only the files and a written brief, with none of my conclusions, and it checked that work. It found nine real problems. Two of them change a conclusion.

The first is about a photograph and a film. A planet's orbit slowly wobbles over years, so a planet that is tilted a little will sooner or later line up and cross its star. My tilt test counted that "sooner or later" as a yes. But a TESS sector is 27 days. It is a photograph, not a film. In a photograph, a small tilt pushes some planets out of the thin strip of sky where we would see a transit just as often as it pushes others in, so the chance barely changes. The auditor simulated 3,000 pretend binaries per row and got 0.135 with no tilt and 0.124 to 0.143 with 1 to 3 degrees of tilt. My rule would have said 0.42 at 3 degrees, three times too big. I had even written in my own note that the photograph was the right picture, and then my script used the film. That is why the "about 1% chance in the most optimistic corner" idea is gone.

The second is about a number that has to be perfect. To decide whether a planet crosses a star I had used how long each star's eclipse lasts. The decision hangs on that width being right to about one percent, and we know the widths to ten or thirty percent. Worse, for about 12% of the stars in the biggest set the width we read was longer than a central eclipse can physically be, so my code quietly set it to a central eclipse, and a central eclipse counts as "the planet will certainly cross". So my factor was mostly tracking how many widths had been clipped, not geometry. The fix is simpler and sturdier: use only the binary's period, which we know well. It gives a factor of about 0.10 to 0.16 for planets at 77 to 139 days.

What stands is the bigger story. The geometry condition itself was derived again from scratch and a 3D simulation agreed with it. Every headline number in the earlier notes recomputed from the saved outputs. With the corrected factor, our four searches expected about 1.5 to 3.3 planets at Kepler's rate and found none, which happens by chance 4% to 23% of the time. So the plain message holds: the nulls are consistent with Kepler's rate, and the searches could not test it. The one thing that changes it is the closest-in planets: if planets existed at ratios closer than any we have seen, our nulls would exclude Kepler's rate, but that is a case I would not bet on. The other change is smaller than I said: 1,400 Census stars add about half to our evidence, not double it. About 3,000 would double it.

I want you to notice one habit. I did not accept the audit because it sounded right. I re-ran its scripts, and the simulation gave the same eight rows and the data check gave the same output. A report is a claim, and re-running it turns it into a result. The whole trial cost about one weekly point for about twenty tool rounds, and it found two conclusion-level problems and seven small ones in about 60 KB of material. That is a hit rate worth having before you decide on the 20-point audit.

There is real reason for hope in this. We found these errors before Census was sized, before any ceiling was quoted as a limit on planets, and the book was corrected the same evening. The system of writing the rule first, labelling every claim and letting someone else try to break it is working.

## Ideas

1. Make an outside check a regular step before every frozen version and before every sealed run, in slices that fit one session each.
2. For the 20-point audit, use the trial's own estimate: about 1 MB of the most science-critical material in depth (the frozen chain and its test harness, the scoring and statistics, the numbers in the book against the saved results), split into about 8 sessions. That estimate is a guess.
3. When one of my notes says "a tilt helps" or "eventually", ask whether it is a photograph or a film.

## Questions for you, no hurry

1. Do you want the 20-point audit scoped that way, in slices of about 6 or 7 points, starting next week after the weekly meter resets?
2. Do you want the simulation explained with a picture in a later lesson?

Next: after you have read Lessons 2 to 4, say which Census stage 2 step to start (or wait), and your S2 and rename answers; I begin the moment you say so.
