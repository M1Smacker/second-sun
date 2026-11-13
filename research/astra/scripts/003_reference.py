"""Read the public NASA composite parameter API; save derived planet columns only."""
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode,quote
ROOT=Path(r'D:\second-sun-astra')
def main():
    query='select pl_name,pl_trandep,pl_trandur from pscomppars where cb_flag=1 and tran_flag=1'
    url='https://exoplanetarchive.ipac.caltech.edu/TAP/sync?'+urlencode(dict(query=query,format='json'))
    with urlopen(url,timeout=60) as response: raw=response.read()
    rows=json.loads(raw)
    for r in rows:
        r['depth_ppm']=None if r['pl_trandep'] is None else r['pl_trandep']*10000
        r['archive_link']='https://exoplanetarchive.ipac.caltech.edu/overview/'+quote(r['pl_name'])
    out=ROOT/'data/astra/003'; out.mkdir(parents=True,exist_ok=True)
    (out/'published-reference.json').write_text(json.dumps(dict(query_url=url,response_bytes=len(raw),rows=rows),indent=2),encoding='utf-8')
    print('Transiting circumbinary rows:',len(rows),'with depth:',sum(r['depth_ppm'] is not None for r in rows),'with duration:',sum(r['pl_trandur'] is not None for r in rows))
if __name__=='__main__': main()
