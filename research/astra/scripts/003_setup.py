"""Add a 003-local copy of the verified harness, changing output paths only."""
import hashlib
import json
from pathlib import Path
ROOT=Path(r'D:\second-sun-astra')
SCRIPTS=ROOT/'research/astra/scripts'

def main():
    source=SCRIPTS/'harness'; dest=source/'sprint003'; dest.mkdir(exist_ok=True)
    provenance=json.loads((source/'provenance.json').read_text(encoding='utf-8'))
    changed=[]
    for name,row in provenance.items():
        content=(source/name).read_bytes().replace(b'\r\n',b'\n')
        assert hashlib.sha256(content).hexdigest()==row['copy_sha256_lf']
        new=content.replace(b'"002"',b'"003"')
        (dest/name).write_bytes(new)
        row['brief002_copy_sha256_lf']=row['copy_sha256_lf']
        row['copy_sha256_lf']=hashlib.sha256(new).hexdigest()
        if new!=content: changed.append(name)
    (dest/'provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    guard=(SCRIPTS/'002_harness.py').read_text(encoding='utf-8').replace('"002"','"003"').replace('data/astra/002','data/astra/003')
    guard=guard.replace('with_name("harness")','with_name("harness") / "sprint003"')
    (SCRIPTS/'003_harness.py').write_text(guard,encoding='utf-8',newline='\n')
    print('Output-path-only adapted modules:',changed)

if __name__=='__main__': main()
