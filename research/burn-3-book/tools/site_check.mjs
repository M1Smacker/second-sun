// Stress / regression checks for the book prototype, driving headless Chrome over CDP (no npm packages).
// Usage: node site_check.mjs <mode> <base-url> [options]
//   modes: layout | tree | learn | repairs (Book 3 audit, --engine=webkit optional) | chapter (responsive reading pages) | offline | fail404 | update | jsoff
//          redirect | images | shots | hammer | eyes | eyeslayout | eyescloud
//          eyesreal (writes to real cloud) | rehearsal | rehearsalcloud | watchtimers | headertitle | textfloor
// --chrome-no-sandbox=1 is an explicit opt-in for a restricted local runner.
// Every mode prints one JSON line {mode, pass, ...evidence}; exit code 1 if pass is false.
// The Claude desktop browser pane can't register service workers, so offline/update tests run here.
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const [mode, base, ...rest] = process.argv.slice(2);
const opt = Object.fromEntries(rest.map((a) => a.replace(/^--/, "").split("=")));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const PAGES = ["", "learn/", "shelf/", "training/", "candidates/", "eyes/", "rehearsal/", "glossary/", "claims/", "field-notes/", "field-notes/2026-11-14/", "watch/", "versions/", "reference/prior-work/", "reference/for-astronomers/"];

