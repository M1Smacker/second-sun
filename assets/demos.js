// Small interactive demos. Material's instant navigation swaps pages without
// reloading, so (re)initialise on every page via document$.
const R_SUN_IN_EARTHS = 109.1;

function initDepthDemo(el) {
  const rp = el.querySelector('[name="rp"]'), rs = el.querySelector('[name="rs"]');
  const out = el.querySelector(".ss-demo__result"), dip = el.querySelector(".ss-demo__lc span");
  const update = () => {
    const depth = (rp.value / (rs.value * R_SUN_IN_EARTHS)) ** 2;   // fraction of light blocked
    el.querySelector('[name="rp_out"]').value = rp.value;
    el.querySelector('[name="rs_out"]').value = rs.value;
    const pct = depth * 100;
    const shown = depth >= 1 ? "100% (the 'planet' covers the whole star: not a planet!)"
      : `${pct < 0.1 ? pct.toFixed(4) : pct.toFixed(2)}% (${Math.round(depth * 1e6).toLocaleString()} ppm)`;
    out.textContent = `Depth: ${shown}`;
    dip.style.height = `${Math.max(2, Math.min(100, Math.sqrt(pct) * 30))}%`; // sqrt scale so tiny dips stay visible
  };
  rp.addEventListener("input", update);
  rs.addEventListener("input", update);
  update();
}

