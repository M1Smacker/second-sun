/* The Tree page (Book 3.0, Claude, 15 Nov 2026). Draws assets/data/tree.json (made by research/tree/brain_build.py on every build).
   Two views: the mission tree (what stops us, by branch) and the journey (the same work through time). PC: a canvas with smooth zoom
   and pan (zoom toward the pointer, inertia after a drag, pinch on touch screens, keyboard), cards anchored where the branch is.
   Phone: a vine down the left edge with full-width cards and a slide-up sheet. Search lights matches; 'N new' shows what changed
   since the last visit; branches with new work pulse softly. Without this script the page shows a plain list (built at build time). */
(function () {
  "use strict";
  const host = document.getElementById("ss-tree");
  if (!host) return;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const WIDE = matchMedia("(min-width: 900px)");
  const S = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const ICON = {
    ACTIVE: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-opacity=".45"/><circle cx="7" cy="7" r="3.4" fill="currentColor"/></svg>',
    NEXT: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor"/><path d="M5.6 4.2 8.6 7l-3 2.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    WAITS: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M4 2h6M4 12h6M4.6 2.4c0 3 4.8 3.2 4.8 4.6S4.6 8.6 4.6 11.6M9.4 2.4c0 3-4.8 3.2-4.8 4.6s4.8 1.6 4.8 4.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>',
    PARKED: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-opacity=".6"/><path d="M5.6 4.6v4.8M8.4 4.6v4.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    BLOCKED: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor"/><path d="m4.8 4.8 4.4 4.4M9.2 4.8 4.8 9.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    DONE: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor"/><path d="m4.4 7.2 1.8 1.8 3.6-3.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  };
  const STATUS_WORD = { ACTIVE: "Active now", NEXT: "Next", WAITS: "Waiting", PARKED: "Parked", BLOCKED: "Blocked", DONE: "Done" };
  const STATUS_COLOR = { ACTIVE: "var(--ss-accent)", NEXT: "var(--ss-text)", WAITS: "var(--ss-text-2)", PARKED: "var(--ss-text-3)", BLOCKED: "var(--leaf)", DONE: "var(--ss-text-2)" };
  const fmtDate = (iso) => { if (!iso) return ""; const d = new Date(iso.length > 10 ? iso : iso + "T12:00"); return d.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }); };
  const fmtWhen = (l) => fmtDate(l.when || l.date) + (l.when && l.kind === "drop" ? ", " + new Date(l.when).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" }) : "");

  let D, nodes = {}, leaves = {}, view = S.get("sst-view") === "journey" ? "journey" : "mission";
  let newIds = new Set(), showNew = false, query = "", openState = null;

  fetch(host.dataset.src, { cache: "no-cache" }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }).then(start).catch(() => {
    host.classList.add("sst-failed");     // the static list stays visible
  });

  function start(data) {
    D = data;
    D.nodes.forEach((n) => { nodes[n.id] = n; });
    D.leaves.forEach((l) => { leaves[l.id] = l; });
    const last = S.get("sst-last-visit");
    if (last) D.leaves.forEach((l) => { if ((l.when || "") > last) newIds.add(l.id); });
    setTimeout(() => S.set("sst-last-visit", D.generated), 4000);
    const stat = host.querySelector(".sst-static");
    if (stat) stat.hidden = true;
    host.classList.add("sst");
    host.insertAdjacentHTML("afterbegin", bar());
    wireBar();
    render(true);
    WIDE.addEventListener("change", () => render(false));
    const m = /^#n=([\d.]+)$/.exec(location.hash);
    if (m && nodes[m[1]]) setTimeout(() => openNode(m[1]), reduce ? 0 : 900);
    addEventListener("popstate", () => { if (openState) closeCard(true); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && openState) closeCard(false); });
  }

  /* ---------- toolbar ---------- */
  function bar() {
    const n = newIds.size;
    return `<div class="sst-bar">
      <div class="sst-seg" role="group" aria-label="Tree view"><i aria-hidden="true"></i>
        <button type="button" data-view="mission" aria-pressed="${view === "mission"}">Mission</button>
        <button type="button" data-view="journey" aria-pressed="${view === "journey"}">Journey</button></div>
      <label class="sst-search"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m11 11 3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        <input type="search" placeholder="Search the Tree" aria-label="Search the Tree" autocomplete="off" enterkeyhint="search"></label>
      ${n ? `<button type="button" class="sst-new" aria-pressed="false" title="Work added since your last visit"><b>${n}</b> new</button>` : ""}
      ${D.now ? `<p class="sst-now"><b>Now:</b> ${esc(D.now)}</p>` : ""}
    </div><div class="sst-view"></div>`;
  }
  function wireBar() {
    const seg = host.querySelector(".sst-seg"), pill = seg.querySelector("i");
    const place = () => { const b = seg.querySelector('[aria-pressed="true"]'); pill.style.left = b.offsetLeft + "px"; pill.style.width = b.offsetWidth + "px"; };
    seg.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-view]"); if (!b || b.dataset.view === view) return;
      view = b.dataset.view; S.set("sst-view", view);
      seg.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      place(); closeCard(false); render(true);
    });
    requestAnimationFrame(place); addEventListener("resize", place);
    const input = host.querySelector(".sst-search input"); let t;
    input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { query = input.value.trim().toLowerCase(); applyFilter(); }, 120); });
    input.addEventListener("keydown", (e) => {
      if (e.key === "Escape") { input.value = ""; query = ""; applyFilter(); }
      if (e.key === "Enter") { e.preventDefault(); const first = host.querySelector("[data-node]:not(.is-dim), [data-leaf]:not(.is-dim)"); if (first) focusOn(first); }
    });
    const nb = host.querySelector(".sst-new");
    if (nb) nb.addEventListener("click", () => { showNew = !showNew; nb.setAttribute("aria-pressed", String(showNew)); applyFilter(); });
  }

  /* ---------- which things match the search or the 'new' filter ---------- */
  function leafText(l) { return (l.plain + " " + l.why + " " + l.explanation + " " + l.technical + " " + l.ids.join(" ")).toLowerCase(); }
  function matches() {
    if (!query && !showNew) return null;
    const ln = new Set(), nn = new Set();
    D.leaves.forEach((l) => {
      if ((!query || leafText(l).includes(query)) && (!showNew || newIds.has(l.id))) { ln.add(l.id); nn.add(l.node); (l.also || []).forEach((a) => nn.add(a)); }
    });
    if (query && !showNew) D.nodes.forEach((n) => { if ((n.title + " " + n.plain + " " + (n.status_text || "") + " " + (n.id_tree || "")).toLowerCase().includes(query)) nn.add(n.id); });
    [...nn].forEach((id) => { const n = nodes[id]; if (n && n.parent && nodes[n.parent]) nn.add(n.parent); });
    return { ln, nn };
  }
  function applyFilter() {
    const m = matches();
    host.querySelectorAll("[data-node]").forEach((e) => e.classList.toggle("is-dim", !!m && !m.nn.has(e.dataset.node) && e.dataset.node !== "goal"));
    host.querySelectorAll("[data-leaf]").forEach((e) => e.classList.toggle("is-dim", !!m && !m.ln.has(e.dataset.leaf)));
    host.querySelectorAll("[data-vine]").forEach((e) => e.classList.toggle("is-dim", !!m && !m.nn.has(e.dataset.vine)));
    host.querySelectorAll(".sst-day").forEach((d) => { d.hidden = !!m && ![...d.querySelectorAll("[data-leaf]")].some((x) => m.ln.has(x.dataset.leaf)) && !(query && d.textContent.toLowerCase().includes(query)); });
  }

  function render(grow) {
    const v = host.querySelector(".sst-view");
    v.innerHTML = "";
    host.classList.toggle("sst-grow", !!grow && !reduce);
    if (view === "journey") journey(v); else if (WIDE.matches) canvas(v); else list(v);
    applyFilter();
    if (grow && !reduce) setTimeout(() => host.classList.remove("sst-grow"), 2600);
  }

  /* ---------- PC: the mission tree on a canvas ---------- */
  const COLW = 340, ROWH = 64, LW = 232, LH = 50;
  function layout() {
    const br = D.nodes.filter((n) => n.parent === "goal");
    const rows = Math.max(...br.map((b) => b.children.length));
    const top = 40, branchY = top + rows * ROWH + 60, rootY = branchY + 150, W = br.length * COLW + 100;
    const pos = {}, cx = W / 2;
    pos.goal = { x: cx, y: rootY };
    br.forEach((b, i) => {
      const x = 60 + COLW * i + 90;
      pos[b.id] = { x, y: branchY };
      b.children.forEach((c, j) => { pos[c] = { x: x + Math.sin(j * 1.25 + i) * 12, y: branchY - 80 - j * ROWH }; });
    });
    return { pos, W, H: rootY + 60, cx, branchY, br };
  }
  function canvas(v) {
    const L = layout(), P = L.pos;
    const stage = document.createElement("div");
    stage.className = "sst-stage"; stage.tabIndex = 0;
    stage.setAttribute("aria-label", "The project tree. Drag to move, scroll or pinch to zoom, arrow keys move, plus and minus zoom, 0 fits.");
    v.appendChild(stage);
    const top = () => stage.getBoundingClientRect().top + scrollY;
    const size = () => { stage.style.height = Math.max(420, innerHeight - (stage.getBoundingClientRect().top)) + "px"; };
    size();
    const svg = el("svg", { role: "img", "aria-label": "Mission tree" }, stage);
    const defs = el("defs", {}, svg);
    const f = el("filter", { id: "sst-glow", x: "-50%", y: "-50%", width: "200%", height: "200%" }, defs);
    el("feGaussianBlur", { stdDeviation: "2.4", result: "b" }, f);
    const fm = el("feMerge", {}, f); el("feMergeNode", { in: "b" }, fm); el("feMergeNode", { in: "SourceGraphic" }, fm);
    const world = el("g", {}, svg);
    const vines = el("g", {}, world), twigs = el("g", {}, world), nodeLayer = el("g", {}, world);
    const hot = (id) => { const n = nodes[id]; if (!n) return false; if (n.status === "ACTIVE") return true; return (n.children || []).some((c) => nodes[c].status === "ACTIVE"); };
    const path = (d, w, id, delay, isHot) => {
      const p = el("path", { d, class: "sst-vine" + (isHot ? " is-hot" : ""), "stroke-width": w, "data-vine": id }, vines);
      p.style.setProperty("--d", delay + "ms");
      requestAnimationFrame(() => { try { p.style.setProperty("--len", p.getTotalLength().toFixed(0)); } catch (e) { /* not rendered yet */ } });
      return p;
    };
    const split = { x: L.cx, y: L.branchY + 86 };
    path(`M${L.cx},${P.goal.y - 20} C${L.cx},${P.goal.y - 70} ${L.cx},${split.y + 40} ${split.x},${split.y}`, 10, "goal", 0, true);
    L.br.forEach((b, i) => {
      const B = P[b.id];
      path(`M${split.x},${split.y} C${split.x},${split.y - 60} ${B.x},${B.y + 80} ${B.x},${B.y + 22}`, 3 + b.weight * 1.3, b.id, 250 + i * 60, hot(b.id));
      let prev = { x: B.x, y: B.y - 22 };
      b.children.forEach((c, j) => {
        const C = P[c], above = b.children.slice(j).map((k) => nodes[k].weight);
        const w = 1.4 + Math.max(...above) * 0.9;
        const isHot = b.children.slice(j).some((k) => nodes[k].status === "ACTIVE");
        path(`M${prev.x},${prev.y} C${prev.x},${prev.y - 30} ${C.x - 6},${C.y + 40} ${C.x},${C.y}`, w, c, 520 + i * 60 + j * 70, isHot);
        prev = C;
      });
    });
    const nodeEl = (id, x, y, w, h, title, sub, cls, delay) => {
      const n = nodes[id], g = el("g", { class: "sst-node " + (cls || ""), tabindex: "0", role: "button", "data-node": id, "aria-label": title + (n ? ", " + STATUS_WORD[n.status] : "") }, nodeLayer);
      g.style.setProperty("--d", delay + "ms");
      el("rect", { x: x, y: y, width: w, height: h, rx: 13 }, g);
      if (n) {
        const ic = el("foreignObject", { x: x + 12, y: y + (h - 14) / 2, width: 14, height: 14 }, g);
        ic.innerHTML = `<div xmlns="http://www.w3.org/1999/xhtml" style="color:${STATUS_COLOR[n.status]};line-height:0">${ICON[n.status]}</div>`;
      }
      const tx = n ? x + 34 : x + w / 2;
      const t = el("text", { x: tx, y: y + (sub ? h / 2 - 1 : h / 2 + 5), "text-anchor": n ? "start" : "middle" }, g);
      t.textContent = title;
      if (sub) { const s = el("text", { x: tx, y: y + h / 2 + 15, class: "sst-sub", "text-anchor": n ? "start" : "middle" }, g); s.textContent = sub; }
      if (n && (n.history || []).some((i) => newIds.has(i))) g.classList.add("is-new");
      return g;
    };
    nodeEl("goal", P.goal.x - 170, P.goal.y - 22, 340, 58, D.goal.title, "Or prove, with numbers, that none was there", "is-root", 0);
    L.br.forEach((b, i) => {
      const B = P[b.id];
      nodeEl(b.id, B.x - 100, B.y - 22, 200, 44, b.title, null, "", 420 + i * 60);
      b.children.forEach((c, j) => {
        const C = P[c], n = nodes[c];
        nodeEl(c, C.x + 16, C.y - LH / 2, LW, LH, n.title, `${n.id} · ${STATUS_WORD[n.status].toLowerCase()}`, "", 700 + i * 60 + j * 70);
        const hist = n.history || [];
        const shown = hist.slice(0, 6);
        shown.forEach((lid, k) => {
          const a = -0.9 + k * 0.36, r = 30;
          const lx = C.x + 16 + LW + 16 + Math.cos(a) * r * 0.9 + k * 6, ly = C.y + Math.sin(a) * r * 0.6;
          el("path", { d: `M${C.x + 16 + LW},${C.y} Q${C.x + 16 + LW + 8},${ly} ${lx},${ly}`, class: "sst-vine", "stroke-width": 1, "data-vine": c, opacity: ".5" }, twigs);
          const dot = el("circle", { cx: lx, cy: ly, r: 5, class: "sst-leaf" + (k > 2 ? " is-old" : "") + (newIds.has(lid) ? " is-new" : ""), tabindex: "0", role: "button", "data-leaf": lid, "aria-label": leaves[lid] ? leaves[lid].plain : "leaf" }, nodeLayer);
          dot.style.setProperty("--d", 1100 + i * 60 + j * 70 + k * 50 + "ms");
        });
        if (hist.length > 6) { const m = el("text", { x: C.x + 16 + LW + 64, y: C.y + 22, class: "sst-more" }, nodeLayer); m.textContent = "+" + (hist.length - 6); }
      });
    });
    host.querySelectorAll(".sst-grow .sst-node, .sst-grow .sst-leaf").forEach(() => {});
    // ---- zoom and pan: transform state, eased toward a target; inertia after a drag ----
    const T = { x: 0, y: 0, k: 1 }, G = { x: 0, y: 0, k: 1 };
    const KMIN = 0.3, KMAX = 3.2;
    let raf = 0, vel = { x: 0, y: 0 }, lastT = 0;
    const apply = () => { world.setAttribute("transform", `translate(${T.x.toFixed(2)},${T.y.toFixed(2)}) scale(${T.k.toFixed(4)})`); placeCard(); };
    const tick = (t) => {
      const dt = Math.min(48, t - (lastT || t)) / 16.67; lastT = t;
      if (Math.abs(vel.x) + Math.abs(vel.y) > 0.05) { G.x += vel.x * dt; G.y += vel.y * dt; const fr = Math.pow(0.9, dt); vel.x *= fr; vel.y *= fr; } else { vel.x = vel.y = 0; }
      const a = reduce ? 1 : 1 - Math.pow(1 - 0.24, dt);
      T.x += (G.x - T.x) * a; T.y += (G.y - T.y) * a; T.k += (G.k - T.k) * a;
      apply();
      if (Math.abs(G.x - T.x) > 0.1 || Math.abs(G.y - T.y) > 0.1 || Math.abs(G.k - T.k) > 0.0005 || vel.x || vel.y) raf = requestAnimationFrame(tick);
      else { T.x = G.x; T.y = G.y; T.k = G.k; apply(); raf = 0; lastT = 0; }
    };
    const kick = () => { if (!raf) raf = requestAnimationFrame(tick); };
    const zoomAt = (px, py, factor) => {
      const k = Math.min(KMAX, Math.max(KMIN, G.k * factor)); const f = k / G.k;
      G.x = px - (px - G.x) * f; G.y = py - (py - G.y) * f; G.k = k; vel.x = vel.y = 0; kick();
    };
    const fit = (instant) => {
      const r = stage.getBoundingClientRect(), pad = 30;
      const k = Math.min((r.width - pad * 2) / L.W, (r.height - pad * 2) / L.H, 1.1);
      G.k = k; G.x = (r.width - L.W * k) / 2; G.y = (r.height - L.H * k) / 2 + 6;
      if (instant) { T.x = G.x; T.y = G.y; T.k = G.k; apply(); } else kick();
    };
    stage._fit = fit; stage._goTo = (wx, wy, k) => { const r = stage.getBoundingClientRect(); G.k = k || Math.max(G.k, 1); G.x = r.width / 2 - wx * G.k; G.y = r.height / 2 - wy * G.k; vel.x = vel.y = 0; kick(); };
    stage._pos = P;
    fit(true);
    addEventListener("resize", () => { size(); fit(false); });
    stage.addEventListener("wheel", (e) => {
      e.preventDefault();
      const r = stage.getBoundingClientRect();
      const dy = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaMode === 2 ? e.deltaY * r.height : e.deltaY;
      zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-dy * (e.ctrlKey ? 0.01 : 0.0016)));
    }, { passive: false });
    const pts = new Map(); let drag = null, pinch = null, moved = 0, downOn = null;
    stage.addEventListener("pointerdown", (e) => {
      if (e.button !== 0 && e.pointerType === "mouse") return;
      if (e.target.closest(".sst-card, .sst-zoom")) return;
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      downOn = e.target;
      stage.setPointerCapture(e.pointerId);
      vel.x = vel.y = 0; moved = 0;
      if (pts.size === 1) drag = { x: e.clientX, y: e.clientY, gx: G.x, gy: G.y, hist: [{ x: e.clientX, y: e.clientY, t: performance.now() }] };
      if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), k: G.k }; drag = null; }
    });
    stage.addEventListener("pointermove", (e) => {
      if (!pts.has(e.pointerId)) return;
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      const r = stage.getBoundingClientRect();
      if (pinch && pts.size === 2) {
        const [a, b] = [...pts.values()], d = Math.hypot(a.x - b.x, a.y - b.y);
        zoomAt((a.x + b.x) / 2 - r.left, (a.y + b.y) / 2 - r.top, (pinch.k * d / pinch.d) / G.k); moved += 10; return;
      }
      if (!drag) return;
      const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      moved = Math.max(moved, Math.hypot(dx, dy));
      if (moved > 4) { stage.classList.add("is-dragging"); if (openState && openState.anchor) closeCard(false); }
      G.x = drag.gx + dx; G.y = drag.gy + dy; T.x = G.x; T.y = G.y; apply();
      drag.hist.push({ x: e.clientX, y: e.clientY, t: performance.now() }); if (drag.hist.length > 6) drag.hist.shift();
    });
    const up = (e) => {
      if (!pts.has(e.pointerId)) return;
      pts.delete(e.pointerId);
      stage.classList.remove("is-dragging");
      if (drag && !reduce) {
        const h = drag.hist, a = h[0], b = h[h.length - 1], dt = Math.max(16, b.t - a.t);
        if (performance.now() - b.t < 80) { vel.x = (b.x - a.x) / dt * 16.67; vel.y = (b.y - a.y) / dt * 16.67; kick(); }
      }
      drag = null; if (pts.size < 2) pinch = null;
    };
    stage.addEventListener("pointerup", up); stage.addEventListener("pointercancel", up);
    stage.addEventListener("click", (e) => {
      if (moved > 4 || e.target.closest(".sst-card, .sst-zoom")) return;
      const t = downOn && downOn.isConnected ? downOn : e.target; downOn = null;
      const n = t.closest("[data-node]"), l = t.closest("[data-leaf]");
      if (l) openLeaf(l.dataset.leaf, l); else if (n) openNode(n.dataset.node, n); else if (openState) closeCard(false);
    });
    stage.addEventListener("dblclick", (e) => { if (e.target.closest("[data-node],[data-leaf]")) return; const r = stage.getBoundingClientRect(); zoomAt(e.clientX - r.left, e.clientY - r.top, 1.8); });
    stage.addEventListener("keydown", (e) => {
      const r = stage.getBoundingClientRect(), k = { ArrowLeft: [60, 0], ArrowRight: [-60, 0], ArrowUp: [0, 60], ArrowDown: [0, -60] }[e.key];
      if (k && e.target === stage) { e.preventDefault(); G.x += k[0]; G.y += k[1]; kick(); }
      if ((e.key === "+" || e.key === "=") && !e.ctrlKey) { e.preventDefault(); zoomAt(r.width / 2, r.height / 2, 1.25); }
      if (e.key === "-" && !e.ctrlKey) { e.preventDefault(); zoomAt(r.width / 2, r.height / 2, 0.8); }
      if (e.key === "0") { e.preventDefault(); fit(false); }
      if (e.key === "Enter" || e.key === " ") { const n = e.target.closest("[data-node]"), l = e.target.closest("[data-leaf]"); if (n || l) { e.preventDefault(); l ? openLeaf(l.dataset.leaf, l) : openNode(n.dataset.node, n); } }
    });
    const zb = document.createElement("div");
    zb.className = "sst-zoom";
    zb.innerHTML = '<button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">&minus;</button><button type="button" data-z="fit" aria-label="Fit the whole tree">&#8982;</button>';
    zb.addEventListener("click", (e) => { const b = e.target.closest("button"); if (!b) return; const r = stage.getBoundingClientRect(); if (b.dataset.z === "fit") fit(false); else zoomAt(r.width / 2, r.height / 2, b.dataset.z === "in" ? 1.35 : 0.74); });
    zb.addEventListener("pointerdown", (e) => e.stopPropagation());
    stage.appendChild(zb);
    const hint = document.createElement("div"); hint.className = "sst-hint"; hint.textContent = "Drag to move · scroll or pinch to zoom · tap a branch";
    stage.appendChild(hint);
  }

  /* ---------- phone: a vine down the left edge ---------- */
  function list(v) {
    const wrap = document.createElement("div");
    wrap.className = "sst-list";
    let d = 0, html = `<div class="sst-sec" data-node="goal" style="--d:0ms"><h2>${esc(D.goal.title)}</h2><p>${esc(D.goal.plain)}</p></div>`;
    D.nodes.filter((n) => n.parent === "goal").forEach((b) => {
      d += 80;
      html += `<div class="sst-sec" data-node="${b.id}" style="--d:${d}ms"><h2>${esc(b.title)}</h2><p>${esc(b.plain)}</p></div>`;
      b.children.forEach((c) => {
        const n = nodes[c], latest = (n.history || [])[0] ? leaves[n.history[0]] : null;
        d += 50;
        html += `<button type="button" class="sst-item${n.status === "ACTIVE" ? " is-hot" : ""}${(n.history || []).some((i) => newIds.has(i)) ? " is-new" : ""}" data-node="${n.id}" style="--d:${d}ms;--w:${1 + n.weight}px">
          <span class="t"><span style="color:${STATUS_COLOR[n.status]};line-height:0">${ICON[n.status]}</span>${esc(n.title)}<small>${esc(n.id)}</small></span>
          <span class="l">${latest ? esc(latest.plain) : esc(STATUS_WORD[n.status])}</span></button>`;
      });
    });
    wrap.innerHTML = html;
    wrap.addEventListener("click", (e) => { const b = e.target.closest("button[data-node]"); if (b) openNode(b.dataset.node, null); });
    v.appendChild(wrap);
  }

  /* ---------- the journey: a trunk through time ---------- */
  function journey(v) {
    const wrap = document.createElement("div");
    wrap.className = "sst-journey";
    const phases = D.phases.slice().sort((a, b) => (a.from < b.from ? 1 : -1));      // newest first
    const days = D.days.slice().sort((a, b) => (a.date < b.date ? 1 : -1));
    let html = "";
    phases.forEach((p, i) => {
      const until = i ? phases[i - 1].from : "9999";
      const pd = days.filter((d) => d.date >= p.from && d.date < until);
      html += `<section class="sst-phase"><h2>${esc(p.title)}</h2><p>${esc(p.plain)}</p><small>From ${esc(fmtDate(p.from))}</small></section>`;
      pd.forEach((d) => {
        html += `<div class="sst-day"><h3>${esc(fmtDate(d.date))}</h3><div class="sst-dl">`;
        if (d.diary) html += `<a class="sst-diary" href="${esc(d.diary)}">Diary entry for this day</a>`;
        d.leaves.slice().reverse().forEach((id) => { const l = leaves[id]; if (l) html += `<button type="button" data-leaf="${esc(id)}"${newIds.has(id) ? ' class="is-new"' : ""}>${esc(l.plain)}</button>`; });
        html += "</div></div>";
      });
    });
    wrap.innerHTML = html || '<p class="sst-empty">Nothing here yet.</p>';
    wrap.addEventListener("click", (e) => { const b = e.target.closest("button[data-leaf]"); if (b) openLeaf(b.dataset.leaf, WIDE.matches ? b : null); });
    v.appendChild(wrap);
  }

  /* ---------- cards ---------- */
  function statusLine(s) { return `<p class="sst-status" style="color:${STATUS_COLOR[s]}">${ICON[s]} ${esc(STATUS_WORD[s])}</p>`; }
  function leafBody(l) {
    let h = "";
    if (l.why) h += `<p>${esc(l.why)}</p>`;
    if (l.explanation) h += `<p>${esc(l.explanation)}</p>`;
    if (l.technical) h += `<p class="sst-tech">${esc(l.technical)}</p>`;
    const rep = (l.links || []).find((x) => /\.md$/.test(x.path)) || (l.links || [])[0];
    if (rep) h += `<a class="sst-quiet" href="${esc(rep.url)}" target="_blank" rel="noopener">Read the full report</a>`;
    if (l.ids && l.ids.length) h += `<p class="sst-id">${esc(l.ids.join(" · "))}</p>`;
    return h;
  }
  function nodeCard(id) {
    const n = nodes[id];
    if (id === "goal") return `<h3>${esc(D.goal.title)}</h3><p>${esc(D.goal.plain)}</p>${D.now ? `<p class="sst-k">Now</p><p>${esc(D.now)}</p>` : ""}`;
    let h = `<h3>${esc(n.title)}</h3><p class="sst-id">${esc(n.id)}${n.id_tree ? " · " + esc(n.id_tree) : ""}</p>${statusLine(n.status)}<p>${esc(n.plain)}</p>`;
    if (n.status_text) h += `<p class="sst-k">Where it stands</p><p>${esc(n.status_text)}</p>`;
    if (n.lesson) h += `<a class="sst-quiet" href="${esc(n.lesson)}">The lesson that explains this</a>`;
    if (n.children) {
      h += `<p class="sst-k">Branches</p><ul class="sst-hist">` + n.children.map((c) => `<li><button type="button" data-open-node="${c}"><small>${esc(STATUS_WORD[nodes[c].status])}</small>${esc(nodes[c].title)}</button></li>`).join("") + "</ul>";
    }
    const hist = n.history || [];
    if (hist.length) {
      h += `<p class="sst-k">History, newest first</p><ul class="sst-hist">`;
      hist.forEach((lid, i) => {
        const l = leaves[lid]; if (!l) return;
        h += `<li${i >= 8 ? " hidden" : ""}><button type="button" data-expand="${esc(lid)}" aria-expanded="false"><small>${esc(fmtWhen(l))}${l.label ? `<span class="sst-label">${esc(l.label)}</span>` : ""}${newIds.has(lid) ? ' <span class="sst-label">new</span>' : ""}</small>${esc(l.plain)}</button></li>`;
      });
      if (hist.length > 8) h += `<li><button type="button" class="sst-more-btn" data-all>Show all ${hist.length}</button></li>`;
      h += "</ul>";
    }
    return h;
  }
  function leafCard(id) {
    const l = leaves[id], n = nodes[l.node];
    return `<h3>${esc(l.plain)}</h3><p class="sst-id">${esc(fmtWhen(l))} · ${esc(l.by)}${l.label ? " · " + esc(l.label) : ""}${n ? ` · <a class="sst-quiet" href="#n=${esc(n.id)}" data-open-node="${esc(n.id)}">${esc(n.title)}</a>` : ""}</p>${leafBody(l)}`;
  }
  function openNode(id, anchor) {
    if (!nodes[id] && id !== "goal") return;
    if (!anchor && WIDE.matches && view === "mission") anchor = host.querySelector(`.sst-stage [data-node="${CSS.escape(id)}"]`);
    if (anchor && WIDE.matches && view === "mission") { const st = host.querySelector(".sst-stage"), P = st && st._pos && st._pos[id]; if (P && !inView(anchor)) st._goTo(P.x + 120, P.y, 1); }
    showCard(nodeCard(id), anchor, "n:" + id);
  }
  function openLeaf(id, anchor) { if (leaves[id]) showCard(leafCard(id), anchor, "l:" + id); }
  function inView(a) { const r = a.getBoundingClientRect(), s = host.querySelector(".sst-stage").getBoundingClientRect(); return r.left > s.left + 20 && r.right < s.right - 400 && r.top > s.top + 10 && r.bottom < s.bottom - 10; }
  function showCard(html, anchor, key) {
    const replacing = !!openState;
    if (openState) removeCard(true);
    const asSheet = !WIDE.matches;
    const card = document.createElement("div");
    card.className = (asSheet ? "sst-sheet sst" : "sst-card") + " sst-pop";
    card.setAttribute("role", "dialog"); card.setAttribute("aria-modal", asSheet ? "true" : "false");
    card.innerHTML = (asSheet ? '<div class="sst-grab" aria-hidden="true"></div>' : "") + '<button type="button" class="sst-x" aria-label="Close">&times;</button>' + html;
    let scrim = null;
    if (asSheet) { scrim = document.createElement("div"); scrim.className = "sst-scrim"; document.body.appendChild(scrim); scrim.addEventListener("click", () => closeCard(false)); document.body.appendChild(card); }
    else { (view === "mission" ? host.querySelector(".sst-stage") || host : host).appendChild(card); }
    openState = { card, scrim, anchor: asSheet ? null : anchor, key, back: document.activeElement };
    if (!replacing) history.pushState({ sst: 1 }, "");
    placeCard();
    card.querySelector(".sst-x").addEventListener("click", () => closeCard(false));
    card.addEventListener("click", (e) => {
      const ex = e.target.closest("[data-expand]"), on = e.target.closest("[data-open-node]"), all = e.target.closest("[data-all]");
      if (on) { e.preventDefault(); openNode(on.dataset.openNode, null); return; }
      if (all) { card.querySelectorAll(".sst-hist li[hidden]").forEach((x) => { x.hidden = false; }); all.parentElement.remove(); return; }
      if (ex) {
        const open = ex.getAttribute("aria-expanded") === "true", nxt = ex.nextElementSibling;
        if (open && nxt) { nxt.remove(); ex.setAttribute("aria-expanded", "false"); }
        else { const div = document.createElement("div"); div.className = "sst-leafbody"; div.innerHTML = leafBody(leaves[ex.dataset.expand]); ex.after(div); ex.setAttribute("aria-expanded", "true"); }
      }
    });
    if (asSheet) sheetDrag(card);
    setTimeout(() => { const f = card.querySelector(".sst-x"); if (f) f.focus({ preventScroll: true }); }, 30);
  }
  function placeCard() {
    if (!openState || !openState.anchor || !openState.card.isConnected) return;
    const card = openState.card, a = openState.anchor.getBoundingClientRect(), box = card.parentElement.getBoundingClientRect();
    const cw = card.offsetWidth, ch = card.offsetHeight;
    let x = a.right - box.left + 14, y = a.top - box.top - 8, ox = "0%";
    if (x + cw > box.width - 12) { x = a.left - box.left - cw - 14; ox = "100%"; }
    if (x < 12) { x = Math.min(Math.max(12, a.left - box.left), box.width - cw - 12); y = a.bottom - box.top + 10; }
    y = Math.min(Math.max(12, y), Math.max(12, box.height - ch - 12));
    card.style.left = x + "px"; card.style.top = y + "px"; card.style.setProperty("--ox", ox);
  }
  function removeCard(instant) {
    const st = openState; openState = null; if (!st) return;
    const kill = () => { st.card.remove(); if (st.scrim) st.scrim.remove(); };
    if (instant || reduce) return kill();
    st.card.classList.add("is-leaving"); if (st.scrim) st.scrim.classList.add("is-leaving");
    setTimeout(kill, 280);
    if (st.back && st.back.focus && document.contains(st.back)) st.back.focus({ preventScroll: true });
  }
  function closeCard(fromPop) { if (!openState) return; removeCard(false); if (!fromPop) history.back(); }
  function sheetDrag(card) {
    let y0 = null, dy = 0;
    card.addEventListener("touchstart", (e) => { if (card.scrollTop > 0) return; y0 = e.touches[0].clientY; dy = 0; card.style.transition = "none"; }, { passive: true });
    card.addEventListener("touchmove", (e) => { if (y0 == null) return; dy = Math.max(0, e.touches[0].clientY - y0); card.style.transform = `translateY(${dy}px)`; }, { passive: true });
    card.addEventListener("touchend", () => { if (y0 == null) return; card.style.transition = ""; if (dy > 110) closeCard(false); else card.style.transform = ""; y0 = null; });
  }
  function focusOn(e) {
    if (e.dataset.leaf) return openLeaf(e.dataset.leaf, WIDE.matches && view === "mission" ? e : null);
    if (WIDE.matches && view === "mission") { const st = host.querySelector(".sst-stage"), P = st._pos[e.dataset.node]; if (P) st._goTo(P.x + 120, P.y, 1.15); setTimeout(() => openNode(e.dataset.node, e), reduce ? 0 : 420); }
    else { e.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" }); if (e.dataset.node !== "goal") setTimeout(() => openNode(e.dataset.node, null), reduce ? 0 : 400); }
  }
})();
