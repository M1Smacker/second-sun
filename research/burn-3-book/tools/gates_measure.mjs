// Shared in-page measurement for release_gates.mjs (Chrome) and webkit_gates.mjs (WebKit). Claude, 15 Nov 2026.
// in-page measurement: header contrast, all-text contrast, overflow vs the set width, transparent sticky blocks, JS errors
export const MEASURE = (setW) => `(() => {
  const parse = (c) => { let m = c && c.match(/^rgba?\\(([^)]+)\\)$/); if (m) { const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; }
    m = c && c.match(/^color\\(srgb ([^)]+)\\)$/); if (m) { const p = m[1].split(/[ /]+/).filter(Boolean).map(Number); return [p[0] * 255, p[1] * 255, p[2] * 255, p.length > 3 ? p[3] : 1]; } return null; };
  const over = (t, b) => { const a = t[3] + b[3] * (1 - t[3]); return a ? [0, 1, 2].map((i) => (t[i] * t[3] + b[i] * b[3] * (1 - t[3])) / a).concat(a) : [0, 0, 0, 0]; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c[0]) + .7152 * f(c[1]) + .0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  let root = [255, 255, 255, 1]; for (const e of [document.documentElement, document.body]) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c[3]) root = over(c, root); }
  const bgOf = (el) => { const st = []; let img = false; for (let e = el; e && e !== document.documentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.backgroundImage !== 'none') img = true; const c = parse(cs.backgroundColor); if (c && c[3] > 0) { st.push(c); if (c[3] > .999) break; } } let bg = root; for (let i = st.length - 1; i >= 0; i--) bg = over(st[i], bg); return { bg, img }; };
  const vis = (el) => { const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false; const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') return false; return !el.closest('[hidden], .md-sidebar, .md-search, [aria-hidden=true]'); };
  const low = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (el.closest('svg, script, style, .katex-mathml, .ss-tour, #ss-splash')) continue;
    if (el.matches('.sst-seg button[aria-pressed=true]')) continue;   // its background is a sliding pill behind it (a sibling), not a parent: not measurable here
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1) || !vis(el)) continue;
    const cs = getComputedStyle(el); let fg = parse(cs.color); if (!fg) continue;
    let op = 1; for (let e = el; e; e = e.parentElement) op *= +getComputedStyle(e).opacity; if (op < .05) continue;
    const { bg, img } = bgOf(el); if (img && !el.closest('.md-header, .md-tabs')) continue;
    const r = ratio(over([fg[0], fg[1], fg[2], fg[3] * op], bg), bg), fs = parseFloat(cs.fontSize), large = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
    if (r < (large ? 3 : 4.5)) low.push({ el: el.tagName.toLowerCase() + '.' + String(el.className).split(' ')[0], text: el.textContent.trim().slice(0, 30), r: +r.toFixed(2), header: !!el.closest('.md-header, .md-tabs') });
  }
  // header icons (svg): their colour against the header background
  for (const b of document.querySelectorAll('.md-header__button, .ss-back')) { if (!vis(b)) continue; const fg = parse(getComputedStyle(b).color); const { bg } = bgOf(b); const r = ratio(over(fg, bg), bg); if (r < 3) low.push({ el: 'header-icon.' + String(b.className).split(' ')[0], r: +r.toFixed(2), header: true }); }
  const sticky = [...document.body.querySelectorAll('*')].filter((e) => { const cs = getComputedStyle(e); if (cs.position !== 'sticky' && cs.position !== 'fixed') return false; if (!vis(e) || e.matches('canvas, #ss-splash, .md-overlay, .md-dialog, .md-top, .ss-tour, .ss-tour__ring, .sst-scrim, .tw-bar, .tw-edge')) return false; const c = parse(cs.backgroundColor); const r = e.getBoundingClientRect(); return r.height > 40 && r.width > innerWidth * .5 && (!c || c[3] < .5) && (cs.backdropFilter || cs.webkitBackdropFilter || 'none') === 'none'; }).map((e) => e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]);
  return { docW: document.documentElement.scrollWidth, setW: ${setW}, low, sticky, title: document.title, redirect: !!document.querySelector('meta[http-equiv=refresh]') };
})()`;