async function launch(tag) {
  const profile = path.resolve(opt.profiles || "data/astra/016/profiles", `cdp-${tag}-${process.pid}`);
  fs.mkdirSync(path.dirname(profile), { recursive: true });
  const port = 9300 + Math.floor(Math.random() * 500);
  fs.rmSync(profile, { recursive: true, force: true });
  const proc = spawn(CHROME, ["--headless=new", ...(opt["chrome-no-sandbox"] ? ["--no-sandbox", "--disable-gpu"] : []), `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    "--no-first-run", "--no-default-browser-check", "about:blank"], { stdio: ["ignore", "ignore", opt.debug ? fs.openSync(opt.debug + ".chrome", "a") : "ignore"] });
  let target;
  for (let i = 0; i < 100 && !target; i++) {
    await sleep(150);
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page"); } catch {}
  }
  if (!target) { proc.kill(); throw new Error("chrome did not start"); }
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  let id = 0;
  const pending = new Map(), listeners = new Set(), errors = [], navigations = [];
  ws.onmessage = (m) => {
    if (opt.debug) fs.appendFileSync(opt.debug, "message " + String(m.data).slice(0, 300) + "\n");
    const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); return; }
    if (!d.method) return;
    if (d.method === "Runtime.exceptionThrown") errors.push("exception: " + String(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text).slice(0, 200));
    if (d.method === "Runtime.consoleAPICalled" && d.params.type === "error") errors.push("console.error: " + d.params.args.map((a) => a.value ?? a.description).join(" ").slice(0, 200));
    if (d.method === "Log.entryAdded" && d.params.entry.level === "error") errors.push("log: " + d.params.entry.text.slice(0, 160) + " " + (d.params.entry.url || ""));
    if (d.method === "Page.frameNavigated" && !d.params.frame.parentId) navigations.push(d.params.frame.url);
    listeners.forEach((f) => f(d));
  };
  if (opt.debug) {
    ws.onclose = (e) => fs.appendFileSync(opt.debug, `closed ${e.code} ${e.reason}\n`);
    ws.onerror = (e) => fs.appendFileSync(opt.debug, `socket error ${e.message} ${e.error?.stack}\n`);
  }
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const i = ++id;
    const timer = setTimeout(() => { pending.delete(i); reject(new Error("CDP timed out: " + method)); }, 20000);
    pending.set(i, (reply) => {
      clearTimeout(timer);
      if (reply.error) reject(new Error(method + ": " + JSON.stringify(reply.error)));
      else resolve(reply);
    });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  const evaluate = async (expression) => {
    const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
    if (r.result?.exceptionDetails) throw new Error("eval: " + JSON.stringify(r.result.exceptionDetails).slice(0, 300));
    return r.result?.result?.value;
  };
  const close = async () => {
    // Chrome may close the CDP socket before acknowledging Browser.close.
    try { await Promise.race([send("Browser.close"), sleep(1000)]); } catch {}
    try { ws.close(); } catch {}
    proc.kill();
    await sleep(500);
    try { fs.rmSync(profile, { recursive: true, force: true, maxRetries: 10, retryDelay: 300 }); }
    catch (e) { console.error("note: could not delete the scratch browser profile " + profile + " (" + e.code + "); it is only a temporary folder, the test result is not affected"); }   // 24 Oct 2026: a locked profile file made a passing run report failure
  };
  try {
    await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable"); await send("Network.enable");
    // Ordinary modes start after onboarding. The repairs mode exercises the real tour separately.
    await send("Page.addScriptToEvaluateOnNewDocument", { source: 'try { localStorage.setItem("ss-tour-3", "done"); } catch {}' });
  } catch (e) { await close(); throw e; }
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
    await goto(b, base);
    await waitFor(b, `!!document.querySelector(".sst-seg button")`);
    out.reducedMotion = await b.evaluate(`({ body: getComputedStyle(document.body).transitionDuration, content: getComputedStyle(document.querySelector(".md-content__inner")).animationName, contentDuration: getComputedStyle(document.querySelector(".md-content__inner")).animationDuration, toolbar: getComputedStyle(document.querySelector(".sst-seg button")).transitionDuration })`);
    await b.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
    await goto(b, base);
    await waitFor(b, `!!document.querySelector(".sst-seg button")`);
    out.normalMotion = await b.evaluate(`({ content: getComputedStyle(document.querySelector(".md-content__inner")).animationName + " " + getComputedStyle(document.querySelector(".md-content__inner")).animationDuration, toolbar: getComputedStyle(document.querySelector(".sst-seg button")).transitionDuration, link: getComputedStyle(document.querySelector(".md-tabs__link")).transitionDuration })`);
    out.hiddenShown = await b.evaluate(`[...document.querySelectorAll("[hidden]")].filter((e) => e.getClientRects().length).length`);
    out.paletteToggles = await b.evaluate(`[...document.querySelectorAll('[data-md-component="palette"] label')].filter((e) => e.getClientRects().length).length`);
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = out.hiddenShown === 0 && out.paletteToggles === 1 && !out.overflow.length && !out.small.length && !out.schemeMismatch.length && out.toggle.changes === 1 && out.toggle.before !== out.toggle.after
      && out.reducedMotion.body.split(",").every((t) => parseFloat(t) <= 0.001) && (out.reducedMotion.content === "none" || parseFloat(out.reducedMotion.contentDuration) <= 0.001) && out.reducedMotion.toolbar.split(",").every((t) => parseFloat(t) <= 0.001) && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

// Book 2's chapter template was removed from Book 3.
async function chapterLayout() {
  const retired = "Book 3 removed the chapter rail, margin-note sweep, chapter strip and fixed chapter-column template, including its line-length and column-width rules.";
  console.log("RETIRED chapter template: " + retired);
  const b = await launch("chapter"), out = { mode: "chapter", retired, checks: 0, fails: [] };
  try {
    // Keep the original narrow, breakpoint-adjacent and wide overflow sweep.
    for (const p of ["reference/for-astronomers/", "field-notes/2026-11-14/"]) {
      for (const [width, height] of [[390, 844], [683, 800], [1100, 800], [1119, 800], [1120, 800], [1366, 650], [1440, 900], [1500, 900]]) {
        await b.send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: width < 768 });
        await goto(b, base + p);
        await sleep(400);
        const overflow = await b.evaluate(`document.documentElement.scrollWidth - document.documentElement.clientWidth`);
        out.checks++;
        if (overflow > 0) out.fails.push(`${p} ${width}x${height}: sideways scroll +${overflow}px`);
      }
    }
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

async function offlineTest() {
  const b = await launch("offline");
  const out = { mode: "offline" };
  try {
    await b.send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    const expected = shellLength();
    await goto(b, base);
    out.precached = await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${expected})`);
    out.shell = `${await b.evaluate(SHELL_COUNT)} / ${expected}`;
    out.firstVisitNavigations = b.navigations.length;             // must be 1: the first install never reloads
    await goto(b, base + "training/");                  // a visited page
    await offline(b, true);
    out.pages = {};
    for (const p of ["", "candidates/", "glossary/", "claims/", "shelf/", "training/"]) {   // demo + search are tested on the last one
      await goto(b, base + p);
      out.pages[p || "/"] = await b.evaluate(PAGE_STATE);
    }
    console.log("RETIRED offline slider: the Book 2 dip-depth demo has no Book 3 page. Offline Tree interaction is checked instead.");
    await goto(b, base);
    // Tree design A (3.4.0): rows and branch cards, not the old canvas nodes. Four branches (PC cards or phone cards) and at least four rows.
    out.treeReady = await waitFor(b, `document.querySelectorAll(".ssta-row").length >= 4 && document.querySelectorAll("[data-branch], .ssta-phcard").length >= 4`);
    out.treeOffline = await b.evaluate(`(() => { document.querySelector('[data-view="journey"]').click(); return document.querySelectorAll(".sst-phase").length > 0 && document.querySelectorAll(".sst-day").length > 0; })()`);
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
    out.pass = out.precached && out.firstVisitNavigations === 1 && okPages && out.treeReady && out.treeOffline && out.search > 0 && out.unknownPage && out.unvisitedImage
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
  // Mutate only the disposable built copy. No source page or rebuild is needed.
  const index = path.join(opt.site, "index.html"), worker = path.join(opt.site, "sw.js");
  const original = fs.readFileSync(index, "utf8"), originalWorker = fs.readFileSync(worker, "utf8");
  const shells = () => b.evaluate(`caches.keys().then((k) => k.filter((x) => x.startsWith("ss-shell-")).sort())`);
  const publish = (letter) => {
    const version = Buffer.from(`book3-test-${letter}`).toString("hex");
    fs.writeFileSync(index, original.replace("</article>", `<p>Update test marker: version ${letter}.</p></article>`));
    fs.writeFileSync(worker, originalWorker.replace(/const VERSION = "[0-9a-f]+"/, `const VERSION = "${version}"`));
    return "ss-shell-" + version;
  };
  try {
    await goto(b, base);
    out.aReady = await waitFor(b, `navigator.serviceWorker.controller && ${SHELL_COUNT}.then((n) => n >= ${shellLength()})`);
    const a = (await shells())[0];
    out.versionA = a;
    // B is published. Reopening the book must show B at once (bug 62: it used to stay on A until Reload was tapped) and offer the update.
    const vb = publish("B");
    const navBefore = b.navigations.length;
    await goto(b, base);
    out.freshB = await waitFor(b, `document.body.innerText.includes("version B")`, 15000);
    out.lineShown = await waitFor(b, `document.querySelectorAll(".ss-update").length === 1`);
    await sleep(2000);
    out.linesAfter2s = await b.evaluate(`document.querySelectorAll(".ss-update").length`);
    out.barDismissible = await b.evaluate(`(async () => { const c = document.querySelector(".ss-update .ss-update__close"); if (!c || !document.body.classList.contains("ss-has-update") || c.getBoundingClientRect().height < 44) return false; c.click(); await new Promise((r) => setTimeout(r, 600)); return !document.querySelector(".ss-update") && !document.body.classList.contains("ss-has-update"); })()`);   // Book 3 animates dismissal for 300 ms. Keep the 44 px and eventual-removal checks.
    out.navigationsForB = b.navigations.length - navBefore;        // the reopen itself: 1, no extra reload
    out.cachesWithB = await shells();                               // A (running) and B (waiting)
    // C is published before anyone tapped Reload: B never ran, so its saved copy must be deleted when C installs.
    const vc = publish("C");
    await goto(b, base);
    out.freshC = await waitFor(b, `document.body.innerText.includes("version C")`, 15000);
    out.prunedB = await waitFor(b, `caches.keys().then((k) => { const s = k.filter((x) => x.startsWith("ss-shell-")); return s.length === 2 && s.includes(${JSON.stringify(vc)}) && s.includes(${JSON.stringify(a)}); })`, 30000);
    out.cachesWithC = await shells();
    const navAtClick = b.navigations.length;
    await b.evaluate(`document.querySelector(".ss-update button").click()`);
    await waitFor(b, `caches.keys().then((k) => k.filter((x) => x.startsWith("ss-shell-")).length === 1)`, 30000);
    await sleep(5000);                                              // watch for any extra reloads
    out.reloadsAfterClick = b.navigations.length - navAtClick;      // must be exactly 1
    out.onC = await b.evaluate(`document.body.innerText.includes("version C")`);
    out.cachesAfter = await shells();
    out.lineAfterReload = await b.evaluate(`document.querySelectorAll(".ss-update").length`);
    await offline(b, true);                                         // the new worker must still work offline
    await goto(b, base + "glossary/");
    out.offlineAfter = await b.evaluate(PAGE_STATE);
    out.errors = b.errors.filter((e) => !/ERR_INTERNET_DISCONNECTED/.test(e));
    out.pass = out.barDismissible && out.aReady && out.freshB && out.lineShown && out.linesAfter2s === 1 && out.navigationsForB === 1
      && out.cachesWithB.length === 2 && out.cachesWithB.includes(a) && out.cachesWithB.includes(vb)
      && out.freshC && out.prunedB && out.reloadsAfterClick === 1 && out.onC
      && out.cachesAfter.length === 1 && out.cachesAfter[0] === vc && out.lineAfterReload === 0
      && out.offlineAfter.controlled && out.offlineAfter.css > 900 && out.offlineAfter.text > 100 && !out.errors.length;
  } finally {
    fs.writeFileSync(index, original);
    fs.writeFileSync(worker, originalWorker);
    await b.close();
  }
  return out;
}

async function jsoff() {
  const b = await launch("jsoff"), out = { mode: "jsoff", pages: {}, checks: 0, fails: [] };
  console.log("RETIRED jsoff lesson quiz/demo: Book 2 lesson removed. Book 3 static Tree, native details and reading/navigation are checked instead.");
  try {
    await b.send("Emulation.setScriptExecutionDisabled", { value: true });
    for (const p of PAGES) {
      await goto(b, base + p);
      const state = await b.evaluate(`({ noJS: document.documentElement.classList.contains("no-js"), text: document.querySelector("article").innerText.length, links: document.querySelectorAll("article a[href]").length, redirect: !!document.querySelector('meta[name="ss-redirect"]') })`);
      out.pages[p || "/"] = state; out.checks++;
      if (!state.noJS || state.text < 50 || state.redirect) out.fails.push((p || "/") + ": missing no-JS reading content or redirected");
    }
    await goto(b, base);
    out.staticTree = await b.evaluate(`document.querySelector(".sst-static").checkVisibility() && document.querySelector(".sst-static").innerText.length > 100 && document.querySelectorAll(".sst-static li").length >= 15 && document.querySelectorAll("article a[href]").length > 0`);
    await goto(b, base + "eyes/");
    out.details = await b.evaluate(`(() => { const d = document.querySelector("details"); if (!d) return { exists: false }; const before = d.open; d.querySelector("summary").click(); return { exists: true, before, after: d.open, text: d.innerText.length }; })()`);
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && out.staticTree && out.details.exists && out.details.before !== out.details.after && out.details.text > 50 && !out.errors.length;
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
    await b.evaluate(`document.querySelectorAll("img").forEach((i) => { i.loading = "eager"; })`);
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
    ["training-390-dark", 390, "slate", "training/", null], ["eyes-details-390-dark", 390, "slate", "eyes/", "details"],
    ["search-open-390-dark", 390, "slate", "", "search"], ["shelf-1280-dark", 1280, "slate", "shelf/", null],
    ["shelf-1280-light", 1280, "default", "shelf/", null], ["search-1280-light", 1280, "default", "", "search"],
    ["claims-390-light", 390, "default", "claims/", null], ["journey-1280-dark", 1280, "slate", "", "journey", null],
  ];
  const out = { mode: "shots", files: [] };
  try {
    for (const [name, w, scheme, page, action] of list) {
      const pal = JSON.stringify({ index: scheme === "slate" ? 0 : 1, color: { media: "", scheme, primary: "custom", accent: "custom" } });
      const { result } = await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `localStorage.setItem(${JSON.stringify(new URL(base).pathname + ".__palette")}, ${JSON.stringify(pal)})` });
      await b.send("Emulation.setDeviceMetricsOverride", { width: w, height: w < 768 ? 844 : 900, deviceScaleFactor: 1, mobile: w < 768 });
      await goto(b, base + page);
      await waitFor(b, `!document.querySelector("#ss-splash") && !document.querySelector(".sst-grow")`, 8000);
      await sleep(400);
      if (action === "search") {
        await b.evaluate(`(() => { const i = document.querySelector(".md-search__input"); document.querySelector('label[for="__search"]').click(); i.focus(); i.value = "depth"; for (const t of ["focus","input","keyup"]) i.dispatchEvent(new Event(t, { bubbles: true })); })()`);
        await sleep(1500);
      }
      if (action === "details") {
        await b.evaluate(`(() => { const d = document.querySelector("details"); d.querySelector("summary").click(); d.scrollIntoView({ block: "center" }); })()`);
        await sleep(600);
      }
      if (action === "journey") {
        await waitFor(b, `!!document.querySelector('[data-view="journey"]')`);
        await b.evaluate(`document.querySelector('[data-view="journey"]').click()`);
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
    checks.easyFeedbackLines = banners.every((t) => /what the numbers say/i.test(t));
    checks.bannerSaysTruth = banners.every((t) => /THIS WAS: (A DIP|NOT A DIP)/.test(t) && /It was /.test(t) && /You said/.test(t));
    checks.lookBackShowsTruthAndAnswer = lookBackTexts.every((t) => /Looking back at light curve \d of 5 \(read only\)/.test(t) && /THIS WAS:/.test(t) && /You said/.test(t));
    let r = (await store())[0];
    checks.measuredStrengthSaved = r.a.every((e) => e.f && typeof e.f.st === "number" && e.f.dh > 0 && e.f.gr > 0);
    checks.practiceSaved = r.mode === "practice" && r.status === "done" && r.a.length === 5 && r.a.every((e) => e.ans && typeof e.ok === "boolean" && e.m && e.ms >= 0) && r.s.n === 5;
    checks.lookBacksRecorded = r.a.filter((e) => e.lb > 0).length >= 2;
    const fin = await text();
    checks.finishScreen = /How you did/.test(fin) && /Saved on this device: 1 round/.test(fin) && /Cloud backup is paused on this test copy of the book/.test(fin);   // local copies never write to Ahmed's real data
    checks.noUploadFromTestCopy = await b.evaluate(`window.SSEyesStore.unsynced().length === 1 && window.SSEyesStore.rounds()[0].sync !== 1`);
    checks.scoreLineFirst = (() => { const m = fin.match(/You got (\d+) of 5 right\./); return !!m && Number(m[1]) === r.a.filter((e) => e.ok).length && fin.indexOf("You got") < fin.indexOf("You looked at"); })();   // the plain score comes first (Ahmed: never open My results to find it)

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
      lastBanner = await text(); if (/THIS WAS:|what the numbers say/i.test(lastBanner)) leaked = true;
      if (i === 5) { await click("◀ Look at previous question"); const t = await text(); if (/THIS WAS:/.test(t) || !/You answered:/.test(t)) leaked = true; await click("Back to light curve 6"); }
      await clickAny(NEXT);
    }
    checks.testHidesTruth = !leaked;
    const tf = await text();
    checks.testFinish = /Test finished/.test(tf) && /Standard test · 1 round\(s\) · 30 curves/i.test(tf) && /Practice result, not an official pass: still needs/.test(tf) && /You found [\d.]+% of the clear dips\./.test(tf) && /Limit: at most 10%/.test(tf) && /Target: at least 85%/.test(tf) && /95% confidence interval/.test(tf) && !/Pass line so far/.test(tf);   // the old lines are behind "All the numbers" (closed)
    checks.testFinishDetails = await b.evaluate(`(() => { const d = document.querySelector(".ss-eyes details.ss-res__det"); return !!d && !d.open && /Pass line so far/.test(d.textContent) && /Not enough yet/.test(d.textContent) && /Test rounds: 1, curves: 30/.test(d.textContent); })()`);
    checks.testScoreLine = await (async () => { const m = tf.match(/You got (\d+) of 30 right\./); return !!m && Number(m[1]) === (await store())[0].a.filter((e) => e.ok).length; })();
    r = (await store())[0];
    checks.testSaved = r.mode === "test" && r.status === "done" && r.a.length === 30 && r.n === 30 && r.a.filter((e) => e.truth === "dip").length === 14 && r.a.filter((e) => e.truth === "none").length === 8;

    // ---- a round left half done, then a reload ----
    await click("Another sitting"); await click("5"); await click("Dip"); await clickAny(NEXT); await click("No dip");
    await goto(b, base + "eyes/");
    await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    await click("My results");
    const res = await text();
    const rounds = await store();
    checks.habitTable = /Your habit by strength/.test(res) && /Curves measured so far: \d+/.test(res) && /Strength (under 3|3 to 5|5 to 7|7 to 10|10 or more): you said Dip on \d+ of \d+ curves/.test(res);
    checks.resultsAfterReload =/3 round\(s\) saved on this device/.test(res) && /abandoned/.test(res) && /done/.test(res);
    checks.abandonedKept = rounds.length === 3 && rounds[0].status === "abandoned" && rounds[0].a.length === 2;
    checks.resultsTable = await b.evaluate(`document.querySelectorAll(".ss-eyes__table tbody tr").length === 3 && document.querySelector(".ss-eyes__table thead").innerText.includes("False alarms")`);
    checks.noCopyOption = !/copy (my|the|your)? ?results|paste|export|send (it |them )?to claude/i.test(res) && !(await b.evaluate(`document.querySelector(".ss-eyes textarea") !== null || [...document.querySelectorAll(".ss-eyes button")].some((x) => /copy|paste|export/i.test(x.textContent))`));   // Ahmed: never make me hand over my results
    checks.exportApiForTheUpload = await b.evaluate(`(() => { const j = JSON.parse(window.SSEyesStore.exportJSON()); return j.schema === 1 && j.rounds.length === 3 && !!j.device.id; })()`);

    // ---- the HARD test: its own cards and its own line, with the official pass line left alone ----
    await click("Back");
    checks.hardButtons = (await visible("Take the HARD test (30 curves)")) && (await visible("Hard practice 20")) && (await visible("Hard practice 50"));
    await click("Take the HARD test (30 curves)");
    let hleak = false;
    for (let i = 0; i < 30; i++) { await click(cyc[i % 4]); if (/THIS WAS:|what the numbers say/i.test(await text())) hleak = true; await clickAny(NEXT); }
    checks.hardTestHidesTruth = !hleak;
    const hf = await text();
    checks.hardFinish = /Test finished/.test(hf) && /Hard test · 1 round\(s\) · 30 curves/i.test(hf) && !/Pass line so far/.test(hf) && /You found [\d.]+% of the clear fake planets\./.test(hf) && /Practice result, not an official pass: still needs/.test(hf) && /Limit: at most 20%/.test(hf);
    checks.hardFinishDetails = await b.evaluate(`(() => { const d = document.querySelector(".ss-eyes details.ss-res__det"); return !!d && !d.open && /Hard line so far/.test(d.textContent) && /Hard test rounds: 1, curves: 30/.test(d.textContent) && /Clear fake planets/.test(d.textContent); })()`);
    await click("Review this round"); const hrv = await text(); checks.hardReviewShowsNumbers = /what the numbers say/i.test(hrv) && /light curve 1 of 30 \(read only\)/.test(hrv); await click("Close the review");
    const hr = (await store())[0], tc = (t) => hr.a.filter((e) => e.t === t).length;
    checks.hardTestSaved = hr.mode === "test" && /^hard/.test(hr.source) && hr.status === "done" && hr.a.length === 30 && tc("clear") === 6 && tc("border") === 6 && tc("hardnoise") === 8 && tc("odd") === 10 && hr.a.some((e) => e.ans === "unsure") && hr.a.every((e) => e.m && e.m.seed > 0 && e.f && typeof e.f.st === "number");
    await click("My results");
    const hres = await text();
    checks.hardInResults = /Hard test · 1 round\(s\) · 30 curves/i.test(hres) && /test \(hard\)/.test(hres) && /Standard test · 1 round\(s\) · 30 curves/i.test(hres);          // the official pass line still counts only the official test
    checks.resultsDetailsClosed = await b.evaluate(`(() => { const d = document.querySelector(".ss-eyes details.ss-res__det"); return !!d && !d.open && /Official test pass line/.test(d.textContent) && /Hard test line/.test(d.textContent); })()`);
    await click("Back");
    checks.resultsReturnToFinish = /Test finished/.test(await text()) && await visible("Another sitting");
    await click("Another sitting");
    checks.hardPracticeStarts = await click("Hard practice 20") && await click("Dip");
    checks.hardPracticeShowsTruth = /THIS WAS: (A DIP|NOT A DIP)/.test(await text());
    checks.plotBarExplained = /dashed line is how deep a dip must be here to score 7/.test(await text());
    const fbl = await b.evaluate(`[...document.querySelectorAll(".ss-eyes__fb")].map((e) => e.textContent)`), fbw = fbl.join(" ").split(/\s+/).filter(Boolean).length;
    checks.hardPracticeFeedback = fbl.length === 3 && fbw >= 36 && fbw <= 44 && !/missed/.test(fbl.join(" ")) && !/[–—]/.test(fbl.join(" "));

    // ---- twin drill: the same noise twice, which curve hides the planet; it must never be saved ----
    await goto(b, base + "eyes/"); await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    const roundsBefore = (await store()).length;
    checks.twinButton = await visible("Twin drill 10");
    await click("Twin drill 10");
    let twinOk = true;
    for (let i = 0; i < 10; i++) {
      await click(["Top", "Bottom", "Not sure"][i % 3]); const tt = await text();
      if (!/THE PLANET WAS IN THE (TOP|BOTTOM) CURVE/.test(tt) || !/Measured strength: top [\d.]+, bottom [\d.]+/.test(tt)) twinOk = false;
      await clickAny(["Next pair", "See how you did"]);
    }
    const twinEnd = await text();
    checks.twinDrillRuns = twinOk && /Twin drill finished/.test(twinEnd) && /You found the planet in \d+ of 10 pairs/.test(twinEnd) && /not saved, not sent anywhere/.test(twinEnd);
    checks.twinDrillSavesNothing = (await store()).length === roundsBefore && !(await b.evaluate(`JSON.stringify(window.SSEyesStore.rounds()).includes("twin")`));

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
    // ---- a visitor (a brand-new device) can play, and nothing is sent anywhere ----
    checks.visitorStatus = /You are a visitor here, so nothing you do is sent anywhere/.test(await text());
    await click("5"); for (let i = 0; i < 5; i++) { await click(["Dip", "No dip", "Odd", "Not sure", "Dip"][i]); await clickAny(NEXT); }
    await sleep(2500);
    checks.visitorSendsNothing = mock.calls.length === 0 && mock.docs.size === 0 && /You are a visitor here/.test(await text()) && (await store()).length === 1;
    await b.evaluate(`localStorage.clear()`);                                // the owner link then makes a brand-new device Ahmed's; start clean
    await goto(b, base + "eyes/?o=1#owner"); await waitFor(b, `!!document.querySelector(".ss-eyes button")`);
    checks.ownerLinkWorks = (await b.evaluate(`localStorage.getItem("ss-eyes-owner")`)) === "1" && (await b.evaluate(`location.hash`)) === "";
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
    await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `window.SSEYES_CLOUD_ALLOW_LOCAL = true; try { localStorage.setItem("ss-eyes-owner", "1"); } catch (e) {}` });   // this one test is allowed to write to the real cloud (labelled e2e-test, deleted after)
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

