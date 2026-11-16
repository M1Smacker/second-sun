# Fable report, big run of 16 Nov 2026

**Plain verdict: found something, and no breakthrough. No bug of the F-01 size turned up. What turned up is (1) a fault in the yardstick itself, (2) a clear picture of where the planets are lost, with prices, and (3) a Petrova 1.1 candidate worth about +3 points with fewer alarms. P 0.75 is out of reach with every lever known today; a realistic 1.1 sits near 0.52 to 0.55.**

## The single most important thing for Ahmed
**The number P (0.48) and the 0.75 bar are measured on a bench with two faults, and both should be fixed in a new dated bar file before more fixes are judged.**
1. About 12% of its test planets cannot exist: 130 of 1,098 are "planets" of 2 to 14 Jupiter radii on big stars. That alone made the depth cap (FIX 96) look like it costs 4.7 points. On planets that can exist it costs 0.1.
2. It only counts a planted crossing if the light survives the quality mask at loading. So the first step of the chain is invisible to it: 606 crossings and 30 planets are missing from the count, and a fix at loading cannot show up as a gain.
Neither fault flatters us much (B is 48.4 on possible planets and 46.8 on raw-observable ones), but together they can turn a good change into a "failure" and hide a whole class of losses. This is his decision because the bar file is his.

## What was done
| Task | File | Result in one line |
|---|---|---|
| F0 | `F0-PREMORTEM.md` | Three ways to fake a win, written first: best-of-eight, changed denominator, doors the upside-down meter cannot see. All three then appeared in the data. |
| F1 | `F1-PETROVA-1.1-VERDICT.md` | Nothing can be frozen yet. Candidate: B + depth cap + dump-shape rule + mask timing (M2): +3.3 points (+2.0 to +4.7) on possible planets with alarms 156 real / 59 upside-down against 174 / 79. Second sample (T156) agrees: +2.9. FIX 94 and FIX 101 are the same code line; brief 026 should change before launch. Pass rule for the freeze written (fresh-seed bench included). |
| F2 | `F2-SILENT-LOSSES.md` | Census from raw data: 1,525 of 5,914 planted crossings are lost before the search (mask 507, QLP safe windows 511, load 404, no score 103), ceiling 9.7 points. Top cause: the scattered-light quality bit. Prototype: dropping it rescues 185 clean detections but the admitted light throws 8 times more strong events, so it is not safe as it stands. A one-neighbour rule for QLP windows is clean and ready for the bench. |
| F4 | `F4-VETTING-VOUCHING.md` | Exact price of every guard flag under B. Best price: the dump hold by shape (18 planets for 3 upside-down alarms). Step holds 23 planets but stands in front of 113 upside-down alarms. Repeater, common moment, mirror match, near-eclipse: zero planets held. Designs with pass rules for a three-signal dump hold and for orbit vouching. |
| F3 | `second-sun-method/SKILL.md` | The procedure file, from Fable's and Codex's work logs, with a step-by-step comparison of the two. |
| Logs | `WORK-LOG-F1.md`, `-F2.md`, `-F4.md`, `-X6.md`, `FABLE-LEDGER-2026-11-16.md` | Lab-notebook style. |

## How far from 0.75 (LIKELY)
- Today: 0.48. F1 candidate with its guards: about 0.50 to 0.52.
- Add what F2 and F4 can fairly harvest (one-neighbour windows, a guarded scattered-light rule, vouching): perhaps +2 to +4 more.
- So a Petrova 1.1 to 1.2 at about 0.52 to 0.58. The bar of 0.75 would need the "too faint" pool (22 points), which no lever here touches.

## Unfinished, in order of value
1. **Fresh-seed confirmation bench** for the F1 candidate: NOT RUN (needs the Codex 006 drawing code and three mask modes; pass rule is F1 section 5). No number in this report is a GO number until it is.
2. Tier-level bench of the F2 variants (one-neighbour windows; scattered-light bit with a scatter guard). My prototype is at detector level only.
3. M4 (mask timing with a leftover-eclipse check), the depth-cap margin and the fallback radius: designed in F1, not built.
4. Orbit vouching and the three-signal dump hold: designed in F4, not built.
5. No mutation test was run on my prototype code (Codex does this better; see the method file).
6. Codex 025 had not landed on main when I wrote F2; I read its work log in the Codex worktree only.

## Decisions waiting for Ahmed
1. A new bar file: reference planets defined physically, "observable" defined from raw cadences. (Recommended: yes.)
2. The dump-shape rule: +1.9 points for about 12 extra dip-only leads near thruster firings, each needing a pixel check by eye, unless the F4 guard removes them. Accept that trade or not.
3. Whether the freeze rule may also limit NEW REAL events, not only upside-down ones (F1 section 5, rule 4). (Recommended: yes.)

## Meter
Start 73% weekly at 9:54 am. F0 and F1: 73 to about 78. F2 and F4 (run together): to 82 at 11:06 am, when the 5-hour bar filled and I stopped for 25 minutes. F3 and this report: 83 to about 84. Details in `FABLE-LEDGER-2026-11-16.md`. Codex jobs 023 to 025 ran on GPT-6.1-Sol at high effort, not GPT-6-Astra.

## Extra tasks (after this report)
X6 (a combined release rule for the guard flags, preregistered in `WORK-LOG-X6.md`) is scoring as this is written; its result is added below when it lands.
