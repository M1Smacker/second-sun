"""Calibrate fixed product timing errors on seed-12 controls."""
import importlib,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
F=importlib.import_module('032b_eclipse_fit')
H=importlib.import_module('032b_harness')
O=importlib.import_module('032b_outputs')

def load(stage,slots):
    return [r for i in range(slots) for r in json.loads((H.OUT/f'eclipse-{stage}-{i}.json').read_text())['rows']]

def family(product):
    return product.removesuffix('-SAP')

def calibrate(rows):
    samples={}
    for r in rows:
        if r['sample']!='control':continue
        tr=r['fit'].get('primary',{})
        fit=tr.get('fit')
        if not fit or abs(fit['period']-r['catalogue']['P'])>.001:continue
        for e in tr['events']:
            samples.setdefault(family(e['product']),[]).append(abs(e['residual']/e['error']))
    return {k:float(max(.05,np.median(v)/.6744897501960817)) for k,v in samples.items() if len(v)>=20}

def apply(row,scales):
    for fit in [row['fit'],*row.get('injected',{}).values()]:
        for name in ('primary','secondary'):
            if name not in fit:continue
            tr=fit[name]
            for e in tr['events']:
                key=family(e['product'])
                e['uncalibrated_error']=e['error']
                e['error']*=scales.get(key,1)
            tr['fit']=F.fit_line(tr['events'],fit['search_period'],tr['epoch_seed']) if tr['epoch_seed'] is not None else None
    return row

def trap(rows):
    library=[r['noise'] for r in rows if r.get('noise')]
    assert library
    rng=np.random.default_rng(2026111414)
    correct=[]
    for i in range(30):
        period=rng.uniform(*[(6,9),(10,13),(14,19),(20,26),(28,40)][i%5])
        delta=.018*period
        t=np.arange(0,9*period,1/48)
        residual=library[i%len(library)]
        noise=np.resize(residual,len(t))
        offset=rng.uniform(0,period)
        depth=15*F.robust_sigma(np.asarray(residual))
        v=noise-depth*np.exp(-(F.folded_distance(t,offset,period)/delta)**2)
        v-=depth*rng.uniform(.9,1)*np.exp(-(F.folded_distance(t,offset+.5*period,period)/delta)**2)
        found,why=F.primary(t,v,period*1.005,delta*2,.5)
        correct.append(bool(found and abs(found[1]/period-1)<.01))
    return sum(correct)

if __name__=='__main__':
    guard=H.Guard()
    guard.start()
    rows=load('calibrate',int(sys.argv[1]))
    scales=calibrate(rows)
    good=trap(rows)
    O.write_json(H.OUT/'timing-calibration.json',dict(scales=scales,trap_pass=good,trap_n=30))
    print('Frozen scales',scales,'trap',good,'/ 30',flush=True)