// F4 step 3 (Claude AI's review): the Eyes screen at every size. The curve is as tall as its aspect needs (170 to 340 px, never a share of the window), the four answers share a
// row where there is room, the Next bar has a reserved slot and is pinned only once it can be pressed, nothing overlaps, every target is 44 px, and the keyboard focus is never dropped.
const EYES_CLICK = (t) => `(() => { const b = [...document.querySelectorAll(".ss-eyes button")].find((x) => x.textContent.trim() === ${JSON.stringify(t)} && x.offsetParent !== null && !x.disabled); if (!b) return false; b.click(); return true; })()`;
const EYES_MEASURE = `(() => {
  const R = (e) => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height }; };
  const q = (s) => document.querySelector(s), vis = (e) => !!e && e.offsetParent !== null && e.getBoundingClientRect().width > 0;
  const stage = q(".ss-eyes"), cv = q(".ss-eyes__cv"), banner = q(".ss-eyes__banner"), nextRow = q(".ss-eyes__next");
  const btns = [...stage.querySelectorAll("button")].filter(vis), ans = [...q(".ss-eyes__ans").children].filter(vis);
  const next = btns.find((b) => /^(Next|Finish the test|See how you did)$/.test(b.textContent.trim()));
  const items = [["curve", cv], ...ans.map((b, i) => ["answer " + (i + 1), b]), ...(vis(banner) ? [["feedback", banner]] : []), ...(next ? [["next", next]] : [])], overlaps = [];
  for (let i = 0; i < items.length; i++) for (let j = i + 1; j < items.length; j++) {
    const a = R(items[i][1]), c = R(items[j][1]); if (Math.min(a.r, c.r) - Math.max(a.l, c.l) > 1 && Math.min(a.b, c.b) - Math.max(a.t, c.t) > 1) overlaps.push(items[i][0] + " x " + items[j][0]); }
  const ae = document.activeElement, ao = ae && getComputedStyle(ae);
  return { vw: innerWidth, vh: innerHeight, over: document.documentElement.scrollWidth - innerWidth, hdr: R(q(".md-header")).b, stage: R(stage), cv: R(cv), cvh: Math.round(parseFloat(cv.style.height)),
    ans: ans.map(R), banner: vis(banner) ? R(banner) : null, next: next ? R(next) : null, nextRow: R(nextRow), rowPos: getComputedStyle(nextRow).position, overlaps,
    small: btns.filter((b) => { const r = b.getBoundingClientRect(); return r.height < 43.5 || r.width < 43.5; }).map((b) => b.textContent.trim()),
    prog: q(".ss-eyes__prog").textContent, active: ae ? ae.textContent.trim() : "", ring: ao ? parseFloat(ao.outlineWidth) * (ao.outlineStyle === "none" ? 0 : 1) : 0,
    truth: (q(".ss-eyes__truth") || {}).textContent || "", you: !!q(".ss-eyes__you"), fb: document.querySelectorAll(".ss-eyes__fb").length };
})()`;
async function eyesLayout() {
  const b = await launch("eyeslayout");
  const out = { mode: "eyeslayout", checks: 0, fails: [], sizes: [] };
  const fail = (m) => out.fails.push(m), ok = (c, m) => { out.checks++; if (!c) fail(m); };
  const key = async (k, code, vk) => { await b.send("Input.dispatchKeyEvent", { type: "keyDown", key: k, code, windowsVirtualKeyCode: vk, text: k === "Enter" ? "\r" : undefined }); await b.send("Input.dispatchKeyEvent", { type: "keyUp", key: k, code, windowsVirtualKeyCode: vk }); };
  const toStage = async (how) => b.evaluate(how === "end" ? `document.querySelector(".ss-eyes").scrollIntoView({ block: "end" })` : `(() => { const h = document.querySelector(".md-header").getBoundingClientRect().bottom, p = document.querySelector(".ss-eyes__prog"); scrollTo(0, p.getBoundingClientRect().top + scrollY - h - 8); })()`);
  try {
    for (const [w, h] of [[390, 844], [683, 325], [1024, 768], [1366, 650], [1440, 900]]) {
      const tag = `${w}x${h}`, wide = w >= 1220, row = w >= 640;
      await b.send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 768 });
      await goto(b, base + "eyes/");
      ok(await waitFor(b, `!!document.querySelector(".ss-eyes button")`, 15000), `${tag}: Eyes did not start`);
      ok(await b.evaluate(EYES_CLICK("5")), `${tag}: no 5-curve practice button`);
      await sleep(400);
      // the question, before any answer
      await toStage("end"); await sleep(150);
      const q = await b.evaluate(EYES_MEASURE);
      const want = Math.min(340, Math.max(170, q.cv.w * 0.55));
      ok(q.over <= 1, `${tag}: sideways scroll +${q.over}`);
      ok(Math.abs(q.cvh - want) <= 1 && q.cvh >= 170 && q.cvh <= 340, `${tag}: curve is ${q.cvh} px tall for ${Math.round(q.cv.w)} wide (want ${Math.round(want)}, between 170 and 340)`);
      ok(q.ans.length === 4, `${tag}: ${q.ans.length} answer buttons`);
      ok(!q.small.length, `${tag}: targets under 44 px: ${q.small.join(", ")}`);
      ok(!q.overlaps.length, `${tag}: overlap before answering: ${q.overlaps.join(", ")}`);
      ok(q.ans.every((a) => a.r <= q.stage.r + 1 && a.l >= q.stage.l - 1), `${tag}: an answer sticks out of the box`);
      if (row) ok(q.ans.every((a) => Math.abs(a.t - q.ans[0].t) <= 1), `${tag}: the four answers should share one row`);
      ok(q.rowPos !== "sticky" && q.nextRow.h >= 60, `${tag}: before an answer the Next slot should be reserved (${Math.round(q.nextRow.h)} px) and not pinned (${q.rowPos})`);
      // the answer
      ok(await b.evaluate(EYES_CLICK("Dip")), `${tag}: no Dip button`);
      await sleep(500);
      await toStage("end"); await sleep(150);
      const a = await b.evaluate(EYES_MEASURE);
      ok(a.over <= 1, `${tag}: sideways scroll after answering +${a.over}`);
      ok(!!a.banner && /this was/i.test(a.truth) && a.you && a.fb >= 1, `${tag}: feedback incomplete (truth "${a.truth}", you ${a.you}, lines ${a.fb})`);
      ok(!!a.next && a.next.h >= 43.5 && a.active === "Next",`${tag}: Next should hold the focus after an answer (focus on "${a.active}")`);
      ok(!a.small.length, `${tag}: targets under 44 px after answering: ${a.small.join(", ")}`);
      ok(!a.overlaps.length, `${tag}: overlap after answering: ${a.overlaps.join(", ")}`);
      ok(Math.abs(a.nextRow.h - q.nextRow.h) <= 1, `${tag}: the Next slot changed height (${Math.round(q.nextRow.h)} to ${Math.round(a.nextRow.h)}), so the page would jump`);
      ok(a.rowPos === "sticky", `${tag}: the Next bar should be pinned once it can be pressed (${a.rowPos})`);
      ok(Math.abs((a.cv.t - a.stage.t) - (q.cv.t - q.stage.t)) <= 1 && Math.abs(a.cv.w - q.cv.w) <= 1,`${tag}: the curve moved or resized when the feedback appeared`);
      await toStage("top"); await sleep(250);
      const t = await b.evaluate(EYES_MEASURE);
      ok(!!t.next && t.next.t >= 0 && t.next.b <= t.vh + 1, `${tag}: with the curve at the top of the window the Next button is off screen (${t.next && Math.round(t.next.t)} to ${t.next && Math.round(t.next.b)} of ${t.vh})`);
      if (wide) {
        ok(t.cv.t >= t.hdr - 1 && t.cv.b <= t.vh, `${tag}: the whole curve should show (${Math.round(t.cv.t)} to ${Math.round(t.cv.b)}, window ${t.vh}, header ends ${Math.round(t.hdr)})`);
        ok(!!t.banner && t.banner.b <= t.vh && t.banner.l >= t.cv.r + 8, `${tag}: the feedback should sit beside the curve and fit the window (${t.banner && Math.round(t.banner.b)} of ${t.vh})`);
        ok(t.ans.every((x) => x.b <= t.vh) && t.next.b <= t.vh, `${tag}: answers and Next should be on screen together with the curve`);
      }
      // the keyboard: Enter on Next moves on, and the focus lands on the first answer, with a visible ring
      await b.evaluate(`document.activeElement.focus()`);
      await key("Enter", "Enter", 13); await sleep(400);
      const k = await b.evaluate(EYES_MEASURE);
      ok(/Light curve 2 of 5/.test(k.prog), `${tag}: Enter on Next did not move to curve 2 ("${k.prog}")`);
      ok(k.active === "Dip", `${tag}: keyboard focus was dropped after Next (it is on "${k.active}", want the first answer)`);
      ok(k.ring >= 2, `${tag}: the focused answer has no visible ring (${k.ring} px)`);
      out.sizes.push({ tag, cvh: q.cvh, cvw: Math.round(q.cv.w), rowH: Math.round(q.nextRow.h), bannerB: t.banner && Math.round(t.banner.b), nextB: t.next && Math.round(t.next.b) });
    }
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length && out.checks >= 70;
  } finally { await b.close(); }
  return out;
}

