// Page-side helpers for the Second Sun book.
// 1. html.ss-ready after the first paint, so theme colour transitions never run on load.
// 2. Offline worker registration + a quiet "Updated. Reload" line.
//    Loop guards: we reload only after the reader taps Reload, and at most once (reloading flag);
//    the first install never reloads; another tab's update only shows the line.
(() => {
  const root = document.documentElement;
  requestAnimationFrame(() => requestAnimationFrame(() => root.classList.add("ss-ready")));

  // 3. Sidebar reading marks: pages you've opened get a filled dot on the sidebar track.
  //    Per-device convenience only (localStorage); everything works without it.
  const KEY = "ss-opened";
  const norm = (u) => new URL(u, location.href).pathname.replace(/index\.html$/, "");
  function markNav() {
    let seen = [];
    try {
      seen = JSON.parse(localStorage.getItem(KEY) || "[]");
      const here = norm(location.href);
      if (!seen.includes(here)) { seen.push(here); localStorage.setItem(KEY, JSON.stringify(seen)); }
    } catch (e) { return; }
    document.querySelectorAll(".md-sidebar--primary a.md-nav__link[href]").forEach((a) => {
      a.classList.toggle("ss-opened", seen.includes(norm(a.href)));
    });
  }
  // Material's instant navigation swaps pages without a reload and announces each one on document$.
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(markNav);
  else markNav();

  // 4. Reading state, reading order and the home "where you stopped" card. All per device (localStorage);
  //    the book reads fine without it. Chapters are identified by number (1 to 15).
  const SRC = document.currentScript && document.currentScript.src;
  const get = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const put = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: nothing is saved */ } };
  const $$ = (s) => Array.from(document.querySelectorAll(s));

  function paint() {
    const read = get("ss-read", []);
    $$("[data-ch]").forEach((el) => el.classList.toggle("is-read", read.includes(Number(el.dataset.ch))));
    $$(".ss-read-btn").forEach((b) => {
      const on = read.includes(Number(b.dataset.ch));
      b.setAttribute("aria-pressed", String(on));
      b.textContent = on ? "Marked as read. Tap to undo" : "Mark as read";
      if (!b.dataset.seen) { b.dataset.seen = "1"; put("ss-last", Number(b.dataset.ch)); }   // opening a chapter = where you stopped
    });
    const card = document.querySelector(".ss-resume");
    if (card) try {
      const chs = JSON.parse(card.dataset.chapters);
      const last = chs.find((c) => c.n === get("ss-last", 0));
      const span = card.querySelector("span");
      span.textContent = "";
      if (last) {
        const a = document.createElement("a");
        a.href = last.u; a.textContent = "Chapter " + last.n + ": " + last.t;
        span.append(a, " · " + read.length + " of " + chs.length + " read");
      } else span.textContent = "Nothing opened yet. " + read.length + " of " + chs.length + " chapters read.";
    } catch (err) { /* keep the static text */ }
  }
  document.addEventListener("click", (e) => {
    const t = e.target.closest && e.target.closest(".ss-read-btn");
    if (!t) return;
    const n = Number(t.dataset.ch), read = get("ss-read", []);
    put("ss-read", read.includes(n) ? read.filter((x) => x !== n) : read.concat(n));
    paint();
  });

  // 5. Glossary popups: a tap on a glossary link shows the plain definition; "More" opens the glossary.
  let G = null, pop = null;
  const closePop = () => { if (pop) { pop.remove(); pop = null; } };
  const glossary = async () => {
    if (!G) { try { G = await (await fetch(new URL("glossary.json", SRC))).json(); } catch (err) { G = {}; } }
    return G;
  };
  function showPop(term, def, href) {
    closePop();
    pop = document.createElement("div");
    pop.className = "ss-pop"; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", term);
    const h = document.createElement("b"), p = document.createElement("p"), more = document.createElement("a"), x = document.createElement("button");
    h.textContent = term; p.textContent = def; more.href = href; more.textContent = "More in the glossary";
    x.type = "button"; x.textContent = "Close"; x.addEventListener("click", closePop);
    pop.append(h, p, more, x);
    document.body.appendChild(pop);
    x.focus({ preventScroll: true });
  }
  document.addEventListener("click", async (e) => {
    const a = e.target.closest && e.target.closest('.md-typeset a[href*="glossary/#"]');
    if (!a) { if (pop && !pop.contains(e.target)) closePop(); return; }
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button || /\/glossary\/?(index\.html)?$/.test(location.pathname) || !SRC) return;
    e.preventDefault(); e.stopImmediatePropagation();
    const hit = (await glossary())[decodeURIComponent(a.hash.slice(1))];
    if (hit) showPop(hit[0], hit[1], a.href); else location.href = a.href;
  }, true);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closePop(); });

  // 5b. PC chapter page (from 1120 px, see shape.css): the evidence and glossary notes also sit in the margin beside the text, only the note nearest the middle of
  //     the screen is open, and "In this chapter" fills in the left rail. The chips and glossary links in the text stay the real thing (phone, keyboard, screen
  //     reader, offline), so the margin only repeats them for the eye: it is aria-hidden and holds no links. Without JavaScript the margin simply is not there.
  const WIDE = matchMedia("(min-width: 70em)");
  let M = null;
  async function marginInit() {
    M = null;
    const inner = document.querySelector(".md-content__inner"), rail = inner && inner.querySelector(":scope > .ss-rail");
    if (!rail) return;
    const toc = rail.querySelector(".ss-rail__toc");
    if (toc && !toc.children.length) $$(".md-content__inner > h2[id]").forEach((h) => {
      const li = document.createElement("li"), a = document.createElement("a");
      a.href = "#" + h.id; a.textContent = Array.from(h.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent).join("").trim();
      li.append(a); toc.append(li);
    });
    const margin = document.createElement("aside"), notes = [], seen = new Set();
    margin.className = "ss-margin"; margin.setAttribute("aria-hidden", "true");
    const add = (anchor, key, label, text, src) => {
      if (seen.has(key)) return; seen.add(key);
      const el = document.createElement("div"), t = document.createElement("span"), q = document.createElement("p");
      el.className = "mn off"; el.dataset.key = key; t.className = "t"; t.textContent = label; q.className = "q"; q.textContent = text; el.append(t, q);
      if (src) { const s = document.createElement("p"); s.className = "s"; s.textContent = src; el.append(s); }
      margin.append(el); notes.push({ el, anchor });
    };
    $$(".md-content__inner a.ss-chip[data-cid]").forEach((a) => add(a, a.dataset.cid, "Evidence · " + a.dataset.cid + " · " + a.textContent.trim().toLowerCase(), a.dataset.claim, "Source: " + a.dataset.src + ". Checked " + a.dataset.checked + "."));
    const G = await glossary();
    $$('.md-content__inner a[href*="glossary/#"]').forEach((a) => { const hit = G[decodeURIComponent(a.hash.slice(1))]; if (hit) add(a, "g:" + a.hash, "Glossary · " + hit[0], hit[1], ""); });
    if (!document.querySelector(".md-content__inner > .ss-rail")) return;           // the reader moved to another page while the glossary loaded
    inner.append(margin);
    M = { inner, rail, margin, notes, on: null, toc };
    marginTick();
  }
  function marginTick() {
    if (!M || !WIDE.matches) return;
    const vis = M.notes.filter((n) => n.anchor.getClientRects().length), vh = innerHeight;
    M.notes.forEach((n) => { n.el.hidden = !vis.includes(n); });
    let best = null, bd = 1e9;
    vis.forEach((n) => { const r = n.anchor.getBoundingClientRect(); if (r.bottom > 90 && r.top < vh * 0.85) { const d = Math.abs(r.top - vh * 0.38); if (d < bd) { bd = d; best = n; } } });
    if (best !== M.on) { M.on = best; M.notes.forEach((n) => { n.el.classList.toggle("on", n === best); n.el.classList.toggle("off", n !== best); }); }
    // The open note sits exactly beside its anchor; the others stack above and below it. A note that cannot sit within 120 px of its own anchor is left out of the margin
    // (its chip or glossary link in the text still works as on a phone) rather than drifting away from what it explains.
    const top0 = M.inner.getBoundingClientRect().top, MAXD = 120;
    const items = vis.map((n) => ({ n, y: n.anchor.getBoundingClientRect().top - top0 - 4, h: n.el.offsetHeight })).sort((a, b) => a.y - b.y);
    const k = items.findIndex((it) => it.n === M.on), put = (it, top) => { it.n.el.style.top = top + "px"; };
    let floor = 0, ceil = Infinity;
    if (k >= 0) { put(items[k], items[k].y); floor = items[k].y + items[k].h + 10; ceil = items[k].y - 10; }
    for (let i = k + 1; i < items.length; i++) { const it = items[i], top = Math.max(it.y, floor); if (top - it.y > MAXD) { it.n.el.hidden = true; continue; } put(it, top); floor = top + it.h + 10; }
    for (let i = k - 1; i >= 0; i--) { const it = items[i], top = Math.min(it.y, ceil - it.h); if (it.y - top > MAXD || top < 0) { it.n.el.hidden = true; continue; } put(it, top); ceil = top - 10; }
    const hs = $$(".md-content__inner > h2[id]"), links = M.toc ? Array.from(M.toc.querySelectorAll("a")) : [];
    let cur = -1; hs.forEach((h, i) => { if (h.getBoundingClientRect().top < vh * 0.3) cur = i; });
    links.forEach((a, i) => { if (i === cur) a.setAttribute("aria-current", "location"); else a.removeAttribute("aria-current"); });
  }
  let marginQueued = false;
  const marginSoon = () => { if (!marginQueued) { marginQueued = true; requestAnimationFrame(() => { marginQueued = false; marginTick(); }); } };
  addEventListener("scroll", marginSoon, { passive: true }); addEventListener("resize", marginSoon); addEventListener("load", marginSoon);
  document.addEventListener("toggle", marginSoon, true);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(marginSoon);
  WIDE.addEventListener("change", marginSoon);
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(marginInit); else marginInit();

  // 6. Read aloud: the device's own voice (free, works offline, nothing is sent anywhere). Reads the chapter text
  //    paragraph by paragraph, skips pictures, code, tables, demos and equations, and highlights what it is saying.
  const SKIP = ".ss-end, .ss-demo, .ss-dg, .ss-strip, .ss-rail, .ss-margin, .ss-listen, .ss-eq, pre, table, figure, .ss-fallback, details, .md-nav, .md-source-file";
  let queue = [], at = 0, speaking = false, current = null;
  const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
  const bar = () => document.querySelector(".ss-listen");
  function chunks() {
    const out = []; let done = false;
    $$(".md-content__inner :is(h2, h3, h4, p, li)").forEach((el) => {
      if (done || el.closest(SKIP) || el.classList.contains("ss-meta")) return;
      if (el.matches("h2") && /^Sources/i.test(el.textContent.trim())) { done = true; return; }      // the reference list is not read aloud
      if (el.matches("li") && el.querySelector(":scope > p, :scope > ul, :scope > ol")) return;       // read the inner paragraph instead
      const c = el.cloneNode(true);
      c.querySelectorAll(".ss-chip, .headerlink, sup, code, svg, .ss-demo").forEach((x) => x.remove());
      const text = c.textContent.replace(/\s+/g, " ").trim();
      if (text.length < 2) return;
      (text.match(/[^.!?]+[.!?]+["')\]]*\s*|[^.!?]+$/g) || [text]).reduce((acc, s) => {                 // sentences, packed to about 220 characters
        if (acc.length && acc[acc.length - 1].length + s.length < 220) acc[acc.length - 1] += s; else acc.push(s);
        return acc;
      }, []).forEach((s) => out.push({ el, text: s.trim() }));
    });
    return out;
  }
  function paintSay(state) {
    const b = bar(); if (!b) return;
    b.querySelector('[data-say="play"]').textContent = state === "paused" ? "Resume" : "Listen";
    b.querySelector('[data-say="play"]').hidden = state === "playing";
    b.querySelector('[data-say="pause"]').hidden = state !== "playing";
    b.querySelector('[data-say="stop"]').hidden = state === "idle";
  }
  function mark(el) {
    if (current) current.classList.remove("ss-saying");
    current = el; if (!el) return;
    el.classList.add("ss-saying");
    const r = el.getBoundingClientRect();
    if (r.top < 70 || r.bottom > innerHeight - 20) el.scrollIntoView({ block: "center", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }
  function next() {
    if (!speaking) return;
    if (at >= queue.length) { speaking = false; at = 0; mark(null); paintSay("idle"); return; }
    const item = queue[at], u = new SpeechSynthesisUtterance(item.text), rate = bar() && bar().querySelector("[data-say-rate]");
    u.lang = document.documentElement.lang || "en"; u.rate = rate ? Number(rate.value) : 1;
    u.onend = () => { if (speaking) { at += 1; next(); } };
    u.onerror = (e) => { if (speaking && e.error !== "interrupted" && e.error !== "canceled") { at += 1; next(); } };
    mark(item.el); synth.speak(u);
  }
  function saycmd(cmd) {
    if (!synth) return;
    if (cmd === "play") { if (!queue.length || at >= queue.length) { queue = chunks(); at = 0; } speaking = true; paintSay("playing"); next(); }
    else if (cmd === "pause") { speaking = false; synth.cancel(); paintSay("paused"); }          // cancel + remember the place: pause() is unreliable on phones
    else { speaking = false; synth.cancel(); queue = []; at = 0; mark(null); paintSay("idle"); }
  }
  function sayInit() {
    const b = bar();
    if (synth && b) { b.hidden = false; queue = []; at = 0; speaking = false; current = null; paintSay("idle"); }
  }
  document.addEventListener("click", (e) => {
    const t = e.target.closest && e.target.closest("[data-say]"); if (t) saycmd(t.dataset.say);
    if (e.target.closest && e.target.closest("[data-print]")) window.print();
  });
  window.addEventListener("pagehide", () => { if (synth) synth.cancel(); });

  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(() => { closePop(); if (synth) synth.cancel(); paint(); sayInit(); });
  else { paint(); sayInit(); }

  const swUrl = document.currentScript && document.currentScript.dataset.sw;
  if (!("serviceWorker" in navigator) || !swUrl) return;

  const hadController = !!navigator.serviceWorker.controller;
  let userAsked = false;
  let reloading = false;
  let shown = false;

  function reloadOnce() {
    if (reloading) return;
    reloading = true;
    location.reload();
  }

  function showLine(reg) {
    if (shown) return;                       // at most one line per page load
    shown = true;
    const bar = document.createElement("div");
    bar.className = "ss-update";
    bar.setAttribute("role", "status");
    bar.innerHTML = '<span>Updated.</span><button type="button">Reload</button>';
    bar.querySelector("button").addEventListener("click", () => {
      userAsked = true;
      if (reg && reg.waiting) reg.waiting.postMessage({ type: "SKIP_WAITING" });   // controllerchange then reloads
      else reloadOnce();                                                             // new worker already active
    });
    document.body.appendChild(bar);
  }

  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (userAsked) reloadOnce();
    else if (hadController) showLine(null);  // updated from another tab: offer, never force
  });

  navigator.serviceWorker.register(swUrl).then((reg) => {
    const watch = (w) => w && w.addEventListener("statechange", () => {
      if (w.state === "installed" && navigator.serviceWorker.controller) showLine(reg);
    });
    if (reg.waiting && navigator.serviceWorker.controller) showLine(reg);
    watch(reg.installing);
    reg.addEventListener("updatefound", () => watch(reg.installing));
  }).catch(() => { /* no service worker here (e.g. private mode): the site still works online */ });
})();
