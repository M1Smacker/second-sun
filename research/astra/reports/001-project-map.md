# 001 Project map, partial onboarding checkpoint

This is a reference map of inspected instructions, source and reported results. It is not a scientific audit. CONFIRMED below means static inspection or a stated catalogue count only. Reported science is NOT TESTED in this task. Read RESUME.md first on every return; its latest block overrides old historical status.

## Mission and authority
Second Sun searches public TESS light for planets orbiting two stars. Ahmed's stated win is a clean measured null, with a candidate welcome but not required. Claude designs, changes, freezes, merges and publishes. Ahmed is the second key and decides major choices and disagreements. Codex reviews and drafts locally, neither key.
The book is Ahmed's unlisted notebook and learning route. Lack of an audience is not access control. Latest local notes say the repository itself is public.

## Timeline and searches, reported not re-derived
- 19 Oct: project founded; G1 selected; known-system trials and literature waves began.
- 20 Oct: detector and product-path work; book expanded to 15 chapters and optional labs.
- 23 Oct: staged audit and 50-star Stage 2 trial; machine-only trial recorded three provisional leads. This historical triage count is not today's lead total.
- 27 to 28 Oct: G1 full search and successive Vesper flags, SAP twin and reporting changes. Current project summary calls the outcome a clean null, no current leads.
- 29 Oct: G2 development, clean-null objective and development/sealed split.
- 30 to 31 Oct: frozen 0.8.0 sealed G2 search, no excess. Local records differ in how they date scoring; chronology not resolved here.
- 3 Nov: 0.8.1 frozen for G3; Horizon and uncertainty work.
- 4 Nov: G3 one-shot search: S1 no excess, S2 failed as filed, zero leads. Census direction and learning plans recorded.
- 8 Nov: FFI-door work; later audit says CLOSED verdict stands. Full preregistration not read in this checkpoint.
- 10 Nov: Fable found the old eclipse mask removes single-visit dips; mask candidate work and book correction.
- 11 Nov: Petrova 1.0.0 frozen; Re-search 1 completed on 803 unseen G2/G3 stars, S1 no excess, zero leads. Morning report gives probabilities 0.41 and 0.31 against 0.005. These are copied report values, not independent calculations.
- 12 Nov: Codex helper kit, local worktree, path restrictions and mailbox established.
G1 with Petrova, Census and Petrova 1.1 are open choices, not authorized searches.

## Repository inventory
Tracked-path enumeration counted pipeline 132, targets 9, research 860, book 169, labs 11 and experiments 11. Research includes stage3 356, Fable audit 117 and astra 80 tracked files at scan time. These are file counts, not quality or completeness measures.
- pipeline: loaders, audits, detector, stage wrappers, recovery harnesses, scorecards, campaign runners, book feeds, tests and STANLEY wrappers.
- targets: G1/G2/G3 catalogues and chain representations, host radii, trial stars, Re-search 1 split. Catalogue comments must be skipped before CSV parsing.
- research/stage3: frozen settings, preregistrations/amendments, gates, result reports, proposed designs and two separate queues.
- research/fable-audit-2026-11: findings, evidence, design studies and work orders. Start at REPORT.md, then the evidence supporting each finding.
- research/astra: numbered inbox/reports, copied memory, usage ledger, helper scripts and Claude's fence checker.
- research root: decision/mistake/uncertainty/prediction registers and research/search-window blueprints. research/claims.md is a pointer register; book/data/claims.csv holds book claims.
- labs: environment helper and ten optional learning scripts. experiments: quality-mask experiment files. Neither was executed.
- data: private machine files. Top-level directory names were listed; sizes remain unfinished. Major families include g1/g2/g3, stage2/stage3 and their prep/run variants, chain_recovery variants, fable_audit variants, census inputs/probes, FFI-door material, known systems, STANLEY, wave-1/2/3 and xmatch. No contents opened.

