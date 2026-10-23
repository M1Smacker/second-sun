import numpy as np
c=[3.29685004771,0.850021465753,-0.285041632435,0.0395908321369,-0.0022308015894,4.73508403525e-5]
sig1h=lambda T: np.exp(sum(ci*T**i for i,ci in enumerate(c)))
RE=1/109.08
print("Single-transit floor, SNR 7: minimum planet radius (R_earth)")
print("beta  Rstar dil  dur_h | T=9   10   11   11.5  12   12.5  13   13.5")
for beta in (1.0,1.4,2.0):
  for Rs in (1.0,1.5):
    for dil in (1.0,0.5):
      for D in (6,10):
        row=[]
        for T in (9,10,11,11.5,12,12.5,13,13.5):
          dmin=7*beta*sig1h(T)*1e-6/np.sqrt(D)
          row.append(Rs*np.sqrt(dmin/dil)/RE)
        print(f"{beta:<5}{Rs:<6}{dil:<4}{D:<5} | "+" ".join(f"{r:5.1f}" for r in row))
# known planets (Davies et al. 2026 Table 2): mean depth %, duration range d
kp={'K16b':(1.80,.31,.43),'K34b':(0.28,.16,.47),'K35b':(0.40,.18,.49),'K38b':(0.05,.35,.84),'K47b':(0.08,.12,.37),
'K47c':(0.17,.18,.47),'K47d':(0.16,.10,.20),'K64b':(0.11,.45,.51),'K413b':(0.17,.12,.39),'K453b':(0.50,.29,.57),
'K1647b':(0.22,.2,.37),'K1661b':(0.21,.31,.49),'TOI1338b':(0.25,.27,.52),'TIC172900988b':(0.30,.35,.48)}
print("\nKnown planets detectable in ONE transit (SNR>=7, shortest..longest duration) at given Tmag, beta=1.4 / 1.0")
for beta in (1.4,1.0):
  for T in (9,10,11,12,13):
    n_lo=sum(dep/100/(beta*sig1h(T)*1e-6/np.sqrt(lo*24))>=7 for dep,lo,hi in kp.values())
    n_hi=sum(dep/100/(beta*sig1h(T)*1e-6/np.sqrt(hi*24))>=7 for dep,lo,hi in kp.values())
    print(f"beta {beta} Tmag {T}: {n_lo}-{n_hi} of 14")
