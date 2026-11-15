# Brief 024 (big run A2): close the short-binary blind spot by subtracting the binary's own light (Claude, 15 Nov 2026; launch after 023 ends)

You run headless; nobody can answer questions. Choose the safest reading, say so in the report, go on. AGENTS.md wins over this brief.

## Why
Node 1.5 of the Tree: for binaries of 5 to 10 days we catch only 6 of 48 planted Saturn-like planets (R 0.13). Your 003 and 005 found the loss is BEFORE detection: 19 of 48 give no event at all (40%, against 13% in other bins), all 19 sit below SNR 7, their depth survives detrending, and the scatter is higher in short binaries (median 3,070 against 2,221 ppm; median best SNR 6.2 against 9.3). Ceiling about 7.9 points of R. Our LIKELY cause: the binary's own repeating light (ellipsoidal and reflection shapes, spots locked to the orbit, eclipse residue outside the mask) stays in the light curve and inflates the noise.

Circumbinary searches in Kepler data commonly remove the binary's own light before searching by folding the light at the binary period and subtracting the folded, phase-binned shape. A planet's transits do not repeat at the binary phase (they drift), so a median across cycles keeps them. Your job: build that step on a bench copy and measure it. This is a measurement for Fable's Monday decision; nothing is adopted.

## Before computing (write into the report first)
1. **Literature check (short, primary pages only, no file links in a browser):** find one or two published circumbinary searches that subtract a phase-folded binary model (Kepler era) and quote the exact sentence describing the step. Label what you find CONFIRMED or UNCERTAIN. If you find a better-suited standard method (for example a model of the binary's light curve fitted per sector), say so and use it instead, with the reason.
2. **The method, fixed in advance:** for each star and sector, fold at the catalogue binary period; phase-binned MEDIAN shape (bins sized so each bin holds points from at least 3 cycles; state the rule); eclipse windows keep the current mask; subtract the shape (or divide, say which and why) BEFORE detrending; apply identically to the real and upside-down arms (the upside-down arm is 2 minus flux; the step must be symmetric, test that it is). Stars with fewer than 3 binary cycles in a sector: skip the step and count them.
3. **Pass rule:** in the 5 to 10 day bin, more planets found AND reaching tier 1 than under B (adopted set) by a margin outside the bootstrap noise (whole-star bootstrap 95%); no other binary-period bin loses planets beyond its noise; untouched-light tier-1 upside-down background not above B's 79; real background reported. Also the paired dip-against-bump control per bin.

## Measure (bench copies only)
- Inject the planted planets into the RAW light before every step, as in 006 (the 10 Nov lesson: inject before the mask, before windows, before detrending).
- T156 R per bin and overall; planet bench P (1,098, equal-bin) per bin and overall; untouched-light background both arms; per-star scatter before and after the step for the short-binary stars.
- A control that could prove the step harmful: on 20 stars, plant a transit exactly at the same binary phase in every cycle (the worst case for a median subtraction) and report how much depth survives.
- Run under B and under B + C96 (the FIX 96 depth cap) so Fable can combine it with the 023 matrix.

## Your method log (for the skill Ahmed wants)
Keep `research/astra/reports/024-worklog.md` WHILE you work: what you looked at first and why; what you chose not to do; the check that could have proven you wrong and whether you ran it; when you stopped reading and started computing; each decision; where you changed your mind. Steps and evidence only.

## Rules and report
Branch `astra/024-short-binary-subtraction` from the latest main. Cap 60 five-hour points; machine time free; long fits in the background; never poll. Data under `data\astra\024\`. Fence A and B never; no G1 or sealed data; frozen files untouched; never push. Report `research/astra/reports/024-short-binary-subtraction.md`: verdict line first; the literature sentence; the method and pass rule as written before; the table per bin; the worst-case control; what you did NOT check; usage.
