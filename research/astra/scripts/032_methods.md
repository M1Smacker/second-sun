# Brief 032 implementation choices, fixed before v3 fitting

The brief is the preregistration. These are numerical details needed to execute it.

Copy the 014 measurement and alias functions unchanged. Use its already frozen product-family error scales, read from 014/timing-calibration.json, before adding the track-specific extra scatter. This keeps errors consistent with the permitted eclipse-times-v2.csv input. No scales are estimated from the fresh controls.

Compute initial weighted linear residuals. In one pass, flag absolute departures from their median above five times 1.4826 MAD, remove the largest first, capped at floor(N/10) and leaving at least three times. Refit once after clipping, then solve reduced chi-square = 1 by a bracketed scalar root. Leave extra scatter at zero if chi-square is already at most one. No iterative clipping. Retained times determine the two-sector requirement and final MAD. Covariance is the inverse weighted normal matrix, including the extra scatter in every error. No second chi-square scaling.

At each catalogue sector midpoint, identify the nearest catalogue primary centre and compare it with the nearest fitted primary centre. Require all differences within one quarter of the catalogue primary width. No epoch relabelling or half-period correction beyond 014. A1 denominator is all selected primary tracks with at least three measured times, including unusable fits. A2 denominator is usable primary tracks. Empty denominators fail.

Use 014's eligibility and five-bin allocation unchanged when 60 controls are available; otherwise use every remaining eligible control, as the brief directs. Exclude both spent control lists. Preserve every selected star, including missing width, missing times or failed fits, in output. The synthetic trap uses the exact 014 noise library, seed and code so its required 30/30 is a regression check.

Runtime checks before judging: independent weighted regression and covariance, quadrature-scatter root, zero-scatter path, clipping cap, sector/width usability, epoch-cycle covariance, quarter-width boundary, pass-rule boundaries, deliberate solver mutation, source identity for timing/alias/trap functions. Count aggregation is independently recomputed after the run. No Part B without A1, A2 and A3 passing.
