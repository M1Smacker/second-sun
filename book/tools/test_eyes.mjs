// Unit tests for the Eyes mode core (book/docs/assets/eyes-core.js). No browser, no packages. Usage: node book/tools/test_eyes.mjs
// Each test targets something that must never go wrong: an answer being changed, a lost save, unreadable storage, a wrong pass line.
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const E = createRequire(import.meta.url)(process.env.EYES_CORE || path.join(here, "..", "docs", "assets", "eyes-core.js"));   // EYES_CORE: used to test the tests on a deliberately broken copy

class Storage { constructor() { this.m = new Map(); this.failWrites = false; } getItem(k) { return this.m.has(k) ? this.m.get(k) : null; } setItem(k, v) { if (this.failWrites) { const e = new Error("quota"); e.name = "QuotaExceededError"; throw e; } this.m.set(k, String(v)); } }
const seeded = (s) => () => { s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; };
const card = (kind, truth, extra = {}) => ({ kind, truth, note: `note for ${kind}`, meta: { w: 7 }, ...extra });
const CARDS = { real: card("real", "dip"), clear: card("dip2500", "dip"), faint: card("dip1500", "dip"), quiet: card("quiet", "none"), eclipse: card("eclipse", "odd"), spike: card("spike", "odd"), step: card("step", "odd") };
let passed = 0;
const test = (name, fn) => { fn(); passed++; console.log("pass:", name); };
const noon = (y, m, d) => new Date(y, m - 1, d, 12, 0, 0).getTime();

test("the official test has exactly 10 clear dips, 4 faint, 8 quiet and 8 odd, and differs between shuffles", () => {
  const a = E.compose("test", 30, seeded(1)), b = E.compose("test", 30, seeded(2));
  assert.equal(a.length, 30);
  const count = (f) => a.filter(f).length;
  assert.equal(count((s) => s.kind === "real" || (s.kind === "dip" && s.depth > 1500)), 10);
  assert.equal(count((s) => s.kind === "dip" && s.depth === 1500), 4);
  assert.equal(count((s) => s.kind === "quiet"), 8);
  assert.equal(count((s) => ["eclipse", "spike", "step"].includes(s.kind)), 8);
  assert.notDeepEqual(a.map((s) => s.kind), b.map((s) => s.kind));
});

test("practice rounds have the length asked for and always include a quiet curve", () => {
  for (const n of [5, 20, 50, 100]) {
    const d = E.compose("practice", n, seeded(n));
    assert.equal(d.length, n, `n=${n}`);
    assert.ok(d.some((s) => s.kind === "quiet"), `n=${n}: no quiet curve`);
    assert.ok(d.some((s) => s.kind === "dip"), `n=${n}: no dip`);
  }
  assert.equal(E.compose("practice", 20, seeded(3)).filter((s) => s.kind === "real").length, 1);
});

test("the banner always says what it truly was: A DIP or NOT A DIP, with the reason, whatever the answer", () => {
  for (const [name, c] of Object.entries(CARDS)) {
    for (const ans of ["dip", "none", "odd", "unsure"]) {
      const p = E.bannerParts(c, ans);
      const want = c.truth === "dip" ? "THIS WAS: A DIP" : "THIS WAS: NOT A DIP";
      assert.equal(p.headline, want, `${name}/${ans}`);
      assert.match(p.what, /^It was .+\.$/, `${name}/${ans}`);
      assert.ok(p.what.length > 12 && p.line.length > 10, `${name}/${ans}: empty text`);
    }
  }
  assert.match(E.bannerParts(CARDS.eclipse, "dip").what, /eclipse/);
  assert.match(E.bannerParts(CARDS.quiet, "dip").what, /quiet/);
  assert.match(E.bannerParts(CARDS.real, "none").what, /TOI-1338 b/);
});

