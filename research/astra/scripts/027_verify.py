"""Verify complete replay coverage and independently recount reported outcomes."""
from collections import defaultdict
import hashlib
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).parent))
D=importlib.import_module('027_inputs')
H=D.H


def main():
    guard=H.Guard()
    provenance=guard.start()
    summary=json.loads((H.OUT/'summary.json').read_text(encoding='utf-8'))
    counts=defaultdict(int)
    for campaign in ('g2','g3'):
        original=H.DATA/f'stage3_{campaign}'/f'r1dev_{campaign}_seen_{H.DEVELOPMENT_HASH}'
        expected=defaultdict(set)
        for kind in D.KINDS:
            for p in (original/kind).glob('*.json'):
                star,sec=map(int,p.stem.split('_'))
                if str(star) in guard.seen[campaign]:
                    expected[star,sec].add(kind)
        folder=H.OUT/f'generated-{campaign}'
        assert {tuple(k) for k in json.loads((folder/'counts.json').read_text(encoding='utf-8'))['affected']}==set(expected)
        for (star,sec),kinds in expected.items():
            for kind in kinds:
                p=folder/'background'/kind/f'{star}_{sec}.json'
                group=json.loads(p.read_text(encoding='utf-8'))
                assert (group['tic'],group['sector'])==(star,sec)
                assert not any(str(m.get('status')).startswith('ERROR') for m in group['meta'])
                counts['background_groups']+=1
        records={'T156':[r for r,_ in D.t156_rows(guard,campaign)],'planets':[]}
        for p in (H.DATA/'astra/006').glob(f'planet-*-*-*-{campaign}/results.jsonl'):
            records['planets'] += [r for line in D.read(guard,p,'006').splitlines() if (r:=json.loads(line))['observed']]
        for bench,rows in records.items():
            for r in rows:
                assert str(r['star']) in guard.seen[campaign]
                sectors=[r['sector']] if bench=='T156' else r['changed']
                for sec in sectors:
                    for sign in (1,-1):
                        for kind in expected[r['star'],sec]:
                            p=folder/bench/f'trial-{r["trial"]}'/str(sign)/kind/f'{r["star"]}_{sec}.json'
                            group=json.loads(p.read_text(encoding='utf-8'))
                            assert (group['tic'],group['sector'])==(r['star'],sec)
                            assert not any(str(m.get('status')).startswith('ERROR') for m in group['meta'])
                            counts[bench+'_injection_groups']+=1
        for p in folder.glob('progress-*.json'):
            assert json.loads(p.read_text(encoding='utf-8'))['status']=='complete'
            counts['completed_workers']+=1
    for bench,key in (('planets','fixed1098'),('T156','T156all')):
        rows=json.loads((H.OUT/f'combined-{bench}.json').read_text(encoding='utf-8'))
        for i in range(4):
            for arm,name in enumerate(('real','flip')):
                rates=[]
                for b in range(5):
                    chosen=[r for r in rows if r['bin']==b]
                    count=sum(bool(r[name][i]) for r in chosen)
                    assert count==summary['metrics'][key]['counts'][b][arm][i]
                    rates.append(count/len(chosen))
                assert abs(sum(rates)/5-summary['metrics'][key]['rates'][arm][i])<1e-12
                counts['independent_rates']+=1
    checks=json.loads((H.OUT/'rule-checks.json').read_text(encoding='utf-8'))
    assert checks['passed'] and checks['cap_mutation_rejections']>0
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (H.ROOT/'research/astra/scripts').glob('027*.py')}
    result=dict(passed=True,counts=dict(counts),source_hashes=source_hashes,verified_copy_count=len(provenance),
                exclusions=['independent review','all-raw c1a-off replay','fresh seed unless separately completed'])
    (H.OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(dict(passed=True,counts=dict(counts))))


if __name__=='__main__':
    main()
