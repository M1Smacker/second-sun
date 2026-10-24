// Second Sun feedback engine, prototype (MIT). Plain JavaScript, no dependencies, deterministic.
// measure(y) -> facts ; compose(facts, ctx) -> {lines, used} ; Learner state helpers.
"use strict";

const BIN_H = 10 / 60;                       // one point every 10 minutes
const DURS = [12, 18, 24, 30, 36, 48, 60, 72]; // box lengths in points (2 to 12 hours)

// ---------- small numeric helpers ----------
const isNum = (v) => typeof v === "number" && isFinite(v);
function median(a) { const b = a.filter(isNum).sort((x, y) => x - y); const n = b.length; if (!n) return NaN; return n % 2 ? b[(n - 1) / 2] : 0.5 * (b[n / 2 - 1] + b[n / 2]); }
function mad(a) { const m = median(a); return median(a.map((v) => (isNum(v) ? Math.abs(v - m) : NaN))); }
function mean(a) { const b = a.filter(isNum); return b.length ? b.reduce((s, v) => s + v, 0) / b.length : NaN; }
function std(a) { const b = a.filter(isNum); if (b.length < 2) return NaN; const m = mean(b); return Math.sqrt(b.reduce((s, v) => s + (v - m) ** 2, 0) / (b.length - 1)); }
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// ---------- measurement ----------
function pointScatter(y) {                       // robust scatter of single points from point-to-point differences
  const d = [];
  for (let i = 1; i < y.length; i++) if (isNum(y[i]) && isNum(y[i - 1])) d.push(y[i] - y[i - 1]);
  return 1.4826 * mad(d) / Math.SQRT2;
}

function gapRuns(y, minLen = 2) {                // runs of missing points, plus the two card edges as zero-length "gaps"
  const runs = [{ s: -1, e: -1, edge: true }];
  let i = 0;
  while (i < y.length) {
    if (!isNum(y[i])) { let j = i; while (j + 1 < y.length && !isNum(y[j + 1])) j++; if (j - i + 1 >= minLen) runs.push({ s: i, e: j, edge: false }); i = j + 1; } else i++;
  }
  runs.push({ s: y.length, e: y.length, edge: true });
  return runs;
}

function boxScan(y, base, sigPt, beta, dirn = -1, durs = DURS, minCover = 0.8) { // all box strengths; dirn -1 = dips, +1 = rises
  const n = y.length, cv = [0], cs = [0];
  for (let i = 0; i < n; i++) { cv.push(cv[i] + (isNum(y[i]) ? 1 : 0)); cs.push(cs[i] + (isNum(y[i]) ? y[i] : 0)); }
  const out = [];
  for (const D of durs) for (let a = 0; a + D <= n; a++) {
    const k = cv[a + D] - cv[a]; if (k < minCover * D) continue;
    const m = (cs[a + D] - cs[a]) / k, s = dirn * (m - base) / (sigPt * beta / Math.sqrt(k));
    out.push({ a, D, k, m, s });
  }
  return out;
}

function nonOverlapBest(boxes, exclude) {        // greedy list of non-overlapping boxes by strength
  const sorted = boxes.slice().sort((p, q) => q.s - p.s), kept = exclude ? [exclude] : [];
  const res = [];
  for (const b of sorted) { if (kept.every((k) => b.a + b.D <= k.a || b.a >= k.a + k.D)) { kept.push(b); res.push(b); if (res.length >= 12) break; } }
  return res;
}

function trapezoid(n, c, D, f) {                 // unit-depth trapezoid model centred at c (points), total length D, ingress fraction f
  const m = new Array(n).fill(0), half = D / 2, ing = Math.max(f * D, 1e-9);
  for (let i = 0; i < n; i++) { const x = Math.abs(i - c); if (x >= half) continue; m[i] = x <= half - ing ? 1 : (half - x) / ing; }
  return m;
}

function fitShape(y, base, c, D) {               // least-squares depth for ingress fractions 0..0.5 and durations 0.75D..1.25D
  const lo = Math.max(0, Math.floor(c - D)), hi = Math.min(y.length, Math.ceil(c + D)); let best = null; const byF = {};
  for (const Df of [0.75 * D, D, 1.25 * D]) for (let f = 0; f <= 0.5001; f += 0.05) {
    const mdl = trapezoid(y.length, c, Df, f); let sxy = 0, sxx = 0;
    for (let i = lo; i < hi; i++) if (isNum(y[i])) { sxy += -(y[i] - base) * mdl[i]; sxx += mdl[i] * mdl[i]; }
    if (sxx <= 0) continue; const dep = sxy / sxx; let sse = 0;
    for (let i = lo; i < hi; i++) if (isNum(y[i])) sse += (y[i] - base + dep * mdl[i]) ** 2;
    const key = f.toFixed(2); if (!(key in byF) || sse < byF[key]) byF[key] = sse;
    if (!best || sse < best.sse) best = { f, Df, dep, sse };
  }
  return { ...best, byF };
}

