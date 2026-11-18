"""Write the counts-only terminal report after the foreground run is complete."""
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/030'
REPORT = ROOT / 'research/astra/reports/030-report.md'


def main():
    progress = json.loads((OUT / 'progress.json').read_text(encoding='utf-8'))
    assert progress['status'] == 'complete', 'Do not replace a partial report without terminal evidence'
    verification = json.loads((OUT / 'verification.json').read_text(encoding='utf-8'))
    assert verification['passed']
    s = json.loads((OUT / 'summary.json').read_text(encoding='utf-8'))
    lines = [f'**Plain verdict: {"found something, chosen N1 passes every written gate" if s["passes"] else "chosen N1 fails at least one written gate"}.**', '',
             '# 030 lower-flank notch tier bench', '',
             'Codex, GPT-6-Astra high (local runner metadata). Brief specifies no model or effort. Branch astra/030-notch-tier-bench. No git writes or commits. Tree nodes 1.3, 1.5 and 1.6.', '',
             '## Findings', '',
             f'CONFIRMED as computed: chosen detection threshold {s["threshold"]:g}, selected only by the prewritten alarm limits. No filter was frozen or published.', '',
             '| Threshold | Real tier 1 | Upside-down tier 1 |', '|---:|---:|---:|']
    for row in s['alarm_curve']:
        lines.append(f'| {row["floor"]:g} | {row["real"]} | {row["upside_down"]} |')
    lines += ['', '| Population | n | B % | N1 % | Paired gain, points (95%) |', '|---|---:|---:|---:|---:|']
    for key, row in s['metrics'].items():
        lines.append(f'| {key} | {row["n"]} | {100*row["rates"][0]:.3f} | {100*row["rates"][2]:.3f} | {100*row["gain"]:+.3f} [{100*row["gain95"][0]:+.3f}, {100*row["gain95"][1]:+.3f}] |')
    lines += ['', 'P gives each of the five binary-period bins equal weight. A whole-star bootstrap keeps all planted planets on the same host together when resampling, avoiding falsely narrow intervals. There are 10,000 draws with seed 2026111830. Fable X1 seed is 2026111601.', '',
              '| Gate | Outcome |', '|---|---|']
    descriptions = dict(a='Fresh gain at least 2 points and lower 95% bound above zero',
                        b='Both untouched alarm budgets', c='Dip/bump 99% interval contains zero in all possible-planet bins',
                        d='Off-switch and unchanged preprocessing checks', e='New real minus 2.3 times new upside-down at most 5',
                        f='Reference T156 R does not fall', g='TOI-1338 b at least six of thirteen')
    for key, yes in s['rules'].items():
        lines.append(f'| {key}: {descriptions[key]} | {"PASS" if yes else "FAIL"} |')
    new = s['new_events']
    lines += ['', f'CONFIRMED: new alarms against B are {new["real"]} real and {new["upside_down"]} upside-down; rule 4 excess is {new["excess"]:.1f}. Matching uses the existing bench tolerance, not exact event identity.', '',
              f'CONFIRMED: TOI-1338 b is {s["known"]["N1"]["total"]} of 13 under N1, versus {s["known"]["B"]["total"]} under B. The denominator includes nine observed and four forecast epochs from T109.', '',
              '## Per-crossing and paired-control counts', '',
              '| Population | Period bin | Crossings | Novel dip tier 1 | Novel bump tier 1 | Planet dip-minus-bump 99%, points |',
              '|---|---|---:|---:|---:|---:|']
    bins = ('5 to 10', '10 to 14', '14 to 20', '20 to 27.4', '27.4 and up')
    for key in ('choosing_possible', 'fresh_possible'):
        m = s['metrics'][key]
        for b, label in enumerate(bins):
            row = m['N1_crossings_by_bin'][b]
            lines.append(f'| {key} | {label} | {row["n"]} | {row["real"]} | {row["flip"]} | [{100*m["control99"][0][b]:+.3f}, {100*m["control99"][1][b]:+.3f}] |')
        lines += ['', f'{key} pooled per-crossing tier-1 rate: {100*m["N1_crossing_rate"]:.3f}%.', '']
    lines += ['## Flags holding new untouched detections', '', 'Counts overlap; they are not additive causes.', '']
    for arm, row in s['holds'].items():
        lines += [f'{arm}: {row["new_detections"]} new detections, {row["not_tier1"]} below tier 1. ' + ', '.join(f'{k} {v}' for k, v in sorted(row['flags'].items())) + '.', '']
    lines += ['## Background by brightness, product, era and period', '',
              '```json', json.dumps(s['background_strata'], indent=2), '```', '',
              '## Verification and evidence', '',
              'CONFIRMED: full saved-outcome B scoring matches both arms trial by trial, including P 48.105% / 48.404%, R 34.207%, and alarms 174 / 79. Independent 030_recount.py joins archived outcomes to raw injection journals without importing the pipeline. Raw off-switch event identity covers 50 untouched star-sectors. N1 untouched preprocessing metadata is checked against B for every regenerated group.', '',
              'N1 reference parity and a separate direct-window oracle cover 27 cadence/duration cases. Deliberate wrong-flank, threshold-context and one-arm-budget mutations are rejected. Three mirror boundary checks, 15 candidate-nesting checks, zero-scale handling, source hashes, worker completion and population assertions also ran. These are producer checks, not independent review.', '',
              'Evidence: data/astra/030/summary.json, verification.json, notch-checks.json, baseline-check.json, independent-recount.json, known.json, chosen.json and worker logs. Reproduction command after preparation: `D:\\second-sun\\.venv\\Scripts\\python.exe -I -B research/astra/scripts/030_run.py`. Frozen source files were not edited.', '',
              '## What I did NOT check', '',
              'No fenced-star searches, witness-star meter, sky search, new downloads, frozen release, book edits or publication. No independent reviewer has assessed this implementation. The benchmark does not establish sensitivity for all planets in the sky. Per-crossing rates are pooled within the reported populations; alarms have brightness/product/era splits, while planet P uses the specified period-bin weighting.', '',
              '## STOP SIGNS hit', '',
              'The brief calls the frozen grid ten lengths; its code and reference have nine, which were retained. An early terminal-status poll returned no output before the 30-minute interval; it was not used to inspect healthy logs or tune settings. A test-result JSON writer initially rejected a NumPy integer; converting the counter to a Python integer fixed it and the full check reran.', '',
              '## QUEUE PROPOSALS', '',
              'None. This is the requested node 1.3 bench, not a filter adoption.', '',
              '## IDEAS', '', 'None outside the brief.', '',
              '## Disagreements with Claude', '', 'Only the documented nine-versus-ten grid wording. No scientific decision was silently changed.', '',
              '## Questions for Ahmed', '', 'None.', '',
              '## Usage', '',
              'Predicted 60 five-hour points / 10 weekly points. The initial local meter was 38% five-hour / 71% weekly; terminal meter requires a fresh session-log reading. See USAGE.md. Lesson: lock the threshold before fresh scoring, and rebuild event-context flags before applying each threshold.', '',
              'Next: Claude reviews the report and producer checks before any adoption decision; review cost unmeasured, Claude required.']
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Wrote counts-only 030 report from terminal verified evidence.')


if __name__ == '__main__':
    main()
