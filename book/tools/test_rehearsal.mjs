// Tests for the rehearsal (book/docs/assets/rehearsal.js and rehearsal-deck.json; 2 Nov 2026). Usage: node book/tools/test_rehearsal.mjs
// What must never go wrong: an answer changed after it is locked, a round the cloud rules would refuse, a pass line that says "meets" when it does not, a picture that leaks the truth,
// a deck that tells the answer by its shape or carries a star name, neighbouring items from one star.
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url)), req = createRequire(import.meta.url);
const R = req(path.join(here, "..", "docs", "assets", "rehearsal.js"));
const core = req(path.join(here, "..", "docs", "assets", "eyes-core.js"));
const DECK = path.join(here, "..", "docs", "assets", "rehearsal-deck.json");
class Storage { constructor() { this.m = new Map(); } getItem(k) { return this.m.has(k) ? this.m.get(k) : null; } setItem(k, v) { this.m.set(k, String(v)); } }
let n = 0;
const ok = (c, msg) => { n++; assert.ok(c, msg); console.log("pass:", msg); };

// ---- 1. statistics ----
ok(Object.keys(R.LABEL).length === 6 && R.BUTTONS.length === 6 && R.BUTTONS.every((b) => R.LABEL[b]), "six answers, each with a label");
const d1 = R.dprime(40, 50, 5, 50);
ok(d1 > 2.0 && d1 < 2.3, `d-prime for 80% hits and 10% false alarms is about 2.1 (got ${d1.toFixed(2)})`);
ok(Math.abs(R.dprime(25, 50, 25, 50)) < 0.01 && Number.isFinite(R.dprime(50, 50, 0, 50)), "equal rates give 0 and perfect scores stay finite");
ok(R.dprime(0, 0, 1, 2) === null, "no planets or no others: not measured");
const w = R.wilson(8, 10); ok(w[0] > 0.45 && w[1] < 0.97 && R.wilson(0, 0)[1] === 1, "Wilson interval for 8 of 10");

// ---- 2. entries, summaries, reveal ----
const item = (cls, tier, star, extra = {}) => ({ cls, tier, star, box_h: 6.5, meta: { strength: 11, depth_ppm: 2400, box_h: 6.5, kind: "primary", amp_ppm: 900, step_ppm: 800 }, ...extra });
const e1 = R.entryOf(0, item("planet", "clear", 1), "planet", "high", 1234), e2 = R.entryOf(1, item("noise", null, 2), "planet", null, 900), e3 = R.entryOf(2, item("eclipse", null, 3), "eclipse", "low", 800);
ok(e1.ok && e1.pc && !e2.ok && e2.pc && e3.ok && !e3.pc && e1.tier === "clear" && e1.st === 11, "entries: right, planet-like call, tier and strength kept");
const s = R.summaryOf([e1, e2, e3]);
ok(s.n === 3 && s.right === 2 && s.clear === 1 && s.clearHit === 1 && s.others === 2 && s.othersCalledPlanet === 1 && s.byClass.eclipse.right === 1, "summary counts hits, false alarms and classes");
const rv = R.reveal(item("noise", null, 2), "planet");
ok(/UNCLEAR/.test(rv.headline) && /false alarm/.test(rv.call) && !rv.right && /Nothing was hidden/.test(rv.what), "reveal: a planet call on nothing is a false alarm");
ok(/hit/.test(R.reveal(item("planet", "near", 1), "planet").call) && /miss/.test(R.reveal(item("planet", "near", 1), "eclipse").call) && /fair to miss/.test(R.reveal(item("planet", "near", 1), "eclipse").what), "reveal: hit, miss, and near-limit wording");

