"""Independent lesson checks. No imports of project code; all outputs private."""
import os
os.environ['NUMBA_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
import csv
import json
import re
from pathlib import Path
import numpy as np
from astropy.io import fits
from scipy.ndimage import median_filter
from scipy.optimize import minimize_scalar, brentq
from scipy.integrate import quad, cumulative_trapezoid, trapezoid
from astropy.timeseries import LombScargle

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/astra/034b'
LESSONS = ['u3/l4-doppler.md', 'u4/l1-eclipsing-binaries.md',
           'u4/l2-how-two-stars-orbit.md', 'u4/l4-planets-around-two-suns.md']
P = 19.658173

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2), encoding='utf-8')

def fence():
    # Derive the requested published identifier from the authorized lesson, never print it.
    text = (ROOT / 'book/docs/learn' / LESSONS[1]).read_text(encoding='utf-8')
    target = int(re.search(r'TIC\s+(\d+)', text)[1])
    with (ROOT / 'targets/r1_targets.csv').open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith('#')))
    key = next(k for k in rows[0] if k.lower() in ('tic','tic_id','ticid'))
    aset = {int(float(r[key])) for r in rows if r['list']=='g1'}
    bset = {int(float(r[key])) for r in rows if r['list'] in ('g2','g3') and int(r['design_seen'])==0}
    result={'fence_a_rows':sum(r['list']=='g1' for r in rows), 'fence_a_unique':len(aset), 'fence_b_rows':sum(r['list'] in ('g2','g3') and int(r['design_seen'])==0 for r in rows),
            'requested_in_a':target in aset, 'requested_in_b':target in bset}
    save('fence.json',result)
    print('FENCE',json.dumps(result))
    if target in aset|bset:
        raise RuntimeError('Requested known system is fenced; raw access stopped')
    return target,aset,bset

def eclipses(target):
    paths=sorted((ROOT/'data/known'/str(target)).glob('tess2021*-s004[4-7]-*_lc.fits'))
    assert len(paths)==4
    events=[]; quality=[]; all_t=[]; all_f=[]
    for path in paths:
        with fits.open(path,memmap=False) as hd:
            assert int(hd[0].header['TICID'])==target
            sector=int(hd[0].header['SECTOR']); d=hd[1].data
            ok=np.isfinite(d['TIME'])&np.isfinite(d['PDCSAP_FLUX'])&(d['QUALITY']==0)
            t=np.array(d['TIME'][ok],float); f=np.array(d['PDCSAP_FLUX'][ok],float)
        f/=np.median(f)
        all_t.append(t);all_f.append(f)
        quality.append({'sector':sector,'kept':len(t),'rejected':int(len(ok)-ok.sum())})
        # Detect individual deep intervals directly, without a supplied epoch or fold.
        low=np.where(f<.9)[0]
        groups=np.split(low,np.where(np.diff(t[low])>.1)[0]+1)
        for group in groups:
            if len(group)<20: continue
            guess=t[group[np.argmin(f[group])]]
            window=np.abs(t-guess)<.5
            x=t[window]; y=f[window]
            sm=median_filter(y,size=5,mode='nearest')
            tc=x[np.argmin(sm)]
            # Quadratic bottom fit using all points in a fixed local time window.
            mask=np.abs(x-tc)<.035
            poly=np.polynomial.polynomial.polyfit(x[mask]-tc,y[mask],2)
            centre=tc-poly[1]/(2*poly[2])
            depth=1-float(np.median(y[np.abs(x-centre)<.02]))
            peak_depth=1-(poly[0]-poly[1]**2/(4*poly[2]))
            def width(level):
                crossings=np.where(np.diff((sm<level).astype(int))!=0)[0]
                times=[float(x[j]+(level-sm[j])*(x[j+1]-x[j])/(sm[j+1]-sm[j])) for j in crossings]
                left=[v for v in times if v<centre]; right=[v for v in times if v>centre]
                return 24*(min(right)-max(left)) if left and right else None
            w=width(1-depth/2); peak_w=width(1-peak_depth/2)
            if w is None or peak_w is None:continue
            events.append({'sector':sector,'centre':float(centre),'depth':depth,'width_h':w,'peak_width_h':peak_w,
                           'primary':depth>.4})
    prim=[r for r in events if r['primary']]; sec=[r for r in events if not r['primary']]
    assert len(prim)==5 and len(sec)==4
    epoch=np.median([r['centre']-round((r['centre']-prim[0]['centre'])/P)*P for r in prim])
    separations=[(r['centre']-epoch)%P for r in sec]
    summary={'files':len(paths),'quality':quality,'primary_count':len(prim),'secondary_count':len(sec),
             'primary_depth_percent':100*np.median([r['depth'] for r in prim]),
             'secondary_depth_percent':100*np.median([r['depth'] for r in sec]),
             'separation_d':np.median(separations),'separation_range_d':[min(separations),max(separations)],
             'primary_width_h':np.median([r['width_h'] for r in prim]),'secondary_width_h':np.median([r['width_h'] for r in sec]),
             'primary_peak_width_h':np.median([r['peak_width_h'] for r in prim]),'secondary_peak_width_h':np.median([r['peak_width_h'] for r in sec]),
             'primary_width_range_h':[min(r['width_h'] for r in prim),max(r['width_h'] for r in prim)],
             'secondary_width_range_h':[min(r['width_h'] for r in sec),max(r['width_h'] for r in sec)]}
    # Diagnostic replay of the producer's width definition, separate from independent event fits.
    t=np.concatenate(all_t);f=np.concatenate(all_f)
    bins=np.floor((t-t[0])/(30/1440)).astype(int)
    n=np.bincount(bins);valid=n>=3
    tb=np.bincount(bins,weights=t)[valid]/n[valid]
    fb=np.bincount(bins,weights=f)[valid]/n[valid]
    origin=tb[np.argmin(fb)];phase=(t-origin+1)%P-1
    replay=[]
    for c in (0,11.879):
        m=np.abs(phase-c)<1;order=np.argsort(phase[m]);x=phase[m][order];y=f[m][order]
        sm=np.convolve(y,np.ones(15)/15,mode='same')[7:-7];x=x[7:-7]
        below=x[sm<1-(1-sm.min())/2]
        replay.append(float(24*(below.max()-below.min())))
    summary['producer_width_definition_replay_h']=replay
    save('eclipses.json',{'summary':summary,'events':events})
    print('ECLIPSES',json.dumps(summary))

