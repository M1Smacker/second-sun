// Release gates for the book (Claude, 15 Nov 2026, after the Book 3 audit found 32 bugs that every older check missed).
// These test what a READER does, not what the code intends: tap the menu, read in both themes, scroll the Tree, meet the tour.
// Chrome over CDP, no packages. Tests run as a normal browser (navigator.webdriver hidden) so first-visit UI is exercised.
// Usage: node release_gates.mjs <base-url> [--pages=all|quick] [--mutate=menu|contrast|overflow|sticky|tour] [--out=file.json]
//   --mutate breaks the page on purpose: the matching gate MUST fail (proof that the gate can fail).
// Exit 1 if any gate fails. Prints one JSON line {pass, gates:{...}, failures:[...]}.
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { MEASURE } from "./gates_measure.mjs";

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const [base, ...rest] = process.argv.slice(2);
const opt = Object.fromEntries(rest.map((a) => a.replace(/^--/, "").split("=")));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1";
const MUT = {
  menu: ".md-sidebar--primary { display: none !important; }",
  contrast: ".md-header, .md-header * { color: #e6e8ee !important; } [data-md-color-scheme=default] .md-header { background: #f5f7fb !important; }",
  overflow: ".md-content__inner::after { content: ''; display: block; width: 900px; height: 2px; }",
  sticky: ".md-content__inner > p:first-of-type { position: sticky; top: 0; height: 60px; background: transparent; }",
  tour: ".ss-tour { position: fixed !important; } .ss-tour__ring { position: fixed !important; }",
};

async function launch() {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "ss-gates-"));
  const port = 9600 + Math.floor(Math.random() * 300);
  const proc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "--no-first-run", "--no-default-browser-check", "--mute-audio", "about:blank"], { stdio: "ignore" });
  let target;
  for (let i = 0; i < 120 && !target; i++) { await sleep(150); try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page"); } catch {} }
  if (!target) throw new Error("chrome did not start");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const pending = new Map(); const B = { events: [] };
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } else if (d.method) B.events.push(d); };
  B.send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  B.js = async (expr) => { const r = await B.send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true }); return r.result?.exceptionDetails ? { evalError: (r.result.exceptionDetails.exception?.description || "").slice(0, 200) } : r.result?.result?.value; };
  await B.send("Page.enable"); await B.send("Runtime.enable"); await B.send("Network.enable");
  B.setup = async ({ width, height, mobile, theme, tour = false, reduced = true }) => {
    await B.send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: mobile ? 3 : 1, mobile });
    await B.send("Emulation.setTouchEmulationEnabled", { enabled: mobile, maxTouchPoints: mobile ? 5 : 0 });
    await B.send("Emulation.setUserAgentOverride", { userAgent: mobile ? UA : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36" });
    await B.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: reduced ? "reduce" : "no-preference" }] });
    const scheme = theme === "light" ? "default" : "slate", idx = theme === "light" ? 1 : 0;
    const scope = new URL(base).pathname;
    if (B.script) await B.send("Page.removeScriptToEvaluateOnNewDocument", { identifier: B.script });
    const src = `try { Object.defineProperty(navigator, 'webdriver', { get: () => false }); } catch (e) {}
      try { const v = JSON.stringify({ index: ${idx}, color: { media: '', scheme: '${scheme}', primary: 'custom', accent: 'custom' } }); localStorage.setItem(${JSON.stringify(scope + ".__palette")}, v);
            ${tour ? "" : "localStorage.setItem('ss-tour-3', 'done');"} sessionStorage.setItem('ss-open', '1'); } catch (e) {}
      ${opt.mutate ? `addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = ${JSON.stringify(MUT[opt.mutate] || "")}; document.head.append(s); });` : ""}`;
    B.script = (await B.send("Page.addScriptToEvaluateOnNewDocument", { source: src })).result.identifier;
  };
  B.go = async (url, wait = 1200) => { B.events = []; await B.send("Page.navigate", { url }); for (let i = 0; i < 120; i++) { await sleep(100); if (B.events.some((e) => e.method === "Page.loadEventFired")) break; } await sleep(wait); };
  B.tap = async (x, y, mobile) => {
    if (mobile) { await B.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x, y }] }); await sleep(40); await B.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] }); }
    else { for (const type of ["mousePressed", "mouseReleased"]) await B.send("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 }); }
  };
  B.close = async () => { ws.close(); proc.kill(); await sleep(300); try { fs.rmSync(profile, { recursive: true, force: true }); } catch {} };
  return B;
}

