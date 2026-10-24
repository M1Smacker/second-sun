// Tests for the Eyes HARD test: the card generator (docs/assets/eyes-hard.js) and its scoring in eyes-core.js. Usage: node book/tools/test_eyes_hard.mjs
// Targets what must never go wrong: a hard-noise card that is NOT the best-looking dip of a sector (then the test is as easy as the old one), a fake planet that is not as strong
// as it says, cards that give themselves away by where the event sits, a hard round leaking into the old pass line (or the reverse), and "Not sure" scored the wrong way.
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url)), req = createRequire(import.meta.url);
const core = req(process.env.EYES_CORE || path.join(here, "..", "docs", "assets", "eyes-core.js"));
const H = req(process.env.EYES_HARD || path.join(here, "..", "docs", "assets", "eyes-hard.js"));
const J = JSON.parse(fs.readFileSync(path.join(here, "..", "docs", "assets", "data", "toi1338-s98.json"), "utf8").replace(/^﻿/, ""));
const P = H.prepare(J), W = H.WIN;
let passed = 0;
const test = (name, fn) => { fn(); passed++; console.log("pass:", name); };
const rngOf = (s) => H.mulberry32(s);

// the best box dip inside one card, scored the way the detector scores it
function windowScore(y, sigma) {
  const x = y.map((v) => (v === null ? 0 : v)), c = [0]; for (let i = 0; i < x.length; i++) c.push(c[i] + x[i]);
  let best = -Infinity; for (const n of H.BOXES) for (let t = 0; t + n <= x.length; t++) best = Math.max(best, -(c[t + n] - c[t]) / Math.sqrt(n) / sigma);
  return best;
}
const med = (a) => a.slice().sort((x, y) => x - y)[a.length >> 1];
const mean = (a) => { const b = a.filter((v) => v !== null); return b.reduce((s, v) => s + v, 0) / b.length; };
const cards = (spec, n, seed0 = 1) => Array.from({ length: n }, (_, i) => H.build(P, spec, seed0 + i * 7919));

test("the star's own noise is measured sensibly", () => {
  assert.ok(P.sigma > 500 && P.sigma < 2000, "sigma " + P.sigma);
  assert.ok(P.resid.length > 3000 && P.ecl.length === 4);
});

test("a card is rebuilt exactly from its seed, and different seeds give different cards", () => {
  for (const spec of [{ kind: "hardnoise" }, { kind: "dip", tier: "clear", snr: 12 }, { kind: "gapdip" }, { kind: "eclipse" }, { kind: "step" }]) {
    const a = H.build(P, spec, 4242), b = H.build(P, spec, 4242), c = H.build(P, spec, 4243);
    assert.deepEqual(a, b, spec.kind + " not repeatable");
    assert.notDeepEqual(a.y, c.y, spec.kind + " seeds not different");
    assert.equal(a.y.length, W);
  }
});

test("hard-noise cards hold the best dip of a whole sector, far better looking than an ordinary stretch", () => {
  const hard = cards({ kind: "hardnoise" }, 60).map((c) => windowScore(c.y, P.sigma));
  const plain = Array.from({ length: 60 }, (_, i) => windowScore(H.surrogate(P, rngOf(900 + i), W), P.sigma));
  assert.ok(med(hard) - med(plain) > 0.8, `hard ${med(hard).toFixed(2)} vs plain ${med(plain).toFixed(2)}`);
  assert.ok(med(hard) > 3.5 && med(hard) < 7, "hard-noise median score " + med(hard).toFixed(2) + " should sit below the hunt's threshold of 7");
  for (const c of cards({ kind: "hardnoise" }, 10)) { assert.equal(c.truth, "none"); assert.equal(c.tier, "hardnoise"); assert.ok(c.meta.score > 3); }
});

test("the event does not sit in the same place on every kind of card (position must not give the answer away)", () => {
  for (const spec of [{ kind: "hardnoise" }, { kind: "dip", tier: "clear", snr: 12 }]) {
    const starts = cards(spec, 60).map((c) => c.box[0]);
    assert.ok(Math.max(...starts) - Math.min(...starts) > 100, spec.kind + " spread " + (Math.max(...starts) - Math.min(...starts)));
  }
  const a = mean(cards({ kind: "hardnoise" }, 80).map((c) => c.box[0])), b = mean(cards({ kind: "dip", tier: "clear", snr: 12 }, 80).map((c) => c.box[0]));
  assert.ok(Math.abs(a - b) < 25, `mean event start differs: ${a.toFixed(0)} vs ${b.toFixed(0)}`);
});

