// Compass check: run the Claude AI feedback engine (scratch copy) on OUR real card generator and on Ahmed's own hard-practice cards.
const fs = require("fs"), path = require("path");
const ROOT = require("path").join(__dirname, "..", "..", ".."), SC = require("path").join(__dirname, "..", "prototype", "feedback-engine") + "/";
const E = require(SC + "engine.js"), H = require(ROOT + "/book/docs/assets/eyes-hard.js"), core = require(ROOT + "/book/docs/assets/eyes-core.js");
const J = JSON.parse(fs.readFileSync(ROOT + "/book/docs/assets/data/toi1338-s98.json", "utf8").replace(/^\uFEFF/, "")), P = H.prepare(J);
const q = (a, p) => a.slice().sort((x, y) => x - y)[Math.floor(p * (a.length - 1))], mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
function auc(a, b) { let w = 0; for (const x of a) for (const y of b) w += x > y ? 1 : x === y ? 0.5 : 0; return w / (a.length * b.length); }
function windowScore(y) { const x = y.map((v) => (v === null ? 0 : v)), c = [0]; for (let i = 0; i < x.length; i++) c.push(c[i] + x[i]); let b = -1e9; for (const n of H.BOXES) for (let t = 0; t + n <= x.length; t++) b = Math.max(b, -(c[t + n] - c[t]) / Math.sqrt(n) / P.sigma); return b; }
const N = 150, mk = (spec, off) => Array.from({ length: N }, (_, i) => H.build(P, spec, off + i * 7919));
const decks = { hardnoise: mk({ kind: "hardnoise" }, 11), border_lo: mk({ kind: "dip", tier: "border", snr: 5.75 }, 22), border_hi: mk({ kind: "dip", tier: "border", snr: 7.5 }, 33), clear: mk({ kind: "dip", tier: "clear", snr: 13 }, 44),
  gapdip: mk({ kind: "gapdip" }, 55), spike: mk({ kind: "spike" }, 66), step: mk({ kind: "step" }, 77), eclipse: mk({ kind: "eclipse" }, 88) };
const F = {}; for (const [k, cs] of Object.entries(decks)) F[k] = cs.map((c) => E.measure(c.y));

console.log("== 1. STRENGTH: engine vs our generator (they must be the same function)");
for (const k of ["hardnoise", "border_lo", "border_hi", "clear"]) {
  const eng = F[k].map((f) => f.strength), ours = decks[k].map((c) => (c.tier === "hardnoise" ? windowScore(c.y) : c.meta.snr));
  console.log(`  ${k.padEnd(10)} engine median ${q(eng, .5).toFixed(1)} [${q(eng, .1).toFixed(1)}, ${q(eng, .9).toFixed(1)}] | ours median ${q(ours, .5).toFixed(1)} [${q(ours, .1).toFixed(1)}, ${q(ours, .9).toFixed(1)}] | median ratio engine/ours ${q(eng.map((e, i) => e / ours[i]), .5).toFixed(2)} | engine >= 7: ${(100 * eng.filter((v) => v >= 7).length / N).toFixed(0)}% vs ours ${(100 * ours.filter((v) => v >= 7).length / N).toFixed(0)}%`);
}
console.log("== 2. Can the engine's measurements tell limit planets from hard noise on OUR cards? (AUC, 0.5 = no)");
const lim = F.border_lo.concat(F.border_hi), hn = F.hardnoise;
for (const f of ["strength", "gap_ratio", "shape_dchi2", "vness", "n_similar", "depth_pts", "beta"]) console.log(`  ${f.padEnd(12)} ${auc(lim.map((x) => x[f]), hn.map((x) => x[f])).toFixed(2)}`);
console.log("== 3. Do the artifact detectors fire on OUR odd cards? (recall) and on ordinary cards (false fires)");
const fire = (arr, fn) => (100 * arr.filter(fn).length / arr.length).toFixed(0) + "%";
const others = ["hardnoise", "border_lo", "border_hi", "clear"].flatMap((k) => F[k]);
console.log(`  gap dips: pre-gap sag >= 3 fires on ${fire(F.gapdip, (f) => f.pregap_z >= 3)}; gap_touch lesson fires on ${fire(F.gapdip, (f) => E.LESSONS.find((l) => l.id === "gap_touch").when(f))}; false fires on ordinary cards (incl. decoy gaps): pregap ${fire(others, (f) => f.pregap_z >= 3)}`);
console.log(`  spikes:   rise lesson fires on ${fire(F.spike, (f) => E.LESSONS.find((l) => l.id === "rise").when(f))} (ours are 3 to 8 sigma, 2 to 5 points); false fires ${fire(others, (f) => E.LESSONS.find((l) => l.id === "rise").when(f))}`);
console.log(`  steps:    step lesson fires on ${fire(F.step, (f) => E.LESSONS.find((l) => l.id === "step").when(f))} (ours are 1.2 to 3 sigma, up or down); false fires ${fire(others, (f) => E.LESSONS.find((l) => l.id === "step").when(f))}`);
console.log(`  eclipses: deep lesson fires on ${fire(F.eclipse, (f) => f.depth_pts >= 8)}; false fires ${fire(others, (f) => f.depth_pts >= 8)}`);
console.log(`  decoy gaps are real gaps: ${fire(others, (f) => f.n_gaps > 0)} of ordinary cards have one (engine sees them)`);

