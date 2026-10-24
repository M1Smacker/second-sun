// Tests for the Eyes feedback text (docs/assets/eyes-feedback.js). Usage: node book/tools/test_eyes_feedback.mjs
// What must never go wrong: a text that is the wrong length or has a number that was not measured, a lead lesson that peeks at the true label, "missed" said about a false alarm,
// a strength that differs from the one on the card, a card that nearly matches an artifact being called plain noise, and sentences that repeat.
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url)), req = createRequire(import.meta.url), assets = path.join(here, "..", "docs", "assets");
const FB = req(process.env.EYES_FEEDBACK || path.join(assets, "eyes-feedback.js"));
const H = req(path.join(assets, "eyes-hard.js")), SS = req(path.join(assets, "eyes-strength.js"));
const J = JSON.parse(fs.readFileSync(path.join(assets, "data", "toi1338-s98.json"), "utf8").replace(/^﻿/, "")), P = H.prepare(J);
let passed = 0;
const test = (name, fn) => { fn(); passed++; console.log("pass:", name); };
const N = 80, mk = (spec, off) => Array.from({ length: N }, (_, i) => H.build(P, spec, off + i * 7919));
const decks = { hardnoise: mk({ kind: "hardnoise" }, 11), lo: mk({ kind: "dip", tier: "border", snr: 5.75 }, 22), hi: mk({ kind: "dip", tier: "border", snr: 7.5 }, 33), clear: mk({ kind: "dip", tier: "clear", snr: 13 }, 44),
  gapdip: mk({ kind: "gapdip" }, 55), spike: mk({ kind: "spike" }, 66), step: mk({ kind: "step" }, 77), eclipse: mk({ kind: "eclipse" }, 88) };
const facts = {}; for (const [k, cs] of Object.entries(decks)) facts[k] = cs.map((c) => FB.measure(c.y, P.sigT));
const pct = (arr, fn) => arr.filter(fn).length / arr.length;
const ANSWERS = ["dip", "nodip", "odd", "unsure"], lesson = (id) => FB.LESSONS.find((l) => l.id === id);
const textOf = (k, i, mode, answer, state) => FB.compose(facts[k][i], { mode, truth: FB.truthKey(decks[k][i]), answer, cardId: k + i, kind: decks[k][i].kind, state: state || FB.newLearner() });

// cards of the easy sittings, built the way practiceSource builds them (real windows of the sector with box fakes)
function easyCards(n, seed) {
  const rnd = H.mulberry32(seed), ri = (a, b) => a + Math.floor(rnd() * (b - a + 1)), W = 216, N0 = J.ppm.length, idx = (t) => Math.round((t - J.t0_btjd) / J.step_days), ecl = J.eclipses_btjd.map(idx), pl = idx(J.planet_btjd);
  const valid = (i) => J.ppm.slice(i, i + W).filter((v) => v !== null).length >= 0.85 * W, clear = (i) => ![...ecl, pl].some((e) => e > i - 36 && e < i + W + 36), out = [];
  while (out.length < n) {
    const kind = ["quiet", "dip", "eclipse", "spike", "step"][out.length % 5]; let i = 0;
    if (kind === "eclipse") { for (let k = 0; k < 2000; k++) { const e = ecl[ri(0, ecl.length - 1)], j = e - ri(40, W - 40); if (j >= 0 && j + W < N0 && valid(j)) { i = j; break; } } }
    else for (let k = 0; k < 4000; k++) { const j = ri(0, N0 - W - 1); if (valid(j) && clear(j)) { i = j; break; } }
    const y = J.ppm.slice(i, i + W), sub = (a, b, v) => { for (let k = a; k < b; k++) if (y[k] !== null) y[k] += v; };
    if (kind === "dip") { const d = ri(24, 48), a = ri(30, W - 30 - d); sub(a, a + d, -[1500, 2500, 4000][ri(0, 2)]); }
    if (kind === "spike") sub(ri(30, W - 30), ri(30, W - 30) + 3, 9000);
    if (kind === "step") sub(ri(60, W - 60), W, 3500);
    out.push({ y, truth: kind === "quiet" ? "none" : kind === "dip" ? "dip" : "odd", kind });
  }
  return out;
}

