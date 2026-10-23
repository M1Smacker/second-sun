// Stress / regression checks for the book prototype, driving headless Chrome over CDP (no npm packages).
// Usage: node site_check.mjs <mode> <base-url> [options]
//   modes: layout | offline | fail404 | update | jsoff | redirect | images
// Every mode prints one JSON line {mode, pass, ...evidence}; exit code 1 if pass is false.
// The Claude desktop browser pane can't register service workers, so offline/update tests run here.
import { spawn, execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const [mode, base, ...rest] = process.argv.slice(2);
const opt = Object.fromEntries(rest.map((a) => a.replace(/^--/, "").split("=")));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const PAGES = ["", "start/", "start/journey/", "progress/", "quests/", "candidates/", "learn/", "learn/l1-dip-depth/", "book/02-light-curves/", "eyes/", "parts/part3/cheat/", "book/05-wandering-transits/", "book/07-noise-and-statistics/", "book/08-our-detector/", "book/14-credit-and-publishing/", "parts/part1/", "parts/part3/review/", "labs/lab3-plot-and-read/", "glossary/", "claims/", "field-notes/2026-10-23/"];

async function launch(tag) {
  const profile = `D:/second-sun/.cache/cdp-${tag}-${process.pid}`;
  const port = 9300 + Math.floor(Math.random() * 500);
  fs.rmSync(profile, { recursive: true, force: true });
  const proc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    "--no-first-run", "--no-default-browser-check", "about:blank"], { stdio: "ignore" });
  let target;
  for (let i = 0; i < 100 && !target; i++) {
    await sleep(150);
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page"); } catch {}
  }
  if (!target) throw new Error("chrome did not start");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  let id = 0;
  const pending = new Map(), listeners = new Set(), errors = [], navigations = [];
  ws.onmessage = (m) => {
    const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); return; }
    if (!d.method) return;
    if (d.method === "Runtime.exceptionThrown") errors.push("exception: " + String(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text).slice(0, 200));
    if (d.method === "Runtime.consoleAPICalled" && d.params.type === "error") errors.push("console.error: " + d.params.args.map((a) => a.value ?? a.description).join(" ").slice(0, 200));
    if (d.method === "Log.entryAdded" && d.params.entry.level === "error") errors.push("log: " + d.params.entry.text.slice(0, 160) + " " + (d.params.entry.url || ""));
    if (d.method === "Page.frameNavigated" && !d.params.frame.parentId) navigations.push(d.params.frame.url);
    listeners.forEach((f) => f(d));
  };
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const evaluate = async (expression) => {
    const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
    if (r.result?.exceptionDetails) throw new Error("eval: " + JSON.stringify(r.result.exceptionDetails).slice(0, 300));
    return r.result?.result?.value;
  };
  await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable"); await send("Network.enable");
  const close = async () => {
    try { await send("Browser.close"); } catch {}
    try { ws.close(); } catch {}
    proc.kill();
    await sleep(500);
    fs.rmSync(profile, { recursive: true, force: true, maxRetries: 10, retryDelay: 300 });
  };
  return { send, evaluate, listeners, errors, navigations, close };
}

async function waitFor(b, expr, ms = 20000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    try { if (await b.evaluate(expr)) return true; } catch {}
    await sleep(200);
  }
  return false;
}

async function goto(b, url) {
  const loaded = new Promise((r) => {
    const f = (d) => { if (d.method === "Page.loadEventFired") { b.listeners.delete(f); r(true); } };
    b.listeners.add(f);
  });
  await b.send("Page.navigate", { url });
  return Promise.race([loaded, sleep(15000).then(() => false)]);
}

