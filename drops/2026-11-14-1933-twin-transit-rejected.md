---
type: finding
node: 1.1
date: 2026-11-14 19:33
label: CONFIRMED
status: done
by: Claude
links: [research/stage3/rs024/rs024_twin.py, research/stage3/rs024/twin.json, research/stage3/rs025/HELD-AND-MISSED-RESEARCH-2026-11-14.md]
ids: [OAE (fairness fix for the dominated rule), OAEt (OAE with a twin-transit exemption)]
supersedes: []
---
**Plain:** Letting a planet's look-alike second transit off the "dominated" rule catches 2 more test planets but adds 7 upside-down false alarms, so it is rejected.
**Why it matters:** keeps OAE as it is for Petrova 1.1; the twin-transit side effect stays a known small cost.
**Explanation:** Noise also comes in look-alike pairs, so the exemption frees false events too.
**Technical:** OAE 527 dips, P 48.28%, background 176/83; OAEt 529, 48.46%, 182/90; paired control passes for both.
