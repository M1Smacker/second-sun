"""Render counts-only terminal evidence after the verifier succeeds."""
import json
from pathlib import Path
ROOT=Path(r'D:\second-sun-astra'); OUT=ROOT/'data/astra/028'; REPORT=ROOT/'research/astra/reports/028-report.md'


def main():
    s=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    v=json.loads((OUT/'verification.json').read_text(encoding='utf-8')); assert v['passed']
    old=REPORT.read_text(encoding='utf-8')
    design=old[old.index('## Pass rule recorded BEFORE scoring'):old.index('## Usage')]
    passed=[name for name,r in s['rules'].items() if r['passes']]
    lines=[f'**{"Passes the initial bench" if passed else "Fails"}: {len(passed)} of 4 orbit configurations passes all five rules.**','',
        '# 028 Orbit-consistent search','',
        'Requested GPT-6-Astra high; runtime model/effort independently unverified. Branch astra/028-orbit-search. No commits or git writes. Tree nodes 1.1 and 1.3.','',design,
        '## Findings, CONFIRMED as computed','',
        'This is producer verification, not independent review. Bootstrap intervals quantify host sampling variability within this restricted experiment. The score is an empirically calibrated ranking statistic, not a Gaussian significance.','',
        '| Configuration | P all 1,098 %, 95% | P possible 968 %, 95% | T156 R %, 95% | Real / upside-down |',
        '|---|---:|---:|---:|---:|']
    def interval(key,i):
        m=s['metrics'][key]
        return f"{100*m['rates'][0][i]:.3f} [{100*m['rate95'][0][0][i]:.2f}, {100*m['rate95'][1][0][i]:.2f}]"
    for i,name in enumerate(s['configs']):
        bg=s['background'][i]
        lines.append(f"| {name} | {interval('fixed1098',i)} | {interval('possible968',i)} | {interval('T156reference',i)} | {bg['real']} / {bg['flip']} |")
    lines += ['', '| Population | Configuration | Paired gain vs matching base, points (95%) |', '|---|---|---:|']
    for key in ('fixed1098','possible968','T156reference'):
        m=s['metrics'][key]
        for i in range(2,6):
            lines.append(f"| {key} | {s['configs'][i]} | {100*m['gain'][i]:+.3f} [{100*m['gain95'][0][i]:+.3f}, {100*m['gain95'][1][i]:+.3f}] |")
    cal=s['calibration']
    lines += ['', '## Null calibration', '',
        f"Both campaigns and arms: {cal['host_arms']} host-arms, {cal['templates']} pair-anchored templates, {cal['sets']} distinct sets before the floor. Best null score {cal['max_null']:.6f}; floor {cal['floor']:.6f}. Zero sets above the floor. The floor was written to calibration.json before injected orbit scoring. Missing-epoch host-arms excluded from orbit fits: {cal['missing_geometry_host_arms']}.", '',
        f"Mutation removing orbit timing: {cal['sets']} to {cal['mutation_sets']} sets. Sensitive: {cal['mutation_sensitive']}. Synthetic independent forward-root test also rejected two-event sets and duplicate crossings.", '',
        'Same-sample background adds zero A or B events by construction. This is training calibration, not independent evidence of zero future false alarms. There are zero new real events requiring dump or eclipse blind-spot checks against either matching base. Background splits by brightness, product and era are saved in summary.json; all additions in each split are zero.', '',
        '| Campaign | Arm | Bin | Hosts | Hosts with sets | Sets before floor | Sets per host |', '|---|---|---:|---:|---:|---:|---:|']
    for r in cal['strata']:
        mean=r['sets']/r['hosts'] if r['hosts'] else 0
        lines.append(f"| {r['campaign']} | {r['arm']} | {r['bin']+1} | {r['hosts']} | {r['hosts_with_set']} | {r['sets']} | {mean:.4f} |")
    lines += ['', '## Rules against the matching base', '', '| Configuration | a: possible gain, 95% points | b: real / upside-down | c: both-population controls | d: R vs base % | e: new-real excess | Verdict |','|---|---|---|---|---|---|---|']
    m=s['metrics']['possible968']; ref=s['metrics']['T156reference']
    for i in range(2,6):
        name=s['configs'][i]; r=s['rules'][name]; base=0 if i<4 else 1; bg=s['background'][i]
        lines.append(f"| {name} | {100*m['gain'][i]:+.3f} [{100*m['gain95'][0][i]:+.3f}, {100*m['gain95'][1][i]:+.3f}], {r['a']} | {bg['real']} / {bg['flip']}, {r['b']} | {r['c']} | {100*ref['rates'][0][i]:.3f} vs {100*ref['rates'][0][base]:.3f}, {r['d']} | {bg['rule4']:.1f}, {r['e']} | {'PASS' if r['passes'] else 'FAIL'} |")
    lines += ['', '## Paired changes, counts and controls', '',
        '| Population | Configuration | Bin | n | Dip gained / lost | Bump gained / lost | Dip-minus-bump 99%, points |',
        '|---|---|---:|---:|---:|---:|---|']
    for key in ('fixed1098','possible968'):
        m=s['metrics'][key]
        for i in range(2,6):
            for b in range(5):
                a=m['moves'][b][0][i]; c=m['moves'][b][1][i]
                lines.append(f"| {key} | {s['configs'][i]} | {b+1} | {m['n'][b]} | {a[0]} / {a[1]} | {c[0]} / {c[1]} | [{100*m['control99'][0][b][i]:.3f}, {100*m['control99'][1][b][i]:.3f}] |")
    inv=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
    caps=inv['capture_coverage_by_bin']
    lines += ['', '## Multiplicity and limitations', '',
        f"Capture inventory joins all {sum(r['captured'] for r in caps)} observed planets. {sum(r['three_scored'] for r in caps)} have at least three scored crossings at their own template times. Among B misses, {sum(r['B_missed_three_scored'] for r in caps)} of {sum(r['B_missed'] for r in caps)} do. This is a necessary multiplicity ceiling, not proof they are soft-held or orbit-search eligible.", '',
        f"Restricting further to detected but unrecovered planets: B has {sum(r['B_detected_missed_three_scored'] for r in caps)} with three scored crossings out of {sum(r['B_detected_missed'] for r in caps)}; K2 has {sum(r['K2_detected_missed_three_scored'] for r in caps)} out of {sum(r['K2_detected_missed'] for r in caps)}. This includes novelty exclusions, so it is not an exact count of soft-held planets.", '',
        '## What I did NOT check', '',
        'Eccentric or mutually inclined orbits, secondary-star transits, true stellar mass ratios, N-body dynamics, periods outside 4 to 8 binary periods, candidates below SNR 4, continuum completeness between pair-anchored templates, independent null validation, pixel-level evidence or G1. M2 was skipped because its SNR-7 replays do not supply the lower-threshold candidate bank. No frozen filter was changed.', '',
        ('Fresh-seed confirmation is REQUIRED and NOT RUN. The initial bench passes for at least one variant; this is a partial handoff until the 1,250 fresh planets are scored.' if passed else 'Fresh-seed confirmation was not triggered because no variant passed all five rules.'), '',
        '## Verification', '', f"Terminal runtime verification: {json.dumps(v['counts'],sort_keys=True)}. The historical B and K2 baseline outcomes are copied by identity and independently recounted, not a new from-scratch baseline fit. Raw zero-injection identity is checked on 25 design sectors in each campaign. Hashes establish source byte identity only.", '',
        '## STOP SIGNS hit', '',
        'No scientific fence breach identified. The foreground request conflicts with the explicit AGENTS background/no-polling rule; the latter was followed. Runtime results are usable only after terminal verification, never from checkpoints.', '',
        '## QUEUE PROPOSALS', '',
        'Tree nodes 1.1 and 1.3: Claude should review this restricted-orbit experiment and its same-sample calibration before any adoption. No production change proposed by this report.', '',
        '## IDEAS', '', 'None beyond the requested experiment.', '',
        '## Disagreements with Claude', '', 'None. A failed restricted search does not reject orbit searches in general.', '',
        '## Questions for Ahmed', '', 'None.', '',
        '## Usage', '',
        'Predicted 60 five-hour / 10 weekly points. Actual meter unavailable in the headless runner, so actual/predicted ratio is unavailable. Lesson: candidate-score coverage must be audited before promising reuse of an injected-time cache.', '',
        'Next: Claude reviews the report and private verification output before deciding whether this experiment warrants more work; review usage is unmeasured.']
    REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Wrote counts-only 028 report; fresh seed required:',bool(passed))


if __name__=='__main__': main()
