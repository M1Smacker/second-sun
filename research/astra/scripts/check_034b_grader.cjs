/* Read-only extraction of the shipped grader; no DOM, browser or localStorage. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '../../..');
const out = path.join(root, 'data/astra/034b');
fs.mkdirSync(out, {recursive:true});
console.log('ROOT=' + root + '\nOUTPUT=' + out);
const source = fs.readFileSync(path.join(root,'book/docs/assets/learn.js'),'utf8');
const start = source.indexOf('  const num = '), end = source.indexOf('  const dueKey =',start);
if(start<0 || end<0) throw Error('grader extraction boundary missing');
const context = {};
vm.createContext(context);
vm.runInContext(source.slice(start,end)+'\nthis.num=num; this.same=same;',context);
const specs = [
 ['u3/l4-doppler.md',[656.28*15000/299792458,'red',299792458*.0015/500,-55.5,111,13100/1048,656.28*55.5/299792458,'yes']],
 ['u4/l1-eclipsing-binaries.md',[100*1.99/4.30,100*.8*2.31/4.3,11.879,19.66/2,35.8,(6050/5983)**4,(.604-.5)*Math.PI/2]],
 ['u4/l2-how-two-stars-orbit.md',[.278/.106,.192*1.2384/(1.2384+1.2019),.278,.192*(1-.448),172*.106/.278,'secondary',.5]],
 ['u4/l4-planets-around-two-suns.md',[2*Math.PI*.901*149.6e6/(200*86400),2*1.312*696000/(.27*86400),4.9/19.66,(.103/1.384)**2*.537*1e6,'no','single dips']]
];
let tests=[], inventory=[];
for(const [file,expected] of specs){
 const text=fs.readFileSync(path.join(root,'book/docs/learn',file),'utf8');
 const tags=[...text.matchAll(/<div class="tw-prob"[^>]*>/g)];
 if(tags.length!==expected.length) throw Error('problem count mismatch');
 tags.forEach((m,k)=>{
  const a={}; for(const v of m[0].matchAll(/data-([\w-]+)=("([^"]*)"|'([^']*)')/g)) a[v[1]]=v[3]??v[4];
  const answers=a.answer.split('|'),tol=a.tol!=null?+a.tol:a.abs!=null?0:.02,abs=+(a.abs||0),unit=a.unit;
  const hints=JSON.parse(a.hints||'{}');
  const grade=v=>answers.some(w=>context.same(v,w,tol,abs,unit));
  const test=(kind,v,want)=>tests.push({file,problem:k+1,kind,input:String(v),expected:want,actual:grade(String(v))});
  answers.forEach(v=>test('declared answer',v,true)); test('independent answer',expected[k],true);
  Object.keys(hints).forEach(v=>test('hint must be wrong',v,false));
  if(typeof expected[k]==='number'){
   const v=expected[k]; test('zero',0,false); test('factor 1000',v*1000,false); test('divide 1000',v/1000,false);
   test('wrong unit',v+' bananas',false);
   if(unit) test('explicit correct unit',v+' '+unit,true);
   test('scientific notation',v.toExponential(6),true);
   // Units are labels, not automatic conversion. Numerically valid different units should be rejected.
   test('ten percent error',v*1.1,tol>=.1);
  }
  inventory.push({file,problem:k+1,line:text.slice(0,m.index).split('\n').length,...a,tol,abs,independent:expected[k]});
 });
}
// Probe legitimate mathematical notation the parser does not implement.
const probes=[['u4/l2-how-two-stars-orbit.md',7,'1/2'],['u4/l4-planets-around-two-suns.md',3,'1/4'],['u3/l4-doppler.md',8,'Yes!']].map(([file,problem,input])=>{
 const p=inventory.find(p=>p.file===file&&p.problem===problem);
 return {file,problem,input,accepted:p.answer.split('|').some(w=>context.same(input,w,p.tol,p.abs,p.unit))};
});
const failures=tests.filter(t=>t.actual!==t.expected);
const mutated={};vm.createContext(mutated);
vm.runInContext(source.slice(start,end).replace('Math.abs(a - b) <=','Math.abs(a - b) >')+'\nthis.same=same;',mutated);
const mutationDetected=!mutated.same('12.5','12.5',.03,0,'m/s');
if(!mutationDetected)throw Error('mutation control failed');
fs.writeFileSync(path.join(out,'grader.json'),JSON.stringify({extractedLines:[source.slice(0,start).split('\n').length,source.slice(0,end).split('\n').length],inventory,tests,failures,probes,mutationDetected},null,2));
console.log(JSON.stringify({problems:inventory.length,answers:inventory.reduce((n,p)=>n+p.answer.split('|').length,0),hints:inventory.reduce((n,p)=>n+Object.keys(JSON.parse(p.hints||'{}')).length,0),tests:tests.length,failures,probes,mutationDetected},null,2));
