# Area N findings (numbers and statistics). Read at commit c9b9aca.

Scripts: `scripts/n01_census_odds_and_s2.py`, output `evidence/n01_census_s2.txt`.

## F-07. The Census odds arithmetic is right; its inputs are not (mask loss). CONFIRMED (arithmetic), UNCERTAIN (size of the correction). Fable used: yes.

| Number | Ours | Mine (Monte Carlo over the prior, not a grid) | Decision changes? |
|---|---|---|---|
| Census 1,400 stars, prior A, c 0.9 | 36% to 52% | 36% to 52% | no |
| Census 1,400, prior B | 21% to 31% | 21% to 31% | no |
| Census 3,000, prior A / B | 59% to 76% / 37% to 52% | same | no |

So WO-1's fix was done correctly. But every E that feeds it (past hunts 1.28 to 2.89, Census E per star) comes from recovery tables measured AFTER the eclipse mask (finding F-01). With m = share of expected detections that survive the mask:

| m | Census 1,400, mask NOT fixed (A / B) | Census 1,400, mask fixed first (A / B) | believed rate after 3 nulls (A / B, mean) |
|---|---|---|---|
| 1.0 (as published) | 36-52% / 21-31% | same | 5.7-7.7% / 2.9-4.1% |
| 0.8 | 32-48% / 19-28% | 38-55% / 23-33% | 6.2-8.3% / 3.2-4.5% |
| 0.6 | 27-42% / 16-25% | 40-58% / 24-36% | 6.9-8.9% / 3.7-4.8% |
| 0.4 | 21-34% / 12-20% | 42-62% / 26-40% | 8.0-9.8% / 4.3-5.3% |

My rough m from `evidence/p01c_real_light.txt` weighted by star-sectors: G2 sealed about 0.5, G3 about 0.65; weighted by E (fast binaries carry more E because short planet periods have a full window) probably 0.6 to 0.8. UNCERTAIN until WO-F01 step 2 measures it through the whole chain. Reading: **fixing the mask before Census is worth about 10 to 16 points of "chance of at least one"**, the same as adding roughly 600 to 900 stars, at near zero data cost. And the three nulls pull the believed planet rate down less than we said.

## F-08. The S2 interval is right; "FAIL" is within noise of the mark. CONFIRMED. Fable used: yes (small).
- Pooled 115 in 13,412 = 8.57 per 1,000, exact 95% interval 7.08 to 10.28 (ours 7.08 to 10.29: same).
- If the true rate were exactly the mark (8), a count of 115 or more happens 24% of the time; G3 alone (32 in 3,425): 21%. Star-sectors of one star are correlated, so the real intervals are wider still.
- `Q6-S2-EVIDENCE-2026-11-04.md` already reached the same numbers (0.24, 0.21); this is an independent confirmation, not a new result.
- So S2 failed as filed (the rule was "at most 8", and the verdict stands), but the data do not show the true rate is above 8. Hunting for one hidden "S2 bug" may be chasing noise. What IS real and large is the arm asymmetry of F-01 (upside-down over real up to 3 to 1 in slow binaries). Recommendation on the pending S2 decision is in the report.

## F-09. Horizon reach: three structural biases, two up and one that cancels. LIKELY (code reading of `pipeline/horizon_reach.py`; not re-run). Fable used: yes.
1. **Recovery table S(K, duration) is post-mask** (`rows_v9base.pkl` from `chain_recovery`): overstates reach, more for slow binaries and deep dips (F-01). Biggest term.
2. **Dilution and radius roughly cancel, by luck.** Main scenario uses dilution 1.0 (line 112), which looks optimistic for a binary. But the TIC radius of an unresolved binary is inflated by the second star's light (about a factor 1.4 for twins), which lowers depth by about 2, the same as dilution 0.5. So "main" is about right for twins and the "dilute0.5" scenario double-counts. This should be said in HORIZON-R0-RULE; it is not. For G2 the radii come from `targets/host_radii_g2_g3.csv`: where that source is NOT blend-inflated (for example spectroscopic or SED-fitted per component) the cancellation fails and E is too high by up to 2 in depth. NOT TESTED which source dominates: work order WO-F09.
3. **W = min(1, covered days / P_planet) per star-sector, sectors treated as independent** (lines 86 to 88): fine for scattered sectors, slightly optimistic for adjacent ones. Small.
4. The c = 0.9 trim is a guess of about 10%; F-01 shows the true trim is period dependent and far larger for slow binaries. c should become c(P_binary), measured.

## F-10. Not re-derived (budget): faint-star value 0.21, bright value 0.45, the noise fit, the g factor, Armstrong anchor. NOT TESTED. Fable used: no.
All four ride on the same post-mask recovery tables, so they inherit F-01; the RATIOS (0.21, 0.45) are probably robust because the mask loss depends on binary period, not brightness, except that bright stars give deeper K and deep dips are cut more (so 0.45 is LIKELY a little high). Work order WO-F10 (Opus): re-derive after the mask is fixed, plus H1's list of numbers that do not reconcile in RESUME (612 vs 611 stars; 4,080 vs 3,425 G3 star-sectors; the 19,464 total). My reading of the last one: 4,080 = star-sector groups searched, 3,425 = star-sectors scored after "no safe windows" and other drops (16.1% lost), so both are right but RESUME does not say which is which.
