# Brief 004: a smarter repeater flag, designed and priced by you on the T156 bench (Tree node 1.1)

**From:** Claude, 13 Nov 2026, after Ahmed's question round. **Branch:** `astra/004-repeater-bench` (made from main in your folder; it contains your merged 003 work, `research/TREE.md` and AGENTS rule 13).
**Ahmed's decisions:** the repeater flag is the first Petrova fix; **one change per bench run**; **Codex does all of it** (design, code, bench, report), on a lighter model to save tokens (Sol, or Astra at medium effort: Ahmed sets it in the app; say which one you are on); FIX 91 goes into the same future version **but is priced separately**, as part 3 below.
**Writes allowed:** `research/astra/reports/004-*.md`, `research/astra/scripts/004_*.py`, harness copies under `research/astra/scripts/harness/` (new subfolder `sprint004`, note every change), `data\astra\004\`, `research/astra/USAGE.md`. Never edit the frozen files in `pipeline/`. Stars: design-seen only, fences as in AGENTS.md.
**Budget:** 10 weekly points of your bar in total (part 1 design: 2, part 2 bench: 5, part 3 FIX 91: 2, report: 1). Be economical: no web research is needed; read only the code you change.
**Run mode:** as before, one working session, commit after each part, stop only at a stop sign, the cap, or the five-hour bar near 90% (then write RESUME HERE at the top of the report).

## Background you already know
`pipeline/stage3_core.py` line 21 sets `REPEAT_N = 3`; `enrich_group` counts every event of the same kind and product in the star-sector (`Counter((kind, product))`) and `enrich_event` flags `repeater` when that count is 3 or more (line 272). The physics note on line 21: a circumbinary planet has P of about 15 d or more, so at most 2 transits fit in one sector. Your 003 reading: in the Saturn-like band the repeater flag sits on 17 of the 53 held-back test planets, and clearing it alone frees 13 (static, overlapping). The flag counts unrelated excursions together with the planet.

## Part 1: write the new rule BEFORE any bench result (commit it first)
Design ONE replacement rule from physics, not from bench outcomes. It must keep the flag's purpose (a signal that repeats too often to be a circumbinary planet) while not counting unrelated events. Candidates you may choose from, or your own:
- (a) **Periodic set:** flag an event only if it belongs to a set of 3 or more same-kind events in the product and sector whose spacings agree within a stated tolerance (a periodic source, which a CBP cannot be).
- (b) **Binary-locked:** flag only if 3 or more same-kind events sit at the same binary phase (catalogue period and epoch), within a stated tolerance.
- (c) A combination, stated exactly.
Write in `reports/004-repeater-bench.md` and commit **before running**: the exact rule, every tolerance with its physical reason, what happens when the catalogue period is missing, and the **acceptance rule** below, unchanged. One setting only: no second setting may be tried on this bench except as a clearly labelled exploration that cannot be adopted.

## Part 2: price it on the same bench (no new searches if you can avoid them)
The repeater flag acts at tiering, after detection. So the cheapest honest test is to **re-tier the saved events** with the new rule:
- the 2,000 T156 trials (`data\astra\003\workers\*\trial-*` group files, dip and bump arms), and
- the un-injected design groups (the stored development-run groups your 003 worker read as baseline), for the **background** count of real and upside-down tier-1 events.
First prove the re-tiering path: with the OLD rule it must reproduce every stored tier exactly (zero-difference on all trials and all baseline groups). A mismatch is a stop sign.
**Report:** reference-band R old vs new (same equal-bin definition and star-cluster bootstrap), per period bin; all-depth dip and bump recoveries; background tier-1 counts real and upside-down, old vs new; trials gained and any trials LOST.

**Acceptance rule (Claude, written before any result; do not change it):** the change counts only if (1) reference-band R rises; (2) the background upside-down tier-1 count does not rise by more than its counting error (new count at most old + 2 x sqrt(old + 1)); (3) planted-bump recovery stays within the paired 99% intervals of dip recovery per bin, as in 003. Report each condition as PASS or FAIL. Anything else is not adopted.

## Part 3: FIX 91 priced alone (same method)
Make the opposite-sign coincidence check symmetric (`stage2_search.py` 194 to 195: give each arm the other arm's events) in a harness copy. If it acts only at tiering, re-tier as above; if it needs detection reruns, say so, estimate the cost, and run only if it fits the cap. Same report lines and the same acceptance rule, except condition (1) becomes "R does not fall".

## Report
`reports/004-repeater-bench.md`: verdict line first (for example "repeater rule (a): R 27.5% to x% [a, b]; background flips old n, new m: ACCEPT / REJECT"), then the rule as committed, the zero-difference proof, the tables, FIX 91, Bugs found (with Tree node), what you would do next. Your final message to Ahmed: the verdict, in plain words, in a few short lines.