const offline = (b, on) => b.send("Network.emulateNetworkConditions", { offline: on, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
const shellLength = () => JSON.parse(fs.readFileSync(path.join(opt.site, "sw.js"), "utf8").match(/const SHELL = (\[.*\]);/)[1]).length;
const SHELL_COUNT = `(async () => { const k = (await caches.keys()).find((x) => x.startsWith("ss-shell-")); return k ? (await (await caches.open(k)).keys()).length : 0; })()`;
const PAGE_STATE = `({ title: document.title, css: [...document.styleSheets].reduce((a, s) => { try { return a + s.cssRules.length } catch (e) { return a } }, 0), controlled: !!navigator.serviceWorker.controller, text: document.querySelector("article") ? document.querySelector("article").innerText.length : 0 })`;

const MEASURE = `(() => {
  const small = [], inline = new Set();
  const isInline = (el) => el.tagName === "A" && !el.classList.contains("md-button") && el.closest(".md-typeset") && el.closest("p, li, td, dd, figcaption, .ss-meta") && !el.closest(".md-nav");
  document.querySelectorAll("a[href], button, input:not([type=hidden]), summary, select, label[for], [role=button]").forEach((el) => {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (!r.width || !r.height || !el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return;   // also catches transparent/hidden ancestors
    if (el.closest(".md-skip") || el.classList.contains("headerlink") || el.closest("[hidden]")) return;
    if (r.bottom < 0 || r.right < 0 || r.left > innerWidth) return;       // off-canvas drawer items
    if (isInline(el)) { inline.add(el.className || "a"); return; }
    const min = el.closest("svg.ss-sky") ? 23.5 : 43.5;   // the home sky map: 24 px (WCAG 2.5.8), the same chapters are in the 44 px list below it
    if (r.width < min || r.height < min) small.push(el.tagName.toLowerCase() + "." + [...el.classList].join(".") + " " + Math.round(r.width) + "x" + Math.round(r.height) + " '" + (el.textContent || el.getAttribute("aria-label") || "").trim().slice(0, 24) + "'");
  });
  return { overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, small: [...new Set(small)], inline: [...inline], scheme: document.body.dataset.mdColorScheme };
})()`;

async function layout() {
  const b = await launch("layout");
  const out = { mode: "layout", checks: 0, overflow: [], small: [], schemeMismatch: [], inlineExempt: [] };
  try {
    for (const [scheme, val] of [["slate", 0], ["default", 1]]) {
      const pal = JSON.stringify({ index: val, color: { media: "", scheme, primary: "custom", accent: "custom" } });
      const { result } = await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `localStorage.setItem(${JSON.stringify(new URL(base).pathname + ".__palette")}, ${JSON.stringify(pal)})` });
      for (const w of [390, 1280]) {
        await b.send("Emulation.setDeviceMetricsOverride", { width: w, height: w < 768 ? 844 : 900, deviceScaleFactor: 1, mobile: w < 768 });
        for (const p of PAGES) {
          await goto(b, base + p);
          await sleep(300);
          const m = await b.evaluate(MEASURE);
          out.checks++;
          if (m.overflow > 0) out.overflow.push(`${p || "/"} ${w} ${scheme} +${m.overflow}`);
          if (m.scheme !== scheme) out.schemeMismatch.push(`${p || "/"} ${w} want ${scheme} got ${m.scheme}`);
          m.small.forEach((s) => out.small.push(`${w} ${scheme} ${p || "/"}: ${s}`));
          m.inline.forEach((c) => out.inlineExempt.includes(c) || out.inlineExempt.push(c));
        }
      }
      await b.send("Page.removeScriptToEvaluateOnNewDocument", { identifier: result.identifier });
    }
    out.small = [...new Set(out.small)];
    // theme toggle: one click = exactly one scheme change (no flicker loop); transitions only after first paint
    await b.send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
    await goto(b, base);
    await waitFor(b, `document.documentElement.classList.contains("ss-ready")`, 5000);
    out.toggle = await b.evaluate(`(async () => {
      let n = 0; const before = document.body.dataset.mdColorScheme;
      new MutationObserver((ms) => { n += ms.filter((m) => m.attributeName === "data-md-color-scheme").length; }).observe(document.body, { attributes: true });
      document.querySelector('[data-md-component="palette"] label:not([hidden])').click();
      await new Promise((r) => setTimeout(r, 1500));
      return { before, after: document.body.dataset.mdColorScheme, changes: n, ready: document.documentElement.classList.contains("ss-ready"), bodyTransition: getComputedStyle(document.body).transitionDuration };
    })()`);
    await b.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
    await goto(b, base + "learn/l1-dip-depth/");
    await sleep(300);
    out.reducedMotion = await b.evaluate(`({ body: getComputedStyle(document.body).transitionDuration, content: getComputedStyle(document.querySelector(".md-content__inner")).animationName, slider: getComputedStyle(document.querySelector(".ss-demo__lc span")).transitionDuration })`);
    await b.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
    await goto(b, base + "learn/l1-dip-depth/");
    await sleep(300);
    out.normalMotion = await b.evaluate(`({ content: getComputedStyle(document.querySelector(".md-content__inner")).animationName + " " + getComputedStyle(document.querySelector(".md-content__inner")).animationDuration, slider: getComputedStyle(document.querySelector(".ss-demo__lc span")).transitionDuration, link: getComputedStyle(document.querySelector(".md-typeset p a")).transitionDuration, headerlink: getComputedStyle(document.querySelector(".headerlink")).transitionDuration })`);
    out.hiddenShown = await b.evaluate(`[...document.querySelectorAll("[hidden]")].filter((e) => e.getClientRects().length).length`);
    out.paletteToggles = await b.evaluate(`[...document.querySelectorAll('[data-md-component="palette"] label')].filter((e) => e.getClientRects().length).length`);
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = out.hiddenShown === 0 && out.paletteToggles === 1 && !out.overflow.length && !out.small.length && !out.schemeMismatch.length && out.toggle.changes === 1 && out.toggle.before !== out.toggle.after
      && out.reducedMotion.body === "0s" && out.reducedMotion.content === "none" && out.reducedMotion.slider === "0s" && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

async function offlineTest() {
  const b = await launch("offline");
  const out = { mode: "offline" };
  try {
    const expected = shellLength();
    await goto(b, base);
    out.precached = await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${expected})`);
    out.shell = `${await b.evaluate(SHELL_COUNT)} / ${expected}`;
    out.firstVisitNavigations = b.navigations.length;             // must be 1: the first install never reloads
    await goto(b, base + "learn/l1-dip-depth/");                  // a visited page
    await offline(b, true);
    out.pages = {};
    for (const p of ["", "candidates/", "glossary/", "claims/", "book/14-credit-and-publishing/", "learn/l1-dip-depth/"]) {   // demo + search are tested on the last one
      await goto(b, base + p);
      out.pages[p || "/"] = await b.evaluate(PAGE_STATE);
    }
    out.demo = await b.evaluate(`(() => { const r = document.querySelector('[name="rp"]'); r.value = 11; r.dispatchEvent(new Event("input")); return document.querySelector(".ss-demo__result").textContent; })()`);
    out.search = await b.evaluate(`(async () => {
      const i = document.querySelector(".md-search__input"); i.focus(); i.value = "depth";
      for (const t of ["focus", "input", "keyup"]) i.dispatchEvent(new Event(t, { bubbles: true }));
      for (let k = 0; k < 40; k++) { const n = document.querySelectorAll(".md-search-result__item").length; if (n) return n; await new Promise((r) => setTimeout(r, 250)); }
      return 0; })()`);
    await goto(b, base + "no-such-page/");
    out.unknownPage = await b.evaluate(`document.body.innerText.includes("404")`);
    await goto(b, base + "stress-unvisited.png");                // an image never viewed, offline
    out.unvisitedImage = await b.evaluate(`document.body ? document.body.innerText.includes("404") : false`);
    await goto(b, base + "learn");                               // no trailing slash, offline
    out.noSlashOffline = { url: await b.evaluate("location.href"), title: await b.evaluate("document.title") };
    out.errors = b.errors.filter((e) => !/ERR_INTERNET_DISCONNECTED|no-such-page|404/.test(e));
    const okPages = Object.values(out.pages).every((s) => s.controlled && s.css > 900 && s.text > 100);
    out.pass = out.precached && out.firstVisitNavigations === 1 && okPages && /1\.0[0-9]%/.test(out.demo) && out.search > 0 && out.unknownPage && out.unvisitedImage
      && out.noSlashOffline.url.endsWith("/learn/") && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

async function fail404() {
  const b = await launch("fail404");
  const out = { mode: "fail404", failing: opt.failing };
  try {
    const expected = shellLength() - Number(opt.missing || 2);
    const t0 = Date.now();
    await goto(b, base);
    out.precached = await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${expected})`, 120000);
    out.installMs = Date.now() - t0;
    out.shell = `${await b.evaluate(SHELL_COUNT)} cached, ${expected} expected (shell ${shellLength()} minus the forced 404s)`;
    out.state = await b.evaluate(`navigator.serviceWorker.getRegistration().then((r) => r.active && r.active.state)`);
    await offline(b, true);
    await goto(b, base + "glossary/");
    out.otherPageOffline = await b.evaluate(PAGE_STATE);
    await goto(b, base + opt.failing);
    out.failedPageOffline = await b.evaluate(`document.body.innerText.includes("404") ? "404 page shown" : document.title`);
    out.pass = out.precached && out.state === "activated" && out.otherPageOffline.controlled && out.otherPageOffline.css > 900;
  } finally { await b.close(); }
  return out;
}

