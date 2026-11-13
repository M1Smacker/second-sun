"""File metadata only for sealed runs, plus preregistered reference hashes."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(r'D:\second-sun-astra')

def main():
    result={}
    for campaign in ('g2','g3'):
        base=ROOT/'data'/f'stage3_{campaign}'/f'r1_{campaign}_unseen_bcd29c7aabb0'
        stats=[p.stat() for folder in ('groups','groups_sap') for p in (base/folder).glob('*.json')]
        result[campaign]=dict(files=len(stats),earliest_modified_utc=datetime.fromtimestamp(min(s.st_mtime for s in stats),timezone.utc).isoformat(),
            earliest_created_utc=datetime.fromtimestamp(min(s.st_ctime for s in stats),timezone.utc).isoformat())
    result['hashes']={name:hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in
        ('targets/r1_targets.csv','research/stage3/R1-S1-REFERENCE-COUNTS.txt','research/stage3/R1-S1-REFERENCE-BINS.txt')}
    (ROOT/'data/astra/002/timeline.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
