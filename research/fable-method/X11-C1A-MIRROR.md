# X11 lever 2: what holds c1a's lost dips (Opus 5.5 Extra, 17 Nov 2026, 5:45 pm; saved files only)

**Verdict in one line: found the cause. 105 of the 133 single dips that c1a loses at tier 1 (79%) are held by the mirror-match flag, because c1a's short detrending window leaves two shallow bumps beside every dip (median 0.8 dip lengths away, 36% of its depth), which the upside-down search sees as dips and calls a mirror. The 71 dips c1a gains are pure detections (B had no SNR 7 event). A ghost-aware mirror rule is therefore the missing half of any shorter-window detrending, but it cannot make c1a pass: c1a's untouched upside-down alarms (111, or 98 with the depth cap) are already over 79, and relaxing a hold can only add alarms. Lever 3 (c1a + ghost-aware mirror) is NOT built.**

Script `data/opus-x11/x11_lever2.py` (copy and output in `research/fable-method/opus-x11/`). Inputs: Codex 027 saved T156 rows with and without c1a, c1a event groups (`generated-g*/T156/trial-N/1`), Codex 003 draws and stored B groups. Rule preregistered in `WORK-LOG-X11.md` (5:43 pm).

## Counts (CONFIRMED as computed; trial counts match Claude's 027 review: 133 lost, 71 gained)
| | Trials | What the run that misses tier 1 shows on the planted dip |
|---|---|---|
| Lost with c1a (B tier 1, c1a not) | 133 | mirror match 105 (78.9%; alone 78, with repeater 18, with step 4, others 5), step 17, repeater 25 (overlapping), no SNR 7 event 4, stored tier 1A but lost in context 7 |
| Gained with c1a (c1a tier 1, B not) | 71 | B had no SNR 7 event at the planted time in all 71 |

Mechanism, the 105 mirror-held dips (CONFIRMED as computed; reading LIKELY): every one has an upside-down event within 1 day in the same c1a run; nearest one at 0.58 / 0.78 / 1.04 dip lengths (10th / 50th / 90th percentile), depth 0.18 / 0.36 / 0.64 of the dip; median 2 such events per dip (one each side). That is the overshoot a short running filter puts on both sides of a box dip.

Decision rule check: mirror match is on 79% of the lost dips (rule: at least half, PASS). Its share among c1a's background events: 12.6% of real-arm SNR 7+ events (2,587 of 20,114), 0% stored on the upside-down arm (PASS: much smaller than 79%). So by the rule a lever 3 would be warranted.

## Why lever 3 is not built anyway (the meter reason, written before any lever-3 number)
- Ceiling: recovering all 105 lifts c1a's T156 single-dip tier 1 from 437 to at most 542 of 2,000, against B's 499: at most +2.2 points over B on T156, and the planet bench P would move from -2.3 to roughly +2 to +3 over B (UNCERTAIN, not scored).
- Rule (b) fails structurally: c1a's untouched background is 186 real / 111 upside-down (K2 + c1a 184 / 98) against 174 / 79, and a ghost-aware mirror rule can only release events, never hold more. Rule (d) also failed by 10 to 12 points of T156 R. So no version of "c1a + mirror fix" can pass the freeze rule without a new alarm cut that does not exist yet.
- What it does give: a design requirement for any future detrending change (the too-faint pool is still the only lever large enough for 0.75): **a shorter window must come with a mirror rule that ignores the dip's own shoulders** (mirror event offset by at least half a dip length AND shallower than about two thirds of the dip), and its alarm cost must be paid by a separate cut.

## Labels
CONFIRMED: counts and the offset and depth distributions. LIKELY: the overshoot reading. NOT TESTED: lever 3, the planet-bench split of the same attribution, the background effect of a ghost-aware mirror rule.
