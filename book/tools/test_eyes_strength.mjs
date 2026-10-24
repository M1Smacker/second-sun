// Golden test: the JavaScript strength function (docs/assets/eyes-strength.js) must give the same numbers as the hunt's own box_scores() in pipeline/detect_v2.py.
// The numbers in golden_box_scores.json come from the Python (make_golden_box_scores.py). Usage: node book/tools/test_eyes_strength.mjs
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url)), req = createRequire(import.meta.url);
const SS = req(process.env.EYES_STRENGTH || path.join(here, "..", "docs", "assets", "eyes-strength.js"));
const golden = JSON.parse(fs.readFileSync(path.join(here, "golden_box_scores.json"), "utf8"));
let passed = 0;
const test = (name, fn) => { fn(); passed++; console.log("pass:", name); };

test("the same numbers as the Python box_scores on every golden array and every hunt duration", () => {
  let compared = 0;
  for (const c of golden) for (const o of c.out) {
    const r = SS.boxScores(c.bf, o.dur_h);
    assert.equal(r.snr.length, o.snr.length, `${c.name} ${o.dur_h} h: length`);
    for (let i = 0; i < o.snr.length; i++) {
      const a = Number.isFinite(r.snr[i]) ? r.snr[i] : null, b = o.snr[i], ma = Number.isFinite(r.m[i]) ? r.m[i] : null, mb = o.m[i];
      assert.equal(a === null, b === null, `${c.name} ${o.dur_h} h box ${i}: missing-ness differs`);
      assert.equal(ma === null, mb === null, `${c.name} ${o.dur_h} h box ${i}: mean missing-ness differs`);
      if (b !== null) { assert.ok(Math.abs(a - b) < 1e-9, `${c.name} ${o.dur_h} h box ${i}: ${a} vs ${b}`); assert.ok(Math.abs(ma - mb) < 1e-7, `${c.name} ${o.dur_h} h mean ${i}`); compared++; }
    }
  }
  assert.ok(compared > 3000, "only " + compared + " numbers compared");
});

test("the hunt durations are whole numbers of ten-minute bins", () => {
  assert.deepEqual(SS.DURS_H.map(SS.widthOf), [18, 24, 30, 39, 48, 60, 72, 90]);
});

test("a deep dip is found where it is, strongest at about its own length, and a card scored with the sector's scale agrees with the array's own scale", () => {
  const x = golden.find((c) => c.name === "noise with a dip").bf, sig = SS.sectorSig(x), hb = SS.huntBoxes(x, sig);
  const best = hb.boxes.reduce((p, q) => (q.s > p.s ? q : p));
  assert.ok(best.a + best.w > 290 && best.a < 350, "best box at " + best.a);
  const own = Math.max(...SS.DURS_H.flatMap((d) => SS.boxScores(x, d).snr.filter(Number.isFinite)));
  assert.ok(Math.abs(own - best.s) < 1e-9, `own ${own} vs ${best.s}`);
});

test("a noise-free dip of unit depth scores depth over the scale of the best box", () => {
  const sig = { 18: 100, 24: 100, 30: 100, 39: 100, 48: 100, 60: 100, 72: 100, 90: 100 }, p = new Array(40).fill(1);
  assert.ok(Math.abs(SS.profileStrength(p, sig) - 0.01) < 1e-12, "flat 40-bin dip, boxes up to 39 bins fit inside: " + SS.profileStrength(p, sig));
});

test("a short or gappy array is handled: no scale from fewer than 20 boxes, and a box missing 20 percent of its points is skipped", () => {
  const short = golden.find((c) => c.name.startsWith("too short"));
  assert.ok(SS.boxScores(short.bf, 15).snr.every((v) => Number.isNaN(v)));
  const x = new Array(60).fill(0); for (let i = 0; i < 12; i++) x[i] = null;
  const m = SS.boxMeans(x, 24, 0.8); assert.ok(Number.isNaN(m[0]) && Number.isFinite(m[12]));
});

console.log(`all ${passed} Eyes strength checks passed`);
