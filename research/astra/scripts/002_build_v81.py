"""Reconstruct pinned 0.8.1 sources and apply only existing harness adaptations."""
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path(r'D:\second-sun-astra')

def main():
    frozen=json.loads((ROOT/'research/stage3/SETTINGS_FROZEN_V81.json').read_text(encoding='utf-8'))
    dest=ROOT/'data/astra/002/v81'; dest.mkdir(exist_ok=True)
    provenance={}
    for name,pinned in frozen['settings']['code'].items():
        raw=subprocess.check_output(['git','show',f"{frozen['provenance']['git_commit']}:pipeline/{name}"],cwd=ROOT)
        lf=raw.replace(b'\r\n',b'\n')
        assert pinned in [hashlib.sha256(lf).hexdigest(),hashlib.sha256(lf.replace(b'\n',b'\r\n')).hexdigest()], name
        original=(ROOT/'pipeline'/name).read_text(encoding='utf-8').splitlines(keepends=True)
        copy=(ROOT/'research/astra/scripts/harness'/name).read_text(encoding='utf-8').splitlines(keepends=True)
        text=lf.decode('utf-8')
        for op,a,b,c,d in difflib.SequenceMatcher(None,original,copy,autojunk=False).get_opcodes():
            if op=='equal': continue
            before,after=''.join(original[a:b]),''.join(copy[c:d])
            assert before and before in text, (name,'adapter mismatch')
            text=text.replace(before,after)
        (dest/name).write_text(text,encoding='utf-8',newline='\n')
        provenance[name]=dict(frozen_sha256=pinned,adapted_sha256=hashlib.sha256(text.encode()).hexdigest())
    (dest/'provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    print('Verified and adapted',len(provenance),'pinned Vesper 0.8.1 modules')

if __name__=='__main__': main()
