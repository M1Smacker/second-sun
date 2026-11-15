"""Historical, one-shot migration used for brief 016. Final checks are in 016-run.mjs.

The migration was followed by review-driven edits. Refuse a second application
to protect those edits. This file records the transformation originally run.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
target = ROOT / 'research/burn-3-book/tools/site_check.mjs'
s = target.read_text(encoding='utf-8')
if 'async function treeTest()' in s:
    raise SystemExit('Already migrated. Run node research/astra/scripts/016-run.mjs to verify.')
s = s.replace('import { spawn, execFileSync }', 'import { spawn }')
s = re.sub(r'const PAGES = .*?;', '''const PAGES = ["", "learn/", "shelf/", "training/", "candidates/", "eyes/", "rehearsal/", "glossary/", "claims/", "field-notes/", "field-notes/2026-11-14/", "watch/", "versions/", "labs/lab3-plot-and-read/", "reference/for-astronomers/"];''', s, count=1)
s = s.replace('const profile = `D:/second-sun/.cache/cdp-${tag}-${process.pid}`;', '''const profile = path.resolve(opt.profiles || "data/astra/016/profiles", `cdp-${tag}-${process.pid}`);
  fs.mkdirSync(path.dirname(profile), { recursive: true });''')
start = s.index('// F4 (27 Oct 2026)')
end = s.index('async function offlineTest()', start)
s = s[:start] + '''// Book 2's chapter template was removed from Book 3.
async function chapterLayout() {
  const reason = "Book 3 removed the chapter rail, margin-note sweep, chapter strip and fixed chapter-column template. General layout remains covered by layout.";
  console.log("RETIRED chapter: " + reason);
  return { mode: "chapter", status: "RETIRED", reason, pass: true, checks: 0 };
}

''' + s[end:]
s = s.replace('base + "learn/l1-dip-depth/"', 'base + "training/"')
s = s.replace('["", "candidates/", "glossary/", "claims/", "book/14-credit-and-publishing/", "learn/l1-dip-depth/"]', '["", "candidates/", "glossary/", "claims/", "shelf/", "training/"]')
# The former slider belongs to the retired lesson. Tree toolbar transitions exercise current motion.
s = s.replace('await goto(b, base + "training/");\n    await sleep(300);\n    out.reducedMotion', 'await goto(b, base);\n    await waitFor(b, `!!document.querySelector(".sst-seg button")`);\n    out.reducedMotion', 1)
s = s.replace('await goto(b, base + "training/");\n    await sleep(300);\n    out.normalMotion', 'await goto(b, base);\n    await waitFor(b, `!!document.querySelector(".sst-seg button")`);\n    out.normalMotion', 1)
s = s.replace('slider: getComputedStyle(document.querySelector(".ss-demo__lc span")).transitionDuration', 'toolbar: getComputedStyle(document.querySelector(".sst-seg button")).transitionDuration')
s = s.replace('out.reducedMotion.body === "0s" && out.reducedMotion.content === "none" && out.reducedMotion.slider === "0s"', 'out.reducedMotion.body.split(",").every((t) => parseFloat(t) <= 0.001) && (out.reducedMotion.content === "none" || parseFloat(out.reducedMotion.contentDuration) <= 0.001) && out.reducedMotion.toolbar.split(",").every((t) => parseFloat(t) <= 0.001)')
s = s.replace('content: getComputedStyle(document.querySelector(".md-content__inner")).animationName, toolbar:', 'content: getComputedStyle(document.querySelector(".md-content__inner")).animationName, contentDuration: getComputedStyle(document.querySelector(".md-content__inner")).animationDuration, toolbar:')
s = s.replace('    out.demo = await b.evaluate(`(() => { const r = document.querySelector(\'[name="rp"]\'); r.value = 11; r.dispatchEvent(new Event("input")); return document.querySelector(".ss-demo__result").textContent; })()`);', '''    console.log("RETIRED offline slider: the Book 2 dip-depth demo has no Book 3 page. Offline Tree interaction is checked instead.");
    await goto(b, base);
    out.treeReady = await waitFor(b, `document.querySelectorAll(".sst-node").length >= 20`);
    out.treeOffline = await b.evaluate(`(() => { document.querySelector('[data-view="journey"]').click(); return document.querySelectorAll(".sst-phase").length > 0 && document.querySelectorAll(".sst-day").length > 0; })()`);''')
s = s.replace('/1\\.0[0-9]%/.test(out.demo)', 'out.treeReady && out.treeOffline')
start = s.index('  const index = path.join(opt.proto')
end = s.index('  try {\n    await goto(b, base);', start)
s = s[:start] + '''  // Mutate only the disposable built copy. No source page or rebuild is needed.
  const index = path.join(opt.site, "index.html"), worker = path.join(opt.site, "sw.js");
  const original = fs.readFileSync(index, "utf8"), originalWorker = fs.readFileSync(worker, "utf8");
  const shells = () => b.evaluate(`caches.keys().then((k) => k.filter((x) => x.startsWith("ss-shell-")).sort())`);
  const publish = (letter) => {
    const version = Buffer.from(`book3-test-${letter}`).toString("hex");
    fs.writeFileSync(index, original.replace("</article>", `<p>Update test marker: version ${letter}.</p></article>`));
    fs.writeFileSync(worker, originalWorker.replace(/const VERSION = "[0-9a-f]+"/, `const VERSION = "${version}"`));
    return "ss-shell-" + version;
  };
''' + s[end:]
s = s.replace('    build();\n    await b.close();', '    fs.writeFileSync(worker, originalWorker);\n    await b.close();')
start = s.index('async function jsoff()')
end = s.index('async function redirect()', start)
s = s[:start] + '''async function jsoff() {
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
    out.staticTree = await b.evaluate(`document.querySelector(".sst-static").innerText.length > 100 && document.querySelectorAll(".sst-static a[href]").length > 0`);
    await goto(b, base + "eyes/");
    out.details = await b.evaluate(`(() => { const d = document.querySelector("details"); if (!d) return { exists: false }; const before = d.open; d.querySelector("summary").click(); return { exists: true, before, after: d.open, text: d.innerText.length }; })()`);
    out.errors = b.errors.filter((e) => !/serviceWorker|sw\\.js/.test(e));
    out.pass = !out.fails.length && out.staticTree && out.details.exists && out.details.before !== out.details.after && out.details.text > 50 && !out.errors.length;
  } finally { await b.close(); }
  return out;
}

''' + s[end:]
s = s.replace('["book/02-light-curves/", "book/10-vetting/", "field-notes/2026-11-02/"]', '["shelf/", "reference/for-astronomers/", "field-notes/2026-11-14/"]')
s = s.replace('["l1-390-dark", 390, "slate", "learn/l1-dip-depth/", null], ["l1-quiz-open-390-dark", 390, "slate", "learn/l1-dip-depth/", "quiz"]', '["training-390-dark", 390, "slate", "training/", null], ["eyes-details-390-dark", 390, "slate", "eyes/", "details"]')
s = s.replace('"chapter-1280-', '"shelf-1280-').replace('"book/14-credit-and-publishing/"', '"shelf/"').replace('"progress-1280-dark", 1280, "slate", "progress/"', '"journey-1280-dark", 1280, "slate", "", "journey"')
s = s.replace('if (action === "quiz")', 'if (action === "details")').replace('document.querySelector("details.quiz")', 'document.querySelector("details")')
s = s.replace('      const shot = await b.send', '''      if (action === "journey") {
        await waitFor(b, `!!document.querySelector('[data-view="journey"]')`);
        await b.evaluate(`document.querySelector('[data-view="journey"]').click()`);
      }
      const shot = await b.send''')
s = s.replace('const modes = { hammer,', 'const modes = { tree: treeTest, hammer,')
target.write_text(s, encoding='utf-8', newline='\n')
publish = ROOT / 'research/burn-3-book/tools/publish_book.ps1'
p = publish.read_text(encoding='utf-8').replace('"layout", "chapter", "eyeslayout"', '"layout", "tree", "eyeslayout"')
publish.write_text(p, encoding='utf-8', newline='\n')
print('Migrated browser checks and publish mode list.')