function acfPeak(r, minLag = 12, maxLag = 108) {  // first clear autocorrelation peak (period of a wobble), in points
  const v = r.map((x) => (isNum(x) ? x : 0)), m = mean(r), n = v.length; let best = { lag: 0, r: 0 };
  const den = r.reduce((s, x) => s + (isNum(x) ? (x - m) ** 2 : 0), 0); if (!den) return best;
  for (let L = minLag; L <= maxLag; L++) { let s = 0; for (let i = 0; i + L < n; i++) if (isNum(r[i]) && isNum(r[i + L])) s += (r[i] - m) * (r[i + L] - m); const c = s / den; if (c > best.r) best = { lag: L, r: c }; }
  return best;
}

function measure(y) {
  const n = y.length, F = {};
  const base0 = median(y), sigPt = pointScatter(y);
  // first pass box search with beta = 1 to locate the event, then measure red noise outside it
  let boxes = boxScan(y, base0, sigPt, 1);
  let best = boxes.reduce((p, q) => (q.s > p.s ? q : p), boxes[0]);
  const outside = y.map((v, i) => (i >= best.a - 6 && i < best.a + best.D + 6 ? NaN : v));
  const base = median(outside);
  const hourMeans = []; for (let i = 0; i + 6 <= n; i += 6) { const seg = outside.slice(i, i + 6).filter(isNum); if (seg.length >= 5) hourMeans.push(mean(seg)); }
  const beta = clamp(std(hourMeans) / (sigPt / Math.sqrt(6)), 1, 3);
  boxes = boxScan(y, base, sigPt, beta);
  best = boxes.reduce((p, q) => (q.s > p.s ? q : p), boxes[0]);
  const others = nonOverlapBest(boxes, best);
  const second = others[0] || { s: 0 };
  // shape and edges
  const c = best.a + best.D / 2 - 0.5, sh = fitShape(y, base, c, best.D);
  const s0 = Math.round(c - sh.Df / 2), e0 = Math.round(c + sh.Df / 2);
  const inEv = []; for (let i = Math.max(0, s0); i < Math.min(n, e0); i++) if (isNum(y[i])) inEv.push(i);
  const dChi2 = ((sh.byF["0.50"] ?? sh.sse) - (sh.byF["0.10"] ?? sh.sse)) / (sigPt * sigPt); // >0: flat-ish fits better than V
  // levels before and after the event
  let pre = median(y.slice(Math.max(0, s0 - 42), Math.max(0, s0 - 6))), post = median(y.slice(Math.min(n, e0 + 6), Math.min(n, e0 + 42)));
  if (!isNum(pre)) pre = median(y.slice(0, Math.max(0, s0)));
  if (!isNum(post)) post = median(y.slice(Math.min(n, e0)));
  const nPre = y.slice(Math.max(0, s0 - 42), Math.max(0, s0 - 6)).filter(isNum).length, nPost = y.slice(Math.min(n, e0 + 6), Math.min(n, e0 + 42)).filter(isNum).length;
  const lvlErr = sigPt * beta * Math.sqrt(1 / Math.max(nPre, 1) + 1 / Math.max(nPost, 1));
  // symmetry: first half against second half of the event
  const mid = Math.round(c), h1 = y.slice(Math.max(0, s0), mid).filter(isNum), h2 = y.slice(mid, Math.min(n, e0)).filter(isNum);
  const asym = (h1.length > 2 && h2.length > 2) ? (mean(h1) - mean(h2)) / (sigPt * beta * Math.sqrt(1 / h1.length + 1 / h2.length)) : 0; // >0: second half deeper
  // gaps and edges
  const runs = gapRuns(y);
  let dGap = Infinity, gapSide = "none", gapIsEdge = false;
  for (const g of runs) {
    const after = g.s - e0, before = s0 - g.e - 1;          // points between event end and gap start / gap end and event start
    if (g.s >= e0 - 1 && after < dGap) { dGap = Math.max(after, 0); gapSide = "after"; gapIsEdge = g.edge; }
    if (g.e <= s0 && before < dGap) { dGap = Math.max(before, 0); gapSide = "before"; gapIsEdge = g.edge; }
    if (g.s < e0 && g.e >= s0 && !g.edge) { dGap = 0; gapSide = "inside"; gapIsEdge = false; }
  }
  // rises (spikes, flares)
  const rises = boxScan(y, base, sigPt, beta, +1, [1, 2, 3, 6, 12], 0.67);
  const rise = rises.reduce((p, q) => (q.s > p.s ? q : p), rises[0] || { s: 0, a: 0, D: 1, m: base });
  // global level change (best split point)
  let stepBest = { z: 0, k: 0, d: 0 };
  for (let k = 24; k <= n - 24; k += 2) { const A = y.slice(0, k), B = y.slice(k); const nA = A.filter(isNum).length, nB = B.filter(isNum).length; if (nA < 12 || nB < 12) continue; const d = median(B) - median(A), z = d / (sigPt * beta * Math.sqrt(1 / nA + 1 / nB)); if (Math.abs(z) > Math.abs(stepBest.z)) stepBest = { z, k, d }; }
  // slow drift: straight line through points outside the event
  let sx = 0, sy = 0, sxx = 0, sxy = 0, m = 0;
  outside.forEach((v, i) => { if (isNum(v)) { sx += i; sy += v; sxx += i * i; sxy += i * v; m++; } });
  const slope = m > 2 ? (m * sxy - sx * sy) / (m * sxx - sx * sx) : 0;                  // ppm per point
  const resid = y.map((v, i) => (isNum(v) ? v - (sy / m + slope * (i - sx / m)) : NaN));
  const wob = acfPeak(resid.map((v, i) => (i >= s0 && i < e0 ? NaN : v)));
  let wobAmp = 0; if (wob.lag) { const sm = []; for (let i = 0; i + 6 <= n; i += 3) { const seg = resid.slice(i, i + 6).filter(isNum); if (seg.length >= 4) sm.push(mean(seg)); } wobAmp = (Math.max(...sm) - Math.min(...sm)) / 2; }
  const risesW = boxScan(y, base, sigPt, 1, +1, [1, 2, 3], 0.67);
  const okRise = risesW.filter((b) => { if (b.a < 3 || b.a + b.D > n - 3) return false; const after = median(y.slice(b.a + b.D + 3, b.a + b.D + 15)); return !isNum(after) || after - base < 0.5 * (b.m - base); });
  const riseW = okRise.reduce((p, q) => (q.s > p.s ? q : p), okRise[0] || { s: 0, a: 0, D: 1, m: base });   // a short rise away from the edges that falls back
  let stepW = { z: 0, d: 0, k: 0 };
  for (let k = 18; k <= n - 18; k += 2) { const A = y.slice(Math.max(0, k - 36), k), B = y.slice(k, k + 36); const nA = A.filter(isNum).length, nB = B.filter(isNum).length; if (nA < 12 || nB < 12) continue; const d = median(B) - median(A), z = d / (sigPt * 1.2533 * Math.sqrt(1 / nA + 1 / nB)); if (Math.abs(z) > Math.abs(stepW.z)) stepW = { z, d, k }; }
  const stays = Math.abs(median(y.slice(stepW.k)) - median(y.slice(0, stepW.k))) >= 0.6 * Math.abs(stepW.d);
  const first = median(y.slice(0, 18)), last = median(y.slice(n - 18)), middle = median(y.map((v, i) => (i >= 54 && i < n - 54 && !(i >= s0 - 6 && i < e0 + 6) ? v : NaN)));
  const rampSide = Math.abs(first - middle) >= Math.abs(last - middle) ? "start" : "end";
  const rampPpm = rampSide === "start" ? first - middle : last - middle;
  let preGap = { z: 0, ppm: 0, h: 99 };            // the deepest 2 hour stretch that ends right where a hole in the data begins
  for (const g of runs) { if (g.edge || g.s < 12) continue; const seg = y.slice(g.s - 12, g.s).filter(isNum); if (seg.length < 8) continue; const ppm = base - mean(seg), z = ppm / (sigPt * beta / Math.sqrt(seg.length)); if (z > preGap.z) preGap = { z, ppm, h: g.s * BIN_H }; }
  let maxZ = 0; y.forEach((v) => { if (isNum(v)) maxZ = Math.max(maxZ, Math.abs(v - base) / sigPt); });

  Object.assign(F, {
    sigma_pt: sigPt, beta, base,
    strength: best.s, depth_ppm: base - best.m, depth_pts: (base - best.m) / sigPt,
    dur_h: best.D * BIN_H, fit_dur_h: sh.Df * BIN_H, fit_depth_ppm: sh.dep,
    ingress_h: sh.f * sh.Df * BIN_H, vness: sh.f / 0.5, shape_dchi2: dChi2,
    second: second.s, gap_ratio: best.s / Math.max(second.s, 0.5),
    n_similar: others.filter((b) => b.s >= 0.7 * best.s).length,
    n_in: inEv.length, coverage: inEv.length / Math.max(sh.Df, 1),
    rebound_ppm: post - pre, rebound_z: (post - pre) / lvlErr, rebound_frac: (post - pre) / Math.max(base - best.m, 1),
    asym_z: asym,
    gap_dist_h: dGap === Infinity ? 99 : dGap * BIN_H, gap_side: gapSide, gap_is_edge: gapIsEdge,
    n_gaps: runs.filter((g) => !g.edge).length, missing_frac: y.filter((v) => !isNum(v)).length / n,
    rise_strength: rise.s, rise_ppm: rise.m - base, rise_h: rise.D * BIN_H,
    step_z: stepBest.z, step_ppm: stepBest.d, step_at_h: stepBest.k * BIN_H,
    drift_ppm: slope * n, drift_z: (slope * n) / (sigPt * beta / Math.sqrt(m / 12)),
    wobble_period_h: wob.lag * BIN_H, wobble_acf: wob.r, wobble_amp_ppm: wobAmp,
    max_point_z: maxZ,
    rise_z: riseW.s, rise1_ppm: riseW.m - base, rise1_h: riseW.D * BIN_H,
    stepw_z: stepW.z, step_stays: stays, stepw_ppm: stepW.d, stepw_at_h: stepW.k * BIN_H,
    ramp_ppm: rampPpm, ramp_z: rampPpm / (sigPt * 1.2533 * Math.sqrt(1 / 18 + 1 / Math.max(1, n - 108))), ramp_side: rampSide,
    event_edge_h: Math.min(s0, n - e0) * BIN_H,
    depth7_ppm: 7 * sigPt * beta / Math.sqrt(Math.max(best.k, 1)),
    pregap_z: preGap.z, pregap_ppm: preGap.ppm, pregap_at_h: preGap.h,
    event_start_h: s0 * BIN_H, event_end_h: e0 * BIN_H,
  });
  return F;
}