## Planet-light path, static trace
All twelve frozen files are placed below. Do not import them casually: dataset.ROOT and stage3_core.ROOT point at Claude's checkout, irrespective of this working directory.
1. **dataset.py** selects campaign data, catalogue, audit, run and prep paths using SS_SET, default g1. **vopts.py** reads optional rules at import; Petrova uses c6,p1. Dormant switches are not the frozen active rule set.
2. **audit_all.py** provides campaign period tables, file inventory, build_windows and neighbour_windows. **audit_paths.py** provides product audit, SPOC-twin selection and noise measurement. These support preparation; full audit paths were not runtime-checked.
3. **detect_v2.py:load** reads FITS with Lightkurve hard quality mask, handles finite times and product columns. QLP selects sys_rm_flux when available, otherwise sap_flux. SPOC prefers PDCSAP, with SAP fallback/fill. Correctness of quality semantics by era is untested here.
4. **stage2_search.py:prepare** loads a product, applies own-SPOC or neighbour good-time windows if needed, records skips, then masks eclipses. The windows precede the eclipse mask in this function.
5. Old route: stage2_search.mask_runs calls **detect_v2.eclipse_mask_auto**, folds at catalogue periods, finds low phase bins and expands their masks. Petrova route: **petrova_mask.py:mask_runs** calls remove, combining catalogue windows and repeat-lane complement. old_removed on f and 2-f defines the union of formerly removed light; recovered intervals are that union minus the new removal mask.
6. stage2_search.Prod constructs real f and control 2-f, calls **detect_v2.detrend**, bin_width/bin10, then box_scores. events selects above-threshold boxes and merges overlapping detections. Preparation is shared before the two Prod objects are constructed.
7. stage2_search.do_group applies **detect_v2.veto** with flip_action=flag, measures second-product agreement, burst and eclipse-distance fields. Its legacy illustrative injections are after prepare, not a measurement of whole-chain completeness.
8. **stage3.py:do_group3 / add_step / search** wraps group processing and step measurements. **stage3_core.py:enrich_event / enrich_group / tier_of** add catalogue-phase, overlap, repetition, step, ramp and dominance flags. common_time.py:common_time_flags is a separate common-time helper; its exact production call relationship still needs completion.
9. **sap_twin.py:load_sap / load_pdc / install / twin_groups** supports the SAP pass and same-file PDCSAP check. **stage3_report.py:merge_sap** merges without double-counting matching primary events; apply_v7 applies common-moment checks, c6 orbit locks and then Petrova's cross-sector phase veto.
10. stage3_report.load/report produces the event view and aggregates. r1_run handles freeze/guards/input provenance; r1_gate runs planted-dip and exchangeability gates; r1_readout.strat_exact/strat_block implements the amended statistic. Only function definitions and selected implementation regions were inspected for these runners.
C-check details still needing a complete source map: C5 is catalogue-phase proximity; C7 is momentum-dump proximity; C8 is second-product agreement; c6 is the orbit-lock option. Do not invent missing C-number meanings from these names.

## Versions
Source: research/stage3/VESPER-VERSIONS.md and book/docs/versions.md, with stale statements flagged in the report.
0.0.0 Stage 2; 0.1/0.2 Stage 3 tiers and overlap/repeater flags; 0.3 step; 0.4 ramp/dominance and measured widths; 0.5 longer box; 0.6 SAP union; 0.7 pooled common moments and PDCSAP confirmation; 0.7.1 dataset switch; 0.8.0 c6 orbit lock; 0.8.1 G3 paths and dormant study options; Petrova 1.0.0 new mask and cross-sector phase veto, fingerprint bcd29c7aabb0. Fingerprint copied, not recomputed.
Compatibility proofs test equality with old outputs. They do not show the old or new scientific assumptions are correct.

