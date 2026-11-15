/* Book 3.0 guided tour (Claude, 15 Nov 2026): four short steps on the first open of the Tree page, once per device.
   Skip or Done ends it for good; "Show the tour again" on the Shelf clears the mark. */
(() => {
  "use strict";
  const KEY = "ss-tour-3";
  let seen = false;
  try { seen = localStorage.getItem(KEY) === "done"; } catch (e) { seen = true; }
  const again = /[?&]tour=1/.test(location.search);
  if (seen && !again) return;
  const RM = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const phone = matchMedia("(max-width: 44.9375em)").matches;
  const steps = [
    { sel: null, title: "Welcome back", text: "Everything Second Sun is doing now grows on one map: the Tree. Four quick steps, then it is yours." },
    { sel: ".ssta-phcard, .ssta-br-h", title: "Branches", text: "Each branch is one part of the work: the hunt, the data, the checks, the book. Tap one to see what it is, why it matters and what happened to it." },
    { sel: ".sst-seg", title: "Mission and Journey", text: "Mission shows the work as it stands. Journey shows the same story along time, day by day." },
    { sel: '.md-header label[for="__drawer"], .md-tabs__link[href*="learn"]', title: "Learning", text: (phone ? "After closing this tour, open the menu at the top left and choose Learning. " : "") + "Twinlight, your new textbook, lives there: real light first, then the idea, then problems you solve yourself. Your place and notes stay on this device." },
  ];
  let i = 0, ring = null, ringTimer = 0, ended = false, target = null, savedY = 0;
  const previousFocus = document.activeElement;
  const savedStyle = document.body.getAttribute("style");
  const inerted = [...document.body.children].filter(e => !e.inert);
  const scrim = document.createElement("div"); scrim.className = "ss-tour__scrim";
  const unlock = () => {
    if (savedStyle == null) document.body.removeAttribute("style"); else document.body.setAttribute("style", savedStyle);
    scrollTo(0, savedY);
  };
  const lock = () => {
    savedY = scrollY;
    Object.assign(document.body.style, { position: "fixed", top: `-${savedY}px`, width: "100%" });
  };
  const placeRing = () => {
    if (!ring) return;
    if (!target?.isConnected) target = [...document.querySelectorAll(steps[i].sel)].find(e => e.getClientRects().length);
    ring.hidden = !target;
    if (!target) return;
    const r = target.getBoundingClientRect();
    Object.assign(ring.style, { left: `${r.left - 6}px`, top: `${r.top - 6}px`, width: `${r.width + 12}px`, height: `${r.height + 12}px` });
  };
  const box = document.createElement("div");
  box.className = "ss-tour"; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-label", "Guided tour");
  const end = () => {
    if (ended) return;
    ended = true; clearTimeout(ringTimer);
    try { localStorage.setItem(KEY, "done"); } catch (e) { /* private mode: the tour may show again */ }
    box.classList.remove("is-in"); if (ring) ring.remove();
    box.inert = true;
    scrim.remove(); inerted.forEach(e => e.inert = false); unlock();
    previousFocus?.focus({ preventScroll: true });
    setTimeout(() => box.remove(), RM ? 0 : 260);
    removeEventListener("keydown", onKey);
    removeEventListener("resize", placeRing);
    removeEventListener("scroll", placeRing);
  };
  const onKey = (e) => {
    if (e.key === "Escape") end();
    if (e.key === "Tab") {
      const buttons = [...box.querySelectorAll("button")], first = buttons[0], last = buttons.at(-1);
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  };
  const show = () => {
    clearTimeout(ringTimer);
    const s = steps[i];
    box.innerHTML = `<p class="ss-tour__step">${i + 1} of ${steps.length}</p><h2>${s.title}</h2><p>${s.text}</p>
      <div class="ss-tour__row"><button type="button" class="ss-tour__skip">${i === steps.length - 1 ? "Close" : "Skip"}</button>
      <button type="button" class="ss-tour__next">${i === steps.length - 1 ? "Done" : "Next"}</button></div>`;
    box.querySelector(".ss-tour__skip").onclick = end;
    box.querySelector(".ss-tour__next").onclick = () => { if (i < steps.length - 1) { i++; show(); } else end(); };
    if (ring) { ring.remove(); ring = null; }
    const t = target = s.sel && [...document.querySelectorAll(s.sel)].find((x) => x.getClientRects().length);
    if (t) {
      // put the target in the upper part of the screen, clear of the tour card at the bottom; draw the ring once the scroll has settled
      unlock();
      const y = t.getBoundingClientRect().top + scrollY - innerHeight * 0.22;
      if (getComputedStyle(t).position !== "fixed" && !t.closest(".md-header, .md-tabs")) scrollTo(0, Math.max(0, y));
      lock();
      ringTimer = setTimeout(() => {
        if (ended || !t.isConnected) return;
        ring = document.createElement("div"); ring.className = "ss-tour__ring";
        placeRing();
        document.body.append(ring);
      }, RM ? 0 : 700);
    }
    box.querySelector(".ss-tour__next").focus({ preventScroll: true });
  };
  const start = () => {
    savedY = scrollY;
    inerted.forEach(e => e.inert = true);
    document.body.append(scrim, box); lock(); show();
    requestAnimationFrame(() => box.classList.add("is-in"));
    addEventListener("keydown", onKey);
    addEventListener("resize", placeRing);
    addEventListener("scroll", placeRing, { passive: true });
  };
  // after the Tree has drawn and any opening animation has ended
  const go = () => setTimeout(start, document.documentElement.dataset.splash === "full" ? 2600 : 900);
  if (document.readyState === "complete") go(); else addEventListener("load", go);
})();
