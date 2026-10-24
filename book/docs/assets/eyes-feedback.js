/* Eyes feedback: the three lines under a card, computed from the card's own dots. Pure and deterministic, no DOM. Browser: window.SSFeedback. Node: module.exports (tested by book/tools/test_eyes_feedback.mjs).
   measure(y, sigT) -> facts about the card; compose(F, ctx) -> three lines of 36 to 44 words, every number taken from the facts.
   Based on the prototype Claude AI wrote on 24 Oct 2026 (MIT), changed after the Compass review (research/compass-reviews/2026-10-24-feedback-engine.md):
   strength is the hunt's own score (eyes-strength.js), the lead lesson never looks at the true label, a wrong answer never says "missed" about a false alarm,
   every lesson has several wordings so the sentences do not repeat, and a card that nearly matches a known artifact is never called plain noise. */
(function (root, factory) {
  const api = factory(typeof module === "object" && module.exports ? require("./eyes-strength.js") : root.SSStrength);
  if (typeof module === "object" && module.exports) module.exports = api; else root.SSFeedback = api;
})(typeof self !== "undefined" ? self : this, function (SS) {
  "use strict";
  const BIN_H = 10 / 60;                                   // one point every 10 minutes

  // ---------- small numeric helpers ----------
  const isNum = (v) => typeof v === "number" && isFinite(v);
  const median = SS.median, clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  function mad(a) { const m = median(a); return median(a.map((v) => (isNum(v) ? Math.abs(v - m) : NaN))); }
  function mean(a) { const b = a.filter(isNum); return b.length ? b.reduce((s, v) => s + v, 0) / b.length : NaN; }
  function std(a) { const b = a.filter(isNum); if (b.length < 2) return NaN; const m = mean(b); return Math.sqrt(b.reduce((s, v) => s + (v - m) ** 2, 0) / (b.length - 1)); }

  // ---------- measurement ----------
  function pointScatter(y) {                               // robust scatter of single points from point-to-point differences
    const d = [];
    for (let i = 1; i < y.length; i++) if (isNum(y[i]) && isNum(y[i - 1])) d.push(y[i] - y[i - 1]);
    return 1.4826 * mad(d) / Math.SQRT2;
  }
  function gapRuns(y, minLen = 2) {                        // runs of missing points, plus the two card edges as zero-length "gaps"
    const runs = [{ s: -1, e: -1, edge: true }];
    let i = 0;
    while (i < y.length) {
      if (!isNum(y[i])) { let j = i; while (j + 1 < y.length && !isNum(y[j + 1])) j++; if (j - i + 1 >= minLen) runs.push({ s: i, e: j, edge: false }); i = j + 1; } else i++;
    }
    runs.push({ s: y.length, e: y.length, edge: true });
    return runs;
  }
  function boxScan(y, base, sigPt, beta, dirn, durs, minCover) {   // short-box scan for rises and level changes (not the hunt's strength)
    const n = y.length, cv = [0], cs = [0], out = [];
    for (let i = 0; i < n; i++) { cv.push(cv[i] + (isNum(y[i]) ? 1 : 0)); cs.push(cs[i] + (isNum(y[i]) ? y[i] : 0)); }
    for (const D of durs) for (let a = 0; a + D <= n; a++) {
      const k = cv[a + D] - cv[a]; if (k < minCover * D) continue;
      const m = (cs[a + D] - cs[a]) / k;
      out.push({ a, D, k, m, s: dirn * (m - base) / (sigPt * beta / Math.sqrt(k)) });
    }
    return out;
  }
  function nonOverlapBest(boxes, exclude) {                // greedy list of non-overlapping boxes by strength
    const sorted = boxes.slice().sort((p, q) => q.s - p.s), kept = exclude ? [exclude] : [], res = [];
    for (const b of sorted) { if (kept.every((k) => b.a + b.D <= k.a || b.a >= k.a + k.D)) { kept.push(b); res.push(b); if (res.length >= 12) break; } }
    return res;
  }
  function trapezoid(n, c, D, f) {
    const m = new Array(n).fill(0), half = D / 2, ing = Math.max(f * D, 1e-9);
    for (let i = 0; i < n; i++) { const x = Math.abs(i - c); if (x >= half) continue; m[i] = x <= half - ing ? 1 : (half - x) / ing; }
    return m;
  }
  function fitShape(y, base, c, D) {                       // least-squares depth for ingress fractions 0..0.5 and durations 0.75D..1.25D
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
  function acfPeak(r, minLag = 12, maxLag = 108) {         // first clear autocorrelation peak (period of a wobble), in points
    const v = r.map((x) => (isNum(x) ? x : 0)), m = mean(r), n = v.length; let best = { lag: 0, r: 0 };
    const den = r.reduce((s, x) => s + (isNum(x) ? (x - m) ** 2 : 0), 0); if (!den) return best;
    for (let L = minLag; L <= maxLag; L++) { let s = 0; for (let i = 0; i + L < n; i++) if (isNum(r[i]) && isNum(r[i + L])) s += (r[i] - m) * (r[i + L] - m); const c = s / den; if (c > best.r) best = { lag: L, r: c }; }
    return best;
  }

  // The thresholds at which a lesson fires, kept in one place so the audit tests can read them.
  const T = { rise: 5, step: 6, ramp: 6, pregap: 3, near: 0.85 };

  function measure(y, sigT) {
    const n = y.length, F = {};
    const sigPt = pointScatter(y);
    // strength: the hunt's own box score, with the scale taken from the sector (eyes-strength.js)
    const hb = SS.huntBoxes(y, sigT), med = hb.med;
    const boxes = hb.boxes.map((b) => ({ a: b.a, D: b.w, m: b.m, s: b.s }));
    let best = boxes.length ? boxes.reduce((p, q) => (q.s > p.s ? q : p)) : { a: 0, D: 18, m: med, s: 0 };
    const kIn = (a, D) => { let k = 0; for (let i = a; i < Math.min(n, a + D); i++) if (isNum(y[i])) k++; return k; };
    best.k = kIn(best.a, best.D);
    const outside = y.map((v, i) => (i >= best.a - 6 && i < best.a + best.D + 6 ? NaN : v));
    const base = median(outside);
    const hourMeans = []; for (let i = 0; i + 6 <= n; i += 6) { const seg = outside.slice(i, i + 6).filter(isNum); if (seg.length >= 5) hourMeans.push(mean(seg)); }
    const beta = clamp(std(hourMeans) / (sigPt / Math.sqrt(6)), 1, 3);          // 1 = white noise, up to 3 = lumpy
    const others = nonOverlapBest(boxes, best), second = others[0] || { s: 0 };
    // shape and edges
    const c = best.a + best.D / 2 - 0.5, sh = fitShape(y, base, c, best.D);
    const s0 = Math.round(c - sh.Df / 2), e0 = Math.round(c + sh.Df / 2);
    const inEv = []; for (let i = Math.max(0, s0); i < Math.min(n, e0); i++) if (isNum(y[i])) inEv.push(i);
    const dChi2 = ((sh.byF["0.50"] ?? sh.sse) - (sh.byF["0.10"] ?? sh.sse)) / (sigPt * sigPt);   // > 0: flat-ish fits better than V
    let pre = median(y.slice(Math.max(0, s0 - 42), Math.max(0, s0 - 6))), post = median(y.slice(Math.min(n, e0 + 6), Math.min(n, e0 + 42)));
    if (!isNum(pre)) pre = median(y.slice(0, Math.max(0, s0)));
    if (!isNum(post)) post = median(y.slice(Math.min(n, e0)));
    const nPre = y.slice(Math.max(0, s0 - 42), Math.max(0, s0 - 6)).filter(isNum).length, nPost = y.slice(Math.min(n, e0 + 6), Math.min(n, e0 + 42)).filter(isNum).length;
    const lvlErr = sigPt * beta * Math.sqrt(1 / Math.max(nPre, 1) + 1 / Math.max(nPost, 1)), known = isNum(pre) && isNum(post);
    const mid = Math.round(c), h1 = y.slice(Math.max(0, s0), mid).filter(isNum), h2 = y.slice(mid, Math.min(n, e0)).filter(isNum);
    // gaps and edges
    const runs = gapRuns(y);
    let dGap = Infinity, gapSide = "none", gapIsEdge = false;
    for (const g of runs) {
      const after = g.s - e0, before = s0 - g.e - 1;
      if (g.s >= e0 - 1 && after < dGap) { dGap = Math.max(after, 0); gapSide = "after"; gapIsEdge = g.edge; }
      if (g.e <= s0 && before < dGap) { dGap = Math.max(before, 0); gapSide = "before"; gapIsEdge = g.edge; }
      if (g.s < e0 && g.e >= s0 && !g.edge) { dGap = 0; gapSide = "inside"; gapIsEdge = false; }
    }
    // slow drift: straight line through the points outside the event
    let sx = 0, sy = 0, sxx = 0, sxy = 0, m = 0;
    outside.forEach((v, i) => { if (isNum(v)) { sx += i; sy += v; sxx += i * i; sxy += i * v; m++; } });
    const slope = m > 2 ? (m * sxy - sx * sy) / (m * sxx - sx * sx) : 0;
    const resid = y.map((v, i) => (isNum(v) ? v - (sy / m + slope * (i - sx / m)) : NaN));
    const wob = acfPeak(resid.map((v, i) => (i >= s0 && i < e0 ? NaN : v)));
    let wobAmp = 0; if (wob.lag) { const sm = []; for (let i = 0; i + 6 <= n; i += 3) { const seg = resid.slice(i, i + 6).filter(isNum); if (seg.length >= 4) sm.push(mean(seg)); } wobAmp = (Math.max(...sm) - Math.min(...sm)) / 2; }
    // short rises (flares, glitches) that fall back
    const risesW = boxScan(y, base, sigPt, 1, +1, [1, 2, 3], 0.67);
    const okRise = risesW.filter((b) => { if (b.a < 3 || b.a + b.D > n - 3) return false; const after = median(y.slice(b.a + b.D + 3, b.a + b.D + 15)); return !isNum(after) || after - base < 0.5 * (b.m - base); });
    const riseW = okRise.reduce((p, q) => (q.s > p.s ? q : p), okRise[0] || { s: 0, a: 0, D: 1, m: base });
    // a level that jumps and stays
    let stepW = { z: 0, d: 0, k: 0 };
    for (let k = 18; k <= n - 18; k += 2) { const A = y.slice(Math.max(0, k - 36), k), B = y.slice(k, k + 36); const nA = A.filter(isNum).length, nB = B.filter(isNum).length; if (nA < 12 || nB < 12) continue; const d = median(B) - median(A), z = d / (sigPt * 1.2533 * Math.sqrt(1 / nA + 1 / nB)); if (Math.abs(z) > Math.abs(stepW.z)) stepW = { z, d, k }; }
    const stays = Math.abs(median(y.slice(stepW.k)) - median(y.slice(0, stepW.k))) >= 0.6 * Math.abs(stepW.d);
    const orBase = (v) => (isNum(v) ? v : base);                                          // an end or the middle that is all hole counts as the base level, not as a slide
    const first = orBase(median(y.slice(0, 18))), last = orBase(median(y.slice(n - 18))), middle = orBase(median(y.map((v, i) => (i >= 54 && i < n - 54 && !(i >= s0 - 6 && i < e0 + 6) ? v : NaN))));
    const rampSide = Math.abs(first - middle) >= Math.abs(last - middle) ? "start" : "end";
    const rampPpm = rampSide === "start" ? first - middle : last - middle;
    let preGap = { z: 0, ppm: 0, h: 99 };                  // the deepest 2 hour stretch that ends right where a hole in the data begins
    for (const g of runs) { if (g.edge || g.s < 12) continue; const seg = y.slice(g.s - 12, g.s).filter(isNum); if (seg.length < 8) continue; const ppm = base - mean(seg), z = ppm / (sigPt * beta / Math.sqrt(seg.length)); if (z > preGap.z) preGap = { z, ppm, h: g.s * BIN_H }; }
    const sigW = sigT[best.D] || sigT[Object.keys(sigT)[0]];
    Object.assign(F, {
      sigma_pt: sigPt, beta, base,
      strength: best.s, depth_ppm: med - best.m, depth_pts: (med - best.m) / sigPt,
      dur_h: best.D * BIN_H, fit_dur_h: sh.Df * BIN_H, ingress_h: sh.f * sh.Df * BIN_H, vness: sh.f / 0.5, shape_dchi2: dChi2,
      second: second.s, gap_ratio: best.s / Math.max(second.s, 0.5), n_similar: others.filter((b) => b.s >= 0.7 * best.s).length,
      n_in: inEv.length, rebound_ppm: known ? post - pre : 0, rebound_z: known ? (post - pre) / lvlErr : 0, rebound_frac: known ? (post - pre) / Math.max(med - best.m, 1) : 1,   // unknown (event at the card edge): no evidence either way
      gap_dist_h: dGap === Infinity ? 99 : dGap * BIN_H, gap_side: gapSide, gap_is_edge: gapIsEdge, n_gaps: runs.filter((g) => !g.edge).length,
      drift_ppm: slope * n, wobble_period_h: wob.lag * BIN_H, wobble_acf: wob.r, wobble_amp_ppm: wobAmp,
      rise_z: riseW.s, rise1_ppm: riseW.m - base, rise1_h: riseW.D * BIN_H,
      stepw_z: stepW.z, step_stays: stays, stepw_ppm: stepW.d, stepw_at_h: stepW.k * BIN_H,
      ramp_ppm: rampPpm, ramp_z: rampPpm / (sigPt * 1.2533 * Math.sqrt(1 / 18 + 1 / Math.max(1, n - 108))), ramp_side: rampSide,
      event_edge_h: Math.min(s0, n - e0) * BIN_H, depth7_ppm: 7 * sigW,
      pregap_z: preGap.z, pregap_ppm: preGap.ppm, pregap_at_h: preGap.h,
    });
    // how close the card comes to each known artifact test without firing it (so "pure noise" is never said about a card that nearly matches one)
    const ratios = [["a level step", stays ? Math.abs(stepW.z) / T.step : 0], ["a short brightening", riseW.s / T.rise], ["a sag before a hole", preGap.z / T.pregap], ["a slide at one end", Math.abs(F.ramp_z) / T.ramp]];
    const nearest = ratios.reduce((p, q) => (q[1] > p[1] ? q : p));
    F.near_name = nearest[0]; F.near_ratio = nearest[1];
    return F;
  }

  // ---------- display: every number shown in text comes from here ----------
  const fmtInt = (v) => Math.round(v).toLocaleString("en-GB");
  const r100 = (v) => fmtInt(Math.round(v / 100) * 100);
  const half = (v) => { const x = Math.round(v * 2) / 2; return (x % 1 ? x.toFixed(1) : String(x)); };
  const dur = (v) => (v < 0.9 ? `${Math.max(10, Math.round(v * 6) * 10)} minutes` : `${half(v)} hours`);
  function display(F) {
    return {
      strength: F.strength.toFixed(1), depth7: r100(F.depth7_ppm), second: Math.max(F.second, 0).toFixed(1), depth: r100(F.depth_ppm), dur: half(F.dur_h),
      ingress: half(F.ingress_h), times: String(Math.round(F.depth_pts)), n_similar: String(F.n_similar), n_in: String(F.n_in),
      rebound: r100(Math.abs(F.rebound_ppm)), gap: half(F.gap_dist_h), rise: r100(F.rise1_ppm), rise_h: dur(F.rise1_h), pregap: r100(F.pregap_ppm), pregap_at: half(F.pregap_at_h),
      ramp: r100(Math.abs(F.ramp_ppm)), side: F.ramp_side, step: r100(Math.abs(F.stepw_ppm)), step_at: half(F.stepw_at_h), drift: r100(Math.abs(F.drift_ppm)),
      period: half(F.wobble_period_h), wob: r100(F.wobble_amp_ppm), beta: F.beta.toFixed(1), near: F.near_name,
    };
  }

  // ---------- lessons: a test on the measured facts, the classes it argues for and against, and its wordings ----------
  // m = measurement sentence(s) for line 1 (the first few times it may carry a gloss); w = meaning sentences for line 2 (several wordings, all true in every mode: they say "often", never "is").
  // for/against name the kinds of card the lesson points towards or away from; they are used only AFTER the answer is known, to word the closing cue, never to choose the lead lesson.
  const G = " (how far it stands out from the noise)";
  const LESSONS = [
    { id: "deep", prio: 10, when: (F) => F.depth_pts >= 8, for: ["eclipse"], against: ["planet", "noise"],
      m: [(d) => `It is ${d.depth} ppm deep, ${d.times} times the scatter of single points.`, (d) => `The dip is ${d.depth} ppm deep, about ${d.times} times the scatter of single points.`],
      w: ["That is far too deep for a planet; one star is passing in front of the other.", "A planet this deep would be unheard of here; this looks like one star hiding the other.", "Depth like this points to an eclipse of the two stars, not a planet."] },
    { id: "rise", prio: 9, when: (F) => F.rise_z >= T.rise && F.rise1_ppm > F.depth_ppm, for: ["flare"], against: ["planet"],
      m: [(d) => `The biggest change is a rise of ${d.rise} ppm lasting about ${d.rise_h}.`, (d) => `The largest feature is a brightening of ${d.rise} ppm that lasts about ${d.rise_h}.`],
      w: ["A planet can only block light, so a brightening comes from the star or the camera.", "Planets only dim a star, so a brief brightening points to a flare or a glitch.", "A brightening cannot be a planet; look for a flare or an instrument glitch."] },
    { id: "step", prio: 9, when: (F) => Math.abs(F.stepw_z) >= T.step && F.step_stays && Math.abs(F.stepw_ppm) >= 0.6 * F.depth_ppm && F.depth_pts < 8, for: ["step"], against: ["planet"],
      m: [(d) => `The level jumps by ${d.step} ppm about ${d.step_at} hours in and stays there.`, (d) => `About ${d.step_at} hours in, the level shifts by ${d.step} ppm and does not return.`],
      w: ["A planet's dip returns to the old level; a jump that stays is usually the instrument.", "After a transit the light comes back; a lasting shift points to the camera.", "Dips come back up; a level that stays changed is usually an instrument effect."] },
    { id: "gap_touch", prio: 9, when: (F) => F.gap_dist_h <= 1 && !F.gap_is_edge && F.strength >= 3, for: ["gapdip"], against: ["planet"],
      m: [(d, F) => (F.gap_dist_h <= 0.25 ? "The dip runs straight into a hole in the data and ends exactly there." : `The dip ends only ${d.gap} hours before a hole in the data.`), (d, F) => (F.gap_dist_h <= 0.25 ? "The dip ends exactly where a hole in the data begins." : `A hole in the data begins ${d.gap} hours after the dip ends.`)],
      w: ["Holes often mark thruster firings, and the camera can wobble just before them, faking dips.", "Thruster firings leave holes in the data, and the wobble before each one can fake a dip.", "A dip that touches a hole is suspect, because thruster firings cause both."] },
    { id: "pregap", prio: 9, when: (F) => F.pregap_z >= T.pregap, for: ["gapdip"], against: ["planet"],
      m: [(d) => `In the 2 hours before the hole at ${d.pregap_at} hours, light sags by ${d.pregap} ppm.`, (d) => `Just before the hole at ${d.pregap_at} hours the light sags by ${d.pregap} ppm.`],
      w: ["A sag that ends exactly where data stops is the classic thruster firing fake.", "Sags that end right at a hole are often thruster firing effects.", "A dip that stops at a hole carries the thruster firing signature."] },
    { id: "drift", prio: 8, when: (F) => Math.abs(F.ramp_z) >= T.ramp && Math.abs(F.ramp_ppm) >= F.depth_ppm && F.event_edge_h <= 4, for: ["ramp"], against: ["planet"],
      m: [(d) => `Near the ${d.side} of the card the level is off by ${d.ramp} ppm from the middle.`, (d) => `The ${d.side} of the card sits ${d.ramp} ppm away from the middle level.`],
      w: ["A slow slide at one end is usually scattered light, not something crossing the star.", "A slide at the edge of a card is more often scattered light than a transit.", "Slow drifts at the ends usually come from the instrument."] },
    { id: "near_artifact", prio: 7, when: (F) => F.near_ratio >= T.near && F.near_ratio < 1 && F.depth_pts < 8, for: [], against: [],
      m: [(d) => `Part of this card comes close to ${d.near}, though no test fires.`, (d) => `Something here is close to ${d.near}, just under the line where a test fires.`],
      w: ["So this card is not clean enough to call plain noise; treat the dip with caution.", "That is enough to keep pure noise off the table; call it not classified.", "Be careful here: a near miss on an artifact test means the dip is not yet explained.", "A near miss is not a clean bill; keep it in the not classified pile.", "Close to an artifact pattern means do not trust a plain noise label."] },
    { id: "wobble", prio: 7, when: (F) => F.depth_pts < 8 && F.wobble_acf >= 0.25 && F.wobble_amp_ppm >= 1.5 * F.sigma_pt / Math.sqrt(6), for: ["variable"], against: ["planet"],
      m: [(d) => `The brightness rises and falls about every ${d.period} hours, by roughly ${d.wob} ppm.`, (d) => `The light repeats an up and down pattern about every ${d.period} hours, roughly ${d.wob} ppm.`],
      w: ["A star that wobbles makes many dips in a row; a planet makes one clean one.", "Repeating ups and downs suggest a spotted, spinning star rather than one planet.", "Many similar dips in a row point to the star itself."] },
    { id: "strong_flat", prio: 6, when: (F) => F.strength >= 9 && F.vness <= 0.6 && F.shape_dchi2 >= 4 && F.depth_pts < 8 && Math.abs(F.rebound_frac) < 0.5, for: ["planet"], against: ["noise"],
      m: [(d, F, g) => `Strength ${d.strength}${g ? G : ""}, with a flat floor and ${F.ingress_h < 0.25 ? "very steep sides" : d.ingress + " hour slopes"}.`, (d, F, g) => `It scores ${d.strength}${g ? G : ""} and has a flat floor with ${F.ingress_h < 0.25 ? "very steep sides" : d.ingress + " hour slopes"}.`],
      w: ["A flat floor between short slopes is what a planet crossing looks like, among other things.", "Flat floor and steep sides is the shape a planet makes, though an eclipse can do it too.", "That shape fits a planet crossing; an eclipse is the other thing that could make it.", "That shape is the planet shape, though eclipses and artifacts can imitate it.", "Planets make flat floors; so can some glitches, so check the rivals too."] },
    { id: "v_shape", prio: 6, when: (F) => F.vness >= 0.8 && F.shape_dchi2 < -4 && F.depth_pts < 8, for: ["eclipse"], against: ["planet"],
      m: [(d) => `It is V shaped: each side takes ${d.ingress} hours and there is no flat floor.`, (d) => `The dip is a V, with ${d.ingress} hour sides and no flat floor.`],
      w: ["A clear V with no floor is more like a grazing eclipse than a planet.", "Without a flat floor, a V shape fits a grazing eclipse better than a planet.", "A pointed bottom is typical of an eclipse that only just clips the star."] },
    { id: "unique", prio: 6, when: (F) => F.strength >= 5 && F.gap_ratio >= 1.6 && F.depth_pts < 8 && Math.abs(F.rebound_frac) < 0.5, for: ["planet"], against: [],
      m: [(d) => `The best dip scores ${d.strength}; the next best wiggle only ${d.second}.`, (d) => `Its strength is ${d.strength}, while the next best wiggle reaches ${d.second}.`],
      w: ["Standing out from the rest is needed for a planet, but noise does it too at this strength.", "A lone dip is a good sign, yet near this strength noise often stands alone as well.", "Being the only strong dip helps a planet's case without settling it.", "No other wiggle matches it, which helps a planet's case, but noise sometimes does the same.", "It stands apart from the rest, a point for a planet that noise can also score."] },
    { id: "not_unique", prio: 5, when: (F) => F.gap_ratio < 1.35 && F.depth_pts < 8, for: ["noise"], against: ["planet"],
      m: [(d) => `The best dip scores ${d.strength}, but the next best wiggle scores ${d.second}.`, (d) => `Its strength is ${d.strength}; another wiggle in the card reaches ${d.second}.`],
      w: ["When other wiggles are nearly as strong, the best one is often just noise.", "Rivals this close in strength suggest the best dip is one of many chance wiggles.", "Several wiggles of similar strength make the top one weak evidence.", "If a rival is nearly as strong, nothing singles this dip out as real.", "Close rivals mean the top dip may only be the luckiest wiggle."] },
    { id: "many", prio: 5, when: (F) => F.n_similar >= 2 && F.depth_pts < 8, for: ["noise", "variable"], against: ["planet"],
      m: [(d) => `${d.n_similar} other dips in this card are at least 70 percent as strong.`, (d) => `This card holds ${d.n_similar} more dips that are at least 70 percent as strong.`],
      w: ["A real crossing usually stands alone; a crowd of similar dips is often noise.", "Many dips of similar strength look like the noise itself, not one event.", "A crowd of alike dips weakens the case for any one of them.", "When the card is full of similar dips, none of them is special.", "Lots of alike dips usually mean noise or a wobbling star, not one planet."] },
    { id: "weak", prio: 4, when: (F) => F.strength < 7 && F.depth_pts < 8 && !(F.near_ratio >= T.near), for: ["noise"], against: [],
      m: [(d, F, g) => `Strength ${d.strength}${g ? G : ""}; the hunt only keeps 7 or more.`, (d, F, g) => `It scores ${d.strength}${g ? G : ""}, under the hunt's line of 7.`],
      w: ["Searching a whole month of pure noise often turns up one dip this strong.", "A month of noise alone often contains a dip of this strength somewhere.", "Dips below the line turn up in pure noise all the time.", "A dip this weak is what a sector of pure noise throws up now and then.", "On a month of noise alone, a dip of this strength is nothing unusual."] },
    { id: "near_limit", prio: 4, when: (F) => F.strength >= 5 && F.strength < 9 && F.gap_ratio >= 1.4 && F.depth_pts < 8, for: ["planet"], against: [],
      m: [(d) => `Strength ${d.strength}, close to the hunt's line of 7, lasting about ${d.dur} hours.`, (d) => `It scores ${d.strength}, near the line of 7, and lasts about ${d.dur} hours.`],
      w: ["Near the line, how unique the dip is matters more than how deep it looks.", "This close to 7, its uniqueness counts for more than its depth.", "Close to the line, ask whether anything else in the card looks as strong.", "Around the line, the hunt asks for more than strength alone.", "At this strength the hunt wants a second reason to believe the dip."] },
    { id: "shape_unclear", prio: 3, when: (F) => F.strength < 9 && Math.abs(F.shape_dchi2) < 4 && F.depth_pts < 8, for: ["noise", "planet"], against: [],
      m: [(d) => `At strength ${d.strength}, a flat floor and a V fit this dip about equally well.`, (d) => `A flat floor and a V fit this strength ${d.strength} dip about equally well.`],
      w: ["So shape cannot decide it; judge by strength and the next best wiggle.", "The shape cannot settle this one; weigh the strength and the rivals.", "At this strength shape tells you little; lean on strength and rivals.", "Neither shape wins at this strength, so the dip's shape adds little.", "Flat or V, the fit is equal here; look at strength and rivals instead."] },
    { id: "few_points", prio: 3, when: (F) => F.n_in <= 18 && F.depth_pts < 8, for: ["noise"], against: [],
      m: [(d) => `Only ${d.n_in} points sit inside the dip, so a few low points can make it.`, (d) => `The dip rests on just ${d.n_in} points, so a few low values can build it.`],
      w: ["A dip built from a handful of points is easy for noise to fake.", "Few points inside means a couple of low values could produce it.", "Dips resting on few points are the easiest for noise to imitate.", "With so few points inside, chance alone can build a dip like this.", "Few points in the dip means little evidence that it is a real shape."] },
    { id: "returns", prio: 3, when: (F) => !F.step_stays && Math.abs(F.rebound_frac) < 0.35 && Math.abs(F.rebound_z) < 3 && F.strength >= 6 && F.depth_pts < 8, for: ["planet"], against: ["step"],
      m: [(d) => `After the dip the level comes back to within ${d.rebound} ppm of where it started.`, (d) => `Once the dip ends, the light returns to within ${d.rebound} ppm of its old level.`],
      w: ["Coming back to the same level is what a crossing does; steps do not.", "A level that returns fits a crossing; a lasting change would not.", "Returning to the old level is typical of a transit."] },
    { id: "lumpy", prio: 2, when: (F) => F.beta >= 1.5, for: ["noise", "variable"], against: [],
      m: [(d) => `The noise is lumpy: hour averages scatter ${d.beta} times more than random points predict.`, (d) => `Hour averages scatter ${d.beta} times more than random points predict, so the noise is lumpy.`],
      w: ["Lumpy noise makes slow wiggles, so any dip here needs more support.", "Lumpy noise fakes slow dips, so ask for extra evidence here.", "Slow wiggles in the noise itself make dips less trustworthy.", "Slow lumps in the noise can pass for a shallow dip.", "Because the noise comes in lumps, a shallow dip proves less here."] },
  ];
  // what to check next, by lesson; and a default for each kind of card, used by the closing cue after the answer is known
  const NEXT = {
    deep: "how deep it is next to the noise", rise: "whether the change goes up or down", step: "whether the level comes back", gap_touch: "where the dip ends", pregap: "the last points before a hole",
    drift: "both ends of the card", wobble: "whether the dips repeat", strong_flat: "the floor and the slopes", unique: "the next best wiggle", not_unique: "the next best wiggle", many: "how many wiggles look alike",
    weak: "the strength against 7", near_limit: "how unique it is", v_shape: "floor or V", shape_unclear: "the next best wiggle", few_points: "how many points make it", lumpy: "how lumpy the noise is",
    returns: "the level afterwards", near_artifact: "the edges of the card and any hole",
  };
  const DEFAULT_CUE = { planet: "the strength against 7", noise: "the next best wiggle", eclipse: "how deep it is next to the noise", flare: "whether the change goes up or down", step: "the left and right halves",
    gapdip: "the last points before a hole", ramp: "both ends of the card", variable: "whether the dips repeat" };

  // ---------- composing three lines of about 40 words ----------
  const numsOf = (t) => t.match(/\d+(?:,\d{3})*(?:\.\d+)?/g) || [];
  const mask = (t) => t.replace(/\d+(?:,\d{3})*(?:\.\d+)?/g, "#");
  const lowerFirst = (t) => (/^[A-Z][a-z]/.test(t) ? t[0].toLowerCase() + t.slice(1) : t);
  function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  const words = (s) => s.split(/\s+/).filter(Boolean).length;
  const ANS = { dip: "Dip", nodip: "No dip", odd: "Odd", unsure: "Not sure" };
  const TRUTH_TXT = { planet: "a hidden planet", noise: "only noise", eclipse: "an eclipse", flare: "a spike up", step: "a lasting step", gapdip: "a fake dip at a hole", ramp: "a slow drift", variable: "a wobbling star" };
  const TRUTH_ANS = { planet: "dip", noise: "nodip", eclipse: "odd", flare: "odd", step: "odd", gapdip: "odd", ramp: "odd", variable: "odd" };
  const ANS_CLASS = { dip: ["planet"], nodip: ["noise"], odd: ["eclipse", "flare", "step", "gapdip", "ramp", "variable"] };

  // Ranking. blind = true never looks at the true label (used for the lead lesson in every mode); the answer alone may be used, since it is known in real work too.
  function rank(F, ctx, blind) {
    const st = ctx.state || newLearner(), out = [], truth = blind ? null : ctx.truth;
    for (const L of LESSONS) {
      if (!L.when(F)) continue;
      let score = 1 + (L.prio || 0) * 0.5;
      if (truth) score += (L.for.includes(truth) ? 3 : 0) - (L.against.includes(truth) ? 4 : 0);
      if (ANS_CLASS[ctx.answer] && ANS_CLASS[ctx.answer].some((c) => L.against.includes(c))) score += 2;   // the measurement argues against what was just said
      score -= 1.5 * st.recentLeads.slice(-4).filter((x) => x === L.id).length;                            // anti-repetition over the last 4 cards
      out.push({ L, score: score + (hash(ctx.cardId + L.id) % 100) / 1000 });
    }
    return out.sort((p, q) => q.score - p.score);
  }

  function compose(F, ctx) {
    const d = display(F), st = ctx.state || newLearner(), practice = ctx.mode === "practice";
    const ranked = rank(F, ctx, true);
    if (!ranked.length) ranked.push({ L: LESSONS.find((x) => x.id === "weak"), score: 0 });
    const lead = ranked[0].L;
    const aware = practice ? rank(F, ctx, false) : null, leadAware = aware && aware.length ? aware[0].L.id : lead.id;      // how often the label-aware choice would differ is logged, never shown
    const cueL = practice ? (aware.find((r) => r.L.for.includes(ctx.truth)) || null) : (ranked[1] || ranked[0]);
    const cue = practice ? (cueL ? NEXT[cueL.L.id] : DEFAULT_CUE[ctx.truth]) : NEXT[cueL.L.id];
    const gloss = (st.glossSeen.strength || 0) < 3;
    const pattern = practice ? patternLine(st) : null;
    const mFns = lead.m, mOpts = [];
    for (const f of mFns) { if (gloss) mOpts.push(f(d, F, true)); mOpts.push(f(d, F, false)); }
    const leadNums = numsOf(mOpts[mOpts.length - 1]);
    const sup = ranked.find((r) => r.L.id !== lead.id && r.score > 0 && !numsOf(r.L.m[0](d, F, false)).some((x) => leadNums.includes(x)));
    const detail = F.depth_pts < 8 ? `To reach 7 over ${d.dur} hours it would need about ${d.depth7} ppm; it has ${d.depth} ppm.` : null;
    const repeated = st.recentLeads.slice(-4).includes(lead.id);
    const extra = repeated ? (sup ? "Also measured: " + lowerFirst(sup.L.m[0](d, F, false)) : detail) : null;
    const wOpts = pattern ? pattern.slice() : lead.w.slice();
    if (extra && !pattern) wOpts.push(extra);
    let l3s;
    if (practice) {
      const it = TRUTH_TXT[ctx.truth], right = TRUTH_ANS[ctx.truth] === ctx.answer, A = ANS[ctx.answer];
      if (ctx.answer === "unsure") l3s = [`You chose Not sure; it was ${it}. Next time, check ${cue}.`, `Not sure; it was ${it}. Check ${cue}.`, `You chose Not sure. It was ${it}; check ${cue} next time.`, `Not sure; it was ${it}.`];
      else if (right) l3s = [`You said ${A}, and it was ${it}. Next time, also check ${cue}.`, `${A} was right: ${it}. Also check ${cue}.`, `Right: ${it}. Also check ${cue}.`, `Right: ${it}.`];
      else l3s = [`You said ${A}, but it was ${it}. Next time, check ${cue} first.`, `You said ${A}; it was ${it}. Check ${cue} first.`, `Not this time: it was ${it}. Check ${cue} first.`, `Not this time: it was ${it}.`];
    } else {
      const where = F.gap_dist_h <= 2 && !F.gap_is_edge ? "the thruster firing times" : F.depth_pts >= 8 ? "the eclipse timing" : "the second light curve";
      l3s = [`Your answer is locked. These are measurements, not a verdict; now compare ${where}.`, `Locked. Measurements, not a verdict; compare ${where}.`, `Locked. These are measurements, not a verdict. Next, compare ${cue} with ${where}.`, "Locked. These are measurements, not a verdict."];
    }
    // length control: every combination is scored; out of range (36 to 44 words) is heavily penalised; recent wordings are penalised so the text does not repeat
    let best = null;
    mOpts.forEach((m, mi) => wOpts.forEach((w, wi) => l3s.forEach((l3, li) => {
      const lines = [m, w, l3], n = lines.reduce((t, l) => t + words(l), 0), seen = (k, t) => (st.recentText[k] || []).slice(-8).includes(mask(t)) ? 1 : 0;
      const cost = Math.abs(n - 40) * 0.4 + (n > 44 || n < 36 ? 100 : 0) + 3 * (seen(0, m) + seen(1, w) + seen(2, l3)) + ((hash(ctx.cardId + m + w + l3) % 100) / 100) * 1.5 + (gloss && /how far it stands out/.test(m) ? -0.5 : 0);
      if (!best || cost < best.cost) best = { lines, n, cost };
    })));
    return { lines: best.lines, words: best.n, lead: lead.id, leadAware, disagree: leadAware !== lead.id, cue: cue, pattern: !!pattern, gloss: /how far it stands out/.test(best.lines[0]), display: d };
  }

  // ---------- learner model (kept in memory for one sitting) ----------
  function newLearner() { return { history: [], recentLeads: [], glossSeen: {}, recentText: [[], [], []], lastPatternAt: -99 }; }
  const bandOf = (F) => (F.strength < 5 ? "under 5" : F.strength < 7 ? "5 to 7" : F.strength < 10 ? "7 to 10" : "10 or more");
  function record(st, F, ctx, out) {
    st.history.push({ truth: ctx.truth, answer: ctx.answer, right: TRUTH_ANS[ctx.truth] === ctx.answer, band: bandOf(F), gapNear: F.gap_dist_h <= 0.5 && !F.gap_is_edge });
    st.recentLeads.push(out.lead);
    out.lines.forEach((l, k) => st.recentText[k].push(mask(l)));
    if (out.pattern) st.lastPatternAt = st.history.length;
    if (out.gloss) st.glossSeen.strength = (st.glossSeen.strength || 0) + 1;
  }
  function patternLine(st) {                               // at most once every 6 cards, from the last 12 answers
    if (st.history.length - st.lastPatternAt < 6) return null;
    const h = st.history.slice(-12), fa = h.filter((x) => x.answer === "dip" && x.truth !== "planet");
    if (fa.length >= 4) { const weak = fa.filter((x) => x.band === "under 5" || x.band === "5 to 7").length; if (weak / fa.length >= 0.6) return [`Pattern: ${weak} of your last ${fa.length} false alarms scored under 7, below the hunt's line.`, `Pattern: ${weak} of ${fa.length} false alarms scored under 7.`]; }
    const gm = h.filter((x) => x.gapNear && x.truth === "gapdip" && x.answer !== "odd");
    if (gm.length >= 3) return [`Pattern: you missed ${gm.length} of the last ${h.filter((x) => x.truth === "gapdip").length} dips that run into a data hole.`, `Pattern: ${gm.length} hole dips missed lately.`];
    const oddNoise = h.filter((x) => x.answer === "odd" && x.truth === "noise");
    if (oddNoise.length >= 3) return [`Pattern: ${oddNoise.length} of your recent Odd answers were plain noise; lumpy noise is still noise.`, `Pattern: ${oddNoise.length} recent Odd answers were plain noise.`];
    const unsure = h.filter((x) => x.answer === "unsure").length, wrong = h.filter((x) => !x.right).length;
    if (h.length >= 12 && unsure === 0 && wrong >= 4) return [`Pattern: ${wrong} wrong and 0 Not sure in 12 cards; Not sure is a fair answer.`, `Pattern: ${wrong} wrong, 0 Not sure in 12 cards.`];
    return null;
  }

  // card -> the engine's words for its kind and for the answer
  function truthKey(card) {
    if (card.truth === "dip") return "planet";
    if (card.truth === "none") return "noise";
    return { eclipse: "eclipse", spike: "flare", step: "step", gapdip: "gapdip" }[card.kind] || "eclipse";
  }
  const ANS_KEY = { dip: "dip", none: "nodip", odd: "odd", unsure: "unsure" };

  return { measure, display, compose, newLearner, record, truthKey, ANS_KEY, LESSONS, T, TRUTH_ANS, words, mask, numsOf };
});
