---
type: finding
node: 1.6
date: 2026-11-14 19:20
label: CONFIRMED
status: open
by: Claude
links: [research/stage3/FIX-QUEUE.md, https://heasarc.gsfc.nasa.gov/docs/tess/sector4_summary.html]
ids: [FIX 95 (known spacecraft events not flagged), Codex 011 (mask re-test)]
supersedes: []
---
**Plain:** A known jump in the telescope's pointing in sector 4 makes fake dips and bumps on many stars at once; our filter catches most but not all.
**Why it matters:** each one that slips through is a false alarm in G1.
**Explanation:** At TJD 1413.26 TESS loaded the right guide star table and its pointing shifted about 4 arcseconds. 50 of our sector 4 events straddle that moment; 3 reached tier 1 because only two stars per camera shared the moment, under the 3-star rule.
**Technical:** fix idea: a known-spacecraft-events list from the data release notes, flagged like a momentum dump for both arms; to be measured on T156 and the background meters.
