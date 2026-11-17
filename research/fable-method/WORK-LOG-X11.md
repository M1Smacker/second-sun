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
