const E=require('./engine.js'), S=require('./sim.js');
const per=Number(process.argv[2]||120), rows=[];
let t0=Date.now();
for(const k of S.KINDS) for(let i=0;i<per;i++){ const c=S.makeCard(k, 1000*S.KINDS.indexOf(k)+i+1); const F=E.measure(c.y); rows.push({k, truth:c.truth, F}); }
console.error('measured',rows.length,'cards in',Date.now()-t0,'ms');
const feats=['strength','depth_pts','dur_h','vness','shape_dchi2','gap_ratio','n_similar','n_in','rebound_frac','rebound_z','asym_z','gap_dist_h','rise_strength','step_z','drift_z','wobble_acf','beta','max_point_z','coverage','ingress_h'];
const q=(a,p)=>{const b=a.slice().sort((x,y)=>x-y);return b[Math.min(b.length-1,Math.floor(p*b.length))];};
console.log('FEATURE MEDIANS [10%,90%] by kind');
for(const f of feats){ let s=f.padEnd(13); for(const k of S.KINDS){const v=rows.filter(r=>r.k===k).map(r=>r.F[f]).filter(Number.isFinite); s+=` ${k}:${q(v,.5).toFixed(2)}[${q(v,.1).toFixed(1)},${q(v,.9).toFixed(1)}]`;} console.log(s);}
// AUC of each feature: planet (clear+limit) vs each other truth class, and limit-planet vs hardnoise
function auc(a,b){let w=0,n=0;for(const x of a)for(const y of b){n++; if(x>y)w++; else if(x===y)w+=0.5;} return w/n;}
const cls=['noise','eclipse','flare','step','gapdip','ramp','variable'];
console.log('\nAUC planet vs class (0.5 = useless; far from 0.5 = useful), and limit vs hardnoise');
const P=rows.filter(r=>r.k==='clear'||r.k==='limit');
for(const f of feats){ let s=f.padEnd(13); for(const c of cls){ const o=rows.filter(r=>r.truth===c); s+=` ${c}:${auc(P.map(r=>r.F[f]),o.map(r=>r.F[f])).toFixed(2)}`;} s+=`  limit_vs_hardnoise:${auc(rows.filter(r=>r.k==='limit').map(r=>r.F[f]),rows.filter(r=>r.k==='hardnoise').map(r=>r.F[f])).toFixed(2)}`; console.log(s);}
// lesson firing rate by kind
console.log('\nLESSON FIRING RATE by kind (%)');
for(const L of E.LESSONS){ let s=L.id.padEnd(12); for(const k of S.KINDS){const R=rows.filter(r=>r.k===k); s+=` ${k}:${Math.round(100*R.filter(r=>L.when(r.F)).length/R.length)}`;} console.log(s);}