// ---- 3. the pass line ----
const DAYS = ["2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09", "2026-11-10"];
function round(day, { clearHits = 3, nearHits = 2, faCalls = 1, status = "done" } = {}) {
  const a = []; let i = 0;
  for (let k = 0; k < 3; k++) a.push(R.entryOf(i++, item("planet", "clear", i), k < clearHits ? "planet" : "noise", null, 1000));
  for (let k = 0; k < 3; k++) a.push(R.entryOf(i++, item("planet", "near", i), k < nearHits ? "planet" : "noise", null, 1000));
  for (let k = 0; k < 14; k++) a.push(R.entryOf(i++, item(["eclipse", "flare", "step", "noise", "instrument"][k % 5], null, i), k < faCalls ? "planet" : "noise", null, 1000));
  return { status, t0: Date.parse(day + "T12:00:00"), a };
}
const good = DAYS.map((d) => round(d, { clearHits: 3, nearHits: 2, faCalls: 1 }));
const pl = R.passLine(good);
ok(pl.verdict === "meets" && pl.sessions === 8 && pl.days === 8 && pl.dprime > 2 && pl.clear.rate === 1, `eight good sessions on eight days meet the line (d-prime ${pl.dprime.toFixed(2)})`);
ok(R.passLine(good.slice(0, 7)).verdict === "not_enough" && R.passLine(good.slice(0, 7)).needs.some((x) => /1 more session/.test(x)), "seven sessions are not enough");
ok(R.passLine(good.map((r) => ({ ...r, t0: Date.parse("2026-11-03T12:00:00") + 3600e3 * 0 }))).verdict === "not_enough", "eight sessions on one day are not enough (needs four days)");
ok(R.passLine(DAYS.map((d) => round(d, { faCalls: 6 }))).verdict === "below", "6 false alarms in 14 others (43%) is below the line");
ok(R.passLine(DAYS.map((d) => round(d, { clearHits: 1 }))).verdict === "below", "one clear fake in three found is below the line");
ok(R.passLine([...good.slice(0, 7), round(DAYS[7], { status: "abandoned" })]).sessions === 7, "an abandoned session does not count");
ok(R.nextSession(good) === 0 && R.nextSession(good.slice(0, 3)) === 3 && R.nextSession([]) === 0, "the next session follows the number finished, cycling after eight");

// ---- 4. order: never two neighbours from one star ----
const items = Array.from({ length: 20 }, (_, i) => item("noise", null, 1 + (i % 12)));
let bad = 0, seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (let t = 0; t < 300; t++) { const o = R.orderSession(items, rnd); for (let i = 1; i < o.length; i++) if (o[i].star === o[i - 1].star) bad++; if (o.length !== 20) bad++; }
ok(bad === 0, "300 random orders: 20 items each, no two neighbours from one star");

// ---- 5. the store: locked answers, cloud rules ----
let t = 1e12; const store = R.createStore(new Storage(), { now: () => (t += 1000), rid: () => "abc123" });
const r = store.startRound({ n: 3, session: 0 });
ok(r.mode === "practice" && r.source === "rehearsal-v1" && r.v === 1 && r.status === "open", "a round is mode practice, source rehearsal-v1, version 1 (the published cloud rules accept it)");
const it0 = item("planet", "clear", 1);
ok(store.recordAnswer(r.id, 1, it0, "planet", null, 10) === null, "skipping ahead is refused");
ok(store.recordAnswer(r.id, 0, it0, "bogus", null, 10) === null, "an unknown answer is refused");
ok(store.recordAnswer(r.id, 0, it0, "planet", "high", 10) !== null && store.recordAnswer(r.id, 0, it0, "noise", null, 10) === null, "the first answer is kept; a second answer to the same item is refused (answers cannot be changed)");
store.recordAnswer(r.id, 1, item("noise", null, 2), "noise", null, 10); store.recordAnswer(r.id, 2, item("flare", null, 3), "flare", null, 10);
ok(store.unsynced().length === 0, "an open round is never offered to the cloud");
store.finishRound(r.id);
ok(store.unsynced().length === 1 && store.finishRound(r.id) === null, "a finished round is offered once and cannot be finished twice");
const doc = core.roundDoc(store.round(r.id), store.device);
ok(Object.keys(doc).every((k) => core.CLOUD_KEYS.includes(k)) && ["practice", "test", "real"].includes(doc.mode) && doc.n <= 200 && doc.a.length <= 200 && doc.v === 1, "the cloud document has only the allowed keys, an allowed mode, at most 200 answers");
const body = core.toFirestoreBody(store.round(r.id), store.device);
ok(body.fields.source.stringValue === "rehearsal-v1" && body.fields.a.arrayValue.values.length === 3, "the document encodes for Firestore with the source tag and every answer");
store.markSynced(r.id); ok(store.unsynced().length === 0, "a synced round is not sent again");
const store2 = R.createStore(new Storage(), { now: () => (t += 1000), rid: () => "zzz999" }); const r2 = store2.startRound({ n: 3, session: 1 }); store2.recordAnswer(r2.id, 0, it0, "planet", null, 5); store2.startRound({ n: 3, session: 2 });
ok(store2.recoverOpen() === 2 && store2.round(r2.id).status === "abandoned" && store2.rounds().length === 1, "a half-done session is kept as abandoned; an empty one is dropped");

