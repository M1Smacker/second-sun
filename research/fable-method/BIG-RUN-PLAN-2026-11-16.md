# The big run: Astra and Fable, 15 to 16 Nov 2026 (plan only; Claude, 15 Nov, 5:20 pm Kuwait)

Ahmed's words (15 Nov, 5:19 pm): use Fable and Astra "to the absolute max"; aim for "a real groundbreaking breakthrough" by Tuesday morning (a bug that lets us find more planets, or a big rise in our chance of finding one); "if we don't get one, it's fine". Fable runs in a nested session with full context. Weekly meter budget: **65% to 95% for the run, 95% to 100% for Claude's report to him.** Not tiny fixes: complex tasks with real thought. Learn from BOTH models and write one method skill that every Claude and Codex model uses. He is away until Monday evening (maths exam study; he uses Claude for it, so his own chats need points too).

## Where we stand (our own numbers, CONFIRMED in research/TREE.md)
- Planet-level chance **P = 0.48 (0.44 to 0.52)**; G1 needs **0.50** (G1-PLANET-BAR.md). Adopted set (OAE + repeater rule b + FIX 91 + known spacecraft events): P 48.11%, background 174 real / 79 upside-down.
- Saturn-like test planets (T156, 222): caught 61; held below tier 1 **53**; outside windows **45**; not found **41**; mask **15**; no safe windows **7**.
- Known levers not yet combined: DS (dump shape rule) reaches P 49.98% at equal upside-down count (with OAE and known events); **FIX 96 depth cap removes 50 real and 26 upside-down background events and costs 0 of 264 planted dips** (Codex 014 part 3); FIX 94 mask timing frees up to about 64 never-found planets on the planet bench but both variants failed their preregistered rule (new real events, half are deep eclipses at wrong catalogue times, RS-027); our own eclipse times failed controls (Codex 012, 014).
- Node 1.5 (binaries of 5 to 10 days): R 0.13 (6 of 48); 40% give no event at all; higher noise in short binaries LIKELY; ceiling about 7.9 points of R (Codex 005 B).
- Node 1.2 windows: of 52 window losses, 15 true archive gaps, **21 lost at load**, 16 had usable data before the window rule; ceiling 2.6 to 7.0 points (Codex 005 C).

**Why a breakthrough is plausible:** FIX 96 frees about a third of the upside-down false-alarm budget at no planet cost. Under Tree rule 1 that freed budget can pay for planet-freeing changes that were rejected only for adding a few upside-down alarms (DS +5, FIX 94 variants +2 to +5, repeater variants). Nobody has measured all of them together. Plus two untouched pools (short binaries, load losses) worth up to about 15 points of R between them.

## What the meters say (CONFIRMED from our ledgers)
- Fable on 10 Nov: real work areas cost **about 1 to 2 weekly points each** when Fable worked directly; the expensive parts were **Fable helpers reading history (about 10 points for 2 summaries)** and **resuming a large context after a pause (about 4 points)**. Fable meter to weekly bar ratio about 2 to 1. Fable shares the 5-hour window with all Claude use, Ahmed's maths chats included.
- Codex (Astra) now: weekly 14% (resets 22 Nov), 5-hour window used about 92% by 021 and 022 (two jobs of 2 h and 16 min); so one Astra job of about 2 h uses most of a 5-hour window and about 5 to 7% of its week. Astra can do 3 or 4 big jobs before Monday evening if spaced by the 5-hour resets.
- Weekly resets Tue 17 Nov 1:00 am Kuwait; Fable access ends then. Points left Monday night vanish at the reset.

## The plan

### Astra (Codex, GPT-6-Astra, high effort): the measurements, tonight and Monday morning
Each job: a preregistered pass rule written by Claude in the brief BEFORE the run, bench copies only (never frozen pipeline files, never G1 or sealed data), a work log of HOW it worked (same format as Fable's), report, Claude reviews with fence_check.
- **A1 (tonight, about 2 to 3 h): the full candidate matrix.** Every candidate alone and in every sensible combination on the same benches: T156 R, planet-level P, real and upside-down background, with intervals. Candidates: adopted set, + DS, + FIX 96 cap (2 Jupiter radii), + FIX 94 V1 and V2, + repeater variants, + known-events. The question it answers: does FIX 96's freed upside-down budget let a combination clear P 0.50 with margin at upside-down at or under 79?
- **A2 (after the next 5-hour reset, about 3 h): the short-binary blind spot (node 1.5).** Prototype the standard fix in the literature for circumbinary searches: subtract a phase-folded model of the binary's own light before searching (bench copy); measure on the 48 planted planets of 5 to 10 day binaries and on the background. Pass rule: more planets found, no more upside-down alarms.
- **A3 (Monday morning, about 2 h): the 21 planets lost at load (node 1.2).** Root cause and a fix prototype, benched the same way.

### Fable (Claude Fable, nested session, Monday evening): the judgement, the second bug hunt, and the skill
Started by Claude with a context file (no helpers, no history reading; that cost 10 points last time). Meters read before and after each task; hard stop when the weekly bar reaches 92%.
- **F1: decide Petrova 1.1** from Astra's matrix (A1 to A3) plus the old evidence (merges the prepared tasks 1 and 2): which combination to freeze, the FIX 94 design that survives its controls, and the one combined test that must pass first. This is where P 0.50 is won or lost.
- **F2: the second "F-01" hunt.** Fable's 10 Nov audit found the bug that mattered most (the eclipse mask deleting dips in slow binaries). Same method on today's adopted set: put planets into the RAW light and follow them step by step through the "not found" (41) and "outside windows" (45) pools, looking for any step that loses planets for a reason that is not physics. Deliver ranked silent losses, each with a measured ceiling and a prototype fix for the top one.
- **F3: the method skill, from both models.** Fable writes `second-sun-method` from its own work logs AND Astra's (A1 to A3), noting where they work differently. Installed for every Claude model and, through sync_kit, for Codex.
- Dropped from the 14 Nov brief: task 3 (Road to G1 plan) - Claude can do it from F1's verdict.

### Claude (Opus): the glue
Tonight: write the A1 to A3 briefs with their pass rules (about 1.5 points), launch A1. Monday: review A1 to A3 (fence check each), write the Fable context file, start Fable, watch the meters, stop at 92 to 95%, then the report to Ahmed (95% to 100%).

## Budget (weekly bar)
| Step | From | To |
|---|---|---|
| Claude tonight (briefs, A1 launch) | 60 | about 61.5 |
| Ahmed's maths (today, Monday daytime) | 61.5 | about 70 |
| Claude Monday (A1 to A3 reviews, Fable context) | 70 | about 73 |
| Fable F1 to F3 | 73 | 92 at most |
| Claude's report to Ahmed | 92 | 95 to 100 |

## Rules kept
Tree rule 1 (a Petrova change counts only if the bench shows more planets without more upside-down alarms; fairness amendment). Tree rule 3 says outside audits only at a version freeze: Ahmed's instruction of 15 Nov overrides it for this run. Fences A and B, frozen files, sealed data, two keys, no pushes by Codex or Fable, nothing outward. Bench tuning is allowed (development data); nothing is tuned on G1.

## Open choices for Ahmed (asked 15 Nov, 5:20 pm)
1. Start Astra A1 tonight (yes, recommended) or wait for Monday.
2. Fable effort: high (recommended; real areas cost 1 to 2 points, so high fits) or medium.
3. Fable start: when Ahmed says go Monday evening, or at a fixed time Claude starts it.