test("a fake planet is as strong as it says it is, on the detector's scale", () => {
  const P0 = { ...P, resid: new Array(20000).fill(0) };                           // no noise at all, so only the dip is measured
  for (const snr of [5, 8, 12, 16]) {
    const got = Array.from({ length: 30 }, (_, i) => windowScore(H.build(P0, { kind: "dip", tier: "clear", snr }, 77 + i * 31).y, P.sigma));
    const r = mean(got) / snr;
    assert.ok(r > 0.75 && r < 1.2, `nominal ${snr}: measured mean ${mean(got).toFixed(2)} (ratio ${r.toFixed(2)})`);
  }
  const c = H.build(P, { kind: "dip", tier: "border", snr: 6 }, 5), m = c.meta;
  assert.equal(c.truth, "dip"); assert.ok(m.d >= 24 && m.d <= 72 && m.ramp >= 2); assert.ok(Math.abs(m.depth - H.dipDepth(6, m.d, m.ramp, P.sigma)) <= 1);
});

test("the dip is really in the data, with sloping sides and a flat bottom", () => {
  const P0 = { ...P, resid: new Array(20000).fill(0) }, c = H.build(P0, { kind: "dip", tier: "clear", snr: 14 }, 11), m = c.meta;
  const inside = c.y.slice(m.a + m.ramp, m.a + m.d - m.ramp), outside = c.y.slice(0, Math.max(1, m.a - 5));
  assert.ok(mean(outside) - mean(inside) > 0.7 * m.depth, "bottom is not " + m.depth + " ppm below the rest");
  assert.ok(c.y[m.a] > mean(inside) + 0.2 * m.depth, "the first step of the dip should still be on the slope");
});

test("the official hard test has exactly the agreed mix, and every strength is inside its band", () => {
  const specs = H.compose("test", 30, rngOf(3)), count = (f) => specs.filter(f).length;
  assert.equal(specs.length, 30);
  assert.equal(count((s) => s.tier === "clear"), 6); assert.equal(count((s) => s.tier === "border"), 6); assert.equal(count((s) => s.kind === "hardnoise"), 8);
  for (const k of ["eclipse", "spike", "step", "gapdip"]) assert.equal(count((s) => s.kind === k), { eclipse: 3, spike: 2, step: 2, gapdip: 3 }[k], k);
  for (const s of specs.filter((s) => s.tier === "clear")) assert.ok(s.snr >= 10 && s.snr <= 16);
  for (const s of specs.filter((s) => s.tier === "border")) assert.ok(s.snr >= 5 && s.snr <= 8.5);
  assert.equal(new Set(specs.map((s) => s.seed)).size, 30, "every card has its own seed");
  const built = specs.map((s) => H.build(P, s, s.seed));
  assert.equal(built.filter((c) => c.truth === "dip").length, 12); assert.equal(built.filter((c) => c.truth === "none").length, 8); assert.equal(built.filter((c) => c.truth === "odd").length, 10);
  for (const n of [5, 20, 50, 100]) assert.equal(H.compose("practice", n, rngOf(n)).length, n, "practice length " + n);
});

test("a dip at a gap really ends where the data stops, and a down-jump never recovers", () => {
  for (const c of cards({ kind: "gapdip" }, 20)) {
    const m = c.meta, nulls = c.y.filter((v) => v === null).length;
    assert.equal(c.truth, "odd"); assert.ok(nulls >= 24, "gap of " + nulls);
    assert.ok(c.y.slice(m.a + m.d, m.a + m.d + 24).every((v) => v === null), "the gap must start right after the dip");
  }
  for (const c of cards({ kind: "step" }, 20)) { const m = c.meta; assert.equal(c.truth, "odd"); assert.ok(Math.sign(mean(c.y.slice(m.a + 5)) - mean(c.y.slice(0, m.a - 5))) === m.sign); }
});

