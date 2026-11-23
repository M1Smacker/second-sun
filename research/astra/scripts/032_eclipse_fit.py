"""Catalogue-epoch-free eclipse discovery and independent linear timing fits."""
import numpy as np
from astropy.timeseries import BoxLeastSquares
from scipy.ndimage import median_filter
from scipy.optimize import minimize_scalar

EPS=np.finfo(float).eps


def robust_sigma(values):
    med=np.median(values)
    return max(1.4826*np.median(abs(values-med)),EPS)


def folded_distance(times,epoch,period):
    return (times-epoch+period/2)%period-period/2


def streams_for_fit(raw,plant=None,sign=0):
    step=1/48
    streams=[]
    for sec,rank,product,t,f in raw:
        f=f.copy()
        if plant:
            for center,duration in plant['observed']:
                shape=np.clip((duration/2-abs(t-center))/(.1*duration),0,1)
                f-=sign*plant['depth_ppm']*1e-6*shape
        med=np.median(f)
        if not np.isfinite(med) or med<=0:
            continue
        index=np.floor(t/step).astype(int)
        unique,inv,n=np.unique(index,return_inverse=True,return_counts=True)
        time=np.bincount(inv,weights=t)/n
        flux=np.bincount(inv,weights=f/med)/n
        grid=np.interp(np.arange(unique[0],unique[-1]+1),unique,flux)
        trend=median_filter(grid,size=241,mode='nearest')[unique-unique[0]]
        good=np.isfinite(trend)&(trend>0)
        if good.sum()>=10:
            streams.append((sec,rank,product,unique[good],time[good],flux[good]/trend[good]-1))
    return streams


def combined(streams):
    _,_,_,indices,t,f=zip(*sorted(streams,key=lambda x:(x[1],x[0],x[2])))
    index=np.concatenate(indices)
    keep=np.unique(index,return_index=True)[1]
    return np.concatenate(t)[keep],np.concatenate(f)[keep]


def support(t,f,period,epoch,width,sigma):
    dt=folded_distance(t,epoch,period)
    inside=abs(dt)<=width/2
    cycle=np.rint((t[inside]-epoch)/period).astype(int)
    counts=np.bincount(cycle-cycle.min()) if len(cycle) else np.array([])
    if np.count_nonzero(counts>=2)<3:
        return False
    return np.count_nonzero(np.bincount(cycle-cycle.min(),weights=-(f[inside]-np.median(f)))>
                            2*sigma*np.sqrt(counts))>=3


def primary(t,f,cat_p,width,secondary_phase):
    base=float(t[0])
    t=t-base
    tspan=t[-1]-t[0]
    sigma=robust_sigma(f)
    candidates=[]
    for alias in (1.,.5,2.):
        low,high=cat_p*alias*np.array([.95,1.05])
        w=min(width, .15*low)
        durations=np.array([.6*w,w])
        df=durations[0]/(4*tspan*high)
        n=max(2,int(np.ceil((1/low-1/high)/df))+1)
        periods=1/np.linspace(1/low,1/high,n)
        power=BoxLeastSquares(t,f,dy=sigma).power(periods,durations,objective='snr',method='fast')
        # Walk peaks in descending score until the band's best supported train.
        for i in np.argsort(power.power)[::-1]:
            p,e,d=float(periods[i]),float(power.transit_time[i]),float(power.duration[i])
            if power.power[i]<5:
                break
            if support(t,f,p,e,d,sigma):
                candidates.append((float(power.power[i]),p,e+base,d,alias))
                break
    if not candidates:
        return None,'no supported band'
    winner=max(candidates)
    catalogue=next((x for x in candidates if x[-1]==1),None)
    _,p,e,d,band=winner
    if band==.5:
        stats=[]
        for parity in (0,1):
            phase=folded_distance(t+base,e+parity*p,2*p)
            inside=abs(phase)<=d/2
            shoulder=(abs(phase)>=.75*d)&(abs(phase)<=1.5*d)
            if inside.sum()<5 or shoulder.sum()<5:
                stats.append(None)
                continue
            depth=np.median(f[shoulder])-np.mean(f[inside])
            uncertainty=robust_sigma(f[shoulder])*np.sqrt(1/inside.sum()+1/shoulder.sum())
            core=inside&(f<np.median(f[shoulder])-.5*depth)
            width_est=2*np.median(abs(phase[core])) if core.any() else 0
            width_error=max(1/48,d/np.sqrt(inside.sum()))
            stats.append((depth,uncertainty,width_est,width_error))
        twin=False
        if all(x is not None for x in stats):
            a,b=stats
            twin=abs(a[0]-b[0])<=3*np.hypot(a[1],b[1]) and abs(a[2]-b[2])<=3*np.hypot(a[3],b[3])
        if catalogue:
            return catalogue,'half rejected: supported catalogue train'
        prior_conflict=np.isfinite(secondary_phase) and abs(secondary_phase-.5)>.15
        if twin and not prior_conflict:
            return winner,'half accepted: compatible odd/even and no supported catalogue train'
        return None,'half rejected: odd/even or phase check inconclusive'
    if band==2:
        if support(t+base,f,p,e+p/2,d,sigma):
            return catalogue,'double rejected: supported half-phase eclipse'
        return winner,'double retained: no supported half-phase eclipse'
    return winner,'catalogue band wins'