## Tests, gates and limitations
- S1: amended Re-search 1 uses period-stratified, one-sided exact comparisons of unseen and fixed design-reference real/flip counts, recovered light, with a two-list threshold of 0.005 and additional SNR-bar conditions. Earlier unamended S1 is not the operative test.
- S2: false-alarm reporting per star-sector; Re-search 1 has no pass/fail mark. Older G3 FAIL remains filed and must not be relabelled.
- S4: strong planted-dip tier-1 recovery. Amendment 3 states injection times are selected in kept light, so it excludes loss of opportunities under the mask. Raw insertion alone does not repair that selection bias.
- Gates (a)/(b): dip/bump retention checks. Gate (c): real/control exchangeability by period bin; failed bins narrow coverage. Full numerical specifications need rereading.
- G2 14 to 20 d and over 27.4 d, plus G3 over 27.4 d, are labelled not covered in Amendment 3. A pooled pass cannot erase that qualification.
- Zero-difference tests: compatibility only. Synthetic tests: mechanism checks, not real-data calibration. Known-planet checks: examples, not population recovery estimates. Book tests: presentation/integrity, not validation of the science.

## Open choices
G1 needs catalogue widths, a new patch with equality proofs, appropriate gates and an amendment managed by Claude. Census needs its own binary list and measured useful coverage, not just a large star count. A future Petrova phase key should be developed only on allowed design data or synthetic inputs. Gaia refresh is a recorded future dependency; its external schedule was not checked. Learning units and reader/dashboard work remain separate from science changes.

## Book
MkDocs Material; configuration book/mkdocs.yml, hook book/hooks.py, layout book/shape.py, chapter/track order book/data/path.yml. Six Parts and fifteen chapters, learning levels L0 to L6 plus running-the-project material. Journey is a story route; labs are optional. Read/Hunt/Reference navigation. Claim chips and version history support traceability.
Current local footer says Book 2.11.2. Learning quick wins include Back, Continue and folded evidence. Search window reads aggregate JSON from watch_export; no live page accessed.
The documented publish wrapper performs strict build, shape/contrast/mission/site and browser checks; it also publishes and is forbidden for Codex. Its implementation and all gates were NOT inspected or run here. path.yml/nav/learning links and mission evidence must agree; brief 001 does not authorize editing any of them.

## Working glossary
- Tier 1A: unflagged second product agrees at SNR at least 4. Tier 1L: agreement 3 to 4. Tier 1B: no usable second product. Tier 2: flagged and retained. Tier 3: disagreement, retained.
- Recovered light: times the old mask removed in either flux orientation which the new mask keeps.
- Design-seen: used in filter design; eligible for development, not fresh confirmation.
- Flip arm: the control made with normalized flux 2-f.
- Star-sector: one star's observation in one sector, not an independent star.
- Census: proposed own eclipsing-binary catalogue from later TESS data.
- Horizon: sensitivity/reach and null interpretation work; geometry and repeated-epoch assumptions matter.
- Eyes: Ahmed's visual-training and vetting interface, tied to real cloud scores. Never test the live page.
- Keystone: proposed second-key examination following the learning/check engine, not evidence he has already passed.
- Compass: review-before-build process, approve/revise/reject based on existing capability and evidence.
- Two keys: Claude's technical assessment and Ahmed's independent human decision; Codex is neither.
- Freeze: recorded code, settings and inputs governing a run. Hash equality means byte identity only.
- Clean null: no detected excess under specified rules and sensitivity, not proof that planets are absent.

## Boundaries and continuation coverage
Writes in this brief are exactly this map, 001-onboarding.md and USAGE.md. Frozen files, preregistrations, queues and RESUME remain unchanged. No pushes, external writes, installs, secrets, live Eyes or fenced real-light work. G1 remains blind; unseen G2/G3 permit only authorized stored-count rederivation, never fresh design. Catalogue counts do not open event data.
The next reader must finish the missing coverage listed in 001-onboarding.md rather than infer a complete onboarding from this map's existence.
