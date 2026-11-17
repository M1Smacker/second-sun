# Work log X11 onward (Opus 5.5 Extra, 17 Nov 2026; bench copies only)

Brief: `OPUS-BRIEF-X5-X11-2026-11-17.md`. X5 result: `X5-PATH-TO-075.md` (scorer `data/opus-x11/x5_rule4.py`). Lab-notebook style; every pass rule is written here BEFORE any score of that lever exists.

## Lever 1: combined rule-4-safe releases (5:40 pm, written before scoring)
**Why this lever (one line):** it has the largest measured ceiling per meter point left: the three releases that pass rule 4 alone (dominated +1.45, ramp +1.23, gap edge +0.73 on the 968; X5 table) sum to about +3.4, and scoring them needs only Fable's existing scorer on saved replays (minutes of machine time, about 1 meter point); every other measured pool either fails rule 4 (DS, R2, M2), belongs to Codex 028 (stacking) or has no passing design yet (faint pool, M2 check).

**Configurations, fixed now (all with the depth cap C96, everything else as B):**
- C1 = dominated hold released + ramp hold released
- C2 = dominated released + gap-edge hold released (gap_dump = known event or momentum-dump text, as Fable's "gap-edge" single release)
- C3 = ramp released + gap edge released
- C4 = dominated + ramp + gap edge released
Each is also stored without the cap (diagnostic only) and scored under M2 (diagnostic only).

**Pass rule (all must hold; the five rules of Codex 027 plus the X1 fresh rule):**
- (a) paired gain against B on the 968 possible planets at least +2.0 points with the 95% whole-star lower bound above zero;
- (a2) fresh seed (941 possible planets): paired 95% interval above zero and point at least half of the (a) estimate;
- (b) untouched background: upside-down at most 79 and real at most 174;
- (c) per-bin control: (dip gain minus bump gain against B) has a 99% whole-star interval containing zero in all five bins, on the 968, on all 1,098 and on the fresh 941;
- (d) T156 reference R (the 023 / 027 definition, B = 34.21%) not below B's (point estimate); the scorer must reproduce B's 34.21 first, or (d) is reported NOT TESTED;
- (e) rule 4 against B: new real minus 2.3 x new upside-down at most 5 (match of `x5_rule4.py`).
- **An M2 configuration cannot pass**, whatever its arithmetic: M2's own excess (17.1, 24 unmirrored new real events, most of them eclipses) stays in the list; released noise that adds upside-down events only hides it in rule 4. Fixed now so the M2 rows cannot tempt me later.
- Winner: among passing configurations, the one with the highest P on the 968. If none passes: the lever is closed and the best row is reported as "fails".

**What would prove me wrong:** flags overlap (X6): C4's upside-down count is predicted 53 + 24 + 11 + 5 = 93, over 79, so I expect C4 to fail (b) and C1 to sit near the line (88 predicted). C3 (predicted about 69 upside-down, +2.0 points) is the one I expect to pass, if any.

**Build:** a copy of Fable's harness in `data/opus-x11/` with writes to `data/opus-x11/out` (Fable's guard only allowed `data/astra/fable-f4`), reading the same saved replays (006, 010, 013, 003, 011, fable-fresh, fable-fresh-m2) read-only. Same identity asserts against 013 on the V0 choosing bench (B and DS trial by trial).
- 5:41 pm, amendment BEFORE any lever-1 score: reading `023_summary.py`, Codex's rule (c) is the configuration's OWN paired dip-minus-bump rate per bin (99% interval contains zero), not the gain version I wrote. The brief says "same five rules as Codex 027", so (c) = 027's definition on the 968, all 1,098 and the fresh 941; my gain version is reported as a diagnostic only. (d) uses 023's reference subset: T156 trials with depth 3,000 to 6,000 ppm and length 6 to 12 h (n = 222), equal weight over bins, real arm.

## Lever 2 (queued behind lever 1; written 5:43 pm before any attribution exists): which hold eats c1a's lost dips
**Why (one line):** the faint pool is the only measured pool big enough to matter for 0.75 (X4: +14.8 points of detection under white noise), c1a reached it at the detector (+7.2) and lost it at the tier rules (Codex 027: 133 single dips lost at tier 1, 71 gained), and no one has attributed the losses; the attribution reads only 027's saved files (about 0.5 meter point), and it decides whether any faint-pool lever is worth a bench.
**This is a ceiling measurement, not a candidate.** Data: Codex 027 saved T156 rows (`T156-g*-V0.json` with c1a, `baseline-T156-g*-V0.json` without), c1a event groups in `generated-g*/T156/trial-N/1/`, planted times from Codex 003 rows; baseline events from 003's stored trial groups. For every trial that B finds at tier 1 and B+c1a does not (and the reverse), take the matched planted-arm event (primary product, SNR 7+, centre within half the planted length of the planted time) in both runs and record which hold flags it carries (step, ramp, gap or dump, repeater, dominated as stored, eclipse overlap, c5, mirror match, burst) and its stored tier.
**Decision rule, fixed now:**
- If ONE flag (or one pair) is on at least half of the lost dips that c1a still detects, AND that flag is on a smaller share of c1a's new upside-down tier-2 candidates than of the lost dips (so releasing or retuning it is not pure noise), THEN a c1a + that-flag bench is worth building as lever 3 (with its own pass rule written first), and its ceiling is the lost dips that flag holds.
- Otherwise the faint pool is closed for c1a-type detrending: the losses are spread over many holds, and no single tier change recovers them. Report that.
- Stored event flags are pre-context (dominated and repeater are recomputed in context by the scorer), so dominated and repeater shares are lower bounds; said in the result.
- 5:45 pm, lever 2 result (`X11-C1A-MIRROR.md`): mirror match holds 105 of 133 lost dips; the rule says lever 3 is warranted, but c1a's background (111 / 98 upside-down) fails rule (b) before any release, so lever 3 cannot pass and is not built. Recorded as a design requirement for future detrending.
- 5:57 pm, lever 1 result (`X11-SAFE-RELEASES.md`): C1, C2, C4 fail (b) as predicted (upside-down 89, 84, 101). C3 (cap + ramp + gap edge) passes every preregistered rule: +2.66 (+1.65 to +3.78) on the 968, fresh +1.56 (+0.76 to +2.45) against the half-bar 1.33, 173 / 73, rule 4 excess 3.0, R 34.81. Short of F1 rule 2 read literally (+2.0 on the fresh bench); flagged for the second key, not decided by me. 34 of its 49 new real events are near gap edges (9 of 20 upside-down).

## Next lever? (5:58 pm) No: loop stopped with the work done, weekly 8% (stop line 13%)
Measured pools left, by ceiling per meter point: DS or R2 on top of C3 (rule 4 already at 3.0 of 5; DS alone adds 12.1: fails by arithmetic); M2 (excess 17.1 alone; C3 + M2 22.8: fails; needs a new leftover-eclipse design, M4 failed); c1a with a ghost-aware mirror rule (lever 2: fails rule b before any release); one-neighbour QLP windows (ceiling 0.1 to 0.6 point, needs new replays and a raw-observable denominator); a narrower gap-edge release (would be designed on the 34 events this lever just showed: tuning on results, not allowed); stacking (Codex 028). None is worth its meter under the brief's "only levers measured, no new designs without a ceiling". What C3 needs next are freeze CHECKS, not levers: TOI-1338 b (F1 rule 8), a pixel look at its 34 gap-edge real events, the class A identity, and the main session's reading of F1 rule 2.
