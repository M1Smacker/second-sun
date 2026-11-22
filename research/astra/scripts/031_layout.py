"""Pre-create shared folders and copy only N1's design-background checkpoint."""
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).parent))
H=importlib.import_module('031_harness')
D=importlib.import_module('031_inputs')


def main():
    guard=H.Guard()
    guard.start()
    (H.OUT/'scored').mkdir(exist_ok=True)
    for campaign in ('g2','g3'):
        assert (H.OUT/'records'/f'{campaign}-complete.json').is_file()
        for version in ('B','N1','D1'):
            root=H.OUT/f'generated-{version}-{campaign}'
            root.mkdir(exist_ok=True)
            for kind in D.KINDS:
                (root/'background'/kind).mkdir(parents=True,exist_ok=True)
            if version=='N1':
                prior=H.OUT.with_name('030')/f'generated-{campaign}'
                for kind in D.KINDS:
                    for path in (prior/'background'/kind).glob('*.json'):
                        assert path.stem.split('_')[0] in guard.seen[campaign]
                        content=D.read(guard,path,'030')
                        (root/'background'/kind/path.name).write_text(content,encoding='utf-8')
                (root/'counts.json').write_text(D.read(guard,prior/'counts.json','030'),encoding='utf-8')
            phases=('choosing','fresh_old','T156_old','fresh_new','T156_new') if version=='D1' else ('fresh_new','T156_new')
            for phase in phases:
                rows=json.loads((H.OUT/'records'/f'{phase}-{campaign}.json').read_text(encoding='utf-8'))
                for r in rows:
                    assert str(r['star']) in guard.seen[campaign]
                    if not phase.startswith('T156') and not r['observed']:
                        continue
                    for sign in ('1','-1'):
                        for kind in D.KINDS:
                            (root/phase/f'trial-{r["trial"]}'/sign/kind).mkdir(parents=True,exist_ok=True)
    print('Shared trial folders prepared before workers; N1 background copied read-only from 030.')


if __name__=='__main__':
    main()
