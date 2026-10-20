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