test("a gap alone is no giveaway: other cards have gaps too, never touching the event, and only the gap-dip card has a dip that ends at one", () => {
  const specs = [{ kind: "hardnoise" }, { kind: "dip", tier: "clear", snr: 12 }, { kind: "dip", tier: "border", snr: 6 }, { kind: "spike" }, { kind: "step" }];
  let withGap = 0, total = 0;
  for (const spec of specs) for (const c of cards(spec, 60, 31)) {
    total++; const nulls = c.y.map((v, i) => (v === null ? i : -1)).filter((i) => i >= 0);
    if (nulls.length) { withGap++; assert.ok(nulls.length >= 24 && nulls.length <= 60); assert.ok(nulls[0] > c.box[1] + 39 || nulls.at(-1) < c.box[0] - 39, "a decoy gap must stay away from the event"); }
  }
  assert.ok(withGap / total > 0.25 && withGap / total < 0.55, "share of ordinary cards with a gap: " + (withGap / total).toFixed(2));
  for (const c of cards({ kind: "gapdip" }, 30, 5)) assert.equal(c.y.indexOf(null), c.meta.a + c.meta.d, "the gap must start exactly where the dip ends");
});

test("an eclipse card is a real eclipse of this star, levelled, and deep", () => {
  for (const c of cards({ kind: "eclipse" }, 6)) { assert.equal(c.truth, "odd"); assert.ok(Math.min(...c.y.filter((v) => v !== null)) < -10000, "min " + Math.min(...c.y.filter((v) => v !== null))); }
});

// ---- scoring ----
const ent = (t, ans, extra = {}) => ({ i: 0, kind: t, truth: t === "clear" || t === "border" ? "dip" : t === "hardnoise" ? "none" : "odd", ans, ok: (t === "odd" && ans === "odd"), t, m: null, ...extra });
function roundOf(day, over = {}) {
  const a = [];
  for (let i = 0; i < 6; i++) a.push(ent("clear", over.clear || "dip"));
  for (let i = 0; i < 3; i++) a.push(ent("border", over.border || "dip", { m: { snr: 5.8 } })), a.push(ent("border", over.border || "unsure", { m: { snr: 7.4 } }));
  for (let i = 0; i < 8; i++) a.push(ent("hardnoise", over.noise ? (i < over.noiseCalls ? "dip" : over.noise) : "none"));
  for (let i = 0; i < 10; i++) a.push(ent("odd", "odd"));
  return { id: "r" + Math.random(), mode: "test", source: "hard-toi1338-s98", status: "done", n: 30, t0: new Date(2026, 9, day, 12).getTime(), t1: 1, a };
}
const v1round = (day) => ({ id: "v" + day, mode: "test", source: "practice-toi1338-s98", status: "done", n: 1, t0: new Date(2026, 9, day, 12).getTime(), t1: 1, a: [{ i: 0, kind: "dip2500", truth: "dip", ans: "dip", ok: true, bin: true, ms: 1, lb: 0, m: null }] });

test("hard scoring counts each tier, and Not sure is a miss on a clear fake planet but free on hard noise", () => {
  const h = core.summarizeHard(roundOf(24, { clear: "unsure", noise: "unsure", noiseCalls: 0 }).a);
  assert.equal(h.clear, 6); assert.equal(h.clearFound, 0); assert.equal(h.clearUnsure, 6);
  assert.equal(h.noise, 8); assert.equal(h.noiseFA, 0); assert.equal(h.noiseUnsure, 8);
  assert.equal(h.border, 6); assert.equal(h.odd, 10); assert.equal(h.oddRight, 10);
  assert.equal(h.unsureOnHard, 8 + 3, "Not sure on hard noise and near-limit planets counts as well placed");
  assert.deepEqual(h.bands.map((b) => b.n), [3, 3]);
  const lines = core.hardLines(h).join(" ");
  assert.match(lines, /Clear fake planets: you said Dip on 0 of 6 \(Not sure on 6\)/); assert.match(lines, /Hard noise \(nothing hidden\): you called a dip on 0 of 8, Not sure on 8/);
});