def geometry():
    e=.4479; a=((1.2384+1.2019)*(P/365.25)**2)**(1/3)
    inc=np.deg2rad(89.4182)
    measured=json.loads((OUT/'eclipses.json').read_text(encoding='utf-8'))['summary']['separation_d']/P
    def dt(f): return (1-e*e)**1.5/(2*np.pi*(1+e*np.cos(f))**2)
    def centres(w,i):
        def sky2(f):
            r=(1-e*e)/(1+e*np.cos(f))
            return r*r*(np.cos(w+f)**2+np.cos(i)**2*np.sin(w+f)**2)
        return [minimize_scalar(sky2,bounds=(c-w-.3,c-w+.3),method='bounded',options={'xatol':1e-13}).x for c in (np.pi/2,3*np.pi/2)]
    def separation(w,i):
        f1,f2=centres(w,i)
        return quad(dt,f1,f2,epsabs=1e-12)[0]
    w=brentq(lambda w:separation(w,np.pi/2)-measured,0,1.5)
    wi=brentq(lambda w:separation(w,inc)-measured,0,1.5)
    # Uniform circular-disc overlap, an explicit diagnostic model, not a photodynamical fit.
    r1=1.384; r2=1.312; au_solar=149597870.7/695700
    def overlap(d):
        if d>=r1+r2:return 0.
        if d<=abs(r1-r2):return np.pi*min(r1,r2)**2
        return r1*r1*np.arccos((d*d+r1*r1-r2*r2)/(2*d*r1))+r2*r2*np.arccos((d*d+r2*r2-r1*r1)/(2*d*r2))-.5*np.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2))
    def model(w,i):
        ff=centres(w,i); widths=[]; depths=[]; impact=[]
        def distance(f):return a*au_solar*(1-e*e)/(1+e*np.cos(f))*np.sqrt(np.cos(w+f)**2+np.cos(i)**2*np.sin(w+f)**2)
        for j,f in enumerate(ff):
            d=distance(f); peak=overlap(d); impact.append(d/(r1+r2))
            depths.append(peak/(np.pi*(r1 if j==0 else r2)**2)*([2.31,1.99][j]/4.30))
            l=brentq(lambda f:overlap(distance(f))-peak/2,f-.4,f)
            r=brentq(lambda f:overlap(distance(f))-peak/2,f,f+.4)
            widths.append(24*P*quad(dt,l,r)[0])
        return {'half_width_h':widths,'ratio':widths[1]/widths[0],'depth_percent':[100*x for x in depths], 'impact_over_sum_radii':impact}
    result={'omega_edge_deg':np.rad2deg(w),'omega_inclination_deg':np.rad2deg(wi),
            'edge_ecosw':e*np.cos(w),'inclined_ecosw':e*np.cos(wi),
            'inclination_shift_seconds':(separation(w,inc)-separation(w,np.pi/2))*P*86400,
            'first_order_inclination_multiplier':1+.5/np.tan(inc)**2,
            'positive_branch':model(w,inc),'negative_branch':model(-w,inc),
            'grazing_sign_counterexample':model(w,np.deg2rad(87.35)),
            'separation_at_eclipses_au':[a*(1-e*e)/(1+e*np.cos(f)) for f in centres(w,inc)],
            'point_planet_max_kms':[2*r*696000/(d*86400) for r,d in [(r1,.4),(r2,.27)]],
            'finite_planet_total_contact_max_kms':[2*(r+.103)*696000/(d*86400) for r,d in [(r1,.4),(r2,.27)]]}
    # Validate the plot against areal-law quadrature instead of its Kepler-equation solver.
    doc=json.loads((ROOT/'book/docs/assets/data/lessons/u4-separation.json').read_text(encoding='utf-8'))
    wplot=np.arccos(.149/e); f0=np.pi/2-wplot
    grid=np.linspace(f0-2*np.pi,f0+4*np.pi,200001)
    time=cumulative_trapezoid(dt(grid),grid,initial=0)*P
    time-=np.interp(f0,grid,time)
    radius=a*(1-e*e)/(1+e*np.cos(grid))
    result['separation_plot_max_error_au']=float(np.max(np.abs(np.interp(doc['t'],time,radius)-doc['f'])))
    assert result['separation_plot_max_error_au']<.0001
    # An independent round-orbit control can contradict the integration/minimization.
    assert abs(quad(dt,0,2*np.pi)[0]-1)<1e-10
    assert abs(separation(np.pi/2,inc)-.5)<1e-7
    assert result['positive_branch']['ratio']>2 and result['negative_branch']['ratio']<.5
    save('geometry.json',result);print('GEOMETRY',json.dumps(result))

