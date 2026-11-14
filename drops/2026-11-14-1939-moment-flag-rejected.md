---
type: finding
node: 1.6
date: 2026-11-14 19:39
label: CONFIRMED
status: done
by: Claude
links: [research/stage3/rs027/rs027_moments.py, research/stage3/rs027/moments.json]
ids: [FIX 95 (known spacecraft events not flagged)]
supersedes: []
---
**Plain:** Finding spacecraft glitches from our own data alone does not work: it would also flag about a quarter of real planet transits.
**Why it matters:** the sector 4 type of false alarm needs a short list of known spacecraft events from TESS's own notes instead.
**Explanation:** With hundreds of stars, ordinary events line up by chance all the time, so "many stars at once" is not a clean signal across cameras.
**Technical:** K=3 other stars, any camera, 0.1 d: background 22 real / 15 upside-down, planted crossings 1,291 of 5,308 at risk.
