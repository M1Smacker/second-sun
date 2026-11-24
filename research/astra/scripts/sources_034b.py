"""Fetch only public sources for this brief, cache under its authorized data folder."""
from pathlib import Path
import json
import urllib.request
import subprocess
import shutil

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'data/astra/034b/sources'
OUT.mkdir(parents=True,exist_ok=True)
print('ROOT='+str(ROOT)+'\nOUTPUT='+str(OUT))
sources={
 'doyle2011.pdf':'https://arxiv.org/pdf/1109.3432',
}
records=[]
for name,url in sources.items():
    path=OUT/name
    if not path.exists():
        with urllib.request.urlopen(url,timeout=35) as response:
            payload=response.read()
        assert payload.startswith(b'%PDF'), 'Response is not a PDF'
        path.write_bytes(payload)
    reader=shutil.which('pdftotext')
    if not reader:raise RuntimeError('No installed PDF text reader')
    textpath=OUT/(name+'.txt')
    subprocess.run([reader,'-enc','UTF-8','-layout',str(path),str(textpath)],check=True)
    pages=textpath.read_text(encoding='utf-8').rstrip('\f\n\r').split('\f')
    records.append({'file':name,'url':url,'bytes':path.stat().st_size,'pages':len(pages)})
    print(name, 'bytes',path.stat().st_size,'pages',len(pages))
    terms=['precess','2018','2042','one half','other half','1995','provence']
    for j,page in enumerate(pages):
        for term in terms:
            index=page.lower().find(term)
            if index>=0:print('page',j+1,'term',term,page[max(0,index-160):index+300].replace('\n',' '))
(OUT/'downloads.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
