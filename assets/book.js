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
    const topic = get("ss-path", "journey") === "topic";
    root.classList.toggle("ss-topic", topic);
    $$("[data-ch]").forEach((el) => el.classList.toggle("is-read", read.includes(Number(el.dataset.ch))));
    $$(".ss-read-btn").forEach((b) => {
      const on = read.includes(Number(b.dataset.ch));
      b.setAttribute("aria-pressed", String(on));
      b.textContent = on ? "Marked as read. Tap to undo" : "Mark as read";
      if (!b.dataset.seen) { b.dataset.seen = "1"; put("ss-last", Number(b.dataset.ch)); }   // opening a chapter = where you stopped
    });
    $$("[data-path-set]").forEach((b) => b.setAttribute("aria-pressed", String((b.dataset.pathSet === "topic") === topic)));
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
    const t = e.target.closest && e.target.closest(".ss-read-btn, [data-path-set]");
    if (!t) return;
    if (t.classList.contains("ss-read-btn")) {
      const n = Number(t.dataset.ch), read = get("ss-read", []);
      put("ss-read", read.includes(n) ? read.filter((x) => x !== n) : read.concat(n));
    } else put("ss-path", t.dataset.pathSet);
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

  // 6. Read aloud: the device's own voice (free, works offline, nothing is sent anywhere). Reads the chapter text
  //    paragraph by paragraph, skips pictures, code, tables, demos and equations, and highlights what it is saying.
  const SKIP = ".ss-end, .ss-demo, .ss-dg, .ss-strip, .ss-listen, .ss-eq, pre, table, figure, .ss-fallback, details, .md-nav, .md-source-file";
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
