/* Eyes mode core: pure logic, no DOM. Browser: window.SSEyes (used by demos.js). Node: module.exports (tested by book/tools/test_eyes.mjs).
   Holds the things that must never be wrong: how an answer is scored, what the truth banner says, what is saved after every answer,
   how the official test is composed and how the pass line is computed. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api; else root.SSEyes = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  const SCHEMA = 1, KEY = "ss-eyes-v1", FAINT = "dip1500";
  const NAME = { dip: "Dip", none: "No dip", odd: "Odd", unsure: "Not sure" };
  const PASS = { clearHit: 0.85, falseAlarm: 0.10, minCurves: 60, minRounds: 2, minDays: 2 };   // agreed with Ahmed, 23 Oct 2026
  const TEST_N = 30;

  // ---- what a card truly is, in plain words ----
  const WHAT = {
    real: "the real planet TOI-1338 b crossing",
    dip: "a hidden fake planet",
    quiet: "nothing hidden: a quiet stretch",
    eclipse: "an eclipse: one star passing in front of the other",
    spike: "a short spike upwards, like a flare or a glitch",
    step: "a sudden jump that stays, like an instrument glitch",
  };
  const baseKind = (k) => (String(k).startsWith("dip") ? "dip" : k);
  const isDip = (card) => card.truth === "dip";
  const isFaint = (card) => card.kind === FAINT;

  function truthOf(card) {
    const dip = isDip(card);
    return { dip, headline: dip ? "A DIP" : "NOT A DIP", what: WHAT[baseKind(card.kind)] || "something we hid", detail: card.note || "" };
  }

  // Score one answer. ok = exactly right (4 answers); bin = right about dip versus not a dip (null if "not sure").
  function verdict(ans, card) {
    const t = truthOf(card);
    if (ans === "unsure") return { result: "unsure", ok: false, bin: null };
    const ok = ans === card.truth, bin = (ans === "dip") === t.dip;
    return { result: ok ? "right" : bin ? "partial" : "wrong", ok, bin };
  }

  // The words shown after an answer: always says what it truly was, never only "you were wrong".
  function bannerParts(card, ans) {
    const t = truthOf(card), v = verdict(ans, card);
    let line;
    if (v.result === "right") line = `You said "${NAME[ans]}": right ✓`;
    else if (v.result === "partial") line = `You said "${NAME[ans]}": you were right that it is not a dip, but it is "${NAME[card.truth]}"`;
    else if (v.result === "wrong") line = `You said "${NAME[ans]}": not quite ✗`;
    else line = `You said "Not sure". That is an honest answer.`;
    return { cls: v.result, headline: `THIS WAS: ${t.headline}`, what: `It was ${t.what}.`, line, detail: t.detail };
  }

  // ---- composing a round ----
  function shuffle(a, rnd) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  function compose(mode, n, rnd) {
    const pick = (arr) => arr[Math.floor(rnd() * arr.length)], specs = [];
    if (mode === "test") {                                        // fixed: 10 clear dips, 4 faint, 8 quiet, 8 odd
      specs.push({ kind: "real" });
      [2500, 2500, 2500, 2500, 2500, 4000, 4000, 4000, 4000].forEach((depth) => specs.push({ kind: "dip", depth }));
      for (let i = 0; i < 4; i++) specs.push({ kind: "dip", depth: 1500 });
      for (let i = 0; i < 8; i++) specs.push({ kind: "quiet" });
      for (let i = 0; i < 4; i++) specs.push({ kind: "eclipse" });
      ["spike", "spike", "step", "step"].forEach((kind) => specs.push({ kind }));
      return shuffle(specs, rnd);
    }
    const real = n >= 20 ? 1 : 0, e = Math.max(1, Math.round(0.15 * n)), o = Math.max(1, Math.round(0.15 * n));
    const dp = Math.max(1, Math.round(0.3 * n) - real), q = Math.max(1, n - real - e - o - dp);
    for (let i = 0; i < real; i++) specs.push({ kind: "real" });
    for (let i = 0; i < e; i++) specs.push({ kind: "eclipse" });
    for (let i = 0; i < o; i++) specs.push({ kind: pick(["spike", "step"]) });
    for (let i = 0; i < dp; i++) specs.push({ kind: "dip", depth: pick([1500, 2500, 4000]) });
    for (let i = 0; i < q; i++) specs.push({ kind: "quiet" });
    return shuffle(specs.slice(0, n).concat(Array(Math.max(0, n - specs.length)).fill({ kind: "quiet" })), rnd);
  }

  // ---- summaries (one scoring code for the live screen, the history and, later, the cloud) ----
  function summarize(entries) {
    const s = { n: entries.length, right: 0, wrong: 0, unsure: 0, partial: 0, dips: 0, dipsFound: 0, clear: 0, clearFound: 0, faint: 0, faintFound: 0,
                quiet: 0, falseAlarms: 0, odd: 0, oddSpotted: 0, oddCalledDip: 0, lookedBack: 0 };
    for (const e of entries) {
      const dip = e.truth === "dip", faint = e.kind === FAINT;
      if (e.ans === "unsure") s.unsure++; else if (e.ok) s.right++; else { s.wrong++; if (e.bin) s.partial++; }
      if (e.lb) s.lookedBack++;
      if (dip) { s.dips++; if (e.ans === "dip") s.dipsFound++; if (faint) { s.faint++; if (e.ans === "dip") s.faintFound++; } else { s.clear++; if (e.ans === "dip") s.clearFound++; } }
      if (e.truth === "none") { s.quiet++; if (e.ans === "dip") s.falseAlarms++; }
      if (e.truth === "odd") { s.odd++; if (e.ok) s.oddSpotted++; if (e.ans === "dip") s.oddCalledDip++; }
    }
    return s;
  }
  function summaryLines(s) {
    const L = [`You looked at ${s.n} light curves: ${s.right} right, ${s.wrong} wrong, ${s.unsure} not sure.`];
    if (s.dips) L.push(`Dips hidden in them: you found ${s.dipsFound} of ${s.dips}${s.faint ? ` (the faintest: ${s.faintFound} of ${s.faint})` : ""}.`);
    if (s.quiet) L.push(`Quiet curves: you called ${s.falseAlarms} of ${s.quiet} a dip (a false alarm).`);
    if (s.odd) L.push(`Odd things (eclipses, spikes, jumps): you spotted ${s.oddSpotted} of ${s.odd}${s.oddCalledDip ? `, and called ${s.oddCalledDip} of them a dip` : ""}.`);
    if (s.partial) L.push(`${s.partial} of your wrong answers were right about "not a dip" but named the wrong kind.`);
    if (s.unsure) L.push("Saying not sure is an honest answer.");
    return L;
  }

  // ---- the pass line (Standard, agreed with Ahmed): at least 85% of the clear dips found and at most 1 in 10 quiet curves called a dip,
  //      over at least 60 test curves, in at least 2 rounds, on at least 2 different days. Faint dips are reported, not required. ----
  function wilson(k, n, z = 1.96) {
    if (!n) return [0, 1];
    const p = k / n, d = 1 + z * z / n, c = p + z * z / (2 * n), m = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n));
    return [Math.max(0, (c - m) / d), Math.min(1, (c + m) / d)];
  }
  const pad = (x) => String(x).padStart(2, "0");
  const localDay = (t) => { const d = new Date(t); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };
  const fmtDate = (t) => { const d = new Date(t); return `${localDay(t)} ${pad(d.getHours())}:${pad(d.getMinutes())}`; };
  const pc = (x) => `${Math.round(100 * x)}%`;

  function passLine(rounds) {
    const done = rounds.filter((r) => r.mode === "test" && r.status === "done" && r.a.length === r.n);
    const entries = done.flatMap((r) => r.a), s = summarize(entries);
    const days = new Set(done.map((r) => localDay(r.t0))).size;
    const clear = { n: s.clear, k: s.clearFound, rate: s.clear ? s.clearFound / s.clear : 0, range: wilson(s.clearFound, s.clear) };
    const faint = { n: s.faint, k: s.faintFound, rate: s.faint ? s.faintFound / s.faint : 0, range: wilson(s.faintFound, s.faint) };
    const quiet = { n: s.quiet, k: s.falseAlarms, rate: s.quiet ? s.falseAlarms / s.quiet : 0, range: wilson(s.falseAlarms, s.quiet) };
    const needs = [];
    if (done.length < PASS.minRounds) needs.push(`${PASS.minRounds - done.length} more test round(s)`);
    if (s.n < PASS.minCurves && done.length >= PASS.minRounds) needs.push(`${PASS.minCurves - s.n} more curves`);
    if (days < PASS.minDays) needs.push("a test on a different day");
    const enough = needs.length === 0;
    const meets = s.clear > 0 && clear.rate >= PASS.clearHit && s.quiet > 0 && quiet.rate <= PASS.falseAlarm;
    const verdictWord = !enough ? "not_enough" : meets ? "meets" : "below";
    const lines = [];
    lines.push(`Test rounds: ${done.length}, curves: ${s.n}, days: ${days}.`);
    if (s.clear) lines.push(`Clear dips found: ${s.clearFound} of ${s.clear} (${pc(clear.rate)}; 95% range ${pc(clear.range[0])} to ${pc(clear.range[1])}). Line: at least ${pc(PASS.clearHit)}.`);
    if (s.faint) lines.push(`Faintest dips (reported, not in the line): ${s.faintFound} of ${s.faint}.`);
    if (s.quiet) lines.push(`Quiet curves called a dip: ${s.falseAlarms} of ${s.quiet} (${pc(quiet.rate)}; 95% range ${pc(quiet.range[0])} to ${pc(quiet.range[1])}). Line: at most ${pc(PASS.falseAlarm)}.`);
    if (s.oddCalledDip) lines.push(`Eclipses, spikes and jumps called a dip: ${s.oddCalledDip} of ${s.odd}.`);
    lines.push(verdictWord === "not_enough" ? `Not enough yet: still needs ${needs.join(", ")}.`
      : verdictWord === "meets" ? "On the numbers you meet the line. Claude decides whether that is enough." : "Below the line on the numbers so far. Keep practising.");
    return { rounds: done.length, curves: s.n, days, clear, faint, quiet, oddCalledDip: s.oddCalledDip, odd: s.odd, enough, meets, verdict: verdictWord, needs, lines };
  }

  // ---- the store: everything is written to the device after EVERY answer ----
  function createStore(storage, opts = {}) {
    const now = opts.now || (() => Date.now()), rid = opts.rid || (() => Math.random().toString(36).slice(2, 8));
    const listeners = [];
    let lastError = null, db;

    function fresh() { return { v: SCHEMA, device: { id: rid(), label: "" }, rounds: [] }; }
    function load() {
      let raw = null;
      try { raw = storage.getItem(KEY); } catch (e) { return fresh(); }
      if (raw == null) return fresh();
      try {
        const s = JSON.parse(raw);
        if (s && s.v === SCHEMA && Array.isArray(s.rounds) && s.device) return s;
      } catch (e) { /* fall through */ }
      try { storage.setItem(`${KEY}-unreadable-${now()}`, raw); } catch (e) { /* nothing more we can do */ }   // never silently overwrite data we could not read
      return fresh();
    }
    db = load();
    function save(event, round) {
      try { storage.setItem(KEY, JSON.stringify(db)); lastError = null; }
      catch (e) { lastError = String((e && e.name) || e); }
      if (!lastError) listeners.forEach((f) => { try { f(event, round); } catch (e) { /* a listener must never break saving */ } });
      return !lastError;
    }
    const find = (id) => db.rounds.find((r) => r.id === id);
    const api = {
      get lastError() { return lastError; },
      get device() { return db.device; },
      onChange(f) { listeners.push(f); },
      setLabel(label) { db.device.label = String(label || "").slice(0, 40); return save("label"); },
      startRound({ mode, source, n }) {
        const t0 = now();
        const r = { id: `${db.device.id}-${t0.toString(36)}-${rid()}`, v: SCHEMA, mode, source, n, t0, t1: null, status: "open", sync: 0, a: [], s: null };
        db.rounds.push(r); save("start", r); return r;
      },
      // Records the answer to question i. Refuses anything but the next unanswered question of an open round: an answer can never be changed.
      recordAnswer(id, i, card, ans, ms) {
        const r = find(id);
        if (!r || r.status !== "open" || i !== r.a.length || !NAME[ans]) return null;
        const v = verdict(ans, card);
        const e = { i, kind: card.kind, truth: card.truth, ans, ok: v.ok, bin: v.bin, ms: Math.round(ms || 0), lb: 0, m: card.meta || null };
        r.a.push(e); r.s = summarize(r.a); save("answer", r); return e;
      },
      noteLookBack(id, i) {                                       // only counts looks during an open round; never touches the answer
        const r = find(id);
        if (!r || r.status !== "open" || !r.a[i]) return false;
        r.a[i].lb += 1; r.s = summarize(r.a); return save("lookback", r);
      },
      finishRound(id) {
        const r = find(id);
        if (!r || r.status !== "open") return null;
        r.status = "done"; r.t1 = now(); r.s = summarize(r.a); save("finish", r); return r;
      },
      markSynced(id) {                                            // the cloud has this round (never for a round still open)
        const r = find(id);
        if (!r || r.status === "open") return false;
        r.sync = 1; r.syncAt = now(); return save("sync", r);
      },
      // A round left open from an earlier page visit is closed as "abandoned" (kept, with its answers); an empty one is dropped.
      recoverOpen() {
        let changed = 0;
        for (const r of db.rounds.slice()) {
          if (r.status !== "open") continue;
          changed++;
          if (!r.a.length) db.rounds.splice(db.rounds.indexOf(r), 1);
          else { r.status = "abandoned"; r.t1 = now(); r.s = summarize(r.a); }
        }
        if (changed) save("recover");
        return changed;
      },
      rounds() { return db.rounds.slice().reverse(); },
      round(id) { return find(id) || null; },
      unsynced() { return db.rounds.filter((r) => r.status !== "open" && !r.sync); },
      exportJSON() { return JSON.stringify({ schema: SCHEMA, device: db.device, exported: now(), rounds: db.rounds }); },
      approxBytes() { try { return JSON.stringify(db).length; } catch (e) { return 0; } },
    };
    return api;
  }

  // ---- the cloud document: its shape is fixed by the published Firestore rules (only these keys; create once, never change) ----
  const CLOUD_KEYS = ["v", "id", "mode", "source", "n", "t0", "t1", "status", "device", "a", "s"];
  function roundDoc(r, device) {
    return { v: r.v, id: r.id, mode: r.mode, source: r.source, n: r.n, t0: r.t0, t1: r.t1, status: r.status,
             device: { id: device.id, label: device.label || "" }, a: r.a, s: r.s || summarize(r.a) };
  }
  function encodeValue(v) {                                       // Firestore REST typed values
    if (v === null || v === undefined || (typeof v === "number" && !Number.isFinite(v))) return { nullValue: null };
    if (typeof v === "boolean") return { booleanValue: v };
    if (typeof v === "number") return Number.isInteger(v) ? { integerValue: String(v) } : { doubleValue: v };
    if (typeof v === "string") return { stringValue: v };
    if (Array.isArray(v)) return { arrayValue: { values: v.map(encodeValue) } };
    const fields = {}; for (const k of Object.keys(v)) fields[k] = encodeValue(v[k]);
    return { mapValue: { fields } };
  }
  function decodeValue(v) {
    const t = Object.keys(v)[0], x = v[t];
    if (t === "nullValue") return null;
    if (t === "integerValue") return Number(x);
    if (t === "arrayValue") return (x.values || []).map(decodeValue);
    if (t === "mapValue") { const o = {}; for (const k of Object.keys(x.fields || {})) o[k] = decodeValue(x.fields[k]); return o; }
    return x;
  }
  function toFirestoreBody(r, device) {
    const d = roundDoc(r, device), fields = {};
    for (const k of CLOUD_KEYS) fields[k] = encodeValue(d[k]);
    return { fields };
  }

  return { SCHEMA, KEY, NAME, PASS, TEST_N, FAINT, CLOUD_KEYS, truthOf, verdict, bannerParts, compose, summarize, summaryLines, wilson, passLine, createStore, localDay, fmtDate, shuffle, roundDoc, encodeValue, decodeValue, toFirestoreBody };
});
