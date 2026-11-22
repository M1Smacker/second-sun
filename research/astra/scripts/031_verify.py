"""Independent saved-outcome checks, source invariance and terminal coverage."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/031'
PHASES=('choosing','fresh_old','T156_old','fresh_new','T156_new')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def rate(rows):
    return sum(sum(r['real'][0] for r in rows if r['bin']==b)/sum(r['bin']==b for r in rows) for b in range(5))/5


def validate_points(summary):
    for phase in PHASES:
        rows={v:[r for c in ('g2','g3') for r in read(OUT/'scored'/f'{phase}-{c}-{v}.json')['rows']] for v in ('B','N1','D1')}
        actual=summary['populations'][phase+'_all']['rates']
        for index,v in enumerate(('B','N1','D1')):
            assert abs(rate(rows[v])-actual[2*index])<1e-14, 'Saved point estimate differs from direct five-bin count'


def main(old_only=False):
    checks=[]
    for phase in ('choosing','fresh_old','T156_old'):
        for campaign in ('g2','g3'):
            for version in ('B','N1'):
                current=read(OUT/'scored'/f'{phase}-{campaign}-{version}.json')
                if version=='B' and phase=='fresh_old':
                    historical=read(OUT.with_name('fable-f4')/f'x1-planets-{campaign}-V0.json')
                    column=historical['configs'].index('B')
                else:
                    bench='T156' if phase=='T156_old' else 'planets'
                    name=(f'baseline-{bench}-{campaign}-V0.json' if version=='B' else
                          f'{bench}-{campaign}-V0{"-fresh" if phase=="fresh_old" else ""}-floor6.5.json')
                    historical=read(OUT.with_name('030')/name)
                    column=0
                indexed={r['trial']:r for r in historical['rows']}
                assert indexed.keys()=={r['trial'] for r in current['rows']}
                for row in current['rows']:
                    previous=indexed[row['trial']]
                    assert row['star']==previous['star'] and row['bin']==previous['bin']
                    assert all(row[arm][0]==previous[arm][column] for arm in ('real','flip')), 'Adapted scorer old-row identity failed'
                checks.append(dict(phase=phase,campaign=campaign,version=version,n=len(indexed)))
    result=dict(status='passed',old_population_checks=checks,scope='producer verification, not independent review')
    if old_only:
        (OUT/'adapted-scorer-identity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print('Twelve historical adapted-scorer checks passed.')
        return
    summary=read(OUT/'summary.json')
    validate_points(summary)
    mutant=copy.deepcopy(summary)
    mutant['populations']['fresh_new_all']['rates'][4]+=.01
    try:
        validate_points(mutant)
    except AssertionError:
        result['point_mutation_rejected']=True
    else:
        raise AssertionError('One-point mutation was not rejected')
    frozen=read(OUT/'frozen-before.json')
    assert frozen=={name:hashlib.sha256((ROOT/'pipeline'/name).read_bytes()).hexdigest() for name in frozen}
    sources=read(OUT/'run-source-hashes.json')
    assert sources=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'research/astra/scripts').glob('031*.py')}
    workers=[]
    for version in ('B','N1','D1'):
        phases=PHASES if version=='D1' else ('fresh_new','T156_new')
        for campaign in ('g2','g3'):
            for phase in (*phases,*(('background',) if version=='D1' else ())):
                for slot in range(3):
                    state=read(OUT/f'generated-{version}-{campaign}'/f'progress-{phase}-{slot}.json')
                    assert state['status']=='complete' and state['done']==state['total']
                    workers.append(state['groups'])
    known=read(OUT/'known.json')
    assert known['B']['total']==6 and known['n_transits']==13
    assert summary['gates']['g']==(known['D1']['total']>=6)
    assert summary['qualifies']==all(summary['gates'].values())
    assert read(OUT/'retier-checks.json')['status']=='passed'
    assert read(OUT/'detector-checks.json')['status']=='passed'
    result.update(frozen_hashes_checked=len(frozen),source_hashes_checked=len(sources),
                  completed_workers=len(workers),generated_groups=sum(workers),point_estimates_recounted=15)
    (OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Terminal verification:',json.dumps({k:v for k,v in result.items() if k!='old_population_checks'}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--old-only',action='store_true')
    main(p.parse_args().old_only)