// ---------- display: every number shown in text comes from here ----------
function fmtInt(v) { return Math.round(v).toLocaleString("en-GB"); }
function r100(v) { return fmtInt(Math.round(v / 100) * 100); }
function dur(v) { return v < 0.9 ? `${Math.max(10, Math.round(v * 6) * 10)} minutes` : `${half(v)} hours`; }
function half(v) { const x = Math.round(v * 2) / 2; return (x % 1 ? x.toFixed(1) : String(x)); }
function display(F) {
  return {
    strength: F.strength.toFixed(1), depth7: r100(F.depth7_ppm), second: Math.max(F.second, 0).toFixed(1), depth: r100(F.depth_ppm), dur: half(F.dur_h),
    ingress: half(F.ingress_h), times: String(Math.round(F.depth_pts)), n_similar: String(F.n_similar), n_in: String(F.n_in),
    rebound: r100(Math.abs(F.rebound_ppm)), gap: half(F.gap_dist_h), rise: r100(F.rise1_ppm), rise_h: dur(F.rise1_h), pregap: r100(F.pregap_ppm), pregap_at: half(F.pregap_at_h), ramp: r100(Math.abs(F.ramp_ppm)), side: F.ramp_side,
    step: r100(Math.abs(F.stepw_ppm)), step_at: half(F.stepw_at_h), drift: r100(Math.abs(F.drift_ppm)),
    period: half(F.wobble_period_h), wob: r100(F.wobble_amp_ppm), beta: F.beta.toFixed(1), scatter: r100(F.sigma_pt),
  };
}