// ---- shared helpers ----
const mk = (tag, props, ...kids) => { const e = Object.assign(document.createElement(tag), props || {}); e.append(...kids); return e; };
function control(label, id, min, max, step, value, fmt) {
  const out = mk("output"), input = mk("input", { type: "range", id, min, max, step, value });
  const show = () => { out.textContent = fmt(Number(input.value)); };
  input.addEventListener("input", show); show();
  return { row: mk("label", { htmlFor: id }, mk("span", {}, label + ": ", out), input), input, show };
}
function fit(canvas, aspect) {
  const dpr = window.devicePixelRatio || 1, w = canvas.getBoundingClientRect().width || 320;
  canvas.style.height = Math.round(w * aspect) + "px";
  canvas.width = Math.round(w * dpr); canvas.height = Math.round(w * aspect * dpr);
  const g = canvas.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { g, w, h: w * aspect };
}
const reduced = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// ---- Demo: two suns and a planet (Chapter 5) ----
// Top-down view; you, the observer, sit at the bottom. A body is "in front" when it is lower on the screen.
// Sizes are not to scale (the planet is drawn far too big so that its dip shows); the orbits are circles.
function initOrbitDemo(el) {
  const MA = 1.1, MB = 0.3, rA = MB / (MA + MB), rB = MA / (MA + MB), RA = 0.04, RB = 0.012, RP = 0.011, LB = 0.004, T = 30, NS = 6000, EXTENT = 4.9;   // star sizes as in TOI-1338 (in units of the stars' separation); the planet is drawn about 4 times too big
  let Q = 6.52, t = 0, playing = false, last = 0, raf = 0, curve = [], hits = [];
  const view = mk("canvas", { role: "img", ariaLabel: "Top-down view of two stars circling each other and a planet circling both" });
  const lc = mk("canvas", { role: "img", ariaLabel: "The brightness over time" });
  const note = mk("p", { className: "ss-demo__result", ariaLive: "polite" });
  const q = control("Planet's year, in orbits of the two stars (TOI-1338 b: 6.52)", "orbit-q", 4, 10, 0.01, Q, (v) => v.toFixed(2));
  const ts = control("Time", "orbit-t", 0, T, 0.01, 0, (v) => v.toFixed(1) + " orbits");
  const play = mk("button", { type: "button", className: "ss-demo__btn" }, "Play");
  el.append(view, lc, mk("div", { className: "ss-demo__ctl" }, q.row, ts.row, play), note);
  const pos = (tt) => {
    const th = 2 * Math.PI * tt, ph = 0.9 + 2 * Math.PI * tt / Q, ap = Math.pow(Q, 2 / 3);
    return { A: [rA * Math.cos(th), rA * Math.sin(th)], B: [-rB * Math.cos(th), -rB * Math.sin(th)], P: [ap * Math.cos(ph), ap * Math.sin(ph)] };
  };
  const overlap = (r1, r2, d) => {                       // area where two discs overlap, by sky distance d
    if (d >= r1 + r2) return 0;
    if (d <= Math.abs(r1 - r2)) return Math.PI * Math.min(r1, r2) ** 2;
    const a = Math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1)), b = Math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2));
    return r1 * r1 * a + r2 * r2 * b - 0.5 * Math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2));
  };
  const sample = (tt) => {
    const { A, B, P } = pos(tt), aA = Math.PI * RA * RA, aB = Math.PI * RB * RB;
    let ea = 0, eb = 0, pa = 0, pb = 0;
    if (B[1] < A[1]) ea = overlap(RA, RB, Math.abs(A[0] - B[0])) / aA;     // one star in front of the other
    if (A[1] < B[1]) eb = overlap(RB, RA, Math.abs(A[0] - B[0])) / aB;
    if (P[1] < A[1]) pa = overlap(RA, RP, Math.abs(A[0] - P[0])) / aA;     // the planet in front of a star
    if (P[1] < B[1]) pb = overlap(RB, RP, Math.abs(B[0] - P[0])) / aB;
    const flux = (x, y) => ((1 - x) + LB * (1 - y)) / (1 + LB);
    return { e: flux(ea, eb), p: flux(pa, pb), planet: pa > 0 };
  };
  function compute() {
    curve = { e: [], p: [] }; hits = []; const durs = []; let run = null;
    for (let i = 0; i <= NS; i++) {
      const tt = T * i / NS, s = sample(tt);
      curve.e.push(s.e); curve.p.push(s.p);
      if (s.planet) { run = run || { a: tt }; run.b = tt; } else if (run) { hits.push((run.a + run.b) / 2); durs.push(run.b - run.a); run = null; }
    }
    if (run) { hits.push((run.a + run.b) / 2); durs.push(run.b - run.a); }
    const gaps = hits.slice(1).map((h, i) => h - hits[i]), spread = gaps.length ? Math.max(...gaps) - Math.min(...gaps) : 0;
    const dur = durs.length ? durs.reduce((x, y) => x + y, 0) / durs.length : 0, f2 = (v) => v.toFixed(2);
    note.textContent = hits.length > 1
      ? `The planet crosses our star ${hits.length} times in ${T} orbits. Each crossing lasts about ${f2(dur)} orbits, but the gaps between crossings (${gaps.map((g) => g.toFixed(2)).join(", ")}) differ by up to ${f2(spread)} orbits` +
        (spread > 0.001 ? `, about ${Math.round(spread / dur)} times as long as a crossing. A search that folds on one steady period would stack the dips in the wrong places.` : ". This planet is in a neat resonance with the stars, so it repeats exactly. Real planets rarely do: try 6.52.")
      : hits.length === 1 ? "The planet crosses our star once in this stretch. Try another year length."
      : "The planet never crosses our star in this stretch. Wandering transits can switch off, so try another year length.";
  }
  let V, L; const size = () => { V = fit(view, 0.78); L = fit(lc, 0.26); };
  function draw() {
    const { g, w, h } = V, sc = Math.min(w, h * 1.28) / (2 * EXTENT) * 0.97, cx = w / 2, cy = h / 2 - 8;
    g.fillStyle = "#070b14"; g.fillRect(0, 0, w, h);
    const X = (x) => cx + x * sc, Y = (y) => cy - y * sc, ap = Math.pow(Q, 2 / 3);
    g.strokeStyle = "rgba(170,177,192,.3)"; g.setLineDash([2, 5]); g.beginPath(); g.arc(cx, cy, ap * sc, 0, 7); g.stroke(); g.setLineDash([]);
    const { A, B, P } = pos(t), disc = (p, r, c, min) => { g.fillStyle = c; g.beginPath(); g.arc(X(p[0]), Y(p[1]), Math.max(min, r * sc), 0, 7); g.fill(); };
    const order = [["B", B, RB, "#ff9f7a", 2], ["A", A, RA, "#ffe9b0", 3], ["P", P, RP, "#9fd0ff", 2.4]].sort((p, q2) => q2[1][1] - p[1][1]);   // farther first
    order.forEach(([, p, r, c, m]) => disc(p, r, c, m));
    g.fillStyle = "#aab1c0"; g.font = "13px system-ui, sans-serif"; g.textAlign = "center";
    g.fillText("you look from here", cx, h - 8); g.beginPath(); g.moveTo(cx, h - 26); g.lineTo(cx - 5, h - 19); g.lineTo(cx + 5, h - 19); g.closePath(); g.fill();
    const lw = L.w, lh = L.h, lo = 0.88, hi = 1.005;
    L.g.fillStyle = "#070b14"; L.g.fillRect(0, 0, lw, lh);
    [["e", "rgba(170,177,192,.55)", 1], ["p", "#e2b45f", 2]].forEach(([k, col, wd]) => {      // grey: the stars eclipsing; amber: the planet
      L.g.strokeStyle = col; L.g.lineWidth = wd; L.g.beginPath();
      curve[k].forEach((f, i) => { const x = lw * i / NS, y = lh - (f - lo) / (hi - lo) * (lh - 6) - 3; i ? L.g.lineTo(x, y) : L.g.moveTo(x, y); }); L.g.stroke();
    });
    L.g.fillStyle = "#fff"; L.g.fillRect(lw * t / T - 0.75, 0, 1.5, lh);
  }
  function frame(now) {
    if (!playing) return;
    t = (t + Math.min(0.1, (now - last) / 1000) / 1.4) % T; last = now;
    ts.input.value = t; ts.show(); draw(); raf = requestAnimationFrame(frame);
  }
  const setPlay = (on) => { playing = on; play.textContent = on ? "Pause" : "Play"; if (on) { last = performance.now(); raf = requestAnimationFrame(frame); } else cancelAnimationFrame(raf); };
  q.input.addEventListener("input", () => { Q = Number(q.input.value); compute(); draw(); });
  ts.input.addEventListener("input", () => { t = Number(ts.input.value); if (!playing) draw(); });
  play.addEventListener("click", () => setPlay(!playing));
  let w0 = 0; new ResizeObserver(() => { const w = el.clientWidth; if (w !== w0) { w0 = w; size(); draw(); } }).observe(el);
  new IntersectionObserver((e) => { if (!e[0].isIntersecting && playing) setPlay(false); }).observe(el);   // never run off-screen
  size(); compute(); draw();
}