test("every measurement is a finite number or a plain label, the same every time, and fast", () => {
  const t0 = Date.now();
  for (const k of Object.keys(decks)) for (let i = 0; i < 10; i++) {
    const f = FB.measure(decks[k][i].y, P.sigT), g = FB.measure(decks[k][i].y, P.sigT);
    assert.deepEqual(f, g);
    for (const [name, v] of Object.entries(f)) assert.ok(typeof v !== "number" || Number.isFinite(v), `${k}${i}: ${name} = ${v}`);
  }
  assert.ok((Date.now() - t0) / 160 < 25, "a card should be measured in a few milliseconds");
});

test("one strength everywhere: the feedback's strength is the card's own strength from the hunt's function", () => {
  for (const k of ["hardnoise", "lo", "clear", "gapdip"]) for (let i = 0; i < 25; i++) {
    const f = facts[k][i], s = H.strengthOf(decks[k][i].y, P.sigT);
    assert.ok(Math.abs(f.strength - s) < 1e-9, `${k}${i}: feedback ${f.strength} vs card ${s}`);
    assert.ok(Math.abs(decks[k][i].meta.st - s) <= 0.051, `${k}${i}: the number in the card note ${decks[k][i].meta.st} vs ${s}`);
  }
});

test("every text is three lines of 36 to 44 words with no dashes, on every kind of card, every answer and both modes", () => {
  let n = 0;
  for (const k of Object.keys(decks)) for (let i = 0; i < 40; i++) for (const a of ANSWERS) for (const mode of ["practice", "real"]) {
    const o = textOf(k, i, mode, a), all = o.lines.join(" ");
    assert.equal(o.lines.length, 3); assert.ok(o.words >= 36 && o.words <= 44, `${k}${i} ${a} ${mode}: ${o.words} words: ${all}`);
    assert.equal(FB.words(all), o.words); assert.ok(!/[–—]/.test(all) && !/ - /.test(all), "dash in: " + all); n++;
  }
  assert.ok(n === 8 * 40 * 8);
});

test("only measured numbers appear: every number in a text is one the card was measured to have (or a fixed line like 7)", () => {
  const fixed = new Set(["7", "70", "2", "12", "0"]);
  for (const k of Object.keys(decks)) for (let i = 0; i < 30; i++) for (const mode of ["practice", "real"]) {
    const o = textOf(k, i, mode, "dip"), shown = new Set(Object.values(o.display).flatMap((v) => FB.numsOf(String(v))));
    for (const l of o.lines) for (const x of FB.numsOf(l)) assert.ok(shown.has(x) || fixed.has(x), `${k}${i}: "${x}" in "${l}" was not measured`);
  }
});

test("the lead lesson and the measurement line never look at the true label", () => {
  for (const k of ["hardnoise", "lo", "gapdip", "step", "clear"]) for (let i = 0; i < 25; i++) {
    const base = FB.compose(facts[k][i], { mode: "practice", truth: "planet", answer: "dip", cardId: k + i, kind: k, state: FB.newLearner() });
    for (const truth of ["planet", "noise", "eclipse", "flare", "step", "gapdip"]) {
      const o = FB.compose(facts[k][i], { mode: "practice", truth, answer: "dip", cardId: k + i, kind: k, state: FB.newLearner() });
      assert.equal(o.lead, base.lead, `${k}${i}: the lead changed with the label (${truth})`);
    }
    const real = FB.compose(facts[k][i], { mode: "real", answer: "dip", cardId: k + i, kind: k, state: FB.newLearner() });
    assert.equal(real.lead, base.lead, `${k}${i}: practice and real chose different leads`);
  }
});

