"""Small real-light pipeline exercise. Never used to choose scientific settings."""
import ast
import importlib
import json
from pathlib import Path
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).parent))
D=importlib.import_module('028_inputs'); H=D.H


def main():
    scripts=Path(__file__).parent
    for p in scripts.glob('028*.py'): ast.parse(p.read_text(encoding='utf-8'))
    timings={}
    for c in ('g2','g3'):
        for name,args in [('028_generate.py',[c,'0','1','background','--pilot']),('028_score.py',[c,'null','--pilot'])]:
            start=time.monotonic()
            with (H.OUT/f'preflight-{c}-{name}.log').open('w',encoding='utf-8') as f:
                r=subprocess.run([r'D:\second-sun\.venv\Scripts\python.exe','-I','-B',str(scripts/name),*args],stdout=f,stderr=subprocess.STDOUT)
            if r.returncode: raise RuntimeError('Preflight failed: '+c+' '+name)
            timings[c+'-'+name]=time.monotonic()-start
    guard=H.Guard(); guard.start()
    groups=0; candidates=0; subthreshold=0
    for c in ('g2','g3'):
        source=H.DATA/f'stage3_{c}'/f'r1dev_{c}_seen_{H.DEVELOPMENT_HASH}'
        folder=H.OUT/f'pilot-generated-{c}'
        coverage=json.loads((folder/'counts.json').read_text(encoding='utf-8'))
        assert len(coverage['affected'])==2
        for star,sec in coverage['affected']:
            assert str(star) in guard.seen[c]
            for kind in D.KINDS:
                p=source/kind/f'{star}_{sec}.json'
                if not p.exists(): continue
                guard.allow_design_file(p)
                old=json.loads(p.read_text(encoding='utf-8'))
                new=json.loads((folder/'background'/kind/p.name).read_text(encoding='utf-8'))
                assert not any(str(m.get('status')).startswith('ERROR') for m in new['meta'])
                fields=('kind','product','center','dur_h','snr','depth_ppm')
                canon=lambda rows:sorted(tuple(e[k] for k in fields) for e in rows if e['snr']>=7)
                assert canon(old['events'])==canon(new['events']), 'Lower floor changed high-SNR detector candidates'
                groups+=1; candidates+=len(new['events']); subthreshold+=sum(4<=e['snr']<7 for e in new['events'])
    result=dict(passed=True,groups=groups,candidates=candidates,subthreshold=subthreshold,timings_seconds=timings,
                scope='First two design sectors of each campaign; flags may change with candidate floor; not a science sample')
    (H.OUT/'preflight.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__': main()
