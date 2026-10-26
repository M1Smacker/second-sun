// Unit tests for the Eyes cloud uploader (book/docs/assets/eyes-cloud.js) with a fake network and fake timers. Usage: node book/tools/test_eyes_cloud.mjs
// Targets what must never go wrong: a round lost, a round sent twice, an open round sent, a refused round blocking the others, a loop of retries.
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url)), req = createRequire(import.meta.url);
const core = req(path.join(here, "..", "docs", "assets", "eyes-core.js"));
const cloud = req(process.env.EYES_CLOUD || path.join(here, "..", "docs", "assets", "eyes-cloud.js"));

class Storage { constructor() { this.m = new Map(); } getItem(k) { return this.m.has(k) ? this.m.get(k) : null; } setItem(k, v) { this.m.set(k, String(v)); } }
const CARDS = { clear: { kind: "dip2500", truth: "dip", note: "n", meta: { w: 1 } }, quiet: { kind: "quiet", truth: "none", note: "n", meta: { w: 2 } } };
function finishedRound(store, n = 2, mode = "practice") {
  const r = store.startRound({ mode, source: "practice-toi1338-s98", n });
  for (let i = 0; i < n; i++) store.recordAnswer(r.id, i, i % 2 ? CARDS.clear : CARDS.quiet, i % 2 ? "dip" : "none", 900);
  return store.finishRound(r.id);
}
// the published rules, re-implemented, so a payload the real Firestore would refuse fails here first
function rulesAllow(body, docId) {
  const f = body.fields, keys = Object.keys(f).sort();
  const ok = JSON.stringify(keys) === JSON.stringify(["a", "device", "id", "mode", "n", "s", "source", "status", "t0", "t1", "v"]);
  return ok && f.v.integerValue === "1" && f.id.stringValue === docId && ["practice", "test", "real"].includes(f.mode.stringValue)
    && f.n.integerValue !== undefined && Number(f.n.integerValue) <= 200 && f.a.arrayValue !== undefined && (f.a.arrayValue.values || []).length <= 200;
}
function harness({ online = true, script = [] } = {}) {
  const store = core.createStore(new Storage(), { rid: (() => { let i = 0; return () => "id" + ++i; })() });
  const net = { online, calls: [], script: script.slice(), server: new Set() };
  const timers = []; let nextT = 1;
  const fetch = async (url, init) => {
    const docId = new URL(url).searchParams.get("documentId"), body = JSON.parse(init.body);
    net.calls.push({ url, docId, body, method: init.method });
    const step = net.script.shift();
    if (step === "throw") throw new Error("network down");
    if (step === "lost") { net.server.add(docId); throw new Error("response lost after the server stored it"); }
    if (typeof step === "number") return { status: step };
    if (net.refuseN && body.fields.n.integerValue === net.refuseN) return { status: 403 };   // the server always refuses rounds of this length
    if (!rulesAllow(body, docId)) return { status: 403 };
    if (net.server.has(docId)) return { status: 409 };
    net.server.add(docId); return { status: 200 };
  };
  const up = cloud.createUploader({ store, core, fetch, isOnline: () => net.online, timeoutMs: 0,
    setTimer: (f, ms) => { const id = nextT++; timers.push({ id, f, ms }); return id; }, clearTimer: (id) => { const i = timers.findIndex((t) => t.id === id); if (i >= 0) timers.splice(i, 1); } });
  store.onChange((ev) => { if (ev === "finish" || ev === "recover") up.flush(); });
  const fire = async () => { const t = timers.shift(); if (t) { await t.f(); } return t && t.ms; };
  return { store, net, up, timers, fire };
}
const settle = () => new Promise((r) => setImmediate(r));
let passed = 0;
const test = async (name, fn) => { await fn(); passed++; console.log("pass:", name); };

await test("a finished round is sent once, in the shape the rules accept, and marked as synced", async () => {
  const h = harness(); finishedRound(h.store); await settle(); await settle();
  assert.equal(h.net.calls.length, 1);
  const c = h.net.calls[0];
  assert.equal(c.method, "POST");
  assert.match(c.url, /^https:\/\/firestore\.googleapis\.com\/v1\/projects\/second-sun-faea5\/databases\/\(default\)\/documents\/eyes_rounds\?documentId=/);
  assert.ok(c.url.includes("&key="), "public key attached");
  assert.ok(rulesAllow(c.body, c.docId));
  assert.equal(h.store.unsynced().length, 0);
  assert.match(h.up.status(), /all 1 finished round\(s\) are safe in the cloud/);
});