test("a false alarm is never called a miss: 'You said Dip' on noise, and 'missed' appears nowhere", () => {
  for (const k of Object.keys(decks)) for (let i = 0; i < 30; i++) for (const a of ANSWERS) {
    const o = textOf(k, i, "practice", a), truth = FB.truthKey(decks[k][i]);
    assert.ok(!/missed/i.test(o.lines.join(" ")), "the word missed in: " + o.lines.join(" "));
    if (a === "dip" && truth !== "planet") assert.match(o.lines[2], /You said Dip|Not this time/);
    if (a === "unsure") assert.match(o.lines[2], /Not sure/);
  }
});

test("real mode gives measurements, not a verdict: no 'it was', 'right', 'hidden planet' or 'wrong' in any real-mode text", () => {
  for (const k of Object.keys(decks)) for (let i = 0; i < 40; i++) for (const a of ANSWERS) {
    const all = textOf(k, i, "real", a).lines.join(" ");
    assert.ok(!/(it was|was right|missed|definitely|certainly|hidden planet|wrong|correct|you were)/i.test(all), "verdict wording in: " + all);
    assert.match(all, /not a verdict/);
  }
});

test("artifact lessons fire on their own kind of card and almost never on ordinary ones", () => {
  const ordinary = ["hardnoise", "lo", "hi", "clear"].flatMap((k) => facts[k]);
  const rate = (id, deck) => pct(facts[deck], (f) => lesson(id).when(f)), false_ = (id) => pct(ordinary, (f) => lesson(id).when(f));
  assert.ok(rate("pregap", "gapdip") >= 0.9, "pre-gap sag found on " + rate("pregap", "gapdip")); assert.ok(false_("pregap") <= 0.02, "false pregap " + false_("pregap"));
  assert.ok(rate("rise", "spike") >= 0.85, "spike found on " + rate("rise", "spike")); assert.ok(false_("rise") <= 0.02, "false rise " + false_("rise"));
  assert.ok(rate("deep", "eclipse") === 1 && false_("deep") === 0);
  assert.ok(rate("step", "step") >= 0.6, "step found on " + rate("step", "step")); assert.ok(false_("step") <= 0.05, "false step " + false_("step"));
  assert.ok(rate("gap_touch", "gapdip") >= 0.9 && false_("gap_touch") <= 0.03, "gap touch false " + false_("gap_touch"));
});

test("a card that nearly matches an artifact is not called plain noise, and the near-miss lesson is rare on ordinary cards", () => {
  const ordinary = ["hardnoise", "lo", "hi", "clear"].flatMap((k) => facts[k]);
  assert.ok(pct(ordinary, (f) => lesson("near_artifact").when(f)) <= 0.12, "near-miss on ordinary cards " + pct(ordinary, (f) => lesson("near_artifact").when(f)));
  for (const f of ordinary.filter((f) => lesson("near_artifact").when(f))) assert.ok(!lesson("weak").when(f), "weak must not fire next to a near miss");
  const art = ["spike", "step", "gapdip", "eclipse"].flatMap((k) => facts[k].map((f, i) => ({ f, c: decks[k][i], k })));
  const weakLead = art.filter((x) => FB.compose(x.f, { mode: "real", answer: "dip", cardId: x.k + x.c.meta.seed, kind: x.k, state: FB.newLearner() }).lead === "weak").length / art.length;
  assert.ok(weakLead <= 0.06, "real mode led with 'pure noise' on " + (100 * weakLead).toFixed(1) + "% of artifact cards");
});

test("the sentences do not repeat: 60 hard-noise cards in one sitting give many different lines, with the numbers masked", () => {
  for (const mix of [(i) => (i % 3 ? "dip" : "nodip"), () => "nodip", (i) => ["dip", "nodip", "odd", "unsure"][i % 4]]) {
    const st = FB.newLearner(), l1 = new Set(), l2 = new Set(), leads = []; let run = 1, maxRun = 1;
    for (let i = 0; i < 60; i++) {
      const ctx = { mode: "practice", truth: "noise", answer: mix(i), cardId: "v" + i, kind: "hardnoise", state: st }, o = FB.compose(facts.hardnoise[i], ctx); FB.record(st, facts.hardnoise[i], ctx, o);
      l1.add(FB.mask(o.lines[0])); l2.add(FB.mask(o.lines[1])); if (leads.at(-1) === o.lead) { run++; maxRun = Math.max(maxRun, run); } else run = 1; leads.push(o.lead);
    }
    assert.ok(l2.size >= 27, "only " + l2.size + " distinct second lines in 60 cards");
    assert.ok(l1.size >= 14, "only " + l1.size + " distinct first lines in 60 cards");
    assert.ok(maxRun <= 4, "the same lead " + maxRun + " times in a row");
  }
});