test("the hard line: not enough, then meets, then below; the numbers are the ones fixed in advance", () => {
  assert.deepEqual({ ...core.HARD }, { clearHit: 0.80, noiseFalseAlarm: 0.20, minCurves: 120, minRounds: 4, minDays: 2 });
  const three = core.hardLine([roundOf(24), roundOf(24), roundOf(25)]);
  assert.equal(three.verdict, "not_enough"); assert.match(three.needs.join(), /1 more hard test round/);
  const oneDay = core.hardLine([roundOf(24), roundOf(24), roundOf(24), roundOf(24)]);
  assert.equal(oneDay.verdict, "not_enough"); assert.match(oneDay.needs.join(), /different day/);
  const good = core.hardLine([roundOf(24), roundOf(24), roundOf(25), roundOf(25)]);
  assert.equal(good.verdict, "meets"); assert.equal(good.curves, 120); assert.equal(good.days, 2);
  const missesClear = core.hardLine([24, 24, 25, 25].map((d) => roundOf(d, { clear: "unsure" })));
  assert.equal(missesClear.verdict, "below", "Not sure on every clear planet must fail the line");
  const edge = core.hardLine([24, 24, 25, 25].map((d) => roundOf(d, { noise: "none", noiseCalls: 2 })));      // 2 of 8 = 25% called a dip
  assert.equal(edge.verdict, "below", "25% of hard noise called a dip is over the 20% line");
  const ok = core.hardLine([24, 24, 25, 25].map((d) => roundOf(d, { noise: "none", noiseCalls: 0 })));
  assert.equal(ok.verdict, "meets");
  const nsOnNoise = core.hardLine([24, 24, 25, 25].map((d) => roundOf(d, { noise: "unsure", noiseCalls: 0 })));
  assert.equal(nsOnNoise.verdict, "meets", "Not sure on hard noise is free");
  assert.match(good.lines.join(" "), /Clear fake planets found: 24 of 24/);
});

test("the old pass line and the hard line never see each other's rounds", () => {
  const old = [v1round(24), v1round(24), v1round(25)], hard = [roundOf(24), roundOf(25), roundOf(25), roundOf(25)];
  assert.deepEqual(core.passLine(old.concat(hard)), core.passLine(old));
  assert.deepEqual(core.hardLine(old.concat(hard)), core.hardLine(hard));
  assert.equal(core.hardLine(old).rounds, 0);
  assert.equal(core.isHard({ source: "hard-toi1338-s98" }), true); assert.equal(core.isHard({ source: "practice-toi1338-s98" }), false); assert.equal(core.isHard({}), false);
});

test("an answer to a hard card is saved with its tier, an answer to an old card is saved exactly as before, and the cloud shape is unchanged", () => {
  class S { constructor() { this.m = new Map(); } getItem(k) { return this.m.has(k) ? this.m.get(k) : null; } setItem(k, v) { this.m.set(k, String(v)); } }
  const store = core.createStore(new S()), r = store.startRound({ mode: "test", source: "hard-toi1338-s98", n: 2 });
  const hardCard = H.build(P, { kind: "hardnoise" }, 9), oldCard = { kind: "quiet", truth: "none", note: "n", meta: { w: 1 } };
  const e1 = store.recordAnswer(r.id, 0, hardCard, "unsure", 900), e2 = store.recordAnswer(r.id, 1, oldCard, "none", 800);
  assert.equal(e1.t, "hardnoise"); assert.equal("t" in e2, false);
  assert.deepEqual(e1.m, hardCard.meta);
  const done = store.finishRound(r.id), doc = core.roundDoc(done, store.device);
  assert.deepEqual(Object.keys(doc).sort(), [...core.CLOUD_KEYS].sort());
  const body = core.toFirestoreBody(done, store.device);
  assert.deepEqual(Object.keys(body.fields).sort(), [...core.CLOUD_KEYS].sort());
  assert.equal(body.fields.mode.stringValue, "test"); assert.equal(body.fields.source.stringValue, "hard-toi1338-s98");
});

test("the banner for hard cards says what they truly were", () => {
  const n = core.bannerParts(H.build(P, { kind: "hardnoise" }, 1), "dip"), g = core.bannerParts(H.build(P, { kind: "gapdip" }, 1), "dip");
  assert.equal(n.headline, "THIS WAS: NOT A DIP"); assert.match(n.what, /best-looking dip of a whole sector of noise/); assert.match(n.detail, /Not sure was a fair answer/);
  assert.equal(g.headline, "THIS WAS: NOT A DIP"); assert.match(g.what, /gap in the data/); assert.match(g.detail, /thruster/);
});

console.log(`all ${passed} Eyes hard-test checks passed`);
