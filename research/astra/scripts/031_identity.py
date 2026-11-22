"""Checkpointed full endpoint tier identities using complete archived pre-tier events."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\second-sun-astra')
S = ROOT/'research/astra/scripts'
OUT = ROOT/'data/astra/031'
PY = r'D:\second-sun\.venv\Scripts\python.exe'


def run(script, args):
    tag = script.removesuffix('.py') + '-' + '-'.join(args)
    marker = OUT/(tag+'.complete.json')
    if marker.exists():
        return
    with (OUT/(tag+'.log')).open('w', encoding='utf-8') as stream:
        result = subprocess.run([PY, '-I', '-B', str(S/script), *args], cwd=ROOT,
                                stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(tag+' failed; inspect private terminal log')
    marker.write_text(json.dumps(dict(status='complete')), encoding='utf-8')


def main():
    assert all(v['identity'] for v in json.loads((OUT/'draw-checks.json').read_text(encoding='utf-8')).values())
    assert json.loads((OUT/'detector-checks.json').read_text(encoding='utf-8'))['status'] == 'passed'
    now = datetime.now(timezone(timedelta(hours=3)))
    state = dict(status='running', stage='full endpoint tier identities', started=now.isoformat(),
                 expected_finish=(now+timedelta(minutes=30)).isoformat(), estimate='Unmeasured conservative identity-only estimate', workers=3)
    def save():
        (OUT/'identity-progress.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
    save()
    try:
        jobs = [('031_score.py', [c, b, 'V0', '--baseline']) for c in ('g2','g3') for b in ('planets','T156')]
        jobs += [('031_endpoint_n1.py', [c, b, 'V0', '--floor','6.5']) for c in ('g2','g3') for b in ('planets','T156')]
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(run, script, args) for script, args in jobs]
            for f in futures:
                f.result()
        comparisons = []
        counts = {}
        for version in ('B','N1'):
            for bench in ('planets','T156'):
                rows, background = [], []
                for campaign in ('g2','g3'):
                    filename = (f'baseline-{bench}-{campaign}-V0.json' if version=='B'
                                else f'{bench}-{campaign}-V0-floor6.5.json')
                    fresh = json.loads((OUT/filename).read_text(encoding='utf-8'))
                    old = json.loads((OUT.with_name('030')/filename).read_text(encoding='utf-8'))
                    keys = ('trial','star','bin','campaign','real','flip')
                    canon = lambda d: sorted(tuple(json.dumps(r[k], sort_keys=True) for k in keys) for r in d['rows'])
                    assert canon(fresh) == canon(old), 'Endpoint trial-level tier identity failed'
                    assert fresh['background'] == old['background'], 'Endpoint background identity failed'
                    rows.extend(fresh['rows'])
                    background.extend(fresh['background'])
                    comparisons.append(dict(version=version, bench=bench, campaign=campaign, rows=len(fresh['rows'])))
                if bench == 'T156':
                    rows = [r for r in rows if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
                p = 20*sum(sum(r['real'][0] for r in rows if r['bin']==b)/sum(r['bin']==b for r in rows) for b in range(5))
                assert round(p,3) == {('B','planets'):48.105, ('B','T156'):34.207,
                                      ('N1','planets'):49.942, ('N1','T156'):31.653}[version,bench]
                counts[f'{version}-{bench}'] = dict(n=len(rows), percent=p)
                if bench == 'planets':
                    alarms = [sum(e['kind']==arm and e['options'][0] for e in background) for arm in ('real','flip')]
                    assert alarms == ([174,79] if version=='B' else [165,77])
                    counts[version+'-background'] = alarms
        output = dict(status='passed', comparisons=comparisons, counts=counts,
                      scope='Full pre-tier event reuse and tier replay; raw endpoint dispatch tested on synthetic light')
        (OUT/'identity-checks.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
        state.update(status='complete', stage='endpoint identities passed')
        print(json.dumps(counts), flush=True)
    except Exception as error:
        state.update(status='failed', error=str(error))
        raise
    finally:
        state['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat()
        save()


if __name__ == '__main__':
    main()
