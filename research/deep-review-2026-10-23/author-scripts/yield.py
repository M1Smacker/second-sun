"""Expected number of NEW detectable transiting CBPs in G1 (Second Sun review, 2026-10-23).
Inputs: Martin 2017 Table 2 (T_prec, % time transitable on primary, E extra planets),
Davies et al. 2026 Table 2 (mean depth, duration range), planet periods (memory, standard values).
"""
import numpy as np, pandas as pd
rng=np.random.default_rng(42)
c=[3.29685004771,0.850021465753,-0.285041632435,0.0395908321369,-0.0022308015894,4.73508403525e-5]
sig1h=lambda T: np.exp(sum(ci*T**i for i,ci in enumerate(c)))
#            Tprec  f_prim  E     depth%  dur_d(lo,hi)  Pp(d)
sys={'K16':(41.4,.425,0.9,1.80,(.31,.43),228.8),'K34':(69.3,.169,3.4,0.28,(.16,.47),288.8),
     'K35':(19.8,.360,0.8,0.40,(.18,.49),131.4),'K47c':(539.1,.197,3.9,0.17,(.18,.47),303.2),
     'K64':(35.4,.284,1.5,0.11,(.45,.51),138.5),'K413':(11.1,.235,0.7,0.17,(.12,.39),66.3),
     'K453':(102.9,.105,6.0,0.50,(.29,.57),240.5),'K1647':(7188.7,.070,13.2,0.22,(.2,.37),1107.6)}
g=pd.read_csv('/home/claude/second-sun/targets/g1_coverage.csv',comment='#')
tm=pd.read_csv('/home/claude/second-sun/targets/g1_targets.csv',comment='#').drop_duplicates('tic')
g=g.merge(tm[['tic','tmag']],on='tic')
# sector mid-dates (decimal yr) from HEASARC sector table (start/end)
sect={14:(2019.545,2019.619),15:(2019.622,2019.693),16:(2019.697,2019.764),19:(2019.909,2019.977),26:(2020.437,2020.505),
40:(2021.477,2021.557),41:(2021.557,2021.633),53:(2022.447,2022.518),54:(2022.518,2022.592),55:(2022.592,2022.666),
56:(2022.666,2022.748),60:(2022.975,2023.047),73:(2023.934,2024.008),74:(2024.008,2024.082),75:(2024.082,2024.156),
76:(2024.156,2024.235),78:(2024.311,2024.386),80:(2024.462,2024.536),81:(2024.536,2024.608),82:(2024.608,2024.679),
83:(2024.679,2024.751),86:(2024.89,2024.964)}
KEP=(2009.37,2013.36); TESS=(2019.54,2024.97)
def run(beta=1.4, rscale=1.3, ptrans=0.7, snr=7.0, nmc=4000, frac_g1=0.433):
    tot=0; rows=[]
    for k,(Tp,f,E,dep,dur,Pp) in sys.items():
        w=f*Tp/2  # two transitable windows per precession cycle
        hits=0; n=0
        for _ in range(nmc):
            ph=rng.uniform(0,Tp); starts=np.array([ph,ph+Tp/2]); starts=np.r_[starts-Tp,starts,starts+Tp]+1990
            win=[(s,s+w) for s in starts]
            ov=lambda a,b: any(s<b and e>a for s,e in win)
            if ov(*KEP): continue      # would have been seen by Kepler: not 'hidden'
            n+=1
            if not ov(*TESS): continue
            star=g.sample(1,random_state=int(rng.integers(1e9))).iloc[0]
            secs=[int(float(x)) for x in str(star.qlp_sectors).split()] if isinstance(star.qlp_sectors,str) else []
            t0=rng.uniform(0,Pp/365.25)
            conj=np.arange(TESS[0]-1+t0,TESS[1]+1,Pp/365.25)
            seen=0
            D=rng.uniform(*dur)*24*rscale
            d=dep/100/rscale**2
            s=d*1e6/(beta*sig1h(star.tmag)/np.sqrt(D))
            for tc in conj:
                if not any(s0<=tc<=e0 and s0<e for s0,e0 in [sect[q] for q in secs if q in sect] for s,e in win if s<=tc<=e): continue
                if rng.random()<ptrans and s>=snr: seen+=1
            hits+= seen>0
        p=hits/max(n,1); exp=E*frac_g1*p; tot+=exp
        rows.append((k,E,round(p,4),round(exp,3)))
    return tot,rows
for args in [dict(beta=1.0,rscale=1.0),dict(beta=1.4,rscale=1.0),dict(beta=1.4,rscale=1.3),dict(beta=1.0,rscale=1.3,snr=6.0)]:
    tot,rows=run(**args); print(args,'TOTAL expected =',round(tot,3)); [print('  ',r) for r in rows]