async function rehearsalTest() {
  const b = await launch("rehearsal");
  const out = { mode: "rehearsal", checks: 0, fails: [], sizes: [] };
  const fail = (m) => out.fails.push(m), ok = (c, m) => { out.checks++; if (!c) fail(m); };
  const press = (k) => b.evaluate(`document.dispatchEvent(new KeyboardEvent("keydown", { key: ${JSON.stringify(k)}, bubbles: true }))`);
  const saved = () => b.evaluate(`JSON.parse(localStorage.getItem("ss-rehearsal-v1") || "{\\"rounds\\":[]}").rounds`);
  const MEASURE = `(() => { const r = (e) => { const x = e.getBoundingClientRect(); return { w: x.width, h: x.height, l: x.left, r: x.right, t: x.top, b: x.bottom }; };
    const btns = [...document.querySelectorAll(".ss-rh button")].filter((e) => !e.hidden && e.offsetParent);
    return { over: document.documentElement.scrollWidth - window.innerWidth, vw: window.innerWidth, svgs: [...document.querySelectorAll(".ss-rh__panel svg")].map((s) => r(s)),
      ans: [...document.querySelectorAll(".ss-rh__a")].map((e) => ({ ...r(e), dis: e.disabled, on: e.getAttribute("aria-pressed") })), small: btns.filter((e) => r(e).h < 44).map((e) => e.textContent.trim().slice(0, 14)),
      lock: (() => { const l = document.querySelector(".ss-rh__lock"); return l ? { dis: l.disabled, hid: l.hidden, h: r(l).h } : null; })(), out: (document.querySelector(".ss-rh__out") || {}).innerText || "",
      next: (() => { const n = document.querySelector(".ss-rh__next"); return n && !n.hidden ? r(n) : null; })(), prog: (document.querySelector(".ss-rh__prog") || {}).innerText || "", caps: document.querySelectorAll(".ss-rh__cap").length }; })()`;
  try {
    for (const [w, h] of [[390, 844], [768, 1024], [1440, 900]]) {
      const tag = `${w}x${h}`;
      await b.send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 768 });
      await goto(b, base + "rehearsal/");
      await b.evaluate(`localStorage.removeItem("ss-rehearsal-v1")`);
      await goto(b, base + "rehearsal/");
      ok(await waitFor(b, `!!document.querySelector(".ss-rh__go")`, 15000), `${tag}: the start button did not appear (deck not loaded?)`);
      ok(/Start session 1 of 8/.test(await b.evaluate(`document.querySelector(".ss-rh__go").textContent`)), `${tag}: the first button should offer session 1 of 8`);
      await b.evaluate(`document.querySelector(".ss-rh__go").click()`);
      ok(await waitFor(b, `document.querySelectorAll(".ss-rh__a").length === 6`, 8000), `${tag}: six answer buttons expected`);
      await sleep(300);
      const q = await b.evaluate(MEASURE);
      ok(q.over <= 1, `${tag}: sideways scroll +${q.over}`);
      ok(q.svgs.length === 3 && q.svgs.every((s) => s.w > 100), `${tag}: three panels expected, got ${q.svgs.length}`);
      ok(q.svgs[1] && q.svgs[1].h >= 130 && q.svgs[1].h > q.svgs[0].h && q.svgs[0].h > q.svgs[2].h, `${tag}: panel heights should run P2 > P1 > P3 (${q.svgs.map((s) => Math.round(s.h)).join(", ")})`);
      ok(q.ans.length === 6 && q.ans.every((a) => a.on === "false"), `${tag}: six answers, none pre-selected`);
      ok(!q.small.length, `${tag}: targets under 44 px: ${q.small.join(", ")}`);
      ok(q.lock && q.lock.dis === true, `${tag}: Lock must be disabled until an answer is chosen`);
      ok(q.ans.every((a) => a.r <= q.vw + 1 && a.l >= -1), `${tag}: an answer sticks out of the window`);
      ok(/Item 1 of 20/i.test(q.prog) && q.caps === 3 && q.out === "", `${tag}: item 1 of 20, three captions, nothing revealed yet ("${q.prog}")`);
      if (w >= 900) ok(Math.abs(q.ans[0].t - q.ans[5].t) <= 1, `${tag}: on a wide screen the six answers should share one row`);
      await b.evaluate(`document.querySelector('.ss-rh__a[data-a="planet"]').click()`);
      await b.evaluate(`[...document.querySelectorAll(".ss-rh__c")].find((e) => e.textContent === "medium").click()`);
      const mid = await b.evaluate(MEASURE);
      ok(mid.lock.dis === false && mid.ans[0].on === "true", `${tag}: choosing an answer should enable Lock and mark the choice`);
      await b.evaluate(`document.querySelector(".ss-rh__lock").click()`); await sleep(200);
      const a = await b.evaluate(MEASURE);
      ok(/THIS WAS:/.test(a.out) && /You said Planet-like/.test(a.out) && /hit|miss|false alarm|correct/.test(a.out), `${tag}: the truth and your answer should be shown ("${a.out.slice(0, 60)}")`);
      ok(a.ans.every((x) => x.dis) && a.lock.hid === true && !!a.next && a.next.h >= 44, `${tag}: after locking the answers are disabled, Lock is gone, Next is there`);
      ok(a.over <= 1 && !a.small.length, `${tag}: sideways scroll or small targets after locking (+${a.over}, ${a.small.join(",")})`);
      let r = await saved();
      ok(r.length === 1 && r[0].status === "open" && r[0].a.length === 1 && r[0].a[0].conf === "medium" && r[0].mode === "practice" && r[0].source === "rehearsal-v1", `${tag}: the answer must be saved at once as an open round`);
      await b.evaluate(`document.querySelector(".ss-rh__next").click()`); await sleep(250);
      ok(/Item 2 of 20/i.test((await b.evaluate(MEASURE)).prog), `${tag}: Next should move to item 2`);
      await press("3"); await press("Enter"); await sleep(200);
      ok(/THIS WAS:/.test((await b.evaluate(MEASURE)).out), `${tag}: keys 3 then Enter should lock an answer`);
      await press("Enter"); await sleep(250);
      ok(/Item 3 of 20/i.test((await b.evaluate(MEASURE)).prog), `${tag}: Enter after the truth should move to item 3`);
      r = await saved(); ok(r[0].a.length === 2 && r[0].a[1].ans === "flare", `${tag}: the keyboard answer should be saved (${r[0].a.map((x) => x.ans)})`);
      await goto(b, base + "rehearsal/");
      ok(await waitFor(b, `!!document.querySelector(".ss-rh__go")`, 15000), `${tag}: no start button after coming back`);
      r = await saved(); ok(r.length === 1 && r[0].status === "abandoned" && r[0].a.length === 2, `${tag}: the half-done session must be kept as abandoned with its 2 answers`);
      ok(/Start session 1 of 8/.test(await b.evaluate(`document.querySelector(".ss-rh__go").textContent`)) && /Sessions 0 of 8/.test(await b.evaluate(`document.querySelector(".ss-rh__results").innerText`)), `${tag}: an abandoned session does not count`);
      out.sizes.push({ tag, p1: Math.round(q.svgs[0].h), p2: Math.round(q.svgs[1].h), p3: Math.round(q.svgs[2].h) });
    }
    await b.send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
    await goto(b, base + "rehearsal/"); await b.evaluate(`localStorage.removeItem("ss-rehearsal-v1")`); await goto(b, base + "rehearsal/");
    await waitFor(b, `!!document.querySelector(".ss-rh__go")`, 15000); await b.evaluate(`document.querySelector(".ss-rh__go").click()`);
    for (let i = 0; i < 20; i++) {
      await waitFor(b, `document.querySelectorAll(".ss-rh__a").length === 6 && !document.querySelector(".ss-rh__a").disabled`, 5000);
      await b.evaluate(`document.querySelector('.ss-rh__a[data-a="noise"]').click(); document.querySelector(".ss-rh__lock").click(); document.querySelector(".ss-rh__next").click()`);
    }
    ok(await waitFor(b, `/Session 1 finished/.test(document.body.innerText)`, 8000), "a whole session of 20 reaches the end screen");
    const fin = await saved(); ok(fin.length === 1 && fin[0].status === "done" && fin[0].a.length === 20 && fin[0].s.n === 20, "a finished session is saved as done with 20 answers and a summary");
    ok(await b.evaluate(`/Sessions 1 of 8/.test(document.body.innerText)`), "the pass line counts the finished session");
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length && out.checks >= 40;
  } finally { await b.close(); }
  return out;
}

// The rehearsal's cloud wiring end to end against a mock of Firestore (same mock rules as eyescloud): a visitor sends nothing; Ahmed's device sends one finished session, once, in the shape the published rules accept.
async function rehearsalCloudTest() {
  const http = await import("node:http");
  const mock = { calls: [], docs: new Map() };
  const rulesOk = (f, id) => JSON.stringify(Object.keys(f).sort()) === JSON.stringify(["a", "device", "id", "mode", "n", "s", "source", "status", "t0", "t1", "v"])
    && f.v.integerValue === "1" && f.id.stringValue === id && ["practice", "test", "real"].includes(f.mode.stringValue) && Number(f.n.integerValue) <= 200 && !!f.a.arrayValue && (f.a.arrayValue.values || []).length <= 200;
  const server = http.createServer((req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*"); res.setHeader("Access-Control-Allow-Headers", "content-type"); res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    if (req.method === "OPTIONS") { res.statusCode = 204; return res.end(); }
    let raw = ""; req.on("data", (c) => (raw += c)); req.on("end", () => {
      const u = new URL(req.url, "http://x"), id = u.searchParams.get("documentId"); let code = 200;
      try {
        const body = JSON.parse(raw), good = req.method === "POST" && u.pathname === "/v1/projects/second-sun-faea5/databases/(default)/documents/eyes_rounds" && u.searchParams.get("key") === "AIzaSyBogX_Jte_4fahJ1Ovp3y-twCmxheLTSxY" && rulesOk(body.fields, id);
        mock.calls.push({ id, good });
        if (!good) code = 403; else if (mock.docs.has(id)) code = 409; else mock.docs.set(id, body);
      } catch (e) { code = 400; }
      res.statusCode = code; res.setHeader("Content-Type", "application/json"); res.end("{}");
    });
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const port = server.address().port;
  const b = await launch("rehearsalcloud"), out = { mode: "rehearsalcloud", checks: 0, fails: [] };
  const ok = (c, m) => { out.checks++; if (!c) out.fails.push(m); };
  const playSession = async () => {
    ok(await waitFor(b, `!!document.querySelector(".ss-rh__go")`, 15000), "the start button did not appear");
    await b.evaluate(`document.querySelector(".ss-rh__go").click()`);
    for (let i = 0; i < 20; i++) {
      await waitFor(b, `document.querySelectorAll(".ss-rh__a").length === 6 && !document.querySelector(".ss-rh__a").disabled`, 5000);
      await b.evaluate(`document.querySelector('.ss-rh__a[data-a="noise"]').click(); document.querySelector(".ss-rh__lock").click(); document.querySelector(".ss-rh__next").click()`);
    }
    ok(await waitFor(b, `/Session \\d+ finished/.test(document.body.innerText)`, 8000), "a whole session of 20 reaches the end screen");
  };
  try {
    await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `window.SSEYES_CLOUD_BASE = "http://127.0.0.1:${port}";` });
    await b.send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
    await goto(b, base + "rehearsal/"); await b.evaluate(`localStorage.clear()`); await goto(b, base + "rehearsal/");
    await playSession(); await sleep(2500);
    ok(mock.calls.length === 0 && mock.docs.size === 0, `a visitor's finished session must be sent nowhere (${mock.calls.length} calls)`);
    ok(/visitor/i.test(await b.evaluate(`document.querySelector(".ss-rh__cloud").innerText`)), "a visitor is told nothing is sent");
    await b.evaluate(`localStorage.clear()`);
    await goto(b, base + "rehearsal/?o=1#owner");
    ok((await b.evaluate(`localStorage.getItem("ss-eyes-owner")`)) === "1", "the owner link makes this device Ahmed's");
    await playSession();
    ok(await waitFor(b, `/safe in the cloud/.test(document.querySelector(".ss-rh__cloud").innerText)`, 15000), "the page should say the finished session is safe in the cloud");
    ok(mock.docs.size === 1 && mock.calls.every((c) => c.good), `exactly one document, in the shape the rules accept (${mock.docs.size} docs, ${mock.calls.filter((c) => !c.good).length} refused)`);
    const f = [...mock.docs.values()][0].fields;
    ok(f.source.stringValue === "rehearsal-v1" && f.mode.stringValue === "practice" && f.status.stringValue === "done" && f.n.integerValue === "20" && f.a.arrayValue.values.length === 20, "the document is a finished 20-answer rehearsal round");
    ok(f.a.arrayValue.values[0].mapValue.fields.cls !== undefined && f.s.mapValue !== undefined, "each answer carries its class and the round carries a summary");
    await sleep(1500);
    ok(mock.calls.length === 1, `the round is sent once, not repeated (${mock.calls.length} calls)`);
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length;
  } finally { await b.close(); server.close(); }
  return out;
}