// ---------- lessons: a test on measured facts, the classes it argues for and against, and its sentences ----------
// m = measurement sentence (line 1), w = meaning sentence (line 2), ws = shorter meaning; g = gloss version used for the first few exposures
const G = { strength: " (how far it stands out from the noise)" };
const LESSONS = [
  { id: "deep", prio: 10, when: (F) => F.depth_pts >= 8, for: ["eclipse"], against: ["planet", "noise"],
    m: (d) => `It is ${d.depth} ppm deep, ${d.times} times the scatter of single points.`,
    w: () => `That is far too deep for a planet; one star is passing in front of the other.`, wr: () => `Planets are rarely this deep; an eclipse of the two stars usually is.`, ws: () => `Far too deep for a planet: one star is hiding the other.` },
  { id: "rise", prio: 9, when: (F) => F.rise_z >= 5 && F.rise1_ppm > F.depth_ppm, for: ["flare"], against: ["planet"],
    m: (d) => `The biggest change is a rise of ${d.rise} ppm lasting about ${d.rise_h}.`,
    w: () => `A planet can only block light, so a brightening is the star or the camera.`, wr: () => `A planet can only block light, so a brightening points to the star or camera.`, ws: () => `Planets only block light; a brightening is something else.` },
  { id: "step", prio: 9, when: (F) => Math.abs(F.stepw_z) >= 6 && F.step_stays && Math.abs(F.stepw_ppm) >= 0.6 * F.depth_ppm && F.depth_pts < 8, for: ["step"], against: ["planet"],
    m: (d) => `The level jumps by ${d.step} ppm about ${d.step_at} hours in and stays there.`,
    w: () => `A planet's dip returns to the old level; a jump that stays is usually the instrument.`, wr: () => `A planet's dip returns to the old level; a lasting jump is often the instrument.`, ws: () => `Dips come back up; a jump that stays is usually the instrument.` },
  { id: "gap_touch", prio: 9, when: (F) => F.gap_dist_h <= 1 && !F.gap_is_edge && F.strength >= 3, for: ["gapdip"], against: ["planet"],
    m: (d, F) => (F.gap_dist_h <= 0.25 ? `The dip runs straight into a hole in the data and ends exactly there.` : `The dip ends only ${d.gap} hours before a hole in the data.`),
    w: () => `Holes often mark thruster firings, and the camera wobbles just before them, faking dips.`, wr: () => `Holes often mark thruster firings, and the camera can wobble just before them.`, ws: () => `Thruster firings leave holes, and wobble before them fakes dips.` },
  { id: "drift", prio: 8, when: (F) => Math.abs(F.ramp_z) >= 6 && Math.abs(F.ramp_ppm) >= F.depth_ppm && F.event_edge_h <= 4, for: ["ramp"], against: ["planet"],
    m: (d) => `Near the ${d.side} of the card the level is off by ${d.ramp} ppm from the middle.`,
    w: () => `A slow slide at one end is usually scattered light, not something crossing the star.`, ws: () => `A slide at one end is usually scattered light.` },
  { id: "wobble", prio: 7, when: (F) => F.depth_pts < 8 && F.wobble_acf >= 0.25 && F.wobble_amp_ppm >= 1.5 * F.sigma_pt / Math.sqrt(6), for: ["variable"], against: ["planet"],
    m: (d) => `The brightness rises and falls about every ${d.period} hours, by roughly ${d.wob} ppm.`,
    w: () => `A star that wobbles makes many dips in a row; a planet makes one clean one.`, ws: () => `A wobbling star makes many dips; a planet makes one.` },
  { id: "strong_flat", prio: 6, when: (F) => F.strength >= 9 && F.vness <= 0.6 && F.shape_dchi2 >= 4 && F.depth_pts < 8 && Math.abs(F.rebound_frac) < 0.5, for: ["planet"], against: ["noise"],
    m: (d, F, g) => `Strength ${d.strength}${g ? G.strength : ""}, with a flat floor and ${F.ingress_h < 0.25 ? "very steep sides" : d.ingress + " hour slopes"}.`,
    w: () => `A flat floor between short slopes is how a planet crossing a star looks.`, wr: () => `A flat floor between short slopes is what a planet crossing looks like, among other things.`, ws: () => `Flat floor, short slopes: a planet crossing.` },
  { id: "unique", prio: 6, when: (F) => F.strength >= 6 && F.gap_ratio >= 1.6 && F.depth_pts < 8 && Math.abs(F.rebound_frac) < 0.5, for: ["planet"], against: ["noise"],
    m: (d) => `The best dip scores ${d.strength}; the next best wiggle only ${d.second}.`,
    w: () => `One dip standing well above every other wiggle is what a real crossing does.`, wr: () => `Standing well above every other wiggle is what real crossings do, and some artifacts too.`, ws: () => `Standing far above the rest is what real crossings do.` },
  { id: "not_unique", prio: 5, when: (F) => F.gap_ratio < 1.35 && F.depth_pts < 8, for: ["noise"], against: ["planet"],
    m: (d) => `The best dip scores ${d.strength}, but the next best wiggle scores ${d.second}.`,
    w: () => `When other wiggles are nearly as strong, the best one is usually just noise.`, wr: () => `When other wiggles are nearly as strong, the best one is often noise.`, ws: () => `Nearly equal rivals mean the best one is likely noise.` },
  { id: "many", prio: 5, when: (F) => F.n_similar >= 2 && F.depth_pts < 8, for: ["noise", "variable"], against: ["planet"],
    m: (d) => `${d.n_similar} other dips in this card are at least 70 percent as strong.`,
    w: () => `A real crossing stands alone; a crowd of similar dips is the noise itself.`, wr: () => `A real crossing usually stands alone; a crowd of similar dips is often noise.`, ws: () => `A crowd of similar dips is the noise itself.` },
  { id: "weak", prio: 4, when: (F) => F.strength < 7 && F.depth_pts < 8, for: ["noise"], against: [],
    m: (d, F, g) => `Strength ${d.strength}${g ? G.strength : ""}; the hunt only keeps 7 or more.`,
    w: () => `Searching a whole month of pure noise often turns up one dip this strong.`, ws: () => `A month of pure noise often gives one dip this strong.` },
  { id: "near_limit", prio: 4, when: (F) => F.strength >= 5 && F.strength < 9 && F.gap_ratio >= 1.4 && F.depth_pts < 8, for: ["planet"], against: [],
    m: (d) => `Strength ${d.strength}, close to the hunt's line of 7, lasting about ${d.dur} hours.`,
    w: () => `Near the line, how unique the dip is matters more than how deep it looks.`, ws: () => `Near the line, uniqueness matters more than depth.` },
  { id: "v_shape", prio: 6, when: (F) => F.vness >= 0.8 && F.shape_dchi2 < -4 && F.depth_pts < 8, for: ["eclipse"], against: ["planet"],
    m: (d) => `It is V shaped: each side takes ${d.ingress} hours and there is no flat floor.`,
    w: () => `A clear V with no floor is more like a grazing eclipse than a planet.`, ws: () => `A V with no floor suggests a grazing eclipse.` },
  { id: "shape_unclear", prio: 3, when: (F) => F.strength < 9 && Math.abs(F.shape_dchi2) < 4 && F.depth_pts < 8, for: ["noise", "planet"], against: [],
    m: (d) => `At strength ${d.strength}, a flat floor and a V fit this dip about equally well.`,
    w: () => `So shape cannot decide it; judge by strength and the next best wiggle.`, ws: () => `Shape cannot decide it at this strength.` },
  { id: "few_points", prio: 3, when: (F) => F.n_in <= 18 && F.depth_pts < 8, for: ["noise"], against: [],
    m: (d) => `Only ${d.n_in} points sit inside the dip, so a few low points can make it.`,
    w: () => `A dip built from a handful of points is easy for noise to fake.`, ws: () => `A handful of low points is easy to fake.` },
  { id: "lumpy", prio: 2, when: (F) => F.beta >= 1.5, for: ["noise", "variable"], against: [],
    m: (d) => `The noise is lumpy: hour averages scatter ${d.beta} times more than random points predict.`,
    w: () => `Lumpy noise makes slow wiggles; they are still noise, not something odd.`, wr: () => `Lumpy noise makes slow wiggles, so any dip here needs more support.`, ws: () => `Lumpy wiggles are still just noise.` },
  { id: "returns", prio: 3, when: (F) => isNum(F.rebound_frac) && !F.step_stays && Math.abs(F.rebound_frac) < 0.35 && Math.abs(F.rebound_z) < 3 && F.strength >= 6 && F.depth_pts < 8, for: ["planet"], against: ["step"],
    m: (d) => `After the dip the level comes back to within ${d.rebound} ppm of where it started.`,
    w: () => `Coming back to the same level is what a crossing does; steps do not.`, ws: () => `Crossings come back to the old level.` },
  // truth anchors: used in practice only when nothing stronger argues for the true class; worded as faint, never as clear
  { id: "step_faint", practiceOnly: true, when: () => true, for: ["step"], against: [], anchor: true,
    m: (d) => `The biggest lasting change is ${d.step} ppm, about ${d.step_at} hours in.`,
    w: () => `That step is small next to the noise; compare the left and right halves.`, ws: () => `Compare the left and right halves.` },
  { id: "flare_faint", practiceOnly: true, when: () => true, for: ["flare"], against: [], anchor: true,
    m: (d) => `The biggest rise here is ${d.rise} ppm, lasting about ${d.rise_h}.`,
    w: () => `In this much noise it is hard to see; any short upward jump is worth a look.`, ws: () => `Faint rises hide in noise.` },
  { id: "pregap", prio: 9, when: (F) => F.pregap_z >= 3, for: ["gapdip"], against: ["planet"],
    m: (d) => `In the 2 hours before the hole at ${d.pregap_at} hours, light sags by ${d.pregap} ppm.`,
    w: () => `A sag that ends exactly where data stops is the classic thruster firing fake.`, wr: () => `Sags that end exactly where data stops are often thruster firing effects.`, ws: () => `A sag ending at a hole is a thruster fake.` },
  { id: "gap_faint", practiceOnly: true, when: (F) => F.pregap_at_h < 99, for: ["gapdip"], against: [], anchor: true,
    m: (d) => `Just before the hole at ${d.pregap_at} hours the light sags by ${d.pregap} ppm.`,
    w: () => `Even a faint dip next to a hole is suspect; holes mark thruster firings.`, ws: () => `Dips next to holes are suspect.` },
  { id: "planet_faint", practiceOnly: true, when: () => true, for: ["planet"], against: [], anchor: true,
    m: (d) => `This hidden planet scores only ${d.strength}, below the hunt's line of 7.`,
    w: () => `Some real planets are this faint; at this level nobody can be sure by eye.`, ws: () => `Planets this faint are hard for anyone.` },
];
const NEXT = {
  deep: "how deep it is next to the noise", rise: "whether the change goes up or down", step: "whether the level comes back",
  gap_touch: "where the dip ends", drift: "both ends of the card", wobble: "whether the dips repeat",
  strong_flat: "the floor and the slopes", unique: "the next best wiggle", not_unique: "the next best wiggle",
  many: "how many wiggles look alike", weak: "the strength against 7", near_limit: "how unique it is",
  v_shape: "floor or V", shape_unclear: "the next best wiggle", few_points: "how many points make it", lumpy: "how lumpy the noise is",
  returns: "the level afterwards", step_faint: "the left and right halves", flare_faint: "for short jumps up", gap_faint: "the last points before a hole", pregap: "the last points before a hole", planet_faint: "the strength against 7",
};

