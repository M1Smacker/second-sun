/* Eyes hard test: the card generator. Pure and deterministic from a seed, no DOM. Browser: window.SSEyesHard. Node: module.exports (tested by book/tools/test_eyes_hard.mjs).
   Why it exists: the first test used random quiet stretches of one short sector and boxy fake dips that were easy to see. Real candidates are the machine's BEST dip of a
   whole sector, so the quiet cards here are the best-looking dip found in a fresh, noise-only sector (made by reshuffling this star's own detrended noise in short blocks),
   the fake planets go down to the edge of what anyone can see, and the odd things include a dip that ends at a gap in the data. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api; else root.SSEyesHard = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  const WIN = 216, SECTOR = 5200, BLOCK = 36, BOXES = [18, 24, 36, 48, 72];            // a card is 1.5 days of 10-minute steps; box lengths are 3 to 12 hours
  const mulberry32 = (a) => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let z = Math.imul(a ^ a >>> 15, 1 | a); z = z + Math.imul(z ^ z >>> 7, 61 | z) ^ z; return ((z ^ z >>> 14) >>> 0) / 4294967296; };
  const median = (a) => { const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
  const shuffle = (a, rnd) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  // The star's own noise: the light curve minus a one-day running median, with the eclipses and the planet cut out.
  function prepare(J) {
    const y = J.ppm, N = y.length, t0 = J.t0_btjd, dt = J.step_days, bad = [...J.eclipses_btjd, J.planet_btjd], resid = [];
    for (let i = 0; i < N; i++) {
      if (y[i] === null || bad.some((b) => Math.abs(t0 + i * dt - b) < 0.6)) continue;
      const w = []; for (let k = Math.max(0, i - 72); k <= Math.min(N - 1, i + 72); k++) if (y[k] !== null) w.push(y[k]);
      if (w.length >= 40) resid.push(y[i] - median(w));
    }
    const m = median(resid), sigma = 1.4826 * median(resid.map((v) => Math.abs(v - m))), r = resid.filter((v) => Math.abs(v - m) < 8 * sigma);
    // Pieces of noise that may be reshuffled: leave out any 6 hour piece that already holds an obvious dip or bump of its own (its mean is beyond 3 sigma of a piece mean).
    const c = [0]; for (let i = 0; i < r.length; i++) c.push(c[i] + r[i]);
    const pool = []; for (let s = 0; s + BLOCK <= r.length; s += 9) if (Math.abs((c[s + BLOCK] - c[s]) / BLOCK) <= 3 * sigma / Math.sqrt(BLOCK)) pool.push(s);
    return { raw: y, ecl: bad.slice(0, -1).map((e) => Math.round((e - t0) / dt)), pl: Math.round((J.planet_btjd - t0) / dt), resid: r, pool, sigma };
  }

  // A fresh noise-only stretch: short pieces of the real noise in random order. No eclipse, no planet and no obvious dip is hidden in it, so the strongest dip in a whole
  // sector of it is what noise alone can do (it lands around 5 to 6 on the detector's scale, and past the hunt's threshold of 7 about one time in ten).
  function surrogate(P, rnd, M) {
    const out = [];
    while (out.length < M) { const s = P.pool[Math.floor(rnd() * P.pool.length)]; for (let k = 0; k < BLOCK; k++) out.push(P.resid[s + k]); }
    return out.slice(0, M);
  }

  // The strongest box-shaped dip in a long stretch, scored like the detector scores it (depth over the scatter of a box mean). Returns where it is.
  function topEvent(x, sigma) {
    const c = [0]; for (let i = 0; i < x.length; i++) c.push(c[i] + x[i]);
    let best = { score: -Infinity, t: 0, n: 0 };
    for (const n of BOXES) for (let t = WIN; t + n <= x.length - WIN; t++) {
      const s = -(c[t + n] - c[t]) / Math.sqrt(n) / sigma;
      if (s > best.score) best = { score: s, t, n };
    }
    return best;
  }

  // A planet-like dip: flat bottom, sloping sides. Its strength is stated on the same scale as topEvent (the best box over the dip).
  const profile = (d, ramp) => Array.from({ length: d }, (_, k) => Math.min(1, Math.min(k + 0.5, d - k - 0.5) / ramp));
  function unitSnr(d, ramp) {
    const p = profile(d, ramp); let best = 0;
    for (let n = 1; n <= d; n++) { const o = (d - n) >> 1; let s = 0; for (let k = 0; k < n; k++) s += p[o + k]; best = Math.max(best, s / Math.sqrt(n)); }
    return best;
  }
  const dipDepth = (snr, d, ramp, sigma) => snr * sigma / unitSnr(d, ramp);

  function build(P, spec, seed) {
    const rnd = mulberry32(seed), ri = (a, b) => a + Math.floor(rnd() * (b - a + 1)), sg = P.sigma, k = spec.kind;
    let y, truth = "none", tier = "hardnoise", box = null, note = "", meta = { seed }, wander = true;
    const dip = (a, d, ramp, depth) => { const p = profile(d, ramp); for (let j = 0; j < d; j++) y[a + j] -= depth * p[j]; };
    if (k === "eclipse") {                                                            // a real eclipse of this star, any position, baseline levelled
      const ok = (i) => { let c = 0; for (let j = i; j < i + WIN; j++) if (P.raw[j] !== null) c++; return c >= 0.85 * WIN; };
      let w = 0, e = P.ecl[0];
      for (let tries = 0; tries < 500; tries++) {
        e = P.ecl[ri(0, P.ecl.length - 1)]; const j = e - ri(40, WIN - 40);
        if (j >= 0 && j + WIN < P.raw.length && ok(j) && !(P.pl > j - 36 && P.pl < j + WIN + 36)) { w = j; break; }
      }
      y = P.raw.slice(w, w + WIN);
      const base = median(y.filter((v, j) => v !== null && Math.abs(j - (e - w)) > 40)); y = y.map((v) => (v === null ? null : v - base));
      truth = "odd"; tier = "odd"; box = [e - w - 14, e - w + 14]; meta = { seed, w }; wander = false;
      note = "an eclipse: one star passing in front of the other. It is not a planet.";
    } else if (k === "hardnoise") {                                                   // the best dip of a whole fresh sector, cut out with the event at a random place
      const sec = surrogate(P, rnd, SECTOR), ev = topEvent(sec, sg), off = ri(30, WIN - 30 - ev.n), s = ev.t - off;
      y = sec.slice(s, s + WIN); box = [off - 4, off + ev.n + 4]; meta = { seed, score: Math.round(ev.score * 10) / 10, n: ev.n };
      note = `nothing hidden. This is the best-looking dip of a whole sector of noise: the detector scores it ${meta.score}, and the hunt keeps ${meta.score >= 7 ? "7 and above, so a real hunt would have flagged this one" : "7 and above, so a real hunt would not have flagged it"}. Not sure was a fair answer here.`;
    } else {
      y = surrogate(P, rnd, WIN);
      if (k === "dip") {
        const d = ri(24, 72), ramp = Math.max(2, Math.round((0.1 + 0.2 * rnd()) * d)), a = ri(30, WIN - 30 - d), depth = dipDepth(spec.snr, d, ramp, sg);
        dip(a, d, ramp, depth); truth = "dip"; tier = spec.tier; box = [a - 4, a + d + 4];
        meta = { seed, a, d, ramp, depth: Math.round(depth), snr: Math.round(spec.snr * 10) / 10 };
        note = `a hidden fake planet, strength ${meta.snr} on the detector's scale (the hunt keeps 7 and above), ${Math.round(d / 6)} hours long.${tier === "border" ? " This one is close to the limit of what anyone can see, so Not sure or No dip would also have been fair." : ""}`;
      } else if (k === "spike") {
        const a = ri(30, WIN - 30), w = ri(2, 5), h = Math.round(ri(3, 8) * sg); for (let j = 0; j < w; j++) y[a + j] += h;
        truth = "odd"; tier = "odd"; box = [a - 3, a + w + 3]; meta = { seed, a, w, h }; note = "a short spike upwards, like a flare or a glitch. A planet only makes dips.";
      } else if (k === "step") {
        const a = ri(60, WIN - 60), sign = rnd() < 0.5 ? -1 : 1, mag = Math.round((1.2 + 1.8 * rnd()) * 1000); for (let j = a; j < WIN; j++) y[j] += sign * mag;
        truth = "odd"; tier = "odd"; box = [a - 4, a + 4]; meta = { seed, a, sign, mag };
        note = `a sudden jump ${sign < 0 ? "down" : "up"} that stays. A planet's dip comes back up, so a jump down that never recovers is an instrument glitch.`;
      } else if (k === "gapdip") {
        const d = ri(18, 36), ramp = Math.max(2, Math.round(0.2 * d)), snr = 8 + 4 * rnd(), a = ri(40, WIN - 100 - d), g = ri(24, 60), depth = dipDepth(snr, d, ramp, sg);
        dip(a, d, ramp, depth); for (let j = a + d; j < a + d + g; j++) y[j] = null;
        truth = "odd"; tier = "odd"; box = [a - 3, a + d + 3]; meta = { seed, a, d, g, snr: Math.round(snr * 10) / 10 };
        note = "a dip that ends where a gap in the data begins. This is the classic thruster-firing artifact: the spacecraft jitters just before it fires, then the data stops. Real planets do not know when the thrusters fire.";
      } else throw new Error("unknown card kind " + k);
    }
    if (k !== "gapdip" && k !== "eclipse" && rnd() < 0.4) {                           // decoy gaps: a gap by itself must not give the answer away, only a dip that touches one does
      const g = ri(24, 60);
      for (let tries = 0; tries < 30; tries++) {
        const s = ri(10, WIN - 10 - g);
        if (s + g < box[0] - 40 || s > box[1] + 40) { for (let j = s; j < s + g; j++) y[j] = null; meta.gap = [s, g]; break; }
      }
    }
    if (wander) { const amp = 150 + 250 * rnd(), per = 70 + 230 * rnd(), ph = 6.2832 * rnd(); y = y.map((v, j) => (v === null ? null : v + amp * Math.sin(6.2832 * j / per + ph))); }
    return { y: y.map((v) => (v === null ? null : Math.round(v))), truth, kind: k === "dip" ? "dipSNR" : k, tier, box, meta, note };
  }

  // The official hard test is fixed: 6 clear fake planets, 6 close to the limit, 8 hard-noise cards, 10 odd things (3 eclipses, 2 spikes, 2 jumps, 3 dips at a gap).
  function compose(mode, n, rnd) {
    const seed = () => Math.floor(rnd() * 2147483647), between = (lo, hi) => lo + (hi - lo) * rnd(), specs = [];
    const add = (c, f) => { for (let i = 0; i < c; i++) specs.push({ ...f(), seed: seed() }); };
    let c;
    if (mode === "test") c = { clear: 6, lo: 3, hi: 3, noise: 8, eclipse: 3, spike: 2, step: 2, gap: 3 };
    else {
      const r = (f) => Math.max(1, Math.round(f * n)), lo = Math.ceil(r(0.2) / 2), hi = r(0.2) - lo;
      c = { clear: r(0.2), lo, hi, eclipse: r(0.1), spike: r(0.05), step: r(0.08), gap: r(0.12) };
      c.noise = Math.max(1, n - c.clear - c.lo - c.hi - c.eclipse - c.spike - c.step - c.gap);
    }
    add(c.clear, () => ({ kind: "dip", tier: "clear", snr: between(10, 16) }));
    add(c.lo, () => ({ kind: "dip", tier: "border", snr: between(5, 6.5) }));
    add(c.hi, () => ({ kind: "dip", tier: "border", snr: between(6.5, 8.5) }));
    add(c.noise, () => ({ kind: "hardnoise" }));
    add(c.eclipse, () => ({ kind: "eclipse" })); add(c.spike, () => ({ kind: "spike" })); add(c.step, () => ({ kind: "step" })); add(c.gap, () => ({ kind: "gapdip" }));
    return shuffle(specs, rnd).slice(0, n);
  }

  return { WIN, BOXES, mulberry32, prepare, surrogate, topEvent, unitSnr, dipDepth, build, compose };
});
