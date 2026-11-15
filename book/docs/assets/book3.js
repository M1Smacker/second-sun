/* Book 3.0 behaviour (Claude, 15 Nov 2026): opening logo, starfield, phone table cards, a calmer update line, gentle reveals.
   Everything here is decoration on top of a page that already works without it: if this file fails, the book still reads. */
(function () {
  "use strict";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  /* 1. Opening logo. The template draws it and CSS runs and ends it on its own (so a failure here can never trap the page);
        this only lets a tap skip it and removes the node afterwards. */
  const splash = document.getElementById("ss-splash");
  if (splash) {
    const done = () => { splash.remove(); document.documentElement.removeAttribute("data-splash"); };
    const mode = document.documentElement.getAttribute("data-splash");
    if (!mode) done();
    else {
      splash.addEventListener("click", () => { splash.classList.add("is-out"); setTimeout(done, 520); }, { once: true });
      splash.addEventListener("animationend", (e) => { if (e.target === splash) done(); });
      setTimeout(done, mode === "full" ? 3200 : 1200);   // belt and braces
    }
  }

  /* 2. Starfield: a few hundred faint stars, a slow drift, a soft twinkle; paused when hidden; none with reduced motion. */
  function sky() {
    if (reduce || document.getElementById("ss-sky")) return;
    const cv = document.createElement("canvas");
    cv.id = "ss-sky"; cv.setAttribute("aria-hidden", "true");
    document.body.prepend(cv);
    const g = cv.getContext("2d");
    let w, h, dpr, stars = [], raf = 0, last = 0;
    function size() {
      dpr = Math.min(2, window.devicePixelRatio || 1);
      w = innerWidth; h = innerHeight;
      cv.width = w * dpr; cv.height = h * dpr; cv.style.width = w + "px"; cv.style.height = h + "px";
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(260, (w * h) / 5200));
      stars = Array.from({ length: n }, () => ({
        x: Math.random() * w, y: Math.random() * h, r: Math.random() < .08 ? 1.3 + Math.random() * .7 : .35 + Math.random() * .75,
        a: .25 + Math.random() * .6, tw: Math.random() * Math.PI * 2, sp: .3 + Math.random() * 1.2,
        c: Math.random() < .18 ? "185,173,255" : Math.random() < .5 ? "190,225,255" : "235,242,255",
      }));
    }
    function frame(t) {
      raf = requestAnimationFrame(frame);
      if (t - last < 33) return;                       // about 30 frames a second is plenty for this
      const dt = (t - last) / 1000; last = t;
      g.clearRect(0, 0, w, h);
      const sy = (scrollY || 0) * .04;
      for (const s of stars) {
        s.x -= s.sp * dt * 1.6; if (s.x < -2) s.x = w + 2;
        s.tw += dt * s.sp;
        const al = s.a * (.72 + .28 * Math.sin(s.tw));
        g.fillStyle = `rgba(${s.c},${al.toFixed(3)})`;
        g.beginPath(); g.arc(s.x, (s.y - sy * s.sp + h) % h, s.r, 0, 6.283); g.fill();
      }
    }
    size(); addEventListener("resize", () => { cancelAnimationFrame(raf); size(); raf = requestAnimationFrame(frame); });
    document.addEventListener("visibilitychange", () => { cancelAnimationFrame(raf); if (!document.hidden) { last = 0; raf = requestAnimationFrame(frame); } });
    raf = requestAnimationFrame(frame);
  }

  /* 3. Phone tables become cards: each cell carries its column name; PC keeps the table (CSS does the switch). */
  function cards(root) {
    root.querySelectorAll(".md-typeset table:not(.ss-keep):not(.ss-cards)").forEach((t) => {
      const heads = [...t.querySelectorAll("thead th")].map((th) => th.textContent.trim());
      if (!heads.length || heads.length > 7) return;
      t.classList.add("ss-cards");
      t.querySelectorAll("tbody tr").forEach((tr) => [...tr.children].forEach((td, i) => td.setAttribute("data-label", heads[i] || "")));
    });
  }

  /* 4. The update line: slides away when dismissed and links to what is new (the diary). */
  function updateLine(bar) {
    if (bar.dataset.ss3) return;
    bar.dataset.ss3 = "1";
    const span = bar.querySelector("span");
    if (span) {
      span.textContent = "A new version of the book is ready.";
      const a = document.createElement("a");
      a.className = "ss-update__new"; a.textContent = "What's new";
      const base = document.querySelector('link[rel="manifest"]');
      a.href = base ? new URL("versions/", base.href).href : "versions/";
      span.after(a);
    }
    const close = bar.querySelector(".ss-update__close");
    if (close) close.addEventListener("click", (e) => {
      if (bar.classList.contains("is-leaving")) return;
      e.stopImmediatePropagation();
      bar.classList.add("is-leaving");
      setTimeout(() => { bar.remove(); document.body.classList.remove("ss-has-update"); }, 300);
    }, { capture: true });
  }
  new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => {
    if (n.nodeType === 1 && n.classList.contains("ss-update")) updateLine(n);
  }))).observe(document.body, { childList: true });

  /* 5. Gentle reveal of blocks as they scroll in (only marked blocks; without JS they simply show). */
  function reveals(root) {
    if (reduce || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
    root.querySelectorAll("[data-reveal]").forEach((el) => { el.classList.add("ss-reveal"); io.observe(el); });
  }

  function init() { sky(); cards(document); reveals(document); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
  window.SS3 = { cards, reveals, store };
})();