def secondary(t,f,period,epoch,primary_width,width):
    # Circular time cumulative sums evaluate every phase without a per-point loop.
    x=(t-epoch)%period
    order=np.argsort(x)
    x=x[order]
    y=f[order]-np.median(f)
    xx=np.r_[x-period,x,x+period]
    yy=np.tile(y,3)
    csum=np.r_[0,np.cumsum(yy)]
    phases=np.linspace(0,period,max(32,int(np.ceil(8*period/width))),endpoint=False)
    l,r=np.searchsorted(xx,phases-width/2),np.searchsorted(xx,phases+width/2)
    n=r-l
    score=-(csum[r]-csum[l])/np.sqrt(n.clip(1))/robust_sigma(f)
    score[(n<5)|(abs(folded_distance(phases,0,period))<=(primary_width+width)/2)]=-np.inf
    sigma=robust_sigma(f)
    for i in np.argsort(score)[::-1]:
        if score[i]<5:
            return None
        e=epoch+phases[i]
        if support(t,f,period,e,width,sigma):
            return float(e)
    return None


def template(t,f,period,epoch,width):
    phase=folded_distance(t,epoch,period)/width
    edges=np.linspace(-1.5,1.5,13)
    med=[]
    for lo,hi in zip(edges[:-1],edges[1:]):
        hit=(phase>=lo)&(phase<hi)
        med.append(np.median(f[hit]) if hit.any() else np.nan)
    med=np.array(med)
    x=(edges[1:]+edges[:-1])/2
    finite=np.isfinite(med)
    if finite.sum()<7:
        return None
    fitted=np.interp(x,x[finite],med[finite])
    baseline=np.median(fitted[abs(x)>=.75])
    depth=baseline-fitted.min()
    if depth<=0:return None
    return x,(baseline-fitted)/depth