// ---- 6. the pictures never carry the truth ----
const deck = JSON.parse(fs.readFileSync(DECK, "utf8"));
const base = deck.sessions[0].find((x) => x.cls === "planet");
const same = (cls) => ({ ...base, cls, tier: null, meta: {} });
ok(R.svgP1(same("noise")) === R.svgP1(same("planet")) && R.svgP2(same("noise")) === R.svgP2(same("eclipse")) && R.svgP3(same("flare")) === R.svgP3(same("step")), "the three panels draw identically whatever the hidden class (they cannot leak it)");
const sv = R.svgP2(base);
ok(/^<svg/.test(sv) && /<path/.test(sv) && /ss-rh-br/.test(sv) && !/planet|noise|flare|instrument/i.test(sv.replace(/ss-rh-[a-z]+/g, "")), "panel 2 is an svg with the data lines and the event bracket and no class words");
ok(R.svgP1(base).includes("ss-rh-ev") && R.svgP3(base).includes("ss-rh-dot"), "panel 1 marks the event and panel 3 marks the phase");

// ---- 7. the deck ----
const GRID = [3, 4, 5, 6.5, 8, 10, 12, 15], KEYS = new Set(["cls", "tier", "meta", "box_h", "t_lo", "t_hi", "tc", "p2", "p1", "p1_t0", "sigma", "ecl", "phase", "wp", "ws", "star"]);
ok(deck.sessions.length === 8 && deck.sessions.every((x) => x.length === 20), "the deck has 8 sessions of 20 items");
const comp = (x) => Object.fromEntries(deck.classes.map((c) => [c, x.filter((i) => i.cls === c).length]));
ok(deck.sessions.every((x) => { const c = comp(x); return c.planet === 6 && c.eclipse === 3 && c.instrument === 3 && c.flare === 2 && c.step === 2 && c.noise === 4 && x.filter((i) => i.tier === "clear").length === 3 && x.filter((i) => i.tier === "near").length === 3; }), "every session: 3 clear and 3 near-limit fake planets, 3 eclipses, 3 instrument, 2 flares, 2 steps, 4 nothing-hidden");
const all = [].concat(...deck.sessions);
ok(all.every((i) => Object.keys(i).every((k) => KEYS.has(k))), "no item carries a field outside the allowed list (no TIC, no sector, no time stamp)");
ok(all.every((i) => i.p2.length === Math.round((i.t_hi - i.t_lo) * 240) && i.p1.length === 672 && i.sigma > 0 && GRID.includes(i.box_h) && i.phase >= 0 && i.phase <= 1), "arrays have the length the window says; box lengths are the hunt's grid");
const ids = new Set(all.map((i) => i.star)); ok(ids.size >= 60, `the deck holds ${ids.size} different star-sectors`);
ok(all.every((i) => i.cls !== "planet" || (i.meta.depth_ppm > 0 && i.meta.strength >= 6 && i.meta.box_h === i.box_h)) && all.filter((i) => i.tier === "clear").every((i) => i.meta.strength >= 13) && all.filter((i) => i.tier === "near").every((i) => i.meta.strength < 10), "fake planets carry their depth; clear ones are strong (13 or more), near-limit ones are under 10");
ok(fs.statSync(DECK).size < 1.6e6, `the deck is ${(fs.statSync(DECK).size / 1e6).toFixed(2)} MB (limit 1.6)`);
// mutation: a pass line that ignores false alarms must be caught by the test above
const naive = (rounds) => R.passLine(rounds).clear.rate >= 0.8;
ok(naive(DAYS.map((d) => round(d, { faCalls: 14 }))) === true && R.passLine(DAYS.map((d) => round(d, { faCalls: 14 }))).verdict === "below", "mutation: a line looking only at fake planets found would pass a player who calls everything a planet; the real line does not");
console.log(`\nall ${n} rehearsal checks passed`);