// ---------- composing three lines of about 40 words ----------
const numsOf = (t) => t.match(/\d+(?:,\d{3})*(?:\.\d+)?/g) || [];
function lowerFirst(t) { return /^[A-Z][a-z]/.test(t) ? t[0].toLowerCase() + t.slice(1) : t; }
function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
const words = (s) => s.split(/\s+/).filter(Boolean).length;
const ANS = { dip: "Dip", nodip: "No dip", odd: "Odd", unsure: "Not sure" };
const TRUTH_TXT = { planet: "a hidden planet", noise: "only noise", eclipse: "an eclipse", flare: "a spike up", step: "a lasting step", gapdip: "a fake dip at a hole", ramp: "a slow drift", variable: "a wobbling star" };
const TRUTH_ANS = { planet: "dip", noise: "nodip", eclipse: "odd", flare: "odd", step: "odd", gapdip: "odd", ramp: "odd", variable: "odd" };
const ANS_CLASS = { dip: ["planet"], nodip: ["noise"], odd: ["eclipse", "flare", "step", "gapdip", "ramp", "variable"] };

function rankLessons(F, ctx) {
  const practice = ctx.mode === "practice", truth = practice ? ctx.truth : null, st = ctx.state || newLearner(), out = [];
  const wrong = practice && ctx.answer !== "unsure" && TRUTH_ANS[truth] !== ctx.answer;
  const noRealForTruth = practice && !["planet", "noise"].includes(truth) && !LESSONS.some((L) => !L.anchor && L.for.includes(truth) && L.when(F));
  const kindMastered = practice && !wrong && st.kindMastered && st.kindMastered[ctx.kind];
  const shownForKind = (st.kindLeads && st.kindLeads[ctx.kind]) || [];
  for (const L of LESSONS) {
    if (L.practiceOnly && !practice) continue;
    if (!L.when(F)) continue;
    let score = (L.anchor ? (noRealForTruth ? 5 : -1) : 1) + (L.prio || 0) * (practice ? 0.05 : 0.5);                         // anchors only win when nothing else argues for the truth
    if (truth) score += (L.for.includes(truth) ? 3 : 0) - (L.against.includes(truth) ? 4 : 0);
    if (wrong && ANS_CLASS[ctx.answer].some((c) => L.against.includes(c))) score += 2;   // argues against his wrong answer
    if (truth && st.mastered[L.id + ":" + truth] && !wrong) score -= 2;         // fade a lesson he has shown he knows
    score -= 1.5 * st.recentLeads.slice(-4).filter((x) => x === L.id).length;   // anti-repetition over the last 4 cards
    if (kindMastered) score -= 1 * shownForKind.filter((x) => x === L.id).length;  // he knows this kind: prefer a fact not yet shown for it
    out.push({ L, score: score + (hash(ctx.cardId + L.id) % 100) / 1000 });
  }
  return out.sort((p, q) => q.score - p.score);
}

