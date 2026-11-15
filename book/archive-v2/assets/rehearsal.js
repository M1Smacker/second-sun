/* Rehearsal in the real layout (rung 3 of the Eyes ladder; research/stage3/REHEARSAL-V1.md; 2 Nov 2026). Pure logic first (tested by book/tools/test_rehearsal.mjs), then the page.
   Items are windows of real TESS light with at most one hidden thing planted in them (assets/rehearsal-deck.json, made by pipeline/make_rehearsal_deck.py). Three panels as in the
   vetting brief: P1 the whole sector, P2 the event up close, P3 where the event falls in the binary's orbit. Six answers. You lock an answer, then the truth is shown.
   Rounds are saved on this device after every answer and sent to the private cloud like the other Eyes rounds (mode "practice", source "rehearsal-v1"). Browser: window.SSRehearsal. */
(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api; else { root.SSRehearsal = api; api.boot(); }
})(typeof self !== "undefined" ? self : this, function (root) {
  "use strict";
  const KEY = "ss-rehearsal-v1", SOURCE = "rehearsal-v1", SESSIONS = 8, SCHEMA = 1;
  const LABEL = { planet: "Planet-like", eclipse: "Eclipse", flare: "Flare", instrument: "Instrumental", step: "Step", noise: "Unclear" };
  const BUTTONS = ["planet", "eclipse", "flare", "instrument", "step", "noise"];       // two rows of three
  const PASS = { sessions: 8, days: 4, clear: 0.8, falseAlarm: 0.15, dprime: 2 };      // research/decisions.md, ladder step 3
  const CONF = ["low", "medium", "high"];

  // ---------- statistics ----------
  function wilson(k, n, z = 1.96) {
    if (!n) return [0, 1];
    const p = k / n, d = 1 + z * z / n, c = p + z * z / (2 * n), s = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n));
    return [Math.max(0, (c - s) / d), Math.min(1, (c + s) / d)];
  }
  function probit(p) {                                         // inverse normal (Abramowitz and Stegun 26.2.23), good to about 4.5e-4
    const q = p < 0.5 ? p : 1 - p, t = Math.sqrt(-2 * Math.log(q));
    const x = t - (2.515517 + 0.802853 * t + 0.010328 * t * t) / (1 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t * t * t);
    return p < 0.5 ? -x : x;
  }
  // d' = z(hit rate) - z(false-alarm rate), with the +0.5 / +1 correction so a rate of 0 or 1 stays finite
  function dprime(hk, hn, fk, fn) {
    if (!hn || !fn) return null;
    return probit((hk + 0.5) / (hn + 1)) - probit((fk + 0.5) / (fn + 1));
  }

  // ---------- answers and scores ----------
  const isPlanetCall = (ans) => ans === "planet";
  function entryOf(i, item, ans, conf, ms) {
    return { i, cls: item.cls, tier: item.tier || null, ans, ok: ans === item.cls, pc: isPlanetCall(ans), conf: conf || null, ms: Math.round(ms || 0), st: item.meta && item.meta.strength != null ? item.meta.strength : null, bx: item.box_h };
  }
  function summaryOf(entries) {
    const pl = entries.filter((e) => e.cls === "planet"), cl = pl.filter((e) => e.tier === "clear"), nr = pl.filter((e) => e.tier === "near"), no = entries.filter((e) => e.cls !== "planet");
    const cnt = (xs) => xs.filter((e) => e.pc).length;
    const byClass = {};
    for (const e of entries) { const b = byClass[e.cls] || (byClass[e.cls] = { n: 0, right: 0 }); b.n++; b.right += e.ok ? 1 : 0; }
    return { n: entries.length, right: entries.filter((e) => e.ok).length, planets: pl.length, planetsHit: cnt(pl), clear: cl.length, clearHit: cnt(cl), near: nr.length, nearHit: cnt(nr), others: no.length, othersCalledPlanet: cnt(no), byClass };
  }
  const pc = (x) => `${Math.round(100 * x)}%`;
  const pad = (x) => String(x).padStart(2, "0");
  const localDay = (t) => { const d = new Date(t); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };
  // The pass line over every finished session (decided before it was played: research/decisions.md, ladder step 3). Claude decides whether it is enough; this is the arithmetic.
  function passLine(rounds) {
    const done = rounds.filter((r) => r.status === "done"), all = [].concat(...done.map((r) => r.a));
    const s = summaryOf(all), days = new Set(done.map((r) => localDay(r.t0))).size;
    const clear = { k: s.clearHit, n: s.clear, rate: s.clear ? s.clearHit / s.clear : 0, range: wilson(s.clearHit, s.clear) };
    const fa = { k: s.othersCalledPlanet, n: s.others, rate: s.others ? s.othersCalledPlanet / s.others : 0, range: wilson(s.othersCalledPlanet, s.others) };
    const d = dprime(s.planetsHit, s.planets, s.othersCalledPlanet, s.others);
    const needs = [];
    if (done.length < PASS.sessions) needs.push(`${PASS.sessions - done.length} more session(s)`);
    if (days < PASS.days) needs.push(`${PASS.days - days} more calendar day(s)`);
    const enough = !needs.length;
    const meets = clear.rate >= PASS.clear && fa.rate <= PASS.falseAlarm && d !== null && d >= PASS.dprime;
    const verdict = !enough ? "not_enough" : meets ? "meets" : "below";
    const lines = [`Sessions ${done.length} of ${PASS.sessions}, on ${days} different day(s) (need ${PASS.days}).`,
      `Clearly visible fake planets found: ${clear.k} of ${clear.n}${clear.n ? ` (${pc(clear.rate)}; 95% range ${pc(clear.range[0])} to ${pc(clear.range[1])})` : ""}. Line: at least ${pc(PASS.clear)}.`,
      `Not-planets called planet-like: ${fa.k} of ${fa.n}${fa.n ? ` (${pc(fa.rate)}; 95% range ${pc(fa.range[0])} to ${pc(fa.range[1])})` : ""}. Line: at most ${pc(PASS.falseAlarm)}.`,
      `Fakes near the limit found: ${s.nearHit} of ${s.near} (reported, not in the line).`,
      `d-prime: ${d === null ? "not measured yet" : d.toFixed(2)}. Line: at least ${PASS.dprime}.`,
      verdict === "not_enough" ? `Practice result, not an official pass: still needs ${needs.join(" and ")}.` : verdict === "meets" ? "On the numbers you meet the line. Claude decides whether that is enough." : "Below the line on the numbers so far. Keep practising."];
    return { sessions: done.length, days, clear, fa, near: { k: s.nearHit, n: s.near }, dprime: d, enough, meets, verdict, needs, lines, summary: s };
  }
  const nextSession = (rounds) => rounds.filter((r) => r.status === "done").length % SESSIONS;

  // never two neighbouring items from one star-sector (best effort; a deck always has far more stars than that needs)
  function orderSession(items, rnd) {
    let out = [];
    for (let attempt = 0; attempt < 60; attempt++) {              // random picks that skip the previous star; retried if the last picks are boxed in
      const pool = items.slice(); out = [];
      while (pool.length) {
        const okIdx = pool.map((x, i) => i).filter((i) => !out.length || pool[i].star !== out[out.length - 1].star);
        const from = okIdx.length ? okIdx : pool.map((x, i) => i);
        out.push(pool.splice(from[Math.floor(rnd() * from.length)], 1)[0]);
      }
      let bad = 0; for (let i = 1; i < out.length; i++) if (out[i].star === out[i - 1].star) bad++;
      if (!bad) break;
    }
    return out;
  }

  function reveal(item, ans) {
    const m = item.meta || {}, right = ans === item.cls;
    const what = {
      planet: `A fake planet was hidden here: ${m.depth_ppm} ppm deep, lasting ${m.box_h} hours, strength ${m.strength} on the hunt's scale (the hunt keeps 7 and above). ${item.tier === "clear" ? "A clearly visible one." : "Near the limit, so it is fair to miss."}`,
      eclipse: `A real eclipse of this binary (${m.kind}), about ${m.depth_ppm} ppm deep. An eclipse is not a planet, but it can sit where a planet dip would.`,
      instrument: `An instrument effect was planted: ${m.kind}. The spacecraft does this next to data gaps. Not a planet.`,
      flare: `A flare: it brightens in minutes and fades slowly (peak ${m.amp_ppm} ppm). Read upside down it looks like a dip with a sharp start and a slow recovery.`,
      step: `A step: the level changes by ${m.step_ppm} ppm and stays changed. A planet's dip comes back to the same level.`,
      noise: `Nothing was hidden. This is the best wiggle the hunt's own search finds in another part of this sector (strength ${m.strength}). Noise can look like a dip.`,
    }[item.cls];
    const call = item.cls === "planet" ? (isPlanetCall(ans) ? "You called it planet-like: a hit." : "You did not call it planet-like: a miss.") : (isPlanetCall(ans) ? "You called it planet-like: a false alarm." : "You did not call it planet-like: correct.");
    return { right, headline: `THIS WAS: ${LABEL[item.cls].toUpperCase()}`, what, you: `You said ${LABEL[ans]}. ${right ? "Right." : "Not this time."}`, call };
  }

  // ---------- panels (pure string builders) ----------
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const med = (xs) => { const a = xs.filter((v) => v != null).sort((p, q) => p - q); return a.length ? a[Math.floor(a.length / 2)] : 0; };
  function path(xs, ys, W, H, nullGap) {                        // polyline segments broken at missing data; y already in pixels
    let d = "", pen = false;
    for (let i = 0; i < xs.length; i++) {
      if (ys[i] == null) { pen = false; continue; }
      d += (pen && !nullGap ? "L" : "M") + xs[i].toFixed(1) + " " + Math.max(0, Math.min(H, ys[i])).toFixed(1); pen = true;
    }
    return d;
  }
  function svgP1(item, W = 358, H = 96) {
    const p = item.p1, n = p.length, padL = 4, padR = 4, x = (d) => padL + (d / 28) * (W - padL - padR);
    const m = med(p), mad = med(p.filter((v) => v != null).map((v) => Math.abs(v - m))) * 1.4826 || 100, half = Math.max(6 * mad, 200);
    const y = (v) => v == null ? null : H / 2 - ((v - m) / half) * (H / 2 - 4);
    const xs = p.map((_, i) => x(i / 24)), ys = p.map(y);
    const ecl = (item.ecl || []).map(([a, b]) => `<rect x="${x(a).toFixed(1)}" y="0" width="${Math.max(2, x(b) - x(a)).toFixed(1)}" height="${H}" class="ss-rh-ecl"/>`).join("");
    const ev0 = x(item.tc - item.box_h / 48), ev1 = x(item.tc + item.box_h / 48);
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Panel 1: the whole sector of light, eclipses shaded, your event marked" class="ss-rh-svg">${ecl}<rect x="${ev0.toFixed(1)}" y="0" width="${Math.max(3, ev1 - ev0).toFixed(1)}" height="${H}" class="ss-rh-ev"/><line x1="${padL}" x2="${W - padR}" y1="${(H / 2).toFixed(1)}" y2="${(H / 2).toFixed(1)}" class="ss-rh-base"/><path d="${path(xs, ys, W, H)}" class="ss-rh-line"/></svg>`;
  }
  function svgP2(item, W = 358, H = 220) {
    const raw = item.p2, n = raw.length, step = 1 / 240, halfD = (item.t_hi - item.t_lo) / 2, halfH = halfD * 24, padL = 34, padR = 6, padT = 22, padB = 22;
    const x = (hrs) => padL + ((hrs + halfH) / (2 * halfH)) * (W - padL - padR);
    const base = med(raw), sg = item.sigma || 100, R = 8 * sg, y = (v) => v == null ? null : padT + (1 - ((v - base + R) / (2 * R))) * (H - padT - padB);
    const hrsAt = (i) => (i * step - halfD) * 24 + step * 12;
    const xs = raw.map((_, i) => x(hrsAt(i))), ys = raw.map(y);
    const bx = [], by = [];                                      // 30 minute bins of the 6 minute points
    for (let i = 0; i + 5 <= n; i += 5) { const v = raw.slice(i, i + 5).filter((q) => q != null); bx.push(x(hrsAt(i + 2))); by.push(v.length >= 3 ? y(v.reduce((a, c) => a + c, 0) / v.length) : null); }
    const tick = halfH > 30 ? 24 : 12, ticks = []; for (let h = -Math.floor(halfH / tick) * tick; h <= halfH; h += tick) ticks.push(h);
    const grid = ticks.map((h) => `<line x1="${x(h).toFixed(1)}" x2="${x(h).toFixed(1)}" y1="${padT}" y2="${H - padB}" class="ss-rh-grid"/><text x="${x(h).toFixed(1)}" y="${H - 6}" text-anchor="middle" class="ss-rh-tx">${h}</text>`).join("");
    const yb = y(base), band = `<rect x="${padL}" y="${y(base + sg).toFixed(1)}" width="${W - padL - padR}" height="${(y(base - sg) - y(base + sg)).toFixed(1)}" class="ss-rh-band"/>`;
    const b0 = x(-item.box_h / 2), b1 = x(item.box_h / 2);
    const yl = `<text x="${padL - 4}" y="${padT + 8}" text-anchor="end" class="ss-rh-tx">+${Math.round(R)}</text><text x="${padL - 4}" y="${H - padB}" text-anchor="end" class="ss-rh-tx">-${Math.round(R)}</text><text x="${padL - 4}" y="${yb.toFixed(1)}" text-anchor="end" class="ss-rh-tx">0</text>`;
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Panel 2: the event up close, hours from the middle on the bottom axis, parts per million up the side, the same scale for every item" class="ss-rh-svg">${band}${grid}<line x1="${padL}" x2="${W - padR}" y1="${yb.toFixed(1)}" y2="${yb.toFixed(1)}" class="ss-rh-base"/><path d="${path(xs, ys, W, H)}" class="ss-rh-raw"/><path d="${path(bx, by, W, H)}" class="ss-rh-line"/><path d="M${b0.toFixed(1)} 14V8H${b1.toFixed(1)}V14" class="ss-rh-br"/>${yl}</svg>`;
  }
  function svgP3(item, W = 358, H = 44) {
    const x = (ph) => 6 + ph * (W - 12), wp = item.wp, ws = item.ws;
    const zone = (a, b) => `<rect x="${x(Math.max(0, a)).toFixed(1)}" y="12" width="${Math.max(2, x(Math.min(1, b)) - x(Math.max(0, a))).toFixed(1)}" height="14" class="ss-rh-zone"/>`;
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Panel 3: where the event falls in the binary's orbit, with the eclipse zones shaded" class="ss-rh-svg"><line x1="6" x2="${W - 6}" y1="19" y2="19" class="ss-rh-base"/>${zone(0, wp / 2)}${zone(1 - wp / 2, 1)}${zone(0.5 - ws / 2, 0.5 + ws / 2)}<circle cx="${x(item.phase).toFixed(1)}" cy="19" r="6" class="ss-rh-dot"/><text x="6" y="40" class="ss-rh-tx">primary</text><text x="${x(0.5).toFixed(1)}" y="40" text-anchor="middle" class="ss-rh-tx">secondary</text><text x="${W - 6}" y="40" text-anchor="end" class="ss-rh-tx">primary</text></svg>`;
  }

  // ---------- the store: same shape as the Eyes store, own key ----------
  function createStore(storage, opts = {}) {
    const now = opts.now || (() => Date.now()), rid = opts.rid || (() => Math.random().toString(36).slice(2, 8)), listeners = [];
    let lastError = null, db;
    function mainDevice() {                                      // one device name across the Eyes pages when the ordinary Eyes store exists
      try { const m = root.SSEyes && JSON.parse(storage.getItem(root.SSEyes.KEY)); if (m && m.device && m.device.id) return { id: m.device.id, label: m.device.label || "" }; } catch (e) { /* none */ }
      return null;
    }
    const fresh = () => ({ v: SCHEMA, device: mainDevice() || { id: rid(), label: "" }, rounds: [] });
    function load() {
      let raw = null;
      try { raw = storage.getItem(KEY); } catch (e) { return fresh(); }
      if (raw == null) return fresh();
      try { const s = JSON.parse(raw); if (s && s.v === SCHEMA && Array.isArray(s.rounds) && s.device) return s; } catch (e) { /* fall through */ }
      try { storage.setItem(`${KEY}-unreadable-${now()}`, raw); } catch (e) { /* nothing more to do */ }
      return fresh();
    }
    db = load();
    function save(event, round) {
      try { storage.setItem(KEY, JSON.stringify(db)); lastError = null; } catch (e) { lastError = String((e && e.name) || e); }
      if (!lastError) listeners.forEach((f) => { try { f(event, round); } catch (e) { /* a listener must never break saving */ } });
      return !lastError;
    }
    const find = (id) => db.rounds.find((r) => r.id === id);
    return {
      get lastError() { return lastError; }, get device() { return db.device; }, onChange(f) { listeners.push(f); },
      startRound({ n, session }) {
        const t0 = now(), r = { id: `${db.device.id}-${t0.toString(36)}-${rid()}`, v: SCHEMA, mode: "practice", source: SOURCE, n, t0, t1: null, status: "open", sync: 0, a: [], s: null, session };
        db.rounds.push(r); save("start", r); return r;
      },
      recordAnswer(id, i, item, ans, conf, ms) {                 // only the next unanswered item of an open round; an answer can never be changed
        const r = find(id);
        if (!r || r.status !== "open" || i !== r.a.length || !LABEL[ans]) return null;
        const e = entryOf(i, item, ans, conf, ms); r.a.push(e); r.s = summaryOf(r.a); save("answer", r); return e;
      },
      finishRound(id) { const r = find(id); if (!r || r.status !== "open") return null; r.status = "done"; r.t1 = now(); r.s = summaryOf(r.a); save("finish", r); return r; },
      markSynced(id) { const r = find(id); if (!r || r.status === "open") return false; r.sync = 1; r.syncAt = now(); return save("sync", r); },
      recoverOpen() {
        let changed = 0;
        for (const r of db.rounds.slice()) {
          if (r.status !== "open") continue;
          changed++;
          if (!r.a.length) db.rounds.splice(db.rounds.indexOf(r), 1); else { r.status = "abandoned"; r.t1 = now(); r.s = summaryOf(r.a); }
        }
        if (changed) save("recover");
        return changed;
      },
      rounds() { return db.rounds.slice().reverse(); }, round(id) { return find(id) || null; }, unsynced() { return db.rounds.filter((r) => r.status !== "open" && !r.sync); },
    };
  }

  // ---------- the page ----------
  function mk(tag, attrs, ...kids) {
    const e = root.document.createElement(tag);
    for (const k of Object.keys(attrs || {})) { if (k === "class") e.className = attrs[k]; else if (k === "html") e.innerHTML = attrs[k]; else e.setAttribute(k, attrs[k]); }
    for (const c of kids) e.append(c);
    return e;
  }
  function mount(el) {
    if (el.dataset.ready) return; el.dataset.ready = "1";
    const doc = root.document, deckUrl = el.dataset.deck;
    let store;
    try { store = createStore(root.localStorage); } catch (e) { store = createStore({ getItem() { return null; }, setItem() { throw new Error("no storage"); } }); }
    store.recoverOpen();
    if (root.SSEyesCloud && root.SSEyes) { try { root.SSEyesCloud.attach(store); } catch (e) { /* the page still works without the cloud */ } }
    const box = mk("div", { class: "ss-rh" }); el.replaceChildren(box);
    const say = (msg) => box.replaceChildren(mk("p", {}, msg));
    fetch(deckUrl).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }).then((deck) => start(deck)).catch(() => say("The rehearsal deck could not be loaded. Reload the page; if you are offline, open this page once while online first."));

    function start(deck) {
      const results = () => {
        const p = passLine(store.rounds()), sec = mk("div", { class: "ss-rh__results" });
        sec.append(mk("h3", {}, "Where you stand"), ...p.lines.map((l) => mk("p", {}, l)));
        const lastErr = store.lastError ? mk("p", { class: "ss-rh__warn" }, "This device could not save (" + store.lastError + "). Your answers will be lost when you leave.") : null;
        if (lastErr) sec.append(lastErr);
        const cloud = mk("p", { class: "ss-rh__cloud" }, root.SSEyesCloud ? root.SSEyesCloud.status() : "Cloud backup: not available in this page.");
        sec.append(cloud);
        if (root.SSEyesCloud) root.SSEyesCloud.onStatus(() => { cloud.textContent = root.SSEyesCloud.status(); });
        return sec;
      };
      function home() {
        const idx = nextSession(store.rounds()), btn = mk("button", { type: "button", class: "ss-rh__go" }, `Start session ${idx + 1} of ${SESSIONS} (20 items)`);
        btn.addEventListener("click", () => play(idx));
        box.replaceChildren(mk("p", { class: "ss-rh__lead" }, "Each item is a stretch of real light with at most one thing hidden in it. Say what you think it is, lock your answer, then see the truth. About 30% of the items hide a fake planet."), btn, results());
      }
      function play(idx) {
        const items = orderSession(deck.sessions[idx], Math.random), round = store.startRound({ n: items.length, session: idx });
        let i = 0;
        function item() {
          const it = items[i]; let chosen = null, conf = null, t0 = Date.now(), locked = false;
          const btns = {}, confBtns = {};
          const grid = mk("div", { class: "ss-rh__ans", role: "group", "aria-label": "Your answer" });
          for (const c of BUTTONS) { const b = mk("button", { type: "button", class: "ss-rh__a", "data-a": c, "aria-pressed": "false" }, LABEL[c]); btns[c] = b; grid.append(b); }
          const confRow = mk("div", { class: "ss-rh__conf", role: "group", "aria-label": "How sure are you (optional)" }, mk("span", {}, "How sure?"));
          for (const c of CONF) { const b = mk("button", { type: "button", class: "ss-rh__c", "aria-pressed": "false" }, c); confBtns[c] = b; confRow.append(b); }
          const lock = mk("button", { type: "button", class: "ss-rh__lock", disabled: "true" }, "Lock my answer");
          const out = mk("div", { class: "ss-rh__out", "aria-live": "polite" });
          const next = mk("button", { type: "button", class: "ss-rh__next", hidden: "true" }, i + 1 < items.length ? "Next" : "Finish the session");
          const pick = (c) => { if (locked) return; chosen = c; for (const k in btns) btns[k].setAttribute("aria-pressed", String(k === c)); lock.disabled = false; };
          grid.addEventListener("click", (e) => { const b = e.target.closest("button[data-a]"); if (b) pick(b.dataset.a); });
          confRow.addEventListener("click", (e) => { const b = e.target.closest(".ss-rh__c"); if (!b || locked) return; conf = b.textContent; for (const k in confBtns) confBtns[k].setAttribute("aria-pressed", String(k === conf)); });
          lock.addEventListener("click", () => {
            if (locked || !chosen) return; locked = true;
            const saved = store.recordAnswer(round.id, i, it, chosen, conf, Date.now() - t0), r = reveal(it, chosen);
            for (const k in btns) btns[k].disabled = true; for (const k in confBtns) confBtns[k].disabled = true; lock.hidden = true;
            out.className = "ss-rh__out ss-rh__out--" + (r.right ? "right" : "wrong");
            out.replaceChildren(mk("p", { class: "ss-rh__truth" }, r.headline), mk("p", {}, r.what), mk("p", {}, r.you), mk("p", {}, r.call), ...(saved ? [] : [mk("p", { class: "ss-rh__warn" }, "This answer could not be saved on this device.")]));
            next.hidden = false; next.focus();
          });
          next.addEventListener("click", () => { i++; if (i < items.length) item(); else done(); });
          const key = (e) => {
            if (!box.isConnected) { doc.removeEventListener("keydown", key); return; }
            if (/^[1-6]$/.test(e.key) && !locked) pick(BUTTONS[Number(e.key) - 1]);
            else if (e.key === "Enter" && !(e.target && e.target.tagName === "BUTTON")) { if (!locked && chosen) lock.click(); else if (locked) next.click(); }
          };
          doc.addEventListener("keydown", key);
          next.addEventListener("click", () => doc.removeEventListener("keydown", key));
          box.replaceChildren(
            mk("p", { class: "ss-rh__prog" }, `Item ${i + 1} of ${items.length}`),
            mk("div", { class: "ss-rh__panel", html: svgP1(it) }, ), mk("p", { class: "ss-rh__cap" }, "Panel 1: the whole sector. Grey bands are eclipses of the binary. The highlighted column is where the event is."),
            mk("div", { class: "ss-rh__panel", html: svgP2(it) }), mk("p", { class: "ss-rh__cap" }, "Panel 2: the event up close. Hours from the middle along the bottom, parts per million up the side. Faint line: every 6 minutes. Bold line: every 30 minutes. Grey band: one standard scatter. The bracket is the event."),
            mk("div", { class: "ss-rh__panel", html: svgP3(it) }), mk("p", { class: "ss-rh__cap" }, "Panel 3: where the event falls in the binary's orbit (shaded: eclipse zones). More evidence panels come in a later version."),
            grid, confRow, lock, out, next);
          const first = box.querySelector(".ss-rh__a"); if (first) first.focus({ preventScroll: true });
        }
        function done() {
          store.finishRound(round.id);
          const s = summaryOf(round.a), sc = mk("div", { class: "ss-rh__results" });
          sc.append(mk("h3", {}, `Session ${idx + 1} finished`), mk("p", {}, `Right class: ${s.right} of ${s.n}.`), mk("p", {}, `Fake planets found: ${s.planetsHit} of ${s.planets} (clear ${s.clearHit} of ${s.clear}, near the limit ${s.nearHit} of ${s.near}).`),
            mk("p", {}, `Not-planets called planet-like: ${s.othersCalledPlanet} of ${s.others}.`));
          const again = mk("button", { type: "button", class: "ss-rh__go" }, "Back to the start"); again.addEventListener("click", home);
          box.replaceChildren(sc, again, results());
        }
        item();
      }
      home();
    }
  }
  function boot() {
    const run = () => root.document.querySelectorAll(".ss-rehearsal").forEach(mount);
    if (root.document$ && typeof root.document$.subscribe === "function") root.document$.subscribe(run);
    else if (root.document.readyState === "loading") root.document.addEventListener("DOMContentLoaded", run); else run();
  }
  return { LABEL, BUTTONS, PASS, wilson, probit, dprime, entryOf, summaryOf, passLine, nextSession, orderSession, reveal, svgP1, svgP2, svgP3, createStore, boot, mount };
});
