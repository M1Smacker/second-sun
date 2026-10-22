# Book redesign brief

*Written 2026-10-23 by Claude, from Ahmed's answers to 19 rounds of questions. **Status: waiting for Ahmed's approval. Nothing has been rebuilt.** To approve, reply "approve" or give numbered corrections. A private page with the three font samples and a visual version of this brief: https://claude.ai/artifact/U5HE6UL2Mz1HW4qJVeh6WN (only Ahmed can open it).*

## 1. What Ahmed told me
- The book **forces labs before he can learn**, he **doesn't know where to start**, and **nothing shows where the pieces fit**.
- Going tab, then folder, then folder feels **disconnected**. It feels **empty and bland**, and some things have **no transitions**.
- He doubts the hunt because **the odds are low** (my estimate: about 20%, range 5 to 40%, for a real candidate from G1).
- He wants the book to teach, so **chat should not teach**. Chat is for decisions and status.

## 2. What the rebuilt book will be
A **project diary that also teaches**, read on **phone and PC equally**, in a **dark night-sky look with quiet motion**. A **constellation map** shows where everything fits, labs are **optional**, and every chapter says **where you are**.

## 3. The decisions
| Area | Decision |
|---|---|
| Identity | The book is "a project diary of everything we do". Teaching is built from it. |
| First screen | The constellation map, one big **Start here** button, and a **where you stopped** card |
| Map shows | Chapters, your reading progress, the readiness bar, the candidates counter, the latest field note |
| Top tabs | **3**: **Read** (start here, chapters, review pages), **Hunt** (progress, quests, candidates, field notes), **Reference** (glossary, facts, reading list) |
| Menu | One flat list of the 15 chapters with Part names as dividers. No nested folders. |
| Two paths | **Journey** (curated order following the project, one line "what happened" per stop, linking to field notes) and **Topic** (Parts 1 to 6). Same pages, switchable. |
| Field notes | Stay under the **Hunt** tab only |
| Chapter top | "You are here" map strip, then a **1-minute summary (3 bullets: what, why, what you'll be able to do)**, then a **short story**, then the **plain-words box** |
| Stories | Kepler-16, TOI-1338 b, PH1 b, and our own day-by-day story |
| Maths | Idea in words first, formula small and skippable, then a worked example with real numbers (Ahmed is anxious about maths) |
| Quizzes | Only on **one review page per Part**, not inside chapters |
| Labs | Move to a **Try it yourself** page at the end of each Part. Real output first, commands tucked in a fold. Out of the Next links. |
| Glossary | Tap a word for a small popup with the plain definition and a link for more |
| Progress | A **Mark as read** button, per device. No reminders, no finish line. |
| Next links | Title plus a one-line reason ("Next: why two-sun dips arrive at odd times") |
| Pictures | One of our diagrams at the top of every chapter; a few NASA images (credited) at Part openings |
| Voice | Science parts neutral and textbook-like; story openings and field notes personal. English words only; Kuwait time and a few local examples are fine. Humour only in field notes and story openings. |
| Look | Dark default, light on request, **high contrast**, subtle motion (soft page fades, gentle reveals, map lines draw once), all off for reduced-motion |
| Offline | Kept on iPhone |
| Extras wanted | Audio narration, one-page cheat sheets per Part, four tap-and-drag demos, eyes mode |

## 4. Home page and a chapter page (sketch)
```
HOME                                      A CHAPTER PAGE
[ constellation map: 6 stars, 15 dots ]   [ small map strip: Part 3 of 6 · Chapter 8 of 15 ]
  Start here            Where you stopped Chapter 8 · Our detector
[ Readiness 36/100 ] [ Candidates: 0 ]    1-MINUTE SUMMARY  - what  - why  - you'll be able to
[ Latest field note: ... ]                STORY (short, about 120 words)
                                          IN PLAIN WORDS (2 sentences)
                                          ...sections; formulas small and skippable...
                                          [ Mark as read ]
                                          < Previous (why)        Next: ... (why) >
```

## 5. The three font candidates (samples in the private page)
Free, self-hostable (no outside requests, works offline):
1. **Literata**, a warm serif made for reading on screens.
2. **Inter**, a clean modern sans-serif.
3. **Atkinson Hyperlegible**, built for maximum legibility (fits your high-contrast need).
Today's font, Source Serif 4, is shown for comparison. **Ahmed picks one.**

## 6. Things that conflicted or are open (please rule on these)
1. **The top of a chapter is getting crowded** (map strip, summary, story, plain-words box). My fix: the story stays under about 120 words and the plain-words box shrinks to two sentences.
2. **Diary vs learn-first.** Resolved with two paths; the Journey path needs about 15 one-line entries written by me.
3. **Maths anxiety vs formulas shown:** formulas stay but are small, skippable and always after the idea.
4. **Reply length:** you said "as long as the topic needs" and also "too many words". My reading: no padding; short for status, longer only when content needs it.
5. **Audio narration:** needs a method. Cheapest is a free "read aloud" button using the phone or PC's own voice. Better quality needs a separate tool. Your call, later.
6. **Phone alerts** (candidate, cap, broken, batch ready): the free service is still not set up.
7. **Estimates:** from now on, a number, a range and what would change it.

## 7. Build plan (estimates, not measured; each phase ends with a publish, a Field Note and a 15-minute read-through by Ahmed)
| Phase | What | Points |
|---|---|---|
| 1 Structure | 3 tabs and flat menu, map home, chapter template (map strip, summary, story slot, mark as read, popups, Next with reason), labs to Try it yourself, one review page per Part, Start here, the two paths | 4 to 6 |
| 2 Look and motion | Chosen font, high-contrast tokens, page and section transitions, chapter diagrams | 4 to 6 |
| 3 Story openings | A short real story for each of the 15 chapters | 3 to 5 |
| 4 Demos | Planet size vs dip, two stars and a planet, noise slider, light-curve explorer | 6 to 10 |
| 5 Eyes mode | Blind first, Dip / No dip / Odd / Not sure, known examples mixed in, sitting size chosen each time | 4 to 6 |
| Extras | Cheat sheets, audio | 3 to 5 |

Usage rules: weekly cap **50%, stop exactly at 50%**, stop at a clean edge and update RESUME.md. Weekly usage was 40% on 23 October, so about 10 points remain before the reset on 27 October. Phase 1 fits; later phases are better after the reset. Helpers only for reading and checking. Every big addition goes through Compass first.

## 8. What does not change
Evidence rules (claims, labels, proof), the same-day Field Note rule, the readiness bar and its tests, the two-key rule. **The star hunt stays on hold** until Ahmed says start. When it restarts: eyes mode and new variable stars first; the 136 unmeasured stars are kept and measured; a real candidate goes to a short research note first; the repo stays public with candidate data local until both keys pass; monthly check for rival papers.

## 9. How we'll know it worked
Ahmed reads for 15 minutes and says where he got lost. Anything that confuses him goes to the top of the fix list.
