"""Terminal coverage, identity, source and independent arithmetic verification."""
import ast
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
D=importlib.import_module('028_inputs'); H=D.H


def main():
    guard=H.Guard(); provenance=guard.start()
    summary=json.loads((H.OUT/'summary.json').read_text(encoding='utf-8'))
    counts=Counter()
    for campaign in ('g2','g3'):
        source=H.DATA/f'stage3_{campaign}'/f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        expected={}
        for kind in D.KINDS:
            for p in (source/kind).glob('*.json'):
                star,sec=map(int,p.stem.split('_'))
                if str(star) in guard.seen[campaign]: expected.setdefault((star,sec),set()).add(kind)
        generated=H.OUT/f'generated-{campaign}'
        assert set(expected)=={tuple(k) for k in json.loads((generated/'counts.json').read_text(encoding='utf-8'))['affected']}
        for (star,sec),kinds in expected.items():
            for kind in kinds:
                p=generated/'background'/kind/f'{star}_{sec}.json'
                g=json.loads(p.read_text(encoding='utf-8')); assert (g['tic'],g['sector'])==(star,sec)
                assert not any(str(m.get('status')).startswith('ERROR') for m in g['meta'])
                counts['background_groups']+=1
        for bench in ('planets','T156'):
            doc=json.loads((H.OUT/f'{bench}-{campaign}.json').read_text(encoding='utf-8'))
            old=json.loads(D.read(guard,H.OUT.with_name('027')/f'baseline-{bench}-{campaign}-V0.json','027'))
            old={r['trial']:r for r in old['rows']}
            assert {r['trial'] for r in doc['rows']}==set(old)
            for r in doc['rows']:
                assert str(r['star']) in guard.seen[campaign]
                for arm in ('real','flip'):
                    assert r[arm][:2]==[old[r['trial']][arm][0],old[r['trial']][arm][3]]
                    assert all(not r[arm][base] or r[arm][i] for i,base in ((2,0),(3,0),(4,1),(5,1)))
                counts['baseline_trial_identity']+=1
        for p in generated.glob('progress-*.json'):
            assert json.loads(p.read_text(encoding='utf-8'))['status']=='complete'; counts['completed_workers']+=1
    for bench,key in (('planets','fixed1098'),('T156','T156all')):
        rows=json.loads((H.OUT/f'combined-{bench}.json').read_text(encoding='utf-8'))
        for arm,name in enumerate(('real','flip')):
            for i in range(6):
                vals=[]
                for b in range(5):
                    chosen=[r for r in rows if r['bin']==b]
                    n=sum(r[name][i] for r in chosen)
                    assert n==summary['metrics'][key]['counts'][b][arm][i]
                    vals.append(n/len(chosen))
                assert abs(sum(vals)/5-summary['metrics'][key]['rates'][arm][i])<1e-12
                counts['independent_rates']+=1
    assert json.loads((H.OUT/'checks.json').read_text(encoding='utf-8'))['passed']
    fingerprints={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('028*.py')}
    for p in Path(__file__).parent.glob('028*.py'): ast.parse(p.read_text(encoding='utf-8')); counts['static_parse']+=1
    result=dict(passed=True,counts=dict(counts),fingerprints=fingerprints,copy_hashes=len(provenance),
        independent_review=False,fresh_seed_checked=False)
    (H.OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(dict(passed=True,counts=dict(counts))))


if __name__=='__main__': main()