test("the pattern line speaks about Ahmed's own habit, at most once every six cards", () => {
  const st = FB.newLearner(), seen = [];
  for (let i = 0; i < 40; i++) {
    const k = i % 2 ? "hardnoise" : "lo", ctx = { mode: "practice", truth: FB.truthKey(decks[k][i]), answer: "dip", cardId: "p" + i, kind: k, state: st }, o = FB.compose(facts[k][i], ctx); FB.record(st, facts[k][i], ctx, o);
    if (o.pattern) seen.push(i);
  }
  assert.ok(seen.length >= 2, "pattern lines: " + seen.length); for (let j = 1; j < seen.length; j++) assert.ok(seen[j] - seen[j - 1] >= 6, "patterns too close: " + seen);
});

test("easy-sitting cards (real windows with box fakes) get valid texts too", () => {
  const cs = easyCards(40, 5);
  for (const [i, c] of cs.entries()) {
    const f = FB.measure(c.y, P.sigT); for (const v of Object.values(f)) assert.ok(typeof v !== "number" || Number.isFinite(v));
    for (const a of ANSWERS) { const o = FB.compose(f, { mode: "practice", truth: FB.truthKey(c), answer: a, cardId: "e" + i, kind: c.kind, state: FB.newLearner() }); assert.ok(o.words >= 36 && o.words <= 44, `easy ${c.kind} ${a}: ${o.words} words`); assert.ok(!/missed/.test(o.lines.join(" "))); }
  }
});

test("a faint brightening just under its test line is never called plain noise: it is 'close to' and not classified", () => {
  let found = 0;
  for (let i = 0; i < N && found < 8; i++) for (let h = 1800; h <= 3600; h += 100) {
    const y = decks.hardnoise[i].y.slice(); for (let j = 100; j < 103; j++) if (y[j] !== null) y[j] += h;
    const f = FB.measure(y, P.sigT);
    if (f.near_name === "a short brightening" && f.near_ratio >= FB.T.near && f.near_ratio < 1 && f.strength < 7) {
      assert.ok(lesson("near_artifact").when(f), "the near-miss lesson must fire"); assert.ok(!lesson("weak").when(f), "'pure noise often does this' must not fire");
      const o = FB.compose(f, { mode: "real", answer: "nodip", cardId: "nm" + i, kind: "x", state: FB.newLearner() }); assert.notEqual(o.lead, "weak"); found++; break;
    }
  }
  assert.ok(found >= 5, "only found " + found + " near-miss cards to test");
});

test("an answer is saved with the measured strength of its card (field f), and a card without one is saved exactly as before", () => {
  const core = req(process.env.EYES_CORE || path.join(assets, "eyes-core.js"));
  class S { constructor() { this.m = new Map(); } getItem(k) { return this.m.has(k) ? this.m.get(k) : null; } setItem(k, v) { this.m.set(k, String(v)); } }
  const store = core.createStore(new S()), r = store.startRound({ mode: "practice", source: "hard-toi1338-s98", n: 2 }), c = decks.hardnoise[0];
  c.feat = facts.hardnoise[0]; const e1 = store.recordAnswer(r.id, 0, c, "dip", 500), e2 = store.recordAnswer(r.id, 1, { kind: "quiet", truth: "none", meta: { w: 1 } }, "none", 400);
  assert.equal(e1.f.st, Math.round(facts.hardnoise[0].strength * 10) / 10); assert.ok(e1.f.dh > 0 && e1.f.gr > 0); assert.equal("f" in e2, false);
  const doc = core.roundDoc(store.finishRound(r.id), store.device); assert.deepEqual(Object.keys(doc).sort(), [...core.CLOUD_KEYS].sort());
});