async function update() {
  const b = await launch("update");
  const out = { mode: "update" };
  const index = path.join(opt.proto, "docs", "index.md");
  const original = fs.readFileSync(index, "utf8");
  const build = () => execFileSync(opt.mkdocs, ["build", "--strict", "-q"], { cwd: opt.proto, env: { ...process.env, XDG_CACHE_HOME: "D:/second-sun/.cache" }, stdio: "pipe" });
  const version = () => b.evaluate(`caches.keys().then((k) => k.filter((x) => x.startsWith("ss-shell-")).sort().join(","))`);
  try {
    await goto(b, base);
    out.aReady = await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${shellLength()})`);
    out.versionA = await version();
    fs.writeFileSync(index, original + "\n\nUpdate test marker: version B.\n");
    build();
    out.versionBExpected = "ss-shell-" + fs.readFileSync(path.join(opt.site, "sw.js"), "utf8").match(/const VERSION = "([0-9a-f]+)"/)[1];
    const navBefore = b.navigations.length;
    await goto(b, base);                                            // reopen: browser checks sw.js, B installs and waits
    out.lineShown = await waitFor(b, `document.querySelectorAll(".ss-update").length === 1`);
    await sleep(2000);
    out.linesAfter2s = await b.evaluate(`document.querySelectorAll(".ss-update").length`);
    out.stillOnA = !(await b.evaluate(`document.body.innerText.includes("version B")`));
    const navAtClick = b.navigations.length;
    await b.evaluate(`document.querySelector(".ss-update button").click()`);
    await waitFor(b, `document.body.innerText.includes("version B")`, 15000);
    await sleep(5000);                                              // watch for any extra reloads
    out.reloadsAfterClick = b.navigations.length - navAtClick;      // must be exactly 1
    out.navigationsWithoutClick = navAtClick - navBefore;           // the reopen itself: 1
    out.onB = await b.evaluate(`document.body.innerText.includes("version B")`);
    out.versionAfter = await version();
    out.lineAfterReload = await b.evaluate(`document.querySelectorAll(".ss-update").length`);
    out.errors = b.errors;
    out.pass = out.aReady && out.lineShown && out.linesAfter2s === 1 && out.stillOnA && out.reloadsAfterClick === 1 && out.onB
      && out.versionAfter === out.versionBExpected && out.lineAfterReload === 0 && out.navigationsWithoutClick === 1 && !out.errors.length;
  } finally {
    fs.writeFileSync(index, original);
    build();
    await b.close();
  }
  return out;
}

async function jsoff() {
  const b = await launch("jsoff");
  const out = { mode: "jsoff" };
  try {
    await b.send("Emulation.setScriptExecutionDisabled", { value: true });
    await goto(b, base + "learn/l1-dip-depth/");
    out.state = await b.evaluate(`(() => {
      const d = [...document.querySelectorAll("details")];
      const before = d.map((x) => x.open);
      d[0].querySelector("summary").click();                        // native toggle, no page script needed
      return { htmlClass: document.documentElement.className, quizBoxes: d.length, closedBefore: before.every((o) => !o), firstOpensOnClick: d[0].open,
        answerText: d[0].innerText.includes("25%"), demoHidden: getComputedStyle(document.querySelector(".ss-demo")).display === "none",
        fallbackVisible: document.querySelector(".ss-fallback").offsetHeight > 0, fallbackSvg: !!document.querySelector(".ss-fallback svg"),
        articleChars: document.querySelector("article").innerText.length, navLinks: document.querySelectorAll(".md-nav__link").length };
    })()`);
    await goto(b, base + "candidates/");
    out.candidates = await b.evaluate(`({ cards: document.querySelectorAll(".ss-card").length, text: document.querySelector("article").innerText.length })`);
    const s = out.state;
    out.pass = s.htmlClass.includes("no-js") && s.quizBoxes === 3 && s.closedBefore && s.firstOpensOnClick && s.answerText && s.demoHidden
      && s.fallbackVisible && s.fallbackSvg && s.articleChars > 1000 && out.candidates.cards >= 1;
  } finally { await b.close(); }
  return out;
}

async function redirect() {
  const b = await launch("redirect");
  const out = { mode: "redirect" };
  try {
    let redirects = 0;
    b.listeners.add((d) => { if (d.method === "Network.requestWillBeSent" && d.params.type === "Document" && d.params.redirectResponse) redirects++; });
    await goto(b, base);
    await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${shellLength()})`);
    redirects = 0;
    await goto(b, base + "learn");
    await sleep(1500);
    out.online = { url: await b.evaluate("location.href"), redirects };
    redirects = 0;
    await offline(b, true);
    await goto(b, base + "glossary");
    await sleep(1500);
    out.offline = { url: await b.evaluate("location.href"), redirects, title: await b.evaluate("document.title") };
    out.pass = out.online.url.endsWith("/learn/") && out.online.redirects <= 1 && out.offline.url.endsWith("/glossary/") && out.offline.redirects <= 1;
  } finally { await b.close(); }
  return out;
}

