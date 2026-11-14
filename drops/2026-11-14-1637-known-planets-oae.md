---
type: finding
node: 1.1
date: 2026-11-14 16:37
label: CONFIRMED
status: done
by: Claude
links: [research/stage3/rs025/HELD-AND-MISSED-RESEARCH-2026-11-14.md, research/stage3/rs025/rs025_q5_known.py, data/t109/toi1338_q5.csv]
ids: [OAE (fairness fix for the dominated rule), RS-025 Q5 (known planets under the new rules), TOI-1338 b, TIC 172900988 b]
supersedes: []
---
**Plain:** The fairness fix lets two more real TOI-1338 b transits through (6 of 13 instead of 4), but it can let a planet's stronger transit hide its weaker one.
**Why it matters:** the fix helps a real planet, not only planted ones; its one side effect is now explained.
**Explanation:** Sectors 89 and 93 were held because a rival event was as strong; under OAE eclipse-labelled rivals no longer count. TIC 172900988 b has two transits 4.95 d apart; OAE counts the stronger one as a rival of the weaker. No effect today (both held by edge flags), but it matters once those are fixed.
**Technical:** identity 10 of 10; single-transit tier-1 31% to 46%; mask timing change cannot touch TOI-1338 (term at most 0.005 d). Refinement idea (NOT TESTED): ignore a same-sign rival matching depth and duration.
