/* Eyes strength: the hunt's own box score, in JavaScript. One function for the cards, the feedback text and (later) the real vetting page, so "strength 7" means the same thing everywhere.
   It is a port of box_scores() in pipeline/detect_v2.py (10 minute bins, boxes of 3 to 15 hours, a box needs 80 percent of its points, scale = 1.4826 x the median absolute deviation of
   the box means). The golden test (book/tools/test_eyes_strength.mjs) feeds the same arrays to the Python and to this file and demands the same numbers.
   On a short card the hunt's scale is taken from a long stretch of the same star's noise (sectorSig), the way the hunt takes it from a whole sector. Browser: window.SSStrength. Node: module.exports. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api; else root.SSStrength = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  const DURS_H = [3, 4, 5, 6.5, 8, 10, 12, 15], MIN_COVER = 0.8;
  const fin = (v) => typeof v === "number" && isFinite(v);
  const nan = (a) => Array.from(a, (v) => (fin(v) ? v : NaN));
  function median(a) { const b = a.filter(fin).sort((x, y) => x - y), n = b.length; if (!n) return NaN; return n % 2 ? b[(n - 1) / 2] : (b[n / 2 - 1] + b[n / 2]) / 2; }
  const widthOf = (durH) => Math.max(Math.round(durH * 60 / 10), 1);            // every hunt duration is a whole number of bins, so this agrees with Python's round()

  // mean of every box of w bins; NaN where fewer than minCover of its points exist
  function boxMeans(bf, w, minCover = MIN_COVER) {
    const x = nan(bf), N = x.length, cn = new Float64Array(N + 1), cf = new Float64Array(N + 1);
    for (let i = 0; i < N; i++) { const v = fin(x[i]); cn[i + 1] = cn[i] + (v ? 1 : 0); cf[i + 1] = cf[i] + (v ? x[i] : 0); }
    const out = new Array(Math.max(N - w + 1, 0));
    for (let i = 0; i < out.length; i++) { const n = cn[i + w] - cn[i]; out[i] = n < minCover * w ? NaN : (cf[i + w] - cf[i]) / Math.max(n, 1); }
    return out;
  }

  // exactly the hunt's box_scores: SNR = (median of all points - box mean) / (1.4826 x MAD of the box means), scale taken from the array itself
  function boxScores(bf, durH, minCover = MIN_COVER) {
    const x = nan(bf), w = widthOf(durH), m = boxMeans(x, w, minCover), med = median(x), good = m.filter(fin);
    if (good.length < 20) return { w, m, med, sig: NaN, snr: m.map(() => NaN) };
    const mm = median(good), sig = 1.4826 * median(good.map((v) => Math.abs(v - mm)));
    return { w, m, med, sig, snr: m.map((v) => (med - v) / sig) };
  }

  // the hunt's scale for each box width, taken from a long stretch (a whole sector, or a long stretch of this star's noise)
  function sectorSig(x) { const o = {}; for (const d of DURS_H) o[widthOf(d)] = boxScores(x, d).sig; return o; }

  // every box on a short card scored with the sector's scale: [{a, w, m, s}] and the card's median
  function huntBoxes(y, sigT, minCover = MIN_COVER) {
    const x = nan(y), med = median(x), boxes = [];
    for (const d of DURS_H) {
      const w = widthOf(d), sig = sigT[w];
      if (!(sig > 0) || w > x.length) continue;
      const m = boxMeans(x, w, minCover);
      for (let a = 0; a < m.length; a++) if (fin(m[a])) boxes.push({ a, w, m: m[a], s: (med - m[a]) / sig });
    }
    return { med, boxes };
  }

  // how strong a noise-free dip of unit depth (profile p, values 0 to 1) scores: best box over every width and position
  function profileScan(p, sigT) {
    const pad = 90, x = new Array(p.length + 2 * pad).fill(0); p.forEach((v, i) => { x[pad + i] = v; });
    let best = { s: 0, w: 0 };
    for (const d of DURS_H) {
      const w = widthOf(d), sig = sigT[w], m = boxMeans(x, w, 0);
      for (const v of m) if (v / sig > best.s) best = { s: v / sig, w };
    }
    return best;
  }
  const profileStrength = (p, sigT) => profileScan(p, sigT).s;

  return { DURS_H, MIN_COVER, widthOf, median, boxMeans, boxScores, sectorSig, huntBoxes, profileScan, profileStrength };
});