await test("a round still open is never sent; sending starts the moment it finishes", async () => {
  const h = harness(); const r = h.store.startRound({ mode: "test", source: "s", n: 2 });
  h.store.recordAnswer(r.id, 0, CARDS.quiet, "none", 1); await h.up.flush(); await settle();
  assert.equal(h.net.calls.length, 0);
  h.store.recordAnswer(r.id, 1, CARDS.clear, "dip", 1); await settle();
  assert.equal(h.net.calls.length, 0, "answering must not send");
  h.store.finishRound(r.id); await settle(); await settle();
  assert.equal(h.net.calls.length, 1);
});

await test("offline: the round waits, nothing is lost, and it goes out when the internet returns", async () => {
  const h = harness({ online: false }); finishedRound(h.store); await settle();
  assert.equal(h.net.calls.length, 0);
  assert.equal(h.store.unsynced().length, 1);
  assert.match(h.up.status(), /1 round\(s\) waiting for the internet. They will send themselves/);
  assert.equal(h.timers.length, 1, "a retry is scheduled");
  h.net.online = true; await h.up.flush(); await settle();
  assert.equal(h.net.calls.length, 1); assert.equal(h.store.unsynced().length, 0);
});

await test("network errors back off 5 s, 15 s, 60 s, 5 min and then recover without losing the round", async () => {
  const h = harness({ script: ["throw", "throw", "throw", "throw", "throw"] }); finishedRound(h.store); await settle(); await settle();
  const delays = [h.timers[0].ms];
  for (let i = 0; i < 4; i++) { await h.fire(); await settle(); await settle(); delays.push(h.timers[0] ? h.timers[0].ms : null); }
  assert.deepEqual(delays.slice(0, 5), [5000, 15000, 60000, 300000, 300000]);
  assert.equal(h.store.unsynced().length, 1);
  await h.fire(); await settle(); await settle();
  assert.equal(h.store.unsynced().length, 0, "the sixth attempt succeeds");
});

await test("no duplicates: if the cloud stored a round but the answer was lost, the resend gets 409 and counts as stored", async () => {
  const h = harness({ script: ["lost"] }); finishedRound(h.store); await settle(); await settle();
  assert.equal(h.store.unsynced().length, 1);
  await h.fire(); await settle(); await settle();
  assert.equal(h.net.calls.length, 2); assert.equal(h.net.calls[1].docId, h.net.calls[0].docId);
  assert.equal(h.store.unsynced().length, 0);
  assert.equal(h.net.server.size, 1, "one document on the server");
});

await test("a refused round (403) stays queued, does not block the others, and is retried slowly", async () => {
  const h = harness(); h.net.refuseN = "2"; const a = finishedRound(h.store, 2); await settle(); await settle();
  const b = finishedRound(h.store, 4); await settle(); await settle();
  assert.equal(h.store.round(a.id).sync || 0, 0, "refused round not marked");
  assert.equal(h.store.round(b.id).sync, 1, "the next round still went through");
  assert.match(h.up.status(), /1 round\(s\) could not be sent yet/);
  assert.equal(h.timers.at(-1).ms, 600000);
});

await test("busy or down server (429, 503) is treated like being offline", async () => {
  const h = harness({ script: [429, 503] }); finishedRound(h.store); await settle(); await settle();
  assert.equal(h.store.unsynced().length, 1); assert.equal(h.up.state, "offline");
  await h.fire(); await settle(); await settle(); assert.equal(h.store.unsynced().length, 1);
  await h.fire(); await settle(); await settle(); assert.equal(h.store.unsynced().length, 0);
});

await test("calling flush many times at once sends each round once", async () => {
  const h = harness(); finishedRound(h.store);
  await Promise.all([h.up.flush(), h.up.flush(), h.up.flush(), h.up.flush()]); await settle(); await settle();
  assert.equal(h.net.calls.length, 1);
});

