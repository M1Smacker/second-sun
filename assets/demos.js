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

const DEMOS = { depth: initDepthDemo, orbit: initOrbitDemo, noise: initNoiseDemo };
const start = () => document.querySelectorAll(".ss-demo[data-demo]").forEach((el) => {
  const init = DEMOS[el.dataset.demo];
  if (init && !el.dataset.ready) { el.dataset.ready = "1"; init(el); }
});
if (typeof document$ !== "undefined") document$.subscribe(start); else start();