test("his own habit by strength: counts per band, d-prime and criterion from measured answers only, and an honest message when nothing is measured yet", () => {
  const core = req(process.env.EYES_CORE || path.join(assets, "eyes-core.js"));
  const e = (truth, ans, st) => ({ truth, ans, f: { st, dh: 3, gr: 1.5 } }), a = [];
  for (let i = 0; i < 20; i++) a.push(e("dip", i < 18 ? "dip" : "none", 7.2 + (i % 3) * 0.9));             // 20 hidden planets, 18 called Dip (strength 7.2 to 9)
  for (let i = 0; i < 20; i++) a.push(e("none", i < 2 ? "dip" : "none", 3.5 + (i % 2) * 0.8));            // 20 quiet curves, 2 called Dip (strength 3.5 to 4.3)
  a.push({ truth: "dip", ans: "dip" });                                                           // an old answer with no measurement is left out
  const h = core.habit([{ a }]);
  assert.equal(h.n, 40); assert.equal(h.bands.find((b) => b.name === "7 to 10").n, 20); assert.equal(h.bands.find((b) => b.name === "7 to 10").planetsDip, 18);
  assert.equal(h.bands.find((b) => b.name === "3 to 5").otherDip, 2); assert.equal(h.bands.find((b) => b.name === "under 3").n, 0);
  assert.ok(Math.abs(h.dprime - 2.36) < 0.08, "d-prime " + h.dprime); assert.ok(Math.abs(h.criterion) < 0.03, "criterion " + h.criterion);
  const lean = core.habit([{ a: [...Array(15).fill(0).map(() => e("dip", "dip", 8)), ...Array(15).fill(0).map((_, i) => e("none", i < 9 ? "dip" : "none", 4))] }]);
  assert.ok(lean.criterion < -0.3, "saying Dip too readily must give a negative criterion: " + lean.criterion); assert.match(core.habitLines(lean).join(" "), /lean towards saying Dip/);
  assert.equal(core.habit([{ a: [{ truth: "dip", ans: "dip" }] }]).n, 0); assert.match(core.habitLines(core.habit([])).join(" "), /fills in as you answer/);
  assert.equal(core.habit([{ a: Array(6).fill(0).map(() => e("none", "dip", 5.5)) }]).saysDipFrom, "5 to 7"); assert.ok(!/[–—]/.test(core.habitLines(h).join(" ")));
});

test("a miss comes back 3 to 5 cards later, only unseen cards move, and the round keeps exactly the same cards", () => {
  const core = req(process.env.EYES_CORE || path.join(assets, "eyes-core.js")), mkc = () => Array.from({ length: 20 }, (_, i) => ({ kind: i % 5 === 2 ? "gapdip" : "hardnoise", id: i }));
  for (const r of [0, 0.5, 0.99]) {
    const cards = mkc(), before = cards.slice(), at = 2, to = core.bringBack(cards, at, () => r);
    assert.ok(to >= at + 3 && to <= at + 5, "placed at " + to); assert.equal(cards[to].kind, cards[at].kind);
    assert.deepEqual(cards.map((c) => c.id).sort((x, y) => x - y), before.map((c) => c.id).sort((x, y) => x - y)); assert.deepEqual(cards.slice(0, at + 3), before.slice(0, at + 3));
  }
  const none = mkc().map((c) => ({ ...c, kind: "hardnoise" })); none[2].kind = "eclipse"; assert.equal(core.bringBack(none, 2, () => 0), -1, "nothing of that kind left to bring back");
  assert.equal(core.bringBack(mkc(), 18, () => 0.5), -1, "too near the end");
});

console.log(`all ${passed} Eyes feedback checks passed`);
