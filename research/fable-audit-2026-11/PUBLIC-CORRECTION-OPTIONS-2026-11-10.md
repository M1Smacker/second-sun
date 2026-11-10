# Public correction: three options for Ahmed (drafted 10 Nov 2026, NOTHING published, no page changed)

You choose the wording. I publish the book myself only after you pick (book publish rule); emails, posts and real-event data keep their own yes.

## What is actually wrong in public (checked by grep and by script, 10 Nov)
1. **Chapter 9** (`book/docs/book/09-fake-planets.md`): the table in 9.5 and the bullets in 9.6 say our search "reliably finds single crossings of planets about 6 Earth radii and bigger around a star like TOI-1338" and that "nothing bigger than about 6 Earth radii crossed in the searched data ... with about 1 crossing in 11 hidden by eclipses". The test behind it (`pipeline/recover_cbp.py` line 21) builds the eclipse mask from the CLEAN light, then injects. A real planet's dip is in the light when the mask is built, and the mask can delete it. **Measured today on TOI-1338's own 40 files (K-05):** dips injected before the mask are found 0.58 of the time against 0.95 when injected after (m = 0.61); a dip at 25 times the 8 h noise and 8 h long: 0.28 against 1.00. So "1 crossing in 11" and "reliably" do not hold. How the chapter's "6 Earth radii" maps onto my K scale for this star: NOT computed.
2. **4 Nov field note** (`field-notes/2026-11-04.md` lines 19, 47 to 49): "found and kept 44% of the time", "A Jupiter-size dip kept about 60%", and the reach map (13 to 22 planets expected). All measured after the mask, so too high. The note already says the reach map is "too generous" for another reason (transit chance); this adds a second, bigger one.
3. **Claims** F-015, F-029, F-048 (Chapter 9 table) and F-078 (already labelled a ceiling) rest on the same method. **Lab 6** (`labs/lab6-fake-planets.md` line 41, "6 and 8 Earth radii: found every time"): NOT CHECKED whether its injection comes before the mask.
4. **Still true as written:** "no excess of real dips over noise" (versions.md, watch.md, home recap: a statement about real against upside-down, not about reach) and "our four nulls ... cannot test [Kepler's rate]" (home recap). Both only need a scope sentence, not a retraction.

Numbers I would quote (all CONFIRMED by script, `WO-F01-PART-A-RESULT-2026-11-10.md`): over G2 and G3, dips of 12 to 25 times the noise are lost to the mask 31% to 60% of the time; the loss grows with binary period (about a third at 5 to 10 d for deep dips, nearly all beyond 20 d); bumps on the upside-down arm are not lost. Both published transits of TIC 172900988 b in the QLP light are deleted (one star).

## Shared core text (all options use it; plain words, no dashes)
> **Correction, 10 Nov 2026.** An audit found a flaw in how we tested our own search. We added our fake planet dips after the step that hides eclipses, so the test never saw that step delete real dips. When the fake dips go in before that step, as a real planet's would, the search loses 30 to 60 percent of dips that are 12 to 25 times deeper than the noise. The loss grows with the binary's period: about a third for 5 to 10 day binaries and nearly all beyond 20 days. Every "found X percent", "smallest planet" and "reach" number marked below was measured the old way, so read it as an upper limit. Our searches still show no excess of real dips over noise; that is unchanged. What they rule out is much less than we wrote. We are building a new eclipse step and will re-measure.

## Option A: footnotes only (smallest)
- The core text as a boxed note at the top of 9.6 and at the top of the 4 Nov field note.
- 9.6 first bullet becomes: "We can say: our search showed no event of planet size in the searched data apart from the known planet. We can't say how many planets it would have found: on TOI-1338's own light, a dip 25 times deeper than the noise is found 28 percent of the time (8 hour dip), not every time."
- Claims F-015, F-029, F-048, F-078 get the note and move to LIKELY (upper limit). Lab 6: add one line after checking it.
- Home page unchanged. Book version: third number (fix). Cost about 0.3 weekly points with the publish gate.
- For: quick, small, honest where the claim lives. Against: a reader of the home page never sees it.

## Option B: banner, new field note and home recap (full)
- Everything in A, plus a new field note `2026-11-10.md` in the teaching format: the story (what the audit found, how we proved it with fake dips before and after the mask, the bump control, the TOI-1338 and TIC 172900988 b examples), one small table of the loss by period bin, and "what this changes" (the old reach numbers become upper limits).
- Home "Two-minute recap" says it in one line (about 45 words); learning track gets one quiz line on "inject before the step that could delete the signal".
- Book version: second number (a page added). Cost about 0.6 to 0.8 points.
- For: the book stays the honest notebook and the lesson is taught. Against: it publishes a big correction before the fix exists, so readers get a problem without the solution.

## Option C: short holding banner now, full note after the new mask is measured
- Only the core text, shortened to three sentences, as a banner on the home page, Chapter 9 and the 4 Nov note: "An audit on 10 Nov found our test dips skipped the step that hides eclipses; with it included, 30 to 60 percent of strong dips are lost. Numbers below are upper limits; a full note follows when the new step is measured." Claims relabelled.
- The full field note (Option B content) is written when Petrova 1.0's mask is tested, with the before and after in one story.
- Book version: third number now, second number later. Cost about 0.3 now and 0.6 later.
- For: stops anyone leaning on the 6 Earth radii statement today at low cost, and tells the whole story once. Against: two publishes, and "a full note follows" is a promise.

## My take
Option C. The Chapter 9 statement is the one that is simply wrong today, so it should not stay up for weeks; but the lesson reads best with the fix beside it. Option A alone would hide a finding that the home page should carry. If you want the notebook to show problems the day they are found, B.

## Not part of any option (needs its own yes)
Emails, CTOI or ExoFOP, posts, anything outside the book. The G1 to G3 verdicts are not re-scored or re-worded: "no excess" stands as filed.