test("scoring: right, wrong, partly right (not a dip but the wrong kind) and not sure", () => {
  assert.equal(E.verdict("dip", CARDS.clear).result, "right");
  assert.equal(E.verdict("none", CARDS.clear).result, "wrong");
  assert.equal(E.verdict("odd", CARDS.quiet).result, "partial");
  assert.equal(E.verdict("none", CARDS.eclipse).result, "partial");
  assert.equal(E.verdict("dip", CARDS.eclipse).result, "wrong");
  assert.equal(E.verdict("unsure", CARDS.clear).result, "unsure");
  assert.equal(E.verdict("unsure", CARDS.clear).ok, false);
  assert.match(E.bannerParts(CARDS.eclipse, "none").line, /right that it is not a dip/);
});

test("every answer is saved at once: a fresh store on the same storage sees it", () => {
  const st = new Storage(), a = E.createStore(st, { rid: seeded(5) && (() => "abc123") });
  const r = a.startRound({ mode: "practice", source: "x", n: 3 });
  assert.equal(E.createStore(st).rounds().length, 1);
  a.recordAnswer(r.id, 0, CARDS.clear, "dip", 1200);
  assert.equal(E.createStore(st).round(r.id).a.length, 1);
  a.recordAnswer(r.id, 1, CARDS.quiet, "dip", 900);
  const b = E.createStore(st).round(r.id);
  assert.equal(b.a.length, 2);
  assert.deepEqual(b.a.map((e) => [e.ans, e.ok]), [["dip", true], ["dip", false]]);
  assert.equal(b.a[1].m.w, 7, "curve metadata kept so the curve can be redrawn");
  assert.equal(b.s.falseAlarms, 1);
});

test("an answer can never be changed, repeated, skipped or added after the round ends", () => {
  const st = new Storage(), s = E.createStore(st), r = s.startRound({ mode: "test", source: "x", n: 2 });
  assert.ok(s.recordAnswer(r.id, 0, CARDS.clear, "dip", 1));
  assert.equal(s.recordAnswer(r.id, 0, CARDS.clear, "none", 1), null, "changing answer 0");
  assert.equal(s.recordAnswer(r.id, 2, CARDS.clear, "dip", 1), null, "skipping ahead");
  assert.equal(s.recordAnswer(r.id, 1, CARDS.quiet, "bogus", 1), null, "unknown answer word");
  assert.equal(s.round(r.id).a[0].ans, "dip");
  assert.ok(s.recordAnswer(r.id, 1, CARDS.quiet, "none", 1));
  s.finishRound(r.id);
  assert.equal(s.recordAnswer(r.id, 2, CARDS.clear, "dip", 1), null, "answer after the round ended");
  assert.equal(s.round(r.id).status, "done");
});

test("looking back counts the look but never touches the answer", () => {
  const s = E.createStore(new Storage()), r = s.startRound({ mode: "practice", source: "x", n: 2 });
  s.recordAnswer(r.id, 0, CARDS.clear, "none", 1);
  const before = JSON.stringify({ ans: r.a[0].ans, ok: r.a[0].ok, bin: r.a[0].bin, truth: r.a[0].truth });
  assert.ok(s.noteLookBack(r.id, 0)); assert.ok(s.noteLookBack(r.id, 0));
  assert.equal(r.a[0].lb, 2);
  assert.equal(JSON.stringify({ ans: r.a[0].ans, ok: r.a[0].ok, bin: r.a[0].bin, truth: r.a[0].truth }), before);
  assert.equal(s.noteLookBack(r.id, 1), false, "cannot look back at a question not yet answered");
  s.finishRound(r.id);
  assert.equal(s.noteLookBack(r.id, 0), false, "looks after the round ended are not counted");
});

test("a round left half done is kept as abandoned, an empty one is dropped", () => {
  const st = new Storage(), s = E.createStore(st);
  const half = s.startRound({ mode: "practice", source: "x", n: 5 }); s.recordAnswer(half.id, 0, CARDS.clear, "dip", 1); s.recordAnswer(half.id, 1, CARDS.quiet, "none", 1);
  s.startRound({ mode: "practice", source: "x", n: 5 });
  const later = E.createStore(st);
  assert.equal(later.recoverOpen(), 2);
  const rs = later.rounds();
  assert.equal(rs.length, 1);
  assert.equal(rs[0].status, "abandoned");
  assert.equal(rs[0].a.length, 2);
  assert.equal(rs[0].s.right, 2);
});