await test("several rounds waiting go out oldest first, and abandoned rounds are sent too", async () => {
  const h = harness({ online: false });
  const a = finishedRound(h.store, 2), b = finishedRound(h.store, 3);
  const half = h.store.startRound({ mode: "practice", source: "s", n: 5 }); h.store.recordAnswer(half.id, 0, CARDS.clear, "dip", 1);
  h.store.recoverOpen(); await settle();
  assert.equal(h.store.unsynced().length, 3);
  h.net.online = true; await h.up.flush(); await settle(); await settle();
  assert.equal(h.store.unsynced().length, 0);
  assert.deepEqual(h.net.calls.map((c) => c.docId), [a.id, b.id, half.id].sort((x, y) => h.store.round(x).t0 - h.store.round(y).t0 || (x < y ? -1 : 1)));
  assert.equal(h.net.calls.find((c) => c.docId === half.id).body.fields.status.stringValue, "abandoned");
});

await test("syncing does not trigger more sending (no loop), and the status listener hears every change", async () => {
  const h = harness(), heard = []; h.up.onStatus((s) => heard.push(s)); finishedRound(h.store); await settle(); await settle(); await settle();
  assert.equal(h.net.calls.length, 1);
  assert.ok(heard.some((s) => /sending/.test(s)) && /safe in the cloud/.test(heard.at(-1)));
});

await test("a paused uploader (a test copy of the book) never sends anything, whatever happens", async () => {
  const store = core.createStore(new Storage()), calls = [];
  const up = cloud.createUploader({ store, core, fetch: async (u) => { calls.push(u); return { status: 200 }; }, paused: true, timeoutMs: 0, setTimer: () => 1, clearTimer: () => {} });
  store.onChange((ev) => { if (ev === "finish") up.flush(); });
  finishedRound(store); await up.flush(); await settle(); await settle();
  assert.equal(calls.length, 0);
  assert.equal(store.unsynced().length, 1, "the round stays on the device");
  assert.match(up.status(), /paused on this test copy of the book/);
});

await test("a visitor can play but nothing is ever sent, and the line says so", async () => {
  const store = core.createStore(new Storage()), calls = [];
  const up = cloud.createUploader({ store, core, fetch: async (u) => { calls.push(u); return { status: 200 }; }, guest: true, timeoutMs: 0, setTimer: () => 1, clearTimer: () => {} });
  store.onChange((ev) => { if (ev === "finish") up.flush(); });
  finishedRound(store); await up.flush(); await settle(); await settle();
  assert.equal(calls.length, 0);
  assert.equal(store.unsynced().length, 1, "the round stays on the device");
  assert.match(up.status(), /You are a visitor here, so nothing you do is sent anywhere/);
});

await test("who is an owner: a device with rounds before the rule, or the #owner link; a visitor stays a visitor even after playing", async () => {
  const win = (hash = "") => { const m = new Map(), w = { hash, replaced: null }; return { localStorage: { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)) },
    location: { hash, pathname: "/second-sun/eyes/", search: "" }, history: { replaceState: (a, b, u) => { w.replaced = u; } }, w, m }; };
  const withRounds = core.createStore(new Storage()); finishedRound(withRounds);
  const empty = () => core.createStore(new Storage());
  let a = win(); assert.equal(cloud.isOwner(withRounds, a), true, "a device that already has rounds is Ahmed's"); assert.equal(a.m.get("ss-eyes-owner"), "1");
  let b = win(); assert.equal(cloud.isOwner(empty(), b), false, "a new device is a visitor"); assert.equal(b.m.get("ss-eyes-owner"), "0");
  assert.equal(cloud.isOwner(withRounds, b), false, "the first decision sticks: playing does not make a visitor the owner");
  let c = win("#owner"); assert.equal(cloud.isOwner(empty(), c), true, "the link makes a new device his"); assert.equal(c.m.get("ss-eyes-owner"), "1"); assert.equal(c.w.replaced, "/second-sun/eyes/", "the hash is removed");
  let d = win(); d.m.set("ss-eyes-owner", "0"); d.location.hash = "#owner"; assert.equal(cloud.isOwner(empty(), d), true, "the link overrides an earlier visitor decision");
  const broken = { localStorage: { getItem() { throw new Error("blocked"); }, setItem() { throw new Error("blocked"); } }, location: { hash: "" } };
  assert.equal(cloud.isOwner(empty(), broken), false, "no usable storage: treated as a visitor");
});

await test("the status line is honest before any round exists", async () => {
  const h = harness(); assert.match(h.up.status(), /Cloud backup is on\. Each finished round is sent by itself/);
});

console.log(`all ${passed} Eyes cloud checks passed`);
