const E=require('./engine.js'),S=require('./sim.js');
const per=150, rows=[];
for(const k of S.KINDS) for(let i=0;i<per;i++){ const c=S.makeCard(k, 200000+1000*S.KINDS.indexOf(k)+i); rows.push({k,truth:c.truth,F:E.measure(c.y)}); }
const groups={planet_clear:['clear','easybox'],planet_limit:['limit'],hardnoise:['hardnoise'],quiet:['quiet','gapdecoy'],eclipse:['eclipse'],spike:['spike'],step:['stepup','stepdown'],gapdip:['gapdip'],ramp:['ramp'],variable:['variable']};
const feats=['strength','gap_ratio','n_similar','depth_pts','dur_h','n_in','vness','shape_dchi2','ingress_h','rebound_frac','asym_z','gap_dist_h','pregap_z','rise_z','stepw_z','ramp_z','wobble_acf','beta','max_point_z','depth7_ppm'];
const q=(a,p)=>{const b=a.filter(Number.isFinite).sort((x,y)=>x-y);return b.length?b[Math.min(b.length-1,Math.floor(p*b.length))]:NaN;};
const fmt=(v)=>Math.abs(v)>=100?Math.round(v):(+v.toFixed(2));
let out='| feature | '+Object.keys(groups).join(' | ')+' |\n|'+'---|'.repeat(Object.keys(groups).length+1)+'\n';
for(const f of feats){ out+='| '+f+' |'; for(const [g,ks] of Object.entries(groups)){ const v=rows.filter(r=>ks.includes(r.k)).map(r=>f==='step_stays'?+r.F[f]:r.F[f]); out+=` ${fmt(q(v,.5))} (${fmt(q(v,.1))} to ${fmt(q(v,.9))}) |`; } out+='\n'; }
function auc(a,b){let w=0,n=0;for(const x of a)for(const y of b){if(!Number.isFinite(x)||!Number.isFinite(y))continue;n++; if(x>y)w++; else if(x===y)w+=0.5;} return w/n;}
const P=rows.filter(r=>['clear','limit','easybox'].includes(r.k)).map(r=>r.F), L=rows.filter(r=>r.k==='limit').map(r=>r.F), HN=rows.filter(r=>r.k==='hardnoise').map(r=>r.F);
let a='| feature | planet vs noise | limit planet vs hard noise | planet vs eclipse | planet vs spike | planet vs step | planet vs gap dip | planet vs ramp | planet vs variable |\n|---|---|---|---|---|---|---|---|---|\n';
const T=(t)=>rows.filter(r=>r.truth===t).map(r=>r.F);
const sep=(x)=>Math.abs(x-0.5)*2; // 0 useless, 1 perfect
for(const f of feats){ const v=[auc(P.map(F=>F[f]),T('noise').map(F=>F[f])),auc(L.map(F=>F[f]),HN.map(F=>F[f])),auc(P.map(F=>F[f]),T('eclipse').map(F=>F[f])),auc(P.map(F=>F[f]),T('flare').map(F=>F[f])),auc(P.map(F=>F[f]),T('step').map(F=>F[f])),auc(P.map(F=>F[f]),T('gapdip').map(F=>F[f])),auc(P.map(F=>F[f]),T('ramp').map(F=>F[f])),auc(P.map(F=>F[f]),T('variable').map(F=>F[f]))]; a+='| '+f+' | '+v.map(x=>x.toFixed(2)).join(' | ')+' |\n'; }
// lesson accuracy: when a lesson fires, how often is the truth in its 'for' list?
let l='| lesson | fires on (% of cards of each truth) | precision: truth is in its "for" list |\n|---|---|---|\n';
for(const Ls of E.LESSONS.filter(x=>!x.anchor)){ const fired=rows.filter(r=>Ls.when(r.F)); const prec=fired.length?fired.filter(r=>Ls.for.includes(r.truth)).length/fired.length:NaN; const by={}; for(const t of ['planet','noise','eclipse','flare','step','gapdip','ramp','variable']){const R=rows.filter(r=>r.truth===t); by[t]=Math.round(100*R.filter(r=>Ls.when(r.F)).length/R.length);} l+=`| ${Ls.id} | ${Object.entries(by).map(([k,v])=>k+' '+v).join(', ')} | ${(100*prec).toFixed(0)}% |\n`; }
require('fs').writeFileSync('tables.md','### Medians (10th to 90th percentile) by card group, '+per+' simulated cards per kind\n\n'+out+'\n### AUC (0.5 = useless, 0 or 1 = perfect separation)\n\n'+a+'\n### Lesson firing and precision\n\n'+l);
console.log('done');