function compose(F, ctx) {
  const d = display(F), ranked = rankLessons(F, ctx), st = ctx.state || newLearner(), practice = ctx.mode === "practice";
  if (!ranked.length) ranked.push({ L: LESSONS.find((x) => x.id === "weak"), score: 0 });
  const lead = ranked[0].L;
  const cueL = practice ? (ranked.find((r) => r.L.for.includes(ctx.truth)) || ranked[0]).L : (ranked[1] || ranked[0]).L;
  const gloss = (st.glossSeen.strength || 0) < 3;
  const pattern = practice ? patternLine(st, ctx) : null;
  const mOpts = gloss ? [lead.m(d, F, true), lead.m(d, F, false)] : [lead.m(d, F, false)];
  const leadNums = numsOf(mOpts[mOpts.length - 1]);
  const repeated = st.recentLeads.slice(-4).includes(lead.id) || (practice && st.kindMastered && st.kindMastered[ctx.kind] && TRUTH_ANS[ctx.truth] === ctx.answer);
  const sup = ranked.find((r) => r.L.id !== lead.id && !r.L.anchor && r.score > 0 && !numsOf(r.L.m(d, F, false)).some((x) => leadNums.includes(x)));
  const detail = F.depth_pts < 8 ? `To reach 7 over ${d.dur} hours it would need about ${d.depth7} ppm; it has ${d.depth} ppm.` : null;
  const swap = !pattern && repeated ? (sup ? "Also measured: " + lowerFirst(sup.L.m(d, F, false)) : detail) : null;
  const wReal = !practice && lead.wr ? lead.wr(d, F) : null;
  const wOpts = pattern ? [pattern[0], pattern[1]] : [swap, wReal || lead.w(d, F), wReal || lead.ws(d, F)].filter(Boolean);
  const cue = NEXT[cueL.id];
  let l3s;
  if (practice) {
    const right = TRUTH_ANS[ctx.truth] === ctx.answer, it = TRUTH_TXT[ctx.truth];
    if (ctx.answer === "unsure") l3s = [`You chose Not sure; it was ${it}. Next time, check ${cue}.`, `Not sure; it was ${it}. Check ${cue}.`];
    else if (right) l3s = [`You said ${ANS[ctx.answer]}, and it was ${it}. Next time, also check ${cue}.`, `${ANS[ctx.answer]} was right: ${it}. Also check ${cue}.`, `Right: ${it}. Also check ${cue}.`];
    else l3s = [`You said ${ANS[ctx.answer]}, but it was ${it}. Next time, check ${cue} first.`, `${ANS[ctx.answer]} missed: it was ${it}. Check ${cue} first.`, `Missed: it was ${it}. Check ${cue} first.`];
  } else {
    const where = F.gap_dist_h <= 2 && !F.gap_is_edge ? "the thruster firing times" : F.depth_pts >= 8 ? "the eclipse timing" : "the second light curve";
    l3s = [`Your answer is locked. These are measurements, not a verdict; now compare ${where}.`, `Locked. Measurements, not a verdict; compare ${where}.`, `Locked. These are measurements, not a verdict. Next, compare ${cue} with ${where}.`];
  }
  // length control: every combination is scored; out of range (36 to 44 words) is heavily penalised
  let best = null;
  mOpts.forEach((m, mi) => wOpts.forEach((w, wi) => l3s.forEach((l3) => {
    const lines = [m, w, l3], n = lines.reduce((t, l) => t + words(l), 0);
    const cost = Math.abs(n - 40) + (n > 44 || n < 36 ? 100 : 0) + (gloss && mi > 0 ? 3 : 0) + (swap && wOpts[wi] !== swap ? 2 : 0) + (wi === wOpts.length - 1 && wOpts.length > 1 ? 0.5 : 0);
    if (!best || cost < best.cost) best = { lines, n, cost, usedGloss: gloss && mi === 0, usedSwap: !!swap && w === swap };
  })));
  return { lines: best.lines, words: best.n, swapped: best.usedSwap, lead: lead.id, cue: cueL.id, pattern: !!pattern, gloss: best.usedGloss && /how far it stands out/.test(best.lines[0]), display: d };
}

