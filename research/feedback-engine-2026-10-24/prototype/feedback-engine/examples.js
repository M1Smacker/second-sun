const E=require('./engine.js'),S=require('./sim.js');
const kinds=['clear','limit','easybox','hardnoise','quiet','gapdecoy','eclipse','spike','stepup','stepdown','gapdip'];
const WRONG={clear:'nodip',limit:'nodip',easybox:'nodip',hardnoise:'dip',quiet:'dip',gapdecoy:'dip',eclipse:'dip',spike:'nodip',stepup:'nodip',stepdown:'dip',gapdip:'dip'};
const out=[];let n=0;
for(const k of kinds){ for(const mode of ['right','wrong','unsure']){
  const c=S.makeCard(k, 777+kinds.indexOf(k)*10+['right','wrong','unsure'].indexOf(mode));
  const F=E.measure(c.y); const ans= mode==='right'?E.TRUTH_ANS[c.truth]: mode==='wrong'?WRONG[k]:'unsure';
  const o=E.compose(F,{mode:'practice',truth:c.truth,answer:ans,cardId:c.id,state:E.newLearner()});
  out.push({n:++n,card:c.id,kind:k,answer:ans,truth:c.truth,inj:c.inj,sig:c.sig,feat:{strength:+F.strength.toFixed(2),second:+F.second.toFixed(2),depth_ppm:Math.round(F.depth_ppm),dur_h:F.dur_h,vness:F.vness,shape_dchi2:+F.shape_dchi2.toFixed(1),gap_dist_h:+F.gap_dist_h.toFixed(2),beta:+F.beta.toFixed(2),n_similar:F.n_similar,n_in:F.n_in,rise_z:+F.rise_z.toFixed(1),stepw_z:+F.stepw_z.toFixed(1)},lead:o.lead,support:o.support,lines:o.lines,words:o.words});
}}
require('fs').writeFileSync('examples.json',JSON.stringify(out,null,1));
for(const e of out) console.log(`#${e.n} ${e.kind}/${e.answer} [${e.words}w] lead=${e.lead}\n  ${e.lines.join('\n  ')}`);
const w=out.map(e=>e.words); console.log('words min',Math.min(...w),'max',Math.max(...w));
