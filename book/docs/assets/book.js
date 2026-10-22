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

  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(() => { closePop(); paint(); });
  else paint();

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
