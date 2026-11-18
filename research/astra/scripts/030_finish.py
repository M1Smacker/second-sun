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
    usage = json.loads((OUT / '030d-usage.json').read_text(encoding='utf-8'))
    lines = [f'**Plain verdict: {"found something, chosen N1 passes every written gate" if s["passes"] else "six rules pass; rule (f) fails. N1 does not qualify under the written rules"}.**', '',
             '# 030 lower-flank notch tier bench', '',
             'Codex, runtime model and effort not independently verified for this continuation. Brief specifies neither. Branch astra/030d-notch-finish. No git writes or commits. Tree nodes 1.3, 1.5 and 1.6.', '',
             '## Findings', '',
             f'CONFIRMED as computed: chosen detection threshold {s["threshold"]:g}, selected only by the prewritten alarm limits. No filter was frozen or published.', '',
             '| Threshold | Real tier 1 | Upside-down tier 1 |', '|---:|---:|---:|']
    for row in s['alarm_curve']:
        lines.append(f'| {row["floor"]:g} | {row["real"]} | {row["upside_down"]} |')
    lines += ['', '| Population | n | B % | N1 % | Paired gain, points (95%) |', '|---|---:|---:|---:|---:|']
    for key, row in s['metrics'].items():
        lines.append(f'| {key} | {row["n"]} | {100*row["rates"][0]:.3f} | {100*row["rates"][2]:.3f} | {100*row["gain"]:+.3f} [{100*row["gain95"][0]:+.3f}, {100*row["gain95"][1]:+.3f}] |')
    lines += ['', 'P gives each of the five binary-period bins equal weight. A whole-star bootstrap keeps all planted planets on the same host together when resampling, avoiding falsely narrow intervals. There are 10,000 draws with seed 2026111830. Fable X1 seed is 2026111601.', '',
              '| Gate | Number or evidence | Outcome |', '|---|---|---|']
    descriptions = dict(a='Fresh gain at least 2 points and lower 95% bound above zero',
                        b='Both untouched alarm budgets', c='Dip/bump 99% interval contains zero in all possible-planet bins',
                        d='Off-switch and unchanged preprocessing checks', e='New real minus 2.3 times new upside-down at most 5',
                        f='Reference T156 R does not fall', g='TOI-1338 b at least six of thirteen')
    fresh = s['metrics']['fresh_possible']
    reference = s['metrics']['T156_reference']
    evidence = dict(a=f'{100*fresh["gain"]:+.3f} points, 95% [{100*fresh["gain95"][0]:+.3f}, {100*fresh["gain95"][1]:+.3f}]',
                    b='165 real <= 174; 77 upside-down <= 79',
                    c='10 of 10 choosing/fresh period-bin intervals include zero',
                    d='50 off-switch sector replays; saved N1 preprocessing comparisons; source checks',
                    e=f'{s["new_events"]["real"]} - 2.3 x {s["new_events"]["upside_down"]} = {s["new_events"]["excess"]:.1f} <= 5',
                    f=f'B {100*reference["rates"][0]:.3f}% to N1 {100*reference["rates"][2]:.3f}%',
                    g=f'B {s["known"]["B"]["total"]}/13; N1 {s["known"]["N1"]["total"]}/13')
    for key, yes in s['rules'].items():
        lines.append(f'| ({key}): {descriptions[key]} | {evidence[key]} | {"PASS" if yes else "FAIL"} |')
    new = s['new_events']
    lines += ['', f'CONFIRMED: new alarms against B are {new["real"]} real and {new["upside_down"]} upside-down; rule 4 excess is {new["excess"]:.1f}. Matching uses the existing bench tolerance, not exact event identity.', '',
              f'CONFIRMED: TOI-1338 b is {s["known"]["N1"]["total"]} of 13 under N1, versus {s["known"]["B"]["total"]} under B. The denominator includes nine observed and four forecast epochs from T109.', '',
              'Rule (g) uses the amended T109/Q5 sector-local context. B matches the historical six successful windows individually, with 10 of 10 O0 flag identities. N1 gives four observed-window and three forecast-window matches. Both versions assess all 13 windows; one has no stored data, as in historical Q5. The 19 existing N1 raw-light group replays cover the other 12 windows and were reused, then re-tiered at 6.5. No heavy phase was rerun. Design-background counts remain separately in known.json: B 1, N1 2. They are not rule (g).', '',
              '## Per-crossing and paired-control counts', '',
              '| Population | Period bin | Planets | Dip/bump planets | Crossings | Dip/bump crossings | Planet dip-minus-bump 99%, points | Control |',
              '|---|---|---:|---:|---:|---:|---:|---|']
    bins = ('5 to 10', '10 to 14', '14 to 20', '20 to 27.4', '27.4 and up')
    for key in ('choosing_possible', 'fresh_possible'):
        if key == 'fresh_possible':
            lines += ['| Population | Period bin | Planets | Dip/bump planets | Crossings | Dip/bump crossings | Planet dip-minus-bump 99%, points | Control |',
                      '|---|---|---:|---:|---:|---:|---:|---|']
        m = s['metrics'][key]
        for b, label in enumerate(bins):
            row = m['N1_crossings_by_bin'][b]
            counts = m['counts_by_bin'][b]
            control = m['control99'][0][b] <= 0 <= m['control99'][1][b]
            lines.append(f'| {key} | {label} | {m["n_by_bin"][b]} | {counts[2]}/{counts[3]} | {row["n"]} | {row["real"]}/{row["flip"]} | [{100*m["control99"][0][b]:+.3f}, {100*m["control99"][1][b]:+.3f}] | {"PASS" if control else "FAIL"} |')
        lines += ['', f'{key} pooled per-crossing tier-1 rate: {100*m["N1_crossing_rate"]:.3f}%.', '']
    lines += ['## Flags holding new untouched detections', '', 'Counts overlap; they are not additive causes.', '']
    for arm, row in s['holds'].items():
        lines += [f'{arm}: {row["new_detections"]} new detections, {row["not_tier1"]} below tier 1. ' + ', '.join(f'{k} {v}' for k, v in sorted(row['flags'].items())) + '.', '']
    lines += ['## Background by brightness, product, era and period', '',
              '```json', json.dumps(s['background_strata'], indent=2), '```', '',
              '## Verification and evidence', '',
              'CONFIRMED: full saved-outcome B scoring matches both arms trial by trial, including P 48.105% / 48.404%, R 34.207%, and alarms 174 / 79. Independent 030_recount.py joins archived outcomes to raw injection journals without importing the pipeline. Raw off-switch event identity covers 50 untouched star-sectors. N1 untouched preprocessing metadata is checked against B for every regenerated group.', '',
              'N1 reference parity and a separate direct-window oracle cover 27 cadence/duration cases. Deliberate wrong-flank, threshold-context and one-arm-budget mutations are rejected. Three mirror boundary checks, 15 candidate-nesting checks, zero-scale handling, source hashes, worker completion and population assertions also ran. These are producer checks, not independent review.', '',
              'Evidence: data/astra/030/summary.json, verification.json, notch-checks.json, baseline-check.json, independent-recount.json, known.json, chosen.json and worker logs. This continuation ran 030_t109.py, 030_summary.py, 030_verify.py and 030_finish.py with the required interpreter and -I -B. Do not restart 030_run.py. Frozen source files were not edited.', '',
              '030d verification independently recounts the saved final T109 tiers, checks the historical B windows, checks 38 input hashes, checks all saved worker completion records, and validates the summary populations and threshold rule. A mutation removing N1 tier-1 hits from the private scored rows is rejected; restoration passes. Earlier raw identity and synthetic checks are saved evidence, not rerun here. Hash equality proves byte identity only. Claude independently recounted the bench in research/stage3/rs039/RECOUNT-030-2026-11-18.md; point estimates and gate verdicts agree. His fresh 95% interval is +0.12 to +4.15; the prescribed 030 bootstrap gives +0.161 to +4.105. The interval difference does not change rule (a). That recount does not independently review the new T109 implementation.', '',
              'Source amendment: only 030_finish.py and 030_verify.py changed among the locked existing scripts; 030_t109.py was added. Full old/new SHA-256 maps are in data/astra/030/030d-source-amendment.json. The scoring, generation, threshold selection and summary sources remain unchanged from the 030b lock. The prior report is preserved privately as 030d-prior-report.md. Earlier 030b amendment provenance remains in 030b-source-amendment.json.', '',
              'The preserved design-background note says two of thirteen sectors. It must not be read as raw-input coverage: the archive and N1 replays cover twelve crossing sectors. The amended sector-local test and full campaign background use different event contexts.', '',
              '## What I did NOT check', '',
              'No fenced-star searches, witness-star meter, sky search, new downloads, frozen release, book edits or publication. No independent reviewer has assessed this implementation. The benchmark does not establish sensitivity for all planets in the sky. Per-crossing rates are pooled within the reported populations; alarms have brightness/product/era splits, while planet P uses the specified period-bin weighting.', '',
              '## STOP SIGNS hit', '',
              'No scientific gate was relaxed. Rule (f) fails, so N1 does not qualify for adoption under this brief. An initial 030d availability assertion demanded stored data in every window; historical Q5 explicitly includes one missing window. That implementation assertion was corrected to preserve the historical missing outcome before B or N1 was scored. B then reproduced 6/13 before N1 was evaluated. The earlier 030b meter stop and nine-versus-ten grid wording are preserved in the prior report; the actual nine-length grid was retained.', '',
              '## QUEUE PROPOSALS', '',
              'None. This is the requested node 1.3 bench, not a filter adoption.', '',
              '## IDEAS', '', 'None outside the brief.', '',
              '## Disagreements with Claude', '', 'None on the completed verdict. The source uses nine grid lengths despite the original brief saying ten. No scientific decision was silently changed.', '',
              '## Questions for Ahmed', '', 'None.', '',
              '## Usage', '',
              f'030d predicted 35 five-hour points / 6 weekly points. Latest observed actual: {usage["actual"]}. Account-wide rounded meter, measured before final handoff. Earlier 030 and 030b usage rows remain separate. Lesson: reproduce the historical context and missing-data outcomes before judging a known-system gate.', '',
              'Next: Claude reviews the report and producer checks before any adoption decision; review cost unmeasured, Claude required.']
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Wrote counts-only 030 report from terminal verified evidence.')


if __name__ == '__main__':
    main()
