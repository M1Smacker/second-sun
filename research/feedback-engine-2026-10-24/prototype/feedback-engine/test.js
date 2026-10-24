const E=require('./engine.js'),S=require('./sim.js'); let fail=0; const ok=(c,m)=>{if(!c){fail++;console.log('FAIL',m);}};
const kinds=S.KINDS, ALLOWED=new Set(['7','2','70','12']);
const numsIn=(s)=>(s.match(/\d+(?:,\d{3})*(?:\.\d+)?/g)||[]);
let all=[], n=0;
for(const k of kinds) for(let i=0;i<40;i++){
  const c=S.makeCard(k,5000+kinds.indexOf(k)*100+i), F=E.measure(c.y);
  for(const ans of ['dip','nodip','odd','unsure']) for(const mode of ['practice','real']){
    const ctx={mode,truth:c.truth,answer:ans,cardId:c.id,state:E.newLearner()};
    const a=E.compose(F,ctx), b=E.compose(E.measure(c.y),{...ctx,state:E.newLearner()});
    ok(JSON.stringify(a.lines)===JSON.stringify(b.lines),'determinism '+c.id);
    const txt=a.lines.join(' '), disp=new Set(Object.values(a.display).flatMap(v=>numsIn(String(v))));
    for(const x of numsIn(txt)) if(!a.pattern) ok(disp.has(x)||ALLOWED.has(x),`number ${x} not computed in ${c.id}: ${txt}`);
    ok(!/[–—]/.test(txt) && !/[A-Za-z]-[A-Za-z]/.test(txt),'dash '+txt);
    ok(a.words>=36&&a.words<=44,`length ${a.words} ${c.id} ${mode}/${ans}: ${txt}`);
    if(mode==='real') ok(!/(it was|was right|missed|definitely|certainly|this is a planet|hidden planet)/i.test(txt),'real-mode verdict leak: '+txt);
    all.push(a.words); n++;
  }
}
console.log('compositions',n,'failures',fail,'words min/max',Math.min(...all),Math.max(...all));
// variety on 60 hard noise cards in one session
const st=E.newLearner(); const leads=[], l1=new Set(); let maxRun=1,run=1;
for(let i=0;i<60;i++){ const c=S.makeCard('hardnoise',9000+i),F=E.measure(c.y); const ctx={mode:'practice',truth:'noise',answer:i%3?'dip':'nodip',cardId:c.id,kind:'hardnoise',state:st}; const o=E.compose(F,ctx); E.record(st,F,ctx,o); if(leads.length&&leads[leads.length-1]===o.lead){run++;maxRun=Math.max(maxRun,run);}else run=1; leads.push(o.lead); l1.add(o.lines[0]); }
const cnt={}; leads.forEach(x=>cnt[x]=(cnt[x]||0)+1); console.log('hard-noise session: distinct leads',Object.keys(cnt).length,cnt,'distinct first lines',l1.size,'of 60; longest run of same lead',maxRun);

// habit simulation must also respect length and number rules
const H=require('child_process').execSync('node habits.js').toString(); const rows=JSON.parse(require('fs').readFileSync('habits.json'));
for(const r of rows) ok(r.words>=36&&r.words<=44,'habit length '+r.words+' '+r.lines.join(' '));
console.log('habit round failures so far',fail);