// ---- Demo: noise hides a dip (Chapter 7) ----
// A fixed random sequence, so everyone sees the same wiggles; only the sliders change.
function initNoiseDemo(el) {
  const N = 720, D0 = 300, DL = 60;                    // the dip: 60 points starting at point 300
  let s = 7; const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let z = Math.imul(s ^ s >>> 15, 1 | s); z = z + Math.imul(z ^ z >>> 7, 61 | z) ^ z; return ((z ^ z >>> 14) >>> 0) / 4294967296; };
  const gauss = () => Math.sqrt(-2 * Math.log(rnd() + 1e-12)) * Math.cos(2 * Math.PI * rnd());
  const white = Array.from({ length: N }, gauss), red = []; let r = 0;
  for (let i = 0; i < N; i++) { r = 0.99 * r + Math.sqrt(1 - 0.99 * 0.99) * gauss(); red.push(r); }
  const mean = (a) => a.reduce((x, y) => x + y, 0) / a.length, sd = (a) => { const m = mean(a); return Math.sqrt(mean(a.map((x) => (x - m) ** 2))); };
  const cv = mk("canvas", { role: "img", ariaLabel: "A light curve with a dip, noise and an average" });
  const out = mk("p", { className: "ss-demo__result", ariaLive: "polite" });
  const dep = control("Dip depth", "noise-d", 200, 3000, 100, 1000, (v) => v + " ppm");
  const sig = control("Noise on each point", "noise-s", 200, 2000, 100, 800, (v) => v + " ppm");
  const avg = control("Points averaged together (what you see)", "noise-a", 1, 60, 1, 1, (v) => String(v));
  let driftOn = false;
  const drift = mk("button", { type: "button", className: "ss-demo__btn ss-demo__toggle", id: "noise-r" }, "Slow drift: off");
  drift.setAttribute("aria-pressed", "false");
  el.append(cv, mk("div", { className: "ss-demo__ctl" }, dep.row, sig.row, avg.row, drift), out);
  let C; const size = () => { C = fit(cv, 0.5); };
  function draw() {
    const D = Number(dep.input.value), S = Number(sig.input.value), B = Number(avg.input.value), useDrift = driftOn;
    const y = Array.from({ length: N }, (_, i) => (i >= D0 && i < D0 + DL ? -D : 0) + S * white[i] + (useDrift ? 1.2 * S * red[i] : 0));
    const { g, w, h } = C, R = 4500, Y = (v) => h / 2 - Math.max(-R, Math.min(R, v)) / R * (h / 2 - 4);
    g.fillStyle = "#070b14"; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,.09)"; g.fillRect(w * D0 / N, 0, w * DL / N, h);       // where the dip is
    g.fillStyle = "rgba(200,210,230,.55)"; y.forEach((v, i) => g.fillRect(w * i / N, Y(v) - 0.9, 1.8, 1.8));
    g.strokeStyle = "#e2b45f"; g.lineWidth = 2; g.beginPath();
    for (let i = 0; i + B <= N; i += B) { const m = mean(y.slice(i, i + B)); g.moveTo(w * i / N, Y(m)); g.lineTo(w * (i + B) / N, Y(m)); } g.stroke();
    const wins = []; for (let i = 0; i + DL <= N; i += 6) if (i + DL < D0 - 20 || i > D0 + DL + 20) wins.push(mean(y.slice(i, i + DL)));
    const spread = sd(wins), snr = D / spread;
    out.textContent = `A 60-point average wobbles by about ${Math.round(spread)} ppm, so the ${D} ppm dip is ${snr.toFixed(1)} times the wobble (SNR ${snr.toFixed(1)}). ` +
      (snr >= 7 ? "Our detector would call this a dip." : snr >= 3 ? "Visible, but below our bar of 7: it would not be called." : "Lost in the noise.");
  }
  [dep, sig, avg].forEach((c) => c.input.addEventListener("input", draw)); drift.addEventListener("click", () => { driftOn = !driftOn; drift.textContent = "Slow drift: " + (driftOn ? "on" : "off"); drift.setAttribute("aria-pressed", String(driftOn)); draw(); });
  let w0 = 0; new ResizeObserver(() => { const w = el.clientWidth; if (w !== w0) { w0 = w; size(); draw(); } }).observe(el);
  size(); draw();
}

