const path=require('path'), fs=require('fs');
const A='D:/second-sun/book/docs/assets';
const FB=require(A+'/eyes-feedback.js'), H=require(A+'/eyes-hard.js');
const J=JSON.parse(fs.readFileSync(A+'/data/toi1338-s98.json','utf8').replace(/^\uFEFF/,'')), P=H.prepare(J);
const out={};
for (const [name,spec,ans] of [['dip',{kind:'dip',tier:'border',snr:7.5},'dip'],['quiet',{kind:'quiet'},'nodip']]) {
  try{
    const c=H.build(P,spec,12345);
    const F=FB.measure(c.y,P.sigT);
    const r=FB.compose(F,{mode:'practice',truth:FB.truthKey(c),answer:ans,cardId:name,kind:c.kind,state:FB.newLearner()});
    out[name]={lines:r.lines,words:r.words,truth:FB.truthKey(c),kind:c.kind,n:c.y.length};
    out[name].y=c.y.map(v=>v===null?null:Math.round(v));
  }catch(e){out[name]={err:String(e)}}
}
fs.writeFileSync('fb_sample.json',JSON.stringify(out));
for (const k in out) console.log(k, out[k].err||JSON.stringify({truth:out[k].truth,kind:out[k].kind,n:out[k].n,words:out[k].words}), '\n', (out[k].lines||[]).join('\n'));
