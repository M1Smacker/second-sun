# 15. Our mistakes, as lessons

<p class="ss-meta">Chapter 15 · about 15 min · no maths</p>

!!! plain "In plain words"
    In the first two days we logged 15 mistakes. None reached anyone outside the project, and each one left a rule behind.

**What this chapter answers:** what went wrong, why, and what each mistake taught us. The full list, with dates and costs, is in `research/mistakes.md`.

## Lesson 1: check numbers against the data, not against your expectations

| What happened | The rule it left |
|---|---|
| An early estimate said we could find planets of 2 to 5 Earth radii. Fake-planet tests showed about 6 | Every "we can see down to X" must come from an injection test (Chapter 9) |
| Kepler-16's one-hour noise was quoted as 236 ppm. Measured the way our search sees the data, it's about 900 {{claim:F-039}} | Measure noise like the detector does; compare with the file's own estimate (Chapter 7) |
| STANLEY's best orbit was reported at 93.8 days; it's 96.1 {{claim:F-045}} | Read an array's order from the data file, not a log message (Lab 8) |
| The G1 rule "morph < 0.5" also let in 136 stars with morph = −1, meaning "not measured" {{claim:F-052}} | Handle missing-value codes on purpose in every selection rule |

**The pattern:** each number looked reasonable, so nobody checked it with a tool that could say "no". Three of these four were caught while **writing this book's labs**, because a lab has to show real output. Teaching is a form of testing.

## Lesson 2: test automation before trusting it

| What happened | The rule it left |
|---|---|
| Timed helper sessions froze about 10 seconds in, on a permission prompt | Run one tiny end-to-end test of any unattended setup while someone can still step in |
| A fix for Avast's certificate checks broke Python's installer; 6 installs failed | After any change that affects every Python start, test the installer immediately |
| STANLEY was about to download data to the full C: drive | Before running someone else's tool, search its code for where it saves files |

**The pattern:** something that works by hand can fail when nobody is watching. Find out while someone is.

## Lesson 3: keep the record clean

| What happened | The rule it left |
|---|---|
| A 1.2 GB tool folder nearly went into git | Ignore every `.venv*` folder; look at `git status` before adding |
| A generated website folder (2.8 MB) was committed | Ignore every `site/` folder; add named paths, not whole trees |
| The facts register `claims.csv` was silently ignored by git, so the book couldn't be rebuilt from GitHub | Check a fresh copy builds; the publish script now does this every time |
| Finish times were written from estimates, not the clock | Read the clock (`date -u`) before writing any time |

## Lesson 4: the code must match the written rule

| What happened | The rule it left |
|---|---|
| Rule C7 says "flag dips up to half a day **before** a thruster firing". The code checked a quarter day either side. Our first G1 dip, on Kepler-16, sat 0.41 days before a firing and slipped through | When a rule is written in words, test the code against an example that sits right at its edge |

## Lesson 5: communicate so you can actually decide

| What happened | The rule it left |
|---|---|
| The project's future story was framed as "Kuwaiti discovers a planet". You're Pakistani, living in Kuwait | Never assume identity from location. Credit line: Ahmed Hanzala, independent citizen scientist (Pakistan), based in Kuwait |
| You were asked to approve "the blueprint with my 3 additions" before the additions were written out | Write out everything being approved before asking |
| An overnight session ended on a question box and nothing ran until morning | Overnight work states its defaults and keeps going; questions wait in the report |

## What the mistakes have in common

- **None was hidden.** Each was logged the day it was found, with its cost, and corrected where it appeared (the book included).
- **Most were caught by a check that could disagree:** a lab's real output, a fresh-copy build, a test at the edge of a rule.
- **Each left a rule**, and the rules are why the next mistake is a different one.

## Check your understanding

The questions for this chapter are on the [Part 6 review page](../parts/part6/review.md).
