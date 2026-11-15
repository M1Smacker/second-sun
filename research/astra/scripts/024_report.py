"""Append the measured outcome to the method recorded before computation."""
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/024'
REPORT = ROOT / 'research/astra/reports/024-report.md'
LABELS = ('5 to 10', '10 to 14', '14 to 20', '20 to 27.4', '27.4+')


def main():
    data = json.loads((OUT / 'summary.json').read_text(encoding='utf-8'))
    verification = json.loads((OUT / 'verification.json').read_text(encoding='utf-8'))
    strata = json.loads((OUT / 'strata.json').read_text(encoding='utf-8'))
    progress = json.loads((OUT / 'progress.json').read_text(encoding='utf-8'))
    assert progress['status'] == 'complete'
    passed = sum(row['passes'] for row in data['gates'])
    verdict = f'**{passed} of 2 subtraction configurations pass the fixed gates.**'
    original = REPORT.read_text(encoding='utf-8-sig').split('\n## Measured outcome')[0]
    original = verdict + '\n' + original.split('\n', 1)[1]
    lines = ['', '## Measured outcome', '',
             'CONFIRMED. Both campaigns, both injection signs, both benchmarks and untouched background were scored. '
             'The table preserves the fixed denominators. Rates give equal weight to the five binary-period bins. '
             'Intervals use 10,000 paired whole-star bootstrap resamples. Producer verification ran in this session. '
             'Independent review is pending. The brief quotes the earlier frozen short-bin result of 6 / 48. '
             'Adopted B gives 7 / 48, matching 023 trial by trial.', '',
             '| Configuration | P %, 95% interval | R %, 95% interval | Real background | Upside-down background |',
             '|---|---|---|---:|---:|']
    for j, name in enumerate(data['configurations']):
        values = []
        for bench in ('planets', 'reference'):
            measurement = data['measurements'][bench]
            values.append(f"{measurement['overall'][0][j]*100:.3f} [{measurement['overall_ci95'][0][0][j]*100:.2f}, {measurement['overall_ci95'][1][0][j]*100:.2f}]")
        background = data['background'][j]
        lines.append(f"| {name} | {values[0]} | {values[1]} | {background['real']} | {background['flip']} |")
    for bench, title in (('planets', 'Planet bench P'), ('reference', 'T156 reference R')):
        m = data['measurements'][bench]
        lines += ['', f'### {title}', '',
                  '| Period, days | Trials | B found / tier 1 | B+C96 found / tier 1 | Subtraction found / tier 1 | C96+subtraction found / tier 1 |',
                  '|---|---:|---|---|---|---|']
        for b, label in enumerate(LABELS):
            cells = [f"{m['found_counts'][b][0][j]} / {m['counts'][b][0][j]}" for j in range(4)]
            lines.append(f"| {label} | {m['n'][b]} | " + ' | '.join(cells) + ' |')
        lines += ['', 'Found means at least one primary SNR-7 event matching an injected crossing. '
                  'Tier 1 additionally applies the adopted gates and the same-configuration pre-existing-event exclusion. '
                  'C96 acts during tiering, so the detection count is shared by the two cap settings.', '',
                  '| Period, days | Subtraction tier-1 change, 95% | C96+subtraction matched change, 95% | C96+subtraction against B, 95% | Subtraction detection change, 95% |',
                  '|---|---|---|---|---|']
        for b, label in enumerate(LABELS):
            cells = []
            for field, j in (('delta_ci95', 2), ('delta_ci95', 3), ('delta_B_ci95', 3), ('found_delta_ci95', 2)):
                cells.append(f"[{m[field][0][b][0][j]*100:.2f}, {m[field][1][b][0][j]*100:.2f}]")
            lines.append(f'| {label} | ' + ' | '.join(cells) + ' |')
        lines += ['', 'Changes are percentage points. The matched C96 column uses B+C96. The other tier-1 columns use B.', '',
                  '| Period, days | B paired control, 99% | B+C96 paired control, 99% | Subtraction paired control, 99% | C96+subtraction paired control, 99% |',
                  '|---|---|---|---|---|']
        for b, label in enumerate(LABELS):
            cells = [f"[{m['control_ci99'][0][b][j]*100:.2f}, {m['control_ci99'][1][b][j]*100:.2f}]" for j in range(4)]
            lines.append(f'| {label} | ' + ' | '.join(cells) + ' |')
        lines += ['', 'The paired control is dip recovery minus bump recovery. The historical fairness rule requires zero inside each 99% interval.']
    lines += ['', '### Background per period bin', '',
              '| Period, days | B real / upside-down | B+C96 | Subtraction | C96+subtraction |',
              '|---|---|---|---|---|']
    for b, label in enumerate(LABELS):
        cells = [f"{row['bins'][b]['real']} / {row['bins'][b]['flip']}" for row in data['background']]
        lines.append(f'| {label} | ' + ' | '.join(cells) + ' |')
    lines += ['', '### Fixed gates', '',
              'Both subtraction configurations are judged against B for the recovery gates. '
              'The matched C96 comparison in the tables separately measures the incremental subtraction effect.', '']
    for gate in data['gates']:
        failed = [name.replace('_', ' ') for name, value in gate['tests'].items() if not value]
        lines.append(f"- {gate['configuration']} {'PASS' if gate['passes'] else 'FAIL'}. Failed conditions are {', '.join(failed) if failed else 'none'}.")
    lines += ['', '### Coverage and scatter', '',
              f"CONFIRMED. {data['total_star_sectors']} design star-sectors on {data['total_stars']} campaign-star clusters were assessed. "
              f"Subtraction changed {data['changed_stars']} stars. Sector statuses are {json.dumps(data['coverage'], sort_keys=True)}. "
              'The FITS header span provides an upper bound for the early skip. Potentially eligible products use their actual retained time coverage. '
              'All short-period products passing the ordinary loader and mask have before/after scatter measurements, including no-op skips.', '',
              f"The three-cycle span rule skipped all products in {data['fewer_than_three_cycles_sectors']} star-sectors. "
              f"{data['fewer_than_three_cycles_all_sectors_stars']} stars had insufficient span in every assessed sector. "
              'Additional exits arise from fixed safe windows, raw cadence counts and occupied-bin cycle coverage.', '',
              f"Per-star median product scatter, aggregated across {data['scatter']['stars']} measured stars, changed from "
              f"{data['scatter']['before_median_ppm']:.1f} to {data['scatter']['after_median_ppm']:.1f} ppm. "
              'Individual per-star measurements are retained in data/astra/024/per-star-scatter.json. '
              'This scatter is measured after masking and before detrending.', '',
              '### Worst-case repeated-phase control', '',
              '| Stage | Median retained depth % | Minimum % | Maximum % |',
              '|---|---:|---:|---:|']
    for stage, row in data['controls'].items():
        lines.append(f"| {stage.replace('_', ' ')} | {row['median']*100:.2f} | {row['minimum']*100:.2f} | {row['maximum']*100:.2f} |")
    lines += ['', 'CONFIRMED. Twenty stars were tested with the same-phase eight-hour planted dip every binary cycle. '
              'Depth is measured from paired flux differences on shared cadences. Values above 100% or below zero can occur from changing masks and model responses. '
              'The control measures attenuation of a deliberately phase-locked signal. Ordinary circumbinary crossings use the original drifting 006 geometry.', '',
              '### Implementation coverage correction', '',
              'CONFIRMED. The first summary used an incomplete no-op shortcut. A learned eclipse mask can change after injection, '
              'which can change phase coverage even when the untouched subtraction is a no-op. The final measurement explicitly reran both signs '
              'on 104 one-bin or coverage-dependent sectors and 93 sectors with an empty learned mask. All 197 supplementary sectors enter the final scorer. '
              'The remaining reused cases have a fixed under-three-cycle time span or an input-independent pre-mask exit. '
              'The bin rule, draws, denominator and pass rule stayed fixed. The earlier summary is superseded.', '',
              '### Verification actually performed', '',
              f"- {data['identity_groups']} disabled-subtraction primary/SAP groups reproduced their stored event lists. "
              'Every B and C96 trial outcome reproduced 023 in both benches. Background reproduced 174 / 79 and 124 / 53.',
              f"- The subtraction step commuted with inversion on processed real light, maximum error {data['symmetry_max_error']:.3g}. "
              'The unchanged eclipse mask remains part of the historical baseline. This identity tests the added operator on shared masked cadences.',
              '- Six synthetic checks ran, including a deliberately asymmetric operator rejected by the symmetry test. The phase-locked synthetic control exposed attenuation.',
              '- Six paired-cluster regression checks ran. Duplicating within-star trials preserved the intervals, and actual independently resampled arms produced a false difference rejected by the paired-identity test.',
              f"- The runtime verifier completed {len(verification['checks'])} groups of checks. " + ', '.join(verification['checks']) + '.',
              '- Static parsing covered the newly authored Python scripts separately from runtime experiments. '
              'Source hashes checked the redirected module copies. Hash agreement establishes byte provenance. '
              'Runtime identity, coverage and independent counting logic establish the stated behavioral evidence.', '',
              'The path redirector initially changed an unused legacy selection seed along with the output paths. '
              'The seed was restored. A byte comparison confirms that this unused select() constant is the only difference from the measured source snapshot. '
              'The bench never calls select(). All twelve delivered copies preserve the numerical literals of their 023 source. '
              'The measured source bundle is retained privately under data/astra/024/source-bundle-at-measurement.', '',
              '## Reproduction', '',
              'From this worktree run `D:/second-sun/.venv/Scripts/python.exe -I -B research/astra/scripts/024_run.py --score-only` '
              'to reproduce the final scoring, summary, descriptive splits and verification from the completed raw replays. '
              '024_prepare.py recreates the redirected harness sources. '
              'The default 024_run.py entry point also runs raw generation, eligibility auditing and both supplementary coverage passes. '
              'Worker destinations cache event groups, so a fresh raw rerun requires preserving the existing generated, coverage and empty folders elsewhere under data/astra/024 first. '
              'The supervisor writes progress.json and private logs under data/astra/024. '
              '024_report.py appends this measured handoff to the recorded method.', '',
              '## What I did NOT check', '',
              '- NOT TESTED. Production integration, a Petrova freeze, G1, sealed stars, known published-system recovery, alternative bin rules or a per-sector physical binary model.',
              '- NOT TESTED. Independent scientific review and the complete runner session-log fence check. Claude owns that handoff check.',
              '- NOT TESTED. Bootstrap sensitivity to another seed or another cluster definition. Intervals describe the fixed design-star bench.',
              '- Brightness, product and era counts are descriptive splits in the supplemental table. Their subgroup uncertainty and fairness gates were NOT TESTED. The requested scatter uses each available prepared product.', '',
              '## STOP SIGNS hit', '',
              'Procedural deviation. Synthetic operator checks ran before the full method text was recorded in the report. '
              'The method and pass rule were recorded before raw-light experiments and outcome inspection.', '',
              'No frozen source was edited and no threshold was selected from measured outcomes. The literature and synthetic tests showed the known phase-lock attenuation mechanism. '
              'The pass rule remains fixed. Any recovery loss or background increase is handed to Fable for the design decision.', '',
              '## QUEUE PROPOSALS', '',
              'Node 1.5. Attach this measured subtraction outcome, its paired uncertainty and repeated-phase depth loss to the existing short-binary review. Claude files the result.', '',
              '## IDEAS', '',
              'No additional method was built.', '',
              '## Disagreements with Claude', '',
              'None on adoption. This is a bench measurement and the fixed gates determine the recorded outcome.', '',
              '## Questions for Ahmed', '',
              'None. The headless instruction was followed.', '',
              '## Usage and timing', '',
              'Predicted 55 five-hour points and nine weekly points. Brief cap 60 five-hour points. '
              'Actual meters and model effort are unavailable in this headless runner. Four web calls were used. '
              f"Supervisor started {progress['started']}, expected {progress['expected_finish']}, finished {progress['finished']}. "
              'Two capped terminal waits covered the initial run. A scoring-only retry followed an adapter naming collision. '
              'Healthy-run logs were left unread during completion waits. The initial raw-light outputs were reused.', '',
              'Lesson. A median model can lower repeated binary noise and absorb a signal that shares its binary phase. '
              'The paired raw-injection experiment measures both effects before adoption.', '',
              '**Next:** Claude reviews report 024 and runs the fence check for Fable. This needs Claude, with review usage unmeasured.']
    REPORT.write_text(original + '\n'.join(lines) + '\n', encoding='utf-8')
    supplement = ['# 024 descriptive recovery splits', '',
                  'CONFIRMED counts on the fixed bench. Cells show tier-1 dip / bump recoveries. '
                  'These are subgroup counts, with sample-weighted rates obtainable from the denominator. '
                  'Period-balanced P and R and their uncertainty remain in 024-report.md. '
                  'Mixed product or era means a planet has changed sectors spanning multiple categories. '
                  'Subgroup uncertainty and fairness gates were not tested.', '',
                  '| Bench | Split | Category | Trials | B | B+C96 | Subtraction | C96+subtraction |',
                  '|---|---|---|---:|---|---|---|---|']
    for row in strata:
        cells = [f"{a} / {b}" for a, b in zip(row['real'], row['flip'])]
        supplement.append(f"| {row['bench']} | {row['dimension']} | {row['label']} | {row['n']} | " + ' | '.join(cells) + ' |')
    supplement += ['', '## All 2,000 T156 trials', '',
                   'This includes the complete T156 depth/duration grid. The 222-trial Saturn-like reference defines R in the main report.', '',
                   '| Period, days | Trials | B dip / bump | B+C96 | Subtraction | C96+subtraction |',
                   '|---|---:|---|---|---|---|']
    all_trials = data['measurements']['all_T156']
    for b, label in enumerate(LABELS):
        cells = [f"{all_trials['counts'][b][0][j]} / {all_trials['counts'][b][1][j]}" for j in range(4)]
        supplement.append(f"| {label} | {all_trials['n'][b]} | " + ' | '.join(cells) + ' |')
    REPORT.with_name('024-strata.md').write_text('\n'.join(supplement) + '\n', encoding='utf-8')
    print(verdict)


if __name__ == '__main__':
    main()
