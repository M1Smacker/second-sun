const E=require('./engine.js'),S=require('./sim.js'),fs=require('fs');
const ex=JSON.parse(fs.readFileSync('examples.json')), H=JSON.parse(fs.readFileSync('habits.json'));
let md='', n=0;
const f=(F)=>'strength '+F.strength.toFixed(1)+', next wiggle '+Math.max(0,F.second).toFixed(1)+', depth '+Math.round(F.depth_ppm)+' ppm ('+F.depth_pts.toFixed(1)+' point scatters), '+F.dur_h+' h, shape difference '+F.shape_dchi2.toFixed(1)+', lumpiness '+F.beta.toFixed(2)+', gap distance '+(F.gap_dist_h>=99?'none':F.gap_dist_h.toFixed(2)+' h')+', pre-gap sag '+F.pregap_z.toFixed(1)+', rise '+F.rise_z.toFixed(1)+', step '+F.stepw_z.toFixed(1)+(F.step_stays?' (stays)':'');
for(const e of ex){ const c=S.makeCard(e.kind, +e.card.split('-')[1]); const F=E.measure(c.y); n++;
 md+='**'+n+'. '+e.kind+', answered '+e.answer+' ('+(E.TRUTH_ANS[e.truth]===e.answer?'right':e.answer==='unsure'?'unsure':'wrong')+'), card '+e.card+'**  \n*In:* '+f(F)+'. *Lead lesson:* '+e.lead+', '+e.words+' words.  \n> '+e.lines.join('  \n> ')+'\n\n';}
const RK=['clear','limit','hardnoise','eclipse','gapdip','stepdown','spike','variable','ramp'];
for(const k of ['clear','hardnoise','eclipse','gapdip','spike','stepdown','variable','ramp']){ const i=RK.indexOf(k); const c=S.makeCard(k,4242+i),F=E.measure(c.y);const o=E.compose(F,{mode:'real',answer:'dip',cardId:c.id,state:E.newLearner()}); n++;
 md+='**'+n+'. REAL MODE, truth hidden (simulated '+k+'), card '+c.id+'**  \n*In:* '+f(F)+'. *Lead lesson:* '+o.lead+', '+o.words+' words.  \n> '+o.lines.join('  \n> ')+'\n\n';}
for(const i of [9,14,18,21,25,26,28,29,31]){ const r=H[i-1]; n++; md+='**'+n+'. Habit round, card '+r.i+' of 34: '+r.kind+', answered '+r.ans+' ('+(r.right?'right':'wrong')+')'+(r.pattern?', pattern line shown':'')+'**  \n*Lead lesson:* '+r.lead+', '+r.words+' words.  \n> '+r.lines.join('  \n> ')+'\n\n';}
fs.writeFileSync('examples.md',md); console.log(n,'examples');
