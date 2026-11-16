# Work log X6: a release rule for the guard flags (Fable, 16 Nov 2026)

- 11:34 am. Extra task X6 asks for each flag's price (done in F4: `F4-VETTING-VOUCHING.md`, exact under B, identity checked) and then the best release rule that spends the upside-down budget the depth cap frees (79 to 53).
- Rules fixed NOW, from the single-flag price list only, before any combined score exists. All include the depth cap (C96):
  - R2 = dump hold by shape (DS) and the gap-edge hold released.
  - R1 = R2 and the ramp hold released. (Single-flag prices: DS +18 planets / +3 upside-down, gap edge +8 / +5, ramp +13 / +11; sum +39 planets, +19 upside-down, so about 72 of the 79 allowed.)
  - R3 = R1 and the eclipse-overlap hold released (+3 planets, 0 upside-down alone).
  - Not included, by price: step (+23 planets for +113 upside-down) and dominated (+15 for +24, which would pass 79).
- Pass rule (Tree rule 1 as F1 reads it): untouched background upside-down at most 79 AND real at most 174; paired change in P against B, on planets that can exist, with its 95% interval above zero; planted dips and planted bumps both rise (arm fairness). Among the rules that pass, the one that frees the most planets is the X6 proposal. Three preregistered rules and one bench: the winner still needs the fresh-seed bench of F1 section 5 before any freeze.
- What would prove me wrong: flags overlap on the same events, so combined alarms may exceed the sum (an event held by gap edge AND ramp is released only when both go). If R1 breaks 79 or 174, R2 is the proposal.
- Scorer: `data/fable/f4/x6_prepare.py` adds the three rules to the F4 copy (`x6_score.py`), same identity assertions. Launched in the background.