def measure(t,f,center,width,profile):
    i,j=np.searchsorted(t,[center-2.1*width,center+2.1*width])
    xx=(t[i:j]-center)/width
    yy=f[i:j]
    if sum(abs(xx)<=.5)<5 or sum(abs(xx)>=.85)<5:
        return None
    x,y=profile
    noise=robust_sigma(yy[abs(xx)>=.85])
    def objective(shift,full=False):
        q=np.interp(xx-shift,x,y,left=0.,right=0.)
        design=np.column_stack((np.ones(len(xx)),xx,-q))
        coeff=np.linalg.lstsq(design,yy,rcond=None)[0]
        if coeff[-1]<=0:
            return (np.inf,0) if full else np.inf
        resid=yy-design@coeff
        chi=float(resid@resid/noise**2)
        return (chi,float(coeff[-1])) if full else chi
    grid=np.linspace(-.6,.6,25)
    loss=[objective(z) for z in grid]
    k=int(np.argmin(loss))
    if k==0 or k==len(grid)-1 or not np.isfinite(loss[k]):
        return None
    fit=minimize_scalar(objective,bounds=(grid[k-1],grid[k+1]),method='bounded',
                        options={'xatol':1e-5})
    shift=fit.x
    chi,depth=objective(shift,full=True)
    h=.01
    curvature=(objective(shift-h)+objective(shift+h)-2*chi)/h**2
    snr=depth/noise*np.sqrt(np.count_nonzero(abs(xx-shift)<=.5))
    if not np.isfinite(curvature) or curvature<=0 or snr<5:
        return None
    error=max(np.sqrt(2/curvature)*width,EPS)
    return dict(time=float(center+shift*width),error=float(error),snr=float(snr),depth=float(depth))


def fit_line(events,period,epoch):
    if len(events)<3:
        return None
    n=np.array([e['cycle'] for e in events],dtype=float)
    if np.ptp(n)<2:
        return None
    t=np.array([e['time'] for e in events])
    sig=np.array([e['error'] for e in events])
    center=int(np.rint(np.average(n,weights=1/sig**2)))
    x=n-center
    a=np.column_stack((np.ones(len(x)),x))
    def fit(a):
        coeff=np.linalg.lstsq(a/sig[:,None],(t-epoch)/sig,rcond=None)[0]
        residual=t-epoch-a@coeff
        return coeff,residual,float(np.sum((residual/sig)**2))
    c,residual,chi=fit(a)
    cov=np.linalg.inv((a/sig[:,None]).T@(a/sig[:,None]))
    trend=len(events)>=5 and chi-fit(np.column_stack((a,x*x)))[2]>9
    large=np.any(abs(residual)>3*sig)
    for e,r in zip(events,residual):
        e['residual']=float(r)
    return dict(period=float(c[1]),epoch=float(c[0]+epoch),epoch_error=float(np.sqrt(cov[0,0])),
                period_error=float(np.sqrt(cov[1,1])),covariance=float(cov[0,1]),
                scatter=float(np.std(residual,ddof=2)),reduced_chi2=chi/(len(x)-2),
                trend=bool(trend),large_residual=bool(large),usable=bool(not (trend or large)),
                n=len(events),seed_period=period)


def track(t,f,streams,period,epoch,width):
    if epoch is None:return [],None
    prof=template(t,f,period,epoch,width)
    if prof is None:return [],None
    cycle_min=int(np.floor((t[0]-epoch)/period))
    cycle_max=int(np.ceil((t[-1]-epoch)/period))
    events=[]
    for cycle in range(cycle_min,cycle_max+1):
        center=epoch+cycle*period
        for sec,rank,product,_,tt,ff in streams:
            if not tt[0]-width<=center<=tt[-1]+width:
                continue
            result=measure(tt,ff,center,width,prof)
            if result:
                events.append(dict(result,cycle=cycle,sector=sec,product=product,width=width))
                break
    return events,fit_line(events,period,epoch)


def fit_star(raw,period,width,ws,secondary_phase,plant=None,sign=0):
    streams=sorted(streams_for_fit(raw,plant,sign),key=lambda x:(x[1],x[0],x[2]))
    if not streams:
        return {}
    t,f=combined(streams)
    if len(t)<100 or np.ptp(t)<period:
        return {}
    found,why=primary(t,f,period,width,secondary_phase)
    if found is None:
        return {'alias_reason':why}
    score,p,epoch,_,alias=found
    secondary_epoch=secondary(t,f,p,epoch,width,ws)
    records={'alias':alias,'alias_reason':why,'search_period':p,'search_snr':score,'primary_epoch_seed':epoch}
    for name,e,w in [('primary',epoch,width),('secondary',secondary_epoch,ws)]:
        events,fit=track(t,f,streams,p,e,w)
        records[name]=dict(events=events,fit=fit,width=w,epoch_seed=e)
    return records
