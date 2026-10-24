const fs=require("fs"),ROOT=require("path").join(__dirname,"..","..",".."),SC=require("path").join(__dirname,"..","prototype","feedback-engine")+"/";
const E=require(SC+"engine.js"),H=require(ROOT + "/book/docs/assets/eyes-hard.js");
const J=JSON.parse(fs.readFileSync(ROOT + "/book/docs/assets/data/toi1338-s98.json","utf8").replace(/^\uFEFF/,"")),P=H.prepare(J),N=200;
const mk=(spec,off)=>Array.from({length:N},(_,i)=>H.build(P,spec,off+i*7919));
const decks={hardnoise:mk({kind:"hardnoise"},101),limit:mk({kind:"dip",tier:"border",snr:6.5},202).concat(mk({kind:"dip",tier:"border",snr:5.5},203).slice(0,0)),clear:mk({kind:"dip",tier:"clear",snr:13},303)};
decks.limit=mk({kind:"dip",tier:"border",snr:5.2},212).slice(0,100).concat(mk({kind:"dip",tier:"border",snr:7.6},213).slice(0,100));
const F={};for(const k in decks)F[k]=decks[k].map(c=>E.measure(c.y));
console.log("LESSON FIRING on OUR decks (% of cards): hard noise | limit planets (strength 5 to 8.5) | clear planets   [their sim, hard noise vs limit: see report]");
for(const id of ["weak","not_unique","unique","many","near_limit","few_points","shape_unclear","strong_flat","returns","lumpy","v_shape"]){
  const L=E.LESSONS.find(l=>l.id===id),pc=k=>Math.round(100*F[k].filter(f=>L.when(f)).length/F[k].length);
  console.log("  "+id.padEnd(14),String(pc("hardnoise")).padStart(3)+"% |"+String(pc("limit")).padStart(4)+"% |"+String(pc("clear")).padStart(4)+"%   argues for: "+L.for.join("/"));
}
const med=(k,f)=>{const a=F[k].map(x=>x[f]).sort((x,y)=>x-y);return a[a.length>>1].toFixed(2)};
console.log("medians hardnoise | limit | clear:", ["strength","gap_ratio","n_in","dur_h","shape_dchi2","beta"].map(f=>`${f} ${med("hardnoise",f)}|${med("limit",f)}|${med("clear",f)}`).join("  "));