// FIX-QUEUE 64: the Search window must keep ONE refresh loop however often the page is visited by instant navigation, and none once the reader has left it. Counts requests for watch.json.
async function watchTimersTest() {
  const b = await launch("watchtimers"), out = { mode: "watchtimers", checks: 0, fails: [] };
  const ok = (c, m) => { out.checks++; if (!c) out.fails.push(m); };
  try {
    await b.send("Page.addScriptToEvaluateOnNewDocument", { source: `window.__wj = []; const of = window.fetch.bind(window); window.fetch = (u, o) => { if (String(u).includes("watch.json")) window.__wj.push(Date.now()); return of(u, o); };` });
    await goto(b, base + `watch/?src=${encodeURIComponent(base + "assets/data/watch.json")}&every=5`);
    ok(await waitFor(b, `!!document.getElementById("ss-watch") && document.querySelectorAll("#ss-watch *").length > 3`, 15000), "the Search window did not draw from the snapshot");
    // Instant navigation only runs on the real host (a local copy loads every page afresh), so a visit is simulated the way Material does it: a fresh page element, then document$ emits.
    ok(await b.evaluate(`typeof document$ !== "undefined" && typeof document$.next === "function"`), "Material's document$ is not available to simulate instant navigation");
    const revisit = `(() => { const old = document.getElementById("ss-watch"); const fresh = document.createElement(old.tagName); fresh.id = "ss-watch"; old.replaceWith(fresh); document$.next(document); })()`;
    const leave = async () => { await b.evaluate(`(() => { const old = document.getElementById("ss-watch"); if (old) old.remove(); document$.next(document); })()`); await sleep(400); };
    for (let i = 0; i < 3; i++) {
      await b.evaluate(revisit);
      ok(await waitFor(b, `document.querySelectorAll("#ss-watch *").length > 3`, 8000), `visit ${i + 2}: the window did not draw`); await sleep(400);
    }
    await b.evaluate(`window.__wj.length = 0`); await sleep(16000);
    const here = await b.evaluate(`window.__wj.length`);
    ok(here >= 2 && here <= 5, `on the page after 4 visits: ${here} requests in 16 s at every=5 (one loop gives 3 to 4; one loop per visit would give 12 or more)`);
    await leave(); await b.evaluate(`window.__wj.length = 0`); await sleep(12000);
    const away = await b.evaluate(`window.__wj.length`);
    ok(away <= 1, `after leaving the page ${away} requests in 12 s (should be none)`);
    out.requests = { onPageIn16s: here, awayIn12s: away };
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

// FIX-QUEUE 63: the header shows the site name only, before and after the page heading scrolls away (Material used to swap in the page title in another style).
async function headerTitleTest() {
  const b = await launch("headertitle"), out = { mode: "headertitle", checks: 0, fails: [], pages: {} };
  const ok = (c, m) => { out.checks++; if (!c) out.fails.push(m); };
  try {
    for (const path of ["shelf/", "reference/for-astronomers/", "field-notes/2026-11-14/"]) {
      await goto(b, base + path); await sleep(500);
      const read = () => b.evaluate(`(() => { const t = [...document.querySelectorAll(".md-header__topic")]; const vis = (e) => e && getComputedStyle(e).display !== "none" && Number(getComputedStyle(e).opacity) > 0.5; return { n: t.length, first: vis(t[0]), second: vis(t[1]), text: t[0] ? t[0].innerText.trim() : "" }; })()`);
      const top = await read();
      await b.evaluate(`window.scrollTo(0, 1400)`); await sleep(900);
      const down = await read();
      out.pages[path] = { top, down };
      ok(top.first && !top.second && down.first && !down.second && /second sun/i.test(down.text), `${path}: the site name must stay and the page title must never show (top ${JSON.stringify(top)}, scrolled ${JSON.stringify(down)})`);
    }
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

// FIX-QUEUE 68 (3 Nov 2026, Ahmed: "u handle it"): no readable text under 14 px on a phone (375 px wide). Every visible HTML text node is judged by its computed size; SVG text scales with its figure and is covered by the layout checks.
async function textFloorTest() {
  const b = await launch("textfloor"), out = { mode: "textfloor", checks: 0, fails: [], pages: {} };
  try {
    await b.send("Emulation.setDeviceMetricsOverride", { width: 375, height: 844, deviceScaleFactor: 1, mobile: true });
    for (const path of [...new Set([...PAGES, "watch/", "versions/", "glossary/"])]) {
      await goto(b, base + path); await sleep(700);
      const bad = await b.evaluate(`(() => { const bad = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        while (w.nextNode()) { const n = w.currentNode; if (!n.nodeValue.trim()) continue; const e = n.parentElement; if (!e || e.closest("svg,script,style,noscript,template,[hidden]")) continue;
          const cs = getComputedStyle(e); if (cs.visibility !== "visible" || cs.display === "none") continue; const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
          const px = parseFloat(cs.fontSize); if (px < 13.99) { const k = e.tagName.toLowerCase() + (typeof e.className === "string" && e.className.trim() ? "." + e.className.trim().split(/\s+/).join(".") : ""); (bad[k] = bad[k] || { n: 0, px }).n++; } }
        return bad; })()`);
      out.checks++;
      if (Object.keys(bad).length) { out.pages[path] = bad; out.fails.push(path + ": " + Object.entries(bad).slice(0, 6).map(([k, v]) => `${k} ${v.px}px x${v.n}`).join("; ")); }
    }
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\.js/.test(e));
    out.pass = !out.fails.length && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

async function learnTest() {
  const manifest = JSON.parse(fs.readFileSync(path.join(opt.site, "assets/data/learn.json"), "utf8"));
  const lessons = manifest.units.flatMap(unit => unit.lessons).filter(lesson => lesson.url);
  const b = await launch("learn");
  const out = { mode: "learn", checks: 0, fails: [], views: [], texToWords: "NOT TESTED: say() is private to learn.js; no page API exposes it" };
  const ok = (value, message) => { out.checks++; if (!value) out.fails.push(message); };
  out.lessons = lessons.map(({ id, url }) => ({ id, url }));
  ok(lessons.length > 0, "built manifest has live lessons");
  const click = async (selector) => {
    const found = await b.evaluate(`(() => { const e = document.querySelector(${JSON.stringify(selector)}); if (!e) return false; e.scrollIntoView({block:"center",behavior:"instant"}); return true; })()`);
    if (!found) return false;
    // Scroll-driven header changes can move controls after scrollIntoView.
    await sleep(180);
    const point = await b.evaluate(`(() => { const r = document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect(),v=visualViewport; return {x:(r.x+r.width/2-v.offsetLeft)*v.scale,y:(r.y+r.height/2-v.offsetTop)*v.scale}; })()`);
    if (!point) return false;
    await b.send("Input.dispatchMouseEvent", { type: "mousePressed", button: "left", clickCount: 1, ...point });
    await b.send("Input.dispatchMouseEvent", { type: "mouseReleased", button: "left", clickCount: 1, ...point });
    return true;
  };
  const closeSheet = async () => {
    await b.evaluate("history.back()");
    return waitFor(b, '!document.querySelector(".tw-sheet")', 3000);
  };
  const measure = async () => b.evaluate(`(() => {
    const small = [], katexScripts = new Set();
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const n = walker.currentNode, e = n.parentElement;
      if (!n.data.trim() || !e || e.closest("script,style,.katex-mathml,[hidden]") || !e.checkVisibility({opacityProperty:true,visibilityProperty:true})) continue;
      const range = document.createRange(); range.selectNodeContents(n);
      if (![...range.getClientRects()].some(r => r.width && r.height)) continue;
      const size = parseFloat(getComputedStyle(e).fontSize);
      if (e.closest(".katex .msupsub,.katex .vlist .mtight")) { katexScripts.add(size); continue; }
      if (size < 13.95) small.push({tag:e.tagName, class:e.className.baseVal ?? e.className, size, text:n.data.trim().slice(0,60)});
    }
    const overflowElements=[...document.querySelectorAll("body *")].filter(e=>!e.closest(".katex-mathml,svg") && e.checkVisibility() && e.getBoundingClientRect().right>innerWidth+1).slice(0,6).map(e=>({tag:e.tagName,class:e.className,text:e.textContent.slice(0,40),right:e.getBoundingClientRect().right}));
    return {overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,viewport:{width:visualViewport.width,scale:visualViewport.scale},overflowElements,small,katexScriptSizes:[...katexScripts].sort((a,b)=>a-b)};
  })()`);
  try {
    await b.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
    for (const width of [390, 1440]) {
      const view = { width, pages: [], accepted: 0, hints: 0, numericRejected: 0, panels: [] };
      out.views.push(view);
      const checkPanel = async (name) => {
        const text = await measure();
        view.panels.push({ name, text });
        ok(!text.small.length && text.overflow <= 0, `${width}: ${name} text floor or overflow`);
      };
      await b.send("Emulation.setDeviceMetricsOverride", { width, height: width === 390 ? 844 : 900, deviceScaleFactor: 1, mobile: width === 390 });
      await goto(b, base + "learn/");
      await b.evaluate('Object.keys(localStorage).filter(k=>k.startsWith("tw-")).forEach(k=>localStorage.removeItem(k))');
      await goto(b, base + "learn/");
      ok(await waitFor(b, 'document.querySelectorAll(".tw-unit").length === 7'), `${width}: seven unit cards`);
      view.home = await b.evaluate('({continue:!!document.querySelector(".tw-continue"),stats:document.querySelectorAll(".tw-stats>div").length,units:document.querySelectorAll(".tw-unit").length})');
      ok(view.home.continue && view.home.stats === 3, `${width}: Continue and three stats`);
      view.home.text = await measure();
      ok(!view.home.text.small.length && view.home.text.overflow <= 0, `${width}: home text floor and overflow ${JSON.stringify(view.home.text)}`);
      for (const [index, lesson] of lessons.entries()) {
        const page = lesson.url;
        await goto(b, base + page);
        ok(await waitFor(b, '!!document.querySelector(".tw-answer input") && [...document.querySelectorAll(".tw-plot")].every(e=>e.querySelector("svg"))'), `${width} ${page}: reader ready`);
        await b.evaluate('document.querySelectorAll("details.tw-sol").forEach(e=>e.open=true)');
        const info = { page };
        view.pages.push(info);
        info.math = await b.evaluate('({errors:document.querySelectorAll(".katex-error").length,rendered:document.querySelectorAll(".katex").length,raw:document.querySelector("article").innerText.includes(String.fromCharCode(92)+"(")})');
        ok(info.math.errors === 0 && info.math.rendered > 0 && !info.math.raw, `${width} ${page}: formulas ${JSON.stringify(info.math)}`);
        info.plots = await b.evaluate('[...document.querySelectorAll(".tw-plot")].map(e=>({source:e.dataset.src,svgs:e.querySelectorAll("svg").length,points:e.querySelectorAll(".tw-plot__pts circle").length}))');
        ok(info.plots.every(plot=>plot.svgs === 1 && plot.points > 0), `${width} ${page}: populated plots ${JSON.stringify(info.plots)}`);
        if (lesson.id === "1.1") ok(info.plots.length === 2 && info.plots.every(plot=>plot.points>100), `${width} ${page}: both introductory plots exceed 100 points`);
        if (lesson.id === "1.2") ok(info.plots.length === 1 && info.plots[0].points>100, `${width} ${page}: percent plot exceeds 100 points`);
        if (lesson.id === "1.3") ok(info.plots.length === 2 && info.plots.every(plot=>plot.source === "u1-quiet-day-30" ? plot.points>=48 : plot.points>100), `${width} ${page}: both noise plots retain their point counts`);
        info.text = await measure();
        ok(!info.text.small.length && info.text.overflow <= 0, `${width} ${page}: text floor or horizontal overflow`);
        const problems = await b.evaluate('[...document.querySelectorAll(".tw-prob")].map(p=>({answers:p.dataset.answer.split("|"),hints:JSON.parse(p.dataset.hints||"{}") }))');
        for (const [number, problem] of problems.entries()) {
          const id = `#prob-${number + 1}`;
          const answer = async (value) => {
            await b.evaluate(`(() => { const i = document.querySelector(${JSON.stringify(id + ' input')}); i.focus({preventScroll:true}); i.value=""; })()`);
            await b.send("Input.insertText", { text: value });
            await click(id + " button");
            const feedback = await b.evaluate(`document.querySelector(${JSON.stringify(id + ' .tw-fb')}).textContent`);
            if (!feedback) {
              info.clickFailures ||= [];
              info.clickFailures.push(await b.evaluate(`(() => {const p=document.querySelector(${JSON.stringify(id)}),i=p.querySelector("input"),r=p.querySelector("button").getBoundingClientRect();return {problem:${number + 1},value:i.value,active:document.activeElement.tagName,button:{x:r.x,y:r.y,width:r.width,height:r.height},hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.outerHTML.slice(0,200),scrollY};})()`));
            }
            return feedback;
          };
          for (const [key, hint] of Object.entries(problem.hints)) {
            const feedback = await answer(key);
            view.hints++;
            ok(feedback.startsWith("Not yet.") && feedback.includes(hint), `${width} ${page} p${number + 1}: hint for ${key}, got ${feedback}`);
          }
          await answer("definitely incorrect");
          const pid = `${lesson.id}-p${number + 1}`;
          ok(await b.evaluate(`JSON.parse(localStorage.getItem("tw-due")||"[]").some(p=>p.pid===${JSON.stringify(pid)})`), `${width} ${page} p${number + 1}: wrong answer queued`);
          for (const value of problem.answers.filter(value=>value.trim() !== "" && Number.isFinite(Number(value)))) {
            const expected = Number(value);
            const wrong = expected === 0 ? 0.2 : expected * 1.2;
            const feedback = await answer(String(wrong));
            view.numericRejected++;
            ok(feedback.startsWith("Not yet."), `${width} ${page} p${number + 1}: 20% off ${wrong} rejected, got ${feedback}`);
          }
          for (const value of problem.answers) {
            const feedback = await answer(value);
            view.accepted++;
            ok(feedback.startsWith("Right"), `${width} ${page} p${number + 1}: answer ${value} got ${feedback}`);
          }
          ok(await b.evaluate(`!JSON.parse(localStorage.getItem("tw-due")||"[]").some(p=>p.pid===${JSON.stringify(pid)})`), `${width} ${page} p${number + 1}: right answer removed`);
        }
        info.feedbackText = await measure();
        ok(!info.feedbackText.small.length && info.feedbackText.overflow <= 0, `${width} ${page}: feedback and solutions text floor or overflow`);
        if (index !== 0) continue;
        await b.evaluate('document.querySelectorAll("details.tw-sol").forEach(e=>e.open=false);scrollTo(0,500)');
        await sleep(500);
        // Capture scroll after bringing the actual link into view, before opening it.
        await b.evaluate('document.querySelector(\'article a[href*="glossary/#"]\').scrollIntoView({block:"center"})');
        const before = await b.evaluate('scrollY');
        await click('article a[href*="glossary/#"]');
        ok(await waitFor(b, 'document.querySelectorAll(".tw-sheet").length===1'), `${width}: glossary opens one sheet`);
        await checkPanel("glossary");
        ok(await closeSheet(), `${width}: Back closes glossary`);
        view.glossaryScrollDelta = await b.evaluate(`Math.abs(scrollY-${before})`);
        ok(view.glossaryScrollDelta <= 2, `${width}: glossary changed scroll by ${view.glossaryScrollDelta}px`);
        await click('.tw-tools [data-a="toc"]');
        await waitFor(b, '!!document.querySelector(".tw-toc")');
        view.contents = await b.evaluate('(async()=>{const d=await (await fetch(new URL("assets/data/learn.json",'+JSON.stringify(base)+'))).json();const wanted=d.units.flatMap(u=>u.lessons).map(l=>l.id);const text=document.querySelector(".tw-toc").innerText;return {expected:wanted.length,missing:wanted.filter(id=>!text.includes(id+" "))};})()');
        ok(view.contents.missing.length === 0, `${width}: Contents missing lessons ${view.contents.missing}`);
        await checkPanel("Contents");
        await closeSheet();
        await b.evaluate(`(() => { const p=[...document.querySelectorAll("article>p")].find(p=>!p.closest(".tw-kicker,.tw-pn") && p.firstChild?.nodeType===3 && p.firstChild.length>30);p.scrollIntoView({block:"center",behavior:"instant"});const r=document.createRange();r.setStart(p.firstChild,0);r.setEnd(p.firstChild,25);getSelection().removeAllRanges();getSelection().addRange(r);document.dispatchEvent(new Event("selectionchange")); })()`);
        ok(await waitFor(b, '!!document.querySelector(".tw-pill:not([hidden])")'), `${width}: selection shows highlight pill`);
        await checkPanel("highlight pill");
        await click('.tw-pill [data-a="hl"]');
        ok(await b.evaluate('!!document.querySelector("mark.tw-hl")'), `${width}: Highlight paints mark`);
        await goto(b, base + page);
        ok(await waitFor(b, '!!document.querySelector("mark.tw-hl")'), `${width}: highlight survives reload`);
        await click('mark.tw-hl');
        ok(await waitFor(b, '!!document.querySelector("#tw-note")'), `${width}: note editor opens`);
        await checkPanel("note editor");
        await b.evaluate('document.querySelector("#tw-note").value="Twinlight local test note"');
        await click('.tw-sheet [data-a="save"]');
        await waitFor(b, '!document.querySelector(".tw-sheet")');
        await goto(b, base + page);
        ok(await waitFor(b, '!!document.querySelector("mark.tw-hl.has-note")'), `${width}: note highlight survives reload`);
        ok(await b.evaluate('Object.values(JSON.parse(localStorage.getItem("tw-hl")||"{}")).flat().some(h=>h.note==="Twinlight local test note")'), `${width}: note text survives reload`);
        await click('.tw-tools [data-a="listen"]');
        ok(await waitFor(b, '!!document.querySelector(".tw-sheet--listen")'), `${width}: Listen opens`);
        view.voices = await b.evaluate('({available:speechSynthesis.getVoices().filter(v=>/^en/i.test(v.lang)).map(v=>v.name),listed:[...document.querySelectorAll("#tw-voice option")].map(e=>e.textContent)})');
        ok(view.voices.available.every(v=>view.voices.listed.includes(v)), `${width}: Listen lists available English voices`);
        await checkPanel("Listen");
        await closeSheet();
        // Clear answer state before finishing to exercise unanswered-problem scheduling.
        await b.evaluate('localStorage.removeItem("tw-prob");localStorage.removeItem("tw-due");localStorage.removeItem("tw-done")');
        await goto(b, base + page);
        await waitFor(b, '!!document.querySelector(".tw-tools")');
        await b.evaluate('scrollTo(0,document.documentElement.scrollHeight)');
        await sleep(800);
        view.finished = await b.evaluate('({done:JSON.parse(localStorage.getItem("tw-done")||"{}"),due:JSON.parse(localStorage.getItem("tw-due")||"[]").length,problems:document.querySelectorAll(".tw-prob").length})');
        ok(!!view.finished.done[lesson.id] && view.finished.due === view.finished.problems, `${width}: finish marks read and queues unanswered problems ${JSON.stringify(view.finished)}`);
        await b.evaluate('localStorage.removeItem("tw-done");scrollTo(0,(document.documentElement.scrollHeight-innerHeight)*.5)');
        await sleep(700);
        view.savedFraction = await b.evaluate('JSON.parse(localStorage.getItem("tw-place")).y');
        await goto(b, base + "learn/");
        await waitFor(b, '!!document.querySelector(".tw-continue")');
        await click('.tw-continue');
        await waitFor(b, `!!document.querySelector(".tw-tools") && document.querySelectorAll(".tw-plot svg").length===${info.plots.length}`);
        await sleep(900);
        view.resumedFraction = await b.evaluate('scrollY/(document.documentElement.scrollHeight-innerHeight)');
        ok(Math.abs(view.savedFraction-view.resumedFraction) <= .1, `${width}: Continue fraction ${view.savedFraction} to ${view.resumedFraction}`);
      }
    }
    out.errors = b.errors;
    ok(!out.errors.length, 'console errors: ' + out.errors.join(' | '));
    out.pass = !out.fails.length;
  } finally { await b.close(); }
  return out;
}

async function treeTest() {
  const { createRequire } = await import("node:module");
  const require = createRequire(import.meta.url);
  process.env.PLAYWRIGHT_BROWSERS_PATH = path.resolve("data/tools/ms-playwright");
  const { chromium } = require(path.resolve("data/tools/playwright/node_modules/playwright"));
  const browser = await chromium.launch({ executablePath: CHROME, args: ["--no-sandbox"] });
  const out = { mode: "tree", checks: 0, fails: [], measurements: [], errors: [] };
  const check = (id, pass, evidence) => { out.checks++; out.measurements.push({id,pass:!!pass,evidence}); if (!pass) out.fails.push(id); };
  const ctx = await browser.newContext({ viewport:{width:1440,height:1000}, reducedMotion:"reduce", serviceWorkers:"block" });
  if (opt.baseline) await ctx.route(/\/assets\/(tree\.(js|css)|tour\.js)(\?.*)?$/, r => r.fulfill({path:path.resolve(opt.baseline,new URL(r.request().url()).pathname.split("/").at(-1))}));
  await ctx.addInitScript(() => { localStorage.setItem("ss-tour-3","done"); sessionStorage.setItem("ss-open","1"); localStorage.setItem("sst-view","mission"); });
  if (opt.mutate) await ctx.addInitScript(({kind}) => {
    addEventListener('DOMContentLoaded',()=>{
      const css = {
        layout: '.ssta-colL { grid-column:3 !important; }',
        phone: '.ssta-phcard { top:0 !important; }',
        gold: '.sst { --ssta-gold:#67bddd !important; --ssta-gold-2:#67bddd !important; --ssta-gold-dim:#67bddd !important; }',
        text: '.ssta-row { width:500px !important; }',
        wheel: '.sst-card { overflow-y:visible !important; overscroll-behavior:auto !important; }',
        journey: '.sst-day:nth-of-type(odd) { margin-left:30% !important; width:65% !important; }',
        contrast: '.sst { --ssta-gold:#777777 !important; }',
      }[kind];
      if(css){const style=document.createElement('style');style.textContent=css;document.head.append(style);}
      if(kind==='scroll')document.addEventListener('wheel',e=>{if(e.target.closest('.ssta-mission'))e.preventDefault();},{passive:false});
    });
  },{kind:opt.mutate});
  const page = await ctx.newPage();
  page.on("pageerror",e=>out.errors.push(e.message));
  const output = path.resolve(opt.output || "data/astra/020"); fs.mkdirSync(output,{recursive:true});
  const screenshot = name => page.screenshot({path:path.join(output,name+".png"),fullPage:false});
  try {
    await page.goto(base); await page.waitForSelector(".sst-view"); await page.waitForTimeout(500);
    const ready = await page.locator(".ssta-pc-cols").count() === 1;
    if (!ready) {
      for (const id of ["A1/pc-layout","A2/phone-layout","A3/golden-uniform","A4/text-fits","A5/normal-scroll","A6/panel-wheel","A7/journey-column","A8/gold-contrast"]) check(id,false,"Design A structure absent on baseline");
      out.pass=false; return out;
    }
    const pc = await page.evaluate(() => {
      const box=s=>document.querySelector(s).getBoundingClientRect();
      const l=box('.ssta-colL'),r=box('.ssta-colR'),d=box('.ssta-detail-slot'),g=box('.ssta-goal'),s=box('.ssta-score');
      return {left:[...document.querySelectorAll('.ssta-colL [data-branch]')].map(e=>e.dataset.branch),right:[...document.querySelectorAll('.ssta-colR [data-branch]')].map(e=>e.dataset.branch),goalBesideScore:g.right<=s.left+1,panelRight:d.left>r.right,branchGap:r.left-l.right};
    });
    check("A1/pc-layout",pc.left.join()==="1,4"&&pc.right.join()==="2,3"&&pc.goalBesideScore&&pc.panelRight&&pc.branchGap>0,pc);
    await page.locator('.ssta-row[data-node="1.1"]').click();
    await page.waitForSelector('.sst-card');
    check("A1/detail",await page.locator('.sst-card .ssta-metric').innerText().then(t=>t.includes('53 of 222')) && await page.locator('.sst-card').getByRole('heading',{name:'What it is',exact:true}).count()===1,await page.locator('.sst-card').innerText());
    const panel=await page.locator('.sst-card').evaluate(e=>({position:getComputedStyle(e).position,overflow:getComputedStyle(e).overflowY,contain:getComputedStyle(e).overscrollBehaviorY}));
    await page.locator('.sst-card').hover(); const before=await page.evaluate(()=>({y:scrollY,top:document.querySelector('.sst-card').scrollTop}));
    await page.mouse.wheel(0,500); await page.waitForTimeout(150);
    const after=await page.evaluate(()=>({y:scrollY,top:document.querySelector('.sst-card').scrollTop}));
    check("A6/panel-wheel",panel.position==='sticky'&&panel.overflow==='auto'&&panel.contain==='contain'&&before.y===after.y&&after.top>before.top,{panel,before,after});
    await page.keyboard.press('Escape'); await page.waitForTimeout(100);
    const ordinaryBefore=await page.evaluate(()=>scrollY); await page.mouse.move(600,500); await page.mouse.wheel(0,250); await page.waitForTimeout(150);
    check("A5/normal-scroll",await page.locator('[data-z],.sst-stage,canvas').count()===0&&await page.evaluate(()=>scrollY)>ordinaryBefore,{before:ordinaryBefore,after:await page.evaluate(()=>scrollY)});
    await page.evaluate(()=>scrollTo(0,0));
    for (const theme of ['slate','default']) {
      await page.evaluate(t=>document.body.dataset.mdColorScheme=t,theme);
      const gold=await page.evaluate(()=>{
        const paths=[...document.querySelectorAll('.ssta-vine path')];
        const strokes=[...new Set(paths.map(e=>getComputedStyle(e).stroke))];
        const colors=[...new Set([...document.querySelectorAll('.ssta-row .ssta-status')].map(e=>getComputedStyle(e).color))];
        const rgb=c=>{const x=document.createElement('canvas').getContext('2d');x.fillStyle=c;x.fillRect(0,0,1,1);return [...x.getImageData(0,0,1,1).data].slice(0,3);};
        const lum=c=>rgb(c).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((n,v,i)=>n+v*[.2126,.7152,.0722][i],0);
        const e=document.querySelector('.ssta-br-h .ssta-n'),s=getComputedStyle(e),bg=getComputedStyle(e.closest('.ssta-box')).backgroundColor,a=lum(s.color),b=lum(bg);
        return {strokes,colors,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),gold:rgb(s.color),paths:paths.length};
      });
      check(`A3/golden-uniform/${theme}`,gold.paths>10&&gold.colors.length===1&&gold.strokes.every(s=>{const n=s.match(/[\d.]+/g).map(Number);return n[0]>n[2]&&n[1]>n[2];}),gold);
      check(`A8/gold-contrast/${theme}`,gold.ratio>=4.5,gold.ratio);
      await page.goto(base+'#n=1.1'); await page.waitForSelector('.sst-card'); await page.waitForTimeout(100);
      await screenshot('design-a-pc-'+theme);
      await page.keyboard.press('Escape'); await page.waitForTimeout(100);
    }
    // Use the release gate's composited contrast measurement, including opacity.
    const { MEASURE: releaseMeasure } = await import('./gates_measure.mjs');
    await page.setViewportSize({width:1280,height:1000});
    for (const theme of ['slate','default']) {
      await page.evaluate(value=>document.body.dataset.mdColorScheme=value,theme);
      const measured = await page.evaluate(releaseMeasure(1280));
      const low = measured.low.filter(item=>!item.header);
      check(`A8/desktop-text/${theme}`, low.length===0, low);
    }
    for (const width of [900,1024,1440]) {
      await page.setViewportSize({width,height:1000}); await page.waitForTimeout(100);
      const overflow=await page.locator('.ssta-row,.ssta-br-h,.ssta-chip,.ssta-goal,.ssta-score').evaluateAll(es=>es.filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent));
      check(`A4/text-fits/${width}`,!overflow.length&&await page.evaluate(w=>document.documentElement.scrollWidth<=w,width),overflow);
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.locator('[data-view="journey"]').click();
    const journey=await page.locator('.sst-journey').evaluate(e=>{
      const days=[...e.querySelectorAll('.sst-day')],positions=days.map(d=>d.getBoundingClientRect().left),dates=days.map(d=>d.dataset.date);
      const vine=parseFloat(getComputedStyle(e,'::before').left)+e.getBoundingClientRect().left;
      return {positions,dates,clear:days.every(d=>d.getBoundingClientRect().left+parseFloat(getComputedStyle(d).paddingLeft)>vine+2)};
    });
    check('A7/journey-column',journey.positions.length>1&&new Set(journey.positions).size===1&&journey.clear&&journey.dates.every((d,i,a)=>!i||a[i-1]>=d),journey);
    await screenshot('design-a-journey');
    await page.locator('[data-view="mission"]').click();
    await page.setViewportSize({width:390,height:844}); await page.waitForTimeout(150);
    const phone=await page.locator('.ssta-phtree').evaluate(e=>{const c=[...e.querySelectorAll('.ssta-phcard')].map(e=>({id:e.dataset.pb,x:e.offsetLeft,y:e.offsetTop,b:e.offsetTop+e.offsetHeight}));return {c,overlap:c.some((v,i)=>i&&v.y<c[i-1].b)};});
    check('A2/phone-layout',phone.c.map(c=>c.id).join()==='1,2,3,4'&&phone.c[0].x<phone.c[1].x&&phone.c[2].x<phone.c[3].x&&phone.c.every((c,i,a)=>!i||c.y>a[i-1].y)&&phone.overlap,phone);
    await page.evaluate(()=>scrollTo(0,0)); await screenshot('design-a-phone');
    await page.locator('[data-pb="4"]').click();
    check('A2/chosen-list',await page.locator('.ssta-phrows .ssta-row[data-node="4.1"]').count()===1,'branch 4 rows');
    await page.locator('.ssta-phrows .ssta-row').first().click(); await page.waitForSelector('.sst-sheet'); await screenshot('design-a-phone-sheet');
    const locked=await page.evaluate(()=>getComputedStyle(document.body).position==='fixed'); await page.locator('.sst-x').focus();await page.keyboard.press('Shift+Tab');
    check('keep/focus-lock',locked&&await page.evaluate(()=>!!document.activeElement.closest('.sst-sheet')),locked);
    await page.goBack();await page.waitForTimeout(100);await page.goForward();await page.waitForSelector('.sst-sheet');
    check('keep/history',await page.locator('.sst-sheet').count()===1,'Back and Forward');
    await page.setViewportSize({width:1440,height:1000});await page.waitForTimeout(150);
    check('keep/resize',await page.locator('.sst-sheet').count()===0&&await page.locator('.sst-card').count()===1,'sheet to panel');
    await page.keyboard.press('Escape');
    const input=page.locator('.sst-search input');await input.fill('zzzzunmatchable');await input.press('Enter');
    check('keep/no-matches',await page.locator('.sst-results').isVisible(),'unmatched Enter');
    await input.fill('1.4');await input.press('Enter');await page.waitForSelector('.sst-card');
    check('keep/search-enter',(await page.locator('.sst-card .ssta-crumb').innerText()).includes('1.4'),'node search');
    await page.keyboard.press('Escape');await input.fill('');await input.press('Escape');
    // A long translated title must grow the normal HTML box.
    await page.locator('.ssta-row .ssta-t').first().evaluate(e=>e.textContent='A longer title with several extra words '.repeat(8));
    check('A4/long-title',await page.locator('.ssta-row').first().evaluate(e=>e.scrollHeight<=e.clientHeight+1&&e.scrollWidth<=e.clientWidth+1),'content-sized row');
    for(const width of [320,390,900,1440]) {
      await page.setViewportSize({width,height:844});await page.waitForTimeout(120);
      const targets=await page.locator('#ss-tree button,#ss-tree a[href]').evaluateAll(es=>es.filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect();return {t:e.textContent.trim().slice(0,40),w:r.width,h:r.height};}).filter(r=>r.w<43.9||r.h<43.9));
      check(`keep/targets/${width}`,targets.length===0,targets);
    }
    const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(base);
    check('keep/static',await staticPage.locator('.sst-static').isVisible(),'JavaScript disabled');await nojs.close();
    check('script-errors',!out.errors.length,out.errors);out.pass=!out.fails.length;return out;
  } catch(e) {out.error=String(e);out.pass=false;return out;} finally {await ctx.close();await browser.close();}
}

async function repairsTest() {
  const { createRequire } = await import("node:module");
  const require = createRequire(import.meta.url);
  process.env.PLAYWRIGHT_BROWSERS_PATH = path.resolve("data/tools/ms-playwright");
  const pw = require(path.resolve("data/tools/playwright/node_modules/playwright"));
  const engine = opt.engine || "chromium";
  const browser = await pw[engine].launch(engine === "chromium" ? { executablePath: CHROME, args: ["--no-sandbox"] } : {});
  const out = { mode: "repairs", engine, checks: 0, fails: [], measurements: [] };
  out.scriptErrors = [];
  const check = (id, pass, evidence) => {
    out.checks++;
    out.measurements.push({ id, pass: !!pass, evidence });
    if (!pass) out.fails.push(id);
  };
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: "reduce", serviceWorkers: "block" });
  ctx.on("page", p => p.on("pageerror", error => out.scriptErrors.push(error.message)));
  const baseline = async context => {
    if (opt.baseline) await context.route(/\/assets\/(tree\.(js|css)|tour\.js|learn\.(js|css))(\?.*)?$/, route => route.fulfill({ path: path.resolve(opt.baseline, new URL(route.request().url()).pathname.split("/").at(-1)) }));
  };
  await baseline(ctx);
  await ctx.addInitScript(() => {
    localStorage.setItem("ss-tour-3", "done");
    window.resizeRegistrations = 0;
    const add = window.addEventListener;
    window.addEventListener = function(type, ...args) {
      if (type === "resize") window.resizeRegistrations++;
      return add.call(this, type, ...args);
    };
  });
  const page = await ctx.newPage();
  const load = async (url = "") => {
    await page.goto(base + url);
    await page.waitForSelector(url.startsWith("learn/u") ? ".tw-answer" : url === "learn/" ? ".tw-unit" : ".sst-view");
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(350);
  };
  const answer = async (url, expected, value, id, right) => {
    await load(url);
    const p = page.locator(`.tw-prob[data-answer="${expected}"]`).first();
    await p.locator("input").fill(value);
    await p.locator("form").evaluate(f => f.requestSubmit());
    check(id, await p.evaluate((e, r) => e.classList.contains(r ? "is-right" : "is-wrong"), right), value);
  };
  const contrast = async selector => page.locator(selector).first().evaluate(e => {
    const canvas = document.createElement("canvas"); canvas.width = canvas.height = 1;
    const ctx = canvas.getContext("2d");
    const rgba = color => {
      ctx.clearRect(0,0,1,1); ctx.fillStyle = color; ctx.fillRect(0,0,1,1);
      return [...ctx.getImageData(0,0,1,1).data];
    };
    const luminance = rgb => rgb.map(v => {
      v /= 255;
      return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
    }).reduce((sum,v,i) => sum + v * [.2126,.7152,.0722][i], 0);
    const chain = [];
    for (let n=e;n;n=n.parentElement) chain.unshift(n);
    let background = [255,255,255], opacity = 1;
    for (const n of chain) {
      const style = getComputedStyle(n), color = rgba(style.backgroundColor);
      opacity *= +style.opacity;
      const alpha = color[3] / 255 * opacity;
      background = background.map((v,i)=>color[i]*alpha+v*(1-alpha));
    }
    const color = rgba(getComputedStyle(e).color), alpha = opacity*color[3]/255;
    const foreground = background.map((v,i)=>color[i]*alpha+v*(1-alpha));
    const a=luminance(foreground), b=luminance(background);
    return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  });
  try {
    if (opt["contrast-only"]) {
      for (const width of [320,390]) {
        await page.setViewportSize({width,height:844});
        for (const theme of ["default","slate"]) {
          for (const [url, selectors] of [["",[".ssta-row .ssta-id"]],["learn/",[".tw-unit.is-soon small",".tw-unit.is-soon li"]],["learn/u1/l1-a-light-curve/",[".tw-pn small"]]]) {
            await load(url); await page.evaluate(t=>document.body.dataset.mdColorScheme=t,theme);
            for (const selector of selectors) {
              const ratio=await contrast(selector);
              check(`M-21/${width}/${theme}/${selector}`,ratio>=4.5,ratio);
            }
          }
        }
      }
      out.pass = out.fails.length === 0;
      return out;
    }
    for (const width of [320, 390]) {
      await page.setViewportSize({ width, height: width === 320 ? 568 : 844 });
      await load();
      const position = await page.locator(".sst-bar").evaluate(e => getComputedStyle(e).position);
      check(`M-03/${width}`, position === "static" || position === "relative", position);
      const search = page.locator(".sst-search input");
      await search.fill("zzzzunmatchable"); await search.press("Enter"); await page.waitForTimeout(500);
      check(`M-17/empty/${width}`, await page.getByText("No matches", { exact: true }).isVisible(), "unmatched query");
      const title = await page.locator(".sst-item .t").first().innerText();
      await search.fill(title.split("\n")[0].trim()); await search.press("Enter"); await page.waitForTimeout(600);
      check(`M-17/enter/${width}`, await page.locator(".sst-sheet").count() === 1, title);
      // Open directly as well, so the modal check survives a broken search.
      if (!await page.locator(".sst-sheet").count()) await page.locator(".sst-item").first().click();
      await page.screenshot({path:path.resolve(opt.output || "data/astra/019",`${engine}-sheet-${width}.png`)});
      const locked = await page.evaluate(() => ({ pos: getComputedStyle(document.body).position, overflow: getComputedStyle(document.body).overflow }));
      await page.locator(".sst-sheet .sst-x").focus();
      await page.keyboard.press("Shift+Tab");
      const trapped = await page.evaluate(() => !!document.activeElement.closest(".sst-sheet"));
      check(`M-11/tree/${width}`, trapped && (locked.pos === "fixed" || locked.overflow === "hidden"), { trapped, locked });
      const closeSize = await page.locator(".sst-sheet .sst-x").boundingBox();
      check(`M-16/tree-close/${width}`, closeSize.width >= 44 && closeSize.height >= 44, closeSize);
      await page.goBack(); await page.waitForTimeout(350);
      await page.goForward(); await page.waitForTimeout(350);
      check(`M-13/${width}`, await page.locator(".sst-sheet").count() === 1, "Back then Forward");
      if (!await page.locator(".sst-sheet").count()) await page.locator(".sst-item").first().click();
      await page.setViewportSize({ width: 1280, height: 800 }); await page.waitForTimeout(450);
      check(`M-14/${width}`, await page.locator(".sst-sheet").count() === 0 && await page.locator(".sst-card").count() === 1, "phone to PC");
      for (const theme of ["default", "slate"]) {
        await page.setViewportSize({ width, height: 844 }); await load();
        await page.evaluate(t => document.body.dataset.mdColorScheme = t, theme);
        const ratio = await contrast(".ssta-row .ssta-id");
        check(`M-21/tree/${width}/${theme}`, ratio >= 4.5, ratio);
        await page.screenshot({path:path.resolve(opt.output || "data/astra/019",`${engine}-tree-${width}-${theme}.png`)});
      }
      await load("learn/u1/l1-a-light-curve/");
      const inputMode = await page.locator('.tw-prob[data-answer="-35.8"] input').getAttribute("inputmode");
      check(`M-05/${width}`, inputMode === "text", inputMode);
      const tools = await page.locator(".tw-tools > *, .tw-pn a").evaluateAll(es => es.map(e => { const r = e.getBoundingClientRect(); return [r.width,r.height]; }));
      check(`M-16/learn/${width}`, tools.every(([w,h]) => w >= 44 && h >= 44), tools);
      await page.locator('.tw-tools [data-a="toc"]').click(); await page.waitForTimeout(250);
      await page.locator(".tw-x").focus(); await page.keyboard.press("Shift+Tab");
      check(`M-11/learn/${width}`, await page.evaluate(() => !!document.activeElement.closest(".tw-sheet")), "Shift+Tab from Close");
      await page.goBack(); await page.waitForTimeout(300);
      await page.evaluate(()=>scrollTo(0,1000)); await page.waitForTimeout(500);
      const placeBeforeSheet = await page.evaluate(()=>JSON.parse(localStorage.getItem("tw-place")));
      await page.locator('.tw-tools [data-a="toc"]').click(); await page.waitForTimeout(550);
      const placeInSheet = await page.evaluate(()=>JSON.parse(localStorage.getItem("tw-place")));
      check(`M-11/place/${width}`, placeInSheet.y === placeBeforeSheet.y, {before:placeBeforeSheet.y,during:placeInSheet.y});
      await page.goBack(); await page.waitForTimeout(300);
      await page.evaluate(() => { scrollTo(0,0); dispatchEvent(new Event("scroll")); }); await page.waitForTimeout(100);
      await page.evaluate(() => { scrollTo(0,500); dispatchEvent(new Event("scroll")); }); await page.waitForTimeout(100);
      await page.evaluate(() => { scrollBy(0,1); dispatchEvent(new Event("scroll")); });
      check(`M-30/${width}`, await page.evaluate(() => document.documentElement.classList.contains("tw-hide")), "down 500 then down 1");
      // Select text, then deliberately wait after focus collapses the selection.
      await page.evaluate(() => {
        scrollTo(0,0);
        const p = [...document.querySelectorAll("article > p")].find(e => !e.closest(".tw-kicker,.tw-pn") && e.firstChild?.nodeType === 3 && e.firstChild.length > 15);
        const r = document.createRange(); r.setStart(p.firstChild,0); r.setEnd(p.firstChild,12);
        getSelection().removeAllRanges(); getSelection().addRange(r); document.dispatchEvent(new Event("selectionchange"));
      });
      await page.waitForTimeout(350);
      await page.locator('.tw-pill [data-a="note"]').click();
      await page.locator("#tw-note").fill("Regression note");
      await page.waitForTimeout(450);
      await page.locator('[data-a="save"]').click(); await page.waitForTimeout(300);
      const notes = await page.evaluate(() => Object.values(JSON.parse(localStorage.getItem("tw-hl") || "{}")).flat().filter(n => n.note === "Regression note").length);
      check(`M-07/${width}`, notes > 0, notes);
      await page.reload(); await page.waitForSelector(".tw-answer"); await page.waitForTimeout(400);
      check(`M-07/reload/${width}`, await page.locator("mark.tw-hl.has-note").count() > 0, "highlight survives reload");
      await page.evaluate(() => scrollTo(0,1800)); await page.waitForTimeout(650);
      const savedY = await page.evaluate(() => scrollY);
      await load("learn/"); await page.locator(".tw-continue").click(); await page.waitForSelector(".tw-answer"); await page.waitForTimeout(1000);
      const resumedY = await page.evaluate(() => scrollY);
      check(`M-12/${width}`, Math.abs(savedY-resumedY) <= 5, { savedY, resumedY });
      for (const theme of ["default", "slate"]) {
        await page.evaluate(t => document.body.dataset.mdColorScheme = t, theme);
        const ratio = await contrast(".tw-pn small"); check(`M-21/next/${width}/${theme}`, ratio >= 4.5, ratio);
        await load("learn/"); await page.evaluate(t => document.body.dataset.mdColorScheme = t, theme);
        const coming = await contrast(".tw-unit.is-soon small"), unit = await contrast(".tw-unit.is-soon li");
        check(`M-21/coming/${width}/${theme}`, Math.min(coming,unit) >= 4.5, { coming,unit });
        await page.screenshot({path:path.resolve(opt.output || "data/astra/019",`${engine}-learn-${width}-${theme}.png`)});
        await load("learn/u1/l1-a-light-curve/");
      }
    }
    await page.setViewportSize({width:844,height:390}); await load();
    await page.evaluate(()=>scrollTo(0,500));
    const barBottom = await page.locator(".sst-bar").evaluate(e=>e.getBoundingClientRect().bottom);
    check("M-03/landscape", barBottom < 0, barBottom);
    await answer("learn/u1/l2-percent-and-ppm/", "2500", "2500%", "M-08", false);
    await answer("learn/u2/l1-orbits-and-periods/", "0.90", "0,90", "M-09", true);
    await answer("learn/u2/l1-orbits-and-periods/", "0.90", "0,900", "decimals/zero", true);
    await answer("learn/u2/l1-orbits-and-periods/", "0.90", "0.9 AU", "M-22/AU", true);
    await answer("learn/u2/l2-how-long-a-dip-lasts/", "2.62", "2.62 hours", "M-22/hours", true);
    await answer("learn/u1/l1-a-light-curve/", "-35.8", "\u221235.8", "M-22/minus", true);
    await answer("learn/u1/l2-percent-and-ppm/", "2500", "2,500 ppm", "units/grouped", true);
    await answer("learn/u1/l2-percent-and-ppm/", "0.03", "0.03%", "units/percent", true);
    await answer("learn/u2/l1-orbits-and-periods/", "0.90", "0.9 hours", "units/wrong", false);
    // Old saves contain only the fractional position. Compare after the asynchronous plots and fonts finish.
    await load("learn/");
    await page.evaluate(() => {
      const url = new URL("u1/l1-a-light-curve/",location.href).pathname;
      localStorage.setItem("tw-place", JSON.stringify({id:"1.1",title:"A light curve",url,y:.3}));
    });
    await page.reload(); await page.locator(".tw-continue").click();
    await page.waitForSelector(".tw-tools"); await page.waitForTimeout(500);
    const legacy = await page.evaluate(() => ({actual:scrollY,expected:.3*(document.documentElement.scrollHeight-innerHeight)}));
    check("M-12/legacy", Math.abs(legacy.actual-legacy.expected)<=5, legacy);
    await page.setViewportSize({ width: 1280, height: 800 }); await load();
    await page.evaluate(() => document.querySelector('[data-view="mission"]').click());
    const registrations = await page.evaluate(() => window.resizeRegistrations);
    for (let i=0;i<4;i++) { await page.locator('[data-view="journey"]').click(); await page.locator('[data-view="mission"]').click(); }
    const afterRegistrations = await page.evaluate(() => window.resizeRegistrations);
    check("M-15/listeners", afterRegistrations === registrations, { registrations, afterRegistrations });
    // The old zoom, fit and SVG-label checks are replaced by the design-A
    // layout, normal scrolling, dynamic text and panel-wheel checks in tree mode.
    const rows = await page.locator('.ssta-row').evaluateAll(es => es.map(e => {
      const r=e.getBoundingClientRect();return {w:r.width,h:r.height,overflow:e.scrollWidth-e.clientWidth};
    }));
    check("M-18/html-labels", rows.length>0 && rows.every(r=>r.overflow<=1), rows);
    check("M-20/normal-page", await page.locator('[data-z],.sst-stage').count()===0, "ordinary page scroll");
    await page.locator('.ssta-row[data-node="1.4"]').click();
    const panelStyle = await page.locator('.sst-card').evaluate(element => {
      const before = element.scrollTop, pageBefore = scrollY;
      const wheel = new WheelEvent('wheel', { deltaY: 80, bubbles: true, cancelable: true });
      element.dispatchEvent(wheel);
      const manual = element.dataset.wheelContain === 'manual' && wheel.defaultPrevented && scrollY === pageBefore && (element.scrollTop > before || element.scrollHeight <= element.clientHeight);
      return { position:getComputedStyle(element).position, overflow:getComputedStyle(element).overflowY, contain:getComputedStyle(element).overscrollBehaviorY, manual };
    });
    check("M-19/mission",panelStyle.position==='sticky'&&panelStyle.overflow==='auto'&&(panelStyle.contain==='contain'||panelStyle.manual),panelStyle);
    await page.keyboard.press('Escape');
    await page.locator('[data-view="journey"]').click();await page.locator('.sst-day button').first().click();
    check("M-19/journey",await page.locator('.sst-card').evaluate(e=>getComputedStyle(e).position==='sticky'),"sticky journey panel");
    await page.keyboard.press('Escape');
    await page.evaluate(() => localStorage.setItem("sst-last-visit", "2000")); await load();
    const oldVisit = await page.evaluate(() => localStorage.getItem("sst-last-visit")); await page.waitForTimeout(4200);
    check("M-31/unread", await page.evaluate(() => localStorage.getItem("sst-last-visit")) === oldVisit, "unread visit after 4.2 seconds");
    await page.locator(".sst-new").click();
    check("M-31/explicit", await page.getByRole("button", { name: "Mark updates read", exact: true }).count() === 1, "explicit acknowledgement");
    if (await page.getByRole("button", { name: "Mark updates read", exact: true }).count()) {
      await page.getByRole("button", { name: "Mark updates read", exact: true }).click();
      check("M-31/read", await page.locator(".sst-new").count() === 0, "acknowledgement clears badge");
    }
    await page.screenshot({ path: path.resolve(opt.output || "data/astra/019", `${engine}-tree.png`) });
    const tourCtx = await browser.newContext({ viewport:{width:390,height:844},isMobile:true,hasTouch:true,serviceWorkers:"block" });
    tourCtx.on("page", p => p.on("pageerror", error => out.scriptErrors.push(error.message)));
    await baseline(tourCtx);
    // Exercise the baseline's hidden tour too, without changing production code.
    await tourCtx.addInitScript(() => Object.defineProperty(navigator,"webdriver",{get:()=>false}));
    const tour = await tourCtx.newPage(); await tour.goto(base+"?tour=1");
    await tour.waitForSelector(".ss-tour.is-in", {timeout:10000});
    check("M-23/version", !(await tour.locator(".ss-tour").innerText()).includes("Book 3.0"), "welcome copy");
    await tour.locator(".ss-tour__next").click();
    await tour.waitForTimeout(1250);
    const modal = await tour.locator(".ss-tour").getAttribute("aria-modal");
    const lock = await tour.evaluate(() => getComputedStyle(document.body).position === "fixed");
    check("M-04", modal === "true" && lock, {modal,lock});
    const ringError = await tour.evaluate(() => {
      const ring=document.querySelector(".ss-tour__ring").getBoundingClientRect(),target=document.querySelector(".ssta-phcard").getBoundingClientRect();
      return Math.max(Math.abs(ring.left-target.left+6),Math.abs(ring.top-target.top+6));
    });
    if (engine === "webkit") await tour.evaluate(()=>scrollBy(0,500));
    else await tour.mouse.wheel(0,500);
    await tour.waitForTimeout(150);
    const pageY = await tour.evaluate(()=>scrollY);
    check("M-04/position", ringError <= 1 && pageY === 0, {ringError,pageY});
    await tour.screenshot({path:path.resolve(opt.output || "data/astra/019",`${engine}-tour.png`)});
    await tour.locator(".ss-tour__next").click(); await tour.locator(".ss-tour__skip").click(); await tour.waitForTimeout(900);
    check("M-06", await tour.locator(".ss-tour__ring").count() === 0, "skip during ring delay");
    await tour.goto(base+"?tour=1"); await tour.waitForSelector(".ss-tour.is-in");
    for(let i=0;i<3;i++) await tour.locator(".ss-tour__next").click();
    check("M-23/menu-copy", (await tour.locator(".ss-tour").innerText()).includes("menu at the top left"), "step four");
    await tour.locator(".ss-tour__next").click(); await tour.waitForTimeout(350);
    await tour.locator('.md-header label[for="__drawer"]').click();
    check("M-23/menu", await tour.locator('.md-sidebar--primary a[href*="learn"]').first().isVisible(), "menu opens after tour");
    await tourCtx.close();
    check("script-errors", out.scriptErrors.length === 0, out.scriptErrors);
    out.pass = out.fails.length === 0;
    return out;
  } catch (error) {
    out.pass = false; out.error = String(error);
    return out;
  } finally { await ctx.close(); await browser.close(); }
}

const modes = { repairs: repairsTest, learn: learnTest, tree: treeTest, hammer, shots, layout, chapter: chapterLayout, eyeslayout: eyesLayout, offline: offlineTest, fail404, update, jsoff, redirect, images, eyes: eyesTest, eyescloud: eyesCloudTest, eyesreal: eyesReal, rehearsal: rehearsalTest, rehearsalcloud: rehearsalCloudTest, watchtimers: watchTimersTest, headertitle: headerTitleTest, textfloor: textFloorTest };
try {
  const r = await modes[mode]();
  console.log(JSON.stringify(r));
  process.exit(r.pass ? 0 : 1);
} catch (e) {
  console.log(JSON.stringify({ mode, pass: false, error: String(e && e.stack || e).slice(0, 500) }));
  process.exit(1);
}
