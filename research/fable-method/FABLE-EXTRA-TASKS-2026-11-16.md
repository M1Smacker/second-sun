# Fable extra tasks, if F0 to F4 and the report finish under 95% weekly (Claude, 16 Nov 2026, 10:10 am)

Ahmed (10:09 am): if Fable finishes early, give it more work and use everything up to 95%. Claude sends these one at a time, in this order, skipping any the main run already did. Same rules as the main brief (`FABLE-BRIEF-BIG-RUN-2026-11-16.md`): bench copies only, no frozen files, no fences, lab-notebook work log, explicit-path commits, stop at 95%.

- **X1. Fresh-seed confirmation (if F1 did not run it).** Run F1's best combination on a new planet bench (new seed, new planets, same rules) that was not used to choose it. Report P and its interval against 0.75/0.65 and the old 0.50. File: `X1-FRESH-SEED.md`.
- **X2. Prototype what F4 only designed.** Build orbit vouching or the cross-star dump veto on a bench copy, with the preregistered pass rule written first, the zero-planet identity check, and both arms. File: `X2-F4-PROTOTYPE.md`.
- **X3. Codex 025 follow-up.** Read 025 as merged and Claude's notes in `ASTRA-REVIEW-2026-11-16.md`. Say whether the stray-light (bit 4096) candidate is safe to combine with F1's set, and what one measurement would settle it. File: `X3-025-STRAY-LIGHT.md`.
- **X4. The "too faint" pool (22.4 points of P, the biggest by RS-037).** Measure which part of it is reachable: planets whose single-crossing signal would clear the threshold under a better per-sector noise estimate or detrending window, on bench copies. Ceiling first, then one prototype if the ceiling is above 2 points. File: `X4-FAINT-POOL.md`.
- **X5. Second opinion on the 0.75 bar.** Given everything measured today, the realistic best P with its interval, and the single change most likely to close the gap. One page. File: `X5-PATH-TO-075.md`.

## Added 10:12 am (Ahmed: more tasks, aim P at 0.60 to 0.70 in this run, use everything to 95%)
Aim: raise P (planet-level recovery, adopted set B 48.11%) as far as the evidence allows, at no more upside-down alarms (79 or fewer) under Tree rule 1. Every gain counts only with its interval and a fresh-seed confirmation. FIX 101 (mask drift) stays with Codex 026: leave a slot for it in combined numbers, do not build it.

- **X6. Guard-flag pool (11.6 points of P, RS-037).** Planets found at SNR 7+ but held at tier 2 by dump, step, gap edge, ramp or repeater flags. Measure each flag's planets lost against upside-down alarms prevented, then build the best release rule that spends the upside-down budget FIX 96 frees (50 real, 26 upside-down removed at 0 planet cost). Preregister the rule before scoring. File: `X6-GUARD-FLAGS.md`.
- **X7. Never-scored pool, the in-chain losses.** Of the about 600 unnamed crossings (good data, away from eclipses), split by cause (no finite score 248, safe windows 235, product table, gap trimming) with replay scripts, and prototype a fix for the largest real (non-bench-artefact) cause. File: `X7-NEVER-SCORED.md`.
- **X8. Failed-to-prepare sectors (308 crossings: no safe windows 165, too little data after masking 143).** Find why each fails and whether a safe change reclaims them without eclipse residue (count new real events within 0.3 d of catalogue eclipses against the upside-down arm). File: `X8-FAILED-SECTORS.md`.
- **X9. Multi-crossing search done properly.** RS-037 measured stacking at 2 to 4 points with a crude sum. Prototype an orbit-consistent search (crossings that one circumbinary orbit can explain, scored together) on bench copies; measure P and upside-down alarms. File: `X9-ORBIT-SEARCH.md`.
- **X10. The combined candidate.** Everything that passed (F1 set, X2, X6 to X9, 025 stray-light if safe, a slot for FIX 101) measured together on the planet bench and T156, with intervals, real and upside-down background, and a fresh-seed confirmation. This is the Petrova 1.1 proposal number. File: `X10-COMBINED.md`.
- **X11 onward (open).** After X10, pick the next lever with the largest measured ceiling per meter point, write one line why in the log, run it, repeat until 95%.

**Order (biggest expected gain first):** X1, X6, X2, X7, X8, X9, X4, X3, X10, X5, then X11 onward. X10 may move earlier if three or more parts have passed.
**If Fable's 95% arrives with tasks open,** Claude continues the open one itself from the work log between 95% and 98%.