test("unreadable saved data is never silently overwritten", () => {
  const st = new Storage(); st.setItem(E.KEY, "{this is not json");
  const s = E.createStore(st, { now: () => 5 });
  assert.equal(s.rounds().length, 0);
  const backup = [...st.m.keys()].find((k) => k.startsWith(E.KEY + "-unreadable-"));
  assert.ok(backup, "no backup of the unreadable data");
  assert.equal(st.getItem(backup), "{this is not json");
  const old = new Storage(); old.setItem(E.KEY, JSON.stringify({ v: 99, rounds: [], device: {} }));
  E.createStore(old); assert.ok([...old.m.keys()].some((k) => k.includes("unreadable")), "newer format must be backed up too");
});

test("when the device refuses to save, the screen is told and the round still works in memory", () => {
  const st = new Storage(), s = E.createStore(st), r = s.startRound({ mode: "practice", source: "x", n: 2 });
  st.failWrites = true;
  const e = s.recordAnswer(r.id, 0, CARDS.clear, "dip", 1);
  assert.ok(e, "answer must still be accepted in memory");
  assert.equal(s.lastError, "QuotaExceededError");
  st.failWrites = false;
  s.recordAnswer(r.id, 1, CARDS.quiet, "none", 1);
  assert.equal(s.lastError, null);
  assert.equal(E.createStore(st).round(r.id).a.length, 2, "the later successful save carries the earlier answer too");
});

test("listeners hear about saves (the cloud upload will use this) and cannot break saving", () => {
  const s = E.createStore(new Storage()), seen = [];
  s.onChange((ev) => seen.push(ev)); s.onChange(() => { throw new Error("bad listener"); });
  const r = s.startRound({ mode: "practice", source: "x", n: 1 });
  s.recordAnswer(r.id, 0, CARDS.clear, "dip", 1); s.finishRound(r.id);
  assert.deepEqual(seen, ["start", "answer", "finish"]);
  assert.equal(s.unsynced().length, 1);
});

test("summary counts: clear and faint dips, false alarms, odd things, looks", () => {
  const mk = (c, ans, lb = 0) => ({ kind: c.kind, truth: c.truth, ans, ok: E.verdict(ans, c).ok, bin: E.verdict(ans, c).bin, lb });
  const s = E.summarize([mk(CARDS.clear, "dip"), mk(CARDS.real, "none"), mk(CARDS.faint, "dip"), mk(CARDS.faint, "unsure"), mk(CARDS.quiet, "dip"), mk(CARDS.quiet, "none"),
    mk(CARDS.eclipse, "odd", 1), mk(CARDS.spike, "dip"), mk(CARDS.step, "none")]);
  assert.deepEqual([s.n, s.right, s.wrong, s.unsure], [9, 4, 4, 1]);
  assert.deepEqual([s.dips, s.dipsFound, s.clear, s.clearFound, s.faint, s.faintFound], [4, 2, 2, 1, 2, 1]);
  assert.deepEqual([s.quiet, s.falseAlarms, s.odd, s.oddSpotted, s.oddCalledDip, s.lookedBack, s.partial], [2, 1, 3, 1, 1, 1, 1]);
  assert.ok(E.summaryLines(s).join(" ").includes("found 2 of 4"));
});

test("Wilson range behaves: 17 of 20 is about 64% to 95%, 0 of 0 is the whole range", () => {
  const [lo, hi] = E.wilson(17, 20);
  assert.ok(lo > 0.62 && lo < 0.66 && hi > 0.93 && hi < 0.97, `${lo} ${hi}`);
  assert.deepEqual(E.wilson(0, 0), [0, 1]);
});

