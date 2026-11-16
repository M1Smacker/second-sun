"""Real-host raw controls, run after the main job frees its worker slots."""
from datetime import datetime, timedelta, timezone
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
R = importlib.import_module('026_run')


def main():
    start = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='running', started=start.isoformat(), expected_finish=(start + timedelta(hours=1)).isoformat())
    def save():
        (R.OUT / 'progress-controls.json').write_text(json.dumps(progress), encoding='utf-8')
    save()
    try:
        R.run('026_control_prepare.py')
        R.run('026_control_generate.py')
        for mode in ('V2', 'V4'):
            R.run('026_control_score.py', ('g2', 'controls', mode))
        two = json.loads((R.OUT / 'controls-g2-V2.json').read_text(encoding='utf-8'))
        four = json.loads((R.OUT / 'controls-g2-V4.json').read_text(encoding='utf-8'))
        assert [r['trial'] for r in two['rows']] == [r['trial'] for r in four['rows']]
        summary = {}
        for case in ('eclipse2', 'eclipse5', 'planet2', 'planet3_regular', 'planet3_irregular'):
            pairs = [(a, b) for a, b in zip(two['rows'], four['rows']) if a['case'] == case]
            row = dict(n=len(pairs))
            for arm in ('real', 'flip'):
                row[arm] = dict(m2=sum(a[arm][0] for a, _ in pairs), m4=sum(b[arm][0] for _, b in pairs),
                                losses=sum(a[arm][0] and not b[arm][0] for a, b in pairs),
                                timing_held=sum(bool(b[arm + '_hold']) for _, b in pairs))
            summary[case] = row
        b_pass = all(summary[case]['n'] == 3 and summary[case][arm]['m2'] >= 1 and
                     summary[case][arm]['m4'] == 0 and summary[case][arm]['timing_held'] == 3
                     for case in ('eclipse2', 'eclipse5') for arm in ('real', 'flip'))
        c_pass = all(sum(summary[case]['n'] for case in ('planet2', 'planet3_regular')) == 6 and
                     sum(summary[case][arm]['losses'] for case in ('planet2', 'planet3_regular')) <= .005 * 6
                     for arm in ('real', 'flip'))
        result = dict(cases=summary, b_pass=b_pass, c_pass=c_pass,
                      definition='Three hosts, equal weight; c uses two crossings and a regular triple, irregular triple separately reported')
        (R.OUT / 'real-controls-summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        progress['status'] = 'complete'
        print(json.dumps(result, indent=2))
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    main()