console.log("== 4. Text on OUR cards: length, numbers, wording, variety (60 hard-noise cards in one session, he answers Dip on 2 of 3)");
const truthOf = { hardnoise: "noise", dip: "planet", eclipse: "eclipse", spike: "flare", step: "step", gapdip: "gapdip" }, ansOf = { dip: "dip", none: "nodip", odd: "odd", unsure: "unsure" };
const lens = [], st = E.newLearner(), leads = {}, w2 = new Set(), l1 = new Set(); let missed = 0, nTxt = 0, maxRun = 1, run = 1, prev = null;
for (let i = 0; i < 60; i++) { const c = decks.hardnoise[i], f = F.hardnoise[i], ctx = { mode: "practice", truth: "noise", answer: i % 3 ? "dip" : "nodip", cardId: "h" + i, kind: "hardnoise", state: st }; const o = E.compose(f, ctx); E.record(st, f, ctx, o);
  lens.push(o.words); leads[o.lead] = (leads[o.lead] || 0) + 1; w2.add(o.lines[1].replace(/[\d,.]+/g, "#")); l1.add(o.lines[0].replace(/[\d,.]+/g, "#")); if (/^(Dip|Odd|No dip) missed/.test(o.lines[2])) missed++; nTxt++; if (prev === o.lead) { run++; maxRun = Math.max(maxRun, run); } else run = 1; prev = o.lead; }
console.log(`  words ${Math.min(...lens)} to ${Math.max(...lens)}; leads`, JSON.stringify(leads), `| distinct line-1 wordings with numbers masked: ${l1.size}; distinct line-2 sentences with numbers masked: ${w2.size} of 60; longest run of one lead ${maxRun}; lines starting "<Answer> missed" on a false alarm: ${missed}`);
const allTxt = [];
for (const [k, cs] of Object.entries(decks)) for (let i = 0; i < 40; i++) for (const ans of ["dip", "nodip", "odd", "unsure"]) for (const mode of ["practice", "real"]) { const c = cs[i], truth = truthOf[c.kind === "dipSNR" ? "dip" : c.kind]; const o = E.compose(F[k][i], { mode, truth, answer: ans, cardId: k + i, kind: k, state: E.newLearner() }); allTxt.push({ k, ans, mode, o }); }
const bad = allTxt.filter((x) => x.o.words < 36 || x.o.words > 44).length, dash = allTxt.filter((x) => /[–—]|[A-Za-z]-[A-Za-z]/.test(x.o.lines.join(" "))).length, leak = allTxt.filter((x) => x.mode === "real" && /(it was|was right|missed|definitely|certainly|hidden planet)/i.test(x.o.lines.join(" "))).length;
console.log(`  ${allTxt.length} texts on our decks: outside 36 to 44 words ${bad}; dashes ${dash}; verdict words in real mode ${leak}`);
const anchorUse = allTxt.filter((x) => x.mode === "practice" && ["step_faint", "flare_faint", "gap_faint", "planet_faint"].includes(x.o.lead)).length, practiceN = allTxt.filter((x) => x.mode === "practice").length;
console.log(`  practice texts led by a truth-anchored lesson (chosen because of the label, not the measurement): ${anchorUse} of ${practiceN} (${(100 * anchorUse / practiceN).toFixed(0)}%)`);
const realWeakOnArtifact = allTxt.filter((x) => x.mode === "real" && ["step", "spike", "gapdip", "eclipse"].includes(x.k) && x.o.lead === "weak").length, realArt = allTxt.filter((x) => x.mode === "real" && ["step", "spike", "gapdip", "eclipse"].includes(x.k)).length;
console.log(`  REAL mode, artifact cards where the lead says "a month of pure noise often gives one dip this strong": ${realWeakOnArtifact} of ${realArt} (${(100 * realWeakOnArtifact / realArt).toFixed(0)}%)`);

console.log("\n== 5. AHMED'S OWN HARD-PRACTICE ROUNDS, rebuilt from their seeds, with the new engine playing along in order");
const rows = fs.readFileSync(ROOT + "/research/eyes-scores/rounds.jsonl", "utf8").split("\n").filter(Boolean).map(JSON.parse).filter((r) => core.isHard(r));
for (const r of rows) {
  const state = E.newLearner(); console.log("round", core.fmtDate(r.t0));
  for (const e of r.a) {
    const spec = e.kind === "dipSNR" ? { kind: "dip", tier: e.t, snr: e.m.snr } : { kind: e.kind }, card = H.build(P, spec, e.m.seed), f = E.measure(card.y);
    const truth = truthOf[e.kind === "dipSNR" ? "dip" : e.kind], ctx = { mode: "practice", truth, answer: ansOf[e.ans], cardId: "a" + e.i + r.t0, kind: e.kind, state }, o = E.compose(f, ctx); E.record(state, f, ctx, o);
    if (!e.ok && ["hardnoise", "gapdip", "step"].includes(e.kind) && e.i % 2 === 1) {
      const old = core.bannerParts(card, e.ans === "none" ? "none" : e.ans);
      console.log(`  card ${e.i + 1} ${e.kind} (our strength ${(card.meta.score || card.meta.snr || "-")}, engine ${f.strength.toFixed(1)}) he said ${e.ans}\n    OLD: ${old.what} ${old.detail.slice(0, 95)}...\n    NEW (${o.words} words, lead ${o.lead}): ${o.lines.join(" / ")}`);
    }
  }
}