def radial_velocity():
    path=next((ROOT/'data/learn-sources/lick-51peg-rv').glob('*.tsv'))
    # Table rows are recognized structurally, without embedding a catalogue identifier.
    rows=[]
    for line in path.read_text(encoding='utf-8').splitlines():
        r=line.split('\t')
        if len(r)>=6 and r[0].strip().isdigit(): rows.append(r)
    arr=np.array([[float(r[k]) for k in (1,2,3,5)] for r in rows])
    t,y,err,dew=arr.T;t=t-t.min()
    groups=np.unique(dew);indicator=np.array([dew==d for d in groups],float).T
    centered=y.copy()
    for d in groups:
        m=dew==d;centered[m]-=np.average(y[m],weights=1/err[m]**2)
    def fit(period,joint=False):
        ang=2*np.pi*t/period
        design=np.column_stack([np.sin(ang),np.cos(ang),indicator if joint else np.ones(len(t))])
        data=y if joint else centered
        # Normal equations independently reproduce the producer's SVD fit on this well-conditioned small system.
        aw=design/err[:,None];yw=data/err
        coef=np.linalg.solve(aw.T@aw,aw.T@yw)
        residual=data-design@coef
        return float(np.sum((residual/err)**2)),coef,residual
    freq,power=LombScargle(t,centered,err).autopower(minimum_frequency=.1,maximum_frequency=1,samples_per_peak=12)
    p0=1/freq[np.argmax(power)]
    best=minimize_scalar(lambda p:fit(p)[0],bounds=(p0-.0002,p0+.0002),method='bounded',options={'xatol':1e-13}).x
    joint=minimize_scalar(lambda p:fit(p,True)[0],bounds=(p0-.0002,p0+.0002),method='bounded',options={'xatol':1e-13}).x
    result={'rows':len(t),'span_years':float(np.ptp(t)/365.25),'dewar_counts':[int(sum(dew==d)) for d in groups], 'best_period_d':best,'joint_period_d':joint}
    for name,period,j in [('published_period_demeaned',4.2307966,False),('best_demeaned',best,False),('joint_offsets',joint,True)]:
        chi,c,res=fit(period,j)
        result[name]={'K_ms':float(np.hypot(*c[:2])),'rms_ms':float(np.sqrt(np.mean(res**2))), 'weighted_rms_ms':float(np.sqrt(np.average(res**2,weights=1/err**2))), 'max_residual_ms':float(np.max(res)), 'chi2':chi}
    chi,c,res=fit(4.2307966)
    plotted=centered-c[2]
    phase=np.remainder(2*np.pi*t/4.2307966+np.arctan2(c[1],c[0])+np.pi/2,2*np.pi)*4.2307966/(2*np.pi)
    doc=json.loads((ROOT/'book/docs/assets/data/lessons/u3-51peg-rv.json').read_text(encoding='utf-8'))
    order=np.argsort(phase)
    result['plot_max_velocity_ms']=float(plotted.max())
    result['plot_x_max_difference_d']=float(np.max(np.abs(phase[order]-doc['t'])))
    result['plot_y_max_difference_ms']=float(np.max(np.abs(plotted[order]-doc['f'])))
    assert len(t)==354 and abs(best-4.2307966)<.001
    assert result['plot_x_max_difference_d']<.000051 and result['plot_y_max_difference_ms']<.0051
    save('rv.json',result);print('RV',json.dumps(result))

