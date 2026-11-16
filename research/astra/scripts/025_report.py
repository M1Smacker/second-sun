"""Render the counts-only handoff from completed, verified private measurements."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/025'
REPORT = ROOT / 'research/astra/reports/025-report.md'


def main():
    if '--partial' in sys.argv:
        partial()
        return
    summary = json.loads((OUT / 'summary.json').read_text(encoding='utf-8'))
    verification = json.loads((OUT / 'verification.json').read_text(encoding='utf-8'))
    progress = json.loads((OUT / 'progress.json').read_text(encoding='utf-8'))
    assert progress['status'] == 'complete'
    assert verification['producer_verification'] and not verification['independent_review']
    diag = summary['diagnostic']
    verdict = ('Found something. The predeclared bench candidate passes its four acceptance checks.'
               if summary['passes'] else 'Found something. The load losses are traced. The predeclared quality candidate fails its acceptance rule.')
    now = datetime.now(timezone(timedelta(hours=3)))
    lines = [f'**{verdict}**', '', '# 025 Load losses', '',
             'Codex runtime model and effort are independently unverified. The brief specifies neither.',
             f'Completed {now:%Y-%m-%d %H:%M} Kuwait. Branch astra/025-load-losses. Tree node 1.2.', '',
             'This report follows the filename and no-git-write instructions in the current user request. '
             'The pre-existing runner lock was preserved. The runner handles the commit.', '',
             '## What was found', '',
             'CONFIRMED. The 005 roster reproduces exactly. Twenty-one of the 52 reference window losses lack loaded '
             'centre support, 15 have an archive gap, ten lie outside safe windows, and six lack safe windows. '
             'Twenty of the 21 load cases have finite archived flux. The remaining case also lacks finite archived flux.', '',
             '| Blocking bits among nearby finite samples, or archived-flux condition | Reference load cases |',
             '|---|---:|']
    for reason, count in diag['original_load_bits'].items():
        lines.append(f'| {reason} | {count} |')
    lines += ['', 'Bit combinations in that table are unions across nearby samples. Each exact quality word, cadence count, '
              'filename, selected column, hypothesis checklist and exact source condition is saved privately in roster.json, '
              'case-evidence.json and the trace files. Bit 4096 means Straylight2 for SPOC-family files. The installed QLP reader also uses '
              'it for low precision before sector 56. QLP adds bit 1073741824 from sector 56. Bit 128 is manual exclusion, '
              'and bit 2048 is stray light. These meanings were checked in the installed reader and quality definitions.', '',
              'CONFIRMED. detect_v2.load() applies Lightkurve hard quality screening before finite-time and flux selection. '
              'The QLP reader adds its product-specific quality mask. The no-finite-flux category records an additional '
              'archived-data limitation. Quality screening can also precede rejection of those nonfinite samples.', '',
              f'CONFIRMED. Zero of the original 21 has a whole-sector FIX 101 mask. '
              f'{diag["load_no_safe_windows"]} also lacks safe windows. '
              f'{diag["load_alternative_product_keeps"]} retain centre support through masking in another product. '
              'That support establishes alternate search input, with recovery measured separately below.', '',
              '## The 16 usable-before-window cases', '',
              '| Rule | Cases | Source condition |', '|---|---:|---|',
              '| Own SPOC support | 3 | stage2_search.py line 154, use good_windows(own) |',
              '| Neighbour intersection | 5 | stage2_search.py line 156, use audit_all.neighbour_windows() |',
              '| Half-day start trim | 2 | detect_v2.py line 111, retain from start + 0.5 d |',
              '| No safe windows | 6 | stage2_search.py line 158, own SPOC absent and fewer than two neighbours |', '',
              'CONFIRMED. These branches implement their comments, including the intersection and start trim. '
              'The six absent-window cases fail a minimum-reference requirement. '
              f'{diag["window_alternative_product_keeps"]} of the 16 has usable alternate-product centre support. '
              'The trace establishes the removing condition. Safety of expanding each interval remains NOT TESTED.', '',
              '## Across all 2,000 fixed T156 draws', '',
              'First-loss accounting assigns each draw to the earliest classified data-support loss. This keeps '
              'overlapping quality, window and mask problems from being added together as separate planets. '
              'The final mask trace includes each planted dip before eclipse masking.', '',
              '| First classified loss or retained support | Draws |', '|---|---:|']
    for cause, count in diag['all_first_loss'].items():
        lines.append(f'| {cause} | {count} |')
    lines += ['', f'CONFIRMED. Missing selected files {diag["missing_files"]}. Missing manifest entries '
              f'{diag["missing_manifest"]}. FITS header sectors have zero mismatches across the 4,613 traced '
              'trial/product rows. Every inspected header uses BJDREFI 2457000 and TIMESYS TDB. '
              'The archive, loader and centre-support timestamps therefore share the expected reference in this sample.', '',
              'The drift overlap counts are separate from first losses. '
              f'{diag["all_drift_overlap"]["FIX101_whole_sector"]} draws have a selected product whose catalogue '
              'window covers its full retained sector. '
              f'{diag["all_drift_overlap"]["FIX101_near_centre"]} intersect a drift-added catalogue window near the '
              'planted centre. A drift-cap prototype was conditional in Claude\'s update. The original 21 load cases '
              'supply zero whole-sector FIX 101 cases, so this brief tests the largest measured load cause.', '',
              'RS-038 supplies its own 006 replay results, cited here without recounting. Its 1,292 never-scored '
              'crossings comprise 526 mask, 248 no-finite-score, 235 safe-window, 192 best-product-table gaps, '
              '60 capture mismatches and 31 load cases. Its bench-capture qualifications also apply when interpreting '
              'single-product diagnostics. [RS-038](../../stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md)', '',
              '## Fixed candidate and measured performance', '',
              'The candidate admits bit 4096 in the loader and SAP/PDC twin loaders. Every other existing blocking '
              'bit, QLP late-sector low-precision bit, finite-flux rule and borrowed-window rule stays active. '
              'The bench copy uses 025_loader.py. The proposed bench diff is 025-loader-prototype.patch. '
              'The frozen pipeline files retain their original bytes.', '',
              'The pass rule was written before candidate computation. Restore searched centre support for at least '
              '11 of the original 21, increase T156 reference R, add no upside-down tier-1 background, and reproduce '
              'events exactly on 50 unaffected star-sectors. The fixed 006 planet P is also measured.', '',
              '| Configuration | Reference R | Planet P | Background real | Background upside-down |',
              '|---|---:|---:|---:|---:|']
    for j, name in enumerate(summary['configurations']):
        r = summary['measurements']['reference']['overall'][0][j] * 100
        p = summary['measurements']['planets']['overall'][0][j] * 100
        bg = summary['background'][j]
        lines.append(f'| {name} | {r:.3f}% | {p:.3f}% | {bg["real"]} | {bg["flip"]} |')
    lines += ['', 'R uses the 222 reference draws. P uses the unchanged 1,098 observable planet trials. '
              'Both scores give equal weight to the five fixed period bins. Raw counts and within-star dependence '
              'are retained. Intervals use 10,000 paired whole-star bootstrap draws, seed 2026111525.', '',
              f'CONFIRMED. Searched centre support restored for {summary["restored_load_centres"]}/21. '
              f'Exact event identity checked on {summary["identity_star_sectors"]} unaffected star-sectors. '
              'Both primary and available SAP group events are compared with the saved development groups.', '',
              '| Acceptance check | Outcome |', '|---|---|']
    for name, passed in summary['tests'].items():
        lines.append(f'| {name} | {"PASS" if passed else "FAIL"} |')
    lines += ['', '| Binary period | Reference draws | B dip / bump | Candidate dip / bump | Candidate paired 99% interval |',
              '|---|---:|---:|---:|---|']
    metrics = summary['measurements']['reference']
    for b, name in enumerate(('5 to 10 d', '10 to 14 d', '14 to 20 d', '20 to 27.4 d', '27.4 d onward')):
        c = metrics['counts'][b]
        lo = metrics['control_ci99'][0][b][2] * 100
        hi = metrics['control_ci99'][1][b][2] * 100
        lines.append(f'| {name} | {metrics["n"][b]} | {c[0][0]} / {c[1][0]} | '
                     f'{c[0][2]} / {c[1][2]} | {lo:.2f} to {hi:.2f} points |')
    lines += ['', 'The following pooled counts within each fixed stratum are descriptive. The official scores above '
              'retain equal period-bin weights.', '',
              '| T156 stratum | Draws | B dip / bump | Candidate dip / bump |', '|---|---:|---:|---:|']
    for label, cell in sorted(summary['descriptive_T156_strata'].items()):
        lines.append(f'| {label} | {cell["n"]} | {cell["real"][0]} / {cell["flip"][0]} | '
                     f'{cell["real"][2]} / {cell["flip"][2]} |')
    lines += ['', '## Falsifiers and eclipse-residue control', '']
    checks = [json.loads((OUT / f'checks-{c}.json').read_text(encoding='utf-8')) for c in ('g2', 'g3')]
    mutations = sum(len(c['archived_mutations']) for c in checks)
    paths = {(r['product'], r['era'], r['cadence_seconds']) for c in checks for r in c['runtime_product_paths']}
    lines += [f'CONFIRMED. {mutations} archived bit-4096 cases fail centre support under the original loader, '
              'pass under the candidate, and fail again when the original policy is restored as a mutation. '
              f'{len(paths)} distinct product/era/median-cadence paths were exercised. These include 30-minute, '
              '10-minute and 200-second data, SPOC 2-minute data, and the three requested QLP eras.', '',
              'CONFIRMED on the 22 audited file/path instances. In two tested sector-94-onward QLP files, '
              '9,755 returned cadences carry bit 536870912. Four tested SPOC-family files retain 871 cadences '
              'carrying bit 32768. Thus the installed hard policy retains some nonzero quality words. '
              'The physical meaning and safety of the QLP high bit remain UNCERTAIN in this brief. '
              'The prototype retains the inherited treatment of these bits.', '',
              'CONFIRMED on constructed light. All three wrong-epoch deep-eclipse controls become detected events '
              'when bit 4096 is admitted. The original quality policy excludes their flagged eclipse samples. '
              'The controls have 30-minute, 10-minute and 200-second sampling. They demonstrate the eclipse-residue '
              'hazard of this quality relaxation. They do not measure real contamination rates.', '',
              f'The candidate introduces {summary["residue"]["new_real"]} new real-arm and '
              f'{summary["residue"]["new_flip"]} new upside-down tier-1 background events, using event identity '
              'at the stored centre and duration. '
              f'{summary["residue"]["new_real_deep_or_high_snr"]} new real events meet RS-027\'s existing '
              '8,000-ppm-or-SNR-50 diagnostic. Their physical origin remains UNCERTAIN without independent '
              'eclipse-time measurements. [RS-027](../../stage3/rs027/NEW-EVENTS-ROOT-CAUSE-2026-11-14.md)', '',
              '## Checks actually performed', '',
              f'Producer verification completed {len(verification["checks"])} check groups. These include direct '
              'trial and transition recounts, complete generated replay coverage, design membership, preparation '
              'exception counts, denied-access probes, 50-sector event identity and twelve frozen-source byte '
              'identities. Static Python parsing and worktree checks are recorded in the worklog. Source hashes '
              'establish the measured bytes. Scientific review remains with Claude.', '',
              '## What I did NOT check', '',
              '- G1 light, fence-B light, new sealed searches, external services and publication.',
              '- A drift-cap or refit-centred-window prototype, because FIX 101 supplies zero whole-sector cases among the 21 load losses.',
              '- SPOC 20-second data. This fixed T156 trace contains no such runtime path.',
              '- Whether relaxing any other quality flag or widening any borrowed window is safe.',
              '- Independent scientific review, the complete runner-log fence check, or the physical origin of every new real-background event.',
              '- Usage-panel percentages. The headless runner exposes no meter.', '',
              '## STOP SIGNS hit', '',
              'The candidate acceptance rule governs adoption. Any failed check leaves the prototype on the bench. '
              'No frozen-file edit, sealed-run reinterpretation or result-driven threshold change was made.', '',
              '## QUEUE PROPOSALS', '',
              'Node 1.2. Attach the measured cause table and the tested bit-4096 result to the existing load/window '
              'and FIX 101 work. The direct trace supports an intentional-quality-cut mechanism for the dominant '
              'load loss. Adoption requires the full acceptance rule.', '',
              '## IDEAS', '', 'None beyond the requested prototype.', '',
              '## Disagreements with Claude', '',
              'The original 21 label is a best-product centre-support diagnosis. Three cases have alternate-product '
              'search input. This is a measured scope correction, with its private row evidence retained for review.', '',
              '## Questions for Ahmed', '', 'None.', '',
              '## Reproduction and evidence', '',
              'Run the scripts with D:\\second-sun\\.venv\\Scripts\\python.exe -I -B. Setup order is '
              '025_prepare.py, the two 025_trace.py CAMPAIGN --roster-only calls, roster merge, baseline traces, '
              '025_install.py, 025_score_prepare.py, the two injected traces, then 025_run.py. '
              '025_report.py renders this completed report. Existing private outputs must be preserved when rerunning.', '',
              'Private evidence lives under data/astra/025. It includes roster.json, candidate-spec.json, per-trial '
              'injected traces, generated raw-injection groups, combined score tables, background events, checks, '
              'source snapshots, verification.json, summary.json and terminal progress.json. The tracked worklog '
              'records the order of decisions and actual execution.', '',
              '## Usage', '',
              'Predicted 40 five-hour points and 8 weekly points, cap 50 five-hour points. Actual bars are unavailable '
              'in the headless runner. Lesson, distinguish best-product centre support, all-product search input '
              'and tier-1 recovery before naming a loss.', '',
              'Next action is Claude reviewing this report to validate the cause accounting and candidate verdict. '
              'It uses Claude\'s review budget, with the amount unmeasured.', '']
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print('Rendered counts-only 025-report.md')


def partial():
    """Leave a reviewable handoff when the authorized terminal waits expire."""
    diag = json.loads((OUT / 'injected-diagnostic-summary.json').read_text(encoding='utf-8'))
    checks = [json.loads((OUT / f'checks-{c}.json').read_text(encoding='utf-8')) for c in ('g2', 'g3')]
    now = datetime.now(timezone(timedelta(hours=3)))
    lines = ['**Found something. The 21 load losses and 16 usable-before-window losses are traced. Full candidate scoring is pending.**', '',
             '# 025 Load losses, partial handoff', '',
             'Codex runtime model and effort are independently unverified. The brief specifies neither.',
             f'Written {now:%Y-%m-%d %H:%M} Kuwait. Branch astra/025-load-losses. Tree node 1.2.', '',
             'The requested report filename and prohibition on git writes take precedence over the older brief. '
             'The runner handles the commit. The pre-existing runner lock is preserved.', '',
             '## CONFIRMED causes', '',
             'The 005 roster reproduces exactly. Of 52 fixed reference-window losses, 21 lack loaded centre support, '
             '15 have no recorded cadence near the centre, ten lie outside safe windows, and six lack safe windows. '
             'Twenty load cases have finite archived flux. The remaining case also lacks finite archived flux.', '',
             '| Blocking bits across nearby finite samples, or archived-flux limitation | Load cases |', '|---|---:|']
    for cause, count in diag['original_load_bits'].items():
        lines.append(f'| {cause} | {count} |')
    lines += ['', 'The blocking-bit entries are unions across nearby samples. '
              'detect_v2.load(), pipeline/detect_v2.py line 44, calls Lightkurve with the hard quality mask. '
              'The installed QLP reader adds its low-precision mask. Individual sample counts, quality words, '
              'files and exact source conditions are in data/astra/025/case-evidence.json. '
              'The private roster carries the predeclared hypothesis checklist for each original case.', '',
              'Bit 4096 is labelled Straylight2 by Lightkurve for SPOC-family files. QLP uses it for low precision '
              'before sector 56 and adds bit 1073741824 from sector 56. Bit 128 is manual exclusion, and bit '
              '2048 is stray light. The installed reader and actual returned timestamps supply the evidence.', '',
              'Zero of the 21 has a whole-sector FIX 101 mask. One also lacks safe windows. Three have another '
              'product with centre support after masking. Those three demonstrate that a best-product support '
              'loss can coexist with alternate search input. Recovery through detection and vetting is still pending.', '',
              '| Rule removing the 16 usable cases | Cases | Source condition |', '|---|---:|---|',
              '| Own SPOC support | 3 | stage2_search.py line 154 |',
              '| Neighbour intersection | 5 | stage2_search.py line 156 |',
              '| Half-day start trim | 2 | detect_v2.py line 111 |',
              '| Fewer than two neighbours and no own SPOC | 6 | stage2_search.py line 158 |', '',
              'These branches implement the recorded comments. One of the 16 has usable alternate-product '
              'support. Safety of widening their intervals remains NOT TESTED.', '',
              '## Across all 2,000 fixed T156 draws', '',
              'The dip is planted before eclipse masking in the final trace. First-loss accounting assigns '
              'each draw to its earliest classified support loss, preventing double counting of overlapping causes.', '',
              '| First classified loss or retained input | Draws |', '|---|---:|']
    for cause, count in diag['all_first_loss'].items():
        lines.append(f'| {cause} | {count} |')
    lines += ['', 'Missing selected files and missing manifest entries are both zero. FITS header sectors have '
              'zero mismatches over 4,613 traced trial/product rows. Every inspected header uses BJDREFI 2457000 '
              'and TIMESYS TDB. The full injected trace gives 94 drift-window first losses. Drift covers a selected '
              'product\'s complete retained sector in 64 draws. This supplies new T156 evidence for the existing '
              'FIX 101 work. It supplies zero whole-sector cases among the original 21 load losses.', '',
              'RS-038\'s separate 006 replay counts are cited as supplied, with no recount. Its 1,292 never-scored '
              'crossings comprise 526 mask, 248 no-finite-score, 235 safe-window, 192 best-product-table gaps, '
              '60 capture mismatches and 31 load cases. '
              '[RS-038](../../stage3/rs038/KEEP-PLANETS-THROUGH-VETTING-2026-11-15.md)', '',
              '## Candidate and tests completed', '',
              'The predeclared bench prototype admits quality bit 4096 in the primary and SAP/PDC loaders. '
              'It retains the other blocking bits and existing borrowed windows. No frozen pipeline file is edited. '
              'The candidate specification was saved before its outcomes. The proposed bench change is '
              'research/astra/scripts/025-loader-prototype.patch.', '',
              f'CONFIRMED. {sum(len(c["archived_mutations"]) for c in checks)} archived 4096 cases fail '
              'loaded centre support before the change, pass after it, and fail again under the reverted-policy '
              'mutation. This measures loaded support. Searched support still requires windows and masking.', '',
              'CONFIRMED on constructed light. Three wrong-epoch deep-eclipse controls, at 30-minute, 10-minute '
              'and 200-second sampling, become detected events when the quality bit is admitted. Both campaign '
              'workers reproduce this hazard. It demonstrates why recovery alone cannot establish safety.', '',
              'Runtime checks exercise 12 distinct product/era/median-cadence paths. The actual-quality audit '
              'covers 22 file/path instances. In two tested QLP files from sector 94 onward, 9,755 returned '
              'cadences retain bit 536870912. Four tested SPOC-family files retain 871 cadences with bit 32768. '
              'The physical meaning and safety of the QLP high bit remain UNCERTAIN here.', '',
              'Thirteen inherited rule/access checks pass, including a rejected dump-shape mutation. '
              'The Petrova synthetic mask self-test passes. The guard verifies twelve copied source hashes, '
              'three denied access events and one permitted output write. Exact frozen-source byte hashes '
              'were recorded before the candidate. This is producer verification. Independent review remains pending.', '',
              '## Pending deliverables', '',
              'NOT TESTED TO COMPLETION. The two-worker candidate generation and scoring run remains active '
              'after the authorized terminal waits. Its complete T156 R, planet P, both untouched-background '
              'arms, restored searched-centre count and 50-sector event identity are pending. No adoption '
              'verdict is supported yet. Its progress.json records the launch time and a three-hour planning '
              'estimate. Machine outputs and logs remain under data/astra/025.', '',
              'The acceptance rule requires at least 11 of the original 21 cases to gain searched centre support, '
              'higher T156 reference R, no extra upside-down tier-1 background and exact identity on 50 unaffected '
              'star-sectors. The fixed 006 planet P must also be measured. No setting will be changed from these outcomes.', '',
              'After terminal completion, 025_report.py renders the full report from summary.json and '
              'verification.json. 025_run.py is the existing bench entry point. It includes fresh generation, '
              'historical baseline scoring, candidate scoring, summary and verification. The worklog records '
              'execution order and the supplementary injection-before-mask trace.', '',
              '## What I did NOT check', '',
              '- Completed R/P/background/identity acceptance results. The run is still active.',
              '- SPOC 20-second data, absent from this fixed trace.',
              '- A drift-cap prototype, conditional on FIX 101 explaining the original 21 load losses.',
              '- Safety of relaxing other bits or widening the 16 windows.',
              '- G1 or fence-B light, sealed searches, independent scientific review, publication, or complete runner-log fence review.',
              '- Actual usage-panel percentages, unavailable in the headless runner.', '',
              '## STOP SIGNS hit', '',
              'No scientific adoption decision is made from an incomplete bench. The two capped terminal waits '
              'allowed by AGENTS are exhausted. The background job continues. Frozen files and sealed results '
              'received no edits or reinterpretation.', '',
              '## QUEUE PROPOSALS', '',
              'Node 1.2. Attach the cause table to the existing load/window and FIX 101 work. Hold any adoption '
              'decision until the requested bench gates are measured.', '',
              '## IDEAS', '', 'None beyond the requested prototype.', '',
              '## Disagreements with Claude', '',
              'The original 21 label is best-product centre support. Three cases retain alternate-product '
              'search input. The private case rows support this scope correction.', '',
              '## Questions for Ahmed', '', 'None.', '',
              '## Usage', '',
              'Predicted 40 five-hour points and 8 weekly points, cap 50 five-hour points. Actual bars are '
              'unavailable in the headless runner. AS-025 quality-policy provenance used installed primary '
              'source and runtime data, with a cap of two local calls and zero web calls. Lesson, keep loaded '
              'support, searched support and tier-1 recovery separate.', '',
              'Next action is Claude running 025_report.py after progress.json reaches complete, to render the '
              'verified bench verdict. This uses one local command, with model usage unmeasured.', '']
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print('Rendered partial counts-only 025-report.md')


if __name__ == '__main__':
    main()
