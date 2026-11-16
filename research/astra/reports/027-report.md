**PARTIAL: B and K2 reproduce; the c1a raw replay is running.**

Requested model GPT-6-Astra high; runtime model and effort independently unverified.
Branch: astra/027-c1a-tier-bench. No git writes. Tree nodes 1.3, 1.5 and 1.6.
Started 2026-11-17 01:39 Kuwait, from Get-Date.

## Pass rule recorded BEFORE scoring

A c1a configuration passes only if ALL hold: (a) on the 968 possible planets, P gain against the same configuration without c1a at least +2.0 points, paired 95% interval above zero; (b) untouched upside-down background at most 79 and real at most 174 (the adopted limits, whatever the base reads); (c) paired control passes in every bin; (d) T156 R not below the base; (e) the F1 new-real rule holds: (new real) minus 2.3 x (new upside-down) at most 5.

Configurations: B, B+c1a, K2=B+C96+R2, K2+c1a. M2 excluded. Same fixed inputs and populations, all 1,098 and 968 possible planets. Equal-weight five binary-period bins; 10,000 whole-star bootstrap draws, seed 2026111523; 95% paired changes and 99% dip-minus-bump controls. Control passes when its per-bin 99% interval includes zero, as in 023. New events are compared both with B and with the same configuration without c1a. The F1 rule binds against B, as in F1 section 5 and 023; the matching-base comparison is diagnostic. This reference clarification was made before reading any c1a outcomes.

Equal-alarm analysis is conditional on failure of (b) ONLY. Even host identifiers choose the smallest SNR floor from 7.0, 7.5, 8.0, 8.5, 9.0, 10.0 with upside-down background no higher than the base on that half. Odd hosts are held out. Floor applies to all candidate events on both arms. Report held-out and pooled results; label the floor 'chosen on half the stars, a proposal, not a frozen setting'. No other threshold tuning.

Fresh-seed confirmation only after passing, subject to the cap. No claims of a new frozen setting or permission to search G1.

## Usage

Predicted 50 five-hour points and 8 weekly points, cap 60 five-hour points. Meter unavailable in the headless tools; actual use unverified.

## Completed baseline verification

At 2026-11-17 01:51 Kuwait (Get-Date), baseline terminal success was observed. B reproduces P 48.1050309%, reference R 34.2070063%, and background 174 real / 79 upside-down. K2 reproduces 158 / 63. Every saved B planet and T156 arm outcome and every saved K2 planet arm outcome matched. Raw c1a-off identity also passed on 50 untouched sectors (70 product groups). Synthetic rule comparison: 288 combinations, 8 deliberate cap-mutation detections. These are producer checks.

The foreground replay is active, with resumable outputs and three workers. Estimated remaining finish approximately 07:52 Kuwait, an unmeasured six-hour allowance from the last clock reading, not a promise. Actual launch-relative estimate is recorded in data/astra/027/progress.json. No c1a recovery or alarm outcome has been read yet.
