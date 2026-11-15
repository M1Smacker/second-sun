// WebKit release gates (Claude, 15 Nov 2026): the same reader checks as release_gates.mjs, run in Safari's engine
// (Playwright WebKit, iPhone 13 profile). Still NOT a real iPhone, but the same engine family as iPhone Safari.
// Needs Playwright and WebKit in D:\second-sun\data\tools (see research/downloads.csv, 15 Nov 2026).
// Usage: node webkit_gates.mjs <base-url> [--pages=all|quick] [--out=file.json]   Exit 1 on any failure.
import { createRequire } from "node:module";
import fs from "node:fs";
import { MEASURE } from "./gates_measure.mjs";

process.env.PLAYWRIGHT_BROWSERS_PATH = process.env.PLAYWRIGHT_BROWSERS_PATH || "D:\\second-sun\\data\\tools\\ms-playwright";
const require = createRequire("D:/second-sun/data/tools/playwright/package.json");
const { webkit, devices } = require("playwright");
const [base, ...rest] = process.argv.slice(2);
const opt = Object.fromEntries(rest.map((a) => a.replace(/^--/, "").split("=")));
const failures = [], gates = {};
const fail = (g, m) => { failures.push(`${g}: ${m}`); gates[g] = "FAIL"; };
const pass = (g) => { if (!gates[g]) gates[g] = "PASS"; };

let pages;
if (opt.pages === "quick") pages = ["", "learn/", "learn/u1/l1-a-light-curve/", "shelf/", "claims/", "glossary/"];
else {
  const x = await (await fetch(new URL("sitemap.xml", base))).text();
  pages = [...x.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => new URL(m[1]).pathname.replace(/^\/second-sun\//, "").replace(/^\//, "")).filter((p) => !/^(eyes|rehearsal)\//.test(p));
}
const browser = await webkit.launch();
const scope = new URL(base).pathname;
for (const theme of ["dark", "light"]) {
  const ctx = await browser.newContext({ ...devices["iPhone 13"], reducedMotion: "reduce" });
  const scheme = theme === "light" ? "default" : "slate", idx = theme === "light" ? 1 : 0;
  await ctx.addInitScript(`try { localStorage.setItem(${JSON.stringify(scope + ".__palette")}, JSON.stringify({ index: ${idx}, color: { media: '', scheme: '${scheme}', primary: 'custom', accent: 'custom' } })); localStorage.setItem('ss-tour-3', 'done'); sessionStorage.setItem('ss-open', '1'); } catch (e) {}`);
  const page = await ctx.newPage();
  const errs = []; page.on("pageerror", (e) => errs.push(String(e).slice(0, 150)));
  for (const p of pages) {
    errs.length = 0;
    try { await page.goto(base + p, { waitUntil: "load", timeout: 20000 }); } catch (e) { fail("load", `${p} ${theme}: ${String(e).slice(0, 100)}`); continue; }
    await page.waitForTimeout(p === "" ? 1800 : 900);
    const m = await page.evaluate(MEASURE(390));
    if (m.redirect) continue;
    const where = `${p || "/"} WebKit iPhone 13 ${theme}`;
    if (m.docW > 391) fail("overflow", `${where}: page ${m.docW}px wide`); else pass("overflow");
    const hdr = m.low.filter((x) => x.header), body = m.low.filter((x) => !x.header);
    if (hdr.length) fail("header-contrast", `${where}: ${hdr.slice(0, 3).map((x) => x.el + " " + x.r).join(", ")}`); else pass("header-contrast");
    if (body.length) fail("text-contrast", `${where}: ${body.length} items, e.g. ${body.slice(0, 3).map((x) => x.el + " '" + (x.text || "") + "' " + x.r).join(", ")}`); else pass("text-contrast");
    if (m.sticky.length) fail("sticky", `${where}: ${m.sticky.join(", ")}`); else pass("sticky");
    if (errs.length) fail("js-errors", `${where}: ${errs[0]}`); else pass("js-errors");
    // negative answers must be typeable: no decimal-only keypad where an answer starts with a minus, unless a sign button exists
    const neg = await page.evaluate(`[...document.querySelectorAll('.tw-prob')].filter((p) => (p.dataset.answer || '').split('|').some((a) => a.trim().startsWith('-'))).map((p) => { const i = p.querySelector('input'); return { mode: i && i.inputMode, sign: !!p.querySelector('[data-sign], .tw-sign') }; })`);
    for (const n of neg) { if (n.mode === "decimal" || n.mode === "numeric") { if (!n.sign) fail("minus-key", `${where}: a problem with a negative answer opens a keypad without a minus key`); } }
    if (neg.length) pass("minus-key");
    // menu: scroll down, back up a little, tap the menu
    if (theme === "dark" || p === "") {
      await page.evaluate(`scrollTo(0, (document.documentElement.scrollHeight - innerHeight) / 2)`); await page.waitForTimeout(250);
      await page.evaluate(`scrollBy(0, -120)`); await page.waitForTimeout(450);
      const box = await page.locator('label.md-header__button[for="__drawer"]').boundingBox();
      if (!box) { fail("menu", `${where}: no menu button`); continue; }
      await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height / 2); await page.waitForTimeout(700);
      const ok = await page.evaluate(`(() => { const s = document.querySelector('.md-sidebar--primary'); if (!s || s.hidden) return false; const r = s.getBoundingClientRect(); return Math.min(r.right, innerWidth) - Math.max(r.left, 0) > 150; })()`);
      if (!ok) fail("menu", `${where}: tapping the menu shows no menu`); else pass("menu");
      await page.evaluate(`(() => { const d = document.getElementById('__drawer'); if (d) { d.checked = false; d.dispatchEvent(new Event('change')); } })()`);
    }
  }
  await ctx.close();
}
await browser.close();
const out = { engine: "webkit", pass: failures.length === 0, pages: pages.length, gates, failureCount: failures.length, failures: failures.slice(0, 300) };
if (opt.out) fs.writeFileSync(opt.out, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out));
process.exit(out.pass ? 0 : 1);