// ---------- learner model ----------
function newLearner() { return { history: [], recentLeads: [], lessonLog: {}, mastered: {}, lastPatternAt: -99, glossSeen: {}, kindLog: {}, kindMastered: {}, kindLeads: {} }; }
function bandOf(F) { return F.strength < 5 ? "under 5" : F.strength < 7 ? "5 to 7" : F.strength < 10 ? "7 to 10" : "10 or more"; }
function record(st, F, ctx, out) {
  const right = TRUTH_ANS[ctx.truth] === ctx.answer;
  const ok = ctx.answer !== "unsure" && right;
  st.history.push({ kind: ctx.kind, truth: ctx.truth, answer: ctx.answer, right, band: bandOf(F), gapNear: F.gap_dist_h <= 0.5 && !F.gap_is_edge, lumpy: F.beta >= 1.5, lead: out.lead });
  st.recentLeads.push(out.lead);
  const key = out.lead + ":" + ctx.truth, log = (st.lessonLog[key] = st.lessonLog[key] || []);
  log.push(right ? 1 : 0); if (log.length >= 5 && log.slice(-5).reduce((a, b) => a + b, 0) >= 4) st.mastered[key] = true;
  if (log.length >= 2 && log.slice(-2).every((v) => v === 0)) delete st.mastered[key];   // lose mastery after two misses
  if (out.pattern) st.lastPatternAt = st.history.length;
  const kl = (st.kindLog[ctx.kind] = st.kindLog[ctx.kind] || []); kl.push(right ? 1 : 0);
  const last5 = kl.slice(-5); st.kindMastered[ctx.kind] = last5.length === 5 && last5.reduce((a, b) => a + b, 0) >= 4;
  (st.kindLeads[ctx.kind] = st.kindLeads[ctx.kind] || []).push(out.lead);
  if (out.gloss) st.glossSeen.strength = (st.glossSeen.strength || 0) + 1;
}
function patternLine(st, ctx) {                                                       // at most once every 6 cards, from the last 12 answers
  if (st.history.length - st.lastPatternAt < 6) return null;
  const h = st.history.slice(-12);
  const fa = h.filter((x) => x.answer === "dip" && x.truth !== "planet");
  if (fa.length >= 4) { const weak = fa.filter((x) => x.band === "under 5" || x.band === "5 to 7").length; if (weak / fa.length >= 0.6) return [`Pattern: ${weak} of your last ${fa.length} false alarms scored under 7, below the hunt's line.`, `Pattern: ${weak} of ${fa.length} false alarms scored under 7.`]; }
  const gm = h.filter((x) => x.gapNear && x.truth === "gapdip" && x.answer !== "odd");
  if (gm.length >= 3) return [`Pattern: you missed ${gm.length} of the last ${h.filter((x) => x.truth === "gapdip").length} dips that run into a data hole.`, `Pattern: ${gm.length} hole dips missed lately.`];
  const oddNoise = h.filter((x) => x.answer === "odd" && x.truth === "noise");
  if (oddNoise.length >= 3) return [`Pattern: ${oddNoise.length} of your recent Odd answers were plain noise; lumpy noise is still noise.`, `Pattern: ${oddNoise.length} recent Odd answers were plain noise.`];
  const unsure = h.filter((x) => x.answer === "unsure").length, wrong = h.filter((x) => !x.right).length;
  if (h.length >= 12 && unsure === 0 && wrong >= 4) return [`Pattern: ${wrong} wrong and 0 Not sure in 12 cards; Not sure is a fair answer.`, `Pattern: ${wrong} wrong, 0 Not sure in 12 cards.`];
  return null;
}

if (typeof module !== "undefined") module.exports = { measure, display, compose, newLearner, record, LESSONS, TRUTH_ANS, words, boxScan, pointScatter, median };