async function images() {
  const b = await launch("images");
  const out = { mode: "images", cap: Number(opt.cap) };
  try {
    await goto(b, base);
    await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${shellLength() - Number(opt.missing || 0)})`, 60000);
    await goto(b, base + opt.gallery);
    await waitFor(b, `[...document.images].every((i) => i.complete)`, 30000);
    await sleep(1500);
    out.imagesOnPage = await b.evaluate(`document.images.length`);
    out.imageCache = await b.evaluate(`(async () => { const k = (await caches.keys()).find((x) => x.startsWith("ss-images-")); return k ? (await (await caches.open(k)).keys()).length : -1; })()`);
    out.pass = out.imageCache > 0 && out.imageCache <= out.cap;
  } finally { await b.close(); }
  return out;
}


async function shots() {
  // Visual evidence: PNGs into opt.out. Each shot: [name, width, scheme, page, action]
  const b = await launch("shots");
  const list = [
    ["home-390-dark", 390, "slate", "", null], ["home-390-light", 390, "default", "", null],
    ["l1-390-dark", 390, "slate", "learn/l1-dip-depth/", null], ["l1-quiz-open-390-dark", 390, "slate", "learn/l1-dip-depth/", "quiz"],
    ["search-open-390-dark", 390, "slate", "", "search"], ["chapter-1280-dark", 1280, "slate", "book/14-credit-and-publishing/", null],
    ["chapter-1280-light", 1280, "default", "book/14-credit-and-publishing/", null], ["search-1280-light", 1280, "default", "", "search"],
    ["claims-390-light", 390, "default", "claims/", null], ["progress-1280-dark", 1280, "slate", "progress/", null],
  ];
  const out = { mode: "shots", files: [] };
  try {
    for (const [name, w, scheme, page, action] of list) {
      const pal = JSON.stringify({ index: scheme === "slate" ? 0 : 1, color: { media: "", scheme, primary: "custom", accent: "custom" } });
      const { result } = await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `localStorage.setItem(${JSON.stringify(new URL(base).pathname + ".__palette")}, ${JSON.stringify(pal)})` });
      await b.send("Emulation.setDeviceMetricsOverride", { width: w, height: w < 768 ? 844 : 900, deviceScaleFactor: 1, mobile: w < 768 });
      await goto(b, base + page);
      await sleep(400);
      if (action === "search") {
        await b.evaluate(`(() => { const i = document.querySelector(".md-search__input"); document.querySelector('label[for="__search"]').click(); i.focus(); i.value = "depth"; for (const t of ["focus","input","keyup"]) i.dispatchEvent(new Event(t, { bubbles: true })); })()`);
        await sleep(1500);
      }
      if (action === "quiz") {
        await b.evaluate(`(() => { const d = document.querySelector("details.quiz"); d.querySelector("summary").click(); d.scrollIntoView({ block: "center" }); })()`);
        await sleep(600);
      }
      const shot = await b.send("Page.captureScreenshot", { format: "png" });
      const file = `${opt.out}/${name}.png`;
      fs.writeFileSync(file, Buffer.from(shot.result.data, "base64"));
      out.files.push(file);
      await b.send("Page.removeScriptToEvaluateOnNewDocument", { identifier: result.identifier });
    }
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.errors.length;
  } finally { await b.close(); }
  return out;
}

async function hammer() {
  // Diagnose connection resets: fetch one asset many times from inside Chrome, 6 at a time (browser-like).
  const b = await launch("hammer");
  const out = { mode: "hammer" };
  try {
    out.loaded = await goto(b, base + (opt.page || "404.html"));
    out.controlled = await b.evaluate("!!(navigator.serviceWorker && navigator.serviceWorker.controller)");
    out.where = await b.evaluate("location.href + ' | ' + document.title");
    const conc = Number(opt.conc || 6), rounds = Number(opt.rounds || 20);
    out.result = await b.evaluate(`(async () => {
      let ok = 0, fail = 0, timeout = 0; const errs = {}; const t0 = performance.now(); const slow = [];
      for (let i = 0; i < ${rounds}; i++) await Promise.all([...Array(${conc})].map(async (_, j) => {
        const ac = new AbortController(); const timer = setTimeout(() => ac.abort(), 5000); const s = performance.now();
        try { const r = await fetch("${opt.asset}?n=" + i + "-" + j, { cache: "no-store", signal: ac.signal }); await r.arrayBuffer(); r.ok ? ok++ : fail++; }
        catch (e) { if (e.name === "AbortError") timeout++; else { fail++; errs[String(e)] = (errs[String(e)] || 0) + 1; } }
        finally { clearTimeout(timer); const d = performance.now() - s; if (d > 1000) slow.push(Math.round(d)); }
      }));
      return { requests: ${rounds} * ${conc}, ok, fail, timeout, errs, slowOver1s: slow.length, totalMs: Math.round(performance.now() - t0) };
    })()`);
    out.pass = out.result.fail === 0 && out.result.timeout === 0;
  } finally { await b.close(); }
  return out;
}

// Eyes mode, end to end in a real browser: practice round with banner and read-only look back, review, the 30-curve test, an abandoned round,
// persistence across a reload, and the phone layout. Nothing here may change a saved answer.
async function eyesTest() {
  const b = await launch("eyes");
  const out = { mode: "eyes" }, checks = {};
  const wait = (ms) => sleep(ms);
  try {
    await goto(b, base + "eyes/");
    checks.started = await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    const click = (text) => b.evaluate(`(() => { const t = ${JSON.stringify(text)}; const bt = [...document.querySelectorAll(".ss-eyes button")].find((x) => x.textContent.trim() === t && x.offsetParent !== null && !x.disabled); if (!bt) return false; bt.click(); return true; })()`);
    const clickAny = async (list) => { for (const t of list) if (await click(t)) return t; return null; };
    const text = () => b.evaluate(`document.querySelector(".ss-eyes").innerText`);
    const visible = (t) => b.evaluate(`[...document.querySelectorAll(".ss-eyes button")].some((x) => x.textContent.trim() === ${JSON.stringify(t)} && x.offsetParent !== null)`);
    const store = () => b.evaluate(`JSON.parse(JSON.stringify(window.SSEyesStore.rounds()))`);
    const NEXT = ["Next", "See how you did", "Finish the test"];
    const start = await text();
    checks.noOldPromise = !/Nothing here is saved/.test(start) && /Take the official test/.test(start) && /My results/.test(start);

    // ---- practice round of 5 ----
    await click("5");
    const ans = ["Dip", "No dip", "Odd", "Not sure", "Dip"], banners = [];
    let snapBefore = null, lookBackTexts = [];
    for (let i = 0; i < 5; i++) {
      if (i === 2) {                                                   // look back from a live, unanswered question
        snapBefore = JSON.stringify((await store())[0].a.map((e) => [e.ans, e.ok, e.truth]));
        checks.backButtonShown = await visible("◀ Look at previous question");
        await click("◀ Look at previous question");
        lookBackTexts.push(await text());
        checks.lookBackReadOnly = !(await visible("Dip")) && !(await visible("No dip")) && !(await visible("Odd")) && !(await visible("Not sure"));
        await click("◀ Earlier"); lookBackTexts.push(await text());
        checks.cannotGoBeforeFirst = !(await click("◀ Earlier"));
        await click("Later ▶");
        await click("Back to light curve 3");
        checks.returnedToLive = /Light curve 3 of 5/.test(await text()) && await visible("Dip");
        checks.answersUnchangedByLooking = snapBefore === JSON.stringify((await store())[0].a.map((e) => [e.ans, e.ok, e.truth]));
      }
      checks["answered" + i] = await click(ans[i]);
      banners.push(await text());
      checks["next" + i] = !!(await clickAny(NEXT));
    }
    checks.bannerSaysTruth = banners.every((t) => /THIS WAS: (A DIP|NOT A DIP)/.test(t) && /It was /.test(t) && /You said/.test(t));
    checks.lookBackShowsTruthAndAnswer = lookBackTexts.every((t) => /Looking back at light curve \d of 5 \(read only\)/.test(t) && /THIS WAS:/.test(t) && /You said/.test(t));
    let r = (await store())[0];
    checks.practiceSaved = r.mode === "practice" && r.status === "done" && r.a.length === 5 && r.a.every((e) => e.ans && typeof e.ok === "boolean" && e.m && e.ms >= 0) && r.s.n === 5;
    checks.lookBacksRecorded = r.a.filter((e) => e.lb > 0).length >= 2;
    const fin = await text();
    checks.finishScreen = /How you did/.test(fin) && /Saved on this device: 1 round/.test(fin) && /Cloud backup is paused on this test copy of the book/.test(fin);   // local copies never write to Ahmed's real data
    checks.noUploadFromTestCopy = await b.evaluate(`window.SSEyesStore.unsynced().length === 1 && window.SSEyesStore.rounds()[0].sync !== 1`);

    // ---- read-only review of the finished round ----
    await click("Review this round");
    const rv = await text();
    checks.reviewOpens = /light curve 1 of 5 \(read only\)/.test(rv) && /THIS WAS:/.test(rv) && !(await visible("Dip"));
    await click("Close the review");
    checks.reviewCloses = /How you did/.test(await text());

    // ---- the official test: 30 curves, no truth until the end ----
    await click("Another sitting");
    await click("Take the official test (30 curves)");
    const cyc = ["Dip", "No dip", "Odd", "Not sure"]; let leaked = false, lastBanner = "";
    for (let i = 0; i < 30; i++) {
      await click(cyc[i % 4]);
      lastBanner = await text(); if (/THIS WAS:/.test(lastBanner)) leaked = true;
      if (i === 5) { await click("◀ Look at previous question"); const t = await text(); if (/THIS WAS:/.test(t) || !/You answered:/.test(t)) leaked = true; await click("Back to light curve 6"); }
      await clickAny(NEXT);
    }
    checks.testHidesTruth = !leaked;
    const tf = await text();
    checks.testFinish = /Test finished/.test(tf) && /Pass line so far/.test(tf) && /Not enough yet/.test(tf) && /Test rounds: 1, curves: 30/.test(tf);
    r = (await store())[0];
    checks.testSaved = r.mode === "test" && r.status === "done" && r.a.length === 30 && r.n === 30 && r.a.filter((e) => e.truth === "dip").length === 14 && r.a.filter((e) => e.truth === "none").length === 8;

    // ---- a round left half done, then a reload ----
    await click("Another sitting"); await click("5"); await click("Dip"); await clickAny(NEXT); await click("No dip");
    await goto(b, base + "eyes/");
    await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    await click("My results");
    const res = await text();
    const rounds = await store();
    checks.resultsAfterReload = /3 round\(s\) saved on this device/.test(res) && /abandoned/.test(res) && /done/.test(res);
    checks.abandonedKept = rounds.length === 3 && rounds[0].status === "abandoned" && rounds[0].a.length === 2;
    checks.resultsTable = await b.evaluate(`document.querySelectorAll(".ss-eyes__table tbody tr").length === 3 && document.querySelector(".ss-eyes__table thead").innerText.includes("False alarms")`);
    checks.noCopyOption = !/copy (my|the|your)? ?results|paste|export|send (it |them )?to claude/i.test(res) && !(await b.evaluate(`document.querySelector(".ss-eyes textarea") !== null || [...document.querySelectorAll(".ss-eyes button")].some((x) => /copy|paste|export/i.test(x.textContent))`));   // Ahmed: never make me hand over my results
    checks.exportApiForTheUpload = await b.evaluate(`(() => { const j = JSON.parse(window.SSEyesStore.exportJSON()); return j.schema === 1 && j.rounds.length === 3 && !!j.device.id; })()`);

    // ---- phone layout: nothing wider than the screen, every button big enough ----
    await b.send("Emulation.setDeviceMetricsOverride", { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
    await goto(b, base + "eyes/"); await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    const phone = async () => b.evaluate(`({ over: document.documentElement.scrollWidth - window.innerWidth, small: [...document.querySelectorAll(".ss-eyes button")].filter((x) => x.offsetParent !== null && x.getBoundingClientRect().height < 43.5).length })`);
    const p1 = await phone(); await click("My results"); const p2 = await phone();
    await click("Back"); await click("5"); await click("Dip"); const p3 = await phone();
    checks.phoneLayout = [p1, p2, p3].every((p) => p.over <= 1 && p.small === 0);
    out.phone = [p1, p2, p3];
    await b.send("Emulation.clearDeviceMetricsOverride");

    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    checks.noConsoleErrors = out.errors.length === 0;
  } catch (e) { out.error = String(e && e.message || e); }
  finally { await b.close(); }
  out.checks = checks;
  out.failed = Object.entries(checks).filter(([, v]) => !v).map(([k]) => k);
  out.pass = !out.error && out.failed.length === 0 && Object.keys(checks).length >= 30;
  return out;
}

// Eyes cloud backup in a real browser against a MOCK Firestore (same rules as the published ones): online, offline, a server error, an abandoned round
// recovered after a reload. Each round must arrive exactly once, in a shape the real rules accept, with no copy/paste step for the user.
async function eyesCloudTest() {
  const http = await import("node:http");
  const mock = { calls: [], docs: new Map(), failNext: 0 };
  const rulesOk = (f, id) => JSON.stringify(Object.keys(f).sort()) === JSON.stringify(["a", "device", "id", "mode", "n", "s", "source", "status", "t0", "t1", "v"])
    && f.v.integerValue === "1" && f.id.stringValue === id && ["practice", "test", "real"].includes(f.mode.stringValue) && f.n.integerValue !== undefined
    && Number(f.n.integerValue) <= 200 && !!f.a.arrayValue && (f.a.arrayValue.values || []).length <= 200;
  const server = http.createServer((req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*"); res.setHeader("Access-Control-Allow-Headers", "content-type"); res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    if (req.method === "OPTIONS") { res.statusCode = 204; return res.end(); }
    let raw = ""; req.on("data", (c) => (raw += c)); req.on("end", () => {
      const u = new URL(req.url, "http://x"), id = u.searchParams.get("documentId");
      let code = 200;
      try {
        const body = JSON.parse(raw);
        const good = req.method === "POST" && u.pathname === "/v1/projects/second-sun-faea5/databases/(default)/documents/eyes_rounds" && u.searchParams.get("key") === "AIzaSyBogX_Jte_4fahJ1Ovp3y-twCmxheLTSxY" && rulesOk(body.fields, id);
        mock.calls.push({ id, good, status: body.fields?.status?.stringValue });
        if (mock.failNext > 0) { mock.failNext--; code = 503; }
        else if (!good) code = 403;
        else if (mock.docs.has(id)) code = 409;
        else mock.docs.set(id, body);
      } catch (e) { code = 400; }
      res.statusCode = code; res.setHeader("Content-Type", "application/json"); res.end("{}");
    });
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const port = server.address().port;
  const b = await launch("eyescloud"), out = { mode: "eyescloud" }, checks = {};
  try {
    await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `window.SSEYES_CLOUD_BASE = "http://127.0.0.1:${port}";` });
    await goto(b, base + "eyes/");
    await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    const click = (t) => b.evaluate(`(() => { const t = ${JSON.stringify(t)}; const bt = [...document.querySelectorAll(".ss-eyes button")].find((x) => x.textContent.trim() === t && x.offsetParent !== null && !x.disabled); if (!bt) return false; bt.click(); return true; })()`);
    const clickAny = async (l) => { for (const t of l) if (await click(t)) return t; return null; };
    const text = () => b.evaluate(`document.querySelector(".ss-eyes").innerText`);
    const NEXT = ["Next", "See how you did", "Finish the test"];
    const playRound = async (n, answers) => { await clickAny(["Another sitting"]); await click(String(n)); for (let i = 0; i < n; i++) { await click(answers[i % answers.length]); await clickAny(NEXT); } };
    const store = () => b.evaluate(`JSON.parse(JSON.stringify(window.SSEyesStore.rounds()))`);
    checks.statusAtStart = /Cloud backup is on\. Each finished round is sent by itself/.test(await text());

    await click("5"); for (let i = 0; i < 5; i++) { await click(["Dip", "No dip", "Odd", "Not sure", "Dip"][i]); await clickAny(NEXT); }
    checks.roundSentAtOnce = await waitFor(b, `window.SSEyesStore.unsynced().length === 0`, 15000) && mock.docs.size === 1;
    checks.shapeAcceptedByRules = mock.calls.length >= 1 && mock.calls.every((c) => c.good);
    checks.statusSaysSafe = await waitFor(b, `/all 1 finished round\\(s\\) are safe in the cloud, and Claude can read them/.test(document.querySelector(".ss-eyes").innerText)`, 8000);
    checks.noCopyOrSendStep = !/copy (my|the|your)? ?results|paste|export|send (it |them )?to claude/i.test(await text());
    const sent = [...mock.docs.values()][0].fields;
    checks.sentMatchesScreen = sent.a.arrayValue.values.length === 5 && sent.mode.stringValue === "practice" && sent.status.stringValue === "done";

    await offline(b, true);
    await playRound(5, ["Dip", "No dip"]);
    await sleep(1500);
    checks.offlineWaits = /1 round\(s\) waiting for the internet. They will send themselves/.test(await text()) && mock.docs.size === 1 && (await store())[0].sync !== 1;
    await offline(b, false);
    checks.sentWhenInternetReturns = await waitFor(b, `window.SSEyesStore.unsynced().length === 0`, 10000) && mock.docs.size === 2;   // 10 s < the 15 s background check, so only the browser's "online" event can do this
    checks.statusAfterReturn = await waitFor(b, `/all 2 finished round\\(s\\) are safe/.test(document.querySelector(".ss-eyes").innerText)`, 8000);

    mock.failNext = 1;                                                       // the server is busy once
    await playRound(5, ["Odd", "Dip", "Not sure"]);
    checks.serverBusyThenRetried = await waitFor(b, `window.SSEyesStore.unsynced().length === 0`, 45000) && mock.docs.size === 3;

    await clickAny(["Another sitting"]); await click("5"); await click("Dip"); await clickAny(NEXT); await click("No dip");   // a round left half done
    const before = mock.docs.size;
    await goto(b, base + "eyes/"); await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    checks.abandonedRoundSentAfterReload = await waitFor(b, `window.SSEyesStore.unsynced().length === 0`, 20000) && mock.docs.size === before + 1
      && [...mock.docs.values()].some((d) => d.fields.status.stringValue === "abandoned" && d.fields.a.arrayValue.values.length === 2);
    const rounds = await store();
    checks.everyRoundExactlyOnce = rounds.length === 4 && rounds.every((r) => r.sync === 1) && mock.docs.size === 4 && new Set(mock.calls.filter((c) => c.good).map((c) => c.id)).size === 4;
    const calls0 = mock.calls.length; await sleep(4000);
    checks.noLoopOrResend = mock.calls.length === calls0;
    out.mock = { calls: mock.calls.length, docs: mock.docs.size };
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js|Failed to load resource|ERR_INTERNET_DISCONNECTED/.test(e));
    checks.noConsoleErrors = out.errors.length === 0;
  } catch (e) { out.error = String(e && e.message || e); }
  finally { await b.close(); server.close(); }
  out.checks = checks; out.failed = Object.entries(checks).filter(([, v]) => !v).map(([k]) => k);
  out.pass = !out.error && out.failed.length === 0 && Object.keys(checks).length >= 12;
  return out;
}

// ONE-OFF end-to-end test against the REAL Firestore (not part of the publish gates): plays a labelled 'e2e-test' round in a real browser, waits until the
// page says it is in the cloud, and prints the round as the device saved it, so pipeline/eyes_e2e.py can compare it with what the cloud holds, then delete it.
async function eyesReal() {
  const b = await launch("eyesreal"), out = { mode: "eyesreal" };
  try {
    await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `window.SSEYES_CLOUD_ALLOW_LOCAL = true;` });   // this one test is allowed to write to the real cloud (labelled e2e-test, deleted after)
    await goto(b, base + "eyes/"); await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    await b.evaluate(`window.SSEyesStore.setLabel("e2e-test")`);
    const click = (t) => b.evaluate(`(() => { const t = ${JSON.stringify(t)}; const bt = [...document.querySelectorAll(".ss-eyes button")].find((x) => x.textContent.trim() === t && x.offsetParent !== null && !x.disabled); if (!bt) return false; bt.click(); return true; })()`);
    const clickAny = async (l) => { for (const t of l) if (await click(t)) return t; return null; };
    await click("5");
    for (const a of ["Dip", "No dip", "Odd", "Not sure", "Dip"]) { await click(a); await clickAny(["Next", "See how you did"]); }
    out.sent = await waitFor(b, `window.SSEyesStore.unsynced().length === 0`, 30000);
    out.statusText = await b.evaluate(`[...document.querySelectorAll(".ss-eyes__cloud")].map((e) => e.textContent).join(" | ")`);
    out.round = (await b.evaluate(`JSON.parse(JSON.stringify(window.SSEyesStore.rounds()))`))[0];
    out.device = await b.evaluate(`window.SSEyesStore.device`);
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = out.sent && out.errors.length === 0;
  } finally { await b.close(); }
  return out;
}

const modes = { hammer, shots, layout, offline: offlineTest, fail404, update, jsoff, redirect, images, eyes: eyesTest, eyescloud: eyesCloudTest, eyesreal: eyesReal };
try {
  const r = await modes[mode]();
  console.log(JSON.stringify(r));
  process.exit(r.pass ? 0 : 1);
} catch (e) {
  console.log(JSON.stringify({ mode, pass: false, error: String(e && e.stack || e).slice(0, 500) }));
  process.exit(1);
}
