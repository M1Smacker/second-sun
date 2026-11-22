"""Render the completed counts-only result, only after terminal verification."""
import json
from pathlib import Path

ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/031'


def main():
    s=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    v=json.loads((OUT/'verification.json').read_text(encoding='utf-8'))
    assert v['status']=='passed'
    failed=[k for k,passed in s['gates'].items() if not passed]
    verdict='All seven rules pass; D1 qualifies for review, not a freeze.' if not failed else 'D1 fails rule(s) '+', '.join(failed)+'; it does not qualify.'
    lines=[f'**Plain verdict: {verdict}**','', '# 031 duration-aware notch D1','',
           'Codex, runtime model and effort unverified; brief specifies neither. Branch `astra/031-duration-notch`. No git writes or commits. Tree nodes 1.3, 1.5 and 1.6.','',
           '## Findings','',
           'CONFIRMED as computed by the producer: the fixed 8-hour split was judged on new seeds 2026112201 and 2026112202. No cut or threshold was tuned. Old choosing, fresh and T156 results are exploratory.','',
           '| Population | n | B % | N1 % | D1 % | D1 minus B, points (95%) |',
           '|---|---:|---:|---:|---:|---|']
    for name,m in s['populations'].items():
        lo,hi=m['gain95']
        lines.append(f"| {name} | {m['n']} | {100*m['rates'][0]:.3f} | {100*m['rates'][2]:.3f} | {100*m['rates'][4]:.3f} | {100*m['gain']:+.3f} [{100*lo:+.3f}, {100*hi:+.3f}] |")
    lines+=['','P and R give equal weight to five binary-period bins. Whole-star resampling keeps every trial on the same host together, so repeated trials do not pretend to be independent stars. Intervals use 10,000 draws, seed 2026112230.','',
            '| Rule | Outcome |','|---|---|']
    for gate,passed in s['gates'].items():
        lines.append(f'| {gate} | {"PASS" if passed else "FAIL"} |')
    lines+=['',f"Untouched tier-1 counts: B {s['background']['B']}; N1 {s['background']['N1']}; D1 {s['background']['D1']}. New D1 events against B: {s['new_background']}. Rule (e): {s['rule_e_excess']:.3f}.",
            '',f"TOI-1338 b: B {s['T109']['B']['total']}/13; D1 {s['T109']['D1']['total']}/13, same T109 context and missing-data outcomes.",
            '', '## Per-bin, per-duration and per-crossing results','',
            'The companion `031-tables.md` contains counts and rates. Duration means the median observed crossing duration per planet; T156 has one duration. Bands are half-open. P within a band uses its populated period bins; absent bins are explicit. These splits are exploratory.','',
            '## Verification and limitations','',
            'CONFIRMED: both original draw designs reproduced exactly before reseeding. Both full endpoint tier identities and twelve adapted-scorer population checks passed. Synthetic tests cover duration-score arrays, normalized candidate ordering, selected step curves and mirror thresholds. Deliberate wrong-order, wrong-curve, wrong-threshold and one-point mutations are detected. The final saved point estimates were recounted directly by bin. Source hashes remained equal; equality proves byte identity, not semantic correctness. These are producer checks, not independent review.',
            '', 'Full endpoint tier identities reused complete stored pre-tier events. The detector endpoint dispatch was exercised on synthetic flux. This is not a fresh raw-light replay of every historical endpoint trial.',
            '', 'Evidence: `data/astra/031/draw-checks.json`, `detector-checks.json`, `identity-checks.json`, `adapted-scorer-identity.json`, `retier-checks.json`, `known.json`, `summary.json`, `verification.json`, per-worker checkpoints and logs.',
            '', '## What I did NOT check','',
            'No fenced-star search, witness-star meter, sky search, frozen release, download, book edit or publication. No independent reviewer has assessed this implementation. The bench does not establish sensitivity across the whole sky.',
            '', '## STOP SIGNS hit','',
            ('The failed scientific rules stand as filed. No scientific setting changed.' if failed else 'No mandatory identity stop or scientific failure.'),
            '', '## QUEUE PROPOSALS','', 'None. Claude decides any adoption after independent recount.',
            '', '## IDEAS','', 'None outside the brief.',
            '', '## Disagreements with Claude','', 'None. The actual grid includes 20 hours. The all-N1 endpoint uses a cut above 20 hours; the D1 cut stays at 8.',
            '', '## Questions for Ahmed','', 'None.',
            '', '## Usage','', 'Prediction: 60 five-hour / 10 weekly points. Initial meter 1% / 0%. Final model-session usage is in `research/astra/USAGE.md`; background compute does not measure model usage.',
            '', 'Next: Claude independently recounts and reviews this result before any adoption decision; Claude required, review cost unmeasured.']
    (ROOT/'research/astra/reports/031-report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    tables=['# 031 counts-only tables','', 'Column order for all rate vectors: B dip, B bump, N1 dip, N1 bump, D1 dip, D1 bump.','',
            'Period-bin indices: 0 = 5 to 10 d; 1 = 10 to 14; 2 = 14 to 20; 3 = 20 to 27.4; 4 = 27.4 and above.','',
            '```json',json.dumps(dict(populations=s['populations'],duration_bands=s['duration_bands'],new_detection_holds=s['new_detection_holds'],
                                    strata=s['strata'],background_strata=s['background_strata'],new_planet_detection_holds=s['new_planet_detection_holds']),indent=2),'```']
    (ROOT/'research/astra/reports/031-tables.md').write_text('\n'.join(tables)+'\n',encoding='utf-8')
    print('Completed counts-only report and tables written.')


if __name__=='__main__':
    main()