// ---- Demo: a real light curve you can drag and zoom (Chapter 2) ----
// Real data: TOI-1338, TESS sector 98, built by book/tools/make_explorer_data.py (10-minute averages, ppm from 1).
const DATA_BASE = document.currentScript ? new URL("data/", document.currentScript.src).href : "";
async function initExplorerDemo(el) {
  const note = mk("p", { className: "ss-demo__result", ariaLive: "polite" });
  let J;
  try { J = await (await fetch(DATA_BASE + "toi1338-s98.json")).json(); }
  catch (e) { el.append(mk("p", {}, "The light curve could not be loaded. Check your connection and reload.")); return; }
  const cv = mk("canvas", { role: "img", tabIndex: 0, className: "ss-demo__drag", ariaLabel: "The real TOI-1338 light curve. Use the left and right arrow keys to move and plus and minus to zoom." });
  const t0 = J.t0_btjd, dt = J.step_days, tEnd = t0 + J.ppm.length * dt, MIN_WIN = 0.25;
  let a = t0, b = tEnd, C;
  const btn = (label, fn) => { const x = mk("button", { type: "button", className: "ss-demo__btn ss-demo__sm" }, label); x.addEventListener("click", fn); return x; };
  const clamp = (lo, hi) => { const w = Math.max(MIN_WIN, Math.min(tEnd - t0, hi - lo)); lo = Math.max(t0, Math.min(tEnd - w, lo)); a = lo; b = lo + w; };
  const show = (mid, win) => { clamp(mid - win / 2, mid + win / 2); draw(); };
  const zoom = (k) => { const m = (a + b) / 2, w = (b - a) * k; clamp(m - w / 2, m + w / 2); draw(); };
  const pan = (f) => { const w = b - a; clamp(a + f * w, b + f * w); draw(); };
  el.append(cv, mk("div", { className: "ss-demo__row" },
    btn("Earlier", () => pan(-0.3)), btn("Later", () => pan(0.3)), btn("Zoom in", () => zoom(0.5)), btn("Zoom out", () => zoom(2)),
    btn("Whole sector", () => show((t0 + tEnd) / 2, tEnd - t0)), btn("Planet crossing", () => show(J.planet_btjd, 1)), btn("An eclipse", () => show(J.eclipses_btjd[1], 1))), note);
  const size = () => { C = fit(cv, 0.62); };
  function draw() {
    const { g, w, h } = C, L = 62, B = 24, T = 8, pw = w - L - 6, ph = h - B - T;
    g.fillStyle = "#070b14"; g.fillRect(0, 0, w, h);
    const i0 = Math.max(0, Math.floor((a - t0) / dt)), i1 = Math.min(J.ppm.length - 1, Math.ceil((b - t0) / dt));
    let lo = 0, hi = 0, n = 0;
    for (let i = i0; i <= i1; i++) { const v = J.ppm[i]; if (v !== null) { lo = Math.min(lo, v); hi = Math.max(hi, v); n++; } }
    const pad = Math.max(300, (hi - lo) * 0.08); lo -= pad; hi += pad;
    const X = (t) => L + (t - a) / (b - a) * pw, Y = (v) => T + (hi - v) / (hi - lo) * ph, big = hi - lo > 20000;
    g.font = "12px system-ui, sans-serif"; g.fillStyle = "#aab1c0"; g.strokeStyle = "rgba(170,177,192,.18)"; g.textAlign = "right";
    for (let k = 0; k <= 3; k++) { const v = lo + (hi - lo) * k / 3; g.beginPath(); g.moveTo(L, Y(v)); g.lineTo(w - 6, Y(v)); g.stroke(); g.fillText(big ? (v / 1e4).toFixed(1) + "%" : (Math.abs(v) >= 1000 ? (v / 1000).toFixed(1) + "k" : Math.round(v)) + " ppm", L - 4, Y(v) + 4); }
    const span = b - a, step = [0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10].find((s) => span / s <= 6) || 10; g.textAlign = "center";
    for (let tk = Math.ceil(a / step) * step; tk <= b; tk += step) g.fillText(tk.toFixed(step < 1 ? 2 : 0), X(tk), h - 8);
    g.fillStyle = "rgba(220,226,240,.85)";
    for (let i = i0; i <= i1; i++) { const v = J.ppm[i]; if (v !== null) g.fillRect(X(t0 + (i + 0.5) * dt) - 0.9, Y(v) - 0.9, 1.8, 1.8); }
    const tick = (t, col) => { if (t >= a && t <= b) { g.fillStyle = col; g.beginPath(); g.moveTo(X(t), T + 14); g.lineTo(X(t) - 5, T + 3); g.lineTo(X(t) + 5, T + 3); g.closePath(); g.fill(); } };
    J.eclipses_btjd.forEach((t) => tick(t, "#aab1c0")); tick(J.planet_btjd, "#e2b45f");
    const low = n ? Math.min(0, ...J.ppm.slice(i0, i1 + 1).filter((v) => v !== null)) : 0;
    note.textContent = `Showing ${span.toFixed(2)} days (BTJD ${a.toFixed(1)} to ${b.toFixed(1)}). Lowest point in view: ${(-low / 1e4).toFixed(2)}% below normal. Grey markers: one star passing in front of the other. Amber marker: the planet's crossing.`;
  }
  let drag = null;
  cv.addEventListener("pointerdown", (e) => { drag = { x: e.clientX, a, b }; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener("pointermove", (e) => { if (drag) { const d = (e.clientX - drag.x) / cv.getBoundingClientRect().width * (drag.b - drag.a); clamp(drag.a - d, drag.b - d); draw(); } });
  cv.addEventListener("pointerup", () => { drag = null; });
  cv.addEventListener("keydown", (e) => {
    const k = { ArrowLeft: () => pan(-0.2), ArrowRight: () => pan(0.2), "+": () => zoom(0.5), "=": () => zoom(0.5), "-": () => zoom(2) }[e.key];
    if (k) { e.preventDefault(); k(); }
  });
  let w0 = 0; new ResizeObserver(() => { const w = el.clientWidth; if (w !== w0) { w0 = w; size(); draw(); } }).observe(el);
  size(); draw();
}

// ---- Eyes mode (practice): look at a stretch of light curve with nothing marked, say what you see, then see the answer ----
// Practice only: every stretch comes from the real TOI-1338 light curve (sector 98) with fake dips, glitches and real eclipses
// whose answer we know. The hunt's real stars are deliberately NOT connected; that waits until Ahmed says start.
async function initEyesDemo(el) {
  let J;
  try { J = await (await fetch(DATA_BASE + "toi1338-s98.json")).json(); }
  catch (e) { el.append(mk("p", {}, "The practice light curve could not be loaded. Check your connection and reload.")); return; }
  const N = J.ppm.length, dt = J.step_days, t0 = J.t0_btjd, WIN = 216;                    // a stretch is 1.5 days of 10-minute steps
  let s0 = (Date.now() ^ 0x9E3779B9) | 0;
  const rnd = () => { s0 |= 0; s0 = s0 + 0x6D2B79F5 | 0; let z = Math.imul(s0 ^ s0 >>> 15, 1 | s0); z = z + Math.imul(z ^ z >>> 7, 61 | z) ^ z; return ((z ^ z >>> 14) >>> 0) / 4294967296; };
  const ri = (a, b) => a + Math.floor(rnd() * (b - a + 1)), pick = (a) => a[Math.floor(rnd() * a.length)];
  const idx = (t) => Math.round((t - t0) / dt), ecl = J.eclipses_btjd.map(idx), pl = idx(J.planet_btjd);
  const clear = (i, pad) => ![...ecl, pl].some((e) => e > i - pad && e < i + WIN + pad);
  const valid = (i) => J.ppm.slice(i, i + WIN).filter((v) => v !== null).length >= 0.85 * WIN;
  function window_(want) {                                                            // find a start that suits the kind of stretch we want
    for (let k = 0; k < 4000; k++) {
      const i = ri(0, N - WIN - 1);
      if (!valid(i)) continue;
      if (want === "eclipse") { const e = pick(ecl); const j = e - ri(40, WIN - 40); if (j >= 0 && j + WIN < N && valid(j) && ![pl].some((q) => q > j - 36 && q < j + WIN + 36)) return { i: j, e: e - j }; }
      else if (want === "planet") { const j = pl - ri(60, WIN - 60); if (j >= 0 && j + WIN < N && valid(j) && !ecl.some((q) => q > j - 36 && q < j + WIN + 36)) return { i: j }; }
      else if (clear(i, 36)) return { i };
    }
    return { i: 0 };
  }
  function trial(kind) {
    const w = window_(kind === "eclipse" ? "eclipse" : kind === "real" ? "planet" : "quiet"), y = J.ppm.slice(w.i, w.i + WIN);
    const sub = (a, b, v) => { for (let k = a; k < b; k++) if (y[k] !== null) y[k] += v; };
    if (kind === "eclipse") return { y, truth: "odd", kind, box: [w.e - 14, w.e + 14], note: "an eclipse: one star passing in front of the other. It is deep, but it is not a planet." };
    if (kind === "real") return { y, truth: "dip", kind, box: [pl - w.i - 15, pl - w.i + 15], note: "the real planet TOI-1338 b crossing, about 2,000 ppm deep and 5 hours long." };
    if (kind === "dip") { const d = ri(24, 48), a = ri(30, WIN - 30 - d), depth = pick([1500, 2500, 4000]); sub(a, a + d, -depth); return { y, truth: "dip", kind: "dip" + depth, box: [a, a + d], note: `a hidden fake planet, ${depth.toLocaleString("en")} ppm deep and ${Math.round(d / 6)} hours long.` }; }
    if (kind === "spike") { const a = ri(30, WIN - 30); sub(a, a + 3, 9000); return { y, truth: "odd", kind, box: [a - 3, a + 6], note: "a short spike upwards, like a flare or a glitch. A planet only makes dips." }; }
    if (kind === "step") { const a = ri(60, WIN - 60); sub(a, WIN, 3500); return { y, truth: "odd", kind, box: [a - 4, a + 4], note: "a sudden jump in brightness that stays, like an instrument glitch. A planet's dip comes back up." }; }
    return { y, truth: "none", kind: "quiet", box: null, note: "nothing hidden here." };
  }
  function deck(n) {
    const real = n >= 20 ? 1 : 0, e = Math.max(1, Math.round(0.15 * n)), o = Math.max(1, Math.round(0.15 * n)), dp = Math.max(1, Math.round(0.3 * n) - real), q = Math.max(1, n - real - e - o - dp);
    const kinds = [...Array(real).fill("real"), ...Array(e).fill("eclipse"), ...Array(o).fill(0).map(() => pick(["spike", "step"])), ...Array(dp).fill("dip"), ...Array(q).fill("quiet")].slice(0, n);
    while (kinds.length < n) kinds.push("quiet");
    for (let i = kinds.length - 1; i > 0; i--) { const j = ri(0, i); [kinds[i], kinds[j]] = [kinds[j], kinds[i]]; }
    return kinds.map(trial);
  }
  const title = mk("h4", {}, "Eyes mode, practice");
  const stage = mk("div", { className: "ss-eyes" });
  el.append(title, stage);
  const NAMES = { dip: "Dip", none: "No dip", odd: "Odd", unsure: "Not sure" };
  let cards, at, answers, revealed, cv, C, fb, nextBtn, prog, btns;

  function start() {
    stage.replaceChildren(mk("p", {}, "How many light curves this time?"),
      mk("div", { className: "ss-demo__row" }, ...[5, 20, 50, 100].map((n) => { const b = mk("button", { type: "button", className: "ss-demo__btn ss-demo__sm" }, String(n)); b.addEventListener("click", () => begin(n)); return b; })),
      mk("p", { className: "ss-demo__result" }, "Each one is a day and a half of the real TOI-1338 light curve with nothing marked. Say what you see; then the answer is shown. The real stars of the hunt are not in here: that waits until you say start."));
  }
  function begin(n) {
    cards = deck(n); at = 0; answers = [];
    cv = mk("canvas", { role: "img", ariaLabel: "A stretch of light curve. Look for a dip, a glitch or nothing." });
    fb = mk("p", { className: "ss-demo__result", ariaLive: "polite" }); prog = mk("p", { className: "ss-demo__result" });
    btns = ["dip", "none", "odd", "unsure"].map((k, i) => { const b = mk("button", { type: "button", className: "ss-demo__btn ss-demo__sm" }, `${NAMES[k]}`); b.title = `Key ${i + 1}`; b.addEventListener("click", () => answer(k)); return b; });
    nextBtn = mk("button", { type: "button", className: "ss-demo__btn ss-demo__sm", hidden: true }, "Next");
    nextBtn.addEventListener("click", step);
    stage.replaceChildren(prog, cv, mk("div", { className: "ss-demo__row" }, ...btns), fb, nextBtn);
    C = fit(cv, 0.55); show();
  }
  function draw(card, reveal) {
    const { g, w, h } = C, L = 56, B = 22, T = 8, pw = w - L - 6, ph = h - B - T, vals = card.y.filter((v) => v !== null);
    const lo = Math.min(-6000, Math.min(...vals) * 1.1), hi = Math.max(6000, Math.max(...vals) * 1.1);
    const X = (k) => L + k / WIN * pw, Y = (v) => T + (hi - v) / (hi - lo) * ph;
    g.fillStyle = "#070b14"; g.fillRect(0, 0, w, h);
    g.font = "12px system-ui, sans-serif"; g.fillStyle = "#aab1c0"; g.strokeStyle = "rgba(170,177,192,.18)"; g.textAlign = "right";
    [lo, 0, hi].forEach((v) => { g.beginPath(); g.moveTo(L, Y(v)); g.lineTo(w - 6, Y(v)); g.stroke(); g.fillText((v / 1e4).toFixed(1) + "%", L - 4, Y(v) + 4); });
    g.textAlign = "center"; for (let hr = 0; hr < 36; hr += 6) g.fillText(hr + " h", X(hr * 6), h - 6);
    if (reveal && card.box) { g.fillStyle = "rgba(226,180,95,.16)"; g.strokeStyle = "#e2b45f"; g.setLineDash([4, 3]); g.fillRect(X(card.box[0]), T, X(card.box[1]) - X(card.box[0]), ph); g.strokeRect(X(card.box[0]), T, X(card.box[1]) - X(card.box[0]), ph); g.setLineDash([]); }
    g.fillStyle = "rgba(220,226,240,.9)";
    card.y.forEach((v, k) => { if (v !== null) g.fillRect(X(k + 0.5) - 1, Y(v) - 1, 2, 2); });
  }
  function show() { prog.textContent = `Light curve ${at + 1} of ${cards.length}`; fb.textContent = ""; nextBtn.hidden = true; btns.forEach((b) => { b.disabled = false; }); revealed = false; draw(cards[at], false); }
  function answer(k) {
    if (revealed) return; revealed = true;
    const c = cards[at]; answers.push({ k, c }); btns.forEach((b) => { b.disabled = true; }); draw(c, true);
    const ok = k === c.truth;
    fb.textContent = (k === "unsure" ? "Not sure is fine. " : ok ? "Right. " : `Not quite: you said ${NAMES[k].toLowerCase()}. `) + `This one had ${c.note}`;
    nextBtn.textContent = at + 1 < cards.length ? "Next" : "See how you did"; nextBtn.hidden = false; nextBtn.focus({ preventScroll: true });
  }
  function step() { at += 1; if (at < cards.length) show(); else finish(); }
  function finish() {
    const of = (f) => answers.filter(({ c }) => f(c)), hit = (arr) => arr.filter(({ k, c }) => k === c.truth).length, cnt = (arr) => arr.length;
    const dips = of((c) => c.truth === "dip"), faint = of((c) => c.kind === "dip1500"), quiet = of((c) => c.truth === "none"), odd = of((c) => c.truth === "odd");
    const falseAlarms = quiet.filter(({ k }) => k === "dip").length, unsure = answers.filter(({ k }) => k === "unsure").length;
    const lines = [`You looked at ${answers.length} light curves.`,
      dips.length ? `Dips hidden in them: you found ${hit(dips)} of ${cnt(dips)}${faint.length ? ` (the faintest: ${hit(faint)} of ${cnt(faint)})` : ""}.` : "",
      quiet.length ? `Quiet curves: you called ${falseAlarms} of ${cnt(quiet)} a dip (a false alarm).` : "",
      odd.length ? `Odd things (eclipses, spikes, jumps): you spotted ${hit(odd)} of ${cnt(odd)}.` : "",
      unsure ? `You said not sure ${unsure} times, which is an honest answer.` : "",
      "A faint dip is hard to see by eye, and that is the point: this is how it feels to hunt. Nothing here is saved."].filter(Boolean);
    stage.replaceChildren(mk("h4", {}, "How you did"), ...lines.map((l) => mk("p", { className: "ss-demo__result" }, l)), (() => { const b = mk("button", { type: "button", className: "ss-demo__btn" }, "Another sitting"); b.addEventListener("click", start); return b; })());
  }
  el.addEventListener("keydown", (e) => {
    if (!cards || !cv || !cv.isConnected) return;
    const k = { 1: "dip", 2: "none", 3: "odd", 4: "unsure" }[e.key];
    if (k && !revealed) { e.preventDefault(); answer(k); } else if (e.key === "Enter" && revealed && !nextBtn.hidden && document.activeElement !== nextBtn) { e.preventDefault(); step(); }
  });
  let w0 = 0; new ResizeObserver(() => { const w = el.clientWidth; if (w !== w0) { w0 = w; if (cv && cv.isConnected) { C = fit(cv, 0.55); draw(cards[at], revealed); } } }).observe(el);
  start();
}

const DEMOS = { depth: initDepthDemo, orbit: initOrbitDemo, noise: initNoiseDemo, explorer: initExplorerDemo, eyes: initEyesDemo };
const start = () => document.querySelectorAll(".ss-demo[data-demo]").forEach((el) => {
  const init = DEMOS[el.dataset.demo];
  if (init && !el.dataset.ready) { el.dataset.ready = "1"; init(el); }
});
if (typeof document$ !== "undefined") document$.subscribe(start); else start();