const failures = [], gates = {};
const fail = (gate, msg) => { failures.push(`${gate}: ${msg}`); gates[gate] = "FAIL"; };
const pass = (gate) => { if (!gates[gate]) gates[gate] = "PASS"; };

async function pageList(B) {
  if (opt.pages === "quick") return ["", "learn/", "learn/u1/l1-a-light-curve/", "shelf/", "claims/", "glossary/", "field-notes/", "labs/lab3-plot-and-read/"];
  const r = await (await fetch(new URL("sitemap.xml", base))).text();
  return [...r.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => new URL(m[1]).pathname.replace(/^\/second-sun\//, "").replace(/^\//, "")).filter((p) => !/^(eyes|rehearsal)\//.test(p));
}

const B = await launch();
const pages = await pageList(B);
const SIZES = [{ w: 320, h: 568, mobile: true }, { w: 390, h: 844, mobile: true }, { w: 768, h: 1024, mobile: true }, { w: 1280, h: 800, mobile: false }];
for (const theme of (opt.only === "tour" ? [] : ["dark", "light"])) {
  for (const s of SIZES) {
    await B.setup({ width: s.w, height: s.h, mobile: s.mobile, theme });
    for (const p of pages) {
      await B.go(base + p, p === "" ? 2200 : 1200);
      const m = await B.js(MEASURE(s.w));
      if (!m || m.evalError) { fail("measure", `${p} ${s.w} ${theme} ${m && m.evalError}`); continue; }
      if (m.redirect) continue;
      const where = `${p || "/"} ${s.w}px ${theme}`;
      if (m.docW > s.w + 1) fail("overflow", `${where}: page ${m.docW}px wide`); else pass("overflow");
      const hdr = m.low.filter((x) => x.header), body = m.low.filter((x) => !x.header);
      if (hdr.length) fail("header-contrast", `${where}: ${hdr.slice(0, 3).map((x) => x.el + " " + x.r).join(", ")}`); else pass("header-contrast");
      if (body.length) fail("text-contrast", `${where}: ${body.length} items, e.g. ${body.slice(0, 3).map((x) => x.el + " '" + x.text + "' " + x.r).join(", ")}`); else pass("text-contrast");
      if (m.sticky.length) fail("sticky", `${where}: transparent pinned block ${m.sticky.join(", ")}`); else pass("sticky");
      const errs = B.events.filter((e) => e.method === "Runtime.exceptionThrown").map((e) => (e.params.exceptionDetails.exception?.description || "").slice(0, 120));
      if (errs.length) fail("js-errors", `${where}: ${errs[0]}`); else pass("js-errors");
      // menu: on touch sizes below the wide layout, scroll half way, tap the menu, the side menu must show links
      if (s.mobile && (theme === "dark" || s.w === 390)) {
        // scroll half way down, then a little back up (as a reader does; Twinlight hides its header while you scroll down)
        await B.js(`(scrollTo(0, (document.documentElement.scrollHeight - innerHeight) / 2), true)`); await sleep(250);
        await B.js(`(scrollBy(0, -120), true)`); await sleep(450);
        const b = await B.js(`(() => { const l = document.querySelector('label.md-header__button[for="__drawer"]'); if (!l) return null; const r = l.getBoundingClientRect(); if (!r.width) return { hidden: true }; return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`);
        if (!b || b.hidden) fail("menu", `${where}: no menu button`);
        else {
          await B.tap(b.x, b.y, true); await sleep(650);
          const ok = await B.js(`(() => { const s = document.querySelector('.md-sidebar--primary'); if (!s || s.hidden) return { ok: false, why: 'menu hidden' }; const r = s.getBoundingClientRect(); const w = Math.min(r.right, innerWidth) - Math.max(r.left, 0); const n = [...s.querySelectorAll('a.md-nav__link')].filter((a) => a.getClientRects().length).length; return { ok: w > 150 && n > 2, why: 'visible width ' + Math.round(w) + ', links ' + n + ', checked ' + document.getElementById('__drawer').checked }; })()`);
          if (!ok.ok) fail("menu", `${where}: tapping the menu shows no menu (${ok.why}; tapped at ${Math.round(b.x)},${Math.round(b.y)})`); else pass("menu");
          await B.js(`(() => { const d = document.getElementById('__drawer'); if (d) { d.checked = false; d.dispatchEvent(new Event('change')); } return true; })()`);
        }
      }
    }
  }
}
// first-visit UI with motion on: the tour must not leave a ring behind its target or after Skip, and must not return after Done
for (const theme of ["dark", "light"]) {
  await B.setup({ width: 390, height: 844, mobile: true, theme, tour: true, reduced: false });
  await B.go(base + 'versions/', 600); await B.js(`(localStorage.removeItem('ss-tour-3'), true)`);
  await B.go(base, 3800);
  const t = await B.js(`!!document.querySelector('.ss-tour')`);
  if (!t) { fail("tour", `${theme}: the tour did not appear on a first visit`); continue; }
  for (let step = 0; step < 4; step++) {
    await sleep(1000);
    // a ring must stay on the thing it highlights: what sits under its centre must not change when the page scrolls
    const r = await B.js(`(() => { const ring = document.querySelector('.ss-tour__ring'); if (!ring) return { ring: false };
      const at = () => { const r = ring.getBoundingClientRect(); const x = Math.max(1, Math.min(innerWidth - 1, r.left + r.width / 2)), y = Math.max(1, Math.min(innerHeight - 1, r.top + r.height / 2)); const e = document.elementFromPoint(x, y); return e && e.closest('[data-node], .sst-seg, .sst-item, .sst-sec, a, button') || e; };
      const before = at(); const sy = scrollY; scrollBy(0, 400);
      return new Promise((res) => setTimeout(() => { const moved = scrollY !== sy; res({ ring: ring.isConnected, moved, same: !moved || !ring.isConnected || at() === before }); }, 350)); })()`);
    if (r.ring && !r.same) fail("tour", `${theme} step ${step + 1}: the highlight ring stayed on screen while its target scrolled away`);
    const n = await B.js(`(() => { const b = document.querySelector('.ss-tour__next'); if (!b) return false; b.click(); return true; })()`);
    if (!n) break;
  }
  await sleep(800);
  if (await B.js(`!!document.querySelector('.ss-tour, .ss-tour__ring')`)) fail("tour", `${theme}: tour parts left after Done`);
  await B.go(base, 3000);
  if (await B.js(`!!document.querySelector('.ss-tour')`)) fail("tour", `${theme}: tour came back after Done`); else pass("tour");
  // Skip inside the ring delay leaves nothing behind
  await B.js(`(localStorage.removeItem('ss-tour-3'), true)`); await B.go(base, 3800);
  await B.js(`(document.querySelector('.ss-tour__next') && document.querySelector('.ss-tour__next').click(), new Promise((r) => setTimeout(() => { const s = document.querySelector('.ss-tour__skip'); if (s) s.click(); r(true); }, 150)))`);
  await sleep(1500);
  if (await B.js(`!!document.querySelector('.ss-tour__ring')`)) fail("tour", `${theme}: a dimming ring stays after Skip`);
}
// the opening splash ends and lets taps through
await B.setup({ width: 390, height: 844, mobile: true, theme: "dark", reduced: false });
await B.js(`(sessionStorage.clear(), localStorage.removeItem('ss-splash-day'), true)`);
await B.go(base + "shelf/", 3600);
const sp = await B.js(`(() => { const e = document.elementFromPoint(200, 400); return { splash: !!document.getElementById('ss-splash'), top: e && e.id }; })()`);
if (sp.splash || sp.top === "ss-splash") fail("splash", "the opening splash still covers the page after 3.6 s"); else pass("splash");
await B.close();

const out = { pass: failures.length === 0, mutate: opt.mutate || null, pages: pages.length, gates, failures: failures.slice(0, 400), failureCount: failures.length, byGate: Object.fromEntries(Object.keys(gates).map((g) => [g, failures.filter((f) => f.startsWith(g + ':')).length])) };
if (opt.out) fs.writeFileSync(opt.out, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out));
process.exit(out.pass ? 0 : 1);