function testRound(store, t0, ansFor) {
  const specs = E.compose("test", 30, seeded(t0 % 997 + 1)), r = store.startRound({ mode: "test", source: "x", n: 30 });
  r.t0 = t0;
  specs.forEach((sp, i) => {
    const c = sp.kind === "real" ? CARDS.real : sp.kind === "quiet" ? CARDS.quiet : sp.kind === "dip" ? (sp.depth === 1500 ? CARDS.faint : CARDS.clear) : sp.kind === "eclipse" ? CARDS.eclipse : sp.kind === "spike" ? CARDS.spike : CARDS.step;
    store.recordAnswer(r.id, i, c, ansFor(c, i), 1000);
  });
  store.finishRound(r.id); return r;
}
const perfect = (c) => c.truth;
const missesThree = (c, i) => (c.truth === "dip" && c.kind !== "dip1500" && i % 4 === 0 ? "none" : c.truth);

test("pass line: needs 2 rounds, 60 curves and 2 days before it says anything", () => {
  const s = E.createStore(new Storage());
  assert.equal(E.passLine(s.rounds()).verdict, "not_enough");
  testRound(s, noon(2026, 10, 23), perfect);
  assert.equal(E.passLine(s.rounds()).verdict, "not_enough");
  testRound(s, noon(2026, 10, 23) + 3600e3, perfect);
  const p = E.passLine(s.rounds());
  assert.equal(p.verdict, "not_enough", "two rounds on the same day are not enough");
  assert.ok(p.needs.some((x) => /different day/.test(x)));
  testRound(s, noon(2026, 10, 24), perfect);
  assert.equal(E.passLine(s.rounds()).verdict, "meets");
});

test("pass line: below the line when clear dips are missed or quiet curves are called dips; faint dips do not count", () => {
  const s = E.createStore(new Storage());
  testRound(s, noon(2026, 10, 23), missesThree); testRound(s, noon(2026, 10, 24), missesThree);
  const p = E.passLine(s.rounds());
  assert.equal(p.verdict, "below");
  assert.ok(p.clear.rate < 0.85, String(p.clear.rate));
  const t = E.createStore(new Storage());
  const faintMissed = (c) => (c.kind === "dip1500" ? "none" : c.truth);
  testRound(t, noon(2026, 10, 23), faintMissed); testRound(t, noon(2026, 10, 24), faintMissed);
  assert.equal(E.passLine(t.rounds()).verdict, "meets", "missing only the faintest dips must not fail the line");
  const u = E.createStore(new Storage());
  const alarms = (c, i) => (c.truth === "none" && i % 2 === 0 ? "dip" : c.truth);
  testRound(u, noon(2026, 10, 23), alarms); testRound(u, noon(2026, 10, 24), alarms);
  const q = E.passLine(u.rounds());
  assert.equal(q.verdict, "below"); assert.ok(q.quiet.rate > 0.10);
});

test("pass line ignores practice rounds and unfinished test rounds", () => {
  const s = E.createStore(new Storage());
  const pr = s.startRound({ mode: "practice", source: "x", n: 20 }); for (let i = 0; i < 20; i++) s.recordAnswer(pr.id, i, CARDS.clear, "dip", 1); s.finishRound(pr.id);
  const half = s.startRound({ mode: "test", source: "x", n: 30 }); s.recordAnswer(half.id, 0, CARDS.clear, "dip", 1);
  assert.equal(E.passLine(s.rounds()).curves, 0);
  s.finishRound(half.id);
  assert.equal(E.passLine(s.rounds()).curves, 0, "a finished test round with fewer answers than planned is not complete");
});

test("export round-trips and holds every round with its answers", () => {
  const s = E.createStore(new Storage()); testRound(s, noon(2026, 10, 23), perfect);
  const x = JSON.parse(s.exportJSON());
  assert.equal(x.rounds.length, 1); assert.equal(x.rounds[0].a.length, 30); assert.equal(x.schema, 1);
  assert.ok(x.device.id);
});

console.log(`all ${passed} Eyes core checks passed`);
