// Card simulator for testing the engine (MIT). Mirrors the kinds in the brief; my own approximation, not the project's generator.
"use strict";
const E = require("./engine.js");
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function gauss(r) { let u = 0, v = 0; while (u === 0) u = r(); v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
const N = 216;
function noise(r, n, sig, red = 0.35, tau = 6) {         // white noise plus AR(1) red noise of amplitude red*sig and time scale tau points
  const phi = Math.exp(-1 / tau), out = []; let x = 0;
  for (let i = 0; i < n; i++) { x = phi * x + Math.sqrt(1 - phi * phi) * gauss(r); out.push(sig * gauss(r) + red * sig * x); }
  return out;
}
function trap(n, c, D, f, depth) { const m = new Array(n).fill(0), h = D / 2, ing = Math.max(f * D, 1e-9); for (let i = 0; i < n; i++) { const x = Math.abs(i - c); if (x < h) m[i] = -depth * (x <= h - ing ? 1 : (h - x) / ing); } return m; }
const add = (a, b) => a.map((v, i) => v + b[i]);
const ri = (r, lo, hi) => lo + Math.floor(r() * (hi - lo + 1));

function hardNoise(r, sig) {                              // best box of a whole 27 day sector of noise, cut to 36 hours around it
  const S = 3888, y = noise(r, S, sig);
  const base = E.median(y), sp = E.pointScatter(y), boxes = E.boxScan(y, base, sp, 1.3, -1, [24, 36, 48, 60]);
  const b = boxes.reduce((p, q) => (q.s > p.s ? q : p));
  const off = ri(r, 40, 176 - b.D), a0 = Math.min(Math.max(0, b.a - off), S - N);
  return y.slice(a0, a0 + N);
}
function makeCard(kind, seed) {
  const r = rng(seed), sig = [1000, 1000, 1000, 2000, 3000][ri(r, 0, 4)];
  let y = noise(r, N, sig), truth = "noise", inj = {};
  const planet = (sMin, sMax, box = false) => {
    const D = ri(r, 24, 72), c = ri(r, 30 + D / 2, N - 30 - D / 2), s = sMin + r() * (sMax - sMin);
    const depth = s * sig * 1.25 / Math.sqrt(D); const f = box ? 0 : 0.08 + 0.15 * r();
    y = add(y, trap(N, c, D, f, depth)); truth = "planet"; inj = { D_h: D / 6, depth, f, target_strength: s };
  };
  if (kind === "clear") planet(10, 16);
  else if (kind === "limit") planet(5, 8.5);
  else if (kind === "easybox") planet(12, 20, true);
  else if (kind === "hardnoise") { y = hardNoise(r, sig); }
  else if (kind === "quiet") { y = noise(r, N, sig, 0.1); }
  else if (kind === "gapdecoy") { for (let g = 0; g < ri(r, 1, 3); g++) { const a = ri(r, 10, N - 30), L = ri(r, 3, 18); for (let i = a; i < a + L; i++) y[i] = null; } }
  else if (kind === "eclipse") { const D = ri(r, 18, 48), c = ri(r, 40, N - 40), dep = 30000 + r() * 100000; y = add(y, trap(N, c, D, 0.3 + 0.2 * r(), dep)); truth = "eclipse"; inj = { depth: dep }; }
  else if (kind === "spike") { const a = ri(r, 30, N - 40), A = (4 + r() * 8) * sig, tau = 1 + 4 * r(); for (let i = a; i < N; i++) y[i] += A * Math.exp(-(i - a) / tau); truth = "flare"; inj = { amp: A }; }
  else if (kind === "stepup" || kind === "stepdown") { const a = ri(r, 60, N - 60), A = (2000 + r() * 3000) * (kind === "stepup" ? 1 : -1); for (let i = a; i < N; i++) y[i] += A; truth = "step"; inj = { amp: A }; }
  else if (kind === "gapdip") { const g = ri(r, 70, N - 40), L = ri(r, 6, 24), D = ri(r, 6, 24), A = (1500 + r() * 2500) * sig / 1000; for (let i = g - D; i < g; i++) y[i] -= A * (i - (g - D) + 1) / D; for (let i = g; i < g + L; i++) y[i] = null; truth = "gapdip"; inj = { amp: A }; }
  else if (kind === "ramp") { const A = (3000 + r() * 5000) * (r() < 0.5 ? 1 : -1), tau = 20 + 60 * r(); for (let i = 0; i < N; i++) y[i] += A * Math.exp(-i / tau); truth = "ramp"; inj = { amp: A }; }
  else if (kind === "variable") { const P = 36 + r() * 84, A = 1000 + r() * 2000, ph = r() * 6.28; for (let i = 0; i < N; i++) y[i] += A * Math.sin(2 * Math.PI * i / P + ph); truth = "variable"; inj = { P_h: P / 6, amp: A }; }
  return { id: kind + "-" + seed, kind, truth, sig, inj, y: y.map((v) => (v === null ? null : Math.round(v))) };
}
const KINDS = ["clear", "limit", "easybox", "hardnoise", "quiet", "gapdecoy", "eclipse", "spike", "stepup", "stepdown", "gapdip", "ramp", "variable"];
module.exports = { makeCard, KINDS, rng };
