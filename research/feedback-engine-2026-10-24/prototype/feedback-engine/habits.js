const E=require('./engine.js'),S=require('./sim.js');
const deck=[]; const mix={clear:5,limit:5,hardnoise:9,quiet:2,gapdecoy:2,eclipse:2,spike:2,stepup:1,stepdown:1,gapdip:5};
let seed=31000; for(const [k,c] of Object.entries(mix)) for(let i=0;i<c;i++) deck.push(S.makeCard(k,seed++));
const r=S.rng(4); for(let i=deck.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[deck[i],deck[j]]=[deck[j],deck[i]];}
function ahmed(c,F){ if(['eclipse','flare','step'].includes(c.truth)) return 'odd'; if(c.truth==='gapdip') return 'dip';
  if(F.beta>=1.4||F.n_similar>=2) return 'odd'; return F.strength>=3.5?'dip':'nodip'; }
const st=E.newLearner(); const rows=[];
deck.forEach((c,i)=>{const F=E.measure(c.y), ans=ahmed(c,F), ctx={mode:'practice',truth:c.truth,answer:ans,cardId:c.id,kind:c.kind,state:st}; const o=E.compose(F,ctx); E.record(st,F,ctx,o); rows.push({i:i+1,kind:c.kind,ans,right:E.TRUTH_ANS[c.truth]===ans,lead:o.lead,pattern:o.pattern,words:o.words,lines:o.lines});});
for(const x of rows) console.log(`${x.i}. ${x.kind}/${x.ans} ${x.right?'RIGHT':'WRONG'} [${x.words}w] ${x.pattern?'PATTERN ':''}lead=${x.lead}\n   ${x.lines.join('\n   ')}`);
console.log('accuracy',rows.filter(x=>x.right).length,'/',rows.length,' patterns shown',rows.filter(x=>x.pattern).length, ' mastered:',Object.keys(st.mastered));
require('fs').writeFileSync('habits.json',JSON.stringify(rows,null,1));