def caveats_and_payloads(aset,bset):
    d=json.loads((ROOT/'book/docs/assets/data/lessons/u3-tess-response.json').read_text(encoding='utf-8'))
    lam=np.array(d['t'])*1e-9; response=np.array(d['f'])
    def photons(temp):return trapezoid(response/lam**4/np.expm1(.01438776877/(lam*temp)),lam)
    surface=photons(6050)/photons(5983)
    band_share=(1.384**2*surface)/(1.384**2*surface+1.312**2)
    result={'bolometric_surface_ratio':(6050/5983)**4,'blackbody_tess_surface_ratio':surface,
            'blackbody_tess_primary_share':band_share,'lesson_primary_share':2.31/4.30,
            'transverse_doppler_equivalent_ms_at_55_5_ms':55.5**2/(2*299792458)}
    payloads=set();audit=[]
    for file in LESSONS:
        text=(ROOT/'book/docs/learn'/file).read_text(encoding='utf-8')
        payloads.update(re.findall(r'data-src="([\w-]+)"',text))
        ids={int(x) for x in re.findall(r'\b(?:TIC|KIC|Gaia\s+(?:DR\d\s+)?source_id)\s*[:=]?\s*(\d+)',text)}
        audit.append({'file':file,'explicit_target_ids':len(ids),'a_matches':len(ids&aset),'b_matches':len(ids&bset)})
    for name in sorted(payloads):
        p=ROOT/'book/docs/assets/data/lessons'/f'{name}.json'
        d=json.loads(p.read_text(encoding='utf-8'))
        ids={int(x) for x in re.findall(r'\bTIC\s+(\d+)',json.dumps(d))}
        if d.get('tic') is not None:ids.add(int(d['tic']))
        # Also scan all integer tokens to catch unlabeled target IDs.
        tokens={int(x) for x in re.findall(r'(?<![\w.])\d{6,}(?![\w.])',p.read_text(encoding='utf-8'))}
        audit.append({'file':p.name,'explicit_target_ids':len(ids),'a_matches':len((ids|tokens)&aset),'b_matches':len((ids|tokens)&bset),
                      'points':len(d['t']),'paired':len(d['t'])==len(d['f']),'finite':bool(np.isfinite(d['t']).all() and np.isfinite(d['f']).all()),
                      'sorted':bool(np.all(np.diff(d['t'])>=0))})
    result['payload_count']=len(payloads);result['audit']=audit
    assert not any(r['a_matches'] or r['b_matches'] for r in audit)
    save('caveats_payloads.json',result);print('CAVEATS_PAYLOADS',json.dumps(result))

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    print('ROOT='+str(ROOT)+'\nOUTPUT='+str(OUT))
    target,a,b=fence()
    eclipses(target)
    geometry()
    radial_velocity()
    caveats_and_payloads(a,b)
